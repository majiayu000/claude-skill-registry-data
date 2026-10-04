---
name: sdlc-techdoc
description: Invoked explicitly by /techdoc. Produces the technical design for a feature — component map, data model, interface specs, sequences and error handling against the project's stack profile — assigns a test level and oracle to every scenario, drafts ADRs for hard-to-reverse decisions, and for AI features writes the prompt spec and eval-set spec.
argument-hint: "<FEAT-ID>"
disable-model-invocation: true
---

# /techdoc — technical design

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

**Phase inputs** — phase `techdocs`, gate `G3`, inputs
`{{paths.srs_dir}}/{FEAT-ID}/SRS.md` + its feature files, template
`{{paths.templates_dir}}/techdoc.md`, output
`{{paths.tech_docs_dir}}/{FEAT-ID}/TD-{FEAT-ID}.md`.

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.techdocs`. Act on its verdict:

- `NO_SOURCE` — no SRS. Report how to create one and **stop**.
- `NOT_READY` — typically: an NFR written as an adjective rather than a number, a use
  case with no `.feature` file, or a §8 path that does not resolve. Report and **stop**.
  A design cannot be judged against "should be fast".
- `PARTIAL` / `READY` — proceed.

A hand-written SRS is a valid input. `G2` reading `unknown` is not a reason to refuse.

Read the SRS, every `.feature` in scope, the core entities catalog, and the merged stack
profile's `layers`, `layout`, `architecture.key_rules` and `coding_standards`.

**Read the existing code** for every area you will touch. A design that ignores what is
already there produces a second way of doing something the codebase already does once.

## Step 2 — Approach and alternatives

State the chosen approach and at least one rejected alternative, each in a paragraph,
each with the reason. If there was genuinely no alternative, say that — but check
first, because "no alternative" usually means the option space was never opened.

## Step 3 — Component map

A table: `Component | Layer | File path | Implements (UC/SC/FR ids) | New/Changed`.

Layers come from the profile's `layers`; paths from `layout.source_root`. Every in-scope
UC must appear somewhere in the `Implements` column, and every row must have a non-empty
`Implements` cell — gate G3 C1 checks both. A component that implements nothing is
either dead on arrival or evidence of a missing requirement.

This table is what `/gen-code` builds from, and what the reviewer checks reality
against, so file paths must be exact rather than approximate.

## Step 4 — Data, interfaces, sequences, errors

- **Data model changes** — new entities and fields with types, and a migration plan.
  Gate G3 C3 blocks a schema change with no migration plan.
- **Interface specs** — exact signatures, request and response type names, status or
  error codes. Use the wrapper and base exception named in the profile's
  `coding_standards`.
- **Sequence per UC** — numbered steps or a diagram, covering the error path as well as
  the happy path.
- **Error map** — which failure produces which exception and which user-visible result.

## Step 5 — AI design (when `ai_class != none`)

Read `.agent/modules/ai-llm/stack-profile.yaml` and write:

- **Prompt(s)** and the **version bump decision** — `patch` (wording only), `minor`
  (behaviour change, same output contract) or `major` (output contract change). Major
  requires an ADR and a consumer migration plan.
- **Model, parameters, fallback provider** and when the fallback engages.
- **Pattern** — one of `rag | chain_of_thought | few_shot | multi_agent`. Naming it
  explicitly lets the reviewer check the prompt against that pattern's structure instead
  of forming an opinion from scratch.
- **Token and cost budget per call**, plus p95 latency. These mirror the SRS `NFR`s and
  become gate checks at G5b.
- **Guardrails** — input validation before the provider call, PII policy, injection
  defences, output validation. Put rejection before the call: an input you were always
  going to refuse should not cost a token.
- **Retry and timeout** behaviour.

Then write two documents:

- `{{paths.prompt_spec_dir}}/{name}/PS-{name}.md` from
  `{{paths.templates_dir}}/prompt-spec.md` — created once per prompt **name** and
  amended thereafter, never duplicated per version. Its version-history table is the
  record of what each version changed and what it scored.
- `{{paths.eval_spec_dir}}/EVAL-{name}.md` from
  `{{paths.templates_dir}}/eval-set.md` — the metrics with **numeric thresholds**, the
  judge rubric with written anchors if a judge is used, and the baselines table.

## Step 6 — Test strategy (§9) — the contract that splits the test phases

A row for **every SC-ID in scope**: `UC/SC | Level | Oracle | Notes`.

Gate G3 C2 blocks if any scenario is missing. This is deliberate: deciding level and
oracle at design time is what lets `/gen-testcase`, `/unittest` and `/run-test` split
cleanly instead of each improvising. Improvised levels are how everything drifts into
one slow integration suite.

Levels: `unit`, `integration-mocked`, `integration-live`, `acceptance`, `eval`.
Oracles: `exact`, `schema`, `similarity`, `judge`.

Carry forward the `@level:` and `@oracle:` chosen in the SRS. If you disagree with one,
change it here **and** say so — do not leave the two documents contradicting each other.

## Step 7 — ADRs

Draft an ADR under `{{paths.adr_dir}}` for every trigger, using
`{{paths.templates_dir}}/adr.md`. Triggers are the list in `CLAUDE.md` plus, for AI
work, `ai_conventions.adr_triggers` — new provider or model family, major prompt bump,
sampling defaults that affect determinism, introducing RAG or changing embeddings or
chunking, adopting a judge as a blocking gate, setting or raising a cost budget, adding
an agentic tool loop, or sending user data to a third party.

Number sequentially from the existing files. Status `Proposed`. AI ADRs carry a
`Cost impact:` line. Gate G3 C4 blocks if a raised trigger has no file.

**Draft at `Status: Proposed`, and list them.** Never write `Accepted` yourself. These
are the decisions that are expensive to reverse, which is why they are written down
rather than made in passing — a person accepts them by editing the Status line in the
file. Report each drafted ADR by path so whoever owns the decision can find it.

If a decision genuinely cannot be made from the SRS — two viable providers with no stated
constraint to choose between them — write the ADR with both options under Alternatives,
leave Decision as `TBD (Q<n>: …)`, and list it. An ADR that records an open choice is
useful; one that invents a rationale for an arbitrary pick is worse than none.

## Step 8 — Evaluate G3 and record

Run `.agent/gates/G3-techdoc.yaml`. Update state: `phase: techdocs`, the techdoc
artifact and hash, `scope.prompts`, `scope.entrypoints`, the prompt and eval spec paths,
the ADR paths, the verdict and `input_hash`.

---

## Boundaries

- **Do not write implementation code.** Interface signatures and short illustrative
  snippets belong here; working code does not. `/gen-code` builds from this document,
  and a design containing the implementation has skipped its own review.
- Do not add a requirement. If the design reveals a missing one, that is a finding
  routed to `srs`.
- Do not choose a new dependency, database or provider without an ADR.
- Do not weaken an NFR because it looks hard. If it cannot be met, say so and route the
  finding to `prd` — that is a product decision, not a design one.
