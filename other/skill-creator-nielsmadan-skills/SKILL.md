---
name: skill-creator
description: Guide for creating or improving Claude skills. Triggers "create a skill", "build a skill", "new skill", "improve this skill", "skill for [use case]".
argument-hint: <skill name or description>
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Skill Creator

## Core Principles

**Concise is key.** The context window is shared with system prompts, conversation history, other skills, and the user's request. Only add context Claude doesn't already have. Challenge each piece: "Does this paragraph justify its token cost?" Prefer concise examples over verbose explanations.

**Match freedom to fragility.** Narrow bridge with cliffs = specific guardrails (exact scripts). Open field = many valid routes (text instructions). See `references/patterns.md` for detailed guidance.

## Skill Structure

### Folder Rules

```
skill-name/              # kebab-case, must match `name` field
├── SKILL.md             # Required (exact case-sensitive spelling)
├── scripts/             # Optional: executable code
├── references/          # Optional: documentation loaded as needed
└── assets/              # Optional: templates, images, fonts for output
```

- Folder name must be kebab-case and match the `name` field exactly
- No README.md or other auxiliary files (CHANGELOG, INSTALLATION_GUIDE, etc.)
- Only include files that directly support the skill's functionality

For details on when to use scripts/, references/, and assets/, see `references/patterns.md`.

### SKILL.md Format

#### Frontmatter

The YAML frontmatter controls whether Claude loads the skill. This is the most important part.

```yaml
---
name: your-skill-name
description: What it does. Use when [specific trigger phrases].
---
```

**Rules:**

| Rule | Detail |
|------|--------|
| `name` | kebab-case, no spaces/capitals, must match folder name |
| `description` | Must include WHAT it does AND WHEN to use it |
| Description length | Under 1024 characters |
| Trigger phrases | Include specific phrases users would say |
| File types | Mention relevant file types if applicable (e.g., ".csv files", ".docx") |
| No XML tags | No `<` or `>` in frontmatter (security restriction) |
| No reserved names | No "claude" or "anthropic" in the name field |

**Good descriptions:**

```yaml
# Specific, includes triggers and file types
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".

# Includes trigger phrases and capabilities
description: Manages Linear project workflows including sprint planning,
  task creation, and status tracking. Use when user mentions "sprint",
  "Linear tasks", "project planning", or asks to "create tickets".
```

**Bad descriptions:**

```yaml
# Too vague - won't trigger correctly
description: Helps with projects.

# Missing triggers - Claude won't know when to load it
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user-facing triggers
description: Implements the Project entity model with hierarchical relationships.
```

Put ALL "when to use" information in the description, not in the body. The body only loads after triggering, so "When to Use This Skill" sections in the body do not help Claude decide to load the skill.

**Optional fields:** `license` (e.g., MIT), `compatibility` (environment requirements, 1-500 chars), `metadata` (author, version, mcp-server).

#### Body Structure

After the frontmatter, write instructions in Markdown. The recommended structure:

```markdown
# Skill Name

## Instructions
### Step 1: [First Major Step]
Clear, specific explanation with examples.

### Step 2: [Next Step]
(continue as needed)

## Examples
### Example 1: [common scenario]
User says: "..."
Actions: 1. ... 2. ...
Result: ...

## Troubleshooting
### Error: [Common error]
**Cause:** [Why it happens]
**Solution:** [How to fix]
```

**All three sections are expected:** Instructions, Examples, and Troubleshooting. Skills missing Examples or Troubleshooting are incomplete.

**Writing guidelines:**
- Use imperative form ("Run the script", not "You should run the script")
- Be specific and actionable — `Run python scripts/validate.py --input {file}` not "Validate the data"
- Include what success looks like after each step
- Reference bundled resources clearly: "Consult `references/api-patterns.md` for rate limiting guidance"

**Size limit:** Keep SKILL.md under ~5,000 words. If approaching this limit, move reference material to `references/` and link to it. See `references/patterns.md` for progressive disclosure patterns.

## Gotchas
- "When to use" information in the skill body has ZERO effect on triggering. Only the frontmatter `description` field is scanned for trigger matching — put all trigger phrases there.
- XML angle brackets (`<`, `>`) in frontmatter silently break skill loading with no error message. Use backticks or natural language instead of `<feature>` in descriptions.
- **Format agnosticism:** Skills are shared across tools (Claude Code, Codex, Pi, etc.). Do not use tool-specific skill invocation prefixes like `/skill-name` or `$skill-name` inside skill bodies — just write `skill-name` or backtick it as `skill-name`. Each tool has its own prefix convention and the skill should not assume which one is used.

## Creation Process

### Step 1: Understand with Concrete Examples

Understand how the skill will be used before writing anything. Ask the user:

- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say that should trigger this skill?"
- "What should NOT trigger this skill?"

Avoid asking too many questions at once. Start with the most important and follow up as needed. Conclude when there is a clear sense of the functionality and trigger scenarios.

### Step 2: Plan Reusable Contents

Analyze each use case example to identify what reusable resources would help:

- **Scripts** — Code that gets rewritten repeatedly (e.g., `scripts/rotate_pdf.py` for a PDF skill)
- **References** — Knowledge Claude needs while working (e.g., `references/schema.md` for a database skill)
- **Assets** — Files used in output (e.g., `assets/template/` for a webapp builder)

Create a list of resources to include. Not every skill needs bundled resources — many skills are instructions-only.

### Step 3: Initialize Directory

Create the skill directory with required SKILL.md and any needed resource directories:

```bash
mkdir -p skill-name/{scripts,references,assets}  # include only dirs you need
touch skill-name/SKILL.md
```

### Step 4: Write the Skill

#### 4a: Implement reusable resources first

Write scripts, references, and assets before SKILL.md. This may require user input (e.g., brand assets, API docs, database schemas). Test all scripts by running them.

#### 4b: Write frontmatter

Follow the frontmatter rules above. Verify:
- Name matches folder name
- Description includes WHAT + WHEN + trigger phrases
- Description under 1024 characters
- No XML tags or reserved words

#### 4c: Write body

Follow the recommended body structure:

1. **Instructions** — Step-by-step workflow. Be specific and actionable. Include concrete commands, expected outputs, and decision points. Reference bundled resources where relevant.
2. **Examples** — At least one worked example showing a user request, the actions taken, and the result. More examples for complex skills.
3. **Troubleshooting** — Cover 2-3 common failure modes with cause and solution.

### Step 5: Test and Iterate

#### Triggering tests

Test that the skill loads at the right times:

```
Should trigger:
- "Help me [primary use case]"
- "[Paraphrased request]"
- "[Domain-specific terminology]"

Should NOT trigger:
- "[Unrelated query]"
- "[Similar but different domain]"
```

Ask Claude: "When would you use the [skill name] skill?" — Claude will quote the description back, revealing gaps.

#### Functional tests

Run the skill on real tasks. Verify:
- Outputs are correct and complete
- All workflow steps execute
- Bundled resources are referenced appropriately

#### Iteration signals

| Signal | Symptom | Fix |
|--------|---------|-----|
| Undertriggering | Skill doesn't load when it should | Add more trigger phrases and keywords to description |
| Overtriggering | Skill loads for unrelated queries | Add specificity or negative triggers ("Do NOT use for...") |
| Execution issues | Inconsistent results or user corrections needed | Improve instructions, add error handling, be more specific |
| Context bloat | Slow responses, degraded quality | Move content to references/, reduce SKILL.md size |

### Step 6: Deploy in this repo

Keep one source directory for skills and render it to each agent's skills
directory with the loadout tool, rather than editing per-agent copies — there is
no list to register a skill in.

**Pick the scope first**, because it decides the directory:

| Scope | Lives in | Reaches |
|---|---|---|
| Global | `loadout/skills/<name>/` | All four harnesses, every project |
| Project-type | `loadout/templates/<type>/skills/<name>/` | Only projects declaring that template |
| This repo only | `.claude/skills/<name>/` | sessions in this repo (see below) |

**Global skill** — write `loadout/skills/<name>/SKILL.md`, then:

```bash
loadout sync --global
```

That renders it into `~/.claude/skills/`, `~/.codex/skills/`,
`~/.config/opencode/skills/` and `~/.pi/agent/skills/`. **The directory is the
declaration** — nothing else needs editing to wire it up. Supporting files
(`references/`, `scripts/`, `assets/`) are copied byte-for-byte with mode preserved,
so an executable script stays executable; `__pycache__` is skipped.

One mandatory hookup: classify the skill in `publish/skills.toml` — add its name
to one of the README groups under `[groups]`, or to `private`. Every global skill
must appear in exactly one place; the pre-commit hook rejects an unclassified
skill, and publishable sources must carry no personal strings.

One optional hookup: add a row to `loadout/skills/README.md`, the human-facing
catalog. Agents read the `description:` frontmatter instead, so that frontmatter is
what actually has to be good.

**Repo-local skill** — `.claude/skills/<name>/` is outside the loadout pipeline: no
sync, no `loadout check` coverage, Claude Code picks it up directly. To reach Codex
too, symlink it into this repo's `.codex/skills/`:

```bash
ln -sfn ../../.claude/skills/<name> .codex/skills/<name>
```

**Never hand-edit a rendered output** under a harness's skills directory. Each
carries a `<!-- GENERATED ... -->` banner; `loadout check --global` runs in
lefthook's pre-commit hook and rejects drift, and `loadout sync` refuses to
overwrite a hand-edited output rather than discarding it.

**Nothing prunes.** Moving a skill between scopes — or deleting one — leaves the
already-rendered copies in all four harness directories. Delete those by hand.

Note: any skill body referencing `docs/` writes into the *target project's*
`docs/`, not this repo — global skills run in arbitrary projects.

### Step 7: Vary the text per harness (only if needed)

Almost no skill needs this — 47 of 49 render identically everywhere. Reach for it
when a skill must genuinely say different things to different agents (e.g.
`code-review`, whose dispatch instructions differ between the claude/codex/opencode
family and pi).

Mark whole blocks inline:

```markdown
::: claude
- **Codex** blocks on "Reading additional input from stdin…" unless stdin is closed.
:::
::: codex opencode
- **Claude** runs non-interactively in print mode (`claude -p`).
:::
```

Constraints: a marker never sits *inside* a fenced code block (to vary a code
example, mark the whole fence twice), and adjacent blocks must have no blank line
between them or that line reaches every harness.

Frontmatter is YAML, so `:::` there would be data. Per-harness **values** use a block
keyed by harness, merged over the shared keys and stripped from the output:

```yaml
name: nono-sandbox
description: Decide whether a failure is actually a nono sandbox denial…
opencode:
  description: Diagnose and resolve permission denials when opencode runs…
```

## Quality Checklist

Before finalizing, verify:

- [ ] Folder is kebab-case, matches `name` field
- [ ] SKILL.md exists (exact case)
- [ ] Frontmatter has `---` delimiters
- [ ] `name`: kebab-case, no spaces/capitals
- [ ] `description`: includes WHAT and WHEN with trigger phrases
- [ ] `description`: under 1024 characters
- [ ] No XML tags (`<` `>`) in frontmatter
- [ ] No "claude" or "anthropic" in name
- [ ] No README.md or auxiliary files inside the skill's own folder
- [ ] Instructions are specific and actionable
- [ ] Examples section included
- [ ] Troubleshooting section included
- [ ] SKILL.md under ~5,000 words
- [ ] References clearly linked from SKILL.md (if using references/)
- [ ] File types mentioned in description (if applicable)
- [ ] Placed by scope: `loadout/skills/` (global), `loadout/templates/<type>/skills/` (project-type), or `.claude/skills/` (this repo only)
- [ ] Classified in `publish/skills.toml` (a `[groups]` entry, or private) — the pre-commit hook fails otherwise
- [ ] `loadout sync --global` run, and the skill appears under all four harness skills directories
- [ ] `loadout check --global` reports no drift
- [ ] Row added to `loadout/skills/README.md` (the human catalog — agents read the `description:` frontmatter instead)

## Examples

### Example: Creating a csv-analyzer skill

**Step 1 — Understand:** User wants a skill that analyzes CSV files, generates summary statistics, and creates visualizations. Triggers: "analyze this CSV", "summarize this data", "chart this spreadsheet".

**Step 2 — Plan resources:**
- `scripts/analyze.py` — Reusable analysis script with pandas
- No references or assets needed

**Step 3 — Initialize:**
```
csv-analyzer/
├── SKILL.md
└── scripts/
    └── analyze.py
```

**Step 4 — Write:**

Frontmatter:
```yaml
---
name: csv-analyzer
description: Analyze CSV files with summary statistics and visualizations.
  Use when user uploads .csv files, asks to "analyze data", "summarize this
  CSV", "chart this spreadsheet", or wants statistical insights from tabular data.
---
```

Body includes: step-by-step workflow (load CSV, validate, analyze, visualize, present), an example showing a user asking "Summarize sales.csv" with the expected output, and troubleshooting for common issues (malformed CSV, missing columns, large files).

**Step 5 — Test:** Verify it triggers on "analyze this CSV" and "give me stats on this data file" but not on "help me write a CSV parser" (that's a coding task, not an analysis task).

## Troubleshooting

### Skill doesn't trigger

**Cause:** Description is too vague or missing trigger phrases.
**Solution:** Add specific phrases users would say. Include file types if relevant. Test with: "When would you use the [skill name] skill?"

### Skill triggers too often

**Cause:** Description is too broad.
**Solution:** Be more specific. Add negative triggers:
```yaml
description: Processes PDF legal documents for contract review.
  Do NOT use for general PDF editing or non-legal documents.
```

### Instructions not followed

**Cause:** Instructions are too verbose, ambiguous, or buried.
**Solutions:**
1. Keep instructions concise — use bullet points and numbered lists
2. Put critical instructions at the top
3. Move detailed reference material to `references/`
4. Replace ambiguous language with specific commands
5. For critical validations, consider bundling a script (code is deterministic; language interpretation isn't)

### Skill feels slow or quality degrades

**Cause:** SKILL.md is too large or too many skills enabled simultaneously.
**Solution:** Move detailed docs to `references/`, keep SKILL.md under ~5,000 words. Link to references instead of inlining content.

---

For advanced patterns (progressive disclosure, resource organization, domain-specific splitting), see `references/patterns.md`.
