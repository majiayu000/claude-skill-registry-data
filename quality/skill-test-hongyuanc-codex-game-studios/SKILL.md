---
name: skill-test
description: "Use when Codex skill files need structural, behavioral, category, or coverage validation."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- A writing workflow may use either one complete approved changeset or sequential bounded section approval. In the section pattern, show the draft, obtain explicit section approval, then write only that approved section without per-file or per-line reapproval.
- A new path, expanded scope, or material change requires fresh approval under the appropriate complete-changeset or bounded-section contract.

## Validation Boundary

Validation is read-only and does not require approval. Resolve skills from the
current task's available skill catalog and use
`../../../tools/codex_studio/validate.py` as the native static validator. The
bundled validator, testing framework, specs, templates, and bundled testing
catalog are read-only. Do not search for or copy repository-local skill files to
reconstruct the catalog. Optional evidence writes only to the project-owned
`production/qa/skill-tests/` directory after approval.

Resolve the validator path against this installed `SKILL.md` directory, not the
project working directory, and convert both it and the catalog-resolved target
skill to absolute paths. Invoke the actual bundled operation as:

```bash
python3.11 <absolute-bundled-studio-root>/tools/codex_studio/validate.py --skill-file <absolute-catalog-resolved-SKILL.md>
```

The bundled validator establishes its own studio root for imports. Do not add
the target project to `PYTHONPATH` or create project-local tool copies.

### Native readiness gate for `$[name]`

Before invoking or routing to `$[name]`, confirm that `[name]` is present in the current task's available skill catalog. If unavailable, report
`Staged dependency: $[name] is not available`, defer the handoff, do not invoke `$[name]`, do not route to `$[name]`, and do not search for or copy a repository-local skill file.

# Skill Test

Validates skill resources from the available skill catalog for structural compliance and
behavioral correctness. No external dependencies — runs entirely within the
existing skill/hook/template architecture.

**Four modes:**

| Mode | Command | Purpose | Token Cost |
|------|---------|---------|------------|
| `static` | `$codex-game-studios:skill-test static [name\|all]` | Structural linter — 7 compliance checks per skill | Low (~1k/skill) |
| `spec` | `$codex-game-studios:skill-test spec [name]` | Behavioral verifier — evaluates assertions in test spec | Medium (~5k/skill) |
| `category` | `$codex-game-studios:skill-test category [name\|all]` | Category rubric — checks skill against its category-specific metrics | Low (~2k/skill) |
| `audit` | `$codex-game-studios:skill-test audit` | Coverage report — skills, agent specs, last test dates | Low (~3k total) |

---

## Phase 1: Parse Arguments

Determine mode from the first argument:

- `static [name]` → run 7 structural checks on one skill
- `static all` → run 7 structural checks on all skills in the available skill catalog
- `spec [name]` → read skill + test spec, evaluate assertions
- `category [name]` → run category-specific rubric from `../../../Codex Studio Testing Framework/quality-rubric.md`
- `category all` → run category rubric for every skill that has a `category:` in catalog
- `audit` → read catalog, list all skills and agents, show coverage
- No argument → run `audit`

If the argument is unrecognized, output usage and stop. A missing argument is not an error; it selects `audit`.

For `spec`, `category`, or `audit`, first check whether `../../../Codex Studio Testing Framework/catalog.yaml` exists. If it does not, report that the native testing framework is incomplete and stop; do not invent catalog entries. Static mode remains available because it uses the available skill catalog and `../../../tools/codex_studio/validate.py` directly.

---

## Phase 2A: Static Mode — Structural Linter

For each skill being tested, read its `SKILL.md` fully and run all 7 checks:

### Check 1 — Native Skill Contract
The YAML frontmatter must contain exactly `name` and `description`; `name` must equal the skill directory name, and `description` must be nonblank.
This static contract does not require a literal `Use when` prefix.

Delegate the structural decision to `validate_skill` in
`../../../tools/codex_studio/validate.py` so the runtime validator remains the single
implementation of this contract and non-native interaction primitives, legacy
paths, model metadata, and tool metadata also fail this check.
Use the absolute-path `--skill-file` invocation defined in the Validation
Boundary; its `Skill validation: PASS|FAIL` result and emitted issues are the
authoritative Check 1 result.
`validate_skill` does not judge whether the prose is trigger-oriented; that is a
human or behavioral-spec quality review, not a structural validator rule.

**FAIL** for any validator issue or blank description.
### Check 2 — Multiple Phases
The skill must have ≥2 numbered phase headings. Look for patterns like:
- `## Phase N` or `## Phase N:`
- `## N.` (numbered top-level sections)
- At least 2 distinct `##` headings if phases aren't explicitly numbered

**FAIL** if fewer than 2 phase-like headings are found.

### Check 3 — Verdict Keywords
The skill must contain at least one of: `PASS`, `FAIL`, `CONCERNS`, `APPROVED`,
`BLOCKED`, `COMPLETE`, `READY`, `COMPLIANT`, `NON-COMPLIANT`

**FAIL** if none are present.

### Check 4 — Bounded Write Approval
For a writing workflow, accept either one complete approved changeset for a multi-file or atomic workflow, or sequential bounded section approval. The section contract must show the draft, obtain explicit section approval, then write only that approved section without per-file or per-line reapproval. A new path or expanded scope requires fresh approval under the appropriate pattern.

**WARN** if absent from a read-only skill that does not explicitly declare its diagnostic boundary.
**FAIL** if writes occur before either appropriate approval or if the body permits unapproved scope expansion.
### Check 5 — Next-Step Handoff
The skill must end with a recommended next action or follow-up path. Look for:
- A final section mentioning another skill (e.g., `$codex-game-studios:story-done`, `$codex-game-studios:gate-check`)
- "Recommended next" or "next step" phrasing
- A "Follow-Up" or "After this" section

**WARN** if absent.

### Check 6 — Delegation Boundary
If the skill delegates work, require independent and bounded child tasks, `agents.max_depth = 1`, parent synthesis, and a prohibition on child commits, publication, or scope expansion.

**WARN** when delegation is used but these boundaries are incomplete.
### Check 7 — Invocation Contract
If the skill accepts arguments or modes, its body must show a dollar-prefixed usage form and define missing-argument behavior. Cross-reference it against the first parsing section.

**WARN** if documented modes do not match the usage form.
---

### Static Mode Output Format

For a single skill:
```
=== Skill Static Check: $[name] ===

Check 1 — Native Skill Contract: PASS
Check 2 — Multiple Phases:       PASS (7 phases found)
Check 3 — Verdict Keywords:      PASS (PASS, FAIL, CONCERNS)
Check 4 — Bounded Approval:      PASS
Check 5 — Next-Step Handoff:     WARN (no follow-up section found)
Check 6 — Delegation Boundary:   PASS
Check 7 — Invocation Contract:   PASS

Verdict: WARNINGS (1 warning, 0 failures)
Recommended: Add a "Follow-Up Actions" section at the end of the skill.
```

For `static all`, produce a summary table then list any non-compliant skills:
```
=== Skill Static Check: All [discovered skill count] Skills ===

Skill                  | Result       | Issues
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | Check 5: no handoff
...

Summary: 48 COMPLIANT, 3 WARNINGS, 1 NON-COMPLIANT
Aggregate Verdict: N WARNINGS / N FAILURES
```

---

## Phase 2B: Spec Mode — Behavioral Verifier

### Step 1 — Locate Files

Resolve `[name]` from the current task's available skill catalog.
Look up the spec path from `../../../Codex Studio Testing Framework/catalog.yaml` — use the
`spec:` field for the matching skill entry. Treat the catalog value as a path
relative to the bundled studio root: ascend three levels from this skill's
directory, then resolve every `spec:` value against the bundled studio root.
Never resolve it against the target repository's working directory.

If either is missing:
- Missing skill: "Skill '[name]' not found in the available skill catalog."
- Missing spec path in catalog: "No spec path set for '[name]' in catalog.yaml."
- Spec file not found at path: "Spec file missing at [path]. Run `$codex-game-studios:skill-test audit`
  to see coverage gaps."

### Step 2 — Read Both Files

Read the skill file and test spec file completely.

### Step 3 — Evaluate Assertions

For each **Test Case** in the spec:

1. Read the **Fixture** description (assumed state of project files)
2. Read the **Expected behavior** steps
3. Read each **Assertion** checkbox

For each assertion, evaluate whether the skill's written instructions, if
followed correctly given the fixture state, would satisfy it. This is a
Codex-evaluated reasoning check, not code execution.

Mark each assertion:
- **PASS** — skill instructions clearly satisfy this assertion
- **PARTIAL** — skill instructions partially address it, but with ambiguity
- **FAIL** — skill instructions would NOT satisfy this assertion given the fixture

For **Protocol Compliance** assertions (always present):
- Check whether the skill uses a complete approved changeset or sequential bounded section contract before file writes
- Check whether the skill presents findings before requesting approval
- Check whether the skill ends with a recommended next step
- Check whether the skill avoids auto-creating files without approval

### Step 4 — Build Report

```
=== Skill Spec Test: $[name] ===
Date: [date]
Spec: Codex Game Studios bundled testing spec: skills/[category]/[name].md

Case 1: [Happy Path — name]
  Fixture: [summary]
  Assertions:
    [PASS] [assertion text]
    [FAIL] [assertion text]
       Reason: The skill's Phase 3 says "..." but the fixture state means "..."
  Case Verdict: FAIL

Case 2: [Edge Case — name]
  ...
  Case Verdict: PASS

Protocol Compliance:
  [PASS] Uses an appropriate complete-changeset or bounded-section approval before file writes
  [PASS] Presents findings before asking approval
  [WARN] No explicit next-step handoff at end

Overall Verdict: FAIL (1 case failed, 1 warning)
```

### Step 5 — Offer to Write Project Evidence

The bundled testing catalog is read-only. Offer one optional project-owned
evidence file at
`production/qa/skill-tests/skill-test-spec-[name]-[date].md`. Show that exact
path and report contents as a complete proposed changeset before writing.

If approved, write only that evidence file. Record the bundled spec's stable
source label plus `last_spec: [date]` and
`last_spec_result: PASS|PARTIAL|FAIL` in the project evidence; never update the
bundled catalog or testing framework.

---

## Phase 2D: Category Mode — Rubric Evaluation

### Step 1 — Locate Skill and Category

Resolve `[name]` from the current task's available skill catalog.
Look up `category:` field in `../../../Codex Studio Testing Framework/catalog.yaml`.

If skill not found: "Skill '[name]' not found."
If no `category:` field: "No category assigned for '[name]' in catalog.yaml.
The bundled catalog is read-only; category validation cannot continue." Report
that result and stop without writing. If the user explicitly requests canonical metadata authoring,
route it only through a verified canonical studio source checkout and its
repository-root testing catalog; never edit or shadow the installed bundle.

For `category all`: collect all skills with a `category:` field and process each.
`category: utility` skills are evaluated against U1 (static checks pass) and U2
(gate mode correct if applicable) only — skip to the static mode for U1.

### Step 2 — Read Rubric Section

Read `../../../Codex Studio Testing Framework/quality-rubric.md`.
Extract the section matching the skill's category (e.g., `### gate`, `### team`).

### Step 3 — Read Skill

Read the skill's `SKILL.md` fully.

### Step 4 — Evaluate Rubric Metrics

For each metric in the category's rubric table:
1. Check whether the skill's written instructions clearly satisfy the criterion
2. Mark PASS, FAIL, or WARN
3. For FAIL/WARN, identify the exact gap in the skill text (quote the relevant section
   or note its absence)

### Step 5 — Output Report

```
=== Skill Category Check: $[name] ([category]) ===

Metric G1 — Review mode read:      PASS
Metric G2 — Full mode directors:   FAIL
  Gap: Phase 3 spawns only CD-PHASE-GATE; TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE absent
Metric G3 — Phase-gated: required gates only: PASS
Metric G4 — Solo: required gates remain, optional gates skipped: PASS
Metric G5 — No auto-advance:       PASS

Verdict: FAIL (1 failure, 0 warnings)
Fix: Add TD-PHASE-GATE, PR-PHASE-GATE, and AD-PHASE-GATE to the full-mode director
     panel in Phase 3.
```

### Step 6 — Offer to Write Project Evidence

The bundled testing catalog is read-only. Offer an optional project-owned
`production/qa/skill-tests/skill-test-category-[name]-[date].md` evidence file
containing `last_category` and `last_category_result`. Write only that approved
file; never update the bundled catalog or testing framework.

---

## Phase 2C: Audit Mode — Coverage Report

### Step 1 — Read Catalog

Read `../../../Codex Studio Testing Framework/catalog.yaml`. If missing, note that catalog doesn't exist
yet (first-run state).

### Step 2 — Enumerate All Skills and Agents

Use the current task's available skill catalog to get the complete list of skills.
Extract skill name from each path (directory name).

Also read the `agents:` section from `../../../Codex Studio Testing Framework/catalog.yaml` to get the
complete list of agents.

### Step 3 — Build Skill Coverage Table

For each skill:
- Check if a spec file exists (use the `spec:` path from catalog, or file search `../../../Codex Studio Testing Framework/skills/*/[name].md`)
- Look up `last_static`, `last_static_result`, `last_spec`, `last_spec_result`,
  `last_category`, `last_category_result`, `category` from catalog (or mark as
  "never" / "—" if not in catalog)
- Priority comes from catalog `priority:` field (critical/high/medium/low)

### Step 3b — Build Agent Coverage Table

For each agent in catalog's `agents:` section:
- Check if a spec file exists (use the `spec:` path from catalog, or file search `../../../Codex Studio Testing Framework/agents/*/[name].md`)
- Look up `last_spec`, `last_spec_result`, `category` from catalog

### Step 4 — Output Report

```
=== Skill Test Coverage Audit ===
Date: [date]

SKILLS ([discovered skill count] total)
Specs written: [spec count] ([percentage]%) | Never static tested: [count] | Never category tested: [count]

Skill                  | Cat      | Has Spec | Last Static | S.Result | Last Cat | C.Result | Priority
-----------------------|----------|----------|-------------|----------|----------|----------|----------
gate-check             | gate     | YES      | never       | —        | never    | —        | critical
design-review          | review   | YES      | never       | —        | never    | —        | critical
...

AGENTS ([discovered agent count] total)
Agent specs written: [spec count] ([percentage]%)

Agent                  | Category   | Has Spec | Last Spec   | Result
-----------------------|------------|----------|-------------|--------
creative-director      | director   | YES      | never       | —
technical-director     | director   | YES      | never       | —
...

Top 5 Priority Gaps (skills with no spec, critical/high priority):
(none if all specs are written)

Skill coverage:  [spec count]/[discovered skill count] specs ([percentage]%)
Agent coverage:  [spec count]/[discovered agent count] specs ([percentage]%)
```

No file writes in audit mode.

Offer: "Would you like to run `$codex-game-studios:skill-test static all` to check structural
compliance across all skills? `$codex-game-studios:skill-test category all` to run category rubric
checks? Or `$codex-game-studios:skill-test spec [name]` to run a specific behavioral test?"

---

## Phase 3: Recommended Next Steps

After any mode completes, offer contextual follow-up:

- After `static [name]`: "Run `$codex-game-studios:skill-test spec [name]` to validate behavioral
  correctness if a test spec exists."
- After `static all` with failures: "Address NON-COMPLIANT skills first. Run
  `$codex-game-studios:skill-test static [name]` individually for detailed remediation guidance."
- After `spec [name]` PASS: "Optionally record the pass under
  `production/qa/skill-tests/`, then run `$codex-game-studios:skill-test audit` to find the next
  spec gap."
- After `spec [name]` FAIL: "Review the failing assertions and record the
  mismatch in project-owned evidence. Stop without writing to the bundled skill
  or spec. Canonical corrections require a verified canonical studio source
  checkout and separate approved source changeset."
- After `audit`: "Start with the critical-priority gaps. The bundled spec
  template at `../../../Codex Studio Testing Framework/templates/skill-test-spec.md`
  is read-only. New canonical specs require a verified canonical studio source
  checkout; this installed workflow stops without writing to the bundle."
