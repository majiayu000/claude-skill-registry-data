---
name: commands-manager
description: "Branch skill for building and improving commands. Use when creating new slash commands, adapting marketplace commands, validating command structure, working with $ARGUMENTS, or improving existing commands. Triggers: 'create command', 'improve command', 'validate command', 'fix command', 'slash command', '$ARGUMENTS', 'adapt command', 'multi-phase command', 'command frontmatter'."
---

# Commands Manager - Branch of JARVIS-06

Build and improve commands following the commands-management policy.

## Policy Source

**Primary policy**: JARVIS-06 → `.claude/skills/commands-management/SKILL.md`

This branch **executes** the policy defined by JARVIS-06. Always sync with Primary before major operations.

## Quick Decision Tree

```text
Task Received
    │
    ├── Create new command? ─────────────> Workflow 1: Build
    │   └── What type?
    │       ├── Simple action ───────────> Single-phase command
    │       ├── Complex workflow ────────> Multi-phase command
    │       └── Skill invocation ────────> Skill-invoking command
    │
    ├── Adapt marketplace command? ──────> Workflow 3: Adapt
    │
    ├── Fix existing command? ───────────> Workflow 2: Improve
    │
    └── Validate command? ───────────────> Validation Checklist
```

## Command Overview

Slash commands are frequently-used prompts defined as Markdown files that Claude executes during interactive sessions.

**Key concepts:**
- Markdown file format for commands
- YAML frontmatter for configuration
- Dynamic arguments ($ARGUMENTS, $1, $2)
- File references (@$1, @file.txt)
- Bash execution for context (!`command`)
- Commands are instructions FOR Claude, not messages TO user

## Critical: Commands are Instructions FOR Claude

**Commands are written for agent consumption, not human consumption.**

When a user invokes `/command-name`, the command content becomes Claude's instructions.

**Correct (instructions for Claude):**

```markdown
Review this code for security vulnerabilities including:
- SQL injection
- XSS attacks
- Authentication issues

Provide specific line numbers and severity ratings.
```

**Incorrect (messages to user):**

```markdown
This command will review your code for security issues.
You'll receive a report with vulnerability details.
```

Always use the first approach - tell Claude what to do.

## Command Locations

| Location | Scope | Label | Use For |
|----------|-------|-------|---------|
| `.claude/commands/` | Project | (project) | Team workflows, project-specific |
| `~/.claude/commands/` | User | (user) | Personal workflows, cross-project |
| `plugin/commands/` | Plugin | (plugin-name) | Plugin-bundled functionality |

## Command Types

| Type | Phases | Use When |
|------|--------|----------|
| Single-phase | 1 | Simple, direct action |
| Multi-phase | 2-4 | Complex workflow with stages |
| Skill-invoking | 1+ | Needs skill knowledge |

## Workflow 1: Build New Command

### Step 1: Define Command Purpose

Answer these questions:

- What task does this command automate?
- What arguments does it need (if any)?
- What tools should it use?
- Does it need multiple phases?
- Should it invoke a skill?
- Does it need bash execution for context?

### Step 2: Write Frontmatter

```yaml
---
description: Brief description for /help (<60 chars)
argument-hint: [file-path] [options]
allowed-tools: Read, Write, Edit, Bash(git:*)
model: inherit
---
```

**Frontmatter fields:**

| Field | Required | Purpose | Example |
|-------|----------|---------|---------|
| description | Yes | Shows in /help, max 60 chars | "Review code for security issues" |
| argument-hint | If args | Shows expected arguments | "[file-path] [options]" |
| allowed-tools | Optional | Restricts available tools | "Read, Bash(git:*)" |
| model | Optional | Override model | sonnet/opus/haiku |
| disable-model-invocation | Optional | Prevent programmatic calls | true |

### Step 3: Write Command Body

**Single-Phase Template:**

```markdown
---
description: [What it does in <60 chars]
argument-hint: [expected-args]
allowed-tools: Read, Write, Edit
---

[Action verb] the [target] to [achieve goal]:

1. [First step with specific action]
2. [Second step]
3. [Third step]

Report [expected output format].
```

**Multi-Phase Template:**

```markdown
---
description: [What it does]
argument-hint: [args]
---

## Phase 1: Analysis

Analyze [target] for [criteria]:

1. [Analysis step 1]
2. [Analysis step 2]

Document findings before proceeding.

## Phase 2: Implementation

Based on Phase 1 findings, implement [changes]:

1. [Implementation step 1]
2. [Implementation step 2]

## Phase 3: Verification

Verify implementation:

1. [Verification step 1]
2. [Verification step 2]

Report completion status with summary.
```

**Skill-Invoking Template:**

```markdown
---
description: [What it does]
disable-model-invocation: true
---

Invoke the [skill-name] skill to [purpose].

Follow the skill's workflow for [specific task].

Report results following skill's output format.
```

### Step 4: Use Arguments Correctly

| Syntax | Purpose | Example |
|--------|---------|---------|
| $ARGUMENTS | All args as single string | "Fix issue #$ARGUMENTS" |
| $1, $2, $3 | Positional arguments | "Compare $1 with $2" |
| @$1 | Include file contents | "Review code in @$1" |
| @file.txt | Static file reference | "Load @config.json" |

**Examples:**

```markdown
# Using $ARGUMENTS (all args)
---
description: Create PR with given title
argument-hint: [title]
---

Create a pull request with title: $ARGUMENTS

# Using positional args
---
description: Compare two files
argument-hint: [file1] [file2]
---

Compare the contents of @$1 with @$2

# Using @$1 for file content
---
description: Review code file
argument-hint: [file-path]
---

Review the following code for issues:

@$1

Provide feedback on quality and suggestions.
```

### Step 5: Add Bash Execution (if needed)

Use `!` backticks to execute bash and include output:

```markdown
---
description: Review changed files
allowed-tools: Read, Bash(git:*)
---

Files changed: !`git diff --name-only`

Review each file for:
1. Code quality and style
2. Potential bugs or issues
3. Test coverage

Provide specific feedback for each file.
```

**Bash execution patterns:**

```markdown
# Get git status
Current branch: !`git branch --show-current`

# Run tests
Test results: !`npm test 2>&1`

# Check environment
Node version: !`node --version`
```

**Note:** Requires `Bash` in `allowed-tools` with appropriate pattern.

### Step 6: Save and Validate

Save to: `commands/[command-name].md`

Run validation checklist.

## Workflow 2: Improve Existing Command

### Step 1: Analyze Current State

```bash
# Read command file
cat commands/[name].md

# Check for common issues:
# - Written as message TO user?
# - Missing description?
# - No argument-hint when needed?
# - Missing output format?
```

### Step 2: Gap Analysis

| Component | Check | Common Issues |
|-----------|-------|---------------|
| description | Present? <60 chars? | Missing or too long |
| argument-hint | Present if args needed? | Missing when command takes args |
| body | Instructions FOR Claude? | Written as "This command will..." |
| body | Imperative form? | Uses "I will" or "should" |
| output | Defined? | No "Report..." section |
| bash | Correct syntax? | Wrong backtick pattern |

### Step 3: Apply Fixes

**Converting message to instructions:**

Before (wrong):

```markdown
This command will analyze your code and find bugs.
You'll receive a report when it's done.
```

After (correct):

```markdown
Analyze the code for bugs and issues:

1. Search for common error patterns
2. Check for security vulnerabilities
3. Identify performance issues

Report findings with severity levels and fix suggestions.
```

**Adding output format:**

```markdown
Report results as:
- Summary: [1-2 sentences]
- Findings: [Bulleted list]
- Recommendations: [Action items]
```

**Converting to multi-phase:**

```markdown
## Phase 1: Discovery
[Analysis steps]

## Phase 2: Action
[Implementation steps]

## Phase 3: Verification
[Check steps]
```

**Fixing bash execution:**

Wrong:

```markdown
`git status`
```

Correct:

```markdown
!`git status`
```

### Step 4: Validate

Run full validation checklist.

## Workflow 3: Adapt Marketplace Command

When taking a command from wshobson-agents, obra-superpowers, or similar:

### Step 1: Read Original Command

```bash
cat marketplace-plugin/commands/[command].md
```

Note:
- Frontmatter structure
- Phase structure (if multi-phase)
- Argument handling
- Tool restrictions
- Bash execution patterns

### Step 2: Identify JARVIS Fit

| Original Purpose | JARVIS Application |
|------------------|-------------------|
| Generic code review | Category-specific code review |
| Generic deployment | MCP-aware deployment |
| Generic testing | Category testing patterns |
| Generic workflow | 4-plugin aware workflow |

### Step 3: Adapt Frontmatter

**Original:**

```yaml
---
description: Review code for issues
---
```

**Adapted for JARVIS:**

```yaml
---
description: Review code following JARVIS standards
argument-hint: [file-path]
allowed-tools: Read, Grep, Glob
---
```

### Step 4: Adapt Body

**Add JARVIS-specific context:**

```markdown
Review the code following JARVIS ecosystem standards:

1. Check compliance with Primary Skill patterns
2. Verify MCP tool usage follows category guidelines
3. Ensure 4-plugin architecture is respected
4. Validate CLAUDE.md references are current

Report findings with JARVIS-specific recommendations.
```

**Add category-specific instructions:**

```markdown
For this category (JARVIS-XX), additionally check:
- [Category-specific check 1]
- [Category-specific check 2]
```

### Step 5: Validate Adaptation

Run full validation checklist.

## Plugin Command Features

### CLAUDE_PLUGIN_ROOT Variable

Plugin commands can reference plugin files portably:

```markdown
---
description: Analyze using plugin script
allowed-tools: Bash(node:*)
---

Run analysis: !`node ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.js $1`

Review results and report findings.
```

**Common patterns:**

```markdown
# Execute plugin script
!`bash ${CLAUDE_PLUGIN_ROOT}/scripts/script.sh`

# Load plugin configuration
@${CLAUDE_PLUGIN_ROOT}/config/settings.json

# Use plugin template
@${CLAUDE_PLUGIN_ROOT}/templates/report.md

# Access plugin resources
@${CLAUDE_PLUGIN_ROOT}/docs/reference.md
```

### Plugin Command Organization

```text
plugin-name/
├── commands/
│   ├── foo.md              # /foo (plugin:plugin-name)
│   ├── bar.md              # /bar (plugin:plugin-name)
│   └── utils/
│       └── helper.md       # /helper (plugin:plugin-name:utils)
└── plugin.json
```

Subdirectories create namespaces shown in `/help`.

### Integration with Plugin Components

**Agent integration:**

```markdown
---
description: Deep code review
argument-hint: [file-path]
---

Initiate comprehensive review of @$1 using the code-reviewer agent.

The agent will analyze:
- Code structure
- Security issues
- Performance
- Best practices
```

**Skill integration:**

```markdown
---
description: Document API with standards
argument-hint: [api-file]
---

Document API in @$1 following plugin standards.

Use the api-docs-standards skill to ensure:
- Complete endpoint documentation
- Consistent formatting
- Example quality
```

**Multi-component workflow:**

```markdown
---
description: Comprehensive review workflow
argument-hint: [file]
allowed-tools: Bash(node:*), Read
---

Target: @$1

Phase 1 - Static Analysis:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

Phase 2 - Deep Review:
Launch code-reviewer agent for detailed analysis.

Phase 3 - Standards Check:
Use coding-standards skill for validation.

Phase 4 - Report:
Template: @${CLAUDE_PLUGIN_ROOT}/templates/review.md

Compile findings into report following template.
```

## Validation Patterns

### Argument Validation

```markdown
---
description: Deploy with validation
argument-hint: [environment]
---

Validate environment: !`echo "$1" | grep -E "^(dev|staging|prod)$" || echo "INVALID"`

If $1 is valid environment:
  Deploy to $1
Otherwise:
  Explain valid environments: dev, staging, prod
  Show usage: /deploy [environment]
```

### File Existence Checks

```markdown
---
description: Process configuration
argument-hint: [config-file]
---

Check file exists: !`test -f $1 && echo "EXISTS" || echo "MISSING"`

If file exists:
  Process configuration: @$1
Otherwise:
  Explain where to place config file
  Provide example configuration
```

### Plugin Resource Validation

```markdown
---
description: Run plugin analyzer
allowed-tools: Bash(test:*)
---

Validate plugin setup:
- Script: !`test -x ${CLAUDE_PLUGIN_ROOT}/bin/analyze && echo "OK" || echo "MISSING"`
- Config: !`test -f ${CLAUDE_PLUGIN_ROOT}/config.json && echo "OK" || echo "MISSING"`

If all checks pass, run analysis.
Otherwise, report missing components.
```

## Validation Checklist

### Structure

- [ ] File in `commands/` directory with `.md` extension
- [ ] Filename is lowercase with hyphens
- [ ] Valid YAML frontmatter between `---` markers

### Frontmatter

- [ ] `description` present and under 60 characters
- [ ] `argument-hint` present if command takes arguments
- [ ] `allowed-tools` present if tool restriction needed
- [ ] `model` valid if specified (sonnet/opus/haiku/inherit)

### Body Content

- [ ] Written as instructions FOR Claude (imperative)
- [ ] Does NOT use "I will", "This command will", "You'll get"
- [ ] Uses action verbs: "Analyze", "Create", "Review", "Check"
- [ ] Has numbered steps for procedures
- [ ] Has "Report..." section defining output format

### Arguments (if applicable)

- [ ] $ARGUMENTS used correctly for all args
- [ ] $1, $2, $3 used correctly for positional args
- [ ] @$1 used correctly for file content inclusion
- [ ] argument-hint matches actual usage

### Bash Execution (if applicable)

- [ ] Uses `!` backticks syntax (!`command`)
- [ ] `allowed-tools` includes Bash with appropriate pattern
- [ ] Commands are safe and tested
- [ ] Error output handled (2>&1 if needed)

### Multi-Phase (if applicable)

- [ ] Phases clearly marked with ## headers
- [ ] Each phase has distinct purpose
- [ ] Phases build on each other logically
- [ ] Final phase includes verification

### Plugin Commands (if applicable)

- [ ] Uses ${CLAUDE_PLUGIN_ROOT} for plugin paths
- [ ] No hardcoded absolute paths
- [ ] Resources exist in plugin

## Command Examples

### Example 1: Simple Review Command

```markdown
---
description: Review file for code quality
argument-hint: [file-path]
allowed-tools: Read, Grep
---

Review @$1 for code quality issues:

1. Check for code style violations
2. Identify potential bugs
3. Look for performance issues
4. Verify error handling

Report findings with:
- Issue: [description]
- Severity: [high/medium/low]
- Suggestion: [fix recommendation]
```

### Example 2: Multi-Phase Deployment Command

```markdown
---
description: Deploy category to production
argument-hint: [category-number]
allowed-tools: Read, Bash(git:*), Bash(gcloud:*)
---

## Phase 1: Pre-Deployment Checks

Verify JARVIS-$1 is ready for deployment:

1. Check all tests pass
2. Verify CLAUDE.md is up to date
3. Confirm Primary Skill has no TODOs
4. Validate mcp.json configuration

Document any issues before proceeding.

## Phase 2: Deployment

Deploy JARVIS-$1:

1. Tag the release with version
2. Push to production branch
3. Deploy MCP server if applicable
4. Update BigQuery tables if needed

## Phase 3: Verification

Verify deployment success:

1. Test MCP tools are responding
2. Verify category loads correctly
3. Check logs for errors

Report deployment status with:
- Version deployed
- Components updated
- Any issues encountered
```

### Example 3: Skill-Invoking Command

```markdown
---
description: Improve category following dev cycle
argument-hint: [category-number]
disable-model-invocation: true
---

Invoke the category-optimizer skill for JARVIS-$1.

Follow the skill's self-improvement cycle:

1. Analyze current CLAUDE.md
2. Review settings.json
3. Check Primary Skill completeness
4. Apply improvements

Report all changes made following the skill's output format.
```

### Example 4: Plugin Command with Bash

```markdown
---
description: Run full analysis pipeline
argument-hint: [target-file]
allowed-tools: Read, Bash(node:*)
---

Target: @$1

Run analysis pipeline:

Step 1 - Lint:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/lint.js $1`

Step 2 - Type Check:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/typecheck.js $1`

Step 3 - Security Scan:
!`node ${CLAUDE_PLUGIN_ROOT}/scripts/security.js $1`

Compile all findings and provide summary with:
- Total issues found
- Issues by severity
- Recommended fixes
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Command not appearing | Wrong directory | Check .claude/commands/ or commands/ |
| Command not appearing | Missing .md extension | Add .md extension |
| Arguments not working | Wrong syntax | Use $1 not ${1}, $ARGUMENTS not ${ARGUMENTS} |
| File reference fails | Missing @ | Use @$1 not $1 for file content |
| Bash not executing | Wrong syntax | Use !`cmd` not `cmd` or $(cmd) |
| Bash fails | No tool permission | Add Bash(pattern:*) to allowed-tools |
| Plugin path fails | Wrong variable | Use ${CLAUDE_PLUGIN_ROOT} not $PLUGIN_ROOT |

## Common Issues & Fixes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Written as message | Uses "This command will" | Rewrite with imperative verbs |
| No output format | Missing "Report..." | Add output specification |
| Args not working | Wrong syntax | Check $ARGUMENTS vs $1 vs @$1 |
| Too vague | "Check the code" | Add specific numbered steps |
| Missing hint | Takes args but no hint | Add argument-hint field |
| Tool errors | Needs restricted tool | Add allowed-tools field |
| Bash not running | Missing allowed-tools | Add Bash(pattern:*) |

## Best Practices

**DO:**
- ✅ Write instructions FOR Claude
- ✅ Use imperative verbs (Analyze, Create, Review)
- ✅ Include numbered steps for procedures
- ✅ Define output format with "Report..."
- ✅ Add argument-hint when taking arguments
- ✅ Use appropriate tool restrictions
- ✅ Test commands before deployment

**DON'T:**
- ❌ Write messages TO user ("This will...")
- ❌ Use vague instructions ("Check the code")
- ❌ Skip output format definition
- ❌ Forget argument-hint for arg-taking commands
- ❌ Use Bash(*) when specific pattern works
- ❌ Hardcode paths in plugin commands
- ❌ Skip validation

## When to Use This Skill

- User asks to create a new slash command
- User asks to adapt a marketplace command
- User asks to validate command structure
- User asks to fix command that's not working
- User asks about command arguments or bash execution
- DEV-Manager detects command issues during improvement cycle
- Regular improvement cycle (~6 sessions)

## Sync Protocol

Before executing any workflow:

1. Read JARVIS-06's commands-management SKILL.md
2. Check for policy updates
3. Apply current policy, not cached knowledge
