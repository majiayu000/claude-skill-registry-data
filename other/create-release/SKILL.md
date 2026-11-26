---
name: create-release
description: Recheck a prepared KoFEM release plan and its completed prerequisites, then open the version/changelog release PR into develop. Use for create release, cut release, or open the release PR; maintainer promotion and CI handle publishing.
---

# Create release

Use only when the maintainer asks to create/cut a release or open its release
PR. Creating these skills or preparing a plan is not such an invocation.
The invocation authorizes the release PR once readiness is verified; do not
ask again merely because checks passed.

Read `AGENTS.md`, [the shared assessment](../release/references/assessment.md),
and the Linear parent created by [prepare-release](../prepare-release/SKILL.md).
If no plan exists, prepare one within this invocation, then apply the gates
below. If the target is ambiguous, resolve it before writes.

## 1. Reuse existing release work

Before applying readiness gates or branching, search open and merged release
PRs, `CHANGELOG.md`, product tags, and published releases for the target version.

- Existing open PR: apply the gates below, then inspect and refresh that PR's
  branch and readiness instead of opening another. Preserve edits and use
  ordinary conflict resolution.
- Release PR already merged into `develop`: report that it awaits maintainer
  promotion. Do not bump again or open the promotion.
- Product release already published: verify its tag/CI provenance, link it on
  the plan, and mark the release parent complete when all work is accounted for.
  Do not create a second release or edit the published release.

Keep the parent open while the PR is open or awaiting promotion/publication.

## 2. Recheck the plan

Read all children, release-labeled issues, blocking relations, relevant comments,
and linked PRs, following pagination. Require completion evidence for every
prerequisite, including manual tasks. For code fixes, verify that the PR merged
and its commit is in current `develop`; Done on a feature branch is insufficient.
Canceled or duplicate tasks require a resolved replacement or an explicit
maintainer scope decision. Never mark work Done to pass this gate.

Fetch live `main`, `develop`, and product tags and repeat the assessment.
Inspect all changes since the plan's recorded SHA, including new correctness
reports; reclassify scope and version as needed. Pending, failed, missing, or
unknown required checks are NO-GO. Do not rely on an earlier green head.
Update the Linear assessment with the current SHA, evidence, and verdict.

If a prerequisite is incomplete or new blockers appear, refresh the same plan
using `prepare-release`, report its links and the concrete blockers, and stop
before changing versions or opening the release PR. Do not silently defer a
correctness issue. If new scope requires a different version, update the plan
and explain the change; obtain the maintainer's choice before creating a
different version than the one explicitly requested.

## 3. Prepare the release diff

Branch from the assessed `origin/develop` SHA (or use the session's designated
branch). Keep the diff to release metadata:

1. Set `web/package.json` `version` and `Cargo.toml` `[workspace.package] version`
   to the chosen version. Run `cargo check` to update the KoFEM entries in
   `Cargo.lock`; do not change dependency versions.
2. Add a `## [X.Y.Z] - YYYY-MM-DD` section below the `CHANGELOG.md` introduction,
   dated today in the maintainer's timezone.
3. Write for users from the entire merged range. Use **Added**, **Changed**,
   **Fixed**, and **Breaking**, only when populated. Include **Known limitations**
   when applicable. Leave internal work out. Explain numerical effects and
   user action explicitly; a research study must not be described as an app fix.

Run and read the output:

```sh
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
bash scripts/release-version.sh
bash scripts/release-version.sh --notes
git diff --check
```

Run the repository's formatting check and any additional checks required by
`AGENTS.md` or the actual diff. A metadata-only release does not require a new
WASM build unless sources changed. Report unavailable checks honestly; missing
required validation keeps the release NO-GO. Inspect the complete diff for
unexpected dependency, source, or saved-model changes.

Before opening or refreshing the PR, fetch `develop` again. If it moved, include
the new range, repeat assessment/checks, and update the notes and Linear plan.
If readiness changed, stop at the plan with the evidence. Do not merge
unassessed commits merely to obtain a green release branch.

## 4. Open the release PR

Target `develop`, with title **Release vX.Y.Z**. Use the applicable `pr` skill
for evidence and merge-risk communication, with these release-specific rules:
`CHANGELOG.md` changes are expected, and no new failing product test is needed
for version metadata. Show the before/after version and consistency-check output.

Include the changelog section and this readiness report:

```markdown
## Readiness

- Plan: Linear parent link; Refs KOF-nn
- Range: last product tag..full assessed develop SHA, N PRs
- Prerequisites: completed tasks and evidence links
- CI on assessed develop head: green, with run link
- Numerical changes: effects and production validation evidence, or none
- Breaking changes: user action, or none
- Open correctness issues: none unresolved affecting this candidate
- Recommendation: GO, with reason
```

Use `Refs`, never `Fixes` or `Closes`, for the release parent, its children,
or already resolved feature issues: merging this PR is not publication. Link
the PR on the existing parent and record the assessed SHA. If it merges on a
later day, update the changelog date before merge.

Report the PR and parent links, checks, and remaining maintainer action.
Agents never merge this PR, create tags or GitHub Releases, deploy, or open/merge
the `develop` → `main` promotion. The maintainer merges and promotes; CI tags
the tested promotion commit and publishes once all required gates pass.
If publishing fails, report the failed job; never tag by hand to bypass it.
