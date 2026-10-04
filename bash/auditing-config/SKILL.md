---
name: auditing-config
description: Audit and optimize an existing Claude Code configuration against current best practices. Use this skill when a user asks to review, improve, clean up, or optimize their Claude Code setup, CLAUDE.md, settings, hooks, MCP servers, or skills. Also use when the user says things like "check my config", "is my CLAUDE.md too long", "reduce token costs", "tighten permissions", or "my Claude Code setup feels bloated". This skill assumes the project has code, and possibly documentation or OpenSpec specs, that inform the optimization.
allowed-tools: Read, Grep, Glob, Edit(**/CLAUDE.md), Edit(.claude/**), Edit(.githooks/**), Edit(.github/workflows/**), Edit(scripts/sync-config-table.js), Edit(.husky/pre-commit), Edit(AGENTS.md), Edit(.mcp.json), Edit(.gitignore), Edit(.claudeignore), Edit(scripts/sync-config-table.sh), Write(CLAUDE.md), Write(.claude/**), Write(.githooks/**), Write(.husky/pre-commit), Write(.gitignore), Write(.claudeignore), Write(.github/workflows/**), Write(scripts/sync-config-table.sh), Write(scripts/sync-config-table.js), Bash(git rev-parse:*), Bash(git log:*), Bash(git config core.hooksPath:*), Bash(jq:*), Bash(bash scripts/sync-config-table.sh), Bash(test -f:*), Bash(wc:*), Bash(date +%Y-%m-%d), Bash(chmod +x .githooks/pre-commit), Bash(rm .githooks/pre-commit), Bash(rmdir .githooks), Bash(chmod +x scripts/sync-config-table.sh)
argument-hint: "[optional: specific area to focus on, e.g. 'CLAUDE.md', 'hooks', 'costs']"
---

# Optimize Claude Code Configuration

You are auditing and improving an existing Claude Code setup. The project has code, possibly documentation, and possibly OpenSpec specifications. Your job is to identify what's good (preserve it), what's missing, what's bloated, and what violates current best practices — then fix it with the user's approval.

## Philosophy

Configuration is a multiplier, but only if it's lean. A 60-line CLAUDE.md with progressive disclosure outperforms a 300-line monolith. Three well-chosen MCP servers beat twenty poorly managed ones. A PostToolUse hook that runs the formatter on every edit eliminates an entire class of manual intervention forever.

The guiding question for every instruction in CLAUDE.md: "Would removing this line cause Claude to make a concrete mistake?" If no — remove it.

## Step 0: Recall learnings

If `.claude/learnings.md` exists, read all entries and apply them silently to inform this run. The `[skill-name]` tag on each entry is provenance only — all entries apply regardless of which skill wrote them. Do not announce that learnings were loaded.

If the file does not exist, proceed without mention.

## Step 1–2: Inventory and analysis

Step 1 (inventory) and Step 2 (analysis) below are read-heavy — dozens of files whose content
feeds into three tiered findings lists. Do this reading directly, in the main conversation:
work through the checklist sections in order, read each file as you reach it, and keep running
notes of the metrics and findings as you go rather than re-reading anything. The interactive
approval (Step 3) and the actual edits (Step 4) happen afterward, in the same thread, so the
user can see and steer them.

If `$ARGUMENTS` specifies a focus area, still work through every section below, but prioritize
reading and depth on the sections that match it.

The **Configuration files**, **Project context**, and **Current state metrics** bullets below
are the inventory scope for Step 1. The `### 2x` sections that follow are the Step 2 analysis
checklist — work through them in order (2a, 2a-bis, 2b, ... 2i), reading whatever each one
needs as you reach it.

### Configuration files

- `CLAUDE.md` (project root and any subdirectories)
- `AGENTS.md`
- `.claude/settings.json` and `.claude/settings.local.json`
- `.claude/local.md`
- `.claude/rules/*.md`
- `.claude/skills/*/SKILL.md`
- `.claude/commands/*.md` (legacy format)
- `.claude/agents/*.md`
- `.claude/learnings.md`
- `.headroom/` (machine-local Headroom data — check for presence with Glob on `.headroom/*`)
- `context/` (domain context files at project root by convention — company profile, brand voice, architecture decisions, etc.; if CLAUDE.md's `## Context files` table registers a different location, use that instead)
- `context/design/` (Claude Design handoff artifacts — PROMPT.md, design-notes.md, screenshots/ — under the registered context location)
- `DESIGN.md` (root-level design system spec — YAML tokens + Markdown rationale; auto-read by Claude Code and other agents)
- `.mcp.json` (project root)
- `~/.claude/CLAUDE.md` (user level — read but don't modify without asking)
- `~/.claude.json` (user-level MCP — read but don't modify without asking)

### Project context

- Package manager and dependencies (package.json, composer.json, Cargo.toml, etc.)
- Build/test/lint commands (scripts in package.json, Makefile targets, etc.)
- Formatter and linter configs (.prettierrc, .eslintrc, phpcs.xml, rustfmt.toml, etc.)
- CI/CD configuration
- Content-project artifacts: static-site configs (`hugo.toml`, `_config.yml`, `astro.config.*`, `mkdocs.yml`), prose tooling (`.vale.ini`, `.markdownlint.*`), shared knowledge bases or style guides referenced from CLAUDE.md
- OpenSpec artifacts (`openspec/` directory, `openspec/project.md`, change specs)
- Documentation (`docs/`, `README.md`, architecture docs)
- Directory structure and apparent architecture patterns
- Hook managers and their hook files (`.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`)
- Project-local git hooks directory (`.githooks/`) and sync scripts (`scripts/sync-config-table.{sh,js}`)
- Design system artifacts: `DESIGN.md` at the project root (persistent design system spec); `context/design/` (or the registered context location's `design/` subfolder) for Claude Design handoff artifacts (PROMPT.md, design-notes.md, screenshots/)

### Current state metrics

Count and report:

- CLAUDE.md word count via `wc -w` (a token-density proxy; line count alone doesn't reflect token load since line length varies) — target ~300–600 words for a lean project-root file, higher only if `@`-imports carry the bulk of the detail out of the main file
- Number of `@`-imports in CLAUDE.md
- Number of active MCP servers
- Number of skills
- Number of hooks
- Permissions: what's allowed, what's denied
- Environment variables set in settings.json
- Number of entries in `.claude/learnings.md` (if it exists)

## Analysis checklist (2a–2i)

This is Step 2, analysis against best practices, performed directly in the main thread. Work
through each section below in order, reading whatever files it needs.

### 2a: CLAUDE.md audit

Check for these anti-patterns:

**Bloat indicators** (things to remove or move):

- Standard language conventions Claude already knows → remove
- Rules that the configured linter/formatter already enforces → remove ("never send an LLM to do a linter's job")
- Personality instructions ("be a senior engineer", "think carefully") → remove
- File-by-file codebase descriptions → remove (Claude can read files itself)
- Domain knowledge that's rarely needed → move to a skill
- Long inline documentation → extract to a reference file and use `@`-import with a trigger condition
- Duplicated information that also exists in AGENTS.md or OpenSpec → remove from CLAUDE.md, reference instead

**Missing essentials** (things to add if absent):

- Exact build/test/lint/dev commands (not vague — actual command strings)
- Key directory structure (only non-obvious parts)
- Conventions that deviate from standard or that Claude commonly gets wrong
- Explicit "Don't" section for known failure modes
- Compact instructions (what to preserve when compacting)
- Progressive disclosure pointers for reference docs (`@path **Read when:** <trigger>`)
- Learnings section (instructs Claude to log corrections to `.claude/learnings.md` instead of modifying CLAUDE.md directly)

**Structural checks:**

- Is the file using `@`-imports for large reference material? (imports reduce token waste by up to 59%)
- If AGENTS.md exists, does CLAUDE.md import it via `@AGENTS.md` instead of duplicating content?
- If OpenSpec is used, does CLAUDE.md reference `@openspec/project.md` for project context?
- If `DESIGN.md` exists at the project root, does CLAUDE.md reference it via `@DESIGN.md **Read when:** building or editing any UI component`? Without this pointer Claude won't consult the design system when making UI decisions.
- If the registered context location (`context/` by convention, or wherever CLAUDE.md's `## Context files` table points) contains files, does CLAUDE.md have a `## Context files` table registering them? Without this table, skills can't discover which context files exist or judge their relevance — they only find files they're explicitly pointed to. Note: this is a plain Markdown table, not an `@`-import — the table itself loads every message, but each underlying file loads only when a skill judges it relevant to the current task from its Summary.
- Are there too many `IMPORTANT:` or `YOU MUST` markers? (if everything is marked important, nothing is)

**Correctness checks** (verify against reality, not just structure):

- For each command referenced in CLAUDE.md (build/test/lint/dev/deploy), verify it exists in the actual manifest (package.json scripts, Makefile targets, Cargo.toml, composer.json, etc.). Flag any command that would fail — renamed script, deleted target, wrong path.
- For each file path referenced (via `@`-import, the `## Context files` table, or inline mention outside those two), verify with `test -f` that it resolves. Flag broken references.
- Flag stack/version claims that contradict the actual dependency manifest (e.g., CLAUDE.md says "Node 16" but `package.json` `engines` says `>=20`).

### 2a-bis: Key Config Files table hygiene

`sync-config-table.sh` (v5+) can only judge whether a file is _config-shaped_ (it matched a
scanned directory/extension) — never whether it's _important enough_ for a lean CLAUDE.md to
carry a row for. That importance call is this skill's job, not the script's. Two things to
check every audit:

**Stale placeholder rows.** Grep the table for `TODO: add description`. For each match, decide:

- The file is genuinely worth a row → write the real one-line purpose.
- The file isn't worth tracking in this table at all (e.g. it's already documented elsewhere in
  CLAUDE.md, or it's boilerplate nobody needs to orient on) → don't just delete the row. The
  script rebuilds the table from the filesystem on every commit, so a bare deletion gets the row
  silently re-added with the same placeholder next time the file is touched. Instead, add it to
  the `key-config-excluded` block (create the block if absent, anywhere in CLAUDE.md):

  ```markdown
  <!-- cc-config: key-config-excluded
  path/to/file.ext — one-line reason — YYYY-MM-DD
  -->
  ```

  The path must match exactly what the table used (repo-relative, matching the script's own
  path construction). The reason and date are for human/agent context only — the script only
  reads the path before the first em-dash.

**Excluded-list review.** If a `key-config-excluded` block exists, re-examine every entry:

- If the referenced path no longer exists on disk, remove that entry — it's dead weight.
- If the file has grown in scope or importance since it was excluded (check `git log` for
  significant recent activity, or judge from its current content) such that a row would now
  earn its keep, remove the entry. The next sync run will pick the file back up automatically
  and add it with a placeholder purpose — treat that placeholder the same way as any other
  stale-TODO finding above (write the real description, don't leave it).
- Otherwise leave the entry as-is; don't re-litigate a still-valid exclusion every audit.

### 2b: AGENTS.md audit

- Does it exist? Should it? (yes if multiple AI tools are used in the project)
- Is it genuinely tool-agnostic? (no Claude-specific features like `@`-imports inside AGENTS.md)
- Does it cover: setup commands, architecture boundaries, code style, testing, safety?
- Is there unnecessary duplication between AGENTS.md and CLAUDE.md?

### 2c: Settings audit

**Permissions:**

- Are sensitive files protected by `permissions.deny`? At minimum the real secret-bearing env files (`.env`, `.env.local`, `.env.*.local`, `.env.development`, `.env.production`, `.env.staging`, `.env.test`) and `secrets/**`.
- **Flag a broad `Read(.env.*)` or `Read(./.env.*)` deny rule as a misconfiguration.** That glob also blocks example/template files (`.env.example`, `.env.sample`, `.env.template`, `.env.dist`, `example.env`), which hold no secrets and must stay readable for documentation. Because Claude Code evaluates `deny` before `allow` with no negation in `Read()` rules, a denied path cannot be re-allowed — an `allow(.env.example)` does not override it. Recommend migrating to the enumerated deny list above (leaving example files unmatched), and pairing it with the PreToolUse secret-file guard hook for full `.env.*` coverage with the example carve-out.
- Is `permissions.deny` used instead of the deprecated `ignorePatterns`?
- Are destructive commands blocked? (`rm -rf`, and consider network download commands unless specifically needed)
- Are safe, frequently-used commands in `permissions.allow`? (reduces approval fatigue)

**Hooks (Claude Code):**

- Is there a PostToolUse formatter hook? If a formatter exists in the project but no hook runs it, this is a high-impact gap. Valid formatter targets include code formatters (prettier, ruff, rustfmt, gofmt, php-cs-fixer) and Markdown formatters (prettier on `.md`, `markdownlint --fix`) — don't skip the audit just because the project produces content rather than code.
- Is there a PreToolUse hook protecting sensitive files? (defense in depth beyond `permissions.deny`) A `Read|Edit` guard that blocks `.env`/`.env.*` basenames while carving out `*.example`/`*.sample`/`*.template`/`*.dist`/`example.env` gives broad coverage that the enumerated deny list cannot, since deny rules must leave example files unmatched. See the secret-file guard hook in `/bootstrapping-config`.
- Do all hooks use `|| true` for graceful degradation? **Exception: security hooks must fail closed.** A secret-file guard must exit non-zero (block) on the bad path and must not be softened with `|| true`, or it will pass silently when its dependency (e.g. `jq`) is missing. Only formatter/lint hooks should carry `|| true`.
- Are hooks doing "block at submit" rather than "block at write"? (fewer interrupts, smoother flow)

**Git hooks and hook-manager drift:**

`/bootstrapping-config` creates a project-local `.githooks/pre-commit` that runs `scripts/sync-config-table.sh` and activates it via `git config core.hooksPath .githooks`. If a hook manager like Husky is added later, it takes over `core.hooksPath` — the `.githooks/pre-commit` is still present in the repo but silently stops running. This is a silent drift scenario. Check for it:

1. Detect hook managers:
   - Husky: `husky` in `package.json` devDependencies, or `.husky/` directory present
   - Lefthook: `lefthook.yml` or `lefthook` in devDependencies
   - pre-commit: `.pre-commit-config.yaml`
2. Detect cc-init hook infrastructure: `.githooks/pre-commit` exists and references `sync-config-table`
3. If both are present, flag as **conflict** and propose one of these migrations:
   - **Migrate to the hook manager** (recommended if the hook manager is the project standard): move the `sync-config-table` invocation into the hook manager's pre-commit config (e.g., append it to `.husky/pre-commit`), then delete `.githooks/pre-commit` and — if empty — the `.githooks/` directory. Optionally run `git config --unset core.hooksPath` so the setting doesn't confuse future contributors.
   - **Keep the project-local hook** (only if the hook manager was added by mistake or is being removed): leave `.githooks/` in place and note that the user needs to resolve which hook system owns `core.hooksPath`.
4. Also check if `scripts/sync-config-table.*` exists but `.githooks/pre-commit` is missing entirely — the script is orphaned and never runs. Same proposal: wire it into the active hook manager or recreate the `.githooks/` setup.
5. If the sync script exists in a variant that doesn't match the filesystem conventions of the project (e.g., a `.sh` script in a Node-only project where the team prefers `.js`), note it as a nice-to-have for harmonization but don't force the change.

**Sync script version drift:**

`scripts/sync-config-table.sh` is copied into a project once, at init time, and nothing updates it afterwards — a plugin update does not reach into repos that were already initialized. Bug fixes to the script therefore only land when this skill runs. Check for it on every audit:

1. Read the version marker from the project's copy: `grep -m1 'sync-config-table-version:' scripts/sync-config-table.sh`. A copy predating the versioning scheme has no marker — treat that as version 0.
2. Read the marker from the plugin's canonical copy. It lives in the sibling `bootstrapping-config` skill directory, i.e. `../bootstrapping-config/scripts/sync-config-table.sh` relative to this skill's own directory. If you cannot locate it, say so and skip this check — do not fall back to guessing a version or reconstructing the script from memory.
3. If the project's version is lower or absent, the copy is stale. **Show the user a diff of the two files and ask before overwriting.** Never overwrite silently: the marker only tells you the copy is old, not whether the user hand-edited it, and an unattended clobber would discard their changes without a trace.
4. On confirmation, copy the plugin's file over the project's and re-apply `chmod +x`. Report which version replaced which.
5. If the versions match, say nothing — this is a no-op on an up-to-date repo, and a clean audit shouldn't spend the user's attention on it.

If the diff shows the project's copy was customized (scan rules added or removed rather than just older core logic), point out that the canonical script guards every scan with a directory check and self-adapts, so the customization is probably unnecessary — but let the user decide. Preserving a deliberate local fork is better than a refresh they didn't expect.

**Secret scanning in pre-commit hooks:**

Check if the project's active pre-commit hook (whether in `.githooks/`, `.husky/`, lefthook, or pre-commit framework) includes a secret scanner like gitleaks. If the project has sensitive files (`.env`, API keys, credentials) or `permissions.deny` entries for secrets, but no pre-commit secret scanning, recommend adding gitleaks to the active pre-commit hook:

```bash
gitleaks git --pre-commit --staged || exit 1
```

This catches secrets committed by both Claude Code and the user. Unlike `permissions.deny` (which only prevents Claude from reading existing secrets), gitleaks prevents anyone from committing new ones. Note: gitleaks must be installed separately (`brew install gitleaks`, `apt install gitleaks`, or via the project's CI toolchain). Only recommend — never install tools on the user's machine without explicit permission.

**Environment variables:**

- Is `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` set? This only affects _proactive_ compaction, which itself only triggers under specific conditions (cloud sessions, `CLAUDE_CODE_AUTO_COMPACT_WINDOW` being set, or specific model versions without extended context). On a typical local session on the current default model, proactive compaction already applies at the model's own default threshold, so this override is very likely a no-op there. If you find it set on a plain local setup, flag it as probably-ineffective and not worth keeping. Only treat it as a legitimate, deliberate tuning if the project actually runs cloud sessions or an older model configuration where the override demonstrably applies.
- Is `MAX_THINKING_TOKENS` set? Consider `10000` (down from the model's default cap of 31999) to lower the thinking-token cap. This reduces the ceiling, not necessarily actual usage — don't cite a specific savings percentage.
- Is `CLAUDE_CODE_MAX_OUTPUT_TOKENS` set? Consider `16000` to prevent unnecessarily verbose responses.
- Is `CLAUDE_CODE_SUBAGENT_MODEL` set? `haiku` meaningfully lowers cost for exploration subagents (Haiku pricing is a fraction of Sonnet/Opus) — avoid citing a specific percentage, it varies by workload. Note this env var overrides every subagent's own `model:` frontmatter, so check whether that's desired for any judgment-heavy analysis subagents the project itself defines.
- Are `alwaysThinkingEnabled` and `effortLevel` (in `settings.json`, not `env`) set sensibly? These control thinking budget more directly than `MAX_THINKING_TOKENS` and independently of any autocompact override. `alwaysThinkingEnabled: true` at `effortLevel: high` pushes token usage per turn up substantially and can make context fill (and any compaction) happen far sooner than expected — flag this combination unless the user has a specific reason for always-on deep reasoning. Default recommendation: leave `alwaysThinkingEnabled` unset/`false` and `effortLevel` at `medium`.

**Auto-pull on session start:**

`cc-config` bundles a `SessionStart` hook (`plugins/cc-config/hooks/auto-git-pull.sh`) that fetches and fast-forwards the current branch at the start of every session — but only when the project has opted in via `CC_CONFIG_AUTO_GIT_PULL=true` in the `env` block of `.claude/settings.local.json`. It never merges or rebases; on divergence it skips and surfaces a message instead. This is a personal multi-machine workflow preference, not a project convention — never write it to the committed `.claude/settings.json`, and never enable it without asking.

Check whether the flag is set. If it is **not** set and the project is a git repo with a remote, surface it as a nice-to-have suggestion (see below) rather than enabling it unprompted — most projects don't need it, and it's the kind of thing only the user asking to work across multiple machines actually wants.

**`.claudeignore`:**

Check whether a `.claudeignore` file exists. This file (`.gitignore` syntax) tells Claude Code which paths to skip entirely when indexing the project, reducing invisible startup token overhead.

Flag as a "should fix" if:

- The repo has `node_modules/`, `vendor/`, `.venv/`, or other dependency trees present and no `.claudeignore` excludes them.
- Build output directories exist (`dist/`, `build/`, `.next/`, `target/`, `_site/`, `coverage/`) and are not excluded.
- Large binary or media asset folders are present that Claude would never usefully read.

Flag as "nice to have" if the repo is small and tidy but could benefit from exclusions as it grows.

Run `/context` in a fresh session to get the current startup token count — if it exceeds ~10,000 tokens before any user message, a missing `.claudeignore` is a likely contributor.

### 2d: MCP audit

- How many servers are active? (5–10 is the sweet spot for most projects)
- Are all servers actually used? Check if they match the project's real needs.
- Are secrets hardcoded or using `${VAR}` expansion?
- Is the project using `.mcp.json` (project-scope, recommended) or `~/.claude.json` (user-scope)?
- Could any MCP server be replaced by a simpler CLI tool? (e.g., `gh` CLI instead of GitHub MCP for basic operations — no permanent context overhead)
- Is Tool Search / deferred tool loading active? Current Claude Code models can defer MCP tool schemas and fetch them on demand once tool descriptions get large — the exact model gating and threshold aren't reliably documented, so don't cite specific numbers; just note whether the project's tool count is small enough that this isn't a concern, or large enough to be worth checking.

### 2e: Skills audit

- Are there skills that duplicate CLAUDE.md content? → Deduplicate.
- Are skills with side effects (deploy, commit, publish) using `disable-model-invocation: true`?
- Are read-only analysis skills using `allowed-tools` restrictions?
- Are there `.claude/commands/` files that should be migrated to the skills format?
- Is skill content concise? (target <50 lines per SKILL.md, split if longer)
- If OpenSpec is used: are OpenSpec skills duplicated across multiple tool directories (`.claude/`, `.codex/`, `.gemini/`, `.github/`)? If so, flag this as a maintenance risk and suggest consolidation.
- Do skills that produce domain-specific output correctly separate context by scope? Check for three types of violations:
  - **Company-level knowledge inlined or duplicated per-skill**: brand voice, company profile, buyer personas, architecture decisions belong in the registered context location (`context/` by convention, project root). Consolidate and register in the `## Context files` table in CLAUDE.md — update once, every skill reflects the change.
  - **Format-level knowledge in the shared context location**: a whitepaper structure guide or blog length rules belong inside the skill's own folder, not the shared context folder.
  - **Campaign/feature briefings in the shared context location**: initiative-specific briefings belong in the relevant project subfolder, not the company-scoped shared folder.
- If a `## Context files` table exists, validate its rows:
  - **Malformed rows**: don't follow `Label | File | Summary` (missing or extra cells).
  - **Orphaned paths**: the `File` value doesn't resolve to an existing file. Check with `test -f`, resolving the path relative to the CLAUDE.md file that contains the table — not the repository root (paths follow the same resolution rule as `@`-imports, so a nested CLAUDE.md's table is relative to its own directory).
  - **Duplicates**: two rows share the same Label or the same File path.
  - **Vague summaries** (soft check — human judgment): a summary too generic to act as a relevance signal, e.g. "Writing style guidelines for the company" instead of "Formal German, em-dash preferred, no exclamation marks — all corporate copy." Flag as a suggestion, not a hard rule.
- Does each skill end with a feedback step? A skill that closes by asking "Did this output meet your expectations? If not, I'll log a correction to `.claude/learnings.md`" makes the learnings loop active rather than passive — corrections are solicited at the point of delivery, not just accumulated from future mishaps. Flag absent feedback steps as "nice to have."
- For each custom subagent in `.claude/agents/*.md` (project-local) or, in a plugin repo, `plugins/*/agents/*.md` (plugin-bundled): is it actually referenced anywhere (grep skills, hooks, and CLAUDE.md for its name in an `Agent(...)`/`subagent_type:` context — for a plugin-bundled agent, that's its plugin-scoped `plugin-name:agent-name` form)? An unreferenced custom agent is dead weight the same way an unused MCP server is. Does its `tools:` allowlist match what it actually needs — a subagent with side effects (writes, deploys) granted `Write`/`Edit`/`Bash` it doesn't use is worth flagging the same way an overbroad skill `allowed-tools` list would be.

### 2f: Multi-tool consistency check

If the project uses multiple AI tool directories:

- Is there a single source of truth (ideally AGENTS.md) that all tools reference?
- Are there contradictions between tool-specific configs?
- Is duplicated content maintained in sync, or is it drifting?

### 2g: Learnings review

If `.claude/learnings.md` exists:

1. Read all entries.
2. Group similar entries to identify recurring patterns (3+ similar corrections suggest a real gap in the config).
3. For each recurring pattern, propose one of:
   - Adding a concrete rule to CLAUDE.md (if it's a universal project convention).
   - Adding it to an existing or new skill (if it's domain-specific or rarely needed).
   - Adding it as a hook (if it's something that should happen deterministically, not by instruction).
4. For one-off entries that don't recur, propose deleting them.
5. Present the full list to the user grouped as "promote to config" vs "delete as one-off", with rationale for each. Wait for approval before changing anything.

If `.claude/learnings.md` does not exist but CLAUDE.md also has no Learnings section, suggest adding the Learnings section to CLAUDE.md:

```markdown
## Learnings

When the user corrects a mistake or points out a recurring issue, append a one-line
summary to .claude/learnings.md. Don't modify CLAUDE.md directly.
```

### 2h: Headroom audit

Headroom is an optional in-flight compression layer that reduces context window usage by compressing tool outputs, Bash results, logs, and code before they reach the model — a different optimization level from env vars and `.claudeignore`, which operate at startup and configuration time.

Check whether `.headroom/` exists with Glob on `.headroom/*`. Then run:

```bash
which headroom 2>/dev/null && headroom --version 2>/dev/null | head -1 || echo "headroom-not-installed"
python3 -c "import sys; print('python-ok' if sys.version_info >= (3, 10) else 'python-too-old')" 2>/dev/null || echo "python-unavailable"
```

**If Headroom is installed:**

1. **`.gitignore` check**: Headroom stores machine-local data in `.headroom/` — session caches and `.headroom/CLAUDE.local.md` (machine-local learnings). These must not be committed: they are per-machine, ephemeral, and will conflict across clones. If `.headroom/` is not in `.gitignore`, flag as "should fix."
2. **Integration mode**: Detect which mode is in use:
   - _MCP mode_: look for a Headroom entry in `.mcp.json`. Verify it is still in the active server list; stale entries add tool-count overhead for nothing.
   - _Proxy/wrap mode_: `headroom wrap claude` or `headroom proxy --port 8787 --code-aware` must be run before each session. If this is not documented in CLAUDE.md (or a project README), note it — teammates will not know to start it.
3. **Code-aware flag**: For code compression to activate, the proxy must be started with `--code-aware`. Without it, code files produce `tokens_saved: 0`. Flag as a note if the user is on proxy mode and this flag is not documented.
4. **Learnings coexistence**: Headroom's `.headroom/CLAUDE.local.md` and cc-config's `.claude/learnings.md` serve different purposes and should both be kept. Headroom's file captures machine-local session patterns; cc-config's file captures explicit user corrections and is team-shared (committed to git, feeds the `auditing-config` promotion cycle). Do not consolidate them.

**If Headroom is not installed and Python 3.10+ is available:**

Add to "Nice to have." Do **not** add if Python is unavailable or below 3.10, or if the project is known to run exclusively in sandboxed/remote environments (CI pipelines, Claude Code on the web) — Headroom requires a persistent local process and is incompatible with those contexts.

**If Python is unavailable or below 3.10:**

Skip. Do not mention Headroom.

### 2i: Cross-file duplication (hierarchical CLAUDE.md trees)

Relevant when a project uses multiple CLAUDE.md files across folder levels (common with the cc-content context-TOC pattern) — Claude Code auto-loads every CLAUDE.md up the directory chain, so content should live once at the shallowest level it applies to.

1. Discover all CLAUDE.md files in the tree: `find . -name CLAUDE.md -not -path '*/node_modules/*' -not -path '*/vendor/*'`
2. Read all discovered files.
3. Compare content across levels — not just identical strings, but near-duplicate rules, conventions, or command lists restated at multiple levels.
4. Distinguish **acceptable repetition** (a one-line pointer restating scope, e.g. "This file covers the `api/` package only") from **true duplication** (the same rule or command list copy-pasted across levels).
5. Flag true duplicates: content should move to the shallowest common ancestor; deeper-level files should only add what's specific to that scope.

## Step 3: Generate findings report

Using the metrics and findings gathered in Step 1–2, organize findings into three categories:

### Must fix (security or correctness issues)

- Missing permissions.deny for sensitive files
- Hardcoded secrets in config files
- Deprecated patterns (ignorePatterns, npm-installed Claude Code)
- Contradictory instructions
- Hook-manager conflict: `.githooks/pre-commit` present alongside an active hook manager (the sync script is not running)
- CLAUDE.md documents a command that doesn't exist in the actual manifest (renamed script, deleted target, wrong path) — Claude will confidently run something that fails
- CLAUDE.md references a file path (outside `@`-imports and the `## Context files` table) that doesn't resolve

### Should fix (quality and cost improvements)

- CLAUDE.md bloat (>80 lines without good reason)
- Missing formatter hook
- Missing cost-optimization env vars
- Redundant content between files
- Skills without proper frontmatter guards
- Learnings entries that should be promoted to CLAUDE.md or a skill
- Orphaned `scripts/sync-config-table.*` with no active hook wiring
- `scripts/sync-config-table.sh` older than the plugin's canonical copy (stale or missing version marker) — the repo is stranded on a version with known bugs
- `DESIGN.md` present at project root but not referenced via `@DESIGN.md` in CLAUDE.md (Claude won't apply the design system without the pointer)
- Context files present in the registered context location but no `## Context files` table in CLAUDE.md — skills cannot discover context files without this table
- `## Context files` table has malformed rows (not `Label | File | Summary`), duplicate Label/File values, or File paths that don't resolve to an existing file
- `## Context files` table exists but is missing the `<!-- cc-config: context-toc-registered -->` marker comment right after the heading (v4+ `sync-config-table.sh` greps for this exact string, not the heading text, to decide whether `context/` files belong in `## Key Config Files` too — without the marker, the sync script will re-list every context file there with a generic placeholder, duplicating the registered table). Add the marker; don't rename or reword it.
- `## Key Config Files` table lists individual `context/*.md` files with a generic/placeholder Purpose even though a populated `## Context files` table already registers them with real summaries — a sign the marker is missing or `sync-config-table.sh` predates v4
- `## Key Config Files` table has one or more `TODO: add description` rows (see 2a-bis) — write the real description, or move the file to the `key-config-excluded` block if it's not worth a row at all
- `key-config-excluded` block (see 2a-bis) has an entry whose path no longer exists, or whose file has demonstrably grown important enough to reconsider
- Headroom installed but `.headroom/` not in `.gitignore`: machine-local Headroom files (session caches, `.headroom/CLAUDE.local.md`) must not be committed — they are per-machine and will break other clones
- True duplicate content across nested CLAUDE.md files in a hierarchical tree (see 2i) — should live once at the shallowest common ancestor

### Nice to have (polish)

- Missing progressive disclosure for reference docs
- Missing compact instructions
- Missing Learnings section in CLAUDE.md
- Skills that could be created for recurring workflows
- MCP servers that could be added or removed
- Missing secret scanner (gitleaks) in pre-commit hook
- Sync script format mismatch with project conventions (e.g., `.sh` in a Node-only repo)
- Skills producing domain-specific output without referencing the registered context location (`context/` by convention, project root) — company-level knowledge duplicated or inlined per-skill
- Context scope violations: company-level knowledge buried in campaign subfolders, or format-level guidelines in the shared context location instead of the relevant skill's folder
- `## Context files` table summaries too vague to act as a relevance signal for skills (soft check — human judgment, e.g. "Writing style guidelines" instead of naming the specific tone, audience, or rules)
- CLAUDE.md stack/version claims that don't match the actual dependency manifest (e.g., states "Node 16" while `package.json` `engines` says `>=20`)
- Multi-level folder project without hierarchical CLAUDE.md files: if the repo has campaign, feature, or package subfolders where context meaningfully changes, each level should have its own CLAUDE.md that @-imports the relevant context for that scope — this lets Claude inherit all relevant context when started in any subfolder, without skills needing hard-coded paths to shared files. Any `## Context files` table in a nested CLAUDE.md follows the same path convention as the root one: `File` values are relative to that CLAUDE.md's own location, not the repository root.
- Skills missing a terminal feedback step that solicits corrections into the learnings loop
- PDFs, DOCX files, or HTML pages referenced in CLAUDE.md or context files without Markdown equivalents: converting them saves significant tokens (HTML→Markdown ~90% reduction, PDF→Markdown ~65–70%, DOCX→Markdown ~33%). Tools like Pandoc, Docling, or `markitdown` convert in seconds. Flag any such files found in the registered context location or referenced via `@`-imports
- Missing `.claudeignore` startup token check: suggest the user run `/context` in a fresh session to measure actual startup overhead — if high, a missing or incomplete `.claudeignore` is a likely cause
- Headroom not installed but Python 3.10+ is available (and the project is not exclusively run in sandboxed/remote environments): Headroom compresses tool outputs, Bash results, and code in-flight before they reach the model — a different optimization level from env vars and `.claudeignore`. Real-workload savings: 73–92% on code-search and log-heavy tasks. Output tokens cost 5× more than input on Opus-class models, so in-flight compression compounds quickly. Install: `pip install "headroom-ai[all]"`. Start with `headroom wrap claude` (quickest path) or `headroom proxy --port 8787 --code-aware` (proxy mode; `--code-aware` is required for code compression). Run `headroom perf` after a few sessions to measure savings. Important constraint: requires a persistent local process — not compatible with remote/sandboxed sessions (Claude Code on the web, CI pipelines). If the project is used in both local and remote contexts, Headroom benefits only the local sessions.
- `CC_CONFIG_AUTO_GIT_PULL` not set and the project is a git repo with a configured remote: ask whether the user works on this repo from multiple machines and forgets to `git pull` before starting a session. If yes, offer to set `CC_CONFIG_AUTO_GIT_PULL=true` in the `env` block of `.claude/settings.local.json` (create the file if absent) so the bundled `auto-git-pull.sh` `SessionStart` hook fast-forwards the branch automatically, skipping (with a message) if history has diverged. Never enable this without asking, and never write it to the committed `.claude/settings.json`.

Present the findings to the user as a concise list, grouped by category. For each finding, state: what the issue is, why it matters, and what you'd change. Ask for approval before making changes.

### Config health score

Compute a single score from the categorized findings above — it reads directly off the counts you already produced, not a separate rubric:

```
score = max(0, 100 − 10 × must_fix_count − 4 × should_fix_count − 1 × nice_to_have_count)
```

Report this score once now (the "before" score) and again in Step 5 after approved changes are applied (the "after" score), so the user sees a concrete before/after (e.g. "Config health: 62/100 → 91/100") rather than only a word-count delta.

## Step 4: Apply approved changes

Make the approved changes. For each file modified:

- Show a before/after summary (not full diffs for large files — just the key changes).
- Explain briefly what changed and why.

When applying learnings review results:

- For entries promoted to CLAUDE.md or a skill, remove them from `.claude/learnings.md`.
- For entries marked as one-off, remove them from `.claude/learnings.md`.
- If all entries are processed, delete `.claude/learnings.md` entirely (it will be recreated naturally when the next correction occurs).

When resolving hook-manager conflicts:

- If migrating to Husky: append the sync-script call to `.husky/pre-commit` (create it if missing), delete `.githooks/pre-commit`, remove the empty `.githooks/` directory, and suggest the user runs `git config --unset core.hooksPath` on each clone.
- If migrating to Lefthook or pre-commit: add the appropriate entry to the respective config file instead.
- Never delete `scripts/sync-config-table.*` itself — the script is still useful, only the wiring changes.

When resolving the Headroom gitignore gap:

Append `.headroom/` to `.gitignore`. Place it under the existing Claude Code personal-files block if one exists, or at the end of the file with a short comment:

```
# Headroom — machine-local session cache and learnings
.headroom/
```

Do not create `.headroom/` or any files inside it — Headroom manages that directory itself.

When enabling auto-pull on session start:

Add or merge `env.CC_CONFIG_AUTO_GIT_PULL: "true"` into `.claude/settings.local.json` (create it with `{"env": {"CC_CONFIG_AUTO_GIT_PULL": "true"}}` if the file doesn't exist yet; merge into the existing `env` block if it does — don't clobber other keys). Confirm this file is already covered by `.gitignore` (`.claude/settings.local.json` is part of the standard ignore block) so the flag stays machine-local and never lands in a shared config.

Preserve things that work well. Don't refactor for the sake of refactoring. If an existing config is well-structured and correct, say so and move on.

## Step 5: Final summary

After all changes:

1. List every file modified or created, with one-line descriptions of changes.
2. Report the new metrics: CLAUDE.md word count, number of active MCP servers, hooks configured, etc.
3. Compare key metrics to before (e.g., "CLAUDE.md: 1,850 words → 480 words").
4. Recompute the config health score from whatever findings remain unresolved and report the before/after (e.g. "Config health: 62/100 → 91/100").
5. If learnings were reviewed: report how many entries were promoted, how many deleted, and how many remain.
6. Note anything you deliberately left unchanged and why.
7. Update the audit marker in CLAUDE.md so the bundled `SessionStart` staleness hook (see
   "Audit staleness reminder" below) has a fresh baseline to compare future commits against:

   ```bash
   date +%Y-%m-%d      # today's date
   git rev-parse HEAD  # current commit SHA
   ```

   Write or replace the line `<!-- cc-config: last-optimize-run: YYYY-MM-DD <sha> -->`
   anywhere in CLAUDE.md (reuse the existing line if one is already present, e.g. right after
   the `## Key Config Files` table, alongside `key-config-excluded` if that block exists —
   don't scatter multiple copies of this marker across the file). This step runs even if this
   audit found nothing to fix — a clean audit still resets the baseline.

8. Suggest running `/auditing-config` again periodically (e.g., after major features, after a few weeks of work) to prevent config drift. Mention that the bundled `SessionStart` hook will also nudge automatically once enough commits accumulate since the marker just written, so this is a backstop, not the primary way it's kept current.
9. Remind the user to commit the changes.

### Audit staleness reminder

`cc-config` ships a `SessionStart` hook (`plugins/cc-config/hooks/check-optimize-staleness.sh`,
declared in `plugins/cc-config/hooks/hooks.json`) that fires in every project the plugin is
active in — no per-repo `.claude/settings.json` wiring needed, since plugin-declared hooks
apply automatically wherever the plugin is installed. On session start it reads the
`last-optimize-run` marker this step writes, compares it against the repo's current commit
count and date, and — only if the project has drifted noticeably since that baseline (default
thresholds: 20+ commits, or 14+ days with at least one new commit) — emits a short reminder
suggesting `/auditing-config`. It never blocks anything and stays silent otherwise,
including in repos that don't use `cc-config` at all (it only speaks up if it also finds
`scripts/sync-config-table.sh`, i.e. clear evidence the project already opted in).
This step is what keeps that hook's comparison meaningful — without a fresh marker, every
session in an active repo would eventually trip the threshold and nag regardless of how
recently an audit actually ran.

## Common optimization patterns

These are recurring improvements you'll often apply:

**CLAUDE.md → Skills migration:**
When CLAUDE.md contains domain knowledge that's only needed for specific tasks, extract it into a skill. The skill loads on demand (~100 tokens metadata at rest), while CLAUDE.md content loads every message.

**Monolithic docs → Progressive disclosure:**
Replace inline documentation in CLAUDE.md with `@`-import pointers:

```markdown
### API Architecture — @docs/api-architecture.md

**Read when:** Adding or modifying API endpoints
```

**AGENTS.md as single source of truth:**
If the project has both CLAUDE.md and AGENTS.md with overlapping content, consolidate the universal parts into AGENTS.md and reduce CLAUDE.md to a slim adapter:

```markdown
@AGENTS.md

## Claude-Code-specific

- <only Claude-specific additions here>
```

**OpenSpec integration:**
If OpenSpec is present, CLAUDE.md should reference it rather than duplicate project context:

```markdown
@openspec/project.md
```

**Hook-ification of repeated instructions:**
If CLAUDE.md says "always run prettier after editing" — that's a hook, not an instruction. Replace the instruction with a deterministic PostToolUse hook and remove the line from CLAUDE.md.

**Learnings graduation:**
When `.claude/learnings.md` has accumulated entries, recurring patterns graduate into CLAUDE.md rules, skills, or hooks. One-off corrections get deleted. The file stays lean or gets removed entirely until the next correction cycle.

**Hook-manager migration for sync-config-table:**
When a project gains Husky or another hook manager after `/bootstrapping-config` was used, the `.githooks/pre-commit` goes silent because `core.hooksPath` is taken over. Migrate the sync script into the active hook manager's pre-commit hook and remove the now-dead `.githooks/` directory.

## What NOT to do

- Don't refactor things that work well. If a config is correct and clean, say so.
- Don't add MCP servers speculatively. Only suggest servers that address a concrete gap.
- Don't create skills for workflows that haven't been repeated yet.
- Don't modify user-level files (`~/.claude/CLAUDE.md`, `~/.claude.json`) without explicit permission.
- Don't remove functionality. If something serves a purpose, keep it — just optimize how it's expressed.
- Don't make the config dependent on tools or servers the user hasn't installed.

## Feedback

**Auto-store phase.** Before asking for feedback, review this run. For each qualifying observation, append one tagged line to `.claude/learnings.md` (create with standard header if missing). Skip entries promoted or deleted by 2g in this run:

```text
[cc-config:auditing-config] <concise fact about this project> — <YYYY-MM-DD>
```

Qualifies: something about this project that differs from what this skill assumes on a generic project; a suggestion the user explicitly accepted or rejected that deviates from skill defaults; a constraint or fact discovered that would change how this skill behaves next time.

Does not qualify: standard skill behavior applied without deviation; facts already present in CLAUDE.md, AGENTS.md, or other config files; anything a reader could determine from the repo without this skill having run; facts semantically equivalent to any existing `.claude/learnings.md` entry — when in doubt, skip.

Before appending, use Glob on `.claude/learnings.md` to check whether the file exists.

Standard header when creating the file:

```markdown
# Learnings

Corrections and observations collected during configuration sessions.
Entries are tagged by skill and dated.

---
```

**Explicit feedback.** After the auto-store phase, ask:

> "Did this optimization meet your expectations? If anything needs adjusting, share it here — or press Enter to finish."

- If the user **provides a correction**: append it as a tagged entry using the same format and qualification criteria above. Confirm total entries written across both phases: "✓ N learning(s) saved to `.claude/learnings.md`."
- If the user **confirms quality or skips**: if any entries were auto-stored, confirm "✓ N learning(s) auto-saved to `.claude/learnings.md`." Then exit. If nothing was stored, skip the confirmation and exit directly.

> **Note:** Learnings are automatically recalled at the start of the next skill run. Run `/auditing-config` periodically to promote recurring patterns into the configuration.
