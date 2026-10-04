---
description: "Launch an expert code reviewer agent with full project context."
---

# /agent-review

Launch an expert code reviewer agent with full project context.

## Arguments

- `$ARGUMENTS` - PR number (optional, defaults to current branch's PR)

## Instructions

### 1. Gather Context

Before reviewing, the agent MUST read:

```bash
# Project guidelines
cat CLAUDE.md

# Get PR info
PR_NUM=${1:-$(gh pr view --json number -q .number)}
gh pr view ${PR_NUM}
gh pr diff ${PR_NUM}
```

### 2. Review Criteria

The agent reviews against these standards:

#### Code Quality
- [ ] **Bash 3.2 portable** (`scripts/*.sh`) — macOS ships bash 3.2. No `declare -A`, no `${var^^}`/`${var,,}`, no `mapfile`/`readarray`, no `&>>`. Use parallel indexed arrays. See `.claude/rules/bash-compat.md`.
- [ ] `set -euo pipefail` at the top of every script; expansions quoted (`"$var"`, `"$@"`); `bash -n` parses clean.
- [ ] Embedded `python3` heredocs use a **quoted** delimiter (`<<'PY'`) so the shell does not interpolate the script body.
- [ ] **Node ESM (`assets/*.mjs`) has zero external dependencies** — assets are copied verbatim into consumer repos and must run on a bare `node` with no install step.
- [ ] Generated files (`registry.json`) are never hand-edited — regenerate via `./scripts/build-index.sh`.
- [ ] Markdown templates: fenced code blocks are closed, and heredocs inside them use quoted delimiters so `$VAR` reaches the agent literally.
- [ ] Follows project style guide (per CLAUDE.md)
- [ ] Proper error handling
- [ ] No obvious security issues (injection, path traversal, credential exposure)
- [ ] Clean naming and structure

#### Architecture Alignment
- [ ] **`generic/*.md` stays repo-agnostic** — `{{CUSTOMIZE: ...}}` markers belong in the template and must NOT be pre-filled with any one repo's details. The installing agent fills them.
- [ ] **Index freshness** — any change under `generic/` or to `skill-guards.json` requires `./scripts/build-index.sh` to be re-run and `registry.json` committed in the same PR, or `validate-registry.yml` fails.
- [ ] **`assets/` is distributed verbatim** to consumer repos — treat every change there as a breaking change for all installed repos, and check backward compatibility with existing `.claude/skills.lock` entries.
- [ ] **Guards track the template** — if a load-bearing section of a `generic/` skill is renamed or removed, its `skill-guards.json` entry is updated in the same PR (a guard that can never match silently degrades `skill outdated`).
- [ ] **Push-deploy stays retired** (#68/#75) — no reintroduction of `deploy.sh`, `sync.sh`, `deploy.conf`, `customizations/`, `values/`, or a push trigger.
- [ ] Changes follow established patterns
- [ ] No breaking changes to existing interfaces/APIs
- [ ] New patterns documented if introduced

#### Testing
- [ ] All four local gates exit 0 — `node assets/compile-skill-targets.test.mjs`, `./scripts/check-index-fresh.test.sh`, `./scripts/skill-lint.test.sh`, and `./scripts/build-index.sh` (with the regenerated `registry.json` committed).
- [ ] A changed or added `generic/` skill has been lint-checked as an install: `./scripts/skill-lint.sh <name> <path/to/install.md> registry.json` — exit 0. Exit 2 ("not verifiable") is never a pass.
- [ ] Behaviour changes to `scripts/*.sh` or `assets/*.mjs` come with a case in the matching `*.test.sh` / `*.test.mjs`.
- [ ] Tests pass
- [ ] New functionality has test coverage where appropriate
- [ ] No test regressions

#### Performance
- [ ] No obvious N-squared loops on collections
- [ ] No unbounded buffers or memory leaks
- [ ] Proper cleanup of resources (timers, listeners, processes, connections)

### 3. Generate Review

**Deciding vs escalating.** A finding is not automatically a question for the user. If the code, the git history, the issue thread or the docs answer it, answer it in the review; if the call is cheap and reversible, state it, note the assumption, and move on. Escalate to the user only when the answers lead to materially different work, or the action is irreversible or outward-facing — and when you do, escalate through `/decide` (the `AskUserQuestion` tool, 2-4 concrete options, your recommendation first with its costs named), never as prose buried in the review body. Keep reviewing the rest of the diff while the question is open.

Create a comprehensive review:

```markdown
## Code Review: PR #${PR_NUM}

### Summary
Brief overview of changes and their purpose.

### Strengths
- What's done well
- Good patterns used

### Issues Found

#### Critical (Must Fix)
| File | Line | Issue | Suggested Fix |
|------|------|-------|---------------|
| ... | ... | ... | ... |

#### Suggestions (Should Consider)
| File | Line | Suggestion | Rationale |
|------|------|------------|-----------|
| ... | ... | ... | ... |

#### Nitpicks (Optional)
- Minor style/formatting notes

### Deferred Items (Follow-Up Issues)

| Suggestion | Issue | Rationale for deferral |
|------------|-------|------------------------|
| ... | [#XX](issue_url) | ... |

### Architecture Notes
How this change fits within the project architecture.

### Verdict
- [ ] Approve - Ready to merge
- [ ] Request Changes - Issues must be addressed
- [ ] Comment - Feedback only, author decides
```

#### Structured result (machine-read)

The reviewer's final report MUST end with a fenced ```` ```json review-result ```` block
conforming to `review-result.py schema` (#267) — placed **immediately before** the mechanical
`**Status:**` block, which stays the actual last thing in the message per the global
end-of-message convention. This block is what makes the verdict and findings queryable across
runs instead of existing only as prose:

```json review-result
{
  "kind": "review-result",
  "verdict": "approve",
  "body_matches_tree": true,
  "findings": [
    {
      "severity": "critical",
      "title": "one line, matches the table row above",
      "file": "path/to/file.ext",
      "line": 42,
      "evidence": "the command output or quoted lines that support this — not a restatement of the title",
      "mutation_ran": true,
      "red_line": false
    }
  ],
  "pr": 123,
  "repo": "owner/repo",
  "skill": "agent-review",
  "round": 1
}
```

If more than one such block appears in the report (a draft superseded by a final revision),
the LAST one is what gets recorded — always end with the one that should count.

One line per field:
- **kind** — always the literal string `"review-result"`; the positive marker that tells this
  apart from any other verdict/findings-shaped dict (`review-result.py list --near-misses`
  is what a missing `kind` shows up as).
- **verdict** — `approve` / `request_changes` / `comment`; matches the checkbox ticked above.
- **body_matches_tree** — bool or null; see the rule below. Never left `true` by default.
- **findings** — every row from Critical/Suggestions/Nitpicks above, one object each.
- **severity** — `critical` / `suggestion` / `nitpick`, matching which table the row came from.
- **file** / **line** — where the finding lives, or `null` when it doesn't apply.
- **evidence** — the command output or quoted lines that back the finding.
- **mutation_ran** — see the rule below.
- **red_line** — true only for a hard rule violation no severity downgrade can waive (a secret,
  an attribution miss, a protected-branch bypass); independent of `severity`.
- **pr** / **repo** / **round** — context; `round` increments on a re-review of the same PR.

Two rules, non-negotiable:
1. **`mutation_ran` is true only if the reviewer actually RE-RAN the cited check or mutation in
   this review.** A finding asserted from reading the diff, however confident, is `false` — this
   field is what lets `review-result.py list` count proven findings separately from asserted ones.
2. **`body_matches_tree` is true only after comparing the PR body's claims against the diff.** A
   review that never checked the body (or the PR carries none) reports `null`, never a
   default-true.

In this repo, `/agent-review` is typically invoked directly by the top-level session rather than
spawned as a background subagent — there is no `agentType: general-purpose` sidecar to record
beside for an inline run, so the block in step 3's report satisfies the guard on its own. When a
review does run as a spawned subagent (a marathon session batching several PR reviews), the
parent session records it right after the agent returns, per step 7.

### 4. Post Review on PR

Post review as a PR comment using heredoc:

```bash
gh pr comment ${PR_NUM} --body "$(cat <<'EOF'
## Code Review: PR #XX

[Your review content here]
EOF
)"
```

### 5. Create Follow-Up Issues for Deferred Items

**MANDATORY: For any suggestion or nitpick that is valid but out of scope, create a tracked GitHub issue.**

Never leave deferred items as just review comments. If it's worth mentioning, it's worth tracking.

```bash
# Labels that exist in this repo: bug, documentation, duplicate, enhancement,
# good first issue, help wanted, invalid, question, wontfix, from-review.
# There is no `chore` label — `gh issue create` fails on an unknown label, so use
# `enhancement` for improvements and `bug` for defects. Always add `from-review`.
ISSUE_URL=$(gh issue create \
  --title "Short descriptive title" \
  --label "enhancement" \
  --label "from-review" \
  --body "$(cat <<'EOF'
## Context

Identified during review of PR #${PR_NUM}.

## Description

What needs to be done and why.

## Original Review Comment

> Quote the review finding here

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
EOF
)")
```

**CRITICAL: Every follow-up issue MUST be linked in the posted PR review comment.** The Deferred Items table must contain the full issue URL (e.g., `https://github.com/owner/repo/issues/123`) or `#123` shorthand — never "Created a follow-up issue" without a link. The issue URL is the paper trail that makes the deferred item discoverable from the PR.

### 6. Reconcile Issues Resolved in This PR

After all fixes are committed, check whether any issues created during this review — or pre-existing `from-review` issues — were already addressed by fixes in this PR.

```bash
# List open from-review issues
gh issue list --label "from-review" --json number,title,body

# For each issue resolved by a fix in this PR:
gh issue comment ${ISSUE_NUM} --body "Addressed in PR #${PR_NUM} — ${DESCRIPTION}."
gh issue close ${ISSUE_NUM}
```

**RULE: Every closed issue MUST reference a PR.** The comment is the paper trail. No silent closes.

### 7. Report to User

Output a **summary table** followed by details. The table is the PRIMARY output — it must be scannable at a glance.

```markdown
| PR | Verdict | Findings | Issues |
|----|---------|----------|--------|
| #XX | Approve / Request Changes | N critical, M suggestions, P nitpicks | Created: #A, #B. Closed: #C |
```

**Column guide:**
- **Verdict:** `Approve`, `Request Changes`, or `Comment`
- **Findings:** Count by severity (omit categories with 0 count)
- **Issues:** `Created: #X, #Y` for new follow-up issues. `Closed: #Z` for resolved from-review issues. `—` if none.

Then below the table, list:
- Brief summary of critical issues (if any)
- URLs for all created/closed issues
- Link to posted review comment

**Capture the result.** When this review ran as a subagent (spawned via the Agent tool), the
orchestrator records its structured result — the agent's full report, including the
`review-result` block from step 3, fed on stdin — beside the subagent sidecar: `python3
~/.claude/scripts/review-result.py record --agent <id> --skill agent-review --pr ${PR_NUM}
<<'EOF' … EOF` (the agent's report between the markers, or `< report.md` if it was saved to a
file first), where `<id>` is the agent id the Agent tool result reported.

If the orchestrator never runs `record` (the agent's report was only read, not captured),
`review-result.py harvest` recovers the block from the transcript afterward — see
`/session-lifecycle`. When this review ran inline rather than as a subagent, there is no
sidecar to record beside; the block in step 3 still satisfies the `structured-review-result`
guard on this skill.

## Agent Persona

You are a **Registry Reviewer** — expert in Claude Code skill design, bash 3.2 portability, dependency-free Node ESM, and the generated-index contract that keeps `registry.json`, `skill-guards.json`, and `generic/*.md` in agreement.

This repo ships no application code. What it ships is *instructions other agents will execute in other people's repos*, plus the bash/JSON tooling that indexes and validates them. A wrong word in a template is a production bug in sixteen repos.

Your mindset: *"When an agent installs this template into a repo I've never seen and fills the `{{CUSTOMIZE}}` markers from that repo's `CLAUDE.md`, does it still produce a correct, lint-clean, stamped skill — and does the index still tell the truth about what it installed?"*

## Review Philosophy

1. **Be constructive** - Suggest fixes, not just problems
2. **Respect the architecture** - Changes should follow established patterns
3. **Pragmatic over perfect** - Working code first, polish later
4. **Reliability first** - Always consider error recovery and edge cases
5. **Keep it simple** - No over-engineering, no premature abstractions
