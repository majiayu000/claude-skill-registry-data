---
name: gh-attach
description: >-
  Upload an image or video to a GitHub issue, pull request, or comment with the
  GitHub CLI's `--attach` flag, and control where it renders in the body. Use
  when attaching or embedding a screenshot, screen recording, diagram, or GIF
  through `gh`, when a body already written references a local image path, or
  when a `gh` attachment upload fails.
---

# gh-attach

`gh` uploads a local image or video to GitHub's user-attachments CDN and
rewrites the markdown to point at the uploaded asset. The asset renders inline
for anyone who can read the repository, in private repositories as well as
public ones.

The flag works on these commands:

| Command            | Destination of the attachment                       |
| ------------------ | --------------------------------------------------- |
| `gh issue create`  | the new issue's body                                |
| `gh issue comment` | the new comment, or the edited one on `--edit-last` |
| `gh issue edit`    | the issue's body                                    |
| `gh pr create`     | the new pull request's body                         |
| `gh pr comment`    | the new comment, or the edited one on `--edit-last` |
| `gh pr edit`       | the pull request's body                             |

## Before attaching

Confirm the installed `gh` carries the flag:

```bash
gh issue comment --help | grep -- --attach
```

Empty output means the flag is missing from this build - upgrade `gh` and tell
the user that is the blocker.

An upload is gated on the host, the repository permission, and the
credential. A refusal on any of the three stops the command before it posts
anything:

- **Host**: github.com and GitHub Enterprise Cloud, including `ghe.com`
  data-residency tenants. GitHub Enterprise Server is refused.
- **Permission**: write, maintain, or admin on the target repository. Read and
  triage are refused.
- **Credential**: a token from `gh auth login`, a classic personal access
  token, or a fine-grained one. Other credential kinds are refused.

## Attaching

`--attach` takes one file and repeats for more:

```bash
gh issue comment 12 --repo monalisa/monas-cafe \
  --body "The menu breaks on load:" \
  --attach ./menu-error.png
```

Written this way the image is appended as its own paragraph after the body, in
flag order.

To place an attachment inside the body instead, reference its local path from
the markdown and pass the same path to `--attach`. `gh` then edits that
reference to point at the uploaded asset and appends nothing:

```bash
gh pr create --title "Fix the menu" \
  --body 'Before: ![the broken menu](./before.png)

After: ![the fixed menu](./after.png)' \
  --attach ./before.png --attach ./after.png
```

A reference-style link works the same way - `gh` edits the definition, so every
use of the label follows.

## Alt text

Alt text follows the path after `#`:

```bash
gh issue create --attach './login.png#The login error state'
```

Quote the argument so the shell keeps the `#`. A path that exists wins over the
delimiter, so a filename containing `#` doesn't need escaping.

Alt text the body already wrote wins over the flag. Without either, `gh` falls
back to the filename with its extension stripped and remaining dots turned into
spaces.

Video renders as a player, which has no alt attribute, so
`--attach './clip.mp4#anything'` fails.

## Video

GitHub renders a video only from a bare URL that is the whole content of a
paragraph. `gh` follows that rule when it rewrites:

| How the body writes the video             | What it becomes                                          |
| ----------------------------------------- | -------------------------------------------------------- |
| `![alt](./clip.mp4)` alone in a paragraph | the bare URL, which plays                                |
| `![alt](./clip.mp4)` mid-sentence         | `[alt](URL)`, a link                                     |
| `[text](./clip.mp4)`                      | `[text](URL)`, a link                                    |
| `![alt][label]` reference-style           | error: `cannot embed a video as a reference-style image` |

A video the body never references is appended as a bare URL and plays.

## Files `gh` accepts

| Kind  | Extensions                                 | Size ceiling |
| ----- | ------------------------------------------ | ------------ |
| Image | `png`, `jpg`, `jpeg`, `gif`, `webp`, `svg` | 10 MB        |
| Video | `mp4`, `mov`, `webm`                       | 100 MB       |

`gh` reads the extension alone. The account plan sets the real video ceiling,
so the server refuses a file under 100 MB that the plan disallows.

Each `--attach` argument must name a distinct regular file with bytes in it.
A directory, a FIFO, a zero-byte file, `-` for standard input, and the same
file passed twice under two names each fail validation.

## Flag conflicts

`--attach` is rejected alongside `--web`, `--dry-run`, and `--delete-last`.
`gh issue edit` and `gh pr edit` reject it when the invocation names more than
one issue or pull request.

On the comment commands, an attachment counts as body input on its own:
`gh pr comment 13 --attach ./shot.png` posts a comment holding only the image
and doesn't prompt. With `--edit-last` and no body flag, the existing comment
keeps its text and the attachment is appended to it.

## Partial uploads

An upload cannot be undone, and GitHub doesn't expose an endpoint to delete an
asset. `gh` stops at the first failed file and still writes the body pointing
at the files that did upload, then reports the error. Read the exit as partial:
check what the issue or pull request now shows before retrying, and re-attach
only the files that are missing.

A 404 from the endpoint means the token cannot write to the repository - `gh`
translates it, since the endpoint answers 404 where 403 would be the honest
status.

## More detail

- `references/markdown-rewriting.md` - read when the body holds markdown beyond
  a plain `![alt](./file.png)`: titles, nesting, code spans, escaped or
  parenthesised paths, or a reference definition, and you need to know which
  ones `gh` rewrites.
