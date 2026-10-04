---
name: evolvable-software
description: >-
  Assess how ready a software product is to evolve itself safely, and how much
  of that AI drives, using the EVOLVE framework. Reports a Software Autonomy
  Level (L0 to L5) for three loops (request to release, issue to fix,
  opportunity to expansion), how far AI itself carries each loop, the critical
  controls that fail, exactly what blocks the next level, a six-capability
  profile, AI Readiness for products with AI features, and a
  prerequisite-ordered remediation plan, with every score tied to file-level
  evidence. Works for platforms, focused applications, developer platforms and
  agent runtimes. Use for self-evolution readiness, software autonomy levels,
  AI-driven or AI-built change, governed change, architecture readiness for
  autonomous change, or repeatable reassessment. Do not use as a security,
  accessibility, pull-request or delivery-process audit.
---

# EVOLVE: Self-Evolution Readiness Evaluation

## Purpose

Answer one question from evidence: **how ready is this product to evolve itself safely?** Three loops make the question concrete:

- **Request → Release:** can it take a request, implement it properly and release it?
- **Issue → Fix:** can it find problems users face, fix them and ship the fix?
- **Opportunity → Expansion:** can it notice adjacent needs and propose or launch them?

Each loop gets a Software Autonomy Level from L0 (manual) to L5 (self-directing). A loop's level is the lowest of four parts: its own stages, a shared release spine, an architecture foundation and a governance ceiling. The headline SAL is the lower of Request → Release and Issue → Fix; Expansion is reported beside it. Beside each loop, the scorer reports how far AI itself carries it, from the AI-qualified readings.

The six-capability profile explains the levels:

| Capability | Asks |
|---|---|
| Elastic (ARC) | Does the architecture scale, survive failure and recover its data? |
| Velocity (DEL) | Can a change be built, verified and released quickly and safely? |
| Open (MAL) | Can the product be reshaped without a code release? |
| Learn (LRN) | Does it notice problems, diagnose them and measure its changes? |
| Vet (GOV) | Are changes reviewed, policy-gated, audited, reversible and bounded? |
| Expand (EXP) | Does it find and launch adjacent value? |

The result is a reading for one product, not a leaderboard. Different archetypes have different applicable criteria.

## Use It For

- A baseline before investing in AI-built change, self-improvement or platform work.
- Finding what blocks the next autonomy level.
- Evidence-backed comparison of releases of the same software.
- A remediation sequence after the current state is scored.

## Do Not Use It For

- Security or accessibility conformance.
- General code quality or pull-request review.
- Team delivery performance.
- Roadmap scoring or future-state promises.
- Declaring production readiness from repository evidence alone.

## Host capability check

Use the repository URL or files the user supplied as authorization to inspect that source with available tools. Do not imply this plugin adds GitHub access, a hosted server or a Python runtime. Uploaded repository archives and user-supplied evidence also work. If sources cannot be accessed, request a repository archive or relevant files and record the evidence gap.

Before scoring, confirm that this host can execute Python and access the bundled scripts and references. If so, use the bundled scorer unchanged. If not, gather evidence and explain the rubric, but do not calculate Software Autonomy Levels or AI Readiness by hand. Supply a clearly marked unscored evidence report and an input/command handoff for running the scorer in a Python-capable environment. Never claim a script ran or an assessment passed without actual output.

## Procedure

### 1. Establish scope

Record the software name, repository paths, branches or immutable tips, assessment date, scope and archetype.

Scope must include every first-party repository that implements the product's core behaviour (companion optimisers, agent servers, automation services, evaluation harnesses). Read the architecture docs: if the named repository delegates capabilities elsewhere, add that repository or record where they live.

Read `references/archetypes.md` before choosing among `configurable-application-platform`, `agent-runtime`, `developer-platform`, `focused-application` and `other`.

Assess only repositories and documents the user supplied or authorised. Never mutate the target repository. The supplied target is authorized by the assessment request; ask before accessing additional remote sources outside that scope.

### 2. Create the input

Generate an input file with the skill's own scripts (paths are relative to this skill's directory, not the target repository). Write it outside the target repository and never overwrite an earlier assessment:

```bash
python3 <skill-dir>/scripts/init_scores.py --product "<software name>" --archetype <type> --source "<repo and tip>" --out <outside-target>/<product>-<date>.json
```

### 3. Declare the scope facts

Set each of the twelve facts in `references/rubric.md` (persistent data, schema changes, multi-tenant, hosted service, machine actions, agent mutations, evolution auto-apply, definition change path, code release path, and the AI facts `ai_features`, `ai_data_access`, `ai_actions`) to true or false with evidence, for the default configuration. Where a shipped opt-in setting turns an AI fact on, record `available_value: true`. They decide which criteria and critical controls apply, including which rollback each change path needs. A wrongly declared fact is a finding, not a shortcut.

### 4. Gather evidence

Follow `references/evidence-plan.md`. Read the target at the named branch or tip. For any product that claims to learn or self-improve, work through the self-modification checklist in `references/archetypes.md` before scoring the Learn and Vet criteria. For parallel exploration, give each explorer only the relevant capability, and require file paths, short evidence summaries, who can make the change, whether a deployment is required, and whether tests exercise the capability.

Evidence grades:

- `A`: verified in code at the named tip.
- `B`: verified in first-party documentation, audit material or configuration supplied for the assessment.
- `C`: inferred from secondary material or product knowledge; scores are capped at 2.

`not_evidenced` is uncertainty, not proof of absence. Record where the assessment searched.

### 5. Score

Use the anchored levels in `references/rubric.md`. Between two levels, score the lower and record the higher as `alt_score` (always `score + 1`). Score what exists now and in the default configuration; record shipped opt-in settings as `available_score`. Learning, intake, implementation-lane and expansion criteria credit changes to the product's own behaviour, not to other software it works on, and count repository tooling only when it is a supported first-party evolution system (rubric rule 12).

If `ai_features` is true in either reading, score the eight AIR checks and add an `ai` reading to each of the 13 reused criteria (MAL-19, MAL-20, DEL-01, DEL-04, LRN-05 to LRN-08, EXP-05, GOV-09 to GOV-11, ARC-08), scored only on AI-backed behaviour. Missing AI behaviour scores 0, not `not_applicable`.

For architecture and critical-control criteria read at 3 or more, record `facets`: implemented, tested and operated. For ARC-08, ARC-09 and GOV-05 at 3 or more, record an `inventory` with a level per surface.

```bash
python3 <skill-dir>/scripts/score.py <file>.json
```

The scorer validates coverage, scope facts, evidence, statuses, archetype exclusions, facets, inventories, caps and deductions, then computes the loop levels, critical controls, blockers, profile, ranges and opt-in readings. Never compute levels by hand.

### 6. Verify

Re-read primary evidence for every criterion at 3 or 4 and for every critical control. For every assessed zero, cite the inspected surface. For every `not_evidenced`, state the search scope. Treat repository evidence as mechanism evidence, not proof of usability, adoption, hosted-edition parity or business impact.

### 7. Prescribe

```bash
python3 <skill-dir>/scripts/score.py <file>.json --prescribe --target 3
```

The plan starts with what blocks the next autonomy level, then orders criterion moves by prerequisites. Projected scores are ceilings if every move lands, not forecasts. Re-estimate every size for the assessed software.

### 8. Report

Use `references/scorecard-template.md`. Report:

- the headline SAL, each loop's level and the part that holds it there;
- how far AI itself drives each loop (the AI-driven levels) and what AI needs for its next level;
- critical controls and which fail;
- what blocks the next level of each loop;
- the profile with ranges, the opt-in reading and the scope facts;
- AI Readiness (level, dimensions, gates) and the descriptive, non-headline AI Capability Footprint, kept separate from SAL;
- coverage, uncertainty, exclusions and every cap or deduction;
- repository and operational evidence limits;
- the remediation sequence when requested.

Never call a product "self-evolving" from a level alone; L3 and above are readiness readings that still need operational validation. For comparisons across products, show ranges and run a second independent pass on the Learn, Vet and Expand criteria.

## Public-Use Guardrails

- The framework contains no private product examples or employer-specific terminology. The field test in the source repository scores public open-source code only.
- Generated reports may name only the software the user explicitly asked to assess.
- Never include confidential repository excerpts, credentials, customer names, tenant identifiers or internal URLs in a shared report.
- Do not publish comparative scores without giving maintainers a chance to correct factual evidence and without disclosing evidence limitations.
- Preserve prior inputs for reassessments; never overwrite historical evidence.

## Files

- `references/rubric.md`: criteria, anchored levels, scope facts, loop conditions and the scoring model.
- `references/archetypes.md`: applicability and interpretation guidance.
- `references/evidence-plan.md`: evidence collection instructions.
- `references/remediation.md`: prerequisite-aware moves to levels 3 and 4.
- `references/scorecard-template.md`: report structure.
- Design and decisions for each version: `spec/` in the source repository, https://github.com/harsh51191/evolvable-software.
- `scripts/init_scores.py`: input template generator.
- `scripts/score.py`: validator, scorer and prescriber.
- Scorer tests and the 11-product field test: `tests/` and `assessments/` in the source repository.
