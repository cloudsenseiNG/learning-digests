# Automating with GitHub Actions

This runs the whole pipeline on a schedule, with no computer of yours left on.
Two cron workflows live in `assets/github/` — copy them into your repo's
`.github/workflows/` folder:

- `daily-digest.yml` — every weekday morning: build the digest, email it to you,
  commit the updated tracker.
- `weekly-carousels.yml` — every Monday: write 5 carousel decks, render them to
  PNGs, and hand them back as a downloadable artifact (and to a Drive output folder).

## How a run works

1. GitHub's cron fires the workflow.
2. It checks out the repo (which holds this skill, `config.yaml`, `TRACKER.md`).
3. It pulls your **books** folder from Google Drive with rclone.
4. It runs Claude Code headless (`claude -p ...`) with this skill available. Claude
   reads the tracker, does the reading/writing work, and updates the tracker.
5. Deterministic steps render the slides / send the email.
6. The updated tracker is committed back, so the next run knows where it left off.

## Secrets — never commit these to the repo

Config that isn't sensitive (paths, schedule, `config.yaml`) lives in the repo.
Anything with a credential goes in **Settings → Secrets and variables → Actions**,
never in a committed file. The workflows read them as `${{ secrets.NAME }}`.

Required secrets:

| Secret | What it is |
|--------|------------|
| `ANTHROPIC_API_KEY` | Powers the Claude Code agent. Create at console.anthropic.com. |
| `GDRIVE_SA_JSON` | A Google **service account** JSON key (full file contents) used to read Drive. |
| `SMTP_HOST` / `SMTP_PORT` | Your mail server, e.g. `smtp.gmail.com` / `587`. |
| `SMTP_USER` / `SMTP_PASS` | Mailbox login. For Gmail, `SMTP_PASS` is a **Google App Password**, not your normal password. |
| `DIGEST_TO` | The address the digest is sent to (can be your own). |

Required repository **variable** (Settings → Variables):

| Variable | What it is |
|----------|------------|
| `GDRIVE_BOOKS_FOLDER_ID` | The ID of your `books` folder in Drive (the long string in its URL). |

## Google Drive access (service account, read-only)

GitHub's runners can't use the Drive desktop app, so they authenticate as a
service account instead:

1. In Google Cloud Console, create a project and enable the **Google Drive API**.
2. Create a **service account** and download its JSON key.
3. **Share your `books` Drive folder** with the service account's email
   (`...@...iam.gserviceaccount.com`), Viewer access.
4. Paste the JSON key's contents into the `GDRIVE_SA_JSON` secret.
5. Put the folder's ID into the `GDRIVE_BOOKS_FOLDER_ID` variable.

rclone then mounts it read-only and copies the PDFs into the runner for that run.
(If you'd rather not use a service account, an rclone OAuth token config works too —
store the whole `rclone.conf` as a secret and drop the config-writing step.)

## Hosting the digests (GitHub Pages)

Full digests are HTML with schematics and are too heavy to email, so they're hosted
and the email just links to them.

- One-time: repo **Settings > Pages > Build from a branch > `main` / `/docs`**.
- Set repo **variable** `SITE_BASE_URL` to your Pages URL
  (e.g. `https://<user>.github.io/<repo>`).
- Each run writes `docs/digests/<slug>.html`, appends `docs/digests.json`, rebuilds
  `docs/index.html` (a browsable library of every digest), and commits `docs/`. Pages
  redeploys automatically on push.

## Delivery

- **Digest** → published to Pages; the workflow emails a small **link email**
  (`build/email.html`) to `DIGEST_TO` via `scripts/deliver_digest.py`. The inbox gets
  the title, a teaser, a "Read the full digest" button, and the exercises note. Prefer
  a draft to review first? Point `DIGEST_TO` at yourself or swap in a Gmail draft call.
- **Carousels** → uploaded as a workflow **artifact** you download from the run page,
  and copied to a `_carousels_out` folder in Drive. You still post each one manually.

(Alternative host: an AWS S3 static-website bucket works the same way and doubles as
practice for your AWS track. Point `SITE_BASE_URL` at the bucket and `rclone/aws s3
sync docs/` instead of committing to `/docs`.)

## Schedules

Both crons are in **UTC**. Convert your local time before editing:
`cron: "0 6 * * 1-5"` is 06:00 UTC, Mon–Fri. Add `workflow_dispatch` (already
included) so you can also trigger either workflow by hand from the Actions tab —
useful for the first test run.

## Cost & notes

- Each run consumes Anthropic API credits (the agent reads a chapter and writes).
  Weekday digests + one weekly carousel batch is light, but keep an eye on it.
- The `permissions: contents: write` block is what lets the bot commit the tracker.
- Start by running each workflow manually (`workflow_dispatch`) once to confirm
  Drive access, the API key, and email all work before trusting the schedule.
