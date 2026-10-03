---
name: prepare-fabric-pr
description: Prepare or update a Fabric pull request by proving the changeset-or-skip decision, validation evidence, DCO sign-off, and public-safe PR metadata. Use before the first push, after later revisions, or when asked to create or update a PR. Do not use to review an unrelated PR or authorize relay.
---

# Prepare a Fabric pull request

Produce a reviewable PR whose release decision is explicit and whose public
metadata contains no private identifiers.

## Before pushing

1. Read the root `AGENTS.md` sections on public repository hygiene and
   changesets, plus `packages/fabric-app/README.md`.
2. Fetch the target branch and inspect the complete diff from its merge base.
   Preserve unrelated working-tree changes.
3. Classify the release impact:
   - Production-shipping or user-visible behavior requires a changeset,
     normally `"fabric-app": patch`.
   - Docs-only, CI-only, Markdown-only, or pure changeset changes are normally
     eligible for `skip-changeset`.
   - A different change may skip only when it has no deployable or
     user-visible effect; state that reason explicitly.
4. For an impacting change, run Changesets with `--output` against the target
   branch and inspect the JSON. Require `.releases | length > 0`; exit code zero
   with an empty release list is a failed release decision.
5. For a skip-eligible change, do not create a meaningless changeset. Record
   the no-impact reason for the PR and plan to apply `skip-changeset` once the
   PR exists.
6. Run validation proportional to the diff and record exact commands and
   results. A skipped, unavailable, timed-out, or sandbox-blocked check is
   unverified, not passing.
7. Inspect all public text—branch, commits, changeset headline/body, and PR
   draft—for real organizations, people, deployments, hostnames, internal URLs,
   or private ticket prose. Replace them with synthetic descriptions.
8. Commit only when authorized. Use `git commit -s`; never add AI attribution.

## Create or update the PR

Creating or updating a PR is an external mutation. Do it only when the user's
request authorizes it.

- Use the repository PR template.
- Explain behavior, release decision, and verification without claiming checks
  that did not run.
- After creating a skip-eligible PR, apply `skip-changeset` immediately and
  verify the stored label.
- After every later push, repeat the diff review, release decision, and
  Changesets JSON check. A previous result belongs to the old head.

Stop after the PR is created or updated unless the user explicitly authorized
landing. PR creation alone never authorizes relay, merge, or deployment.
