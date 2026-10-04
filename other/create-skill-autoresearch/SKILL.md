---
name: create-skill-autoresearch
version: 0.2.1
license: MIT
description: >-
  Factory skill that creates production-grade, benchmarked, autonomously improved,
  and verified agent skills. Orchestrates a 5-phase pipeline: interview the
  user to discover purpose and gold standards, research domain materials with parallel
  subagents, draft the skill with a design-first approach, invoke autoresearch to
  iterate against gold-standard-driven LLM-as-judge evaluation, and verify quality
  through multi-agent consensus with a devil's advocate. Use when building a new
  skill, creating a skill from existing materials, or upgrading a skill to
  production quality with benchmarking and autonomous improvement.
---

# Create Skill via Autoresearch Factory

A factory for forging production-grade agent skills through gold-standard-driven autoresearch, multi-agent verification, and structured consensus.

The factory orchestrates 4 agent roles through 5 phases:

| Phase | What Happens | Agent Role |
|-------|-------------|------------|
| 1. Interview | Discover purpose, gold standards, scope | ORCHESTRATOR |
| 2. Research | Study domain materials, build dossier, propose rubric | RESEARCHER (N parallel) |
| 3. Draft | Design structure, generate SKILL.md, measure baseline | BUILDER |
| 4. Autoresearch | Iterate skill against gold standards (LLM-as-judge, or an objective real-world metric for procedural skills — see 3.4) | BUILDER + autoresearch skill |
| 5. Verify | Premortem, panel scoring, consensus, ship/iterate | PANEL (3 subagents) |

Key constraint: BUILDER and PANEL never share context. Panel receives only the skill output, gold standards, and rubric -- no bias from the building process.

## Relation to create-skill

This factory **extends** the official single-pass skill creators (Anthropic's Skills best-practices and `skill-creator`; Cursor's `create-skill`) rather than replacing them. It adds what a one-shot generator cannot: a research dossier, gold-standard benchmarking, an autonomous improvement loop, and independent multi-agent verification. The skills it produces follow the same official conventions -- see [references/skill-authoring-best-practices.md](references/skill-authoring-best-practices.md).

## Companion skills

The factory orchestrates these sibling skills at runtime: **autoresearch** (Phase 4 improvement loop), **premortem** (Phase 5 risk pass), and **handoff** (cross-session continuity); the Phase 5 panel/consensus design draws on **llm-council**. In this harness they are vendored under `.agents/skills/`. If you install this skill standalone, install those alongside it. The factory's craft layer ([references/skill-craft-principles.md](references/skill-craft-principles.md)) is distilled from **writing-great-skills** ([mattpocock/skills](https://github.com/mattpocock/skills), MIT), which the harness vendors under `.agents/skills/`. Phase 5 will delegate to **tribunal** when it is installed (see 5.2).

---

## Phase 1: Interview

Discover what the user needs through structured questions. Do not assume -- ask. Ask them one topic at a
time and record the answers; the exact question wording and follow-ups are in
[references/pipeline-phases.md](references/pipeline-phases.md).

### 1.1 - 1.5 What to discover

| Topic | Ask about | Record |
|-------|-----------|--------|
| **Purpose and domain** | the problem it solves, the domain, which agent will use it, what "success" looks like | `SKILL_PURPOSE`, `DOMAIN`, `TARGET_USER`, `SUCCESS_CRITERIA` |
| **Gold standards** | examples of "what good looks like" — input/output pairs, reference artifacts, previously solved problems, existing quality reports; where they are, what format, how many | `GOLD_STANDARD_SOURCE`, `GOLD_STANDARD_FORMAT`, `GOLD_STANDARD_COUNT` |
| **Study materials** | docs, existing code, transcripts, design docs, reference implementations, specs, style guides | `STUDY_MATERIALS` |
| **Scope and constraints** | conventions to follow, skills to integrate with, anti-patterns to avoid, target line count (default < 500), and invocation mode — model-invoked (pays permanent context load) or user-invoked (`disable-model-invocation: true`) | `CONSTRAINTS`, `INTEGRATION_SKILLS`, `ANTI_PATTERNS`, `INVOCATION_MODE` |
| **Existing skill** | is there one for this domain already? If so it is both a study material and a baseline — research it, measure it against the rubric, improve it rather than starting over | `EXISTING_SKILL`, and set mode to **upgrade** rather than **greenfield** |

Minimum 3 gold standards. Fewer is a risk -- warn the user and offer alternatives: create synthetic
examples, or find additional reference materials.

### 1.6 Confirm and Create Workspace

Summarize all parameters in a table. Ask the user to confirm.

Once confirmed, create the build workspace at `builds/<skill-name>/` with three ownership zones:
- `input/` -- where the user drops gold standards + study materials, in **any** structure
- `work/` -- everything the factory generates: `manifest.yaml`, `research/`, `evaluation/`, `experiments/`, `handoffs/`
- `output/<skill-name>/` -- the finished skill (`SKILL.md` + `references/`) in its own named dir, publish-ready

Do **not** ask the user to hand-author a manifest. Scan whatever is in `input/`, classify each item as a gold standard (exemplar input/output pair or reference artifact) vs a study material, and write your derived index to `work/manifest.yaml` with train/validation/test tags. Present the derived manifest for the user to confirm or correct. See [references/pipeline-phases.md](references/pipeline-phases.md) for intake formats and the manifest schema.

---

## Phase 2: Research

Study the domain thoroughly before writing any skill code.

### 2.1 Spawn Researcher Subagents

Cluster study materials by relatedness, then launch one `explore` subagent per cluster. Clustering heuristic:
- **By source type**: existing skills in one cluster, gold standard outputs in another, planning docs in a third
- **By subtopic**: if materials cover distinct areas (e.g., backend vs frontend), split by area
- **Cap at 5-7 clusters**: more than 7 creates synthesis overhead without proportional depth gain
- **Minimum 2 clusters**: a single cluster means no parallelism benefit

Each subagent:
1. Reads the assigned material deeply
2. Distills findings into a research note in `work/research/`
3. Identifies patterns, conventions, and quality signals relevant to the skill

Naming: `work/research/01-<topic>.md`, `work/research/02-<topic>.md`, etc.

### 2.2 Synthesize Research

After all researchers complete, synthesize findings into `work/research/00-synthesis.md`:
- Cross-cutting patterns
- Key conventions the skill must follow
- Quality signals that distinguish good from bad output
- Potential rubric dimensions

### 2.3 Propose Rubric

Based on research, draft `work/evaluation/rubric.yaml`:

```yaml
name: <skill-name>-rubric
dimensions:
  - name: <dimension>
    weight: <0.0-1.0>
    scale: "1-10"
    criteria: "<what this dimension measures>"
  # ... 5-10 dimensions
target_score: 0.85
max_iterations: 20
plateau_window: 5
```

Always include these universal dimensions (adjust weights per domain):
- **correctness**: Instructions are technically accurate and executable
- **completeness**: All necessary sections and edge cases covered
- **clarity**: A naive agent can follow without ambiguity
- **consistency**: Aligns with existing codebase conventions
- **predictability**: Drives the same process every run -- completion criteria checkable and exhaustive, no vague gates, no no-op lines (see [references/skill-craft-principles.md](references/skill-craft-principles.md))

Add 3-5 domain-specific dimensions from the research synthesis (5-10 dimensions total).

Present the rubric to the user for review. Iterate until confirmed.

See [references/rubric-templates.md](references/rubric-templates.md) for templates.

---

## Phase 3: Draft

Design before writing. Write before measuring.

### 3.1 Design Document

Create `work/experiments/DESIGN.md` with:
- Skill name and description (following create-skill conventions)
- Structural decisions: section count, reference file split, progressive disclosure plan
- Invocation mode, information-hierarchy plan (steps vs reference; inline vs disclosed,
  licensed by branching), and candidate leading words -- see [references/skill-craft-principles.md](references/skill-craft-principles.md)
- Integration points with other skills
- Key terminology and voice decisions

### 3.2 Grill the Design

Before writing any skill code, challenge the design adversarially:
- What would make this skill fail in practice?
- Are the structural decisions justified or assumed?
- Does the design match what the gold standards demonstrate?
- Are there simpler alternatives?

Present concerns to the user. Iterate until the design survives scrutiny.

### 3.3 Generate SKILL.md Draft

Following the design and the official skill-authoring rules (see [references/skill-authoring-best-practices.md](references/skill-authoring-best-practices.md)), run this **pre-flight checklist** before writing -- these are hard constraints, not preferences:
- `name`: <= 64 chars, lowercase/numbers/hyphens only, **no reserved words `anthropic`/`claude`**; descriptive kebab-case, matching the naming of the set it ships with
- `description`: <= 1024 chars, **third person**, states both WHAT it does and WHEN to use it
- Body < 500 lines; progressive disclosure (essentials in SKILL.md, detail in `references/`)
- File references **one level deep** only; a table of contents for any reference file > 100 lines
- Concrete examples over abstract instructions; consistent terminology; forward-slash paths
- Description craft: leading word front-loaded, one trigger per branch, no synonym padding;
  user-invoked skills get a one-line human-facing description ([references/skill-craft-principles.md](references/skill-craft-principles.md))

Write the draft to `output/<skill-name>/SKILL.md` (reference files in `output/<skill-name>/references/`).

### 3.4 Build Evaluation Script

Create `work/evaluation/evaluate.sh` that:
1. Takes a gold standard test case path as argument
2. Extracts the input from the test case
3. Invokes the skill on the input -- since skills are markdown instructions (not
   executables), this means calling an LLM with the SKILL.md as a system prompt
   and the test case input as the user message. Use `curl` to an OpenAI-compatible
   API, or a language-specific SDK. Capture the LLM's output.
4. Compares the output to the gold standard reference using an LLM-as-judge
5. Emits `METRIC <dimension>=<score>` lines to stdout
6. Emits `METRIC overall_score=<weighted_average>` as the primary metric

See `self-test/evaluation/evaluate.sh` in the [agent-skills-harness](https://github.com/a-tokyo/agent-skills-harness) repo for a complete reference implementation.

**`overall_score` steers Phase 4; it is not the shipping evidence.** It measures absolute output quality
against gold standards, with no bare-model comparison in it, so it cannot answer "does this skill help".
That question needs a **same-model uplift benchmark** -- the same model on identical tasks with the skill
and without -- built before ship and reported with its honest negatives. Reading effectiveness off
`overall_score` is the most common way to conclude a working skill is useless. Standard, arms, sample
sizes and the retry-parity rule: [references/benchmark-standard.md](references/benchmark-standard.md).

The LLM judge should:
- Use structured JSON output for per-dimension scoring
- Score each dimension independently (prevent halo effects)
- Require evidence (verbatim quotes) for extreme scores
- Use a different model family from the builder when possible

**Deterministic vs LLM-judge evaluation**: Not every dimension needs an LLM judge. Prefer deterministic checks where possible:
- Line count, frontmatter validation, link integrity → shell/grep checks
- Pattern coverage (does output mention X?) → regex matching
- Structural conformance → programmatic validation

Use LLM-as-judge only for dimensions that require subjective judgment (clarity, quality match, curation). Mix both in `evaluate.sh`: deterministic checks emit METRIC lines directly, LLM judges handle the rest. If no LLM API is available, fall back to deterministic-only scoring and log a warning.

**Procedural / agentic skills (prefer this when it applies)**: some skills don't *generate* an artifact in
one shot — they instruct an agent to perform a multi-step task on a real artifact (migrate a framework
version, refactor a module, scaffold infra). For those, the single-call harness above is the wrong
instrument: evaluate by **execution against a real artifact with an objective real-world metric**, where
the artifact's own ground truth replaces the judge. Full method — baseline capture, reset-then-fresh-agent
orchestration, and why a fresh agent per run is the point — in
[references/benchmark-standard.md](references/benchmark-standard.md).

For **multi-judge evaluation** (recommended when budget allows):
- Run 2-3 different LLM models as judges on the same output
- Average their per-dimension scores for a more robust signal
- Track per-judge variance -- high variance on a dimension indicates the criteria may be ambiguous
- Configure judges in `work/evaluation/judges.yaml`:
  ```yaml
  judges:
    - model: "<model-1>"
      weight: 1.0
    - model: "<model-2>"
      weight: 1.0
  aggregation: "mean"
  ```

Optionally create `work/evaluation/evaluate-checks.sh` for correctness gates.

### 3.5 Measure Baseline

Run `evaluate.sh` on the test cases with the initial draft.
Record baseline scores. This is experiment 0.

Report to the user:
> Baseline established: **overall_score = [value]**
> Dimensions: [per-dimension breakdown]

---

## Phase 4: Autoresearch

Invoke the **autoresearch skill** to iterate the skill draft against the evaluation rubric.

### 4.1 Configure Autoresearch

Provide these parameters to the autoresearch skill. All paths are relative to the
build workspace root (`builds/<skill-name>/`), which is the autoresearch
working directory. Autoresearch session files (`.md`, `.jsonl`, `.tsv`, `run.log`)
are created at the workspace root during the active session, then archived to
`work/experiments/` when the session ends or on handoff.

- **Goal**: Improve `<skill-name>` quality as measured by `overall_score` (LLM-as-judge against gold standards, or the objective real-world metric for procedural skills — see 3.4)
- **Metric command**: `./work/evaluation/evaluate.sh` (relative to workspace root)
- **Primary metric**: `overall_score`
- **Direction**: `higher_is_better`
- **In-scope files**: `output/<skill-name>/SKILL.md`, `output/<skill-name>/references/*`
- **Out-of-scope files**: `input/`, `work/`
- **Constraints**: Must follow the official skill-authoring rules (< 500 lines, frontmatter format -- see 3.3)
- **Budget**: From rubric config `max_iterations` (default 20)
- **Checks**: If `work/evaluation/evaluate-checks.sh` exists, create `autoresearch.checks.sh` at workspace root that calls it (autoresearch skill expects this name)

### 4.2 Data Split

If gold standards count >= 10:
- **70% training**: Used during each autoresearch experiment
- **20% validation**: Checked adaptively to detect overfitting (see below)
- **10% test**: Held out entirely until Phase 5 verification

If gold standards count 3-9:
- **Leave-one-out rotation**: Each experiment evaluates against all but one, rotating which is held out

Record the split in `work/evaluation/data-split.yaml`.

**Cost awareness for large sets (100+ gold standards)**: Each LLM-as-judge call costs real money. With 70 training cases at ~$0.50/call, that's ~$35/experiment. Mitigate with a sampling strategy: evaluate against a random sample of training cases per experiment (e.g., 10-15), rotating the sample. Run the full training set only when validating kept experiments or at phase boundaries.

**Overfitting detection**: run `evaluate.sh` against the validation set adaptively — after every **kept**
experiment, after a **plateau** (is the ceiling real or training-specific?), and when the training score
jumps by more than 0.05. If training improves while validation drops by more than 0.05, warn the user
that recent changes may be over-fitted and offer to generalize them, revert to the last
validation-stable commit, or widen rubric criteria that have become too narrow. Log validation checks in
`autoresearch.jsonl` as `"type": "validation_check"`.

**Overfitting detection for leave-one-out** (< 10 gold standards): with no fixed validation set, track
per-case variance — if it widens while the mean improves, the skill is specializing for some cases at
others' expense. Flag when any single case drops > 1.0 point while others improve.

### 4.3 Let Autoresearch Run

The autoresearch skill handles the loop:
- THINK-EDIT-COMMIT-RUN-MEASURE-DECIDE-LOG cycle (commit-first git model)
- METRIC protocol for measurement
- ASI fields for structured memory
- Plateau detection
- Results logging to `autoresearch.jsonl` and `results.tsv`

The factory adds to the autoresearch ideas backlog (`autoresearch.ideas.md`):
- Ideas from research synthesis
- Per-dimension improvement strategies from the rubric
- Patterns observed in gold standards that aren't yet reflected in the skill
- Craft passes from [references/skill-craft-principles.md](references/skill-craft-principles.md): leading-word hunt, no-op/duplication/sediment prune, disclosure rebalance

**Ending the loop is the factory's call, not the loop's.** The autoresearch skill treats a plateau as
advisory and continues while budget remains, so a `target_score` the task cannot reach burns the whole
budget and reports "exit criteria not met" -- forever. Override that:

- **A confidence-qualified plateau is terminal.** If the plateau sits within judge variance (~0.2-0.3 on
  a 1-10 scale, below which gains are not measurable), stop and carry best-so-far into Phase 5.
- **Below target is a verdict, not a failure** -- Phase 5.4 grades it (SHIP WITH CAVEATS at or above
  `target_score - 0.10`). Honour `baseline_lock` in `state.yaml` the same way, logging the real target
  in the ideas backlog.
- Never ask for repeated re-runs toward an unreachable number: report the ceiling, name the binding
  constraint (target too high, or gains below judge variance), and proceed.

### 4.4 Monitor and Handoff

If the autoresearch session exceeds context limits or the experiment budget:
1. Invoke the **handoff skill** to generate `work/handoffs/HANDOFF-<session>.md`
2. Write `work/handoffs/state.yaml` with structured resume state — phase, session counter, best score
   and commit, experiments run, remaining budget, validation score, top concerns, blocked dimensions,
   and `baseline_lock` (full schema in [references/pipeline-phases.md](references/pipeline-phases.md))
3. The next session reads `state.yaml` to resume from the correct phase

### 4.5 Resume Protocol

When `work/handoffs/state.yaml` exists: read it for the current phase, read the most recent
`work/handoffs/HANDOFF-*.md` for context, resume at the recorded phase (re-confirm parameters on
**interview**; synthesize if the dossier is incomplete on **research**; measure a baseline if the draft
exists on **draft**; read `autoresearch.jsonl` for ASI history and continue with the remaining budget on
**autoresearch**; re-run the panel if the last verdict was ITERATE on **verify**), then bump the session
number. Per-phase detail: [references/pipeline-phases.md](references/pipeline-phases.md).

---

## Phase 5: Verify

Independent verification by agents that did NOT participate in building. The context wall between BUILDER and PANEL is critical -- it prevents bias from the building process.

### 5.1 Premortem

Invoke the **premortem skill** on the skill artifact. Feed identified risks into the panel evaluation as additional test scenarios, including the five craft failure modes (premature completion, duplication, sediment, sprawl, no-op) as required probes.

### 5.2 Panel Evaluation

Spawn 3 independent verifier subagents **in parallel**. Each receives ONLY:
- The skill SKILL.md and references
- The gold standards
- The rubric
- The premortem risks

They do NOT receive: research notes, experiment logs, builder context, or ASI.

**Panel roles:**

| Role | Focus | Bias |
|------|-------|------|
| Verifier-A (Quality) | Correctness, completeness, clarity, spec adherence | Neutral |
| Verifier-B (Utility) | Real-world usability, edge cases, developer experience | Neutral |
| Devil's Advocate | Failure modes (incl. the five craft failure modes), hidden assumptions, missing constraints | Explicitly adversarial |

Each panel member scores every rubric dimension independently with:
- Score (per rubric scale)
- Confidence (0.0-1.0)
- Evidence (verbatim quote from artifact)

Use a **different model family** for the panel when possible (e.g., if the builder used one model, use a different one for verifiers).

**One agent per role — this is the mechanism, not a formality.** A single agent simulating the panel in
one context scores at its own solo floor (0.62 measured, vs 0.75 for separate agents): shared context
means shared blind spots. The ORCHESTRATOR dispatches and adjudicates; it scores nothing. Without
parallel agents, run each role as its own fresh-context session and label the result "single-context (no
independence)". **Grep every verdict-driving citation** against the artifact before consensus math; one
that cannot be found verbatim discards its finding.

See [references/pipeline-phases.md](references/pipeline-phases.md) for panel prompt templates.

**If the `tribunal` skill is available, delegate Phase 5 to it** — this pattern generalized and separately
benchmarked. Pass the BUILDER's output as the artifact and the Phase-2.3 rubric (frozen before the Phase-3
draft) as the criteria; its orchestrator must not be the agent that built the skill. Otherwise run the
inline panel — a standalone install must not depend on a second skill.

### 5.3 Consensus Protocol

After collecting all 3 scoring outputs:

1. **Agreement check**: all scores within 1 point on every dimension → weighted average, done
2. **Synthesis round** (any dimension spread >= 2, or DA scores a dimension at 1): each member writes a rationale on the disputed dimensions (max 500 words); rationales are **anonymized** and shared simultaneously; a member may revise with written justification, or must rebut the strongest opposing argument to keep their score
3. **Resolution**: converged within 1 point → weighted average; 2-of-3 majority → majority adopted and the dissent logged as a minority report in `work/experiments/craft-decisions.md`; **deadlock → escalate to user**
4. **DA escalation**: the DA may write `ESCALATE: <reason>` for a critical concern the majority dismisses, which surfaces it to the user rather than averaging it away

See [references/consensus-protocol.md](references/consensus-protocol.md) for the full protocol, anti-patterns, and research basis.

### 5.4 Ship or Iterate

| Final Score | Action |
|-------------|--------|
| >= target_score AND no dimension blocked | **SHIP** -- copy skill to final location |
| >= target_score - 0.10 | **SHIP WITH CAVEATS** -- log concerns, proceed |
| < target_score - 0.10 | **ITERATE** -- feed panel feedback to autoresearch |
| Any dimension < 3/10 by majority | **BLOCK** -- address blocking concern first |

If ITERATE:
1. Extract top concerns from each panel member
2. Extract failure scenarios from the Devil's Advocate
3. Add specific improvement hypotheses to `autoresearch.ideas.md`
4. Log panel scores and rationales in `work/experiments/craft-decisions.md`
5. Return to Phase 4 with structured feedback

On SHIP, write `BENCHMARK.md` at the build root (the panel's final scores and verdict), then follow
[references/publishing.md](references/publishing.md) — shipping is a registration checklist, not a file
copy, and a version that disagrees with its registry entry installs the wrong thing. Prove the skill
earns its place with an uplift benchmark: [references/benchmark-standard.md](references/benchmark-standard.md).

---

## Output Structure

Each build lives in one self-contained folder, `builds/<skill-name>/`, with three zones:

```
builds/<skill-name>/
  input/                  # HUMAN: gold standards + study materials (any structure)
  work/                   # FACTORY: process artifacts (not shipped)
    manifest.yaml         #   derived gold-standard index    <- yours to correct
    research/             #   study notes and dossier
    evaluation/           #   rubric.yaml (exit criteria), evaluate.sh, judges.yaml, data-split.yaml
    experiments/          #   results.tsv, autoresearch.jsonl, run.log, DESIGN.md, craft-decisions.md
    handoffs/             #   cross-session context (state.yaml, HANDOFF-*.md)
  output/                 # FACTORY: the finished, publish-ready skill
    <skill-name>/         #   the skill in its own named dir
      SKILL.md
      README.md           #   optional, ships on install: what it does, method, results
      references/         #   if needed
      scripts/            #   if needed (NOT evaluation scripts)
      assets/             #   if needed
  BENCHMARK.md            # FACTORY: final panel scores + verdict (Phase 5)
```

`work/` is generated, but four files are the human's to correct at phase boundaries: `manifest.yaml`,
`evaluation/rubric.yaml` (the exit criteria), `evaluation/judges.yaml`, `evaluation/data-split.yaml`.
Never write a credential into any of them — `work/` is often committed inside a real project repo.

Only `output/<skill-name>/` ships; its uplift benchmark belongs **outside** the skill dir, at
`benchmarks/<skill-name>/`. To publish: [references/publishing.md](references/publishing.md).

---

## Handoff Rules

Write a handoff when any of these occur:
- Context window approaching limit (high turn count)
- Experiment budget for current session exhausted
- Phase transition (research → draft, draft → autoresearch, etc.)
- User explicitly requests

Each handoff produces:
1. `work/handoffs/state.yaml` -- structured state for automatic resume
2. `work/handoffs/HANDOFF-<label>.md` -- rich context for human readability

To resume: read `state.yaml`, determine current phase, load relevant context, continue.
