---
name: workspace-layout
description: Use when an agent is exploring a relayfile mount for the first time or trying to locate a specific resource (Notion page, Linear issue, Slack channel, GitHub PR). Tells the agent to start with `<mount>/LAYOUT.md` and `<provider>/LAYOUT.md` rather than guessing paths from memory, and to use the `by-title/`, `by-id/`, `by-name/`, `by-edited/<date>/`, `by-state/` alias subtrees instead of recursively grepping. Filename convention is `<identifier>__<uuid>` (ticket number / slug first so listings are scannable). NOT for activity-summary questions, which should use the `activity-summary` skill instead.
---

# Workspace Layout — Start With LAYOUT.md

## Overview

A relayfile mount is **self-describing**. Every workspace has a `LAYOUT.md` at its root, and every provider has a `LAYOUT.md` at its provider root, that together describe the directory shape, the filename conventions, and the indexes available for fast lookup. Read these first. Do not guess paths from memory — provider layouts can be customized per workspace and the indexes available may differ.

## When to use this skill

- You just connected to a relayfile mount and have no prior context about its shape.
- You need to find a specific resource (a Notion page by title, a Linear issue by number, a Slack channel by name).
- You're tempted to run `find` or `grep -r` across the mount — almost always there is an index that does it cheaper.
- You see paths in someone else's code or in a digest and want to understand them.

If the user is asking an activity-summary question ("what did I work on yesterday"), use the `activity-summary` skill instead. This skill is for resource lookup, not time-windowed queries.

## Step 1: Read the root layout

```bash
$ cat $MOUNT/LAYOUT.md
```

The root `LAYOUT.md` lists the connected providers, the digests directory, the skills directory, and any cross-provider conventions in effect for this workspace.

## Step 2: Read the provider layout

```bash
$ cat $MOUNT/linear/LAYOUT.md
```

The per-provider layout covers:

- Top-level directories under the provider root (e.g. `issues/`, `projects/`, `cycles/`)
- Filename conventions in use (`<identifier>__<uuid>.json`, plain UUID, slug-based, …)
- Which `by-*` alias indexes are populated
- Writeback directories and their schemas (see the `writeback-as-files` skill)
- Whether content is paginated and how

## Step 3: Use alias indexes, not recursive search

Canonical records are keyed by UUID for stability. Alias indexes live under `by-*/` and point back to the canonical files. Reach for an index that matches your query shape:

```bash
# Find a Notion page by title
$ ls $MOUNT/notion/pages/by-title/ | grep -i "onboarding"
onboarding-runbook__c24642bb.json
$ jq -r '.id' $MOUNT/notion/pages/by-title/onboarding-runbook__c24642bb.json

# Find a Linear issue by ticket number (identifier is part of the canonical
# filename, so a direct ls is sufficient — no by-id/ needed)
$ ls $MOUNT/linear/issues/ | grep "^AGE-16"

# Find what was edited yesterday in Notion
$ ls $MOUNT/notion/pages/by-edited/2026-05-12/

# Find all Linear issues currently In Progress
$ ls $MOUNT/linear/issues/by-state/in-progress/

# Find a Slack channel by name
$ ls $MOUNT/slack/channels/by-name/ | grep "gtm"
```

Indexes are symlinks (or directory listings on filesystems without symlink support) — they don't duplicate the underlying content, so they stay cheap to enumerate even on workspaces with thousands of records.

## Filename convention

Canonical files use **`<identifier>__<uuid>.<ext>`** — identifier first so directory listings are immediately scannable:

```bash
$ ls $MOUNT/linear/issues/
AGE-9__2bb2c00f-ee93-4c73-a793-df5b725d9a1a.json
AGE-10__8c313d70-9800-4539-820f-96a481c09ce0.json
AGE-16__87389837-62b1-4e1a-a237-59218bab2974.json
```

The `__` (double underscore) separator is reserved — provider data must not produce it in the identifier portion. If you see a filename without `__` it's an alias-index symlink or a metadata file, not a canonical record.

We borrowed the `<identifier>__<uuid>` shape from [Mirage](https://github.com/strukto-ai/mirage) after seeing the pattern in their mount.

## Common patterns

### "Where does X live?"

```bash
cat $MOUNT/LAYOUT.md              # provider list and cross-cutting layout
cat $MOUNT/<provider>/LAYOUT.md   # provider-specific shape
ls   $MOUNT/<provider>/           # top-level resource directories
ls   $MOUNT/<provider>/<resource>/by-*/   # available indexes
```

Three to four `cat`/`ls` calls and you have the full map.

### "I have a UUID, what is it?"

The UUID is in the filename. `ls` and `grep` find it without needing to know which directory:

```bash
$ find $MOUNT -name "*87389837-62b1-4e1a-a237-59218bab2974*" -type f
$MOUNT/linear/issues/AGE-16__87389837-62b1-4e1a-a237-59218bab2974.json
```

Use `find` here because UUIDs are globally unique — the result is one file.

### "I have a slug or title, what is it?"

Use `by-title/` or `by-name/` rather than `find`. The index is sorted and bounded; `find` walks the full tree.

## What NOT to do

- **Don't `grep -r` over the mount** for a title or name. There's an index. Use it.
- **Don't hardcode paths from a different workspace's LAYOUT.md.** Workspaces can customize which adapters and indexes are mounted.
- **Don't ignore provider `LAYOUT.md`.** If you wrote a Notion-specific path from memory and it doesn't exist, the provider's `LAYOUT.md` will tell you the actual shape in one read.
