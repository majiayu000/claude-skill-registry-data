---
name: plan-review
description: "Run an independent fresh-session review loop over a saved design plan before approval, converging reviewer feedback or recording SKIP. Use for high-risk, multi-file, architectural, or costly-to-undo plans. Skip implementation code review (code-review), finished-feature verification (verify), and drafting the plan itself (design)."
argument-hint: "handoff [plan] | run [plan] | continue [plan] | skip [plan] --reason cost|latency|auth_unavailable|low_risk|user_override|other"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
effort: high
disable-model-invocation: false
---

Coordinate an independent review loop for a saved plan. This skill reviews the plan artifact before implementation; it does not replace `/design`, `/verify`, `/retro`, or the user's explicit approval.

## Hard Rules

- Every review round uses a fresh reviewer context. R1 is fresh; R2 is also fresh and receives the updated plan plus compact prior-round summaries, not the previous reviewer session.
- Same-conversation self-review is invalid. If no fresh reviewer can run, emit a manual handoff prompt or record an explicit `SKIP`.
- Reviewers are read-only. They return verdicts and findings; they never edit files.
- The author session owns plan edits and compact review-loop summaries.
- Store summaries under `## Plan Review Loop` in the plan. Keep the section append-only and do not store full raw transcripts.
- Reviewer `APPROVED` is not implementation approval. The plan still needs the user's explicit approval before promotion or implementation.
- User-facing wording should be neutral: use independent review, structured review, findings, and convergence. Avoid "adversarial" unless quoting an existing backlog id.

## Commands

- `handoff [plan]`: emit a fresh-session prompt for a reviewer.
- `run [plan]`: run the best available fresh reviewer backend, then summarize the result.
- `continue [plan]`: inspect the latest recorded round and create or run the next fresh review round.
- `skip [plan] --reason <reason>`: record an explicit `SKIP` outcome with residual risk instead of running a fresh reviewer.

If the user explicitly chooses not to run review, record `SKIP` instead of pretending approval happened.

## Resolve The Plan

1. If the user supplied a plan path/id, resolve that exact plan with `resolve-plan`. Otherwise
   use the strict tool and exact id from the injected session-routing block:

   ```bash
   PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" node "$HOME/.config/ai/lib/worktree.mjs" resolve-session --root "$PWD" --tool "<injected session tool>"
   ```

2. For an explicit plan, verify its worktree mapping under canonical `main_root`; it is an
   intentional override of session selection, not a launcher lookup.
3. Otherwise use only the session resolver's `plan`. An unbound main session must receive
   an explicit plan; never consult main `current.txt` or guess from old plans.
4. Use `execution_root` for repository reads and `main_root` for the canonical plan path.
5. Read the plan and identify:
   - frontmatter `id`, `title`, `status`, `files_affected`,
   - frontmatter `base_branch`, immutable `base_commit`, `branch`, and `worktree`,
   - `## Goal`, `## Decisions`, `## Verifiable Success Criteria`, `## Risks`, `## Implementation Steps`,
   - existing `## Plan Review Loop` summaries.

If the plan lacks `## Plan Review Loop`, add it before `## Post-Implementation Notes` when recording the first result.

## Build The Review Packet

Include as much relevant context as practical without dumping unrelated repository state:

- the full current plan,
- the resolved `main_root`, `execution_root`, `branch`, and immutable `base_commit`,
- compact prior review summaries from `## Plan Review Loop`,
- target files listed in `files_affected`, read from `execution_root`, when needed to judge the plan,
- relevant diffs or command outputs already produced, rooted at `execution_root` and compared
  from `base_commit`,
- explicit reviewer instructions and the verdict template below.

For R2+, include only compact prior-round summaries, not previous raw reviewer transcripts.

## Backend Selection

Prefer a different model from the author session:

1. Codex author session: use the `ask-claude` skill when available.
2. Claude author session: use the `ask-codex` skill when available; it delegates to `codex exec --sandbox read-only --ephemeral`.
3. If cross-model review is unavailable, use a same-tool fresh subagent/session when the environment supports one.
4. If no automatic fresh reviewer can run, emit a manual handoff prompt.

Do not silently fall back to same-conversation self-review.

## Reviewer Verdict Template

Give reviewers this exact output shape:

```text
Verdict: APPROVED | NEEDS_REVISION | BLOCKED
Summary: <2-4 sentences>
Findings:
- [severity: high|medium|low] <finding with evidence and why it matters>
Required changes before approval:
- <actionable change, or "none">
Suggested changes:
- <optional improvement, or "none">
If BLOCKED:
Reason: invalid_premise | insufficient_context | needs_human_decision | constraint_conflict
Unblock condition: <exact input, decision, or correction needed>
```

Verdicts:

- `APPROVED`: no required plan changes before the user decides whether to approve implementation.
- `NEEDS_REVISION`: fixable plan issues exist. The author session revises the plan, then starts a new fresh review round.
- `BLOCKED`: reviewability or progress is structurally blocked. Do not auto-loop.

`BLOCKED` requires a reason code and unblock condition. If revising the plan can resolve the issue, the verdict must be `NEEDS_REVISION`, not `BLOCKED`. Model disagreement alone is never `BLOCKED`.

## SKIP Records

`SKIP` is not a reviewer verdict. It is an explicit plan-review outcome when the user or author session intentionally chooses not to run review because of cost, latency, auth, tool availability, low-risk scope, or override.

Never infer `SKIP` from silence or tool failure. A skipped review never counts as `APPROVED`.

Record a skip like this:

```markdown
### R<N> — Review Skipped

- Status: `SKIP`
- Reason: `cost | latency | auth_unavailable | low_risk | user_override | other`
- Scope: <which plan or round was skipped>
- Residual risk: <what review coverage is missing>
- Next action: <continue, ask user, or proceed only after explicit approval>
```

## Recording Results

Append compact summaries only:

```markdown
### R<N> — <Reviewer> Fresh Review

- Reviewer: <claude | codex | same-tool fresh subagent | manual handoff>
- Verdict: `APPROVED | NEEDS_REVISION | BLOCKED`
- Summary: <short summary>
- Findings:
  - <finding summary>
- Required changes before approval: <none or list>
- Author response: <accepted/rejected/deferred decisions and rationale>
- Next action: <approve separately | revise and run R<N+1> | ask user | blocked until ...>
```

When the verdict is `NEEDS_REVISION`, revise the plan in the author session before running the next round. When the verdict is `BLOCKED`, stop the loop and ask the user for the exact missing input, decision, or correction. When the verdict is `APPROVED`, remind that explicit user approval is still separate.
