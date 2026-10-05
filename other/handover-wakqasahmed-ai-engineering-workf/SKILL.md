---
name: handover
description: Compact the current conversation into a handover document a fresh agent can pick up and continue seamlessly. Invoke when only 5-10% of the session limit remains, when context usage passes 40% (less than 60% of the context window remaining), when context is about to cross an agent or session boundary, when work is blocked, or on explicit user request — never haphazardly mid-task. Covers decisions, shipped changes, key files, running state, verification, deferrals, and open questions.
argument-hint: "[what the next session will focus on]"
---

# Handover

Produce a compact, structured summary so a fresh agent or session can continue without re-deriving what already happened. This is a **context-handover artifact**, not a status report — the audience is the next agent, not a stakeholder. Save to the temporary directory of the user's OS, not the current workspace.

## When to invoke

- 5-10% of the session limit remains with work unfinished: pause at the next safe point and write the handover — don't run to the last token and stop silently.
- Context usage passes 40% of the window on unfinished multi-step work.
- Context is about to cross an agent, session, or clear boundary — including when the user signals they're about to clear context — or work is blocked and non-obvious state must be preserved.
- User says "handoff", "handover", "wrap up session", or a near-equivalent.

Skip it when ample context remains and work is progressing, or when the work is complete and legible from the issue, PR, and tests.

## How to produce it

1. Review the full conversation, not just the last few turns — handovers miss things when they only look at recent context.
2. Pull state from these sources, in order:
   - Any plan file referenced this session.
   - Task/todo list state — anything in progress or pending.
   - Background processes started this session — their IDs are load-bearing; the next agent can't rediscover them.
   - Files created or modified this session — you already know what you touched, don't re-grep to rediscover it.
   - Memory files written or updated this session.
   - Current branch/worktree/PR/issue.
   - Unresolved questions — things asked that never got a clear answer, or user asks that got deflected.
3. Do not audit the filesystem or git history to reconstruct this. It's a synthesis of this session, not a fresh investigation.
4. Include a "suggested skills" section listing skills the next agent should invoke.
5. Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL.
6. Redact secrets, API keys, passwords, personally identifiable information, credential values, and local credential-file paths as `Credential details: [redacted]`. Separate local and public rendering: retain absolute paths only in the local temporary artifact. When publishing to GitHub, sanitize machine-local paths to prevent leaking host usernames, private home directory layouts, or internal service environments: omit the temporary handover file path, convert workspace file paths to repository-relative paths (e.g. `src/cache/redis_client.py`) or commit URLs, and replace all other machine-specific local paths (e.g. `/home/*`, `C:\Users\*`, `/opt/*`) with `[local path redacted]`.
7. If the user passed arguments, treat them as what the next session will focus on and tailor the doc accordingly.

## Publish to the issue

If the work traces to a GitHub issue or PR:

1. Comment on the issue with the full handover content, sanitized per Rule 6 above (workspace paths converted to repository-relative, other local paths redacted, temp file path omitted) — temp directories do not survive; the comment is the durable copy.
2. Add the label `paused by agent` (create it if missing). It marks half-done work waiting for pickup and pairs with `picked by agent`.
3. The agent that resumes removes `paused by agent`, applies `picked by agent`, and continues from the "Pick up here" line.

If no issue exists, report the handover file path in chat instead.

## Output template — use this structure every time

```
# Handover — <one-line title of what this session was about>

## Where it started
<2-3 sentences: what was asked, key framing or constraints that emerged>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives (absolute path if a file)>

## Key files for next session
- `<absolute path>` — <why the next agent should read this first>
- Plan file: `<path>` (if a plan drove the session)
- Memory files touched: `<paths>` — or "none"

## Running state
- Background processes: <IDs + what they are + how to stop them> — or "none"
- Dev servers / ports: <url + port> — or "none"
- Open worktrees / branches / PRs / issues: <paths, numbers> — or "none"

## Verification — how to confirm things still work
- `<command>` — <expected outcome>

## Deferred + open questions
- Deferred: <item> — <why pushed to later>
- Open: <question needing the user's input> — <context>

## Pick up here
<1-2 sentences: the single most likely next action for a fresh agent>
```

## Hard rules

- Never invent state. If a section has nothing to report, write "none" — don't omit the section; structure stability is the point.
- Absolute paths always in the local artifact so an agent on the same host can locate files directly; in the public issue/PR comment, use repository-relative paths and replace host-specific paths with [local path redacted] to protect environment privacy.
- If a plan file drove the session, name it first under "Key files."
- Terse and concrete: paths, commands, IDs, decisions. Prefer links to issues, PRs, and files over prose. No retrospective, no hype, no emojis.
- No next steps beyond the single "Pick up here" line — the next agent decides.
