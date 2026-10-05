---
name: release-audit
description: |
  Detect-only pre-release validation sweep over the processkit content tree.
  Walks entity files, SKILL.md definitions, MCP server tools, and
  cross-references, then emits a single human-readable report with
  ERROR / WARN / INFO counts. Use when the user invokes `/pk-release-audit`,
  before tagging a release, or any time you need a comprehensive structural
  health check beyond what pk-doctor covers. Detect-only; never modifies any
  file under `context/`.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-release-audit
    version: "1.0.0"
    created: 2026-04-26T00:00:00Z
    category: processkit
    layer: 3
    uses:
      - skill: pk-doctor
        purpose: Complementary health check — pk-doctor covers schema/drift/migration checks; release-audit covers entity frontmatter, skill structure, MCP tool annotations, and cross-references.
    commands:
      - name: pk-release-audit
        args: "[--repo-root=<path>] [--tree=context|src-context|both]"
        description: "Run the pre-release validation sweep and print a single report."
---

# release-audit

## Intro

`/pk-release-audit` is the structural correctness sweep you run before
tagging a processkit release. It answers: "are all entity files, skill
definitions, MCP server tools, and cross-references internally consistent?"
without modifying any file.

The skill complements `pk-doctor`: doctor covers schema validation, drift
between `context/` and `src/context/`, and pending migrations; release-audit
covers entity frontmatter correctness, SKILL.md structural requirements, MCP
tool annotation completeness, and `uses:` cross-reference resolution.

Exit code is `0` if there are no ERRORs (WARNs are permitted), `1` if any
ERROR is found. This makes it suitable as a blocking CI gate before `git tag`.

## Overview

### Invocation

```
/pk-release-audit                       # detect-only; all four checks; report to stdout
uv run --script context/skills/processkit/release-audit/scripts/release_audit.py
uv run --script .../release_audit.py --repo-root=/path/to/repo
uv run --script .../release_audit.py --tree=src-context
uv run --script .../release_audit.py --tree=both
```

Exit code `0` = clean (0 ERRORs). Exit code `1` = at least one ERROR found.
The default `context` tree is the live dogfood/project tree. `src-context`
audits the shipped release deliverable tree under `src/context/` and does
not warn when dogfood-only entity directories such as `workitems/` or
`decisions/` are absent.

### The four checks

1. **`entity_files`** — walks every selected tree's `<dir>/*.md` for the registered
   entity directories (`workitems`, `decisions`, `logs`, `artifacts`, `actors`,
   `bindings`, `scopes`, `gates`, `roles`, `migrations`, `team`, `team-members`,
   `notes`, `discussions`). For each file verifies:
   - YAML frontmatter is present and parseable (between `---` markers).
   - `apiVersion: processkit.projectious.work/v2` is present.
   - `kind:` is present and is one of the 13 registered kinds.
   - `metadata.id` is present and matches the filename stem.

2. **`skill_structure`** — walks every selected tree's `skills/**/SKILL.md`. For each
   file verifies:
   - Frontmatter has `name`, `description`,
     `metadata.processkit.apiVersion`, `metadata.processkit.id`,
     `metadata.processkit.version`, `metadata.processkit.category`, and
     `metadata.processkit.layer` for processkit-category skills.
   - Body contains the four required sections: `## Intro`, `## Overview`,
     `## Gotchas`, `## Full reference`.

3. **`mcp_annotations`** — walks every selected tree's `skills/**/mcp/server.py`.
   For each file verifies that every `@server.tool(...)` decoration includes
   an `annotations=ToolAnnotations(...)` argument containing all four required
   hint keys: `readOnlyHint`, `destructiveHint`, `idempotentHint`,
   `openWorldHint`.

4. **`cross_references`** — walks every selected tree's `skills/**/SKILL.md` and reads
   `metadata.processkit.uses[*].skill`. For each named skill, checks that a
   corresponding `SKILL.md` exists at `context/skills/<category>/<name>/SKILL.md`
   (searches all category directories, not just `processkit/`). ERROR per
   unresolvable reference.

### What release-audit will NEVER do

- Modify any file under `context/` or `src/context/`.
- Validate YAML schemas against `src/context/schemas/` — that is pk-doctor's
  `schema_filename` check.
- Write to `context/logs/` — this tool is a CLI script, not an MCP server.
- Block on missing `context/templates/` — the template mirror is not consulted.

### Report shape

```
# pk-release-audit v1.0.0
repo_root: /path/to/repo

## entity_files — 0 ERROR / 0 WARN / 47 INFO
  [i] BACK-20260409_1449-BoldVale-fts5-full-text-search (workitems) — OK

## skill_structure — 1 ERROR / 0 WARN / 36 INFO
  [E] skill.missing-section — context/skills/foo/bar/SKILL.md missing section: ## Gotchas

## mcp_annotations — 0 ERROR / 0 WARN / 12 INFO
  [i] skill-gate:acknowledge_contract — annotations present

## cross_references — 0 ERROR / 0 WARN / 14 INFO
  [i] pk-doctor → event-log — resolved

## totals — 1 ERROR / 0 WARN / 109 INFO
```

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Running release-audit as a replacement for pk-doctor.** The two tools
  complement each other. Release-audit does NOT check schema conformance,
  drift, or pending migrations. Always run both before tagging.
- **Treating cross-reference ERRORs as false positives.** The `uses:` resolver
  searches all `context/skills/<category>/<name>/SKILL.md` paths. If a skill
  truly exists but is in an unexpected location, the fix is to correct the
  `uses:` entry, not to suppress the check.
- **Fixing ERRORs by editing files directly without understanding the cause.**
  A `metadata.id` mismatch ERROR means either the file was renamed without
  updating the frontmatter, or the frontmatter was edited without renaming the
  file. The correct fix depends on which copy is canonical — check git history.
- **Running release-audit against a partial tree.** The script walks the live
  `context/` tree from the detected repo root. Running it in a worktree or
  checkout missing some files will produce false ERRORs for every absent entity
  directory. Use `--tree=src-context` when auditing only the shipped
  release deliverable.
- **Ignoring WARNs before a release.** WARNs indicate structural drift that
  does not prevent the release but will accumulate into ERRORs in future
  versions. Address all WARNs before a minor or major release.

## Full reference

### CLI contract

```
release_audit.py [--repo-root=PATH] [--tree=context|src-context|both]
```

| Flag | Meaning |
|------|---------|
| `--repo-root` | Explicit repo root path. Defaults to `git rev-parse --show-toplevel`. |
| `--tree` | `context` audits the live tree, `src-context` audits the release deliverable tree, and `both` audits both. |

### Registered entity kinds

| kind | directory |
|------|-----------|
| `WorkItem` | `workitems/` |
| `DecisionRecord` | `decisions/` |
| `LogEntry` | `logs/` |
| `Artifact` | `artifacts/` |
| `Actor` | `actors/` |
| `Binding` | `bindings/` |
| `Scope` | `scopes/` |
| `Gate` | `gates/` |
| `Role` | `roles/` |
| `Migration` | `migrations/` |
| `TeamMember` | `team-members/` |
| `Note` | `notes/` |
| `Discussion` | `discussions/` |

### Required SKILL.md frontmatter fields

- `name` (string)
- `description` (string)
- `metadata.processkit.apiVersion` (string)
- `metadata.processkit.id` (string, must start with `SKILL-`)
- `metadata.processkit.version` (string)
- `metadata.processkit.category` (string)
- `metadata.processkit.layer` (integer or null)

### Required SKILL.md body sections

- `## Intro`
- `## Overview`
- `## Gotchas`
- `## Full reference`

### Required MCP tool annotation keys

- `readOnlyHint`
- `destructiveHint`
- `idempotentHint`
- `openWorldHint`

### Adding a check in future versions

1. Add a new check function in `release_audit.py` following the
   `run_<name>(repo_root) -> list[Finding]` pattern.
2. Register it in `CHECKS` at the bottom of the file.
3. Add a gotcha for that check in this SKILL.md.
4. Mirror the updated script to `src/context/skills/processkit/release-audit/scripts/`.
