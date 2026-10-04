---
name: profile-generation
description: "Generate or update a package's profile.yaml and provenance-ledger.md from interrogation records — Phase 5 of the authoring cycle. Use when interrogation is complete and the profile (role, when-to-use, modes, quality bar, forbidden behaviours) must be derived or refreshed; normally invoked by the author-subagent pipeline at Step 7, not directly."
---

# Skill: profile-generation

**Purpose:** Generate or update `profile.yaml` and `provenance-ledger.md` from
interrogation records. Phase 5 of the authoring cycle.

---

## Input

- Interrogation record(s) from source-interrogation
- Subagent package path `subagents/<slug>/`
- Source metadata from `sources/metadata/`

---

## Steps

### 0. Apply importance ranking (Phase 2.5 gate)

Before deriving any field, confirm the candidate units were scored and filtered:

```bash
python -m tools.subagent_factory.score_extracted_units <units.yaml>
```

Derive profile content only from `keep` units. Route `discard` units to the
provenance ledger only. Resolve `review` units with a human decision before use.
Exit non-zero means malformed scores — fix before continuing.

### 1. Resolve profile fields

Apply derivation rules from Phase 5:

| Field | Rule |
|-------|------|
| `slug` | kebab-case, role-based, already established |
| `display_name` | From Q1 — explicit role label or synthesized |
| `role` | One sentence: what, to what, for what reason |
| `router_description` | The string the runtime routes on — see below. Required whenever the agent has >2 triggers, >1 exclusion, or a sibling it hands work to |
| `when_to_use[]` | Q3 triggers as caller-observable situations (3–6) |
| `when_not_to_use[]` | Q4 exclusions (2+) |
| `inputs.required[]` | Q5 first required artifact/scope |
| `outputs.primary_format` | Q6 canonical deliverable noun |
| `quality_bar[]` | Q7 rewritten as falsifiable checks (3–5) |
| `supported_modes[]` | Q9 only modes with evidence |
| `handoff_rules[]` | Q8 downstream owner |
| `canonical_owner` | Q8+Q17 |
| `forbidden_behaviours[]` | Q10 do-not rules |
| `minimum_useful_output` | Q11 |
| `source_of_truth_policy` | Q8+Q17 |
| `knowledge_partition.*` | Q12–Q16 |
| `examples[]` | **2 worked few-shot examples** (see below) — one `happy-path`, one `failure-recovery` |

**`router_description` (author this — it is the routing signal).** The adapter's frontmatter
`description` is the *only* text the runtime sees when deciding whether to invoke this agent; skills,
principles, and the quality bar are invisible at routing time. Without `router_description`,
`export_claude_agent` composes that string mechanically as
`role — Use when: <trigger[0..1]> — Not for: <exclusion[0]>`, keeping **only the first two triggers
and the first exclusion**. Every later domain and every sibling hand-off is silently dropped, so the
agent under-fires on its own remit and never routes work to its siblings.

Write one tight paragraph (aim ~250–500 characters) that names:

1. the **full remit** — every `when_to_use` domain, compressed, not just the first two;
2. the **advice-only boundary** — what it does *not* do (advises/reviews vs. performs);
3. every **sibling route** — "not for X, which belongs to `<sibling>-advisor`".

It is **excluded from the body-word budget** (like `examples[]`), so completeness costs nothing
there. Phase 8 check 19 (`router-description`) WARNs when it is absent and the composed fallback
would drop scope, and names exactly what is lost.

**`examples[]` (author these — they were a dormant slot until now).** Two grounded worked examples
that show the agent's behaviour, derived from the interrogation you already have:

- one **`happy-path`**: a core `when_to_use` task → the ideal in-role response (what a good answer
  covers, anchored to `quality_bar`/`minimum_useful_output`);
- one **`failure-recovery`**: a `when_not_to_use` / `forbidden_behaviours` request → the agent
  declines, says why it is out of scope, and hands off per `handoff_rules`.

Shape (each item):

```yaml
examples:
  - title: <short label>
    kind: happy-path          # or: failure-recovery
    scenario: >-
      <the situation the caller brings>
    ideal_response: >-
      <a sketch of the correct in-role response>
```

The validator requires **≥1 `failure-recovery`** whenever any example is present (A4), so always
author both. Examples are **excluded from the body-word budget** (they are few-shot data, not rules)
and render into the adapter's `## Worked examples` section on export.

If the source justified a `purpose-review` pattern (see source-interrogation),
embed the `purpose_review` mode from `templates/purpose-review-contract.yaml.j2`,
or emit it as `subagents/<slug>/references/purpose-review-pattern.md` and list it
in `knowledge_partition.references[]`.

### 1.5 Regulated-domain no-advice boundary (J-track / Step-15)

If the source's domain is **regulated / high-stakes — finance, legal, or medical** — the package must
ship a graded no-advice boundary, and you must author it from the **deterministic per-domain
template**, not by hand (prompt-only scope control is unstable; the template is the research-validated
method).

1. Set `domain_risk_category: <finance|legal|medical>` in the profile.
2. Fold in the template from `tools/subagent_factory/domain_policy.py` — `domain_policy(<domain>)`
   gives the graded `forbidden_behaviours` (safe-completion: answer the general part → refer to a
   licensed professional, **not** a binary refusal), defer-to-professional `handoff_rules`, a
   `standing_disclaimer`, and the J5 `evidence_norms` (mandatory-citation / answer-from-authority).
   **Read those lines and copy them verbatim** into the matching profile fields (merged with the
   source-derived lines); do **not** paraphrase — paraphrase weakens the boundary and risks the gate.
   Also add the disclaimer as a `handoff_rules` entry so it renders in the adapter. (The manager can
   emit the exact YAML with `python -m tools.subagent_factory.domain_policy <domain>` or preview a
   merge with `--merge profile.yaml`.)
3. **Evidence norms (J5).** Put `domain_policy(<domain>)`'s `evidence_norms` into
   `source_of_truth_policy.evidence_norms` (the citation/authority *discipline* — deterministic). The
   *source-specific* authority and precedence (which work governs, what corroborates) is **LLM-derived
   from Q17** — author it into `source_of_truth_policy.canonical_owner` / `precedence` as for any
   package. (Runtime retrieval-from-authority is Step-14's job; these norms are its contract.)
4. The deferral rule must trigger on an **external** uncertainty signal (scope, missing context,
   jurisdiction), explicitly **not** the model's own confidence — it is worst-calibrated on exactly
   these domains.

This is **enforced**: `validate_generated_package` block #14 FAILs a package that declares a regulated
`domain_risk_category` without the no-advice / defer / disclaimer boundary **and the J5 evidence norm**.
For technical / non-regulated packages, leave `domain_risk_category` unset — the gate stays inert.

### 1.6 Knowledge-partition routing (G1 / Step-14 — advisory)

When you decide what goes in `knowledge_partition.always_on` (distilled, in-prompt) vs
`skills` / `references` (file-backed, read on demand), apply the deterministic routing rule rather
than deciding ad hoc: `tools/subagent_factory/knowledge_partition.py` `route_knowledge_item(reuse,
volatility, size, citation_need)` →

- **distill → `always_on`**: stable + high-reuse + small + non-citable (the rules the expert always
  applies);
- **retrieve → `skills`/`references`**: volatile **or** long-tail (low-reuse) **or** large **or**
  citation-bearing (anything that ages, is rarely needed, is too big, or must cite a real passage).

**Advisory, not a gate.** G1 (own-store vs runtime retrieval) is an open question, so treat the
routing as guidance and confirm by A/B on the package's behaviour-tests before trusting a non-obvious
move — never apply it as a silent default. The full runtime-retrieval spine (G2–G6) is **spec only**
(see `step-14-runtime-retrieval.md`); today "retrieve" means a reference file the agent reads.

### 2. Check profile bloat limits

| Check | Limit |
|-------|-------|
| Total body | Under 800 words |
| Universal rules | Max 12 |
| Rules per mode | Max 3 |
| Procedures in body | No ordered sequence > 2 steps |
| Static tables/checklists | None |
| Platform-specific nouns | Zero |

Move violations to skills or references.

### 3. Write profile.yaml

Use `templates/profile.yaml.j2`. Write to `subagents/<slug>/profile.yaml`.

**YAML-safety rule:** emit every free-text scalar as a folded block scalar
(`>-`). A plain scalar containing a colon-space (`": "`) — e.g.
`- Domain model under review: a diagram` — is parsed as a mapping and breaks the
file. The template encodes this; preserve it when hand-authoring. Constrained
tokens (slug, version, booleans, kebab names) stay inline.

### 4. Write provenance-ledger.md

For every profile field, add a distillation log row:
- field name
- source_id(s)
- QID(s) used
- brief note

Use `templates/provenance-ledger.md.j2`. Write to `subagents/<slug>/provenance-ledger.md`.

### 5. Write CHANGELOG.md

Use `templates/changelog.md.j2`. Write to `subagents/<slug>/CHANGELOG.md`.

### 6. Write README.md

Write brief package README to `subagents/<slug>/README.md`.

### 7. Generate golden tests

Use `templates/golden-tests.yaml.j2`. Write to `subagents/<slug>/tests/golden-tests.yaml`.

### 8. Run Phase 8 self-check

Check #0 is **profile.yaml parses as valid YAML** — verify this first; the
content checks are meaningless on an unparseable file. Then verify the profile
against the remaining Phase 8 checks. Report PASS / WARNING / FAIL.

The authoritative verdict comes from the deterministic
`python -m tools.subagent_factory.cli selfcheck <slug>`, not from a hand
self-assessment. Do not export adapter until that gate returns PASS/WARNING.

---

## Output

- `subagents/<slug>/profile.yaml`
- `subagents/<slug>/provenance-ledger.md`
- `subagents/<slug>/CHANGELOG.md`
- `subagents/<slug>/README.md`
- `subagents/<slug>/tests/golden-tests.yaml`
- Phase 8 self-check verdict
