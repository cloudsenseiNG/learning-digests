#!/usr/bin/env python3
"""Lint generated carousel decks against the content guardrails.

The guardrails in SKILL.md / references/carousels.md are prose the agent is *asked* to
follow. This script *checks* them, so a slip is caught before you post rather than after.

Reads every `<carousels>/<book>/<slug>/deck.json` and checks:

  1. Book tells      - words that reveal a book/course sits behind the post
                       ("chapter", "the book", "the author", ...)          -> ERROR
  2. Structure       - 7-10 slides, exactly one `code` visual-proof slide,
                       cover first and close last, and counters that run
                       01/N .. N/N over the non-cover slides (the cover is an
                       unnumbered title card, so a final `07 / 08` is a bug) -> ERROR
  3. Fixed chrome    - `terminal` path and cover `counter` prefix match the
                       track, so they never drift between chapters         -> ERROR
  4. Unbounded absolutes - "always/never/only/every/must/guarantees" with no
                       nearby boundary word ("usually", "by default", ...)  -> WARNING

Absolutes are only warnings on purpose: some are legitimately true ("Every MySQL table
runs on two stacked layers"), so a human decides. Tells and structure are objective.

Exit code is 1 if any ERROR was found, else 0. Wire it into CI with
`continue-on-error: true` so findings are loud but never cost an already-generated batch.

Usage:
    python lint_carousels.py --carousels build/carousels
"""
import argparse
import glob
import json
import os
import re
import sys

# Track folder -> (expected terminal, expected counter prefix). Mirrors the
# "Fixed per-track chrome" table in references/carousels.md.
TRACKS = {
    "DDIA": ("~/learning/systems", "SYSTEMS"),
    "AI-Engineering": ("~/learning/ai", "AI"),
    "High-Performance-MySQL": ("~/learning/sql", "SQL"),
    "AWS": ("~/learning/aws", "AWS"),
}

# Unambiguous source tells. Deliberately excludes bare "page(s)"/"reading"/"text",
# which are ordinary database words ("page cache", "reading from a replica", TEXT column).
TELLS = [
    r"\bchapters?\b", r"\bthe book\b", r"\bthis book\b", r"\bthe author\b",
    r"\bthe course\b", r"\bthe material\b", r"\bCh\.\s*\d", r"\bpp?\.\s*\d",
    r"\bpages?\s+\d+\b",
]
# Context-dependent: usually innocent in a DB/AI context, so warn only.
SOFT_TELLS = [r"\bre-?read(ing)?\b", r"\bthe text\b"]

ABSOLUTES = [r"\balways\b", r"\bnever\b", r"\bonly\b", r"\bevery\b", r"\beverything\b",
             r"\bmust\b", r"\bcan'?t\b", r"\bcannot\b", r"\bguarantees?\b", r"\bguaranteed\b"]
# Any of these in the same field neutralises an absolute.
BOUNDARIES = [r"\busually\b", r"\btypically\b", r"\bmost\b", r"\bby default\b", r"\bdefault\b",
              r"\bcommon(ly)?\b", r"\boften\b", r"\bgenerally\b", r"\btends? to\b",
              r"\bin practice\b", r"\bfor beginners\b", r"\bthis architecture\b",
              r"\bthis setup\b", r"\broughly\b", r"\babout\b", r"\baround\b", r"\bmay\b"]

CHROME_FIELDS = {"terminal", "counter", "handle", "tags"}


def hits(patterns, text):
    return sorted({m.group(0) for p in patterns for m in re.finditer(p, text, re.I)})


def lint_deck(path, root, errors, warnings):
    # Human-readable "<book>/<slug>" for the report; full path kept for CI annotations.
    rel = os.path.dirname(os.path.relpath(path, start=root))
    try:
        deck = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        errors.append((rel, f"deck.json is not valid JSON: {e}"))
        return
    slides = deck.get("slides") or []

    # --- 3. structure -----------------------------------------------------
    n = len(slides)
    if not 7 <= n <= 10:
        errors.append((rel, f"{n} slides (must be 7-10)"))
    templates = [s.get("template") for s in slides]
    n_code = templates.count("code")
    if n_code != 1:
        errors.append((rel, f"{n_code} `code` visual-proof slides (must be exactly 1)"))
    if templates and templates[0] != "cover":
        errors.append((rel, f"first slide is `{templates[0]}` (must be `cover`)"))
    if templates and templates[-1] != "close":
        errors.append((rel, f"last slide is `{templates[-1]}` (must be `close`)"))

    # --- counters ---------------------------------------------------------
    # The cover is an unnumbered title card, so TOTAL counts only the non-cover
    # slides and the final slide must read N/N (never "07 / 08").
    body_slides = slides[1:]
    k = len(body_slides)
    for pos, s in enumerate(body_slides, 1):
        counter = (s.get("fields") or {}).get("counter", "")
        if not counter:
            continue
        m = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", counter)
        if not m:
            errors.append((rel, f"slide {pos + 1}: counter `{counter}` (must be `NN / {k:02d}`)"))
            continue
        num, den = int(m.group(1)), int(m.group(2))
        if den != k:
            errors.append((rel, f"slide {pos + 1}: counter `{counter}` has total {den}, "
                                f"but there are {k} non-cover slides (cover is not counted)"))
        if num != pos:
            errors.append((rel, f"slide {pos + 1}: counter `{counter}` is out of sequence "
                                f"(expected {pos:02d})"))

    # --- 4. fixed chrome --------------------------------------------------
    book = os.path.basename(os.path.dirname(os.path.dirname(path)))
    if book in TRACKS:
        want_term, want_prefix = TRACKS[book]
        for i, s in enumerate(slides, 1):
            term = (s.get("fields") or {}).get("terminal")
            if term and term != want_term:
                errors.append((rel, f"slide {i}: terminal `{term}` (must be `{want_term}`)"))
        cover = (slides[0].get("fields") or {}) if slides else {}
        counter = cover.get("counter", "")
        if counter and not counter.upper().startswith(want_prefix):
            errors.append((rel, f"cover counter `{counter}` (must start with `{want_prefix}`)"))
    else:
        warnings.append((rel, f"unknown track folder `{book}`, skipped chrome check"))

    # --- 1/2. copy checks -------------------------------------------------
    for i, s in enumerate(slides, 1):
        for field, val in (s.get("fields") or {}).items():
            if field in CHROME_FIELDS or not isinstance(val, str):
                continue
            found = hits(TELLS, val)
            if found:
                errors.append((rel, f"slide {i} `{field}`: book tell {found}"))
            soft = hits(SOFT_TELLS, val)
            if soft:
                warnings.append((rel, f"slide {i} `{field}`: possible tell {soft}"))
            if field == "code":
                continue  # schematic art, not prose
            abs_found = hits(ABSOLUTES, val)
            if abs_found and not hits(BOUNDARIES, val):
                warnings.append((rel, f"slide {i} `{field}`: unbounded absolute {abs_found} "
                                      f"- true generally, or only in a common setup?"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--carousels", default="build/carousels")
    ap.add_argument("--report", default="",
                    help="write the findings to this file, for the auto-fix pass to read")
    args = ap.parse_args()

    decks = sorted(glob.glob(os.path.join(args.carousels, "*", "*", "deck.json")))
    if not decks:
        print(f"lint: no deck.json found under {args.carousels}, nothing to check")
        return 0

    errors, warnings = [], []
    for d in decks:
        lint_deck(d, args.carousels, errors, warnings)

    ci = os.environ.get("GITHUB_ACTIONS") == "true"
    print(f"lint: checked {len(decks)} deck(s)\n")
    for where, msg in warnings:
        print(f"  WARN  {where}: {msg}")
        if ci:
            print(f"::warning::{where}: {msg}")
    for where, msg in errors:
        print(f"  ERROR {where}: {msg}")
        if ci:
            print(f"::error::{where}: {msg}")

    print(f"\nlint: {len(errors)} error(s), {len(warnings)} warning(s)")

    # A report the auto-fix pass can read, and a flag the workflow can branch on.
    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            for where, msg in errors:
                f.write(f"ERROR {where}: {msg}\n")
            for where, msg in warnings:
                f.write(f"WARN  {where}: {msg}\n")
        print(f"lint: report written to {args.report}")

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"errors={len(errors)}\n")
            f.write(f"warnings={len(warnings)}\n")
            f.write(f"has_errors={'true' if errors else 'false'}\n")

    if errors:
        print("lint: the auto-fix pass will try to clear these.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
