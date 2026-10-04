---
name: thalarch-project-brain
description: >
  Maintains an opt-in, repository-local project knowledge layer for stable architecture, invariants,
  decisions, regressions, commands, design rules, and project-scoped experience. Use when a project
  is revisited repeatedly and durable context would reduce rediscovery. Current repository/runtime
  evidence always outranks the brain; entries carry provenance/freshness; stale facts are retired;
  secrets and private chain-of-thought are forbidden; and repository files are created or changed
  only when durable project memory is explicitly authorized.
---

# Thalarch Project Brain

A Project Brain is a **compact project-specific knowledge index**, not a replacement for the source
code, tests, repository instructions, or current runtime evidence.

## 1. Activation and authorization

Use when:

- the repository is worked on repeatedly;
- important invariants are expensive to rediscover;
- regressions recur;
- architecture or product decisions need durable rationale;
- project-specific workflows/commands repeatedly matter.

Do not create `.thalarch/brain/` automatically during ordinary work. A repository-local durable sink
is an external mutation and requires user/project authorization.

## 2. Canonical layout

When authorized, prefer this small inspectable layout:

```text
.thalarch/brain/
  project.md
  invariants.md
  decisions.md
  regressions.md
  playbooks.md
  design.md          # only when the project has meaningful visual/product rules
  memory.sqlite3     # optional indexed project memory
```

Do not create empty files merely to satisfy the layout. Add only surfaces the project actually needs.
If the repository already has authoritative architecture/decision/runbook documentation, reference or
update that system instead of creating a competing source of truth.

## 3. What belongs where

### `project.md`

Stable project identity and navigation:

- language/framework/toolchain facts with provenance;
- important modules/boundaries;
- authoritative repository rule files;
- verified build/test/lint commands;
- pointers to deeper project docs.

### `invariants.md`

Behavior that must remain true, for example ownership, queue identity, cache semantics, wire
compatibility, data constraints, or lifecycle rules.

### `decisions.md`

Durable decisions with rationale, alternatives, scope, evidence, and revisit trigger. Do not turn
minor implementation choices into ADR theatre.

### `regressions.md`

Compact incident cards:

`trigger → proven root cause → discriminator → fix → must-preserve behavior → regression proof`.

### `playbooks.md`

Verified project-specific workflows and diagnostic commands. Commands must come from real project
scripts/docs/CI/tooling, never memory alone.

### `design.md`

Only stable product/design rules: visual identity, spacing/interaction principles, banned patterns,
accessibility constraints, and reference locations.

## 4. Entry contract

Every load-bearing brain entry should make freshness inspectable:

```text
Title
Status: active | retired
Scope: subsystem/module
Last verified: date + commit/version when available
Evidence: source/test/run/doc references
Statement: concise invariant/decision/lesson
Apply when: trigger/conditions
Do not apply when: counterexample/version boundary
```

If freshness cannot be established, retrieval may still use the entry as a lead but not as current
truth.

## 5. Read path

At the start of meaningful repeat work:

1. read repository/system/user rules first;
2. inspect `project.md`/relevant brain index if it exists;
3. query project memory for the subsystem/failure mode;
4. retrieve only a small relevant capsule;
5. verify load-bearing claims against current source/runtime;
6. feed accepted/rejected memory into `thalarch-context`.

Do not load the entire Project Brain into every task.

## 6. Write path

After a verified task:

1. run `thalarch-compound`;
2. use `thalarch-experience` to create a concise candidate card;
3. classify with `thalarch-memory`;
4. persist only project-worthy knowledge;
5. deduplicate against existing entries;
6. update/retire contradicted entries instead of appending forever.

Prefer editing one existing entry over adding a near-duplicate.

## 7. Current truth wins

Resolve conflicts in this order:

1. explicit current user/system/repository rules;
2. current executable/runtime evidence;
3. current source/config/manifests/tests;
4. current primary/vendor contract for version-sensitive facts;
5. verified project documentation;
6. Project Brain memory.

The brain speeds discovery. It never outranks the project it describes.

## 8. Privacy and repository hygiene

Never store credentials, secrets, auth material, private chain-of-thought, unnecessary personal data,
or raw confidential payloads. Distill the engineering lesson.

Before committing a project brain file:

- confirm repository policy permits it;
- keep entries concise;
- avoid machine-specific absolute paths unless the project contract truly requires them;
- do not commit the SQLite store if repository policy prefers local-only state; add it to ignore rules
  only when authorized and appropriate.

## 9. Bootstrap template

For a new authorized Project Brain, begin with the minimum useful `project.md`:

```text
# Project Brain

## Authority
- Repository rules: <verified paths>

## Stack
- <only proven current stack facts>

## Critical invariants
- <link or concise invariant>

## Verified commands
- <real project-native commands>

## Known regression areas
- <only verified recurring surfaces>

## Memory policy
Current source/runtime evidence overrides this file. Revalidate load-bearing entries before use.
```

Grow only from verified recurring need.
