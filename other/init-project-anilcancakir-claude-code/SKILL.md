---
name: init-project
description: "Set up or audit a project's Claude Code files, project documents, permissions, lint hook and language server from one approved proposal."
argument-hint: "[path] [--max-depth=N] [--dry-run] [--propose-only] [--no-local] [--no-docs] [--force-overwrite] [--no-oracle]"
effort: medium
disable-model-invocation: true
---

# /ac:init-project

Investigates a project, then writes an optimized CLAUDE.md, optional CLAUDE.local.md, up to five path-scoped `.claude/rules/*.md` files, permission rules, the project settings from `${CLAUDE_PLUGIN_ROOT}/skills/claude-md-rules-creator/references/settings-wiring.md` that earn their keep, a lint or format hook that provably fires, and a language server that provably answers. Everything is one proposal approved once before anything is written, and the drafts pass one `ac:oracle` review. On a project that already has instruction files it audits them and the auto-memory line by line, keeps what the user decided and the code cannot show, and proposes cuts, moves, merges and memory cleanup as decisions. It also creates, repairs and brings up to date the project documents `PROJECT.md`, `ARCHITECTURE.md` and `DESIGN.md`, each through its own writer skill and only where that document's bar is met. Drives `ac:claude-md-rules-creator` as the writing playbook for the instruction files.

Request: $ARGUMENTS

Do NOT call `EnterPlanMode` or `ExitPlanMode`; this command uses no plan mode.

## Phase 0: Identity, Arguments, Primer, and Existing-File Branch

You are the `/ac:init-project` orchestrator, running on the main thread; the four discovery agents in Phase 1 and the Phase 3e reviewer are subagents you spawn.

**CAN**: Use `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Bash`, `LSP`, `AskUserQuestion`. Spawn `Agent` with `subagent_type: "ac:explore"` for codebase fan-out, and one `ac:oracle` at Phase 3e to review the drafts. Invoke the `ac:claude-md-rules-creator` skill at Phase 3 entry, and at 3h the writer skill of each project document the proposal approved (`ac:project-md-writer`, `ac:architecture-md-writer`, `ac:design-md-writer`). Write `<target>.proposed` sidecar files when an existing target would be overwritten. Write one hook script under `.claude/hooks/` and merge its entry, plus the approved permission rules and the other Phase 4 settings keys, into the target project's `.claude/settings.json` or `.claude/settings.local.json` as the 2d proposal named (Phase 4). Merge one `enabledPlugins` key for a language server into the file the 2d proposal named (Phase 5).

**CANNOT**: Spawn `ac:librarian`, or `ac:oracle` anywhere but 3e. `ac:explore` cannot spawn anything; every discovery agent returns to this orchestrator before the next step. Author CLAUDE.md prose without first invoking `ac:claude-md-rules-creator`. Write or change `PROJECT.md`, `ARCHITECTURE.md` or `DESIGN.md` without first invoking its writer skill, replace an existing one wholesale, or pick a palette or typeface for a `DESIGN.md` (a theme file or a chosen `ac:design-director` direction supplies it, otherwise the document is skipped). Edit files outside the target project directory, with three exceptions: `~/.claude/<PROJECT_SLUG>-instructions.md` in 3c for sibling worktrees, the 3e scratch directory under `${TMPDIR:-/tmp}`, and the project's auto-memory directory in 3g, only for changes 2d approved. Delete or cut a fact from an existing file without the user's approval in 2e. The `enabledPlugins` key goes to `~/.claude/settings.json` only when the user moved it there through "Other" in 2d. Interview the user about MCP servers or about settings keys generally, or write any settings key outside the menu in `${CLAUDE_PLUGIN_ROOT}/skills/claude-md-rules-creator/references/settings-wiring.md`: `permissions.deny`, `permissions.allow`, `permissions.ask`, one `hooks.PostToolUse` entry, `enabledPlugins` for a language server, `worktree.symlinkDirectories` and `claudeMdExcludes`, each only when 2d named it. Never write the keys that file lists under "Never from a setup command": `permissions.defaultMode` in particular (a mode is the user's choice), and the model and effort keys, which override each person's own pick. Write anything to `.claude/settings.json` that the approved 2d proposal did not place there. Repair a pre-existing malformation in a settings file this command did not create.

**MUST**: Apply argument precedence: when both `--dry-run` and `--force-overwrite` are set, `--dry-run` wins and no `Write` or `Edit` fires. Spawn the four Phase 1 discovery agents in a single parallel block. Unless `--no-docs`, settle the project documents in 2f and list them in the 2d proposal. Show the 2d proposal and take its approval before the first `Write`, `Edit` or settings merge. Invoke the writing skill exactly once at the very start of Phase 3. Run the skill's Pre-flight checklist before every `Write` (new file) or `Edit` (existing file), except the one-line rule repairs 2d approved as they are. Cap the root `CLAUDE.md` and rule files within the line budgets stated in Phase 3. Take a timestamped backup before every settings merge, and restore it when a post-write check fails.

### 0a. Parse arguments

1. Default `PATH_ARG` to the current working directory when no positional path is given; otherwise treat the first non-flag token as `PATH_ARG`. Resolve to an absolute path before any tool call.
2. `--max-depth=N`: parse the integer after `=`. Default `MAX_DEPTH=2`. Reject negative values; treat `0` as "root only". It bounds how deep a path-scoped rule's glob may be rooted in Phase 2c.
3. `--dry-run`: set `DRY_RUN=true` if present.
4. `--no-local`: set `WRITE_LOCAL=false` if present; otherwise `WRITE_LOCAL=true`.
5. `--force-overwrite`: set `FORCE_OVERWRITE=true` if present.
6. `--no-oracle`: set `REVIEW=false` if present; otherwise `REVIEW=true`. It only skips the 3e review.
7. `--no-docs`: set `WRITE_DOCS=false` if present; otherwise `WRITE_DOCS=true`. It skips 2f and 3h, so `PROJECT.md`, `ARCHITECTURE.md` and `DESIGN.md` are neither inventoried for action nor touched.
8. `--propose-only`: set `PROPOSE_ONLY=true` if present. Nothing in the working tree or the memory directory changes: every instruction-file result goes to `<PATH_ARG>/.ac/init/proposed/<path relative to PATH_ARG>`, the memory plan to `.ac/init/proposed/memory-cleanup.md`, the settings changes to `.ac/init/proposed/settings.md`, with no Apply question. The 2d proposal warns that the proposed files will show in diffs when `.ac/` is not gitignored.
9. Precedence rule: if `DRY_RUN` and `FORCE_OVERWRITE` are both true, set `FORCE_OVERWRITE=false` for the rest of the run. `PROPOSE_ONLY` also sets `FORCE_OVERWRITE=false`. `--dry-run` always wins; it prints intended writes and runs no command with a side effect.
10. Derive `PROJECT_SLUG` from the basename of `PATH_ARG`: lowercase, replace runs of non-alphanumeric characters with a single hyphen, strip leading and trailing hyphens. Used in user-facing messages and the sibling-worktree stub filename.

### 0b. Primer, then the existing-file branch

Print a short plain-language primer before the first question, in five lines: `CLAUDE.md` is read at the start of every session in this project, so it costs tokens on every request and earns them back only where Claude would otherwise get something wrong; `CLAUDE.local.md` is the same file for you alone and is gitignored; `.claude/rules/<topic>.md` with `paths:` loads only when Claude reads a matching file; a hook is the only one of them that runs code, and a permission rule in `.claude/settings.json` stops Claude from doing something without any code. Then say the run will ask a few questions one at a time, show one proposal of everything it would write, and write nothing until that proposal is approved; any answer can be "skip".

Then take the inventory of what already exists, with `Bash` only (`test -f`, `wc -lc`, `ls`), never `Read` on a path that may be missing:

- instruction files: `<PATH_ARG>/CLAUDE.md`, `<PATH_ARG>/.claude/CLAUDE.md`, `<PATH_ARG>/CLAUDE.local.md`, `AGENTS.md`, every `CLAUDE.md` and `CLAUDE.local.md` below the root, tracked, untracked or gitignored (`find <PATH_ARG> \( -name node_modules -o -name vendor -o -name .git -o -name references \) -prune -o \( -name CLAUDE.md -o -name CLAUDE.local.md \) -print`), and every `.claude/rules/**/*.md`;
- settings: `.claude/settings.json`, `.claude/settings.local.json`;
- project documents (skip on `--no-docs`): `PROJECT.md`, `ARCHITECTURE.md` and `DESIGN.md` at the root and under `docs/`, plus `.planning/PROJECT.md` and `docs/architecture*`. For each `DESIGN.md`, `rg -q '^colors:'` tells its kind: a hit means YAML design tokens (the visual-identity file; a `primary` colour is required there), none means the old architecture home. Record them as `DOCS` with lines and bytes. They do not count toward `MODE`, which is decided by the instruction files alone; 2f settles them.
- auto-memory: when a settings file sets `autoMemoryDirectory`, that directory. Otherwise `MEMORY_DIR = ~/.claude/projects/<key>/memory`, where `<key>` is the absolute path of the main worktree's root (`git -C <PATH_ARG> rev-parse --path-format=absolute --git-common-dir`, minus its trailing `/.git`; `PATH_ARG` itself outside git) with every character that is not a letter or a digit replaced by `-` (names over 200 characters are hashed, so for a very long path match the directory by its prefix with `ls ~/.claude/projects`). When no such directory exists, say so in the inventory rather than skipping the memory silently.

Record each with its line and byte count as `EXISTING`, and its total as `EXISTING_BYTES`. When no instruction file exists, set `MODE=fresh` and ask nothing. Otherwise print the inventory as a short table (file, lines, bytes, `paths:` or not, and the per-file budget from the skill's principle 1 it is over) and ask before anything else:

```
AskUserQuestion({
  header: "Existing?",
  question: "This project already has <N> instruction files (<total lines> lines, <total KB> KB)<, and <M> auto-memory files>. How should this run treat them?",
  options: [
    {label: "Audit and slim", description: "Read every file and the auto-memory line by line, keep what you decided and the code cannot show, and propose cuts, moves into scoped rules, merges and memory cleanup as decisions you approve. Nothing is removed without your answer."},
    {label: "Leave them", description: "Do not touch existing instruction files or memory. Missing files, rule repairs, permissions, the hook and the language server still run."},
    {label: "Start fresh", description: "Draft a new setup from the codebase; every existing file goes through the .proposed gate in 3f before anything is overwritten."}
  ]
})
```

Record the answer as `MODE` (`audit`, `leave` or `fresh`). On `leave`, Phases 1c, 2e and 3g are skipped, and 3b is skipped when a root `CLAUDE.md` exists (a project with only `AGENTS.md` still gets one drafted). On `audit`, Phase 1c audits every file in `EXISTING`, 2e settles each proposed change with the user, and 3b applies the approved changes as `Edit`s against the existing files rather than a fresh draft.

### 0c. Preference queue

Open one typed record and carry it through every later phase. Every interview answer writes exactly one field; a skipped question leaves the field `null` and the writing phase omits that section rather than inventing content.

```
PREFS = {
  mode: "audit" | "leave" | "fresh",
  scope: "project" | "personal" | "both",
  commands: {dev, build, test, lint, typecheck},
  golden_rules: [],          // at most 5 strings, each grep- or review-checkable
  testing: {command, single, quirks},
  offlimits: [],
  git: {branch_pattern, pr_rule},
  hook: {kind, tools, target},        // kind: "lint" | "format" | "format+lint"; tools baked into the script
  permissions: {deny: [], deny_target, allow: [], allow_target},
  lsp: {plugin, marketplace},
  docs: {project, architecture, design},  // each: {action: "write" | "audit-fix" | "move" | "leave" | "skip", evidence}
  skill_candidates: [],                // procedures from 2c and 1c, reported only
  audit: []                            // MODE=audit: one entry per 1c finding with its 2e decision
}
```

### 0d. Gitignore guard for `CLAUDE.local.md`

Run only when `WRITE_LOCAL=true`, or when a `CLAUDE.local.md` already exists at the target root and `WRITE_LOCAL=false`. In `PATH_ARG`:

1. If `git rev-parse --git-dir` exits non-zero, skip the guard.
2. Otherwise run `git check-ignore -q CLAUDE.local.md` and set `NEEDS_IGNORE=true` when it exits 1 (not ignored yet), `false` when it exits 0. Append nothing here: the line is a 2d Files bullet, and 3f appends it with the other approved writes, printing "Added CLAUDE.local.md to .gitignore so personal instructions stay local."

Under `--dry-run` the 2d proposal shows the line that would be appended.

## Phase 1: Codebase Discovery

### 1a. Worktree disambiguation

Run one `Bash` call: `git -C <PATH_ARG> worktree list`. When the output contains more than one worktree row, ask the user to disambiguate via `AskUserQuestion` (header "Worktrees?", question "Multiple git worktrees detected. Where do your sibling worktrees live relative to the main repo?", options "Nested inside main repo (e.g., `.claude/worktrees/<name>/`)", "Sibling or external (e.g., `../<repo>-feature/`)", "Single worktree, ignore"). The choice routes `CLAUDE.local.md` placement: nested worktrees inherit the main repo's `CLAUDE.local.md` via the upward walk; sibling worktrees need a `~/.claude/<PROJECT_SLUG>-instructions.md` file and a `CLAUDE.local.md` stub per worktree that imports it.

Skip the question when only one worktree row is reported.

### 1b. Four parallel `ac:explore` agents

Spawn exactly four discovery agents in a single response, targeting `PATH_ARG` (not this repository), together with the 1c audit agents when `MODE=audit`. Each brief follows the "predict the standard answer first, report only the deviations" style and carries its own `DEPTH` and `BUDGET` line.

```
Agent({
  subagent_type: "ac:explore",
  run_in_background: true,
  effort: "low",
  prompt: "Discovery agent 1 of 4 for `/ac:init-project`. Target project: <PATH_ARG>. Predict the standard manifest and build setup for this kind of project, then report only deviations.\n\nCONTEXT: We are authoring CLAUDE.md for this project. Standing instructions only need to capture what Claude cannot already infer from the manifest.\n\nGOAL: Decide which build, test, lint, type-check, and run commands belong in CLAUDE.md, plus which linter and formatter binaries the Phase 4 hook could call.\n\nDEPTH: shallow. The manifests answer this directly; do not read application source.\nBUDGET: one pass over the root plus any workspace package manifests, then report.\n\nDOWNSTREAM: Phase 3 will feed these findings to `ac:claude-md-rules-creator`. Standard commands (`pnpm test`, `cargo test`, `pytest`) get dropped; non-standard or wrapped commands stay.\n\nREQUEST: Read every manifest, lockfile, Makefile, justfile, and CI config in the project root. Predict the conventional command set for the detected stack in one line. List the deviations as `file:line` citations: custom scripts, wrapped commands, required pre-steps, environment bootstrap. Name the linter and the formatter, each with its on-disk path (`node_modules/.bin/`, `vendor/bin/`, `.venv/bin/`), when installed. Skip standard commands the model already knows."
})

Agent({
  subagent_type: "ac:explore",
  run_in_background: true,
  effort: "medium",
  prompt: "Discovery agent 2 of 4 for `/ac:init-project`. Target project: <PATH_ARG>. Predict the standard language and framework set, then report only deviations.\n\nCONTEXT: We are deciding which framework facts deserve a CLAUDE.md line. Language defaults the model already knows do not.\n\nGOAL: Identify languages, framework versions, runtimes, and package managers in active use, plus the file-extension histogram Phase 5 matches against language-server manifests.\n\nDEPTH: medium. Version pins and config files, plus the top of a representative source file per language.\nBUDGET: two passes, the second only to resolve a version that the first pass left ambiguous.\n\nDOWNSTREAM: Phase 3 writes the stack paragraph from the deviations; Phase 5 matches the extension histogram against installed language-server plugins.\n\nREQUEST: Read manifest version pins, framework config files (next.config, vite.config, tsconfig, pyproject, build.gradle, etc.), and the top of representative source files. Predict the conventional stack profile in one line. List the deviations as `file:line` citations: pinned major versions that gate features, custom resolver setups, framework-specific conventions that diverge from defaults. End with a count of tracked files per extension, from `git ls-files`, for the top five extensions."
})

Agent({
  subagent_type: "ac:explore",
  run_in_background: true,
  effort: "high",
  prompt: "Discovery agent 3 of 4 for `/ac:init-project`. Target project: <PATH_ARG>. Predict the standard code style and report only deviations.\n\nCONTEXT: We are picking the style rules CLAUDE.md needs to encode. Defaults the linter and formatter already enforce do not belong in CLAUDE.md.\n\nGOAL: Identify formatter, linter, type-checker configuration which of them formats in place (prettier, biome, ruff format, black, gofmt, rustfmt, pint, or a unified `format` script) and which only reports, decided from the config and the manifest scripts, never by running a tool (a `--version` check at most: a formatter run to see what it does rewrites the files), plus any naming, layout, or testing conventions the team enforces by convention rather than by tool, and note for each whether it applies project-wide or only under one directory.\n\nDEPTH: deep. This is the angle that decides both the conventions section and every path-scoped rule, so it earns the widest read of the four.\nBUDGET: three passes, ending when a pass adds no convention the previous one missed.\n\nDOWNSTREAM: Phase 2c routes each convention you report to the root CLAUDE.md, to a hook, or to a path-scoped rule, so the scope note on each finding decides its destination.\n\nREQUEST: Read `.editorconfig`, `.prettierrc`, `.eslintrc*`, `biome.json`, `ruff.toml`, `pyproject.toml` tool tables, `.golangci.yml`, `phpstan.neon`, `pint.json`, plus 2 or 3 representative source files per detected language. Predict the conventional style profile in one line. List the deviations as `file:line` citations: rules the tooling does not catch, naming patterns, file layout conventions, test-file pairing rules. Mark each one `project-wide` or `only under <dir>`, and flag any whose violation would cost data, secrets, or a broken main branch."
})

Agent({
  subagent_type: "ac:explore",
  run_in_background: true,
  effort: "low",
  prompt: "Discovery agent 4 of 4 for `/ac:init-project`. Target project: <PATH_ARG>. Predict the standard agent-infra footprint and report only deviations.\n\nCONTEXT: We are deciding whether the new CLAUDE.md should import existing agent-tool instructions via `@path` rather than restate them.\n\nGOAL: Inventory every pre-existing agent-tool instruction surface in the project, any settings file this run would have to merge into, and the secret-shaped files a `permissions.deny` rule should cover.\n\nDEPTH: shallow. This is an inventory, not an analysis; one line of summary per file found is enough.\nBUDGET: one pass over the known paths, then report. A clean empty set is a useful answer; say so rather than widening the search.\n\nDOWNSTREAM: Phase 3 imports an `AGENTS.md` with `@AGENTS.md` rather than restating it, and migrates the other tools' rules into focused `.claude/rules/*.md` topics. Phase 4 needs to know whether a settings file already exists and whether it already carries hooks.\n\nREQUEST: Check for `AGENTS.md`, `.claude/AGENTS.md`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`, `.devin/rules/`, `.windsurf/rules/`, `.windsurfrules`, `.clinerules`, `.mcp.json`, existing `CLAUDE.md`, existing `.claude/rules/*.md`, existing `.claude/CLAUDE.md`, subdirectory `CLAUDE.md` files (`git ls-files '*CLAUDE.md'`), `.claude/skills/`, `.claude/settings.json`, `.claude/settings.local.json`, `.claude/hooks/`. For each, report path, line count, and a one-line summary. Flag every existing `.claude/rules/**/*.md` (rules are discovered recursively) that carries a `paths:` line but whose first bytes are not `---` (a comment, a title or a blank line above the frontmatter): Claude Code then ignores its `paths:` and loads it at every launch. For the two settings files, report whether `jq .` parses them, whether they already carry a `hooks.PostToolUse` entry, and the `permissions.allow` and `permissions.deny` rules they already hold. Also list, by path only and never with `Read`, `cat` or any other read of their contents (a hook denies the attempt), the secret-shaped files present in the project: `ls -a` of the root plus `git ls-files` and `git ls-files --others --exclude-standard` filtered to `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa*`, `credentials*.json`, `service-account*.json`, `config/master.key`, `auth.json`; mark `.env.example`, `.env.sample` and `.env.dist` as templates rather than secrets. Predict the empty set as the standard baseline; report every found surface as a deviation citing `file:line` for the most load-bearing block."
})
```

Each block also passes the Agent tool's `effort`, mapped from its `DEPTH` line: `shallow` is `"low"`, `medium` is `"medium"`, `deep` is `"high"`. Omit it when `CLAUDE_CODE_EFFORT_LEVEL` is set, and on a `haiku` that resolves to Haiku 4.5 (Bedrock, Vertex, Foundry), which takes none.

### 1c. Audit agents (`MODE=audit` only)

Split the instruction files in `EXISTING` into groups of about 120 KB, at most six groups, and give the root `CLAUDE.md` and `CLAUDE.local.md` to every group. Past six groups, audit the largest files first and name the rest as not audited in 2d. Spawn one `ac:explore` per group in the same message as the discovery agents, with `effort: "high"`.

The auto-memory gets its own agents, one per 30 topic files: start with one batched Bash call that prints every listed file's frontmatter (`head -n 8` over the list) and one `git ls-files` listing, then per file read the `description`, check every backticked path, command and symbol in the body with `git ls-files`, Grep or the manifest, and read the whole body only when those two cannot place it. Same classes; the destination for a project fact every session needs is the root CLAUDE.md or a rule.

The instruction-file brief:

```
Agent({
  subagent_type: "ac:explore",
  run_in_background: true,
  effort: "high",
  prompt: "Audit agent <i> of <n> for `/ac:init-project`. Target project: <PATH_ARG>.\n\nCONTEXT: These files are loaded into Claude Code sessions in this project and cost tokens on every request they load in. The user wants them as short as they can be without losing a decision only they could make. Root CLAUDE.md and unscoped rules load at every launch; a rule with `paths:` loads when a matching file is read or edited; auto-memory topic files load when a session opens them.\n\nGOAL: Classify every section (a heading and its body, or a bullet) of these files: <file list with line counts>.\n\nDEPTH: thorough. BUDGET: one read of each file, then one verification pass of the claims below.\n\nDOWNSTREAM: Each finding becomes a decision the user approves or rejects. A wrong CUT deletes the user's own rule, so mark it only with evidence.\n\nREQUEST: For each section return `file:start-end | class | evidence | proposed destination`. Classes: KEEP (a decision, constraint or trap the code does not show); MOVE (applies only to files under a path: propose the `.claude/rules/<topic>.md` and its `paths:` glob; or a multi-step procedure: propose a skill; or long reference material: propose a doc it points at); MERGE (the same fact exists in another file: cite both); DERIVABLE (restates what the manifest, the linter or formatter config, the language default or the code itself shows: cite where); OUTDATED (names a path, symbol, command, package or version that no longer exists or no longer applies: cite the `git ls-files`, Grep or manifest check that shows it); HISTORY (a dated narrative, an incident log, a changelog of the rule: the fact it teaches, if any, is a KEEP line). Verify every OUTDATED and DERIVABLE claim with a command before you write it; without evidence the class is KEEP. Also report, per file, its lines and bytes, whether a `paths:` frontmatter starts at byte 0, and any content safety-critical enough that it must not sit only in a path-scoped rule. Do not paste file contents back; cite ranges."
})
```

An audit agent reads the user's own rules, so the classes are evidence, not verdicts: nothing it marks is removed until 2e. A rule the code cannot confirm or refute is a decision the user made and stays KEEP.

Wait for every agent to return before continuing, by ending the turn with a one-line status: each completion arrives as a task-notification that starts your next turn. Never poll one with a `sleep` loop or by re-reading its output file. Merge their reports into a single findings list keyed by file path. The merged list feeds the Phase 2 interview and placement pass; the 1c findings go into `PREFS.audit`.

## Phase 2: Gap-Fill Interview and Placement

### 2a. Interview protocol

Ask one question per `AskUserQuestion` call, except in 2e, whose groups are independent. Skip any question the Phase 1 findings already answered with a citation; say which finding answered it instead of asking.

Mark an option `(Recommended)` only where the question has a factually correct answer, for example the target file for a hook. Never mark one on a question about how the team works or what the user prefers.

Every answer writes its `PREFS` field before the next question is asked.

### 2b. The question nodes

In order, skipping any the Phase 1 findings resolved:

1. **Scope**: which files this run should produce (project `CLAUDE.md`, personal `CLAUDE.local.md`, both). Skip when `--no-local` already decided it. The answer sets `PREFS.scope` and `WRITE_LOCAL` (`false` for project only), and a project-only answer drops the `CLAUDE.local.md` bullet from 2d, and its `.gitignore` line too unless a `CLAUDE.local.md` already exists.
2. **Commands**: confirm the command set agent 1 found, or correct it. Present the found commands in the option descriptions.
3. **Golden rules**: the rules a reviewer would reject a PR over. At most five, each one checkable by grep or by review. Reject a vague answer back to the user once ("Write clean code" is not checkable; ask what a reviewer would grep for). This fills `## Golden Rules` in the template; when the user has none, the section is omitted rather than filled with filler.
4. **Testing**: the test command, how to run a single test file or case, and any prerequisite (a `.env.test`, a running database, a seeded fixture). This fills `## Testing`.
5. **Off-limits**: paths Claude must not edit (generated code, migrations, vendored trees), each with what to do instead. Each path becomes an `Edit` deny rule in 2d, which the file tools enforce; keep a CLAUDE.md line only for the instead-part the rule cannot carry.
6. **Git**: branch naming and PR rules, when the repository history does not already show them. A stated rule that a push needs confirmation becomes a `permissions.ask` rule for `Bash(git push *)` in 2d.

### 2c. The placement rule

Every candidate convention, from the Phase 1 findings and from the interview, goes through two questions in this order. Answer both before writing anything, and record the branch each one took.

1. **Does this apply only to files matching a specific pattern?** No means the root `CLAUDE.md`.
2. **Is it safety-critical?** A convention whose violation costs data, secrets, or a broken main branch is safety-critical. Yes means the root `CLAUDE.md`, which loads unconditionally at session start, or a `PreToolUse` hook when it has to actually block. Never a path-scoped rule: those load on demand, only after Claude reads, edits or writes a matching file (or runs a single-file `cat`, `head`, `tail`, `sed -n` or `grep` on it), so nothing is in context at launch or before that first touch, and compaction summarizes them away until the next one. A secret file is the common case, and its answer is the 2d deny rule.

A third outcome sits beside the two: a multi-step procedure (a deploy, a release checklist, a review routine) is neither a convention nor a rule. It belongs in a skill, which loads only when invoked, so list it as a skill candidate for the Phase 6 report instead of writing it into any file here.

Only a convention that is pattern-specific and not safety-critical becomes a `.claude/rules/<topic>.md` file with `paths:` frontmatter. `paths` is the only frontmatter field Claude Code reads from a rule; any other field is ignored without an error. Cap the newly created rule files at 5 (an audited project's existing rules are restructured in 2e, not counted against the cap), keep each glob rooted no deeper than `MAX_DEPTH`, and when more than five survive, ask the user which five to keep (header "Which rules?", one option per candidate plus "Keep the first five").

Each emitted rule file carries a one-line block-level HTML comment naming the branch it took, placed directly after the closing `---` of its frontmatter and never above it, and the Phase 6 report lists every convention with its destination and the question that sent it there.

### 2e. Audit decisions (`MODE=audit` only; runs before 2d)

Group `PREFS.audit` by class, and within a class by file. Settle each group with the user in rounds of up to three questions per `AskUserQuestion` call, each question one group, in this order: OUTDATED, DERIVABLE and HISTORY (cuts), MERGE, MOVE, then memory. Each question names the file, the count of sections and lines, and two or three examples quoted with their `file:line` and the evidence; the options are `Apply all <n>`, `Let me pick` (the next call lists them, up to four per question, multiSelect) and `Keep all`. A group of one asks about that one section. KEEP needs no question.

For the auto-memory, treat each topic file as one item: OUTDATED and MERGE are proposed for deletion (a MERGE folds its surviving fact into the file it duplicates first), a fact every session in the project needs is proposed as a move into the root CLAUDE.md or a rule, and `MEMORY.md` is rewritten to point only at what remains. A topic file whose fact is still true and project-specific stays where it is.

Write each answer into its `PREFS.audit` entry before the next call. A section the user did not approve stays exactly as it is.

### 2f. Project documents (skip on `--no-docs`; runs after 2e, before 2d)

Decide, per document, whether its writer skill runs. The writer owns the content; nothing in this command drafts a document. Take the evidence from the 0b inventory and the Phase 1 findings, and ask nothing a finding already answers.

Read the rows top to bottom; the first match decides.

| Document | State | Action |
|---|---|---|
| any | no code to describe | `skip` |
| `.planning/PROJECT.md` | exists | `leave`: another tool manages it |
| `DESIGN.md` | exists, describes architecture, and an `ARCHITECTURE.md` exists too | `leave` both and report the clash |
| `DESIGN.md` | exists and describes architecture | `move`, run by `ac:architecture-md-writer`: it asks whether to `git mv` the file to `ARCHITECTURE.md`, then repairs it in place; the size bar does not apply to a file that exists. If the user declines, both files stay as they are and no `ARCHITECTURE.md` is written. `leave` under `MODE=leave` |
| any | exists and is the right kind | `audit-fix`; `leave` under `MODE=leave` |
| `PROJECT.md` | missing | `write`: what the project is for, its scope and its decisions are what the code cannot show, so the writer asks the user for them |
| `ARCHITECTURE.md` | missing, bar met | `write` |
| `ARCHITECTURE.md` | missing, below the bar | `skip`, with the numbers that failed it |
| `DESIGN.md` | missing (or moved away), the project has a UI and a theme | `write`: the tokens come from the theme |
| `DESIGN.md` | missing, a UI but no theme | `skip`: no direction exists yet, so the report names `ac:frontend-design` |

The ARCHITECTURE.md bar is the "Decide first" test in `ac:architecture-md-writer`; this command only measures it. Take the source languages in Phase 1 agent 2's histogram (not Markdown, JSON, YAML, lockfiles or images) and run `git ls-files -z -- '*.<ext>' ':!:*lock*' ':!:dist/**' ':!:build/**' ':!:vendor/**' ':!:node_modules/**' | xargs -0 cat | wc -l` for each, leaving out any generated or built bundle you can see in the listing, then glance at the top-level directories. A project under the bar, with a handful of modules, gets no file.

A UI is present when a manifest names a UI framework (React, Vue, Svelte, Angular, Next, Nuxt, `flutter` in `pubspec.yaml`), when the tree has SwiftUI imports, Blade views or HTML templates, or when stylesheets are tracked. A theme exists when `ac:design-md-writer` step 1 would find a source to derive tokens from; read that step rather than listing sources here.

`MODE=leave` leaves every existing document alone and still creates a missing one that meets its bar. Under `audit` and `fresh` an existing document is audited and fixed in place: this command never replaces a document wholesale, because each holds the user's rationale, so "Start fresh" does not reach them.

A `DESIGN.md` that is written or fixed also needs its `.claude/rules/ui.md` rule (the pointer, scoped with `paths:` to the view files). Add it to the 2c rule candidates now so it counts against the cap of five; when that makes six, ask "Which rules?" again.

Write each decision, with its evidence, into `PREFS.docs`.

### 2d. One proposal, one approval

Before any file is drafted, print everything the run would write as one list, then take one approval. Build it from the Phase 1 findings, the `PREFS` queue and the 2c placement, one bullet per item, each naming its target file:

- **Files.** Each `CLAUDE.md`, `CLAUDE.local.md` and `.claude/rules/<topic>.md` the run would write or change, with a one-line summary, an estimated line count, the glob of each rule, `@AGENTS.md` when 3b or 3c will import one, and the `.gitignore` lines: `CLAUDE.local.md` when 0d set `NEEDS_IGNORE`; `settings.local.json` when any approved item targets that file and 4a would create it; the hook script when its registration is local.
- **Permissions.** Skip any rule the settings files already hold.
  - `permissions.deny` in `.claude/settings.json` (team-shared: deny beats allow in every file, so it protects every teammate), one `Read` rule per secret shape agent 4 found. A bare filename matches at any depth (`Read(.env)`, `Read(*.pem)`), a directory takes `Read(secrets/**)`, and a template the shape also catches is carved out by a negation listed after it (`Read(.env.*)` then `Read(!.env.example)`). Say in the bullet that this blocks Claude's file tools and `cat`-style shell reads but not `grep -r` or a script, so the file is guarded, not sealed.
  - `permissions.allow` in `.claude/settings.local.json`: the project's own non-destructive commands from `PREFS.commands`, in the space form with the `*` after the subcommand (`Bash(pnpm test *)`, `Bash(vendor/bin/pint --test *)`). Never a bare program (`Bash(npm *)`, `Bash(php *)`) or a runner wildcard (`npm run *`, `pnpm run *`, `python *`, `npx *`, `bash *`), which auto mode drops. Name the script (`Bash(pnpm run lint *)`). Nothing that deploys, migrates, pushes or deletes.
  - Signal-driven rules, each only with its signal and in the file `settings-wiring.md` names: `Read` deny for tracked generated or vendored trees; `Edit` deny for the 2b off-limits paths; `ask` for `Bash(git push *)` on a stated push rule.
- **Restructure** (`MODE=audit`). Per existing file: the approved cuts, merges and moves as counts with the line ranges, the lines before and after, the rule files a move creates or extends with their globs, and the skill candidates the moves produced. Each result must sit inside its budget from the skill's principle 1, or the bullet says by how much it is over and why.
- **Memory** (`MODE=audit`). The topic files to delete, to merge and to move, each with its one-line evidence, and the resulting `MEMORY.md` line count.
- **Settings cleanup** (`MODE=audit`). Existing permission rules that no longer match anything (a `Read` deny for a path that is gone, an `allow` for a script the manifest no longer has) and exact duplicates, each to be removed only on approval here.
- **Project documents** (omit on `--no-docs`). One line per document: its path, its state (missing, current, stale, wrong kind, below the bar), the action (`write`, `audit-fix`, `move`, `leave`, `skip`) and the evidence (the lines it was measured on, the theme file found, the numbers that failed the bar). Say that each action runs its writer skill in 3h, that a writer may ask a few questions about rationale the code cannot show, and which pointer line each adds to `CLAUDE.md` (or `AGENTS.md` when the project has no `CLAUDE.md`) and, for `DESIGN.md`, which `paths:` rule over the view files, counted against the cap of five new rules.
- **Rule repairs.** Each existing rule agent 4 flagged for content above its frontmatter, with the one change: move that content to directly after the closing `---`. This is a correction of a silent loader failure, not a rewrite, so it applies under every `MODE`, `leave` included.
- **Hook.** `PREFS.hook`: `format` when agent 3 found a formatter that rewrites in place, `lint` when it found only a reporter, `format+lint` as one script when it found both, with each resolved executable path, the exact pipe-test command string `hook-wiring.md` step 4 will run, the script path and the target file (`.claude/settings.local.json` by default: the committed file runs the script on every machine and in CI). Omit the bullet when no tool is installed on disk, and say so.
- **Language server.** Run Phase 5 step 1 now, against the installed marketplace manifests, never from memory: match Phase 1 agent 2's extension histogram against their `extensionToLanguage` maps. One plugin per extension with its marketplace; when two legitimate candidates exist for one language, name both, and Phase 5 asks which. The key goes to `.claude/settings.local.json` by default, or to the shared file or `~/.claude/settings.json` when the user says so.
- **Project settings.** `worktree.symlinkDirectories` when Phase 1 saw several worktrees and a `node_modules`; `claudeMdExcludes` (local) when the repo has several unrelated nested `CLAUDE.md` files and the user named their area. Omit the bullet when neither signal exists.
- **Skill candidates.** The procedures 2c set aside, listed only. This run writes no skill.

Then:

```
AskUserQuestion({
  header: "Proposal",
  question: "Does this setup look right? Nothing is written until you approve it.",
  options: [
    {label: "Proceed", description: "Write everything listed above: each instruction file through the 3f existing-file gate, each project document fixed in place by its writer."},
    {label: "Drop settings", description: "Instruction files, project documents and the language server; no permission rules, no hook and no project settings keys."},
    {label: "Drop the hook", description: "Everything except the hook."},
    {label: "Instruction files only", description: "CLAUDE.md files and rules; no settings, no hook, no language server, no project documents."}
  ]
})
```

No option carries `(Recommended)`. The tool adds an "Other" answer on its own, which is where a moved target file, a dropped rule or a dropped project document arrives; apply it to the queue and print the changed bullets before continuing. Record the approved set in `PREFS`; Phases 3 to 5 act on that set and nothing outside it. Under `--dry-run`, print the proposal and skip the question.

## Phase 3: Draft and Write

### 3a. Invoke the writing skill (once, at phase entry)

Before drafting any file, invoke the writing skill exactly once:

```
Skill({skill: "ac:claude-md-rules-creator"})
```

Treat its Pre-flight checklist as the gate every emitted file must pass before the `Write` or `Edit` call.

### 3b. Draft the root `CLAUDE.md` (skip when `MODE=leave`)

Skip the `/init` preface; it carries no information. The five-question frame in the skill's `references/content-rules.md` (stack, where code lives, how to run things, conventions, off-limits) drives section selection, extended by the `## Golden Rules` and `## Testing` sections the template carries. Pull content from the Phase 1 deviations and the `PREFS` queue; never restate language defaults or anything the linter and formatter already enforce.

When Phase 1 found a root `AGENTS.md`, put `@AGENTS.md` on its own first line and write below it only what is specific to Claude Code; restate nothing the import already carries. Claude Code reads `AGENTS.md` by itself only when no `CLAUDE.md` or `CLAUDE.local.md` sits in the working directory or above it, a project that has both loads the CLAUDE.md files only, and an imported `AGENTS.md` is never read twice. The same covers `CLAUDE.local.md` in such a project: writing one would stop the direct read, so the import in the project file has to exist first.

When `MODE=audit`, do not draft a replacement. Apply the approved `PREFS.audit` decisions as one `Edit` per change against each existing file (CLAUDE.md, CLAUDE.local.md, nested CLAUDE.md files and rules alike): a cut removes the range, a merge removes the duplicate and keeps the more specific home, a move writes the content into its new rule file (created through 3d's shape, `paths:` at byte 0) or doc before removing it from the source. Never remove a range before its moved copy exists. Add only what Phase 1 found missing and the user approved. The gate in 3f applies to the merged result.

Length budget: the root-file budget in the skill's principle 1. When the draft exceeds its target, cut lines that fail the deletion test, then move topic content into `.claude/rules/<topic>.md` files or behind pointer lines. A fact the 2d proposal places in a hook, permission rule or plugin entry is not also written as prose.

Run the skill's Pre-flight checklist against the draft and resolve every unchecked box before writing.

### 3c. Draft `CLAUDE.local.md` (skip when `--no-local`)

When `WRITE_LOCAL=false`, skip drafting; when a `CLAUDE.local.md` already exists, the 0d check still feeds the `.gitignore` bullet in 2d.

When `WRITE_LOCAL=true`, draft the personal companion. Content follows Example 3 in the skill's `references/examples.md`: the user's role, sandbox URLs, test accounts (pointers, never credentials), communication preferences. Honor the 1a worktree branch: for sibling or external worktrees, write the personal content to `~/.claude/<PROJECT_SLUG>-instructions.md` and make `CLAUDE.local.md` a stub whose first line is `@~/.claude/<PROJECT_SLUG>-instructions.md`.

When a root `AGENTS.md` exists and no project `CLAUDE.md` will exist after this run, the personal file is what switches Claude Code's direct `AGENTS.md` read off for this user, so it has to carry the import itself: put `@AGENTS.md` on its first line, and name that in the 2d Files bullet. For sibling worktrees the import goes into the `CLAUDE.local.md` stub as a second line, not into the home-directory file; this run writes `PATH_ARG`'s stub only, and 6d prints the two-line stub for the user to copy into each other worktree.

Run the skill's Pre-flight checklist before writing. Length budget: the CLAUDE.local.md budget in principle 1.

### 3d. Draft up to five `.claude/rules/*.md`

For each convention that took the rule branch in 2c, and for the `ui.md` rule 2f added for a `DESIGN.md`, draft a focused rule file at `<PATH_ARG>/.claude/rules/<topic>.md` with `paths:` frontmatter per the path-scoped rule example in the skill's Draft the file step. Topic name follows the convention in the writing skill: lowercase, hyphen-separated, one focused subject.

Length budget per rule: the rule budget in principle 1. When a draft exceeds its target, cut it or split the topic before writing.

Run the skill's Pre-flight checklist against each rule draft. The path-scoped items under "By shape" matter most here: the glob actually matches your intent, and no `paths: ['**']`, which the loader treats as no `paths:` at all.

### 3e. Review the drafts (skip when `REVIEW=false` or `DRY_RUN=true`)

Create a fresh scratch directory with `mktemp -d "${TMPDIR:-/tmp}/ac-init-<PROJECT_SLUG>-XXXXXX"`, so an aborted earlier run's drafts are never reviewed again, put every draft from 3b to 3d under it mirroring its target path, write the merged Phase 1 findings beside them as `findings.md`, and spawn one reviewer:

```
Agent({
  subagent_type: "ac:oracle",
  description: "Review init-project drafts",
  prompt: "Review the Claude Code instruction drafts under <scratch dir> for the project at <PATH_ARG>, before they are written. findings.md holds the discovery evidence. The readers run <your own model ID>, which gets the <LEAN | CLASSIC> system prompt shape; judge duplication against that shape's section of the reference below and against the per-model bundle section for that model. Line budgets: CLAUDE.md 40 to 80 lines with a ceiling of 120, CLAUDE.local.md 10 to 30, each rule 15 to 50 with a ceiling of 80. Also test that no fact appears in two files and that nothing a hook, permission rule or plugin entry already enforces is also written as prose.\n\nClaims to test against the project itself, not against findings.md: every command in a draft runs as written (it is a manifest script, a Makefile or justfile target, or an installed binary); every path and every rule glob matches at least one tracked file (`git -C <PATH_ARG> ls-files`); no line restates what the linter, the formatter or the language already enforce; no line duplicates or contradicts ${CLAUDE_PLUGIN_ROOT}/skills/claude-md-rules-creator/references/claude-code-builtin-prompts.md for the model this project runs; nothing safety-critical sits only in a path-scoped rule; every rule file starts with `---` at byte 0, since anything above the frontmatter makes the rule load unconditionally; no secret, token or personal path appears in a team-shared file; each file is inside its line budget; any project test that reads instruction files (grep the test tree for `.claude/rules` and `CLAUDE.md`) still passes against the drafts, applying its logic by reading it rather than running the suite. Return your standard report, read-only."
})
```

`${CLAUDE_PLUGIN_ROOT}` is already substituted when this body renders, so the reference path reaches the reviewer as an absolute path. Then fix every CONFIRMED finding in the scratch drafts, run the check a PLAUSIBLE finding names before acting on it, and keep the dismissed ones for the 6d report. The drafts 3f writes are the reviewed ones. Delete the scratch directory at the end of Phase 6.

### 3f. Existing-file safety and dry-run handling

Under `PROPOSE_ONLY`, the `.gitignore` lines and the rule repairs go into `.ac/init/proposed/` like every other change (the repaired rule as a copy, the lines in `settings.md`), and nothing below touches the tree. Otherwise, when 2d approved the `.gitignore` line and `DRY_RUN=false`, append `CLAUDE.local.md` to `<PATH_ARG>/.gitignore` (create it if missing) before the first file below. Apply each approved rule repair as one `Edit` that moves the content above the frontmatter to directly after it; 2d already showed that exact change, so it skips the sidecar gate. Then, for every target file (`CLAUDE.md`, `CLAUDE.local.md`, each rule):

1. When `DRY_RUN=true`: print the intended write target path, the line count of the draft, and the first 20 lines of the draft. Do not call `Write` or `Edit`. After all targets have been printed, exit Phase 3 and continue to Phase 4 (Phases 4 and 5 have their own dry-run branches that write nothing); Phase 6 then reports a dry run.
2. When the target file does not exist: pass the pre-flight checklist, then call `Write`.
3. When the target file exists and `FORCE_OVERWRITE=true`: pass the pre-flight checklist, then call `Edit` (or `Write` for a full replacement when the existing content is being fully superseded).
4. When `PROPOSE_ONLY=true`: write the draft, or the existing file with the approved edits applied, to `<PATH_ARG>/.ac/init/proposed/<relative target path>` whether or not the target exists, ask nothing, and continue with the next target. Apply edits to a copy there, never to the target.
5. When the target file exists and `FORCE_OVERWRITE=false`: write the draft to `<target>.proposed`. Then ask via `AskUserQuestion` (header "Apply?", question "`<target>` already exists. The proposed draft is at `<target>.proposed`. How should this file be handled?", options "Apply (overwrite original)", "Skip (leave original, keep `.proposed` for review)", "Edit (open the proposed file for manual edits, then re-run with `--force-overwrite`)"). Apply the user's choice. On "Apply", `Edit` or `Write` the original file with the proposed content and delete the sidecar. On "Skip", leave both files in place. On "Edit", leave the sidecar in place and print a one-line instruction to re-run the command with `--force-overwrite` after the manual edits.

### 3g. Memory cleanup (`MODE=audit`, approved items only)

Apply the approved memory items in `MEMORY_DIR`: fold a merged fact into its surviving topic file first, then delete the merged or outdated topic file, then rewrite `MEMORY.md` so every pointer names a file that exists and nothing points at a deleted one. A fact moved into CLAUDE.md or a rule was already written in 3b to 3d; delete its topic file only after that write landed. Under `PROPOSE_ONLY`, write the same plan to `<PATH_ARG>/.ac/init/proposed/memory-cleanup.md` (one line per item: file, action, evidence, and the rewritten `MEMORY.md` below it) and change nothing in `MEMORY_DIR`. Under `--dry-run`, print it.

### 3h. Project documents (`WRITE_DOCS=true`, approved items only)

Run after 3g, in this order: `PROJECT.md`, `ARCHITECTURE.md`, `DESIGN.md`. For each document whose approved action is neither `leave` nor `skip`, invoke its writer once with the Skill tool (`ac:project-md-writer`, `ac:architecture-md-writer`, `ac:design-md-writer`) and follow that skill's workflow in the mode the action names: `write`; `audit-fix`, which is its audit mode followed by the fixes below; or `move`, which `ac:architecture-md-writer` runs as its own question about `git mv` followed by an in-place repair, with a visual `DESIGN.md` written afterwards when 2f decided so. The memory-file gate lets the writes through because the skill was invoked, the budget hook stays silent in this session, and the writer's own size rule governs.

- **Questions.** A writer asks the user only what the code cannot show, one question at a time (2a), after the 2d approval. It does not re-ask what Phase 2 settled.
- **Fixes.** In `audit-fix`, apply directly a repair that only restores a fact: a cited path or symbol that moved, a lint error, a stale count. Put every finding that removes or rewrites the user's own rationale through one question per document (`Apply all <n>`, `Let me pick`, `Keep all`), as in 2e. Edit in place with one `Edit` per change, never with a wholesale `Write` over an existing document.
- **Pointers.** The writer's last step adds a pointer line to the rules file. Add it to the `CLAUDE.md` that 3b wrote or edited (`AGENTS.md` only when the project has no `CLAUDE.md`), then check that file against its budget again. Under `MODE=leave` with a `CLAUDE.md` already in place, 3b did not touch it and neither does 3h: print the pointer lines in the report as not applied. The `ui.md` rule for a `DESIGN.md` was drafted in 3d, which satisfies the writer's pointer step, so `ac:claude-md-rules-creator` is not invoked a second time.
- **Blocked.** A writer that cannot proceed (a `DESIGN.md` with neither a theme nor a direction, a run that cannot ask) writes nothing, and its open question goes to the report.

Under `--dry-run`, print each document's path, action and evidence and run no writer. Under `PROPOSE_ONLY`, give each writer a target under `<PATH_ARG>/.ac/init/proposed/<relative path>`: the existing document copied there first, or for `write` the path the writer would have chosen. Put the pointer line in the proposed copy of the rules file, record a `move` as a planned `git mv` line in `settings.md`, skip the design writer's export step, and change nothing in the tree.

## Phase 4: Settings: Permission Rules and the Hook

Under `PROPOSE_ONLY` this phase writes no script and no settings file and runs no proof: the hook script body, each merge and removal with its target file, and the `.gitignore` lines go into `.ac/init/proposed/settings.md`, and 6d lists the proofs as not run.

This phase writes only what the 2d proposal approved: the permission rules (`deny`, `allow`, `ask`), the approved removals of stale ones, one `PostToolUse` hook and the project keys 2d listed; the language-server key follows in Phase 5 through the same guarded merge. Skip it when the approval dropped them all, and say so.

### 4a. Targets

Each item goes to the file its 2d bullet named: `deny` and `ask` rules to `<PATH_ARG>/.claude/settings.json`; `allow` rules, the hook, `claudeMdExcludes` and `worktree.symlinkDirectories` to `<PATH_ARG>/.claude/settings.local.json`; unless the user moved one through "Other"; a moved item goes where the user said and nowhere else.

When a target does not exist, create it containing `{}` (`jq` on a zero-byte file prints nothing, so a merge would `mv` an empty file into place), and for `settings.local.json` add its name to `<PATH_ARG>/.gitignore` in the same step.

### 4b. Build the hook script (skip when the approval dropped the hook)

Follow the seven-step procedure, the script and the three proofs in `${CLAUDE_PLUGIN_ROOT}/skills/claude-md-rules-creator/references/hook-wiring.md`, including its format-on-edit variant for `PREFS.hook.kind` `format` and its single-script rule for `format+lint`; do not re-derive them here. The 2d bullet printed the exact command the pipe-test runs, so its approval is that procedure's step 3 gate. When the registration target is `settings.local.json` and 2d approved it, append the script's path (`.claude/hooks/<script>.sh`) to `<PATH_ARG>/.gitignore` in the same step that writes the script. Take each executable name from the Phase 1 finding and bake it into the script as a literal; repository content never names the executable. State what the hook cannot do in the bullet and again in the report: it runs after the write lands, so it reports rather than blocks, and it does not fire when a `Bash` command rewrites the same file.

### 4c. Guard every settings write

For each target file, once, with all of its approved keys in one merge, stopping at the first failure:

1. `jq . <target>` when the file existed before this run. A non-zero exit means it was already malformed: stop, report the parse error and the path, and change nothing, not even a backup. Do not repair a malformation this command did not create. Say which way it fails: interactively Claude Code offers a fix dialog, while a `-p` or CI run shows no dialog and skips the broken file or values (`claude doctor` lists what it dropped). Skip this step for a file 4a just created.
2. `cp` the target to `<target>.bak.$(date +%Y%m%d%H%M%S)` when it existed before this run.
3. Merge into `<target>.tmp`, then `mv` it into place. Never hand-write the whole file with `Write`. The hook entry uses the expression in `hook-wiring.md`; permission rules append without duplicating and keep every rule in its order, except that all `!` negations, existing and new, move to the end, because a negation only carves out of the rules listed before it:
   ```sh
   jq --argjson deny '["Read(.env)","Read(.env.*)","Read(!.env.example)"]' '
      def neg: test("^[A-Za-z]+\\(!");
      ((.permissions.deny // []) + $deny | reduce .[] as $r ([]; if index($r) then . else . + [$r] end)) as $all
      | .permissions.deny = [$all[] | select(neg | not)] + [$all[] | select(neg)]' \
      <target> > <target>.tmp && mv <target>.tmp <target>
   ```
   and the same shape with `allow` or `ask` for `.permissions.allow` or `.permissions.ask`. An approved removal is `jq --argjson drop '["<rule>"]' '.permissions.deny -= $drop'` in the same merge. `claudeMdExcludes` and `worktree.symlinkDirectories` are arrays and merge the same way.
4. `jq -e` per key written: the hook selector from `hook-wiring.md` for the hook, and `jq -e --arg r '<rule>' '.permissions.deny | index($r)'` for each rule (the same with `allow` or `ask`), and `jq -e '.<key>'` for each other key written. Exit 0 is correct; exit 1 or 4 means the rule is missing, exit 5 means malformed JSON or wrong nesting.
5. `claude doctor` with the target project as the working directory. It reads the settings files without a trust prompt and names a rule it cannot parse.

Roll back when step 4 or step 5 fails, then report which step failed and what it printed. Rollback has two shapes: restore the backup when step 2 took one, and when 4a created the file this run, delete it and remove the `.gitignore` line instead. A rolled-back hook also takes its script and the script's `.gitignore` line with it.
### 4d. Prove the rules and the hook

Claude Code reloads settings files on change, so when `PATH_ARG` is this session's primary working directory the deny rules already apply: list them and run `claude doctor` to confirm none was rejected. For the hook, run the three proofs `hook-wiring.md` names; the live-fire proof is the only one that exercises the wiring, and it needs this session to be running in `PATH_ARG`. When `PATH_ARG` is another directory, this session never loads that project's settings, so run the pipe-test and `jq -e` proofs, skip the live fire, and report it as not yet proved, to be checked from a session opened in that project, rather than as a failed hook.

Under `--dry-run`, print the script, each merge expression and each target path, then stop: create no file, add no `.gitignore` entry, and run none of the steps.

## Phase 5: Language Server

Under `PROPOSE_ONLY`, write the matched plugin and the `enabledPlugins` merge into `.ac/init/proposed/settings.md` and run neither the merge nor the probe.

Follow `${CLAUDE_PLUGIN_ROOT}/skills/claude-md-rules-creator/references/lsp-wiring.md`: enumerate the installed marketplace manifests at runtime rather than consulting any table, prefer a plugin from `claude-plugins-official` and say so explicitly when falling back to a third-party marketplace, and refuse a proposal whose candidates declare overlapping extensions instead of silently disabling one of them.

1. Match the extension histogram from Phase 1 agent 2 against the `extensionToLanguage` maps the reference enumerates, after dropping what its Rule 1b excludes: extensions an enabled plugin already serves, and plugins the user set to `false`.
2. The 2d proposal named at most one plugin per extension and the marketplace each comes from, and its approval covers them. When 2d named two legitimate candidates for one language, ask which through one `AskUserQuestion` now: that is a choice to hand to the user, not something to resolve silently.
3. On approval, merge `enabledPlugins["<plugin>@<marketplace>"] = true` into the file 2d named (default `<PATH_ARG>/.claude/settings.local.json`) through the same five guarded steps as 4c, with one substitution: step 4's assertion is `jq -e '.enabledPlugins["<plugin>@<marketplace>"]' <target>`, not 4c's hook selector, which exits 4 on a file without hooks. When the marketplace holding the plugin is not installed, do not install it: print the `/plugin marketplace add` and `/plugin install` lines for the user to run, and stop the phase there.
4. Verify both parts the reference requires, because neither is sufficient alone: the plugin appears under `enabledPlugins`, and one real `LSP` `hover` or `documentSymbol` call against an existing file of that language answers. Name the server that replied. When part 1 passes and part 2 fails, report it as a missing server binary or a plugin not yet loaded, not as a misconfiguration: name the binary, and say that `/reload-plugins` or a new session settles the second. When `PATH_ARG` is not this session's working directory, this session never loads that project's settings: run part 1 only and report part 2 as not yet proved, to be checked from a session opened there.

When the detected language is outside every installed marketplace's coverage, name that gap and stop. Authoring a `.lsp.json` means authoring a plugin, which is not a project-setup step.

Under `--dry-run`, print the matched candidates and the marketplace each comes from, and write nothing.

## Phase 6: Read-Back, Dedupe, and Report

### 6a. Read every emitted file

Under `PROPOSE_ONLY` every emitted file is a copy under `.ac/init/proposed/`, and 6b and 6c edit those copies, never the targets.

`Read` each file actually written or proposed in Phase 3. A rule repair is not part of 6b or 6c and gets no second pass. For `--dry-run` runs there is nothing to read; skip to 6d and emit a summary stating that the run was a dry run.

### 6b. Parent-versus-child dedupe pass

For each line in a `.claude/rules/<topic>.md` file, check whether the same fact or near-paraphrase exists in the root `CLAUDE.md`. When a duplicate is found:

1. Keep the version in the more specific scope. A path-scoped rule for `src/api/**` keeps the rule; the root file drops it, unless `MODE=leave`, where CLAUDE.md is not touched: drop the line from the rule instead and say so in the report.
2. When the parent is more specific (the rule is a vague restatement), keep the parent and drop the child line.

Check each project document written or changed in 3h against the root `CLAUDE.md` the same way: a fact that sits in both stays in the document and the `CLAUDE.md` line becomes a pointer; under `MODE=leave`, where `CLAUDE.md` is untouched, report it instead.

Apply the dedupe pass by `Edit`ing the affected files. Run the pre-flight checklist again on any file the dedupe pass touched.

### 6c. Anti-pattern check

For every emitted file, scan against the skill's principles 1, 2, 6, 7 and 10: nothing the model acts on without being told, no fact in two files, no emphasis caps, no duplication of the host system prompt for the readers' model or of another loaded layer.

When a violation is found, fix it in place with `Edit` and re-run the pre-flight checklist on the affected file.

### 6d. Report

Read `${CLAUDE_SKILL_DIR}/references/final-output.md` now and print the report exactly as it specifies.

Under `PROPOSE_ONLY`, also write `.ac/init/proposed/SOURCES.md`: `git rev-parse HEAD` and, for every source file a draft was made from, `<path> <git hash-object of it>` taken when the drafts were finished. A proposal is a snapshot; applying later starts by re-hashing every listed source and redrafting each one whose hash changed.

Read `${CLAUDE_SKILL_DIR}/references/provenance.md` before changing the behaviour a rule in this body backs.
