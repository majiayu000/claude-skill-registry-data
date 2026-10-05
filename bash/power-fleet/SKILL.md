---
name: power-fleet
description: Use when approved phases should run in parallel — visually in a cmux panel or unattended — when fleet status is requested, or when a fleet member must be stopped or merged
---

# Operate a Fleet

Read [fleet](../../references/fleet.md) before launching, resuming, or tearing down;
[cmux](../../references/cmux.md) before a visual panel; [safety](../../references/safety.md) before
the first launch — the privileged flags and the fixed-runtime rule live there; and
[artifacts](../../references/artifacts.md) when a `fleet/` record or path is unfamiliar. `--status`
needs none of them.

## Routes

| Route | Meaning |
|---|---|
| `<slug...>` | launch 1–4 approved phases as a **visual panel** — the default |
| `<slug...> --auto` | launch them unattended, one workspace each, as the fleet did before panels |
| `<slug...> --via-kanban` | launch through the Hermes Kanban board — see [kanban](../../references/kanban.md) |
| `--status` | one-shot dashboard |
| `--teardown <slug> [--merge]` | stop one member |
| `--teardown --all` | stop every validated member, one call each |

Pass `--merge` only when the human explicitly asks for it.

## Launch

**Visual is the default.** A panel is one cmux workspace holding one pane per member, each pane an
interactive provider session in its own worktree, seeded with that phase's brief. The human watches
all of them at once and steers any of them. `--auto` selects the previous behaviour: unattended
members, one workspace each, structured results and correction cycles.

Tell the human, before launching a panel, that every pane opens on a folder-trust prompt and waits
there: each worktree is a path the provider has never seen, and the permission flag gates tools,
not folders. One answer per pane, given by them. A panel that looks stuck on arrival is usually
this.

A panel holds **1 to 4 members**. Four panes is where a grid stops being readable, and an unreadable
panel defeats the point of having one. Only one panel may be active at a time: a second one cannot
reuse the first's workspace without splitting into it and typing a privileged command into a live
shell, which is exactly what the packaged scripts exist to avoid.

1. Inspect repository status and confirm a named current branch. Read `config.json` and the
   requested `spec.md` and `plan.md`. **Never read a generated fleet environment file.**
2. Resolve scripts from this installed skill at `../../scripts/`. Call only the packaged fleet
   scripts; never assemble a provider command yourself.
3. **Use the launcher of the runtime you are, and never another.** The runtime is fixed by that
   choice, recorded in the member, and refused by a runner bound to a different one. There is
   no default and no override.

   | You are | Visual launcher | Autonomous launcher |
   |---|---|---|
   | Claude Code | `claude-fleet-panel.sh` | `claude-fleet-up.sh` |
   | Codex | not implemented | `codex-fleet-up.sh` |
   | Hermes | not implemented | `hermes-fleet-up.sh` |

   | You are | Visual vector | Autonomous vector |
   |---|---|---|
   | Claude Code | `claude --dangerously-skip-permissions <brief>` | `claude -p --dangerously-skip-permissions --no-session-persistence --output-format json <prompt>` |
   | Codex | — | `codex exec --dangerously-bypass-approvals-and-sandbox --ephemeral --cd <worktree> --output-schema <schema> --output-last-message <file> <prompt>` |
   | Hermes | — | `hermes -z <prompt> --in <worktree> --yolo --accept-hooks` |

   Visual mode on `codex` and `hermes` fails with `visual mode is not implemented for the <runtime>
   runtime`. Route those runtimes to `--auto`.

4. **Before the first launch, display your runtime's exact command shape and require explicit
   acknowledgement of its dangerous flag** — `--dangerously-skip-permissions`,
   `--dangerously-bypass-approvals-and-sandbox`, or `--yolo`. No acknowledgement, no launch.
   Reject any configured `permission_mode` other than `danger-full-access`.

   **The gate applies to visual mode too, and is not softened by it.** A human watching a pane is
   not a human approving a tool call: the session still runs with permissions bypassed, and it
   still acts on its own between glances. Show the interactive shape, not the autonomous one.
5. For several slugs, compare their specs and plans for repeated repository paths. Emit an
   advisory overlap warning naming the paths and let the human decide. Do not block
   automatically — plausible overlap is common and only the human knows if it matters here.
6. Visual: invoke `claude-fleet-panel.sh` **once with every acknowledged slug**, because the grid
   is built in a single call. Autonomous: invoke `claude-fleet-up.sh` once per slug, stopping
   after any failure and reporting the recovery state rather than pressing on with a partial
   fleet. The panel reports which members it could provision and names the one that failed.

The launcher owns provisioning; the runner owns the lifecycle. Neither is yours to reimplement.

## Status

Invoke `fleet-dashboard.sh --once` and report each slug with its runtime, stage, status, ports,
branch, and a short message.

**Do not load or reproduce fleet logs, prompts, or result payloads**, and do not print absolute
worktree paths. If someone needs a log, give them the path to read, not its contents.

## Teardown

`fleet-teardown.sh <slug>` stops the stack, closes the member's cmux surface or workspace, and
removes the member record, **preserving the branch and the worktree**. That default is deliberate:
a fleet member that failed is evidence.

For a panel member it closes **its pane** and leaves the workspace to its siblings; the workspace
goes only with the last member out. A panel member whose pane was never recorded is reported and
left alone rather than closed by closing the whole panel.

`--merge` is refused for any member that is not `DONE`, and re-validates the terminal status
before merging. The database volume is always kept and reported.

For `--teardown --all`, enumerate validated `fleet/<slug>.json` entries and call the script once
per slug. Never hand it a glob.

## When something is wrong

| Symptom | Meaning |
|---|---|
| `cmux: no socket` | cmux is not running. Say so; do not proceed without it. |
| Every panel pane sits on a folder-trust prompt | expected, not a fault. A worktree is a path the provider has never seen, and the permission flag does not answer a trust dialog — it gates tools, not folders. The human answers it once per pane. Never answer it for them. |
| `a visual fleet panel is already active` | one panel at a time. Tear the current one down first. |
| `a panel holds at most 4 members` | split the work across two panels, run some with `--auto`, or drop a slug. |
| `visual mode is not implemented for the … runtime` | that runtime has no interactive vector here. Use `--auto`. |
| `registered fleet member does not match…` | you are the wrong runtime for this member, or the worktree moved. |
| `approved fleet contracts changed…` | someone edited the spec or plan mid-flight. The member is stopped on purpose. |
| A retained runner lock | a provider process group could not be proven gone. A human must look before relaunching. |
| `invalid structured result` | the provider answered with something that is not the contract. Both the parsed file and the provider's raw bytes are preserved next to the member's results — give the human the path, never the contents. |
| A member stopped mid-flight | relaunch the runner with `--resume` once a human has looked. It re-runs the recorded stage and keeps the correction count; without it, a re-run fails on the first finished stage. |

None of these are retried by re-running the launcher. Resolve the cause first.
