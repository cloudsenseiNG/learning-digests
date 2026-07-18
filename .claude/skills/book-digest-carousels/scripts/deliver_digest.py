#!/usr/bin/env python3
"""Send a digest as an email over SMTP.

Supports two inputs:
  * .html  -> sent as a rich HTML email. Because Gmail and most clients strip
              inline <svg> and block data: image URIs, this script automatically
              rasterizes each inline <svg> to PNG and converts data:image URIs
              into real attached images referenced by CID, so schematics show up
              everywhere. Subject comes from <title> or the first <h1>.
  * .md    -> sent as plain text. First line `Subject: ...` becomes the subject.

SMTP settings and recipient come from environment variables so nothing sensitive
lives in the repo:
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, DIGEST_TO   (SMTP_FROM optional)

For Gmail: SMTP_HOST=smtp.gmail.com, SMTP_PORT=587, SMTP_PASS = a Google App
Password (requires 2-Step Verification).

Usage:
    python deliver_digest.py --file output/digests/ddia_ch01_digest.html

Deps for HTML with schematics: pip install cairosvg
"""
import argparse
import base64
import glob
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage


def send(subject, from_addr, to_addr, text=None, html=None, images=None, attachments=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(text or "This digest is best viewed as HTML.")
    if html is not None:
        msg.add_alternative(html, subtype="html")
        if images:
            payload = msg.get_payload()[-1]  # the html part
            for cid, data in images.items():
                payload.add_related(data, maintype="image", subtype="png", cid=f"<{cid}>")
    for path in (attachments or []):
        with open(path, "rb") as fh:
            data = fh.read()
        name = os.path.basename(path)
        sub = "zip" if name.lower().endswith(".zip") else "octet-stream"
        msg.add_attachment(data, maintype="application", subtype=sub, filename=name)

    ctx = ssl.create_default_context()
    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587"))) as s:
        s.starttls(context=ctx)
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        s.send_message(msg)


def build_html(path):
    """Return (subject, html, images) with inline svg/data-uris turned into CID images."""
    html = open(path, encoding="utf-8").read()
    images = {}

    subject = "Daily digest"
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I) or re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if m:
        subject = re.sub(r"<[^>]+>", "", m.group(1)).strip()

    # inline <svg>...</svg> -> PNG attachment
    try:
        import cairosvg
        def svg_repl(mo):
            cid = f"fig{len(images)}"
            images[cid] = cairosvg.svg2png(bytestring=mo.group(0).encode(), output_width=1200)
            return f'<img src="cid:{cid}" style="width:100%;max-width:620px;display:block;margin:0 auto">'
        html = re.sub(r"<svg\b.*?</svg>", svg_repl, html, flags=re.S | re.I)
    except Exception as e:
        print(f"warning: could not rasterize inline SVG ({e}); sending as-is", file=sys.stderr)

    # data:image/...;base64,XXXX in <img src> -> attachment
    def data_repl(mo):
        cid = f"fig{len(images)}"
        try:
            images[cid] = base64.b64decode(mo.group(1))
        except Exception:
            return mo.group(0)
        return f'src="cid:{cid}"'
    html = re.sub(r'src="data:image/[^;]+;base64,([^"]+)"', data_repl, html)

    return subject, html, images


def load_md(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    subject, body = "Daily digest", text
    if lines and lines[0].lower().startswith("subject:"):
        subject = lines[0].split(":", 1)[1].strip()
        body = "\n".join(lines[1:]).strip()
    return subject, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="path or glob to the digest (.html or .md)")
    ap.add_argument("--attach", action="append", default=[],
                    help="file(s) to attach, e.g. a carousels zip (repeatable, glob ok)")
    args = ap.parse_args()

    attachments = []
    for pat in args.attach:
        attachments.extend(sorted(glob.glob(pat)))

    matches = sorted(glob.glob(args.file))
    if not matches:
        sys.exit(f"No digest file matched: {args.file}")
    path = matches[-1]

    from_addr = os.environ.get("SMTP_FROM", os.environ["SMTP_USER"])
    to_addr = os.environ["DIGEST_TO"]

    if path.lower().endswith((".html", ".htm")):
        subject, html, images = build_html(path)
        send(subject, from_addr, to_addr, html=html, images=images, attachments=attachments)
        print(f"Sent HTML '{subject}' to {to_addr} with {len(images)} image(s), {len(attachments)} attachment(s)")
    else:
        subject, body = load_md(path)
        send(subject, from_addr, to_addr, text=body, attachments=attachments)
        print(f"Sent '{subject}' to {to_addr} with {len(attachments)} attachment(s)")


if __name__ == "__main__":
    main()
