---
name: skill-optimize
description: Reduce the loaded token cost of one existing skill without weakening its trigger, decisions, safety, or outcome. Use when the user supplies a skill path and authorizes a focused rewrite, not to create or repurpose a skill.
---

# Skill Optimization

Rewrite one existing `SKILL.md` for lower context cost while preserving its effective contract. Treat token reduction as a constraint, not the primary outcome.

## Inspect the contract

1. Resolve a relative path by joining it to the output of `pwd`, not to this skill's own directory or the repository that holds it, and confirm that it points to one existing `SKILL.md`, that editing it is authorized, and which repository or plugin owns it. Read applicable repository instructions, the skill format, the complete target, and each resource whose contract may justify removing target text. Inspect working-tree state and preserve unrelated changes. If the target is already modified, treat its working content as the source; use Git only to understand committed history.
2. Record baseline line, word, and byte counts. Record tokens only when a suitable tokenizer is already available; do not add a dependency for measurement.
3. Search with `rg` for catalog entries, callers, references, neighboring skills, shared policy, and other owners of the same mechanics. Before relying on another skill to replace text, confirm it is available in the target runtime, read it completely, and verify that its trigger and contract cover the delegated work.
4. Use `git log --follow -- <path>`, `git blame -- <path>`, and relevant `git show` diffs to learn why clauses were added. History is evidence, not current policy. Preserve the intent of past fixes only while it remains applicable.
5. Map the target's trigger and exclusions, responsibility, decisions, routing and ordering, unique invariants, permissions, safety boundaries, failure and exception paths, evidence, completion state, and required result. Classify each instruction as `keep`, `compress`, `delegate`, or `delete`, with a current owner or reason for every delegation and deletion. Keep this map in the active workflow unless the user requests an artifact.

## Rewrite the skill

1. Preserve the skill name and trigger semantics. Shorten the frontmatter description only when it remains concise, discriminating, and accurate.
2. Keep unique, non-obvious instructions that change decisions or protect outcomes. Compress repeated wording and delete generic capability or policy only when the repository, platform, or an assured runtime instruction already owns it.
3. When the target invokes another skill, retain the routing condition, order, authority boundary, handoff, and required result. Remove the invoked skill's internal mechanics only after confirming that its current contract covers them. Do not reproduce another skill's checklist.
4. Remove redundant preamble, examples, parallel-work variants, report fields, and repeated safety language only when they carry no distinct behavior. Merge headings and steps when sequence and ownership remain clear.
5. Do not hide context cost by moving always-required instructions into references. Add or move supporting resources only for genuinely conditional detail with a current consumer. Do not add scripts, dependencies, schemas, or abstractions merely to optimize prose.
6. Use `text-improve` after contract decisions to tighten the wording; do not use prose editing to decide which behavior can disappear.

Stop before a cut makes an instruction ambiguous, weakens authorization or safety, changes responsibility or observable output, loses a failure path, or relaxes the terminal state. Do not optimize toward a fixed percentage; an unchanged skill is correct when no safe material reduction exists.

## Verify the result

1. Compare the rewrite with the original contract map and relevant history. Confirm every retained requirement still has one clear owner, every delegation resolves, and no deletion changes behavior.
2. Review the final diff and every changed file. Update directly affected catalog text only when it became inaccurate; do not rename, version, release, install, commit, push, or change unrelated documentation unless separately authorized.
3. Measure the final file with the same method as the baseline. Report exact line, word, and byte changes; call a number a token reduction only when it came from a named tokenizer.
4. Run the available skill validator and the owning repository's native required checks. Do not add a wording-match test or parallel validator that cannot prove the contract.
5. A validator proves structure, not behavior. When eval cases exist for the skill, run the same cases before and after the rewrite, for example with `claude plugin eval --case <glob>`, and compare the scores. Each case runs a billed agent session, so create new cases or run a large suite only with the user's approval. Without an evaluation, report that behavior preservation rests on the contract map, not on a run.

Finish with the optimized path, before-and-after measurements, the important contracts preserved or delegated, checks and outcomes, and any residual risk or reason further reduction would be unsafe.
