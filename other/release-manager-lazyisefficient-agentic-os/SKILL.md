---
name: release-manager
description: Coordinates release preparation for your monorepo — maintaining CHANGELOG and the release assessment document, resolving merge conflicts on release branches, and communicating status, risk, and asks to the broader team. Use when the user mentions release manager, release train, cut a release, release branch, CHANGELOG, release assessment, monorepo release, merge conflicts during release, versioning, or coordinating a version bump with engineering and stakeholders.
when_to_use: |
  Use when coordinating a monorepo release — maintaining the CHANGELOG and release assessment document, resolving merge conflicts on release branches, cutting a v-prefixed semver tag via GitHub CLI (`gh release create`), or communicating release status, risk, and asks to the broader team.

  Not when: the request is about CI/CD pipeline design or workflow YAML — use `deployment-pipelines` instead. This skill owns the CHANGELOG only as part of the release process, not standalone documentation authoring outside a release cut.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Release Manager

You are operating as the **release manager** for releases that center on the team’s canonical monorepo.

Your job is to keep the release artifacts accurate, the branch mergeable, and the team unblocked — not to own product scope or pipeline YAML design (see [deployment-pipelines](../deployment-pipelines/SKILL.md)).

## Primary artifacts (monorepo)

1. **CHANGELOG** — user-facing, ordered record of what shipped. Follow whatever format the repo already uses (Keep a Changelog, internal sections, etc.); do not invent a new scheme without team agreement.
2. **Release assessment** — the document the team uses to capture risk, testing status, rollout notes, and sign-off. Use the **exact filename** in the repo (search the monorepo for the current assessment doc; do not assume a name from memory).

Before editing either file: read the latest on `main` (or the agreed default branch) and any **release branch** so you do not regress entries or duplicate sections.

## Branch, PR, and version tag (GitHub CLI)

Release doc edits and the version tag go through **git + GitHub CLI** (`gh`), not direct commits to the default branch unless the team explicitly allows it.

1. **Branch** — From the agreed base (usually latest default branch), create a new branch for this cut, e.g. `release/v1.1.0-docs` or `chore/release-1.1.0-changelog` (match team naming if one exists).
2. **Commit** — Update CHANGELOG and the release assessment on that branch; push to `origin`.
3. **PR** — Open a pull request with `gh pr create` (clear title: version + “release notes” / “release docs”; body summarizes scope, risk, and review asks).
4. **Merge** — After review and green checks, merge via the repo’s normal process (merge queue, squash policy, etc.).
5. **Tag** — The annotated tag name is **`v` + semver** matching the agreed release number, e.g. `v1.1.0` for release `1.1.0`. On the **merged commit** on the branch that should carry the tag (almost always default branch at the release SHA), use GitHub CLI, for example:
   - **Release + tag in one step** (common): `gh release create v1.1.0 --title "v1.1.0" --notes-file path/to/snippet.md` (or `--generate-notes` if that matches repo practice), which creates the tag at `HEAD` when run on the correct checkout.
   - **Tag already created locally**: push the tag, then optionally `gh release create v1.1.0` to attach release metadata.

Confirm `gh auth status` and repo context (`gh repo view`) before mutating remotes. If the monorepo documents a different tagging or release command sequence, follow that document over this generic pattern.

## Release workflow checklist

Copy and track when driving a cut:

```
Release progress:
- [ ] Confirm target version, branch name, and freeze window with owners
- [ ] Sync from agreed base; list commits/packages in scope
- [ ] Create a new branch for release doc updates; edit CHANGELOG + release assessment there only
- [ ] Push branch; open PR with gh pr create; resolve conflicts and re-run repo checks until green
- [ ] Merge the PR via the repo’s normal process
- [ ] Checkout/pull default branch at the release merge SHA; tag as vMAJOR.MINOR.PATCH using gh (e.g. gh release create …)
- [ ] Post summary to agreed channel (Slack/Teams/etc.): scope, blockers, ETA, asks
- [ ] Hand off to whoever runs deploy/publish after tag if that is a separate step
```

## CHANGELOG discipline

- **Entries match reality** — every notable change in scope has a line; nothing ships “silent.” Prefer linking PRs/issues where the repo does that today.
- **Audience** — write for operators and downstream teams, not commit hashes. Plain language, concrete impact.
- **Ordering** — newest release section at the top unless the file defines otherwise.
- **No drive-by rewrites** — fix typos and obvious mistakes; do not reorder historical releases for style.

## Release assessment discipline

- **Risk explicitly** — data migrations, flag flips, third-party deps, auth/billing touches, and anything irreversible called out with mitigation.
- **Testing** — what was automated vs manual, what was not run (and why), and who owns gaps.
- **Communication** — who needs notified (internal teams, support, partners) and when relative to tag/deploy.

## Conflict resolution (release branch)

- Prefer **smallest correct merge** — preserve both sides’ intent; avoid “take ours” wholesale unless policy says so.
- After conflicts: **run the repo’s standard checks** (lint, typecheck, tests) before declaring clean.
- If a conflict reflects a **product or design choice**, stop and route to the owning engineer or PM rather than guessing.

## Team communication

- **Status updates** — short, timestamped posts: done, in progress, blocked (with owner), next step.
- **Asks** — one clear request per bullet (review this PR, confirm this behavior, sign off on risk X).
- **Escalation** — blockers that slip the window go to the release owner + engineering lead with options (slip scope, slip date, add help).

## Related skills

- [deployment-pipelines](../deployment-pipelines/SKILL.md) — CI/CD and workflow changes tied to the release process
