---
name: release-conventions
description: "Versioning and release rules: semantic versioning driven by Conventional Commits, release-me as the default tool, release-please where still used, moving major tags, Renovate conventions and release labels. Use when setting up release automation or deciding what a change means for the version."
---

# Release conventions

How versions, changelogs and dependency updates get produced.

## When to use

- Setting up release automation or dependency updates in a repository.
- Deciding what a change means for the next version.
- Reviewing a release pull request or a Renovate configuration.

## Rules

### Versioning

- Semantic versioning, driven by Conventional Commits: `feat` is a minor, `fix` and
  `perf` are a patch, a `!` marker or a `BREAKING CHANGE` footer is a major. `chore`,
  `docs`, `ci`, `test`, `build`, `style` and `refactor` do not release on their own.
- Before `1.0.0` a breaking change bumps the minor, `bump-minor-pre-major: true` in either
  tool's configuration. Reaching `1.0.0` is a deliberate decision, not a side effect.
- A version is never set by hand and never edited in a file the release tool owns.
- The workflow runs the release tool with the token of the release app, see the Apps
  section of `github-as-code`. A pull request opened with `GITHUB_TOKEN` triggers no checks.
- A feature pull request merges as a merge commit, never squashed: every `feat` and `fix`
  commit stays visible to the release tool on its own, instead of collapsing into one line.
  release-please reads the pull request title alone and recommends squash merges;
  release-me's default first-parent walk needs the merge commit itself, resolving the pull
  request it names through the forge. Either way the merge commit is a deliberate
  deviation from the tool's own recommendation, the atomic commits matter more.
- Never push a tag by hand. A manual tag desynchronizes release-please's manifest, or risks
  landing one commit off the merge commit release-me itself would have tagged.

### release-me

- The default for a new repository. Configuration lives in `release-me.yaml`, committed.
  No separate manifest: the tags already on the branch and the release pull request's own
  label are the only state.
- One component at the root by default. Split with a `components:` map only when parts are
  genuinely consumed and released separately, each with its own branch and tag prefix.
- The flow: commits land on the default branch, `release-me run` (`pr` then `release`, the
  CI entry point) maintains a release pull request, merging it tags and releases on the
  next run.
- A pre-release moves through a label on the release pull request
  (`release: alpha|beta|rc` by default); the workflow also triggers on that pull request's
  `labeled`/`unlabeled` events so a label change updates the branch without waiting for the
  next push.
- `CHANGELOG.md` is generated, prepended to on each release: existing entries above the new
  one survive, nothing is lost the way a full regeneration would lose hand edits.
- The moving major tag (`major-tag: true` per component) is for an actions or workflow
  repository other repositories pin a floating major version against. Skip it otherwise.

### release-please (legacy)

- For a repository that already runs it; a new repository uses release-me instead.
- Configuration lives in `release-please-config.json`, state in
  `.release-please-manifest.json`. Both are committed.
- One repository version by default. Split into components only when parts are genuinely
  consumed and released separately.
- The flow: commits land on the default branch, release-please maintains a release pull
  request, merging it creates the tag, the release and the changelog entry.
- `CHANGELOG.md` is fully regenerated. Hand edits are lost on the next release.

### Actions and workflow tags

- Every action is pinned to a commit digest: `uses: owner/action@<commit sha> # v<tag>`. The
  digest is what runs, the tag comment is for readers, and Renovate keeps both updated.

### Renovate

- Every repository extends the shared preset where the organisation provides one.
  Repository rules add to the preset, not copy it.
- Group updates that always release together: one pull request per logical upgrade.
- `:pinDigests` for container images and GitHub Actions, with Renovate updating both
  the tag and the digest.
- Automerge only for patch updates of trusted dependencies and digest only updates.
  Major updates always get their own reviewed pull request.
- Updates carry the `dependencies` label so the triage skill can find them.

### Release labels

- release-me: `release: pending`/`tagged`/`alpha`/`beta`/`rc` by default, configurable under
  `release-me.yaml`'s `labels.pending`/`labels.tagged`/`labels.prerelease.<type>`; a type set
  to `false` or an empty string is disabled.
- `labels.create-missing` (default `true`) makes release-me create a missing label itself;
  `false` restores the old behaviour, report by name and fail.
- release-please: `autorelease: pending` and `autorelease: tagged`, fixed.
- Either set is owned by its tool. A missing label is never created by hand.

## Guardrails

- Commit types match the intended version bump.
- The release tool's config and any state file committed, no hand written versions.
- Changelogs and versions belong to the release tool. Never hand edit them, and never cut a
  release with the CLI where the release tool is configured.
- Breaking changes documented with a migration path in the commit body.
- Actions and images pinned by digest, with Renovate keeping them current.
- Automerge limited to low risk updates, major updates always reviewed.

## References

- `ci-conventions` for workflow files and the action pinning rule.
- `git-conventions` for the merge strategy that keeps commits visible to the release tool.
- release-me ships a `migrate-release-please-to-release-me` skill through skills.sh, for
  moving an existing release-please repository over.
- <https://github.com/googleapis/release-please>
- <https://www.conventionalcommits.org/en/v1.0.0/>
- <https://docs.renovatebot.com/configuration-options/>
