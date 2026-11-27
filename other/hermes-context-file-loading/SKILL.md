---
name: hermes-context-file-loading
description: >-
  Trace which SOUL.md, AGENTS.md, MEMORY.md or USER.md Hermes loads into the system prompt. When an
  instruction is ignored, duplicated or put in the wrong layer, check project-file precedence,
  working directory, subagent inheritance and prompt caching. Not for
  agent-operating-contract-evolution.
metadata:
  revision: "5"
  areas: "software-development"
  targets: "hermes"
  summary: "which Hermes instruction file loads from where, which project file wins, and which prompt tier a rule belongs to"
  summary_zh: "Hermes 指令文件各自从何处加载、哪个项目文件生效，以及规则该放进哪个 prompt 层"
  kind: "entry"
---

# Trace Hermes context files

Resolve the installed Hermes revision, effective profile home, entry point,
terminal backend and session cwd. Read back the selected profile's effective
`terminal.cwd`, but verify the actual cwd used for prompt assembly: local CLI,
gateway and worker entry points can differ. Do not infer the result from a
config file or scan unrelated profiles.

For startup, separate the profile's identity (`SOUL.md`) from project context
and from memory/user snapshots. At the pinned revision, the project slot tries
the nearest `.hermes.md` / `HERMES.md`, the merged `AGENTS.md` directory chain,
then cwd-scoped `CLAUDE.md` or Cursor rules. A loaded Hermes project file
suppresses the entire AGENTS chain. Tool-result subdirectory hints are a
different injection path. A delegated child can skip identity and project
context; pass required instructions explicitly instead of assuming inheritance.

Use the [versioned loader probe](references/loader-2de9f51.md) for per-directory
override precedence, filtering and an isolated readback. For requested edits
or de-duplication, use the [audit workflow](references/auditing-instruction-files-workflow.md).
Keep identity in the profile, project rules in project files, durable user
facts in the appropriate memory layer, and reusable procedures in skills.

Report observed files and precedence, effective profile and cwd, the prompt tier
or hint path, and any unverified inheritance or caching behavior. Recheck the
installed source after an upgrade before applying the pinned mechanics.
