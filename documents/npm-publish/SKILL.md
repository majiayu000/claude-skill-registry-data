---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: npm-publish
description: >
  Release an npm package end to end: commit pending work, pick the semver bump,
  write the CHANGELOG (or consume .changeset files manually), publish with the
  lockfile's package manager (never npm publish in pnpm/bun repos, workspace:^
  leaks), tag, push, create the GitHub release, and deploy the website/ folder via its deploy script.
  Covers monorepo order and prerelease --tag. ALWAYS load when asked to publish,
  release, or bump a package version. This skill is also called changepub;
  load it when the user says changepub.
---

# Publishing npm Packages

## Step 1: Understand Current Changes

Read the diff and commit history since the last release:

```bash
git diff HEAD
git log packagename@0.4.55..HEAD --oneline
```

Replace `packagename@0.4.55` with the actual last published tag.

## Step 2: Determine What Needs Publishing

Check the last published version:

```bash
npm show packagename version
```

**Compare the npm version against `package.json`.** If `package.json` is already ahead (e.g. npm has 0.0.89 but package.json says 0.0.101), those intermediate versions were never published. The changelog and GitHub release MUST cover everything since the last **published** npm version, not just the latest changelog section.

Use the npm version (not the package.json version) as the baseline for:
- `git log` to find all commits that need covering
- changelog content to include in GitHub release notes
- determining what features are "new" to users

For monorepos, check each workspace package to identify which ones have unpublished changes.

## Step 3: Bump Version and Update Changelog

1. Bump the version in `package.json` (never do major bumps)
2. Update or create `CHANGELOG.md` with a **numbered list** under the new version heading, using only the final user-facing changes since the last published version. If none remain, do not add an empty version heading.

### Semver bump rules

- **minor** when users get a **new feature, new command, new flag, new option, or new capability**
- **patch** only when the release is **only fixes, small behavior adjustments, or performance improvements**
- Never default to patch when there are new user-facing features

Examples:

- new `build --watch` command → **minor**
- new `--format json` option → **minor**
- support for a new config field or API callback → **minor**
- fix crash on invalid config with no new capability → **patch**
- faster startup with no new behavior → **patch**

### Changelog format

Use numbered lists, not bullets. Each item describes a **user-facing outcome**.

**Always sort by relevancy:**

1. **Big new features** — user-facing capabilities that change what users can do
2. **New CLI commands/options** — always with usage examples
3. **Behavior changes** — things users will notice
4. **Bug fixes** — issues users hit
5. **Performance improvements** — only if users feel the difference

````md
## 0.5.0

1. **New streaming upload mode** — upload large files without loading them into memory:
   ```bash
   mycli upload --stream ./huge-file.zip
   ```
````

Supports files up to 100GB. Progress is shown in real-time.

2. **Added `--dry-run` flag** — preview publish without uploading:

   ```bash
   mycli publish --dry-run
   ```

3. **Fixed timeout on large uploads** — uploads over 50MB no longer hang
4. **Changed default retry count from 3 to 5** — improves reliability on flaky networks

````

### Research commits for context

Before writing changelog entries for new features, read the documentation and markdown files that were updated in the commits:

```bash
# Find docs updated alongside the feature
git show <commit> --stat | grep -E '\.(md|mdx)$'

# Read the actual doc changes
git show <commit> -- docs/
````

This gives you the full context: examples, diagrams, and explanations the author wrote. Use this to write rich changelog entries that help users understand the feature.

If a feature ships in this release, the version bump should usually be **minor**, not patch.

### CLI commands and options

**Always include usage examples for new CLI flags, commands, or options:**

````md
3. **New `--format` option** — output results in different formats:

   ```bash
   # JSON for scripting
   mycli list --format json | jq '.items[]'

   # Table for humans
   mycli list --format table
   ```
````

````

Show real-world use cases, not just the flag name. If a flag interacts with others, show the combination.

### Big features deserve depth

For significant new capabilities, go beyond one-liners:

- Explain **what users can now do** that they couldn't before
- Include **code examples** showing typical usage
- Add **ASCII diagrams** if they clarify architecture or flow
- Mention **limitations or caveats** users should know
- Link to docs if available

```md
1. **New plugin system** — extend functionality with custom plugins:

   Plugins can hook into the upload lifecycle:
   ```ts
   export default {
     beforeUpload(file) {
       console.log(`Uploading ${file.name}`)
     },
     afterUpload(result) {
       notify(`Done: ${result.url}`)
     }
   }
````

Load plugins via config or CLI:

```bash
mycli upload --plugin ./my-plugin.ts
```

See [Plugin Guide](./docs/plugins.md) for the full API.

````

### Code snippets

Include code snippets when they help users understand the change:

```md
3. **New `onProgress` callback** — track upload progress:
   ```ts
   await upload(file, {
     onProgress: (pct) => console.log(`${pct}% done`)
   })
````

````

### What NOT to include

Exclude anything users don't directly experience:

- "added tests for X" — internal quality, not user-facing
- "improved test flakiness" — CI stability, users don't see this
- "refactored internals" — no behavior change
- "updated CI config" — internal tooling
- "bumped dev dependencies" — doesn't affect published package

**Transform internal work into user-facing impact when relevant:**

- bad: "fixed race condition in retry logic"
- good: "fixed intermittent upload failures under high concurrency"

### Group related changesets into single items

Read all pending changesets before writing the changelog. Compare them with the code and the last published version. Multiple changesets that describe the same user-facing outcome should become **one** changelog item, even if they were written in different commits. Describe the final behavior, not the sequence of implementation steps. A changeset is a source of context, not a guarantee of its own item.

If a change was added and then undone before publication, omit it entirely. Likewise, omit fixes to a feature that users never received in a broken state. If no user-facing change remains from a group of changesets, produce **no** changelog item for that group. Keep unrelated outcomes as separate items.

Examples of what to merge:
- 3 changesets about Prism grammar loading, highlighting extras, and nested fence support → one item about improved code highlighting
- a changeset that adds a feature + another that fixes a bug in that same feature → one item describing the feature (skip the bug fix)
- a changeset for a UI fix + another for the same UI area → one item

Examples of what stays separate:
- a sidebar change and an OpenAPI change → two items (different areas)
- a new CSS variable and a chat animation fix → two items

### Omit bug fixes for unreleased features

If a feature was added in this release cycle and a later changeset fixes a bug in that feature, the fix is invisible to users. Just describe the feature working correctly. Never list "fixed X" when X was never released broken. If the feature itself was removed before publication, omit both entries.

### Merging unreleased versions

If multiple versions accumulated since last publish, merge them into one changelog entry. Only describe the final state:
- If a feature was added then removed, don't mention it
- If a feature was added then bug-fixed, just mention the added feature

### Verify examples against source code

Before committing the changelog, **read the actual source code, README, and docs** to verify every example is accurate. Never guess or hallucinate identifiers like model IDs, flag names, command names, enum values, or API endpoints.

Specifically:

1. **Read the README** — check that CLI examples, flag names, and option values match what the README documents
2. **Read relevant source files** — for CLIs, read the command definitions to verify flag names and accepted values. For libraries, read the public API surface to verify function signatures, parameter names, and types
3. **Run help commands** — if the tool has a `--help` flag or a `models`/`list` command, run it to get the real identifiers instead of inventing them
4. **Cross-check every code snippet** — every model ID, flag name, enum value, URL, and command in the changelog must exist in the source. If you're not sure, grep for it

```bash
# Example: verify CLI flags exist
node bin.js --help
node bin.js <subcommand> --help

# Example: verify model/enum IDs
grep -r 'some-model-id' src/

# Example: check README examples match
cat README.md | grep -A5 'some-feature'
```

This prevents publishing changelogs and release notes with wrong identifiers that confuse users.

## Step 4: Commit the Release

If any changeset `.md` files reference GitHub issues with `Fixes #123`, `Closes #456`, or similar keywords, include those references in the commit message body. GitHub closes issues automatically when the commit containing these keywords lands on the default branch.

```bash
git add .
git commit -m 'release: packagename@x.y.z

Fixes #123
Closes #456'
```

Collect issue references from changesets for changes that actually ship and append them as separate lines in the commit body. Do not close an issue for a change that was undone before publication. This ensures issues get closed at publish time without needing a separate PR or GitHub Action.

## Step 5: Publish to npm

**NEVER use `npm publish` if the project uses pnpm or bun.** `npm` does not understand `workspace:^` references and will publish them as literal strings, breaking the package for every consumer. This is not a theoretical risk; it has caused broken releases.

Detect the package manager from the lockfile and use ONLY that tool:

- `pnpm-lock.yaml` → `pnpm publish` (NEVER `npm publish`)
- `bun.lock` or `bun.lockb` → `bun publish` (NEVER `npm publish`)
- `package-lock.json` → `npm publish` (only valid option)

Run publish from **inside the package directory** (use `workdir` in bash tool, NOT `--dir` or `--filter`). `pnpm publish` does not support `--dir`. Do NOT run from the monorepo root.

```bash
# pnpm — cd into the package folder first, then publish
# CORRECT:
cd vite && pnpm publish --access public --no-git-checks

# WRONG — these do NOT work:
# pnpm --dir vite publish        ← npm parses flags wrong
# pnpm publish --dir vite        ← --dir is not a publish flag
# pnpm --filter @pkg/name publish ← does not resolve workspace refs

# bun project — also from inside the package folder
bun publish --access public
```

After publishing, immediately verify no `workspace:` references leaked:

```bash
npm view packagename@x.y.z dependencies --json | grep workspace
# must return empty — if it returns anything, the publish is broken
```

If a broken version was published, bump patch, republish correctly, and deprecate the broken version:

```bash
npm deprecate 'packagename@x.y.z' 'Broken: unresolved workspace references. Use x.y.z+1 instead.'
```

**After publishing**, regenerate the lockfile:

```bash
pnpm i  # or bun i
```

This updates the lockfile with the new version so workspace references resolve correctly.

### Monorepo Publishing Order

Publish packages in topological order (dependencies first). Always publish dependencies if they have changes.

## Step 6: Tag and Push

```bash
git tag packagename@x.y.z
git push origin HEAD --tags
```

## Step 7: Create GitHub Release

**Never create draft releases** — always publish releases immediately so users see them.

**NEVER pass `--prerelease` to `gh release create`**, even for prerelease npm versions (like `1.0.0-rsc.2`). Prerelease releases are hidden from the main GitHub page of the repo and users can't find them. Always use `--latest` instead.

**Do NOT use `--notes-file CHANGELOG.md`** — that dumps the entire changelog into the release body.

### Merging unpublished versions into release notes

If `package.json` was bumped multiple times without publishing (e.g. npm has 0.0.89, package.json has 0.0.101, you're publishing 0.0.102), the GitHub release notes must merge ALL changelog entries from 0.0.90 through 0.0.102 into a single release. Users jumping from 0.0.89 to 0.0.102 need to see everything that changed.

Sort merged entries by impact — big new features first, bug fixes last. Remove duplicates where a feature was added then refined across versions (only describe the final state).

Extract only the current version's section and pass via `--notes`:

```bash
gh release create packagename@x.y.z --title "packagename@x.y.z" --notes "$(cat <<'EOF'
1. **Added `--dry-run` flag** — preview publish without uploading
2. **Fixed timeout on large uploads** — uploads over 50MB no longer hang
3. **Changed default retry count from 3 to 5** — improves reliability on flaky networks

Thanks @contributor for #42!
EOF
)" --latest
```

### Group and omit in release notes too

Apply the same grouping and omission rules from the changelog section. Related changes become one item. Bug fixes for features added in this release are omitted. The release notes and the changelog should have the same items; do not expand changesets 1:1 into release note entries.

### Release notes decision flow

```
┌─────────────────────────────────────┐
│  For each commit/PR since last tag  │
└──────────────┬──────────────────────┘
               │
               v
       ┌───────────────┐
       │ User notices  │──no──> exclude
       │ this change?  │
       └───────┬───────┘
               │ yes
               v
       ┌───────────────┐
       │ Behavior or   │──behavior──> describe what changed
       │ new feature?  │
       └───────┬───────┘
               │ feature
               v
         describe what users
         can now do + example
```

### What belongs in release notes

- **New flags/options** — "Added `--format json` for machine-readable output"
- **Bug fixes users hit** — "Fixed crash when config file missing"
- **Behavior changes** — "Default timeout increased from 30s to 60s"
- **Breaking changes** — "Renamed `--old` to `--new` — update your scripts"
- **Performance users feel** — "Startup time reduced from 2s to 200ms"

### What does NOT belong

- "Added unit tests" / "Improved test coverage"
- "Refactored X module" (no behavior change)
- "Fixed CI flakiness" / "Updated GitHub Actions"
- "Bumped internal dependencies"

Include external contributors: "Thanks @username for #42!"

**Submodule packages:** Run `gh release` from inside the submodule directory.

## Step 8: Deploy the website if present

After the npm publish and GitHub release, deploy the website so docs match the new package version.

Do this when a `website/` folder exists in the repo and has a `package.json`. Also check `docs/` only if it is clearly a website package (has its own `package.json`), not a random markdown folder. Any framework counts (Holocron, Vite, Next, Spiceflow, etc).

**Only run a script from that folder's `package.json`.** Never run raw `wrangler deploy`, `vite build`, `npx holocron deploy`, or any other deploy command you invent.

Pick **one** production script, in this order if several exist:

1. `deployment:production`
2. `deploy:production`
3. `deployment`
4. `deploy`

Skip preview-only scripts (`deployment:preview`, `deploy:preview`, `preview`).

Run it with the repo package manager **from inside the website folder**:

```bash
# example when website/package.json has "deployment:production"
cd website && pnpm deployment:production
```

Skip this step if there is no website folder or no `deploy` / `deployment` script.

## Step 9: Handle Publish Failures

If publish fails due to TypeScript errors or other issues, fix them and retry.

## Output

After publishing, report what you did and include:
- the GitHub release link
- links to any GitHub issues that were closed by the release (full URLs like `https://github.com/owner/repo/issues/123`)
- the website deploy result, if Step 8 ran (script name and live URL)

The GitHub release notes should also mention closed issues at the bottom, linking to each one. For example:

```
Fixes https://github.com/owner/repo/issues/123
Fixes https://github.com/owner/repo/issues/456
```

also make sure that we always use `workspace:^` instead of `workspace:*` for workspace dependencies in package.json. using :\* will use the pinned package in released npm package.json files, instead of ^.

## .changeset based changelogs

some packages use the changeset convention for changelogs. so instead of updating the changelog directly they create .md files inside `.changeset` folder. with shape

```md
---
"packagename": minor
---

Changelog item entry here. with examples
```

For packages that contain these `.md` files we should

- read the .md files inside `.changeset` if any (also check in parent folders if this is a workspace. sometimes `.changeset` is at the repo root)
- check for `<!-- depends-on: <package> ... -->` comments. Publish each named package before the package whose changeset has the comment. Never copy HTML comments into `CHANGELOG.md` or release notes
- compare the entries with the final user-facing behavior since the last published version; merge related entries into one numbered changelog item per outcome, and omit entries for changes that were undone or never visible to users. If nothing remains, add no item for those entries
- keep useful examples and details from related entries in the merged item, but verify that every example still matches the shipped code
- if the final release adds a **new feature or capability**, use a **minor** bump
- use **patch** only when the changes that still ship are fixes or non-feature improvements
- then delete these .md files
- publish as normal

NEVER use the changesets cli to publish or update changeset based packages. always do these steps manually.

## prereleases

if a `package.json` version has a version like `1.18.0-rsc.0` you MUST add the option --tag rsc. rsc is for the tag used in the version.

example: `pnpm publish --tag next` for `1.0.0-next.0`. the `.0` does not matter in what `--tag` name you would use.

## working directory

do not change cwd if there are git diff that don't let you publish, instead just commit them with the appropriate message. do this before starting the publish.

## additional context
