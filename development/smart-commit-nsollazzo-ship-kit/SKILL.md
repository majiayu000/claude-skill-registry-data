---
name: smart-commit
description: |
  Automatically cluster and commit git changes into logical groups with conventional commit
  messages. Use when: committing multiple unrelated changes, cleaning up work before PR,
  organizing messy commits, or when asked to "commit my changes", "smart commit", "organize
  commits", or "cluster commits". Pass `--no-coauthor` to omit any Co-Authored-By trailer.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "[--no-coauthor]"
---

# Smart Commit

Cluster uncommitted changes into logical groups and commit each with a clear conventional commit message.

> **Sub-agents.** Committing is **sequential by design** — every commit shares one git index,
> so parallel sub-agents staging into it would corrupt each other. Do the clustering and
> commits in one agent. (For a very large diff you may use a sub-agent to *propose* the
> clustering, but the `git add` / `git commit` steps stay in the main agent.)

## Flags

| Flag | Effect |
|------|--------|
| `--no-coauthor` | Omit any `Co-Authored-By` trailer from every commit message this run |

Follow the repo's own convention by default: if recent commits carry a `Co-Authored-By`
trailer, match them; if none do, don't add one. `--no-coauthor` forces it off regardless.

## Workflow

1. Run `git status` and `git diff` to inspect all uncommitted changes
2. Check for pre-staged changes with `git diff --cached`. If anything is already
   staged, don't fold it into clusters silently — commit it as its own commit
   (it was likely staged deliberately) or ask the user what to do with it
3. Analyze changes and cluster into logical groups by:
   - Feature or functionality
   - Bug fix
   - Related files (e.g., component + its test + its styles)
   - Type (docs, config, refactor, etc.)
   - If a single file contains changes belonging to different clusters, assign
     it to the most related cluster and mention the extra change in the commit
     body (interactive `git add -p` is not available)
4. For each logical group:
   - Stage relevant files: `git add <files>`
   - Generate conventional commit message (see format below)
   - Commit: `git commit -m "<message>"`
5. Repeat until all changes are committed
6. Docs drift check (see below)
7. Update `CHANGELOG.md` unreleased section (see below), then commit: `docs: update changelog`

## Commit Message Format

Use conventional commits: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`

Examples:
- `feat(auth): add password reset flow`
- `fix(api): handle null response from users endpoint`
- `refactor(utils): extract date formatting helpers`
- `docs: update README installation steps`

## Docs Drift Check (Step 6)

After all code commits are made, check whether the change made existing docs stale:

1. From the commits just created, identify user-facing surface changes: CLI flags/commands,
   config options, install/setup steps, public API, renamed files or skills, changed defaults.
   If there are none (pure refactor/test/internal), skip this step silently.
2. Grep the now-stale terms (old flag names, old commands, old paths) across `README.md`
   and `docs/` (and any other tracked doc the repo's instruction file points at).
3. Update only what the diff invalidated — surgical edits, no rewrites or reorganizing.
4. Stage and commit: `git commit -m "docs: sync docs with <change>"` (or fold into the
   changelog commit if both are one-liners).

This step fixes docs the change broke; it does NOT write new guides or lessons — that is
`reflect`'s job. If the project's instruction file forbids doc edits, skip.

## Changelog Update (Step 7)

After all commits are made, update the `## [Unreleased]` section of `CHANGELOG.md`:

1. Review all commits just created (use `git log` to see them)
2. Write concise changelog entries grouped under Keep a Changelog sections:
   - `### Added` — new features or capabilities
   - `### Changed` — changes to existing functionality
   - `### Fixed` — bug fixes
   - `### Improved` — enhancements to existing features
   - `### Removed` — removed features
3. Classify each entry as **public** or **internal**:
   - **Public**: User-facing features, behavior changes, critical bug fixes
   - **Internal**: Refactors, test changes, lint fixes, DX improvements, infra plumbing
4. Format internal entries under an `#### Internal` heading with `<!-- internal -->`:
   ```markdown
   ### Added
   - **Feature name**: User-facing description

   #### Internal
   <!-- internal -->
   - Implementation detail that users don't need to see
   ```
5. Stage and commit: `git add CHANGELOG.md && git commit -m "docs: update changelog"`

If `CHANGELOG.md` doesn't exist or has no `## [Unreleased]` section, skip this step.

## After Committing

If this session involved tricky bugs, new integrations, or non-obvious patterns, suggest
running the `reflect` skill to capture lessons learned.

## Rules

- Keep commit messages under 72 characters
- Use imperative mood ("add" not "added")
- One logical change per commit
