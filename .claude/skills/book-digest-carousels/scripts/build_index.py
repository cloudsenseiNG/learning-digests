#!/usr/bin/env python3
"""Rebuild the digest library index page (docs/index.html) from a manifest.

The daily run appends an entry to docs/digests.json, then calls this to regenerate
the landing page that lists every digest, newest first. GitHub Pages serves docs/.

manifest entry: {"slug","book","ch","title","date"}

Usage:
    python build_index.py --docs docs
"""
import argparse
import json
import os

C = dict(bg="#0A0A0B", card="#0E0E10", line="rgba(242,239,233,0.10)",
         ink="#F2EFE9", body="#C9C7C1", mut="#7A7A80", red="#C8453A")


def card(d):
    return (f'<a href="digests/{d["slug"]}.html" style="display:block;text-decoration:none;'
            f'background:{C["card"]};border:1px solid {C["line"]};border-radius:12px;padding:18px 20px;margin:12px 0">'
            f'<div style="font-family:\'JetBrains Mono\',monospace;color:{C["red"]};font-size:12px;letter-spacing:2px">{d["book"]} · {d["ch"]}</div>'
            f'<div style="font-family:\'Bricolage Grotesque\',sans-serif;font-weight:700;color:{C["ink"]};font-size:22px;margin:6px 0 2px">{d["title"]}</div>'
            f'<div style="color:{C["mut"]};font-size:13px;font-family:\'JetBrains Mono\',monospace">{d.get("date","")} · read →</div></a>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    args = ap.parse_args()

    manifest = os.path.join(args.docs, "digests.json")
    items = json.load(open(manifest)) if os.path.exists(manifest) else []
    items = sorted(items, key=lambda d: d.get("date", ""), reverse=True)

    html = f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Learning digests</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Inter:wght@400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"></head>
<body style="margin:0;background:{C['bg']};font-family:Inter,-apple-system,sans-serif;color:{C['body']}">
<div style="max-width:720px;margin:0 auto;padding:40px 22px">
<div style="font-family:'JetBrains Mono',monospace;color:{C['red']};font-size:13px;letter-spacing:3px">~/mayowa/learning</div>
<h1 style="font-family:'Bricolage Grotesque',sans-serif;font-weight:800;color:{C['ink']};font-size:38px;margin:8px 0 4px">Learning digests</h1>
<p style="color:{C['mut']};font-size:16px;margin:0 0 26px">One chapter at a time. Systems design, and AWS beyond the basics.</p>
{''.join(card(d) for d in items)}
</div></body></html>'''
    os.makedirs(args.docs, exist_ok=True)
    open(os.path.join(args.docs, "index.html"), "w").write(html)
    print(f"index rebuilt with {len(items)} digest(s)")


if __name__ == "__main__":
    main()
