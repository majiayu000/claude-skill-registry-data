---
name: engineer-skill
description: >-
  Guide for creating agent-invocable Agent Skills (SKILL.md packages
  auto-discovered by description). Use when users want to create or author a
  skill, or ask about skill structure or format. Not for user-invoked slash
  commands. Works across IDEs.
license: 'Based on https://github.com/anthropics/skills'
---

# Skill Creator

This skill guides through creating effective Agent Skills — markdown-based packages that teach AI agents specialized workflows, domain knowledge, and procedural capabilities.

## Question Format (FR-UNIVERSAL.QA-FORMAT)

When asking the user a choice (IDE, scope, behavior decisions):

- **Numbered** — each question is a numbered list item (`1.`, `2.`, …), not a heading, a bold-only line, or a paragraph.
- **Self-contained** — the question is answerable from itself and its options alone. Name what is being decided and what the answer changes, inside the question. "Which of the above?", a bare "Your choice?", and "Which variant do you prefer?" with nothing restated are defects: they send the reader back up the transcript to reconstruct the question.
- **Each option stands on its own** — a reader often jumps straight to the options, so an option's title and the lines under it must be enough to choose without the text above the question or the earlier turns. The title is a short name after the option's letter or number, and the reader answers with that letter or number; the `**Essence:**` line under it says what would be done, to what, and what the reader gets. A short reply option with no analysis of its own (Apply / Skip / Edit) has no Essence line, and its title says it alone. **Inside an option, name things in words, never by a report's ids.** Every line of the option — title, Essence, Pros, Cons, Risks, Best for — is read without the report, and ids slip in most often in Pros, Cons and Risks. Write what the thing is instead of its label: "the checkout errand on the shop site", not `E4`; "the search box ignoring the first keystroke", not `N3`. A label in parentheses after a general phrase — "the two most expensive errands (E4, E3)" — is still a bare label: name each item. A number taken from a report keeps what it measures in the same sentence: a percentage names the whole it is a share of ("page text takes about 40% of the cost", not "a 40% share"), and a sum says whose cost it is. **Any phrase that stands for a group is a pointer**: a count ("the four slow pages", "the same three errands"), a category ("the anomalies", "the issues found"), a rank or superlative ("the costliest runs"), "these", "as above", "the current round" — and so is a partial list, a count followed by a few examples or a "such as". Replace it with every member of the group, named in words, in that option — even when the list is long, even when the report above already lists them; if the whole set does not fit, drop the group from the option. Test: with the report deleted, could the reader name every member from this option alone? A word coined in this session gets a short explanation in the option. An explanation elsewhere in the reply does not count — not in the report above the question, not in another option. Before sending, read each option alone, line by line, and list every label (letters plus digits such as `E4` or `N3`), number, group phrase (a count, a category, a superlative, "the same", "these") and coined term in it; replace each with words or remove it.
- **No catch-all option** — never add an option whose only content is an invitation to answer freely ("Other", "Something else", "Your own variant", "Tell me what you need"). The user can always type a free-form reply instead of a letter or number, and an IDE's question tool (`AskUserQuestion` and the like) already offers a free-text answer of its own, so such an option adds a line and no choice. An option that names a concrete alternative is a real option, even when its title starts with "Other".
- **`agent's choice`** — on a multi-select where the user delegates with `agent's choice` (or its language equivalent), pick the subset yourself, justify the pick in one line, and proceed without re-asking for confirmation.
- When the choices are mutually exclusive alternatives with their own analysis, that analysis is nested under the option inside the question — never repeated as a separate block before it. It opens with the `**Essence:**` line, then `**Pros:**`, `**Cons:**`, `**Risks:**` and `**Best for:**`, each on its own labelled line.

## About Skills

Skills are self-contained packages (directory with `SKILL.md`) that extend agent capabilities with:

1. **Specialized workflows** — multi-step procedures for specific domains
2. **Tool integrations** — instructions for working with specific file formats or APIs
3. **Domain expertise** — company-specific knowledge, schemas, business logic
4. **Bundled resources** — scripts, references, and assets for complex tasks

## IDE Detection and Skill Placement

Skills work across multiple IDEs. Before creating a skill, determine the current environment and ask the user where to place it.

### Control Primitives Map by IDE

| Primitive | Scope | Claude Code | Cursor | OpenCode |
| :--- | :--- | :--- | :--- | :--- |
| **Persistent Instructions** | User | `~/.claude/CLAUDE.md` | - | `~/.config/opencode/AGENTS.md`<br>`~/.claude/CLAUDE.md` (fallback) |
| | Project | `CLAUDE.md`<br>`.claude/rules/*.md` | `AGENTS.md`<br>`.cursor/rules/*/RULE.md`<br>~~`.cursor/rules/*.mdc`~~ | `AGENTS.md`<br>`CLAUDE.md` (fallback)<br>`opencode.json` `instructions` |
| | Folder | `subdir/CLAUDE.md`<br>`CLAUDE.local.md` | `subdir/AGENTS.md` | - |
| **Conditional Instructions** | Project | `.claude/rules/*.md` | `.cursor/rules/*/RULE.md`<br>~~`.cursor/rules/*.mdc`~~ | `opencode.json` `instructions` (globs) |
| **Custom Commands** | User | `~/.claude/commands/*.md` | `~/.cursor/commands/*.md` | `~/.config/opencode/commands/*.md` |
| | Project | `.claude/commands/*.md`<br>`.claude/commands/<namespace>/*.md` | `.cursor/commands/*.md` | `.opencode/commands/*.md` |
| **Skills** | User | `~/.claude/skills/<name>/` | `~/.cursor/skills/<name>/` | `~/.config/opencode/skills/<name>/`<br>`~/.claude/skills/<name>/` (fallback) |
| | Project | `.claude/skills/<name>/` | `.cursor/skills/<name>/` | `.opencode/skills/<name>/`<br>`.claude/skills/<name>/` (fallback) |
| **Event Hooks** | User | `~/.claude/settings.json` | `~/.cursor/hooks.json` | `~/.config/opencode/plugins/*.{js,ts}` |
| | Project | `.claude/settings.json`<br>`.claude/settings.local.json` | `.cursor/hooks.json` | `.opencode/plugins/*.{js,ts}` |
| **MCP Integration** | User | `settings.json`<br>`managed-mcp.json` | `~/.cursor/mcp.json` | `opencode.json` `mcp` |
| | Project | `.mcp.json` | `.cursor/mcp.json` | `opencode.json` `mcp` |
| **Context Ignoring** | User | `.claude/settings.json` | - | - |
| | Project | - | `.cursorignore` | `.gitignore`<br>`.ignore`<br>`opencode.json` `watcher.ignore` |

### Skill-Specific Paths

| IDE | Personal Skills | Project Skills |
|-----|----------------|----------------|
| **Cursor** | `~/.cursor/skills/<name>/` | `.cursor/skills/<name>/` |
| **Claude Code** | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| **OpenCode** | `~/.config/opencode/skills/<name>/` | `.opencode/skills/<name>/` |

OpenCode also reads skills from fallback locations: `.claude/skills/`, `.agents/skills/`, `~/.claude/skills/`, `~/.agents/skills/`.

### Detection Strategy

1. Check for IDE-specific markers in the project:
   - `.cursor/` directory → Cursor
   - `.claude/` directory → Claude Code
   - `.opencode/` directory or `opencode.json` → OpenCode
2. If multiple detected or none → ask the user
3. Ask: personal skill (user-level) or project skill (shared via repo)?

**IMPORTANT**: Never create skills in `~/.cursor/skills-cursor/` — reserved for Cursor internals.

## Core Principles

### Concise is Key

Context window is shared with conversation, other skills, and user request. Every token competes for space.

**Default assumption: the agent is already very smart.** Only add context it doesn't already have.

Challenge each piece:
- "Does the agent really need this explanation?"
- "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

| Freedom Level | When to Use | Example |
|---------------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | Code review guidelines |
| **Medium** (pseudocode/templates) | Preferred pattern with acceptable variation | Report generation |
| **Low** (specific scripts) | Fragile operations, consistency critical | Database migrations |

### Anatomy of a Skill

Every skill: required `SKILL.md` + optional bundled resources in a directory:

```
skill-name/
├── SKILL.md              # Required - main instructions
├── references/           # Optional - detailed documentation
│   ├── api_reference.md
│   └── patterns.md
├── scripts/              # Optional - executable code
│   └── validate.py
└── assets/               # Optional - output resources
    └── template.md
```

#### SKILL.md (required)

- **Frontmatter** (YAML): `name` and `description` fields. These determine when the skill triggers.
- **Body** (Markdown): Instructions loaded AFTER skill triggers.

#### Bundled Resources (optional)

| Type | Path | Purpose | When to Include |
|------|------|---------|-----------------|
| **Scripts** | `scripts/` | Executable code (Python/Bash) | Same code rewritten repeatedly; deterministic reliability needed |
| **References** | `references/` | Documentation loaded into context as needed | Detailed info too lengthy for SKILL.md |
| **Assets** | `assets/` | Files used in output (templates, images, fonts) | Templates, boilerplate, images for final output |

#### What NOT to Include

No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other auxiliary docs. The skill contains only what the agent needs to do the job.

### Progressive Disclosure

Three-level loading to manage context:

1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — when skill triggers (<5k words)
3. **Bundled resources** — as needed (unlimited)

Keep SKILL.md under 500 lines. Split content into separate files when approaching this limit. Reference them clearly from SKILL.md with guidance on when to read them.

**Important**: Keep references one level deep from SKILL.md. Avoid deeply nested chains.

## Writing Effective Descriptions

Description is critical for skill discovery. The agent uses it to decide when to apply the skill.

### Rules

1. **Third person** (injected into system prompt):
   - Good: "Processes Excel files and generates reports"
   - Bad: "I can help you process Excel files"

2. **Specific with trigger terms**:
   - Good: "Extract text/tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
   - Bad: "Helps with documents"

3. **Include WHAT and WHEN** (the WHEN phrase is MANDATORY, not optional):
   - WHAT: specific capabilities
   - WHEN: trigger scenarios — an explicit phrase such as "Use when …" or "when the user …"
   - Enforced: `validate_skill.ts` (and flowai's `check-skills.ts` for every `skills/` primitive) reject a description that has no recognized WHEN-trigger phrase. Lazy forms ("How to X", "Helps with X", a bare domain label) fail.

### Constraints

| Field | Limit |
|-------|-------|
| `name` | Max 64 chars, `[a-z0-9-]` only, no leading/trailing/consecutive hyphens |
| `description` | Max 1024 chars, no angle brackets `<>` |
| `name + description` combined | **<100 tokens** (~400 chars; chars/4 approx) — the flowai validator `check-skills.ts` rejects over-budget catalog metadata. Agents load this tuple at session start for skill discovery; over-budget means the skill won't be visible. Aim for ~75 tokens to leave headroom. |
| `SKILL.md` body | **<5000 tokens** (~20000 chars; chars/4 approx) — also enforced by `check-skills.ts`. **Plan the budget BEFORE editing**: run `wc -c <SKILL.md>`; if `(current + planned-additions) / 4 > 4000` tokens, put the bulk in `references/<topic>.md` from the start instead of inlining. The cap rejects late, so retry-and-compress cycles waste tool calls. Multiple skills in this repo (`maintenance`, `engineer-skill`, `engineer-command`, `write-agent-benchmarks`, etc.) already follow this pattern — check their `references/` for prior art. |

## Common Patterns

### Template Pattern

Provide output format templates when consistent structure matters:

```markdown
## Report structure
ALWAYS use this template:
# [Title]
## Executive summary
[One-paragraph overview]
## Key findings
- Finding 1 with data
## Recommendations
1. Specific action
```

### Examples Pattern

For output quality dependent on seeing examples:

```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Workflow Pattern

Break complex operations into steps with checklists:

```markdown
## Workflow
- [ ] Step 1: Analyze input
- [ ] Step 2: Create mapping
- [ ] Step 3: Validate
- [ ] Step 4: Execute
- [ ] Step 5: Verify
```

### Conditional Workflow Pattern

Guide through decision points:

```markdown
1. Determine type:
   **Creating new?** -> "Creation workflow" below
   **Editing existing?** -> "Editing workflow" below
```

### Feedback Loop Pattern

For quality-critical tasks:

```markdown
1. Make edits
2. Validate: `deno run scripts/validate_skill.ts output/`
3. If fails -> fix -> validate again
4. Only proceed when validation passes
```

## Anti-Patterns

- **Windows paths**: Use `scripts/helper.py`, not `scripts\helper.py`
- **Too many options**: Provide a default with escape hatch, not a buffet
- **Time-sensitive info**: Use "Current method" / "Old patterns (deprecated)" sections
- **Inconsistent terminology**: Pick one term, use throughout
- **Vague names**: `code-review` not `helper` or `utils`

## Priming: Output Shape Teaches The Agent

Two lessons for authors changing a skill's output contract (what the final response should look like). Derived from debugging a skill whose output kept leaking into a file even after the `write to file` directive was removed.

### Embedded examples are ground truth

When SKILL.md contains an example output block, the agent treats the *shape* of that example as the imitation target. A directive like `"deliver findings inline in the response"` competes with an example that starts with `# Report Title (YYYY-MM-DD)` + `## 1. Section` + `- [ ] item` — and usually loses. That shape reads as "markdown file to save", and the agent saves it, regardless of the surrounding prose.

**Rule**: when changing an output contract, audit the example block, not just the directives. Drop file-shaped scaffolding:

- `#` / `##` headings → plain-text category labels (`1. Section Name`).
- Timestamped titles (`# Report (YYYY-MM-DD)`) → remove; chat responses don't need titles.
- `- [ ]` checkbox syntax → plain `-` bullets; checkboxes imply "tracked task file".

The shape must match the target delivery medium. For inline chat output, the example should read like a chat message.

### Remove the priming source, don't stack prohibitions

When unwanted behavior is primed by a rule, example shape, or system-level context (e.g., project `AGENTS.md` rules imported by a benchmark runner), the instinct is to add a negative constraint like `Do NOT create files` or `Rule X does NOT apply to this skill`. These rarely beat a shape-level or system-level prior — the agent has to pick a winner, often inconsistently.

**Better approach**: find the priming source inside the skill and remove it.

- Directive rule pointing at a file (`Output Target: write to <path>`) → delete the rule entirely.
- Section title with file connotations (`Reporting`, `Save report`, `Persist`) → rename (`Deliver findings`).
- Prose using "report" as a directive noun → switch to "findings" or "output".
- Example shaped like a document → reshape to chat-message form (see above).

Add explicit prohibitions only as a last resort, after reframing fails.

## Skill Creation Process

### Phase 1: Discovery

Gather from user:
1. Purpose and primary use case
2. Target IDE and storage location (personal vs project)
3. Trigger scenarios (when should agent apply this?)
4. Domain knowledge the agent lacks
5. Output format preferences
6. Existing patterns to follow

If context from prior conversation exists, infer the skill from discussed workflows/patterns.

### Phase 2: Design

1. Draft skill name (lowercase, hyphens, max 64 chars)
2. Write specific, third-person description with WHAT + WHEN
3. Outline main sections
4. Identify supporting files needed (references, scripts, assets)

### Phase 3: Implementation

1. Create directory structure
2. Write SKILL.md with frontmatter
3. Create supporting reference files
4. Create utility scripts if needed
5. Run `deno run -A scripts/init_skill.ts` for scaffolding if starting from scratch

### Phase 4: Verification (BLOCKING gate)

Run validation and do NOT finish until it exits 0:

```bash
deno run -A scripts/validate_skill.ts <path/to/skill-directory>
```

`validate_skill.ts` is the portable per-skill FLOOR. It rejects a missing, oversized, or angle-bracketed description AND a description with no WHEN-trigger phrase (e.g. "Use when …"). If it fails, FIX the description and re-run — never proceed while it is red.

> **Two validators, two roles.** `validate_skill.ts` (bundled here) is the portable floor that runs on ONE skill anywhere: it caps the description at the 1024-character agentskills.io limit. Inside the flowai repo, `scripts/check-skills.ts` is the repo-wide gate wired into `deno task check`, and it is far stricter. Three limits sit on one field there, and the tightest one binds: a 250-character cap on the description alone (the IDE skill-listing budget, applied to commands as well as skills), a 100-token cap on name+description (the agentskills.io catalog ceiling, which the 250-character cap now keeps out of reach), and the 1024-character spec limit above both. The repo gate also applies the same WHEN-trigger requirement to every `skills/` primitive. A description can pass the portable floor and still fail the repo gate on length, so when authoring inside flowai satisfy BOTH.

Description self-review rubric (BLOCKING — a "no" on any line means rewrite before finishing):
- [ ] WHAT — names the concrete capability (not the lazy "Helps with X" / "How to X")?
- [ ] WHEN — carries an explicit trigger phrase ("Use when …", "when the user …")?
- [ ] Specific — trigger terms a user would actually say, not a vague domain label?
- [ ] Third person — "Processes …", not "I can help you …"?
- [ ] Within budget — description at most 250 characters (the enforced cap inside flowai)?

Checklist:
- [ ] `validate_skill.ts` exits 0 (line count, description present + WHAT + WHEN, no angle brackets)
- [ ] Description passes the self-review rubric above
- [ ] Consistent terminology
- [ ] File references one level deep
- [ ] No time-sensitive information
- [ ] No auxiliary docs (README, CHANGELOG)
- [ ] Examples are concrete, not abstract

### Phase 5: Packaging

```bash
deno run -A scripts/package_skill.ts <path/to/skill-directory> [output-directory]
```

Creates a `.skill` zip file for distribution.

### Phase 6: Iterate

1. Use skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Test again

## Design Patterns Reference

- **Multi-step processes**: See [references/workflows.md](references/workflows.md)
- **Output formats and quality standards**: See [references/output-patterns.md](references/output-patterns.md)
