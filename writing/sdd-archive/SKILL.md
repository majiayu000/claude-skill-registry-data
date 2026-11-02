---
name: sdd-archive
description: |-
  Use when completing and archiving a change after all tasks are done and specs are synced. Triggers: "archive the change", "complete this change", "close out the change", "finish the change", "archive".
---

# SDD Archive

Complete a change by moving its directory to the archive.

> `SPECS_ROOT` is resolved by the `sdd` router before this skill runs.
> Replace `.specs/` with your project's actual specs root in all paths below.

## Writing Style

Write the archive report in the voice of a professional technical writer.
Prefer ASD-STE100 Simplified Technical English: short sentences, one instruction per sentence, active voice, and one term per concept.
Keep identifiers, commands, paths, and RFC 2119 keywords exact.

## When to Use

- All tasks in `tasks.md` are complete (`- [x]`)
- Delta specs have been synced into main specs with `sdd-sync`
- Ready to close out the change

## When Not to Use

- Tasks are incomplete — finish implementation first
- Delta specs exist but haven't been synced — consider running `sdd-sync` first (no automatic check; user judgement)

## Invocation Notice

- Tell the user when this skill is running: `sdd-archive`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Soft Gate

Check `tasks.md` for unchecked tasks before archiving.

If incomplete tasks remain:

> "{N} tasks are still incomplete. Archive anyway?"

Wait for user confirmation before proceeding.

## Process

### Phase 1: Confirm

1. Confirm which change to archive (ask if multiple active changes exist)
2. Read `tasks.md` — count complete vs. total tasks
3. If incomplete tasks: issue soft gate warning, wait for user

### Phase 2: Check Target

Target path: `.specs/changes/archive/YYYY-MM-DD-<change-name>/`

Where `YYYY-MM-DD` is today's date.

If the target already exists:

> "Archive target already exists: `.specs/changes/archive/{date}-{name}/`. Suggest using `{name}-2` or waiting until tomorrow."

Stop and ask the user how to proceed.

### Phase 3: Move

```bash
mkdir -p .specs/changes/archive/
mv .specs/changes/<name>/ .specs/changes/archive/YYYY-MM-DD-<name>/
```

Confirm the move succeeded by checking the archive path exists.

The change's `.verify/` scratch (if present) is self-gitignored, so it never enters the archived commit even though `mv` carries it along — leave it or delete it; it is not part of the archived record.

### Phase 4: Update Change Order

If `.specs/changes/ORDER.md` exists, update it per `references/sdd-change-formats.md` § 6.5:

1. Remove the archived change from every section.
2. Remove each **Starts after** entry and each **Reasons** bullet that names the archived change.
3. Remove each shared requirement line that now names fewer than two changes.
4. Update **Last reviewed**.
5. If no **Starts after** entry, no shared requirement, and no `## Not scheduled` change remains, delete `ORDER.md`.

Check the result against the rules in § 6.4.
Every active change directory must appear in exactly one section, and no archived change may appear anywhere.

### Phase 5: Report

```text
Archived: .specs/changes/<name>/ → .specs/changes/archive/YYYY-MM-DD-<name>/
Tasks: {N}/{N} complete
Change order: {updated | deleted | no ORDER.md}
Ready to start: {each change in ORDER.md whose Starts after entries are all met, or "none"}
```

## Common Mistakes

- Deleting instead of moving (archive, not delete — change history is preserved)
- Archiving before syncing delta specs into main specs
- Not checking for the target path existence before moving
- Leaving the archived change in `ORDER.md` as a met prerequisite, instead of removing it
- Keeping `ORDER.md` after the remaining changes can apply in any order

## References

- `references/sdd-change-formats.md` — change order format and maintenance (§ 6)
