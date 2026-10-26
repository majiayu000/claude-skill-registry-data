---
name: devrites-lib
description: Internal shared DevRites helper library. Documents cross-cutting engine commands and references; not a user workflow. Do not invoke directly.
user-invocable: false
disable-model-invocation: true
---

# devrites-lib: shared workflow contracts

Do **not** invoke this skill directly.

## Ownership boundary

- The host owns instruction loading, exact-agent dispatch, scheduling, waiting,
  follow-up, results, and history. Skills state the role/result, never native
  fields or dispatch receipts.
- Dispatch every workflow-required role fresh. A missing role stops for HITL;
  never skip, substitute, or perform its work in the root.
- The root owns DevRites state/artifacts but never source/tests. Codex grants it
  workspace permission only because children cannot elevate; writing follows
  [`reference/standards/agents.md`](reference/standards/agents.md).
- The engine owns the retained deterministic structure, atomic-write, install,
  evidence-freshness, and safety primitives only.

## Workspace orientation

Use the supplied slug or read `.devrites/ACTIVE`. Require its authoritative
`state.md`; read it directly, then only needed phase artifacts. Never infer
lifecycle state from chat or optional `README.md`.

## Shared references

- [`reference/standards/agents.md`](reference/standards/agents.md): native custom-agent roles,
  immutable inputs, result contracts, and source-boundary review.
- [`reference/candidate-integrity.md`](reference/candidate-integrity.md): the
  content-bound candidate lifecycle from Build through Ship
  ([`workspace-artifact-schema.md`](reference/workspace-artifact-schema.md)).
- [`reference/reply-contract.md`](reference/reply-contract.md): compact user-facing
  completion states. The host renders the response normally.
- [`reference/visual-playbooks/index.md`](reference/visual-playbooks/index.md): progressive
  visual HTML playbook router (load matching ids only; dual-read outline).

## Deterministic engine surface

The engine is limited to:

- Checks: `check candidate` (content-bound identity), `check readiness`
  (structure; `--emit-binding` emits the Build-input binding), `check
  preconditions` (Vet preflight rows), `check seal` (structure
  plus exact artifact bindings and evidence freshness), `check slice` (slice
  contract preflight before wright dispatch), `check task-graph`, `check
  diff-scope` (mechanical changed-paths ⊆ allowlist before reviewer dispatch),
  `check path-disjoint`, `check skill-trust`, `check indexes`, `check
  regression` (progress high-water mark), `check drift` (readiness-input
  attribution), `check windows` (deferral-marker waivers), `check dup`
  (advisory near-duplicates), `check anchors` (Critical/Important quote
  anchoring), `check perturb` (safe-perturbation probe), `detect commands` (repository test/lint wiring).
- Observation: `observe summary` (`orient` alias), `observe slice`, `next`
  (minimal remaining lifecycle path), `handoff` (deterministic resume record).
- Coordination: `context` emits one deduplicated read-set bundle from each
  skill's `loads:` manifest into `.devrites/work/<slug>/ctx/` — dispatch targets
  read it instead of selecting files. It prints `unselected=[...]` for declared
  triggers not passed; an omitted applicable trigger is a gap, not a shortcut. A
  `--role` call is a dispatch, so the `agents` trigger auto-fires when declared
  (`auto=[agents]` in output); a role with no agent contract file fails instead
  of emitting a contract-less packet.
  Manifest grammar: `always` loads every call; `triggers` maps names to files that
  load only when passed or suggested; `workspace` lists the feature artifacts every
  reader may need; `workspaceByRole` maps a dispatch role to its own artifact list —
  present role wins, absent role falls back to `workspace`, an empty list means the
  role reads no workspace files. The engine prints `suggested=[...]` triggers
  inferred from workspace facts (AFK/parallel flags, frontend/security wording,
  principles presence); confirm them rather than re-deriving conditions. Repeat
  calls with unchanged inputs print `unchanged` and reuse the existing bundle.
  `dispatch` owns the launch-wave barrier — seal needs a distinct handle per
  role (the last start seals), return needs seal, open --claim-session/--claim
  takes the wave's file claim (released by the completing return or abandon
  --release), and start/return auto-record into the `metrics` ledger;
  `candidate freeze` and `packet` write a wave's frozen diff and packets. `claim` owns the advisory session-scoped `claims.jsonl` ledger;
  `note` owns anchored `notes.md` entries (`check seal` refuses non-exact
  anchors); `parallel` owns deterministic worktree lease/create/integrate/
  cleanup for parallel slices.
- `gates` owns the machine-checked acceptance ledger (`gates.md`): `scaffold`,
  `status`, `run`, `reverify`, `lint`, `precheck`, `attest`, `abandon` — grammar and
  authoring rules in
  [`reference/standards/gates.md`](reference/standards/gates.md).
- Atomic state: `state resolve` for answer/drop/batch, `state merge-manifest`
  for the predecessor-chain union, `state set`/`state append` for cursor fields and
  ledger sections, transactional `state close`, and `migrate`
  for fail-closed workspace-schema normalization.
- `secret-scan`, `open-visual`, and `version` remain read-only helpers.
- Offline, local `install`, `update`, and `uninstall`; their shell/npm callers
  acquire the candidate bundle, source, and binary before invoking the engine.

Exact native agents/checklists own semantics; the host filesystem owns ledger
reads/preview/confirmed no-clobber writes, spec grammar re-reading, question-id
allocation, clarify cursor edits, AFK accounting, recovery accounting, and
read-only diagnostics. Repository scripts and CI own gates.
