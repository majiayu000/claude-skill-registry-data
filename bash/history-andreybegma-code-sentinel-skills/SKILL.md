---
name: cs-history
description: Generate a comprehensive project history by combining PR/release note data with a product status report. Maps development effort to user role portals (e.g., owner, banker, charter) and produces a narrative of what was worked on, effort distribution per role, and current product state. Use when asked to create release notes, project timeline, effort retrospective, work summary, or development history. Triggers on phrases like "project history", "what did we work on", "release notes", "effort summary", "retrospective", "development timeline". Requires `docs/project-status.md` from the repo-analysis skill (or equivalent status report).
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
---

# Project History Skill

Combine PR history with the product status report to produce a project retrospective organized by user role portals.

## Prerequisites

Check for `docs/project-status.md` (or ask user for the status report path).

- **If it exists**: read it to learn which role portals exist, what pages each role has, and current completion status per page. Use this data to populate the "Completion %" column in the Effort Distribution table.
- **If it doesn't exist**: continue without it. Omit the "Completion %" column from all output tables and add a note at the top of the report: `⚠️ No project-status.md found — completion data unavailable. Run /cs-repo first to add it.`

## Process

### 1. Gather PR Data

Detect the git hosting platform and pull **all** PR data — both merged AND closed-not-merged. This is crucial — partial data produces misleading effort stats, and ignoring abandoned PRs hides real effort that was invested but didn't land.

#### 1a. Fetch merged PRs

**GitHub (preferred) — paginated fetch to guarantee completeness:**

First, count the total merged PRs:
```bash
gh pr list --state merged --limit 1 --json number | gh pr list --state merged --limit 9999 --json number --jq 'length'
```

Then fetch all PRs. The `gh` CLI returns at most ~1000 per call, so paginate if needed:
```bash
# Fetch all merged PRs (gh handles pagination internally up to the limit)
gh pr list --state merged --limit 9999 --json number,title,body,createdAt,mergedAt,labels,files,additions,deletions,commits,author
```

If the result count is less than the total, paginate manually using `--search` with date ranges:
```bash
# Split by date ranges to fetch all PRs
gh pr list --state merged --limit 9999 --search "merged:<=2025-06-30" --json number,title,body,createdAt,mergedAt,labels,files,additions,deletions,commits,author
gh pr list --state merged --limit 9999 --search "merged:2025-07-01..2025-12-31" --json number,title,body,createdAt,mergedAt,labels,files,additions,deletions,commits,author
gh pr list --state merged --limit 9999 --search "merged:>=2026-01-01" --json number,title,body,createdAt,mergedAt,labels,files,additions,deletions,commits,author
```

**Verify completeness:** after fetching, compare the number of unique PRs collected against the total count. If any are missing, retry once with narrower date ranges; if still incomplete, note the gap and proceed with available data.

**If `gh` CLI not available**, fall back to:
```bash
git log --merges --pretty=format:'%H|%s|%ai' --since="[project start or reasonable lookback]"
```

#### 1b. Fetch closed-not-merged PRs (abandoned/rejected work)

Closed-not-merged PRs represent real effort that was invested but didn't make it into the product. Ignoring them:
- Understates total investment per role
- Hides wasted effort patterns (failed experiments, abandoned approaches, rejected work)
- Skews effort distribution — if one role had many closed PRs, its true investment is higher than merged PRs alone suggest

```bash
# Fetch closed-not-merged PRs directly using jq
# IMPORTANT: gh returns null (not "") for mergedAt on unmerged PRs — you MUST check for null
gh pr list --state closed --limit 9999 \
  --json number,title,body,createdAt,closedAt,mergedAt,labels,additions,deletions,author \
  --jq '[.[] | select(.mergedAt == null)]'
```

**IMPORTANT — `mergedAt` null check:** The `gh` CLI represents unmerged PRs with `mergedAt: null`, NOT `mergedAt: ""`. Using `select(.mergedAt == "")` will silently return zero results. Always use `select(.mergedAt == null)`.

**Mandatory count verification** — immediately after fetching, cross-check:
```bash
CLOSED_TOTAL=$(gh pr list --state closed --limit 9999 --json number --jq 'length')
MERGED_TOTAL=$(gh pr list --state merged --limit 9999 --json number --jq 'length')
EXPECTED_UNMERGED=$((CLOSED_TOTAL - MERGED_TOTAL))
echo "Closed total: $CLOSED_TOTAL, Merged: $MERGED_TOTAL, Expected unmerged: $EXPECTED_UNMERGED"
```
Compare `EXPECTED_UNMERGED` against the count from the jq filter above. If they don't match, debug before proceeding.

For each closed-not-merged PR, also fetch files if possible (same approach as merged PRs).

#### 1c. Fetch release notes

If auto-generated release notes or tags exist, pull those too:
```bash
gh release list --limit 50
gh release view [tag] --json body
```

### 2. Map PRs to Role Portals

This is the critical step. The codebase has partial folder separation with lots of shared code, so use a layered approach:

**Layer 1 — Direct folder match (requires file data):**
Scan PR changed files for role-specific directories (e.g., `*/owner/*`, `*/banker/*`, `*/charter/*`). If ALL changed files are within one role's folder → assign to that role.

**Layer 2 — Import tracing for shared code:**
If a PR touches shared/common files, check which role pages import or consume those components. Trace the dependency direction:
- Read the changed shared files
- Search for imports of those files across role-specific pages
- If a shared component is only used by one role → attribute to that role
- If used by multiple roles → attribute proportionally or mark as shared

**Layer 3 — PR context clues:**
Use PR title, description, and labels to disambiguate:
- PR title mentions "owner dashboard" → owner, even if it touches shared files
- Label says "banker" → banker
- Description references a specific role workflow → that role

**Layer 4 — Genuinely shared:**
PRs that are truly cross-cutting (infra, auth, CI/CD, design system, refactors) → classify as "Shared/Platform". Do NOT force these into a role. Expect 15-25% of PRs here; that's normal.

**IMPORTANT — file data is essential for accurate classification:**
If you cannot fetch file lists for PRs (e.g., GitHub API rate limits, GraphQL node limits), do NOT fall back to title-only classification. Title-only classification dramatically inflates the Shared/Platform category because most PRs touching role-specific backend code (e.g., `apps/api/src/vessel/`) don't mention the role name in the title.

If `--json files` causes GraphQL errors due to node limits:
1. Fetch core data WITHOUT files first: `--json number,title,createdAt,mergedAt,labels,additions,deletions,author`
2. Then fetch files separately in batches of ~50 PRs using `gh pr view {number} --json files`
3. Use `xargs -P 10` or similar for parallel fetching
4. If some file fetches fail, classify those specific PRs by title — but the majority MUST have file data

**Sanity check after classification:** If Shared/Platform exceeds 25% of all PRs, review the classification. A high Shared count usually means file-based classification failed and too many role-specific PRs fell through to the title-based fallback.

### 3. Time Period Grouping

Group PRs into logical periods. Use whichever fits best:
- Sprint boundaries (if visible from labels/milestones)
- Monthly (default fallback)
- Release tags (if they exist)

Per period, summarize:
- What was delivered per role (in product terms, not technical terms)
- Key PRs and what they changed from a user perspective
- Whether the work was net-new features, fixes, or visual polish

### 4. Effort Distribution (Weighted)

Raw PR count is misleading — a 1-line typo fix and a 5-day feature rewrite both count as "1 PR". Use **weighted effort estimation** to produce more honest numbers.

#### 4a. Classify PR complexity

Before computing weight, classify each PR into a **complexity category**. This is critical — a refactor touching 40 files is fundamentally easier than a 40-file feature, and the weight must reflect that.

**Classify each PR by scanning its title, description, labels, and file patterns:**

| Category | Multiplier | How to detect |
|----------|------------|---------------|
| **Feature** | `1.0` | Title contains `feature/`, `feat:`, `add`, `implement`, `create`, `new`. New files created. New endpoints, pages, or components. |
| **Bug fix** | `0.9` | Title contains `fix/`, `fix:`, `patch/`, `hotfix`. Usually targeted changes to existing logic. |
| **Refactor** | `0.3` | Title contains `refactor`, `rewrite`, `replace`, `rename`, `move`, `simplify`, `clean`, `remove unused`, `chore/`. High file count + high line churn but mechanically simple (search-replace, restructuring). Also: if `deletions > additions * 0.7` and `len(files) > 5`, likely a refactor. |
| **Bump / Merge / Release** | `0.1` | Title contains `bump`, `merge/`, `Merge main`, `Merge/main`, `release/`, `Release/`. Dependency bot authors. Version-only changes. These are near-zero effort regardless of diff size. |
| **Schema / Migration** | `0.4` | Files are predominantly `*.prisma`, `*.sql`, `*migration*`, `*schema*`. High line count but generated or declarative — low cognitive effort per line. |
| **Style / UI polish** | `0.6` | Title contains `style`, `ui update`, `feedback`, `colour`, `color`, `responsive`, `layout`. Changes concentrated in CSS/Tailwind/component JSX without logic changes. |
| **Infrastructure / Config** | `0.5` | Files are predominantly config (`*.json`, `*.yaml`, `*.toml`, `Dockerfile`, CI files, `pulumi/*`). Important but usually low-complexity. |

**Rules:**
- Classify using title first (strongest signal), then file patterns, then fall back to "Feature" as default.
- When uncertain between two categories, pick the lower-effort one — it's better to slightly undercount effort than to inflate a refactor into feature-level work.
- A single PR can only have one category. If a PR mixes feature work with refactoring, classify by the dominant intent (what the PR title describes).

#### 4b. Compute effort weight per PR

For each PR, compute an **effort weight** using these signals (all available from the fetched data):

| Signal | Source | Why it matters |
|--------|--------|----------------|
| Lines changed | `additions + deletions` | Larger diffs generally mean more work |
| Files touched | `len(files)` | More files = more coordination and context switching |
| Time open | `createdAt` → `mergedAt` | Longer-lived PRs usually represent harder problems |
| Commit count | `len(commits)` | More commits = more iteration/rework |
| Complexity category | from step 4a | Mechanical work should weigh less than creative work |

**Effort weight formula:**

```
linesScore        = log2(additions + deletions + 1)         # dampens outliers (schema renames, generated code)
filesScore        = sqrt(len(files))                         # diminishing returns on file count
daysOpen          = max((mergedAt - createdAt) in days, 0.1) # floor at 0.1 to avoid zero
commitsScore      = log2(len(commits) + 1)                   # more commits = more iteration
complexityMult    = multiplier from category table (step 4a)

effortWeight = linesScore * filesScore * min(daysOpen, 14) * commitsScore * complexityMult
```

**Important adjustments:**
- Cap `daysOpen` at 14 days. PRs open for months are usually stale/forgotten, not actively worked on for months.
- If a PR has 0 commits (data unavailable), default `commitsScore` to `1.0`.
- The `complexityMult` is the key differentiator: a refactor touching 30 files (x0.3) will weigh less than a feature touching 10 files (x1.0), even though the refactor has a larger raw diff.

#### 4c. Aggregate weighted effort per role

Per role portal, calculate:
- **PR count** — raw number of PRs (still useful for volume context)
- **Lines changed** — raw additions + deletions
- **Weighted effort** — sum of `effortWeight` for all PRs in that role
- **Weighted effort %** — each role's share of total weighted effort
- **Time span of activity** — first PR to last PR
- **Avg effort per PR** — weighted effort / PR count (shows typical PR "heaviness" for that role)
- **Top 5 heaviest PRs** — the PRs with highest effort weight per role (helps identify where most effort actually went)

Also calculate for Shared/Platform work separately.

#### 4d. Caveats on effort estimation

Always include these caveats — weighted effort is *better* than raw PR count, but still imperfect:
- The weight formula is a heuristic, not a time tracker. It cannot measure thinking time, debugging, or design work that happened outside the PR.
- Lines changed is dampened by log2 but still over-counts generated code, schema migrations, and formatting changes.
- Time open includes weekends, holidays, review wait time — not just active coding time.
- Shared/Platform work benefits all roles but won't show up in any role's numbers.
- Very small PRs (quick fixes, config changes) will have near-zero weight even if they solved critical issues.

### 5. Consistency Checks (MANDATORY)

Before writing ANY output, run these assertions. If any fail, fix the data — do NOT proceed with inconsistent numbers.

**Check 1 — Role totals match grand total:**
```
sum(PRs per role) == total merged PRs fetched
```
If this fails, some PRs were lost or double-counted during classification. Debug by finding which PR numbers are missing or duplicated.

**Check 2 — Monthly sub-totals match role totals:**
```
for each role:
  sum(monthly PR counts for that role) == total PRs for that role
```
If this fails, some months are missing from the breakdown.

**Check 3 — Category totals match role totals:**
```
for each role:
  sum(category counts for that role) == total PRs for that role
```

**Check 4 — No duplicate PR numbers across roles:**
```
len(all PR numbers) == len(set(all PR numbers))
```
Each PR must be assigned to exactly one role.

**Check 5 — Appendix counts match main tables:**
```
for each role:
  sum(appendix monthly counts for that role) == effort table PR count for that role
```

**How to implement:** After all classification is done, write a verification script that checks all 5 conditions and prints PASS/FAIL for each. If any FAIL, print which specific numbers don't match and why. Fix before proceeding to output.

### 6. Synthesis with Status Report (including abandoned work)

Cross-reference effort data (both merged and abandoned) with the product status from `docs/project-status.md`:

**Per role, answer:**
- How much effort went into this role's portal? (merged + abandoned)
- What's the current product state? (X pages functional, Y visual only, Z empty)
- Does effort correlate with completion? If not, why? (complexity, rework, scope changes, abandoned work)
- What was the trajectory? (early work = scaffolding, recent work = wiring up, or stalled?)
- How much work was abandoned? Does the closed-to-merged ratio reveal problems?

**Overall, answer:**
- Which role got the most investment? Which the least?
- Are there roles with lots of effort but low completion? (potential red flags)
- Are there roles with high completion but minimal recent activity? (potentially done, or potentially abandoned)
- What's the ratio of product work vs. platform/shared work?
- Which roles had the most abandoned work? What does that signal?

### 7. Output Format

Save to `docs/project-history.md` (or user-specified path).

**Formatting rules:**
- Keep the document scannable — prefer tables over prose for data, prose for narrative
- The PR appendix should be **condensed** — list only key/notable PRs per month, not every single PR
- Use `*Release: [tags]*` at the end of timeline periods when release tags exist

```markdown
# Project History & Retrospective
Generated: [date]
Period: [first PR date] — [last PR date]
Role portals analyzed: [list]
Total merged PRs: [N] | Closed without merge: [M] | Total effort tracked: [N+M]

## Executive Summary
[5-7 sentences: what was built per role, total effort, current product state, key insights. Mention abandoned work if significant.]

---

## Product Timeline

### [Month Year] — [Descriptive Title]
**[Role]:** [what was delivered in product terms, mention PR count]
**[Role]:** [...]
**Shared:** [infrastructure/platform work]
*Release: [release tags that fall in this period]*

### [Month Year] — [Descriptive Title]
[...]

---

## Effort Distribution by Role

| Role | PRs | Lines Changed | Weighted Effort | Effort % | Avg Weight/PR | Active Period | Completion % |
|------|-----|---------------|-----------------|----------|---------------|---------------|-------------|
| Owner | ... | ... | ... | ...% | ... | ... | [from status report] |
| Charter | ... | ... | ... | ...% | ... | ... | ... |
| Banker | ... | ... | ... | ...% | ... | ... | ... |
| Shared/Platform | ... | ... | ... | ...% | ... | ... | — |
| **Total** | **[must equal total merged PRs]** | ... | ... | **100%** | ... | ... | ... |

### PR Complexity Breakdown

| Role | Feature | Bug Fix | Refactor | Bump/Merge | Schema/Migration | Style/Polish | Config |
|------|---------|---------|----------|------------|------------------|-------------|--------|
| [per role, count of PRs in each category — row total must equal role PR count] |
| **Total** | ... | ... | ... | ... | ... | ... | ... |

### Monthly Effort Heatmap

| Month | [Role 1] | [Role 2] | ... | Shared | Total |
|-------|----------|----------|-----|--------|-------|
| YYYY-MM | effort (count) | effort (count) | ... | effort (count) | effort (count) |

*Format: Weighted Effort (PR count). "—" = zero PRs.*

### Heaviest PRs by Role

[Per role, use a table format:]

#### [Role] — Top 5
| # | Title | Weight | Category | Changes | Files | Date |
|---|-------|--------|----------|---------|-------|------|
| [number] | [title] | [weight] | [category] | +X/-Y | [count] | [merged date] |

## Abandoned / Rejected Work

This section covers PRs that were closed without merging — real effort that was invested but didn't make it into the product.

| Role | Closed PRs | Lines Written | Weighted Effort | Closed-to-Merged Ratio |
|------|-----------|---------------|-----------------|----------------------|
| [per role] | ... | ... | ... | [closed / merged — high ratio = churn signal] |

### Notable Abandoned PRs
[List the largest/most significant closed-not-merged PRs per role — what was attempted and why it might have been abandoned]

### What This Tells Us
[Analysis: Which roles had the most abandoned work? Does it correlate with stalled areas? Does it reveal false starts, scope changes, or rejected approaches?]

---

## Per-Role Deep Dive

### [Role Name]

**Effort invested (merged):** [X PRs, Y weighted effort (Z% of total), over N months]
**Effort invested (abandoned):** [A PRs, B weighted effort — Z% of this role's merged effort was also spent on abandoned work]
**Current state:** [summary from status report — X/Y pages functional]
**Trajectory:** [arrow notation: phase 1 → phase 2 → phase 3]

**Key deliverables:**
- [bulleted list of notable features/pages completed]

**Gaps:**
- [bulleted list of what's unfinished or missing]

**Notable pattern:** [one observation about this role's PR patterns — e.g., high bug fix ratio, feature-to-fix ratio, refactor campaigns]

[repeat per role, separated by `---`]

---

## Key Insights

### Effort vs. Completion Correlation

| Role | Effort % | Completion % | Ratio | Interpretation |
|------|----------|-------------|-------|----------------|
| [per role] | ...% | ...% | ...x | [brief interpretation] |

### Velocity Trends
- **[Period]:** [PR count, characterization]
- **[Period]:** [...]

### Stalled Areas
1. **[Area]:** [what's stalled and why]
2. [...]

### Shared Work Impact
[Brief analysis of shared/platform work proportion and what it enabled]

### Team Contribution Patterns

| Author | PRs | Primary Focus |
|--------|-----|---------------|
| [login] | [count] | [1-line description of what they worked on] |

---

## Caveats
[Standard disclaimers as bullet points — PR count ≠ effort, log2 dampening, time open caveats, shared work attribution, role classification methodology]
[Note: closed-not-merged PRs may include draft PRs, superseded PRs, or PRs closed by mistake — not all represent "wasted" work]

---

## Appendix: Release History

| Release | Date | Key Changes |
|---------|------|-------------|
| [tag] | [date] | [1-line summary from release notes] |

## Appendix: PR Log by Role (Condensed)

[IMPORTANT: This is a CONDENSED log — list only notable/key PRs per month, not every single PR.
Use format: **YYYY-MM (N PRs):** #X title, #Y title, #Z title
Monthly counts in parentheses MUST match the effort distribution table — verified by consistency checks.
For months with many PRs, list only the 5-10 most significant ones.]

### [Role] ([total] PRs)

**YYYY-MM (N PRs):** #X [key PR title], #Y [key PR title], ...

## Appendix: Closed-Not-Merged PR Log
[List grouped by role, with PR number, title, date, and lines changed — condensed format]
```

### 8. Tone

- Write for the internal team, not external stakeholders
- Product language: "the owner can now view fund performance" not "added GET /api/funds endpoint"
- Be direct about gaps. If a role's portal is mostly visual mockups despite months of work, say so plainly
- Do not judge team performance — describe what happened and where things stand
