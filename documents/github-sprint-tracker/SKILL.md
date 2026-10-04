---
name: github-sprint-tracker
description: >
  Summarizes pull requests without Jira reference over a sprint period into Markdown and PDF reports.
  Trigger on: "sprint summary", "résumé du sprint", "PR sans ticket", "sprint tracker",
  "génère le résumé du sprint", "quelles PR sans Jira", "summary of PRs without tickets",
  "PRs hors Jira du sprint".
  Requires GitHub MCP and Jira MCP to be configured.
  Uses md-to-pdf (must be installed locally) for PDF export.
---

## Purpose

Generate a sprint summary report listing all pull requests created or merged during a sprint
that do **not** reference a Jira ticket. The report is produced as both Markdown and PDF files,
grouped by merge status and target branch.

This is a **read-only** skill — it never creates, modifies, or closes any PR or issue.

---

## GitHub repository

This project is always hosted at:

- **owner**: `faberNovel`
- **repo**: `idf-subventionjeunes-web`

Use these values for all GitHub MCP calls. Never guess or ask the user.

---

## Inputs to collect

Two modes are supported. **Mode A (sprint number)** is the default.

### Mode A — Sprint number (default)

The user provides the number of the sprint that just ended or is about to end (e.g. "Sprint 36",
or simply "36"). If the user does not specify a sprint number, ask for it.

Once you have the sprint number, resolve the sprint dates via Jira MCP:

1. Call `mcp_sooperset_mcp_jira_search` with:
   - `jql`: `sprint = "Sprint <N>" AND project = IDF`
   - `fields`: `sprint`
   - `limit`: 1
2. In the returned issue, read the `sprint` field (array of sprint objects). Find the one whose
   `name` matches `Sprint <N>`. Extract its `startDate` and `endDate`.
3. If no issue is returned or the sprint object has no dates, tell the user the sprint was not
   found in Jira and ask them to provide explicit dates (→ Mode B).

Derived variables:

- `sprint_name` — e.g. `Sprint 36`
- `start_date` — the sprint's `startDate` (format: `YYYY-MM-DD`)
- `end_date` — the sprint's `endDate` (format: `YYYY-MM-DD`)

### Mode B — Explicit dates (fallback)

The user explicitly provides two dates. Snap each to the nearest Tuesday (midnight).

Validate that the two dates are roughly **2 weeks apart** (±3 days). If they are wildly off,
warn the user and ask to confirm before continuing.

Derived variables:

- `sprint_name` — `Sprint` (omitted; folder/file names use dates only)
- `start_date` — nearest Tuesday to the user-provided start date (format: `YYYY-MM-DD`)
- `end_date` — nearest Tuesday to the user-provided end date (format: `YYYY-MM-DD`)

---

## Step 1 — Fetch pull requests via GitHub MCP

Use `mcp_github_search_issues` to retrieve PRs in the date range. Run **two searches**:

### 1a — PRs created in the date range

```
q: "repo:faberNovel/idf-subventionjeunes-web is:pr created:<start_date>..<end_date>"
per_page: 100
sort: created
order: asc
```

### 1b — PRs merged in the date range

```
q: "repo:faberNovel/idf-subventionjeunes-web is:pr merged:<start_date>..<end_date>"
per_page: 100
sort: created
order: asc
```

Deduplicate results across both queries (a PR may appear in both if it was created and merged
within the sprint).

### 1c — Fetch full details for each PR

For each unique PR found, call `mcp_github_get_pull_request` to retrieve full details including:

- `base` branch name
- `merged_at` timestamp
- `body` (full description)
- `user` (author)

This step is necessary because search results do not include the target branch.

---

## Step 2 — Filter and classify

### Filter out Jira-referenced PRs

Discard any PR whose **title** or **body** contains a Jira ticket reference matching the
pattern `IDF-\d+` (case-insensitive). A single PR may reference multiple tickets — if any
reference is found, it is excluded from the report.

### Classify remaining PRs

Split the remaining PRs into two groups:

- **Merged** — PRs with a non-null `merged_at` date within the sprint range
- **Opened** — PRs that were created in the range but are still open (not merged)

### Sort

- Merged PRs: sorted by `merged_at` ascending
- Opened PRs: sorted by `created_at` ascending

### Summarize

For each PR, generate a `short_description` — a concise, informative summary of the PR in ≤ 200
characters, derived from the PR body. If the body is empty, use the PR title as fallback.

---

## Step 3 — Generate the Markdown report

Create a folder and write the Markdown file inside.

When `sprint_name` is known (Mode A):

- **Folder:** `sprint-summary-sprint-<N>-<start_date>-<end_date>/`
- **File:** `pr-summary_sprint-<N>_<start_date>_<end_date>.md`

When using explicit dates only (Mode B):

- **Folder:** `sprint-summary-<start_date>-<end_date>/`
- **File:** `pr-summary_<start_date>_<end_date>.md`

### Report structure

```markdown
# Pull Request Summary - Sprint <N> (<start_date> to <end_date>)

## Merged

### Target branch `main`

| GitHub Link | Target Branch | PR Author | Opening Date | Merge Date | PR Title | Short Description |
| ----------- | ------------- | --------- | ------------ | ---------- | -------- | ----------------- |
| [#NNN](url) | main          | Author    | YYYY-MM-DD   | YYYY-MM-DD | Title    | Description       |

<Page break between each target branch section>

### Target branch `feature/some-feature`

| GitHub Link | Target Branch | PR Author | Opening Date | Merge Date | PR Title | Short Description |
| ----------- | ------------- | --------- | ------------ | ---------- | -------- | ----------------- |
| [#NNN](url) | branch-name   | Author    | YYYY-MM-DD   | YYYY-MM-DD | Title    | Description       |

<Page break between each target branch section>

## Opened pull requests

| GitHub Link | Target Branch | PR Author | Opening Date | PR Title | Short Description |
| ----------- | ------------- | --------- | ------------ | -------- | ----------------- |
| [#NNN](url) | branch-name   | Author    | YYYY-MM-DD   | Title    | Description       |
```

Rules:

- Group merged PRs by **target branch**, with `main` first, then other branches alphabetically
- Add a page break between each target-branch section
- Opened PRs are listed in a single flat table (no branch grouping)
- If a section is empty, still include the heading with a note: _"No pull requests in this category."_

---

## Step 4 — Generate the PDF report

Run the following command in the terminal to generate the PDF from the Markdown file:

```bash
cd <folder> && npx md-to-pdf <markdown-file> --pdf-options '{"landscape": true}'
```

Use the folder and file names determined in Step 3 (sprint-aware or date-only).

`md-to-pdf` should already be installed locally. If the command fails, tell the user to install
it with `npm install -g md-to-pdf` and retry.

---

## Step 5 — Present the results

Confirm to the user with:

- Number of PRs found (total, merged, opened)
- Number of PRs excluded (Jira-referenced)
- Path to the Markdown file
- Path to the PDF file

---

## Rules

- Never create, modify, or close PRs — this skill is **strictly read-only**.
- Never query more than 100 PRs per search call. Sprints never produce that many.
- All data processing (filtering, classification, summarization) is done by the agent directly —
  do not generate or run external scripts (Node.js, Python, etc.) for data manipulation.
- The only terminal command allowed is `md-to-pdf` for PDF generation (no need for `npx` prefix)
- If the GitHub MCP is unavailable, tell the user and stop. Do not fall back to `gh` CLI.
- If the Jira MCP is unavailable and the user provided a sprint number, tell the user and ask
  for explicit dates instead (Mode B).

## Jira ticket reference pattern

Jira tickets follow the pattern `IDF-\d+` (e.g. `IDF-1573`). This pattern is used for exclusion
filtering only.

## Absolute restrictions — never do this

- **Never create, update, or close a pull request** — this is a reporting skill
- **Never create, update, or close a GitHub issue** — fully out of scope
- **Never push code or create branches** — no write operations on the repository
- **Never modify repository settings** — no admin operations
- **Never create, update, or close a Jira ticket or sprint** — Jira is used for reading sprint dates only
