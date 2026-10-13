---
name: skill-creator
description: "Guide for creating new Claude Code skills AND tweaking/fixing existing ones. Use when: (1) User wants to create a new skill, (2) User wants to improve, fix, or tweak an existing skill, (3) User says 'create skill', 'new skill', 'fix skill', 'update skill', 'tweak skill', 'skill not working', or 'skill triggers too often'. Covers skill anatomy (SKILL.md, scripts/, references/, assets/), progressive disclosure, frontmatter, bundled resources, init_skill.py, diagnosing trigger/behavior issues, and iteration."
---

# Skill Creator

This skill provides guidance for creating new skills **and** tweaking existing ones.

For tweaking an existing skill, jump to ["Tweaking an Existing Skill"](#tweaking-an-existing-skill). For new skills, follow the Skill Creation Process below.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Principles

### Concise is Key

The context window is a public good. Skills share the context window with everything else Claude needs: system prompt, conversation history, other Skills' metadata, and the actual user request.

**Default assumption: Claude is already very smart.** Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this explanation?" and "Does this paragraph justify its token cost?"

Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

Match the level of specificity to the task's fragility and variability:

**High freedom (text-based instructions)**: Use when multiple approaches are valid, decisions depend on context, or heuristics guide the approach.

**Medium freedom (pseudocode or scripts with parameters)**: Use when a preferred pattern exists, some variation is acceptable, or configuration affects behavior.

**Low freedom (specific scripts, few parameters)**: Use when operations are fragile and error-prone, consistency is critical, or a specific sequence must be followed.

Think of Claude as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom).

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata
│   │   ├── name: (optional — defaults to the directory name)
│   │   └── description: (recommended)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Every SKILL.md consists of:

- **Frontmatter** (YAML): `description` is the field Claude reads to decide when to use the skill, so it is very important to be clear and comprehensive in describing what the skill is and when it should be used. `name` sets the display label shown in skill listings and defaults to the directory name if omitted.
- **Body** (Markdown): Instructions and guidance for using the skill. Only loaded AFTER the skill triggers (if at all).

**Case-sensitivity warning (macOS):** The canonical file name is `SKILL.md` (uppercase). On case-insensitive filesystems (macOS), if a skill directory already contains `skill.md` (lowercase), creating `SKILL.md` will overwrite it on disk but git will track both as separate index entries, causing clone-time collision warnings. Before creating or renaming: check for existing variants with `git ls-files '<skill-dir>/'` and remove any lowercase duplicate with `git rm --cached '<path>/skill.md'`.

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

#### What to Not Include in a Skill

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files, including:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

The skill should only contain the information needed for an AI agent to do the job at hand. It should not contain auxilary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc. Creating additional documentation files just adds clutter and confusion.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited because scripts can be executed without reading into context window)

#### Progressive Disclosure Patterns

Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat. Split content into separate files when approaching this limit. When splitting out content into other files, it is very important to reference them from SKILL.md and describe clearly when to read them, to ensure the reader of the skill knows they exist and when to use them.

**Key principle:** When a skill supports multiple variations, frameworks, or options, keep only the core workflow and selection guidance in SKILL.md. Move variant-specific details (patterns, examples, configuration) into separate reference files.

**Pattern 1: High-level guide with references**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.

**Pattern 2: Domain-specific organization**

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When a user asks about sales metrics, Claude only reads sales.md.

Similarly, for skills supporting multiple frameworks or variants, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When the user chooses AWS, Claude only reads aws.md.

**Pattern 3: Conditional details**

Show basic content, link to advanced content:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Claude reads REDLINING.md or OOXML.md only when the user needs those features.

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md.
- **Structure longer reference files** - For files longer than 100 lines, include a table of contents at the top so Claude can see the full scope when previewing.

## Skill Creation Process

Skill creation involves these steps:

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Format SKILL.md with mdx-formatter
6. Iterate based on real usage

Follow these steps in order.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

**Capture intent from the current conversation first.** If the user says something like "turn this into a skill" or "make this a skill", extract answers from the conversation history before asking questions: the tools used, the sequence of steps, corrections the user made, input/output formats already observed. Then confirm gaps with the user instead of starting an interview from scratch.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <parent-directory>
```

**Important**: `--path` is the **parent** directory. The script appends `<skill-name>` automatically.
If `--path` already ends with `<skill-name>`, it won't double-nest.

```bash
# Correct: creates $HOME/.claude/skills/my-skill/SKILL.md
scripts/init_skill.py my-skill --path $HOME/.claude/skills

# Also correct (no double-nesting): creates $HOME/.claude/skills/my-skill/SKILL.md
scripts/init_skill.py my-skill --path $HOME/.claude/skills/my-skill
```

The script:

- Creates the skill directory at `<parent-directory>/<skill-name>/`
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

#### Learn Proven Design Patterns

Consult these helpful guides based on your skill's needs:

- **Multi-step processes**: See references/workflows.md for sequential workflows and conditional logic
- **Specific output formats or quality standards**: See references/output-patterns.md for template and example patterns

These files contain established best practices for effective skill design.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Added scripts must be tested by actually running them to ensure there are no bugs and that the output matches what is expected. If there are many similar scripts, only a representative sample needs to be tested to ensure confidence that they all work while balancing time to completion.

Any example files and directories not needed for the skill should be deleted. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

**Path Safety Rule:** In skill instructions, always use `$HOME` instead of `~` (tilde) for home directory references. The `~` character is only expanded by interactive shells -- it is NOT expanded by Node.js `fs` operations, Python `open()`, or non-login shell contexts. Using `~` in file paths can create a literal directory named `~/` inside the working directory instead of resolving to the user's home directory. For example, write `$HOME/cclogs/...` and `$HOME/.claude/...`, never `~/cclogs/...` or `~/.claude/...`.

##### Frontmatter

Write the YAML frontmatter. `description` is recommended so Claude knows when to trigger the skill; `name` is optional and defaults to the directory name if omitted. See [frontmatter.md](references/frontmatter.md) for all available fields including:

- **Invocation control**: `disable-model-invocation`, `user-invocable`, `argument-hint`
- **Execution control**: `allowed-tools`, `model`, `context`, `agent`, `hooks`
- **String substitutions**: `$ARGUMENTS`, `$N`, `${CLAUDE_SESSION_ID}`
- **Dynamic context injection**: bang-backtick syntax for shell command output

Basic example:

- `name`: The skill name
- `description`: Primary triggering mechanism. Include what the skill does AND when to use it.
  - Example: "Comprehensive document editing with tracked changes. Use when: (1) Creating new documents, (2) Modifying content, (3) Working with tracked changes"
  - **Be slightly pushy.** Claude tends to undertrigger skills — to skip them when they'd be useful. Counter this by making the description explicit about when to use the skill, even on near-misses. Instead of "How to build a fast dashboard for internal data.", write "How to build a fast dashboard for internal data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"

##### Body

Write instructions for using the skill and its bundled resources.

### Step 5: Format SKILL.md

Format the SKILL.md file using the mdx-formatter to ensure consistent markdown formatting:

```bash
pnpm dlx @takazudo/mdx-formatter --write <path-to-SKILL.md>
```

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

**Writing principles when revising:**

- **Generalize from feedback, don't overfit.** A skill is meant to be used many times across many prompts. If a fix only works for the one example you tested on, it's noise. Reach for a different metaphor or pattern instead of piling on rigid rules.
- **Keep the prompt lean.** Remove instructions that aren't pulling their weight. If you can read the skill's transcript and see Claude wasting time on something the skill told it to do, cut that part.
- **Explain the why, don't pile on MUSTs.** Today's models have good theory of mind — when you explain *why* something matters, they handle edge cases on their own. Heavy-handed all-caps "ALWAYS" / "NEVER" / "MUST" is a yellow flag: usually you can reframe with a one-sentence explanation of the underlying reason and get better results with less rigidity.
- **Look for repeated work → bundle as scripts.** If you notice Claude rewriting the same helper across multiple uses of the skill (a parser, a formatter, a config builder), that's a strong signal to write it once into `scripts/` and have the skill point to it.

## Tweaking an Existing Skill

Use this flow when fixing, improving, or adjusting a skill that already exists. It reuses the formatting, path-safety, and frontmatter guidance from the creation flow above — don't duplicate that work here, just defer to those sections.

### Step 1: Identify the skill file

Skills live at `$HOME/.claude/skills/<name>/SKILL.md` (personal) or `.claude/skills/<name>/SKILL.md` (project).

**Case-sensitivity check (macOS):** the file may be `SKILL.md` or `skill.md`. On a case-insensitive filesystem both resolve to the same file on disk, but git tracks them as separate index entries. Run `git ls-files --stage '<skill-dir>/'` to see what's actually tracked, and if both variants exist, remove the duplicate via `git rm --cached '<path>/<wrong-case>.md'`. Edit the variant that matches the rest of the project.

Read the skill file and any referenced files in `scripts/`, `references/`, `assets/`.

### Step 2: Diagnose

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Skill not triggering | `description` missing trigger keywords | Rewrite with explicit triggers and "use when" scenarios. Claude tends to **undertrigger** — make the description slightly pushy ("use this whenever the user mentions X, Y, or Z, even if they don't explicitly ask for it") |
| Skill triggers too often | `description` too broad | Narrow it; or set `disable-model-invocation: true` for manual-only |
| Skill not visible in `/context` | Description budget exceeded | Shorten description, or raise `SLASH_COMMAND_TOOL_CHAR_BUDGET` |
| Wrong agent in fork mode | `agent:` field incorrect | Set the correct agent name |
| Forked skill lacks context | Skill body assumes conversation history | In fork mode the skill body IS the prompt — make it self-contained |
| Bundled script fails | Bug or env issue | Read and run the script; fix in place |

### Step 3: Apply changes

When inserting a new step into a numbered step list (`Step 1`, `Step 2`, ...), **renumber the steps** so the sequence stays contiguous. Avoid `Step 2.5` or `Step 0`. After renumbering, grep the file for stale references ("proceed to Step 3" where you now mean Step 4) and fix them, including any sibling files (scripts, references, TODO checklists) that mention step numbers.

For frontmatter changes, see [references/frontmatter.md](references/frontmatter.md) — same fields apply whether creating or tweaking.

When rewriting body content, the same iteration principles from "Step 6: Iterate" apply: generalize over special-casing, prefer one-sentence "why" over piles of `MUST` / `ALWAYS` / `NEVER`, and cut sentences that aren't pulling their weight.

### Step 4: Format and verify

Format with `pnpm dlx @takazudo/mdx-formatter --write <path-to-SKILL.md>` (same as creation Step 5). Then verify:

1. YAML frontmatter parses
2. Description matches the intended trigger scenarios
3. Referenced files exist and are correct
4. For forked skills: body is self-contained
5. SKILL.md stays under ~500 lines (otherwise split into `references/`)
6. No `~/` paths — use `$HOME/` (see "Path Safety Rule" in Step 4 of creation)

## Skill Locations

Where a skill is stored determines its scope:

| Location | Path | Applies to |
|----------|------|------------|
| Enterprise | Managed settings | All users in organization |
| Personal | `$HOME/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled |

**Priority**: Enterprise > Personal > Project. Plugin skills use `plugin-name:skill-name` namespace.

**Monorepo support**: Skills in nested `.claude/skills/` directories are auto-discovered when working in subdirectories.

## Troubleshooting

### Skill not triggering

1. Check description includes keywords users would naturally say
2. Verify skill appears in "What skills are available?"
3. Try rephrasing request to match description
4. Invoke directly with `/skill-name`

### Skill triggers too often

1. Make description more specific
2. Add `disable-model-invocation: true` for manual-only invocation

### Claude doesn't see all skills

Skill descriptions share a character budget (default 15,000). Run `/context` to check for excluded skills. Increase with `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

## Advanced Patterns

### Eval-Driven Skill Development

This skill is intentionally a lightweight scaffolder. For skills that need to be reliable across many uses (team-shared, public release, business-critical), Anthropic ships a heavier eval-driven version of skill-creator at github.com/anthropics/skills (install via `/plugin marketplace add anthropics/skills`). It runs parallel subagent test cases, produces benchmark.json with mean ± stddev, opens an HTML eval viewer, and includes a description-optimization loop. Use that one when the skill quality matters enough to justify the token cost and setup time.

### Visual Output

Skills can generate interactive HTML files that open in browser:

```
my-visualizer/
├── SKILL.md
└── scripts/
    └── visualize.py  # Generates HTML, opens in browser
```

Use `allowed-tools: Bash(python *)` to allow script execution without permission prompts.
