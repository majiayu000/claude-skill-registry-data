---
name: author-skills
description: "Author the bodies of a package's stub skills (skills/<name>/SKILL.md) and references (references/<name>.md) from its principles / evidence / source, then promote the package from status: draft to ready. Closes the Phase 6 authoring gap."
---

## Purpose

A generated package ships with **stubs**: `cli stubs` scaffolds every
`knowledge_partition.skills` / `references` entry as a `STATUS: STUB` placeholder, and nothing
fills them — so packages stay at `status: draft` forever. This skill is the missing producer:
it authors each stub **body** grounded in that package's own principles / evidence / source
(not invented), then promotes the package to `status: ready`. Output is validated by
`validate_skill_authoring.py` (status-gated) and re-checked by faithfulness + quote-scan.

## Input

- `profile.yaml` — `knowledge_partition.{skills,references}` (what to author), `always_on`,
  `supported_modes`, `quality_bar`, `forbidden_behaviours`, `status`, rights status.
- **Tier 1+:** `principles/principles.yaml` (entries whose `operational_mapping.skill` ==
  the slug), their `derived_from_claims` → `analysis/claims.jsonl` →
  `evidence/evidence-records.yaml` → `source_anchors` → source markdown (via `source_text`).
- **Tier 0:** profile `always_on` + `when_to_use` + source markdown directly (no principle layer).

## Procedure

For each stub **or `status: stale` doc** (use the same slug `generate_stubs` chose — see
`planned_slugs`; a stale doc is one Step 9 flagged because its grounding drifted, re-author it
exactly like a stub):

1. **Gather grounding.** Tier 1+: collect the principle(s) mapped to this slug, their evidence
   records, and the cited source anchors. Tier 0: collect the relevant `always_on` rules + source.
2. **Author the body** from that grounding only:
   - **Skill** (`skills/<slug>/SKILL.md`, ≤ 500 lines / 5,000 tokens): `## Purpose`,
     `## When to use`, `## Procedure` (the repeatable/branching steps that justified extraction),
     `## Inputs`, `## Output`, `## References` (link sibling reference docs), `## Provenance`.
   - **Reference** (`references/<slug>.md`): the actual table / taxonomy / rubric / checklist the
     entry names, plus a Provenance line. No `## Procedure` (that is what makes it a reference).
3. **Set frontmatter** to `authored-doc-v1`: `name`, `kind`, `status: ready`, and `provenance`
   (`principles`/`claims`/`source_anchors` — real IDs; empty arrays are valid at Tier 0).
4. **Respect rights + faithfulness.** `distillation-only` source → no verbatim (quote-scan must
   stay green). No statement stronger than its evidence (faithfulness check).
5. **Remove the stub markers** (`STATUS: STUB`, `TODO: author`) — a `status: ready` body that
   still contains them fails validation.

When **all** skills and references are authored:

6. **Stamp the drift baseline** so Step 9 can detect future staleness:

   ```bash
   python -m tools.subagent_factory.cli stale <slug> --stamp
   ```

   This writes `provenance.authored_from_digest` (a sha256 over each body's cited principle +
   claim statements) into every `ready` doc. Deterministic; run it as the final authoring step.
7. Run `python -m tools.subagent_factory.validate_skill_authoring subagents/<slug>` (no FAIL),
   `quote_scan`, and faithfulness. Only then set profile `status: ready`, bump `agent_version`,
   add a CHANGELOG entry, and re-export the adapter (`cli export <slug>`).

## Output

Authored `skills/<slug>/SKILL.md` + `references/<slug>.md` bodies and a package promoted to
`status: ready`. Must pass `cli validate <slug>` (the gate runs `validate_skill_authoring`
status-gated: with `status: ready`, every stub remaining is a FAIL).

## Caveats

- **Derive, do not invent.** A Tier 1+ body must trace to the principle/evidence it cites in
  `provenance`. The validator proves shape + mapping; faithfulness + quote-scan guard substance.
- **Author the agent one file at a time** via the `skill-author` agent (its `Write` is locked to
  the single target file). The `status: draft → ready` flip is done here, under the gate — never
  by the per-file agent.
- **Opt-in.** Default authoring runs at release / on request, not on every campaign PDF (cost:
  one LLM pass per skill + reference).
- **`stale`** status (source drift, Phase 12) re-opens a body for re-authoring; clear it by
  re-running this skill.
