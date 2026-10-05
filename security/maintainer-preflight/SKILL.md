---
name: maintainer-preflight
description: Use before claiming work is done, before committing, and before opening a PR in this repo — runs the mcp-server test/typecheck/build gates and the committed-bundle rule. Trigger on "done", "ready to commit", "open a PR", or any completion claim.
---

# Maintainer preflight (claude-grok-build-plugin)

Run these before saying done. Evidence, not vibes.

**And these gates are not the last step.** Step 8 of "작업 수행 방법" in root `CLAUDE.md` —
post-execution verification plus an audit of the measurements that got you here — is mandatory
and runs AFTER the PR merges. `CLAUDE.md` owns that rule; do not restate it here. The short of
it: check `origin/main` content rather than the log, re-run the original reproduction against
the shipped bundle, and re-derive every finding by a second independent method before acting on
it. Measured 2026-09-12: in one audit the measurement harness was wrong 6 times against 2 real
defects.

**A code fix also needs a Grok second opinion before done** — the adversarial pass is step 5 of
"작업 수행 방법" in root `CLAUDE.md`; the full recipe and its history live in
`docs/11-maintainer-playbook.md` "5번 조리법" (its old rationale — "a prose-only review prompt never
terminates" — did not reproduce on 2026-09-12; use the recipe, do not cite that as a law). Give Grok
the code verbatim, not retyped facts. Read its `verdict.md` yourself, and verify any finding by
measurement before acting on it.

## Always

```bash
cd mcp-server
npm ci          # missing OR possibly-stale node_modules — see below
npm test
npm run typecheck
```

Both must pass. Report the real counts from this session's run — never summarize a run you
did not execute.

**`npm ci` is not only for a missing `node_modules`.** A tree that is merely *stale* is worse
than a missing one, because the build succeeds and silently ships the wrong dependency. Measured
2026-08-09: `node_modules` held `fast-uri` 3.1.4 while the lockfile pinned 3.1.5, and
`npm run build` produced a `dist/index.js` with the v0.2.6 security patch (GHSA-7p8r-x3mc-p8w7)
**removed** — a clean-looking rebuild that reverted a shipped fix. Cheap check before trusting a
build:

```bash
node -e "console.log(require('./node_modules/<pkg>/package.json').version)"   # vs package-lock.json
```

When in doubt, just run `npm ci` — it costs seconds and removes the whole class of error.

## If you touched anything that changes the bundle

That means **any** of these — not just source:

- `mcp-server/src/**`
- `mcp-server/package-lock.json` or `mcp-server/package.json` (dependency bumps)

```bash
cd mcp-server
npm ci                # required after a lockfile change
npm run build
git add dist/index.js dist/hook.js
```

Why the lockfile counts: `build.mjs` runs esbuild with `bundle: true`, so runtime
dependencies are **inlined** into `dist/index.js` (~805KB). A lockfile-only bump can therefore
change the committed bundle. This is not hypothetical — PR #27 and PR #49 (`fast-uri`) touched
no source file and still required a rebuild.

**On Windows, `git status` lies about `dist/` after a build.** `core.autocrlf=true` rewrites the
checkout to CRLF while esbuild writes LF, so a rebuild that changed nothing still shows
`M mcp-server/dist/index.js`. **`git diff` is the authority** — empty output means the committed
bundle already reproduces, and there is nothing to commit. This is the same CRLF noise that keeps
CI's dist check Linux-only (`.github/workflows/ci.yml`).

**But it is per-package, not universal.** Only deps that actually reach the bundle matter:

```bash
grep -c "node_modules/<pkg>" mcp-server/dist/index.js   # 0 → no rebuild needed
```

Measured 2026-08-08: `fast-uri` (via `ajv`) is inlined. `ip-address`, `hono`, `nanoid` and
`postcss` are not — they belong to MCP SDK HTTP/express transports and the vitest tree, which
this stdio server never loads. PR #48 (`ip-address`) passed CI's dist check with a
lockfile-only diff. Grep the `node_modules/` marker, not the bare name: a `nanoid` search hits
zod's `.nanoid()` validator 16 times and proves nothing.

End users execute the **committed** bundles without ever running `npm install`. A commit that
changes the dependency graph or the source without both regenerated bundles ships a plugin
whose behaviour does not match its inputs. CI catches it on Linux by comparing content — but
only after you push.

Staging `dist/` is not the same as rebuilding it. Run the build.

## Dependency PRs (Dependabot) — you own the rebuild

**A human must never run `npm run build` to land a dependency PR.** A Dependabot PR that turns
CI red on the dist check changes what users run, so landing it is a release — the next section
applies. Cherry-pick its lockfile change onto your own branch instead of pushing to the PR
branch; the commands are in `CONTRIBUTING.md` "Dependabot". The gate is the one every bundle
change takes:

```bash
cd mcp-server && npm ci && npm test && npm run typecheck && npm run build
git add dist/index.js dist/hook.js
```

The human reviews and merges; the tag and release follow at once.

## If the rebuild changed `dist/` for end users

The plugin cache is keyed by version —
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` — and each update materialises a
**new version directory**. Republishing a different bundle under an already-shipped version
leaves two artifacts sharing one version string, and `/grok:status` → `serverVersion` can no
longer identify which one is installed. So a bundle change that reaches users needs a version
bump and release notes (sites and steps: `CONTRIBUTING.md` "Release"), not a silent re-push to `main`.

## If you touched `hooks/hooks.json`

The wrapped shape is mandatory:

```json
{ "hooks": { "PreToolUse": [ … ] } }
```

A bare `{ "PreToolUse": … }` makes Claude Code report **Status: failed to load**, and every
`/grok:*` command disappears. `hooks-contract.test.ts` guards this — do not skip it.

## If you bumped the version

`.claude-plugin/plugin.json` and `mcp-server/package.json` move together. Every other site
`handoff-version.test.ts` checks is in `CONTRIBUTING.md` "Release" step 1 — the table and the
paragraph under it (the lockfile twice, `docs/03`, CHANGELOG).

⚠️ **`src/version.ts` is under `src/`, so a version bump is a bundle change.** esbuild inlines its
`return '<version>';` fallback literal — the real v0.2.18 commit moved `0.2.17` → `0.2.18` inside `dist/index.js`. Run
`npm run build` and commit both bundles (see the sections above), or CI's dist check fails.

After the squash-merge, tag and cut the GitHub release immediately. Full procedure, commands and
the reason (the version-keyed plugin cache): `CONTRIBUTING.md` "Release".

## Never

- Commit directly to `main` — the ruleset requires a PR with **both CI jobs green**, and there is
  no bypass actor (admins included). Details: `CONTRIBUTING.md` "Branch & PR"
- Auto-commit Grok's output — a human reviews the diff first
- Claim green from a run you did not execute in this session
