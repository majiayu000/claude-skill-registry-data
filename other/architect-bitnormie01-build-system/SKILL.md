---
name: architect
description: >
  Use this skill at the very START of any new build, before writing a single line of code, to
  turn a project idea (plus any reference docs) into an approved spec and a set of bite-sized,
  machine-parseable implementation plans that a mastermind/executor agent pool can build
  autonomously. Trigger it whenever the user says "architect this", "break this project down",
  "decompose this", "plan this build", "turn this idea/spec into tasks", or hands over a folder
  of docs and asks how to build it. Do NOT skip this and jump to coding even if the project
  "seems simple" — unplanned builds are where executors drift, duplicate work, and hallucinate
  interfaces.
---

# Architect

## What this is

The architect is the **front-end of an autonomous build pipeline**. It does not write the
product. It turns a fuzzy idea + reference docs into two artifacts the rest of the system can act on:

1. An **approved spec** — the single source of truth for *what* is being built and *why*.
2. A set of **plan documents** — one per independent subsystem — broken into bite-sized,
   test-first tasks, each self-contained enough for an executor with **zero session memory and no
   access to the architect's context** to build it correctly.

It then emits a **task manifest** (see `../references/task-contract.md`) so a mastermind/orchestrator
can load the work into a task DAG and distribute tasks across an executor pool — no copy-paste.

**Announce at start:** "I'm using the architect skill to decompose this project into a spec and
executor-ready plans."

## Why decompose at all

A single executor agent reasons best about work it can hold in context at once. When you hand a
fresh executor "build the prediction-market hook," it invents its own interfaces, picks its own
file layout, and 40 minutes later you have code that doesn't match the next task's assumptions.
When you hand it "Task 3: write the failing test for `OutcomeToken.mintFor(address,uint256)`, here
is the exact signature, here is the file path, here is the command to prove it fails" — it
succeeds, and so does the executor that picks up Task 4. **The plan is what makes a stateless,
rotating pool of executors behave like one coherent engineer.**

## Build on existing skills — do not reinvent

This skill orchestrates a proven chain. Resolution order, per stage:

1. **Installed superpowers skills** — invoke them when the session has them (maintained source).
2. **Vendored copies** — `../references/vendor/superpowers/<skill>/SKILL.md` (pinned snapshot,
   embedded in this repo). When superpowers is not installed, follow the vendored SKILL.md
   **verbatim as a document** — same method, no skill machinery needed.
3. `../references/pipeline-fallback.md` — a condensed checklist of the same flow; a summary to
   keep yourself honest, not a substitute for 1 or 2.

| Stage | Skill to invoke | Vendored fallback | Produces |
|-------|-----------------|-------------------|----------|
| Spec  | `superpowers:brainstorming` (or `brainstorming`) | `../references/vendor/superpowers/brainstorming/SKILL.md` | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` |
| Plans | `superpowers:writing-plans` (or `writing-plans`) | `../references/vendor/superpowers/writing-plans/SKILL.md` | `docs/superpowers/plans/YYYY-MM-DD-<subsystem>.md` |
| Review| plan-document-reviewer prompt (task-contract §4; upstream original in `../references/vendor/superpowers/writing-plans/plan-document-reviewer-prompt.md`) | — | Approved / Issues per plan |

The architect's job is to run them **in order, with the right inputs, and to enforce the
executor-ready output contract** at the end — which vanilla superpowers does not do, because it
assumes same-session subagent execution. You are building for a multi-account, multi-agent pool
instead.

> **Two overrides when you fall back to the vendored skills — follow their *method*, not these tails:**
> 1. **Ignore `writing-plans` §Execution Handoff** — its raw "Which approach?" menu. Execution is
>    governed by the Stage-4 hand-off below instead: Claude-Code-native (the `orchestrator` builds it
>    in-session via subagents) or external-pool (stop at the manifest for a separate kernel).
> 2. **Do not emit `writing-plans`' `REQUIRED SUB-SKILL: superpowers:…` plan header.** That line rides
>    into the plan document and reaches stateless executors that have no superpowers skills. Use the
>    plan header from `../references/task-contract.md` §1 instead.
>
> Likewise the vendored `brainstorming` skill's terminal "invoke writing-plans" step: you sequence the
> stages yourself, so follow its dialogue/method, not its skill-to-skill hand-off. (Recorded in
> `../references/vendor/superpowers/UPSTREAM.md`.)

## The pipeline

Run these four stages in order. Do not start a stage until the previous one is approved.

### Stage 1 — Ingest

- **Resolve the project repo first** (`../references/repo-bootstrap.md`): the kickoff's `REPO:`
  field, else the working directory's remote — never the build-system kit checkout. Sync it and read
  the brief/pack from it. If no project repo exists (the user came straight to you with an idea,
  Steps 0a/0 skipped), create it once the `PROJECT:` line is confirmed:
  `gh repo create <project-slug> --private --description "<PROJECT one-liner>" --clone` — announce
  what you created. If the resolved repo is **pipeline-created and still event-named** (Step 0a ran
  but Step 0 was skipped, so idea-forge's rename never happened), perform that upgrade yourself once
  `PROJECT:` is confirmed — the rename + description commands in
  `../references/repo-bootstrap.md` §The rename step — and report the new name for the runsheet.
  Everything you produce commits there.
- Read the project idea and **every** reference doc the user pointed at (specs, API docs,
  hackathon rules, existing code). If a docs folder was given, list it and read the relevant files
  before asking anything.
- **If a resource pack exists** at `docs/resources/<event>/` (from `resource-extractor`), read it —
  its `sponsors/*` carry the verbatim testnet package/contract addresses, entry-point signatures, and
  integration model to plan against, and `event.md` the exact constraints/deadline. Prefer these
  extracted, sourced facts over re-deriving interfaces; guessed addresses/signatures are the kit's top
  residual risk. The brief's *Feasibility notes for the architect* field points at the specifics.
- Establish: target platform/chain, language/runtime, hard deadline, and any non-negotiable
  constraints. Pull these into the spec header verbatim.

### Stage 2 — Brainstorm into a spec

- Invoke the brainstorming skill. Any reviewer subagent the method dispatches (the spec-document
  reviewer here, the §4 plan reviewer at Stage 4) runs at §Seat settings' reviewer row
  (`../references/model-routing.md`) — per-spawn model, plus per-spawn effort where the Routing
  section shows `per-spawn`; under `routing: inherit` it inherits, and a dispatched architect that
  cannot spawn runs the review inline. Honor its **hard gate**: present
  a design and get explicit approval before any planning. **In an autopilot campaign** (your kickoff
  carries an `AUTOPILOT CAMPAIGN` block — `../references/campaign-contract.md`) the gate survives
  but the approver is the autopilot: answer the brainstorming dialogue's questions **from the locked
  contract and the brief** — recording each as a line in a `Design decisions` section of the spec
  (question → answer → source: contract field / brief field / derived) — then return the design
  summary as your final report for the autopilot's contract-conformance approval; it approves or
  re-dispatches you with concrete corrections. A question neither the contract nor the brief can
  answer is not yours to guess: return BLOCKED with the exact question.
- **Decomposition gate (critical):** if the project spans multiple independent subsystems
  (e.g. contracts + off-chain worker + frontend + deploy), flag it immediately and split into
  sub-projects. Each subsystem gets its own spec→plan cycle. This is why a real build becomes 3–5
  plan files, not one giant one.
- Save the approved spec to `docs/superpowers/specs/`. Get the user to review the written spec
  before moving on (in an autopilot campaign, that reviewer is the autopilot — same
  conformance-approval loop as the design gate above).

### Stage 3 — Decompose into plans

- Invoke the writing-plans skill once per subsystem, feeding it the spec.
- Enforce **bite-sized TDD granularity**: each step is one 2–5 minute action
  (write failing test → run it to confirm fail → minimal implementation → run to confirm pass →
  commit).
- Enforce the **executor-ready contract** from `../references/task-contract.md`. Beyond standard
  writing-plans output, every task MUST also declare:
  - `provides:` — the interfaces/types/exports this task creates (so downstream tasks can name them)
  - `requires:` — the interfaces it consumes from earlier tasks (paste the actual signatures into
    the task body — never assume the executor "remembers" them). **A `Requires:` entry must match
    its provider's `Provides:` entry character-for-character** — the kernel resolves them by literal
    string equality, so copy-paste the signature, never retype or reformat it. A near-match
    silently degrades the executor's context instead of erroring.
  - `effort:` — the reasoning level for this task (`low|medium|high|xhigh|max` — the canonical
    ladder, `../references/model-routing.md`; never `ultracode`, which is a main-session-only
    mode, and never the legacy `none`/`minimal`). You assign
    this because you're the only component that knows each task's difficulty: boilerplate/scaffolding
    `low`, normal feature work `medium`, tricky algorithms or security-sensitive code `high`/`xhigh`
    (`max` is the rare last rung, not a default).
    It's the dispatcher's budget throttle (see `../references/task-contract.md` §6) — don't default
    everything to high. Author it for the task's difficulty only — never raise it to compensate for
    a model; the dispatcher applies each tier's effort floor at dispatch
    (`../references/model-routing.md`), so the plan stays portable.
  - `Model tier:` — the abstract model class (`top|standard|fast`, optional, absent = `standard`;
    `../references/model-routing.md`). Same don't-default-everything-up discipline as effort.
    **Pin rule:** every `human_gate: true`, security-sensitive, or `effort: xhigh|max` task is
    `top` — never write a lower tier on one. `fast` only on provably mechanical `low`-effort work
    (scaffolding, config). Plans never name a vendor model — tiers bind to models at dispatch,
    per campaign.
  - a single **gate** command with expected result (this becomes the kernel's acceptance check)
  - an **exhaustive `Files:` list** — the kernel's commit is scoped to exactly these paths (plus
    lockfiles) and fails the task on any undeclared change, so a forgotten file here makes the task
    unbuildable. Think through every file the implementation touches, including configs and test
    helpers.
  - the **dispatch-control fields where they apply** (manifest level): `human_gate: true` on every
    deploy / key-operation / fund-movement task — the kernel/orchestrator pauses these for a human,
    never auto-runs them — plus, on each such task, the advisory `gate_profile`
    (`deploy|wallet|faucet|account|secret|submission`, `../references/task-contract.md` §2) when the
    category is obvious, so the Step-3 gate-concierge can map tools without re-deriving it;
    `provider` (external-pool only — in Claude-Code-native mode there is one
    provider, so omit it) only when a task genuinely needs a specific pool: the external-pool topology
    is a rotating Codex executor pool plus one strong Claude seat, so leave tasks unpinned by default
    and pin `claude` only for work that truly needs the strong model; `allow_empty: true` only on
    tasks that legitimately change no files (rare — placeholders, verification-only tasks).
- **Emit the README task** (`../references/readme-schemas.md`): pick the schema from its decision
  table (one of R1–R8, by the product's shape) and add one **ordinary** task — late in the DAG,
  after the tasks that create what it documents — whose body names the schema id + version, pastes
  the resolved heading list concrete (plus any event-mandated overlay headings quoted verbatim from
  the pack's `event.md`), and carries `TBD-post-build:<what>` lines for facts that land later
  (deployed addresses, live link, demo video URL — the Step-3 closing pass resolves them). Its
  `Files:` list is `README.md`; its gate is the schema library's conformance check with the resolved
  list, semicolon-joined onto the task's single `Run:` line. No new grammar fields — it is a normal
  task. (Monorepos: one README task per package README as well, schema R8.)
- Apply `../references/conventions.md` (no placeholders, exact paths, complete code, strict-TS rules,
  key-safety rules).

### Stage 4 — Review and hand off

- Run the plan-document-reviewer over each plan (see `../references/task-contract.md` for the prompt).
  Fix any blocking issues inline.
- Generate the **task manifest** (`docs/superpowers/manifest.json`) per `../references/task-contract.md`.
  It is a DAG of tasks with dependencies, files, gate commands, and provides/requires edges — and the
  **only place the `human_gate` safety flags live** (they are not in the §1 plan grammar). Generate it
  by default in *both* configs: it is **required** for external-pool, and the **recommended default**
  for Claude-Code-native because it carries the validated human-gate coverage the orchestrator relies
  on. A native build *may* skip it and have the orchestrator parse plans directly — but then the
  orchestrator must derive human-gating from each task's content itself (`../orchestrator/SKILL.md`),
  so only skip it when the build has no deploy / key / fund-movement tasks.
- **Validate the manifest mechanically before pushing** — a manifest that doesn't validate fails at
  dispatch time, mid-build. Never gate "done" on tooling you may not have; gate it on the checks
  passing. Run whichever is available:
  - **If the kernel checkout is present:** `npm run kernel -- validate --manifest docs/superpowers/manifest.json`.
  - **If it is not** (the kernel is a separate build — see `../README.md`): run the equivalent by hand.

  Either way the manifest must pass **all** of:
  1. **Clean parse + valid DAG** — no cycles; every `depends_on` id exists.
  2. **Zero unmatched `requires`** — every `requires` string found verbatim in a dependency's
     `provides` (literal string equality; see the character-for-character rule above).
  3. **Manifest ⇄ plan equality** — every task's `gate`, `files`, `effort`, `provides`, `requires`,
     and `commit` — plus `model_tier`, present in the manifest iff the plan carries the line
     (a manifest-only value is invalid) — byte-match its plan task
     block. The manifest is a *projection* of the plans, not a
     second draft (`../references/task-contract.md` §2); a drifted field is the one bug the executor
     and kernel can't catch alone.
  4. **Effort present** — every task has an `**Effort:**` line (a missing one silently dispatches at
     `medium`), with canonical values (`low|medium|high|xhigh|max`).
  5. **Human-gate coverage** — every deploy / key-operation / fund-movement task carries
     `human_gate: true` (canonical snake_case; `../references/task-contract.md` §2).
  6. **Model-tier pin coverage** — no `human_gate: true`, security-sensitive, or `effort: xhigh|max`
     task carries an explicit `Model tier:` below `top` (the Stage-3 pin rule;
     `../references/model-routing.md`).

  Fix and re-validate until clean; a manifest that fails any check is not done.
- **Emit the submission draft (hackathon builds).** When the build targets a hackathon (a brief or
  resource pack exists), also write `docs/gates/submission-draft.md` — the platform form,
  pre-answered: every field the event's submission requires (from the pack's `event.md`, verbatim
  where it specifies format) filled from the brief and spec — project name, one-liner, description,
  target track(s)/bounties, tech stack, team. Facts that don't exist until the build lands — demo
  video URL, deployed addresses, live demo link, the public repo URL — are marked
  `TBD-post-build:<what>`, one per line, nothing else deferred. (This is the one artifact where
  deferred fields are correct: they are named build outputs, not vague work — the no-placeholders
  rule for plan tasks is untouched.) The post-build seats resolve the TBDs — `demo-studio` (Step 2.5)
  fills the demo-video URL, the Step-3 gate-concierge resolves the rest at the closing pass and pastes
  the draft into the platform — so submission day is a paste and a click, not authorship under
  deadline.
- **Append the stack requirements to the tollgate report** (campaign builds — when
  `docs/tollgate/*-tollgate.md` exists; skip silently otherwise). You are the only seat that knows
  the project's toolchain: from each plan's Tech Stack header, add one row per required CLI/runtime
  to the report's **Stack requirements** section — name, the version the plans assume, an exact
  probe (`forge --version`, `sui --version`, `pnpm --version`, …), a fix hint
  (`../references/tollgate.md`). The orchestrator probes these at boot, so a missing compiler is
  caught before the first task instead of failing mid-build as a pseudo-flake.
- **Commit and push the whole system to the project repo** — spec, plans, the `manifest.json`
  (whenever you generated one; that is the default — see above), and — hackathon builds —
  `docs/gates/submission-draft.md` plus the tollgate report's appended Stack requirements section
  (when one exists — the bullet above). The project repo is
  the single source of truth (`../references/conventions.md`, `../references/repo-bootstrap.md`);
  the mastermind and executors pull from
  it, so until you've pushed, the system doesn't exist for them. Regenerating later is just another
  commit — agents that boot afterward pick it up automatically.
- **Hand off to the build — two supported configurations; pick per the user's setup:**
  - **Claude-Code-native (default):** the plan is built *in Claude Code itself* by the `orchestrator`
    (`../orchestrator/SKILL.md`) — the main session dispatches a subagent per task, proves each gate,
    and commits. End by confirming the spec/plans (+ the `manifest.json` — the default; + the
    submission draft on a hackathon build) are committed
    and pushed,
    and offer to start the orchestrator (continue here, or a fresh session via
    `../prompts/INVOKE_ORCHESTRATOR.md`) — and remind the user the concierge's preflight pass
    (`../prompts/INVOKE_GATE_CONCIERGE.md`, MODE: preflight) can now run in parallel. No external
    kernel needed.
  - **External-pool (optional):** for a separate deterministic kernel + multi-account executor pool,
    stop at the reviewed, pushed `manifest.json` and hand it to that kernel — do not execute here.

  Either way the architect's own job ends at a built, reviewed, pushed plan: it plans, it never writes
  product code.

> Shared references: `../references/{task-contract,conventions}.md` are the same files all three
> roles follow — they are the structure, not skills, so sharing them does not break role isolation.

## Output layout

```
docs/superpowers/
├── specs/
│   └── YYYY-MM-DD-<topic>-design.md      # one per sub-project
├── plans/
│   └── YYYY-MM-DD-<subsystem>.md         # one per subsystem, bite-sized TDD tasks
└── manifest.json                          # the task DAG for the orchestrator (Stage 4)
docs/gates/
└── submission-draft.md                    # hackathon builds: the platform form pre-answered (Stage 4)
```

## Hard rules

- **Strongest model only.** Decomposition quality is model-bound. Run the architect on your top
  reasoning seat (tier `top`, at its §Seat settings effort — `../references/model-routing.md`).
  Never let a cheap executor write the plan — it produces vague tasks that drift the whole pool.
- **No placeholders, ever.** "TODO", "add error handling", "similar to Task N", or a step that
  says *what* without showing *how*, are plan failures. The executor has no context to fill them in.
- **Self-contained tasks.** Because executors are stateless and may run on different accounts, each
  task must carry the signatures it depends on. A task that references an undefined type is a bug.
- **The gate is the contract.** Every task ends in a runnable check with an expected result. If it
  can't be checked, it isn't done.

## When NOT to use this skill

- Editing an existing, well-understood file (just edit it).
- A one-off script under ~30 lines (just write it).
- Pure research/Q&A with no build deliverable.

Use it whenever the work is "build a thing" and that thing has more than a couple of moving parts.
