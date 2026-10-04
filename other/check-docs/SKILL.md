---
name: check-docs
description: Check docs/ai/ spec files and ADRs for inconsistencies with the actual codebase. Report only, no modifications.
allowed-tools: Read, Glob, Grep, Agent, Bash(ls *)
---

# Check Docs Consistency

Scan all documentation in `docs/ai/`, site docs, and app help for inconsistencies with the actual codebase. **Do not modify any files.**

## Scope

Check these doc files against implementation:

### Root docs

1. `README.md` — project description, feature list, tech stack, project structure

### AI / internal docs (`docs/ai/`)

2. `CLAUDE.md` — project description, build commands, conventions, key architecture notes
3. `docs/ai/BACKLOG.md` — check completed items against code, remove if done
4. `docs/ai/architecture.md` — ADR statuses, component list, directory structure, commands
5. `docs/ai/overview.md` — current state, non-goals
6. `docs/ai/sequencer-spec.md` — Pattern/Track/Trig interfaces, playback behavior
7. `docs/ai/audio-interface.md` — WorkletCommand, WorkletPattern, WorkletTrig, Engine API
8. `docs/ai/sound-design.md` — voice params, paramDefs ranges/defaults
9. `docs/ai/ui-design.md` — component descriptions, layout, mobile views
10. `docs/ai/glossary.md` — term accuracy, missing terms
11. `docs/ai/DATA_MODEL.md` — Song/Pattern/Cell/Track/Trig interfaces, relationships, **mermaid ERD entity fields and classDiagram runtime state fields**
12. `docs/ai/MESSAGE_FLOW.md` — WorkletCommand flow, message protocol, signaling, **mermaid sequence diagram function names**
13. `docs/ai/adr/INDEX.md` — ADR statuses (Implemented vs actual state)
14. All ADR files marked as "Implemented" in INDEX.md — check against code

### Site docs (`site/src/content/docs/`)

15. All `.mdx` files under `site/src/content/docs/docs/` (EN) and `site/src/content/docs/ja/docs/` (JA) — tutorials, feature guides, getting-started pages
16. Feature descriptions must match current implementation (e.g. number of FX slots, available parameters, signal flow)
17. EN and JA versions must stay in sync with each other

### App help (`src/lib/components/SidebarHelp.svelte`)

18. Help card text — feature descriptions, parameter lists, workflow descriptions

## Process

1. **Read all doc files** listed above.

2. **Cross-reference with codebase** by reading/grepping these key source files:
   - `src/lib/types.ts` — Song, Pattern, Cell, Trig, Track interfaces
   - `src/lib/state.svelte.ts` — reactive state shape
   - `src/lib/audio/engine.ts` — Engine API, patternToWorklet serialization
   - `src/lib/audio/dsp/types.ts` — WorkletCommand, WorkletPattern, WorkletTrig, WorkletInsertFx
   - `src/lib/audio/worklet-processor.ts` — WorkletCommand handling
   - `src/lib/paramDefs.ts` — voice parameter definitions (names, ranges, defaults)
   - `src/lib/components/*.svelte` — component names and existence
   - `src/lib/audio/dsp/voices.ts` — voice registry
   - `src/lib/components/SidebarHelp.svelte` — app help text

3. **Check for these types of inconsistencies**:
   - Type/interface field mismatches (missing fields, wrong field names, wrong types)
   - **Mermaid diagrams**: treat `erDiagram` entity fields and `classDiagram` class fields as structured data — compare every field name, type, and description 1:1 against the source TypeScript interfaces (DATA_MODEL.md ERD vs `types.ts`, classDiagram vs `state.svelte.ts`, MESSAGE_FLOW.md sequence diagrams vs actual function names in `scenePlayback.ts` / `engine.ts`)
   - Wrong parameter ranges or defaults in docs vs paramDefs.ts
   - Components mentioned in docs that don't exist, or existing components not documented
   - ADR status mismatches (doc says PROPOSED but feature is implemented, or vice versa)
   - Removed/renamed features still documented
   - Missing documentation for implemented features
   - Stale line-number references to source files

4. **Output a report** in this format:

```
## Docs Consistency Report

### [filename]
- **[section]**: [description of inconsistency]
  - Doc says: [what the doc states]
  - Code says: [what the code actually does]

### No issues found
- [filename] — OK
```

## Guidelines

- Use parallel Agent tools to speed up codebase exploration
- Be thorough — check every interface field, every param range, every component reference
- Only report confirmed inconsistencies, not stylistic preferences
- Group findings by file for easy reference
- This is a READ-ONLY operation — do not edit any files
