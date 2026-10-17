---
name: skill-creator
description: Guide for creating and editing Claude Code skills. Use when user wants to create a new skill, create a new slash command (skills are the unified primitive - commands live in skills/ now), update an existing skill, or needs help structuring a SKILL.md file.
disable-model-invocation: true
---

# Skill Creator

Official docs: <https://code.claude.com/docs/en/skills.md>. Fetch when unsure about frontmatter semantics, subagent forking, hook integration, or recent features.

## Process

### 1. Gather requirements

Ask the user:

- What task/domain does the skill cover?
- What specific use cases should it handle?
- Does it need executable scripts or just instructions?
- Any reference materials to include?

If the user's description is already clear, skip straight to drafting.

### 2. Determine placement

Infer from context, ask only if ambiguous:

- **Global** (`~/.claude/skills/`) - across all projects
- **Project** (`<project>/.claude/skills/`) - repo-specific
- **Plugin** (`<plugin>/plugins/<name>/skills/`) - distributed via marketplace

### 3. Assess complexity

**Simple** (just write the SKILL.md):

- Purely instructional (workflow, guidelines, domain knowledge)
- No supporting files needed

**Full** (skill with bundled resources):

- Needs scripts for deterministic/repeated operations
- Needs reference docs (schemas, API docs, large knowledge bases)
- Needs assets (templates, images, fonts)

### 4. Draft the skill

**Simple path:** Create the directory and write SKILL.md directly.

**Full path:**

1. Plan supporting files (what scripts/references/assets are needed)
2. Create the skill directory and subdirs
3. Write supporting files first (may need user input for assets/docs)
4. Write SKILL.md last, referencing the supporting files

### 5. Review with user

Present draft and iterate. Skills improve most after real usage.

## Skill Structure

```
skill-name/
├── SKILL.md              # Main instructions (required)
├── references/           # Docs loaded into context on demand (optional)
│   ├── api-reference.md
│   └── schema.md
├── scripts/              # Deterministic code (optional)
│   └── helper.py
└── assets/               # Files used in output (optional)
    └── template.html
```

Reference supporting files from SKILL.md so Claude knows they exist:

```md
- For API details, see [references/api-reference.md](references/api-reference.md)
- For schema docs, see [references/schema.md](references/schema.md)
```

## SKILL.md Format

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

[Core instructions, workflows, and guidance]
```

### Frontmatter reference

All fields are optional. Only `description` is recommended so Claude knows when to use the skill.

| Field                      | Required    | Description                                                                                                                                                                                                                                                                                                         |
| :------------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                     | No          | Display name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only (max 64 characters).                                                                                                                                                                                  |
| `description`              | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Front-load the key use case: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage. |
| `when_to_use`              | No          | Additional context for when Claude should invoke the skill, such as trigger phrases or example requests. Appended to `description` in the skill listing and counts toward the 1,536-character cap.                                                                                                                  |
| `argument-hint`            | No          | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`.                                                                                                                                                                                                  |
| `disable-model-invocation` | No          | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Default: `false`.                                                                                                                                                               |
| `user-invocable`           | No          | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`.                                                                                                                                                                                            |
| `allowed-tools`            | No          | Tools Claude can use without asking permission when this skill is active. Accepts a space-separated string or a YAML list.                                                                                                                                                                                          |
| `model`                    | No          | Model to use when this skill is active.                                                                                                                                                                                                                                                                             |
| `effort`                   | No          | Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model.                                                                                                                 |
| `context`                  | No          | Set to `fork` to run in a forked subagent context.                                                                                                                                                                                                                                                                  |
| `agent`                    | No          | Which subagent type to use when `context: fork` is set.                                                                                                                                                                                                                                                             |
| `hooks`                    | No          | Hooks scoped to this skill's lifecycle. See Hooks in skills and agents for configuration format.                                                                                                                                                                                                                    |
| `paths`                    | No          | Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. Uses the same format as path-specific rules.                                                             |
| `shell`                    | No          | Shell to use for `` !​`command` `` and ` ```! ` blocks in this skill. Accepts `bash` (default) or `powershell`. Setting `powershell` runs inline shell commands via PowerShell on Windows. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.                                                                            |

### Available string substitutions

Skills support string substitution for dynamic values in the skill content:

| Variable               | Description                                                                                                                                                                                                                                                                              |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`.                                                                                                                                             |
| `$ARGUMENTS[N]`        | Access a specific argument by 0-based index, such as `$ARGUMENTS[0]` for the first argument.                                                                                                                                                                                             |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`, such as `$0` for the first argument or `$1` for the second.                                                                                                                                                                                               |
| `${CLAUDE_SESSION_ID}` | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions.                                                                                                                                                                  |
| `${CLAUDE_SKILL_DIR}`  | The directory containing the skill's `SKILL.md` file. For plugin skills, this is the skill's subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory. |

Additionally, `` !​`<command>` `` (inline) and ` ```! ` fenced blocks preprocess shell command output into the prompt before Claude sees it.

## Writing Guidelines

**Description** is the most important field. It's the only thing Claude sees when deciding which skill to load. Include:

- First sentence: what the skill does
- Second sentence: when to trigger it (keywords, file types, scenarios)
- Max 1024 chars, third person

**Two types of skill content:**

- **Reference** - knowledge Claude applies to current work (conventions, patterns, domain knowledge). Runs inline alongside conversation.
- **Task** - step-by-step instructions for a specific action (deploy, commit, code generation). Often paired with `disable-model-invocation: true`.

**Body** should contain:

- Procedural knowledge non-obvious to Claude
- Concrete workflows with actionable steps
- References to supporting files so Claude knows they exist

**Keep SKILL.md lean.** Aim for under 200 lines, hard max 500. Move detailed material to supporting files.

**List prerequisites.** If the skill relies on external programs/CLIs (jq, ffmpeg, a vendored binary, etc.), add a short **Prerequisites** section near the top listing them — with install hints when non-obvious. An unstated dependency makes the skill silently fail on a machine that lacks it. List only what could plausibly be missing; skip ubiquitous tools (curl, date, grep) and skip the section entirely for purely instructional skills.

## When to Add Scripts

Add `scripts/` when:

- Same code would be generated repeatedly
- Operation needs deterministic reliability
- Errors need explicit handling

Scripts save tokens and improve reliability vs regenerating code each time.

**Path resolution:** For plugin skills, reference scripts with `${CLAUDE_SKILL_DIR}/scripts/helper.js` (relative paths won't resolve). Use `${CLAUDE_PLUGIN_ROOT}` only when referencing files outside the skill's own directory. For global/project skills, relative paths work fine.

## When to Split Files

Split content out of SKILL.md when:

- SKILL.md would exceed ~200 lines
- Content covers distinct domains (separate files per domain)
- Advanced features are rarely needed
- Large schemas, API docs, or knowledge bases

Prefer multiple focused files over one large reference file. E.g. `api-reference.md`, `schema.md`, `examples.md` rather than a single `reference.md` with everything.

For large files (>10k words), include grep patterns in SKILL.md so Claude can search efficiently.

## Review Checklist

After drafting, verify:

- [ ] Description includes triggers ("Use when...")
- [ ] Prerequisites section lists required programs (if any external tooling is used)
- [ ] SKILL.md is lean (under ~200 lines)
- [ ] No time-sensitive information
- [ ] Concrete examples included where helpful
- [ ] All supporting files referenced in SKILL.md
- [ ] No duplicate info between SKILL.md and supporting files
