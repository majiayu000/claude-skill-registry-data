---
name: openspec-sdd
description: >-
  Spec-driven development (SDD) using OpenSpec with GitHub Copilot. Use when initializing
  OpenSpec in a project, writing specifications (requirements + scenarios), proposing changes
  with delta specs, designing and breaking down tasks, implementing from tasks.md, verifying
  against specs, syncing/archiving completed changes, managing the openspec/ directory,
  or adopting specs in existing brownfield codebases.
  Triggers: "openspec", "spec-driven", "SDD", "write specs", "propose a change",
  "delta spec", "archive change", "opsx", "/opsx:", "GIVEN/WHEN/THEN scenarios",
  "requirements specification", "change proposal", "brownfield specs", "verify implementation".
metadata: 
    version: 0.2.0
    author: arisng
---

# OpenSpec Spec-Driven Development

Specify what to build before writing code. Track changes as structured proposals. Keep specs as living documentation.

**Principle**: Fluid, iterative, brownfield-first. Artifacts are enablers, not gates.  
**Source**: <https://github.com/Fission-AI/OpenSpec>

## Prerequisites

- Node.js >= 20.19.0
- `npm install -g @fission-ai/openspec@latest`
- Initialize: `openspec init --tools github-copilot` (creates `openspec/` + `.github/` integration)

## Directory Structure

```
openspec/
├── config.yaml                                      # Project context + artifact rules
├── specs/<product-ns>/<domain>/spec.md              # Current-state specs (multi-system)
│   # OR specs/<domain>/spec.md                      # (single-system repos)
├── changes/<change-name>/                           # Active change proposals
│   ├── .openspec.yaml
│   ├── proposal.md
│   ├── specs/<product-ns>/<domain>/spec.md          # Delta specs (ADDED/MODIFIED/REMOVED/RENAMED)
│   ├── design.md
│   └── tasks.md
└── changes/archive/YYYY-MM-DD-<name>/               # Completed changes
```

> **`<product-ns>` vs `<domain>`**: `<product-ns>` (product namespace) is a stable folder that groups related domains under one system or product area — e.g. `ordering/`, `billing/`, `auth/`. `<domain>` is a single capability within that area — e.g. `payments/`, `invoices/`, `sessions/`. Use `<product-ns>/<domain>/` in repos that host multiple distinct systems; use `<domain>/` alone in single-system repos.
> This directory path segment is **unrelated** to the SDD process steps below.

## SDD Process

```
/opsx:explore  →  Think, investigate, clarify (no code, no artifacts)
/opsx:propose  →  Create change + all planning artifacts in one step
/opsx:apply    →  Implement tasks from tasks.md checklist
/opsx:archive  →  Validate, merge delta specs, move to archive
```

**Typical flow**: `propose` → `apply` → `archive`.  
Use `explore` first when the problem has hidden design gaps or ambiguities.

## Child Skills

`openspec-sdd` is an entry-point/routing skill. Each phase of the SDD process is implemented by a dedicated **child skill** that carries the focused instructions for that step only.

### Why separate skills, not one bundle?

- **CLI-generated and CLI-owned** — `openspec init --tools github-copilot` and `openspec update` write these skill files to `.github/skills/`. This is confirmed: running `openspec update --force` regenerates all four child skill files at the same timestamp as their matching `.github/prompts/opsx-*.prompt.md` files. Because the CLI owns these files, merging child skill content into a hand-authored parent skill would create a drift problem every time `openspec update` runs.
- **Context efficiency** — A developer running `/opsx:apply` doesn't need the explore or propose rules in their context window. Loading only the relevant child skill keeps token overhead low.
- **Independent triggering** — Each child skill has its own `description` frontmatter with specific trigger phrases, so it can fire directly without routing through the parent.

### What `openspec update` generates for GitHub Copilot

For each workflow in your active config, the CLI generates **two files** under `.github/`:

| File type | Path | Purpose |
|---|---|---|
| Skill | `.github/skills/openspec-<workflow>/SKILL.md` | Loaded by Copilot automatically via skills discovery |
| Prompt | `.github/prompts/opsx-<workflow>.prompt.md` | Invokable via `/opsx:<workflow>` slash command |

Both files are stamped with `generatedBy: "<version>"` metadata and share an identical write timestamp after each `openspec update` run. The active workflow list is controlled by the `workflows` key in global config (see [Profile vs Custom Profile](#profile-vs-custom-profile) below).

### Currently generated child skills (this repo)

```bash
openspec config list  # profile: custom, delivery: both, workflows: propose/explore/apply/archive
```

| Child skill | Location | Phase |
|---|---|---|
| `openspec-explore` | `.github/skills/openspec-explore/` | Explore |
| `openspec-propose` | `.github/skills/openspec-propose/` | Propose |
| `openspec-apply-change` | `.github/skills/openspec-apply-change/` | Apply |
| `openspec-archive-change` | `.github/skills/openspec-archive-change/` | Archive |

### Profile vs Custom Profile

OpenSpec has two profiles, configured globally via `openspec config profile`:

**`core`** — Opinionated preset. Generates the four base workflows (explore, propose, apply, archive) with a fixed, non-configurable setup. No `openspec config set` needed.

**`custom`** — Unlocks three configurable settings:

| Setting | Values | Effect |
|---|---|---|
| `delivery` | `both` \| `prompts` \| `skills` | What `openspec update` generates — both skill + prompt files, prompts only, or skills only |
| `workflows` | Array of workflow names | Which workflows to include; controls how many skill/prompt pairs are generated |
| `featureFlags` | Object | Feature-specific toggles |

**Concrete example — this repo's config** (`C:\Users\ADMIN\AppData\Roaming\openspec\config.json`):
```json
{
  "profile": "custom",
  "delivery": "both",
  "workflows": ["explore", "propose", "apply", "archive"]
}
```
Result: 4 skill files + 4 prompt files generated (identical to `core` output, but each setting is now explicit and editable).

**Concrete example — prompts-only delivery** (for a team that doesn't use Copilot skills routing):
```json
{
  "profile": "custom",
  "delivery": "prompts",
  "workflows": ["explore", "propose", "apply", "archive"]
}
```
Result: only `.github/prompts/opsx-*.prompt.md` files generated; no `.github/skills/` files written.

To switch and regenerate: `openspec config profile` (interactive) → `openspec update`.

### Role of `openspec-sdd` (this skill)

`openspec-sdd` covers everything the child skills don't: initialization, brownfield adoption, the mutation rule, the decision table, config, profile setup, and the overall mental model. It also serves as the landing skill when the user's intent spans multiple phases or doesn't map cleanly to a single child skill command.

## AI Coding Agent Adaptation

When slash prompts aren't available, use skill files or CLI steps directly:

| Alias | Skill file | CLI equivalent |
|---|---|---|
| `/opsx:explore` | `openspec-explore/SKILL.md` | `openspec list --json`, read files, no artifacts |
| `/opsx:propose` | `openspec-propose/SKILL.md` | `openspec new change <name>` + `openspec instructions` |
| `/opsx:apply` | `openspec-apply-change/SKILL.md` | `openspec status --change "<name>" --json` → implement tasks |
| `/opsx:archive` | `openspec-archive-change/SKILL.md` | `openspec archive <name> -y` |

Read [references/ai-coding-agent-workflow.md](references/ai-coding-agent-workflow.md) before modifying anything under `openspec/`.

## Config

```yaml
# openspec/config.yaml
schema: spec-driven
context: |
  Tech stack: Node.js 22, Express 5
  Tests: Vitest + supertest
rules:
  specs:
    - Use GIVEN/WHEN/THEN for all scenarios
  tasks:
    - Each task must be independently verifiable
```

`context` is injected into all generated artifacts (keep concise, max 50 KB).

## Agent Decision Guide

| Situation | Action |
|---|---|
| Problem unclear or complex | `/opsx:explore` — clarify first, never write code |
| Ready to plan + implement | `/opsx:propose` → `/opsx:apply` → `/opsx:archive` |
| Granular artifact control needed | `/opsx:new` → `/opsx:continue` (repeat) → `/opsx:apply` |
| Multiple small changes | `/opsx:propose` each → `/opsx:bulk-archive` |
| Implementation done, need validation | `/opsx:verify` |
| Specs changed mid-implementation | `/opsx:sync` then continue `/opsx:apply` |
| New contributor onboarding | `/opsx:onboard` |
| Existing codebase, no specs yet | [Brownfield Adoption](#brownfield-adoption) |
| Change should be abandoned | Delete folder from `openspec/changes/` |
| Multiple changes touch same domain | `/opsx:bulk-archive` (conflict detection built-in) |

For detailed per-command behavioral rules (explore/apply/verify/archive), see [references/command-rules.md](references/command-rules.md).

## Spec Format

Requirements use RFC 2119 keywords (SHALL/MUST/SHOULD/MAY). Scenarios use GIVEN/WHEN/THEN. No implementation details in specs — those go in `design.md`.

See [references/spec-format.md](references/spec-format.md) for the full template, delta spec marker usage (ADDED/MODIFIED/REMOVED/RENAMED), and RFC 2119 guidance.

**Delta merge order during archive**: RENAMED → REMOVED → MODIFIED → ADDED.

## Change Artifacts

| Artifact | Purpose |
|---|---|
| `proposal.md` | Why + what changes + impact + rollback |
| `specs/<domain>/spec.md` | Delta specs — behavioral changes only |
| `design.md` | Technical approach, architecture decisions, file changes |
| `tasks.md` | Phased checklist with `- [ ]` / `- [x]` checkboxes |

For detailed templates, see [references/artifact-templates.md](references/artifact-templates.md).

## Brownfield Adoption

1. `openspec init --tools github-copilot` — creates `openspec/` + `.github/` integration files
2. Edit `openspec/config.yaml` with tech stack and conventions
3. `/opsx:explore` — map current architecture, identify spec domains
4. Create `openspec/specs/<domain>/spec.md` for each domain, describing **current** behavior  
   *(baseline capture — the only time direct spec edits are permitted)*
5. All future changes: `/opsx:propose` → `/opsx:apply` → `/opsx:archive`

## Current-Spec Mutation Rule

`openspec/specs/**` is protocol-governed. Do not directly edit main specs for new, changed, renamed, or removed behavior.

- Stage all behavior changes in `openspec/changes/<name>/specs/**` first
- Merge into main specs only via `sync` or `archive`
- Exception: brownfield baseline capture (Step 4 above) and user-approved repair of corrupted content

Full policy: [references/ai-coding-agent-workflow.md](references/ai-coding-agent-workflow.md)

## CLI Quick Reference

Key commands: `openspec init`, `openspec new change <name>`, `openspec status --change "<name>" --json`, `openspec validate --all`, `openspec archive <name> -y`

Full command reference and flags: [references/cli-reference.md](references/cli-reference.md)

## Spec Quality Checklist

- [ ] Requirements use RFC 2119 keywords (SHALL/MUST/SHOULD/MAY)
- [ ] Every requirement has at least one GIVEN/WHEN/THEN scenario
- [ ] No implementation details in specs (those go in `design.md`)
- [ ] Delta specs use correct markers (ADDED/MODIFIED/REMOVED/RENAMED)
- [ ] REMOVED requirements include deprecation reason
- [ ] RENAMED requirements include FROM:/TO: mapping

## Error Handling

| Failure | Action |
|---|---|
| `openspec` not found | `npm install -g @fission-ai/openspec@latest` |
| `validate` fails | Fix CRITICAL issues first, then WARNINGs → re-validate |
| `archive` fails | Check: incomplete tasks, invalid delta markers, or use `--skip-specs` |
| `validate --strict` fails | Resolve all WARNINGs or downgrade to non-strict |

## References

- [ai-coding-agent-workflow.md](references/ai-coding-agent-workflow.md) — mutation policy, agent safety rules
- [artifact-templates.md](references/artifact-templates.md) — full templates for all 4 change artifacts
- [cli-reference.md](references/cli-reference.md) — complete CLI commands and flags
- [command-rules.md](references/command-rules.md) — per-command rules for explore/apply/verify/archive
- [spec-format.md](references/spec-format.md) — spec template, delta markers, RFC 2119 guide
- [e2e-simulation.md](references/e2e-simulation.md) — annotated end-to-end workflow example (rate limiting on a SaaS API)

