---
name: md-to-confluence
created_by: Aman Parmar
last_modified: 19-04-2026
description: |
  Push markdown files to Confluence - update existing pages or create new ones under a parent page.
  Use this skill whenever the user wants to publish markdown to Confluence, update a Confluence page
  from a local .md file, create new Confluence pages, or batch-create pages. Also triggers on "push
  to confluence", "update confluence page", "create confluence page", "publish to confluence",
  "sync to confluence", or any mention of uploading/pushing markdown content to Confluence. Use this
  even when the user says "put this on confluence" or "make a confluence page for this".
---

# Markdown to Confluence

Push local markdown to Confluence - update existing pages or create new ones. The bundled script
handles pandoc conversion, image uploads, Confluence macro formatting, and wide mode. It avoids
the many pitfalls of Confluence's storage format so you don't have to build HTML manually.

## Quick start

```bash
# Update existing page
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py <page_id> <markdown_file>

# Create new page under a parent
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py --create --parent-id <parent_id> --space <SPACE_KEY> <markdown_file> --wide

# Batch create
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py --create --parent-id <parent_id> --space <SPACE_KEY> file1.md file2.md --wide
```

The script auto-loads credentials from `.env` at the project root.

## Workflow

### Step 0: Preflight check (MANDATORY for updates — skip for --create)

Before updating an existing page, ALWAYS run the preflight. It detects whether
anyone edited the page directly on Confluence since your last sync — so you
don't silently overwrite their changes.

```bash
python3 .claude/skills/md-to-confluence/scripts/confluence-preflight.py <page_id> <local.md>
```

Exit codes:
- **0** — Safe to push. Continue to Step 1.
- **1** — CONFLICT. Confluence has edits your local .md is missing. STOP.
  Pull Confluence into a temp file, merge the missing content into your .md,
  re-run preflight until it returns 0.
- **2** — Error running the check (credentials, network, etc.).

How snapshots work (Git-style 3-way diff):
- Every successful push (md-to-confluence) saves the pushed .md as a baseline
- Every successful pull (confluence-to-md) saves the pulled .md as a baseline
- Stored at `.local/confluence-snapshots/<page_id>.md` (auto-created, gitignored)
- Preflight compares: YOUR changes (local vs baseline) vs THEIR changes
  (Confluence vs baseline). If THEIR changes is non-empty, pushing would
  overwrite those edits.

First-time push (no baseline yet): preflight falls back to a 2-way diff and
prints a warning. The baseline is auto-created after the push succeeds, so
subsequent pushes have the full 3-way protection.

Use `--show-diff` to see full diffs inline; use `--force` only if you have
explicitly verified the Confluence-side changes and decided to overwrite.

### Step 1: Determine the mode

**Update** - user has an existing page URL:
```
https://[your-instance].atlassian.net/wiki/spaces/[SPACE]/pages/1234567890/Page+Title
                                                                ^^^^^^^^^^ page ID
```

**Create** - user wants a new page. You need:
- `--parent-id` (from the parent page URL)
- `--space` key (the Confluence space key for your project)

### Step 2: Run the script

```bash
# Update with title change and wide mode
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py 1234567890 my-doc.md --title "New Title" --wide

# Create under parent with auto-title (extracted from first H1)
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py --create --parent-id 9876543210 --space [SPACE_KEY] guide.md --wide

# Dry run first
python3 .claude/skills/md-to-confluence/scripts/md-to-confluence.py 1234567890 my-doc.md --dry-run
```

### Step 3: Post-push verification (EVALS)

After every push, verify these automatically:

1. **No duplicate H1** — Confluence page title IS the H1. If the markdown starts with `# Title`, the
   script strips it. Verify: fetch `body.storage` and confirm no `<h1>` tag exists (Confluence adds
   its own page title separately).
2. **No Source callout** — The `> Source: [Confluence](...)` line in markdown is a local-only reference.
   The script strips it. Verify: fetch `body.storage` and confirm no "Source:" info panel or blockquote.
3. **Numbering columns present** — All tables should have auto-numbering. Verify: fetch `body.storage`
   and confirm `<th class="numberingColumn">` exists in every `<table>`.
4. **Wide tables** — Verify: `data-table-width="1800"` and `data-layout="wide"` on every `<table>`.
5. **No broken images** — For pages with images, verify all `<ri:attachment ri:filename="...">` have
   matching attachments on the page.
6. **@mentions** — The script auto-converts `@Name` to `<ac:link><ri:user>` macros by looking up
   account IDs from `.local/team/users.md`. Handles pandoc's citation span wrapping (`<span class="citation" data-cites="Name">@Name</span>`).
   Verify: no `@Name` plain text or `class="citation"` remains.
7. **TOC macro** — Auto-added at the top (H1-H3). Verify: `ac:name="toc"` present.
8. **Versioning table subtext** — Grey italic description text below "Versioning" heading.
   Verify: "version control and releases management" in HTML.
9. **Versioning table grey headers** — `data-highlight-colour="#b3bac5"` on versioning table `<th>` cells.
   Verify: attribute present on non-numberingColumn headers.
10. **Date macros in versioning** — DD-MM-YYYY dates in the versioning table become `<time datetime="YYYY-MM-DD" />`
    macros (styled date pill). Verify: `<time datetime=` in HTML.

```bash
# Quick eval: fetch page and check for common issues (9 checks)
python3 -c "
import http.client, json, os, base64
email = os.environ.get('CONFLUENCE_EMAIL', '')
token = os.environ.get('CONFLUENCE_TOKEN', '')
auth = base64.b64encode(f'{email}:{token}'.encode()).decode()
base_url = os.environ.get('CONFLUENCE_BASE_URL', '').replace('https://', '').rstrip('/')
conn = http.client.HTTPSConnection(base_url)
conn.request('GET', '/wiki/rest/api/content/PAGE_ID?expand=body.storage',
             headers={'Authorization': f'Basic {auth}'})
html = json.loads(conn.getresponse().read())['body']['storage']['value']
checks = []
checks.append(('No duplicate H1', '<h1' not in html))
checks.append(('Numbering columns', 'numberingColumn' in html))
checks.append(('Wide tables', 'data-table-width' in html))
checks.append(('No plain @mentions', 'citation' not in html))
checks.append(('TOC macro', 'ac:name=\"toc\"' in html))
checks.append(('Versioning subtext', 'version control and releases management' in html))
checks.append(('Grey headers', 'data-highlight-colour' in html))
checks.append(('Date macros', '<time datetime' in html))
checks.append(('No broken images', 'UNKNOWN_ATTACHMENT' not in html))
for name, passed in checks:
    print(f'{\"PASS\" if passed else \"FAIL\"}: {name}')
print(f'{sum(1 for _,p in checks if p)}/{len(checks)} checks passed')
"
```

## What the script handles

- **Pandoc with `--wrap=none`** - prevents premature line breaks that Confluence renders literally
- **Images** - detects `![](path)` refs, uploads missing attachments, converts to `<ac:image>` macros at `ac:width="1350"` (fills the wide content area). After creating a page, re-pushes HTML so image refs resolve against uploaded attachments (prevents `UNKNOWN_ATTACHMENT` bug).
- **Callout panels** - blockquotes with `**bold label:**` become Confluence info/note panels
- **Code blocks** - `<pre><code>` becomes Confluence code macro with CDATA
- **Wide tables** - all tables get `data-table-width="1800" data-layout="wide"` and `data-number-column="true"` for full width with numbered rows
- **Manual `#` column stripping** - auto-strips manual `| # |`, `| Sr |`, `| S# |` first columns from tables before adding Confluence numbering (prevents duplicate row numbers). Keep `#` columns in markdown for local readability — the script handles it.
- **Numbering columns** - auto-adds Confluence numbering column (`numberingColumn` class) to all tables — header gets empty `<th>`, data rows get sequential `<td>` numbers
- **H1 stripping** - removes the first `<h1>` from HTML output since Confluence uses the page title as H1 (avoids duplicate heading)
- **Source callout stripping** - removes `> Source: [Confluence](...)` info panels/blockquotes that are only meaningful in local markdown
- **Bold headers** - `<th>` content is wrapped in `<strong>` so header row text renders bold
- **Figure stripping** - removes pandoc's figure/figcaption wrappers that cause visible caption boxes
- **Wide mode** - `--wide` flag sets both draft and published content appearance properties
- **@mentions** - converts `@Name` to Confluence user mention macros using `.local/team/users.md` lookup. Handles pandoc's citation span wrapping automatically.
- **TOC macro** - auto-adds Table of Contents (H1-H3) at the top of every page
- **Versioning table formatting** - adds grey italic subtext and dark grey header row background (matching 10x SPEC template)
- **Date macros** - converts ALL DD-MM-YYYY dates (anywhere on the page, not just versioning tables) to Confluence native `<time>` date pills. Keep plain dates in markdown for local readability — the script converts them on push.

## Key things to know

**Pandoc column widths are the #1 table gotcha.** Pandoc generates equal-percentage `<col>` widths
(e.g., 7 columns = 14% each). This makes ALL columns the same width regardless of content — a
short "Type" column gets the same width as a long "Rationale" column. The script now replaces
pandoc's `<colgroup>` with proportional pixel-based widths using a heuristic: columns with short
header names (< 10 chars) like "Type", "#", "Count" get narrow widths; columns with known long-
content names like "Rationale", "Summary", "Reason", "Description" get wide widths. If the auto-
heuristic is wrong, fix column widths post-push by replacing the `<colgroup>` block via REST API
with `<col style="width: Npx;" />` values that match the content. Confluence uses pixel widths
in `<col>` tags inside `<colgroup>`, NOT `data-colwidth` on `<td>`/`<th>` cells.

**Manual `#` columns are auto-stripped.** The script detects manual numbering columns (`| # |`,
`| Sr |`, `| S# |`, `| S.No |`) and removes them before adding Confluence's built-in
`numberingColumn`. Keep `#` columns in your markdown for local readability — the script handles
the deduplication automatically.

**Pandoc line wrapping is the #2 gotcha.** Without `--wrap=none`, pandoc breaks lines at ~72 chars
and Confluence renders those as actual line breaks. The script already handles this, but if you ever
call pandoc directly, always include `--wrap=none`.

**Paragraph width is a Confluence design decision.** Even in wide mode, paragraph text constrains to
~740px readable width. Only tables expand with `data-layout="wide"`. This is how Confluence works -
it's not a bug.

**Single newlines in markdown merge into one paragraph.** Pandoc treats a single newline as a space,
not a line break. If you have Q&A pairs (`**Q:**\nA:`) or intro text followed by a numbered list,
they'll render on the same line in Confluence. Always use **blank lines** between elements that
should be separate paragraphs - e.g., between a question and its answer, or between intro text
and a numbered/bulleted list.

**Duplicate titles cause errors.** Confluence rejects creating a page if another page with the same
title exists in the space. The script reports the 400 error clearly.

**Fabric editor rejects inline code in tables.** Confluence's new Fabric editor throws
`BAD_REQUEST: Content contains unsupported extensions` when HTML contains `<code>` tags inside
`<table>` cells. The fix: replace all backtick code spans in markdown with bold (`**text**`)
before running pandoc. The script should strip `<code>` tags from table cells and wrap the content
in `<strong>` instead. If the script fails with this error, manually replace backticks in the
markdown source and retry.

**Fabric editor rejects `--create` but accepts updates.** The v2 page creation API
(`POST /wiki/api/v2/pages`) uses the Fabric editor which rejects `<code>` tags in tables,
`numberingColumn`, and `colgroup`. However, updating an existing page via the v1 API
(`PUT /wiki/rest/api/content/{id}`) works fine and preserves all formatting. Workaround for
`--create` failures: create the page manually via v1 API with minimal HTML, then immediately
update it using the script. The script's update path handles numbering, colgroups, and all
post-processing correctly.

**Relative links MUST be fixed in the source .md, not in post-processing HTML.** When markdown
references other spec files via relative paths (e.g., `../011-p2p-peer-to-peer-sync/p2p-peer-to-peer-sync.md`),
these render as broken links on Confluence. Fixing them only in the pushed HTML is NOT sufficient
because the next full push regenerates HTML from the unchanged .md, bringing broken links back.

Before pushing, grep the markdown for `../` relative links and replace them IN THE .MD FILE with
the full Confluence URL from each target spec's header line (`> Source: [Confluence](url)` or
`> Confluence: url`). This is a one-time fix per file - once the .md has absolute Confluence URLs,
all future pushes will be correct.

Check: `grep '\.\.\/' <file.md>` - if any matches, fix them before pushing.

For the full list of Confluence storage format details (image format, callout panels, code blocks,
status badges, @mentions, colored cells, TOC macros), read `references/confluence-format-guide.md`.

## @mentions — ALWAYS convert names to @mentions on Confluence

Whether a name appears as plain text ("Jane Doe") or with `@` prefix ("@Jane Doe") in the
local .md file, it MUST render as a Confluence @mention macro on the pushed page. Plain text names
are not acceptable on Confluence.

The script handles `@Name` patterns automatically. For plain text names (e.g., in Attendees lines
of decisions.md), do a **post-push find-replace**:

1. Push the page with the script first
2. Fetch the pushed page's `body.storage` via REST API
3. Look up user account IDs from `.local/team/users.md`
4. Find-replace each known team member name with `<ac:link><ri:user ri:account-id="ACCOUNT_ID" /></ac:link>`
5. PUT the modified HTML back via REST API (increment version number)

Sort names by length (longest first) to avoid partial matches (e.g., "Jane Doe" before "Jane").

## STOP: Check before full-page push (MANDATORY)

This script does a **full page replacement**. Pandoc CANNOT preserve Confluence-native macros:
- Jira smart links (`<ac:structured-macro ac:name="jira">`) become broken UUID text
- Images (`<ac:image>`) are lost
- Status badges (`<ac:structured-macro ac:name="status">`) become plain text
- Expand macros, @mentions, and other Confluence macros are destroyed

**Before pushing to ANY existing page, check:**
1. Does the page have Jira smart links, images, status badges, or macros? If YES, **do NOT use this script**
2. Instead, use `confluence-update.py` for surgical updates:
   - `add-section` — add a new section before/after a heading
   - `find-replace` — replace specific text
   - `add-table-row` — add a versioning row
   - `insert` — add an info callout before specific text

**This script is ONLY safe for:**
- Brand new pages being created for the first time (`--create`)
- Pages where the local .md is the SOLE source of truth (never edited on Confluence)

**Real incident:** A full push to a dashboard page destroyed 12 images, 2 status badges, and 15 Jira smart links. Required reverting to a previous version and re-adding content surgically.

## Overwriting user's manual Confluence edits

Use Step 0 (`confluence-preflight.py`) — it's the enforced version of this check.
The preflight does a 3-way diff against the snapshot baseline and fails loudly
if anyone has edited the page on Confluence since your last sync.

Real incident: a full-page push via this script removed answers that a reviewer
had typed directly on the Confluence page. The snapshot + preflight system
exists to make this class of failure detectable before the push.

## Script location (IMPORTANT)

Scripts live INSIDE the skill folder, NOT in a shared `.claude/scripts/` folder:
- **Project**: `.claude/skills/md-to-confluence/scripts/md-to-confluence.py`
- **Global**: `~/.claude/skills/md-to-confluence/scripts/md-to-confluence.py`

**NEVER use symlinks** — always copy actual Python files. Symlinks break when the target moves.

Keep both locations in sync when modifying the script.

## Dependencies

- Python 3 (standard library only)
- Pandoc (`brew install pandoc`)
- `.env` with: `CONFLUENCE_EMAIL`, `CONFLUENCE_TOKEN`, `CONFLUENCE_BASE_URL`
