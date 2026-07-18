#!/usr/bin/env python3
"""Build the batch's link email (build/email.html) deterministically.

Why a script and not the agent: email clients (Gmail especially) strip <style>
blocks, ignore CSS variables/flex/grid, and only show images that are embedded.
Hand-authored email HTML renders inconsistently. This builder emits a Gmail-safe
email: table layout, fully inline styles, web-safe font stack, and the logo embedded
as a data: URI (deliver_digest.py turns that into a CID attachment so it always shows).

It reads docs/digests.json, takes the entries from the most recent date (the batch that
was just produced), and renders one card per digest linking to the hosted page.

Usage:
    python build_email.py --docs docs --site-base-url "$SITE_BASE_URL" \
        --logo .claude/skills/book-digest-carousels/assets/brand/logo.png \
        --out build/email.html
"""
import argparse
import base64
import io
import json
import os
import re

C = dict(bg="#0A0A0B", card="#0E0E10", line="#26262A",
         ink="#F2EFE9", body="#C9C7C1", mut="#7A7A80", red="#C8453A")
MONO = "'JetBrains Mono', Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

TRACK_ORDER = [
    "Designing Data-Intensive Applications",
    "AI Engineering",
    "High Performance MySQL",
    "AWS",
]


def chap_num(ch):
    m = re.search(r"\d+", ch or "")
    return int(m.group()) if m else 9999


def part_num(ch):
    m = re.search(r"[Pp]art\s+(\d+)", ch or "")
    return int(m.group(1)) if m else 0


def logo_data_uri(path, px=96):
    """Return a data: URI for the logo, downscaled to px if Pillow is available."""
    if not path or not os.path.exists(path):
        return None
    raw = open(path, "rb").read()
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
        im.thumbnail((px, px))
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        raw = buf.getvalue()
    except Exception:
        pass  # embed original; deliver_digest still CID-attaches it
    return "data:image/png;base64," + base64.b64encode(raw).decode()


def button(href, label):
    # Bulletproof table button so it renders in Outlook/Gmail alike.
    return (
        f'<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin:14px 0 2px">'
        f'<tr><td align="center" bgcolor="{C["red"]}" style="border-radius:8px">'
        f'<a href="{href}" style="display:inline-block;padding:11px 20px;font-family:{SANS};font-size:14px;'
        f'font-weight:700;color:#ffffff;text-decoration:none;border-radius:8px">{label}</a>'
        f'</td></tr></table>'
    )


def card(d, base):
    href = f'{base}/digests/{d["slug"]}.html'
    eyebrow = f'{d.get("book","")} &middot; {d.get("ch","")}'.strip(" &middot;")
    return (
        f'<tr><td style="padding:0 0 14px">'
        f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" '
        f'style="background:{C["card"]};border:1px solid {C["line"]};border-radius:12px">'
        f'<tr><td style="padding:18px 20px">'
        f'<div style="font-family:{MONO};color:{C["red"]};font-size:12px;letter-spacing:2px">{eyebrow}</div>'
        f'<div style="font-family:{SANS};font-weight:700;color:{C["ink"]};font-size:20px;line-height:1.3;margin:6px 0 2px">{d.get("title","")}</div>'
        f'{button(href, "Read the digest &rarr;")}'
        f'</td></tr></table>'
        f'</td></tr>'
    )


def build(items, base, logo_uri):
    n = len(items)
    subject = f'{n} new digests are up' if n != 1 else f'New digest: {items[0]["title"]}'
    items = sorted(items, key=lambda d: (
        TRACK_ORDER.index(d["book"]) if d.get("book") in TRACK_ORDER else 99,
        chap_num(d.get("ch", "")), part_num(d.get("ch", "")),
    ))
    logo_html = (f'<img src="{logo_uri}" width="48" height="48" alt="" '
                 f'style="display:block;border-radius:10px" />') if logo_uri else ""
    cards = "".join(card(d, base) for d in items)
    return subject, f'''<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{subject}</title></head>
<body style="margin:0;padding:0;background:{C['bg']};">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:{C['bg']}">
<tr><td align="center" style="padding:28px 16px">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:600px;max-width:100%">
  <tr><td style="padding:0 4px 18px">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0"><tr>
      <td style="padding-right:12px">{logo_html}</td>
      <td style="font-family:{MONO};color:{C['red']};font-size:12px;letter-spacing:3px">~/mayowa/learning</td>
    </tr></table>
  </td></tr>
  <tr><td style="padding:0 4px 6px;font-family:{SANS};font-weight:800;color:{C['ink']};font-size:26px">{subject}</td></tr>
  <tr><td style="padding:0 4px 18px;font-family:{SANS};color:{C['mut']};font-size:15px;line-height:1.5">
    Fresh from today's batch. Each links to the full digest with schematics and a "Try it yourself" section, and the carousels are attached as a zip (foldered per book).
  </td></tr>
  <tr><td><table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">{cards}</table></td></tr>
  <tr><td style="padding:10px 4px 0;border-top:1px solid {C['line']};font-family:{MONO};color:{C['mut']};font-size:12px">
    Tick each in TRACKER.md once you've studied it &mdash; the next batch only ships when this one is done.
  </td></tr>
</table>
</td></tr></table>
</body></html>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--site-base-url", default=os.environ.get("SITE_BASE_URL", ""))
    ap.add_argument("--logo", default="")
    ap.add_argument("--out", default="build/email.html")
    args = ap.parse_args()

    manifest = os.path.join(args.docs, "digests.json")
    items = json.load(open(manifest)) if os.path.exists(manifest) else []
    if items:
        latest = max(d.get("date", "") for d in items)
        batch = [d for d in items if d.get("date", "") == latest]
    else:
        batch = []

    base = (args.site_base_url or "").rstrip("/")
    subject, html = build(batch, base, logo_data_uri(args.logo))
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    open(args.out, "w", encoding="utf-8").write(html)
    print(f"email built: {len(batch)} digest(s), subject={subject!r} -> {args.out}")


if __name__ == "__main__":
    main()
