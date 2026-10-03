---
name: pr-babysitter
description: >-
  Keep a PR merge-ready after push: monitor CI until green, poll for new review
  comments (human, Copilot, security scanners, bots), alert the user, validate
  and auto-fix legitimate feedback, auto-commit and auto-push, reply and resolve
  threads. Use after pushing to a PR branch or when asked to babysit a PR.
---

# PR Babysitter

Autonomous PR operations loop with **auto-fix** and **auto-push**. Use after pushing to a PR branch, or invoke `/pr-babysitter`.

## Prerequisites

- `gh` installed and authenticated (`gh auth status`)
- `node` on PATH (for the bundled poll script)
- Run from the repository root that owns the PR
- On Windows PowerShell: use separate shell commands (no `&&` chaining) and variableized GraphQL (`-F owner=… -F name=… -F number=…`) instead of string-interpolated queries

## Resolve PR context

```bash
gh pr view --json number,url,baseRefName,headRefName,isDraft,mergeable,statusCheckRollup
```

If owner/repo are needed:

```bash
gh repo view --json nameWithOwner
```

## Alert on new comments

Run the bundled cross-platform poll script:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/poll-pr-comments.mjs" --pr <number>
```

Optional flags:

- `--owner <org> --repo <name>` — override auto-detection from the current repo
- `--state-dir <dir>` — where seen-comment state is stored (default: OS temp dir, never inside the repo)
- `--json` — machine-readable output only

### Script behavior

1. Fetches unresolved review threads, **minimized/suppressed** review comments, bot review summaries with suppressed hints, issue comments, and reviews via `gh`
2. Flags items as `suppressed` / `requiresValidation` (Copilot, security scanners, bots, minimized/low-confidence)
3. Diffs against per-PR state (`<owner>-<repo>-<pr>.json` in the state dir); first run initializes state without alerting
4. Prints new items and updates state
5. Fires a native OS notification (macOS notification + sound, Windows tray balloon) via the bundled `scripts/pr-babysitter-notify.mjs`, and emits the sentinel line `AGENT_LOOP_WAKE_PR_COMMENT` for loop/wake integration

### Suppressed bot comments (critical)

GitHub may hide Copilot feedback as **"Comments suppressed due to low confidence"** in the PR UI. Do **not** treat these as ignorable.

The poll script handles them by:

- Fetching `isMinimized` / `minimizedReason` on review comments
- Parsing review summaries for suppressed `file:line` hints when the full comment body is not inline
- Tagging output with `[SUPPRESSED]` and `[VALIDATE-FIRST]`

**Alert always. Auto-fix only after validation passes.**

## Comment validation gate (before auto-fix)

**Functional correctness is the #1 goal.** Auto-fix is enabled, but never blind.

For each comment (human, Copilot, scanner, bot — including suppressed):

| Step | Check |
|------|--------|
| 1 | Read cited code and understand **current runtime behavior** |
| 2 | Is this a **confirmed defect** (broken test, schema/type mismatch, security issue) or preference/refactor? |
| 3 | Would the suggested fix **change behavior**? If yes, only proceed if the bug is proven (failing test, repro, contract violation) |
| 4 | Does the fix obey the project's standards, PR scope, and module boundaries? |
| 5 | Is this refactor/style-only? If it's in touched files and materially improves clarity/testability with low behavior risk, **prefer a minimal safe fix**; otherwise reject with rationale |
| 6 | Still uncertain? **Do not auto-fix** — reply with analysis; leave open or escalate |

### Outcomes

- **Fix + push** — validated defect; minimal diff; scoped tests pass; behavior preserved or bug corrected
- **Improve + push** — non-functional improvement in touched area that clearly improves maintainability/readability and is behavior-preserving
- **Reply only** — invalid, speculative, out of scope, or refactor-only; explain why with evidence
- **Needs human** — ambiguous behavior impact or conflicting intent

Never resolve a thread with code changes unless validation passed and tests support the fix.

### Alert the user

When the script reports new items (or on loop wake):

1. Post a chat summary per item: **author**, **source**, **suppressed/VALIDATE-FIRST flags**, **location**, **snippet**, **URL**
2. The OS notification fires automatically from the poll script
3. Proceed to auto-fix **only** for comments that pass the validation gate

## Comment triage and auto-fix

1. Fetch unresolved review threads **and** minimized/suppressed comments (GraphQL). Read comment body + minimal location; avoid dumping full JSON.
2. Classify author:
   - **Human reviewer** — treat change requests as actionable unless clearly nitpick/out of scope; still validate behavior impact
   - **Copilot** — always validate; **never skip suppressed/low-confidence** items
   - **Security scanners** (Aikido, Snyk, CodeQL, etc.) — validate and fix real issues only
   - **Other bots** — validate before fixing
3. For each comment passing the **validation gate**:
   - Declare allowed file list (PR scope + comment path)
   - Implement the minimal fix, following the project's own conventions and rules
   - Run scoped lint/typecheck/tests when available
   - Commit with the repository's commit-message convention
   - **Push** to PR branch
   - Reply on thread with concrete resolution notes
   - Resolve thread via GraphQL
   - Restart CI loop
4. For **invalid** feedback: reply with rationale; do not change code; resolve only if fully addressed by explanation
5. Do not silence constructive feedback in touched code by default. If declining a maintainability/readability suggestion, explain concrete trade-offs (scope, risk, behavior uncertainty) and prefer leaving the thread open unless clearly settled.

## Documentation currency gate (required)

Before each push from babysitter fixes:

1. Check whether changed behavior/contracts/config require docs updates (README, onboarding, runbooks, endpoint docs).
2. If docs are impacted, update the relevant docs in the same PR before push.
3. If no docs are needed, state why in the final babysitter summary.
4. Do not mark merge-ready if docs are stale relative to merged code behavior.

### Reply and resolve (GraphQL)

Use variableized `gh api graphql` with `-F owner=`, `-F name=`, `-F number=` (mandatory on Windows PowerShell; good practice everywhere).

Resolve a thread after the fix is pushed and the reply is posted. Prefer replying through `gh pr comment` or review comment APIs as appropriate to the thread type.

## CI loop

1. After every push, poll until current runs complete:

```bash
gh pr checks <number> --watch
```

Or inspect rollup:

```bash
gh pr view <number> --json statusCheckRollup
```

2. On failure: fetch logs for the failed check, fix in scope, commit, push, repeat
3. Do not mark healthy while required checks are red or pending

## Periodic polling while working

While the PR is open and you are otherwise idle, poll on an interval:

```bash
while true; do
  sleep 300
  node "${CLAUDE_SKILL_DIR}/scripts/poll-pr-comments.mjs" --pr <number>
done
```

```powershell
while ($true) {
  Start-Sleep -Seconds 300
  node "$env:CLAUDE_SKILL_DIR/scripts/poll-pr-comments.mjs" --pr <number>
}
```

When the output contains `AGENT_LOOP_WAKE_PR_COMMENT`, wake and run the full babysit loop (alert → validate → fix → push → reply → resolve); otherwise keep polling.

## Code-change rules (every fix)

Every babysitter fix follows the host project's own rules first (root agent instructions, contributing guide, lint config). Baseline regardless of project:

| Area | Rule |
|------|------|
| Scope | Only touch files within PR scope + the commented path; no opportunistic refactors |
| Behavior | Preserve runtime behavior unless a defect is proven; match existing style; minimal diff |
| Line endings | Preserve existing line endings; never rewrite whole files for small edits |
| Tests | Run the smallest relevant suite before push; a fix with failing tests never ships |
| Hygiene | No agent/IDE config folders or local secrets in commits; verify staged paths before commit |

## Auto-push commit flow

After each scoped fix:

```bash
git add <allowed-files-only>
git status
git commit -m "<repo-convention message>"
git push
```

Verify staged paths contain only intended files before commit.

## Stop conditions

**Merge-ready:** green required checks + mergeable + no unresolved actionable threads

**Blocked — report and stop:**

- Auth / permission errors
- Fix needs out-of-scope or CI workflow changes
- Unresolvable merge intent conflict
- Cannot validate a bot finding and the fix would be risky — leave thread open with explanation
