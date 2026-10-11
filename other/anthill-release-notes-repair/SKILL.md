---
name: anthill-release-notes-repair
description: Use when asked to rename or fix a published AntHill release, or when its "What changed" entry or forge page shows no title, the version as its title, "Nothing was recorded", or no release at all.
---

# Repairing AntHill release notes

## Overview

Every release's notes come from git tags. When `publish-client.yml` runs, `build/changelog.ps1`
writes `changelog.json`, packed into the client for "What changed", and the forge page's body,
headed by the tag message's first line. The pipeline then names the forge release after that
line. Nothing reads the forge back. So the tags are the truth, a shipped package never changes,
and most of what looks wrong is designed behaviour.

## Find the cause

Reproduce it first, writing outside the repository:

```powershell
pwsh -NoProfile -File build/changelog.ps1 -JsonPath <scratch>/changelog.json -NotesPath <scratch>/notes.md -Tag <tag>
```

| What you see | Cause |
|---|---|
| The version as the title | The tag's message was the version. beta.11, beta.12 and beta.22 to beta.30 went out that way. |
| No title, only the version | A lightweight tag, or a first line identical to the subject of the release's only commit. Both are dropped on purpose; the comments in `changelog.ps1` and the wiki's `Cutting a release.md` say why. The forge name has no such rule, so it can still show that subject. |
| "Nothing was recorded for this one" | The tag points at the same commit as the previous version's tag, or at an ancestor of it, so its range is empty. |
| No release page (404) | The tag wasn't on the tip of `origin/main` when the pipeline ran, so its guard logged "History, not a release" and built nothing. That's by design. |

## What each fix reaches

- **The forge page:** rename the release, and edit the `# title` line that opens its body. It's
  a published page, so only with the user's go-ahead. This reaches the forge and nothing else.
- **"What changed" in the client:** nothing reaches it for a published tag. Every package
  rebuilds it from the tag messages, so tell the user it keeps what the tag says.
- `tools/backfill-release-notes.ps1` rebuilds bodies from those same tags and, when a tag gives
  a title, renames the release to it. It can't fix a title, and run after a hand rename it puts
  the tag's title back.

Preventing a repeat is anthill-release-tagging's job.

## Don't

- **Change `changelog.ps1` or `publish-client.yml` to make one release read better.** Every rule
  above is deliberate. If one looks wrong, raise it with the user as a design change.
- **Rewrite a published tag,** even only its message, and even once `main` has moved past it.
  Published tags are kept. Each forge release is tied to its tag, other clones keep the old one
  because `git fetch` won't overwrite a tag without `--force`, and what a rewrite does to the
  forge and the update feed is untried. If the user wants the client's title changed, tell them
  this and let them decide.
- **Create a release by hand for a tag that has none,** prerelease or not. The pipeline makes
  no release for a history tag on purpose, and that tag's notes are already in every client's
  "What changed".
- **Read a token out of the credential store, or type one in.** Anything that needs a token is
  the user's to run.
