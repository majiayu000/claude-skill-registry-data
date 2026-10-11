---
name: anthill-release-tagging
description: Use when pushing AntHill work to main, or when asked to tag it, cut a release, or ship the client to the studio's beta machines. Also use before creating or pushing any v* tag in the AntHill repository.
---

# Tagging an AntHill release

## Overview

In AntHill a `v*` tag is a client release, not a label. Pushing `main` deploys the dashboard.
Pushing an annotated tag on the tip of `main` also builds the client and publishes it to every
beta machine. So there is no tag unless a release is wanted, and then exactly one, on the tip.

The repository's full reference is `wiki/content/Cutting a release.md`.

## Push or release?

| The user says | Do |
|---|---|
| "push it" | `git push origin main`. No tag, and no question about one. |
| "tag it", "ship the client", "release it" | Push `main`, then one tag on the tip. Asking was the approval. |
| Many commits since the last tag | Still one tag. Commits between releases stay untagged. Never backfill them. |

## The tag

- **Name:** the newest tag plus one. `git tag -l "v*" --sort=-v:refname | head -1` gives, say,
  `v1.1.0-beta.30`, so the next is `v1.1.0-beta.31`. Starting a new series, such as
  `v1.2.0-beta.1`, is the user's call.
- **Annotated**, on `HEAD`, after `main` is pushed.
- **Message:** the first line is the release's title. It names the forge release and heads the
  client's "What changed" screen. Write one plain sentence saying what changed for the studio,
  chosen by you from the commits, such as `Pull sets a deleted folder up again`. Not the version
  number, and not one commit's subject word for word; the changelog drops a title that equals one.

## Steps

```bash
git fetch --tags origin
git push origin main
git status -sb                                  # "## main...origin/main", nothing ahead
git tag -l "v*" --sort=-v:refname | head -1     # the newest tag
git tag -a v1.1.0-beta.31 -m "Pull sets a deleted folder up again" HEAD
git for-each-ref --format="%(objecttype)" refs/tags/v1.1.0-beta.31   # prints: tag
git push origin v1.1.0-beta.31
git ls-remote --tags origin "v1.1.0-beta.31*"   # two lines; the ^{} one is HEAD's SHA
```

As you push the tag, tell the user it ships a client to the beta machines, and give the title.

## After the push

- `publish-client.yml` runs on the forge's Actions page
  (https://git.ba.bigant-internal.com/alex.mollard/AntHill/actions) in about two and a half
  minutes. Its first job checks the tag is on the tip of `origin/main` at that moment; a tag
  anywhere else builds nothing. Push nothing more to `main` until that check has passed.
- The release page should carry your title, list every commit since the previous tag under
  "What changed", and hold the installer, the portable zip and the full and delta packages.
- Whether the installer is signed is `SIGN_RELEASES` in `publish-client.yml`. Read it before
  saying so.

## Mistakes

| Mistake | Instead |
|---|---|
| One tag per commit, or backfilling untagged commits | One tag on the tip. A tag below the tip publishes nothing. |
| Tagging on "push it" | A tag ships a client. Tag only when a release is asked for. |
| The version number, or a commit subject, as the message | A sentence saying what changed for artists. |
| A lightweight tag | `git tag -a`. `%(objecttype)` must print `tag`. |
| Continuing `v1.0.0-beta.*`, or sorting tags by plain name | Sort with `-v:refname`. Plain name order puts `beta.9` above `beta.30`. |
| Deleting or renumbering a published tag | Keep it and count on from it, because clients never step down a version. Renaming the release on the forge fixes the release page only: the client's "What changed" reads the tag's message and keeps it. So get the title right before pushing. The wiki page covers the one exception: a lightweight tag caught before anyone installed it. |
| Retrying a push that printed an error | "Everything up-to-date" on a retry means the first push landed. Check with `ls-remote`. |

When "What changed" is wrong, use anthill-release-notes-repair.
