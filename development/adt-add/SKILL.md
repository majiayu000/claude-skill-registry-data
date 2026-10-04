---
name: add
description: Meta-adder for toolkit artifacts. Single entry point to add a skill, pattern, best-practice, hook, agent, or guide with correct frontmatter + sync to 4 publish targets.
triggers:
  - "add a skill"
  - "add a pattern"
  - "add a hook"
  - "add an agent"
  - "add a guide"
  - "add to toolkit"
---

# Add

Meta-adder for toolkit artifacts. Single entry point to add a skill, pattern, best-practice, hook, agent, or guide to the right location(s) with correct frontmatter + triggers + sync to all 4 publish targets.

## Purpose

Eliminate manual file-path guessing and frontmatter boilerplate. Route artifact creation through a unified dispatcher that handles schema validation, location routing, and bilingual sync.

## Artifact Types & Locations

| Type | EN Path | PT Path | Local | Dotfiles |
|------|---------|---------|-------|----------|
| Skill | `packages/core/kit/core/skills/<name>.md` | `packages/core/kit/core/skills/<name>.md` | `~/.claude/skills/<name>/SKILL.md` | `dot_claude/skills/<name>/SKILL.md` |
| Pattern | `packages/core/patterns/<name>.md` | `packages/core/patterns/<name>.md` | `~/.claude/patterns/<name>.md` | `dot_claude/patterns/<name>.md` |
| Best-Practice | `packages/core/best-practices/<name>.md` | `packages/core/best-practices/<name>.md` | `~/.claude/best-practices/<name>.md` | `dot_claude/best-practices/<name>.md` |
| Hook | `packages/core/kit/hooks/<name>/hook.json` + `.md` | N/A (EN only) | `~/.claude/hooks/<name>/hook.json` | `dot_claude/hooks/<name>/hook.json` |
| Agent | `packages/core/kit/core/agents/<name>/AGENT.md` | `packages/core/kit/core/agents/<name>/AGENT.md` | `~/.claude/agents/<name>/AGENT.md` | `dot_claude/agents/<name>/AGENT.md` |
| Guide | `docs/guides/<name>.md` | `docs/guides/<name>.md` | N/A | N/A |

## Invocation

```
add skill "name" --description "..." --triggers "trigger1,trigger2" --body "..."
add pattern "name" --description "..." --references "ref1,ref2" --body "..."
add hook "name" --event "post-commit" --body "..."
```

## Workflow

1. **Parse type** — Determine artifact kind from command.
2. **Validate frontmatter** — Ensure `name`, `description` (+ `triggers` for skills).
3. **Create EN canonical** — Write to primary repo location with full frontmatter.
4. **Sync to PT** — Copy file to PT mirror, insert "Tradução pendente" blockquote **after** frontmatter (critical).
5. **Write local** — Copy to `~/.claude/` location for immediate availability.
6. **Write dotfiles** — Copy to dotfiles repo for chezmoi sync.
7. **Stage & commit** — Commit across all 4 repos on feature branches.
8. **Open PRs** — Create PRs on EN, PT, dotfiles (auto-merge on CI pass).

## Frontmatter Schema

**Skills**:
```yaml
---
name: <slug>
description: <1 sentence>
triggers:
  - "trigger 1"
  - "trigger 2"
---
```

**Patterns**:
```yaml
---
name: <slug>
description: <1 sentence>
context: <when to use>
---
```

**Best-Practices**:
```yaml
---
name: <slug>
description: <1 sentence>
applies_to: [framework1, framework2]
---
```

## Example: Add a Skill

```
add skill "my-validator"
  --description "Validate code against team standards"
  --triggers "validate code,lint check,run validator"
  --body "# My Validator\n\nChecks code..."
```

Creates:
1. `ai-dev-toolkit/packages/core/kit/core/skills/my-validator.md` (EN)
2. `ai-dev-toolkit-pt-br/packages/core/kit/core/skills/my-validator.md` (PT + blockquote)
3. `~/.claude/skills/my-validator/SKILL.md` (local)
4. `dotfiles/dot_claude/skills/my-validator/SKILL.md` (dotfiles)

Then stages, commits, opens 3 PRs.

## References

- Bilingual sync: `sync-pt-parity` skill
- Frontmatter spec: `packages/core/kit/scripts/validate.sh`
- Auto-merge: `ship` skill
