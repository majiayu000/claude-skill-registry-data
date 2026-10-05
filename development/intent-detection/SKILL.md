---
name: intent-detection
description: "Route ambiguous Home Assistant (integration/coordinator/config-flow/Lit) work requests to the correct /ha: workflow. Use when intent is unclear, mixed (bug fix vs. refactor), or scope is ambiguous."
effort: medium
user-invocable: false
---

# Intent Detection — Workflow Routing

When user describes work WITHOUT specifying a `/ha:` command, analyze their intent and suggest the appropriate workflow BEFORE starting work.

**Hard guard — check FIRST**: if the message starts with any slash command
(`/ha:`, `/coordinator:`, `/lit:`, or any other `/command`), this skill does not apply.
Follow the invoked command directly — no routing analysis, no suggestion, zero
output from this skill.

## Routing Table

| Signal | Detected Intent | Suggest |
|--------|----------------|---------|
| "bug", "error", "crash", "failing", "broken", stack trace | Bug investigation | `/ha:investigate` |
| "brainstorm", "explore idea", "not sure what I need", "vague idea", "let's discuss", "how to approach" | Ideation/requirements | `/ha:brainstorm` |
| "add", "implement", "build", "create" + multi-step | New feature | `/ha:plan` |
| "review", "check", "audit" code | Code review | `/ha:review` |
| "fix" + small/specific scope | Quick fix | handle directly or `/ha:quick` |
| "refactor", "clean up", "improve" | Refactoring | `/ha:plan` (needs scope) |
| "research", "how to", "what's the best" | Research | `/ha:research` |
| "evaluate", "compare", "adopt", "library", "should we use" | Library evaluation | `/ha:research --library` |
| "test", "spec", "coverage" | Testing | handle directly or `/ha:plan` |
| Describes 1-2 file changes, < 50 lines | Small task | handle directly |
| "deploy", "release", "production" | Deployment | `/ha:verify` then deploy |
| "performance", "slow", "blocking I/O", "event loop", "memory" | Performance | `/ha:perf` |
| "PR review", "review comments", "address feedback", "respond to PR" | PR response | `/ha:pr-review` |
| "that worked", "fixed it", "problem solved" | Knowledge capture | `/ha:compound` |
| "enhance plan", "more detail", "deepen" | Plan enhancement | `/ha:plan --existing` |
| "triage", "which findings", "prioritize fixes" | Finding triage | `/ha:triage` |

### Framework-development routing (audience gate)

Some requests are about developing Home Assistant *itself* — the `homeassistant/`
core or the frontend framework layer — not authoring an integration. Route these
to the framework-development skills ONLY when the project is a **core checkout**
(`homeassistant/__init__.py` + `script/`) or the **frontend repo**
(`home-assistant-frontend` in `package.json`); never for a custom-integration
project. Detection matches `hooks/scripts/detect-target.sh`.

| Signal (framework-dev target only) | Detected Intent | Suggest |
|---|---|---|
| Editing `homeassistant/helpers/`, `core.py`, `config_entries.py`, `bootstrap.py`, `loader.py`, `websocket_api/`, `auth/`, `util/` | Core internals work | `core-internals` skill |
| "public helper", "core API", "rename this helper", "TypedDict interface", boot resilience | Core-internals contract | `core-internals` skill |
| Editing `script/`, hassfest validators, `tests/common.py`, `tests/conftest.py` | Dev-tooling work | `dev-tooling` skill |
| "break a core API", "deprecate", "new device class", "entity-model change", "needs an ADR", "architecture discussion" | Architecture/process | `architecture-process` skill (PR4: stop and open a discussion) |
| Editing `src/state/`, `src/entrypoints/`, `src/mixins/`, `src/common/`, `src/util/`, build scripts (frontend repo) | Frontend internals | `lit-patterns` framework-internals sections (FI-1…FI-6) |

If the target is a plain integration or custom-integration project, do NOT surface
these — the integration-authoring routing above applies instead.

## Behavior

1. Read user's first message
2. Match against routing table (use keyword + context signals, not exact match)
3. If match found with multi-step workflow: "This looks like [intent]. I'd suggest `[command]` — want me to run it, or should I just dive in?"
4. If trivial task (typo, single-line fix, config change): skip suggestion, just do it
5. If user already specified a `/ha:` command: follow it, don't re-suggest
6. **NEVER block the user** — suggestion only, not mandatory

## Confidence Signals

High confidence (suggest immediately):

- Stack trace or error message pasted → `/ha:investigate`
- "Add [feature] with [multiple components]" → `/ha:plan`
- "Review my changes" or "check this PR" → `/ha:review`

Medium confidence (suggest with caveat):

- "Fix [thing]" — could be quick or complex, suggest based on scope description
- "Update [thing]" — could be small edit or refactor

Low confidence (just do it):

- Single file mentioned, clear change
- "Change X to Y"
- Configuration or dependency updates

## Complexity Signals

When a task matches a workflow command, check complexity before suggesting:

**Trivial signals** (suggest `/ha:quick` or handle directly):

- Single file mentioned explicitly
- "exclude X from Y", "add X to config", "rename", "change X to Y"
- Problem + solution both stated ("X is wrong, change to Y")
- One-line fix described

**Complex signals** (suggest `/ha:plan` or `/ha:investigate`):

- 3+ modules or files mentioned
- "intermittent", "race condition", "sometimes", "random"
- Stack trace with 5+ frames
- "across", "all", "every" (scope indicators)

**Override rule**: If user invokes `/ha:full` but task matches trivial signals:
"This looks like a quick fix. Want `/ha:quick` instead, or stick with the full cycle?"

## Iron Laws

1. **NEVER block on suggestion** — If user starts explaining, just do the work
2. **One suggestion max** — Don't re-suggest if user ignores first suggestion
3. **Commands are shortcuts, not gates** — All work can be done without commands

## Routing Logic Example

```
if has_slash_command($ARGUMENTS) -> follow command directly
elif has_stack_trace(message) -> suggest /ha:investigate
elif matches("add|build|implement", message) and multi_step -> suggest /ha:plan
elif matches("fix", message) and small_scope -> handle directly or /ha:quick
elif matches("review|audit", message) -> suggest /ha:review
else -> handle directly (no suggestion)
```

## Integration

This skill is consulted at session start. It works alongside:

- SessionStart hook (shows plugin loaded message)
- CLAUDE.md routing instructions (passive reference)
- Individual workflow skills (activated by commands)
