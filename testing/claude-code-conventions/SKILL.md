---
name: claude-code-conventions
description: |
  How to create and manage Claude Code rules, skills, and hooks for this project.
  Use when: user asks to document a convention, note a rule, create a skill, add a hook,
  or persist any project knowledge for future Claude Code sessions.
  Triggers on: "remember this", "note this down", "create a rule for", "create a skill for",
  "add a hook for", "document this convention", or any request to persist project knowledge.
---

# Claude Code Conventions — Rules, Skills, and Hooks

## Design Pattern

```
CLAUDE.md     → brief always-loaded context (~120-200 lines max per file)
Rules         → short always-loaded reminders with skill load conditions (~15-25 lines each)
Skills        → detailed content loaded on demand when Claude decides it's needed
Hooks         → deterministic shell enforcement (zero context cost, runs automatically)
```

**Decision guide — where does the content go?**

| Content type | Where |
|---|---|
| Brief universal context, project overview, tech stack | `CLAUDE.md` |
| Short reminder + when to load a skill | `.claude/rules/<name>.md` |
| Detailed conventions, workflows, code patterns | `.claude/skills/<name>/SKILL.md` |
| Deterministic enforcement (block bad commands) | `.claude/hooks/<name>.sh` |

---

## Skills

### Templates — start here

- `templates/SKILL.template.md` — copy this into a new `.claude/skills/<name>/SKILL.md`.
  It has four mutually-exclusive shapes (pick one, delete the rest) derived from
  reviewing every skill in this repo — see "Shapes" below.
- `templates/RULE.template.md` — copy into `.claude/rules/<name>.md` for the
  companion rule (see "Rules" section further down).

### Shapes (observed across this repo's skill corpus)

Every skill in `.claude/skills/` clusters into one of four repeatable shapes.
Identify which one a new skill is *before* writing it — mixing shapes in one
file is the main reason skills drift long and hard to maintain.

| Shape | What it does | Body reads like | Examples in this repo |
|---|---|---|---|
| **A. Convention / rule** | Standing rule Claude applies while writing/reviewing code — nothing is "run" | Rules list + good/bad code | `tdd`, `performance`, `backward-compatibility`, `hasura`, `extraction-dev`, `multi-env-dev` |
| **B. Procedure / slash-command** | A deterministic runbook, often invoked as `/name [args]` | Numbered steps ending in a checkable outcome | `sync-main`, `force-merge-pr`, `linear-log-bug`, `generate`, `check-codebuild`, `release-phoenix-sdk` |
| **C. Scaffold / generator** | Produces new files from a template | Short SKILL.md + `references/guide.md` for the full spec | `new-agent`, `new-remote-app`, `new-sdk`, `implement-engineer-local-env` |
| **D. External SDK / platform reference** | Adapts a third-party API/tool to this repo's conventions | Reference link + "Purpose" + "Core API" + "this repo's conventions" | `statsig-react`, `statsig-server`, `statsig-feature-gates`, `agents-dev` |

Companion-file conventions that go with these shapes:
- **Shape C** puts its full spec in `references/<name>.md` (e.g. `implement-engineer-local-env/references/guide.md`) and says "Read `references/guide.md` first" as the opening line — the only case where a skill should NOT be fully self-contained inline, because the spec is too long to reload on every quick question.
- **Shape B** may colocate a deterministic helper script next to `SKILL.md` (e.g. `check-codebuild/check-codebuild.sh`) and call it by exact relative path in the procedure.

### Known deviations — don't copy these

A few existing skills drifted from the schema below; they still work because
they're invoked explicitly by name from a rule, not autonomously matched, but
new skills should not repeat this:
- `doltgres-ops`, `e2e-testing`, `generate` ship with **no frontmatter at all**
  — always include `name` + `description`, even for a skill you expect to be
  invoked explicitly.
- `check-codebuild` has a top-level `metadata: {type: skill}` frontmatter key
  — **not part of the schema**. Only `name` and `description` are supported
  for skills (`description` and `paths` for rules).

### Location

```
.claude/skills/<name>/SKILL.md
```

One folder per skill. The folder name becomes the skill name.

### Frontmatter

```yaml
---
name: <skill-name>
description: |
  One-line summary of what this skill covers.
  Use when: <specific situations that warrant loading this skill>.
  Triggers on: <keywords, file patterns, imports, or commands that indicate this skill is needed>.
---
```

- `name` — matches the folder name, kebab-case
- `description` — Claude Code reads this to decide whether to load the skill. Be specific.
  - `Use when:` — concrete situations (not "when working in X folder")
  - `Triggers on:` — file names, import paths, CLI commands, code patterns

### Content rules

- **Self-contained** — never reference other skills by name. If the skill needs context from another domain, inline the minimum needed content.
- **No cross-skill mentions** — referencing a skill by name can cause Claude Code to load it unnecessarily. Use `CLAUDE.md` or file paths instead.
- **Detailed is fine** — skills are loaded on demand, so length is less critical than always-loaded files. Include code examples, templates, checklists.
- **Actionable** — every section should tell Claude Code what to do, not just describe.

### When to create a skill (vs putting content in CLAUDE.md)

Create a skill when the content is:
- Only needed for specific tasks (not general background knowledge)
- More than ~15 lines of detailed instructions or code
- A workflow, checklist, or pattern that Claude needs to follow step-by-step

Keep in `CLAUDE.md` when the content is:
- Needed as background context for almost every task in that folder
- A short rule that can be stated in 1-3 lines

---

## Rules

### Location

```
.claude/rules/<name>.md
```

### Frontmatter

```yaml
---
description: <one-line description>
---
```

For path-scoped rules (only active when working in a specific folder):

```yaml
---
description: <one-line description>
paths:
  - "agents/**"
---
```

**Supported frontmatter attributes**: `description`, `paths`. Nothing else.
- Do NOT use `alwaysApply` — not supported
- Do NOT use `globs` — not supported, use `paths` instead

### Content rules

Rules are always loaded (within their path scope). Keep them short — ~15-25 lines max.

**Required structure** — every rule that mentions a skill MUST include load conditions:

```markdown
# <Topic>

<2-3 line summary of the key constraint or reminder>

Load the `<skill-name>` skill when:
- <specific condition 1>
- <specific condition 2>

Skip the `<skill-name>` skill when:
- <condition where loading would be wasteful>
- <read-only or unrelated tasks>
```

**Why load conditions matter**: Rules fire on every relevant context. Without conditions, Claude Code has no signal for when the skill is actually needed vs. when it's irrelevant overhead. The `Load when` / `Skip when` pattern gives Claude Code the information to make a conditional decision.

### When a rule can omit a skill reference

If a convention can be fully stated in 2-3 lines and needs no detailed procedure, the rule itself IS the complete guidance — no skill needed. Example: "Always use bun/bunx instead of npm/npx." That's it.

---

## Hooks

### Location

```
.claude/hooks/<name>.sh
```

Must be executable (`chmod +x`).

### Registration in `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/<name>.sh"
          }
        ]
      }
    ]
  }
}
```

Available hook events: `PreToolUse`, `PostToolUse`, `Stop`, `Notification`.
Available matchers: tool names (`Bash`, `Write`, `Edit`) or `*` for all tools.

### Hook script contract

Claude Code passes the tool input as JSON on stdin. Exit code controls behavior:
- `exit 0` — allow the tool call
- `exit 1` — block the tool call (print reason to stderr before exiting)

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
# Parse with python3 (available on all macOS/Linux)
FIELD=$(echo "$INPUT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('fieldName', ''))" 2>/dev/null || echo "")

if <condition>; then
  echo "ERROR: <clear explanation of what was blocked and what to do instead>" >&2
  exit 1
fi

exit 0
```

### When to use a hook (vs a rule)

Use a hook when:
- The enforcement is binary (allow/block) and always correct regardless of context
- The mistake is common enough that a reminder alone won't prevent it
- No judgement is needed — the rule has no exceptions

Use a rule (not a hook) when:
- The guidance requires context or judgement to apply
- There are legitimate exceptions
- You want Claude Code to understand why, not just be blocked

---

## Checklist: Adding a new convention

1. **Decide the format** — rule only, skill + rule, or hook?
2. **Create the skill** (if needed):
   - `mkdir -p .claude/skills/<name>`
   - Copy `templates/SKILL.template.md` to `SKILL.md`, pick the one matching
     shape (A/B/C/D — see "Shapes" above), delete the other three
   - Fill frontmatter (`name`, `description` with `Use when` + `Triggers on`)
   - Keep self-contained — no references to other skills
3. **Create the rule** (if skill-backed):
   - Copy `templates/RULE.template.md` to `.claude/rules/<name>.md`
   - Add `paths:` if it only applies to a specific folder
   - Include `Load the X skill when:` and `Skip the X skill when:` sections
4. **Create the hook** (if enforcement needed):
   - Write `.claude/hooks/<name>.sh`, make it executable
   - Register in `.claude/settings.json` under the right hook event + matcher
5. **Trim the source CLAUDE.md** — if the content was moved from a `CLAUDE.md`, remove it and add a one-line pointer if useful
