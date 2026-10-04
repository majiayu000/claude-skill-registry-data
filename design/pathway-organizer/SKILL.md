---
name: pathway-organizer
description: Organize discovered pathway/portal/theme content into the docs repo structure. Copies new files, resolves duplicates, updates the README, and ensures each portal directory has complete coverage. Run after pathway-collector to consolidate content.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
---

Organize pathway content into the docs repo: $ARGUMENTS

$ARGUMENTS can specify:
- A portal slug to focus on (reframation, metanoia, mdna, movement-intelligence, forgotten-ways, discipleship)
- A source repo to pull from (e.g., "from movemental-ai")
- "all" to do a full organization pass

If no arguments, perform a full organization across all portals.

---

## Docs Repo Location

`~/Desktop/Dev/repos/docs/`

---

## Target Directory Structure

```
docs/
├── pathways/
│   ├── {portal-slug}/
│   │   ├── vision/          # Strategic/conceptual vision documents
│   │   ├── articles/        # Written content pieces
│   │   ├── case-studies/    # Real-world examples
│   │   └── html-templates/  # HTML/CSS/JS prototypes
│   └── _shared/             # Cross-portal resources
│       ├── christocentric-spine/
│       ├── glossary/
│       └── architecture/
├── knowledge/        # Research, mappings, inventories
│   ├── portal-mappings/
│   ├── inventories/
│   ├── core-content/
│   └── evals/
├── pastoral-warm/           # Pastoral-Warm themed portal content
│   ├── apest/
│   ├── christocentric/
│   ├── disciple-making/
│   ├── formation/
│   ├── kingdom-mission/
│   └── missional-church/
└── reference/               # Design specs, skills, prototypes
    ├── design/
    ├── skills/
    └── stitch-prototypes/
```

---

## Step 1 — Read Current State

1. Read `~/Desktop/Dev/repos/docs/INVENTORY.md` if it exists (produced by `pathway-collector`)
2. Glob the current docs repo to understand what's already organized
3. Identify what's missing or needs updating

---

## Step 2 — Source Mapping

Map content from source repos to docs directory:

| Source Location | Docs Destination |
|----------------|------------------|
| `alan-hirsch/_docs/pathways/*-vision.md` | `pathways/{slug}/vision/` |
| `alan-hirsch/_docs/portal/*.md` | `pathways/_shared/` |
| `alan-hirsch/_docs/PORTAL_MAP_AND_CHRISTOCENTRIC_SPINE.md` | `pathways/_shared/christocentric-spine/` |
| `alan-hirsch/public/html/pathway-templates/*` | `pathways/{slug}/html-templates/` |
| `alan-hirsch/public/html/pathways/*` | `reference/stitch-prototypes/` |
| `alan-hirsch/public/html/site/portals.json` | `pathways/_shared/` |
| `alan-hirsch/_docs/design/PATHWAYS_DESIGN_ALIGNMENT.md` | `reference/design/` |
| `alan-hirsch/_docs/current-ui-overviews/03-pathways.md` | `reference/` |
| `alan-hirsch/.claude/skills/pathway-*` | `reference/skills/` |
| `movemental-ai/_docs/themes-content/knowledge/*` | `knowledge/` |
| `movemental-ai/_docs/themes-content/articles/{theme}/*` | `pathways/{slug}/articles/` |
| `movemental-ai/_docs/themes-content/pastoral-warm/*` | `pastoral-warm/` |
| `adam-seiz/.claude/skills/pathway-*` | `reference/skills/` |

### Article Theme-to-Portal Mapping

| Article Theme Directory | Portal Slug |
|------------------------|-------------|
| `reframation/` | `reframation` |
| `metanoia/` | `metanoia` |
| `forgotten-ways/` | `forgotten-ways` |
| `movement-intelligence/` | `movement-intelligence` |
| `discipleship-disciple-making/` | `discipleship` |
| `apest-fivefold-ministry/` | `mdna` |
| `jesus-is-lord-mdna/` | `mdna` |
| `apest-culture/` | `mdna` |
| `liminality-communitas/` | `forgotten-ways` |
| `missional-incarnational-impulse/` | `movement-intelligence` |
| `organic-systems/` | `movement-intelligence` |

---

## Step 3 — Copy New Content

For each source file:
1. Check if it already exists in the docs repo (by filename)
2. If not, copy it to the correct destination directory
3. If it exists, compare modification dates — keep the newer version
4. Never overwrite without checking

Use `cp` via Bash for file operations. Create directories as needed with `mkdir -p`.

---

## Step 4 — Deduplicate

Some content exists in multiple repos (e.g., pathway-audit skill in both alan-hirsch and adam-seiz). When duplicates are found:
1. Compare content — if identical, keep one and note the duplicate
2. If different versions, keep both with a suffix indicating source (e.g., `pathway-audit-alan-hirsch.md`, `pathway-audit-adam-seiz.md`)
3. Log deduplication decisions

---

## Step 5 — Update README

After organizing, update `~/Desktop/Dev/repos/docs/README.md`:
1. Verify the directory structure section matches reality
2. Update the source repositories table with any new sources
3. Add file counts per section

---

## Step 6 — Generate Per-Portal Index

For each portal, create or update `pathways/{slug}/INDEX.md`:

```markdown
# {Portal Title} — Content Index

## Vision
- [filename](vision/filename.md) — brief description

## Articles (N files)
- [filename](articles/filename.md) — brief description
...

## Case Studies
...

## HTML Templates
...

## Completeness (vs 12-section architecture)
- [x] Overview
- [ ] The Model
- [x] Quotes
...
```

---

## Step 7 — Report

Print a summary of what was organized:
- Files added
- Files updated
- Duplicates resolved
- Gaps remaining per portal
