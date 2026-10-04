---
name: sdlc-prd
description: Invoked explicitly by /prd. Turns a feature request into a product requirements document with numbered use cases (UC-IDs), measurable success metrics, scope boundaries, and — for AI features — the quality bar stated in user terms. Fans out one spec-writer agent per use case when the feature is large.
argument-hint: "<FEAT-ID>"
disable-model-invocation: true
---

# /prd — product requirements

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

**Phase inputs** — phase `prd`, gate `G1`, input `{{paths.product_dir}}/{FEAT-ID}-*.md`,
template `{{paths.templates_dir}}/prd.md`, output
`{{paths.prd_dir}}/PRD-{FEAT-ID}-{slug}.md`.

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.prd`. Act on its verdict:

- `NO_SOURCE` — no intake document exists. Report how to create one and **stop**.
- `NOT_READY` — the intake exists but a blocking requirement is unmet (no concrete
  problem, no numeric success signal, no AI classification). Report the gaps by file and
  section and **stop**. Do not write a PRD around them: the answers change the use case
  list, so a PRD written first would have to be thrown away.
- `PARTIAL` / `READY` — proceed.

**Do not require that `/feature` ever ran.** An intake document a PO wrote by hand, or
one `/feature` generated and the PO then edited, is an equally valid input. What matters
is the content, which the input check already judged.

Read the intake document, the business dictionary and the core entities.

## Step 2 — Carry the open questions forward

Any question in the intake marked `blocks: prd` that the input check classed
non-blocking travels into the PRD as a `TBD (Q<n>: …)` marker plus a row in §10, with the
owning role. Never resolve one by guessing — an invented answer becomes a requirement
nobody agreed to, and it is indistinguishable from a decided one three weeks later.

## Step 3 — Derive use cases

A use case is **one goal, one actor, one outcome**. Split when the actor changes, when
the outcome changes, or when one half could ship without the other.

Number them `{FEAT-ID}-UC{n}` in priority order. Each gets a row in the §6 table and its
own subsection headed exactly:

```
#### {FEAT-ID}-UC{n}: {name}
```

**That heading format is load-bearing.** `.agent/steps/spawn-agent.md` scans for it to
enumerate work units, and gate G1 checks it. Do not restyle it.

Assign `P0` (the feature is pointless without it), `P1` (expected, can follow), or `P2`
(nice to have). If everything is P0, the scope is wrong — say so.

## Step 4 — Success metrics

Every metric needs four cells: metric, baseline today, target, and **how it will be
measured**. A target with no measurement method is a wish; the fourth column is what
makes it checkable later.

Carry the intake's success signal forward as the primary metric.

## Step 5 — AI product section (when `ai_class != none`)

This section is what the SRS turns into measurable `AIR-` requirements, so vagueness
here becomes unmeasurable quality later. State:

- **Capability** — what the model does, in one sentence
- **Quality bar in user terms** — what "good enough" means to the person reading the
  output, before anyone converts it into a score
- **Human-in-the-loop policy** — reviewed before use, reviewed after, or fully
  automatic; and who reviews
- **Tolerated failure modes** — which errors are acceptable and at roughly what rate,
  and which are never acceptable
- **Ceilings** — a number for latency and a number for cost per operation

The tolerated-failure-modes line is the one people skip. Skipping it means every model
mistake later gets litigated from scratch.

## Step 6 — Generate

If the feature has **more than 3 use cases** or the intake exceeds 300 lines, follow
`.agent/steps/spawn-agent.md`: one `spec-writer` per use case, then merge. Otherwise
write it directly.

The orchestrator — not any subagent — writes the surrounding sections, merges the use
case subsections, and runs the gate.

Enforce the banned-term list. Use entity names and field names from the core entities
catalog rather than inventing synonyms.

## Step 7 — Evaluate G1 and record

Run `.agent/gates/G1-prd.yaml`. Then update the feature state file: `phase: prd`, the
PRD artifact path and hash, `scope.ucs` with the new UC-IDs, the gate verdict and
`input_hash`, and any new open questions. Update `current.yaml`.

If the verdict is `revise` or `block`, list the failing checks and stop.

---

## Boundaries

- **Do not design the solution.** No endpoints, no schemas, no layer names, no library
  choices. The PRD says what and why; the SRS says exactly-what; the tech doc says how.
  A PRD that names a database has foreclosed a decision nobody made deliberately.
- **Do not write Gherkin.** Acceptance criteria here are prose bullets. Executable
  scenarios are the SRS phase's output, and writing them early means writing them twice.
- Do not invent a metric the user did not agree to. Record it as an open question.
- Do not renumber existing UC-IDs when amending an existing PRD. Append new ones —
  trace rows, code tags and tests already point at the old numbers.
