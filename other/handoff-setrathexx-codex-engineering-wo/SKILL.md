---
name: handoff
description: Creates a concise local handoff document so Codex work can resume in a later session or another local context. Use when ending a session, pausing work, transferring context, or summarizing current progress without duplicating existing PRDs, issues, tests, or plans.
---

# Handoff

Create a short, durable handoff that lets future Codex work resume without rebuilding context from the whole conversation.

Do not copy large PRDs, issues, diffs, or test logs into the handoff. Link or reference existing artifacts and capture only what is needed to continue.

## Read First

Before writing, inspect:

- `docs/agents/handoff.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/test-commands.md`
- current PRD or issue paths mentioned in the conversation
- changed files if available
- recent verification commands and outcomes

If setup docs are missing, propose this default:

```txt
docs/agents/handoff/
```

Use a timestamped file name such as:

```txt
docs/agents/handoff/YYYY-MM-DD-topic.md
```

Keep Windows paths quoted when showing commands or file locations.

## What To Capture

Capture the current state of work:

- current goal,
- user-approved decisions,
- files changed or created,
- current implementation state,
- verification run and results,
- open questions,
- risks and gotchas,
- recommended next action.

Capture only enough detail for continuation.

## What Not To Capture

Do not include:

- secrets, tokens, API keys, credentials, private personal data,
- full PRD or issue contents already stored elsewhere,
- long command logs,
- speculative future roadmap unrelated to the current work,
- unrelated repo findings,
- hidden chain-of-thought or private reasoning.

If sensitive data appeared in the conversation, redact it and mention that redaction occurred.

## Workflow

### 1. Identify Purpose

Determine why the handoff is being created:

- end of session,
- pause before implementation,
- follow-up tomorrow,
- switch to testing,
- switch to another workflow skill,
- preserve decisions after a long conversation.

If the purpose is unclear, infer it from the latest user request and state the assumption.

### 2. Collect Existing Artifacts

Find and reference existing artifacts:

- PRDs,
- local issues,
- architecture notes,
- ADRs,
- test command docs,
- prior handoffs.

Prefer paths over duplicated content.

### 3. Check Worktree Context

If working in a repo, inspect changed files when appropriate.

Summarize:

- created files,
- modified files,
- deleted files if any,
- files intentionally untouched,
- verification evidence.

Do not run destructive git commands. Do not revert changes.

### 4. Propose Target Path

Before writing, propose:

- handoff directory,
- file name,
- sections to include.

Ask for approval before creating the file.

If the user explicitly asks for a handoff immediately and the path convention is already clear, proceed with the configured local path.

### 5. Write The Handoff

Use this structure:

```md
# Handoff: <topic>

## Current Goal

## What Changed

## Decisions Made

## Verification

## Open Questions

## Risks

## Continue From Here

## Useful Paths
```

See `references/handoff-template.md` for the compact template.

### 6. Keep It Actionable

The next session should know:

- where to start,
- what not to redo,
- what is already decided,
- what still needs verification,
- which skill should run next.

Recommended next skills may include:

- `zoom-out`,
- `grill-with-docs`,
- `to-prd`,
- `to-issues`,
- `tdd`,
- `diagnose`,
- `prototype`.

## Safety Rules

- Do not include secrets or credentials.
- Do not overwrite an existing handoff without approval.
- Do not publish remotely by default.
- Do not delete temporary files unless explicitly asked.
- Do not claim tests passed without verification evidence.

## Verification

Before finishing:

- State the handoff path written or proposed.
- Confirm sensitive data was excluded.
- Confirm existing PRDs/issues/tests were referenced, not duplicated.
- List remaining open questions.
- State the recommended next skill and why.

Use `references/handoff-quality-checklist.md` before presenting the handoff.
