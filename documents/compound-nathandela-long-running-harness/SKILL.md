---
name: Compound
description: Reflect on the cycle and capture high-quality lessons for future sessions
---

# Compound Skill

## Overview
Extract and store lessons learned during the cycle, and update project documentation. This is what makes the system compound -- each session leaves the next one better equipped.

**CRITICAL**: Store all lessons via `ca learn` -- NOT via MEMORY.md, NOT via markdown files.
Lessons go to `.claude/lessons/index.jsonl` through the CLI. MEMORY.md is a different system and MUST NOT be used for compounding.

## Methodology
1. Review what happened during this cycle (git diff, test results, plan context)
2. Detect spec drift: compare final implementation against original EARS requirements in the epic description (`bd show <epic>`). Note any divergences -- what changed, why, was it justified. If drift reveals a spec was wrong or incomplete, flag that for lesson extraction.
3. Detect **verification drift**: compare the work and review evidence against the epic's `## Verification Contract`. If review had to escalate the contract, or if planned evidence was too weak/too strong, capture that as a workflow-quality lesson.
4. Spawn the analysis pipeline in an **AgentTeam** (TeamCreate + Task with `team_name`):
   - Role skills: `.claude/skills/compound/agents/{context-analyzer,lesson-extractor,pattern-matcher,solution-writer,compounding}/SKILL.md`
   - For large diffs, deploy MULTIPLE context-analyzers and lesson-extractors
   - Pipeline: context-analyzers -> lesson-extractors -> pattern-matcher + solution-writer -> compounding
   - Agents coordinate via SendMessage throughout the pipeline
5. Agents pass results through the pipeline via `SendMessage`. The lead coordinates: context-analyzer and lesson-extractor feed pattern-matcher and solution-writer, which feed compounding.
6. Apply quality filters: novelty check (>0.98 cosine similarity = skip), specificity check
7. Classify each item by type: lesson, solution, pattern, or preference
8. Classify severity: high (data loss/security/contradictions), medium (workflow/patterns), low (style/optimizations)
9. Use `AskUserQuestion` to confirm high-severity items with the user before storing; medium/low items are auto-stored
10. Store via `ca learn` with supersedes/related links where applicable.
   At minimum, capture 1 lesson per significant decision made during this cycle
11. **Lint graduation**: Spawn the `lint-classifier` subagent (`.claude/agents/compound/lint-classifier.md`). Pass it the list of newly captured insights from step 10 via SendMessage (each with id, insight text, and severity). The subagent classifies each as LINTABLE, PARTIAL, or NOT_LINTABLE. For LINTABLE + HIGH confidence items, it detects the project's linter and creates beads tasks under a "Linting Improvement" epic. All insights remain stored as lessons regardless of classification.
12. Delegate to the `compounding` subagent to run synthesis: cluster accumulated lessons by similarity and write CCT patterns to `.claude/lessons/cct-patterns.jsonl`
13. Update outdated docs and deprecate superseded ADRs (set status to `deprecated`)

## Docs Integration
- doc-gardener checks if `docs/` content is outdated after the cycle
- Check `docs/decisions/` for ADRs contradicted by the work done
- Set ADR status to `deprecated` if a decision was reversed, referencing the new ADR

## Literature
- Consult `docs/compound/research/learning-systems/` for knowledge compounding theory, spaced repetition, and lesson extraction methodology
- Run `ca knowledge "knowledge compounding"` for indexed knowledge on learning systems
- Run `ca search "compound"` for lessons from past compounding cycles

## Common Pitfalls
- Not spawning the analysis team (analyzing solo misses cross-cutting patterns)
- Capturing without checking for duplicates via `ca search`
- Skipping supersedes/related linking when an item updates prior knowledge
- Not checking if docs or ADRs need updating after the cycle
- Requiring user confirmation for every item (only high-severity needs it)
- Not classifying items by type (lesson/solution/pattern/preference)
- Capturing vague lessons ("be careful with X") -- be specific and concrete
- Not capturing when the Verification Contract was too weak or over-specified for the actual work

## Quality Criteria
- Analysis team was spawned and agents coordinated via pipeline
- Quality filters applied (novelty + specificity)
- Duplicates checked via `ca search` before capture
- Items classified by type (lesson/solution/pattern/preference)
- Supersedes/related links set where applicable
- Outdated docs and ADRs were updated or deprecated
- User confirmed high-severity items
- Beads checked for related issues (`bd`)
- Each item gives clear, concrete guidance for future sessions
- Spec drift analyzed and captured
- Verification drift analyzed and captured when the contract needed adjustment

## FINAL GATE -- EPIC CLOSURE
Before closing the epic:
- Run `ca verify-gates <epic-id>` -- must return PASS for both gates
- Run `pnpm test` and `pnpm lint` -- must pass
- Read the epic's `## Verification Contract` and run every required evidence item that remains applicable. If `build` is required, run `pnpm build`
If verify-gates fails, the missing phase was SKIPPED. Go back and complete it.
CRITICAL: 3/5 phases is NOT success. All 5 phases are required.
