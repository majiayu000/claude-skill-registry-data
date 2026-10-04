---
name: "Project: Tag Version"
description: "Tag the release after a merge to main, computing the next semver tag with svu"
when_to_use: "When a merge to main has landed and the release should be tagged, or to report what bump is pending on a branch. Never tags at PR creation, mid-branch or on staging; releases are things that happened to main."
model: sonnet
effort: low
metadata:
  glyph: ᚺ
  family: project
disable-model-invocation: true
allowed-tools: ["Bash(svu:*)", "Bash(git:*)", "Bash(~/.claude/library/scripts/safe-version-next.sh:*)"]
disallowed-tools: ["Bash(git push --tags:*)"] # publishes every stray local tag; this skill pushes single tags only
---

# Tag the release with `svu`

[`svu`](https://github.com/caarlos0/svu) derives the next semver tag from conventional-commit history. It only computes the version; it never commits, pushes or merges.

**Hard rule:** the tag always comes from `safe-version-next.sh`, never bare `svu next`. The script is identical to `svu next` except it refuses to cross 0.x → 1.x automatically; declaring the API stable is a human decision, so it emits a 0.x minor bump instead (and says so on stderr; relay the note when it fires). Later major bumps pass through.

## The one tagging moment: merge to `main`

A release is a commit on `main`; nothing else gets a tag. No tagging at PR creation (the version would point at unreviewed commits, race other open PRs and burn numbers on branches that may never merge), no tagging mid-branch, no plain-semver tags on `staging` (two branches sharing one version sequence means the same number can point at different commits).

From an **up-to-date main checkout** (`git checkout main && git pull` first if there's any doubt; tagging from a feature branch or stale main tags the wrong commit):

```bash
TAG="$("$HOME"/.claude/library/scripts/safe-version-next.sh)" && git tag "$TAG" && git push origin "$TAG"
```

Push the single tag, never `git push --tags`; that publishes every local tag you've ever made, strays included.

Script exit codes: **3** = nothing to release (no version-bumping commits since the current tag): say so and stop, don't force a tag. **2** = environment error; report it.

## Mid-branch: report, never tag

When a branch accumulates significant work, it's worth *saying* what's pending, as information, not an offer to tag. Detect the level by comparing `svu current` with `svu next`:

- Different major segment → major pending
- Same major, different minor → minor pending
- Only the patch segment changed → stay silent

Phrase it as a statement about the future merge:

```text
⬆️ minor bump pending: this branch will tag v1.3.0 when it merges to main.
```

On a **stacked child branch** (its PR's base is another branch, not main), `svu next` counts the unmerged parent layers' commits too: report the pending bump as belonging to the stack as a whole ("this stack will tag..."), never to this layer alone.

Nothing mid-branch ever creates a tag. The tag happens once, on main, after the merge (`pr-land` runs this exact sequence as its Step 3).
