---
name: adr
description: Creates and maintains Architecture Decision Records (ADRs) in docs/decisions/ using the MADR format. Supports creating, listing, updating, superseding, and searching ADRs.
argument-hint: "[create <title> | list | update <n> <status> | supersede <n> | search <keyword>]"
model: haiku
allowed-tools: Read, Write, Edit, Glob, Grep
---

# adr

## Purpose

Create, list, update, and supersede Architecture Decision Records (ADRs) following the Markdown Architectural Decision Records (MADR) format. Maintains an ADR directory (see Directory Convention below). Works standalone or as a companion to `/architecture-design`.

---

## Directory Convention

Before creating anything, detect where this project keeps ADRs. Use Glob to check, in order: `docs/decisions/ADR-*.md`, `docs/adr/*.md`, `adr/*.md`, `docs/architecture/decisions/*.md`. Use the first directory that already contains ADRs. Only if none exists, default to `docs/decisions/`. All paths below refer to this detected directory.

---

## ADR Format (MADR)

Every ADR uses this structure:

```markdown
# ADR-NNN: <Title>

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN
**Deciders:** <names or roles>
**Tags:** <architecture | security | database | api | infrastructure | ...>

## Context and Problem Statement

[1-3 paragraphs: what situation led to this decision? What is the problem being solved? What forces are at play?]

## Decision Drivers

- [driver 1: most important constraint or goal]
- [driver 2]

## Considered Options

1. **[Option A — Recommended]** — one-sentence description
2. **[Option B]** — one-sentence description
3. **[Option C]** — one-sentence description

## Decision Outcome

**Chosen option:** [Option A], because [one paragraph justification tied to decision drivers].

### Positive Consequences
- [what becomes easier, better, or possible]

### Negative Consequences / Trade-offs
- [what becomes harder, more expensive, or is given up]

## Pros and Cons of the Options

### Option A — [Name]
- ✅ [pro]
- ✅ [pro]
- ❌ [con]
- ❌ [con]

### Option B — [Name]
- ✅ [pro]
- ❌ [con]

## Links
- [Link to related ADR, design doc, RFC, or Jira ticket]
```

---

## Instructions

### Step 1 — Determine the action

Parse `$ARGUMENTS` first and dispatch directly — do not ask if the action is given:

| Invocation | Action |
|------------|--------|
| `/adr create <title>` | Step 2a, using `<title>` as the decision title |
| `/adr list` | Step 2b |
| `/adr update <n> <status>` | Step 2c on ADR-`<n>`, setting `<status>` |
| `/adr supersede <n>` | Step 2d replacing ADR-`<n>` |
| `/adr search <keyword>` | Step 2e with `<keyword>` |

If no arguments were given, ask the user what they want to do:
- **(a) Create a new ADR** — document a new architectural decision
- **(b) List existing ADRs** — show all ADRs with status and one-line summary
- **(c) Update an ADR's status** — mark as Accepted, Deprecated, or Superseded
- **(d) Supersede an ADR** — create a new ADR that replaces an existing one
- **(e) Search ADRs** — find ADRs by tag, status, or keyword

---

### Step 2a — Create a new ADR

1. Use Glob to find all existing ADRs in the detected ADR directory. Determine the next number.
2. Use Read on any related existing ADRs mentioned.
3. Ask the user (skip the title question if it was passed as an argument):
   - What is the decision being made? (one sentence title)
   - What is the context / problem? (what forced this decision)
   - Who are the deciders?
   - What options were considered?
   - What was chosen and why?
4. Generate the full ADR using the MADR format above.
5. Use Write to save to `<adr-dir>/ADR-<NNN>-<kebab-case-title>.md`. Create the directory if it doesn't exist.
6. Update the ADR index (see Step 3).

---

### Step 2b — List existing ADRs

Use Glob to find all ADRs in the detected ADR directory. Use Read on each to extract: number, title, status, date, tags. Output a sorted table:

```
## Architecture Decision Records

| # | Title | Status | Date | Tags |
|---|-------|--------|------|------|
| ADR-001 | Use PostgreSQL as primary database | Accepted | 2026-01-15 | database |
| ADR-002 | Adopt hexagonal architecture | Accepted | 2026-01-20 | architecture |
| ADR-003 | Use Redis for session storage | Proposed | 2026-02-01 | infrastructure |
```

---

### Step 2c — Update status

Use Read to load the ADR. Use Edit to update the Status field. Valid transitions:
- Proposed → Accepted (decision confirmed)
- Proposed → Deprecated (no longer relevant before being accepted)
- Accepted → Deprecated (no longer the right approach)
- Accepted → Superseded by ADR-NNN (replaced by a newer decision)

---

### Step 2d — Supersede

1. Create a new ADR (Step 2a) that documents the new decision.
2. In the new ADR, add a link: "Supersedes ADR-NNN: [title]"
3. Use Edit to update the old ADR's status to "Superseded by ADR-NNN".

---

### Step 2e — Search

Use Grep across the detected ADR directory for the keyword or tag. Return matching ADRs with context.

---

### Step 3 — Maintain ADR Index

After any create/update operation, regenerate `<adr-dir>/README.md` — an index of all ADRs sorted by number, showing status as a text badge: `[ACCEPTED]`, `[PROPOSED]`, `[DEPRECATED]`, `[SUPERSEDED]`.
