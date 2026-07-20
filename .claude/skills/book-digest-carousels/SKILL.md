---
name: book-digest-carousels
description: "Turn a book chapter (PDF) into a beginner-friendly daily DIGEST drafted as a ready-to-send email, plus a batch of ready-to-post TikTok CAROUSEL image slides that follow the user's own template, and keep a progress tracker so chapters are never skipped or repeated. Use this skill whenever the user asks for a digest, chapter summary, carousels, slides, this week's carousels, today's digest, wants to turn a book or PDF into social content, or mentions their study or TikTok content routine, even if they don't name the skill. Trigger it on any recurring book-to-content request."
---

# Book Digest & Carousels

This skill runs a personal learning-to-content pipeline for someone **new to the
material**. It reads a chapter from a book PDF and produces:

1. A **daily digest** — a plain-language email that teaches the chapter without
   assuming prior knowledge and without dropping important detail.
2. **Carousels** — one on-brand set of ready-to-post image slides per track each batch
   (7–10 slides), distilling that unit's key idea, rendered on the user's dark brand
   templates and ready for TikTok or LinkedIn.

It also keeps a **tracker** so you always know what's been covered and what's next.

**Voice:** the user (Mayowa) is learning this material alongside their audience.
Write everything, digests and carousels, as a relatable fellow learner ("here's what
finally made this click"), in plain English, never as a lecturing expert. Define terms
as they appear.

**Write like a person, not an AI.** No em dashes anywhere (use commas, periods,
parentheses, or a colon). Avoid the giveaway patterns: "it's not X, it's Y",
forced rule-of-three phrasing, and stacking colons for drama. Use contractions and
the occasional short sentence. Read it back and cut anything that sounds generated.

**Don't cite the source book on carousels.** These are general field concepts in
Mayowa's own words, so no attribution is needed on a social post. Just never reproduce
the source's exact wording or its signature examples verbatim. Keep the chrome
topic-based (e.g. "SYSTEMS · 01"), not book-based.

**And never hint that a book exists at all.** Not naming it isn't enough: keep every
source-shaped word out of the slide copy, including titles and subtitles. No "chapter",
"this chapter", "the book", "the author", "the text", "reading", "Ch.1", "pages". Write
about the **topic** ("that rule explains half of how MySQL behaves"), never about the
material it came from ("that rule explains half this chapter"). First-person learning
voice is fine, pointing at study material is not. Digests are the opposite and must
cite their source in "Sources & verify" — this rule is **carousels only**.

**Use fresh, real examples, not the book's.** When a point needs an illustration,
reach for a true real-world example from outside the source (verify it with a quick
web search first), and prefer ones that tie into Mayowa's own tracks. For instance, to
show "faults shouldn't become failures," use S3 storing every file across 3+ data
centers; to show human error, use the 2017 AWS typo outage. Don't reuse the book's own
case studies (that's the tell that it's a book recap).

Because there is no automatic scheduling or cross-session memory, the tracker file
is the source of truth. Read it at the start of every run and update it at the end.

---

## Content guardrails (non-negotiable)

These apply to every digest, carousel, and micro-project. If a run cannot satisfy
them, hold and surface the gap rather than shipping something that violates them.

**1. Accuracy and source discipline**
- Treat every digest as a **teaching draft, not an authoritative source**.
- Ground every technical claim in the supplied book chapter, official AWS
  documentation, or another explicitly provided primary source.
- Put a short **"Sources & verify"** section in every HTML digest: book title,
  chapter, relevant page range where available, and source links for AWS material.
- Do **not** invent commands, APIs, configs, performance numbers, pricing, limits,
  or "best practices." If you can't ground it, leave it out.
- When you simplify a concept for a beginner, **label it a simplification** and state
  the important caveat.
- Prefer "here's the mental model" over unsupported certainty. If the source is
  unclear or insufficient, **flag the uncertainty** instead of filling the gap.
- **Never teach a false universal.** Simplifying for a beginner is fine; implying a
  claim is universal when it only holds for one common setup is not.

**Bounded claims (how to simplify without lying).** Before writing an absolute, ask:
*is this true generally, or only under a particular configuration, version, architecture,
workflow, or convention?* The tells are **always, never, only, every, must, can't,
guarantees**. Keep the simple mental model, but **name the boundary**: "usually", "in
most setups", "by default", "in a common pattern", "in this architecture", "for
beginners, think of it as".

| ❌ False universal | ✅ Bounded, still simple |
|---|---|
| "SQL has one writer." | "In a common MySQL source-replica setup, one server handles writes." |
| "MySQL will only let one server take writes." | "Replicas are copies that catch up by replaying changes." |
| "Every table lives on one server." | "Two uncoordinated writers can create conflicts." |

Note the error in the first one: **SQL is the language, not the topology**. Never let a
language, tool, framework, or protocol be described as if it always behaves the way one
common deployment does (MySQL, for instance, also has multi-writer configurations). One
bounding word is usually enough — bound the claim once, clearly, and don't bury the
reader in caveats.

**2. Copyright and originality**
- Never reproduce substantial book passages, tables, illustrations, diagrams,
  exercises, or end-of-chapter material.
- Write every explanation in **entirely original language**; build every diagram and
  schematic **from first principles** (never trace or imitate a source figure).
- Use quotations only when essential: brief, clearly attributed, with chapter/page.
- Cite the source, but never present the digest as a substitute for reading the book.
- Micro-projects are **original adaptations**, never copied book exercises.

**3. One book = one job (don't bundle)**
Each book (and the AWS track) is handled as its **own independent job**, carried
through the six stages below in order. Do not merge multiple books into one job unless
the user explicitly asks. Keep it fully automated: **no human PR-review step before
delivery**, and the default output is for the user's **private use**, not an audience.

  1. **Source** — identify the exact chapter or docs section, extract the learning
     objective, and record citations (book/chapter/pages, or the AWS doc URLs).
  2. **Teaching** — write the beginner-friendly explanation, examples, caveats, and
     recall questions.
  3. **Visual** — create original diagrams that clarify the system or idea.
  4. **Build** — design a small, runnable micro-project with clear completion criteria.
  5. **Verification** — check factual claims, commands, citations, links, and
     consistency with the source before delivery. Fix or flag anything that fails.
  6. **Delivery** — package the final HTML digest and companion assets and deliver
     them straight to the user: **no human PR-review step, ever**. Publishing the
     digest to the user's **own GitHub Pages library** is authorized (they've opted
     into it). Beyond that, do not push to any other public platform (e.g. posting the
     carousels to TikTok) unless the user explicitly asks. A cycle's carousels are
     zipped with a **top-level folder per book** and attached to the digest email.

**Combined delivery, independent jobs.** In the unattended cycle the four jobs are
processed independently (each through stages 1–6 above) but delivered in **one**
email: all the new digests linked, plus a single carousels zip organised with a
**folder per book**. "Don't bundle" is about the *work* (each book sourced, taught,
and verified on its own), not about forcing four separate emails.

---

## First-run setup

If `config.yaml` does not exist in the working directory, create it from
`assets/config.example.yaml` and ask the user to fill in the paths. Key fields:

- `books_dir` — where the PDFs live. This is normally a **Google Drive folder
  synced to the local disk** (via the Google Drive desktop app) so the skill can
  read PDFs as ordinary files. A plain repo folder or downloaded PDFs work too.
- `output_dir` — where digests and rendered slides are written.
- `tracker` — path to the `TRACKER.md` progress file (create from `assets/TRACKER.example.md`).
- `carousel_templates` / `carousel_fonts` — the SVG templates directory and the fonts
  map for the slides (both ship inside the skill under `assets/`).
- `digest.email_to` — the address the digest email is addressed to.

If any path is missing, ask before guessing. Never invent a books folder.

---

## Locating a chapter in a PDF

A book PDF contains many chapters, so you must find the right one:

1. Check the tracker first — if this book+chapter already has a cached page range,
   use it directly (fast path).
2. Otherwise, read the PDF's table of contents / headings to find the chapter's
   start and end pages, then extract just those pages' text.
3. **Cache the discovered page range back into the tracker** so the next run is instant.

Use `scripts/extract_chapter.py --pdf <file> --pages <start-end>` to pull clean text,
or read the pages directly if the PDF is scanned (then OCR).

## Web-sourced topics (e.g. AWS)

Not every source is a book. For a track whose source is a website (the tracker lists
`https://docs.aws.amazon.com/` for the AWS track), treat each topic like a chapter but
read it from the web instead of a PDF: fetch the relevant service doc pages for that
topic, then produce the same digest and carousel. Record the topic as done in the
tracker just like a chapter. Everything downstream (voice, templates, delivery) is
identical.

---

## Workflow A — Daily digest

Trigger phrases: "today's digest", "digest chapter N of <book>", "catch me up on <book>".

1. Read `config.yaml` and `TRACKER.md`. Work through the plan **sequentially and
   finish the current chapter before starting the next**. Don't force a whole chapter
   into one day: if a chapter is long, cover a coherent section, mark it "in progress"
   in the tracker, and pick up where you left off next time. Only move to the next
   chapter once the current one is done. **There is no rush to finish a book — depth
   over speed.** Prefer splitting a chapter across several batches to bring out real
   detail (clear explanations, concrete examples, and a real named case study) over
   racing ahead; only advance when the current unit is genuinely thorough.
2. Locate and extract the chapter text (see above).
3. Write the digest as **HTML** into `docs/digests/<slug>.html` (the GitHub Pages
   folder), using the content structure in `references/digest-template.md` and the
   layout in `references/digest-html.md`. Teach for a beginner: define every term,
   explain each idea with a concrete example, keep important detail. **Add simple SVG
   schematics where a diagram makes a concept clearer** (fault/flow, a percentile
   distribution, an architecture sketch). End with a **"Try it yourself" micro-projects
   section**: 4 to 6 small things to build (each an hour or two in any language) that
   reinforce the chapter, since building broadens understanding more than notes. Match
   the dark brand theme; keep the fellow-learner voice and the no-em-dash / human style.
   **End every digest with a "Sources & verify" section** (book title, chapter, page
   range where known; source doc links for AWS) per the accuracy guardrail above.
   Obey all **Content guardrails**: ground claims, label simplifications, flag
   uncertainty, and keep all wording and diagrams original.
4. Publish and notify:
   - Append the digest's entry (`slug, book, ch, title, date`) to `docs/digests.json`
     and rebuild the index with `scripts/build_index.py --docs docs`.
   - Build the **lightweight link email** with `scripts/build_email.py --docs docs
     --site-base-url <site_base_url> --logo assets/brand/logo.png --out build/email.html`
     (Gmail-safe: inline styles, embedded avatar, a button per new digest). Don't
     hand-author it.
   - Send it with `scripts/deliver_digest.py --file build/email.html`. The full digest
     is hosted (too big to email); the inbox just gets the link.
5. Update the tracker: mark the chapter digested (or "in progress") with today's date.

---

## Workflow B — Carousels (one per track/unit, on demand)

Trigger phrases: "make the carousels", "carousel for <chapter/track>", "this batch's carousels".

1. Read `config.yaml` and `TRACKER.md`. Identify the unit(s) to cover: normally the
   current batch's next unit for each track, or a specific chapter/track the user names.
   **One carousel per unit** (`carousels.per_batch_per_track: 1`).
2. For each unit, take the single most **post-worthy idea** from that chapter (not the
   whole digest) and build one carousel. One clear idea per carousel.
3. Write the slide copy following `references/carousels.md`: the signature arc at
   **7–10 slides** (7 is the floor), with the required **visual-proof** slide, a **real
   case study**, and the **fixed per-track chrome** (terminal + counter prefix). Use the
   editable SVG templates in `assets/templates/` (`cover`, `concept`, `code`, `close`).
   Save each carousel as a `deck.json` (schema in that reference) under
   `output_dir/carousels/<book>/<slug>/`.
4. Render each carousel to PNGs:
   ```bash
   python scripts/render_carousels.py \
     --templates assets/templates --fonts assets/fonts.json \
     --content output_dir/carousels/<book>/<slug>/deck.json \
     --out output_dir/carousels/<book>/<slug>/
   ```
   This produces `slide_01.png … slide_NN.png` sized and styled per the template.
5. Present the carousel(s) to the user. Update the tracker: mark each unit's carousel
   made with today's date.

The user posts each carousel manually — the skill just prepares them.

---

## Updating the templates

The four SVG templates in `assets/templates/` already match the user's brand. To
change the look, edit those SVGs directly (see the "How the templates work" section
in `references/carousels.md`) or swap the TTFs in `assets/fonts/`.

If the user submits **new** designs: the cleanest input is an SVG exported with live
text (not outlined) — replace its text with `{{field}}` tokens. If the export has
outlined text, rebuild by keeping the design's non-text vector parts (background,
decoration, logo) and adding `<text>` fields with `data-*` layout attributes.

---

## Progress tracker rules

`TRACKER.md` is the memory of this system. Always:

- Read it at the start of a run to know what's done and what's next.
- Update it at the end of a run (chapters digested, carousels made, cached page ranges).
- Never re-digest or re-post a chapter already marked done unless the user asks.

---

## Running unattended (GitHub Actions)

`assets/github/content.yml` runs **twice a day (00:00 and 18:00 GMT+1)**. Each run first
checks a **completion gate**: `scripts/gate.py` reads the "Current batch" checklist in
`TRACKER.md`, and only if every box is ticked does the run proceed. This keeps content
self-paced: nothing new is produced, published, or emailed until the user has worked
through the previous batch.

When the gate is clear, the run produces the **next batch**: the next unit for each of
the four tracks (the three books plus AWS), finishing an in-progress chapter before
starting a new one. Each track is handled as its **own independent job** (source →
teaching → visual → build → verification → delivery) under the **Content guardrails**,
and every digest ends with a **"Sources & verify"** section.

For each unit it publishes the HTML digest to GitHub Pages and renders that unit's
carousel PNGs into a **per-book folder**, `build/carousels/<book>/<slug>/`, so the
final zip is organised with **one top-level folder per book**. It then sends **one
combined link email** for the whole batch with that single foldered zip attached, and
rewrites the "Current batch" checklist (all unchecked) for the next cycle.

Full setup (secrets, Drive service account, GitHub Pages, `SITE_BASE_URL`) is in
`references/github-actions.md`. Credentials go in GitHub Actions **Secrets**, never in
the repo.

## Reference files

- `references/digest-template.md` — digest content structure, voice, and a worked example.
- `references/digest-html.md` — the HTML digest layout, brand tokens, and schematics guide.
- `references/carousels.md` — copywriting rules, the SVG templates, and the
  `deck.json` schema the renderer consumes.
- `references/github-actions.md` — the scheduled-automation architecture and setup.

## Scripts

- `scripts/extract_chapter.py` — extract clean text from a PDF page range.
- `scripts/render_carousels.py` — fill the SVG templates and render slide PNGs.
- `scripts/deliver_digest.py` — email a digest or link email over SMTP (HTML with
  inline schematics / `data:` images is auto-converted to CID images).
- `scripts/build_index.py` — rebuild the hosted digest library index from the manifest,
  grouped by track and ordered by chapter (additive; never deletes a digest).
- `scripts/build_email.py` — build the batch's **Gmail-safe** link email deterministically
  (table layout, fully inline styles, logo embedded as a CID image). Do not hand-author
  the email; email clients strip `<style>` blocks and non-embedded images.
- `scripts/lint_carousels.py` — **check the generated decks against the guardrails** before
  delivery: book tells and structure (7–10 slides, exactly one `code` visual-proof slide,
  cover first / close last) and fixed per-track chrome are **errors**; unbounded absolutes
  are **warnings** (some are legitimately true, so a human decides). Run it after rendering:
  `python scripts/lint_carousels.py --carousels build/carousels`.
