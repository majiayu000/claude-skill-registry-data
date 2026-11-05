---
name: effort-score
description: Score planning units with the effort spec (8 factors, 0-2 each, levels low/med/high/enormous) instead of time estimates. Use after new or changed units, or when the user asks to score units.
---

# Effort score

Read `planning/EFFORT.md` (the factors U, M, C, P, D, B, V, T with their descriptions and examples). Never write a time estimate.

1. List the units to score (the ones the user names, or every unit file without an `Effort:` line).
2. For each unit, read its file. For C (changes to existing work) and T (test cover today), take a short look at the code it touches: are there tests in or next to those files?
3. Score each factor 0, 1 or 2. Total 0-16: low 0-5, med 6-8, high 9-11, enormous 12+.
4. Write `Effort: <level> (U1 M1 C1 P1 D1 B1 V1 T1). <reason, at most 15 words>` under the branch line of the unit file, and in the `Effort` column of its batch table.
5. Many units: split them among read-only subagents (about 35 each) that return JSON lines (`unit`, the 8 scores, `why`); write the results yourself.
6. Report the counts per level and list every enormous unit (they must be split before they start: `/plan-batches`), plus the close calls.
