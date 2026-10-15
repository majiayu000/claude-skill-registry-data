---
name: commit
description: Stage and commit changes with Conventional Commits format and co-author attribution.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "[-m \"message\"] (or auto-generate from diff)"
category: dev-tools
status: candidate
---
# Commit Command

Create a well-formed commit following project conventions.

## Execution

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=commit] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### 1. Review changes
```bash
git status --short --untracked-files=all
git diff --stat              # unstaged tracked changes only
git diff --cached --stat     # staged changes only
git diff                     # full unstaged tracked diff for analysis
```

`git diff --stat` does not include untracked files. Treat every `??` line in
`git status --short --untracked-files=all` as separate scope evidence before
staging. For material new files or directories, record `wc -l <file>` or
`find <dir> -type f | wc -l` before claiming size/scope.

### 2. Draft commit message
Follow Conventional Commits format:
```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `perf`
**Scope**: module or area affected (e.g., `cognition`, `security`, `tests`, `bus`)

### 3. Stage specific files
```bash
git add <file1> <file2> ...
```
- **Never** use `git add -A` or `git add .` (may include secrets or large files)
- **Never** stage `.env`, `credentials.json`, or files with tokens
- Review what's staged: `git diff --cached --stat`

### 3b. Diff-stat sanity check (verbatim numbers only)

Before writing any line-count claim into the commit body, capture the staged diff-stat **and use those exact numbers** in the message. Don't infer insertion/deletion counts from earlier diff summaries or agent memory — they drift.

```bash
git diff --cached --stat | tail -1
# example output:  3 files changed, 88 insertions(+), 1 deletion(-)
```

If the commit body says "88 insertions", that phrase must match the above output. If it says "118 net adds", verify `118 = insertions - deletions` against the stat.

**Rationale**: On 2026-04-16 during the Gemini-crce salvage, adversary.py was described as "116 insertions" in the commit message and "+118 net adds" elsewhere in the same session's output. The stat was `116 insertions(+), 2 deletions(-)` → 114 net, making both numbers wrong. Harmless here, but drift compounds. Capture before you cite.

### 3c. Consequential change pre-flight (skills, rules, agents)

Before staging, check if any changed file is under `skills/`, `rules/`, or `agents/`:
```bash
git diff --name-only | grep -cE '^(skills/|rules/|agents/)' || echo 0
```
If the count is > 0, this is a **consequential skill/rule change**. You MUST:
1. Read `~/.agents/rules/skill-commit-preflight.md` and run the checklist.
2. Verify platform smoke tests passed (Windows + Unix if shell commands present).
3. Create a review packet at `review-packets/YYYY-MM-DD-<topic>-<agent>.md`.
4. Only then proceed to `git add`.

Skipping this pre-flight will trigger the governance hook at commit time and force a retry.

### 4. Commit
```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body if needed>

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

### 5. Verify
```bash
git log --oneline -1
git status
```

## Rules
- Pre-commit hook runs targeted tests on changed files -- if it fails, fix the issue and create a NEW commit (don't amend)
- Never use `--no-verify` to skip hooks
- Never amend published commits without explicit approval
- Keep commits focused: one logical change per commit
- If unsure about scope, split into multiple smaller commits

## Skill Chains

### Mandatory (MUST pass before commit)

- **`[dod]`** (Definition of Done) MUST pass for the task type. No exception.
  Prevents committing incomplete work.

### Advisory

- **After commit**: `[pr-summary]` (if ready for PR), `[bus]` (STATUS message)

## Authority

- **T1 (TRUSTED)**: May commit without pre-approval
- **T2 (Active/High)**: May commit with `[dod]` passed
- **T3 (Medium)**: MUST get operator approval AND `[dod]` passed
- **T4 (Probationary)**: BLOCKED — cannot invoke this skill
- **Operator**: Override any restriction
