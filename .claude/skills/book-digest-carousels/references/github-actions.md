# Automating with GitHub Actions

This runs the whole pipeline on a schedule, with no computer of yours left on.
**One** workflow does it all: `.github/workflows/content.yml` (source lives in
`assets/github/content.yml`). Copy it into your repo's `.github/workflows/` folder.

It runs **twice a day** and is **gated**: each run only produces the next batch once
you've ticked off the current one, so content never piles up.

- `content.yml` — cron `0 23 * * *` and `0 17 * * *` (= 00:00 and 18:00 GMT+1), plus
  `workflow_dispatch` so you can run it by hand from the Actions tab.

## How a run works

1. GitHub's cron fires the workflow (or you click **Run workflow**).
2. **Completion gate** (`scripts/gate.py`) reads the "Current batch" checklist in
   `TRACKER.md`. If any box is unchecked it **holds** — nothing is produced, emailed, or
   published. If every box is checked (or the list is empty) it's **clear** to proceed.
3. It checks out the repo (which holds this skill, `config.yaml`, `TRACKER.md`), installs
   deps + the bundled fonts, and pulls your **books** folder from Google Drive with rclone.
4. It runs Claude Code headless (`claude -p ...`) with this skill available. Claude
   produces the **next unit for each of the four tracks** (DDIA, AI Engineering, High
   Performance MySQL, AWS) as independent jobs: writes each HTML digest to
   `docs/digests/<slug>.html`, appends `docs/digests.json`, and renders each carousel's
   PNGs to `build/carousels/<book>/<slug>/`. It then rewrites the "Current batch"
   checklist (all unchecked) for the next cycle.
5. Deterministic steps rebuild the index (`build_index.py`), build a Gmail-safe link
   email (`build_email.py`), zip the carousels (foldered per book), and send the email
   with the zip attached (`deliver_digest.py`).
6. The `content-bot` commits `docs/` + `TRACKER.md` back (rebase + retry push), so the
   next run knows where it left off and Pages redeploys.

## Secrets — never commit these to the repo

Config that isn't sensitive (paths, schedule, `config.yaml`) lives in the repo. Anything
with a credential goes in **Settings → Secrets and variables → Actions**, never in a
committed file. The workflow reads them as `${{ secrets.NAME }}`.

Required secrets:

| Secret | What it is |
|--------|------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Powers the Claude Code agent using a **Claude Pro/Max subscription** (generate with `claude setup-token`, ~1-year token). Use this **or** `ANTHROPIC_API_KEY` for pay-as-you-go API credits — if both are set, the API key wins, so set only one. |
| `GDRIVE_SA_JSON` | A Google **service account** JSON key (full file contents) used to read Drive. |
| `SMTP_HOST` / `SMTP_PORT` | Your mail server, e.g. `smtp.gmail.com` / `587`. |
| `SMTP_USER` / `SMTP_PASS` | Mailbox login. For Gmail, `SMTP_PASS` is a **Google App Password**, not your normal password. |
| `DIGEST_TO` | The address the link email is sent to (can be your own). |

Required repository **variables** (Settings → Variables):

| Variable | What it is |
|----------|------------|
| `SITE_BASE_URL` | Your GitHub Pages URL, e.g. `https://<user-or-org>.github.io/<repo>`. |
| `GDRIVE_BOOKS_FOLDER_ID` | The ID of your `books` folder in Drive (the long string in its URL). |

## Google Drive access (service account, read-only)

GitHub's runners can't use the Drive desktop app, so they authenticate as a service
account instead:

1. In Google Cloud Console, create a project and enable the **Google Drive API**.
2. Create a **service account** and download its JSON key.
3. **Share your `books` Drive folder** with the service account's email
   (`...@...iam.gserviceaccount.com`), Viewer access.
4. Paste the JSON key's contents into the `GDRIVE_SA_JSON` secret.
5. Put the folder's ID into the `GDRIVE_BOOKS_FOLDER_ID` variable.

rclone then reads it read-only and copies the PDFs into the runner for that run. (If
you'd rather not use a service account, an rclone OAuth token config works too — store
the whole `rclone.conf` as a secret and drop the config-writing step.)

## Hosting the digests (GitHub Pages)

Full digests are HTML with schematics and are too heavy to email, so they're hosted and
the email just links to them.

- One-time: repo **Settings > Pages > Build from a branch > `main` / `/docs`**. (A
  private repo needs a paid plan for Pages; a public repo works on the free plan.)
- Set repo **variable** `SITE_BASE_URL` to your Pages URL.
- Each run writes `docs/digests/<slug>.html`, appends `docs/digests.json`, rebuilds
  `docs/index.html` (a library grouped by track, ordered by chapter), and commits
  `docs/`. The library is **additive** — digests are never auto-deleted. Pages redeploys
  automatically on push.

## Delivery

- **Digest** → published to Pages; the workflow emails one small **link email**
  (`build/email.html`, built by `scripts/build_email.py`) to `DIGEST_TO` via
  `scripts/deliver_digest.py`. The email is Gmail-safe (inline styles, the avatar
  embedded as a CID image) and links each new digest.
- **Carousels** → zipped with a **top-level folder per book** and **attached to that same
  email**. You post each one manually (they suit TikTok and LinkedIn, 1080×1350).

(Alternative host: an AWS S3 static-website bucket works the same way and doubles as
practice for your AWS track. Point `SITE_BASE_URL` at the bucket and `aws s3 sync docs/`
instead of committing to `/docs`.)

## Schedule

The crons are in **UTC**. `0 23 * * *` and `0 17 * * *` are 23:00 and 17:00 UTC = 00:00
and 18:00 **GMT+1 (West Africa Time)**. Convert to your own timezone before editing.
`workflow_dispatch` is included, so you can also trigger a run by hand from the Actions
tab — useful for the first test run.

## Cost & notes

- With `CLAUDE_CODE_OAUTH_TOKEN`, generation runs on your **Claude subscription** (no
  per-token API charge). If you use `ANTHROPIC_API_KEY` instead, each run spends API
  credits (the agent reads chapters and writes) — a batch is light, but keep an eye on it.
- The `permissions: contents: write` block is what lets the bot commit `docs/` and the
  tracker. The publish step rebases and retries so a concurrent push never drops a batch.
- Start by running the workflow manually (`workflow_dispatch`) once to confirm Drive
  access, the token, Pages, and email all work before trusting the schedule.
