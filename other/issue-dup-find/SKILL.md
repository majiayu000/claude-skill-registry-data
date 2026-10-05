---
name: issue-dup-find
category: business-product
codex-short-description: "Scan open Jira issues for likely duplicates; markdown report with probability + reason"
description: >
  Scan a Jira project's open issues for likely duplicates and report each suspected pair
  with a probability score and reasoning. Read-only. Use when the user says "find
  duplicates", "duplicate check", "dedupe issues", or invokes /issue-dup-find.
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_get_issue
loop-eligible: false

compatibility: claude-code codex opencode
---

# Issue Duplicate Finder

Read-only scan of open issues in a Jira project to surface likely duplicates. Output is a markdown report — **no tickets are linked, transitioned, commented, or modified**.

## Input

- **Project key** — resolved from memory (`reference_jira_default_project.md` → `**Default Jira project key:**`). If that memory entry is missing, prompt via `AskUserQuestion` for the key and save the answer back to that file before proceeding. Accept a per-invocation override if the user provides one (`/issue-dup-find ABC` or "find duplicates in PROJ") — the override always wins.
- **Output destination** — chat by default. If the user specifies a file path (e.g. `C:\temp\dups.md`), also write the report there.

If the user message is ambiguous, confirm the project key and output destination once before proceeding.

## Workflow

```text
Duplicate scan progress:
- [ ] Phase 1: Fetch open issues (paginated)
- [ ] Phase 2: Cluster candidate pairs
- [ ] Phase 3: Semantic comparison
- [ ] Phase 4: Render report
- [ ] Phase 5: Optional file write
- [ ] Phase 6: Cleanup scratch folder
```

### Phase 1 — Fetch open issues

JQL: `project = {KEY} AND statusCategory != Done ORDER BY created DESC`

Paginate `jira_search` until exhausted. Use `max_results: 100` per call and increment until the API returns fewer than `max_results` (or zero). Do not impose an artificial ceiling.

For each issue capture: `key`, `summary`, `description` (first 1500 chars), `issuetype`, `status`, `components`, `labels`, `priority`, `created`, `reporter`, and any existing `duplicates` / `is duplicated by` issuelinks.

**Create a per-run scratch folder** at `C:\temp\issue-dup-find-{PROJECT}-{YYYYMMDD-HHMM}\` and use it for all intermediate state. Tell the user the path once. Persist the harvested table to `issues.json` inside that folder as you fetch — protects the work if a later phase fails so you can resume without re-fetching.

If issues already have an existing `is duplicated by` / `duplicates` link, note them and **exclude** those pairs from the candidate set (they're already known).

### Phase 2 — Cluster candidate pairs

Avoid O(n²) blowup. Group issues that share **any** of:
- the same component
- an overlapping label
- ≥3 shared significant tokens in the summary (ignore stopwords, common verbs, and the project key)

Form candidate pairs only **within** each group. De-duplicate pairs across groups. Surface the final pair count to the user as a progress checkpoint, then proceed — no budget cap.

Persist the candidate-pair list to `pairs.json` in the scratch folder so Phase 3 can resume mid-stream if interrupted.

### Phase 3 — Semantic comparison

Process every candidate pair — no sampling. For very large pair sets, work in batches of ~25 and append scored results to `scores.jsonl` in the scratch folder after each batch. This keeps progress durable.

For each candidate pair, judge semantically using the issue summaries, descriptions, components, and labels. Assign one of:

- **High (80–100%)** — clearly the same defect / feature request, even if worded differently. Same observable symptom, same affected area, or one is plainly a re-report of the other.
- **Medium (50–79%)** — overlapping symptom or scope, but meaningful differences in cause, environment, or scope make it possible they're distinct.
- **Low (25–49%)** — superficial similarity (shared keywords or component) but the underlying issues look different.
- **Below 25%** — drop from the report.

For each kept pair, write **one or two sentences** of reasoning that cites specific evidence (shared error string, identical reproduction steps, same component + same symptom, etc.). Do not pad. Do not invent evidence not present in the tickets.

When uncertain between two bands, pick the lower. False positives waste reviewer time.

### Phase 4 — Render report

Render in this exact format:

```markdown
# Duplicate Issue Scan — {PROJECT_KEY}

**Scanned:** {N} open issues · **Candidate pairs evaluated:** {M} · **Reported:** {K}
**Generated:** {YYYY-MM-DD HH:MM} · **Read-only — no tickets modified**

## Suspected duplicates

### {ISSUE-KEY-A} — {short summary}

| Possible duplicate | Probability | Reason |
| --- | --- | --- |
| [{KEY-B}]({jira-base}/browse/{KEY-B}) — {short summary} | High (92%) | {1–2 sentence reason citing concrete evidence} |
| [{KEY-C}]({jira-base}/browse/{KEY-C}) — {short summary} | Medium (64%) | {reason} |

### {ISSUE-KEY-D} — {short summary}

| Possible duplicate | Probability | Reason |
| --- | --- | --- |
| [{KEY-E}]({jira-base}/browse/{KEY-E}) — {short summary} | High (87%) | {reason} |
---

## Notes

- Issues with existing `duplicates` / `is duplicated by` links were excluded.
- Pairs scoring below 25% were dropped.
- This is a read-only report. To act on a pair, link the tickets manually in Jira or run the appropriate update skill.
```

Group by the **anchoring** issue (lower issue number wins as anchor). Each pair appears once. Sort anchors by highest probability score within their group, descending.

If no duplicates clear the 25% threshold, render the header + a single line: `_No suspected duplicates found above the 25% threshold._`

### Phase 5 — Optional file write

If the user supplied a file path in their original request, write the rendered markdown there with `Write`. Confirm with the absolute path written.

If they didn't specify, ask once via `AskUserQuestion` whether to save (offer "No — chat only" as the default, "Yes — save to {default path}", "Yes — custom path"). Do not nag; if they decline, move on.

### Phase 6 — Cleanup

After the report is delivered (and any user-requested file write is confirmed complete), remove the scratch folder `C:\temp\issue-dup-find-{PROJECT}-{YYYYMMDD-HHMM}\` and everything in it via `Bash: rm -rf`. Confirm cleanup with one line: *"Scratch folder removed."*

**Skip cleanup** if the run aborted with an error — leave the scratch folder intact so the user can inspect partial state or resume. Surface the path explicitly when an error occurs: *"Partial state retained at {path} for inspection."*

## Constraints

- **Read-only.** No `jira_update_issue`, `jira_link_issues`, `jira_transition_issue`, `jira_add_comment`, or any write tool. The only filesystem write is the optional report file in Phase 5.
- Do not infer duplicates from issue keys alone (e.g. consecutive numbers). Use ticket content.
- Do not include closed/resolved issues in the candidate set.
- Do not invent reasons. If the only signal is "same component", say so plainly and rate it Low.
- Cap reported pairs per anchor at 5. If more candidates score High, list the top 5 and add a footnote: `_+N additional medium/low matches suppressed._`
- The default project key is read from memory (`reference_jira_default_project.md`). Always confirm the resolved project key in the report header so the user can verify scope.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Each suspected pair has a probability score and a one-line reason
- Pairs are ordered by descending probability
- Read-only respected — no tickets linked, transitioned, or edited
- Obvious non-duplicates are not padded into the report

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/issue-dup-find.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
