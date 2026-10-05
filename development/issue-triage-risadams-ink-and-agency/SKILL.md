---
name: issue-triage
category: business-product
codex-short-description: "Triage a bug into ranked root-cause hypotheses + solution paths (read-only)"
description: >
  Triage a bug or Jira ticket into ranked root-cause candidates and proposed solution paths.
  Read-only unless the user opts in to publish. Use when the user says "triage this",
  "triage [TICKET-KEY]", "what's causing this bug", "help me find the root cause", or
  invokes /issue-triage.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Agent
  - Skill
  - mcp__atlassian__jira_get_issue
  - mcp__atlassian__jira_get_comments
  - mcp__atlassian__jira_get_changelog
  - mcp__atlassian__jira_get_remote_links
  - mcp__atlassian__jira_search
  - mcp__atlassian__jira_add_comment
  - mcp__atlassian__confluence_search
  - mcp__atlassian__confluence_get_page
  - mcp__gitlab-mcp__list_commits
  - mcp__gitlab-mcp__get_commit
  - mcp__gitlab-mcp__list_merge_requests
  - mcp__gitlab-mcp__get_merge_request
  - mcp__gitlab-mcp__search_project_code
related-skills:
  - codebase-explain
  - clarity-council
  - debug
loop-eligible: false

compatibility: claude-code codex opencode
---

# Issue Triage

Read-only triage of a bug or defect. Gathers context, maps the suspected code area, hypothesizes root causes, and produces a ranked triage report with proposed investigation paths.

**Read-only by default.** The skill never modifies Confluence pages, MRs, or code files, and never changes Jira ticket fields. The single exception is Phase 7: with explicit user opt-in, the final report may be posted as a comment on the originating Jira ticket.

## Input

One of:
1. **Jira ticket key** — pattern `[A-Z][A-Z0-9]+-\d+` (e.g. `PROJ-1234`)
2. **Free-form description** — a narrative description of the issue, error message, or symptom

If neither is clear from the user's message, ask which they want to triage.

## Workflow

```text
Triage Progress:
- [ ] Phase 1: Gather issue context
- [ ] Phase 2: Map suspected code area (codebase-explain)
- [ ] Phase 3: Pull related signals (git, MRs, sibling tickets)
- [ ] Phase 4: Clarify gaps with the user (grill-me)
- [ ] Phase 5: Hypothesize root causes (clarity-council)
- [ ] Phase 6: Produce triage report
- [ ] Phase 7: Optionally publish report as Jira comment (user opt-in)
```

### Phase 1 — Gather issue context

**If Jira ticket:**
- `jira_get_issue` — summary, description, type, priority, status, components, labels, affected version, environment.
- `jira_get_comments` — capture user-reported reproduction steps and prior investigation notes.
- `jira_get_changelog` — note recent status changes, reassignments, or version field updates.
- `jira_get_remote_links` — capture linked Confluence pages, MR URLs, log dashboards.

**If free-form description:**
- Echo the description back in a structured form: **Symptom**, **When it happens**, **Expected vs actual**, **Environment** (if known).
- Flag any missing fields — these become questions for Phase 4.

Compile a **Context Summary** and present it. Ask if anything important is missing before proceeding.

### Phase 2 — Map suspected code area

Identify file paths, modules, error messages, function names, or stack frames mentioned in the issue.

Invoke the `/codebase-explain` skill against the most likely module(s). The goal is a map of:
- Which modules are involved
- How they connect (callers, callees)
- Which seams exist for reproduction

Use `Glob` and `Grep` to confirm files exist and locate the actual symbols. If the issue mentions a stack trace, walk the trace top-down and read each frame's source.

If the suspected area is genuinely unclear from the issue, **stop and ask the user** which subsystem they suspect — guessing wastes context.

### Phase 3 — Pull related signals

For each signal, **time-box to the most relevant items.** Don't drown in noise.

1. **Recent git history** — `list_commits` on suspected files for the last 30 days. Use `Bash: git log --oneline -20 -- <path>` for local. Note: who, when, and short message.
2. **Related GitLab MRs** — `list_merge_requests` with `search` filter on suspected file paths or symbol names; limit to 5 most recent merged MRs. Look for: regressions introduced, recently changed contracts, refactors that touched the area.
3. **Linked Confluence pages** — fetch up to 2 pages from remote links via `confluence_get_page`. Look for runbooks, design intent, known limitations.
4. **Sibling/duplicate Jira tickets** — `jira_search` with JQL like `text ~ "{key error keyword}" AND project = {PROJECT} ORDER BY created DESC` (limit 5). Check for already-known issues with fixes or workarounds.

Present a **Signals Summary**: each signal with one-line takeaway + relevance flag.

### Phase 4 — Clarify gaps

Identify the open questions blocking a confident hypothesis. Examples:
- "When did this start happening?"
- "Does it reproduce on a clean checkout?"
- "Which environment(s) — local, dev, staging, prod?"
- "Is it tied to specific input data?"

If the answers materially change the hypothesis space, invoke the `/grill-me` skill to walk the user through these questions one at a time. Otherwise, skip this phase — don't manufacture interrogation for trivial gaps.

### Phase 5 — Hypothesize root causes

Invoke the `/clarity-council` skill in multi mode:

```
user_problem: "Identify the most likely root causes for: {issue summary}"

context: |
  Symptom: {one-line symptom}
  Repro: {steps if known, else "not yet established"}
  Environment: {where it happens}

  Code map (from codebase-explain):
  {paste relevant excerpts of the module map}

  Recent activity in suspected area:
  {top 3-5 commits / MRs with one-line takeaways}

  Sibling issues:
  {1-2 closest matches if any}

  User-clarified facts:
  {answers from Phase 4}

desired_outcome: >
  3-5 ranked root-cause hypotheses, each with: a falsifiable prediction
  (how to test it), the evidence supporting it, and the proposed first
  diagnostic step.

selected_personas:
  - researcher
  - senior-architect
  - senior-developer
  - qa-engineer
  - devils-advocate

depth: standard
```

Persona focus:
- **Researcher** — owns hypothesis falsifiability. For each candidate root cause raised by the others, the researcher checks: is the evidence cited actually load-bearing, or is it pattern-matching? Is the proposed diagnostic step truly falsifiable (would a negative result rule the hypothesis out), or merely consistent with the hypothesis? Surfaces missing data — "we don't yet know X; here's the cheapest way to find out" — before the council starts ranking. This is the persona's load-bearing contribution: keeping the team from pattern-matching on the most-recent commit.
- **Senior architect** — structural causes (coupling, hidden state, contract drift).
- **Senior developer** — implementation-level causes (off-by-one, race, null path, recent change).
- **QA engineer** — environmental and data-shape causes (config, fixture drift, version mismatch).
- **Devil's advocate** — challenges the obvious answer; flags hypotheses that fit too neatly.

**Order of synthesis:** present the researcher's evidence-quality audit *first*, then the ranked hypotheses. A hypothesis the researcher has flagged as evidentially weak should not be ranked #1 unless the others explicitly counter the flag.

### Phase 6 — Triage report

Present the report in this format:

```markdown
## Triage Report: {TICKET-KEY or short-title}

### Symptom
{1-2 sentences — what is broken, observable behavior}

### Suspected area
{module / file paths / functions implicated}

### Root cause hypotheses (ranked)

#### 1. {Hypothesis title} — {confidence: high/medium/low}
- **Why this fits:** {evidence — recent commits, related MRs, code patterns}
- **Falsifiable prediction:** "If this is the cause, then {X} should reproduce / {Y} should fix it."
- **First diagnostic step:** {what to instrument / what test to write / what to inspect}
- **Proposed solution path:** {high-level fix direction}

#### 2. {Hypothesis title} — {confidence}
{same structure}

#### 3. {Hypothesis title} — {confidence}
{same structure}

### Signals consulted
- Recent commits in {area}: {N} reviewed, {key finding or "none relevant"}
- Recent MRs touching {area}: {N} reviewed, {key finding or "none relevant"}
- Sibling tickets: {N} matches, {key finding or "no close matches"}
- Confluence: {pages reviewed if any}

### Open questions
- {questions still unresolved that would sharpen the diagnosis}

### Recommended next step
{One concrete action — e.g. "reproduce in a controlled environment first",
"ask {person} who wrote the recent commit to {area}", "instrument {X} to
test hypothesis #1", or "spike a fix branch against hypothesis #1"}

> **Read-only triage.** No tickets, code, or MRs were modified.
```

### Phase 7 — Optional: publish report as Jira comment

**Only runs if the input was a Jira ticket.** If the input was a free-form description, skip this phase and end the skill.

After presenting the report, ask the user — using `AskUserQuestion` — exactly one question:

> **Publish this triage report as a comment on `{TICKET-KEY}`?**
> - **No** *(recommended default)* — end the skill, no action taken.
> - **Yes** — post the report as a comment on the originating ticket.

**If "No":** the skill ends. Confirm with a single sentence: *"Report kept local. No comment posted."*

**If "Yes":** follow the posting steps in [jira-comment-template.md](jira-comment-template.md) — Jira wiki markup, the mandatory disclaimer panel, and error handling.

## Constraints

- **Read-only across all systems, with one explicit exception.** Never `jira_create_issue`, `jira_update_issue`, `jira_transition_issue`, `confluence_create_page`, `create_or_update_file`, or any other write operation. The single permitted write is `jira_add_comment` in Phase 7, and only after explicit user opt-in.
- Never auto-publish the comment. Phase 7 must always go through the explicit yes/no prompt — even if the user previously said "yes" in another session.
- The disclaimer panel from `jira-comment-template.md` is mandatory whenever a comment is posted. Do not edit, soften, or omit it.
- Do not write files to disk unless the user explicitly asks to save the report.
- Do not propose code edits. The output is a hypothesis + path, not a fix.
- If the input is ambiguous (no Jira key and no clear description), ask once for clarification — do not invent an issue to triage.
- Time-box signal gathering. Five recent commits beats fifty; one close sibling ticket beats ten weak matches.

## Quality Loop

Before returning, check the output against these criteria. If two or more fail, revise and re-check — at most two passes, then note what still falls short.

- Root-cause candidates are ranked and each is falsifiable (states what would confirm/refute it)
- Each hypothesis names the suspected code area with evidence (commit, file, or sibling ticket)
- At least one concrete next step / solution path per top candidate
- Read-only respected — no files written unless the user asked

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/issue-triage.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
