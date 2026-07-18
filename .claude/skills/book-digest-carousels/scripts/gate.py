#!/usr/bin/env python3
"""Completion gate: only clear to send the next batch when the current one is done.

Reads the "Current batch" checklist in TRACKER.md. If any item is still unchecked
(`- [ ]`), the user hasn't finished the current batch, so we HOLD. If every item is
checked (`- [x]`) or the list is empty, we're CLEAR to produce and send the next batch.

Writes `send=true|false` to $GITHUB_OUTPUT (for the workflow) and prints a summary.

Usage:
    python gate.py --tracker TRACKER.md
"""
import argparse
import os
import re
import sys

SECTION = "Current batch"


def read_batch(tracker_text):
    """Return list of (checked: bool, label: str) under the Current batch heading."""
    lines = tracker_text.splitlines()
    items, in_section = [], False
    for ln in lines:
        if ln.lstrip().startswith("#") and SECTION.lower() in ln.lower():
            in_section = True
            continue
        if in_section and ln.lstrip().startswith("#"):
            break  # next heading ends the section
        if in_section:
            m = re.match(r"\s*-\s*\[([ xX])\]\s*(.*)", ln)
            if m:
                items.append((m.group(1).lower() == "x", m.group(2).strip()))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tracker", default="TRACKER.md")
    args = ap.parse_args()

    text = open(args.tracker, encoding="utf-8").read() if os.path.exists(args.tracker) else ""
    items = read_batch(text)
    pending = [lbl for done, lbl in items if not done]
    send = len(pending) == 0

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"send={'true' if send else 'false'}\n")

    if send:
        print(f"CLEAR: current batch fully checked ({len(items)} item(s)). Sending next batch.")
    else:
        print(f"HOLD: {len(pending)} item(s) still unchecked. Waiting for you to finish:")
        for p in pending:
            print(f"   - {p}")
    sys.exit(0)


if __name__ == "__main__":
    main()
