---
name: team-csharp
description: "Orchestrate the C# / .NET engineering team: architecture, implementation, tests, review, determinism, Unity adapter work, and build/CI coordination for Project Aegis C# code."
argument-hint: "[architecture|implementation|test|review|devops|determinism|full-story] [scope] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
model: sonnet
agent: lead-programmer
---

# Team C# — C# / .NET Engineering Orchestration

Use this skill as the coordinated entry point for C# work across plain .NET,
Unity-facing C#, test projects, build configuration, and deterministic simulation
code. It routes work through `lead-programmer` and the C# specialist agents.

## Phase 0: Resolve Mode and Review Level

Modes:

- `architecture` — design assemblies, namespaces, APIs, interfaces, and dependency seams.
- `implementation` — implement approved C# contracts and story logic.
- `test` — author or review EditMode, PlayMode, or plain .NET tests.
- `review` — run language- and Unity-specific C# review.
- `devops` — update build, test, CI, project, solution, or assembly configuration.
- `determinism` — inspect seeded RNG, ordering, wall-clock, replay, and hash behavior.
- `full-story` — story-readiness → architecture → implementation → tests → review → done.
- No mode — infer from the request; if ambiguous, ask one focused question.

Review mode:
1. If `--review [full|lean|solo]` is present, use it.
2. Else read `production/review-mode.txt` if present.
3. Else default to `lean`.

## Team Composition

- **lead-programmer** — orchestration, API fit, routing, code-level decisions.
- **c-sharp-architect** — assembly boundaries, namespaces, contracts, dependency direction.
- **c-sharp-engineer** — approved C# implementation in plain .NET and Unity C#.
- **c-sharp-test-engineer** — NUnit, Unity Test Framework, fixtures, test seams.
- **c-sharp-reviewer** — read-only C# review for correctness, GC, async, lifecycle, SOLID.
- **c-sharp-devops-engineer** — dotnet/MSBuild, Unity batchmode, CI, package/assembly config.
- **unity-specialist** and Unity sub-specialists — Unity adapter and engine API authority.
- **determinism-engineer** — reproducibility, replay, deterministic ordering, seeded RNG.
- **qa-lead / qa-tester** — test strategy, acceptance evidence, bug reporting.
- **technical-director** — escalation for cross-system architecture or dependency decisions.

## Phase 1: Load Required Context

Read and summarize only the necessary context:

- Story/spec/GDD or user-provided scope.
- `docs/architecture/architecture.md` and relevant ADRs when architecture is affected.
- `docs/architecture/control-manifest.md` if present.
- `.claude/teams/csharp-team.yaml` for routing and ownership.
- Relevant `.csproj`, `.sln`, `.asmdef`, Unity package, and test files.
- Existing source files in the target area.

Report the likely owning agent, affected source areas, and validation needed.

## Phase 2: Select Workflow Pipeline

### Architecture Pipeline

1. Route to `c-sharp-architect` for assembly/API/namespace contract.
2. Consult `unity-specialist` for Unity-facing or DOTS/Addressables/UI concerns.
3. Escalate to `technical-director` for dependency, package, or cross-layer decisions.
4. Produce an architecture sketch and ask before implementation.

### Implementation Pipeline

1. Confirm story/spec readiness and approved architecture contract.
2. Route implementation to `c-sharp-engineer` or the owning domain programmer.
3. Require tests or a test plan for logic changes.
4. Hand off to `c-sharp-reviewer` before completion.

### Test Pipeline

1. Route test design to `c-sharp-test-engineer`.
2. Prefer isolated plain .NET or Unity EditMode tests; use PlayMode only when required.
3. Coordinate with `c-sharp-engineer` if seams are missing.
4. Run the smallest relevant test scope and report results.

### Review Pipeline

1. Route C# files to `c-sharp-reviewer` for language and Unity-specific review.
2. Route architectural drift to `c-sharp-architect`.
3. Route acceptance/test-evidence gaps to `qa-lead` or `/test-evidence-review`.
4. Produce APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED.

### DevOps Pipeline

1. Route build, solution, project, asmdef, package, and CI changes to `c-sharp-devops-engineer`.
2. Require explicit approval before dependency or workflow changes.
3. Validate with `dotnet build`, `dotnet test`, or Unity test runner where available.

### Determinism Pipeline

1. Route deterministic simulation concerns to `determinism-engineer`.
2. Check for wall-clock reads, unordered iteration, unseeded RNG, and replay hash drift.
3. Use `/determinism-audit` and `/replay-verify` when sim behavior is affected.

## Phase 3: Decision Gates

Ask before proceeding when the change affects:

- Public APIs, assembly boundaries, or dependency direction.
- NuGet/UPM packages, `.csproj`, `.sln`, `.asmdef`, or CI configuration.
- Unity engine integration patterns.
- Deterministic replay behavior or golden baselines.
- Multi-file implementation plans.

## Output

Produce a concise orchestration report:

- Mode and scope.
- Agents/skills invoked or recommended.
- Affected source areas.
- Architecture and determinism risks.
- Test/review/build validation plan.
- Next approved action.
