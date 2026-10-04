---
name: sf-workflow-orchestration
description: Runs Salesforce delivery as a five-wave parallel agent workflow with deterministic gates. Use when a story, bug, or refactor touches more than one metadata type, when several agents must work at once without colliding, when deciding which wave a task belongs to, when a gate fails and the wave must abort, or when wiring the vf-check runner, the vibe-force hooks, and the .vibeforce state files into a pipeline from local edit to verified production deploy.
---

# Salesforce workflow orchestration

The unit of work is a **story**: one user-visible behaviour change, delivered through five
waves. Waves 1, 2 and 4 run several agents at the same time; waves 0 and 3 are serial because
they produce a decision the others depend on.

Nothing in this skill is advisory decoration: every wave boundary is a machine-checked gate
(`vf-check`), and the file-collision rules are enforced by the `pre-edit-guard` hook, not by
politeness.

## When to use

| Situation | Use this skill |
| --- | --- |
| Story touches Apex + LWC + metadata | Yes: full five-wave run via `/vf-story` |
| Single-file typo fix, one metadata attribute | No: fix it, run `vf-check static --changed` |
| Bug with unknown root cause | Wave 0 only first (`sf-scout`), then decide |
| Production incident | Waves 3-4 only, with a human in the loop on every step |
| Refactor with no behaviour change | Waves 1-2, plus a diff review through `/vf-review` |
| Package release | Waves 3-4 plus skill `sf-packaging-release` |

## Wave model

```
wave 0  scope      sf-scout (read-only)              -> impact map
        design     sf-technical-architect (read-only, when the story has a real choice)
                                                     -> .vibeforce/state/architecture.md
        decide     orchestrator                      -> .vibeforce/state/contract.md
wave 1  build      sf-apex-engineer      \
                   sf-lwc-engineer        |  one parallel batch, disjoint owned paths
                   sf-metadata-engineer   |
                   sf-integration-engineer/
wave 2  check      sf-test-engineer       \
                   sf-quality-gate         |  one parallel batch, read-mostly
                   sf-security-reviewer   /
        gate       vf-check local                    -> must pass
wave 3  deploy     sf-deploy-engineer (serial)
        gate       vf-check deploy-validate -> deploy-quick
wave 4  verify     sf-org-verifier        \  one parallel batch
                   sf-test-engineer       /
        gate       vf-check verify                   -> verdict
```

Rules that make the parallelism safe:

1. **One batch per wave.** All agents of a wave are dispatched in a single parallel batch.
   Dispatching them one at a time is a defect, not a style choice: it serialises the wave and
   doubles the wall clock.
2. **Disjoint ownership.** Each wave-1 agent owns metadata paths no sibling may write. The
   `pre-edit-guard` hook denies a cross-slice write and names the owning agent.
3. **Contracts before code.** Anything two agents both depend on (Apex method signature, field
   API name, event payload, permission set name) is decided in wave 0 and written to
   `.vibeforce/state/contract.md`. Agents read it; they never negotiate mid-wave.
4. **No mid-wave validation.** Wave-1 agents do not run the project-wide gate; they would block
   on each other's half-finished edits. Checks belong to wave 2.
5. **Gates are blocking.** A wave starts only after the previous wave's gate returned exit 0.

## Wave 0: scope, design, contract

Serial, read-only, cheap relative to what a wrong design costs in wave 1. Each step feeds the next.

```bash
# what the story touches, before any edit
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" static --changed   # baseline: is the tree already clean?
git log --oneline -10 -- force-app/main/default/classes                     # recent churn in the area
```

**Step 1 - `sf-scout`** returns an impact map: metadata files in scope, existing tests covering
them, triggers and flows already on the affected objects, integration touch points, and risks.

**Step 2 - `sf-technical-architect`**, only when the story has more than one defensible design.
It gets the story and the scout map, and returns decisions with the rejected alternative and the
binding limit for each. Run it when the story:

| Trigger | Example |
| --- | --- |
| changes the data model | a new object, a relationship, a field that carries volume |
| changes who sees what | OWD, sharing rules, Apex sharing, restriction rules |
| crosses a system boundary | a callout, an inbound API, an event, middleware, identity |
| states a non-functional number | row counts, latency, retention, availability |
| forces a declarative-versus-code call | Flow or trigger, rollup or Apex, External Services or hand-written callout |
| changes packaging or environments | a new package, a changed promotion path |

Skip it for a typo, a single-file fix, or a story whose design the contract already fixed. An
architecture run on a story with one defensible design returns one line and costs a turn.

**Step 3 - the orchestrator** applies the **minimal change ladder** (skill `sf-minimal-change`) and
records the outcome in the contract file: which rung each requirement landed on, which alternative
was rejected and why. Scope that does not survive the ladder never reaches wave 1. The architect's
**Contract inputs** go in verbatim; its full record is persisted to
`.vibeforce/state/architecture.md` so wave 2 can review against the decision, not against taste.

Contract file shape (full template in `references/contract-file.md`):

```markdown
## Story
As a service agent I need the case escalation reason on the case list.

## Decisions
- Escalation reason: existing field Case.Escalation_Reason__c reused (rung 2), no new field.
- List UI: lightning-datatable inside existing caseList LWC (rung 4), no custom table.
- Validation: validation rule Case.Escalation_Reason_Required (rung 3), no Apex.

## Contracts
- Apex: CaseEscalationService.escalate(List<Id> caseIds, String reasonCode) -> List<EscalationResult>
- Field API: Case.Escalation_Reason__c (picklist, values: Sla_Breach, Customer_Request)
- Permission set: Case_Escalation_Access (field read/edit + Apex class access)

## Ownership
- sf-apex-engineer: classes/CaseEscalationService*.cls, classes/CaseEscalationServiceTest.cls
- sf-lwc-engineer: lwc/caseList/**
- sf-metadata-engineer: objects/Case/**, permissionsets/Case_Escalation_Access.permissionset-meta.xml
```

## Wave 1: parallel build

Dispatch every needed engineer in one batch. Each gets: the story, the contract file, its owned
paths, and its non-goals. Typical split:

| Agent | Owns | Never touches |
| --- | --- | --- |
| `sf-apex-engineer` | `**/classes/**`, `**/triggers/**` | `classes/integration/**`, LWC, object metadata |
| `sf-lwc-engineer` | `**/lwc/**`, `**/aura/**`, `**/staticresources/**` | Apex, metadata XML |
| `sf-metadata-engineer` | `**/objects/**`, `**/permissionsets/**`, `**/flows/**`, `**/layouts/**`, `**/flexipages/**`, `**/labels/**`, Agentforce and Data Cloud definitions | Apex, LWC, named credentials |
| `sf-integration-engineer` | `**/namedCredentials/**`, `**/externalCredentials/**`, `**/externalServiceRegistrations/**`, `**/externalClientApps/**`, `**/platformEventChannels/**`, `classes/integration/**` | everything else |

Each agent writes its own tests as part of the build (`*Test.cls`, `__tests__/*.test.js`) and
runs only the narrow check for its own files, for example:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" jest --files force-app/main/default/lwc/caseList
```

Hook support during this wave:

- `post-edit-check` claims every written path for the editing agent and records it in the
  session touch list.
- `pre-edit-guard` denies a write to a path another live agent claimed, and denies cross-slice
  writes with the owner's name in the reason.
- `subagent-stop-release` frees the claims when an agent finishes, so wave 2 is unobstructed.

## Wave 2: parallel checks

Three agents, one batch, over the same tree:

| Agent | Runs | Fails the wave when |
| --- | --- | --- |
| `sf-test-engineer` | `vf-check jest`, `vf-check apex --target-org <dev>` | coverage below `apexOrgCoverageMin`/`apexClassCoverageMin`/`jestCoverageMin`, or any test fails |
| `sf-quality-gate` | `vf-check static` | a finding at or above `analyzerFailSeverity` |
| `sf-security-reviewer` | read-only review against skill `sf-security-model` | missing CRUD/FLS or sharing enforcement, secret in source, injection path |

The wave gate is the composite local check:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed
```

`local` = `format` + `lint` + `analyzer` + `jest`. It needs no org, which is why it is the gate
that runs on every turn: the `stop-local-gate` hook re-runs the configured gate over the files
touched in the session and refuses to end the turn while it fails.

Fix rule: failures are fixed at the source by the owning wave-1 agent. Thresholds are never
lowered, assertions are never weakened, and findings are never suppressed to pass a gate.

## Wave 3: serial deploy

One agent, one org at a time, always validate before deploy.

```bash
# 1. check-only validation, runs the tests in the target org without committing anything
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-validate --target-org acme-uat

# 2. deploy the already-validated job, no re-run of tests
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" deploy-quick --target-org acme-uat
```

`deploy-validate` records the job id in `.vibeforce/state/deploy-jobs.json`; `deploy-quick`
refuses to run without a matching validated job for that org. For production aliases the
`pre-bash-guard` hook denies `sf project deploy start` outright and forces the
validate + quick-deploy path; the direct command becomes available only with an explicit human
decision (`VF_ALLOW_PROD=1`). Details in skill `sf-deployment-strategies`.

Promotion order is fixed: `dev -> integration -> uat -> prod`. A wave-3 failure never gets
"fixed forward" in the target org by hand; it goes back to wave 1.

## Wave 4: parallel post-deploy verification

The deploy succeeding is not the story working. Two agents, one batch:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" smoke  --target-org acme-uat
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" apex   --target-org acme-uat --tests CaseEscalationServiceTest
```

`sf-org-verifier` runs the smoke probes (deploy report, anonymous-Apex probes, verification
queries, limits, error-log scan) and collects diagnostics into `.vibeforce/reports/`.
`sf-test-engineer` runs the targeted org test set. The verdict table and the forward-fix versus
rollback decision are covered in skill `sf-post-deploy-verification` and in
`references/failure-and-rollback.md`.

## Gate and hook map

| Gate | Command | Enforced by | Blocks |
| --- | --- | --- | --- |
| Baseline clean | `vf-check static --changed` | wave 0 | starting on a dirty tree |
| Local gate | `vf-check local --changed` | `stop-local-gate` hook, wave 2 | ending a turn with failing source |
| Org test gate | `vf-check apex --target-org <alias>` | wave 2/4 | deploying untested behaviour |
| Validation gate | `vf-check deploy-validate` | wave 3, `pre-bash-guard` | unvalidated production deploys |
| Verification gate | `vf-check verify` | wave 4 | declaring done without org evidence |
| Ownership | claim file in `.vibeforce/state/ownership.json` | `pre-edit-guard`, `post-edit-check` | two agents writing one file |
| Secret guard | content patterns | `pre-edit-guard` | credentials entering the repo |
| Destructive guard | command patterns | `pre-bash-guard` | prod data/metadata deletion |

Hook modes: `off`, `minimal` (deny-only guards), `standard` (default: guards + advisory notes +
stop gate), `strict` (also denies deploying without a passing local gate). Set
`hooks.mode` in `.vibeforce/config.json` or `VF_HOOK_MODE` per shell.

## Anti-patterns

| Anti-pattern | Why it breaks | Instead |
| --- | --- | --- |
| Dispatching wave-1 agents one by one | no parallelism, doubles wall clock, invites drift between slices | one batch, disjoint paths |
| Letting two agents share a file "carefully" | last write wins, silent loss; the hook denies it anyway | split the file or serialise that edit through one owner |
| Running `vf-check local` inside wave 1 | fails on a sibling's half-written file, agents block each other | check in wave 2 |
| Negotiating a method signature mid-wave | both sides stall or diverge | decide it in wave 0, write it to the contract |
| `sf project deploy start` to production | no validated job, no quick deploy, full test run in the release window | validate + quick deploy |
| Treating deploy success as done | metadata deploys fine and the feature still fails on permissions or data | wave 4 |
| Lowering a gate threshold to finish | the gate stops meaning anything | fix the source, or get an explicit human decision |
| Skipping wave 0 for a "small" story | the small story turns out to touch a trigger, a flow and a permission set | scout first; it is cheap |

## Verification

```bash
# hook engine behaves as specified (runs in this repository)
node --test tests/

# the gate the Stop hook runs, on the current change set
node "${CLAUDE_PLUGIN_ROOT}/scripts/checks/vf-check.mjs" local --changed

# state the orchestrator relies on
cat .vibeforce/state/contract.md
jq . .vibeforce/state/ownership.json
jq '.jobs[-1]' .vibeforce/state/deploy-jobs.json
ls -1 .vibeforce/reports | tail -5
```

A wave is complete when: its gate returned exit 0, every owned path is released, and the
hand-off report lists changed files, published contracts, check results and residual risk.

## References

- `references/wave-playbook.md` - per-wave dispatch briefs, inputs, hand-off formats.
- `references/ownership-matrix.md` - path-to-agent map, claim lifecycle, conflict resolution.
- `references/gates-and-hooks.md` - every hook, every mode, exit codes, escape hatches.
- `references/contract-file.md` - contract template, decision log, worked examples.
- `references/failure-and-rollback.md` - abort conditions per wave, forward-fix vs rollback.
- `references/external-skills.md` - where Salesforce-authored plugins fit in the waves, who owns
  generated metadata, DevOps Center versus CLI promotion.

Related skills: `sf-minimal-change`, `sf-deployment-strategies`, `sf-post-deploy-verification`,
`sf-apex-testing`, `sf-lwc-jest-testing`, `sf-code-analyzer-quality`, `sf-security-model`,
`sf-cli-operations`, `sf-project-structure`, `sf-agentforce-development`, `sf-data-cloud`.
