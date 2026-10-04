---
name: init-pipeline
description: "Infrastructure skill for scaffolding pipeline enforcement into a project. Sets up Claude Code hooks (TDD classification gate, git guardrails, optional quality gate), pre-commit hooks (detects existing tools, defaults to Lefthook + Biome + pnpm if none found). Run when setting up a project for pipeline work, and again to re-scaffold a hook that predates the post-review edit lock or a classification marker; /execute Step 0 auto-invokes it when the hook is missing or stale."
---

# Init Pipeline

Scaffold pipeline enforcement infrastructure into the current project: Claude Code hooks for skill compliance, git guardrails for safety, and pre-commit hooks for code quality. Detects existing tools before suggesting defaults.

## When to use

- Automatically invoked by `/execute` Step 0 if `.claude/hooks/enforce-classification.sh` is missing, or if the installed hook does not read every path its own classification clause tests — the lock's stamp flag, or a marker such as `.claude/.lfg-active` (see § 2's re-scaffold note)
- Manually by the user when setting up a new project for pipeline work

## What it sets up

All files are created in the **target project**, not in the Skill Kit repo.

### 1. Git guardrails (Claude Code hook)

Invoke `/git-guardrails-claude-code` with project scope.

This installs a PreToolUse hook on Bash that blocks destructive git commands — force pushes, hard resets, forced cleans, force branch deletes, and whole-tree checkout/restore. The authoritative list lives in `/git-guardrails-claude-code`'s "What Gets Blocked" and "What Stays Allowed" sections; read it there rather than here.

The list is deliberately not restated in this file. It was, and the copy was wrong: it claimed plain `git push` was blocked, which it never has been. That is the same defect as #227 — documentation asserting coverage the matcher does not have — and a second copy is a second thing to keep true, in the file more downstream projects actually read.

### 2. TDD classification gate (Claude Code hook)

Create `.claude/hooks/enforce-classification.sh` and make it executable. This blocks Write/Edit to implementation files unless the `/execute` Step 3 classification gate has been passed.

The hook checks for any of `.claude/.tdd-active` (TDD invoked), `.claude/.tdd-skipped` (visual frontend, explicitly opted out), or `.claude/.lfg-active` (`/lfg` proof-of-concept mode). No path checking beyond the trigger surface — it enforces "did you go through the gate?"

It carries a second clause on the same trigger surface: the **post-review edit lock**, which refuses an implementation write while `.claude/.review-stamped` exists and `.claude/.fix-findings-active` does not. The first clause asks "was this work classified?"; the second asks "is this edit landing after a review, authored by the session the review went around?" Both are one script because both key off the same file-pattern decision.

**The two clauses are ordered, not independent — read the `.review-stamped` term in the first one before editing either.** The classification clause stands down on a stamped branch, so the post-review clause is the only one that decides there. This is not a stylistic preference: `/execute` Step 6 removes `.claude/.tdd-active`, `.claude/.tdd-skipped`, and `.claude/.lfg-active` *before* it hands off to `/pre-merge`, so a stamped branch never carries a classification marker. Two independent clauses in this order therefore never reach the second one — the `/fix-findings` fixer is refused despite holding the flag written for it, and the authoring session is refused by the wrong clause, told to invoke `/tdd` and never told that `/fix-findings` is the route. A lock whose designed affordance never prints is a lock nobody can use, and it was described here as "independent" while behaving this way. `scripts/test-post-review-edit-lock.sh` now drives `/execute` Step 6's removal as part of the round trip, so the ordering is measured rather than asserted.

**Install-time: the trigger surface is settled on one of three paths, and at most one of them applies to a given run.** Read `.claude/hooks/enforce-classification.sh` in the target project before writing anything. What is already installed there decides the path — not how this skill was invoked, because `/execute` Step 0 routes both of its verdicts (`hooks-absent` and `hooks-stale`) to the same auto-invocation. Take no instruction from a path you are not on.

**Path A — no hook installed, and a user is present.** Present the default include list and ask:

> "The TDD classification gate fires on Write/Edit of files matching a pattern list. Default: `*.ts, *.tsx, *.astro, *.py, *.go, *.rb, *.java, *.rs, *.js, *.jsx, *.vue, *.svelte`. Over-gating is acceptable — classification is a quick decision at the top of /execute, though backend/behavior-heavy matches will trigger a full /tdd cycle. Accept the default, or customize for this project?"

Use the confirmed list (default or customized) to populate the `IMPL_PATTERNS` array in the hook body below. Over-gating is acceptable — the cost of an extra classification prompt is lower than the cost of silent under-fire on a polyglot project.

**Path B — no hook installed, and `/init-pipeline` is running non-interactively** (auto-invoked by `/execute` Step 0 on a project whose hooks gate reported `hooks-absent`). Do not ask. Populate `IMPL_PATTERNS` with the default list from Path A's question and record that fact in the hook body via a leading comment.

**Path C — a hook is installed but does not read every path clause 1 tests** (`hooks-stale`: a project initialized before one of those paths shipped — before the post-review edit lock, or before `.claude/.lfg-active`). `/execute` Step 0 prints the terms it found missing on a `missing:` line on stderr, beside the verdict it prints on stdout; every one of them is a boundary this project's install predates, and this path's job is to bring the hook up to all of them at once rather than one boundary per run. The trigger-surface question was answered at that project's own install, so neither Path A's question nor Path B's default applies here — both belong to the fresh-install case, and reaching for either on this path is the one harm this path exists to prevent. Do not ask again, and do not silently re-default: carry the installed hook's `IMPL_PATTERNS` array — with the provenance comment above it — and its skip clauses over verbatim, because the project may have customized them at its own install time, and changing them changes the classification gate's behavior for work that has nothing to do with the lock. Replace everything from the installed hook's `# Check for classification markers` comment through its final `exit 0` with the marker-check clauses at the foot of the block below. On a pre-lock hook that is one clause replaced and one added, not two replaced, because such a hook carries the classification clause alone and the post-review clause is what the upgrade brings; on a hook that already has both, it is both replaced with current text. Either way the span is the same and the replacement is wholesale, so this path never has to know which boundary it is crossing — which is what lets one run fix a hook that is behind on several.

**The rest of the run, per path.** § 4 and § 5 are the two sections below that wait on a human — § 4 presents its detection findings and holds for a confirmation before invoking `/setup-pre-commit`, and § 5 asks whether to install the optional quality gate — and a run with nobody to ask cannot execute either. That is not hypothetical: `/execute` Step 0 sends both of its verdicts here and holds Step 1 until this skill reports, so a section waiting on an answer nobody is present to give stalls the caller rather than the callee, and an AFK Ralph iteration drives `claude --message` with no user at the keyboard at all. On **Path A**, run everything below, § 4 and § 5 included. On **Path B**, run § 3, § 6 and § 7; take § 4 without asking, applying what its detection block finds or the default it names when it finds nothing; and skip § 5, which is optional and whose unanswered default is no. On **Path C**, run § 3 (a merge, never an overwrite) and § 6 — whose `.gitignore` append is idempotent, and is the step that stops the lock's two flags from landing as committable untracked files in a repo that predates them — then stop: skip § 4, § 5 and § 7 outright, because this project answered them at its own install and a lock upgrade that re-opens a settled toolchain decision is doing something nothing asked it to do. If a Path C run notices that a section it skipped never ran at that project at all, say so in what it reports and leave it — `/init-pipeline` invoked by hand, with a user present, is Path A and asks properly.

**Skip logic stays extension-agnostic.** Tests, type declarations, and config files are detected by path substring (`*test*`, `*spec*`, `.d.ts`, `.config.*`) rather than per-language expansion.

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Implementation patterns — populated at install time from the user's answer to
# the /init-pipeline trigger-surface question. Over-gating is intended.
IMPL_PATTERNS=("*.ts" "*.tsx" "*.astro" "*.py" "*.go" "*.rb" "*.java" "*.rs" "*.js" "*.jsx" "*.vue" "*.svelte")

MATCHED=0
for pattern in "${IMPL_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == $pattern ]]; then MATCHED=1; break; fi
done
if [ $MATCHED -eq 0 ]; then exit 0; fi

# Skip test files and type declarations (extension-agnostic)
if [[ "$FILE_PATH" == *test* || "$FILE_PATH" == *spec* || "$FILE_PATH" == *.d.ts ]]; then
  exit 0
fi
# Skip config files (drizzle.config, vite.config, etc.)
if [[ "$FILE_PATH" == *.config.* ]]; then
  exit 0
fi
# Check for classification markers — but stand down on a stamped branch, so the
# post-review clause below is the one that decides there. /execute Step 6 removes
# EVERY classification marker before it hands off to /pre-merge, so by the time
# .review-stamped exists there is never a marker left for this test to find.
# Without the .review-stamped term, this clause short-circuits every post-review
# write: the /fix-findings fixer is refused outright, and the authoring session is
# refused by the wrong clause, under a message that names /tdd and never names the
# route the lock was built to offer.
if [ ! -f "$CLAUDE_PROJECT_DIR/.claude/.review-stamped" ] && [ ! -f "$CLAUDE_PROJECT_DIR/.claude/.tdd-active" ] && [ ! -f "$CLAUDE_PROJECT_DIR/.claude/.tdd-skipped" ] && [ ! -f "$CLAUDE_PROJECT_DIR/.claude/.lfg-active" ]; then
  echo '{"decision":"block","reason":"BLOCKED: classify work in /execute Step 3 before writing implementation files. Either invoke /tdd (backend/behavior-heavy), create .claude/.tdd-skipped (visual frontend), or invoke /lfg (proof-of-concept mode)."}' >&2
  exit 2
fi
# Post-review edit lock. /pre-merge Phase 4 touches .review-stamped beside the
# review-currency stamp; /fix-findings touches .fix-findings-active when it
# loads and removes it when it reports. Between those two, an implementation
# edit is a post-review fix authored by the session the review just went around.
if [ -f "$CLAUDE_PROJECT_DIR/.claude/.review-stamped" ] && [ ! -f "$CLAUDE_PROJECT_DIR/.claude/.fix-findings-active" ]; then
  echo '{"decision":"block","reason":"BLOCKED: this branch has been reviewed and stamped. A post-review fix needs an independent author. Either invoke /fix-findings <numbers>, or delete .claude/.review-stamped to take the edit yourself."}' >&2
  exit 2
fi
exit 0
```

**The two routes the refusal names, and what the clause actually refuses.**
Invoking `/fix-findings` routes the edit to a sub-agent that did not write the
code; deleting `.claude/.review-stamped` by hand takes the edit anyway. That
second choice is made silently today, and printing it is what makes it visible.
It is not the only way out, and the difference matters at install time: the hook
is registered in § 3 below on `"matcher": "Write|Edit"`, so no `Bash` write is
ever presented to it — `sed -i`, `tee`, a heredoc, `printf >`, or `rm
.claude/.review-stamped` itself — and within Write/Edit it refuses only a path
that matches `IMPL_PATTERNS` and survives the skip logic, which leaves
`.claude/.fix-findings-active`, this hook script, and `.claude/settings.json`
all writable while the lock is armed. Install it as a stop on the *default*
post-review edit, not as an enclosure around the branch.

**What the clause does not cover, in the matcher's terms rather than a file's
role.** It reuses the `IMPL_PATTERNS` list and the `*test*` / `*spec*` /
`*.d.ts` / `*.config.*` skip logic above, unchanged, and those patterns match a
*substring of the whole path*. Claude Code hands the hook an absolute path, so
the skips reach further than the file roles they were named for:
`src/latest-news.ts` and `src/respectful.ts` are skipped for containing `test`
and `spec`, so is anything under a `testimonials/` directory, so is
`src/app.config.local.ts`, and so is every file in a project checked out beneath
a path like `/Users/tester/`. Giving the two clauses different definitions of
"implementation file" would make the hook's behavior unreadable from its own
source, so the patterns stay — a re-run of `/pre-merge`, not this hook, covers
the edits they let through.

After writing, run: `chmod +x .claude/hooks/enforce-classification.sh`

### 3. Claude Code settings

Create or merge `.claude/settings.json` with both hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/enforce-classification.sh"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If `.claude/settings.json` already exists, merge the `hooks.PreToolUse` entries — do not overwrite existing settings.

### 4. Pre-commit hooks and package manager enforcement

**Gated by § 2's rule for the rest of the run, per path — read it before asking anything here.**

**Detect before suggesting.** Before invoking any setup, check what the project already uses:

```bash
# Package manager — check lockfiles
ls pnpm-lock.yaml package-lock.json yarn.lock bun.lockb 2>/dev/null

# Formatter/linter — check deps and configs
grep -E "biome|prettier|eslint|oxlint|dprint" package.json 2>/dev/null
ls biome.json biome.jsonc .prettierrc .prettierrc.* prettier.config.* .eslintrc* eslint.config.* 2>/dev/null

# Hook manager — check for existing setup
ls lefthook.yml .husky 2>/dev/null
```

**Present findings to the user and ask for confirmation:**

- If a formatter/linter is detected → "Found [tool]. I'll use it for pre-commit hooks."
- If none detected → "No formatter/linter found. I'd suggest Biome (handles both formatting and linting, fast, zero-config). Want Biome, or something else?"
- If a hook manager is detected → "Found [Lefthook/Husky]. I'll use it." (Suggest migrating Husky to Lefthook if Husky is found.)
- If none detected → "No hook manager found. I'd suggest Lefthook. OK?"
- If a package manager lockfile is detected → use that package manager
- If none detected → "No lockfile found. I'd suggest pnpm. OK?"

**After user confirms**, invoke `/setup-pre-commit` with the confirmed tools.

**Recommended Lefthook + Biome config** (when both are confirmed):

```yaml
# Pre-push hook for vitest run should be added after test suite stabilizes.
pre-commit:
  commands:
    check:
      glob: "*.{js,ts,cjs,mjs,d.cts,d.mts,jsx,tsx,json,jsonc}"
      run: pnpm biome check --write --no-errors-on-unmatched --files-ignore-unknown=true --colors=off {staged_files}
      stage_fixed: true
```

Key flags: `--no-errors-on-unmatched` prevents false failures when no staged files match, `--files-ignore-unknown=true` avoids Biome choking on unsupported files, `--colors=off` gives cleaner hook output. Skip typecheck in pre-commit (too slow) — add it as a pre-push hook later.

**Package manager enforcement:** If the confirmed package manager is pnpm (detected or chosen), add the `only-allow` guard:

```json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```

For npm or yarn, skip this step — `only-allow` is only needed when enforcing pnpm specifically.

### 5. Quality gate (Claude Code hook — optional)

**Gated by § 2's rule for the rest of the run, per path — read it before asking anything here.**

Ask the user: "Do you want a quality gate hook that runs feedback loops during editing? This catches issues while Claude works, not just at commit time."

If yes, create `.claude/hooks/quality-gate.sh` and make it executable. This runs as a **PostToolUse** hook on `Write|Edit`, providing immediate feedback after each file change. The first thing it does is anchor to `$CLAUDE_PROJECT_DIR` and no-op if that directory is gone — a hook firing from a worktree that was just torn down (e.g. during `/closeout`) must not emit false `MODULE_NOT_FOUND` errors from a vanished `node_modules`.

**Detect available feedback loops first.** Check `package.json` scripts for `check`/`lint`, `tsc`/`typecheck`, and `test`/`vitest`. Only include loops that actually exist.

```bash
#!/bin/bash
# Quality gate — runs after each Write/Edit to catch issues early.
# Only runs on TypeScript/JavaScript files. Skips test/config files.

# Anchor to the project root before running any feedback loop. If the
# directory is gone — e.g. a worktree was removed out from under the
# shell during /closeout teardown — no-op instead of emitting false
# MODULE_NOT_FOUND errors from a vanished node_modules. A stranded cwd
# must never masquerade as a lint/type failure.
if [ -z "$CLAUDE_PROJECT_DIR" ] || [ ! -d "$CLAUDE_PROJECT_DIR" ]; then
  exit 0
fi
cd "$CLAUDE_PROJECT_DIR" || exit 0

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only gate TypeScript/JavaScript implementation files
if [[ ! "$FILE_PATH" == *.ts && ! "$FILE_PATH" == *.tsx && ! "$FILE_PATH" == *.js && ! "$FILE_PATH" == *.jsx ]]; then
  exit 0
fi
# Skip test files, type declarations, config files
if [[ "$FILE_PATH" == *test* || "$FILE_PATH" == *spec* || "$FILE_PATH" == *.d.ts || "$FILE_PATH" == *.config.* ]]; then
  exit 0
fi

# 1. Biome check (fast — format + lint)
BIOME_OUTPUT=$(pnpm biome check src/ 2>&1)
BIOME_EXIT=$?

# 2. TypeScript type check
TSC_OUTPUT=$(pnpm tsc --noEmit 2>&1)
TSC_EXIT=$?

if [ $BIOME_EXIT -ne 0 ] || [ $TSC_EXIT -ne 0 ]; then
  if [ $BIOME_EXIT -ne 0 ]; then
    echo "Biome errors found:" >&2
    echo "$BIOME_OUTPUT" >&2
    echo "" >&2
  fi
  if [ $TSC_EXIT -ne 0 ]; then
    echo "TypeScript errors found:" >&2
    echo "$TSC_OUTPUT" >&2
  fi
  exit 2
fi

# 3. Run tests for changed files only (vitest import graph analysis)
VITEST_OUTPUT=$(pnpm vitest run --changed 2>&1)
VITEST_EXIT=$?

if [ $VITEST_EXIT -ne 0 ]; then
  echo "Tests failed for changed files:" >&2
  echo "$VITEST_OUTPUT" >&2
  exit 2
fi

exit 0
```

**Project-specific extensions:** If the project has domain-specific smoke tests (e.g., RAG agent tests, API health checks), append them after the generic checks. Use `git diff --name-only HEAD` to scope them to relevant directories.

After writing, run: `chmod +x .claude/hooks/quality-gate.sh`

Add the PostToolUse hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/quality-gate.sh"
          }
        ]
      }
    ]
  }
}
```

Merge into existing settings — do not overwrite.

### 6. `.gitignore` additions

Append these lines if not already present:

```
.claude/.tdd-active
.claude/.tdd-skipped
.claude/.lfg-active
.claude/.ralph-checked
.claude/.review-stamped
.claude/.fix-findings-active
```

`.claude/.lfg-active` is the third classification marker the hook's first clause accepts, created by `/lfg` and removed by `/execute` Step 6 alongside the two `.tdd-*` markers. It is reserved here rather than created: `/init-pipeline` scaffolds the gate, never a classification.

`.claude/.ralph-checked` is reserved here but created by `/setup-ralph-loop`, which is auto-invoked by `/execute` when a multi-slice task needs AFK bounds or may be run manually. `/init-pipeline` does not create the marker itself.

`.claude/.review-stamped` and `.claude/.fix-findings-active` are the post-review edit lock's two flags, also reserved here rather than created: `/pre-merge` Phase 4 writes the first beside the review-currency stamp and `/closeout` removes it at merge; `/fix-findings` writes the second when it loads and removes it when it reports. Both are transient, and a committed one would hold the lock open or shut across every future branch.

### 7. Worktree provisioning mode (optional)

`/execute` Step 0 and `/closeout` consult an optional `.claude/settings.json` key, `worktree.provisioning`, to decide whether the *pipeline* owns worktree provisioning and teardown or whether the *host* environment does. It mirrors the existing `research.storage` precedent — a single, in-repo, authoritative representation of an environment fact (Hunt/Thomas, DRY) rather than env-sniffing scattered across skills.

- `"auto"` (default when the key is absent) — `/execute` stands down if a host env var describes the current tree (the block below) or the current tree is not the repo's primary working tree; otherwise it provisions via worktrunk or plain git.
- `"host"` — isolation is always host-owned. `/execute` works in place; `/closeout` merges but cedes worktree teardown and branch pruning to the host.
- `"pipeline"` — the pipeline always provisions and tears down (the pre-host behavior).

```json
{
  "worktree": {
    "provisioning": "host"
  }
}
```

**Do not scaffold this key — leave it unset.** Whether a tree is host-provisioned is a fact about the machine and the checkout, and `.claude/settings.json` is committed: a `"host"` written from one Conductor workspace travels to every other clone, including the maintainer's own plain checkout and other contributors', where `/execute` would then stand down permanently and `/closeout` would cede teardown to a host that is not there. `auto` re-derives the answer on every run from the tree it is standing in:

```bash
# host-signal: does a host env var describe THIS tree, not just this shell?
host_owned=no
top=$(cd "$(git rev-parse --show-toplevel)" && pwd -P)
if [ -n "${CONDUCTOR_WORKSPACE_PATH:-}" ]; then
  ws=$(cd "$CONDUCTOR_WORKSPACE_PATH" 2>/dev/null && pwd -P) || ws=
  if [ -n "$ws" ]; then
    case "$top/" in "$ws"/*) host_owned=yes ;; esac
  fi
fi
if [ -n "${CODESPACES:-}" ] || [ -n "${REMOTE_CONTAINERS:-}" ]; then host_owned=yes; fi
echo "host_owned=$host_owned"
```

The bare presence of a host env var does not answer the question: `CONDUCTOR_WORKSPACE_PATH` is inherited by any shell started under Conductor and can name a workspace of a different repository entirely, so it counts only when it contains the current toplevel. `"host"` and `"pipeline"` remain for a user who sets them by hand, knowing every clone of the repo shares the answer.

## Verification

Before considering setup complete, check — against the sections § 2's per-path rule actually sent this run through, not against all seven. A Path C re-scaffold produces § 2's hook body, § 3's merge and § 6's append and nothing else, so the pre-commit and quality-gate items below belong to the install that already ran and are not this run's to satisfy:

- [ ] `.claude/hooks/enforce-classification.sh` exists and is executable
- [ ] Hook's `IMPL_PATTERNS` array matches the project's implementation surface: on § 2's Path A or B, the default list or the customized answer confirmed during this install; on Path C, byte-identical to the array in the hook that was already there
- [ ] `.claude/hooks/block-dangerous-git.sh` exists and is executable
- [ ] `.claude/settings.json` has both PreToolUse hooks configured
- [ ] If quality gate accepted: `.claude/hooks/quality-gate.sh` exists, is executable, and PostToolUse hook is in settings
- [ ] Hook manager config exists (e.g. `lefthook.yml`)
- [ ] Pre-commit hooks run successfully
- [ ] `.gitignore` has marker entries
- [ ] `.claude/settings.json` has no `worktree.provisioning` key written by this run (`auto`), whether or not a host env var is set
- [ ] No existing project settings were overwritten

## Handoff

- **Expected input:** any project that will use `/execute`
- **Produces:** complete enforcement infrastructure — Claude Code hooks, git guardrails, pre-commit hooks using detected or user-confirmed tools
- **Auto-invoked by:** `/execute` Step 0 when `.claude/hooks/enforce-classification.sh` is missing, or when it exists but does not read every term in that gate's `GATE_TERMS` — a pre-lock or pre-marker install, re-scaffolded per § 2
- **Invokes:** `/git-guardrails-claude-code` (project scope), `/setup-pre-commit`
- **Supports downstream:** `/tdd` (marker creation), `/execute` (marker cleanup); reserves `.claude/.ralph-checked` for `/setup-ralph-loop`, which creates the marker itself (auto-invoked by `/execute` for multi-slice work, or run manually); reserves `.claude/.review-stamped` and `.claude/.fix-findings-active` for the post-review edit lock, written by `/pre-merge` Phase 4 and `/fix-findings` respectively
