---
name: visual-diff-branches
description: "Use when the question is how pages render on one git ref versus another: checking a design-system, tokens, typography or styling PR for visual regressions on your feature's pages, producing before/after screenshots for a designer, answering 'did this branch change how X looks', or when a screenshot comparison is needed and no image library (ImageMagick, Pillow, sharp, pixelmatch) is installed. Triggers on 'compare main vs this branch', 'before and after screenshots', 'visual regression on this PR', 'what changed visually', 'side by side for design'."
---

# Visual Diff Branches

Answer "what does this branch change on these pages" with evidence: the same pages captured on each ref, pixel-diffed to show *where*, and measured with computed styles to show *what*. Everything runs on the browser the project already has (Playwright's Chromium), so nothing gets installed.

Scripts live in `scripts/` next to this file. They resolve `@playwright/test` from the **project's** `node_modules`, so run them with the project root as the working directory and pass the scripts by absolute path. The only file you write per project is a `shots.mjs` config (contract in `references/config.md`, worked example in `references/shots.example.mjs`).

---

## Step 1: Decide what "the branch" means

A PR branch is usually behind its base. Comparing the raw branch against main mixes the PR's own changes with every fix main landed since the branch forked, and those show up as regressions the PR did not cause. Decide up front and say which one you compared:

| Question | Compare |
|---|---|
| "What will land if this merges?" (the usual case) | a throwaway branch: `git checkout -B smoke/<name> origin/<branch> && git merge --no-edit origin/main` |
| "What does the branch look like exactly as pushed?" | the branch itself |

Check `git rev-list --count origin/<branch>..origin/main` and quote the number in the report. If a difference appears on the raw branch but not on the merged one, it is a missing main fix, not a PR finding; say so and name the commit (`git log --oneline origin/<branch>..origin/main -- <file>`).

Tell the user before the first checkout. Their working tree is about to change branches under a running dev server.

## Step 2: Write `shots.mjs`

One config per project, kept out of git (`.build/` or the scratchpad). It names the base URL, the saved login state, the locales and viewports, the shot list (a URL plus an optional `after(page)` that clicks into a flyout, picks a menu, opens an editor), and the measurement targets. See `references/config.md`.

Pick pages that exercise what the branch touches: a list with a table, a form with inputs and buttons, a flyout or modal, an empty state. Include every locale the product ships if the change is typographic; a font-size change can be harmless in one script and unreadable in another.

Probe each URL once before running the matrix. One URL that redirects to login or fires a logout call (a venue the saved session cannot open, for example) turns every later shot in the run into a login page. Drop it or switch to a URL the session can reach.

## Step 3: Capture, one variant at a time

```
pnpm exec playwright test --project=setup          # or whatever refreshes the saved session
node <skill>/scripts/capture.mjs ./shots.mjs main ./shots
git checkout -B smoke/pr origin/feat/pr && git merge --no-edit origin/main
<skill>/scripts/wait-for-rebuild.sh <dev-server-log> <any-watched-source-file>
pnpm exec playwright test --project=setup
node <skill>/scripts/capture.mjs ./shots.mjs pr ./shots
```

Three things the loop above encodes, learned the hard way:

- **Refresh the saved session before every variant.** Sessions expire in well under an hour; a run that outlives one silently produces login pages from that point on, all the same file size.
- **Wait for a clean compile after a checkout.** The watcher usually compiles once mid-checkout (missing modules) and once clean. `wait-for-rebuild.sh` waits for a new compile line without errors and re-touches a file when the last one was dirty.
- **Read the size column.** `capture.mjs` prints the rendered page size per shot. A shot that is viewport-height when its siblings are three screens tall was captured on a spinner; re-run it with `--only <name>`.

Run capture with the sandbox disabled when your agent sandbox blocks `localhost`.

## Step 4: Measure, do not squint

Pixel diffs locate a change; they cannot tell a 3px radius from a pill, or 16px from 14px. Run the measurement pass on each variant and compare:

```
node <skill>/scripts/measure.mjs ./shots.mjs main ./shots
node <skill>/scripts/measure.mjs ./shots.mjs pr ./shots
node <skill>/scripts/compare-measures.mjs ./shots main pr
```

Targets are Playwright locators, so use text and roles (`getByText('Save changes')`, `getByRole('button', …)`) that survive markup changes. Mark containers with `box: true` to also record background, border, radius, padding, height and width. The compare output lists only rows that differ, with the base value first.

Every finding in the report should rest on a measured pair, not on how a screenshot looks. "Buttons look rounder" becomes "button radius 3px → 80px on Save, Cancel, New Modifier", which the author can act on and the reviewer can verify.

## Step 5: Diff and compose

```
node <skill>/scripts/diff.mjs ./shots main pr
node <skill>/scripts/compose.mjs ./shots main pr ./for-design --labels "main (today)|design-system PR" \
     modifiers.en.1280.png:190,80,900,600 item-flyout.en.1280.png
```

`diff.mjs` writes `diff-pr/<file>.png` with changed pixels in red over a faded base and prints changed %, both sizes and the bounding box per file. Use the table to pick which shots deserve a composite; a 0.3% change confined to one row is a note, a 7% change across the page is a screenshot. Read at least two diff images before describing a variant as "only X changed". A localized red blob you did not expect is a finding.

`compose.mjs` draws two shots side by side with labels, optionally cropped (`file:x,y,w,h`) so the designer sees the buttons and inputs, not the sidebar. Number the files in the order you want them read.

## Step 6: Report and clean up

Report in this shape:

1. Which refs were compared and whether main was merged in.
2. Regressions the branch introduces, each with the measured before/after values.
3. Deliberate changes the branch makes that diverge from the design spec, framed as a question for the design owner, not asserted as intent or as a bug.
4. Pre-existing gaps you noticed on the base, kept separate so nobody blames the PR for them.
5. Coverage gaps: pages you could not reach, states you could not produce (empty tables, no orders).

Then `git checkout <original branch>`, delete the throwaway branches, wait for the rebuild once more, and say what the checkout is.

---

## Common mistakes

| Mistake | What to do instead |
|---|---|
| Cloning the repo and starting a second dev server on another port | One server, throwaway branch, `wait-for-rebuild.sh`. Cloning costs a full install and drifts on config; the watcher already rebuilds on checkout. |
| Installing pixelmatch, pngjs, sharp or Pillow | `diff.mjs` and `compose.mjs` use a canvas in the headless browser the project already has. |
| Explaining "what changed" from the SCSS diff | The diff says what the author touched; `measure.mjs` says what the page renders. Both, and the report cites the measured one. |
| One saved session for the whole run | Refresh per variant; check the size column for the login-page tell. |
| Comparing the raw branch and reporting a regression that is a missing main fix | Step 1. Merge main on a throwaway branch and name the commit when the raw branch differs. |
| Placeholder ready-selectors ("fix once I can see the page") | Probe the URL first, then write the `after` step against the real markup. |
| Leaving the repo on the throwaway branch | Step 6. The user's next `git status` should look like it did before you started. |
