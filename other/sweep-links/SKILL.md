---
name: sweep-links
agent: hestia
description: Hestia's broken wikilink detection skill. Scans vault notes for [[wikilinks]] that point to non-existent files. Reports broken links with source file and line. Does not fix — reports only.
allowed-tools: Read, Grep, Glob
user-invocable: true
triggers:
  - sweep links
  - broken links
  - find broken wikilinks
  - wikilink scan
  - link check
  - find dead links
  - broken wikilink scan
  - check wikilinks
---

# Sweep Links

You are Hestia scanning for broken wikilinks. Report only. No fixes. No prose.

## What this skill does

Scan vault markdown files for `[[wikilinks]]` that reference notes that don't exist on disk. Return a list of broken links with source file and line number. Fixing broken links is a Lyra task — Hestia surfaces them.

## Protocol

### Step 1: Inventory the vault

Use Glob to get the full list of `.md` files in `vault/`. Extract the stem of each filename (filename without path and without `.md` extension) as the valid link targets.

### Step 2: Scan for wikilinks

Use Grep to find all `[[wikilink]]` patterns across vault notes. Pattern: `\[\[[^\]]+\]\]`

For each match, extract the link target (the text between `[[` and `]]`). Strip any alias (text after `|`). Strip any heading anchor (text after `#`).

### Step 3: Cross-reference

For each extracted link target, check whether a matching filename exists in the vault inventory from Step 1. Match is case-insensitive.

### Step 4: Return report (terse)

```
## Link Sweep — YYYY-MM-DD

Total wikilinks scanned: N
Broken links found: N
Clean links: N

### Broken Links
- `vault/path/to/source.md` line N: [[BrokenTarget]]
- `vault/path/to/source2.md` line N: [[AnotherBrokenTarget]]

### Notes
- <any patterns noticed — e.g., "7 broken links all reference deleted agent files">
```

If zero broken links found:
```
Broken links found: 0. Vault is clean.
```

## Constraints

- Report only. No edits. No fixes.
- Read-only tools: Read, Grep, Glob only.
- No Write, Edit, Bash, Agent, or WebFetch.
- Fixing broken links is a Lyra task — include this note in every report with broken links.
- Alias links (`[[Target|Display Text]]`) — check Target, not Display Text.
- Heading anchors (`[[Note#Section]]`) — check Note, not the section.
