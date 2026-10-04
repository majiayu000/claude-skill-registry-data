---
name: fleet-changelog-generation
description: How the technical writer generates changelogs from git history — conventional commits as structured data, Keep a Changelog format, audience-appropriate summaries per release.
---

# Changelog Generation — Writer's Release Communication

Conventional commits aren't just for developers. When structured correctly, they're the source data for changelogs that tell users, operators, and the PO what changed and why.

## Source Data: Conventional Commits

The fleet enforces conventional commit format via hook:
```
type(scope): description [task:XXXXXXXX]
```

Each commit type maps to a changelog section:

| Commit Type | Changelog Section | Audience Cares? |
|------------|------------------|-----------------|
| feat | Added | YES — new capabilities |
| fix | Fixed | YES — problems resolved |
| perf | Performance | YES — speed/resource improvements |
| refactor | Changed | SOMETIMES — if it affects behavior |
| docs | Documentation | SOMETIMES — if user-facing docs |
| test | — | NO — internal quality |
| chore | — | NO — maintenance |
| ci | — | NO — pipeline changes |
| style | — | NO — formatting |

## Keep a Changelog Format

The fleet follows [keepachangelog.com](https://keepachangelog.com):

```markdown
# Changelog

## [Unreleased]

### Added
- Stage-aware effort selection in model_selection.py — reasoning/investigation stages 
  now get higher thinking effort automatically ([task:abc12345])

### Fixed
- Dispatch records now use stage-aware model_config for Claude backends, 
  ensuring effort consistency between selection and execution ([task:def67890])

### Changed
- Architect skills reorganized: architecture-health moved to all_stages 
  for continuous monitoring ([task:ghi11111])

## [0.3.0] - 2026-04-07

### Added
- 36 role-specific group calls across 10 agent roles
- Contribution completeness checking via synergy matrix
...
```

## The Generation Process

### Step 1: Extract Commits Since Last Release

```bash
# Commits since last tag
git log v0.3.0..HEAD --oneline --format="%h %s"

# Or since a date
git log --since="2026-04-01" --oneline --format="%h %s"
```

### Step 2: Parse and Categorize

Group by type. Within each type, group by scope:

```
feat(core): add _STAGE_EFFORT_FLOOR to model_selection [task:abc12345]
feat(core): add _apply_stage_adjustment [task:abc12345]
fix(dispatch): use model_config for Claude backends [task:abc12345]
test(model): add 10 stage-aware effort tests [task:abc12345]
chore(config): add 8 chain docs to tool-chains.yaml [task:def67890]
```

→ Added: 2 features (both core/model_selection)
→ Fixed: 1 fix (dispatch)
→ Internal: 1 test, 1 chore (not in changelog)

### Step 3: Write Human-Readable Entries

Transform commit messages into changelog entries:

```
# BAD — just copying commit messages
- feat(core): add _STAGE_EFFORT_FLOOR to model_selection [task:abc12345]

# GOOD — human-readable, audience-appropriate
- Stage-aware effort selection: reasoning and investigation stages now 
  automatically get higher thinking effort, improving analysis depth 
  for complex tasks ([task:abc12345])
```

The commit tells WHAT changed. The changelog entry tells WHY it matters.

### Step 4: Group Related Changes

Multiple commits for the same feature → one changelog entry:

```
# 2 commits that are really 1 feature:
feat(core): add _STAGE_EFFORT_FLOOR to model_selection [task:abc12345]
feat(core): add _apply_stage_adjustment [task:abc12345]

# → 1 changelog entry:
- Stage-aware effort selection in model_selection.py — reasoning/investigation 
  stages now get higher thinking effort automatically ([task:abc12345])
```

## Phase-Appropriate Changelogs

| Phase | Changelog Scope |
|-------|----------------|
| poc | Informal — bullet list of what works now |
| mvp | Structured — Added/Fixed/Changed sections |
| staging | Full keepachangelog — with version numbers and dates |
| production | Full + migration notes + breaking changes highlighted |

## Integration With Fleet Systems

- **PR template:** `fleet_task_complete` generates PR body with commit changelog
- **Labor stamps:** each PR includes provenance (model, effort, backend)
- **Board memory:** sprint standup includes velocity from changelog data
- **Plane:** release notes posted to Plane cycle comments

Your changelog complements the PR's automatic changelog by adding the human context — not what files changed, but what the user/operator/PO should know.

## The `/pm-changelog` Skill

The PM has a `/pm-changelog` skill that generates raw changelogs from git history. Your value add is:
1. **Audience translation:** technical commits → user-facing descriptions
2. **Grouping:** related commits → coherent feature descriptions
3. **Context:** why this change matters, not just what changed
4. **Migration notes:** if something breaks or requires action

The PM generates the data. You produce the communication.
