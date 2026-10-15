---
name: ci-cd-and-automation
description: "Create or change CI/CD pipelines, quality gates, and delivery controls."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: high
  capabilities: addyosmani,ci-cd-and-automation
---

# CI/CD and automation

Use this workflow to create or change build and delivery pipelines. Read the
repository's runtime versions, lockfiles, existing checks, runner model, and
release policy before writing configuration. Repairing one failed check does
not require redesigning the pipeline.

## Build the smallest useful pipeline

1. Run the repository's actual commands locally where possible. Map each job
   to a failure it catches and a meaningful output. Do not add a Node toolchain,
   browser suite, or coverage target to a project that does not need it.
2. Put inexpensive checks early. Parallelize independent work when useful;
   preserve dependencies between build artifacts and their tests. Test the
   merge candidate or merge-queue revision used by the repository.
3. Use the authoritative lockfile and supported frozen-install mechanism.
   Key caches by relevant platform, runtime, and dependency inputs. Cache hits
   do not replace integrity checks or authorization.
4. Give jobs bounded timeouts. Preserve useful failure output and test reports
   without uploading credentials or private fixtures. Triage flaky tests rather
   than silently skipping them or retrying until a green result appears.
5. Check trigger and path-filter behavior: a required status must not remain
   pending forever when its workflow is skipped. Document which check names
   branch protection expects; changing repository settings is a separate action.

## Keep untrusted code away from delivery credentials

Use the host's current security documentation when choosing events and tokens.
For GitHub Actions, start with read-only permissions and grant writes only to
the job that needs them. Pull-request tests should run without production
credentials. Do not execute untrusted PR code, scripts, or artifacts in a
privileged `pull_request_target` or `workflow_run` job.

Treat PR titles, branch names, workflow inputs, caches, and artifacts as
untrusted. Pass text through environment variables or structured arguments
instead of interpolating it into shell source. Validate release identifiers
against permitted artifacts. Follow the repository's action-pinning policy;
verify any new immutable action revision against the official upstream.

Use disposable runners for untrusted contributions. Separate test credentials
from deployment credentials and limit environment access. Prefer short-lived
deployment identity where the chosen provider supports it. Do not introduce
new secrets or production access merely to make a check pass.

## Delivery and recovery

Build and test an identifiable artifact, then promote that same artifact.
Define target environment, rollout health signals, observation window, and
recovery steps before enabling delivery. Scope concurrency per environment;
canceling an old validation job is different from interrupting a live deploy.
A feature flag cannot reverse data mutations.

Preserve existing authorization and environment approval gates. A request to
write CI configuration does not grant permission to publish, merge, deploy,
change branch protection, or enable automatic merging. Use authorization
already present in the task without asking for it again.

## Verify

Validate configuration and execute relevant jobs on the exact candidate. Check
failure propagation, fork behavior, permissions, artifact identity, and skipped
job semantics. Rehearse delivery and recovery only in an authorized environment.
Report which paths ran, which were inspected, and which remain untested.

Reference: [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
