---
name: release
description: "Create a GitHub release with auto-generated changelog. Use this skill whenever the user wants to create a release, tag a release, publish a release, cut a release, or ship a version. Triggers on phrases like \"release 1.2.3\", \"create a release\", \"tag a new version\", \"ship it\", \"cut a release\", or any mention of creating GitHub releases."
argument-hint: "[[version]=auto|1.2.3|major|minor|patch, [branch]=main, [pre-release]=false]"
---

# GitHub Release

Create a GitHub release using the `gh` CLI with auto-generated changelog from all changes since the last release.

## Arguments

The user provides these in natural language — extract them from the prompt:

- **version** (optional): An explicit semver tag without `v` prefix (e.g. `1.2.3`, `2.0.0-beta.1`), a semver bump keyword (`major`, `minor`, `patch`), or omitted entirely to auto-detect the bump type from the changelog.
- **branch** (optional): Branch to create the tag/release on. Defaults to `main`.
- **pre-release** (optional): Explicitly mark as pre-release. Auto-detected if the version contains `alpha`, `beta`, or `rc` (e.g. `1.0.0-rc.1`).

## Commit subjects

Commits use scoped conventional subjects, `type(scope): subject`:

- **type**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style` or `perf`; `ci`, `build` and `revert` are accepted too.
- **scope** (optional): the area touched, e.g. `fix(auth): handle expired sessions`. Omit it for repo-wide changes.
- **`!`** right before the colon marks a breaking change: `feat(api)!: remove v1 routes`. So does a `BREAKING CHANGE:` or `BREAKING-CHANGE:` footer at the start of a body line.
- Legacy subjects in the old `(type): subject` form, e.g. `(feat): add planner agent`, classify the same way: the word in parentheses is the type, and there is no scope.
- Any other subject (e.g. `Update README`) has no type.

## Workflow

### 1. Resolve the version

**If no version was provided** (auto-detect from changelog):

1. Fetch the latest release tag:
   ```bash
   gh release list --limit 1 --json tagName --jq '.[0].tagName'
   ```
2. Strip any `v` prefix from the tag to get the current version. If no previous release exists, use `0.0.0` as the base.
3. List the commits since the last release. The second command, the footer command, lists the commits whose body carries a `BREAKING CHANGE:` or `BREAKING-CHANGE:` footer, which the subjects alone do not show:
   ```bash
   git log <latest-tag>..HEAD --no-merges --format='%h %s'
   ```
   ```bash
   git log <latest-tag>..HEAD --no-merges -E --grep='^BREAKING[ -]CHANGE:' --format='%h %s'
   ```
   If there is no previous release, drop `<latest-tag>..HEAD` from both commands.
4. Parse each subject as described in Commit subjects above and pick the bump:
   - **major** — any subject has `!` right before the colon (`feat!:`, `fix(api)!:`), or the footer command printed any commit
   - **minor** — any commit has type `feat`
   - **patch** — everything else, including subjects without a type

   The highest-priority classification wins: major > minor > patch. If a subject without a type looks like a new feature or a breaking change, point it out in the summary so the user can choose a higher bump.
5. **Present a confirmation summary to the user and wait for approval before proceeding.** The summary must include:
   - **Previous version**: the current latest release tag
   - **Changes**: a categorised list of commits since that tag (grouped as in the changelog: breaking, features, fixes, other)
   - **Detected bump**: the bump type and the commit that decided it (e.g. "major — `feat(api)!: remove v1 routes`")
   - **Proposed version**: the computed next version

   Do NOT proceed to create the release until the user explicitly confirms.

**If the user provided a bump keyword** (`major`, `minor`, or `patch`):

1. Fetch the latest release tag:
   ```bash
   gh release list --limit 1 --json tagName --jq '.[0].tagName'
   ```
2. Strip any `v` prefix from the tag to get the current version. If no previous release exists, use `0.0.0` as the base.
3. Bump the appropriate component:
   - `major`: increment MAJOR, reset MINOR and PATCH to 0 (e.g. `1.2.3` → `2.0.0`)
   - `minor`: increment MINOR, reset PATCH to 0 (e.g. `1.2.3` → `1.3.0`)
   - `patch`: increment PATCH (e.g. `1.2.3` → `1.2.4`)
4. Show the user the resolved version and confirm before proceeding.

**If the user provided an explicit version string:**

Confirm the version string is valid semver. It should match the pattern `MAJOR.MINOR.PATCH` with an optional pre-release suffix like `-alpha.1`, `-beta.2`, or `-rc.1`. Reject anything with a `v` prefix — strip it and inform the user if they include one.

### 2. Determine pre-release status

A release is pre-release if:
- The version contains `-alpha`, `-beta`, or `-rc` (e.g. `1.0.0-beta.1`)
- The user explicitly says it's a pre-release

### 3. Build the changelog

Reuse the two commit lists from auto-detection. If the version was given explicitly or as a bump keyword, fetch the latest release tag and run both `git log` commands from step 1 now.

Group the commits into these sections, in this order. Each commit goes in the first section it matches:

- **Breaking Changes** — `!` before the colon, or listed by the footer command
- **New Features** — type `feat`
- **Bug Fixes** — type `fix`
- **Other Changes** — every other type (`refactor`, `perf`, `chore`, `docs`, `test`, `style`, `build`, `ci`, `revert`) and subjects without a type

Write each commit as one bullet:

- Strip the `type(scope)!: ` prefix (the scope and `!` are optional), or the legacy `(type): ` prefix.
- If the subject has a scope, start the bullet with `**scope:** `.
- Capitalise the first letter of the description and keep it concise.
- For a commit listed by the footer command, append the footer's explanation (`git show -s --format='%b' <hash>` prints the body).

For example, `feat(api)!: remove v1 routes` becomes `**api:** Remove v1 routes` under Breaking Changes, and the legacy `(fix): handle empty input` becomes `Handle empty input` under Bug Fixes.

Omit empty sections. If a section has no commits, don't include it.

Format the body as:

```markdown
## Breaking Changes

- **api:** Remove v1 routes

## New Features

- **agents:** Add planner agent for task decomposition
- **agents:** Add verifier agent for plan validation

## Bug Fixes

- **swoole-expert:** Restore API surfaces stripped during compression
- **consolidation:** Remove arbitrary subtask limit

## Other Changes

- **android-expert:** Remove training-redundant content
- Rename elite-fullstack-architect -> architect, code-griller -> reviewer
- Update commands to use consolidation pattern for parallel work
```

### 4. Create the release

```bash
gh release create <version> --title '<version>' --target <branch> [--prerelease] --notes-file - <<'EOF'
[changelog body from step 3]
EOF
```

Use `--notes-file -` with the hand-crafted changelog, NOT `--generate-notes`.

### 5. Confirm

After creation, display the release URL:

```bash
gh release view <version> --json url,tagName,isPrerelease,createdAt
```

## Examples

**Explicit version:**
Prompt: `release 1.2.3`
1. Build changelog from commits since last tag
2. Create the release:

```bash
gh release create 1.2.3 --title '1.2.3' --target main --notes-file - <<'EOF'
[changelog body from step 3]
EOF
```

**Auto-detect:**
Prompt: `create a release`
1. Fetch last tag (`1.2.3`); the commits since are `feat(auth): add passkey login` and `fix(api): accept empty filters`, and the footer command prints nothing
2. Detect bump: minor — `feat(auth): add passkey login`
3. Show confirmation with changelog preview and proposed version (`1.3.0`)
4. After user confirms:

```bash
gh release create 1.3.0 --title '1.3.0' --target main --notes-file - <<'EOF'
[changelog body from step 3]
EOF
```

**Breaking change:**
Prompt: `ship it`
1. Fetch last tag (`1.3.0`); `feat(api)!: remove v1 routes` has `!` before the colon (a `BREAKING CHANGE:` footer on any commit counts the same)
2. Detect bump: major; the changelog opens with Breaking Changes: `- **api:** Remove v1 routes`
3. Show confirmation with changelog preview and proposed version (`2.0.0`)
4. After user confirms:

```bash
gh release create 2.0.0 --title '2.0.0' --target main --notes-file - <<'EOF'
[changelog body from step 3]
EOF
```

**Pre-release:**
Prompt: `cut a release 2.0.0-beta.1 on develop`
1. Create the pre-release:

```bash
gh release create 2.0.0-beta.1 --title '2.0.0-beta.1' --target develop --prerelease --notes-file - <<'EOF'
[changelog body from step 3]
EOF
```
