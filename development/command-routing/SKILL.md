---
model_tier: inherit
name: command-routing
description: "Use when the user invokes a slash command like /create-pr, /commit, /fix-ci, or pastes command file content — routes to the right command with context inference and GitHub API patterns."
domain: process
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# commands

## When to use

Triggered when user invokes a slash command. The `slash-command-routing-policy` rule (always loaded) handles core behavior — this skill adds context inference and GitHub API patterns.

## Procedure: Execute a command

1. **Match command** — Find the command file in `.augment/commands/` or `agents/overrides/commands/`.
2. **Infer inputs** — Before asking the user, try to infer values (see table below).
2b. **List a matching playbook in the preamble.** If a playbook's `task` matches the
   command's name, name it before the steps run — it is this repository's own procedure and
   outranks a shipped one ([`playbook-precedence`](../../rules/playbook-precedence.md)).
3. **Execute steps** — Follow the command steps in exact order.
4. **Verify output** — Confirm expected result was produced (commit, PR, file change, etc.).

Before asking the user for input, try to infer it:

| Input needed | How to infer |
|---|---|
| Jira ticket | Extract from branch name (`fix/DEV-1234-...` → `DEV-1234`) |
| Default branch | `git symbolic-ref refs/remotes/origin/HEAD` or assume `main` |
| Project type | Check for `artisan` (Laravel) or `composer.json` (Composer) |
| Module name | Extract from current working directory or file path |
| Current branch | `git branch --show-current` |

Only ask the user if inference fails and the command cannot proceed without the value.

## Command locations

| Location | Scope |
|---|---|
| `.augment/commands/` | Shared commands (work across projects) |
| `agents/overrides/commands/` | Project-specific overrides (used instead of original) |

## Commands that dispatch to the work engine

Most commands are pure markdown procedures — the agent reads the steps
and executes them. Two commands delegate to the `work_engine` engine
(TypeScript, run via tsx) via the `./agent-config` dispatcher; both share the same
Option-A loop (read state → run engine → handle exit code → repeat),
they only differ in the input envelope they build:

| Command | Subcommand | Envelope | Use when |
|---|---|---|---|
| `/implement-ticket` | `./agent-config implement-ticket` | `input.kind="ticket"` | User points at a Jira/Linear ticket or supplies a structured ticket payload |
| `/work` | `./agent-config work` | `input.kind="prompt"` | User supplies a free-form prompt — no ticket id, no acceptance criteria yet |

Route prompt-shaped intents (`"add a CSV export endpoint…"`,
`"fix the failing login test"`, `"refactor the audit-log controller"`)
to `/work`. Route ticket-shaped intents
(`"work on PROJ-123"`, `"start on the ticket on this branch"`) to
`/implement-ticket`. If the user pastes both a ticket id **and** a
free-form goal, prefer `/implement-ticket` and let it pull the AC from
the ticket — `/work` is the fallback when no ticket exists.

The actual step logic, halt formats, scoring breakdowns, and delivery
report are emitted by the engine. Do not paraphrase or reorder engine
output — surface it as-is. The two flows are mutually exclusive at the
state-file level: one `.work-state.json` carries one envelope at a
time, and the engine refuses to switch mid-flight.

The unified `./agent-config migrate` command sweeps any legacy
`.implement-ticket-state.json` file into the v1 `.work-state.json`
schema as one of its cleanup steps (see
`docs/contracts/migrate-command.md`). The wrapper invokes it
automatically when the legacy file is detected; agents should not
bypass the dispatcher.

## GitHub API: Replying to PR review comments

When commands reply to PR review comments (e.g. `/fix-pr-comments`):

### 1. Read the setting

Read `github.pr_reply_method` from `.agent-settings.yml`:

| Value | API call |
|---|---|
| `replies_endpoint` | `POST /repos/{owner}/{repo}/pulls/comments/{comment_id}/replies` with `{"body": "..."}` |
| `create_review_comment` | `POST /repos/{owner}/{repo}/pulls/{number}/comments` with `{"body": "...", "in_reply_to": comment_id}` |
| `auto` | Try `replies_endpoint` first. If it works → update setting. If 404/error → try `create_review_comment`. |

### 2. Bot icon prefix

Read `personal.pr_comment_bot_icon` from `.agent-settings.yml`:
- `true` → prefix reply body with `🤖 `.
- `false` or not set → no prefix.

### 3. API call rules

- `data` must be clean JSON with ONLY required API fields — no `summary` or extra params.
- Each reply is a separate API call — do NOT batch.
- On first success with `auto` → update `github.pr_reply_method` in `.agent-settings.yml` to the method that worked.

### Validate

1. Verify all command steps were executed in order.
2. Confirm expected output was produced (commit, PR, file change, etc.).
3. Check that no step was skipped or improvised.

## Output format

1. Command executed — all steps completed in order
2. Final result or summary as defined by the command

## Gotcha

- Don't ask questions when executing a command unless the command says "ask the user".
- Don't add opinions during execution — follow steps exactly.
- If a step fails, stop and report — don't improvise.

## Do NOT

- Do NOT ask questions during command execution unless the command says "ask the user".
- Do NOT add opinions or summaries — execute steps exactly as written.
- Do NOT improvise when a step fails — stop and report.

## Auto-trigger keywords

- slash command
- command execution
- agent command
