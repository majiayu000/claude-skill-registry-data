---
name: pr-screenshots
description: Capture light + dark screenshots of the UI a branch changes and attach them to the pull request with `gh pr create --attach` / `gh pr edit --attach`. Run before opening any PR that changes something a user can see (renderer components, styles, dashboards, wizard, settings). Also use to add screenshots to an existing PR.
---

# PR Screenshots

Every PR that changes visible UI ships with screenshots of the changed screens, in light and dark, taken from a deterministic mock instance and uploaded to GitHub as attachments. Reviewers see the change without checking out the branch.

The pieces:

- `capture.mjs` — runs a JSON shot list against the mock web server with Playwright's bundled Chromium, seeds agents/sessions through `/api`, writes PNGs at 2x, and prints the markdown lines + `--attach` flags to paste.
- `shots.example.json` — a shot list covering home, agent home, a session thread, and settings. Copy and trim it.
- `gh pr create --attach <file>#<alt>` (gh ≥ 2.99) — uploads each file and rewrites any `![alt](<that path>)` in the body to the hosted asset URL. Unreferenced attachments are appended to the end of the body in flag order.

## Prerequisites

- `gh --version` ≥ 2.99.0 (`brew upgrade gh`). Older gh rejects `--attach` as an unknown flag.
- This checkout's `node_modules` must be fresh. Claude worktrees do not inherit the parent's install: if Vite fails with `Cannot find module 'vite-plugin-pwa'`, run `npm ci` in the worktree. Never rebuild the user's main checkout.
- Playwright Chromium present (`npx playwright install chromium` if `capture.mjs` fails to launch a browser).

## Procedure

### 1. Decide what to shoot

List the files the branch changes against `origin/main`:

```bash
git diff --name-only "$(git merge-base origin/main HEAD)" HEAD
```

Nothing under `src/renderer/`, `agent-container/dashboard*`, or `*.css` → no screenshots. Say so in the PR body ("No UI change") and skip the rest.

Otherwise map each changed component to the screen(s) that render it and pick one shot per distinct visual state the PR introduces (not one per file). Web routes are path-based:

| Screen | Path |
| --- | --- |
| Home (agent cards / graph) | `/` |
| Notifications | `/notifications` |
| Explore | `/explore` |
| Agent home | `/agents/{{agent:<Name>}}` |
| Session thread | `/agents/{{agent:<Name>}}/sessions/{{session:<Name>:0}}` |
| Agent sub-pages | `/agents/{{agent:<Name>}}/connections`, `/secrets`, `/api-logs`, `/completed-tasks`, `/called-from-agents`, `/x-agent-permissions`, `/dashboards/<slug>` |
| Settings tab | `/settings/<tab>` (`general`, `models`, `browser`, `web`, ...; see `src/renderer/router/routes.ts`) |

States reached by interaction (a dialog, a popover, a hover) use `steps`; see the step list in the header of `capture.mjs`. Prefer `data-testid` hooks the e2e suite already uses over text matching.

### 2. Start the mock server

Dedicated port and a scratch data dir, so it never touches a real install or the `mock-web` launch config on 47899:

```bash
export SUPERAGENT_DATA_DIR="$SCRATCH/pr-shots/data" E2E_MOCK=true PORT=47897 VITE_CACHE_DIR="$SCRATCH/pr-shots/vite"
node e2e/setup-e2e-data.js && npm run dev:web
```

Run it in the background (`run_in_background`), where `$SCRATCH` is the session scratchpad. `setup-e2e-data.js` writes `setupCompleted: true` so the wizard stays closed, and `capture.mjs` PUTs the e2e placeholder API key so the "No API key configured" banner does not appear. The mock container answers every message with canned text and never calls out.

### 3. Write the shot list and capture

Copy `shots.example.json` to `$SCRATCH/pr-shots/shots.json`, keep only the shots that show the change, and run:

```bash
node .claude/skills/pr-screenshots/capture.mjs "$SCRATCH/pr-shots/shots.json"
```

Output lands in `$SCRATCH/pr-shots/shots/<name>-<light|dark>.png`. The script waits up to two minutes for the server, seeds, then prints the markdown lines and the `--attach` flags.

**Look at every image** with the Read tool before attaching it. A blank frame, the wizard, an error boundary, or the wrong screen is a failed capture, not a screenshot. Fix the shot (wrong path, missing `waitFor`, a step that needs a `wait`) and rerun; the script overwrites in place.

`fullPage: true` for long pages, `clip: "<selector>"` to crop to one component, `colorScheme: "light" | "dark"` to skip a scheme when the change is scheme-neutral. Default viewport is 1280×800 at 2x.

### 4. Before / after (optional, for restyles)

When the PR restyles something that already exists, a before column is worth the extra minute. Second worktree at the merge base, sharing this checkout's `node_modules` through a symlink, on its own port and data dir:

```bash
BASE=$(git merge-base origin/main HEAD)
git worktree add "$SCRATCH/pr-shots/base" "$BASE"
ln -s "$PWD/node_modules" "$SCRATCH/pr-shots/base/node_modules"
(cd "$SCRATCH/pr-shots/base" && SUPERAGENT_DATA_DIR="$SCRATCH/pr-shots/base-data" E2E_MOCK=true PORT=47896 VITE_CACHE_DIR="$SCRATCH/pr-shots/base-vite" node e2e/setup-e2e-data.js && npm run dev:web)
```

Run the same shot list with `"baseUrl": "http://localhost:47896"` and `"outDir": "$SCRATCH/pr-shots/before"`. Remove the worktree afterwards (`git worktree remove --force "$SCRATCH/pr-shots/base"`).

Lay before/after out as a two-column table in the body; `--attach` rewrites image paths inside tables too.

### 5. Write the body and create the PR

Add a `## Screenshots` section to the body file. Reference each image by the **same absolute path** you pass to `--attach`, with a short alt that names the screen and scheme:

```markdown
## Screenshots

| Light | Dark |
| --- | --- |
| ![Agent home (light)](/abs/path/agent-home-light.png) | ![Agent home (dark)](/abs/path/agent-home-dark.png) |
```

Then:

```bash
gh pr create --title "..." --body-file "$SCRATCH/pr-body.md" \
  --attach '/abs/path/agent-home-light.png#Agent home (light)' \
  --attach '/abs/path/agent-home-dark.png#Agent home (dark)'
```

For a PR that already exists, `gh pr edit <n> --body-file ... --attach ...` with the full body, or `gh pr comment <n> --body-file ... --attach ...` to add them as a comment. Rules gh enforces: a file can be attached once per command, images ≤ 10 MB, alt text after `#`, and push access to the repo.

Confirm with `gh pr view <n> --json body --jq .body | grep -o 'github.com/user-attachments' | wc -l` — the count should equal the number of attachments. A local path still in the body means the reference and the flag did not match.

### 6. Clean up

Stop the background server(s) and remove the base worktree if you made one. The PNGs stay in the scratchpad; nothing is written to the repo.

## Electron-only changes

Title bar, traffic-light inset, native menus, vibrancy, and anything gated on `isElectron()` do not render on the web target. For those, launch the desktop app against a scratch data dir and screenshot the window with computer-use:

```bash
SUPERAGENT_DATA_DIR="$SCRATCH/pr-shots/electron-data" SUPERAGENT_DISABLE_SINGLE_INSTANCE=1 E2E_MOCK=true npm run dev:electron
```

`SUPERAGENT_DISABLE_SINGLE_INSTANCE=1` stops the dev instance from exiting silently when the user's own Gamut is running. Web-target shots from step 3 are still the default for everything else: they are deterministic, carry no personal data, and need no window focus.

## Never

- Never screenshot the user's real install (`~/Library/Application Support/Superagent*` or `~/.superagent`). Agent names, session text, connected accounts, and emails would land in a public PR.
- Never commit the PNGs. They live in the scratchpad and on GitHub's asset host.
- Never attach an image you have not looked at.
