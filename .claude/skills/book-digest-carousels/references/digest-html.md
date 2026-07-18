# HTML digest layout + schematics

The digest is a dark, on-brand HTML email that matches the carousels. Content and
voice come from `digest-template.md`; this file covers the visual layout, the brand
tokens, and how to add schematics.

## Brand tokens

- Background `#0A0A0B`, cards/panels `#0E0E10` / `#131316`, hairline `rgba(242,239,233,0.10)`.
- Text: headings/ink `#F2EFE9`, body `#C9C7C1`, muted `#7A7A80`. Accent red `#C8453A`.
  A soft green `#6FCF97` is fine for "good outcome" marks in schematics.
- Fonts: Bricolage Grotesque (headings), Inter (body), JetBrains Mono (eyebrows, code,
  the terminal-style labels). Load them with a Google Fonts `<link>` for browser viewing.

## Structure

Wrap in a `max-width:660px` centered container. Order:
mono eyebrow (`SYSTEMS · CH.N DIGEST`) -> `<h1>` title (also used as the email subject)
-> lead line -> THE BIG IDEA -> KEY TERMS -> the pillars/sections (each a short para plus
a schematic where useful) -> a bordered "REMEMBER THIS" box -> a footer with the round
avatar (`assets/brand/logo.png`), the name, and the socials, matching the close slide.

## Schematics (the point of the HTML format)

Add a schematic whenever a picture explains faster than a paragraph. Draw them as inline
`<svg>` using the brand tokens above, wrapped in a bordered figure with a one-line caption.
Good default types:
- **Flow / relationship** (e.g. fault -> contained -> works, or -> spreads -> failure).
- **Distribution / chart** (e.g. a right-skewed latency curve with p50/p95/p99 marked and
  the slow tail shaded red). This one earns its place often.
- **Architecture / topology** (boxes and arrows: services, replicas, data centers, a
  request path). For AWS topics especially, a small topology sketch is worth a lot.
Keep them simple and legible, 2 to 4 per digest. Don't decorate for its own sake.

## Exercises

End every digest with a "Try it yourself" box (use the green accent `#6FCF97` on the
left border to set it apart from the red "Remember this" box). 4 to 6 concrete tasks,
per `digest-template.md`.

## Hosting + the link email

The full HTML digest is heavy (schematics, embedded avatar), so it is hosted on GitHub
Pages under `docs/digests/<slug>.html`, not emailed. Each run also:
- appends `docs/digests.json` and rebuilds `docs/index.html` via `scripts/build_index.py`
  (a browsable library of all digests), and
- writes a small **link email** to `build/email.html`: eyebrow, title, one-line teaser,
  a red "Read the full digest" button pointing at `<site_base_url>/digests/<slug>.html`,
  a one-line exercises note, and the brand footer. Keep it light: downscale the avatar
  (about 96px) and include no schematics, so the email stays a few KB.

## Email delivery caveat (already handled)

Gmail and most clients strip inline `<svg>` and block `data:` image URIs. `deliver_digest.py`
handles this automatically: it rasterizes each inline `<svg>` to PNG and rewrites `data:`
images, attaching them as CID parts so everything renders in the inbox. So author the
digest with inline SVG (crisp for browser/archive) and let the send step convert it.
