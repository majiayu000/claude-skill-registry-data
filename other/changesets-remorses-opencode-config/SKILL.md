---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: changesets
description: >
  Changeset-based versioning workflow. Manually add .changeset/*.md files to
  describe changes instead of editing CHANGELOG.md directly. Changesets are
  consumed at publish time to bump versions and generate changelogs. ALWAYS
  load this skill when a repo has a .changeset/ folder. Before writing a
  changeset, read pending ones and update or remove overlapping entries so
  the next changelog describes the final user-facing behavior.
---

# Changesets

Changesets is a workflow for versioning and publishing packages. Instead of manually editing `CHANGELOG.md` or bumping `version` in `package.json`, you drop a small markdown file inside `.changeset/` describing what changed. At publish time, these files are consumed to bump versions, generate changelog entries, and publish to npm.

## Always manual

Never run the `changeset` CLI command interactively. Never run `npx changeset`, `pnpm changeset`, or any variant. The changeset file is always created manually by writing a `.md` file directly into the `.changeset/` folder. The CLI's interactive wizard is designed for humans typing in a terminal; agents must write the file themselves.

## Reconcile pending changesets first

Before writing a changeset, list and read the pending `.changeset/*.md` files in the repo root. Exclude the folder readme and config files. Compare their descriptions and package bumps with the final user-facing behavior of the current change, including changes made in earlier commits since the last release.

- If a pending changeset describes the same logical user-facing change, update that file instead of adding another. Merge related fixes, examples, package entries, and issue references into one accurate description; set the bump for each package to the level the final behavior needs.
- If multiple pending files describe the same change, consolidate them into one and remove the redundant files. Keep unrelated changes in separate files.
- If a pending entry describes behavior that has been removed before release, remove that entry. Delete its file only if no other change remains in it; otherwise edit the file to describe what still ships. For example, if a feature was added and then removed before release, delete the feature changeset rather than adding a second changeset that says it was removed.
- If the current change cancels an earlier unreleased change and leaves no user-facing difference from the last release, do not add a changeset for that canceled change. Keep changesets that describe other differences that still ship.

Only pending changesets can be reconciled this way. Do not rewrite a published `CHANGELOG.md` entry or a changeset already consumed by a release.

## Adding a changeset

After reconciling pending changesets, create a new `.md` file only for a distinct user-facing change that remains. Use a short descriptive kebab-case filename (e.g. `fix-boolean-query-coercion.md`). The filename should make the change recognizable in `git status` without opening the file. The file has YAML frontmatter declaring which package(s) changed and the semver bump level, followed by a markdown description.

Before writing the file, list the last 20 GitHub issues to see whether the change closes any of them:

```bash
gh issue list --state all --limit 20
```

If a matching issue exists, mention it in the changeset description with `Fixes #123` or `Closes #123` on its own line.

```md
---
'spiceflow': patch
---

Fix query parameter coercion for boolean arrays in GET handlers.
```

Multiple packages can be listed in one changeset:

```md
---
'spiceflow': minor
'create-spiceflow': patch
---

Add federation support for remote RSC components. The create-spiceflow
template now includes a federation example.
```

## Rules

1. **Never use `major`.** Use `patch` for fixes and `minor` for new features. Releases are frequent enough that breaking changes don't warrant a major bump.
2. **Include private websites and apps.** `"private": true` is not a reason to skip a changeset. User-facing private packages (websites, dashboard apps, hosted workers) still get a `CHANGELOG.md`. Add them in the frontmatter next to any public package that changed. Configure `.changeset/config.json` with `"privatePackages": { "version": true, "tag": false }` so `changeset version` writes their changelog without publishing them to npm. Skip only internal packages with no user-facing surface, or packages with no `version` field.
3. **Don't edit CHANGELOG.md.** New changes must be added as changesets instead. That includes private-package changelogs.
4. **Never run the changeset CLI.** Always write the `.md` file manually.
5. **Present tense.** Write "add support for X", "fix bug with Y", not "added" or "fixed".
6. **One pending changeset per logical change.** Reuse and update it across commits until release. If a PR has two unrelated changes, keep two changeset files.
7. **Use descriptive filenames.** Prefer `fix-auth-token-refresh.md` over random names like `cool-lions-dance.md`. Keep filenames concise, kebab-case, and focused on the logical change.
8. **Check recent GitHub issues before writing.** List the last 20 issues with `gh issue list --state all --limit 20` before deciding there is no issue to reference. Do not rely only on commit messages.
9. **Reference fixed issues.** When a change fixes a GitHub issue, include `Fixes #123` (or `Closes #123`) on its own line in the changeset description. At publish time, the [`changepub`](https://github.com/remorses/opencode-config/blob/main/commands/changepub.md) command collects these references and includes them in the release commit message body. GitHub closes the issues automatically when that commit lands on the default branch. This also creates a clickable link in the CHANGELOG for users to find context.

## What goes in the description

Changeset descriptions become the public changelog. Write them as **rich content** aimed at end users. These are not commit messages; they should be detailed and helpful.

Include any combination of:

- **Code examples** showing new APIs or changed behavior
- **Migration steps** if the user needs to update their code
- **Diagrams** (ASCII) explaining architecture or data flow changes
- **Before/after comparisons** showing old vs new usage
- **Links** to relevant docs or issues

Focus on what the user sees, not internal refactoring. Explain why the change matters and how to use it.

**Good example:**

```md
---
'spiceflow': minor
---

Add `parseFormData()` utility for type-safe form handling with Standard Schema validation.

\`\`\`ts
import { parseFormData } from 'spiceflow'
import { z } from 'zod'

const schema = z.object({
  name: z.string(),
  age: z.coerce.number(),
})

app.post('/users', async (ctx) => {
  const data = await parseFormData(ctx.request, schema)
  // data is fully typed: { name: string, age: number }
})
\`\`\`

Handles string-to-number and string-to-boolean coercion automatically.
Array fields use `getAll()` under the hood.
```

**Example with issue reference:**

```md
---
'spiceflow': patch
---

Fix race condition in WebSocket reconnection that caused duplicate event handlers.

The `reconnect()` method now drains pending listeners before re-attaching,
preventing the exponential handler growth reported in the issue.

Fixes #287
```

**Bad examples:** "update internals", "refactor code", "misc improvements", or any single vague sentence without context.

## Pre-release mode

Some repos run in pre-release mode (configured in `.changeset/pre.json`). When active, versions are bumped with a pre-release tag like `1.20.0-rsc.3` instead of stable semver. The workflow stays the same: add changeset files normally, and the pre-release tag is applied automatically at publish time.

## Publishing (consuming changesets)

Publishing is a separate step from adding changesets, done by the user manually. The flow:

1. **During development:** reconcile pending `.changeset/*.md` files with the final behavior, then add a file only for a distinct user-facing change
2. **At publish time:** the user runs a publish command which reads all pending changeset files, bumps `package.json` versions, writes `CHANGELOG.md` entries, and deletes the consumed changeset files
3. **Then:** packages are published to npm

Never attempt to publish or version-bump yourself. Maintaining pending changesets and publishing are decoupled on purpose. Your job is only step 1: keeping pending changesets accurate.

## Finding the .changeset folder

The `.changeset/` folder lives at the monorepo root (next to the root `package.json`). If your current working directory is inside a package subfolder, look in parent directories.

## README for .changeset folders

Repos should have a short `.changeset/readme.md` explaining what the folder contains and what belongs there. Add it when the folder is created or when the repo lacks one. Keep the filename lowercase to satisfy kebab-case filename rules.

Example `.changeset/readme.md`:

```md
# Changesets

This folder contains **pending release notes**. Each `.md` file describes one user-facing fix or feature that should appear in the next generated changelog, including private websites and apps.

## What to put here

- Add one descriptive kebab-case `.md` file per logical change, for example `fix-auth-token-refresh.md`.
- Read pending entries first. Update an existing entry for the same change, and remove entries for behavior that no longer ships.
- Use `patch` for fixes and `minor` for new features.
- Include private user-facing packages in the frontmatter so they keep a CHANGELOG.
- Write in present tense, focused on what users see.
- Check GitHub issues first. If the change fixes one, include `Fixes #123` on its own line.

## What not to put here

- Do not skip a website or app just because it is `"private": true`.
- Do not add changesets for packages without a `version` field.
- Do not edit `CHANGELOG.md` directly.
- Do not run the interactive changeset CLI.
- Do not add vague entries like "misc improvements" or "update internals".
```
