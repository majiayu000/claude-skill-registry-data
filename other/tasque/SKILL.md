---
name: tasque
description: Operational guide for Tasque (tsq) local task tracking and management.
---

<!-- tsq-managed-skill:v1 -->

Tasque (`tsq`) = durable local task graph for agent work.

## Use

- Use `tsq`: multi-step, multi-session, blocked, shared-agent, release, or follow-up work.
- Use transient checklist: short linear same-session work.

## Start

```bash
tsq find ready --lane planning
tsq find ready --lane coding
tsq find blocked
tsq show <id> [--deps] [--notes] [--history] [--spec]
tsq root
tsq --root <path> <cmd> ...
```

Pick one task. Inspect before edit. `tsq` does not walk parent dirs; use `tsq root` to verify current store and `--root` from subdirs.

## Create

```bash
tsq create "Implement <feature>" --kind feature -p 1 --needs-plan
tsq create "Fix <bug>" --kind task -p 1 --needs-plan
tsq create "Implement <feature>" --planned
```

Good task = verb + object + scope. Set `kind`, priority, labels, spec/deps when useful.

## Split

```bash
tsq create --parent <parent-id> \
  "Design API contract" \
  "Implement service logic" \
  "Add regression tests"
```

Shared defaults:

```bash
tsq create --parent <parent-id> --kind task -p 2 --planned \
  "Wire CLI args" \
  "Update docs" \
  "Add integration tests"
```

Safe rerun:

```bash
tsq create --parent <parent-id> --ensure \
  "Wire CLI args" \
  "Update docs" \
  "Add integration tests"
```

`tasks.md` batch. Two-space nested bullets create child hierarchy.

```md
- Add parser tests
  - Cover nested task hierarchy
  - Cover invalid indentation
- Wire CLI command
- Update skill docs
```

```bash
tsq create --parent <parent-id> --from-file tasks.md
```

Plan markdown preview/apply. Headings, bullets, and checkboxes become child tasks; inline `#labels` attach in same batch.

```bash
tsq plan <parent-id> --from plan.md
tsq plan <parent-id> --from plan.md --apply --planned
tsq plan <parent-id> --from - --apply --ensure
```

## Spec / Plan State -> Code

```bash
tsq spec <id> --text "## Plan\n...\n## Acceptance\n..."
tsq spec <id> --show
# Choose one edit mode when changing an existing spec:
tsq spec <id> --update --stdin
tsq spec <id> --patch --stdin
tsq planned <id>
tsq claim <id> --assignee <name> --start
tsq workon <id> --assignee <name>
```

Use `tsq spec <id> --show` when spec markdown lives in sync worktree.
Use `--update` for whole-spec replacement. Use `--patch` for small agent edits; patch applies only to the attached spec and fails if context is stale. Prefer `--stdin` or `--file` for patches because unified diffs start with `---`.

## Parallel Work

Hard blocker; affects readiness:

```bash
tsq block <child-id> by <blocker-id>
```

Soft order; no readiness block:

```bash
tsq order <later-id> after <earlier-id>
```

Check next:

```bash
tsq find ready --lane coding
tsq find ready --lane planning
```

Prefer many independent tasks. Use `blocks` only for true gates. Use `starts_after`/`order` for sequence.

## Follow-Up

```bash
tsq create "Handle edge case <x>" --discovered-from <current-id> --needs-plan
tsq relate <new-id> <current-id>
```

Follow-up work belongs in `tsq`, not chat TODOs.

## Park / Resume

```bash
tsq defer <id> --note "waiting"
tsq find deferred
tsq open <id>
```

## Duplicate / Replace

```bash
tsq duplicate <id> of <canonical-id> --note "same root issue"
tsq duplicates
tsq merge <source-id...> --into <target-id> --dry-run
tsq merge <source-id...> --into <target-id> --force
tsq supersede <old-id> with <new-id> --note "replaced approach"
```

## Close / Report

```bash
tsq done <id> --note "verified"
tsq history <id> --limit 20
tsq find open --tree
```

Use `--format json` for scripts/parsers. Use `--plain` / `--format plain` for tab-delimited grep/awk parsing. Human output fine for inspection.

## Habits

- Keep `status` and `planning_state` separate.
- Use deps/relations to expose parallel shape.
- Use `--ensure` in rerunnable automation.
- Keep task small enough for one focused agent pass.
- Need edge flags? Run `tsq <cmd> --help`.

## Need More

- Edge flags/full command matrix: `references/command-reference.md` or `tsq <cmd> --help`.
- Planning/deferred semantics: `references/planning-workflow.md`.
- JSON/durability: `references/machine-output-and-durability.md`.
- Missing install: `npm install -g @bumpyclock/tasque`.
