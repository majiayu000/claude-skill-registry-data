---
name: wikicommit-serve
description: Build the published wiki with Quartz v5 and preview it locally, instead of waiting for a GitHub Pages deploy. Use this when someone asks to see, preview, or check how the wiki looks when published, or wants to confirm a page renders before it goes out. It runs a real npm build, so invoke it when a preview is actually wanted rather than to answer a question about page content — wikicommit-search or wikicommit-ask do that without a build.
---

# wikicommit-serve

A thin wrapper around the Quartz v5 build/dev-server commands (`npm run build` / `npm run preview`) that `/wikicommit-init --quartz` sets up. This Skill has no dedicated script of its own — it is a thin sequence of a prerequisite check and an `npm` invocation.

## Usage

```
/wikicommit-serve [--build]
```

- Default: build the wiki and start a local preview server (wraps `npm run preview`).
- `--build`: build only, without starting a server (wraps `npm run build`) — useful for confirming the build succeeds (e.g. before running `/wikicommit-merge`) without leaving a server running.

## Processing Flow

### Step 1: Prerequisite Check

Confirm `quartz.config.yaml` exists at the repository root. `init.py` only ever creates this file when `/wikicommit-init --quartz` runs, and it always skips writing it if it already exists — so its presence reliably means Quartz publishing was actually set up for this repository, unlike `package.json`, which may instead be the repository's own pre-existing file that `/wikicommit-init --quartz` left untouched (see the second check below).

If `quartz.config.yaml` is missing, report and stop:

```
This repository hasn't set up Quartz v5 publishing yet. Run /wikicommit-init --quartz first
(or re-run /wikicommit-init and answer Y to "Set up Quartz v5?").
```

Otherwise, confirm `package.json` actually has the script this invocation needs (`preview` by default, `build` for `--build`), e.g.:

```bash
node -e "process.exit(require('./package.json').scripts?.preview ? 0 : 1)"
```

(use `.scripts?.build` in place of `.scripts?.preview` for the `--build` case). If the script is missing, this repository already had its own `package.json` before `/wikicommit-init --quartz` ran, so the WikiCommit template's `scripts`/`devDependencies` were never merged into it (`init.py`'s `package.json` copy is always skip-existing). Report and stop:

```
⚠️ quartz.config.yaml exists, but package.json has no "<preview|build>" script. This repository
already had its own package.json before running /wikicommit-init --quartz, so WikiCommit's build
scripts were never added to it (init.py never overwrites an existing package.json). Merge the
"scripts" and "devDependencies" from
<skill-tree>/wikicommit-init/scripts/templates/package.json into your package.json by hand,
then re-run /wikicommit-serve.
```

Fill `<skill-tree>` with the directory this Skill was actually loaded from, minus its own name (`.claude/skills` or `.agents/skills`); the reader runs the merge from the repository root, where a Skill-relative `../` path means nothing.

### Step 2: Run the Build/Preview

`--build` given:

```bash
npm run build
```

Run this in the foreground — it exits on its own. Report success/failure, and on success, that the built site landed under `quartz/public/`.

No `--build` (default):

```bash
npm run preview
```

`npm run preview` ends in `npx quartz build --serve`, a long-running local dev server that does not exit on its own — run it as a background process so control returns to the user rather than blocking on it indefinitely. Once the server's own startup output confirms it's listening (Quartz prints a line such as `Started a Quartz server listening on port 8080`), report the local URL to the user (e.g. `http://localhost:8080`) and that the server is running in the background, along with how to stop it (stop the background process, or Ctrl+C if the user is running it directly in their own terminal instead).

## Notes

- Do not commit or create a PR against `main` or any branch — this Skill has no Git side effects of its own
- Do not write to `.wikicommit/schema/`
- Windows: see the "Windows only" caveat in `wikicommit-init`'s next-steps guidance — `npm run install-plugins` (part of both `build` and `preview`) needs Developer Mode or Administrator privileges for the Quartz plugin symlinks to load
- A single broken Quartz community plugin (e.g. a plugin referenced in `quartz.config.yaml` has no `dist/` under `quartz/.quartz/plugins/<name>/`) does not abort `npm run build`/`preview` outright — `install-plugins`'s own `repair-plugin-builds.cjs` step retries it up to 3 times, and if it's still broken afterward, the `build`/`preview` scripts print a `WARNING: one or more Quartz community plugins failed to install/build` line and continue into `npx quartz build` anyway, which generates the site using the plugins that did install successfully. If the build output includes that warning, scroll up to `repair-plugin-builds`'s own error output — it names the still-broken plugin(s) and the exact command to run inside that plugin's directory to see the underlying error (a real failure in the plugin's own dependencies, not something WikiCommit or this Skill can fix)
