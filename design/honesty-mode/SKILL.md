---
name: honesty-mode
description: Toggle the badges-page Honesty Mode build-time flag on or off. ON makes the README badge generator emit direct /badges/_assets/<handle>/<file>.svg URLs (no Cloudflare Worker, no ?repo= validation). OFF restores worker-validated URLs. Use when the user says "/honesty-mode on", "/honesty-mode off", "turn honesty mode on/off", or asks for the current honesty-mode state.
version: 1.0.0
---

# honesty-mode

Flip the `HONESTY_MODE` build-time constant in `docs/badges/index.html` and document the flip. There is no runtime UI for this flag — the on-page pill is read-only — so changing it always means editing the source.

## What the flag controls

In `docs/badges/index.html` (script block near the top):

```js
const HONESTY_MODE = true;   // or false
```

| Value | Copied-markdown URL | Where it works |
|---|---|---|
| `true` (default backup) | `https://gaiaskilltree.com/badges/_assets/<handle>/<file>.svg` | Anywhere — bypasses worker, no `?repo=` |
| `false` | `https://gaiaskilltree.com/badges/<handle>/<file>.svg?repo=<repo>` | Only when the Cloudflare Worker is deployed and `run_worker_first = true` |

When the user says `/honesty-mode on`, set the constant to `true`. When they say `/honesty-mode off`, set it to `false`. When they ask for status without an argument, just report the current value — don't edit.

## Workflow

1. **Parse the argument.** Accept `on`, `off`, `true`, `false`, `enable`, `disable` (case-insensitive). If the argument is missing or just `status`, report the current value of `HONESTY_MODE` from `docs/badges/index.html` and stop.

2. **Read the current value.** Grep for `const HONESTY_MODE = ` in `docs/badges/index.html`. If the line is missing, surface that and stop — the flag may have been ripped out per the removal plan in `docs/badges/CLAUDE.md`.

3. **No-op check.** If the requested state already matches, say so and stop. Don't open a PR for a no-op edit.

4. **Edit the constant.** Use `Edit` to change `const HONESTY_MODE = true;` ↔ `const HONESTY_MODE = false;`. Touch nothing else in the file — the indicator paint, `badgeMarkdownUrl()`, and detection logic all read from this single constant.

5. **Verify the chip painting still matches.** Sanity-check that the indicator-paint lines (`honestyPill.dataset.state = HONESTY_MODE ? "on" : "off"` and the `.bd-honesty-state` text) are still present and read from the constant. If they've drifted, fix them in the same edit.

6. **Don't run `gaia dev docs`.** This flag only affects `docs/badges/index.html` — none of the generated artifacts (`registry/gaia.json`, `docs/graph/`, `tree.md`) depend on it. A rebuild is unnecessary noise.

## Branch + PR convention

Per `CLAUDE.md` § Branch Naming, this is a `design/` change (website behavior, `docs/` HTML/CSS/JS).

1. **Branch.** `git checkout -b design/honesty-mode-{on,off}` from the current branch (or `main` if the user asks for a clean branch). Don't push to `main`.

2. **Commit.** Single commit, message:
   ```
   design(badges): set HONESTY_MODE = {true|false} [skip-gen]
   ```
   Include `[skip-gen]` so the `Regenerate and Commit Artifacts` workflow doesn't loop on this — there's nothing to regenerate.

3. **Push and open PR.** `git push -u origin <branch>` then `gh pr create` with a body that:
   - States the new value (`HONESTY_MODE = true` / `false`).
   - Explains the practical effect (which URL shape lands in the user's clipboard).
   - Links to `docs/badges/CLAUDE.md` for the full rationale.
   - Does NOT mark the PR as ready-to-merge if turning OFF — call out the worker-deployed prerequisite from `docs/badges/CLAUDE.md` § "When to flip Honesty Mode OFF".

4. **Report PR URL** back to the user. Don't merge.

## Anti-patterns

- **Don't add a runtime toggle back.** The whole point of this flag being build-time is that "the URL you see copied is the URL everyone else gets." See `docs/badges/CLAUDE.md` § "Why no runtime/localStorage toggle?".
- **Don't touch `_assets/` detection or local previews.** Those always read from `_assets/` regardless of mode — that's how the page renders before the worker runs. Honesty Mode only swaps the *copied markdown URL*.
- **Don't bump versions.** This change touches one HTML file's script constant; the three-file version lockstep (pyproject / cli-npm / gaia.json) doesn't apply.
- **Don't edit `worker/index.js`.** The worker stays as-is — Honesty Mode just routes around it for embedded badges.
