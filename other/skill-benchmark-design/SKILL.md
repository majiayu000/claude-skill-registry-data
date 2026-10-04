---
name: skill-benchmark-design
description: Design lightweight benchmarks for agent skills and skillsets. Use when Codex is asked to prove whether a skill improves outputs, define benchmark scenarios, compare baseline versus skill-enabled behavior, or create a skill evaluation plan.
license: MIT
---

# Skill Benchmark Design

## Core Workflow

1. Name the skill or bundle under test, target user, target artifact, and
   decision the benchmark must support.
2. Select realistic scenarios that exercise normal, edge, and risky requests
   without leaking expected answers into the prompt.
3. Define baseline and skill-enabled runs using the same prompt, source
   material, and acceptance criteria.
4. Choose scoring criteria from `docs/evaluation/skill-quality-rubric.md` and
   add task-specific pass/fail checks.
5. Specify evidence capture: prompt, inputs, outputs, reviewer notes,
   validation output, loaded context, tools/scripts, and overhead when
   available.
6. Set the decision rule: keep, revise, split, merge, defer, or retire.

## Overhead And Composition Checks

- Include one repeated-run or batch scenario when the skill may be used many
  times in one thread.
- Compare monolithic guidance against composed skills or skillsets when the
  workflow has separable stages.
- Capture activated skills, loaded references, command/script output, MCP tool
  use, artifacts, and validation results.
- Keep host optimizations optional. Benchmark Claude Code `context: fork`,
  dynamic `!command` injection, or MCP Tool Search separately from the portable
  AgentSkills baseline.
- Do not report exact context or token savings unless the host exposes reliable
  measurements.

## Safety Rules

- Do not use private customer, employee, security, or financial data in public
  benchmark artifacts.
- Do not optimize prompts by exposing the expected answer.
- Do not treat an automated judge as sufficient for legal, financial,
  security, employment, medical, or production-impacting workflows.
- Keep tracing, scoring, and observability tools optional and vendor-neutral.

## Deliverable Shape

For benchmark plans, provide:

- Skill or bundle under test
- Target artifact and target user
- Scenarios and source material
- Baseline and skill-enabled run plan
- Acceptance criteria and scoring rubric
- Evidence capture plan
- Overhead and composition checks
- Safety boundaries
- Promotion decision rule

## References

- Read `references/skill-benchmark-design-checklist.md` when designing or
  reviewing a skill benchmark.
