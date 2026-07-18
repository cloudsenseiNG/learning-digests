#!/usr/bin/env python3
"""Rebuild the digest library index page (docs/index.html) from a manifest.

The daily run appends an entry to docs/digests.json, then calls this to regenerate
the landing page. The library is ADDITIVE: digests are never removed here, only
listed. Entries are grouped into a section per track/book and ordered by chapter
within each, so the page reads like a growing syllabus you can reference any time.

manifest entry: {"slug","book","ch","title","date"}

Usage:
    python build_index.py --docs docs
"""
import argparse
import json
import os
import re
from collections import defaultdict

C = dict(bg="#0A0A0B", card="#0E0E10", line="rgba(242,239,233,0.10)",
         ink="#F2EFE9", body="#C9C7C1", mut="#7A7A80", red="#C8453A")

# Preferred display order for the tracks. Any book not listed here is appended
# afterwards in alphabetical order, so a new track still shows up automatically.
TRACK_ORDER = [
    "Designing Data-Intensive Applications",
    "AI Engineering",
    "High Performance MySQL",
    "AWS",
]


def chap_num(ch):
    """First integer in the chapter/topic label ('Ch.2 (Part 1 of 2)' -> 2)."""
    m = re.search(r"\d+", ch or "")
    return int(m.group()) if m else 9999


def part_num(ch):
    """Part number if the label splits a chapter ('Part 1 of 2' -> 1), else 0."""
    m = re.search(r"[Pp]art\s+(\d+)", ch or "")
    return int(m.group(1)) if m else 0


def card(d):
    return (f'<a href="digests/{d["slug"]}.html" style="display:block;text-decoration:none;'
            f'background:{C["card"]};border:1px solid {C["line"]};border-radius:12px;padding:18px 20px;margin:12px 0">'
            f'<div style="font-family:\'JetBrains Mono\',monospace;color:{C["red"]};font-size:12px;letter-spacing:2px">{d["book"]} · {d["ch"]}</div>'
            f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:700;color:{C["ink"]};font-size:22px;margin:6px 0 2px">{d["title"]}</div>'
            f'<div style="color:{C["mut"]};font-size:13px;font-family:\'JetBrains Mono\',monospace">{d.get("date","")} · read →</div></a>')


def section(book, entries):
    entries = sorted(entries, key=lambda d: (chap_num(d.get("ch", "")), part_num(d.get("ch", "")), d.get("date", "")))
    head = (f'<h2 style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:800;color:{C["ink"]};'
            f'font-size:24px;margin:34px 0 2px;padding-top:18px;border-top:1px solid {C["line"]}">{book}</h2>'
            f'<div style="color:{C["mut"]};font-size:13px;font-family:\'JetBrains Mono\',monospace;margin-bottom:8px">'
            f'{len(entries)} digest(s)</div>')
    return head + "".join(card(d) for d in entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    args = ap.parse_args()

    manifest = os.path.join(args.docs, "digests.json")
    items = json.load(open(manifest)) if os.path.exists(manifest) else []

    groups = defaultdict(list)
    for d in items:
        groups[d.get("book", "Other")].append(d)
    ordered = [b for b in TRACK_ORDER if b in groups] + sorted(b for b in groups if b not in TRACK_ORDER)
    body = "".join(section(b, groups[b]) for b in ordered)
    if not items:
        body = (f'<p style="color:{C["mut"]};font-size:15px">No digests yet. The next scheduled run '
                f'will publish Chapter 1 for each track here.</p>')

    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Learning digests</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Inter:wght@400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"></head>
<body style="margin:0;background:{C['bg']};font-family:Inter,-apple-system,sans-serif;color:{C['body']}">
<div style="max-width:720px;margin:0 auto;padding:40px 22px">
<div style="font-family:'JetBrains Mono',monospace;color:{C['red']};font-size:13px;letter-spacing:3px">~/mayowa/learning</div>
<h1 style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;color:{C['ink']};font-size:38px;margin:8px 0 4px">Learning digests</h1>
<p style="color:{C['mut']};font-size:16px;margin:0 0 6px">A growing library, one chapter at a time. Grouped by track, in reading order.</p>
{body}
</div></body></html>'''
    os.makedirs(args.docs, exist_ok=True)
    open(os.path.join(args.docs, "index.html"), "w").write(html)
    print(f"index rebuilt with {len(items)} digest(s) across {len(groups)} track(s)")


if __name__ == "__main__":
    main()
