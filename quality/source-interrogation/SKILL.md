---
name: source-interrogation
description: "Run the Q1–Q18 source interrogation against approved canonical Markdown sources to extract the fields needed to author a subagent profile (role, when-to-use, modes, evidence). Use after ingestion produces canonical Markdown and before profile derivation — Phase 3 of the authoring cycle."
---

# Skill: source-interrogation

**Purpose:** Run Q1–Q18 against approved canonical Markdown sources to extract all
information needed to author a subagent profile.

---

## Input

- Path(s) to `subagents/<slug>/sources/markdown/*.md`
- Topic context (from `--topic` argument)
- Source metadata from `sources/metadata/<source_id>.metadata.json`

---

## Questions Q1–Q18

Read the Markdown source carefully. Answer each question from source evidence only.
Do not invent information not found in the source.

| QID | Question | Maps to |
|-----|----------|---------|
| Q1  | What expert title or function does the source describe? | `display_name`, `role` |
| Q2  | What job is repeatedly performed? | `role`, `supported_modes` |
| Q3  | 3–5 concrete situations that trigger this expert? | `when_to_use[]` |
| Q4  | 2–3 situations this expert should NOT be involved? | `when_not_to_use[]` |
| Q5  | What does the expert first ask for before engaging? | `inputs.required[]` |
| Q6  | What is the primary deliverable? | `outputs.primary_format`, modes |
| Q7  | What distinguishes good work from bad? | `quality_bar[]` |
| Q8  | Who receives the work next / owns the final decision? | `handoff_rules`, `canonical_owner` |
| Q9  | Which modes does the source actually justify? | `supported_modes[]` |
| Q10 | What would the expert refuse even if asked? | `forbidden_behaviours[]` |
| Q11 | What is the smallest useful output? | `minimum_useful_output` |
| Q12 | What knowledge must be always-on? | `knowledge_partition.always_on[]` |
| Q13 | What is actionable but too detailed for the profile? | `knowledge_partition.skills[]` |
| Q14 | What content is better as a reference file? | `knowledge_partition.references[]` |
| Q15 | What must be retrieved through MCP or tools? | `knowledge_partition.mcp[]` |
| Q16 | What is project-specific, must be caller-supplied? | `knowledge_partition.caller_supplied[]` |
| Q17 | What is the source of truth for this domain? | `source_of_truth_policy` |

> **Q16 note — `caller_supplied` vs `inputs.required`:**
> `inputs.required` = artifacts the subagent cannot start without (code to review, document to process).
> `caller_supplied` = per-project runtime context that varies per engagement (team naming conventions, existing error patterns, project-specific constraints).
> If Q16 yields required artifacts, put them in `inputs.required` and set `caller_supplied: []`.
> Document the decision in the provenance ledger Q16 row.
| Q18 | What is volatile or likely to drift? | provenance ledger review schedule |

> **Regulated-domain flag (J-track / Step-15):** if Q1/Q2 place the source in a **regulated,
> high-stakes advice domain — finance, legal, or medical** — record that explicitly. It is the
> dominant influence on Q4/Q8/Q10 for these domains: the expert distills *education*, never
> personalized advice, and defers the decision to a licensed professional. The deriver then sets
> `domain_risk_category` and ships the deterministic no-advice boundary (graded refusal +
> defer-to-professional + standing disclaimer) from `tools/subagent_factory/domain_policy.py`; the
> validate gate (block #14) enforces it. Non-regulated/technical sources: no flag.

---

## Mode evidence rule

Assign a mode only when the source provides BOTH a credible action verb AND a credible deliverable.

| Evidence | Allowed mode |
|----------|-------------|
| Draft / create from scratch | `produce` |
| Review / critique existing artifact | `review` |
| Verify / gate against criteria | `validate` |
| Extract / classify / structure | `extract` |
| Suggest minimal bounded change | `patch-suggest` |
| Compare alternatives | `compare` |
| Recommend / consult / guide | `advise` |

---

## Output format

Return a YAML interrogation record:

```yaml
source_id: <id>
q1_display_name: "<answer>"
q1_role: "<answer>"
q2_job: "<answer>"
q3_triggers:
  - "<trigger 1>"
  - "<trigger 2>"
  - "<trigger 3>"
q4_exclusions:
  - "<exclusion 1>"
  - "<exclusion 2>"
q5_required_input: "<answer>"
q6_primary_deliverable: "<answer>"
q7_quality_marks:
  - "<mark 1>"
  - "<mark 2>"
q8_handoff: "<answer>"
q9_modes:
  - name: <mode>
    evidence: "<source evidence>"
q10_refusals:
  - "<refusal>"
q11_minimum_output: "<answer>"
q12_always_on:
  - "<item>"
q13_skills:
  - "<item>"
q14_references:
  - "<item>"
q15_mcp: []
q16_caller_supplied: []
q17_source_of_truth: "<answer>"
q18_volatile: "<answer>"
evidence_gaps:
  - "<any Q where source gave no usable evidence>"
```

Flag `evidence_gaps` for any question the source could not answer. Do not invent.

---

## Phase 2.5 — Importance ranking (before triage)

After interrogation, segment the source into candidate units and score each on
the 9 importance dimensions (1–5): `authority`, `actionability`, `reusability`,
`risk_impact`, `evidence_strength`, `uniqueness`, `transferability`, `stability`,
`operational_fit`. Record them as a YAML file:

```yaml
schema_version: importance-scores-v1
candidate_units:
  - id: U1
    source_id: <source_id>
    summary: "one-line description of the unit"
    scores: { authority: 5, actionability: 4, reusability: 4, risk_impact: 5,
              evidence_strength: 4, uniqueness: 3, transferability: 4,
              stability: 4, operational_fit: 4 }
```

Apply the deterministic decision rule with the factory script:

```bash
python -m tools.subagent_factory.score_extracted_units <units.yaml>
```

`keep` units proceed to Phase 4 triage; `discard` units route to the provenance
ledger only; `review` units need a human decision. Do not let low-value
background material into the profile just because it is structurally valid.

## Purpose-review detection

If the source justifies critiquing goals, intent, or project framing — not only
code or documents — record a `purpose-review` advisory pattern layered over
`advise` / `validate` / `compare`. Realise it from
`templates/purpose-review-contract.yaml.j2` (embed as a profile mode or emit
`references/purpose-review-pattern.md`).
