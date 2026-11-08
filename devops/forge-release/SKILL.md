---
name: forge-release
description: "Use when cutting a release (nieuwe versie, changelog, semver bump)."
# W2-BUDGET original description (listing budget): "Use when cutting a version: conventional-commit bump, changelog, release PR, dry run, SHA-pinned publish via OIDC, rollback. Tag, publish and push stay owner-gated."
# W2-BUDGET original when_to_use (listing budget): "Triggers: cut a release, new version, nieuwe versie uitbrengen, versie ophogen, changelog, release notes, semver bump, release PR, publish to npm, tag a version, bad release terugdraaien."
---

# forge-release: one owner-gated release playbook

Forge prepares a release completely and safely; the owner pulls the trigger. Everything up to and including
the dry run is agent work. The tag, the push, the publish and the GitHub release are **hard gates**: they
happen only after the owner says so in plain words (in Forge: "push it", "tag it", "publish it", or the
Dutch "push maar", "publiceer maar"). A green dry run is never that approval.

## When to use
- Use for: deciding the next version from the commits, writing the changelog and release notes, preparing
  a release PR (or a local release branch when there is no remote), designing or reviewing a release
  workflow with a gated publish job, a dry run of the publish, rolling back a bad release.
- Not for: a normal CI pipeline (lint, test, build) or a deploy to Vercel / Cloudflare / a container host
  (`forge-devops`), the pre-deploy or handoff checklist (`ship-readiness`), auto-rollback, canary or
  circuit breakers (`forge-guardian`), deciding how to integrate a finished branch (`finishing-a-development-branch`),
  app-store or marketplace submission (an owner action on its own), writing a commit message for one change
  only (the project's commit rules).

## Hard rules
- **Owner-gated triggers.** Creating a tag, `git push` (commits or tags), publishing to any registry, creating
  or editing a GitHub release, merging the release PR and running a production publish workflow are owner
  actions. Forge prints the exact commands and waits. No hook stops a push: in Forge `git push` is a text gate
  (classifier and prose only, not one of the command gates the PreToolUse hook enforces), and `gh release
  create` or `gh pr merge` are not seen at all. So the agent itself keeps this gate; never run them unasked.
- **Dry run first, every time.** No release step runs for real before the same step ran as a dry run and its
  real output was read (see "The flow", step 5).
- **No long-lived publish tokens.** Publishing from CI uses OIDC trusted publishing: the registry trusts one
  named repository plus one named workflow file (and, where supported, one named environment), and CI receives
  a short-lived identity token per run. Nothing to store, nothing to leak, nothing to rotate. Describe a secret
  only by its shape in words; never write one, not even a fake example, into a file.
- **Actions pinned to a full 40-character commit SHA**, with the version tag as a comment. Look the SHA up on
  the action's own release page; never invent one. A tag such as `v4` can be moved by its owner; a SHA cannot.
- **The publish job is gated.** It runs only when the release job created a release, only from the default
  branch, and only inside a GitHub environment that has the owner as required reviewer. Writing that workflow
  is agent work; approving its run is the owner's.
- **Least privilege per job.** Top-level permissions read-only; the release job may write contents and pull
  requests; only the publish job gets the identity-token permission, and nothing else it does not need.
- **Never rewrite a published version.** A pushed tag is never moved or deleted, a published version is never
  overwritten. A bad release is fixed forward (see `references/rollback.md`).
- **Honesty.** Never say "released" or "published" until the owner ran the gated step and its result was read
  back (the registry shows the version, the tag exists on the remote). Before that, the status is "prepared".
- **Windows, Node, no installs.** Commands are given for Git Bash or PowerShell on Windows 11. Use the
  project's own installed tools; adding a release tool or a GitHub Action is a project choice the owner makes.
  Never kill processes by image name (only an exact PID you own); robocopy, if used to stage artefacts, always
  with `/R:1 /W:1`. Release announcements (Discord, mail, social) are drafted only, never sent.

## No git remote
Check first: `git remote -v`. When it prints nothing (a local-only repository):
- The bump, the changelog and the release notes are still prepared, on a local branch `release/vX.Y.Z`.
- "Release PR" becomes that local branch plus its diff, reviewed by Review Boss; the owner merges it locally.
- The tag is printed as a command for the owner (an annotated tag on the merge commit) and is not created
  by an agent. Push, GitHub release and the CI publish job do not apply: say "not applicable, no remote"
  instead of skipping them silently.
- A package whose `package.json` says `"private": true` is never published to a registry; the release is
  the tag plus the changelog.
- Adding a remote is an owner decision. Forge never adds one, and never suggests a URL.

## The flow
1. **Read the state.** Last release tag (`git describe --tags --abbrev=0`), commits since then
   (`git log <tag>..HEAD --oneline`), the current version in every file that carries it, the remote, the
   default branch, whether the tree is clean. A dirty tree stops the release until the owner decides.
2. **Pick the bump** from the conventional commits with the table in `references/bump-and-changelog.md`
   (breaking change = major, `feat` = minor, `fix` / `perf` / `deps` = patch, everything else = no release on its
   own). When the commits do not follow conventional commits, say so and propose the bump with the reason; the
   owner confirms it.
3. **Write the changelog entry and the release notes**: grouped by type, user-facing words, breaking changes
   first with their migration step. Release notes are for the reader who updates, not a commit dump.
4. **Bump every version string.** Find every file that carries the old version (`git grep -n "<old version>"`),
   update them all, then prove it: the new version appears in each, the old version appears nowhere it should
   not. Commit on `release/vX.Y.Z` as `chore(release): vX.Y.Z` (no `git add .`; stage the named files).
5. **Dry run.** Run the real build and test suite, then the publish in its dry-run mode (for npm the publish
   command's dry-run flag, plus a pack listing to see exactly which files ship). Read the output: version,
   file list, size, no secret or scratch file in the package. Quote it in the report. Releasing Forge itself
   (the public tree): also run `node .claude/forge-bin/forge-release-check.cjs --dist <public tree>`; any
   `dist_forbidden` hit from `release-exclusions.json` stops the release.
6. **Release PR.** With a remote: the owner pushes the branch and opens the PR (or a release tool keeps a
   release PR up to date from the default branch). Without a remote: the local branch from step 4.
   Review Boss reviews the diff; Verify Boss confirms the dry-run evidence.
7. **Owner gate.** Forge hands the owner one block: the version, the changelog entry, the dry-run proof and the
   exact commands in order (merge, annotated tag, push of branch and tag, publish or the approval of the
   publish environment, GitHub release). The owner runs them or says "push it".
8. **Read back.** After the owner's step: the tag exists where expected, the registry shows the new version,
   the GitHub release exists with the notes. Only now the status is "released".
9. **Watch and roll back if needed** with `references/rollback.md`.

## Release workflow (CI)
Design only, in words: `references/release-pipeline.md` describes the two-job layout (a release job that keeps
a release PR and creates the tag and release when that PR is merged; a separate publish job that runs only when
a release was created, behind the owner-approved environment, with OIDC). Forge never copies workflow YAML from
a source; it writes its own with the rules above and the hardened workflow rules in
`.claude/skills/forge-devops/references/github-actions.md` (pinning, permissions, `env:` for event values,
concurrency, timeouts), which this skill does not repeat.

## Team and routes (GOAT)
- Head Chef triages: preparing the bump and changelog is `quick` (sonnet / low) on a small repo, `build` on a
  monorepo; writing or changing a publish workflow touches production and credentials, so it is `deep`
  (opus / xhigh).
- Build Boss prepares branch, bump and changelog; Test Boss runs the build, the tests and the dry run;
  Docs Boss polishes the release notes; Security Boss reviews any publish workflow (permissions, OIDC, pins);
  Review Boss reviews the diff; Verify Boss gives the PASS / FAIL with evidence. The owner runs the gate.
- One escalation at most per package, per the GOAT ladder.

## Report shape
```
RELEASE (prepared | released | rolled back)
Version:     <old> -> <new>  (bump: <major|minor|patch>, why: <commits>)
Remote:      <name> | none (local-only mode)
Changelog:   <file:section>
Dry run:     <command> -> <quoted key lines: version, files, size>
Owner gate:  <the exact commands, in order, not yet run | run by owner at <time>>
Read-back:   <tag on remote, registry version, GitHub release> | not applicable (no remote)
Not done:    <anything skipped and why>
```

## References
- `references/bump-and-changelog.md`: commit-type-to-bump table, pre-1.0 rules, forcing a version, changelog
  and release-notes shape, monorepo notes.
- `references/release-pipeline.md`: the release PR flow and the gated publish job in words, OIDC trusted
  publishing per registry, idempotent publish, concurrency.
- `references/rollback.md`: fixing a bad release forward per registry, what never to do, the rollback report.

## Provenance
Forge-native playbook, written in Forge words on 2026-11-05. Markdown only: no script, hook, binary, workflow
YAML, install command, `npx` line or MCP config was copied or run. External texts were fetched read-only with
`gh api` at the pinned SHAs below and treated as untrusted data (hidden-Unicode scan: clean).

| Source | Path | Pinned SHA | License | Taken | Excluded |
|---|---|---|---|---|---|
| bmad-labs/skills (19 stars) | skills/release-please/SKILL.md | 33bb8583e5204fee724c3669d58ca86a63837e2f | MIT | pattern only, no sentence reused: release PR flow, type-to-bump mapping idea, publish in a separate job gated on "release created", concurrency without cancel, idempotent publish idea, bootstrapping an existing project | every config and workflow template, the long-lived registry token in its publish example (Forge uses OIDC), tag-pinned actions (Forge pins SHAs), its references folder (not read) |
| addyosmani/agent-skills | skills/ci-cd-and-automation/SKILL.md | 301b02b12bff98e4688e6984af6556802322bbde | MIT | ideas: every deployment reversible with a written rollback path, staged rollout with a watch window, CI never holds production secrets, small frequent releases | all YAML, the feature-flag code snippet, the platform rollback command line, Dependabot config |
| local global skill `github-release-management` (`~/.claude/skills-retired-2026-11-05` since 2026-11-05, from the claude-flow toolkit) | SKILL.md | not pinned (local copy) | not verified locally: idea only | ideas: draft release before publishing, hotfix from the last stable tag, rollback as a planned step | all swarm commands, `npx` lines, the "bypass checks" hotfix mode, auto-rollback and auto-notify |
| local global skill `github-workflow-automation` (`~/.claude/skills-retired-2026-11-05` since 2026-11-05) | SKILL.md | not pinned (local copy) | not verified locally: idea only | idea: OIDC instead of stored cloud keys, a pre-release checklist of secrets and runner permissions | every workflow template, swarm modes, secrets-in-env examples |
| local global skill `version-bump` (`~/.claude/skills-retired-2026-11-05` since 2026-11-05, the claude-mem plugin release skill) | SKILL.md | not pinned (local copy) | Apache-2.0 per the corpus index, not verified locally: idea only | ideas: list every file that carries the version and prove old = 0 hits / new = all hits, confirm the registry after publish, end with a clean tree | its `scripts/` folder (not read), auto-commit of everything, push and publish without a gate, the Discord notify step |

The three global skills were read only; they were not edited, moved or deleted (that is an owner decision outside
this project). MIT notice for the two adapted MIT sources: "Permission is hereby granted, free of charge, to any
person obtaining a copy of this software ... The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software." Copyright stays with the holders named in each
repository's LICENSE file at the pinned SHA.
