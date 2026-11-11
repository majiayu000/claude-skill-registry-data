---
name: git-commit
description: "Commit staged changes safely. Runs /verify-before-done first, lets the user choose which files to stage, drafts a project-style commit message (subject + Files / Verification / Contract / Status sections + Co-Authored-By trailer), and commits via HEREDOC. Halts on verification failure, suspected secrets, or pre-commit hook errors. Never uses --no-verify or --amend without explicit user request. Use when the user says /git-commit, 'commit this', 'make a commit', or after a feature is implementation-complete."
user_invocable: true
---

# /git-commit — Safe, Verified, Project-Style Commits

When invoked, run every step below in order. **Do not skip steps. Do not commit on red.** If any halt condition fires, stop and surface the failure to the user — never proceed by bypassing it.

## Context — why this skill exists

Commit hygiene is currently distributed across three places: the Bash tool's default git guidance, the project's `.githooks/pre-commit` regen automation, and the `/verify-before-done` skill. Without a single entrypoint, every commit relies on Claude remembering the rules — which means they get forgotten. This skill is the entrypoint: it ties verification, staging, secret-scan, message-drafting, and commit into one auditable flow.

The skill is **user-global** but **project-adaptive** — it reads recent `git log` output to learn the project's commit-message style instead of hardcoding one.

## Step 0: Preconditions

```bash
git rev-parse --is-inside-work-tree
git status --porcelain=v1 --branch
```

**Halt conditions:**
- Not inside a git work tree → tell the user and stop.
- `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, or `.git/rebase-merge/` exists → resolve those first with raw git, this skill does not handle mid-operation states.
- Working tree is clean (no staged, no unstaged, no untracked) → tell the user there is nothing to commit and stop.

Then read recent commits to learn the project's message style:

```bash
git log -5 --format=fuller
```

Note the structure used in this repo:
- Multi-section bodies with `## Files`, `## Verification`, `## Open follow-ups`?
- `Contract:` and `Status:` trailer lines?
- `Co-Authored-By:` trailer format?
- Subject line tone (imperative, declarative, prefixed `[area]`)?

The drafted message in Step 4 must match the style observed here. **Do not invent a format the project doesn't use.**

## Step 1: Verification gate

Invoke `/verify-before-done` via the Skill tool.

**Halt conditions:**
- Any failure reported by the verification skill → stop, surface the failure, do NOT stage or commit.
- The skill is unavailable in the current project → fall back to baseline checks based on the diff:
  - `.cs` files changed → `dotnet build --nologo --verbosity minimal`
  - `.ts`/`.html`/`.scss` under the `frontend.root-container` slot of `.claude/project-profile.md` → `npm run build` in the relevant project
  - `.py` files changed → `python -m py_compile <changed files>` or the project's lint command
  - Migration files changed → confirm the `*ModelSnapshot.cs` file under `migration.root` is also staged
- Only run baseline checks that are obviously required by the diff. Don't re-run the full suite if `/verify-before-done` ran cleanly.

## Step 2: Inventory changes

```bash
git status --porcelain
git diff --stat
git diff --cached --stat
```

Categorize and present to the user:
- **Staged** — already in the index
- **Modified** — tracked, edited, not staged
- **Added (untracked)** — new files git doesn't know about
- **Deleted** — removed but not staged

If everything is already staged and the user has explicitly indicated "just commit what's staged," skip Step 3 and go to Step 4.

## Step 3: Interactive staging

Show the modified + untracked files in a single list. Use AskUserQuestion (or a clear text prompt with file paths) to confirm which files to stage. Default selection: modified + untracked, deselected by default for any file matching the danger patterns below.

**Hard refuse to stage** (halt and ask for explicit override even if user picks them):
- `.env`, `.env.*`, `*.env`
- `*.pem`, `*.key`, `*.pfx`, `*.p12`
- `id_rsa*`, `id_ed25519*`, `*.ppk`
- Files matching `*credentials*`, `*secret*`, `*password*`, `*token*` (case-insensitive) — but not files where the literal string is a normal identifier (e.g., `PasswordResetTokenEntity.cs` is fine, `tokens.json` is suspicious).

**Hard refuse to stage manually** (the pre-commit hook will regen and stage these):
- `**/generated/**` under the `frontend.root-container` slot
- The generated OpenAPI document the client generator writes
- The generated handbook trees the project's docs generator writes
- `docs/generated/**`
- Any file with the marker header `THIS FILE IS GENERATED`

For each file the user confirms, run:

```bash
git add -- <path>
```

Use `--` and quote paths with spaces. Stage explicit paths only — never `git add -A`, never `git add .`.

After staging, re-run `git diff --cached --stat` and confirm with the user that the staged set matches their intent.

## Step 4: Draft the commit message

**Subject line:**
- Imperative voice ("Add", "Fix", "Refactor"), ≤72 characters.
- Summarize the dominant change, not every file.
- No trailing period.
- If the project's recent commits use a prefix convention (`[area]`, `feat:`, `fix:`), match it. If not, don't invent one.

**Body** (include only the sections that apply, in this order):

```
<subject line>

<one-paragraph explanation of WHY this change exists — the problem it solves
or the goal it serves. 1-3 sentences. Skip for trivial commits where the
subject says everything.>

## Files

- `path/to/file.cs` — one-line role of this file in the change
- `path/to/other.ts` — ...

## Verification

- `dotnet build` — green
- `dotnet test --filter <project>` — N passed
- `/verify-before-done` — passed
- (whatever was actually run)

## Open follow-ups

- <non-blocking item the user mentioned in conversation>

Contract: .claude/concepts/<YYYY-MM-DD>-<slug>.md
Status: implemented (<YYYY-MM-DD>)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**Section rules:**
- `## Files` — skip entirely if ≤2 files staged. Otherwise list every staged file.
- `## Verification` — only include checks that actually ran in Step 1. Never invent verification claims.
- `## Open follow-ups` — only if the user mentioned non-blocking items in this conversation. Never fabricate.
- `Contract:` — only if a concept contract path under `.claude/concepts/` was touched, referenced in the conversation, or actively governs this change. Never invent a path.
- `Status:` — only paired with `Contract:`. Use today's date.
- `Co-Authored-By:` — **always** the last line, no blank line after, exact format `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.

## Step 5: Confirm the draft

Show the full drafted message to the user. Offer three actions:
1. **Approve** → proceed to Step 6.
2. **Edit** → user provides revisions, redraft, show again.
3. **Cancel** → unstage nothing, just stop. Files remain staged for the user to commit manually.

**Never proceed to commit without explicit approval.** Silence is not approval.

## Step 5.5: Changed-file check on the staged files

Once per commit, after the staged set is final and approved, ask the plugin's Changed-file check
whether every staged file is covered by an approved contract. It judges the staged added, copied,
modified and renamed files through the concept gate's own matcher. Find the script through the
plugin only; a copy under the project's `.claude/` is never used, because a file there is trivial
to both gates and could be forged.

```bash
S=.claude/scripts/concept_changed_check.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then CC=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  CC=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$CC" --staged   # macOS and Linux: python3 "$CC" --staged
```

If `CC` is empty, do not run the last line. Otherwise read its exit code:

- **2:** refuse the commit. Show the files the check listed and its `/design-first` text, and tell the
  user to run `/design-first` or pin the contract that covers them. Do not stage around it.
- **0:** go on to Step 6.
- **3, or `CC` empty:** say in one sentence that the check could not run (git missing, not a git
  tree, a slow git call, or the plugin's script not found), then go on to Step 6.

## Step 6: Commit

Use a single-quoted HEREDOC so `$variable`, backticks, and `!history` inside the message stay literal:

```bash
git commit -m "$(cat <<'EOF'
<subject line>

<body>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**Hard rules:**
- **Never** `--no-verify`. If a hook fails, halt, surface the error, and let the user decide what to do.
- **Never** `--amend` unless the user explicitly used the words "amend" or "fix the last commit" at the start of this skill invocation.
- **Never** sign-off bypass (`-c commit.gpgsign=false`) unless the user explicitly requested it.
- **Never** retry a hook-failed commit by stripping the failing files — fix the underlying issue.

If the pre-commit hook regenerates files (TypeScript models, OpenAPI, docs) and stages them into the in-flight commit, that is expected. Note it in Step 7.

## Step 7: Post-commit confirmation

```bash
git status
git log -1 --format=fuller
```

Report to the user:
- Subject line of the new commit + the short SHA.
- Files committed (note any pre-commit-regenerated files that were auto-added).
- Whether the working tree is now clean.
- If anything was *not* committed (e.g., user chose to leave some files unstaged), list those explicitly.

If the post-commit `git status` shows new untracked or modified files that didn't exist before the commit, that's hook output worth surfacing — the user may want a follow-up commit or may need to investigate.

## Halt-and-fix conditions (summary)

| Condition | Action |
|---|---|
| Mid-rebase / mid-merge | Stop. User resolves manually. |
| Working tree clean | Stop. Nothing to commit. |
| `/verify-before-done` fails | Stop. Surface failure. Do not stage or commit. |
| Suspected secret in staging selection | Halt. Require explicit override or remove. |
| Generated file staged manually | Halt. Unstage; let pre-commit hook own it. |
| User declines draft | Stop. Leave files staged. |
| Pre-commit hook fails | Stop. Surface error. Never `--no-verify`. |
| User asks to amend without saying so up front | Stop. Confirm intent before amending. |

## When NOT to use this skill

- Mid-rebase, mid-merge, mid-cherry-pick → use raw git.
- Force-push, history rewrite, branch surgery → out of scope by design.
- Squash / fixup workflows → use raw `git commit --fixup` and `git rebase -i` manually.
- Pushing to remote → out of scope. The user runs `git push` themselves.

## Skill integrations

- **Always invokes** `/verify-before-done` at Step 1 (or its baseline fallback).
- **Plays well with** `/debug` and `/tdd-first` — both leave the working tree in a state this skill can commit.
- **Replaces** ad-hoc "let me commit this for you" Bash tool flows. Once this skill exists, default to it for any commit.
