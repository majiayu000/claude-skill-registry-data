---
name: mc-commit
description: ALWAYS use this skill when creating git commits. Follows conventional commit standards with scope detection and secret awareness. Trigger on any commit, stage and commit, save changes, checkpoint, or request to commit work.
---

# MC Commit

Create commits following conventional commit standards.

## Process

### 1. Pre-flight & Analyze (one call)

Gather everything in a single command rather than four round-trips:

```bash
git branch --show-current && git status --porcelain && git diff --stat HEAD && git log --oneline -5
```

If on `main`/`master`, ask whether to branch first. If nothing is staged or modified, stop.

### 2. Stage

- Identify which top-level areas are touched (directory names, packages, or modules) and the type of change
- Read full diffs only for files you need to classify or stage safely
- **Never commit**: `.env`, `.dev.vars`, `credentials.json`, `*.pem`, private keys, or anything matching a gitignored secrets file (e.g. `secrets.zsh`) — warn if present and unstage it
- Prefer explicit path staging (`git add <files>`)
- Use `git add -A` only after confirming every changed path belongs in the same commit
- If changes are mixed, make multiple commits by staging coherent path groups; after each commit, re-run `git status --porcelain` and continue until clean

### 3. Compose the Message

```
<type>(<scope>): <subject>

<body — optional, explain why>
```

**Types**: `feat` · `fix` · `refactor` · `docs` · `chore` · `test` · `ci` · `perf` · `style`

**Scope**: the top-level directory or module the change is concentrated in (e.g. `git`, `fish`, `dot`, `packages`, `docs`). Omit scope for genuinely cross-cutting changes.

**Subject**: imperative mood, lowercase after colon, no period, max ~70 chars total.

**Body**: explain motivation/what was wrong, not what the diff already shows. Use real newlines, never literal `\n`.

Never include AI attribution footers unless the user explicitly asks.

### 4. Verify, then Commit

First, run whatever cheap verification actually applies to what changed — e.g. `bash -n <script>` for a touched shell script, `npm run typecheck`/`lint` if a `package.json` defines them and JS/TS files changed. Skip verification that clearly doesn't apply; don't invent checks the project doesn't have. If a verification step already ran this session against the currently staged changes with nothing since, don't re-run it — just mention it already passed.

**Always write the message to a temp file and commit with `git commit -F`.** Do not use inline `-m`
for anything but a bare subject line, and never use a heredoc inside process substitution
(`git commit -F <(cat <<'EOF' ...)`). A single apostrophe in a word like "shell's", or a backtick,
`$`, or quote anywhere in the body, breaks the shell and costs a retry. The temp file is always
correct, so skip straight to it:

```bash
# write /tmp/commit-msg.txt with the file-writing tool, then:
git diff --cached --stat && git diff --cached --check && git commit -F /tmp/commit-msg.txt
```

`git diff --cached --check` catches trailing whitespace and conflict markers.

Then confirm in one call:

```bash
git status --porcelain && git log -1 --format="%B"
```

Clean up the temp file once the commit is verified.

## Examples

```
feat(dot): add oh-my-zsh bootstrap to init tool registry

Fish is no longer the managed shell; dot init should be able to set
up oh-my-zsh on a fresh machine the same way it used to set up fish.
```

```
fix(git): stop fomo/lg aliases shelling out to fish

Both aliases called `fish -c ...`, which no longer exists now that
the shell is zsh. Rewrote fomo as a self-contained sh one-liner since
git `!` aliases don't run in the interactive shell's rc files.
```

```
chore(packages): drop fish and fisher from the base bundle
```

## Principles

- One coherent change per commit; the repo should be in a working state after each
- If current branch is `main`/`master`, ask whether to create a branch first; suggest `<scope>/<short-topic>`
- Explain **why**, not just **what**
- Never skip pre-commit hooks (`--no-verify`)
- Batch independent git reads into one command; every extra round-trip costs time and tokens
- **Never run `git stash pop` speculatively.** It pops whatever is on top of the stack, which may be
  an unrelated stash someone left months ago. Only pop a stash you just created in the same command
  chain, and use `git stash push` + an explicit `git stash apply stash@{0}` if you must be sure.
  To read a file from another ref, use `git show <ref>:<path>` instead of stashing.
