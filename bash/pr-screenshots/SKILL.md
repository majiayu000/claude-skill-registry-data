---
name: pr-screenshots
description: Capture before/after screenshots of visual changes and attach them to a PR. Use when opening a PR, or when asked to "add screenshots to the PR", "show what this looks like", "prove the UI change works", or "document this visually". Any PR that changes rendered output — a route, a shared component, a theme token, or a calculator's displayed result — needs these. Screenshots are uploaded to GitHub's CDN, never committed to the repo.
user_invocable: true
---

# PR Screenshots

A reviewer reading a diff has to imagine the result. Screenshots mean they don't
have to — and they catch the regressions a diff hides: a value that now renders
`NaN`, a card that lost its padding, a theme where the text went invisible.

Two pieces do the work:

- `scripts/pr-screenshots.ts` — captures a **shot list** against a running dev
  server, writes WebP files.
- `gh pr edit --attach` — uploads those files to GitHub's CDN and rewrites the
  local paths in the PR body to permanent `user-attachments/assets/…` URLs.
  Nothing lands in the repo.

`--attach` needs **gh 2.99.0 or newer**. Check with `gh --version` first — on
older gh the flag does not exist and the command fails with
`unknown flag: --attach`. It is also unsupported on GitHub Enterprise Server at
any version.

Upgrading, in order of what's likely to work where you are:

```bash
brew upgrade gh                          # macOS, and Linuxbrew

# No Homebrew, no root — the release tarball works anywhere.
V=2.99.0; OS=linux; ARCH=amd64           # ARCH=arm64 on aarch64
curl -fsSL "https://github.com/cli/cli/releases/download/v$V/gh_${V}_${OS}_${ARCH}.tar.gz" \
  | tar xz -C /tmp
export PATH="/tmp/gh_${V}_${OS}_${ARCH}/bin:$PATH"
gh --version
```

Distro packages (apt, dnf, apk, winget, scoop) lag by days to weeks; check
<https://github.com/cli/cli/blob/trunk/docs/install_linux.md> before assuming
one has 2.99.0 yet.

**If you cannot get gh 2.99.0**, don't improvise an uploader — there is no
scripted fallback in this repo any more, and the browser-driving flow it
replaced was deleted. Capture the shots (steps 2-4), then either hand the files
to a human to drag into the PR comment box, or say in the PR description that
screenshots were captured but could not be uploaded from this environment.
Leaving the section out silently is the one thing that isn't acceptable.

## Step 1 — Decide whether the change is visual

**Visual** if the diff touches any of:

- `apps/dorkroom/src/**` — routes, components, styles
- `packages/ui/**` — shared components, theme tokens
- a calculator in `packages/logic/**` whose result is *displayed*:
  `use-*-calculator.ts`, `use-light-meter-solver.ts`, `border-calculator/`

**Not visual** if the diff only touches `api/`, `packages/api/**`, tests,
configs, docs, or CI.

If it isn't visual, say so in the PR description — one line, e.g. *"No rendered
output changes; no screenshots."* Don't just omit the section, or a reviewer
can't tell whether it was considered or forgotten.

## Step 2 — Map the diff to routes, write the shot list

Routes live in `apps/dorkroom/src/routes/` and map 1:1 to paths
(`reciprocity.tsx` → `/reciprocity`). For a changed shared component or logic
hook, grep for its consumers — every route that renders it is affected.

**Default matrix: desktop × dark, one shot per affected route.** Widen only for
cause:

| Diff touches | Add |
|---|---|
| layout / responsive classes | a `mobile` shot |
| theme tokens, colors, a theme's stylesheet | a shot in *that* theme (not all four) |
| an error path, or output that needs specific inputs | an `actions` block |

Themes are `light`, `dark`, `darkroom`, `high-contrast`. There is no `system` —
a screenshot must be deterministic.

Write the list to `.pr-screenshots/shots.json`:

```jsonc
{
  "shots": [
    // Bare route. Calculators have sensible defaults, so this already renders
    // a real calculation — no actions needed.
    { "id": "reciprocity", "route": "/reciprocity" },

    // A driven state, for an error path or specific inputs.
    {
      "id": "reciprocity-negative",
      "route": "/reciprocity",
      "actions": [
        { "fill": "#duration", "value": "-5" },
        { "waitFor": "[role=alert]" }
      ]
    }
  ]
}
```

Fields: `id` (required — becomes the filename and the image's alt text), `route`
(required), `viewport` (`desktop` | `mobile`, default `desktop`), `theme`
(default `dark`), `actions` (optional: `fill`, `click`, `select`, `waitFor`).

Keep it tight. Three or four shots that show the change beat twelve that bury
it. One `gh` command takes at most **50 attachments**, which is far more than
any honest shot list.

## Step 3 — Capture "after"

**Read the dev server's port from its output; don't hardcode it.**
`@vercel/microfrontends` assigns it from a hash of the package name and
increments when that port is taken, so `PORT=…` does *not* override it. Always read the port
back from the server's own output:

```bash
bun run dev > /tmp/dr-after.log 2>&1 &
until grep -q 'Local:' /tmp/dr-after.log; do sleep 1; done
AFTER=$(grep -o 'http://localhost:[0-9]*' /tmp/dr-after.log | head -1)

bun run scripts/pr-screenshots.ts .pr-screenshots/shots.json \
  --base-url "$AFTER" --out-dir .pr-screenshots/after
```

If a shot fails here, the shot list is wrong — a bad selector, a route that
doesn't exist. Fix it; don't ship a PR with a missing screenshot.

## Step 4 — Capture "before"

The "before" state is the merge-base, not your working tree. Get it from a
worktree, which never touches your working tree — no stashing, nothing to lose.

**Stop the "after" server first.** The two dev servers cannot run side by side:
the microfrontends proxy claims a fixed port and dies with `Microfrontends proxy
error: Port is not available` rather than picking another one. (Bare `vite` does
increment — `bun run dev` doesn't, because the proxy is in front of it.)

```bash
pkill -f 'turbo run dev'          # free the port before starting the second server

BASE=$(git merge-base HEAD origin/main)
git worktree add --detach /tmp/dr-before "$BASE"
(cd /tmp/dr-before && bun install && bun run dev > /tmp/dr-before.log 2>&1 &)
until grep -q 'Local:' /tmp/dr-before.log; do sleep 1; done
BEFORE=$(grep -o 'http://localhost:[0-9]*' /tmp/dr-before.log | head -1)

bun run scripts/pr-screenshots.ts .pr-screenshots/shots.json \
  --base-url "$BEFORE" --out-dir .pr-screenshots/before

pkill -f 'turbo run dev'
git worktree remove --force /tmp/dr-before
```

**Always remove the worktree**, including when capture fails.

Two things to know:

- **A failed "before" shot is often correct.** A route or selector that doesn't
  exist at the merge-base means the UI is *new*. Read
  `.pr-screenshots/before/manifest.json`, confirm the failure is "this didn't
  exist yet", and give that shot an after-only entry in the table.
- **Shortcut:** if the PR's base is `main`, `--base-url https://dorkroom.art`
  captures "before" from production and skips the worktree install entirely —
  by far the slowest step. Only valid when `main` is deployed and current.

## Step 5 — Write the Screenshots section

Write the section with **Markdown image syntax pointing at the local files**.
`gh` rewrites those paths to CDN URLs on upload. Group by route, and put the
shot that best shows the change first:

```markdown
## Screenshots

### `/reciprocity` — desktop, dark

| Before | After |
|---|---|
| ![reciprocity before](.pr-screenshots/before/reciprocity.webp) | ![reciprocity after](.pr-screenshots/after/reciprocity.webp) |
```

New UI has no before — use a single **After** column and say the route is new.

**Markdown syntax only.** `gh` rewrites `![alt](path)` and nothing else. An HTML
`<img src="./shot.webp">` is left untouched — you get a broken image *and* the
file appended a second time at the bottom of the body. This is the one rule that
silently produces a wrong PR, so don't reach for `<img>` to set a width. A
two-column table already constrains each image to half the body width, which is
the only sizing the old flow was buying.

`gh pr edit --body-file` replaces the whole body, so build the new body from the
current one:

```bash
PR=$(gh pr view --json number -q .number)
gh pr view "$PR" --json body -q .body > /tmp/dr-body.md
cat .pr-screenshots/section.md >> /tmp/dr-body.md
```

## Step 6 — Upload and embed, in one command

Pass every screenshot as a repeated `--attach`. Each value is
`<path>#<alt text>`; without the `#` part the filename becomes the alt text.

```bash
gh pr edit "$PR" --body-file /tmp/dr-body.md \
  --attach '.pr-screenshots/before/reciprocity.webp#reciprocity before' \
  --attach '.pr-screenshots/after/reciprocity.webp#reciprocity after'
```

One command, all files, no browser and no session to keep alive.

Then verify, because two different failures both leave a body that *looks*
fine. Read it back and check two things — that no local path survived, and that
the number of CDN URLs equals the number of `--attach` flags you passed:

```bash
gh pr view "$PR" --json body -q .body > /tmp/dr-body-live.md

# 1. No local path may survive. A hit here means a reference didn't match —
#    almost always an HTML <img> or a typo'd path.
if grep -n '\.pr-screenshots/' /tmp/dr-body-live.md; then
  echo 'FAIL: a local path was not rewritten'
fi

# 2. One CDN URL per attachment, no more. A surplus means a file was appended
#    at the bottom instead of landing in its table cell.
grep -o 'user-attachments/assets' /tmp/dr-body-live.md | wc -l
```

**Count occurrences, not lines.** `grep -c` counts *matching lines*, and a
before/after table row holds two URLs on one line — it would report `1` for a
correct two-shot table. `grep -o … | wc -l` counts the URLs themselves.

Neither check alone is enough: an unmatched path leaves the local text behind
*and* appends the asset elsewhere, so check 1 catches the broken reference and
check 2 catches the stray image.

Rules that matter in practice:

- **Every attached file must be referenced in the body.** An unreferenced
  attachment is not an error — it gets appended to the bottom of the body, out
  of its table. If you see a stray image below the section, that's a path that
  didn't match.
- **Path forms are normalized**, so `./shot.webp` in the body matches
  `shot.webp` in the flag and vice versa. Subdirectories work fine.
- **Alt text in the body wins.** `--attach 'x.webp#flag alt'` referenced as
  `![body alt](x.webp)` keeps *body alt*. The `#alt` only applies to
  attachments the body doesn't reference.
- **A file can be attached only once per command** (`… are the same file;
  attached files must be unique`). If one screenshot belongs in two places,
  reference it once and link to it in the second.
- **Supported types:** png, jpg, jpeg, gif, webp, svg, mp4, mov, webm. Anything
  else is refused up front. Images cap at 10 MB; our WebP shots are kilobytes.
- Every run **re-uploads** — editing the body a second time mints new asset
  URLs. Harmless, but don't expect the old URLs back.
- The same flag works on `gh pr create`, `gh pr comment`, and the `gh issue`
  equivalents, so a follow-up screenshot can go in a comment instead.

## Step 7 — Clean up

`.pr-screenshots/` is gitignored, but confirm `git status` is clean before
committing. Nothing from this flow belongs in a commit.
