---
name: later
description: Backlog for off-scope work — capture drive-by bugs, cleanup, and ideas without derailing the current task; promote when ready
model: haiku
---

# x-later — Off-Scope Work Queue (Todo for Later)

Capture work you notice but should **not** do right now, so the current task stays focused. Backed by `xm build later` — a per-project JSON queue at `.xm/build/projects/<project>/later.json`. This is the **Later Queue discipline** from CLAUDE.md made directly invocable.

> **⚠ Call `xm build later` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xmb()`) defined in one call do NOT persist to the next, causing `command not found: xmb`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XMB_CLI=$(ls -d ~/.claude/plugins/cache/xm/{build,xm}/*/lib/x-build-cli.mjs 2>/dev/null | sort -V | tail -1)
> node "$XMB_CLI" later <command> [args]
> ```
>
> **Forbidden:** `XMB="node ..."; $XMB later ...` — zsh treats the quoted string as a single command and fails.

## Model Routing

This skill is **haiku** (Agent tool). Every path is a CLI call + structured display — the CLI does all the work, no reasoning involved.

```
Agent tool: { model: "haiku", description: "x-later", prompt: "Run: xm build later <command> [args]" } <!-- managed-model: writer -->
```

**Guardrail**: escalate to **sonnet** only if the user asks you to *decide what to defer* across a large diff, or to triage a long backlog by priority — those are reasoning tasks, not mechanical queue ops.

## When to Use

Use when the user (or you, mid-task) wants to **park** work for later instead of doing it now:

- "이거 나중에 하자 / 따로 빼두자" → `add`
- Drive-by bug, cleanup idea, refactor, stale comment spotted while doing something else → `add`
- "나중에 할 일 목록 보여줘 / later 뭐 있어?" → `list`
- "later 3번 지금 하자 / 그거 작업 시작하자" → `promote` (turns it into a real task)
- "그건 안 해도 돼 / 취소" → `dismiss`
- Before claiming a task done, confirm parked items stayed parked → `verify-scope`

Do **NOT** use this skill to track the *current* task's own subtasks — that is what `xm build tasks` is for. `later` is strictly for work that is **out of the current scope**.

## Core Process

### Step 1 — Classify the user's intent

Map the request to exactly one subcommand: `add` | `list` | `promote` | `dismiss` | `verify-scope`.

### Step 2 — For `add`, enforce deferability BEFORE running

A later item must be safe to defer. Confirm all three, else do not add:

1. **It does not block the current task.** If B blocks A or changes A's correctness, it is in-scope — fix it now or update the active task. Do not park it.
2. **Its impact is `none`, `low`, or `unknown`.** The CLI rejects anything else. Pass `--impact` honestly; never downgrade impact just to make `add` succeed.
3. **You will not touch its files until promoted.** Adding to `later` is a promise to leave that code alone.

Then run, passing as much context as the user gave you:

```bash
xm build later add "title" --reason "why it can wait" --source "where it came from" --impact low --files "a.ts,b.ts"
```

`--files` records a content snapshot so `verify-scope` can later prove the parked code was untouched. Always include it when the item names specific files.

### Step 3 — For `list` / `promote` / `dismiss` / `verify-scope`, run directly

```bash
xm build later list                       # status=open (default)
xm build later list --status all          # open + promoted + dismissed
xm build later promote <id> --size small --deps t1,t2   # → creates a real task
xm build later dismiss <id> --reason "obsolete"
xm build later verify-scope               # add --strict to fail on missing baselines
```

`promote` is the **only** moment editing that item's code becomes allowed — it converts the parked item into a task in `xm build tasks`. Until then, the item is off-limits.

### Step 4 — Report the result

Relay the CLI output to the user in their language. Example (normal mode):

```
✅ 나중에 할 일로 등록했습니다: L3 — "토큰 만료 에러 메시지 개선"
   현재 작업 범위 밖이라 미뤄둠. promote 전까지 이 코드는 건드리지 않습니다.
```

For `list`, render the items as a short checklist with their IDs so the user can `promote`/`dismiss` by number.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll just fix this unrelated bug while I'm here" | No. Parking it with `add` keeps the current diff reviewable; fixing it now expands blast radius and hides the real change. Capture, don't detour. |
| "it's in later, so let me pre-edit the code a bit too" | Adding to `later` is a promise to NOT touch that code. Editing before `promote` defeats the entire mechanism. |
| "it's medium impact but I'll just file it as low" | Misreporting impact to pass `add` is how blocking work gets silently deferred. If it is not truly `none/low/unknown`, it is in-scope — handle it now. |
| "these are subtasks of the current work, but later is handy" | `later` is for OUT-of-scope work. Current-task subtasks belong in `xm build tasks`; mixing them corrupts both queues. |
| "let me file it quickly without --files" | Without a file snapshot, `verify-scope` cannot prove the parked code stayed untouched. Omitting `--files` for a file-specific item removes the only guardrail. |
| "I'll just start working on it without promoting" | Editing a parked item's code without `promote` means it never became a tracked task — no done-criteria, no traceability. Promote first, then code. |

## Red Flags

Stop and reconsider if you catch any of these:

- You are about to edit a file that belongs to an **open** later item (not yet promoted).
- You are adding something to `later` that, if left undone, would make the current task wrong or incomplete → it is in-scope, not later.
- You are using `later` to hold the current task's own steps.
- You ran `add` with `--impact` set lower than the truth to dodge the deferability check.
- You are about to mark a task complete without running `verify-scope`.

## Verification

- After `add`: the CLI prints `Later item added: <id> — <title>`. Re-run `xm build later list` to confirm it appears with status `open`.
- After `promote`: `xm build later list --status all` shows the item as `promoted` with a `promoted: <taskId>`, and `xm build tasks list` shows the new task.
- Before declaring any task done: `xm build later verify-scope` must print `Later scope check passed.` — a failure means a parked file was modified, which is a discipline violation to fix before shipping.

## Arguments

- `/xm:later` or `/xm:later list` — show open parked items (default)
- `/xm:later add "..."` — park off-scope work (see Step 2)
- `/xm:later promote <id>` — turn a parked item into a task
- `/xm:later dismiss <id>` — drop a parked item
- `/xm:later verify-scope` — confirm parked files stayed untouched
