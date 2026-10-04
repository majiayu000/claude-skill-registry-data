---
name: manage-skills
description: This skill should be used when the user asks to "create a skill", "build a new skill", "write a SKILL.md", "improve a skill", "update a skill", "audit a skill", "verify a skill", or mentions skill structure, skill best practices, or skill authoring. Provides expert guidance for creating, updating, auditing, and managing Claude Code Skills.
---

<essential_principles>
Skills are modular, filesystem-based capabilities that provide domain expertise on demand. They follow the [Agent Skills](https://agentskills.io) open standard. Custom slash commands (`.claude/commands/`) have been merged into skills — existing commands keep working, but skills add directory support, frontmatter options, and auto-discovery.

**1. Skills Are Prompts** — All prompting best practices apply. Be clear, be direct, use XML structure. Assume Claude is smart — only add context Claude doesn't have.

**2. SKILL.md Is Always Loaded** — When a skill is invoked, Claude reads SKILL.md. Use this guarantee:
- Essential principles go in SKILL.md (can't be skipped)
- Workflow-specific content goes in workflows/
- Reusable knowledge goes in references/

**3. Router Pattern for Complex Skills:**
```
skill-name/
├── SKILL.md              # Router + principles
├── workflows/            # Step-by-step procedures (FOLLOW)
├── references/           # Domain knowledge (READ)
├── templates/            # Output structures (COPY + FILL)
└── scripts/              # Reusable code (EXECUTE)
```

SKILL.md asks "what do you want to do?" → routes to workflow → workflow specifies which references to read.

- **workflows/** — Multi-step procedures Claude follows
- **references/** — Domain knowledge Claude reads for context
- **templates/** — Consistent output structures Claude copies and fills (plans, specs, configs)
- **scripts/** — Executable code Claude runs as-is (deploy, setup, API calls, data processing)

**4. Pure XML Structure** — No markdown headings (#, ##, ###) in skill body. Use semantic XML tags (`<objective>`, `<process>`, `<success_criteria>`). Keep markdown formatting within content (bold, lists, code blocks).

**5. Progressive Disclosure** — SKILL.md under 500 lines. Split detailed content into reference files. Load only what's needed for the current workflow.

**6. Two Types of Skill Content:**
- **Reference content** — conventions, patterns, domain knowledge. Runs inline alongside conversation.
- **Task content** — step-by-step actions with side effects. Often set `disable-model-invocation: true` so only users trigger it. Task skills often use `context: fork` to run in a subagent.

**7. Invocation Control** — Three modes via frontmatter:
- **Default** — both user (`/skill-name`) and Claude can invoke
- **`disable-model-invocation: true`** — user-only (for deploy, commit, destructive actions)
- **`user-invocable: false`** — Claude-only (for background knowledge skills)

**8. Subagent Execution** — Add `context: fork` to run a skill in an isolated subagent. The skill content becomes the subagent's prompt (no access to conversation history). CLAUDE.md is also loaded. The `agent` field selects the execution environment (`Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`). Default: `general-purpose`. See [references/advanced-patterns.md](references/advanced-patterns.md).

**9. Tool Restriction** — `allowed-tools` limits which tools Claude can use when a skill is active. Supports tool-specific patterns: `Bash(gh *)` allows only `gh` commands. Your permission settings still govern all other tools. You can also restrict Claude's skill access via permission rules: `Skill(name)` for exact match, `Skill(name *)` for prefix match.

**10. Extended Thinking** — Include the word "ultrathink" anywhere in skill content to enable extended thinking mode.
</essential_principles>

<intake>
What would you like to do?

1. Create new skill
2. Audit/modify existing skill
3. Add component (workflow/reference/template/script)
4. Get guidance

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action | Workflow |
|----------|-------------|----------|
| 1, "create", "new", "build" | Ask: "Task-execution skill or domain expertise skill?" | Route to appropriate create workflow |
| 2, "audit", "modify", "existing" | Ask: "Path to skill?" | Route to appropriate workflow |
| 3, "add", "component" | Ask: "Add what? (workflow/reference/template/script)" | workflows/add-{type}.md |
| 4, "guidance", "help" | General guidance | workflows/get-guidance.md |

**Progressive disclosure for option 1 (create):**
- If user selects "Task-execution skill" → workflows/create-new-skill.md
- If user selects "Domain expertise skill" → workflows/create-domain-expertise-skill.md

**Progressive disclosure for option 3 (add component):**
- If user specifies workflow → workflows/add-workflow.md
- If user specifies reference → workflows/add-reference.md
- If user specifies template → workflows/add-template.md
- If user specifies script → workflows/add-script.md

**Intent-based routing (if user provides clear intent without selecting menu):**
- "audit this skill", "check skill", "review" → workflows/audit-skill.md
- "verify content", "check if current" → workflows/verify-skill.md
- "create domain expertise", "exhaustive knowledge base" → workflows/create-domain-expertise-skill.md
- "create skill for X", "build new skill" → workflows/create-new-skill.md
- "add workflow", "add reference", etc. → workflows/add-{type}.md
- "upgrade to router" → workflows/upgrade-to-router.md

**After reading the workflow, follow it exactly.**
</routing>

<quick_reference>
**Simple skill (single file):**
```yaml
---
name: skill-name
description: What it does and when to use it.
---

<objective>What this skill does</objective>
<quick_start>Immediate actionable guidance</quick_start>
<process>Step-by-step procedure</process>
<success_criteria>How to know it worked</success_criteria>
```

**Complex skill (router pattern):**
```
SKILL.md:
  <essential_principles> - Always applies
  <intake> - Question to ask
  <routing> - Maps answers to workflows

workflows/:
  <required_reading> - Which refs to load
  <process> - Steps
  <success_criteria> - Done when...

references/:
  Domain knowledge, patterns, examples

templates/:
  Output structures Claude copies and fills
  (plans, specs, configs, documents)

scripts/:
  Executable code Claude runs as-is
  (deploy, setup, API calls, data processing)
```
</quick_reference>

<reference_index>
All in `references/`:

**Structure:** recommended-structure.md, skill-structure.md
**Principles:** core-principles.md, be-clear-and-direct.md, use-xml-tags.md
**Patterns:** common-patterns.md, workflows-and-validation.md
**Assets:** using-templates.md, using-scripts.md
**Advanced:** advanced-patterns.md, executable-code.md, api-security.md, iteration-and-testing.md
</reference_index>

<workflows_index>
All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| create-new-skill.md | Build a skill from scratch |
| create-domain-expertise-skill.md | Build exhaustive domain knowledge base for build/ |
| audit-skill.md | Analyze skill against best practices |
| verify-skill.md | Check if content is still accurate |
| add-workflow.md | Add a workflow to existing skill |
| add-reference.md | Add a reference to existing skill |
| add-template.md | Add a template to existing skill |
| add-script.md | Add a script to existing skill |
| upgrade-to-router.md | Convert simple skill to router pattern |
| get-guidance.md | Help decide what kind of skill to build |
</workflows_index>

<yaml_requirements>
Only `description` is recommended. All other fields are optional:

```yaml
---
name: skill-name                    # Optional. Defaults to directory name. Lowercase, hyphens, max 64 chars.
description: ...                    # Recommended. What it does + trigger phrases. Fallback: first paragraph of content.
disable-model-invocation: false     # true = user-only invocation (for deploy, commit, etc.)
user-invocable: true                # false = Claude-only (background knowledge, hide from / menu)
allowed-tools: Read, Grep, Glob     # Tools granted without per-use permission prompts
argument-hint: [issue-number]       # Autocomplete hint for arguments
model: sonnet                       # Model to use when skill is active
context: fork                       # Run in forked subagent context. SKILL.md content becomes the prompt. CLAUDE.md also loads.
agent: Explore                      # Subagent type when context: fork (Explore, Plan, general-purpose, or custom from .claude/agents/). Default: general-purpose.
hooks: ...                          # Hooks scoped to skill lifecycle
---
```

**String substitutions** in skill content: DOLLAR+ARGUMENTS, DOLLAR+ARGUMENTS[N] / DOLLAR+N, DOLLAR+CLAUDE_SESSION_ID. Dynamic shell injection: BANG + backtick-wrapped command. See [references/advanced-patterns.md](references/advanced-patterns.md) for exact syntax.

**Description best practice** — include specific trigger phrases:
```yaml
description: This skill should be used when the user asks to "create a hook", "add a PreToolUse hook", or mentions hook events. Provides comprehensive hooks API guidance.
```

**Name conventions:** `create-*`, `manage-*`, `setup-*`, `generate-*`, `build-*`

**Skill locations** (higher priority wins; skills beat commands with same name):
| Level | Path |
|-------|------|
| Enterprise | Managed settings |
| Personal | `~/.claude/skills/<name>/SKILL.md` |
| Project | `.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` |
</yaml_requirements>

<success_criteria>
A well-structured skill:
- Has valid YAML frontmatter
- Uses pure XML structure (no markdown headings in body)
- Has essential principles inline in SKILL.md
- Routes directly to appropriate workflows based on user intent
- Keeps SKILL.md under 500 lines
- Asks minimal clarifying questions only when truly needed
- Has been tested with real usage
- Configures invocation control appropriately (disable-model-invocation for side-effect skills)
- Uses trigger phrases in description for reliable discovery
</success_criteria>
