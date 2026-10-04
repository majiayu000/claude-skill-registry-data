---
name: sdlc-srs
description: Invoked explicitly by /srs. Produces the software requirements specification — functional, non-functional and AI requirements, data and interface contracts — together with the executable Gherkin acceptance criteria, one feature file per use case. The SRS and its feature files are generated and gated together.
argument-hint: "<FEAT-ID>"
disable-model-invocation: true
---

# /srs — requirements + executable acceptance criteria

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

**Phase inputs** — phase `srs`, gate `G2`, input `{{paths.prd_dir}}/PRD-{FEAT-ID}-*.md`,
templates `{{paths.templates_dir}}/srs.md` and `{{paths.templates_dir}}/feature.template`,
outputs `{{paths.srs_dir}}/{FEAT-ID}/SRS.md` **and**
`{{paths.bdd_dir}}/{domain}/{UC-ID}.feature`.

---

## The two halves

The user asked for an SRS; the executable half is Gherkin. They are not competitors —
one contains the other:

- **`SRS.md`** is the prose half: requirements with IDs, data contracts, interfaces.
  This is what a person reviews and what the tech design answers.
- **`{UC-ID}.feature`** is the executable half: one `Scenario` per SC-ID. This is what
  traceability, test-case generation and acceptance execution consume.

They are produced by this one command and gated together. A feature file generated
separately from its requirements drifts from them within one iteration — which is why
there is no separate `/generate-bdd`.

**They live in different trees** (`docs/srs/` and `specs/bdd/`), so §8 of the SRS is the
only link between them. Every path in that column must be exact and must resolve; gate
G2 C2 checks each one.

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.srs`. Act on its verdict:

- `NO_SOURCE` — no PRD. Report how to create one and **stop**.
- `NOT_READY` — the PRD is missing something an SRS cannot be written without: no use
  case with a UC-ID, no acceptance bullets, an unanswered question marked `blocks: srs`,
  or (for AI features) no quality bar and no ceilings. Report each gap with its file,
  section and owning role, and **stop**.
- `PARTIAL` / `READY` — proceed, carrying any non-blocking gap forward as a `TBD`.

**This is the handoff point between two people**, so it matters that the check is on the
document rather than on framework bookkeeping. A Tech Lead can run `/srs` against a PRD
that never went through `/prd` — one written in an editor, or generated and then edited
by the PO. `G1` may read `unknown`; that is fine. The input check re-derives what it
needs from the PRD as it stands today.

What the check will not do is let you proceed on a PRD that cannot support an SRS. When
it stops, the report says exactly which section is missing and that the **PO/BA** owns
it — hand that back rather than filling it in yourself, because a Tech Lead inventing an
acceptance criterion is a product decision made by the wrong person.

## Step 2 — Write requirements

**Functional (`FR-{n}`)** — one testable statement each, MUST or SHOULD, mapped to a UC.
If a sentence contains "and" joining two behaviours, it is two requirements.

**Non-functional (`NFR-{n}`)** — every one carries a number: p95 latency, throughput,
availability, retention, cost per request. Gate G2 C5 rejects "fast", "reliable",
"scalable". A non-functional requirement without a number cannot fail, so it cannot pass.

**AI (`AIR-{n}`, when `ai_class != none`)** — each must be measurable **by the eval
suite**, and each names the metric that will measure it: output schema validity rate,
groundedness or faithfulness score, refusal rate, maximum output tokens, hallucination
tolerance. Translate the PRD's user-terms quality bar into these; that translation is the
whole point of this section.

**Data** — entities touched, new fields, retention, PII. Use the core entities catalog
for names and types.

**Interfaces** — exact signatures, request and response schema names, error codes.

## Step 3 — Write scenarios

Per use case, decompose into scenarios `{UC-ID}-SC{n}`: the happy path, each meaningful
alternate path, each error path, and the boundary conditions the NFRs imply.

Every Feature carries `@feat: @uc: @domain: @req:`. Every Scenario carries `@sc:`,
`@level:` and `@oracle:`, plus `@prompt:` when the behaviour comes from a model. The full
tag contract is in `.agent/rules/traceability.md`.

Choosing `@level:` and `@oracle:` here is a real decision, not bookkeeping — it
determines which test phase owns the scenario and how it can be asserted:

| `@oracle:` | Means | Typical level |
|---|---|---|
| `exact` | one correct answer, compared literally | unit |
| `schema` | shape and constraints, not exact content | unit / acceptance |
| `similarity` | close enough to a reference | eval |
| `judge` | a rubric scored against written anchors | eval |

For model behaviour, prefer the strongest oracle that is actually valid. Assert structure
where you can (`schema`) and reserve `judge` for what genuinely needs judgement — a
judge-scored assertion can only ever gate on regression, never on an absolute value.

**Write behaviour, not implementation.** No HTTP verbs, table names, function names or
class names in Given/When/Then. A scenario that mentions `POST /v1/summaries` cannot
survive a refactor that was supposed to be invisible.

Every FR and AIR must be referenced by at least one scenario's `@req:` tag — gate G2 C4
checks this as rule T6.

## Step 4 — Write the §8 index

One row per scenario: `UC-ID | SC-ID | Title | Level | Oracle | Feature file path`.

This table is the join between the two trees. Verify each path exists after writing.

## Step 5 — Generate

More than 3 UCs, or a PRD over 300 lines → `.agent/steps/spawn-agent.md`: one
`spec-writer` per UC, each producing its requirements rows, its index rows and its
`.feature` file. Otherwise write directly.

The orchestrator writes the surrounding sections, checks 1:1 UC↔feature coverage across
the whole set, and runs the gate. A subagent cannot check coverage — it only sees its
own unit.

## Step 6 — Evaluate G2 and record

Run `.agent/gates/G2-srs.yaml`. Update state: `phase: srs`, the SRS artifact and hash,
the `features` list, the verdict and `input_hash`.

## Amending an existing SRS

When the loop routes back here:

1. **Append, never renumber.** Existing FR/SC ids are referenced by code tags, tests and
   trace rows.
2. Write the change into **§10 Change log**: date, the RF-ID that caused it, and what
   changed. This is what makes a later reader able to tell a clarification from a
   silent redefinition.
3. Changing a scenario's steps changes its `spec_hash`, which marks every downstream
   artifact stale. Run `/sdlc --blast {FEAT-ID}` first to see the scope before
   regenerating anything.

---

## Boundaries

- **Do not design.** No layers, no classes, no libraries, no database choices — that is
  the tech design. The SRS says exactly-what; the tech doc says how.
- Do not write test code or test cases. Scenarios are specifications; the catalog comes
  later from them.
- Do not invent a requirement absent from the PRD. New scope routes back to `/prd`.
- Do not soften a requirement to make it easier to implement. If it cannot be met, that
  is a finding routed to `techdoc` or `prd`, not a quiet edit here.
