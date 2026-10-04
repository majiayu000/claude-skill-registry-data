---
name: evidence-first-debugging
description: Use when debugging a crash, lỗi, failing game, tool, build, service, script, or reproducible local code failure requires repro or reproduction, giả thuyết or ranked hypotheses, instrumentation, root-cause isolation, a minimal fix, regression proof, and a regression test.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: verify
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: debug-verdict.md
    required_evidence: [reproduction, hypothesis-log, regression-test]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from:
        repo: mattpocock/skills
        path: skills/engineering/diagnosing-bugs/SKILL.md
        commit: 84fdeffd12f2ee307994d1eb6feb48173b6e0502
        license: MIT
      patterns_from: [addyosmani debugging eval fixtures, AGENTS.md evidence contract]
      copied_text: none
---
# Evidence-First Debugging

## Overview
Find the root cause before changing code. A fix is complete only when the original symptom is reproduced, isolated, repaired minimally, and guarded by regression evidence.

## When to use
Use for crashes, wrong behavior, failing tests, startup problems, packet mismatches, offline failures, build errors, or unexpected generated output.

## When NOT to use
Do not use for open-ended feature design, routine build verification, broad code review, or mutation without a reproducible symptom.

## Required inputs and context discovery
Collect exact symptom, expected behavior, reproduction steps, frequency, environment, first failing version or commit when known, logs, relevant ownership boundaries, and safe instrumentation options.

## Safety and risk level
Inspection and instrumentation are preferred. Any mutation follows test-first discipline and exact file ownership; database, services, assets, or external projects need separate safety approval.

## Workflow
1. Reproduce the symptom with the smallest deterministic command or fixture.
   Completion criterion: failure occurs for the expected reason, or reproduction is BLOCKED with evidence.
2. Trace the data and control path from observed failure toward its source using native inspection and, when available, a fresh code-intelligence provider.
   Completion criterion: component boundaries and the first incorrect state are identified; inferred, dynamic, generated, and stale graph edges are labeled rather than treated as causal proof. Source, logs, tests, and runtime evidence own the root-cause verdict.
3. Rank hypotheses and add minimal instrumentation that distinguishes them.
   Completion criterion: one hypothesis is supported and alternatives are weakened by output.
4. Write a failing regression test or executable check before the fix.
   Completion criterion: the check fails on the original behavior.
5. Apply the smallest root-cause fix and rerun the focused check.
   Completion criterion: the focused check passes without weakening assertions.
6. Run adjacent and broader verification, then record limitations.
   Completion criterion: regressions are checked or explicitly BLOCKED.

## Evidence and output contract
Produce reproduction command, failure output, hypothesis table, instrumentation evidence, changed files, regression test, verification commands, verdict, and limitations.

## Handoff contract
Include the exact failing symptom, confirmed root cause or remaining hypotheses, instrumentation locations, failed attempts, current diff, commands, and the next discriminating experiment.

## Pitfalls and anti-rationalization
- Do not edit code before reproduction or a failing check.
- Do not stack speculative fixes.
- Do not replace a root-cause explanation with “timing issue” or “Unity quirk” without evidence.
- No graph result is not proof that no dependency exists. Confirm important edges with source, logs, tests, or runtime evidence.
- Do not mark intermittent or unavailable reproduction as PASS.

## Verification checklist
- [ ] Original symptom was reproduced or labeled BLOCKED.
- [ ] Root cause is supported by evidence.
- [ ] Regression check failed before the fix.
- [ ] Focused and adjacent checks are fresh.
- [ ] Limitations and remaining hypotheses are explicit.

## References and scripts
Use project logs and native tests first. Pair with `build-and-runtime-verification` for the final verdict and `studio-handoff` for multi-session work.
