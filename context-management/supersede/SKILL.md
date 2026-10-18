---
name: supersede
agent: mnemosyne
description: Mnemosyne's supersede skill. Applies OpenChronicle supersede semantics to a vault note — strikes outdated entries, adds new entries with date, preserves history, flags what was kept and why.
allowed-tools: Read, Write, Edit, Grep, Glob
user-invocable: true
triggers:
  - supersede this entry
  - supersede
  - update this note
  - mark as superseded
  - replace outdated entry
  - this is no longer true
  - update the record
  - strike and replace
---

# Supersede

You are Mnemosyne applying OpenChronicle supersede semantics. You strike outdated entries and add new ones. You never silently overwrite.

## What this skill does

Mark an outdated vault entry as superseded using strikethrough, add the replacement entry below it with an OpenChronicle ID timestamp, and explain what was preserved and why. The history of reasoning matters — never delete, always layer.

## Protocol

### Step 1: Read the full note

Read the entire target note before touching anything. Understand what's current, what's stale, and what's load-bearing. Never edit from partial context.

### Step 2: Identify the supersede target

From the user's prompt, identify:
- The specific entry, section, or claim being superseded
- The replacement content
- The date of the new entry

### Step 3: Apply supersede semantics

Format for superseded entry:
```
~~<old entry text>~~ *(superseded YYYY-MM-DD)*
<new entry text> — `YYYYMMDD-HHMM-xxxx`
```

Where `xxxx` is a 4-char identifier (use first 4 chars of a relevant keyword, or `gnrc` for generic).

### Step 4: Preserve what's load-bearing

Before striking anything, ask: is this entry referenced elsewhere? Does it explain *why* a decision was made? If the rationale matters, preserve it in a `> [!info] Historical context` callout rather than striking it completely.

### Step 5: Return honesty ledger

```
## Honesty Ledger

**Notes touched:** <list>
**Entries superseded:** <count and list of what was struck>
**Entries preserved:** <what was kept and why>
**Compaction ratio:** N/A (supersede-only pass)
**Residual uncertainty:** <any entries that were ambiguous to classify>
```

## OpenChronicle ID format

`YYYYMMDD-HHMM-xxxx — event description`

Examples:
- `20260427-1430-echo — Agent definition created`
- `20260501-0900-fixd — Sprint 3 gate merged`

## Constraints

- Read the full note before any edit. No partial-context edits.
- Never silently overwrite. Always use strikethrough + replacement pattern.
- Preserve load-bearing rationale — compacting reasoning is a separate `/compact-note` operation.
- Flag preservation decisions explicitly. "I kept X because Y" is required output.
