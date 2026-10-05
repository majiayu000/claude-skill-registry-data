---
name: commit-trailers
description: "Structured commit trailers — adds Constraint, Rejected, Scope-risk, and Not-tested metadata to commit messages. Captures architectural decisions and known gaps in git history."
alwaysApply: true
---

# Structured Commit Trailers

When creating git commit messages, append structured trailers that capture decision context. This metadata makes architectural decisions searchable in git history and helps future developers understand why changes were made the way they were.

## Trailers

### Required (every commit)

**Scope-risk:** — How much of the project does this change affect?
- `low` — isolated change, single file or tightly scoped feature
- `medium` — touches multiple systems or changes shared interfaces
- `high` — modifies shared infrastructure, serialization format, or build pipeline

### Conditional (include when applicable)

**Constraint:** — Architectural constraints that were respected during this change. Reference the rule or convention by name.

**Rejected:** — Alternatives that were considered and rejected, with brief reason. Helps future developers avoid re-exploring dead ends.

**Not-tested:** — Known gaps in test coverage or scenarios that weren't verified. Use `none` if everything is covered.

## Format Rules

- Trailers go after a blank line at the end of the commit message body
- One trailer per line
- Keep each trailer under 100 characters
- `Scope-risk` is always present
- Omit `Constraint` if no specific constraints were relevant
- Omit `Rejected` if no alternatives were considered
- Omit `Not-tested` for trivial changes; include it for anything non-trivial

## Examples

### Simple feature addition
```
Add object pooling for projectiles

Replaces Instantiate/Destroy cycle with a pre-warmed pool of 32.
Pool size is configurable via SerializeField on SpawnSystem.

Scope-risk: low
Constraint: no-alloc-in-update — pool grows only in Awake
Rejected: addressables-pool — overkill for single prefab type
Not-tested: pool exhaustion when max size exceeded during boss fight
```

### Bug fix
```
Fix enemy health not resetting on respawn

EnemyModel.Health was not reset in ObjectPool.OnGet callback.
Added explicit reset in EnemySystem.OnSpawn().

Scope-risk: low
Not-tested: none
```

### Cross-system refactor
```
Migrate score tracking from static class to VContainer

ScoreManager was a static singleton — replaced with ScoreSystem
registered in GameLifetimeScope. All 4 consumers updated to
use constructor injection.

Scope-risk: high
Constraint: no-singletons — VContainer is the only DI mechanism
Rejected: SO-based-score-channel — adds complexity for simple int tracking
Not-tested: score persistence across scene transitions
```

### Serialization change
```
Rename _speed to _moveSpeed on PlayerView

Added FormerlySerializedAs to preserve prefab overrides.
All 3 prefab variants verified in inspector.

Scope-risk: medium
Constraint: formerly-serialized-as — mandatory on all serialized field renames
```
