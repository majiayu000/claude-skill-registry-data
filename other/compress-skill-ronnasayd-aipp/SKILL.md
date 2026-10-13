---
name: compress-skill
description: "Compresses a verbose SKILL.md into a short, scannable core file by moving prose into tables, mermaid flowcharts, and reference files — without losing technical substance. Use when a SKILL.md has grown long (200+ lines of numbered prose, repeated Notes sections, verbatim templates inline) and the user asks to make it 'shorter but still effective', 'more direct', 'use tables/lists/graphs', 'split into reference files', or 'compress this skill'."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.1.0"
---

# Compress Skill

Shrinks an existing `SKILL.md` into a short, decision-critical core, relocating dense/large/redundant content into reference files. Preserves every rule, threshold, and edge case — nothing is lost, only relocated or deleted if truly redundant.

## Steps

| #   | Step                  | Action                                                                                                                                               | Output / Gate                                                                                                      |
| --- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| 1   | Read target           | Read the full `SKILL.md`                                                                                                                             | inventory of sections: steps, branching logic, tables, verbatim templates, Notes/recap                             |
| 2   | Read existing refs    | Read every file already linked from the skill (`references/*.md` or similar)                                                                         | flag any that describe a stale/older mechanism than the current main file — these must be rewritten, not just kept |
| 3   | Classify content      | See classification table below                                                                                                                       | each section tagged: table / flowchart / extract-to-ref / delete                                                   |
| 4   | Design ref file set   | One file per template category; one file for detailed mechanism/flowchart; keep existing example/troubleshooting files (rewrite if stale per step 2) | file list finalized before writing                                                                                 |
| 5   | Write reference files | Write tool, refs first                                                                                                                               | main file's pointers can be one line each since detail lives here                                                  |
| 6   | Rewrite main SKILL.md | See rewrite checklist below                                                                                                                          | short core file + "Reference files" map at the end                                                                 |
| 7   | Verify nothing lost   | Diff old content section-by-section against new tables/refs                                                                                          | every rule/threshold/edge case appears somewhere in the new set                                                    |
| 8   | Report                | State size delta + what moved where                                                                                                                  | e.g. "298 → 55 lines; templates → agent-prompts.md, flowchart → orchestrator-model.md, stale example rewritten"    |

## Classification table (Step 3)

| Content shape                                     | Treatment                                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Linear numbered steps with input/output           | table: step, input, output/gate                                                      |
| Branching logic (if/else, retry/skip/abort)       | table (condition → action); use mermaid flowchart instead if branches loop/cycle     |
| Verbatim templates (agent prompts, code payloads) | extract to dedicated reference file, one-line pointer left in main file              |
| Notes/recap section restating the body            | delete — redundant content has zero compression floor, don't summarize it, remove it |
| Wordy prose inside an already-tabular cell        | trim in place — see wording-tightening pass below; no restructure needed             |

## Wording-tightening pass (already-tabular content)

When a table/section already exists but cells are verbose, tighten wording without dropping substance:

- Drop filler: "in order to" → "to", "make sure to" → drop, "you should" → drop, restated rationale already implied by a command.
- Cut connective throat-clearing ("Also actually open...", "Note that...") — keep the instruction, drop the preamble.
- Shorten to fragments: commands, thresholds, flags, and named tools stay verbatim; surrounding prose becomes clipped phrases.
- Collapse repeated qualifiers ("don't X, and don't Y, and don't Z" → "don't X/Y/Z" or a short list).
- Keep every number, flag, command, filename, and named exception — only the connective tissue is cut.
- Apply per-cell, not per-file: a cell can be tightened even when the surrounding table structure is otherwise left alone.

## Rewrite checklist (Step 6)

- Keep frontmatter (`name`, `description`, `metadata`) unchanged unless scope changed — bump `version` if content meaningfully changed.
- Open with 2-3 sentences: who drives what, the one non-obvious rule (a gate, a threshold, an ownership boundary).
- Replace numbered prose steps with the Step 1 table's output.
- Replace branching prose with condition→action tables or a flowchart.
- Replace verbatim templates with one-line pointers to extracted files.
- Delete sections that only recap content already covered elsewhere.
- End with "Reference files" list — one line per file, stating what it contains.

## Reusable heuristic

Compress only what is dense and unique. Delete what is redundant. Relocate what is large and copy-paste (templates). Keep in the main file only what is decision-critical and short (tables, gates, thresholds).
