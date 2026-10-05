---
name: lril
description: >
  Second-brain workflow command suite for Claude Code, built around the PIV
  loop (Plan → Implement → Validate) from the Dynamous claude-code-second-brain
  workshop. Installs 19 slash commands under the `lril:` namespace covering
  project priming, feature planning, plan execution, code review, root-cause
  analysis, bug fixing, validation, PRD creation, atomic commits, and a content
  ideation suite (LinkedIn, X, YouTube, Shorts). Use when you want a repeatable,
  reviewable engineering workflow instead of one-shot prompting — prime the
  agent on a codebase, plan a feature, execute the plan, then review and
  validate the result.
---

# LRIL — Second-Brain Workflow Commands

A cohesive suite of slash commands that turn ad-hoc prompting into a repeatable,
reviewable engineering loop. Originally from the Dynamous
*claude-code-second-brain* workshop.

After installing, the commands are available under the `lril:` namespace
(e.g. `/lril:prime`, `/lril:plan-feature`, `/lril:execute`).

## The PIV loop

The core workflow is **Plan → Implement → Validate**:

1. **Prime** — `/lril:prime` (and `/lril:prime-tools`) load codebase context so
   the agent understands structure, stack, conventions, and current state.
2. **Plan** — `/lril:plan-feature` produces a comprehensive, research-backed
   feature plan; `/lril:create-prd` turns a conversation into a PRD.
3. **Implement** — `/lril:execute` runs an implementation plan;
   `/lril:implement-fix` and `/lril:rca` handle bug fixing and root-cause
   analysis.
4. **Validate** — `/lril:code-review` (pre-commit technical review),
   `/lril:code-review-fix`, `/lril:validate`, and `/lril:commit` close the loop
   with atomic, conventionally-tagged commits.
5. **Reflect** — `/lril:execution-report` and `/lril:system-review` compare what
   was built against the plan to surface process improvements.

## Commands

| Command | Purpose |
|---------|---------|
| `prime` | Prime the agent with codebase understanding |
| `prime-tools` | Prime the agent on available tools/MCP servers |
| `init-project` | Initialize project conventions and context |
| `plan-feature` | Create a comprehensive feature plan with deep codebase analysis and research |
| `create-prd` | Create a Product Requirements Document from a conversation |
| `execute` | Execute an implementation plan |
| `implement-fix` | Implement a fix for an identified issue |
| `rca` | Root-cause analysis for a bug or failure |
| `code-review` | Technical code review for quality and bugs (runs pre-commit) |
| `code-review-fix` | Apply fixes surfaced by a code review |
| `validate` | Validate an implementation against its requirements |
| `commit` | Commit all uncommitted changes with an atomic, conventionally-tagged message |
| `execution-report` | Generate an implementation report for system review |
| `system-review` | Analyze implementation against plan for process improvements |
| `content-all` | Generate content for all channels at once |
| `content-linkedin` | Draft a LinkedIn post |
| `content-x` | Draft an X / Twitter post |
| `content-youtube` | Draft YouTube content |
| `content-shorts` | Draft short-form video content |

## How it installs

This skill folder contains a Claude Code plugin (`.claude-plugin/plugin.json`)
plus the command definitions under `commands/`. The installer copies the whole
folder to `~/.claude/skills/lril/` (global) or `.claude/skills/lril/` (project),
which is exactly where Claude Code expects the `lril:` command suite to live.
Restart Claude Code after installing and the `/lril:*` commands become available.
