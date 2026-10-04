---
name: create-skill
allowed-tools:
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Read
  - Skill
  - Task
  - Write
version: 1.2.5
author: "Ashay Kubal @ Qball Inc."
description: Generates Claude Code skills from requirements using adaptive interview, complexity classification, and iterative validation. Use when creating new skills, scaffolding skill structure, or generating skills with sub-agent orchestration.
argument-hint: "<purpose-as-prompt> | --doc <path-to-requirements-file> | --from-template <archetype> <skill-name>"
skills:
  - subagent-prompting
---

# Create Skill

Generates a complete Claude Code skill from a description or requirements document. Conducts an adaptive interview to understand the skill's purpose, classifies it into one of 7 archetypes (Generator, Tool Wrapper, Pipeline, Research, Script-driven, Reviewer, Inversion), surfaces candidate sub-patterns for the chosen archetype, spawns a Sonnet sub-agent to generate the files, validates with anthropic-validator, and presents the scaffold with architectural decisions.

---

## When to Use This Skill

**Load this skill when the user request matches ANY of these patterns:**

| Trigger Pattern | Example User Request |
|-----------------|---------------------|
| Skill creation | "Create a new skill", "Make a skill for X" |
| Scaffolding | "Scaffold a skill", "Set up a new skill" |
| Generation | "Generate a skill that does X" |
| Skill design | "Design a skill for X", "I need a skill that does X" |

**DO NOT use for:**
- Editing existing skills (edit directly)
- Creating standalone sub-agents (use `create-subagent`)
- Debugging skill issues (use `issue-debugging`)
- Validating existing skills (use `anthropic-validator`)

---

## Dependencies

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Decision framework** | `references/decision-framework.md` | **REQUIRED** | Load at Stage 0 for interview + classification |
| **Content guidance** | `references/content-guidance.md` | **REQUIRED** | Include in Stage 2 generator prompt |
| **Skill templates** | `references/template-*.md` | **REQUIRED** | Load the matching template at Stage 2 |
| **Agent template** | `references/agent-template.md` | **REQUIRED** | Include in Stage 2 prompt when archetype = Pipeline |
| **Agent conventions** | `references/agent-conventions.md` | **REQUIRED** | Include in Stage 2 prompt when archetype = Pipeline |
| **Diagnostic template** | `templates/diagnostic-output.yaml` | **REQUIRED** | Use at Stage 6 |
| **Subagent prompting** | `subagent-prompting` skill | **REQUIRED** | Load at Stage 0 for 4-part prompt template |
| **Eval shape** | `references/eval-shape.md` | **REQUIRED** when scaffolding `evals/` data | Schema for `evals.json` / `triggers.json` / `compliance.json` (Layer 1 DATA) |
| **Eval scaffolding** | `references/eval-scaffolding.md` | **REQUIRED** | Per-archetype emission guide for Stage 2 — defines default `grading_mode`, assertion templates, sub-pattern × eval impact, placeholder substitution markers |
| **Scripts conventions** | `references/scripts-conventions.md` | **REQUIRED** when `bundles_scripts = true` (Stage 1) | Per-skill `scripts/` directory invocation convention (`${CLAUDE_PLUGIN_ROOT}` pattern), Justfile recipe pattern, bun runtime prerequisite |
| **Eval grader agent** | `agents/skill-eval-grader.md` | Bundled (no external load) | `scripts/grade.ts` returns `SKIPPED` for fuzzy assertions and emits a manual-invoke directive pointing at this agent. The orchestrator (or a future automation step) invokes the grader against `evidence_paths` to complete grading. |
| **Eval comparator agent** | `agents/skill-eval-comparator.md` | Bundled (no external load) | Blind A/B comparison of two grading runs. Invoked manually with two `grading-<timestamp>.json` paths; not auto-spawned by `grade.ts`. |

**Fallback behavior:**
- If a template file is missing: Use the closest available template, note mismatch in diagnostics
- If content-guidance is missing: Proceed without it, note in diagnostics (output quality will be lower)

---

## Runtime Prerequisites

The eval framework (Layer 2 infrastructure shipped in `scripts/run-loop.ts` + `scripts/grade.ts`) requires the **`bun`** runtime on PATH. Invocation via `just eval-skill <path>`.

**Interim contract** (until P10.11 ships): users must install bun manually. See [bun.sh/install](https://bun.sh/install). Bulwark's scaffold/init flow does **not** auto-install bun yet — formal installer scoped as P10.11 (`plans/task-briefs/P10.11-bun-runtime-installer.md`).

If you are scaffolding a skill into an environment without bun, generated `evals/` data still ships, but `just eval-skill` will fail until bun is installed.

---

## Usage

```
/create-skill <description-or-name>
/create-skill --doc <requirements-document>
/create-skill --from-template <archetype> <skill-name>
```

**Arguments:**
- `<description-or-name>` — Free-text description of the desired skill, or a skill name to start from
- `--doc <path>` — Path to a requirements document. Extracts interview answers from it instead of asking fresh.
- `--from-template <archetype> <skill-name>` — Fast path for experienced authors. Skips the Stage 0 interview and uses archetype defaults. Valid archetypes: `Generator`, `Tool Wrapper`, `Pipeline`, `Research`, `Reviewer`, `Script-driven`, `Inversion`. Stage 1 (classification confirmation), Stage 2 (generation), and Stage 3 (validation) all still run.

**Examples:**
- `/create-skill a skill that audits dependency versions` — Start from description
- `/create-skill --doc plans/task-briefs/P5.4-create-skill.md` — Start from requirements doc
- `/create-skill changelog-generator` — Start from a name
- `/create-skill --from-template Generator slug-from-title` — Skip interview, use Generator defaults

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping.**

This skill uses a 6-stage pipeline. You are the orchestrator. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 0 — Pre-Flight**: Arguments parsed (description, name, --doc, or --from-template)
- [ ] **Stage 0 — Pre-Flight**: Decision framework and content guidance loaded
- [ ] **Stage 0 — Pre-Flight**: If `--from-template <archetype> <name>`: archetype validated against 7-set; interview SKIPPED; defaults loaded
- [ ] **Stage 0 — Pre-Flight**: Else: Adaptive interview conducted (1-2 rounds via AskUserQuestion)
- [ ] **Stage 1 — Classify**: Primary archetype determined per decision-framework.md (1 of 7) + context mode
- [ ] **Stage 1 — Classify**: Candidate sub-patterns for the archetype looked up; default-ON sub-patterns pre-checked
- [ ] **Stage 1 — Classify**: Default `grading_mode` resolved per archetype (objective for Generator/Tool Wrapper/Pipeline/Reviewer/Script-driven; subjective for Research/Inversion); author may override at Stage 1 confirmation
- [ ] **Stage 1 — Classify**: `bundles_scripts` resolved (true for Script-driven canonical; ask follow-up for non-Script-driven archetypes; default false)
- [ ] **Stage 1 — Classify**: Classification (archetype + selected sub-patterns + context + grading_mode + bundles_scripts) presented to user and confirmed via AskUserQuestion
- [ ] **Stage 2 — Generate**: Sonnet sub-agent spawned via Task tool (you do NOT generate the files yourself)
- [ ] **Stage 2 — Generate**: Generated files verified to exist in working directory
- [ ] **Stage 2 — Generate**: `evals/evals.json` and `evals/triggers.json` scaffolded per references/eval-scaffolding.md (always)
- [ ] **Stage 2 — Generate**: `evals/compliance.json` scaffolded if grading_mode = subjective (Research, Inversion, or override)
- [ ] **Stage 2 — Generate**: Sub-pattern × eval impact applied per references/eval-scaffolding.md → Sub-Pattern × Eval Impact
- [ ] **Stage 2 — Generate**: `scripts/.gitkeep` scaffolded if bundles_scripts = true; SKILL.md documents `${CLAUDE_PLUGIN_ROOT}` invocation convention per references/scripts-conventions.md
- [ ] **Stage 2 — Generate**: If Pipeline archetype — sub-agent files generated in {working-directory}/agents/
- [ ] **Stage 3 — Validate**: `just check-description {working-directory}/SKILL.md` invoked via Bash (E.1 description quality gate — exits 1 on multi-line / over-length)
- [ ] **Stage 3 — Validate**: `just check-skill-size {working-directory}/SKILL.md` invoked via Bash (E.3 tiered cap enforcement — exits 1 on hard cap with refactor proposal)
- [ ] **Stage 3 — Validate**: `/anthropic-validator` invoked via Skill tool (manual review is NOT a substitute)
- [ ] **Stage 3 — Validate**: If Pipeline archetype — `/anthropic-validator` invoked on each sub-agent file
- [ ] **Stage 3 — Validate**: Validator output read and findings counted
- [ ] **Stage 3 — Validate**: Manual checks completed (single-line description, no unnecessary files)
- [ ] **Stage 3 — Validate**: Cross-file consistency check completed — if skill bundles `templates/`, `references/`, or `scripts/`, scan SKILL.md for content that mirrors or references those files; verify both sides agree on rules, schemas, character sets, error conditions (per references/content-guidance.md → Cross-File Consistency)
- [ ] **Stage 3 — Validate**: Sub-pattern review soft prompt presented to user IF (sub-patterns selected at Stage 1 > 0) OR (archetype has default-ON sub-patterns that were opted out — Research, Inversion). SKIP entirely for Generator/Tool Wrapper/Reviewer/Script-driven/Pipeline when 0 sub-patterns selected (per references/content-guidance.md → Sub-Pattern Catalog)
- [ ] **Stage 4 — Refine**: If validation found critical/high issues, Sonnet sub-agent spawned to fix (max 2 retries)
- [ ] **Stage 5 — Deploy & Present**: Skill files deployed from working directory to target directory
- [ ] **Stage 5 — Deploy & Present**: If Pipeline archetype — sub-agent files deployed to `.claude/agents/`
- [ ] **Stage 5 — Deploy & Present**: Working directory cleaned up
- [ ] **Stage 5 — Deploy & Present**: Post-generation summary presented with architectural decisions
- [ ] **Stage 5 — Deploy & Present**: If Pipeline archetype — sub-agent permissions communicated
- [ ] **Stage 5 — Deploy & Present**: Next steps communicated (this is a scaffold, not production-ready output)
- [ ] **Stage 6 — Diagnostics**: Diagnostic YAML written to `$PROJECT_DIR/logs/diagnostics/`

---

## Pipeline

```fsharp
// create-skill pipeline
PreFlight(args)                              // Stage 0: Orchestrator — parse input, adaptive interview
|> Classify(interview_answers)               // Stage 1: Orchestrator — three independent decisions
|> Generate(classification, template, examples) // Stage 2: Sonnet sub-agent — produce skill files
|> Validate(generated_output)                // Stage 3: Orchestrator — run anthropic-validator
|> Refine(validator_findings)                // Stage 4: Sonnet sub-agent (conditional, max 2 retries)
|> DeployAndPresent(working_dir, target_dir)  // Stage 5: Orchestrator — deploy to target + post-generation summary
|> Diagnostics()                             // Stage 6: Orchestrator — write YAML
```

---

## Stage Definitions

### Stage 0: Pre-Flight (Orchestrator)

```
Stage 0: Pre-Flight
├── Parse arguments (description, name, --doc path, or --from-template <archetype> <name>)
├── Load references/decision-framework.md
├── Load references/content-guidance.md
├── Load subagent-prompting skill
├── If --from-template provided (E.2 escape hatch):
│   ├── Validate <archetype> against the 7-set (Generator, Tool Wrapper, Pipeline,
│   │   Research, Reviewer, Script-driven, Inversion). Case-insensitive match;
│   │   normalize to canonical form
│   ├── If invalid: print valid options + exit (do NOT scaffold)
│   ├── Skip interview entirely
│   ├── Load classification with archetype defaults:
│   │   ├── primary_archetype = <archetype>
│   │   ├── selected_sub_patterns = default-ON only (Research → reviewer-validated;
│   │   │   Inversion → generator-coupled; others → empty)
│   │   ├── context_mode = fork if archetype ∈ {Pipeline, Research} else inline
│   │   ├── grading_mode = archetype default per references/eval-scaffolding.md
│   │   └── bundles_scripts = (archetype = Script-driven)
│   └── Stage 1 still runs (classification confirmation prompt presented to user)
├── Elif --doc provided:
│   ├── Read the requirements document
│   ├── Extract answers to Q1-Q5 from the document
│   └── Present extracted answers to user for confirmation via AskUserQuestion
├── If no --doc and no --from-template:
│   └── AskUserQuestion: Present all 5 core questions from decision-framework.md
│       ├── Q1: What does this skill do? (2-3 concrete invocation examples)
│       ├── Q2: Primary action? (Audit / Create / Document / Orchestrate / Wrap script — routes to archetype)
│       ├── Q3: If creating: CLI/state inputs OR AskUserQuestion-driven? (Generator vs Inversion)
│       ├── Q4: If orchestrating: sequential stages OR parallel viewpoints? (Pipeline vs Research)
│       └── Q5: Needs conversation history, or can run in isolation? (context: inline vs fork)
├── If sub-pattern disambiguation needed (Round 2):
│   └── AskUserQuestion: Follow-up questions per decision-framework.md
│       ├── Q6: Reviewer sub-pattern? (standalone / pipeline-stage / multi-source)
│       ├── Q7: Generator sub-pattern? (single-template / multi-template / configuration-emitting)
│       ├── Q8: Tool Wrapper sub-pattern? (context-injected / schema-convention / methodology / pattern-catalog / curated-data-library)
│       ├── Q9: Pipeline sub-pattern? (reviewer-orchestrating / research-orchestrating / generator-orchestrating)
│       ├── Q10: Research — reviewer-validated default ON; opt out?
│       └── Q11: Script-driven — hook-orchestrated?
├── Determine target directory for generated skill
│   └── Default: skills/{skill-name}/ (or user-specified path)
├── Set working directory: tmp/create-skill/{skill-name}/
│   └── All generation and refinement happens here to avoid .claude/ edit approval storms
│       Files are deployed to the target directory only after validation passes (Stage 5)
└── Token budget check (warn if >30% consumed)
```

**Interview behavior**: Maximum 2 AskUserQuestion rounds. Present Q1-Q5 together in round 1. Follow-ups (if needed) in round 2. Do NOT ask questions one at a time.

### Stage 1: Classify (Orchestrator)

Apply the archetype classification from `references/decision-framework.md`:

```
Stage 1: Classify
├── Decision: Primary archetype (1 of 7) — per Decision Tree → Primary Archetype in decision-framework.md
│   ├── Q2 = Audit/score                              → Reviewer
│   ├── Q2 = Document conventions                     → Tool Wrapper
│   ├── Q2 = Wrap external script                     → Script-driven
│   ├── Q2 = Create + Q3 = CLI/state                  → Generator
│   ├── Q2 = Create + Q3 = AskUserQuestion            → Inversion
│   ├── Q2 = Orchestrate + Q4 = sequential            → Pipeline
│   └── Q2 = Orchestrate + Q4 = parallel viewpoints   → Research
├── Decision: Context mode (orthogonal to archetype)
│   ├── Q5 = needs conversation                       → inline (no fork)
│   ├── Q5 = isolation OK + (Pipeline OR Research)    → context: fork (recommended for orchestrators)
│   └── Otherwise                                     → inline (warn if fork requested for non-orchestrator)
├── Lookup: Candidate sub-patterns for chosen archetype (per decision-framework.md → Sub-Pattern Lookup)
│   ├── Default-ON: Research → reviewer-validated; Inversion → generator-coupled
│   └── Pre-check default-ON sub-patterns in user prompt; user may opt out
├── Decision: Default `grading_mode` for evals scaffolding (per references/eval-scaffolding.md → Default grading_mode Per Archetype)
│   ├── objective: Generator, Tool Wrapper, Pipeline, Reviewer, Script-driven
│   ├── subjective: Research, Inversion
│   └── Author may override at the classification confirmation prompt below (rare — typical override is Pipeline → subjective when synthesis-quality grading is wanted)
├── Decision: `bundles_scripts` for scripts/ scaffolding (per references/scripts-conventions.md → When a Skill Bundles Scripts)
│   ├── true: Archetype = Script-driven (canonical — always bundles a script)
│   ├── ask: Archetype ∈ {Generator, Tool Wrapper, Pipeline, Reviewer, Research, Inversion}
│   │   └── AskUserQuestion: "Will this skill bundle executable scripts (TypeScript via bun, or shell scripts)? [Yes / No]"
│   │       └── Answer = bundles_scripts (default No if unanswered or ambiguous)
│   └── If true and archetype ∉ {Script-driven}, note "non-canonical scripts bundling" in diagnostics for review
├── Map archetype → template (1 of 7 from decision-framework.md → Archetype → Template Mapping)
└── Present classification to user via AskUserQuestion:
    ├── "Primary archetype: {archetype} — {one-line reason from Q2}"
    ├── "Template: {template-name}"
    ├── "Context: {inline/fork} — {reason}"
    ├── "Default grading_mode: {objective/subjective} — {reason from archetype default}"
    ├── "Bundles scripts: {Yes/No} — {reason}"
    ├── "Candidate sub-patterns for {archetype}:"
    │   └── For each: "{sub-pattern}: {one-line definition from content-guidance.md → Sub-Pattern Catalog}"
    ├── "Which sub-patterns apply? (Select 0-N — default-ON pre-checked)"
    └── "Proceed with generation? [Yes / Adjust grading_mode / Adjust bundles_scripts / Adjust sub-patterns / Adjust]"
```

**MANDATORY**: Wait for user confirmation before proceeding to Stage 2. If user selects "Adjust", re-classify with their feedback. Selected sub-patterns + final grading_mode are passed to Stage 2 generator as CONSTRAINTS — generator MUST document each selected sub-pattern in the generated SKILL.md and emit eval data per the resolved grading_mode.

### Stage 2: Generate (Sonnet sub-agent)

```
Stage 2: Generate
├── Read the selected template from references/template-{type}.md
├── Construct prompt using 4-part template (GOAL/CONSTRAINTS/CONTEXT/OUTPUT):
│   ├── GOAL: Generate a complete, structurally correct skill matching the
│   │   classification. The skill must activate reliably and instruct clearly.
│   ├── CONSTRAINTS:
│   │   ├── Follow the template structure exactly
│   │   ├── Description MUST be a single line (multi-line breaks discovery)
│   │   ├── Description MUST be ≤250 chars (over-length silently truncates per Issue #881)
│   │   ├── Description MUST use "Use when..." trigger framing
│   │   ├── Frontmatter MUST include `version: 1.0.0` for the new skill (E.4 — semver-flavored;
│   │   │   patch=typo/wording, minor=new feature, major=breaking. Migration guidance in
│   │   │   references/content-guidance.md → "Skill version + migration checklist")
│   │   ├── Frontmatter MUST include `author:` field. Default to `"Ashay Kubal @ Qball Inc."`
│   │   │   for first-party Bulwark generation; prompt the user during interview if
│   │   │   generating in an external repo.
│   │   ├── Include "When to Use" table with ≥3 trigger patterns
│   │   ├── Include "DO NOT use for" section with ≥2 anti-triggers
│   │   ├── MUST include "## Mandatory Execution Checklist (BINDING)" at top of
│   │   │   SKILL.md with SC1-SC3 reference — bottom checklists are advisory and
│   │   │   ignored (see references/content-guidance.md → "Top-of-File Execution
│   │   │   Checklist" pattern)
│   │   ├── Checklist placement: after frontmatter → overview → When-to-Use →
│   │   │   Dependencies → optional Usage, BEFORE Pipeline/Stages body
│   │   ├── If skill has sub-agents: include subagent-prompting in skills: dependency
│   │   ├── Do NOT add unnecessary files (no README, CHANGELOG, LICENSE)
│   │   ├── Do NOT use emojis in generated content
│   │   ├── Keep total SKILL.md under target line count for the archetype:
│   │   │   ├── Tool Wrapper: 150, Generator: 200, Reviewer: 250
│   │   │   ├── Inversion: 350, Pipeline: 400, Research: 400, Script-driven: 400
│   │   │   └── Tiered enforcement (memo D8 amended S107):
│   │   │       ├── 200 lines = Advisory — emit a soft note in return summary suggesting modularization
│   │   │       ├── 500 lines = Strong warn — emit a loud warning recommending split into references/
│   │   │       └── 600 lines = HARD CAP — STOP. Do NOT emit a single SKILL.md exceeding 600 lines.
│   │   │           Return a refactor proposal listing which sections should move to
│   │   │           references/{name}.md or examples/{name}.md, then await user direction.
│   │   ├── Cross-file consistency (memo D11, S107):
│   │   │   If the skill bundles templates/, references/, or scripts/, any rules,
│   │   │   algorithms, schemas, or validation logic in those files MUST agree with rules
│   │   │   stated in SKILL.md. Before returning, scan for cross-file claims (character sets,
│   │   │   error conditions, output formats, validation rules) and confirm both sides agree.
│   │   │   Disagreements are HIGH-severity functional bugs. Canonical example: a slug
│   │   │   algorithm in templates/ that preserves Unicode while SKILL.md validation accepts
│   │   │   only ASCII — both files individually compile clean; together they fail silently
│   │   │   on non-ASCII input. Fix BEFORE returning, do not defer to validation.
│   │   ├── For each selected sub-pattern, include a documented section in the generated SKILL.md:
│   │   │   ├── Quote the canonical definition from references/template-{archetype}.md → ## Common Sub-Patterns
│   │   │   └── Apply the sub-pattern's shape directives (e.g., context-injected → user-invocable: false + hook setup docs)
│   │   ├── Eval scaffolding (Layer 1 DATA — per references/eval-scaffolding.md):
│   │   │   ├── ALWAYS emit {working-directory}/evals/evals.json + {working-directory}/evals/triggers.json
│   │   │   ├── If grading_mode = subjective → ALSO emit {working-directory}/evals/compliance.json
│   │   │   ├── grading_mode follows the archetype default unless explicitly overridden in CONTEXT
│   │   │   ├── Use the matching archetype section in eval-scaffolding.md as the JSON shape
│   │   │   ├── Substitute placeholders (<<SKILL_NAME>>, <<SKILL_PATH>>, <<INVOCATION_EXAMPLE_1>>, etc.)
│   │   │   │   from the classification + interview state — see eval-scaffolding.md → Placeholder Substitution Guide
│   │   │   ├── Seed at least ONE concrete starter test in evals.json from Q1 examples
│   │   │   ├── Seed 3-5 should-trigger and 3-5 should-not-trigger queries in triggers.json from Q1;
│   │   │   │   leave remaining slots as explicit <<TODO>> placeholders for the user
│   │   │   ├── For subjective: seed compliance.json stage_id entries from the SKILL.md pipeline
│   │   │   │   (one stage_id per declared pipeline stage); deterministic evidence preferred
│   │   │   └── Apply sub-pattern × eval impact additions per eval-scaffolding.md → Sub-Pattern × Eval Impact
│   │   └── Scripts scaffolding (per references/scripts-conventions.md):
│   │       ├── If bundles_scripts = true → emit {working-directory}/scripts/.gitkeep (empty file)
│   │       ├── If bundles_scripts = true → SKILL.md MUST document the `${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/`
│   │       │   invocation convention (do NOT use `$CLAUDE_PLUGIN_DIR` — non-existent latent bug source)
│   │       ├── If bundles_scripts = true and any script is TS-via-bun → SKILL.md MUST include a "Runtime Prerequisites" section
│   │       │   noting bun on PATH (cross-link to P10.11 bun installer brief)
│   │       ├── If bundles_scripts = true → SKILL.md MUST include a "Permissions Setup" section
│   │       │   listing required Bash(bun:*), Bash(bash:*), Bash(just:*) entries per scripts-conventions.md
│   │       ├── If bundles_scripts = true and SKILL.md emits Justfile recipe examples → quote `${CLAUDE_PLUGIN_ROOT}`
│   │       │   AND all parameters per SEC-008 (unquoted opens command-injection vectors when invoked from automation)
│   │       └── Do NOT generate concrete script files — only .gitkeep. Script content is author-supplied
│   │           (generate-and-customize contract; refer to existing skills for starter patterns)
│   ├── CONTEXT:
│   │   ├── Classification from Stage 1 (primary archetype + selected sub-patterns + context mode + template + grading_mode + bundles_scripts)
│   │   ├── User's interview answers (concrete examples from Q1)
│   │   ├── Selected template: references/template-{archetype}.md
│   │   ├── Content guidance: references/content-guidance.md (incl. Sub-Pattern Catalog)
│   │   ├── Eval scaffolding guide: references/eval-scaffolding.md (per-archetype evals/ emission)
│   │   ├── Eval schema lock: references/eval-shape.md (when in doubt about field shapes)
│   │   ├── If bundles_scripts = true: references/scripts-conventions.md (scripts/ scaffolding + invocation convention + Justfile recipe pattern + bun runtime prerequisite)
│   │   ├── Selected sub-patterns: explicit list passed from Stage 1 (0-N — generator MUST document each)
│   │   ├── Sub-pattern definitions: references/template-{archetype}.md → ## Common Sub-Patterns
│   │   ├── If Pipeline archetype: references/agent-template.md (sub-agent file structure)
│   │   ├── If Pipeline archetype: references/agent-conventions.md (system-prompt register, frontmatter)
│   │   ├── Instruction: "Read 1-2 existing skills of the same archetype from the
│   │   │   codebase for structural reference (use Glob to find skills/*/SKILL.md)"
│   │   ├── If Pipeline archetype: "Read 1-2 existing agents from .claude/agents/*.md
│   │   │   for sub-agent structural reference"
│   │   ├── Target output directory (final deployment location)
│   │   └── Working directory: tmp/create-skill/{skill-name}/
│   └── OUTPUT:
│       ├── Write SKILL.md to {working-directory}/SKILL.md
│       ├── Write reference files to {working-directory}/references/ (if applicable)
│       ├── Write template files to {working-directory}/templates/ (if applicable)
│       ├── Write script files to {working-directory}/scripts/ (if applicable)
│       ├── Write {working-directory}/evals/evals.json (always — per eval-scaffolding.md archetype section)
│       ├── Write {working-directory}/evals/triggers.json (always — 20-query format)
│       ├── If grading_mode = subjective: Write {working-directory}/evals/compliance.json (stage execution checks)
│       ├── If bundles_scripts = true: Write {working-directory}/scripts/.gitkeep (empty file — preserves directory in git)
│       ├── If Pipeline archetype: Write sub-agent files to {working-directory}/agents/
│       │   ├── One .md file per pipeline stage: {skill-name}-{stage-name}.md
│       │   ├── Each sub-agent follows agent-template.md structure
│       │   ├── Each sub-agent uses system-prompt register (agent-conventions.md)
│       │   └── Orchestrating SKILL.md references sub-agents by Task(subagent_type="{name}")
│       └── Return summary: list of files created with line counts (include evals/* paths)
├── Spawn: Task(description="Generate skill files", subagent_type="general-purpose",
│          model="sonnet", prompt=...)
├── Read generator output (file list + summary)
└── Verify files were created (Glob for {working-directory}/**)
```

### Stage 3: Validate (Orchestrator)

```
Stage 3: Validate
├── PRE-FLIGHT scripts (E.1 + E.3 deterministic gates — run BEFORE anthropic-validator):
│   ├── Bash: `just check-description {working-directory}/SKILL.md`
│   │   ├── Exit 0 → continue
│   │   ├── Exit 1 → BLOCK; route to Stage 4 with the FAIL findings as directives
│   │   └── Exit 2 → infrastructure error; surface to user
│   └── Bash: `just check-skill-size {working-directory}/SKILL.md`
│       ├── Exit 0 → continue (advisory / strong-warn notes captured for Stage 5 summary)
│       └── Exit 1 (HARD CAP) → BLOCK; route to Stage 4 with the refactor proposal as directive
├── FIRST: Invoke /anthropic-validator (this is the PRIMARY validation — NOT optional)
│   ├── Use the Skill tool: Skill(skill="anthropic-validator", args="{working-directory}/")
│   ├── Do NOT substitute manual review for this step
│   └── Do NOT proceed past this node until the Skill tool has been invoked
├── If Pipeline archetype: Also validate each sub-agent file in {working-directory}/agents/
│   └── Run /anthropic-validator on each {skill-name}-{stage-name}.md
├── Read validator output
├── Check for critical/high findings:
│   ├── 0 critical AND 0 high → proceed to Stage 5 (skip Stage 4)
│   └── Any critical or high → proceed to Stage 4 (refine)
├── THEN: Manual checks (these supplement the validator, they do NOT replace it)
│   ├── Check description is single-line (read SKILL.md, verify no multiline description)
│   ├── If Pipeline archetype: Check each sub-agent uses system-prompt register
│   ├── Check no unnecessary files (no README.md, CHANGELOG.md, etc.)
│   ├── Check evals/evals.json exists and parses as valid JSON with the resolved grading_mode
│   ├── Check evals/triggers.json exists and parses as valid JSON
│   ├── If grading_mode = subjective: Check evals/compliance.json exists and parses as valid JSON
│   ├── Check evals/* placeholder substitutions: no leftover <<SKILL_NAME>>, <<SKILL_PATH>>,
│   │   <<SKILL_VERSION>>, <<GRADING_MODE>>, or <<INVOCATION_EXAMPLE_*>> markers (literal <<TODO>>
│   │   slots are permitted — they are explicit user-fill placeholders for additional tests/queries)
│   ├── If bundles_scripts = true: Check scripts/.gitkeep exists
│   └── If bundles_scripts = true: Check SKILL.md documents `${CLAUDE_PLUGIN_ROOT}` invocation convention
│       (grep for `${CLAUDE_PLUGIN_ROOT}`; ensure no `$CLAUDE_PLUGIN_DIR` references — non-existent var, latent bug)
├── THEN: Cross-file consistency check (memo D11, S107 — defense-in-depth for Stage 2 CONSTRAINT)
│   ├── If skill bundles templates/, references/, or scripts/:
│   │   Scan SKILL.md for content that mirrors or references those files.
│   │   For each mirror (validation rules, character sets, error conditions, output schemas,
│   │   algorithm descriptions), verify SKILL.md and the referenced file agree.
│   │   Canonical disagreement shape: Unicode-preserving algorithm + ASCII-only validation
│   │   step (S107 slug-from-title probe). Read references/content-guidance.md →
│   │   Cross-File Consistency for the full pattern catalog.
│   ├── If a disagreement is found: Treat as HIGH finding. Route to Stage 4 refinement
│   │   with directive to align both files. Do NOT proceed to Stage 5.
│   └── If no supporting files OR no disagreements: Note "no cross-file claims" in diagnostics, proceed.
├── THEN: Sub-pattern review soft prompt (B.6 — Path A — conditional per memo D12, S107)
│   ├── DECISION TREE:
│   │   ├── If sub-patterns selected at Stage 1 > 0:
│   │   │   Present full prompt — "Your skill is archetype {archetype}. Selected sub-patterns
│   │   │   at Stage 1: {list}. Common sub-patterns for this archetype that were NOT
│   │   │   selected: {remaining_list}. Review the generated SKILL.md — should any
│   │   │   additional sub-pattern apply?"
│   │   ├── Elif 0 sub-patterns selected AND archetype has default-ON sub-patterns
│   │   │   that were opted out (Research → reviewer-validated; Inversion → generator-coupled):
│   │   │   Present LIGHT confirmation only — "You opted out of {default-ON list}. Confirm
│   │   │   exclusion intentional? [Yes / Re-enable]". Do NOT re-present the full sub-pattern
│   │   │   catalog.
│   │   └── Else (0 selected AND no default-ON in archetype — Generator, Tool Wrapper,
│   │       Reviewer, Script-driven, Pipeline):
│   │       SKIP the soft prompt entirely. The 0-selection at Stage 1 already represents
│   │       an explicit user choice; re-asking adds friction without surfacing new info.
│   │       Note "soft prompt skipped — 0 sub-patterns selected for non-default-ON archetype"
│   │       in diagnostics.
│   ├── If user identifies a missed sub-pattern OR re-enables a default-ON: trigger Stage 4
│   │   with directive to add the documentation
│   ├── If user confirms (or skip path triggers): proceed to Stage 5
│   └── Reference: content-guidance.md → ## Sub-Pattern Catalog for full definitions
└── Stage 3 exit gate:
    ├── [ ] `just check-description` exited 0 (or all FAIL findings routed to Stage 4 and resolved)
    ├── [ ] `just check-skill-size` exited 0 (HARD CAP refactor proposal, if any, applied via Stage 4)
    ├── [ ] /anthropic-validator was invoked via the Skill tool (not manual review)
    ├── [ ] Validator output was read and findings counted
    ├── [ ] Cross-file consistency check completed (or N/A if no supporting files)
    ├── [ ] Sub-pattern review soft prompt presented OR skipped per D12 decision tree (with diagnostic note)
    ├── [ ] evals/evals.json exists and parses as valid JSON with the resolved grading_mode
    ├── [ ] evals/triggers.json exists and parses as valid JSON
    ├── [ ] If grading_mode = subjective: evals/compliance.json exists and parses as valid JSON
    ├── [ ] No leftover non-TODO placeholders in evals/* (<<SKILL_NAME>>, <<SKILL_PATH>>, <<SKILL_VERSION>>, <<GRADING_MODE>>, <<INVOCATION_EXAMPLE_*>> all substituted)
    ├── [ ] If bundles_scripts = true: scripts/.gitkeep exists
    ├── [ ] If bundles_scripts = true: SKILL.md uses `${CLAUDE_PLUGIN_ROOT}` (not `$CLAUDE_PLUGIN_DIR`) for script invocation paths
    └── If any is unchecked, Stage 3 is NOT complete — go back and complete the missing step
```

### Stage 4: Refine (Sonnet sub-agent, conditional, max 2 retries)

This stage only runs if Stage 3 found critical or high issues.

```
Stage 4: Refine (attempt {N} of 2)
├── Construct prompt using 4-part template:
│   ├── GOAL: Fix all critical and high findings from anthropic-validator
│   ├── CONSTRAINTS:
│   │   ├── Only fix the specific issues identified — do not restructure
│   │   ├── Preserve the existing skill content and structure
│   │   └── Description must remain single-line
│   ├── CONTEXT:
│   │   ├── Validator findings (critical and high items with descriptions)
│   │   ├── Current generated files (read from working directory)
│   │   └── Content guidance: references/content-guidance.md
│   └── OUTPUT: Edit files in {working-directory}/ to fix findings
├── Spawn: Task(description="Fix validator findings", subagent_type="general-purpose",
│          model="sonnet", prompt=...)
├── Re-run Stage 3 (validate)
├── If still failing after 2 retries:
│   └── Proceed to Stage 5 with caveats noted
└── Token budget check
```

### Stage 5: Deploy & Present (Orchestrator)

```
Stage 5: Deploy & Present
├── Deploy skill: Move skill files from {working-directory}/ to {target-directory}/
│   ├── Copy directory tree preserving structure (SKILL.md, references/, templates/, scripts/, evals/)
│   └── This is the ONLY point where skill files are written to the final location
├── If Pipeline archetype: Deploy sub-agents
│   ├── Move {working-directory}/agents/*.md to .claude/agents/
│   └── Each sub-agent file: .claude/agents/{skill-name}-{stage-name}.md
├── Clean up: Remove {working-directory}/ after successful copy
├── Read all generated files for summary
├── Present to user:
│   ├── "Generated skill at: {target-directory}/"
│   ├── If pipeline: "Generated sub-agents at: .claude/agents/"
│   ├── "Files created:"
│   │   └── List each file with line count (skill files + evals/* + sub-agent files)
│   ├── "Architectural decisions:"
│   │   ├── "Context: {fork/inline} — {reason}"
│   │   ├── "Sub-agents: {none/sequential/parallel/AT} — {reason}"
│   │   ├── "grading_mode: {objective/subjective} — {reason}"
│   │   ├── "Bundles scripts: {Yes/No} — {reason}"
│   │   └── "Supporting files: {list} — {reason}"
│   ├── "Skill type: {template used}"
│   ├── "Validation: {pass/fail with details}"
│   ├── If caveats: "Unresolved issues: {list}"
│   ├── If pipeline: "Sub-agent permissions to configure:"
│   │   └── {List tool permissions for each sub-agent that must be added to settings.json}
│   └── "Next steps:"
│       ├── "1. Review and customize the generated instructions"
│       ├── "2. Test activation by asking Claude to invoke it"
│       ├── "3. Iterate on trigger patterns until activation is reliable"
│       ├── "4. Add domain-specific content to reference files"
│       ├── "5. Fill in evals/ <<TODO>> placeholders with concrete test prompts and trigger queries"
│       ├── "6. Run `just eval-skill {target-directory}` to baseline behavior (requires bun on PATH)"
│       └── If pipeline: "7. Configure tool permissions for sub-agents in .claude/settings.json"
└── Note: This is a scaffold, not production-ready output (generate-and-customize contract). evals/ ships with one starter test + 3-5 seeded triggers; user fills the rest.
```

### Stage 6: Diagnostics (REQUIRED)

**MANDATORY**: Write diagnostic output after every invocation. This cannot be skipped.

```
Stage 6: Diagnostics
├── Write to: $PROJECT_DIR/logs/diagnostics/create-skill-{YYYYMMDD-HHMMSS}.yaml
│   └── Use templates/diagnostic-output.yaml schema
└── Include:
    ├── Input: description/name/doc path
    ├── Interview: questions asked, rounds completed
    ├── Classification: all three decisions + template selected
    ├── Generation: files created, line counts, model used
    ├── Validation: pass/fail, findings count, retry count
    └── Outcome: success/partial/failure
```

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Generator sub-agent returns empty output | Re-spawn once with reinforced instructions. If still empty, STOP: "Generation failed. Please try with a more detailed description." |
| anthropic-validator finds critical issues | Stage 4 retry (max 2). After 2 retries, present with caveats. |
| anthropic-validator unavailable | Skip validation, note in diagnostics, warn user: "Validation skipped — run /anthropic-validator manually." |
| Interview answers are ambiguous | Ask 1-2 follow-up questions (max 2 AskUserQuestion rounds total). |
| User requests Agent Teams | Include experimental warning: "Agent Teams requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. This is an experimental feature." |
| Token budget exceeded | Stop at current stage, present partial output with explanation. |
| Target directory already exists | AskUserQuestion: "Directory {path} already exists. Overwrite / Choose different name / Cancel?" |
| Working directory already exists | Silently remove and recreate tmp/create-skill/{skill-name}/ (working dirs are ephemeral) |
| User rejects classification | Re-classify with user's feedback. Max 2 classification rounds. |

---

## Token Budget Management

| Checkpoint | Threshold | Action |
|------------|-----------|--------|
| After Pre-Flight | >30% consumed | Warn: "Pipeline agents will consume significant context." |
| After Generate | >55% consumed | Warn: "Approaching budget. Validation + refinement may be limited." |
| After Validate | >65% consumed | Skip refinement if needed, present as-is with caveats. |

