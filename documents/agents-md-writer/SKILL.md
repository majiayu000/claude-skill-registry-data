---
name: agents-md-writer
description: Generate the dual-agent workspace contract, an AGENTS.md skill registry plus a CLAUDE.md pointer, so one set of skills serves both Claude Code (which auto-discovers them) and agents like Codex (which need required-reading instructions). Use when the user says "set up AGENTS.md", "make my skills work in Codex too", "dual agent setup", or "workspace contract".
---

# AGENTS.md Writer

Claude Code auto-discovers `.claude/skills/`. Codex and most other agents do not. Without a contract, half your tooling is invisible to half your agents. This skill writes that contract: one AGENTS.md that turns your skill folder into required reading for any agent, plus a CLAUDE.md pointer that keeps a single source of truth.

## Step 1: Inventory the workspace

1. List `.claude/skills/` at the workspace root: every folder with a SKILL.md, and its `name` and `description` frontmatter.
2. Note which are real folders and which are links into a shared library (both work; the contract references the workspace-relative path either way).
3. Read any existing AGENTS.md or CLAUDE.md so you extend rather than clobber. Per-project files deeper in the tree stay untouched.

## Step 2: Group the skills

Group by task domain, not alphabetically, so an agent can find the right skill from the task in front of it. Typical groups: Design, Writing, Business, Development, Workflow. Two or three groups beat seven.

## Step 3: Write AGENTS.md

Structure, proven in real dual-agent workspaces:

```markdown
# AGENTS.md

Workspace-level guidance for all projects under <root>. Applies to any agent that reads AGENTS.md.

## Local skills

Skills live in `.claude/skills/`. Claude Code auto-discovers them.
Other agents should treat the files referenced below as required reading,
because they do not auto-load skills from this folder.

## <Group> skills

When a task involves <domain>, read the relevant skill file first and apply its guidance.

- **<skill-name>** (`.claude/skills/<skill-name>/SKILL.md`)
  One line: what it covers and when it is required.

How to use them:
- <task shape>: read **<skill-a>** first, then **<skill-b>**.
- These are reference guidance, not code. Read the SKILL.md, then apply.

## <Hard rules>

Any non-negotiable workspace rules an agent must follow in every output.
```

The per-skill line answers "when is reading this mandatory", not just "what is this".

## Step 4: Write the CLAUDE.md pointer

CLAUDE.md stays short and defers to AGENTS.md, so there is one source of truth:

```markdown
# CLAUDE.md

Use `AGENTS.md` as the workspace guidance for <root>.
Claude Code should use `.claude/skills/` as the local skill source at this root.

For <task shape>, load `<skill-a>` first, then `<skill-b>`.
```

## Step 5: Verify

Ask the target agent (in a fresh session) to describe the workspace rules. If it cannot name the skills and when to read them, the contract failed; tighten the wording.

## Rules

- Extend existing files, never overwrite silently. Show a diff of what changes.
- Register only skills that exist on disk. A contract pointing at missing files is worse than none.
- Keep AGENTS.md under two screens. It is a map, not documentation.
- No em dashes in any output.

## Output

An AGENTS.md skill registry and a CLAUDE.md pointer at the workspace root, extending whatever already existed.
