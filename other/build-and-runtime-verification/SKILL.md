---
name: build-and-runtime-verification
description: Use when running build, compile, test, launch, or runtime checks and producing a verdict tied to exact commands, exit codes, artifact paths, limitations, and fresh evidence.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: gate
    lifecycle_stage: verify
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: verdict.md
    required_evidence: [command-output, exit-code, artifact-path]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [AGENTS.md Claim to Evidence to Verdict contract]
      copied_text: none
---
# Build and Runtime Verification

## Overview
Verification is a reproducible claim: exact command, environment, exit code, observable artifact, verdict, and limitations.

## When to use
Use after implementation, before completion claims, for build failures, runtime smoke checks, script compilation, generated artifact comparison, or release preflight.

## When NOT to use
Do not use a compile-only result to claim gameplay, performance, database, network, or regression safety that was not exercised.

## Required inputs and context discovery
Collect repository root, expected command, prerequisites, environment/version snapshot, expected artifact, timeout, safe side effects, and what the check does not prove.

## Safety and risk level
The gate is read-only with respect to source. If a command starts services, writes caches, imports data, opens an editor, or mutates external state, route through the relevant safety workflow first.

## Workflow
1. Define the claim and the single command or command sequence that proves it.
   Completion criterion: success and failure signals are explicit before execution.
2. Verify prerequisites and capture environment versions without changing them.
   Completion criterion: missing dependencies are labeled BLOCKED.
3. Run the narrowest check and capture stdout, stderr, duration, and exit code.
   Completion criterion: raw results are available even when the command fails.
4. Inspect the expected artifact or runtime signal rather than relying on exit code alone.
   Completion criterion: artifact existence and relevant properties are recorded.
5. Issue PASS, FAIL, or BLOCKED with limitations.
   Completion criterion: the verdict does not exceed what the evidence proves.

## Evidence and output contract
Produce `verdict.md` or a summary JSON with claim, command, exit code, artifact path, environment snapshot, verdict, limitations, and reviewer when required.

## Handoff contract
Include failing command, first actionable error, artifact/log paths, prerequisites, retries already attempted, and the safest next diagnostic step.

## Pitfalls and anti-rationalization
- Previous successful output is not fresh evidence.
- Exit code zero without the expected artifact may still be FAIL.
- Compile success is not runtime success.
- Missing Unity, services, model runner, or credentials is BLOCKED.

## Verification checklist
- [ ] Claim and command match.
- [ ] Exit code is captured.
- [ ] Expected artifact or runtime signal is inspected.
- [ ] Limitations are explicit.
- [ ] Verdict is PASS, FAIL, or BLOCKED.

## References and scripts
Read [references/commands.md](references/commands.md) for exit-code capture across shells, environment snapshots, artifact freshness proof, runtime smoke patterns, and the observation-to-verdict mapping. Use repository-native commands first, then `python -m unittest`, `python -m compileall`, and kit gate scripts where applicable.
