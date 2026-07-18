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

**4–8 slides, matched to complexity.** A simple idea is a tight 4; a meatier one earns
the full 7–8 so the arc can breathe. Don't compress a rich idea to hit a low count, and
don't pad a thin one: give the idea the length it deserves. It should never feel
overwhelming, but **depth wins** over brevity.

- Slide 1 hooks: a promise, a surprising number, or "I kept getting this wrong."
- One thought per slide. Short lines. No paragraphs — this is glanceable.
- Include **one `code` visual-proof slide per deck** (the tiny schematic, see below);
  add further `code` slides only if another snippet genuinely carries a point.
- Close with the takeaway distilled to a line, plus a light CTA.

## Signature structure (match this — the AWS core-networking carousel is the benchmark)

The carousels the user loves read like a short **story**, not a list of facts. Match
this arc (each numbered beat is one `concept` slide unless noted):

1. **Cover / hook** — frame a real tension or realization in the learner's voice
   ("Public subnet or private subnet? It's ONE line in a table."). The subtitle is a
   first-person promise ("The route table trick that finally made VPC click for me.").
2. **Orient** (kicker e.g. `THE SETUP`) — one plain-language slide giving the beginner
   the ground they need ("Everything in AWS lives inside a VPC").
3. **The crux** — put the single **concrete artifact** at the centre as the heading: a
   real value, row, command, or number (`0.0.0.0/0 pointed at an internet gateway =
   public`), then explain it simply. Specific always beats abstract.
4. **Visual proof (REQUIRED — one per deck).** A `code`-panel slide that *shows* the
   crux as a tiny monospace schematic instead of describing it: a route-table snippet,
   a replication fan-out, a fault → failure flow, a next-token strip. See "The
   visual-proof slide" below. This is the beat that turns "I read it" into "I see it."
5. **Why it matters — a real, named, dated case study (REQUIRED).** Tie the small
   detail to a real incident with stakes: the Feb 2017 S3 typo outage, the Dec 2021
   AWS outage, a documented postmortem. **Verify it with a quick web search; never
   invent an incident, date, or number.** This is the beat that makes the set land.
6. **Bring it home** (kicker e.g. `SAME INSTINCT, SMALLER STAKES`) — scale it back to
   the learner's own situation: the practical caution, or how to apply it day to day.
7. **Close / takeaway** — the whole thing distilled to one memorable line, plus the
   Follow CTA, avatar, name, and the social handles.

**Kickers are punchy and specific**, never generic: "THE ONE ROW THAT DECIDES IT" and
"WHY THIS ROW MATTERS SO MUCH" beat "Definition" and "Example". Footer chrome stays
topic-based ("aws · route tables") with the `@mayowa` handle. Every track (DDIA, AI
Engineering, MySQL, AWS) follows this same arc — it is not AWS-only.

**Length stays flexible, 4–8 — the arc is a menu, not a fixed seven.** The beats above
are the full-length shape. For a simpler idea, merge beats (fold "orient" into the crux,
or "bring it home" into the close) and run as tight as **4**: cover → crux + visual
proof → case study or takeaway → close. Scale toward 8 only when the idea genuinely has
that much to show. The one visual-proof slide (and a real case study, when the concept
has one worth telling) fit inside that range. **Never pad slides to hit a number.**

## The visual-proof slide (required, one per deck)

Every deck includes **exactly one** `code`-template slide whose job is to *show* the
idea, not tell it. The `code` template is a terminal-window panel with a monospace body
(JetBrains Mono, line breaks preserved), so a small ASCII/box schematic renders crisply
and on-brand. Keep it **≤ 13 lines and ≤ ~40 characters wide** so it never shrinks to
unreadable. Safe glyphs: `-> | + [ ] :` and the arrows/box-drawing `→ ▶ ┌ ┐ └ ┘ ├ ┤ │ ─`.
Put a short `kicker` (e.g. `SEE IT`), a `filename` label, the schematic in `code`
(`data-pre` keeps your line breaks), and a one-line `caption` under the panel. If a value
is illustrative (a probability, an ID), keep it obviously rounded/example — per the
guardrails, don't pass invented numbers off as real.

One per track, matched to the chapter's crux:

```
AWS — route table (filename: route-table)        DDIA — fault vs failure (fault-model)
Destination    Target                            fault ──▶ [ caught in time? ]
10.0.0.0/16    local                                         │yes        │no
0.0.0.0/0      igw-0abc   ← public                           ▼           ▼
                                                          contained    FAILURE

MySQL/DDIA — replication (replication)           AI Engineering — next token (predict)
          writes                                 "the cat sat on the ___"
Primary ──┬──▶ Replica A  (reads)                  mat    ▓▓▓▓▓▓▓  0.71
          └──▶ Replica B  (reads)                  floor  ▓        0.09
   async, may lag                                  roof   ▓        0.04
```

These are the *shape*, not gospel: adapt the schematic to whatever the unit's crux is
(an index B-tree, a queue, a cache-aside path). The point is a glanceable picture that
proves the concept.

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
    { "template": "code", "fields": {
        "terminal": "~/learning/sql", "counter": "02 / 04",
        "kicker": "SEE IT", "filename": "inner-join",
        "code": "users        orders\n1 ann        1 ann\n2 ben        1 ann\n\nINNER  ->  keeps only id 1",
        "caption": "The overlap is the whole point: no match, no row.",
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
