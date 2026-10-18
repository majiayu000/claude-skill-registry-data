---
name: parallel-research
description: Coordinate aggressive parallel subagent fan-out for readonly work and persist one consolidated research report. Use when Codex is researching, auditing, updating docs, investigating multiple hypotheses, or exploring unrelated code paths without writing code. Do not use for code-writing tasks, tightly coupled edits, or work that is faster to finish locally on the critical path.
---

# Parallel Research

Use this skill only for readonly workflows. Goal: widen coverage fast, keep prompts clean, then synthesize before acting.

## Decide Fast

1. Confirm the task is readonly.
2. Confirm the work can be split into independent questions or areas.
3. Keep the immediate blocking step local. Delegate only sidecar work that can run in parallel.
4. Skip this skill for source or code mutation, patching, rebases, unrelated
   writes, or tightly coupled debugging that needs one continuous thread.
5. Durable-report mode is mandatory. Read [DURABLE-REPORT.md](DURABLE-REPORT.md)
   before dispatching lanes. Every run persists one consolidated report in the
   repository at the intended project-wiki folder or path; findings must not
   remain response-only or context-only.
   Research lanes remain readonly. Only the coordinator or one designated
   consolidator may write the report after synthesis. Finder child resolution
   uses this same mandatory durable mode.

## Split Cleanly

- Split by hypothesis, subsystem, artifact set, or question.
- Give each subagent one concrete ask.
- Avoid overlap. Two agents should not answer the same unresolved question unless cross-checking is the explicit goal.
- Prefer small batches, usually 2-4 subagents.

## Prompt Minimally

- Pass raw artifacts, paths, errors, or files.
- Do not leak your preferred answer, suspected fix, or private conclusions unless the task truly requires them.
- Ask for findings, evidence, primary-source citations, and file references.
- Prefer owning sources: official docs, source code, specs, and first-party APIs.
- Treat secondary write-ups as leads, not proof.
- For validation passes, make the prompt look like a normal user request, not a hidden test of the skill.

## Run In Parallel

1. Spawn subagents once the split is clear.
2. Keep working locally while they run. Synthesize, inspect source, or prepare follow-up questions.
3. Wait only when their output is needed for the next step.
4. Reuse an existing agent for related follow-ups instead of spawning duplicates.

## Synthesize Before Acting

- Compare outputs against the repo, docs, or other primary artifacts.
- Resolve disagreements with evidence, not majority vote.
- Follow every retained factual claim back to its primary source.
- Extract the few facts that matter, then decide locally.
- Close agents that are no longer needed.

## Good Fits

- Auditing separate features for regressions
- Researching several code paths before planning
- Checking multiple hypotheses for a bug without editing code
- Updating docs after parallel fact-gathering
- Reading unrelated subsystems to build context quickly

## Bad Fits

- Implementing production code
- Writing tests or making repo edits
- One small question that is faster to answer locally
- Work where every step depends tightly on the previous sub-step
- Delegation that would just duplicate your own immediate next action

## Output Contract

Return:
- what each subagent covered
- the evidence worth trusting, with claim-level source citations
- conflicts or uncertainty
- the synthesized conclusion
- the next local action
- durable report path in the intended project-wiki folder
