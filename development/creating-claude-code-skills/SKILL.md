---
name: Creating Claude Code Skills
description: This skill guides the process of creating new Claude Code skills, covering skill anatomy, frontmatter format, naming conventions, organization patterns, and when to use personal vs company-specific skills. Use this skill when you want to create a new skill or understand skill structure.
allowed-tools: [Bash, Write, Read, Edit]
---

# Creating Claude Code Skills

This meta-skill guides you through creating well-structured Claude Code skills.

## What are Claude Code Skills?

Skills are packaged sets of instructions that extend Claude's capabilities for specific tasks. They are:
- **Filesystem-based**: Stored as directories with a `SKILL.md` file
- **Automatically discovered**: Claude loads them when relevant to tasks
- **Progressive**: Content loaded in stages (metadata → instructions → resources)

## Skill Locations

Choose the appropriate location based on portability:

### Personal Skills (`~/.claude/skills/`)
- **Use for**: Portable skills that work across any company or project
- **Examples**: Generic coding patterns, tool workflows (git, docker), debugging techniques
- **Version control**: In dotfiles repo, symlinked to ~/.claude/skills/
- **Portability**: Follow you across all companies and projects

### Company Skills (`~/.claude/skills.private/`)
- **Use for**: Company-specific workflows and infrastructure
- **Examples**: Internal tool access, company infrastructure patterns, cross-project company workflows
- **Version control**: NOT in git (excluded via .gitignore)
- **Portability**: Specific to current employer, not portable

### Project Skills (`<project>/.claude/skills/`)
- **Use for**: Team-shared, project-specific procedures
- **Examples**: Deployment procedures, project conventions, architecture-specific patterns
- **Version control**: In project repo, shared with team
- **Portability**: Available to all team members

## Decision Tree: Where Should My Skill Go?

```
Is it company/employer-specific?
├─ Yes: Does the team need it?
│  ├─ Yes: Project skills (project/.claude/skills/)
│  └─ No: Company skills (~/.claude/skills.private/)
└─ No: Personal skills (~/.claude/skills/)
```

## Skill File Structure

Every skill requires this structure:

```
skill-name/
└── SKILL.md           # Required: Main skill definition
```

Optional supporting files:

```
skill-name/
├── SKILL.md           # Required
├── script.py          # Optional: Supporting scripts
├── reference.md       # Optional: Additional documentation
└── examples/          # Optional: Example files
    └── sample.csv
```

## Multi-File Skills

Skills can include multiple markdown files for better organization. Claude Code's progressive loading architecture loads each file only when needed.

### When to Use Multiple Files

**Use companion markdown files when:**
- Main skill content exceeds ~800 lines
- You have extensive reference data that's not always needed
- Environment-specific details are substantial (different configs, workflows)
- Troubleshooting content is extensive

**Progressive loading benefit:**
- `SKILL.md` is always loaded when the skill triggers
- Companion files (`REFERENCE.md`, `ENVIRONMENTS.md`, etc.) are loaded only when Claude explicitly needs them
- Zero token cost for unneeded content

### Structure Example

```
skill-name/
├── SKILL.md              # Required: Core instructions
├── REFERENCE.md          # Optional: Quick reference lookups
├── ENVIRONMENTS.md       # Optional: Environment-specific details
├── TROUBLESHOOTING.md    # Optional: Detailed error solutions
└── examples/
    └── sample.csv
```

### Companion File Naming Conventions

- `REFERENCE.md` - Quick lookup tables, configuration values, command syntax
- `ENVIRONMENTS.md` - Environment-specific workflows (dev/staging/prod variations)
- `TROUBLESHOOTING.md` - Detailed error diagnosis and solutions
- `EXAMPLES.md` - Extended usage examples and patterns

### Cross-Referencing Between Files

In `SKILL.md`, reference companion files clearly:

```markdown
## Environment-Specific Details

For Wonder's specific environments:
- **BA-FR-ENVIRONMENTS.md** - BA/FR configurations and workflows
- **AZURE-ENVIRONMENT.md** - Azure Kubernetes setup and operations
```

This helps Claude know which companion file to load for specific queries.

### Real-World Example

From the "Working with Kubernetes" skill:

```
working-with-kubernetes/
├── SKILL.md (~450 lines)
│   └── Generic kubectl patterns usable in any cluster
├── BA-FR-ENVIRONMENTS.md (~320 lines)
│   └── BA/FR-specific configs, ba CLI, kubectl-envx plugin
└── AZURE-ENVIRONMENT.md (~680 lines)
    └── Azure-specific setup, grpcurl, kafkactl, load testing
```

**Loading behavior:**
- Query: "How do I debug a pod?" → Loads `SKILL.md` only (450 lines)
- Query: "How do I use ba CLI in BA production?" → Loads `SKILL.md` + `BA-FR-ENVIRONMENTS.md` (770 lines)
- Query: "How do I test Azure gRPC endpoints?" → Loads `AZURE-ENVIRONMENT.md` only (680 lines)

**Why this works:**
1. **Token efficiency**: Only load what's needed for each query
2. **Maintainability**: Environment-specific content doesn't pollute generic patterns
3. **Discoverability**: Clear file names help Claude find the right information
4. **Scalability**: Easy to add new environments without modifying core skill

## SKILL.md Anatomy

### Required Structure

```markdown
---
name: Skill Name Here
description: Clear, specific description of what this skill does and when to use it
---

# Skill Content

Instructions and documentation go here...
```

### YAML Frontmatter Fields

#### Required Fields

**`name`** (max 64 characters):
- Use gerund form (verb + -ing): "Processing PDFs", "Refreshing TNM Data"
- Be specific and descriptive
- Avoid vague names like "Helper" or "Utility"

**`description`** (max 1024 characters):
- Written in third person
- Be specific about what the skill does
- Include key terms and usage contexts
- Explain when to use it
- Example: "This skill refreshes TNM configuration data from BA production to local FES development environments"

#### Optional Fields

**`allowed-tools`**: Restrict which tools Claude can use within this skill
```yaml
allowed-tools: [Bash, Read, Write, Edit]
```

### Content Structure Best Practices

Organize your skill content with these sections:

1. **Overview** - Brief description of capabilities
2. **What This Skill Does** - Specific capabilities list
3. **Prerequisites** - Required tools, access, environment setup
4. **Usage** - Step-by-step instructions
5. **Examples** - Concrete use cases with quotes
6. **Verification** - How to check success
7. **Troubleshooting** - Common issues and solutions
8. **Related Skills** - Links to complementary skills
9. **Best Practices** - Guidelines for effective use

## Naming Conventions

### Directory Names
- Use kebab-case: `my-skill-name`
- Be descriptive and specific
- Avoid generic names

### Examples by Type

**Personal skills**:
- `debugging-with-printf`
- `git-bisect-workflow`
- `analyzing-performance-profiles`

**Company skills**:
- `refreshing-ba-tnm-data`
- `accessing-wonder-kubernetes`
- `deploying-to-freshrealm-staging`

**Project skills**:
- `fes-local-development-setup`
- `running-integration-tests`
- `generating-api-documentation`

## Step-by-Step Creation Process

### 1. Decide on Location

```bash
# Personal skill (portable)
cd ~/Code/dotfiles/.claude/skills

# Company skill (company-specific)
cd ~/.claude/skills.private

# Project skill (team-shared)
cd ~/Code/project/.claude/skills
```

### 2. Create Directory

```bash
mkdir my-skill-name
cd my-skill-name
```

### 3. Create SKILL.md

```bash
cat > SKILL.md << 'EOF'
---
name: My Skill Name
description: This skill does X by doing Y. Use this skill when you need to accomplish Z.
allowed-tools: [Bash, Read, Write]
---

# My Skill Name

Brief overview of what this skill does.

## What This Skill Does

- Capability 1
- Capability 2
- Capability 3

## Prerequisites

1. **Requirement 1**
   - Details about requirement

2. **Requirement 2**
   - Details about requirement

## Usage

### Step 1: First Action

```bash
command-example
```

Expected behavior:
- What should happen

### Step 2: Second Action

Detailed instructions...

## Verification

How to confirm the skill worked:

```bash
verification-command
```

## Troubleshooting

### Issue: Common Problem

**Cause:** Why this happens

**Solution:**
```bash
fix-command
```

## Best Practices

1. **Practice 1**: Description
2. **Practice 2**: Description

## Related Skills

- **Other Skill Name** - When to use instead
EOF
```

### 4. Test the Skill

```bash
# Restart Claude Code to load new skills
# (Skills are discovered at startup)

# In a new conversation, trigger the skill:
# "Help me with [skill topic]"
```

### 5. Iterate and Refine

- Test with real use cases
- Add troubleshooting sections as issues arise
- Update examples based on actual usage
- Refine prerequisites based on feedback

## Skill Design Smell Tests

Use these indicators to catch design problems early.

### 🚩 Red Flags (Skill Needs Splitting)

**Environment overload:**
- Phrase "For environment A... For environment B..." appears 3+ times
- Different kubeconfigs, URLs, or credentials for each section
- Example: "In production use X, in staging use Y, in dev use Z..."

**Tool sprawl:**
- Covering 3+ distinct tools in one skill
- Each tool has its own installation, config, and usage sections
- Example: Single skill teaching kubectl, helm, AND kustomize

**Duplicate-with-variations:**
- Copy-pasted sections with slight parameter changes
- "This is the same as above but with different values..."
- Tables showing per-environment variations

**Troubleshooting dominance:**
- Troubleshooting section exceeds 200 lines
- More content about what can go wrong than what should go right
- Spending more time on edge cases than happy path

**Reference data heavy:**
- Long tables of configuration options (>100 lines)
- API reference documentation embedded in usage instructions
- Lookup tables users reference but rarely read fully

**Mode switching:**
- "Depending on your use case, do A or B or C..."
- Multiple distinct workflows in one skill
- User must choose their path through the content

**Excessive length:**
- File exceeds 1000 lines
- You're scrolling extensively to find sections
- Table of contents is needed

### ✅ Green Checks (Good Scope)

**Single responsibility:**
- Skill does one thing well
- Easy to describe in one sentence
- Name clearly indicates what it does

**Most content relevant:**
- >80% of users need >80% of the content
- Little branching ("if you're doing X, skip this")
- Linear flow through the instructions

**Simple prerequisites:**
- 1-3 clear requirements
- All prerequisites are related to the core task
- No "depending on your environment" prerequisites

**Focused examples:**
- Examples all demonstrate the same core concept
- Variations show different use cases, not different tools
- No need for "Example for environment A, Example for environment B"

**Reasonable length:**
- File is 300-800 lines
- Can read the whole thing in 10-15 minutes
- Don't need extensive scrolling to navigate

**Clear audience:**
- Written for one type of user (not "beginners can X, advanced users can Y")
- Consistent level of detail throughout
- No jarring shifts in complexity

### Specific Thresholds

| Indicator | Green | Yellow | Red |
|-----------|-------|--------|-----|
| **File size** | <800 lines | 800-1000 lines | >1000 lines |
| **Environments** | 1 | 2 | 3+ |
| **Tools covered** | 1 | 2 | 3+ |
| **"Depending on"** | 0-2 | 3-5 | 6+ |
| **Troubleshooting** | <100 lines | 100-200 lines | >200 lines |
| **Prerequisites** | 1-3 | 4-5 | 6+ |

### Action Items

**If you see red flags:**
1. Stop and assess before adding more content
2. Re-read the "Multi-File Skills" section
3. Identify natural boundaries (environments, tools, data)
4. Plan a refactoring into multiple files
5. See "Refactoring Existing Skills" section for migration steps

**If you see green checks:**
- Keep going!
- Continue adding content to the single file
- Monitor the thresholds as you grow

## Quality Checklist

Before considering a skill complete:

### Content Quality
- [ ] Name is descriptive and uses gerund form
- [ ] Description clearly states what and when
- [ ] Prerequisites are complete and accurate
- [ ] Instructions are step-by-step and clear
- [ ] Examples use concrete commands/code
- [ ] Troubleshooting covers common issues
- [ ] Best practices guide users to success

### Technical Quality
- [ ] YAML frontmatter is valid
- [ ] File size is appropriate (see File Size Guidelines below)
- [ ] Code blocks use proper syntax highlighting
- [ ] Commands are tested and work
- [ ] No hardcoded credentials or secrets
- [ ] Paths use ~ for home directory

### Organization Quality
- [ ] Skill is in correct location (personal/company/project)
- [ ] Supporting files are in skill directory
- [ ] Related skills are cross-referenced
- [ ] Version control status is correct

## Common Patterns

### Multi-Step Process Skills

For complex workflows:

```markdown
## Process Overview
Brief summary of the entire flow

## Step 1: Preparation
Detailed instructions

## Step 2: Execution
Detailed instructions

## Step 3: Verification
How to check success

## Step 4: Cleanup
Post-execution tasks
```

### Reference Data Skills

For skills with lookup tables or reference data:

```markdown
## Quick Reference

| Item | Value | Description |
|------|-------|-------------|
| A    | 1     | Details     |
| B    | 2     | Details     |

## Usage
How to use the reference data
```

### Troubleshooting-Heavy Skills

For error-prone operations:

```markdown
## Common Issues

### Issue 1: [Error Message]
**Symptoms**: What you see
**Cause**: Why it happens
**Solution**: Step-by-step fix

### Issue 2: [Error Message]
[Same structure]
```

## Tips and Tricks

### Keep Skills Focused
- One skill = one job
- If a skill tries to do too much, split it
- Link related skills instead of combining them

### Use Concrete Examples
- Show actual commands, not placeholders
- Include expected output
- Use real file paths (with ~ for portability)

### Document Edge Cases
- What doesn't work
- Known limitations
- Workarounds for common blockers

### Update Skills Over Time
- Add new troubleshooting as issues arise
- Update commands when tools change
- Refine instructions based on usage

### Test with Fresh Eyes
- Have someone else try your instructions
- Test in a clean environment
- Verify all commands actually work

## File Size Guidelines

Claude Code's progressive loading architecture means different content has different token costs.

### Loading Stages

1. **Metadata** (~100 tokens): Name, description - always loaded
2. **Instructions** (<5k tokens recommended): Main SKILL.md content - loaded when skill triggers
3. **Resources** (zero cost): Companion files - loaded only when Claude explicitly needs them

### Size Targets Per File

**Target**: <800 lines per file (~5000 tokens)
- Sweet spot for readability and performance
- Most skills should aim for this range

**Acceptable**: 800-1000 lines
- Still manageable but getting large
- Consider if content could be split

**Time to refactor**: >1000 lines
- Hard to navigate and maintain
- Strong signal to split into multiple files
- Consider companion files (REFERENCE.md, ENVIRONMENTS.md, etc.)

**Absolute maximum**: <1200 lines per file
- Beyond this, Claude may struggle to navigate effectively
- Definitely split into multiple files

### Token Estimation

To estimate tokens from line count:

```bash
# Rough estimate: word count ÷ 0.75
wc -w SKILL.md
# Example: 4000 words ≈ 5300 tokens

# More accurate: use a token counter
# Most words = ~1.3 tokens on average
```

**Rule of thumb**: 5-6 words per line × 1.3 tokens/word = ~7 tokens per line

### When to Split

If your SKILL.md exceeds 800 lines, consider:
- **Reference data** → Extract to REFERENCE.md
- **Environment variations** → Extract to ENVIRONMENTS.md
- **Extensive troubleshooting** → Extract to TROUBLESHOOTING.md
- **Many examples** → Extract to EXAMPLES.md

See "Multi-File Skills" section above for details.

## Refactoring Existing Skills

As skills grow and evolve, you may need to refactor them into multi-file structures.

### When to Refactor

**Strong signals it's time to split:**
- SKILL.md exceeds 1000 lines
- You're scrolling extensively to find content
- Multiple distinct "modes" or environments covered
- Troubleshooting section is >200 lines
- Reference tables dominate the content
- You use "depending on..." frequently

### Identifying Natural Boundaries

Look for distinct sections that could stand alone:

**Environment boundaries:**
```
Before (single file):
## Using in Development
## Using in Staging
## Using in Production

After (split):
SKILL.md - Generic patterns
ENVIRONMENTS.md - Dev/staging/prod specifics
```

**Tool boundaries:**
```
Before (single file):
## Using Tool A
## Using Tool B
## Using Tool C

After (split):
SKILL.md - Core concepts
TOOL-A.md - Tool A specifics
TOOL-B.md - Tool B specifics
```

**Data type boundaries:**
```
Before (single file):
## API Reference (500 lines of tables)
## Usage Instructions

After (split):
SKILL.md - Usage instructions
REFERENCE.md - API tables
```

### Migration Steps

1. **Backup** your current SKILL.md
   ```bash
   cp SKILL.md SKILL.md.backup
   ```

2. **Identify sections** to extract
   - List distinct content types
   - Note line ranges for each
   - Choose companion file names

3. **Create companion files**
   ```bash
   # Extract reference content
   sed -n '100,400p' SKILL.md > REFERENCE.md

   # Add frontmatter if needed (optional for companion files)
   ```

4. **Update SKILL.md**
   - Remove extracted content
   - Add cross-references to companion files
   - Update table of contents if present

5. **Test both paths**
   - Verify SKILL.md works alone for generic queries
   - Verify companion files load when needed
   - Check cross-references are clear

6. **Iterate**
   - Use the refactored skill in real scenarios
   - Adjust boundaries if needed
   - Update cross-references based on usage

### Example: Splitting a Large Skill

**Before** (1200-line "Database Operations" skill):
```
database-operations/
└── SKILL.md (1200 lines)
    ├── Connection patterns (generic, 200 lines)
    ├── PostgreSQL specifics (400 lines)
    ├── MySQL specifics (400 lines)
    └── Troubleshooting (200 lines)
```

**After** (split into focused files):
```
database-operations/
├── SKILL.md (300 lines)
│   └── Generic connection patterns and concepts
├── POSTGRES.md (450 lines)
│   └── PostgreSQL-specific commands and patterns
├── MYSQL.md (450 lines)
│   └── MySQL-specific commands and patterns
└── TROUBLESHOOTING.md (200 lines)
    └── Common errors across all databases
```

**Benefits:**
- Query: "How do I connect to a database?" → Loads SKILL.md only (300 lines vs 1200 lines)
- Query: "PostgreSQL array operators" → Loads POSTGRES.md (450 lines vs 1200 lines)
- Easier to maintain (edit MySQL without touching PostgreSQL)

### Common Refactoring Patterns

**Pattern 1: Environment Split**
- SKILL.md: Generic workflow
- ENVIRONMENTS.md: Environment-specific configs

**Pattern 2: Tool Split**
- SKILL.md: Core concepts
- TOOL-X.md: Tool-specific details (one file per major tool)

**Pattern 3: Reference Extraction**
- SKILL.md: Usage instructions
- REFERENCE.md: Lookup tables, API docs, config options

**Pattern 4: Troubleshooting Extraction**
- SKILL.md: Happy path instructions
- TROUBLESHOOTING.md: Error diagnosis and solutions

### Avoiding Over-Splitting

**Don't split if:**
- Total content is <800 lines
- Sections are tightly coupled (can't understand one without the other)
- You'd need to reference other files in every section
- Splitting would create files <100 lines each

**Rule of thumb:** Each file should be independently useful for some query.

## Version Control Best Practices

### For Personal Skills (in dotfiles)
```bash
cd ~/Code/dotfiles/.claude/skills/my-skill
git add SKILL.md
git commit -m "Add [skill name] skill"
git push
```

### For Company Skills (not in git)
```bash
# No git operations - these stay local
# Backup strategy recommended (Time Machine, etc.)
```

### For Project Skills (in project repo)
```bash
cd ~/Code/project/.claude/skills/my-skill
git add SKILL.md
git commit -m "Add [skill name] skill for team"
# Follow project's PR process
```

## Examples of Well-Structured Skills

### Example 1: Simple Tool Workflow

```markdown
---
name: Running Git Bisect
description: This skill guides you through using git bisect to find the commit that introduced a bug using binary search. Use this when you know a bug exists but don't know which commit caused it.
allowed-tools: [Bash]
---

# Git Bisect Workflow

Binary search through git history to find bug-introducing commits.

## What This Skill Does

- Starts git bisect session
- Tests commits interactively
- Identifies the breaking commit
- Provides commit hash and details

## Prerequisites

1. **Git repository** with history
2. **Known good commit** (working state)
3. **Known bad commit** (broken state, usually HEAD)
4. **Reproducible test** to identify bug

## Usage

[Rest of skill content...]
```

### Example 2: Complex Multi-Step Process

```markdown
---
name: Deploying to Production
description: This skill automates the production deployment process including pre-deployment checks, deployment execution, and post-deployment verification. Use this when you need to deploy a release to production.
allowed-tools: [Bash, Read]
---

# Production Deployment Workflow

[Comprehensive deployment instructions...]
```

## Getting Help

If you're unsure about skill structure:
- Look at existing skills for examples
- Start simple and iterate
- Test early and often
- Ask for feedback from teammates (for project skills)

## Next Steps

After creating your first skill:
1. Use it in a real task
2. Note what's missing or unclear
3. Iterate and improve
4. Create related skills as needed

Remember: Skills improve with use!
