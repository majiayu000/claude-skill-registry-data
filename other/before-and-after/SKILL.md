---
name: before-and-after
description: Capture before/after proof for a PR and put it in the PR body. Screenshots for anything with a visible surface, measured numbers for anything without. Use when opening a PR, when the user says "before and after", "PR screenshots", "visual diff", "show me proof".
allowed-tools:
  - Bash(npx @vercel/before-and-after *)
  - Bash(before-and-after *)
  - Bash(which before-and-after)
  - Bash(which gh)
  - Bash(npm install -g @vercel/before-and-after)
  - Bash(*/upload-and-copy.sh *)
  - Bash(curl -s -o /dev/null -w *)
  - Bash(gh pr view:*)
  - Bash(gh pr edit:*)
  - Bash(lsof -i:*)
---

# Before and after

Every PR carries proof. A reviewer should be able to tell the change works
without reading the diff.

> Package is `@vercel/before-and-after`. Plain `before-and-after` on npm is a
> different package, do not install it.

Adapted from [vercel-labs/before-and-after](https://github.com/vercel-labs/before-and-after),
PolyForm Shield 1.0.0, license in this folder.

## Data rule, read this first

1. **There is no account and no database, so the only data on screen is
   whatever is typed into the editor.** Billy keeps the draft in the browser's
   `localStorage` (`billy_invoice_data`). Before capturing, load a made-up
   invoice with obviously fake names, addresses, GSTIN and bank details, or a
   profession preset. Never capture a draft that holds someone's real client or
   bank details. If the browser profile you drive has been used for real
   invoices, clear `billy_invoice_data` first, or use a fresh profile.
   The dev server is `bun run dev` on http://localhost:3000. Routes are `/` and
   `/editor`. For a WYSIWYG change, capture the exported PDF as well as the
   screen, since the PDF is the thing that has to match.
2. **Never upload to the default host.** The upstream default adapter posts to
   `0x0.st`, a public paste host with no auth and no delete. This kit defaults to
   the gist adapter instead, which creates a secret, unlisted gist. Secret is
   not access-controlled, anyone with the URL can read it, so it is a step up
   from a public paste host and not a substitute for keeping something private.
   Set it explicitly every time:

   ```bash
   IMAGE_ADAPTER=gist ./scripts/upload-and-copy.sh before.png after.png --markdown
   ```

   Better still, drag the PNGs into the PR body on github.com, which stores them
   on GitHub behind the repo's own access control. Use that for anything you are
   unsure about.

## Which kind of proof

| Change touches | Proof |
|---|---|
| Any page or component a user sees | Screenshot pair |
| A flow that only makes sense over time | Short screen recording, see `evidence-driven-testing` |
| Latency, token cost, query count, bundle size | Measured numbers, before and after, same conditions |
| A migration | Row counts and index list before and after |
| Backend logic with no surface | Test output, or a curl pair showing the old and new response |

A change with no visible surface still needs proof. Numbers count.

## Capture

Do not switch branches, stash, or guess what "before" is. Current state is
**after**. Ask for the before source when it is not obvious:

> What should I use for the before state: the deployed app, a preview URL, or
> should I stash to the base commit and capture locally?

Record this project's local ports here. Confirm the port answers *your* dev
server before trusting it, since ports are global and worktrees share them:

```bash
lsof -i :<port>
```

Then:

```bash
# Pre-flight
which before-and-after || npm install -g @vercel/before-and-after

# Two URLs
before-and-after "http://localhost:<port>/<route>" "http://localhost:<port>/<route>"

# One component, which is usually what you want, it keeps other firms' data out
before-and-after <url1> <url2> ".the-component"

# Two PNGs you already captured while developing
before-and-after before.png after.png --markdown

# Viewports
before-and-after <url1> <url2> --mobile   # 375x812
before-and-after <url1> <url2> --tablet   # 768x1024
```

| Flag | Meaning |
|---|---|
| `-m, --mobile` | 375x812 |
| `-t, --tablet` | 768x1024 |
| `--size <WxH>` | Custom viewport |
| `-f, --full` | Full scroll, only when asked |
| `-s, --selector` | CSS selector |
| `-o, --output` | Output dir, default `~/Downloads` |
| `--markdown` | Upload and print the table |
| `--upload-url` | Custom endpoint |

Do not pass `--full` unless the user asks for a full-page capture. A full page
pulls in the sidebar and any surrounding chrome, which is how real data leaks
into a screenshot.

In a container or VM where Chrome reports "No usable sandbox", set
`AGENT_BROWSER_ARGS="--no-sandbox"` for the capture command.

## Never commit a screenshot to the repo

Git keeps every blob forever. A deleted PNG is still in history, still in every
clone, still counted against the repo size. Two screenshots run about 800 KB, so
one a week is tens of megabytes a year that nobody can ever reclaim without
rewriting history for everyone. This repo merges with merge commits rather than
squashing, so anything committed on a branch lands in `main`'s history intact.

So: screenshots do not go in `docs/`, in the source tree, or anywhere under
version control.

A capture is a build artifact. Treat it like one.

### Upload it instead

```bash
./scripts/publish-captures.sh before.png after.png            # print the markdown
./scripts/publish-captures.sh --pr <n> before.png after.png   # and append it to the PR
```

That posts each file to GitHub's attachment store, the same place a file dragged
into a PR description ends up, and prints a markdown table to paste in. The
images **render inline**, including on a private repo, and nothing is committed.

It needs nothing but an authenticated `gh`. No secret, no workflow, no branch.

Dragging the files into the PR description in a browser does exactly the same
thing and is still fine when you are there anyway.

### Why this works on a private repo when a link to a repo file does not

GitHub fetches a copy of every image in a PR body through a proxy that is not
logged in as the reader. A URL pointing into a private repo gets refused, so the
image is broken for everyone. Anything that does render from such a URL had to
be publicly readable, which is why a bucket or a secret gist does not solve
this, it only moves where the public copy lives.

Attachments are the exception: GitHub stores and serves them itself, so there is
no fetch to fail, and access follows the repo.

The upload endpoint is `POST https://uploads.github.com/user-attachments/assets`
with a Bearer token. GitHub has not documented it, so if it starts returning 404
or 422, assume it changed and drag the files in by hand rather than debugging
the script.

## Put it in the PR

The table goes in the PR body, not a comment, so it is the first thing a reviewer
sees.

```bash
gh pr view --json number,body
gh pr edit <number> --body "<existing body>

## Before and after

| Before | After |
|:------:|:-----:|
| ![Before](<url>) | ![After](<url>) |
"
```

When the proof is numbers instead of images:

```markdown
## Before and after

| Metric | Before | After |
|---|---:|---:|
| `/api/items` p95 | 815 ms | 61 ms |
| DB queries per request | 43 | 2 |

Measured on the seeded test account, 20 records, same machine, 10 runs.
```

State the conditions. A number without conditions is not proof.

## When the after does not match the claim

Look at the after capture before you post it. If it does not show the feature
working, the change is not done. Go back and build, then capture again. Do not
post a pair that shows the old behavior and describe it as fixed.

## Errors

| Error | Fix |
|---|---|
| `command not found` | `npm install -g @vercel/before-and-after` |
| `could not determine executable` | Use the full name, `npx @vercel/before-and-after` |
| Element not found | Check the selector exists on the page |
| Blank screenshot on a protected route | Not logged in. Sign in as the test user first |
| Upload went to 0x0.st | You forgot `IMAGE_ADAPTER=gist`. Delete nothing, it cannot be deleted. Report it |
