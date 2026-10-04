---
name: Qplan
description: "Use when starting or resuming a Plan. Runs bounded tacit-knowledge intake when needed, creates or updates a roadmap, then advances one verified Goal at a time. Use Qgoal only as a goal-intake alias."
user_invocable: true
recommendedModel: opus
tier: core
---

> **Planning state → DB:** `.qe/planning/**` is a DB-only namespace in the
> SQLite `qe_files` store. Its directories are logical paths, not folders to
> create on disk. Read them with `node scripts/qe-cat.mjs <path>` (or
> `--ls`/`--exists`) and mutate them only through QE state/store utilities.
> See `QE_CONVENTIONS.md`.

# Qplan — Plan-owned Goal Controller

`Qplan` is the user-facing control surface for work. A Plan owns an ordered
Goal queue; Goals are not separate user commands. The user supplies an intent,
reviews material Plan changes, and receives results. QE runs the internal work.

Qplan is an explicit high-assurance entry. Only active-prefix `$Qplan`/`/Qplan`
or the `$Qgoal`/`/Qgoal` alias activates Full SIVS. Ordinary requests use the
native client execution path while the Safety Kernel and QE response style stay
active; prompt size, file count, and risk words never activate this workflow.

## Model

```text
Plan → Goal 1 → Goal 2 → … → Goal N
          │
          ├─ knowledge preflight
          ├─ assurance lane (bounded micro contract | formal spec)
          ├─ execute
          ├─ verify
          └─ verified knowledge write-back
```

- **Plan** is the durable contract: roadmap, requirements, phases, and ordered Goals.
- **Goal** is the smallest independently verifiable Plan outcome.
- Canonical `.qe/` document rows in `qe.db` are evidence; derived index tables and
  `.qe/wiki/` projections are lookup/knowledge layers. Do not treat an index row
  or LLM summary as the source of truth.
- Only a verified Goal with explicit evidence may write back to the wiki.

## Deterministic tacit-knowledge intake

For a broad or ambiguous intent, Qplan owns one durable intake before it
finalizes execution artifacts. This is a bounded decision-discovery stage, not
an invitation to interview the user about facts already available in the
repository.

1. **Reconnaissance first:** inspect the minimum relevant sources and record
   source facts. Build a canonical base-question inventory only for unresolved
   decisions, with stable ordinals and material dimensions from
   `core/KNOWLEDGE_ELICITATION_CONTRACT.md`.
2. Initialize `.qe/planning/plans/{slug}/INTAKE.json` with
   `node scripts/qe-intake.mjs init`, the current full session UUID, and the
   inventory JSON. Before asking, disclose the actual base total, the maximum
   12 allocated follow-ups, and the maximum batch size of 3.
3. Run `node scripts/qe-intake.mjs next` with the stored revision. Render only
   the returned batch through `core/INTERACTION_ADAPTER.md`; preserve engine
   labels such as `[17/30]` and `[17-1/3]` exactly. Persist every answer, skip,
   correction, pause, resume, re-baseline, or stop through the CLI using the
   returned revision. Never hand-edit counters or `INTAKE.json`.
4. When no material question remains, run the CLI `synthesize` operation and
   show the synthesis to the user. Persist corrections or a material
   re-baseline, and run `confirm` only after the user accepts the synthesis.
5. A pause preserves the earliest unresolved label and returns control to the
   user. A stop persists a blocked terminal. Do not convert either state into
   an inferred answer.

Interactive Claude and Codex sessions ask the same labeled open questions and
wait for answers. In non-interactive mode, skip only a question that the engine
classifies as explicitly reversible and non-material; record that resolution
as an assumption. If any material question remains, retain the intake draft,
report the earliest unresolved label, and block Plan finalization without
fabricating an answer.

The intake may be omitted only when reconnaissance proves that the intent is
already bounded and has no unresolved material decision. Record that reason in
the Plan decision log; convenience or non-interactive execution is not a
bypass. Qplan is the sole owner of this stage. Qgoal and downstream PSE stages
must not duplicate its questions, counters, or transitions.

## Entry and bootstrap

1. Ensure the shared `QE.md` and active-client instruction pointer exist before planning.
   The explicit `/Qplan` or `$Qplan` entry bootstrap creates them without overwriting user
   instructions. Then check `.qe/`; if it is absent, bootstrap the minimal
   Plan state (`.qe/state/`, `.qe/planning/`, and `.qe/tasks/`) through the existing QE
   state/store utilities before continuing. Initialization is part of Qplan; there is no
   separate initialization skill or user command.
2. Derive a unique slug from the intent (2–4 salient Latin keywords, lowercase
   `[a-z0-9-]`, max 40 chars; append `-2`, `-3` on collision).
3. Run the deterministic intake above when the intent is broad, ambiguous, or
   has an unresolved material decision. Reach `confirmed`, or block and return
   without finalizing a Plan. A bounded intent with no material gap may use the
   documented omission path.
4. Only after confirmed intake (or a recorded safe omission), build the exact
   input from `core/PLAN_INITIALIZATION_CONTRACT.md` and run
   `node scripts/qe-plan.mjs init --slug {slug} --session {full UUID} --input {path}`.
   This atomically creates the DB-authoritative Plan documents, Goal ledger,
   active pointer, and session binding. Do not write canonical planning paths
   with raw filesystem tools. Full Plans must divide work into ordered,
   independently verifiable Wave bullets; these become Goals. Split until every
   Goal has one user-visible outcome, 1–5 allowed paths, at most three criteria,
   at most two journeys, explicit dependencies, and explicit non-goals. A broad
   feature area is a Phase, never a Goal.
5. For every Goal, select its assurance lane after reconnaissance and before
   activation. A bounded micro Goal includes the exact admission request from
   `core/GOAL_ACCEPTANCE_CONTRACT.md`; the ledger replaces it with a session-
   and digest-bound plan-controller admission. Otherwise omit `assurance` and
   use the formal lane. Then define the pre-execution acceptance contract from
   `core/GOAL_ACCEPTANCE_CONTRACT.md`: schema 2 with exactly one structured outcome,
   the same `outcomeId` on every requirement, journey, regression, and alignment,
   verbatim Goal alignment, requirement criteria,
   at least one runnable user-journey scenario, a regression command, risk assessment,
   and whether human acceptance is required. High-impact risk categories (authentication,
   authorization, payment, deployment, data migration, destructive data changes, external
   integrations, or security) require human acceptance.
   Save it as `evidence/{goalId}.acceptance.json`, then run
   `node hooks/scripts/lib/ledger.mjs set-acceptance --slug {slug} --goal-id {goalId} --file {path}`.
   Stored schema 1 contracts may resume, but never create a new schema 1 contract.
   Do not let tests or implementation retrospectively define what success means.
6. On resume, run `node scripts/qe-plan.mjs bind --slug {slug} --session {full UUID}`; if an active Goal's prior session ended, use the explicit CAS `takeover` protocol in `core/PLAN_INITIALIZATION_CONTRACT.md`.
7. Run `node hooks/scripts/lib/ledger.mjs render-state --slug {slug}`. Never hand-edit
   the `## Phase Progress` block.

## Internal Goal loop

Run this loop until the Plan is complete, blocked, or needs a material user decision.
Do not expose `Qgenerate-spec`, `Qexecute`, derived-wiki internals, or a copied next-command handoff.

1. **Select:** Run `node hooks/scripts/lib/ledger.mjs advance --slug {slug} --action next --session {current full session UUID}`.
   It starts only the first pending Goal and binds that Goal to the execution-owner
   session. An active or blocked Goal prevents skipping, and another live session
   cannot continue, block, fail, or complete the owned Goal.
2. **Knowledge preflight:** Run `node scripts/qe-plan-context.mjs "{Goal objective}"`.
   Then run `node scripts/qe-analysis-drift.mjs --json`. When it reports
   `actionRequired: true`, generated analysis is advisory-only for the returned
   `affectedPaths`: read the live source in those paths before planning, execution,
   or verification. Drift detection is non-blocking and a missing baseline does not
   fail the Goal; it only removes analysis freshness as usable evidence.
   Use the returned reviewed wiki entries and QE artifact paths as pointers. Read only
   the source documents required for the Goal; source files override summaries.
3. **Assurance lane execution:** consume the immutable lane selected and
   ledger-validated before activation; prompt length alone never decides it.

   **Bounded micro-Goal lane** applies only when all conditions hold: one low-risk
   implementation outcome, at most three allowed paths, fewer than three work
   items, no unresolved material decision, and no authentication, authorization,
   payment, deployment, migration, destructive-data, security-boundary, or external-
   integration impact. The stored contract must contain the ledger-issued
   `assurance` admission defined by `core/GOAL_ACCEPTANCE_CONTRACT.md`; absence
   or rejection means the formal lane. The immutable Goal
   acceptance contract is the executable micro spec. Do not create a TASK_REQUEST
   or run the three-reviewer Spec gate. The ledger seals a Git scope baseline at
   admission and rejects evidence or completion when observed changes escape
   `allowedPaths`; without a Git worktree the bounded-micro lane is unavailable.
   Execute in the main thread or one bounded worker, apply the Qexecute TDD gate,
   run the locked commands, and retain the distinct-session independent machine
   verification and Goal-alignment verdict required by Step 4. Do not run a
   separate Supervise fan-out unless changed risk evidence requires escalation.

   **Formal Goal lane** applies otherwise. Generate the Goal's TASK_REQUEST and
   VERIFY_CHECKLIST, execute it, then run the complete SIVS verification loop.
   These are internal units, not user commands.

   After implementation and before verification, rerun
   `node scripts/qe-analysis-drift.mjs --json`. If the Goal introduced actionable
   structural drift, include the returned paths in live-source verification and do
   not claim that the generated analysis map is current. This advisory check never
   substitutes for the locked regression and Goal-alignment gates.

   If a micro Goal grows beyond any limit, reveals a high-impact risk, or fails
   verification, do not mutate its immutable acceptance. Stop before expanded
   work, block it through the audited Goal transition, and create a new linked
   formal Plan/Goal with a fresh acceptance contract and dependency on the
   blocked micro Goal. The original micro Goal cannot later claim completion.
4. **Completion evidence:** Before completion, record `evidence/{goalId}.completion.json`
   against the immutable acceptance contract. It must show every requirement and
   user-journey scenario passing, a passing regression result, machine re-execution by a
   named verifier, that verifier's Goal-to-evidence alignment verdict, known limitations,
   and required human acceptance. Run every
   locked contract command via `ledger.mjs run-evidence` first for `implementation`
   and again from a distinct QE session for `verification --verifier {identity}`;
   then run `record-evidence`.
5. **Gate:** If verification fails, evidence is incomplete, or a required decision is unresolved, keep the Goal
   active or call `advance --action block --evidence "{specific blocker}" --session {owner UUID}`; do not start
   another Goal. Ask the user only for a material scope, risk, or irreversible choice.
6. **Complete:** Only after the acceptance evidence has been recorded, run
   `node hooks/scripts/lib/ledger.mjs advance --slug {slug} --action complete --session {owner UUID}`.
   Formal Goals are accepted only when a Goal-bound SIVS controller has already
   reached `complete` with matching TASK_REQUEST, VERIFY_CHECKLIST, Verify, and
   Supervise proof. This records the lifecycle event, updates STATE, and writes a
   provenance-linked reviewed project-wiki page.
7. Repeat at Step 1. When `advance --action next` returns `complete`, report the Plan
   outcome, remaining risks, and evidence.
8. At each completed Phase boundary, `advance next` requires the sealed proof
   from `core/PHASE_RETROSPECTIVE_CONTRACT.md`. Run `node scripts/qe-plan.mjs
   retrospective --slug {slug} --session {full UUID} --input {path}`; it generates
   the Phase report, executes fresh regression, and records the retrospective.

## Goal quality rules

- One active Goal at a time. A safe parallel Wave is internal execution within
  that Goal; it never creates multiple active Goals.
- A Goal must state its verbatim objective alignment, one primary outcome, bounded file scope, explicit non-goals, dependencies, at most three requirement criteria, at most two user-journey scenarios, regression scope, risk assessment, and evidence before work starts.
- Draft plans, model hypotheses, and unverified research never become reviewed project knowledge.
- Use source-backed contracts, tests, verification reports, and decisions as first-class evidence.
- Preserve an append-only ledger. Do not rewrite prior Goal events or fabricate completion.

## User communication

At Plan creation or material replan, show the ordered Goal list, current Goal, success criteria,
and any required decision. During normal progression, report concise status rather than internal
commands. On completion, provide the evidence-backed Plan result.

## Will

- Create, resume, and advance Plan-owned Goals.
- Use QE knowledge internally before each Goal and write back only verified outcomes.
- Run internal spec, execution, and verification units without user command choreography.

## Will Not

- Ask the user to invoke internal PSE stages, derived-wiki internals, or a raw ledger command.
- Skip an active or blocked Goal.
- Mark a Goal complete from a bare test claim, implementation report, or self-verification.
- Promote LLM-generated text to reviewed knowledge without verification evidence.
