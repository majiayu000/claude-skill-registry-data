---
name: change-amplification
description: >
  Detect change amplification — Ousterhout's clearest signal of bad architecture —
  by fetching the last N merged PRs from the current git repo and analysing them
  for conceptual changes that forced edits across scattered files because no module
  owned the decision. Produces a ranked architectural debt backlog with PR links
  as evidence and concrete remediation steps. Use when asked to "find change
  amplification", "analyse PR history for architecture debt", "detect missing
  boundaries", "find architectural debt in my PRs", or invokes
  /change-amplification.
---

# Change Amplification Skill

Analyses merged pull requests as **architecture evidence**. One intended change
forcing edits across conceptually separate files, tests, configs, prompts, and
docs is Ousterhout's *change amplification* — the clearest symptom that a module
boundary, contract, or owner is missing.

This skill fetches the last N merged PRs from the current git repo (default 50),
formats each as a structured context block, applies a structured LLM analysis
lens, and writes a ranked architectural debt backlog to the Obsidian vault.

---

## Intellectual Grounding

> "Change amplification: a seemingly simple change requires code modifications
> in many different places."
> — John Ousterhout, *A Philosophy of Software Design* (2018), §2

The root cause is always the same: a design decision is not hidden inside one
module. Instead it leaks across many. David Parnas (1971) named the fix:
*information hiding* — if a decision must be revisited, exactly one module
should change.

Adam Tornhill's *change coupling* (CodeScene, *Software Design X-Rays*)
detects the same problem structurally — files that co-commit repeatedly are
logically coupled regardless of what the architecture claims. This skill adds
the semantic layer: it uses PR **intent** (title + description) as the signal
to distinguish *amplification* (scattered edits for one conceptual reason) from
*justified breadth* (a genuinely cross-cutting feature).

---

## Prerequisites

| Requirement | Details |
|---|---|
| `GITHUB_TOKEN` | Personal access token with `repo` scope (read-only is fine) |
| Current directory | Must be inside a git repo with a GitHub remote (`origin`) |
| Anthropic API | The analysing agent (this session) handles LLM inference — no separate call needed |

---

## Workflow

### Step 1 — Detect the repo

Run this exactly:

```bash
git remote get-url origin 2>/dev/null
```

Parse the output to extract `OWNER` and `REPO`:
- SSH format: `git@github.com:OWNER/REPO.git`
- HTTPS format: `https://github.com/OWNER/REPO.git` or `https://github.com/OWNER/REPO`

Strip the `.git` suffix. If the remote is not a GitHub URL, abort with:
> "This skill requires a GitHub remote. Found: {remote}. Set origin to a
> github.com URL or provide the repo as `owner/repo`."

If no remote is found, ask:
> "No git remote detected. Please provide the target repo as `owner/repo`."

---

### Step 2 — Auto-discover domain structure and ask for clarification

Before fetching any PRs, build a picture of the codebase's module structure
and ask the user to confirm or correct it. The LLM cannot reliably classify
files as `CORE` vs `AMPLIFIED` without knowing the codebase's bounded contexts.
This step is mandatory — do not skip it even if the auto-discovery looks complete.

**2a — Auto-discover**

Run these in parallel:

```bash
# Top-level source directories (the coarsest module map)
find . -maxdepth 3 -type f -name 'package.json' ! -path '*/node_modules/*' \
  | head -30

# CODEOWNERS — explicit ownership map
cat .github/CODEOWNERS 2>/dev/null || cat CODEOWNERS 2>/dev/null

# Workspace / monorepo config
cat package.json 2>/dev/null | python3 -c "
import sys,json; d=json.load(sys.stdin); print(d.get('workspaces',''))
" 2>/dev/null
cat pnpm-workspace.yaml 2>/dev/null
cat lerna.json 2>/dev/null

# ADRs — architectural decisions already recorded
ls docs/adr/ 2>/dev/null || ls doc/adr/ 2>/dev/null || ls adr/ 2>/dev/null

# CONTEXT.md — domain glossary (pi/grill-with-docs convention)
cat CONTEXT.md 2>/dev/null | head -80

# Top-level source tree (2 levels deep, dirs only)
find . -maxdepth 2 -mindepth 1 -type d \
  ! -path '*/.git/*' ! -path '*/node_modules/*' ! -path '*/.next/*' \
  ! -path '*/dist/*'  ! -path '*/__pycache__/*' ! -path '*/target/*' \
  | sort | head -60
```

**2b — Present findings and ask**

Summarise what you found into a short domain map. Then ask the user this
exactly — do not proceed until you have an answer:

---

> Before I analyse the PRs I need to understand your module boundaries.
> I've inferred the following structure from the repo:
>
> ```
> {auto-discovered module list, one entry per line, e.g.:
>   src/referral/      — Referral domain
>   src/appointment/   — Appointment domain
>   src/billing/       — Billing domain
>   infra/             — Infrastructure / CDK
>   shared/            — Shared utilities
> }
> ```
>
> **Is this the right bounded-context map?**
> Please:
> 1. Correct any module whose boundary or name is wrong.
> 2. Add any modules not listed (e.g. shared kernels, platform services,
>    third-party integrations that count as a separate context).
> 3. Flag any two modules that are *intentionally* tightly coupled so I
>    don't flag changes between them as amplification.
> 4. Describe in one sentence the architectural style (e.g. modular monolith,
>    microservices, layered monolith, event-driven) — this affects what
>    "cross-boundary" means.
>
> Once you confirm, I'll fetch and analyse the PRs.

---

Wait for the user's response. Incorporate all corrections into the **confirmed
domain map** before continuing. Store it as a variable — it will be prepended
to the analysis prompt in Step 6.

---

### Step 3 — Fetch merged PRs

Fetch the last **N** merged PRs (default 50; use whatever the user specified).

Use the **Search API** — not the pulls list endpoint. The pulls list endpoint
sorted by `updated` returns the most recently *commented-on* closed PRs, not
the most recently *merged* ones. The search API with `is:merged` returns only
merged PRs, sorted by creation date.

```bash
N=50  # replace with user-specified count

curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/search/issues?q=repo:{OWNER}/{REPO}+is:pr+is:merged&sort=created&order=desc&per_page=${N}" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('items', [])
for p in items:
    print(json.dumps({
        'number': p['number'],
        'title': p['title'],
        'body': (p.get('body') or '')[:500],
        'merged_at': p.get('pull_request', {}).get('merged_at', ''),
        'url': p['html_url'],
        'author': p['user']['login']
    }))
"
```

> **Note:** The Search API response does not include `additions`, `deletions`,
> or `changed_files` at the list level. Those stats are fetched per-PR in
> Step 4 alongside the file list — one request covers both.

> **Rate limits:** The Search API allows 30 requests/minute authenticated.
> If N > 100, page through using `&page=2`, `&page=3` etc. (`per_page` max
> is 100). Pause 2 seconds between pages to stay under the rate limit.

---

### Step 4 — Fetch PR detail and changed files

For each PR number collected in Step 3, make **two parallel requests**:

1. **PR detail** — provides `additions`, `deletions`, `changed_files` totals:
   ```
   GET /repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}
   ```

2. **File list** — provides per-file stats:
   ```
   GET /repos/{OWNER}/{REPO}/pulls/{PR_NUMBER}/files?per_page=100
   ```

Batch up to 10 PR numbers simultaneously using `&` and `wait` in bash.

```bash
fetch_pr() {
  PR=$1
  DETAIL=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/{OWNER}/{REPO}/pulls/${PR}")

  FILES=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/{OWNER}/{REPO}/pulls/${PR}/files?per_page=100")

  python3 -c "
import sys, json
detail = $DETAIL_JSON
files  = $FILES_JSON
print('additions:', detail.get('additions', 0))
print('deletions:', detail.get('deletions', 0))
print('changed_files:', detail.get('changed_files', 0))
for f in files:
    print(f\"{f['additions']:+d}/{f['deletions']:+d}  {f['filename']}\")
"
}
```

> **Implementation note:** Pass `DETAIL` and `FILES` as shell variables into
> the python3 call using process substitution or temp files — do not inline
> raw JSON directly into `-c` strings. Write to a temp file per PR and
> aggregate after all background jobs finish.

Cap at 100 files per PR. If `changed_files` > 100, mark the PR auto-excluded
before fetching its file list — save the API call entirely.

---

### Step 5 — Pre-filter structural noise

Exclude only PRs that are **unambiguously unanalysable regardless of content**.
Do not exclude on title keywords — that job belongs to Pass 1 triage, which
has domain context and semantic reasoning. Keyword filters produce false
exclusions (a PR titled "Migrate referral expiry" may be a genuine amplification
candidate) and add no signal that triage does not already provide.

**Auto-exclude if and only if:**

1. **`changed_files` > 100** — almost certainly generated code, a lock file
   explosion, or a mass rename. The file list is too large for meaningful
   per-file classification and was already skipped in Step 4.

2. **Author is a known bot account** — match against:
   `dependabot[bot]`, `renovate[bot]`, `github-actions[bot]`,
   `snyk-bot`, `semantic-release-bot`. These PRs contain no intentional
   conceptual change authored by a human.

For every excluded PR, record: PR number, title, author, reason for exclusion.
Show this list at the start of the report. These are not bad PRs — they are
structurally unanalysable. Everything else, including refactors and chores,
goes to triage in Pass 1 where the LLM decides.

---

### Step 6 — Format the analysis batch

Assemble the surviving PRs into a single structured context block:

```
=== PR #{number} ===
URL: {url}
Author: {author}
Merged: {merged_at}
Title: {title}
Description: {body (first 500 chars, stripped of markdown)}
Total: +{additions}/-{deletions} across {changed_files} files

Files changed:
  {+additions/-deletions}  {filename}
  {+additions/-deletions}  {filename}
  ...
```

One block per PR. Separate blocks with a blank line. Do NOT include diff
content — file paths and stats are the signal.

---

### Step 7 — Analyse: two-pass approach

Do not send all PRs to a single analysis call. Analysis quality degrades on
large batches — items in the middle get shallower treatment and the final
Patterns synthesis is written at peak attention dilution.

Use three focused passes instead.

---

#### Pass 1 — Triage (all N PRs, one call)

Send the full formatted batch from Step 6. Ask only for a triage table.
Prepend the confirmed domain map.

```
You are an architecture reviewer. The team has confirmed the following
bounded-context map for this codebase:

{CONFIRMED DOMAIN MAP — verbatim from Step 2}

Architectural style: {user's one-sentence description}

Intentionally coupled module pairs (do NOT flag changes between these):
{list from user, or "none specified"}

Use this map to classify files. A file is AMPLIFIED only if it lives in a
different bounded context than the intended change's primary context.
Do not infer contexts from file paths alone — use the confirmed map.

---

Below is a batch of merged pull requests. For each PR, output exactly one
row in this markdown table and nothing else:

| PR | Title | Severity | Justified | One-line reason |
|----|-------|----------|-----------|----------------|

Severity scale:
  1 = CORE-only — no amplification
  2 = TEST alongside CORE — expected
  3 = 1–2 AMPLIFIED files — possibly justifiable
  4 = 3+ AMPLIFIED files OR CONFIG+CORE+TEST all touched
  5 = AMPLIFIED files span multiple bounded contexts

Justified: YES or NO.
  YES if: the breadth is explained by the PR description, the change is
  genuinely cross-cutting by nature, or a single well-placed abstraction
  could NOT have kept it local.
  NO if: a missing owner, contract, or boundary caused the spread.

One-line reason: for severity ≥ 3, name the missing boundary in one sentence.
For justified PRs, state why it was justified.

Output the table only. No prose, no headers, no commentary.

{PR BATCH}
```

Collect the triage table. Extract all rows where **Severity ≥ 3 AND Justified
= NO**. These are the **deep-analysis candidates**.

If zero candidates: write the report with only the triage table and the note
"No change amplification detected in this batch." Stop here.

If candidates ≥ 15: ask the user:
> "Triage found {N} candidates with severity ≥ 3. Deep analysis of all of
> them will be thorough but slow. Shall I analyse all {N}, or trim to the
> top 10 by severity?"
Wait for the answer before proceeding.

---

#### Pass 2 — Deep analysis (one call per candidate)

For each deep-analysis candidate, submit a **separate call** with only that
one PR's data. This gives the model full attention per item.

```
You are an architecture reviewer.

Bounded-context map:
{CONFIRMED DOMAIN MAP}

Architectural style: {user's one-sentence description}

Intentionally coupled pairs: {list or "none"}

---

Analyse this single merged PR for change amplification.

{SINGLE PR BLOCK}

Output exactly this structure:

### #{number} — {title}
**PR:** {url}
**Severity:** {1–5} / 5
**Intended change:** {the single conceptual change — one sentence}
**Amplification evidence:**
  - `{path}` (+{n}/-{n}) — {why this file had to change, given the intended change}
**Why architectural:** {name the missing boundary, owner, or contract.
  Target sentence: "No single module owns the concept of X."}
**Better architecture:** {the smallest structural change that makes the next
  similar PR touch only one module. Name a concrete class, interface, module,
  or service. Not "refactor the whole system".}
**Mechanical prevention:** {a specific test, type check, lint rule, or
  contract check that would catch this drift next time.}
**Deletion criterion:** {what temporary compatibility shim or duplicated
  definition should be removed once the new owner exists.}
```

Run Pass 2 calls sequentially, not in parallel — the outputs feed Pass 3.

---

#### Pass 3 — Patterns synthesis (one call, all Pass 2 outputs)

Once all Pass 2 analyses are complete, send them together for synthesis.

```
You are an architecture reviewer. Below are deep analyses of {N} PRs that
showed change amplification in a {REPO} codebase.

{ALL PASS 2 OUTPUTS CONCATENATED}

---

Write two things only:

1. Executive summary (one paragraph): how many PRs showed amplification,
   what fraction of the batch, and the 2–3 most structurally significant
   missing boundaries across the whole set.

2. Patterns section: group the backlog items by the TYPE of missing boundary.
   Use a heading per pattern type. Under each heading, list the PR numbers
   that exemplify it. Name each pattern concisely — this vocabulary is what
   the team should use in future ADRs, PR descriptions, and code review
   comments.

   Example pattern names:
   - "Validation scattered across layers"
   - "No owner for feature-flag schema"
   - "Domain rules duplicated in API and worker"
   - "Configuration not encapsulated — callers know the shape"

Do not re-emit the individual PR analyses. Reference them by number only.
```

---

### Step 8 — Write the report

Write the analysis output to:

```
{VAULT_ROOT}/01.Technical/arch-debt-{REPO}-{YYYY-MM-DD}.md
```

Where `VAULT_ROOT` is the Obsidian vault root (the working directory when the
skill was invoked, or the nearest ancestor containing `00.Tasks/`).

Use this file header:

```markdown
---
type: architecture-analysis
repo: {OWNER}/{REPO}
date: {YYYY-MM-DD}
prs_analysed: {N}
prs_excluded: {M}
method: change-amplification
references:
  - "Ousterhout, A Philosophy of Software Design (2018) §2"
  - "Tornhill, Software Design X-Rays (2018) — change coupling"
  - "Parnas, On the Criteria to Be Used in Decomposing Systems into Modules (1971)"
tags: [architecture, technical-debt, change-amplification]
---

# Architecture Debt: {REPO}
*Analysed {N} merged PRs · {YYYY-MM-DD}*

> **Method:** Change amplification analysis. Each item below is a missing
> module boundary, evidenced by a PR that forced edits across conceptually
> separate places. This is not a list of bad PRs — it is a backlog of
> missing abstractions.

---

## Auto-excluded PRs

{list of excluded PRs with one-line reasons}

---

{LLM analysis output starting from the executive summary}
```

After writing, print the full path and the executive summary paragraph.

---

## Error Handling

| Condition | Response |
|---|---|
| `GITHUB_TOKEN` not set | Abort: "Set GITHUB_TOKEN (read-only `repo` scope is enough)" |
| GitHub API returns 401 | Abort: "Token rejected. Check GITHUB_TOKEN has `repo` scope." |
| GitHub API returns 404 | Abort: "Repo {OWNER}/{REPO} not found or not accessible." |
| GitHub API rate-limited | Wait 60s, retry once. Print remaining rate limit from response headers. |
| PR has no description | Use `(no description)` — do not skip |
| Fewer than 10 PRs returned | Warn: "Only {N} merged PRs found. Analysis may lack statistical signal." |

---

## Invocation Examples

```
/change-amplification
→ Uses current git repo, last 50 merged PRs

/change-amplification last 30 PRs
→ Uses current git repo, last 30 merged PRs

/change-amplification 100 PRs
→ Uses current git repo, last 100 merged PRs
```

---

## Intellectual References

| Source | Concept | Relevance |
|---|---|---|
| Ousterhout, *A Philosophy of Software Design* (2018) §2 | Change amplification | The named symptom this skill detects |
| Ousterhout, *APOSD* §5–6 | Information hiding, deep modules | The structural fix |
| Parnas, "On the Criteria to Be Used in Decomposing Systems into Modules" (1971) | Information hiding principle | Original definition: one module hides one design decision |
| Tornhill, *Software Design X-Rays* (2018) | Change coupling via git history | Structural complement — co-commit patterns vs. semantic intent |
| Tornhill, *Your Code as a Crime Scene* (2015) | Hotspot analysis | Context for why PR-level analysis > file-level churn alone |
| Khononov, *Balancing Coupling in Software Design* (2023) | Module boundaries, coupling taxonomy | Framework for naming the missing boundary in each item |
