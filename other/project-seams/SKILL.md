---
name: project-seams
description: Discover and load optional project-tier skills and agents by concern/role, plus the soft docs/narrative and docs/domain inputs. Every seam is optional — absent means proceed, never block. Loaded by the engineering-context crew agents.
---

# Project seams skill

The user-tier kit (installed to `~/.claude/`) is stack-agnostic. A consuming repo supplies stack/rule content in its own `.claude/` tree. This skill is how a generic agent finds and honors those optional seams — and never blocks when they are absent.

## Reserved project skills (auto-discover)
For each concern this agent references, check `<repo>/.claude/skills/<concern>/SKILL.md`. Load and honor it if present; emit no error and proceed if absent.

| Concern | Governs | Referenced by |
|---|---|---|
| `architecture-rules` | layering, boundaries, allowed patterns, dependency direction | architect, software-engineer (context), workflow-step-planner |
| `coding-rules` | language/style conventions, forbidden patterns, naming | software-engineer, workflow-step-planner |
| `test-rules` | test layout, naming, coverage targets, fixtures | tester, software-engineer (unit/e2e layout) |

## Open project skills
A repo may add more concern skills (e.g. `dotnet-patterns`, `react-patterns`, `db-rules`). Honor any concern in this agent's reference list using the same present-or-proceed rule. Cite sections precisely (`per coding-rules §3.2`); a same-named project skill **overrides** a generic one (project scope outranks user scope).

## Project agents (invoke by role, never by hardcoded name)
| Role | Job |
|---|---|
| `test-runner` | runs the project's build/test command; returns only failures + build errors |
| `rules-checker` | read-only audit of a diff against the rule skills; returns a punch list; honors `Project-Specific Rule Overrides` in `analyzed.md` |
| `<lang>-reviewer` | stack-specific review (e.g. `csharp-reviewer`) |

Refer to these by role so any repo can plug its own. Proceed without them if the repo ships none.

## Soft documentation inputs
- `docs/narrative/` — plain-language wiki overview. Absent → `docs/narrative/ not found - run /project:overview to generate it; proceeding without it.`
- `docs/domain/` — canonical DDD schema. Absent → `docs/domain/ not found - run /project:explore to generate it; proceeding without it.`
- `docs/architecture.md` — free-form architecture notes (read by BA, architect, SE, tester).

Emit the symmetric one-line advisory for whichever tree is absent, then proceed. Optional inputs never block.

## Per-feature overrides
A feature may override a project rule in the `Project-Specific Rule Overrides` section of `<feature>.analyzed.md`, citing the rule skill + section. Honor the override over the rule for that feature.

## Invariant
Every seam is optional. Missing seam → no error, proceed. Never edit a project's `.claude/` content from a generic agent; treat it as read-only input.
