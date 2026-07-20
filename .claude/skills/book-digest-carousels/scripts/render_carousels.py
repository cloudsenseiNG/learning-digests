#!/usr/bin/env python3
"""Fill text into editable SVG carousel templates and rasterize to PNG.

Templates are normal SVGs (your design) where each dynamic text lives in a
<text> element carrying data-* attributes and a {{field}} token, e.g.:

  <text data-field="title" x="80" y="560" data-box-w="920" data-max-lines="4"
        data-size="96" data-min-size="52" data-line-height="1.06" data-align="left"
        font-family="Space Grotesk" font-weight="700" fill="#F2EFE9">{{title}}</text>

The renderer word-wraps the value to data-box-w, shrinks the font from data-size
down to data-min-size until it fits data-max-lines, emits <tspan> lines, then
rasterizes with cairosvg. Code fields (data-pre="true") keep their own line breaks.

Input deck (content JSON):
  { "slides": [ { "template": "cover", "fields": { "title": "..." } }, ... ] }

Usage:
  python render_carousels.py --templates assets/templates --fonts fonts.json \
      --content deck.json --out ./out --width 1080 --height 1350

Deps: pip install cairosvg pillow   (+ the template fonts installed via fontconfig)
"""
import argparse
import json
import os
import re
import sys
import html

from PIL import ImageFont
import cairosvg

TEXT_RE = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.DOTALL)
ATTR_RE = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')


def parse_attrs(s):
    return dict(ATTR_RE.findall(s))


def load_font_map(path):
    """Load fonts.json, resolving its TTF paths **relative to the json file itself**.

    The values in fonts.json are relative (`assets/fonts/X.ttf`). Resolving them against
    the current working directory means running the renderer from anywhere but the skill
    directory silently loses every font: PIL then measures with a tiny default bitmap
    font, wrap_words concludes long headings fit on one line, and the rendered text
    overflows the canvas (cairosvg still draws the real font via fontconfig, so the
    output looks correctly typefaced but is unwrapped). Anchor to the file instead.
    """
    here = os.path.dirname(os.path.abspath(path))
    # fonts.json lives in assets/ but its paths are written relative to the skill root
    # ("assets/fonts/X.ttf"), so try the file's own dir, its parent, and plain cwd.
    bases = [here, os.path.dirname(here), os.getcwd()]
    raw = json.load(open(path, encoding="utf-8"))
    resolved, missing = {}, []
    for key, val in raw.items():
        if os.path.isabs(val):
            candidates = [val]
        else:
            candidates = [os.path.join(b, val) for b in bases]
        p = next((c for c in candidates if os.path.exists(c)), candidates[0])
        resolved[key] = p
        if not os.path.exists(p):
            missing.append(f"{key} -> {val}")
    if missing:
        sys.exit("render: these fonts in %s could not be found:\n  %s\n"
                 "Text measurement would silently fall back and overflow the slides."
                 % (path, "\n  ".join(missing)))
    return resolved


def load_font(font_map, family, weight, size):
    weight = "700" if str(weight) == "bold" else str(weight)
    for key in (f"{family}|{weight}", family):
        path = font_map.get(key)
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception as e:
                sys.exit(f"render: could not open font {path} for {family}|{weight}: {e}")
    # Never fall back silently: a default bitmap font measures far narrower than the real
    # face, so the shrink-to-fit and wrapping logic would produce overflowing slides.
    sys.exit(f"render: no font mapped for `{family}` weight `{weight}`. "
             f"Add it to fonts.json (known keys: {sorted(font_map)}).")


def measure(font, text):
    return font.getlength(text)


def wrap_words(font, text, max_w):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            trial = (cur + " " + w).strip()
            if not cur or measure(font, trial) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def build_tspans(attrs, value, font_map):
    x = float(attrs.get("x", 0))
    size = int(float(attrs.get("data-size", 48)))
    min_size = int(float(attrs.get("data-min-size", max(18, size // 3))))
    box_w = float(attrs.get("data-box-w", 900))
    max_lines = int(float(attrs.get("data-max-lines", 6)))
    lh = float(attrs.get("data-line-height", 1.2))
    align = attrs.get("data-align", "left")
    family = attrs.get("font-family", "Space Grotesk")
    weight = attrs.get("font-weight", "400")
    pre = attrs.get("data-pre", "false") == "true"

    # Shrink to fit.
    chosen, lines = size, None
    for s in range(size, min_size - 1, -2):
        font = load_font(font_map, family, weight, s)
        ls = value.split("\n") if pre else wrap_words(font, value, box_w)
        if len(ls) <= max_lines:
            chosen, lines = s, ls
            break
    if lines is None:
        font = load_font(font_map, family, weight, min_size)
        chosen = min_size
        lines = (value.split("\n") if pre else wrap_words(font, value, box_w))[:max_lines]

    anchor = {"left": "start", "center": "middle", "right": "end"}[align]
    line_px = int(chosen * lh)

    # Rebuild the <text> element with clean presentation attrs + tspans.
    keep = ["x", "y", "fill", "font-family", "font-weight", "letter-spacing", "opacity"]
    parts = [f'{k}="{attrs[k]}"' for k in keep if k in attrs]
    parts.append(f'font-size="{chosen}"')
    parts.append(f'text-anchor="{anchor}"')
    if pre:
        parts.append('xml:space="preserve"')
    head = "<text " + " ".join(parts) + ">"
    spans = []
    for i, line in enumerate(lines):
        dy = "0" if i == 0 else str(line_px)
        spans.append(f'<tspan x="{x}" dy="{dy}">{html.escape(line) or " "}</tspan>')
    return head + "".join(spans) + "</text>"


def render_slide(svg_text, fields, font_map):
    def repl(m):
        attrs = parse_attrs(m.group(1))
        field = attrs.get("data-field")
        if not field:
            return m.group(0)
        value = str(fields.get(field, "")).strip()
        if not value:
            return ""  # drop empty optional fields
        return build_tspans(attrs, value, font_map)
    return TEXT_RE.sub(repl, svg_text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--templates", required=True, help="dir with <template>.svg files")
    ap.add_argument("--fonts", required=True, help="JSON map: family -> ttf path")
    ap.add_argument("--content", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    args = ap.parse_args()

    font_map = load_font_map(args.fonts)
    deck = json.load(open(args.content))
    os.makedirs(args.out, exist_ok=True)

    paths = []
    for i, slide in enumerate(deck["slides"], 1):
        tpl_path = os.path.join(args.templates, slide["template"] + ".svg")
        svg_text = open(tpl_path).read()
        filled = render_slide(svg_text, slide.get("fields", {}), font_map)
        png = os.path.join(args.out, f"slide_{i:02d}.png")
        cairosvg.svg2png(bytestring=filled.encode("utf-8"), write_to=png,
                         output_width=args.width, output_height=args.height)
        paths.append(png)
    print(json.dumps({"rendered": paths, "count": len(paths)}, indent=2))


if __name__ == "__main__":
    main()
