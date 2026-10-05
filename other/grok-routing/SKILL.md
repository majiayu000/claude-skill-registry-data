---
name: grok-routing
description: >
  When to delegate coding work to Grok Build vs handle it in Claude. Use whenever
  the user asks for bulk edits, test backfill, migrations, boilerplate, exploratory
  prototypes, or whether to use /grok:delegate — and when reviewing whether a task
  is safe to hand to Grok.
---

# Grok routing (Claude orchestrates, Grok executes)

You are in a session where the **grok** plugin can run Grok Build via MCP.
Product goal: help the user **use Grok well**, **feel Grok’s strength**, and enjoy
**Claude ↔ Grok collaboration** — not replace Claude.

## Default posture

When a task is a good fit for Grok, **propose delegation first** (brief why + tool),
then run it if the user agrees or already asked to use Grok. Do not dump every
coding task on Grok.

## Delegate to Grok when

| Fit | Examples |
|---|---|
| Bulk / repetitive | Same pattern across many files, renames, import fixes |
| Low-risk volume | Test backfill, docs sync, boilerplate CRUD/DTO/scaffold |
| Narrow independent scope | Single module, clear acceptance criteria, little monorepo coupling |
| Exploratory prototype | Try an approach fast; user will review |

**Tools (prefer this order):**

1. **Route first (no side effects):** `grok_build_route` or `/grok:route` — read **`nextAction`**
   (`handle_with_claude` | `call_mcp_tool` + tool/flags). Do not re-derive the plan.
2. If `nextAction.requiresHumanGateBeforeDelegate`: **plan** (`grok_build_plan` / `/grok:plan`)
   then wait for approval before any edit tool. If the plan result has `planWroteFiles` or `committed`
   set to `true`, the tree already changed before any approval — say so first.
3. Execute: `grok_build_delegate` / `/grok:delegate` or verify `/grok:verify` as `nextAction.tool` says.
4. **Review gate:** `/grok:review` — diff + `billing`; never auto-commit.
5. Multi-turn: `/grok:resume` using `usage.lastSession.sessionId` or the last result’s `sessionId`.
6. Presets: `/grok:tests`, `/grok:migrate`, `/grok:boilerplate`
7. Auth / ready: `grok_build_status` (or `grok_auth_check`) with the task's absolute `cwd`, or `/grok:setup`. If status
   reports **`billingMismatch`**, warn that the server is in subscription mode while past
   delegations were recorded as metered — they ran when `GROK_BUILD_AUTH_MODE` was `api`; ask the
   user to confirm the current value is the one intended. Do not stop on it: it describes history
   and stays true while those rows remain, so treating it as a gate would block every later
   delegation. If it reports **`billingCaveat`**, relay its `message` (grok's `config.toml` gives
   some model its own key, or could not be checked) but do not stop — it is a warning, not a gate.

Always pass absolute `cwd`. Prefer English prompts for the `prompt` field.

**Do not make coding edits through `grok_cli` / `/grok:cli`.** A passthrough that carries a
prompt is a real grok turn: the pre-delegate auth hook gates it and delegation history records it
(`via: 'grok_cli'`). But it has none of delegate's review aids — no worktree isolation, no parsed
summary, no `committed` check, no `billingCaveat`. `/grok:cli` stays the escape hatch for
non-editing subcommands (`models`, `sessions`, `memory`, …); use `grok_build_delegate` /
`grok_build_verify` for anything that changes files.

Optional tool fields (validated; bad values fail without running grok): `model` — **omit it**
unless you have a reason, so the run follows whatever the CLI defaults to (`grok models` is the
only current answer; on 2026-09-22 that was `grok-4.7`, with a `grok-4.7-build-fast` tier beside
it, and the model the run records is reported back as `model`). `grok-build` is remapped to the
CLI default. Also `max_turns` (stop cleanly after n turns, keeping partial edits — a bound on work
rather than `timeout_ms`'s wall clock), `effort`
(`low`/`medium`/`high`/`xhigh`), `resume` / `continue` (not both),
`sandbox` (`workspace` | `read-only` | `strict` | `devbox` | `off` — Linux/macOS kernel
enforce; Windows not assumed). Do **not** pass `best_of_n` — CLI 1.0 removed `--best-of-n`.
Results may include `sessionId` for later `resume`.
`filesChanged` lists paths that became dirty *during* the run; use `worktree: true` on
already-dirty trees for full attribution.

External orchestrators: copy the loop in `examples/orchestrator-consumer.md` and
`${CLAUDE_PLUGIN_ROOT}/docs/07-orchestrator-integration.md`.

## Keep in Claude (do not delegate)

- Architecture / design decisions, API shape trade-offs
- Security (auth, crypto, permissions), secrets, compliance / regulated domains
- Work needing whole monorepo or very large context
- Final code review and quality gate (you always review Grok’s diff)

## After every Grok run

1. If `status` is not `completed` (`auth_error`, `timeout`, or `grok_error`), show the returned
   `message` and stop — do not report the run as done. Otherwise show `summary`,
   `filesChanged`, and especially **`billing`** (`subscription` vs `metered_api`) — with the
   `message` of **`billingCaveat`** beside it when the result carries one. If **`committed`** is
   `true`, grok made a git commit although the server never commits: show the returned `message`
   — it names the folder whose HEAD moved and the commit it moved from, with how to inspect and
   undo it there (never run those commands in another folder) — and remember the committed files are no longer in `filesChanged`. An absent
   `committed` means the run could not be checked, not "no commit". If
   **`resumedCwd`** is present, the resumed session belongs to that directory and grok worked
   there, not in the `cwd` you passed — review the diff there.
2. Run the **`/grok:review`** checklist (or equivalent): adversarial correctness/security/scope.
3. **Never auto-commit**; the server never commits. User decides accept / fix / discard.
4. Risky or large work: use `worktree: true` so changes land in an isolated worktree (`worktreePath`); review there before merge.
5. Partial failure still may list `filesChanged` — inspect before continuing.
6. Offer `/grok:resume` when a `sessionId` is available for follow-ups.

## Auth failures

If tools fail with install/login messages, guide `/grok:setup` or the message’s commands.
Do not attempt `grok login` or install inside this session for the user.

## Cost note

Default mode is **subscription**. Do not thrash (no delegate-on-every-keystroke).
In API/metered mode, be stricter about fit and avoid wasteful retries.
