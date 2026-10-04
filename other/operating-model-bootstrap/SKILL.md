---
name: operating-model-bootstrap
description: Bootstrap or harden a project's operating model for mixed human and AI delivery teams. Use when starting a repository, adopting an agent harness, defining authority and risk tiers, coordinating parallel agents safely, binding evidence and review to an exact candidate, or correcting fragmented rules that prevent coherent, consistent, complete delivery.
---

# Operating Model Bootstrap

## When to use

- Starting a new repository or team project that will use AI agents or agent-harness skills
- Adopting this harness into an existing project for the first time
- Defining or repairing authority, risk tiers, lane isolation, or evidence-binding contracts
- Coordinating parallel human and agent lanes safely (worktrees, ownership, integration)
- Binding review to an exact candidate commit before R2/R3 work
- Correcting fragmented or contradictory rules across AGENTS.md, CLAUDE.md, and GEMINI.md

---

Establish a portable operating kernel and one tracked project profile. Treat humans,
agents, skills, tools, and gates as one delivery system with explicit authority,
ownership, evidence, and completion semantics. The day-one seed lets a new team begin
system design and delivery planning while explicitly owned project unknowns are resolved.

## Project awareness — seven areas to establish at init

The bootstrap must establish or explicitly own each of the following. Required areas must
be answered before the profile leaves `seed` state. Optional areas have a recommended
default; record `not yet established — owner: role; required before: trigger` for any
unknown rather than leaving it blank or fabricating a value.

| # | Area | Status | Default if not declared |
|---|---|---|---|
| 1 | Product vision, objectives, actors, scope, out-of-scope, SOW / acceptance record | **Required** | None — must be declared |
| 2 | Team roster: PO, SMEs, integration owner, reviewer roles, escalation path | **Required** | None — must be declared |
| 3 | Technical stack: language, framework, architecture, repos, interfaces, runtime | **Required** | None — must be declared |
| 4 | Tooling: package manager, linter, type checker, unit / integration / e2e test commands | Optional — recommended defaults | Linting + validation + unit tests minimum |
| 5 | Cloud, hosting, data classification, residency, compliance, approved-vendor constraints | Optional — advised | Deduced from stack; invoke `governance-guardrail` to confirm policy alignment |
| 6 | Automation: CI/CD, branch policy, release process, deployment owner, rollback | Optional — default provided | GitHub SemVer + tag-based releases; invoke `release-manager` to document and confirm |
| 7 | Delivery controls: source of truth, issue/PR conventions, DoD, escalation triggers | Optional — default provided | GitHub stack; this repository's issues, ADRs, and architecture docs are the source of truth |

### Backfill from an existing repo

When adopting into a repo that already has code, do not present a blank seven-area form.
Run the read-only inspection pass to pre-fill what the repository already reveals:

```bash
python3 .agents/skills/operating-model-bootstrap/scripts/inspect_repo.py .
```

It reads manifests, tool configs, CI, `CODEOWNERS`, and docs, and prints **inferred**
findings — each a machine guess with an evidence pointer and the exact
`inferred — source: <evidence>; confirm: <role>` marker to paste into the profile. Rules:

- Transcribe each finding into the profile as its `inferred` marker; **never** silently
  promote it to a verified fact.
- Confirm inferred fields **one at a time** with the named human; a confirmed field
  becomes a plain verified value. The profile cannot go `active` while any `inferred`
  field remains (the validator enforces this).
- The pass is read-only and **never infers authority** — `CODEOWNERS` handles are roster
  *candidates* only; role and accountability stay `unknown` until a human assigns them.

### Init artefacts

The initializer script seeds structure, not decisions. Running `bootstrap` (or the `init`
command, which runs `bootstrap` first) creates these records with template content to be
grounded from verified project evidence:

- `docs/operating-model/PROJECT-OPERATING-PROFILE.md` — the project contract, holding the
  seven-area answers above.
- `docs/VISION.md` — product vision, objectives, actors, scope, and out-of-scope (area 1).
- `docs/ROADMAP.md` — the big-picture scope of work: ordered outcome gates, seeded
  unpopulated. The team adds dates as the Product Owner confirms them.
- `docs/STATUS.md` — the derived situation-report structure, seeded unpopulated.
- `docs/operating-model/DELIVERY-WORKFLOW.md`, `CHANGELOG.md`, and the
  `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` adapters.

The script seeds structure; the agent records the decisions. As part of the bootstrap
workflow, capture the choices made during init as durable, referenceable authority:

- **Baseline ADR** — author the project's first architecture decision record at its ADR
  convention (`ADR/ADR-0000-baseline-structure-DRAFT.md`, approved to
  `-approved.md`; see `the-architect`),
  capturing every choice confirmed or deferred during init, with the owner and resolving
  trigger for each explicit unknown. This is the authority record for the starting
  structure.
- **First status entry** — add one entry to `docs/STATUS.md` recording the initialization
  event and the open unknowns. This records what happened, not invented progress; roadmap
  outcomes stay unpopulated until the Product Owner validates them.

Do not fabricate answers to populate any of these files. An honest `unknown — owner: X;
required before: Y` is better than a plausible-sounding invention that will mislead every
agent that later reads the profile.

## Portability boundary

The operating model is model-, vendor-, and IDE-agnostic. Thin surface adapters only make
the same contract discoverable and invocable. They may not change authority, risk,
evidence, review, or completion semantics. This is a team-project harness bootstrap, not a
production application scaffold or a substitute for project/domain controls.

## Load the assets

Read the four contract assets before editing the target project:

- `assets/OPERATING-MANUAL.md` — released vendor-neutral normative kernel; copy it unchanged.
- `assets/PROJECT-OPERATING-PROFILE.template.md` — project-specific contract.
- `assets/CHECKPOINT.template.yaml` — durable state for R2/R3 work.
- `assets/EVIDENCE-MANIFEST.template.yaml` — exact-candidate evidence and review record.

Read the five planning-seed assets before initialising project delivery records:

- `assets/VISION.template.md` — durable product direction and initial focus.
- `assets/DELIVERY-WORKFLOW.template.md` — project mapping of the shared lifecycle.
- `assets/ROADMAP.template.md` — ordered outcome gates, initially unpopulated.
- `assets/STATUS.template.md` — derived situation-report structure, initially unpopulated.
- `assets/CHANGELOG.template.md` — project release-history structure.

Use the thin starter files under `assets/adapters/` for agent surfaces the target
project supports. They are discovery adapters, not competing constitutions.
For a greenfield adoption, read `references/DAY-ONE-EXAMPLE.md` to calibrate what may
start in `seed` state and what must wait for `active` controls.

Do not copy project details into the universal manual. Bind its exact SHA-256 in the
profile and adapters. Unknown profile facts must be owned and time-bounded, never
fabricated. Never call a seed profile active while applicable placeholders remain.

## Initialise safely

From a target repository containing this skill, preflight and install the day-one seed:

```bash
python3 .agents/skills/operating-model-bootstrap/scripts/bootstrap_operating_model.py \
  --dry-run --project-name "<project name>" .
python3 .agents/skills/operating-model-bootstrap/scripts/bootstrap_operating_model.py \
  --project-name "<project name>" .
```

The initializer creates the manual, seed profile, checkpoint/evidence templates, vision,
delivery workflow, blank roadmap/status structures, project changelog, and `AGENTS.md`,
`CLAUDE.md`, and `GEMINI.md` adapters. It preflights the whole file set, preserves
different existing project planning records, and refuses conflicting operating contracts
or adapters before writing anything. Map existing planning records in the profile; merge
a protected contract deliberately rather than forcing replacement.

## Bootstrap workflow

1. **Ground the project.** Read its existing constitutions, architecture, delivery
   flow, test commands, deployment path, protected surfaces, and current state. List
   contradictions and stale claims before adding policy.
2. **Classify risk.** Map project work into R0–R3. Round ambiguity upward. Name the
   highest-impact silent failure, rollback owner, and observation surface.
3. **Confirm authority.** Separate useful intent from permission at the classified
   risk tier. Obtain explicit approval before constitutional, destructive, credential,
   external, deployment, production-data, or capital changes.
4. **Install the kernel.** Run the safe initializer or copy the released manual byte for
   byte to the canonical governance location. Record version, digest, owner, adoption
   status, and review trigger.
5. **Ground the profile.** Resolve the day-one minimum first. Fill applicable fields
   with verified facts and use `not applicable — reason` or `not yet established — owner:
   role; required before: trigger` elsewhere. Keep status `seed` for design/R0/R1; require
   `active` and runnable controls before R2/R3. Never invent a command, role, or control.
6. **Route baseline skills.** Confirm paths or equivalents for orchestration,
   architecture, specification, domain/adversarial validation, candidate review, release
   readiness, status, and cost. Invocation syntax may vary; semantics may not.
7. **Define the squad.** Assign one accountable human/operator, one integration owner,
   bounded mutating lanes, and independent reviewers. Give every lane owned files,
   owned resources, and a falsifiable success test. A skill supplies capability; it
   never supplies authority.
8. **Wire lightweight adapters.** Use only the adapters the team needs. Keep the
   generated protected block identical across surfaces and surface-specific workflow
   details outside it. Run the deterministic drift check.
9. **Isolate mutation.** Require one branch/worktree and resource namespace per
   mutating lane. Read-only reviewers may share. Only the integration owner assembles
   pinned lane commits in a clean worktree.
10. **Bind evidence.** Instantiate both checkpoint and evidence-manifest assets for R2/R3.
    Retain exact base/candidate identity, commands, exit status, environment, data
    provenance, artifacts, reviewers, conditions, and rollback. Any candidate change
    invalidates prior review.
11. **Enforce verdicts.** PASS means zero conditions. Conditional/amendment verdicts
    block until fixed and re-reviewed; REJECT/BLOCKING halts. Make any override an
    explicit operator path with a durable reason, never a passing reviewer token.
12. **Close the lifecycle.** Run focused and convergence gates, obtain independent
    review of the exact integrated candidate, deliver only with authority, observe the
    result, and reconcile status, changelog, HLD/runbooks, evidence, open risk, and
    rollback.

## Minimum mechanical controls

Implement controls proportionate to the project:

- a profile/adapter drift check;
- a protected-path gate that detects edits, modes, deletions, and renames;
- regression-first tests for defects;
- one convergence command for the assembled candidate;
- secret and dependency scanning;
- exact-snapshot review invalidation;
- post-delivery health/rollback checks.

Prefer a required remote check or signed attestation for high-risk approval. A local
hook is defence in depth and does not authenticate reviewer identity.

## Validation

Before completion:

1. Validate the distributed assets before adoption:

   ```bash
   python3 .agents/skills/operating-model-bootstrap/scripts/validate_operating_model.py \
     --template-root .agents/skills/operating-model-bootstrap
   ```

2. Validate an adopted seed. Before R2/R3, repeat with `--require-active` and pass the
   resolved checkpoint/evidence paths:

   ```bash
   python3 .agents/skills/operating-model-bootstrap/scripts/validate_operating_model.py \
     --target .
   python3 .agents/skills/operating-model-bootstrap/scripts/validate_operating_model.py \
     --target . --require-active \
     --checkpoint docs/operating-model/checkpoints/<task-id>.yaml \
     --evidence docs/operating-model/evidence/<task-id>.yaml
   ```

3. Verify all mutating lanes and external resources have one owner.
4. Change one adapter inside its protected block; confirm semantic drift fails.
5. Rename a protected file; confirm the project-specific protected-path gate catches it.
6. Change the candidate after review; confirm checkpoint/evidence binding fails or is stale.
7. Run the project's lint, type, test, security, and convergence commands.
8. Run the Adversarial Gate: name how authority, isolation, evidence, delivery, or
   observation could still fail silently.

## Required outputs

- Adopted universal manual with version/digest.
- Completed, tracked project operating profile with all seven project-awareness areas
  recorded (verified fact or explicit unknown with owner and trigger).
- `ADR/ADR-0000-baseline-structure-DRAFT.md` (approved to `-approved.md`) — baseline ADR
  capturing all init decisions and deferred unknowns.
- Initializer-seeded `docs/VISION.md`, `docs/ROADMAP.md`, and `docs/STATUS.md`, grounded
  from evidence; the first `docs/STATUS.md` entry records the init event and open unknowns.
- Grounded delivery workflow plus project changelog.
- Lightweight surface adapters plus drift enforcement.
- Durable checkpoint for active R2/R3 work.
- Exact-candidate evidence manifest for active R2/R3 work.
- Validation evidence and explicitly owned unresolved platform/operator actions.
- Updated project status, changelog, and architecture/runbook documentation when the
  operating contract or delivery flow changes.

Do not claim complete enforcement while local checks remain bypassable, reviewer
identity is unauthenticated, credentials remain exposed, or delivery has not been
observed.
