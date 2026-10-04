---
name: mbg-extension-authoring
description: Creates or reviews canonical agent skills and workflows under .ai/, plus OpenCode-only custom tools under .opencode/tools, for the Microelectronic Block Generator repository. Use this for authoring or reviewing SKILL.md files, .ai/workflows entries, or .opencode/tools/*.ts files. Do not use it for analog design, simulation, routing, DRC, LVS, or PEX implementation.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-extension-authoring/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Extension Authoring

## Purpose

Create safe, consistent, and reviewable agent extensions for the
Microelectronic Block Generator project: skills, workflows, and (OpenCode
only) custom code tools.

## When to Use

- Creating or reviewing a canonical `SKILL.md` under `.ai/skills/`.
- Creating or reviewing a canonical workflow under `.ai/workflows/`.
- Creating an OpenCode-only custom tool under `.opencode/tools/*.ts`.
- Updating project-level shared instructions (`AGENTS.md`).
- Reviewing the authoring standard itself
  (`docs/opencode/AUTHORING_GUIDE.md`).

## When Not to Use

Do not use this skill to implement:

- Analog circuit topology, transistor sizing, or device placement.
- Routing or power structures.
- Simulation algorithms.
- DRC, LVS, or PEX engines.

These tasks remain dependencies of their respective project owners (Huda:
analog/placement/routing/power/simulation; Ahmad: DRC/LVS/PEX/verification
automation).

## Required Inputs

Before creating an extension, determine:

1. Extension type (skill, workflow, or OpenCode tool).
2. Extension name (must use the `mbg-` prefix).
3. Primary responsibility — one clear job.
4. Intended platforms (`opencode`, `Codex`, `codex` — a skill or workflow
   almost always targets all three; a code tool targets `opencode` only,
   since it is the only platform among the three that supports code
   tools).
5. Required inputs, expected outputs, and side effects.
6. Failure conditions.
7. Owner and dependencies on other team members' modules.

## Preconditions

- **`.ai/` is the source of truth.** Do not create or edit files directly
  under `.opencode/skills/*`, `.Codex/skills/*`,
  `plugins/mbg-analog/skills/*`, `.opencode/commands/*`, or
  `.Codex/commands/*` — those directories are generated output. A sync
  script (`scripts/sync_agent_tools.py`) reads `.ai/skills/`,
  `.ai/workflows/`, and `.ai/manifest.json` and regenerates the per-platform
  adapters. Any hand-edit made directly to a generated adapter file is
  silently discarded the next time the sync script runs.
- The one documented exception is `.opencode/tools/*.ts`: OpenCode is the
  only one of the three platforms that supports arbitrary code tools, so
  those files are authored directly in place and are not generated from
  `.ai/`.
- For a skill or workflow name, the directory (skill) or file basename
  (workflow) must exactly match the `name` field in its frontmatter.

## Naming Rules

Project-specific extensions must use the `mbg-` prefix. Names must:

- Use lowercase letters, digits, and single hyphens as separators.
- Not contain spaces, underscores, consecutive hyphens, or leading/trailing
  hyphens.

Examples: `mbg-extension-authoring`, `mbg-repo-analysis`,
`mbg-placement-debug`, `mbg-new-skill`.

## Workflow

### Authoring a skill

1. Create `.ai/skills/<skill-name>/SKILL.md`.
2. Use flat frontmatter only — the sync script's parser is hand-rolled and
   does not support nested YAML maps, block lists, or multi-line folded
   scalars. Write list fields inline: `capabilities: [cap_a, cap_b]`,
   `platforms: [opencode, Codex, codex]`.

   ```yaml
   ---
   name: mbg-example-skill
   description: 2-4 sentences — what it does, when to use it, when not to.
   class: READ-ONLY | GENERATING | MUTATING | DESTRUCTIVE
   owner: huda | ahmad | jabir
   capabilities: [cap_id]
   platforms: [opencode, Codex, codex]
   ---
   ```
3. Follow the project's section layout in
   `docs/opencode/AUTHORING_GUIDE.md`: `## Purpose`, `## When to Use`,
   `## When Not to Use`, `## Required Inputs`, `## Preconditions`,
   `## Workflow`, `## Outputs`, `## Failure Modes`.
4. Keep the body platform-neutral — do not write "OpenCode" or
   "Codex" into the instructions unless the skill is genuinely about
   authoring for that one platform (as this skill is, for the code-tool
   section above). The same body ships to all three adapters.
5. Do not invent tools, APIs, modules, or verification results that do not
   exist in the codebase — verify every referenced function or module by
   reading the actual source first.
6. Run `python3 scripts/sync_agent_tools.py` to regenerate the OpenCode,
   Codex, and Codex adapters from the new `.ai/skills/` entry, and to add
   it to `.ai/manifest.json` if the manifest itself needs a new capability
   entry (the manifest is owned by the lead and hand-edited separately —
   coordinate rather than editing it unreviewed).

### Authoring a workflow

1. Create `.ai/workflows/<workflow-name>.md`.

   ```yaml
   ---
   name: mbg-example-workflow
   description: One sentence.
   agent: build | plan
   platforms: [opencode, Codex]
   ---
   ```
2. Use `plan` for read-only analysis/review workflows, `build` when the
   workflow may create or edit files.
3. Use `$ARGUMENTS` for the full argument string, or `$1`/`$2`/... for
   positional arguments. Stop and report a missing required argument
   instead of guessing.
4. Reference only skills and capabilities that actually exist — check
   `.ai/manifest.json`'s `capabilities` and `workflows` sections.
5. Run `python3 scripts/sync_agent_tools.py` after creating or editing the
   file.

### Authoring an OpenCode custom tool

Only for genuinely OpenCode-specific code tools; skills and workflows are
never the right place for this.

1. Create `.opencode/tools/<tool-name>.ts` directly (not generated).
2. Use the `tool()` helper from `@opencode-ai/plugin`, define a precise
   `description`, validated `args` via `tool.schema`, and an `execute`
   function that returns a structured result.
3. Resolve any accepted filesystem path against `context.worktree`; reject
   empty paths, absolute paths, and `../` parent traversal. See the
   `resolveInsideWorktree` pattern in `docs/opencode/AUTHORING_GUIDE.md`.
4. Never read `.env` or credential files; never embed a personal absolute
   path.
5. This file type has no `.ai/` source — it is authored once, in place,
   and not touched by the sync script.

## PDK Body Constraint

**MOSFET body: `pfet_03v3` -> VDD ONLY, `nfet_03v3` -> VSS ONLY.** Any
skill, workflow, or tool that generates or processes SPICE netlists must
state and enforce this rule.

## Outputs

Report, for any extension created or reviewed:

```text
Extension type:
Name:
Owner:
Platforms:
File(s) created or edited:
Capability/manifest entry (if any):
Sync command run: python3 scripts/sync_agent_tools.py
Validation performed:
Known limitations:
```

## Failure Modes

- **Editing a generated adapter directly** — e.g. hand-editing
  `.opencode/skills/<name>/SKILL.md` or `.Codex/skills/<name>/SKILL.md`.
  Stop and redirect the edit to the corresponding `.ai/` file instead; the
  generated copy will be overwritten on the next sync.
- **Nested or block YAML in frontmatter** — the sync script's parser is
  minimal and does not handle it (no PyYAML is available in this repo's
  Python environments). Flatten to `key: value` lines and inline lists.
- **Directory/file name does not match the frontmatter `name`** — reject
  and correct before proceeding.
- **Referencing a capability, entry point, or module that does not exist**
  — verify with a source-code search before writing it into a skill or
  workflow body.
- **Missing `mbg-` prefix or invalid kebab-case** — reject the name and
  request a valid one.

## Safety Rules

- Never read or display `.env`.
- Never include API keys or credentials.
- Never include personal absolute filesystem paths.
- Never use unlimited retry or refinement loops.
- Never claim simulation or verification success without evidence.
- Never modify another team member's owned implementation outside the
  assigned scope.
- Never stage, commit, or push automatically.
