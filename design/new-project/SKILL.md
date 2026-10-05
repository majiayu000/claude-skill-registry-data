---
name: new-project
description: Full project bootstrap - interviews the developer (name, description, stack, components), then scaffolds directory structure, CLAUDE.md, config files, hooks, skills, and first commit.
user_invocable: true
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
---

# New Project Bootstrap

<!-- Mirrors AGENT.md in the agent-starter repo. If guides change, update this skill to match. -->

Use when starting a new project from scratch. Scaffolds a complete AI-friendly project following the agent-starter patterns: feature-based directory structure, CLAUDE.md with memory taxonomy, config files, optional hooks and skills, first commit.

For existing projects, use `/adopt-project` instead.

## Phase 0: Detect what's already installed

Hooks and skills install **system-wide** under `~/.claude/`, so they're shared
across every project. Detect them first and never ask about components that are
already present. Run:

```bash
# Hooks: install.sh stamps this file with the installed version
HOOKS_VER=$( [ -f ~/.claude/hooks/.agent-starter-version ] && cat ~/.claude/hooks/.agent-starter-version || echo "" )
HOOKS_N=$( ls ~/.claude/hooks/*.sh 2>/dev/null | wc -l | tr -d ' ' )

# Skills: the starter skills this bootstrap installs
for s in commit commit-push-pr simplify remember dream new-project adopt-project reflect; do
  [ -d ~/.claude/skills/$s ] && echo "skill:$s present" || echo "skill:$s missing"
done
echo "hooks: version ${HOOKS_VER:-none}, $HOOKS_N scripts"
```

Interpret the output:
- **Hooks installed** if `.agent-starter-version` exists (or hook scripts are
  found). Record the stamped version.
- **Skills installed** per directory listed as `present`.

Carry this into the interview and scaffold: only ask about, and only install,
what's **missing**. If a stamped hooks version is present but older than the
repo `VERSION` (checked in Phase 1 once you have the repo path), note that an
update is available and offer to re-run `install.sh` (idempotent) - don't force it.

## Phase 1: Interview

Ask these questions **one at a time** before taking any action:

1. **Project name** - what is the name of the project?
2. **Description** - one sentence describing what it does.
3. **Tech stack** - language, framework, package manager (e.g. "TypeScript, Next.js, pnpm").
   - **Tailwind design-system lint** - ask this follow-up only when the stack is
     TypeScript/JavaScript with a UI framework (React, Next.js, Remix, Vite +
     React): "Does the project use Tailwind v4, and should I add `@shadcn/lint`
     (blocks raw palette colors, arbitrary values, inline styles, unknown
     classes, and restyling design-system components via `className`)? yes/no".
     Record the answer; it drives the optional block in Phase 2 step 3. Skip
     the question for non-UI stacks.
4. **Optional components** - ask **only about what Phase 0 reported as missing**.
   If hooks and all skills are already installed, skip this question entirely -
   state what was detected ("Hooks v0.4.4 and all 8 skills already installed
   system-wide, skipping") and move on. Otherwise offer the missing set:
   - Hooks (auto-enforce file size limits, lint-on-save, silent-error and dangerous-command blocking, codebase health checks at `~/.claude/hooks/`)
   - Skills (commit, commit-push-pr, simplify, remember, dream, new-project, adopt-project, reflect at `~/.claude/skills/`)
   - Both
   - Neither
5. **Repo path** - what is the local path to the agent-starter repo? (e.g. `~/code/agent-starter`). Always required: the CLAUDE.md template, foundation templates, and lint configs are all copied from the repo. (Hooks and skills also install from here when selected and not already present.)

Do not proceed past this step until you have all answers.

## Phase 2: Scaffold

Execute these steps in order.

### 1. Create directory structure

```bash
mkdir -p <project-name>/src/features
mkdir -p <project-name>/src/services
mkdir -p <project-name>/src/utils
mkdir -p <project-name>/src/types
mkdir -p <project-name>/src/constants
mkdir -p <project-name>/src/schemas
mkdir -p <project-name>/src/entrypoints
mkdir -p <project-name>/src/migrations
mkdir -p <project-name>/tests
mkdir -p <project-name>/docs
mkdir -p <project-name>/scripts
```

Design principle: organize by feature, not by technical layer. Each feature gets its own directory under `src/features/` with ALL related files (implementation, types, constants, validation, tests). Keep files under 200 lines each. Shared type definitions go in `src/types/` to break import cycles. Named constants go in `src/constants/` (no magic strings anywhere).

### 2. Generate CLAUDE.md

Copy the canonical template - do **not** inline or hand-write it, so it never
drifts from `templates/CLAUDE.md` (which carries the Memory System, Git Safety,
Implementation Notes, and Self-improvement loop sections):

```bash
cp <repo-path>/templates/CLAUDE.md <project-name>/CLAUDE.md
```

Then fill in the `## Project-Specific Instructions` section at the bottom:

```
**Project:** <project-name>
**Description:** <project-description>
```

### 3. Create config files

**`.gitignore`** at `<project-name>/.gitignore`:
```
node_modules/
dist/
.env
*.log
.DS_Store
.cache/
coverage/
CLAUDE.local.md
```

**`.env.example`** at `<project-name>/.env.example`:
```
# Required environment variables - copy to .env and fill in values
```

**`README.md`** at `<project-name>/README.md`:
```markdown
# <project-name>

<project-description>

## Getting Started

<!-- Add setup instructions here -->
```

**`CLAUDE.local.md`** at `<project-name>/CLAUDE.local.md` (gitignored above - personal, machine-local instructions that never get committed):
```markdown
# Personal Instructions (local only)

<!-- Your personal preferences for this project. Not committed. -->
```

**`.claude/rules/`** - modular instruction files the agent loads alongside CLAUDE.md. Create the directory and the apply-on-touch pattern index, which is the same file `/adopt-project` writes (Tier 4):

```bash
mkdir -p <project-name>/.claude/rules
```

Write `<project-name>/.claude/rules/starter-patterns.md`:

```markdown
# Starter patterns - apply on touch

Apply these when already editing the relevant code. Never as a bulk refactor.

- Editing a file over 300 lines -> split per the file-size hook's suggestions
  (types / constants / validation / utils).
- Touching a `throw` / `raise` site -> route it through the error registry
  (`guides/error-id-registry.md`).
- Changing a fallible function's signature -> consider returning a Result
  (`guides/discriminated-union-results.md`).
- Touching an env read -> move it behind the env boundary
  (`guides/zod-at-the-boundary.md`).
- Adding a long-running operation -> thread cancellation through it
  (`guides/abort-signal-threading.md`).
- Adding a new tool -> use the directory-per-tool layout
  (`guides/tool-authoring-pattern.md`).
```

Optionally also create topic stubs (`testing.md`, `git-workflow.md`, `code-style.md`, `security.md`) per `templates/NEW_PROJECT_PROMPT.md` - offer these but don't force them.

**Lint configs** - if the stack is TypeScript/JavaScript:

```bash
cp <repo-path>/templates/biome.jsonc <project-name>/biome.jsonc
cp <repo-path>/templates/eslint.config.mjs <project-name>/eslint.config.mjs
cd <project-name> && npm i -D @biomejs/biome eslint typescript-eslint eslint-plugin-import \
  eslint-plugin-sonarjs eslint-plugin-security eslint-plugin-eslint-comments
```

**Tailwind design-system lint (opt-in, only if the Phase 1 follow-up was yes):**

```bash
cp <repo-path>/templates/eslint.shadcn.mjs <project-name>/eslint.shadcn.mjs
cd <project-name> && npm i -D @shadcn/lint
```

Then wire the fragment into `eslint.config.mjs`: add
`import shadcnRules from './eslint.shadcn.mjs'` next to the other imports and
`...shadcnRules,` as the last entry of the `tseslint.config(...)` call. Set
`settings.shadcn.ui` in the fragment to the project's component import prefix
(`@/components/ui` is the shadcn default) and the `**/components/ui/**`
override to the directory that owns the components. `@shadcn/lint` needs
ESLint 9.30+ and Tailwind v4; it finds the theme without a `components.json`,
so shadcn/ui itself is not required.

If the stack is Python:

```bash
cp <repo-path>/templates/ruff.toml <project-name>/ruff.toml
cp <repo-path>/templates/pyrightconfig.json <project-name>/pyrightconfig.json
cd <project-name> && uv add --dev ruff pyright   # or: python -m pip install ruff pyright
```

See `guides/lint-rules-for-ai.md` for what the rules catch. Skip for other stacks.

### 4. Copy foundation templates (TypeScript/JavaScript or Python)

Reference: `guides/error-id-registry.md`, `guides/zod-at-the-boundary.md`,
`guides/large-codebase-best-practices.md`

These are the "create from day one" foundation files (see
`templates/NEW_PROJECT_PROMPT.md` -> Foundation Files): a centralized env
boundary, a numbered error registry, and an output truncator. Copy them for the
matching stack and adapt import paths to the layout.

If the stack is TypeScript/JavaScript:

```bash
cp <repo-path>/templates/env.ts <project-name>/src/utils/env.ts
cp <repo-path>/templates/errorIds.ts <project-name>/src/constants/errorIds.ts
cp <repo-path>/templates/truncate-for-context.ts <project-name>/src/utils/truncate-for-context.ts
```

If the stack is Python:

```bash
cp <repo-path>/templates/env.py <project-name>/src/utils/env.py
cp <repo-path>/templates/error_ids.py <project-name>/src/constants/error_ids.py
cp <repo-path>/templates/truncate_for_context.py <project-name>/src/utils/truncate_for_context.py
```

Skip for other stacks (Rust, Go, etc.) - point the developer at the guides above
to build equivalents.

### 5. Install hooks (if selected and not already installed)

Skip if Phase 0 detected hooks already installed **and** the stamped version
matches the repo `VERSION` - they're system-wide, so they already cover this
project. If installed but stale, offer to update by re-running the installer
(it's idempotent). Otherwise run it now.

The installer copies the hooks (and `lib/`) to `~/.claude/hooks/`, stamps the
installed version, and merges the hook wiring into `~/.claude/settings.json`
with jq. Existing entries are preserved and re-running never duplicates
anything - do not hand-edit the JSON:

```bash
bash <repo-path>/install.sh
```

Hook behavior (wired by default):
- `check-file-size.sh` - runs after every Write/Edit. Blocks (exit 2) files over 300 lines; warns over 200 lines. Skips `.md`, `.json`, `.yaml`. Override per project with `.harness/file-size.conf`.
- `lint-on-edit.sh` - Biome + ESLint on save for JS/TS; ruff check + format for Python.
- `check-silent-errors.sh` - blocks writes that introduce swallowed exceptions.
- `block-dangerous-commands.sh` - blocks force-push, `git reset --hard`, recursive rm on `/`/`~`, before they run.
- `rm-scope-guard.py` - blocks any `rm` whose targets escape the working directory, and allows the rest. Complements the hook above, which only catches the catastrophic roots.
- `check-codebase-health.sh` - runs at session start. Reports files over 500 lines that need splitting. Silent when healthy.
- `worktree-session-prompt.sh` - at session start, says whether this is the shared main checkout or a linked worktree, and has Claude ask before editing the shared one. Two agents in one checkout is how a branch flip silently reverts a peer's edits.
- `worktree-exit-offer.sh` - on Stop, offers to leave the worktree once it is clean and fully pushed, which is the one moment exiting loses nothing.
- `suggest-loop-improvements.sh` - when you run `/loop`, proposes 2-3 tighter drop-in rewrites (explicit success criteria, stop condition, scope, verification) and lets you pick one via an interactive menu. Scoped to `/loop` only (client-side commands like `/goal` run before Claude's turn, so they can't be gated).

Requires `jq` and `python3`.

Optional: `--with-read-guard` also wires `track-reads.sh` + `require-read-before-edit.sh`. Recent Claude Code versions enforce read-before-edit natively, so only add it for older versions. `--with-comment-guard` blocks edits that add comments or docstrings; `--with-em-dash-guard` blocks em dashes in `.md`/`.mdx`/`.markdown`. Both are house style rather than correctness rules, so ask before wiring them.

### 6. Install skills (if selected and not already installed)

Copy **only the skills Phase 0 reported as `missing`**. Skills are system-wide,
so any already present already cover this project - leave them as-is rather than
overwriting (a blind `cp -r` would clobber local edits). The guard below copies
each skill only when its directory is absent:

```bash
mkdir -p ~/.claude/skills
for s in commit commit-push-pr simplify remember dream new-project adopt-project reflect; do
  [ -d ~/.claude/skills/$s ] || cp -r <repo-path>/skills/$s ~/.claude/skills/
done
```

To deliberately refresh an already-installed skill (e.g. after pulling a newer
repo), copy that one explicitly: `cp -r <repo-path>/skills/<name> ~/.claude/skills/`.

Installed skills:
- `/commit` - single well-crafted git commit with "why not what" message
- `/commit-push-pr` - full workflow: branch, commit, push, create/update PR
- `/simplify` - 3 parallel agents review your diff for reuse, quality, efficiency
- `/remember` - review auto-memory and promote to CLAUDE.md or CLAUDE.local.md
- `/dream` - memory consolidation: merge, prune, re-index memory files
- `/new-project` - this skill (bootstrap a new project)
- `/adopt-project` - apply these patterns to an existing codebase
- `/reflect` - read ledger, cluster recurring mistakes, propose improvements

### 7. Initialize the self-improvement ledger

```bash
mkdir -p <project-name>/.harness/reflections
touch <project-name>/.harness/reflections/.gitkeep
echo '.harness/ledger.jsonl' >> <project-name>/.gitignore
```

The enforcement hooks use `hooks/lib/log-event.sh` to append structured events to
`.harness/ledger.jsonl` as the agent works. Run `/reflect` periodically: it reads
the ledger via `harness-ledger-stats.sh`, clusters recurring mistakes, and proposes
rule / threshold / ADR changes for your approval. See `templates/CLAUDE.md` →
"Self-improvement loop".

### 8. Initialize git and first commit

```bash
cd <project-name>
git init
git add .
git commit -m "$(cat <<'EOF'
Initial project scaffold

Bootstrapped using agent-starter patterns.
EOF
)"
```

## Phase 3: Verify

Confirm each item before reporting done:

- [ ] Project directory with feature-based structure (`src/features`, `src/services`, `src/utils`, `src/types`, `src/constants`, `src/schemas`, `src/entrypoints`, `src/migrations`, `tests/`, `docs/`, `scripts/`)
- [ ] `CLAUDE.md` copied from `templates/CLAUDE.md` (not inlined) with project name and description filled in
- [ ] `.gitignore`, `.env.example`, `README.md`, and `CLAUDE.local.md` present (`CLAUDE.local.md` gitignored)
- [ ] `.claude/rules/starter-patterns.md` written
- [ ] Lint configs copied + deps installed - `biome.jsonc` + `eslint.config.mjs` (TS/JS) or `ruff.toml` + `pyrightconfig.json` (Python); skipped for other stacks
- [ ] `eslint.shadcn.mjs` copied, `@shadcn/lint` installed, and the fragment spread into `eslint.config.mjs` - only if the Tailwind follow-up was yes
- [ ] Foundation templates copied - env boundary + error registry + truncator for the stack (TS or Python); skipped for other stacks
- [ ] Hooks present in `~/.claude/hooks/` and configured in `settings.json` (installed now if selected, or already detected in Phase 0)
- [ ] Skills present in `~/.claude/skills/` (missing ones installed if selected; already-present ones left as-is)
- [ ] `.harness/reflections/` created and `.harness/ledger.jsonl` added to `.gitignore`
- [ ] `reflect` skill present at `~/.claude/skills/reflect`
- [ ] Initial git commit created

## Allowed Tools

Read, Write, Edit, Bash, Glob
