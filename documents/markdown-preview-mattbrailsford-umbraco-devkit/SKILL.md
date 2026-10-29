---
name: markdown-preview
description: >-
  Opens a Markdown file or folder in the browser as GitHub will show it, drawn by GitHub's own
  renderer, refreshing as the file changes. A folder opens GitHub-style, its file list beside
  its README. Readers comment on any line and send the comments to Claude in one batch, and
  Claude fixes the doc and replies on each. Use when the user asks to see, show, open, view or
  preview a doc ("show me the brief", "open the plan", "preview the spec"), or says "go
  through my comments". Also owns when a phase offers a preview, how a step picks up open
  comments left on its files, which docs a step asks the reader to approve, and the check
  for unresolved comments and approvals before a step moves on.
user-invocable: true
argument-hint: [file or folder, optional]
---

# markdown-preview

Show a doc the way GitHub will, while it's still on disk, and let the reader comment on it
in place. GitHub turns the Markdown into HTML, so what the reader sees here is what they'll
see in a PR or on the repo. The page refreshes each time the file is saved, so a comment can
be fixed while the reader watches. Whatever changed since the reader last sent comments is
marked: added text in green, removed text struck through in red. An edited paragraph that
only gained or only lost words shows once with the change marked in place; one that did both
shows old above new, with just the changed words picked out. So they can check every edit
made in answer, not just the line they commented on.

## Pick what to open

- **"The plan", "the plan folder"**: the current feature's plan folder, scoped to it (below).
  Its page shows `README.md`, the read-order index, beside a file list in that same order.
  Find the folder the way the pipeline does (see `CLAUDE.md`'s "Finding the current
  feature's plan folder"), and ask only if it's still ambiguous.
- **"The brief", "the spec", "the plan's tasks"**: that file in the plan folder, scoped to
  the folder.
- **A named file or folder**: that one, unscoped unless it's in a plan folder.
- **Nothing named**: the file you last wrote or the user last mentioned in this session.

**Scope** keeps the page's navigation and comments inside one folder: the path bar starts
there, the file list has no way up, and pages outside it are read-only. Images and links that
reach outside still work.

## Open it

Run `scripts/preview.py` from this skill's folder as a background command, then start the
comment helper from the same folder, also in the background:

```bash
python3 <this skill's folder>/scripts/preview.py <file-or-folder> [--scope [<folder>]]
python3 <this skill's folder>/scripts/preview.py wait
```

- `--scope` on its own scopes to the opened folder, or the file's folder. Name a folder to
  scope wider.
- `--no-comments` opens it read-only, for "just show me". Then don't start the helper.
- **One server and one helper per git worktree.** Asking again reuses them: an open preview
  tab is sent to the new page instead of opening another, and a second helper exits at once
  saying one is already waiting. Never stop a running server to open another file.
- The script prints the page's URL. Give it to the user.
- The server stops when the session ends, when it's killed, or once its worktree is removed.
  The helper then stops by itself within a minute, saying the preview has stopped. Don't start
  it again unless the preview is opened again.

## Review comments

The reader leaves comments on lines, table rows, diagrams or picked-out words, then clicks
"Send to Claude". The helper's background run then finishes, and its output is the batch. (It
also finishes once every doc asked for is approved; see "Approval".)
"Go through my comments" means the same: `scripts/preview.py comments` prints the batch.

Answer every comment in the batch, then start the helper again for the next one. Only the
reader resolves a comment. The most Claude does is mark it done, for them to check. For each:

1. **Find the spot.** The batch gives each comment's file, the text it's on, the text around
   it and the section heading it's under.
2. **Decide who may change the file.** A plan folder's files each have one owner: the step
   whose "Where this writes" names it.
   - **This run owns the file, or no step is running** (the user only opened the preview):
     make the change, following the owning skill's rules for that file. Then
     `scripts/preview.py reply <id> "<what changed>" --done`.
   - **Another step owns it, and a step is running:** don't touch the file.
     `scripts/preview.py reply <id> "Left for <step>." --defer <step>`. That step picks it
     up under "Open comments on your files".
3. **Unsure what's wanted, or it needs a decision only the user can make:** ask, don't
   guess. `scripts/preview.py reply <id> "<question>"`, with no flag, leaves it open as
   "Waiting on you". Their answer comes back in a later batch with the whole thread.
4. **Just an acknowledgement** ("looks great"): reply briefly with `--done`.

- **A suggested change** (a ```` ```suggestion ```` block, as on GitHub) is the reader's exact
  new wording. Use it word for word, keeping the line's own Markdown (links, code, bold)
  where the words carry over, then reply with `--done`.

- A change that settles a decision gets a line in `DECISION-LOG.md`, as every phase's does.
- Replies are a sentence or two: what changed, or the one question. The reader sees them
  beside the line.

## Check before removing text

A comment often settles something the doc left open: an `IMPORTANT` box asking for a
decision, a list of options. The change can then replace or remove the text it was on, and
other text around it. Before saving, list the file's open comments
(`scripts/preview.py comments --file <path>`) and, for each one on text you're replacing or
removing:

- **The comment that prompted the change:** add `--move "<new text>"` to its reply, so it
  stays pinned beside what replaced its text. The thread keeps the text it was first made
  on, struck through as "Was:", so the comment still makes sense.
- **Any other open comment on removed text:** reply saying the text is gone and why, with
  `--done`. Don't leave it to be found later.

A comment whose line goes some other way (the reader edits the file) shows under its
section's heading, marked "Line removed". If the heading's gone too, it's listed at the
bottom of the doc. Either way it stays open until the reader resolves it.

## Open comments on your files

A step that owns files in a plan folder checks them for open comments before it starts:

```bash
python3 <this skill's folder>/scripts/preview.py comments --file <path> [--file <path>...]
```

Each comment listed as new, or left for this step, is part of this run's input. Handle it
under "Review comments" as part of the step's normal work, and reply on it. The rest are
waiting on the reader; leave them, apart from "Check before removing text". This reads the
comments straight from the worktree, so the preview needn't be open.

## Comments before moving on

A step that builds on a plan folder (`feature-design`, `feature-plan`, `feature-build`), or
archives one (`feature-close`), first checks the whole folder for anything unresolved, and
whether the last step's docs were approved:

```bash
python3 <this skill's folder>/scripts/preview.py comments --folder <plan folder>
python3 <this skill's folder>/scripts/preview.py approval
```

- **New, or left for this step:** input to this run, under "Open comments on your files".
- **Left for an earlier step** (one parked for `feature-design` when `feature-plan` runs):
  stop, and send the user to that step. It's that step's question to settle, not this one's
  to guess at.
- **Waiting on the reader:** their answer ("Waiting on you"), their check ("Done, please
  check"), or a comment they wrote but didn't send. List them in one message and ask whether
  to deal with them first or carry on. One question, not one per comment; "carry on" is a
  fine answer. If this step already asks the user something before starting, ask it there.
- **A doc asked for approval isn't approved** (still waiting, or changed since): name it in
  that same question. Approving is the reader's call, so "carry on" is still a fine answer.
- **Nothing open, and no approval waiting (or none asked for):** carry on without mentioning
  it.

## Approval

A step's Hand off asks the reader to approve the docs it owns, as a PR is approved on
GitHub. Only when a preview has been opened this session; without one, the usual Hand off
stands in for it.

```bash
python3 <this skill's folder>/scripts/preview.py approval --request <file> [<file>...] --step <step>
```

| Step | Asks for approval on |
| --- | --- |
| `feature-explore` | `BRIEF.md` |
| `feature-design` | `SPEC.md` and `ARCHITECTURE.md` |
| `feature-plan` | `PLAN.md` |

- Each ask replaces the last, so the page only marks this step's docs. Say in the Hand off
  which docs are waiting for approval.
- The reader approves on the page, once a doc's comments are all resolved. Claude never
  approves: as with resolving, there's no command for it.
- A doc changed after approval needs approving again. The page shows which.
- The helper also wakes once every doc asked for is approved. Say so in one line, give the
  suggested next step, and start the helper again. Don't start the next step unasked.

## Offering a preview

A phase that writes a doc a person reviews (`BRIEF.md`, `ARCHITECTURE.md`, `SPEC.md`,
`PLAN.md`) offers to open it in its Hand off, before the suggested next step:

- **First time this session:** one line, such as "Open BRIEF.md in a live preview? You can
  comment on it there. It sends the file's text to GitHub to be drawn." Then carry on. It's
  an offer, not a stop.
- **A preview is already open in this worktree:** don't ask. Open the new file on it.
- **The user said no earlier this session:** don't offer again.

## *What it needs*

- macOS, `python3` (part of Xcode's command line tools, which git already needs) and `gh`,
  signed in. `gh auth status` says whether it is.
- Internet access: GitHub draws the page, and the styles, Mermaid and math load from a CDN.
- The file's text, and the text of comments on it, go to GitHub's Markdown API to be drawn,
  including plans that aren't committed. Nothing else is sent anywhere. The `gh` sign-in is read once and kept in memory only.
- Comments are kept in the worktree's git folder (`markdown-preview/comments.json` under
  `git rev-parse --git-dir`), and so is a copy of each doc as it was when the reader last sent
  comments (`markdown-preview/seen/`), which the page compares against to mark what's changed,
  and the approvals (`markdown-preview/approvals.json`). None of it is ever committed, and
  removing the worktree removes it.

## *How close it is to GitHub*

- **Drawn by GitHub:** headings, alerts, tables, task lists, footnotes, code colours, `#123`
  issue links for the repo, and remote images through GitHub's image proxy.
- **Finished in the page, as github.com does:** heading anchors, Mermaid and math, with the
  styles from the github-markdown-css package (a copy of GitHub's own). Spacing or a
  diagram's layout can differ by a few pixels.
- **Shown as code, not drawn:** GeoJSON and TopoJSON maps, and STL 3D models. github.com
  draws those in the browser.
- **Other files** open in the page, read-only, as on github.com: source as coloured code,
  images and media in place, anything else (or anything over 512 KB) as a note. HTML mockups
  and PDFs show live in the page, where github.com shows a mockup's source; a **Preview |
  Code** switch, as github.com has for an SVG, shows a mockup's or SVG's source instead. The
  header's **Raw** button opens any of them on its own.
- **Local images, SVGs included,** load from the worktree. One that's broken here will be
  broken on GitHub too.
