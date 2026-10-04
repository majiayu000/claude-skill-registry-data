---
name: format-for-publish
description: Convert the cited draft into a Strapi-ready package — clean markdown body + Strapi-shaped JSON payload + a README with paste/publish instructions. Pushes directly to Strapi via API when STRAPI_API_TOKEN is set. With --auto-publish (or BLOG_AGENT_AUTO_PUBLISH=1), publishes the article live (publishedAt = now) instead of as draft.
allowed-tools: Read, Write, Edit, Bash
---

# Format for Publish Skill (Strapi)

Transform the cited draft into a publish-ready package for Strapi. The skill produces three files: a clean markdown body (for pasting into Strapi rich-text fields), a Strapi-shaped JSON payload (for API publish), and a README with step-by-step publish instructions.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft)
- `references/strapi-format.md` (application rules)
- `../../templates/strapi-format.md` (canonical Strapi reference)

## Process

1. **Read the cited draft.** Make a working copy in memory; don't edit the source.
2. **Strip the editor-notes section** if present (everything from `## Editor notes` onward). That's internal pipeline metadata, not for publishing.
3. **Extract the H1 as the title** and remove it from the body. Strapi renders the title separately; an H1 in the body causes duplicate-title bugs.
4. **Apply callout transformations** per `references/strapi-format.md`:
   - `**Tip:** ...` and `**Pro tip:** ...` → `:::tip ... :::`
   - `**Note:** ...` and `**Sidenote:** ...` → `:::note ... :::`
   - `**Editor:** ...` → `:::editor ... :::`
4b. **Convert GFM tables for the live renderer (PLEAA-567 workaround — publish boundary ONLY).** The draft/preview keep real markdown tables; the public Next.js renderer can't render GFM tables yet (CTO ticket pending), so at THIS stage convert each table in the working copy: render it to a legible table-card PNG (same matplotlib table-card path `/generate-visuals` uses for `type=table` text-tables), upload as a media block where the table stood, and keep a compact bulleted text version beneath the image (one bullet per row, bold first-column label) so the content stays crawlable. When the renderer fix ships, delete this step — nothing upstream changes.
5. **Build the Strapi v5 JSON payload** with title, slug, description (first 1–2 sentences of intro, ≤80 chars — also serves as `<meta name="description">`), blocks[] (single `shared.rich-text` component holding the markdown body), category (documentId resolved via `/api/categories`), publishedAt. The schema is strict — `author_name`, `read_time`, `cover_image_url`, `tags`, `excerpt`, `content`, `seo` are NOT in the Article content-type; Strapi 400s on them. Author is attached manually in admin if needed. The article-level `cover` relation is auto-attached on `--auto-publish` to the first uploaded image (PLEAA-570, 2026-05-11) so RSS feeds, OG tags, social cards, and admin preview resolve the hero too. SEO surface is `title` + `description` only (PLEAA-457 DOD#4 resolved 2026-05-07).
6. **Run the formatter script:**
   ```bash
   python .claude/skills/format-for-publish/scripts/format_for_strapi.py "<slug>"
   ```
   The script writes the three files to `content-pipeline/8-publish/{slug}/`.
7. **If the user has wired up Strapi API access via Doppler** AND wants direct publish, append `--publish`:
   ```bash
   doppler run -- python .claude/skills/format-for-publish/scripts/format_for_strapi.py "<slug>" --publish
   ```
   Requires `STRAPI_BASE_URL` and `STRAPI_API_TOKEN` env vars. Article is created in Strapi as a DRAFT (publishedAt = null) — editor publishes manually after review.
8. **Tell the user** the output paths and which option (paste vs API) is active.

## Output

`content-pipeline/8-publish/{slug}/`
- `article.md` — clean markdown body (paste in Strapi rich-text field)
- `article.json` — Strapi-shaped payload
- `README.md` — paste-or-publish instructions with title, slug, excerpt, SEO fields, suggested categories/tags

## Quality checklist

- [ ] H1 stripped from body (title lives in JSON only)
- [ ] No `**Tip:**` / `**Note:**` / `**Editor:**` markdown prefixes remaining in body — all converted to `:::` callouts
- [ ] Editor-notes section excluded from output (it's pipeline metadata, not content)
- [ ] `description` is real prose from the intro, not the title or first heading
- [ ] `description` ≤ 80 chars (Strapi v5 cap)
- [ ] `blocks[0].__component == "shared.rich-text"` and `blocks[0].body` non-empty
- [ ] No legacy v4 fields (`excerpt`, `content`, `seo`, `categories[]`) in payload
- [ ] `category` (when set) is a documentId STRING, not an array
- [ ] Slug matches the input slug exactly
- [ ] `publishedAt: null` for draft mode; ISO timestamp only when `--auto-publish` is set

## Customizing for your Strapi schema

The default JSON shape assumes a typical "Article" content type with: `title`, `slug`, `excerpt`, `content`, `seo` (component), `categories` (relation), `tags` (relation), `publishedAt`. If your Strapi has different field names or component shapes:

1. Open `format_for_strapi.py`
2. Edit the `build_payload()` function — adjust field names, nest components per your schema
3. The transformation logic (callouts, excerpt extraction) works regardless of payload shape

## When direct API publish fails

Common causes:
- **401 Unauthorized:** API token missing or wrong scope. Check Strapi admin → Settings → API Tokens; needs at least "Authenticated" or "Full access" for content creation
- **400 Bad Request:** Payload doesn't match your Strapi schema. Check `article.json` against your real content type — likely a missing required field or extra unknown field
- **404 Not Found:** `STRAPI_BASE_URL` is wrong or the endpoint isn't `/api/articles` (e.g., your content type is named differently — check Settings → API Tokens → endpoint list)

When `--publish` fails the script keeps the local files so you can paste manually.

## Auto-publish vs draft modes

The skill supports two publish modes:

**Draft mode** (default; what `--publish` does without `--auto-publish`):
- `publishedAt: null` in the payload
- Article enters Strapi as a draft
- Editor reviews in admin, hand-edits, captures any remaining screenshot placeholders into media library, then clicks Publish
- The human checkpoint is where the last 20% of quality lives

**Auto-publish mode** (`--auto-publish` flag, or `BLOG_AGENT_AUTO_PUBLISH=1` env var):
- `publishedAt` set to the current ISO timestamp in the payload
- Article goes live on Strapi immediately
- Required for `/auto-blog-loop` autonomous mode (no human in the loop, by design)
- Compensating control: a quality precondition gate (see "Quality precondition" below) refuses to publish if the upstream `/quality-check` verdict is FAIL — belt-and-suspenders even if the orchestrator is misconfigured

Pick auto-publish for the cron-driven `/auto-blog-loop` path. Pick draft mode for one-off manual runs where an editor is going to review.

## Quality precondition (auto-publish only)

Before issuing the Strapi POST when `--auto-publish` is set, the script re-reads `content-pipeline/quality-checks/{slug}.md` and parses the verdict line. If the verdict is FAIL OR if the file is missing, the script refuses to publish, exits non-zero, and prints the reason. The orchestrator will then quarantine the slug. This is a safety net — `/blog-pipeline` should never call `/format-for-publish --auto-publish` on a FAIL'd article, but the precondition makes a misconfigured orchestrator harmless.

## Publish gate (PLEAA-581) — artifact must be on `origin/main`

`--publish` and `--auto-publish` both run an artifact precondition before any HTTP write to Strapi (`POST /api/articles`, `PUT /api/articles/{id}`, `POST /api/upload`). The script verifies:

1. `content-pipeline/8-publish/{slug}/article.json` exists locally, AND
2. The same path is present in `origin/main` HEAD (`git ls-tree -r origin/main -- <path>` returns a non-empty line).

Both must hold. If either check fails the script exits non-zero with a `publish gate REJECT` message that names the missing artifact and links `/blog-pipeline`. This is a HARD gate, not a warning — `--auto-publish` is no longer allowed to write to Strapi for a slug whose package isn't committed and pushed.

### Override: `--human-approved "<reason>"`

The only escape hatch is `--human-approved "<reason>"` (required, non-empty). When set, the script:

- skips the artifact check,
- appends one tab-separated line to `content-pipeline/audit/publish-overrides.log` with: ISO timestamp, slug, reason, `git config user.email`, current branch, HEAD sha,
- prints `publish gate OVERRIDDEN — reason=...` to stderr,
- proceeds with the publish flow.

Use the override only for legitimate one-off operations like a manual unpublish/reseed or a hotfix where the package can't be committed first. Every override is forensically recoverable from the audit log. The log file is gitignored (per-environment append-only); rotate it to long-term storage via your own retention policy if you need an organization-wide trail.

### Why this exists

PLEAA-577 (root cause + audit) traced an incident where eight Strapi articles went live without ever passing through `/blog-pipeline` — the Strapi UI / API token had publish authority with nothing local to gate against. Layer 1 of [PLEAA-581](https://github.com/lionelndong/blog-agent-2/blob/main/.claude/skills/format-for-publish/SKILL.md#publish-gate-pleaa-581) is the client-side belt: a `--publish` call without an artifact in `origin/main` is now refused at the script level. Layers 2 (Supabase approval registry + edge-function gate) and 3 (Strapi token surface reduction) live server-side and continue to enforce the same rule even when this script is bypassed.

### `manifest.json` (Layer 2 hook)

Every run of `format_for_strapi.py` writes `content-pipeline/8-publish/{slug}/manifest.json` alongside `article.md` / `article.json` / `README.md`. The file is small (`slug`, `title`, `pipeline_run_id`, `approved_by`, `generated_at`) and is the source-of-truth artifact that the `sync-publish-approvals.yml` GitHub Action upserts into the Supabase `blog_publish_approvals` registry on push to `main`. The edge function (`sync-blog-posts`) then refuses any Strapi `entry.publish` webhook whose slug has no registry row.

## Whiteboard staging (PLEAA-448)

After the publish package is written (and any Strapi POST has run), the script bakes the GitHub-Pages whiteboard artifacts for the slug:

1. Calls `scripts/bundle_viewer.py <slug>` → writes `docs/run-<slug>.html` (self-contained offline viewer with every stage's content inlined).
2. Idempotently appends `"<slug>"` to the fallback runs array in `docs/index.html` (the `catch (e) { return [...] }` block at ~line 197). If the slug is already there, the file is not rewritten.
3. Best-effort `git add docs/run-<slug>.html docs/index.html` so one `git commit && git push` from the operator surfaces the run at https://lionelndong.github.io/blog-agent-2/ within ~1 minute.

This step is best-effort — any failure prints a warning and the operator can re-run `python scripts/bundle_viewer.py <slug>` manually. Set `BLOG_AGENT_SKIP_WHITEBOARD=1` to disable (e.g. for one-off non-board runs).
