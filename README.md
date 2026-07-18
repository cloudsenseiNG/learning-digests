# learning-digests

A self-paced learning engine. It turns book chapters (and AWS docs) into a beginner-
friendly **HTML digest** (with schematics and a micro-project to build) and a matching
**carousel** for TikTok, on a dark personal-brand theme.

- Digests are published to **GitHub Pages** and you get a lightweight **link email**
  with that batch's carousels attached as a zip.
- It's **gated**: new content only ships once you've ticked off the current batch in
  `TRACKER.md`, so it never piles up.
- The cron runs **twice a day, 00:00 and 18:00 GMT+1**, and checks the gate each time.

A "batch" is the next unit for each of four tracks: DDIA, AI Engineering,
High Performance MySQL, and AWS.

## Layout

```
.claude/skills/book-digest-carousels/   the skill (Claude Code auto-discovers this)
.github/workflows/content.yml           the twice-daily gated workflow
docs/                                   GitHub Pages site (index + digests/)
books/                                  PDFs (pulled from Drive in CI; gitignored)
config.yaml                             your settings (edit the two EDIT ME lines)
TRACKER.md                              reading plan + the "Current batch" checklist
```

## One-time setup

1. **Create the repo and push** this folder.
2. **Edit `config.yaml`**: set `digest.email_to` and `digest.site_base_url`
   (`https://<your-gh-username>.github.io/learning-digests`).
3. **Books in Drive.** Put your PDFs in a Google Drive folder named `books`. Create a
   Google Cloud **service account**, enable the Drive API, and **share the folder** with
   the service account's email (Viewer).
4. **Add GitHub Actions Secrets** (Settings > Secrets and variables > Actions > Secrets):

   | Secret | What it is |
   |--------|------------|
   | `CLAUDE_CODE_OAUTH_TOKEN` | Powers the Claude Code agent using your Max/Pro subscription. Generate with `claude setup-token` (1-year token). Use this **or** `ANTHROPIC_API_KEY` (API credits) — if both are set, the API key wins. |
   | `GDRIVE_SA_JSON` | The service account JSON key, full contents. |
   | `SMTP_HOST` / `SMTP_PORT` | e.g. `smtp.gmail.com` / `587`. |
   | `SMTP_USER` / `SMTP_PASS` | Mailbox login. For Gmail, `SMTP_PASS` is a Google **App Password** (needs 2-Step Verification). |
   | `DIGEST_TO` | Where the email is sent (can be yourself). |

5. **Add repo Variables** (same page > Variables):

   | Variable | What it is |
   |----------|------------|
   | `SITE_BASE_URL` | Your Pages URL, same as `config.yaml`. |
   | `GDRIVE_BOOKS_FOLDER_ID` | The ID of your Drive `books` folder (from its URL). |

6. **Turn on GitHub Pages**: Settings > Pages > Build from a branch > `main` / `/docs`.

That's it. The workflow runs at 00:00 and 18:00 GMT+1. You can also run it by hand:
Actions > **Content** > Run workflow.

## How the gate works

`TRACKER.md` has a **Current batch** checklist. Each run checks it first:
- any box unchecked -> it waits (no email, no Pages update),
- all boxes ticked -> it produces and sends the next batch, then writes a fresh
  checklist.

Tick a box after you've read the digest and built its micro-project. Easiest on mobile:
open `TRACKER.md` in GitHub's web editor, change `- [ ]` to `- [x]`, commit.

## Test it locally with Claude Code

```bash
# from the repo root
pip install -r requirements.txt
# register the bundled fonts so carousels/digests render on-brand (Linux/mac):
mkdir -p ~/.fonts && cp .claude/skills/book-digest-carousels/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f

# drop a PDF to test with (e.g. DDIA) into ./books
cp ~/Downloads/Designing_Data_Intensive_Applications.pdf books/

# then launch Claude Code in the repo and ask:
claude
> Using the book-digest-carousels skill, produce today's batch from the books in ./books.
```

Claude Code auto-discovers the skill in `.claude/skills/`. It will read `TRACKER.md`,
build the HTML digest into `docs/digests/`, render the carousel into `build/`, update the
index, and write the link email to `build/email.html`. To try emailing, export the SMTP
vars in your shell and run:

```bash
python .claude/skills/book-digest-carousels/scripts/deliver_digest.py \
  --file build/email.html --attach "build/carousels-*.zip"
```

## Notes

- Book PDFs are **not** committed (see `.gitignore`); they live in Drive.
- Secrets live in GitHub Actions Secrets, never in the repo.
- Cron is in UTC under the hood: `23:00` and `17:00` UTC = `00:00` and `18:00` GMT+1.
