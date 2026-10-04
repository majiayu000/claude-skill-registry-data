---
name: command-creator
description: "Create or audit a Claude Code slash command: arguments, shell-injected context, phases, and approval gates."
when_to_use: "Use when writing, editing or debugging a slash command."
---

# Command Creator

You are about to write or edit a Claude Code slash command another Claude will execute. A command is a markdown file that becomes a `/name` invocation: when the user types `/foo bar baz`, Claude Code reads the file, substitutes `&#36;ARGUMENTS` with `bar baz`, runs shell injection blocks, and injects the resulting prompt as a single user message. The model then executes the body as the next turn.

This skill is the playbook for designing arguments, shell-injection-driven context gathering, phase-based body structure, approval gates, and the storage-format choice. Target is Opus 5.5. The same shape works for Sonnet 5.5 at lower cost and for Haiku 4.5, which supports no effort parameter.

## Three jobs, not one

Writing a slash command splits into three tasks. Conflating them is the most common authoring mistake.

1. **Surrounding skill shape.** Frontmatter fields, scope (project/user/plugin/managed), invocation control (`disable-model-invocation`, `user-invocable`), `paths:`, `allowed-tools`, `model`, `effort`. Same rules as any skill. Route through `ac:skill-creator` (its body, references, and pre-flight checklist all apply).
2. **Command-specific shape.** Argument design, shell injection for context gathering, phase-based body structure, approval gates, storage format (flat `.md` vs skill-directory). This file teaches that.
3. **Body content.** The markdown the model reads when the command fires. This is a prompt. Route through `ac:prompt-writer` (architecture, snippets, anti-patterns, Opus 5 tuning).

A great command body in the wrong shape never gets used. A modest body in the right shape with crisp arguments and well-placed approval gates gets used every day.

## What a command actually is, mechanically

Slash commands and skills share the same loader in Claude Code. The distinction is one of file shape and intended use, not runtime mechanics. Source of truth: `loadSkillsDir.ts`, `utils/markdownConfigLoader.ts`, `utils/argumentSubstitution.ts`, `utils/promptShellExecution.ts` in the CC source.

The lifecycle:

1. **Discovery.** At session start, Claude Code scans for markdown under `.claude/commands/`, `.claude/skills/<name>/SKILL.md`, the user-global equivalents, managed dirs, and plugin paths (`<plugin>/commands/`, `<plugin>/skills/`). It does this via ripgrep on `*.md`.
2. **Parsing.** Each file's YAML frontmatter is parsed; metadata (`description`, `argument-hint`, `allowed-tools`, etc.) is registered.
3. **Invocation.** User types `/name args` (or the model invokes via the Skill tool when allowed). Claude Code locates the file, reads it again, and runs the preprocessor.
4. **Substitution.** Tokens in the body are replaced: `&#36;ARGUMENTS`, `&#36;ARGUMENTS[N]`, `&#36;N`, `&#36;<name>` (per `argumentSubstitution.ts`); `&#36;{CLAUDE_SKILL_DIR}` (only when the file is in skill-directory format); `&#36;{CLAUDE_SESSION_ID}`; `&#36;{CLAUDE_EFFORT}`.
5. **Shell injection.** Inline `` \!`<cmd>` `` and fenced ` \```\! ... \``` ` blocks are executed with BashTool (or PowerShellTool when `shell: powershell`). Each match is replaced with the command's stdout. Permissions still apply; deny rules still block.
6. **Injection into conversation.** The fully rendered body enters the conversation as a single user message and stays for the rest of the session. Auto-compact preserves the first 5,000 tokens of each invoked command across summaries.
7. **Execution.** The model reads the rendered body and performs the work, including any subsequent tool calls the body asks for.

The model never sees the raw command syntax, only the post-substitution prompt with shell output already inlined.

## Decision flow

Route by the user's request.

```
Is a slash command the right tool at all?
├── Single fact, no action → CLAUDE.md note, route through `ac:claude-md-rules-creator`. Not a command.
├── Reference content for the model (conventions, style) → reference skill, route through `ac:skill-creator`. Not a command.
├── Deterministic enforcement (must run on every edit) → hook, route through `update-config`. Not a command.
├── Custom subagent (isolated worker the orchestrator delegates to) → route through `agent-creator` if available.
└── User-driven slash invocation with arguments / side effects / context gathering → COMMAND, continue.

Does the command need bundled files (references, scripts, assets) the body points to?
├── YES → use the skill-directory format: `<scope>/.claude/skills/<name>/SKILL.md`
│        (or `<plugin>/skills/<name>/SKILL.md` for plugins). The `&#36;{CLAUDE_SKILL_DIR}` token resolves.
└── NO  → use the flat command file: `<scope>/.claude/commands/<name>.md`
         (or `<plugin>/commands/<name>.md` for plugins). Simpler, no `&#36;{CLAUDE_SKILL_DIR}` substitution.

Is this a fix or audit of an existing command?
├── YES → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` first, then specific reference (argument-design,
│         shell-injection, or phase-structure) as the symptom dictates.
└── NO  → walk the Workflow below.
```

For everything outside command-specific concerns (frontmatter fields, scope, paths, hooks, etc.), defer to `/ac:skill-creator` rather than duplicating that material here.

## Frontmatter: minimal by default

A working command needs only `description`. Everything else is opt-in. Modern Claude Code merged commands into skills, so command frontmatter accepts the same fields as a skill (see `${CLAUDE_SKILL_DIR}/references/command-vs-skill.md` for the differences between the two file shapes).

Command-specific fields most often used:

| Field | Required? | When to set |
|-------|-----------|-------------|
| `description` | recommended | always; this is the trigger surface |
| `argument-hint` | optional | the command takes positional arguments and you want autocomplete to hint at them |
| `arguments` | optional | the command takes input and you want named-positional substitutions (e.g., `$pr_number` instead of `&#36;0`) |
| `disable-model-invocation` | optional | the command has side effects you want the user to control (deploy, commit, send-message); this is the common command default |
| `allowed-tools` | optional | the body fires specific tool calls (`Bash(gh:*)`, `Bash(git commit:*)`) you want pre-approved during the run |
| `shell` | optional | the shell injection blocks should run via PowerShell on Windows (`CLAUDE_CODE_USE_POWERSHELL_TOOL=1` required) |
| `effort` | optional | the command needs more or less reasoning budget than the session default |

Fields you almost never need on a command: `user-invocable: false` (commands are user-driven by nature), `context: fork` (commands usually need to steer mid-process), `paths:` (commands are typed, not auto-loaded by file).

Skip everything else unless you can name the specific condition that requires it. Full per-field reference: invoke `/ac:skill-creator` and consult its `frontmatter.md`.

> **Escape convention used in this documentation.** This SKILL.md is itself a skill body that the Claude Code loader preprocesses. Any literal full-arguments token (a plain dollar sign followed by `ARGUMENTS`), a literal indexed shorthand (a dollar sign followed by a digit), or the skill-directory and session-id tokens would be substituted on every invocation, corrupting the documentation. To prevent that, the docs below render those tokens with the HTML entity `&#36;` standing in for the dollar sign. In your own command body, drop the entity and write a plain dollar sign.

## Argument design

A command's argument shape is the contract with the user. Get it right before writing the body.

Three shapes:

| Shape | Frontmatter | Body uses | When to pick |
|-------|-------------|-----------|--------------|
| **Free-form** | (none; just write `&#36;ARGUMENTS` in body) | `&#36;ARGUMENTS` (full string as typed) | The command takes a sentence or query: `/deep-research how does auth work?` |
| **Positional** | `argument-hint: "[arg1] [arg2]"` | `&#36;0`, `&#36;1`, or `&#36;ARGUMENTS[N]` | The command takes structured positional inputs: `/migrate-component SearchBar React Vue` |
| **Named** | `arguments: [pr_number, target_branch]` | `&#36;pr_number`, `&#36;target_branch` | The command takes structured inputs that read better with names: `/cherry-pick 123 release` |

Argument parsing rules (from `argumentSubstitution.ts`):

- `&#36;ARGUMENTS` substitutes the raw string the user typed, verbatim.
- `&#36;ARGUMENTS[N]` and `&#36;N` substitute the Nth shell-quoted token, 0-indexed. `/cmd "hello world" foo` produces `&#36;0 = "hello world"` and `&#36;1 = "foo"`.
- `$<name>` only substitutes when the name appears in the `arguments:` frontmatter list. Without that frontmatter, `$myvar` stays literal in the body.
- Named arguments cannot be digits (`arguments: [0, 1]` is rejected, since those would conflict with `&#36;0`/`&#36;1` shorthand).
- If the body contains no `&#36;ARGUMENTS` placeholder and the user typed arguments, the loader appends `\n\nARGUMENTS: <input>` to the end of the body. Treat that as a fallback, not a design.

For flag detection (`--interactive`, `--dry-run`, `--skip-X`), parse `&#36;ARGUMENTS` inside the body using AskUserQuestion or simple string checks. There is no built-in flag parser; the body decides. Detail and copy-paste patterns: `${CLAUDE_SKILL_DIR}/references/argument-design.md`.

## Shell injection (dynamic context)

The most distinctive feature of command bodies is shell injection: pre-execution of shell commands whose output is inlined into the prompt before the model reads anything. This is the canonical pattern for grounding a command in live state (git status, PR diff, server status, file contents) rather than guessing.

Two forms:

- **Inline:** `` \!`<cmd>` `` is replaced with the command's stdout. The exact CC regex is `(?<=^|\s)!`([^`]+)`/gm`; the inline form requires whitespace or start-of-line before the bang.
- **Fenced:** ` ```\! ` opens a multi-line block; everything until the closing ` ``` ` is run as a single shell script and replaced with its output. CC regex: `\`\`\`!\s*\n?([\s\S]*?)\n?\`\`\`/g`.

(The docs above use `\!` to keep this SKILL.md itself from triggering the preprocessor. In your command, write a plain `!`.)

Canonical pattern from the built-in `/commit` command (CC source `commands/commit.ts`). The example below uses `\!` to keep this very SKILL.md from triggering the preprocessor when documenting it; in your real command body, write a plain `!`:

```markdown
## Context

- Current git status: \!`git status`
- Current git diff (staged and unstaged changes): \!`git diff HEAD`
- Current branch: \!`git branch --show-current`
- Recent commits: \!`git log --oneline -10`

## Your task
Based on the changes above, create a single git commit...
```

When `/commit` runs, each inline injection token is replaced with that command's output before the model sees the prompt. The model gets the real diff, branch, and history inlined; it never executes those `git` commands itself.

Critical caveats:

- Inline injection is preprocessing, not a tool call. The user does not see the commands run; only the rendered output appears in context.
- Each shell command goes through the normal permission flow. `allowed-tools` patterns are auto-applied during the injection so the user is not prompted mid-render. Deny rules still block.
- MCP-loaded commands cannot run shell injection (remote and untrusted); `&#36;{CLAUDE_SKILL_DIR}` is meaningless for MCP commands too.
- `disableSkillShellExecution: true` in settings disables injection for user/project/plugin/`--add-dir` sources. Bundled and managed commands are unaffected.
- **The footgun:** if you paste a literal `` \!`<cmd>` `` or ` \```\! ... \``` ` block into a command body as a documentation example, it will execute on every invocation. To document the syntax without executing, escape the bang as `\!`. The backslash breaks the inline regex's lookbehind and the fenced regex's literal-start match.

Full security model, performance notes (the inline scan is gated on a substring check), and 8 copy-paste patterns for common context-gathering recipes: `${CLAUDE_SKILL_DIR}/references/shell-injection.md`.

## Body structure: phase-based workflows

Command bodies are usually multi-phase workflows: a context-gathering phase, an analysis or research phase, an approval phase, an execution phase, and a verification phase. The phase-based structure helps the model orchestrate without losing the thread.

Standard shape:

```markdown
# <Command Title>

<One-line statement of what the command achieves for the user.>

## Phase 1: Context
**Goal**: Read the state needed to proceed.
**Actions**:
1. <action with `\!`shell command`` for live data, or explicit step>
2. <action>

## Phase 2: Analyze / Plan
**Goal**: Decide what to do based on Phase 1.
**Actions**:
1. <decision logic>
2. <branching: if X, do A; if Y, do B>

## Phase 3: Approve (skip in auto mode)
**Goal**: Confirm with the user before side effects.
Use AskUserQuestion with concrete options. Auto mode (default): proceed.
Interactive mode (`--interactive` in `&#36;ARGUMENTS`): prompt.

## Phase 4: Execute
**Goal**: Perform the action.
**Actions**: <specific commands, tool calls, file edits>
**Success criterion**: <observable signal the step worked>

## Phase 5: Report
**Goal**: Tell the user what happened.
<One-line result format, e.g., "Committed: <hash> <msg>, pushed to <remote>/<branch>"

## Error Handling
- **<error case>**: <what to do>
- **<another case>**: <what to do>
```

Conventions worth honoring:

- Each phase has **Goal** + **Actions** + (when consequential) **Success criterion**. The model needs to know when each phase is done.
- Place approval gates (AskUserQuestion) directly before irreversible operations: writing to remote, sending messages, destructive git operations, dropping data.
- Have an "auto mode" default (no prompts) and an interactive escape (`--interactive` flag) so the same command serves both human-driven and pipeline use.
- Lead with one-paragraph **Identity** or **Goal** if the persona matters.
- End with an **Error Handling** section listing the failure modes you can name and what to do for each.
- Sub-numbered steps (3a, 3b) signal steps that can run in parallel.

Detail and three worked phase structures (auto-mode workflow, interview-driven command, context-gathering report): `${CLAUDE_SKILL_DIR}/references/phase-structure.md`.

## Storage format: flat `.md` vs skill-directory

Two storage paths produce the same `/name` slash command but differ in capability:

| Format | Path | `&#36;{CLAUDE_SKILL_DIR}` | Bundled files | Use when |
|--------|------|------------------------|---------------|----------|
| Flat | `.claude/commands/<name>.md` or `<plugin>/commands/<name>.md` | Not substituted (no baseDir) | None (the body is the whole command) | Simple command with no references or scripts to bundle |
| Skill-directory | `.claude/skills/<name>/SKILL.md` or `<plugin>/skills/<name>/SKILL.md` | Resolves to the skill's directory | `references/`, `scripts/`, `assets/` work | The command needs supporting files |

A flat command file is the simpler choice and matches the "command" mental model best. Use it for context-gathering recipes, simple actions, single-script orchestrations. If the command grows references or scripts, migrate to the skill-directory format (the slash invocation stays the same).

Plugin-only path substitutions (the loader behavior is different for plugins than for user/project skills):

- `&#36;{CLAUDE_PLUGIN_ROOT}` is substituted in the body of every plugin command and plugin skill (per `utils/plugins/loadPluginCommands.ts:339-343`). Resolves to the plugin's root directory. Use this when a flat plugin command at `<plugin>/commands/<name>.md` needs to reference a plugin-level file: write `&#36;{CLAUDE_PLUGIN_ROOT}/templates/foo.md`.
- `&#36;{CLAUDE_SKILL_DIR}` is additionally substituted for plugin skills in skill-directory format (per the same loader, `isSkillMode` branch), pointing at the skill's subdirectory inside the plugin. Use this when files live inside the skill's own folder.
- `&#36;{user_config.X}` substitutes per-plugin user config values. Sensitive keys resolve to a placeholder. Set up via plugin manifest `userConfig` field.
- For non-plugin skills (user, project, managed at `.claude/skills/<name>/SKILL.md`), only `&#36;{CLAUDE_SKILL_DIR}` substitutes; `&#36;{CLAUDE_PLUGIN_ROOT}` stays literal.

Both `&#36;{CLAUDE_PLUGIN_ROOT}` and `&#36;{CLAUDE_SKILL_DIR}` are ALSO available in hook commands, MCP configs, and LSP configs (`utils/hooks.ts:818`, `utils/plugins/mcpPluginIntegration.ts:462`, `utils/plugins/lspPluginIntegration.ts:226`).

## Workflow

Walk these in order. Each step assumes the previous resolved.

### 1. Capture intent

Always-needed questions:

- What does the command do, in one sentence?
- What input does it take (free-form, positional, named, none)?
- What side effects does it have (read-only, writes locally, writes remotely, sends messages)?
- Project, user, or plugin scope?

Conditional questions (ask only when the answer to a previous question implies the need):

- Approval gates before specific side effects? Ask when side effects are irreversible.
- Allowed-tools? Ask when the body fires repeated bash commands the user would otherwise have to approve one-by-one.
- Auto mode vs interactive default? Ask when the command will be used in both human and automated contexts.

Do not pre-ask about every optional field; pull each in only when intent makes it relevant.

### 2. Pick storage format

Per the table above: flat for simple, skill-directory if bundled files are needed.

### 3. Design arguments

Decide free-form, positional, or named. Set `argument-hint` so autocomplete reflects the shape. Plan flag detection inside the body if the command needs `--interactive`, `--dry-run`, `--skip-X`. See `${CLAUDE_SKILL_DIR}/references/argument-design.md` for copy-paste flag-detection snippets.

### 4. Draft the frontmatter

Minimal:

```yaml
---
description: <Imperative verb + object, one sentence, 60-120 chars. Name any flag the model must pass.>
when_to_use: <Optional. One "Use when..." sentence.>
---
```

Add `argument-hint`, `arguments`, `disable-model-invocation`, `allowed-tools` only when the command actually needs them. The "Frontmatter: minimal by default" table above lists every field and the condition that justifies it.

### 5. Write the body

Body structure follows the phase template above. For each phase, write the Goal, then Actions with explicit steps. Place shell injection (`` \!`<cmd>` ``) wherever live state is needed.

The body is a prompt. Hand it off to `/ac:prompt-writer` for architecture, snippets, and anti-patterns.

Skill-creator's body conventions also apply: persona at top if relevant, success criteria per step, end-of-prompt reminders for the top constraints, no aggressive caps (state the rule plain and explain the why), and scope stated in both directions (where a rule spans, and where the command must stop, since Opus 5 widens scope on its own).

> **Repeat the shell-injection footgun warning here**: if your body contains documentation examples showing the syntax, escape the bang as `\!` to keep the preprocessor from executing them on every invocation. Live usage of injection (the real thing) takes a plain `!`.

### 6. Verify

Before shipping:

1. **Frontmatter parses.** `description` is a string, `allowed-tools` is space-separated or YAML list, no nonsense fields.
2. **Arguments substitute correctly.** Mentally run the body with a sample invocation. Does the right text replace the right placeholders?
3. **Shell injection executes.** Run the command in a fresh session. Each `` \!`<cmd>` `` should produce the expected output inlined into the prompt.
4. **Approval gates fire before side effects.** Trace the body: every irreversible action is preceded by an AskUserQuestion (in interactive mode) or guarded by an explicit safety check (in auto mode).
5. **Error handling covers the named failure modes.** Each error case in the Error Handling section maps to a real way the command can fail.
6. **Description triggers cleanly.** Read `description` aloud. Would the user (or model) know when to invoke this command on a relevant request?

Five worked commands that pass all gates: `${CLAUDE_SKILL_DIR}/references/examples.md`.

### 7. Iterate

| Symptom | Fix |
|---------|-----|
| Does not trigger when the user types `/name` | Confirm directory name = slash command name; check `disable-model-invocation` and `user-invocable` settings; verify the file is in a discoverable location |
| Substitution leaves literal `&#36;ARGUMENTS` in output | Check the body actually contains the literal placeholder; check `arguments:` frontmatter matches `&#36;<name>` usage in body |
| Shell injection executes when it should not (e.g., on documentation examples) | Escape the bang as `\!` in documentation contexts; only use literal `!` for real injection |
| Approval gate skipped in auto mode | Ensure auto-mode logic explicitly bypasses AskUserQuestion; do not silently approve irreversible actions |
| Repeated permission prompts during the run | Add narrow `allowed-tools` patterns matching exactly the bash subcommands the body issues |
| Command works but body bloats over time | Move repeated logic into `scripts/` (skill-directory format); reference via `&#36;{CLAUDE_SKILL_DIR}/scripts/<name>.<ext>` and orchestrate around it |

Deeper symptom-to-fix mapping for command-specific issues: `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## Sibling skills (route the surrounding shape)

This skill stays focused on command-specific concerns. Everything else routes through one of these:

| Producing | Route shape through | Use this skill for |
|---|---|---|
| The surrounding skill shape (frontmatter, scope, invocation, bundling, char budget) | `ac:skill-creator` | Command-specific patterns (arguments, shell injection, phase structure) |
| The prompt body itself | `ac:prompt-writer` | Command-specific patterns (this file) |
| A subagent definition that the command delegates to | `agent-creator` (when available) | Whether to write a command at all (vs a subagent) |
| CLAUDE.md or `.claude/rules/<topic>.md` | `ac:claude-md-rules-creator` | Whether to write a command at all (vs a CLAUDE.md note) |
| Hook configuration | `update-config` | Whether to write a command at all (vs a deterministic hook) |

When the user request implies any of the rows above, do both: invoke the matching creator for shape, and keep this skill loaded for what is still command-shaped.

## Quick template

Full annotated blank template: `${CLAUDE_SKILL_DIR}/assets/COMMAND.template.md` (flat command form; copy directly).

For the skill-directory form (when you need bundled files), use the SKILL.template at `${CLAUDE_SKILL_DIR}/../skill-creator/assets/SKILL.template.md` after invoking `/ac:skill-creator`.

## Pre-flight checklist

Always check:

- [ ] Storage format chosen (flat `.md` for simple, skill-directory for bundled files).
- [ ] Directory or file name = slash command name (lowercase, hyphens, no `claude` or `anthropic`).
- [ ] Frontmatter has `description`; `argument-hint` set if the command takes input; `arguments` set only for named-positional substitutions.
- [ ] `description` opens with an imperative verb, carries no phases, names any flag a model caller must pass, and stays at 60 to 120 characters (about 200 with `when_to_use`); a `disable-model-invocation` command's description is read by humans in `/help`, so keep it to one sentence too.
- [ ] `disable-model-invocation: true` set if the command has irreversible side effects.
- [ ] `allowed-tools` narrow patterns set if the body chains specific tool calls.

Check only the items that apply to the command's specific shape:

- [ ] (If arguments are taken) every `&#36;ARGUMENTS`, `&#36;N`, or `&#36;<name>` placeholder matches the frontmatter declaration.
- [ ] (If shell injection is used) every `` \!`<cmd>` `` and ` \```\! ... \``` ` references a command the user's permission setup actually allows.
- [ ] (If documentation examples show injection syntax) the bang is escaped as `\!` to prevent self-execution.
- [ ] (If the command has side effects) approval gates are placed before each irreversible step; auto mode has explicit safety checks.
- [ ] Phase structure: each phase has Goal + Actions; consequential phases have a Success criterion.
- [ ] Error Handling section names the failure modes you can anticipate.
- [ ] Final report format is specified (the user knows what to read at the end of the run).
- [ ] Body passes the `ac:prompt-writer` audit: no aggressive caps, no negative-only instructions, positive instructions, why explained when non-obvious.
- [ ] Test invocation in a fresh session: does the rendered prompt look right?

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/command-vs-skill.md` | Deciding between flat `.md` and skill-directory format; understanding the merged-into-skills nuance and what each storage choice gains or loses. |
| `${CLAUDE_SKILL_DIR}/references/argument-design.md` | Designing `&#36;ARGUMENTS`, `$N`, `$<name>`; flag detection patterns; multi-line input; shell-quote nuances. |
| `${CLAUDE_SKILL_DIR}/references/shell-injection.md` | Using inline and fenced injection for context gathering; security model; performance gates; eight copy-paste recipes; documentation escape. |
| `${CLAUDE_SKILL_DIR}/references/phase-structure.md` | Structuring multi-phase command bodies; AskUserQuestion patterns (binary, multi-select, clearance); approval gates; auto-vs-interactive mode. |
| `${CLAUDE_SKILL_DIR}/references/builtin-catalog.md` | Case studies from built-in commands (`/commit`, `/init`, `/sync-claude-code`); what each does and what to copy. |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Five worked commands at different complexity tiers, ready to copy and adapt. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Diagnosing a misbehaving command or auditing one before shipping. |
| `${CLAUDE_SKILL_DIR}/assets/COMMAND.template.md` | Starting a new flat-format command from a blank annotated template. |

For surrounding skill shape, invoke `/ac:skill-creator`. For the prompt body itself, invoke `/ac:prompt-writer`. Sibling-skill files cannot be read by path from here, since the install layout is unknown at author time. Invocation is the portable form.

Canonical Anthropic documentation, served as raw markdown by appending `.md` to the URL:

- Slash commands and skills (merged): `https://code.claude.com/docs/en/skills.md`
- Plugins (plugin commands, namespacing, the plugin-root token usage): `https://code.claude.com/docs/en/plugins.md`
- Hooks: `https://code.claude.com/docs/en/hooks.md`
- Subagents: `https://code.claude.com/docs/en/sub-agents.md`
- Agent Skills open standard: `https://agentskills.io/specification`

When canonical docs conflict with observed CLI behavior, trust the live binary.
