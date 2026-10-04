---
name: github-image-upload
description: Upload local images or video to GitHub and embed them in pull requests, issues or comments, without drag-and-drop and without committing them to the repo. Use when asked to attach, add or upload screenshots, GIFs or video to a PR/issue, when a PR needs before/after evidence, or when someone says GitHub has no API for image uploads.
---

# GitHub image upload

Both routes below put the file in the same place — GitHub's user-attachments store — and both
authenticate with an ordinary `gh auth token`. Pick by whether you need the URL in hand.

| You want | Route |
|---|---|
| An image or video embedded in a body `gh` is writing | `gh --attach` |
| The URL itself — sized `<img>`, a body you patch yourself, a table | `scripts/upload-asset.sh` |

## Route A — `gh --attach`

Needs `gh` 2.99.0 or newer. Available on `issue create`, `issue edit`, `issue comment`,
`pr create`, `pr edit`, `pr comment`.

```bash
gh pr comment 13 --attach './login.png#The login error state'
```

Alt text follows the path after `#`; without it `gh` uses the filename. Video renders as a player
and takes no alt text, so giving it any is an error.

Attachments append to the end of the body. To place them yourself, reference the local paths in the
body and attach those same files — each markdown reference is rewritten to point at the uploaded
asset:

```bash
gh pr create --body-file report.md --attach ./before.png --attach ./after.png
```

Only markdown references are rewritten — `![alt](./before.png)` and `[text](./before.png)`, inline
or reference-style, outside code fences. An `<img src="./before.png">` is not a markdown reference,
so the file is appended instead and the tag stays pointing at a path that does not exist. Sized
images mean route B.

Refused with `--web` and `--dry-run`, and on GitHub Enterprise Server. Uploads cannot be undone, so
`gh` writes the body even when only some attachments succeeded.

## Route B — upload, then embed

```bash
scripts/upload-asset.sh OWNER/REPO before.png after.png
# https://github.com/user-attachments/assets/<uuid>   (one per line, in order)
```

Embed with `<img src="…" width="460">` rather than `![](…)` when the width matters, which it does in
a before/after table:

```markdown
### Desktop
| Before | After |
|---|---|
| <img src="https://github.com/user-attachments/assets/UUID-A" width="460"> | <img src="…UUID-B" width="460"> |

### Mobile (390px)
| Before | After |
|---|---|
| <img src="…UUID-C" width="260"> | <img src="…UUID-D" width="260"> |
```

`gh pr edit` silently fails on repos still carrying classic Projects, so append to an existing body
through the API instead:

```bash
cur=$(gh api repos/OWNER/REPO/pulls/123 --jq .body)
printf '%s\n\n---\n\n%s\n' "$cur" "$NEW_SECTION" > /tmp/body.md
gh api -X PATCH repos/OWNER/REPO/pulls/123 -F body=@/tmp/body.md
```

`-F body=@file` avoids shell-quoting problems with markdown. Issues and comments are
`repos/OWNER/REPO/issues/123` and `repos/OWNER/REPO/issues/comments/<id>`.

## Constraints

- Extensions: `png` `jpg` `jpeg` `gif` `webp` `svg` `mp4` `mov` `webm`
- 10MB per image, 100MB per video, and the server holds video to the account plan below that
- Write access or better — read and triage both get a 404
- An OAuth token, PAT or fine-grained PAT. A GitHub Actions token cannot upload
- github.com and GHEC with data residency; not Enterprise Server

## Gotchas

- **Anonymous `curl` on the asset URL returns 404.** Assets inherit repo visibility. Authenticate
  (`-H "Authorization: token $(gh auth token)"`) to download one, and verify a render by checking
  `naturalWidth > 0` on the page rather than by fetching the URL.
- **GitHub rewrites the URL** at render time into a signed `private-user-images.githubusercontent.com`
  link. Store the `user-attachments` one; it stays valid.
- **Encode video as H.264** (`ffmpeg -i in.webm -c:v libx264 -pix_fmt yuv420p out.mp4`) so GitHub
  renders a native `<video>` rather than a download link.

## When not to use this

If the images get regenerated often, or readers need them without repo access, commit them to a
branch and embed `raw.githubusercontent.com` URLs instead.
