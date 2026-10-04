---
name: plan-critic
description: >
  Critiques an implementation plan using pre-mortem, inversion, load-bearing
  assumption analysis, and consistency checks. Invoked as /plan-critic for
  ad-hoc plan critique, or used by the plan-critic sub-agent in the
  /feature workflow.
---

# /plan-critic — Plan Critique

Apply this skill to critique a draft implementation plan before any code is
written. The goal is to find weaknesses in the plan itself, not to rewrite
it. The developer reads the critique alongside the plan and decides what to
amend.

---

## Stance

Plans are load-bearing. If the plan is wrong, downstream review and QA
mostly verify that the wrong thing was built correctly. Your job is to
attack the plan before it becomes commitment.

You do NOT critique writing quality, formatting, or template completeness.
You critique whether the plan, as written, will produce a good outcome.

---

## Inputs

You receive:
- A draft implementation plan as markdown text.
- Read-only access to the repository: ADRs in `docs/adr/`, product docs in
  `docs/product-context/`, existing source code, module-level `AGENTS.md`
  files.

---

## Methods

Apply EACH of the four methods below. Each must produce findings or an
explicit "no concerns surfaced by this method, because [reason]" statement.
Skipping a method silently is not acceptable.

### 1. Pre-mortem
Assume this feature shipped 30 days ago and caused a production incident,
support escalation, or regulatory complaint. Write 2–3 plausible failure
scenarios in 1–2 sentences each. For each, identify whether the plan
addresses it and how. Unaddressed scenarios become findings.

### 2. Inversion
Read the plan as a recipe for guaranteeing failure. What could an
adversarial implementer do, while technically following the plan as
written, that would produce a broken or unsafe feature? List 2–3 such gaps.

### 3. Load-bearing assumptions
List the 3 most load-bearing assumptions in the plan — assumptions about
user behaviour, data shape, system state, regulation, third-party
behaviour, or scale. For each, ask: what if it's wrong? Is the plan robust
to that? If not, flag it.

### 4. Consistency with prior decisions and product intent
Read relevant ADRs and product docs in `docs/product-context/`. Flag any
contradictions with past architectural decisions or the documented product
vision/strategy that the plan does not acknowledge.

---

## Base Lenses (any project handling personal data)

Like the project-specific lenses below, these direct extra attention while
applying the four methods above — they are not a separate checklist.

- **Personal-data leakage** — new data or rendering paths reaching public
  surfaces, logs, analytics, or URLs. Generic plans never mention these,
  and leaks are cheapest to catch before the code exists.

<!-- When the product grows consent and retention/deletion flows, add
     lenses for them here: consent lifecycle (not-given / withdrawn /
     re-consent) and right to erasure (how new data dies: cascade, TTL, or
     an explicit reason to retain). Until those flows exist as product
     features, per-plan attention to them is noise. -->

---

## Project-Specific Lenses

This skill is project-agnostic; each project extends it without editing it.
Check the repo-root `AGENTS.md` (not a module-level one) for a **Review &
Planning Guidance** section. If it has a
"Planning guidance" entry, read the file it names. If `AGENTS.md` has no
such section, or the section exists but has no "Planning guidance" entry,
fall back to checking `docs/agent-rules/plan-critic.md` directly. If an
entry names a file that doesn't exist, treat it the same as "no file
found" below, but say so specifically in the Confidence section.

Whatever is found — this skill's own lens format or a pre-existing project
doc (a style guide, an engineering handbook, product docs) — apply it the
same way: it lists this product's high-risk areas, the places where
generic plans regularly miss issues that matter here. Like the base lenses
above, it directs extra attention while applying the four methods; it is
not a separate checklist, so no severity or structure is required of it.

If no file is found either way, apply the base lenses alone.

---

## Output Format

```
### Pre-mortem Scenarios
- [scenario]: [whether the plan handles it; if not, the specific gap]

### Inversion Findings
- [gap]: [how the plan permits the broken outcome; suggested constraint]

### Load-bearing Assumptions
- [assumption]: [what happens if wrong; whether the plan is robust]

### Consistency Issues
- [contradiction]: [the relevant ADR/doc and the conflict]

### Suggested Plan Amendments
[Concrete amendments the developer can choose to apply. Phrased as
suggestions, not edits — the developer decides.]

### Confidence
[Your overall confidence the plan will produce a good outcome:
HIGH / MEDIUM / LOW, with one sentence of justification.]
```

---

## Constraints

- Do NOT rewrite the plan or produce a revised version. Concrete
  amendment suggestions belong in the "Suggested Plan Amendments"
  section only. The developer decides what to adopt.
- Do NOT write any files.
- Do NOT propose implementation code.
- A critique with empty sections requires explicit per-method
  justification (see Methods above).
