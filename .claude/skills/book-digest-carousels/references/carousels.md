# Carousels: voice, copy rules + editable SVG templates

A carousel is a short, scannable visual thread — not the digest. Each carousel
takes **one idea** from a chapter and makes it land, in the user's own design.

## Voice

Write as a **fellow learner**, not a guru. The user is learning these concepts too
and wants to help others get them. So: plain English, relatable, "here's the thing
that finally made this click for me", never lecturing or jargon-as-branding. Define
terms the moment they appear. Warmth and honesty ("this one tripped me up") beat
authority.

**Sound human, not generated.** No em dashes (use commas, periods, or parentheses).
Skip "it's not X, it's Y" phrasing and forced rule-of-three lists. Contractions and
short fragments are good. **Don't name the source book on the slides** (chrome stays
topic-based like "SYSTEMS · 01"); the concepts are common knowledge in your own words,
so there's nothing to attribute. Just never copy the source's exact wording.

## Length

**4–8 slides, matched to complexity.** A simple idea is a tight 4; a meatier one can
run to 8. Err on the shorter side — it should never feel overwhelming. Structure:
**cover (hook) → concept/code slides (one idea each) → close (takeaway + CTA)**.

- Slide 1 hooks: a promise, a surprising number, or "I kept getting this wrong."
- One thought per slide. Short lines. No paragraphs — this is glanceable.
- Use a `code` slide only when a snippet or concrete example carries the point.
- Close with the takeaway distilled to a line, plus a light CTA.

## The templates (already built, on-brand)

Four editable SVGs in `assets/templates/`, dark theme with a red `#C8453A` accent,
mono "terminal" chrome, and the user's photo as a circular avatar. Canvas 1080×1350.
Fonts (bundled in `assets/fonts/`, mapped in `assets/fonts.json`): **Bricolage
Grotesque** (display headlines, wght 700/800), **Inter** (body, 400), **JetBrains
Mono** (all mono chrome: terminal path, counters, eyebrow kickers, code, captions,
handle, CTA — weights 400/500/700).

Fields per template:

- `cover` — `terminal`, `counter`, `title`, `subtitle`, `swipe`
- `concept` — `terminal`, `counter`, `kicker`, `heading`, `body`, `handle`, `tags`
- `code` — `terminal`, `counter`, `kicker`, `heading`, `filename`, `code`, `caption`, `handle`, `tags`
- `close` — `terminal`, `counter`, `kicker`, `heading`, `body`, `cta`, `name`, `tagline`

Any field left empty is simply omitted, so slides degrade gracefully.

## deck.json (what the renderer consumes)

```json
{
  "slides": [
    { "template": "cover", "fields": {
        "terminal": "~/learning/sql", "counter": "SQL · 01",
        "title": "The 3 SQL joins I kept mixing up",
        "subtitle": "The mental model that finally made them stick.",
        "swipe": "SWIPE →" } },
    { "template": "concept", "fields": {
        "terminal": "~/learning/sql", "counter": "01 / 04",
        "kicker": "THE MENTAL MODEL",
        "heading": "Picture two tables as circles",
        "body": "INNER JOIN keeps only the overlap.\n\nLEFT JOIN keeps everything on the left, blanks on the right.",
        "handle": "@yourhandle", "tags": "sql · joins" } },
    { "template": "close", "fields": {
        "kicker": "THE TAKEAWAY",
        "heading": "INNER = overlap. LEFT = keep the left.",
        "body": "Pick the join by which rows you refuse to lose.",
        "cta": "Follow — I post what I learn",
        "name": "Your Name", "tagline": "learning in public" } }
  ]
}
```

Use `\n` in a field to force a line break; otherwise text wraps automatically.

## Rendering

```bash
python scripts/render_carousels.py \
  --templates assets/templates --fonts assets/fonts.json \
  --content output/carousels/mon/deck.json --out output/carousels/mon/
```

The renderer word-wraps each field to its box, shrinks the font until it fits, and
rasterizes each slide to `slide_01.png … slide_NN.png` with cairosvg.

## Editing the design

Each dynamic text is a `<text>` with a `{{field}}` token and `data-*` attributes:
`data-field`, `data-box-w`, `data-max-lines`, `data-size`/`data-min-size`,
`data-line-height`, `data-align`, and `data-pre="true"` (keep line breaks, for code).
Edit the SVGs to move boxes or change colors; swap TTFs in `assets/fonts/` (and
`assets/fonts.json`) to change typography. The circular avatar is `assets/brand/logo.png`.

If the user sends new designs, the cleanest input is an SVG exported with **live
text** (not outlined); otherwise rebuild by keeping the non-text vector parts and
adding `<text>` fields.
