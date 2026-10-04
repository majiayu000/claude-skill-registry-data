---
name: claude-md-rules-creator
description: "Write or audit CLAUDE.md, CLAUDE.local.md and .claude/rules files: scope, paths, imports, size, and why a rule is ignored."
when_to_use: "Use when creating or editing any of those files, or when Claude is not following one."
disable-model-invocation: false
---

# CLAUDE.md and Rules Creator

You are about to write or edit a CLAUDE.md, CLAUDE.local.md, or `.claude/rules/*.md` file. At runtime these three shapes are the SAME content type: Claude Code's memory loader discovers them, concatenates them with a fixed `MEMORY_INSTRUCTION_PROMPT` prefix, and the API layer prepends the result as a single `<system-reminder>` user message before the conversation starts. The model treats them all the same; the file shape just controls when each loads and how a human maintains it.

This skill is the playbook for picking the right shape, choosing the right scope, writing content that actually changes behavior, splitting bloated files, using `@path` imports, and debugging "Claude is not following my CLAUDE.md". Target is Opus 5.5 (`model: opus` on Claude Code 2.1.280). The same rules work on Sonnet 5 and Haiku 4.5, whose built-in prompt already carries more of what a CLAUDE.md would otherwise say (principle 9).

## Three jobs, not one

Writing a CLAUDE.md or rule splits into three tasks. Conflating them is the most common authoring mistake.

1. **Surrounding skill shape.** None. CLAUDE.md and `.claude/rules/*.md` are not skills, not commands, not agents. They are plain markdown files the memory loader picks up. No frontmatter fields apply except `paths:` (only on `.claude/rules/*.md`). Route through `ac:skill-creator` ONLY if you are wrapping CLAUDE.md authoring inside a custom slash command or skill.
2. **CLAUDE.md / rule shape.** Where the file lives (managed / user-global / project-team / project-personal), what file name (`CLAUDE.md` / `CLAUDE.local.md` / `.claude/rules/<topic>.md`), `paths:` frontmatter for rules, `@path` imports, HTML comments. This file teaches that.
3. **Body content.** The markdown text the model reads. This is a standing instruction set, a prompt at runtime. Route through `ac:prompt-writer` for prompt architecture, snippets, and per-model tuning.

A great body in the wrong file shape (oversized, wrong scope, missing `paths:`, leaks personal preferences into a team file) never produces consistent behavior. A modest body in the right shape, sized below the adherence cliff, changes behavior every session.

## What CLAUDE.md actually is, mechanically

The lifecycle:

1. **Discovery.** At session start, the loader walks: managed → user → project (root → cwd) → local → AutoMem/TeamMem. Within each project directory: `CLAUDE.md` first, then `.claude/CLAUDE.md`, then `.claude/rules/*.md` (unconditional only - files without `paths:` or with `paths: ['**']`), then `CLAUDE.local.md`.
2. **Frontmatter strip + HTML comment strip.** Each file's content is processed: YAML frontmatter is parsed (only `paths:` is meaningful), and block-level HTML comments (`<!-- ... -->`) are stripped. Comments inside fenced code blocks survive. Inline HTML comments inside paragraphs survive.
3. **Conditional rule deferral.** `.claude/rules/*.md` files WITH a `paths:` frontmatter are held back from the initial concatenation. They activate later when Claude reads a file matching their glob.
4. **Concatenation.** Eligible files are formatted as `Contents of <absolute-path><description>:\n\n<content>` (description varies by type - "user's private global instructions for all projects", "project instructions, checked into the codebase", "user's private project instructions, not checked in", "user's auto-memory, persists across conversations"). All entries are joined with `\n\n`, prefixed with `MEMORY_INSTRUCTION_PROMPT`.
5. **Injection into the API call.** On 2.1.280 the files travel as an `instructions` attachment and render as their own `<system-reminder>` block in the first user message, with `isMeta: true` (the UI hides it; the model sees it). The block opens with `MEMORY_INSTRUCTION_PROMPT` and nothing after it softens that; the "may or may not be relevant" line now closes a separate block (`userEmail` and similar), not this one.
6. **Compact behavior.** On `/compact` or auto-compact, the runtime wipes the memory-file cache. The NEXT turn re-reads project-root CLAUDE.md, CLAUDE.local.md, and unconditional rules from disk and re-injects them. Path-scoped rules and nested-subdir CLAUDE.md files lazy-loaded into message history during the session are summarized away and reload only on the next matching file touch.

The model NEVER sees CLAUDE.md as the system prompt. It sees a `<system-reminder>`-wrapped meta-message that opens "Codebase and user instructions are shown below ... OVERRIDE any default behavior". Binding, but not system. This is the single most-misunderstood mechanic; debugging "Claude is not following my CLAUDE.md" always starts here.

## Decision flow

Route by the user's request.

```
Is CLAUDE.md / rules the right tool at all?
├── Single fact never changes; behavior must hold every session → CLAUDE.md, continue.
├── Workflow with steps, invocable on demand → SKILL, route through `ac:skill-creator`.
├── User-typed `/name [args]` action → COMMAND, route through `ac:command-creator`.
├── Deterministic guarantee (must fire on every edit, no model judgment) → HOOK, configure in settings.json.
├── Custom-context worker → SUBAGENT, route through `ac:agent-creator`.
└── Standing rule, conventions, what-to-avoid, project facts → CLAUDE.md / rule, continue.

Which file shape inside the CLAUDE.md layer?
├── Universal rule, every session needs it, file stays under 200 lines → inline in `./CLAUDE.md` (project) or `~/.claude/CLAUDE.md` (user).
├── Personal override of a team rule → `./CLAUDE.local.md` (project-personal, gitignored).
├── Topic-focused team rule, want its own file → `./.claude/rules/<topic>.md` (no `paths:`, loads at session start).
├── Path-conditional rule (only matters in `src/api/`, only frontend, only migrations) → `./.claude/rules/<topic>.md` with `paths:` frontmatter.
├── Personal preference across all projects → `~/.claude/CLAUDE.md` or `~/.claude/rules/<topic>.md`.
└── Org-wide policy → managed CLAUDE.md (admin deploys).

Is this an audit or fix of an existing file?
├── YES → read `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` first, then the specific reference as the symptom dictates.
└── NO → walk the Workflow below.
```

## Frontmatter: only one shape takes any

CLAUDE.md and CLAUDE.local.md have NO frontmatter. They are pure markdown. Anything that looks like YAML at the top is treated as content.

`.claude/rules/<topic>.md` files accept ONE frontmatter field: `paths:`.

| Field | Required? | Behavior |
|-------|-----------|----------|
| `paths:` | optional | Comma string or YAML list of gitignore-syntax globs. Without it, the rule loads at session start with the same priority as `.claude/CLAUDE.md`. With it, the rule loads on demand when Claude reads a file matching any glob. `paths: ['**']` is treated identically to no `paths:` |

Everything else (`name`, `description`, `model`, `effort`, etc.) is ignored by the memory loader. Do not add fields that mean nothing in this context.

> **Escape convention used in this documentation.** This SKILL.md is itself a skill body inside a plugin. The Claude Code loader substitutes plugin-context tokens before injecting the body. Real path references in this file using `${CLAUDE_SKILL_DIR}/references/<file>.md` stay literal so the loader resolves them to actual files the model can Read. Documentation-context references that NAME the tokens without using them use the HTML entity `&#36;` so the docs survive intact. In CLAUDE.md and rule files you author, none of this applies, those files do not go through any substitution pass; tokens stay literal.

## Where each file lives (verified paths)

| Type | Path |
|------|------|
| Managed CLAUDE.md | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL: `/etc/claude-code/CLAUDE.md`; Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` |
| Managed rules dir | `<managed-policy-path>/.claude/rules/` |
| User CLAUDE.md | `~/.claude/CLAUDE.md` |
| User rules dir | `~/.claude/rules/` - **not** `~/.claude/.claude/rules/` |
| Project CLAUDE.md | `<dir>/CLAUDE.md` AND `<dir>/.claude/CLAUDE.md` (both loaded per directory in the walk) |
| Project rules dir | `<dir>/.claude/rules/` (per directory in the walk; recursive into subdirs) |
| Local CLAUDE.local.md | `<dir>/CLAUDE.local.md` (per directory in the walk; gitignored by convention) |
| Auto memory entrypoint | `~/.claude/projects/<project>/memory/MEMORY.md` (200 lines / 25KB cap) |

The asymmetry to remember: USER rules live one level shallower than PROJECT rules. User: `~/.claude/rules/<topic>.md`. Project: `<dir>/.claude/rules/<topic>.md`.

## The four scopes

The runtime treats CLAUDE.md content identically regardless of scope. The scopes differ in WHO sees the file and WHEN it gets loaded.

| Scope | Path | Audience | Where it lives | Loaded |
|-------|------|----------|----------------|--------|
| Managed policy | platform-specific path above | Every user on the machine; cannot be excluded by user settings | Org-deployed via MDM, Group Policy, Ansible | Always |
| User global | `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md` | Just you, every project on this machine | Your dotfiles (personal); not in any repo | Always |
| Project team | `./CLAUDE.md`, `./.claude/CLAUDE.md`, `./.claude/rules/*.md` | Everyone working on this repo | Committed to source control | Always (walked from filesystem root down to cwd) |
| Project personal | `./CLAUDE.local.md` | Just you, just this project | Add to `.gitignore`; never committed | Always |

The litmus test: if the team gets value from this rule, it is project-team. If it is yours alone, it is user-global (cross-project) or project-personal (this project only). Org-wide compliance and security rules go to managed policy.

Full scope deep-dive, AGENTS.md interop, worktree handling, monorepo `claudeMdExcludes`, and `--add-dir` behavior: `${CLAUDE_SKILL_DIR}/references/scopes.md`.

## Core principles

These ten rules drive every authoring decision. Detail and source in the references.

1. **Concise wins adherence.** Anthropic's docs target "under 200 lines per CLAUDE.md". Adherence drops as files grow; over 200 lines the model notices less of what is there. The hard cap is 40,000 characters per file (`MAX_MEMORY_CHARACTER_COUNT` in the loader).
2. **Specificity beats vagueness.** "Use 2-space indentation in TypeScript" beats "format code properly". "Run `pnpm test` before committing" beats "test your changes". "API handlers live in `src/api/handlers/`" beats "keep files organized". The instruction must be concrete enough for the model to verify and apply.
3. **The "would removing this cause Claude to make mistakes?" test.** Apply to every line. If the answer is no, cut it. CLAUDE.md is paid by the token on every request in the project; lines that do not change behavior are pure tax.
4. **No aspirations.** "We aim for 90% test coverage" is not a rule the agent can enforce, and trying to satisfy aspiration produces irrelevant work. Write what is actually true and enforced. If it is true in CI, say what runs in CI.
5. **Standing instructions, not conversation echoes.** CLAUDE.md is read once at session start (and re-injected after compact for project root). It must read sensibly cold. Avoid "as we discussed", "for this turn", "remember from last time".
6. **Match the scope to the audience.** Project-team CLAUDE.md is shared via git; write what the team agrees on. User-global is yours alone. Project-personal CLAUDE.local.md is your private fixture for this repo. Rules leaking into the wrong scope is the most common source of friction.
7. **Point at sources of truth; do not duplicate them.** A one-line `@docs/architecture.md` import beats a ten-line summary that drifts. Use `@path` imports for content that lives elsewhere. Never inline answers that change faster than the file.
8. **No aggressive caps.** "CRITICAL", "you MUST", "ALWAYS" wording produces compliance brittleness on modern Claude. The runtime already prepends `MEMORY_INSTRUCTION_PROMPT` which contains an explicit "IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written." Your file does not need to repeat that authority; state the rule plainly.
9. **Audit the existing layered context before writing.** Your new content does not land alone. It joins a stack: CC's built-in system prompt + managed CLAUDE.md + user-global + project + local + auto memory + path-scoped rules. Adding a rule that the CC system prompt already provides ("reference code as file:line", "confirm before destructive actions") or that another layer already covers is pure tax. What the host provides depends on the model: Opus 5.5 gets the LEAN prompt, which lacks "be concise", "no comments unless non-obvious", "no speculative abstraction" and "no compatibility shims", so for a 5.5 user those lines are not duplicates. `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` carries the built-in text verbatim, per shape and per model; check a candidate line against it before writing, and never contradict a line there except as a stated override ("Push to `main` without asking; this overrides the default confirmation."). Adding a rule that contradicts a higher-precedence layer creates a silent conflict. Before writing, run `/memory` to see what is already loaded, Grep the loaded files for the topic, and decide one of three actions: skip (already covered), edit in place (existing file is wrong/outdated), or move to the right scope. See `${CLAUDE_SKILL_DIR}/references/layered-context.md` for the audit protocol and the "do not restate" cheat sheet covering ~12 CC built-in defaults.
10. **Write for Opus 5.5 specifically.** On 5.5 the host prompt says little about behavior, so CLAUDE.md carries it, and a few 5.5 facts decide what earns a line:
    - Name the concrete behavior, not the category. Anthropic documents 5.5 as "responsive to instructions that name the specific kinds of early stop" (a summary that announces the next step instead of taking it), and a generic "avoid a generic AI look" as merely swapping one design default for another.
    - A delegation limit belongs here if the user wants one: the host dropped the Opus 5 line that suppressed Agent use, and the 5.5 Agent tool encourages it.
    - Skip lines the file cannot act on. Effort is set by `/effort` or agent frontmatter, not prose, and 5.5 thinks at its own depth, so "think carefully" costs bytes and latency. The host already reminds 5.5 after five silent turns, so no "update me every N steps".
    - Cost is per turn and per spawn. The block is cache-read on every main-thread turn (cheap: $0.20 per MTok on 5.5) and re-sent whole to every subagent whose definition does not set `omitClaudeMd: true`. Prune for the spawn count, not only the line count.

## Choosing the file shape inside the CLAUDE.md layer

A 400-line CLAUDE.md and four 100-line `.claude/rules/<topic>.md` files (all loaded unconditionally, no `paths:`) have identical token cost and identical model behavior. Splitting is for human maintainability, plus the option to add `paths:` to scope a rule to part of the codebase.

| Pick | When | Loaded |
|------|------|--------|
| `./CLAUDE.md` (root) or `./.claude/CLAUDE.md` | Universal rules every session needs; file under 200 lines | Always at session start |
| `./CLAUDE.local.md` | Personal overrides of team rules; gitignored | Always at session start |
| `./.claude/rules/<topic>.md` without `paths:` | Topic-scoped rule (testing, security, api) the team wants in its own focused file | Always at session start, same priority as `.claude/CLAUDE.md` |
| `./.claude/rules/<topic>.md` with `paths:` | Path-conditional rule (only `src/api/**`, only `**/*.tsx`, only migrations) | On demand when Claude reads a matching file; loads into message history (summarized away by compact) |
| `~/.claude/CLAUDE.md` | Personal preferences across all your projects | Always at session start |
| `~/.claude/rules/<topic>.md` | Personal preferences split by topic | Always at session start; loads BEFORE project rules so project rules win on conflict |

Two caveats worth front-loading:

- **Path-scoped rules and nested CLAUDE.md files do NOT survive compaction the same way.** They are injected into message history when triggered (not into the user-context message), so compact summarizes them away. They reload only when Claude next reads a matching file. If a rule MUST hold across compact, drop `paths:` or move it to project-root CLAUDE.md.
- **Subdirectory CLAUDE.md** (e.g., `packages/web/CLAUDE.md` when cwd is the monorepo root) loads on demand the same way. Useful for monorepo per-package rules without bloating root context.

Full splitting strategy, topic-file naming conventions, and `paths:` glob design: `${CLAUDE_SKILL_DIR}/references/rules-writing.md`.

## Five questions every project CLAUDE.md should answer

A pragmatic frame:

1. **What is the stack?** One paragraph: language, framework, runtime, package manager.
2. **Where does code live?** Top-level directories with one-line meanings - only when non-obvious.
3. **How do I run things?** Dev server, tests, lint, type-check, build, deploy. Exact strings.
4. **What are the conventions?** Style rules that differ from defaults, naming patterns, architectural rules.
5. **What is off-limits?** "Do not edit `migrations/`", "never push directly to `main`", "do not run `npm install` (use `pnpm`)".

If your CLAUDE.md does not answer these five, add the missing ones. If it answers more than five, audit whether the extras pull weight. Full INCLUDE/EXCLUDE coverage with examples: `${CLAUDE_SKILL_DIR}/references/content-rules.md`.

## `@path` imports

The loader recognizes a `@path` syntax for splitting content across files (four hops of importing):

- Syntax: `@path`, `@./relative`, `@~/home`, `@/absolute`. The regex requires whitespace or start-of-line before the `@`.
- Imports recurse up to four hops. The loader's `MAX_INCLUDE_DEPTH = 5` (`utils/claudemd.ts:537`) is an exclusive bound on a zero-indexed depth (`:630`, `depth >= MAX_INCLUDE_DEPTH`), so levels 0 through 4 are processed and four levels of importing land; the docs state the same as "a maximum depth of four hops". Cycles are detected and broken via path tracking.
- Only text-file extensions (~70 are listed) - `.md`, `.txt`, `.json`, `.ts`, `.py`, etc. Binary files (images, PDFs) are silently skipped.
- Imports inside fenced code blocks and codespans are NOT followed (the marked lexer respects token boundaries).
- Imports inside block-level HTML comments are NOT followed (comments are stripped before lex).
- Fragment identifiers (`@path#heading`) are stripped before resolution.
- External imports (paths outside cwd) trigger a one-time approval dialog the first time the runtime sees them, except in User memory which always permits externals.

Use imports to point at sources of truth (`@docs/architecture.md`, `@AGENTS.md`, `@README.md`), share personal content across worktrees (`@~/.claude/<project>-instructions.md`), and avoid duplicating long content. Imports help organization - they do NOT reduce context cost; imported content lands in context the same as inlined content.

Full syntax, edge cases, and the `claudeMdExcludes` setting for monorepo path filtering: `${CLAUDE_SKILL_DIR}/references/imports-and-paths.md`.

## HTML comments for human-only notes

Block-level `<!-- ... -->` comments are stripped before injection. Use them for maintainer notes that should not consume tokens:

```markdown
<!-- Maintainer note: keep this section under 30 lines, adherence drops past that. -->
## Testing

- Run `pnpm test` before committing.
```

Stripping rules: block-level only (CommonMark type-2 HTML block). Comments inside fenced code survive (they are part of code's literal content). Inline comments inside paragraphs survive. Unclosed `<!--` is left intact so a typo does not silently eat the rest of the file.

## Quick recipes

Common user requests mapped to the action this skill takes. Use these as pattern-match shortcuts before falling through to the full Workflow.

| User says | This skill does |
|-----------|-----------------|
| ANY of the patterns below | First: run `/memory` to see what is already loaded. Grep loaded files for the topic. Cross-check against the CC built-in system prompt list in `${CLAUDE_SKILL_DIR}/references/layered-context.md`. Decide skip / edit-in-place / move / new BEFORE drafting. |
| "Add X to CLAUDE.md" / "tell Claude X" / "remember X for the team" | After the audit: determine scope (team / user-global / personal), pick shape (inline CLAUDE.md vs `.claude/rules/<topic>.md`), draft with attribution comment, verify with `/memory`. |
| "Init CLAUDE.md" / "set up project memory" / "scaffold CLAUDE.md for this repo" | Copy `${CLAUDE_SKILL_DIR}/assets/CLAUDE.template.md` to `./CLAUDE.md`. Detect stack from manifest files. Fill stack, structure (non-obvious only), commands, verification loop, conventions, off-limits, git etiquette. Add attribution comment. |
| "Make a rule that only applies to X" / "scoped rule for `src/api/`" | Create `./.claude/rules/<topic>.md` with `paths:` (NOT `globs:`). Verify glob with a mental trace. Warn that path-scoped rules trigger only on Read (not Write/Edit), persist after first match, and are summarized by compact. |
| "My CLAUDE.md is over 200 lines / Claude is ignoring rules" | Run `/memory` to confirm load. Identify universal core (stack/commands/off-limits). Move topic content to `.claude/rules/<topic>.md`. Move long content to `@path` imports. Cut every line that fails "would removing this cause Claude to make mistakes?". |
| "Claude is not following my CLAUDE.md" | Walk the troubleshooting checklist in `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md`: file loaded? rule specific enough? conflicts? size? compact? wrong shape (should be hook)? path-scoped not triggering? settings-source disabled? `claudeMdExcludes` filtering? |
| "Global preferences" / "user-level instructions" / "add to my dotfiles" | Edit `~/.claude/CLAUDE.md` (cross-project preferences) or `~/.claude/rules/<topic>.md` (split by topic). Do NOT include project-specific stack or commands here. |
| "Personal preference for this project" / "sandbox URL" / "don't commit this" | Edit `./CLAUDE.local.md`. Add to `.gitignore` first. Use it for sandbox URLs, test accounts (POINTER not credentials), default branch, project-specific communication preferences. |
| "Migrate from AGENTS.md / .cursorrules / Copilot instructions" | Use `@AGENTS.md` import or symlink in `./CLAUDE.md`. Add Claude-specific overlay below the import. Single source of truth for shared content. |
| "Monorepo rules" / "rules for `packages/web/` only" | Option 1: subdirectory `packages/web/CLAUDE.md` (loads on demand). Option 2: root `.claude/rules/<topic>.md` with `paths: ["packages/web/**"]`. Discuss compact survival difference. Add `claudeMdExcludes` for ancestor noise. |
| "globs: vs paths:" / "rule loads every session despite frontmatter" | Definitively: use `paths:`. `globs:` is silently ignored (loads unconditionally). `paths: ['**']` is treated as no `paths:` (loads unconditionally). Both are common footguns. |

## Workflow

Walk these in order.

### 1. Audit the existing layered context

Before any drafting, run `/memory` to list every CLAUDE.md, CLAUDE.local.md, and rule file currently loaded. Then for the topic of the new rule:

- Grep the loaded files for keywords related to the topic.
- Check the built-in prompt text in `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` for overlap, on the shape the readers' model gets: section 1 for Opus 5.5, Sonnet 5.5 and other LEAN models, section 3 for Sonnet 5 and earlier and Haiku, section 5 for what every subagent already receives. If the shape already says it, skip. If the rule contradicts it, write it as an explicit override or drop it.
- For each existing mention, decide one of three: **skip** (already covered at the right scope), **edit in place** (existing file is wrong/outdated), or **move to the right scope** (rule is in the wrong layer; e.g., team rule in user-global).
- Check for conflicts: does the new rule contradict any existing layer? If yes, either drop one, or explicitly call out the override in the higher-precedence file.

**Concrete audit walkthrough.** User says: "Add to CLAUDE.md that we always use pnpm not npm." Walk the audit:

1. Run `/memory`. See files loaded: `~/.claude/CLAUDE.md`, `./CLAUDE.md`, `./.claude/rules/testing.md`, `./CLAUDE.local.md`.
2. Grep them for `pnpm` and `npm`. Found in `~/.claude/CLAUDE.md`: "Prefer `pnpm` over `npm`, `uv` over `pip`."
3. Cross-check CC built-in defaults: package-manager preference is NOT in the CC system prompt cheat sheet. Not a duplicate with CC.
4. Decision: user-global already covers it FOR YOU. But teammates may have different user-globals (or none). If the team needs ENFORCEMENT, the rule belongs in project `./CLAUDE.md` (committed, every contributor gets it). If it is just your personal preference, user-global is enough.
5. Ask the user: "Your `~/.claude/CLAUDE.md` already says 'prefer pnpm over npm'. Do you want this enforced for the whole TEAM (commit to `./CLAUDE.md`), or is your user-global rule enough?"
6. Based on the answer: skip (user-global is enough), or write to `./CLAUDE.md` with sharper wording ("Use `pnpm`. Do NOT run `npm install`.") + attribution comment + verify with `/memory` after.

Skipping this audit step is the single most common cause of "Claude is not following my CLAUDE.md" complaints later. The model is usually not ignoring the rule; two layers are saying different things and the model is reconciling badly.

### 2. Capture intent

Always-needed questions:

- What is the rule, in one sentence?
- Does the team need it, or just you?
- Universal, or only relevant when working on specific paths?
- Editing an existing file, or starting fresh?

Conditional questions (ask only when intent surfaces a need):

- Is this a multi-step procedure? If yes, route to `ac:skill-creator` instead - CLAUDE.md is not the right shape.
- Must this fire on every edit deterministically? If yes, this is a hook, not CLAUDE.md.
- Is it really a fact the agent already knows? (Language defaults, common framework idioms.) If yes, cut it; do not write.

Do not pre-ask every option; pull each in only when intent makes it relevant.

### 3. Pick the shape

Use the "Choosing the file shape" table above. Default to inline in `./CLAUDE.md` until size or path-scoping pushes you toward `.claude/rules/`.

### 4. Pick the scope

Use the "Four scopes" matrix above. Litmus test: if the team gets value, project-team; otherwise user-global or project-personal.

### 5. Draft the file

Lead every generated CLAUDE.md or CLAUDE.local.md with a block-level HTML attribution comment so a human reader knows where the file came from and when; in a `.claude/rules/*.md` file put it directly after the closing `---` of the frontmatter, never above it, because frontmatter is parsed only at byte 0 and anything above it makes the rule load unconditionally. The comment is stripped at injection time (`stripHtmlComments` removes block-level `<!-- ... -->`), so it costs ZERO tokens for the model but stays visible when a human opens the file with Read or in an editor. Substitute the actual ISO date.

```markdown
<!-- Generated by ac:claude-md-rules-creator on YYYY-MM-DD. This comment is block-level HTML, stripped before injection: zero token cost for the model, visible when a human opens the file. -->
```

Then for project-team `./CLAUDE.md`, add the canonical preface (the `/init` command uses this exact form):

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

Then the rules. Markdown headers (`##`) and bullets. One rule per bullet, specific and verifiable. Lead with the highest-value sections - they get the most weight when the file is read top-to-bottom.

For `.claude/rules/<topic>.md`, decide the `paths:` shape first:

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/api/**/*.ts"
---
<!-- Generated by ac:claude-md-rules-creator on YYYY-MM-DD. -->

# API Conventions

- Endpoints validate input with Zod schemas in `src/api/schemas/`.
- Return errors as `{ error: { code, message } }`. Never bare strings.
- Log requests with `requestId`, `userId`, `endpoint`. Never log tokens.
```

For `CLAUDE.local.md`, no preface needed. Just rules. Personal preferences, sandbox URLs, test data overrides, communication preferences.

Templates at `${CLAUDE_SKILL_DIR}/assets/`:

- `CLAUDE.template.md` - project-team starter with the canonical preface.
- `CLAUDE.local.template.md` - project-personal starter.
- `global-CLAUDE.template.md` - `~/.claude/CLAUDE.md` starter.
- `rule.template.md` - `.claude/rules/<topic>.md` starter with optional `paths:` frontmatter.

Hand off the prose-writing details to `/ac:prompt-writer`. CLAUDE.md content is a standing instruction set; the prompt-writer principles all apply (no aggressive caps, specific verifiable rules, scope stated, structure with headers, no aspirations).

### 6. Verify

Before declaring it done:

1. **Length under 200 lines (soft); 40,000 chars (hard).** `wc -l` and `wc -c`. If over the soft cap, run the cut/move pass.
2. **Every line passes "would removing this cause Claude to make mistakes?"** Walk it line by line.
3. **No aspirations, no platitudes, no secrets.** Skim for "we aim", "always", "good code", credentials.
4. **No file-by-file tours, no standard-language conventions.** Skim for redundancy with what the model already knows.
5. **Every rule is specific enough to verify.** Skim for vague verbs like "format properly", "handle errors", "test thoroughly".
6. **No conflicts with other CLAUDE.md files in the hierarchy.** Run `/memory` after editing - every file the runtime sees is listed. If you have project-team + project-personal at the same level, scan for contradictions.
7. **`@path` imports resolve.** Every imported file exists; circular imports detected by the loader but messy in practice.
8. **`# CLAUDE.md` preface present** for project-team file.
9. **`CLAUDE.local.md` in `.gitignore`** for project-personal scope. The `/init` command adds this automatically when generating the file.
10. **For `.claude/rules/*.md` with `paths:`, the glob actually matches**. Mentally trace a representative file path through your glob.

### 7. Iterate

| Symptom | Fix |
|---------|-----|
| Claude is not following the rule | Check `/memory` to confirm load. Tighten specificity. Check for conflicts. Consider whether a hook is the right shape instead. See `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md` troubleshooting. |
| File is over 200 lines | Run the cut/move pass: remove "removing-this-would-not-cause-mistakes" lines, move topic content to `.claude/rules/<topic>.md`, move references to `@path` imports. |
| Rule keeps disappearing after `/compact` | The rule is in a nested-subdir CLAUDE.md or a `paths:`-scoped rule. Move to project-root CLAUDE.md if it must persist. |
| Personal preferences are showing up in PRs | The team file (CLAUDE.md / `.claude/rules/`) absorbed personal content. Split: move to `CLAUDE.local.md` or `~/.claude/CLAUDE.md`. |
| Subdirectory CLAUDE.md not loading | It loads on demand when a file in that subdir is touched, not at session start. By design. If you want it at start, move content to a `paths:`-scoped rule at the root or to root CLAUDE.md. |

Deeper symptom-to-fix mapping and source citations: `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## Sibling skills (route the surrounding shape)

This skill stays focused on CLAUDE.md / rule files themselves. Route the surrounding work elsewhere.

| Producing | Route through | This skill handles |
|---|---|---|
| The prompt content INSIDE CLAUDE.md (how to phrase rules, structure, anti-patterns at the prose level) | `ac:prompt-writer` | The file shape, scope, splitting, imports, frontmatter |
| A multi-step procedure (deploy, release, audit) | `ac:skill-creator` (or `ac:command-creator` for user-typed slash) | The decision: not CLAUDE.md, build a skill instead |
| A custom subagent with its own CLAUDE.md inheritance | `ac:agent-creator` | The decision: not CLAUDE.md, build an agent; but a subagent INHERITS the project's CLAUDE.md by default unless its definition sets `omitClaudeMd: true` (parsed for user and plugin agents since 2.1.271; a spawn with it carries managed instructions only, confirmed in a 2.1.280 subagent transcript) |
| Deterministic enforcement (must hold every time, no model judgment) | configure a hook in `settings.json` | The decision: not CLAUDE.md, write a hook |
| Org-wide policy that survives compaction and cannot be excluded by users | this skill, managed scope | Same authoring rules, deployment via MDM/Ansible/Group Policy |

When the user request implies any row above, do both: invoke the matching creator for shape, then keep this skill loaded for the parts still in the CLAUDE.md layer.

## Pre-flight checklist

Always check:

- [ ] Layered audit done. `/memory` was run, loaded files were Grep'd for the topic, `claude-code-builtin-prompts.md` was checked for the readers' model shape, and no duplicate or unstated contradiction remains with any layer.
- [ ] Block-level HTML attribution comment: `<!-- Generated by ac:claude-md-rules-creator on YYYY-MM-DD. -->` with the real ISO date, at the top of a CLAUDE.md and DIRECTLY AFTER the closing `---` of a rule file. Stripped at injection (zero token cost), visible when humans Read the file. Above a rule's frontmatter it silently breaks `paths:`: the loader only parses frontmatter that starts at byte 0, so the rule loads unconditionally.
- [ ] Right scope (managed / user-global / project-team / project-personal).
- [ ] Right shape (`CLAUDE.md` / `CLAUDE.local.md` / `.claude/rules/<topic>.md`).
- [ ] File at the right path (user rules: `~/.claude/rules/` not `~/.claude/.claude/rules/`; project rules: `<dir>/.claude/rules/`).
- [ ] Under 200 lines (soft cap, adherence cliff). Hard cap 40,000 characters. Sweet spot 60 to 120 lines for project-team CLAUDE.md, measured across eight production repositories at a pinned commit SHA: median 105 to 110 lines, six of eight above 80 (`redpanda-data/connect` 174, `alibaba/spring-ai-alibaba` 150, `archtechx/tenancy` 129, `jrnl-org/jrnl` 108, `reidmorrison/semantic_logger` 103, `confluentinc/vscode` 84). The short ones stay short by pointing one line at a deeper document, not by carrying less content.
- [ ] Every line passes the "removing this would cause mistakes" test.
- [ ] Specific, verifiable rules; no vague verbs.
- [ ] No aspirations ("we aim for X"); state what is actually enforced.
- [ ] No standard-language conventions or self-evident advice.
- [ ] No file-by-file tours; only non-obvious directory roles.
- [ ] No credentials, secrets, sensitive data (CLAUDE.md is committed to the repo).
- [ ] No aggressive `CRITICAL` / `MUST` / `ALWAYS` repetition (runtime already prepends `MEMORY_INSTRUCTION_PROMPT`).

Check the items that apply to your file's shape:

- [ ] (Project team `CLAUDE.md`) `# CLAUDE.md` canonical preface present.
- [ ] (`CLAUDE.local.md`) Listed in `.gitignore`.
- [ ] (`.claude/rules/<topic>.md` with `paths:`) Glob actually matches your intent; no `paths: ['**']` (treated as no `paths:`).
- [ ] (`.claude/rules/<topic>.md` without `paths:`) Topic is universal and one focused subject; not a dumping ground.
- [ ] (Imports) `@path` references resolve; no chain deeper than four hops; external imports approved if needed.
- [ ] (HTML comments) Maintainer notes wrapped in `<!-- ... -->` are block-level (own line); inline comments survive injection.
- [ ] (Run `/memory`) The file appears in the loaded list. If not, the path is wrong, the scope source is disabled, or `claudeMdExcludes` is filtering it.
- [ ] (Hook command) No secret or credential appears in the hook command string.
- [ ] (Hook script) A path-containment guard is present, rejecting any target outside the intended directory.
- [ ] (Settings merge) A timestamped backup of the settings file was taken before the merge.
- [ ] (Post-write) `claude doctor` runs clean in the target directory after the write.

## References

| File | Load when... |
|------|--------------|
| `${CLAUDE_SKILL_DIR}/references/claude-code-builtin-prompts.md` | Before writing or cutting any line: the verbatim Claude Code 2.1.280 system prompt text per shape (LEAN for Opus 5.5 and Sonnet 5.5, CLASSIC for Sonnet 5 and earlier and Haiku), the per-model bundle sections, the CLAUDE.md wrapper as the model sees it, and what every subagent already receives. The duplicate-and-contradiction check runs against this file. |
| `${CLAUDE_SKILL_DIR}/references/layered-context.md` | Auditing the existing stack (CC built-in system prompt + managed + user + project + local + auto memory + path-scoped rules) BEFORE writing. Includes the full "do not restate" cheat sheet of CC built-in defaults, the audit protocol (`/memory` + Grep + decide), conflict-precedence rules, duplicate-detection patterns, and cross-layer worked examples. Read this FIRST when generating or editing a CLAUDE.md or rule. |
| `${CLAUDE_SKILL_DIR}/references/loader-and-injection.md` | Understanding the runtime mechanics: how files are discovered, concatenated, where they land in the API call (the `<system-reminder>` wrapper), compact survival rules, the `InstructionsLoaded` hook, troubleshooting "Claude is not following my CLAUDE.md". |
| `${CLAUDE_SKILL_DIR}/references/scopes.md` | Deep dive on the four scopes (managed / user-global / project-team / project-personal): platform-specific managed paths, `--add-dir` behavior, `CLAUDE_CODE_DISABLE_CLAUDE_MDS` env, `--bare` mode, AGENTS.md interop, worktree handling, monorepo `claudeMdExcludes`, the loader filters. |
| `${CLAUDE_SKILL_DIR}/references/rules-writing.md` | Splitting CLAUDE.md into `.claude/rules/`, choosing topic boundaries, `paths:` glob design, common rule topics (testing, security, frontend, api, migrations), user-level rules at `~/.claude/rules/`, recursive rule directories, symlink sharing. |
| `${CLAUDE_SKILL_DIR}/references/imports-and-paths.md` | `@path` import syntax, recursion limit (5), path resolution rules, fragment stripping, external-import approval dialog, `claudeMdExcludes` setting, HTML comments, text-file-extension allowlist. |
| `${CLAUDE_SKILL_DIR}/references/content-rules.md` | Comprehensive INCLUDE / EXCLUDE list with examples per category, the five-question framework, specificity examples, the canonical `# CLAUDE.md` preface, what `/init` includes by default. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Failure modes specific to CLAUDE.md and rules: aspiration, drift, secrets, oversize, scope leakage, vague rules, compact misunderstanding, conflicting hierarchies. Quick audit checklist. |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Four full annotated examples: global (`~/.claude/CLAUDE.md`), project-team (`./CLAUDE.md`), project-personal (`./CLAUDE.local.md`), path-scoped rule (`.claude/rules/api.md` with `paths:`). |
| `${CLAUDE_SKILL_DIR}/references/hook-wiring.md` | Constructing a linter hook for a target project and proving it fires: the seven-step procedure. |
| `${CLAUDE_SKILL_DIR}/references/lsp-wiring.md` | Detecting, proposing, and verifying a language server for a target project. |
| `${CLAUDE_SKILL_DIR}/assets/CLAUDE.template.md` | Starting a project-team `./CLAUDE.md` from a blank template with the canonical preface. |
| `${CLAUDE_SKILL_DIR}/assets/CLAUDE.local.template.md` | Starting a project-personal `./CLAUDE.local.md` from a blank template. |
| `${CLAUDE_SKILL_DIR}/assets/global-CLAUDE.template.md` | Starting a user-global `~/.claude/CLAUDE.md` from a blank template. |
| `${CLAUDE_SKILL_DIR}/assets/rule.template.md` | Starting a `.claude/rules/<topic>.md` from a blank template with optional `paths:` frontmatter. |

For the prompt-writing principles that apply to CLAUDE.md prose, invoke `/ac:prompt-writer`. For deciding between CLAUDE.md vs skill vs command vs agent vs hook, the decision flow above plus the matrix in [features-overview](https://code.claude.com/docs/en/features-overview.md) cover it.

Canonical Anthropic documentation, served as raw markdown by appending `.md` to the URL:

- Memory page (CLAUDE.md, rules, auto memory): `https://code.claude.com/docs/en/memory.md`
- Features overview (CLAUDE.md vs skills vs rules vs hooks): `https://code.claude.com/docs/en/features-overview.md`
- Context window (what survives compaction): `https://code.claude.com/docs/en/context-window.md`
- Hooks (`InstructionsLoaded` event for debugging): `https://code.claude.com/docs/en/hooks.md`
- Settings (`claudeMdExcludes`, `--setting-sources`): `https://code.claude.com/docs/en/settings.md`

When canonical docs conflict with observed CLI behavior, trust the live binary.
