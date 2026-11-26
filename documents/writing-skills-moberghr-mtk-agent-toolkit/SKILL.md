---
name: writing-skills
description: Use when creating a new skill for this toolkit — ensures the skill follows the anatomy, CSO principle, and is tested against agent rationalizations before shipping.
type: skill
license: MIT
compatibility:
  - claude-code
user-invocable: false
---

# Writing Skills

## Overview

A skill is a reusable behavior contract that shapes how an agent approaches a category of work. Writing a good skill requires observing baseline failures first, then writing the minimum documentation that closes those gaps, then testing that the skill resists pressure.

## When To Use

- Adding a new skill to the toolkit
- Substantially rewriting an existing skill

### When NOT To Use

- One-off project-specific conventions (put those in CLAUDE.md)
- Mechanical constraints better handled by automation (put those in hooks or settings)

## Workflow

### Phase 1: Observe Baseline Failures

Before writing any skill content:

1. Run 2-3 representative scenarios without the skill.
2. Document what went wrong:
   - What steps were skipped?
   - What rationalizations were used to skip them?
   - What outcomes were produced?
3. This creates the "RED" baseline — the specific gaps the skill must close.

### Phase 2: Write The Minimum Skill

1. Follow the anatomy defined in `docs/skill-anatomy.md`:
   - Required: frontmatter (`name`, `description`, `type: skill` — or `type: tech-stack` for tech stack skills), `# Title`, `## Overview`, `## When To Use`, `## Workflow`, `## Verification`
   - Recommended: `### When NOT To Use`, `## Rules`
   - Do not add rationalization tables, red-flag lists, or ALL-CAPS emphasis. Current models follow instructions literally and over-trigger on pressure language; state each rule once, in plain words, in the step it governs.

2. **Apply the CSO principle:** The `description` in frontmatter must trigger on conditions, not summarize the workflow.
   - Bad: "Create implementation plans with acceptance criteria and dependency ordering"
   - Good: "Use after a spec is approved and before multi-file implementation begins"
   - Why: Workflow summaries cause the agent to follow the description instead of reading the full SKILL.md

3. **Put field-earned rules in the workflow:** When a baseline failure shows a step being skipped, close it with one plain sentence in that step (what to do and, if it is not obvious, why). Do not restate it in a separate table or list.

4. **Write verification checklist:** Every claim the skill makes about outcomes must have a verification step.

5. **Keep it under 500 lines.** If the skill needs more, use progressive disclosure:
   - Core workflow in SKILL.md
   - Reference material in separate files loaded on demand
   - The SKILL.md is a **navigation layer, not a payload** (S2.26): it holds the
     decision logic and links to references — it does not inline detail it could
     point to. The budget is the ceiling, not the target.

### Phase 3: Test Under Pressure

1. Create 3-5 adversarial scenarios that try to break the skill's discipline:
   - Time pressure: "We need to ship this now, skip X"
   - Simplicity argument: "This is too simple to need X"
   - Authority argument: "The engineer said to skip X"
   - Precedent argument: "We didn't do X last time and it was fine"

2. Run each scenario and verify the skill holds.
3. If the skill breaks, strengthen the specific gap:
   - Tighten the workflow step that was skipped

4. Save pressure tests to `tests/pressure-tests/<skill-name>-pressure.md`.

### Phase 3b: Add Evals (If The Skill Gates Shipping)

If the skill is on the ship path — meaning a miss ends up in a commit, a PR,
or a release — add measurable evals in addition to pressure tests:

1. Add a native `claude plugin eval` case: `evals/<case>/prompt.md` (the user
   prompt plus `tags`, limits and `allowed_tools` frontmatter), `case.yaml`
   naming a `scaffold.sh` that builds the repo the prompt runs in, and one
   grader per file under `graders/`. Layout and run commands: `evals/README.md`.
2. Prefer deterministic graders (`regex` over a produced file or the trace,
   `tool_used`, `file_exists`) and keep `llm` rubrics to short outputs with
   concrete PASS/FAIL conditions. Grade behaviour, not wording.
3. Mark graders that can only pass with the plugin `arm: with-only`, and
   "must not do X" checks `arm: both`, so the without-plugin arm stays comparable.
4. Tag the case `core` (and `smoke` if it is cheap), then iterate with
   `claude plugin eval . --case <case> --runs 1 --ablation none --scaffold
   --allow-tools Bash Write Edit --trust-plugin` until it loads and grades sensibly.

Pressure tests are adversarial-only scenarios read by a human. Evals are
executed and give a measurable score against a no-plugin baseline. Use both
for ship-path skills; pressure tests alone are sufficient for advisory skills.

### Phase 4: Register

1. Add the skill to `.claude/manifest.json` with action `sync`.
2. Add routing rules to `AGENTS.md` if the skill changes how tasks are dispatched.
3. Update `docs/skill-anatomy.md` if the skill establishes a new pattern.
4. Run `bash scripts/validate-toolkit.sh` to verify the skill passes validation.

Note: tech stack skills (`type: tech-stack`) follow the S2.13 declarative anatomy instead of the workflow anatomy above.

## Cache-Stable Prefixes

When a skill runs repeatedly across sessions — especially a reviewer agent or an entry-point skill that the whole team loads on every run — prompt caching cuts token cost dramatically. Caching works by matching an **exact prefix** of the prompt. If the prefix changes every session (because a date, branch, or diff stat is at the top), the cache misses.

**Rule:** put invariants first, volatile state last.

- Invariants (top): persona statement, output contract, standards checklist. These never change between sessions.
- Dynamic state (bottom): current branch, diff stats, touched files, behavioral diff. Inject these via `` !`command` `` fenced blocks or at the call site, not woven through the static body.

A good reviewer agent has the same top ~80% byte-for-byte across every invocation, with only the diff + behavioral-diff injected at the end. That prefix caches; subsequent sessions pay only for the tail.

Entry-point skills follow the same pattern — Phase 0 load instructions stay identical, only the user-supplied task description varies.

## Rules

- No skill without baseline failure observations.
- Field-earned rules live in the workflow step they govern, stated once in plain words.
- No skill without a verification checklist.
- Descriptions trigger on conditions, never summarize workflows (CSO principle).
- Keep frequently-loaded skills under 500 lines.
- Test discipline-enforcing skills with adversarial pressure scenarios.
- Cache-stable prefix for reviewer agents and high-traffic entry-point skills: invariants top, dynamic state bottom.

## Verification

- [ ] Baseline failures were documented before writing the skill
- [ ] Description follows the CSO principle (condition-based triggering)
- [ ] Every skippable step states its rule in the step itself (no rationalization tables or red-flag lists)
- [ ] Verification checklist covers every outcome claim
- [ ] SKILL.md is under 500 lines
- [ ] Pressure tests exist and the skill passes them
- [ ] If this skill claims another skill consumes/invokes/checks its output, grep that skill and confirm the reciprocal reference exists
- [ ] Skill is registered in manifest.json and `validate-toolkit.sh` passes
