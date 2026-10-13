---
name: ref
description: "Refer another project while protecting sensitive information. Use when: (1) User says 'refer project', 'copy from project', or 'look at another repo', (2) User wants to reference patterns or setup from another codebase, (3) User needs to learn from another project's structure without leaking private data. Pass -p/--pull to verify the referenced repo is fresh before reading it — checks it's on its default branch, checks for uncommitted work, then pulls and reports the commit it landed on."
argument-hint: "[-p|--pull] [-u|--update] <slug|path> [slug2 ...] — repo slug (e.g. zmod) or full path"
---

> **DO NOT auto-invoke this skill.** Referencing another project exposes its contents to the current session, which may leak private/client information across project boundaries. Always ask for user confirmation before proceeding.

# Refer Another Project Command

Use this command when you need to reference, copy, or learn from another project's setup, structure, or patterns.

## Resolving Project Paths

Arguments can be **slugs** (short names) or **full paths**. Multiple slugs/paths can be provided, space-separated.

**Slug resolution rule:**

For each slug argument (any argument that is NOT an absolute path starting with `/`):

1. Search for matching directories at `$HOME/repos/*/{slug}` (one level of category directories)
2. If exactly one match is found, use it as the project path
3. If no match is found, **stop and report the error** to the user — do not guess or continue
4. If multiple matches are found, list them and ask the user to clarify

**Examples:**

- `/ref zmod` → resolves `$HOME/repos/*/zmod` → e.g. `$HOME/repos/zp/zmod`
- `/ref zmod dotfiles` → resolves both slugs independently
- `/ref $HOME/repos/zp/zmod` → uses full path directly

```bash
# Resolution command for each slug
ls -d $HOME/repos/*/{slug} 2>/dev/null
```

## Pull Mode (`-p` / `--pull`)

The referenced repo is a working checkout, not a pristine mirror. It may sit on a stale
commit, or on someone's topic branch, or hold half-finished edits. Reading it in that
state means referring to **data that isn't the project's current truth** — the exact
failure this flag exists to prevent.

When `-p` or `--pull` is passed, run the freshness gate below **for each resolved path,
before reading a single file from it**. The gate composes with every other mode: with
`-u` it runs before `/x-as-pr` is invoked there.

Run every command with `git -C <resolved-path> …` — never `cd` into the referenced repo
for the gate.

### Step 1 — Branch check

```bash
git -C <path> rev-parse --abbrev-ref HEAD                       # current branch
git -C <path> symbolic-ref --quiet refs/remotes/origin/HEAD     # default branch (origin/<default>)
```

If `symbolic-ref` fails, fall back in this order and stop at the first that answers:

```bash
git -C <path> remote show origin | sed -n 's/.*HEAD branch: //p'
gh repo view --json defaultBranchRef -q .defaultBranchRef.name  # run with cwd = <path>
```

If none resolves, tell the user the default branch can't be determined and ask which
branch to treat as default. Do not assume `main`.

**If current branch == default branch:** go to Step 2.

**If current branch != default branch:** STOP and ask the user. Do not check out
anything on your own — this is a checkout of a repo the user may be mid-work in.

> The referenced repo `<slug>` is **not** on its default branch `<default>` — it's on
> `<current-branch>`. Check out `<default>` there instead of `<current-branch>`?

- **Yes** → `git -C <path> checkout <default>`, then go to Step 2.
  If checkout fails (local changes would be overwritten), report the git error verbatim
  and go to the Step 2 dirty-tree question instead of forcing anything.
- **No** → **cancel referring to this repo entirely.** Do not read it, do not fall back
  to reading the topic branch. The user being on another branch is a signal that
  something is in flight there; a "no" means they've now noticed it and want to handle it
  themselves. Report the cancellation and continue with any other resolved repos.

### Step 2 — Uncommitted changes check

```bash
git -C <path> status --porcelain
git -C <path> diff --stat
git -C <path> diff --cached --stat
```

Clean tree → go to Step 3.

Dirty tree → classify what's there. Judge by **what the files are**, not by how many.

**Benign — proceed to Step 3 without asking:**

- Build output and generated assets (`dist/`, `build/`, `.next/`, `out/`, compiled CSS/JS)
- Temp / scratch dirs (`tmp/`, `__inbox/`, `.cache/`, `node_modules/` noise)
- Lockfile churn with no `package.json` change
- Editor / OS cruft (`.DS_Store`, `*.swp`)
- A one-or-two-line tweak in a file irrelevant to what's being referenced

**Not benign — STOP and ask:**

- Edits to source files, configs, or docs — especially anything in the area being
  referenced
- Anything staged and clearly deliberate
- A broad diff across many source files (real work in progress)

> The referenced repo `<slug>` has uncommitted changes that look like real work:
> `<short file list + diffstat>`. How should I handle this? I can (a) leave them and pull
> anyway if it fast-forwards, (b) skip the pull and refer to the repo as-is, or
> (c) cancel referring to this repo.

Act on the answer only. **Never `stash`, `checkout --`, `reset`, or `clean` in the
referenced repo** — those discard the user's work in a repo they didn't ask you to
modify. If they want a stash, they can make one themselves.

### Step 3 — Pull and confirm

```bash
git -C <path> pull --ff-only
```

`--ff-only` is deliberate: a pull that can't fast-forward means the local branch has
diverged, which is exactly the "something is going on there" case. On failure, report the
git error and ask the user how to proceed — do not merge or rebase to force it through.

Then confirm the checkout actually advanced to current upstream:

```bash
git -C <path> log -1 --format='%h %ad %s' --date=short
git -C <path> status -sb | head -1     # should show no "behind"
```

Report the result in one line before reading anything:

> `<slug>` @ `<default>` — pulled, now at `<sha> <date> <subject>`

If the repo was already up to date, say that instead. Either way the user must see
**which commit the reference is based on**, so a stale reference is visible rather than
silent.

### Example

```
/ref -p zmod how does it configure vitest
```

1. Resolve `zmod` → `$HOME/repos/*/zmod`
2. Confirm it's on `develop` (its default) — if it's on `topic/foo`, ask before checking out `develop`
3. Confirm nothing meaningful is uncommitted there
4. `git pull --ff-only`, report `zmod @ develop — pulled, now at abc1234 2026-08-29 <subject>`
5. Only then read its vitest config

### Without `-p`

Default behaviour is unchanged — the repo is read exactly as it sits on disk. If you
notice while reading that the repo looks stale or is on a topic branch, mention it and
offer `-p`; don't run the gate uninvited, since it mutates another repo's checkout.

## Update Mode (`-u` / `--update`)

When `-u` or `--update` is passed, this skill switches to **fix-and-PR mode**: you've found a problem in the referenced project and want to fix it there directly.

### How it works

1. **Remember the current project path** (you'll return here afterward)
2. **`cd` into the resolved project path**
3. **Run `/x-as-pr -co` from the main branch** with the fix instructions
- The `/x-as-pr` workflow handles branching, implementing, reviewing, and opening a draft PR
- Pass any remaining arguments (after the slug and flags) as implementation instructions to `/x-as-pr`
4. **After the PR is created**, `cd` back to the original project and resume work

### PR content rules for update mode

The PR on the referenced project must:

- **Describe the fix in full detail** — what was wrong, why, and how it's fixed
- **NEVER mention the originating project** — do not write which project led to discovering the bug. Each project must remain completely independent. No project names, slugs, paths, or hints about what you were working on when you found the issue
- Use generic phrasing like "discovered during usage" or "found during testing" if context is needed

### Example

```
/ref -u zmod fix the broken export path in package.json
```

This will:

1. Resolve `zmod` → `$HOME/repos/*/zmod`
2. `cd` into that directory
3. Run `/x-as-pr -co fix the broken export path in package.json`
4. Return to the original project after PR is created

### Constraints

- Only **one slug** is allowed with `-u` (you can't fix multiple projects at once)
- If multiple slugs are provided with `-u`, report an error and stop

## Critical Security Warning

When referencing another project, you MUST protect project-specific sensitive information. Never copy concrete content or secrets - only copy patterns, structures, and configurations.

**NEVER leak the referenced project's name or directory path into the current project's artifacts.** This includes:

- Git commit messages
- PR titles and descriptions
- GitHub issue titles and comments
- Log files, TODO comments, or any written output in the working project

The referenced project may belong to a work client. Exposing client names or project identifiers in public or semi-public artifacts (issues, PRs, commits) causes real problems. Always use generic descriptions like "another project" or "reference implementation" instead.

## What You CAN Copy (Safe)

- **Project structure**: Directory organization, folder naming conventions
- **Configuration patterns**: Build tool configs, linter configs, framework setup patterns
- **Package dependencies**: package.json dependencies (not scripts with project-specific values)
- **Code patterns**: Component structures, utility function patterns, architectural approaches
- **Setup procedures**: How things are configured (but not the concrete values)
- **Type definitions**: Generic type patterns and interfaces
- **Test patterns**: Testing setup and structure (not test data with real values)

## What You MUST NOT Copy (Dangerous)

- **Project titles and names**: Product names, brand names, company names
- **Concrete content**: Article text, documentation content, marketing copy
- **HTML content with specific info**: Pages with real product/company information
- **Database information**: Connection strings, table names with business meaning, credentials
- **API keys and secrets**: Any `.env` values, API tokens, passwords
- **URLs and endpoints**: Production URLs, internal service addresses
- **User data**: Any real user information, emails, names
- **Business logic specifics**: Proprietary algorithms, pricing logic, business rules
- **Internal documentation**: Private docs, internal guides, company-specific processes
- **Asset files**: Images, logos, brand assets that belong to the other project

## Argument Parsing

Parse `$ARGUMENTS` to extract:

- **`-p` or `--pull` flag**: If present, run the freshness gate on every resolved path before reading anything (see "Pull Mode" above)
- **`-u` or `--update` flag**: If present, switch to update mode (see "Update Mode" above)
- **Slug(s) or path(s)**: Project identifiers to resolve
- **Remaining text** (update mode only): Implementation instructions passed to `/x-as-pr -co`

Flags are independent and may be combined: `-p` alone freshens then reads; `-p -u` freshens then fixes; `-u` alone fixes whatever is on disk.

## Instructions

### Default mode (no `-u` flag)

0. **If `-p` was passed**: run the Pull Mode gate on every resolved path first, and abort any repo the gate cancels
1. **Identify what you need**: Clearly state what patterns or setup you want to learn from
2. **Read with filtering mindset**: When reading files, mentally separate:
- Generic patterns (copy these)
- Project-specific values (never copy these)
3. **Adapt, don't copy verbatim**: Transform patterns to fit the target project
4. **Replace all identifiers**: Any names, titles, or identifiers must be replaced with appropriate values for the target project
5. **Double-check before writing**: Before writing any file, verify no sensitive info leaked through

## Example Scenario

When copying Docusaurus setup from `$HOME/foo/bar/`:

**Safe to reference:**

- `docusaurus.config.js` structure and plugin configurations
- Directory structure (`docs/`, `src/`, `static/`)
- Theme customization patterns
- Sidebar configuration format
- Build and deployment scripts structure

**Must NOT copy:**

- Site title, tagline, organization name in config
- Actual documentation article content
- Logo and favicon files
- Any URLs (baseUrl, url, GitHub links)
- Author information
- Analytics IDs
- Any text content within markdown files

## Reminder

Always ask yourself: "Does this contain information specific to the source project?" If yes, do not copy it directly. Extract the pattern and apply it fresh to the target project.
