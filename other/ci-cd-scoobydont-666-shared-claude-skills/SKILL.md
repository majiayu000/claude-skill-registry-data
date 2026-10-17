---
name: ci-cd
description: "Design or repair CI/CD pipelines, runner selection, release artifacts, promotion, deployment verification and rollback with checks matched to risk."
---
# CI/CD: Prove, Package, Promote, Deploy, Verify

> CI earns integration confidence. Delivery produces an identifiable release.
> Deployment changes an environment. Verification proves the intended outcome.

## Scope and authority

Apply with `software-development-lifecycle`. CI runs during development; release
and deployment use its reviewed result. This skill guides behavior but does not
create permissions, enforce policy, grant reviews, or authorize production work.
Use existing pipelines, protected branches, review receipts, artifact storage,
GitOps controllers, and operational tools. Do not add a parallel control plane.

Default to continuous **delivery**: prepare releases for an authorized promotion.
Continuous **deployment**, where eligible changes automatically reach production,
requires an explicitly approved policy. Application-source merge is not deployment
permission. A promotion-repository merge may trigger deployment immediately;
obtain deployment authorization before that merge, not afterward.

Preserve the team's two independent source reviews and any separate promotion
approval. Reuse still-valid scoped grants. Missing authority blocks only the
corresponding mutation; continue authorized read-only diagnosis.

## 1. Define the pipeline's decisions

Before adding or changing a job, identify the decision it protects, the failure
it detects, its owner, required inputs, runner trust boundary, timeout/resource
budget, and output evidence. Reuse canonical repository commands across local
and hosted/on-prem execution. Do not create competing definitions of "tests pass."

**Hard rule: run the cheapest reliable checks sufficient for the change's risk;
never remove necessary evidence merely to save compute or obtain a green badge.**

| Lane | Trigger and purpose | Examples |
|---|---|---|
| Fast PR | Every relevant candidate; quick integration feedback | Formatting, lint/types, focused units, secret checks, workflow/schema validation. |
| Targeted integration | Changed boundaries or dependencies | Consumer contracts, database/service fixtures, packaging, supported-platform checks. |
| Deep qualification | Scheduled/on-demand and whenever the change requires it | Broad regression, load/soak, hardware, recovery, compatibility matrices. |
| Release and promotion | Canonical artifact and proposed target | Artifact install/smoke, provenance, policy/security checks, migration/preflight checks. |

A deep test can be a merge or release requirement for a specific risky change;
its normal nightly schedule is not a waiver. Documentation-only changes need
appropriate lightweight checks, not an unrelated GPU fleet exercise. Executable
examples, agent instructions, policies, build files, and dependencies are not
inert documentation. Changed shared components require consumer-impact selection.

Start with a team feedback target around ten minutes for the fast lane, then
measure and tune it. This is a budget objective, not permission to time out
necessary checks and mark success. Cancel superseded PR work, bound concurrency,
and avoid duplicate branch-push/PR suites proving the same candidate property.
Retest where the source, integration context, platform, or evidence actually differs.

## 2. Keep selection and results truthful

Use a trusted change classifier and a stable required summary check. Trigger the
summary workflow for every eligible PR and the merge queue event when applicable;
perform selective work inside it. Do not make a required workflow disappear
through a top-level path filter. GitHub distinguishes a skipped workflow, whose
required check can remain pending, from a skipped job that may appear successful.

The summary must run after failures where possible and evaluate the explicit
expected job set. Missing, failed, timed-out, cancelled, malformed, or unexpectedly
skipped required evidence must not produce success. A job is **NOT_APPLICABLE**
only when a trusted selector establishes why. If selection is unknown, expand
to a conservative relevant suite or block; never assume nothing changed. Whole
workflow cancellation cannot count as passing evidence even if no summary ran.

Record source/head and tested integration SHA, workflow/suite revision, test
configuration, runtime/dependency identity, selected/collected/executed test
counts, results, and evidence locations. Empty test collection is a failure
when tests were expected. Failures remain failures even if logs contain "PASS."
Do not use `continue-on-error`, `|| true`, or an unconditional final success to
hide a required failure. Explicit advisory checks may be non-blocking and must
be labeled accordingly.

Protect required-check definitions and policy changes with established review
and platform controls. A PR must not gain approval by editing its own expected
checks, disabling tests, or fabricating a receipt. A signed assertion still needs
an authorized issuer and binding to the expected subject. Test pipeline changes
with cases for relevant/irrelevant paths, shared dependencies, zero tests, job
failure/skip/cancellation, and wrong-head evidence. This skill does not implement
that checker or replace the current trusted gate.

## 3. Separate compute placement from authority

Use GitHub-hosted runners for public repositories. Use private runners for private
repositories, with disposable isolation appropriate to the input trust boundary.
Scheduling is based on trust and required capabilities, not cheapest location
alone. Private repository code and generated code are not automatically safe.

| Execution class | Boundary |
|---|---|
| Untrusted PR/build input | GitHub-hosted for public repositories; an approved isolated disposable private runner for private repositories; no lab/production access or privileged credentials. |
| Admitted private-repository build/test | Bounded private sandbox with clean state, dedicated service identity, restricted network/filesystem reach, and no deployment authority. |
| Release/promotion operation | Separate protected execution identity and environment; only approved inputs and narrowly scoped publishing/promotion rights. |

Do not expose a host control socket, privileged container, production kubeconfig,
SSH key, shared writable agent home, or unrestricted lab network to ordinary
build/test jobs. A runner label, private network, disposable registration, or
container alone does not prove isolation. Clean workspace, process, cache,
credential, and network state across jobs. Hardware CI still needs containment.

Never check out or execute untrusted PR code in a privileged
`pull_request_target` or `workflow_run` path. Treat upstream artifacts and caches
as untrusted inputs until validated. Pin external actions/reusable workflows to
verified full commit SHAs and record toolchain/container/dependency versions.
Keep token permissions minimal; use short-lived scoped credentials where the
platform supports them. Prevent untrusted interpolation into shell commands.

Measure runner CPU/RAM/swap, disk on the actual mount, processes, existing jobs,
and accelerator availability before admitting heavy work. Set time, process,
memory, and parallelism limits. An unavailable required runner means pending or
blocked evidence, not successful CI. Do not install more runners or shift work
onto operational hosts without approved scope.

## 4. Diagnose failures instead of rerunning until green

Read the first causal failure, not just the final red job. Classify it:

- **Product:** reproducible behavior defect. Fix the code and regression test.
- **Test:** invalid assertion, fixture, discovery, or nondeterminism. Prove the
  diagnosis; repair the test without weakening the intended requirement.
- **Infrastructure:** capacity, permissions, tooling, registry/network, or runner
  state. Preserve evidence, repair the execution path, then rerun the same candidate.
- **Policy/selection:** missing triggers, wrong check identity, permissions, or
  incorrect scope. Repair the pipeline contract, not the code to appease it.

Allow only bounded retries for identified transient failures and retain all
attempts. A retry success does not erase the original evidence. Quarantine a
flaky test only through the approved exception process with an owner, deadline,
risk statement, and replacement evidence where required. No self-issued waiver.

Treat caches as acceleration, not proof or the canonical artifact store. Separate
trust domains; key by relevant locks/toolchain/platform/configuration; verify
outputs and tolerate cache misses. Periodically check clean builds. Do not
promote an artifact merely because it came from a warm cache.

## 5. Build the release once; promote the same bytes

An authorized release workflow builds from the actual integrated source in a
clean, controlled environment with resolved inputs recorded. PR artifacts remain
candidates unless the release policy verifies their exact source, builder,
provenance, and reuse eligibility. Test the actual distributable: image, package,
binary, wheel, or versioned source/configuration bundle. A unit suite alone does
not establish that packaging installs or starts correctly.

Publish to the authorized immutable destination. Record version, source commit,
artifact URI and digest, platform variants, dependency/SBOM information, build
identity/provenance, relevant test evidence, release notes, and configuration/
migration constraints. Apply the existing release signing/attestation policy.
At promotion, verify artifact bytes, provenance subject, and authorized builder
identity, not just that some signature exists. Do not claim an achieved SLSA
level without evidence for its complete requirements.

Promote the same digest through environments; never rebuild separately for
staging and production or deploy a mutable `latest` tag. Supply environment
configuration and secret references separately and record their versions without
secret values. Different architectures can have different declared artifacts;
validate the selected platform and its digest. A security scan's risk decision
can expire even while the artifact bytes stay unchanged.

If an environment-specific build is unavoidable, it is a distinct artifact with
its own identity and qualification, not an untested substitution for the staged
release. Artifacts may be released but held from deployment.

## 6. Preflight the promotion

Before the mutation, bind a deployment plan to:

```text
Release/source/artifact digest and verified evidence:
Target: environment, cluster/namespace or exact host/service identities
Desired-state repository/revision and current observed revision:
Configuration version and secret references (never values):
Affected consumers, compatibility, and migration order:
Capacity, mounts, permissions, network/dependency health:
Current baseline health and existing incidents/drift:
Rollout stages and authorized concurrency:
Success criteria, failure thresholds, observation window, minimum traffic/sample:
Previous known-good artifact/configuration and rollback constraints:
Backup/restore evidence for affected persistent state when applicable:
Deployment authority, operator, recovery owner, and valid holds:
```

Check actual target identity and the rendered delta. Do not trust a selected
context name alone. Resolve drift and competing writers; serialize promotions
per environment/service and use conditional updates against the observed version.
Revalidate when the target or candidate changes. Dry-run/Ansible check mode is
useful preview, not proof that every action or migration is safe or will work.

No data-changing operation without an applicable recovery strategy. A backup
job succeeding is not a restore test. Prefer expand/migrate/contract steps that
preserve old/new compatibility during rollout. Do not automatically downgrade
an application across an incompatible schema or replay an irreversible migration.

Unknown safety-critical prerequisites mean **DEPLOYMENT_BLOCKED**. Do not replace
an absent mount, secret, dependency, or approval with a permissive fallback.

## 7. Deploy through the existing desired-state path

Change the authorized GitOps desired state to the reviewed immutable artifact
and configuration. Let the established reconciler apply it. For approved host
management, use the existing version-pinned Ansible/systemd deployment path.
A one-off playbook does not by itself provide continuous drift reconciliation;
record who observes and reconciles the actual state.

Do not deploy a branch checkout, `git pull` an application directory as a release
mechanism, copy files into a live service tree, or patch a host/cluster out of band
as the normal path. Do not add another orchestrator to work around a pipeline
problem. Separate installation/activation from optional user-facing feature enablement.

Begin with a bounded canary appropriate to the service: one instance, an isolated
tenant, a limited traffic slice, or an approved maintenance target. Expand only
when the prior stage satisfies its criteria. Singleton/stateful services may
need a maintenance window or other strategy rather than a fictitious canary.

Use idempotent deployment primitives. In an isolated qualification environment,
exercise first apply, repeated apply, interruption, and recovery. A second apply
with unchanged intent must not unnecessarily rewrite configuration, restart
healthy services, reset credentials, rerun migrations, or duplicate effects.
After a timeout, inspect the actual outcome before retrying.

Cancel obsolete PR tests, **not** an in-flight production mutation merely because
another commit arrived. Deployment cancellation requires an explicit safe-stop
and reconciliation strategy. Only one authorized writer advances the target.

## 8. Verify, then expand or recover

Observe actual runtime identity: artifact digest/version, deployed configuration,
and reconciled desired-state revision. Run the intended consumer transaction;
check permissions/auth behavior, errors, latency, resource use, and relevant
data invariants against the predeclared baseline and thresholds. A green
workflow, running process, open port, or health endpoint alone is insufficient.

Require the specified observation window **and** meaningful traffic/samples.
An idle canary with no errors is inconclusive; use an authorized representative
synthetic transaction or hold. Bound verification and record exactly what it
covers. Do not run destructive tests against real user data to obtain proof.

If a threshold fails, stop expansion, preserve evidence, and execute only the
pre-authorized recovery that remains safe for current data/state. Restore the
previous artifact/configuration via the desired-state path where appropriate;
use forward repair or a separately authorized data restoration when rollback
would lose or corrupt data. Verify recovery independently. Do not claim a
rollback succeeded because its command exited zero.

Break-glass changes require the existing emergency authority, narrow scope,
identity/audit evidence, and reconciliation back into Git. Preserve observations
before repair when practical. Do not leave undocumented live drift or change
desired state blindly to match a compromised/incorrect runtime.

## Required completion report

Link trusted evidence. This template reports results; it cannot authorize them.

```text
CI: PASS | FAIL | BLOCKED | PENDING — candidate/integration SHA and run references
Release: NOT_RELEASED | RELEASED — source, artifact URI, digest, build evidence
Promotion: NOT_REQUESTED | BLOCKED | APPROVED — target, authority, desired-state revision
Deployment: NOT_DEPLOYED | IN_PROGRESS | DEPLOYED | FAILED | RECOVERED
Observed runtime: artifact/configuration/reconciled revision
Verification: PASS | FAIL | INCONCLUSIVE | NOT_RUN — scope, samples, time, evidence
Recovery: NOT_NEEDED | AVAILABLE | EXERCISED | BLOCKED — evidence and data limits
Remaining work / drift / exception / owner:
```

Mark an environment **VERIFIED** only when all applicable acceptance checks and
observation criteria pass. Always name the environment: a verified staging
release says nothing by itself about production. Maintain artifact/recovery
retention, patch dependencies and runners, and review CI cost, queue time, flake
rate, escaped failures, deployment failure, and recovery time. Remove duplicate
work, not the evidence needed for a safe decision.

## Reference basis

Team policy, not a certification claim. Current primary references:

- GitHub required checks, skips, and merge queues:
  https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
- GitHub Actions trust boundaries, runner security, permissions, and pinning:
  https://docs.github.com/en/actions/reference/security/secure-use
- SLSA artifact verification:
  https://slsa.dev/spec/v1.2/verifying-artifacts
- OpenGitOps desired-state and reconciliation principles:
  https://opengitops.dev/
