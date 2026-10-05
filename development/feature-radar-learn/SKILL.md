---
name: feature-radar-learn
description: |
  Extract reusable patterns, architectural decisions, and pitfalls from completed work
  into .feature-radar/specs/. Captures the "why" behind choices so future sessions build
  on past experience. MUST use this skill when the user reflects on what worked or didn't,
  wants to record a decision or pattern for future use, or hit a dead end worth documenting.
  Use when the user asks to remember, document, or extract lessons from recent work.
  Do NOT use for recording external observations — that's feature-radar-ref's job.
  Do NOT use for archiving completed features — that's feature-radar-archive's job.
---

# Extract Learnings

Capture reusable knowledge from completed work into `.feature-radar/specs/`.

## Deep Read

<HARD-GATE>
Read and follow `../feature-radar/references/DEEP-READ.md` — complete all 6 steps before proceeding.
</HARD-GATE>

## Behavioral Directives

<HARD-GATE>
Read and follow `../feature-radar/references/DIRECTIVES.md`.
</HARD-GATE>

## Workflow

1. **Identify the source** — ask the user what was just completed (feature, bug fix, refactor, investigation)
2. **Analyze the work** — review recent commits, changed files, and implementation decisions
3. **Extract knowledge** — classify each reusable piece into exactly one category, and state the classification in your output:
   - **Pattern**: recurring solution worth replicating (e.g., "three-tier config merge")
   - **Decision**: architectural choice with rationale (e.g., "YAML over JSON because...")
   - **Pitfall**: mistake or dead end to avoid
   - **Technique**: implementation approach that worked well

4. **Write to specs** — create or append to `.feature-radar/specs/{topic}.md`
5. **Checkpoint** — State what was written and ask: "I've written to `specs/{topic}.md` ({classification type}). Does this look correct, or should I adjust anything?" Wait for user confirmation before proceeding.
6. **Update base.md** — increment the specs count in Tracking Summary

## File Format

Use the format defined in `../feature-radar/references/SPEC.md` § 3.4 (`specs/{topic}.md`).

## Guidelines

- One topic per file. If the learning spans multiple topics, create multiple files.
- Name files by the pattern, not by the feature that produced it.
  - Good: `yaml-config-merge.md`, `symlink-vs-copy-tradeoffs.md`
  - Bad: `audit-feature-learnings.md`, `v2-refactor-notes.md`
- Append to existing files when the new learning extends a known topic.
- Keep it concise — future readers need the insight, not the full story.

## Example Output

```
→ Created specs/symlink-vs-copy-tradeoffs.md (Decision)
→ Updated base.md: specs 2 → 3
```

## Completion Summary

Follow the template in `../feature-radar/references/DIRECTIVES.md`, with skill name "Learn Complete".
