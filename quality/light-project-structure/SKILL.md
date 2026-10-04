---
name: light-project-structure
description: >-
  Audit, plan, scaffold, and safely migrate research project structures across
  greenfield, existing Git/non-Git repositories, and monorepo subroots. Use for
  project folders, repository cleanup, source inventory, move maps, naming and
  storage policy, Python/R/mixed/LaTeX profiles, template provenance, conflict
  review, applied-move evidence, or rollback. Existing projects are read-only
  until the user authorizes exact action IDs bound to a plan digest. Preserve
  uncommitted and untracked work, symlinks, submodules, and memory-pm's .light
  content. This is an off-DAG local tool: do not emit findings or invent a
  STAGE_GATES/ROUTES connection.
---

# Project structure lifecycle

Own the **visible project tree** and its migration evidence. Do not mistake a
tidy directory for reproducible research.

Read
[`references/project-lifecycle-resource-map.md`](references/project-lifecycle-resource-map.md)
before an existing-repository migration. It defines artifacts, policy, access
levels, provenance, and cross-skill ownership. Use
[`references/structure-profiles.json`](references/structure-profiles.json) for
small profile minima and
[`templates/project-policy.template.json`](templates/project-policy.template.json)
for explicit project/file policy.
Use `scripts/structure_governance_gate.py` before delivery to validate profile
choice, existing-project read-only safety, template residuals, secret scan,
environment doctor, authorization binding, applied-manifest binding, and
rollback evidence.

## Non-negotiable boundary

1. Treat inventory as read-only access, not authorization to move.
2. Never overwrite, delete, run `git rm --cached`, initialize DVC, rewrite
   configuration, or move a symlink automatically.
3. Never use `--force` as consent. The lifecycle has no force bypass.
4. Preserve all `.light/` content. `memory-pm` alone creates or edits passport,
   project card, decision log, version history, terminology, and handoff files.
5. Keep absent facts `UNKNOWN`. A path such as `data/raw` does not prove size,
   sensitivity, immutability, recomputability, or Git policy.
6. Do not turn this overlay into a DAG node. Emit no `light.findings.v1`; add no
   `STAGE_GATES`, `ROUTES`, stage number, or back-edge.
7. State that structural conformance does not prove data quality, experiment
   reproducibility, statistical validity, or paper quality.
8. Never ship a generated or migrated tree with unresolved template placeholders,
   unhandled secret-scan hits, or missing required Python/R/environment checks.

## Choose the mode

| Situation | Mode |
|---|---|
| Empty target and the user wants a starting tree | `scaffold` with one explicit profile |
| Existing repository, monorepo package, or non-Git directory | `intake`, then stop at the decision |
| User approved exact moves after seeing the plan | create authorization, then `apply` |
| Applied moves need reversal | `rollback` from the applied manifest |

Do not scaffold a non-empty directory. Do not retrofit a fixed 23-directory
tree onto R, paper-only, mixed-language, custom, or monorepo projects.

## Phase 1 — Intake and requirements

Collect or preserve as `UNKNOWN`:

- project type and whether the selected root is a Git root, monorepo subroot, or
  non-Git directory;
- deliverables, compute environment, data volume, remote storage,
  collaborators, CI, license, and retention;
- Git root, branch, tracked/untracked/ignored state, uncommitted changes,
  submodules, symlinks, large files, and sensitive path signals.

Choose the smallest profile after inspecting observed technology signatures and
the user's declared deliverables:

- `python-research`
- `r-research`
- `mixed-research`
- `paper-only`
- `existing-custom`

Profiles are extensible minima, not compliance verdicts.
The selected profile is not evidence about the project. `intake` records
observed file/config signals separately from policy-declared artifact types,
recommends a profile, and fails the governance gate when a different profile
has no concrete `profile_selection_reason`.

Copy the policy template outside the source root, fill known project facts, and
add file rules only where there is evidence. Legitimate tracked artifacts
include small public fixtures, reviewed golden files, DVC pointers, final paper
figures, release artifacts, or audit evidence when project policy requires
them. Large/sensitive source data, models, and results usually need DVC/object
storage, but require a decision rather than a directory-name verdict.

Run:

```text
python scripts/scaffold.py intake <root> --out <evidence-dir> \
  --profile mixed-research --policy <project-policy.json>
```

The command writes evidence to `--out` and verifies that the source snapshot
and Git status did not change.

`intake` also emits technology signatures, the environment doctor, template
residual scan, secret scan, and governance report named in the resource map.
Tool checks derive from observed or explicitly declared artifact types, not
from the chosen profile alone. If the project requires Python, R, Quarto, DVC,
LaTeX, or other local tools, record those requirements in the policy. Use the
standalone doctor command only when you need an extra ad-hoc check:

```text
python scripts/structure_governance_gate.py --doctor python r
```

## Phase 2 — Review the dry-run

Read the intake artifacts named in the resource map. Check:

- every inventory row has locator/hash/size/Git state plus explicit or
  `UNKNOWN` owner, producer, recomputability, sensitivity, classification,
  target, and policy basis;
- technology signatures identify their locator and distinguish observed
  evidence from `policy.project.artifact_types`; the selected profile matches
  the recommendation or has a concrete user override reason;
- duplicates are evidence, never auto-delete instructions;
- symlinks, existing targets, and many-to-one moves are blocked;
- `../`, absolute, drive-letter, UNC, or otherwise root-escaping action paths
  are blocked in the dry-run plan and governance gate, not deferred to apply;
- a monorepo subroot uses paths relative to that subroot without treating the
  whole Git root as its project;
- `.light/` is preserved and has no move action;
- large tracked fixtures are not condemned merely for being under `raw`;
- large recomputable or sensitive artifacts surface a storage-policy decision.
- template provenance, residual placeholder scan, secret scan, and environment
  doctor are present when relevant; `.env` ignore is not a secret-scan result.

Present:

1. the recommended profile and why;
2. safe action IDs;
3. blocked conflicts and unknowns;
4. separate decisions for move/rename, overwrite (not supported), deletion,
   `git rm --cached`, configuration rewrite, and DVC initialization;
5. the plan SHA-256.

Then stop. Ask which action IDs the user authorizes. Do not prewrite their
answer.

Run the governance gate on the delivery bundle before presenting a structure as
ready:

```text
python scripts/structure_governance_gate.py \
  --input templates/project-structure-governance.example.json
```

The bundled example is intentionally fail-closed: it attempts scaffold on an
existing R project, leaves template placeholders, reports secret values, misses
R, uses force, moves `.light/`, duplicates action IDs, applies delete, moves a
symlink, and risks overwrite.

## Phase 3 — Bind authorization

After the user chooses, create an authorization document:

```json
{
  "schema": "light.project-structure.v2.authorization",
  "authorization_id": "<user-created stable authorization id>",
  "plan_sha256": "<exact migration-plan plan_sha256>",
  "approved_action_ids": ["move-0001"],
  "authorized_by": "<user-supplied identifier>",
  "authorized_at": "<YYYY-MM-DD>"
}
```

Do not include blocked or unknown actions. `authorization_id` and
`authorized_by` must be concrete user-supplied values, not template text;
`authorized_at` cannot be in the future. A changed plan requires fresh
authorization. The authorization cannot resolve an overwrite or bypass a
symlink block.

## Phase 4 — Apply, verify, rollback, reapply

```text
python scripts/scaffold.py apply \
  --plan <migration-plan.json> \
  --authorization <authorization.json> \
  --manifest-out <applied-manifest.json> \
  --as-of <YYYY-MM-DD>

python scripts/scaffold.py rollback \
  --manifest <applied-manifest.json> \
  --rollback-out <rollback-manifest.json>
```

`apply` re-verifies source hashes and absolute containment, creates missing
target parents, refuses existing targets, moves only ordinary files, records
before/after SHA-256, and writes an applied manifest that binds the exact plan
file and authorization file by locator plus file SHA-256. A path that escaped
the selected root should already have been marked blocked during planning; if
one reaches apply anyway, apply still fails closed. `rollback` verifies target
hashes and refuses to overwrite a reappeared source; it uses the applied
manifest for safe restoration and does not require the original plan/auth files
to still be present.

After rollback:

1. compare the source snapshot and Git status with intake;
2. verify untracked drafts and `.light/` content remain byte-identical;
3. reapply only if the authorization remains intended;
4. report unresolved conflicts and separate manual Git/DVC decisions.

## Greenfield scaffold

Use only on an empty target:

```text
python scripts/scaffold.py scaffold <target> --profile r-research --name <name>
```

The command records profile and generator hashes in
`.project-structure-provenance.json`. It is one-time generation, not safe
template updating. For managed template evolution, evaluate Copier or Cruft and
review local modifications and conflicts; do not claim drift detection is a
merge guarantee.

## Ownership handoff

- Ask `memory-pm` to run `pm.py init` when `.light/` memory is needed; do not do
  its work here.
- Hand data quality, lineage, and release design to `data-engineering`.
- Hand run manifests and executable reproducibility to `experiment-coding`.
- Let `file-reading` understand supplied repositories/materials; this skill
  alone owns moves.
- Let `orchestrator` consume a delivery if useful; do not create a gate.

## Validation

Run the script self-test:

```text
python scripts/scaffold.py --selftest
python scripts/structure_governance_gate.py --selftest
```

It exercises source-read-only intake, a tracked fixture policy, generated
environment/template/secret/governance reports, an untracked draft, `.light/`
preservation, authorization binding, applied-manifest plan/auth file binding,
real move/hash evidence, rollback, reapply, non-Git mode, monorepo subroot
handling, profile scaffold idempotence, and a best-effort Windows symlink
branch.

Before delivery, verify:

- [ ] No source mutation occurred during intake.
- [ ] The user saw conflicts, unknowns, action IDs, and plan digest before apply.
- [ ] Applied moves exactly match authorized IDs and have before/after hashes.
- [ ] Applied manifest binds the exact migration-plan file and authorization
      file by locator and file SHA-256.
- [ ] No target was overwritten and no symlink was moved.
- [ ] No planned/applied source or target path escapes the selected project root.
- [ ] Untracked work and `.light/` content survived move and rollback.
- [ ] Fixtures/golden files/DVC pointers were classified by policy, not path.
- [ ] Template residual scan, secret scan, environment doctor, and profile
      reason are present; observed/declared signatures support the profile, and
      R/Python requirements are checked when claimed.
- [ ] `structure_governance_gate.py` passes for the actual delivery bundle.
- [ ] Template source/version/hash/parameters and update limitation are recorded.
- [ ] The delivery does not claim that structure proves reproducibility.
