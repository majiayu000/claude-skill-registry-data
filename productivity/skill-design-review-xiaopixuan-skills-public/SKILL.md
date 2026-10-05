---
name: skill-design-review
description: Evaluate whether a Codex skill should be kept, simplified, merged, rewritten, deleted, or improved through realistic task cases, baseline comparisons, necessity checks, rubrics, and targeted SKILL.md revisions. Use when the user asks to review a skill, 检验/评测/优化/删除/合并一个 skill, run a skill evaluation loop, compare performance with and without a skill, build a scorecard for a skill, or identify whether a skill's trigger, necessity, workflow, output format, and content quality are strong enough.
license: MIT
tags:
  - codex-skill
  - agent-skill
  - skill-review
  - skill-evaluation
  - skill-assessment
  - prompt-evaluation
  - prompt-optimization
  - rubric
  - baseline-comparison
---

# Skill Design Review

## Goal

Use an evaluation loop to determine whether a target skill still deserves to exist, whether it actually improves task execution, and what smallest change should be made next.

Prefer concrete tests over abstract critique. The expected result is a disposition decision, a filled scorecard, and one targeted action: keep, simplify, merge, rewrite, delete, or patch the skill depending on the evidence and the user's edit permissions.

## Inputs

Collect or infer these inputs before scoring:

- Target skill path or skill name.
- Two realistic test cases with different user styles. Each test case should include the user request and any input artifact, file, or context needed to run it.
- Expected output shape for each test case.
- Candidate overlap: any nearby skill, built-in capability, tool, script, template, or higher-level instruction that may make the target skill unnecessary.

If the user did not provide test cases, draft two realistic cases from the skill's purpose and say they are inferred.

## Evaluation Loop

1. Inspect the target skill.
   Read its `SKILL.md` completely. Read referenced files only when needed to understand the workflow being tested.

2. Assess necessity before improving.
   Decide whether the skill provides durable value beyond a strong general agent. A skill is worth keeping when it provides at least one of these:
   - Non-obvious domain knowledge that a general agent would often miss.
   - A repeatable workflow that prevents common failures.
   - Tool, script, asset, template, or file-routing knowledge.
   - Output standards that must stay stable across runs.
   - Organization-specific judgment, terminology, or process memory.
   - Evidence that using the skill improves quality versus a baseline without it.

   A skill should be simplified, merged, rewritten, or deleted when:
   - It only restates general reasoning patterns.
   - A baseline agent already performs equally well without it.
   - It adds long instructions but no measurable quality gain.
   - It conflicts with higher-level system/developer instructions.
   - It mainly preserves outdated tool behavior or obsolete workflows.
   - It overlaps heavily with another stronger skill.

3. Prepare the tests.
   Use two test cases that differ in tone, specificity, or artifact type. Include at least one ordinary request and one edge or ambiguous request.

4. Run a baseline comparison.
   For each test case, compare how the task would be handled without the target skill versus with the target skill. If a clean baseline is impossible because the skill has already been read, mark the baseline as "best-effort / contaminated" rather than pretending it is independent.
   When independent subagents or fresh tasks are available and safe to use, run the with-skill pass separately from the baseline pass. Pass only the target skill, user request, and raw artifacts; do not pass the expected diagnosis or planned fix.

5. Score with the rubric.
   Read `references/rubric.md` before assigning scores. Score skill necessity, trigger behavior, workflow guidance, output format, and content quality. Add short evidence for every non-perfect score.

6. Choose a disposition.
   Select exactly one disposition:
   - Keep: the skill clearly improves results and is not too costly.
   - Keep but simplify: the skill is useful but has excess instructions, weak examples, or stale details.
   - Merge: the skill is useful but mostly belongs inside another stronger skill.
   - Rewrite: the skill is valuable in intent but structurally unclear or misleading.
   - Delete: the skill adds no measurable value beyond baseline or is obsolete.
   - Patch: the skill is worth keeping and has one narrow, high-impact gap.

7. Revise and re-run.
   If the disposition is Patch, Keep but simplify, Merge, Rewrite, or Delete, make the smallest evidence-backed file change allowed by the user. For Merge or Delete, do not remove content unless the user explicitly asked for destructive cleanup; otherwise recommend the exact merge/delete action.
   Patch the target skill only where the evidence shows a gap, then re-run the affected test or rubric check. Record whether the score changed and why.
   If the user forbids edits or asks for review-only, do not patch files. Instead, describe the smallest recommended patch and re-score the affected criterion as a dry-run projection, clearly marking the actual file as unchanged.

## Output Format

Return the result in this order:

1. **Verdict**
   State whether the skill passes, conditionally passes, or fails, and give the disposition: Keep, Keep but simplify, Merge, Rewrite, Delete, or Patch.

2. **Necessity Assessment**
   State the durable value the skill provides, what overlaps with baseline agent ability or nearby skills, and why the skill should or should not continue to occupy context.

3. **Test Cases**
   List the two test cases and expected output shapes.

4. **Scorecard**
   Provide a table with criterion, score, evidence, and fix.

5. **Comparison**
   Summarize the with-skill versus without-skill difference.

6. **Targeted Action**
   Describe the exact change made or recommend the smallest keep/simplify/merge/rewrite/delete/patch action if the user asked for review only.

7. **Re-run Result**
   State what changed after the revision, including any remaining risk.

## Judgment Rules

- Pass when all required criteria score 2 and total score is at least 9 out of 10.
- Conditional pass when total score is 6-8 or one required criterion scores 1.
- Fail when any required criterion scores 0 or total score is below 6.
- Required criteria are skill necessity, trigger behavior, output format, and content quality.
- Do not optimize for prettiness alone. Prefer changes that make the next agent know what to do, when to do it, and what to produce.
- Keep revisions narrow, measurable, and tied to a test failure.
- Prefer deletion or merge recommendations over polishing when the skill no longer produces measurable lift over a baseline agent.
