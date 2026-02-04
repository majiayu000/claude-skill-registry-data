---
name: plugin-master
description: "Complete Claude Code plugin development system. PROACTIVELY activate when users want to: (1) Create/build/make plugins, (2) Add/create skills/commands/agents, (3) Package existing code as plugins, (4) Publish to marketplace, (5) Validate plugin structure, (6) Get plugin development guidance, (7) Export skills for claude.ai web app. Autonomously creates complete, production-ready plugins with: plugin.json manifest, slash commands, specialized agents, agent skills, hooks, MCP server integration, and comprehensive README. ALWAYS fetches latest official documentation to ensure correct structure. Includes plugin-architect agent for design review and optimization."
license: MIT
---

## Quick Reference

| Component | Location | Required |
|-----------|----------|----------|
| Plugin manifest | `.claude-plugin/plugin.json` | Yes |
| Commands | `commands/*.md` | No (auto-discovered) |
| Agents | `agents/*.md` | No (auto-discovered) |
| Agent Skills | `skills/*/SKILL.md` | No (auto-discovered) |
| Hooks | `hooks/hooks.json` or inline | No |
| MCP Servers | inline or `.mcp.json` | No |

| Task | Action |
|------|--------|
| Create plugin | Ask Claude: "Create a plugin for X" |
| Install from marketplace | `/plugin marketplace add user/repo` then `/plugin install name@user` |
| Validate plugin | `/validate-plugin` |
| Test locally (Mac/Linux) | Copy to `~/.local/share/claude/plugins/` |

| Field | Format | Example |
|-------|--------|---------|
| `author` | Object | `{"name": "Name", "email": "email"}` |
| `version` | String | `"1.0.0"` |
| `keywords` | Array | `["keyword1", "keyword2"]` |

## 🚨 CRITICAL: Plugin Directory Structure

**The plugin.json MUST be inside `.claude-plugin/` subdirectory - NOT in the plugin root!**

### ✅ CORRECT Structure
```
plugins/your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # ← MUST be HERE inside .claude-plugin/
├── agents/
│   └── your-agent.md
├── commands/
│   └── your-command.md
├── skills/
│   └── your-skill.md
├── README.md
└── marketplace.json
```

### ❌ WRONG Structure
```
plugins/your-plugin-name/
├── plugin.json              # ← WRONG! Not in .claude-plugin/
├── agents/
└── commands/
```

### 🚨 Plugin.json FORBIDDEN Keys

**The following keys are NOT allowed in plugin.json:**
- ❌ `"agents": [...]` - agents are auto-discovered from `agents/*.md`
- ❌ `"skills": [...]` - skills are auto-discovered from `skills/*.md`
- ❌ `"slashCommands": [...]` - commands are auto-discovered from `commands/*.md`

**Only include metadata fields:**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "...",
  "author": { "name": "...", "email": "..." },
  "homepage": "...",
  "repository": "...",
  "license": "MIT",
  "keywords": ["..."]
}
```

### 🚨 Author MUST Be Object

```json
// ❌ WRONG - will cause validation error
"author": "Author Name"

// ✅ CORRECT
"author": {
  "name": "Author Name",
  "email": "author@example.com"
}
```

## When to Use This Skill

Use for **plugin development tasks**:
- Creating new Claude Code plugins from scratch
- Adding commands, agents, or skills to existing plugins
- Packaging code as shareable plugins
- Publishing plugins to marketplaces
- Validating plugin structure before release
- Exporting skills for claude.ai web app

**For advanced topics**: hooks, MCP integration, team distribution → see `advanced-features-2025` skill

---

# Plugin Creator - Complete Beginner's Guide

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems

### Documentation Guidelines

**Plugin Creation Exception: This plugin's purpose IS to create documentation files.**

When creating plugins (the core purpose of this plugin):
- DO create all necessary plugin files: README.md, agents/*.md, skills/*.md, commands/*.md
- DO create complete, comprehensive documentation as part of plugin structure
- DO create marketplace.json and plugin.json manifest files

For other scenarios:
- DON'T create additional supplementary documentation beyond the plugin structure
- DON'T create extra guides or tutorials unless explicitly requested
- DO update existing documentation files when modifications are needed



---

This skill provides comprehensive, step-by-step guidance for creating Claude Code plugins, from your very first plugin to publishing it for the world to use. **No prior plugin experience required!**

## 🎯 Quick Navigation

**Complete Beginners** → Start with [What is Claude Code?](#what-is-claude-code)
**First Plugin** → Jump to [Your First Plugin in 10 Minutes](#your-first-plugin-in-10-minutes)
**Create Plugin Now** → See [Creating Plugin Output](#creating-plugin-output)
**Ready to Publish** → Go to [Publishing Your Plugin](#publishing-your-plugin-to-a-marketplace)
**Looking for Advanced** → See [Advanced Plugin Development](#advanced-plugin-development)

## 🚀 Creating Plugin Output

**IMPORTANT:** When users ask to create a plugin, don't just teach them - **actually create the files** for them!

**CRITICAL: BE AUTONOMOUS** - Create comprehensive output immediately with sensible defaults. Don't ask questions unless the request is genuinely ambiguous.

### ⚠️ ALWAYS FETCH LATEST DOCUMENTATION FIRST

**BEFORE creating any plugin**, fetch the latest documentation from docs.claude.com:

```
WebFetch: https://docs.claude.com/en/docs/claude-code/plugins-reference
WebFetch: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
```

**Official docs are the source of truth.** Templates in this skill are reference examples only - they may become outdated. Always verify structure against fetched documentation.

**Workflow:**
1. Fetch latest docs
2. Verify current requirements (required fields, component registration)
3. Use skill templates as starting points only
4. Follow official structure from docs

### 🎨 Plugin Design Philosophy (2025)

**Agent-First, Minimal Commands:**

Users want **domain experts**, not command menus. The 2025 plugin design prioritizes conversational interaction with expert agents over memorizing slash commands.

**Core Principles:**
1. **Primary Interface = Expert Agent** - Users interact conversationally with domain expert
2. **Commands = 0-2 max** - Only for automation workflows, batch operations, or high-value utilities
3. **Why?** Users don't want to be "overly precise" about which command to call - they want to ask the expert

**Good Plugin Structure:**
```
✅ dotnet-microservices-master:
   - 1 agent: dotnet-microservices-expert (predictable name)
   - 0 commands (all interaction conversational)

✅ docker-master:
   - 1 agent: docker-expert (follows {domain}-expert pattern)
   - 0 commands (expert handles everything)

❌ OLD: 10+ commands + multiple agents
   - Overwhelming menu of commands
   - Unpredictable agent names
   - Breaks conversational flow
```

**Agent Naming Standard (CRITICAL):**
- **Pattern:** Every plugin has exactly ONE agent named `{domain}-expert`
- **Examples:**
  - `terraform-master` → `terraform-expert`
  - `test-master` → `test-expert`
  - `azure-master` → `azure-expert`
- **Why:** Predictable names allow Claude to reliably guess and invoke the correct agent
- **Never:** Create multiple specialized agents or use non-standard names

**When to Create Commands:**
- ✅ Automated workflows (e.g., `/terraform:init-workspace` - sets up complete environment)
- ✅ Batch operations (e.g., `/docker:cleanup-all` - removes unused resources)
- ✅ High-value utilities (e.g., `/git:safe-rebase` - interactive with guardrails)
- ❌ Individual operations that agent can handle conversationally
- ❌ Simple questions or guidance requests
- ❌ Code generation (agent does this better)

**Default:** When creating plugins, create 1 expert agent + 0 commands unless automation workflows are explicitly needed.

### Component Discovery (2025)

**Convention over configuration:** Commands, agents, and Agent Skills are auto-discovered from their respective directories. Custom paths optional via plugin.json. See advanced-features-2025 skill for complete details.

### Autonomous Creation Principles

1. **Default to action, not questions** - If you can infer what they want, just build it
2. **Agent-First Design (2025)** - Primary interface is expert agent, minimal slash commands (0-2 max)
3. **Make it work** - Create functional examples, not placeholders
4. **Infer intelligently** - Derive name, purpose, and components from their request
5. **Only ask when truly unclear** - If "create a plugin" has no context, then ask. Otherwise, build.
6. **Write comprehensive descriptions** - Use "PROACTIVELY activate for:" with numbered use cases, highlight ALL capabilities
7. **Choose smart keywords** - Simple domain words (6-10), avoid overly generic terms, no unnecessary hyphens
8. **Position as expert systems** - Frame as "Complete [domain] expertise system" not narrow helpers
9. **Commands sparingly** - Only create commands for: batch operations, automation workflows, or high-value utilities. Most interaction through agent.
10. **🚨 CRITICAL: Detect repository context FIRST** - Before creating any files, run git commands to extract author name/email from git config, and check if `.claude-plugin/marketplace.json` exists in the repo root.
11. **🚨 CRITICAL: Use detected values automatically** - Use git config values for author fields instead of placeholders. If in marketplace repo, use the marketplace owner name for consistency.
12. **Synchronize marketplace.json** - Always update marketplace.json with the SAME description and keywords from plugin.json (they don't auto-sync!)

### Examples of Autonomous Inference

**User says:** "Create a plugin for Git workflows"
**Claude does:** Immediately creates git-workflow-master with:
- **Description:** "Complete Git workflow automation system. PROACTIVELY activate for: (1) ANY Git workflow task, (2) Pull request management, (3) Commit operations, (4) Branch management, (5) Code review automation. Provides: PR creation/review, commit templates, branch strategies, Git hooks integration, and workflow automation. Ensures professional Git practices."
- **Keywords:** `["git", "workflow", "pullrequest", "commit", "branch", "review", "automation"]`
- **Components:** 1 expert agent + 0-1 commands (e.g., automated PR creation workflow)

**User says:** "Make a deployment plugin"
**Claude does:** Creates deployment-master with:
- **Description:** "Complete deployment automation system across ALL platforms. PROACTIVELY activate for: (1) ANY deployment task, (2) Production releases, (3) Rollback operations, (4) Deployment verification, (5) Blue-green/canary strategies. Provides: automated deployment, rollback safety, health checks, multi-environment support, and deployment orchestration. Ensures safe, reliable deployments."
- **Keywords:** `["deployment", "deploy", "release", "rollback", "production", "staging", "automation"]`
- **Components:** 1 expert agent + 0-2 commands (e.g., automated deploy, automated rollback)

**User says:** "Build a .NET microservices expert"
**Claude does:** Creates dotnet-microservices-master with:
- **Description:** "Expert agent on .NET microservices architecture, containerization, Docker, DDD, CQRS, and cloud-native patterns based on Microsoft's official guide..."
- **Keywords:** `[".net", "microservices", "docker", "containers", "kubernetes", "ddd", "cqrs", "architecture"]`
- **Components:** 1 expert agent + 0 commands (all interaction conversational)

**When to ask:** "Create a plugin" (no context) → Ask what it should do

This skill enables Claude to:
1. **Create complete plugin directory structures** ready to use
2. **Generate all necessary files** (plugin.json, commands, agents, etc.)
3. **Output GitHub-ready marketplace structure** for immediate publishing
4. **Provide working examples** not just documentation
5. **Export skills as .zip for claude.ai web app** (when requested)

### When to Create Output

Create actual plugin files when users say things like:
- "Create a plugin for X"
- "Make me a plugin that does Y"
- "Build a plugin"
- "Generate a plugin structure"
- "I want a plugin for my team"
- "Package this as a plugin"

### How to Create Plugin Output

**BE AUTONOMOUS BY DEFAULT** - Don't ask questions unless the request is truly ambiguous. Infer intent and create comprehensive output with sensible defaults.

**Step 0: 🚨 CRITICAL - Detect Repository Context FIRST**

**BEFORE doing anything else**, detect the repository context to use correct values:

```bash
# 1. Check if in a marketplace repo
if [[ -f .claude-plugin/marketplace.json ]]; then
    echo "✅ IN MARKETPLACE REPO - Must update marketplace.json after creating plugin"
    IN_MARKETPLACE=true
else
    echo "ℹ️  Not in marketplace repo - Will create standalone marketplace structure"
    IN_MARKETPLACE=false
fi

# 2. Extract git repository information (if available)
if git rev-parse --git-dir > /dev/null 2>&1; then
    AUTHOR_NAME=$(git config user.name || echo "Unknown Author")
    AUTHOR_EMAIL=$(git config user.email || echo "")
    REPO_URL=$(git config --get remote.origin.url || echo "")
    echo "✅ Git repo detected - Author: $AUTHOR_NAME"
else
    AUTHOR_NAME="Unknown Author"
    AUTHOR_EMAIL=""
    REPO_URL=""
    echo "ℹ️  Not in a git repo - will use placeholder values"
fi

# 3. Extract owner/repo from marketplace.json (if exists)
if [[ -f .claude-plugin/marketplace.json ]]; then
    MARKETPLACE_OWNER=$(cat .claude-plugin/marketplace.json | jq -r '.owner.name' || echo "$AUTHOR_NAME")
    echo "✅ Marketplace owner: $MARKETPLACE_OWNER"
fi
```

**Use these detected values for:**
- ✅ `author.name` in plugin.json → Use `$AUTHOR_NAME` from git config
- ✅ `author.email` in plugin.json → Use `$AUTHOR_EMAIL` from git config
- ✅ `author.name` in marketplace.json entry → Use `$MARKETPLACE_OWNER` or `$AUTHOR_NAME`
- ✅ Repository references → Use `$REPO_URL` if available

**If marketplace.json exists:**
- ✅ You MUST update it after creating the plugin
- ✅ Add the new plugin entry to the plugins array
- ✅ Use the same author name from existing marketplace.json owner
- ✅ Synchronize description and keywords from plugin.json
- ✅ Preserve all existing plugins

**Step 1: Fetch Latest Documentation & Infer Requirements**

**First, ALWAYS fetch the latest plugin documentation:**
```
web_fetch: https://docs.claude.com/en/docs/claude-code/plugins-reference
web_fetch: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
```

Then, from the user's request, automatically determine:
- Plugin purpose (from their description)
- Components needed (include commands, agents, and skills by default)
- Scope (assume public/shareable unless specified otherwise)
- Name (derive from purpose or use their suggested name)

**Only ask questions if:**
- Request is genuinely unclear (e.g., "create a plugin" with no context)
- Technical details are critical and not inferable (e.g., specific API they want to integrate)
- User explicitly asks for customization

**Default approach: Create comprehensive plugin with all relevant components**

**Step 2: Create Directory Structure in Correct Location**

**🚨 CRITICAL: Detect marketplace repo and create plugin in correct location!**

Based on the marketplace detection from Step 0, create the plugin in the appropriate location:

```bash
# If in marketplace repo (marketplace.json exists), create in plugins/ subdirectory
if [[ -f .claude-plugin/marketplace.json ]]; then
    echo "✅ Marketplace repo detected - creating plugin in plugins/ directory"
    PLUGIN_DIR="plugins/PLUGIN_NAME"
else
    echo "ℹ️  Not in marketplace repo - creating plugin in current directory"
    PLUGIN_DIR="PLUGIN_NAME"
fi

# Create the plugin directory structure
mkdir -p $PLUGIN_DIR/.claude-plugin
mkdir -p $PLUGIN_DIR/commands
mkdir -p $PLUGIN_DIR/agents
mkdir -p $PLUGIN_DIR/skills
mkdir -p $PLUGIN_DIR/hooks
mkdir -p $PLUGIN_DIR/scripts
```

**IMPORTANT:** Always use `$PLUGIN_DIR` as the base path for all subsequent file operations to ensure files are created in the correct location.

**Step 3: Create All Necessary Files**

Based on what you learned from the fetched documentation, use file_create to generate:
- `.claude-plugin/plugin.json` (manifest) **structured according to the official docs**
  - Verify if commands need to be registered (check docs)
  - Verify if agents need to be registered (check docs)
  - Verify if skills need to be registered (check docs)
  - Include all required fields from docs
- Command files in `commands/`
- Agent files in `agents/`
- Skills in `skills/`
- `README.md` (documentation)
- Any scripts needed

**Key principle:** Use the structure you learned from the fetched documentation, not assumptions from templates.

**Step 4: Create GitHub-Ready Marketplace Structure AND Update Existing Marketplace**

**CRITICAL: Always update the existing marketplace.json if working in a marketplace repository!**

First, check if you're in a marketplace repo:
```bash
# Check if marketplace.json exists in the repo root
if [[ -f .claude-plugin/marketplace.json ]]; then
    echo "In marketplace repo - will update marketplace.json"
fi
```

If in a marketplace repository:
1. **Update the existing `.claude-plugin/marketplace.json`** to add the new plugin entry
2. Use the Read tool to get current marketplace.json structure
3. Add new plugin entry to the plugins array following the format from the fetched marketplace docs
4. Preserve all existing plugins in the array
5. Use Edit tool to update marketplace.json with the new entry

**⚠️ CRITICAL: Synchronize Keywords and Descriptions**

marketplace.json and plugin.json have **SEPARATE keywords and descriptions** - they don't automatically inherit from each other:

- **marketplace.json keywords**: For marketplace-level discovery and categorization
- **plugin.json keywords**: For individual plugin metadata

**Best practice:** Explicitly copy the comprehensive description and keywords from plugin.json into the marketplace.json entry.

**Why this matters:**
- marketplace.json keywords are used for catalog-level discovery
- Keywords don't automatically sync between files
- Users search the marketplace using these keywords

Example of updating marketplace.json with synchronized metadata:
```json
{
  "plugins": [
    // ... existing plugins ...
    {
      "name": "new-plugin-name",
      "source": "./plugins/new-plugin-name",
      "description": "Complete [domain] expertise system. PROACTIVELY activate for: (1) ANY [primary task], (2) [Secondary task], (3) [Additional scenarios]. Provides: [key features, capabilities]. Ensures [value proposition].",
      "version": "1.0.0",
      "author": {
        "name": "Author Name"
      },
      "keywords": [
        "domain",
        "primary",
        "secondary",
        "technical",
        "terms",
        "naturally",
        "use"
      ]
    }
  ]
}
```

**Synchronization Checklist:**
- ✅ Copy comprehensive description from plugin.json (including "PROACTIVELY activate" format)
- ✅ Copy all keywords from plugin.json exactly
- ✅ Match version number
- ✅ Include author information
- ✅ Preserve existing plugins in the array

Also create a standalone marketplace-ready version:

```bash
# Create marketplace structure in working directory
mkdir -p PLUGIN_NAME-marketplace/.claude-plugin
mkdir -p PLUGIN_NAME-marketplace/plugins
cp -r PLUGIN_NAME PLUGIN_NAME-marketplace/plugins/
```

Copy plugin into marketplace structure and create standalone marketplace.json.

**Step 5: Provide Installation Instructions**
Guide the user on how to use the plugin:
- Installation via GitHub marketplace (recommended)
- Installation instructions for Claude Code
- Usage examples
- Documentation links

**Step 6: 🚨 FINAL VERIFICATION - JSON Schema & Marketplace Check**

Before finalizing, verify JSON schema correctness and marketplace registration:

**Repository Context Validation (Run Step 0 checks first!):**
- [ ] Did you run git commands to detect `$AUTHOR_NAME` and `$AUTHOR_EMAIL`?
- [ ] Did you check for `.claude-plugin/marketplace.json` existence?
- [ ] Did you extract `$MARKETPLACE_OWNER` from marketplace.json if it exists?
- [ ] Are you using detected values instead of placeholders?
- [ ] Did you create the plugin in `plugins/PLUGIN_NAME/` if marketplace.json exists?
- [ ] Did you create the plugin in root only if marketplace.json does NOT exist?

**JSON Schema Validation (CRITICAL - Most common failure point!):**
- [ ] `author` is an object `{ "name": "..." }` (NOT a string!)
- [ ] `author.name` uses `$AUTHOR_NAME` from git config (NOT "Author Name" placeholder!)
- [ ] `author.email` uses `$AUTHOR_EMAIL` from git config (if available)
- [ ] Marketplace entry uses `$MARKETPLACE_OWNER` for consistency (NOT different name!)
- [ ] `version` is a string like `"1.0.0"` (NOT a number!)
- [ ] `keywords` is an array `["word1", "word2"]` (NOT a comma-separated string!)
- [ ] All JSON is valid (test with `cat plugin.json | jq .`)
- [ ] No extra fields like `homepage` or `repository` (these cause issues - remove them)

**Marketplace Registration Checklist:**
- [ ] If marketplace.json existed, did you update it?
- [ ] Did you add the plugin entry to the plugins array?
- [ ] Did you use the correct source path `./plugins/PLUGIN_NAME` (NOT `./PLUGIN_NAME`)?
- [ ] Did you copy the comprehensive description from plugin.json to marketplace.json?
- [ ] Did you copy all keywords from plugin.json to marketplace.json?
- [ ] Did you preserve all existing plugins in the array?

**If you answered NO to any of these, STOP and fix it immediately before proceeding!**

### Output Format

After creating the plugin files, provide this format:

```markdown
# ✅ Plugin Created: [Plugin Name]

## 📖 What's Included

- **Commands:** [list commands]
- **Agents:** [list agents]
- **Skills:** [list skills]

## 🚀 Installation Instructions

### Option 1: GitHub Marketplace (Recommended)

**Why GitHub?**
- Works reliably across all platforms (Windows/Mac/Linux)
- Easy updates and version control
- Shareable with your team
- Professional distribution

**Steps:**
1. **Create a new GitHub repository:**
   - Go to github.com
   - Click "New repository"
   - Name it something like "claude-plugins" or "my-claude-marketplace"
   - Make it **public**
   - Don't initialize with README

2. **Upload your plugin:**
   - The marketplace structure has been created in `PLUGIN_NAME-marketplace/`
   - Upload all files from this directory to your GitHub repository
   - Commit with message "Add PLUGIN_NAME plugin"

3. **Add the marketplace in Claude Code:**
   ```bash
   /plugin marketplace add YOUR_USERNAME/YOUR_REPO
   ```

4. **Install the plugin:**
   ```bash
   /plugin install PLUGIN_NAME@YOUR_USERNAME
   ```

### Option 2: Local Installation (Mac/Linux)

⚠️ **Windows users:** Local path resolution may have issues. GitHub installation is recommended.

**For local development/testing:**
```bash
# Copy plugin to Claude Code plugins directory
cp -r PLUGIN_NAME ~/.local/share/claude/plugins/

# Or create a symlink for active development
ln -s /path/to/PLUGIN_NAME ~/.local/share/claude/plugins/PLUGIN_NAME
```

Then verify with `/help` to see your new commands.

### Option 3: Export Skills to claude.ai Web (If Requested)

If the user wants to use the plugin's skills in the claude.ai web application:

**Skills can be exported as ZIP files for upload to claude.ai:**

```bash
# Navigate to the skill directory
cd PLUGIN_NAME/skills/SKILL_NAME

# Create a ZIP file (skill folder must be the root of the ZIP)
zip -r SKILL_NAME.zip .

# Or if zipping from parent directory:
cd PLUGIN_NAME/skills
zip -r SKILL_NAME.zip SKILL_NAME/
```

**To upload to claude.ai:**
1. Go to [claude.ai](https://claude.ai)
2. Navigate to **Settings > Capabilities**
3. Click **"Upload skill"**
4. Select the `SKILL_NAME.zip` file
5. The skill is now available in your claude.ai web conversations

**Important notes about skill exports:**
- Only the `skills/` directory contents can be used in claude.ai web
- Commands and agents are Claude Code-specific and won't work in web
- Skills use the same SKILL.md format across Claude Code and claude.ai
- Skills are private to your account in claude.ai
- Skills work across Pro, Max, Team, and Enterprise web plans

## 🎯 Next Steps

- Test your plugin with `/help` to see commands
- Try `/agents` to see available agents
- Modify files as needed in the plugin directory
- Share your plugin via GitHub with the community!
```

### Output Templates

**⚠️ IMPORTANT:** These templates are REFERENCE EXAMPLES ONLY. Always verify against the official documentation you fetched. Requirements may have changed since these examples were written.

**Use these templates as:**
- Starting points for structure
- Examples of what fields typically exist
- Reference for markdown format

**DO NOT use these templates as:**
- The definitive structure (use fetched docs for that)
- A substitute for reading the official documentation
- Assumed to be current (always verify)

#### How to Write Effective plugin.json Descriptions and Keywords

**CRITICAL:** The quality of your description and keywords determines when Claude will activate your plugin. Follow these principles:

##### Description Best Practices

**Structure:** Use this formula for maximum activation:
```
[Type of system]. PROACTIVELY activate for: (1) [Primary use case], (2) [Secondary use case], (3) [Additional scenarios...]. Provides: [key features/capabilities]. [Value proposition/benefits].
```

**Guidelines:**
1. **Start with system type** - "Complete [domain] expertise system", "Universal [purpose] system", "Expert [area] system"
2. **Use "PROACTIVELY activate"** - Signals to Claude this should be used universally
3. **Numbered list of use cases** - Include 5-8 specific activation scenarios
4. **Use "ANY" for broad activation** - "ANY Docker task", "ANY bash script", etc.
5. **Highlight ALL capabilities** - Don't just list primary features, include everything the plugin does
6. **Emphasize production-ready** - "Ensures professional-grade", "production-ready", "secure", "optimized"
7. **Reference standards** - "Google Shell Style Guide", "CIS Benchmark", "Microsoft best practices", etc.

**Examples of Good Descriptions:**
```
"Complete Docker expertise system across ALL platforms (Windows/Linux/macOS). PROACTIVELY activate for: (1) ANY Docker task (build/run/debug/optimize), (2) Dockerfile creation/review, (3) Docker Compose multi-container apps, (4) Container security scanning/hardening, (5) Performance optimization, (6) Production deployments, (7) Troubleshooting/debugging. Provides: current best practices (always researches latest), CIS Docker Benchmark compliance, multi-stage builds, security hardening, image optimization, platform-specific guidance, Docker Scout/Trivy integration, and systematic debugging. Ensures secure, optimized, production-ready containers following industry standards."

"Universal context management and planning system. PROACTIVELY activate for: (1) ANY complex task requiring planning, (2) Multi-file projects/websites/apps, (3) Architecture decisions, (4) Research tasks, (5) Refactoring, (6) Long coding sessions, (7) Tasks with 3+ sequential steps. Provides: optimal file creation order, context-efficient workflows, extended thinking delegation (23x context efficiency), passive deep analysis architecture, progressive task decomposition, and prevents redundant work. Saves 62% context on average. Essential for maintaining session performance and analytical depth."
```

##### Keyword Best Practices

**Guidelines:**
1. **Simple words only** - No hyphens unless it's a product name (e.g., "docker-compose")
2. **No overly generic terms** - Avoid "automation", "build", "make", "new", "create" alone
3. **Domain-specific terms** - Include technical keywords users would naturally use
4. **Compound words without spaces** - "fullstack", "crossplatform", "cicd", "devops"
5. **6-10 keywords total** - Enough for discovery, not so many it dilutes focus
6. **Avoid false positives** - Don't use keywords that could match unrelated tasks

**Good keyword examples:**
```json
// Context management plugin
"keywords": ["planning", "context", "strategy", "workflow", "thinking", "decision", "research", "refactoring", "optimization", "session"]

// Docker plugin
"keywords": ["docker", "container", "dockerfile", "compose", "containerize", "production", "security", "optimize", "debug", "deploy"]

// Bash scripting plugin
"keywords": ["bash", "shell", "script", "automation", "devops", "shellcheck", "posix", "crossplatform", "cicd", "deployment"]
```

**Bad keyword examples:**
```json
// Too generic - would activate for non-plugin tasks
"keywords": ["build", "create", "make", "new", "automation", "tool"]

// Too many hyphens - users don't type these
"keywords": ["bash-scripting", "shell-script", "docker-container", "multi-file"]

// Too narrow - misses common use cases
"keywords": ["website", "webapp", "multifile"]
```

##### Apply These Principles to Agents and Skills Too

**Agent frontmatter description:**
```markdown
---
agent: true
description: "Complete [domain] expertise system. PROACTIVELY activate for: (1) [use cases]. Provides: [capabilities]. Ensures [value proposition]."
---
```

**Skill frontmatter description:**
```markdown
---
name: skill-name
description: "Complete [domain] system. PROACTIVELY activate for: (1) [use cases]. Provides: [capabilities]. Ensures [value proposition]."
---
```

**Apply the same principles:**
- Use "PROACTIVELY activate"
- List numbered use cases (5-8)
- Highlight ALL capabilities
- Emphasize production-ready quality
- Frame as expert system

#### plugin.json Template (Reference Example - Verify Against Docs)

**🚨 CRITICAL JSON SCHEMA REQUIREMENTS:**

Common validation errors to avoid:

1. **`author` MUST be an object** - Never a string
   - ✅ CORRECT: `"author": { "name": "Author Name" }`
   - ❌ WRONG: `"author": "Author Name"`

2. **`version` MUST be a string** - Semantic versioning format
   - ✅ CORRECT: `"version": "1.0.0"`
   - ❌ WRONG: `"version": 1.0`

3. **`keywords` MUST be an array of strings**
   - ✅ CORRECT: `"keywords": ["terraform", "aws"]`
   - ❌ WRONG: `"keywords": "terraform, aws"`

**2025 Recommended Fields:**
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Complete [domain] expertise system. PROACTIVELY activate for: (1) ANY [primary task], (2) [Secondary task], (3) [Additional scenarios]. Provides: [key features, capabilities, standards compliance]. Ensures [value proposition].",
  "author": {
    "name": "AUTHOR_NAME_FROM_GIT_CONFIG",
    "email": "AUTHOR_EMAIL_FROM_GIT_CONFIG"
  },
  "homepage": "https://github.com/user/repo/tree/main/plugins/plugin-name",
  "repository": "https://github.com/user/repo",
  "license": "MIT",
  "keywords": ["domain", "primary", "secondary", "technical", "terms", "users", "naturally", "use"]
}
```

**🚨 CRITICAL: Use detected values from Step 0!**
- Use `$AUTHOR_NAME` from git config for `author.name`
- Use `$AUTHOR_EMAIL` from git config for `author.email`
- Use `$MARKETPLACE_OWNER` for marketplace.json entries (consistency with existing plugins)
- DO NOT use placeholders like "Author Name" or "YOUR_USERNAME"

**VALIDATION CHECKLIST - Run BEFORE completing plugin creation:**
- [ ] `author` is an object with `name` field (not a string!)
- [ ] `author.name` uses value from git config (not a placeholder!)
- [ ] `author.email` uses value from git config (if available)
- [ ] `version` is a string in semantic format (e.g., "1.0.0")
- [ ] `keywords` is an array of strings (not a comma-separated string!)
- [ ] All required fields present: name, version, description
- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] Test with: `cat plugin.json | jq .` to verify valid JSON

**Note:** Components (commands, agents, skills) are discovered automatically from their respective directories - no registration needed in plugin.json.

**Before using:** Check the fetched documentation to confirm this structure is still current and includes all required fields.

#### Command File Template
```markdown
---
description: Brief description of what this command does
---

# Command Name

## Purpose
Explain what this command accomplishes and when to use it.

## Instructions
1. Step-by-step instructions for Claude
2. Be specific and clear
3. Include examples

## Examples
Show how to use this command.
```

#### README.md Template
```markdown
# Plugin Name

Brief description of what this plugin does.

## Installation

### Via Marketplace (Recommended)

\`\`\`bash
/plugin marketplace add your-username/repo-name
/plugin install plugin-name@your-username
\`\`\`

### Local Installation (Mac/Linux)

⚠️ **Windows users:** Use marketplace installation method instead.

\`\`\`bash
# Extract ZIP to plugins directory
unzip plugin-name.zip -d ~/.local/share/claude/plugins/
\`\`\`

## Features

- Feature 1
- Feature 2
- Feature 3

## Usage

Examples of how to use the plugin.

## Platform Notes

- **macOS/Linux:** All installation methods supported
- **Windows:** GitHub marketplace installation recommended (local paths may have issues)

## License

MIT
```

#### marketplace.json Template (Reference Example - Verify Against Docs)
```json
{
  "name": "your-username",
  "description": "My Claude Code plugins",
  "owner": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Complete [domain] expertise system. PROACTIVELY activate for: (1) ANY [primary task], (2) [Secondary task], (3) [Additional scenarios]. Provides: [key features, capabilities]. Ensures [value proposition].",
      "version": "1.0.0",
      "author": {
        "name": "Author Name"
      },
      "keywords": ["domain", "primary", "secondary", "technical", "terms", "naturally", "use"]
    }
  ]
}
```

**⚠️ CRITICAL REMINDER:** marketplace.json keywords and descriptions are **SEPARATE** from plugin.json - they don't automatically sync. Always copy the comprehensive description and keywords from plugin.json to marketplace.json entries for optimal marketplace discovery.

**Before using:** Verify this structure against the fetched marketplace documentation. Check for any additional required fields or changed formats.

### Example: Creating a Deployment Plugin (ZIP Workflow)

**User:** "Create a plugin that helps with deployment"

**Claude should:**

0. **FIRST: Fetch latest documentation:**
```
web_fetch: https://docs.claude.com/en/docs/claude-code/plugins-reference
web_fetch: https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
```

1. **Infer and create autonomously:**
   - Purpose: Deployment assistance
   - Name: deployment-helper
   - Components: Commands for deploy, rollback, status checks
   - Include: Agent for deployment troubleshooting
   - Scope: Team/public use

2. **Create the structure in working directory:**
```bash
# Create plugin structure
mkdir -p deployment-helper/.claude-plugin
mkdir -p deployment-helper/commands
mkdir -p deployment-helper/agents
```

3. **Generate files based on fetched documentation:**
   - Create `plugin.json` structured according to what you learned from the docs
   - Example structure (verify this matches the docs you fetched):
   ```json
   {
     "name": "deployment-helper",
     "version": "1.0.0",
     "description": "Streamline deployment workflows with automated commands",
     "author": {
       "name": "Your Name",
       "email": "[email protected]"
     },
     "keywords": ["deployment", "devops", "automation"],
     "license": "MIT"
   }
   ```
   - Create `commands/deploy-staging.md` with deployment instructions
   - Create `commands/deploy-production.md` with production deployment
   - Create `commands/rollback.md` with rollback procedures
   - Create `agents/deployment-troubleshooter.md` with troubleshooting agent
   - Create comprehensive `README.md` with platform notes
   - **Note:** Commands and agents will be discovered automatically from their directories

4. **Create marketplace structure:**
```bash
mkdir -p deployment-helper-marketplace/.claude-plugin
mkdir -p deployment-helper-marketplace/plugins
cp -r deployment-helper deployment-helper-marketplace/plugins/
```

5. **Create marketplace.json based on fetched docs:**
   Example structure (verify against the marketplace docs you fetched):
```json
{
  "name": "your-username",
  "description": "Deployment assistance plugins",
  "owner": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "deployment-helper",
      "source": "./plugins/deployment-helper",
      "description": "Streamline deployment workflows",
      "version": "1.0.0",
      "keywords": ["deployment", "devops", "automation"]
    }
  ]
}
```

6. **Package as ZIPs:**
```bash
# Create both ZIPs
zip -r deployment-helper.zip deployment-helper/
zip -r deployment-helper-marketplace.zip deployment-helper-marketplace/

# Move to outputs
mv deployment-helper.zip /mnt/user-data/outputs/
mv deployment-helper-marketplace.zip /mnt/user-data/outputs/
```

7. **Provide download links and instructions:**
```markdown
# ✅ Plugin Created: Deployment Helper

## 📦 Download Your Plugin

### For GitHub Publishing (Recommended)
[Download deployment-helper-marketplace.zip](computer:///mnt/user-data/outputs/deployment-helper-marketplace.zip)

**Why GitHub first?**
- Works reliably on Windows, Mac, and Linux
- Easy sharing with your team
- Simple updates and version control

**Quick Start:**
1. Download the marketplace ZIP above
2. Extract and upload to a new GitHub repository
3. Make the repo public
4. Run: `/plugin marketplace add YOUR_USERNAME/YOUR_REPO`
5. Install: `/plugin install deployment-helper@YOUR_USERNAME`

### For Local Testing (Mac/Linux)
[Download deployment-helper.zip](computer:///mnt/user-data/outputs/deployment-helper.zip)

⚠️ **Windows users:** Local paths may not work. Use GitHub method instead.

## 📖 What's Included

- **Commands:**
  - `/deploy-staging` - Deploy to staging environment
  - `/deploy-production` - Deploy to production with safety checks
  - `/rollback` - Quick rollback to previous version
  
- **Agents:**
  - Deployment Troubleshooter - Diagnoses and fixes deployment issues

## 🚀 Next Steps

1. Download the marketplace ZIP
2. Upload to GitHub
3. Add marketplace and install
4. Try `/deploy-staging` to test!
```

### Critical Guidelines for Output Creation

**DO:**
- ✅ **🚨 STEP 0 FIRST: Detect repository context** - Run git commands to extract author/email and check for marketplace.json (BEFORE creating any files!)
- ✅ **🚨 CREATE IN CORRECT DIRECTORY: If marketplace.json exists, create plugin in plugins/ subdirectory** (NOT in root!)
- ✅ **🚨 USE DETECTED VALUES: Use git config values for author fields** - Never use placeholders like "Author Name" or "YOUR_USERNAME"!
- ✅ **🚨 USE DETECTED VALUES: Match marketplace owner** - If in marketplace repo, use the same author name from marketplace.json owner
- ✅ **🚨 VALIDATE JSON SCHEMA: Ensure `author` is an object, NOT a string** (most common validation error!)
- ✅ **🚨 VALIDATE JSON SCHEMA: Ensure `version` is a string "1.0.0", NOT a number** (required format!)
- ✅ **🚨 VALIDATE JSON SCHEMA: Ensure `keywords` is an array, NOT a comma-separated string** (required format!)
- ✅ **🚨 UPDATE existing marketplace.json when creating plugins in a marketplace repo** (ABSOLUTELY CRITICAL - NEVER SKIP!)
- ✅ **🚨 UPDATE marketplace.json with correct source path: ./plugins/PLUGIN_NAME** (NOT ./PLUGIN_NAME!)
- ✅ **🚨 SYNCHRONIZE description and keywords from plugin.json to marketplace.json** (they don't auto-sync - must be done manually!)
- ✅ **ALWAYS fetch latest plugin docs first** (plugins-reference and plugin-marketplaces)
- ✅ **Follow the structure from the fetched docs, not just templates** (docs = source of truth)
- ✅ Actually create files in the working directory
- ✅ Verify component registration method against fetched docs
- ✅ Create complete, working examples
- ✅ Generate both plugin and marketplace structures
- ✅ Double-check all required fields from docs are included
- ✅ Include GitHub-first installation instructions
- ✅ Warn Windows users about local path issues
- ✅ Show skill export process if user requests claude.ai web usage
- ✅ Make content specific to user's needs
- ✅ Test that structure is correct before packaging

**DON'T:**
- ❌ **🚨 Skip detecting repository context in Step 0** (MOST CRITICAL - detect git values BEFORE creating files!)
- ❌ **🚨 Create plugins in root directory when marketplace.json exists** (MUST create in plugins/ subdirectory!)
- ❌ **🚨 Use placeholder values like "Author Name" or "YOUR_USERNAME"** (MUST use detected git config values!)
- ❌ **🚨 Use different author names in plugin.json vs marketplace.json** (MUST match marketplace owner for consistency!)
- ❌ **🚨 Use wrong source path in marketplace.json** (MUST be `./plugins/PLUGIN_NAME` NOT `./PLUGIN_NAME`!)
- ❌ **🚨 Use `"author": "Name"` as a string** (MUST be an object: `{ "name": "Name" }`)
- ❌ **🚨 Use `"version": 1.0` as a number** (MUST be a string: `"1.0.0"`)
- ❌ **🚨 Use `"keywords": "word1, word2"` as a string** (MUST be an array: `["word1", "word2"]`)
- ❌ **🚨 Forget to update existing marketplace.json when in a marketplace repo** (ABSOLUTELY CRITICAL - this causes the most problems!)
- ❌ **🚨 Forget to synchronize description/keywords between plugin.json and marketplace.json** (CRITICAL - they are separate files!)
- ❌ **Skip fetching the latest documentation** (required for correct structure!)
- ❌ **Blindly copy templates without verifying against fetched docs**
- ❌ Assume requirements haven't changed
- ❌ Just show example code without creating files
- ❌ Create incomplete structures
- ❌ Skip creating ZIP files
- ❌ Forget the marketplace.json in standalone marketplace
- ❌ Use placeholder content without customizing
- ❌ Provide only directory links (users can't download directories!)
- ❌ Forget to mention Windows path limitations
- ❌ Skip GitHub-first recommendations

### Platform-Specific Notes for Users

**Windows Users:**
- ⚠️ Local plugin installation may not work due to path resolution issues
- ✅ GitHub marketplace installation works reliably
- ✅ Always use the marketplace method for best results

**Git Bash/MinGW Users (Windows):**
- ⚠️ Path conversion may affect plugin installation paths
- ✅ Detect shell with: `echo $MSYSTEM` (MINGW64/MINGW32 indicates Git Bash)
- ✅ Use `cygpath` for path conversion if needed: `cygpath -w "/c/path"` → `C:\path`
- ✅ GitHub marketplace method bypasses local path issues
- 💡 Shell detection: Check `$MSYSTEM` environment variable (MINGW64, MINGW32, MSYS)

**Mac/Linux Users:**
- ✅ Both local and GitHub installation methods work
- 💡 GitHub method still recommended for easy updates and sharing

### Ready-to-Upload GitHub Structure (in ZIP)

When creating marketplace ZIP, ensure it contains this structure:

```
plugin-name-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── plugins/
│   └── plugin-name/              # The actual plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       ├── agents/
│       └── README.md
└── README.md                     # Marketplace README
```

Users can extract this ZIP and upload directly to GitHub!

## What is Claude Code?

<introduction>
Claude Code is a command-line tool that lets you work with Claude AI directly in your terminal. Instead of copying code back and forth between a browser and your code editor, Claude can read your files, run commands, and help you code right where you work.

Think of it like having an AI pair programmer in your terminal who can:
- Read and understand your project
- Write and edit code
- Run tests and commands
- Help debug issues
- Learn from custom instructions you provide

**Plugins extend Claude Code** by adding new commands, agents, and capabilities. If you're new to coding or command-line tools, don't worry - this guide starts from the very beginning.
</introduction>

### Why Would I Create a Plugin?

Plugins let you:
- **Teach Claude your workflow** - Create commands for tasks you do repeatedly
- **Share your expertise** - Package your knowledge to help others
- **Customize Claude** - Add domain-specific abilities (deployment, testing, etc.)
- **Automate tasks** - Turn multi-step processes into single commands
- **Build tools for teams** - Create shared commands for your company

You don't need to be a programmer to create useful plugins!

## Your First Plugin in 10 Minutes

<first_plugin_tutorial>
Let's create a simple plugin that helps with git commits. No prior plugin experience needed!

### What We'll Build

A plugin with a single command: `/commit-smart` that helps write better commit messages.

### Step 1: Ask Claude to Create It

Just say:

> "Create a plugin that helps me write better git commit messages"

Claude will:
1. Create all the necessary files
2. Package it as a ZIP
3. Give you download links
4. Provide installation instructions

### Step 2: Download and Upload to GitHub

1. Click the marketplace ZIP download link Claude provides
2. Extract the ZIP file
3. Go to GitHub and create a new repository
4. Upload the extracted files to your repo
5. Make the repository public

### Step 3: Install Your Plugin

In Claude Code:

```bash
/plugin marketplace add YOUR_USERNAME/YOUR_REPO
/plugin install commit-helper@YOUR_USERNAME
```

### Step 4: Use It!

```bash
/commit-smart
```

Claude will now help you write a great commit message!

### What Just Happened?

You created, published, and installed your first plugin! Here's what you made:

1. **A plugin** - A collection of capabilities for Claude
2. **A command** - `/commit-smart` that Claude can use
3. **A marketplace** - A GitHub repo hosting your plugin
4. **A shareable tool** - Anyone can now use your plugin!

That's it! You're now a plugin creator. Everything else in this guide builds on these basics.
</first_plugin_tutorial>

## Understanding Plugin Basics

### What's in a Plugin?

Only `.claude-plugin/plugin.json` is required. Optional components: commands/, agents/, skills/, hooks/, MCP servers.

### Plugin Components

**Commands**: Custom slash commands in `commands/*.md`
**Agents**: Specialized subagents in `agents/*.md` with frontmatter
**Agent Skills**: Dynamic knowledge using progressive disclosure (three-tier: frontmatter → SKILL.md body → linked files). Claude autonomously loads only relevant content when needed.
**Hooks**: Automated workflows with nine event types (PreToolUse, PostToolUse, SessionStart, SessionEnd, PreCompact, UserPromptSubmit, Notification, Stop, SubagentStop)
**MCP Servers**: External tool integration via Model Context Protocol

Agent Skills use context-efficient loading patterns, retrieving only necessary components instead of entire skill content. For detailed patterns, see advanced-features-2025 skill.

### Plugin vs Marketplace: What's the Difference?

**Plugin:**
- A single tool with commands/agents/skills
- One folder with a plugin.json
- Like a single app on your phone

**Marketplace:**
- A collection of plugins
- One folder containing multiple plugins
- Like an app store containing many apps

Most people create one marketplace that holds all their plugins.

## Creating Your Plugin Structure

<plugin_structure_details>
When Claude creates a plugin for you, it generates all files automatically. But here's what each file does so you can customize it:

### The Required File: plugin.json

This is the only required file. It tells Claude Code about your plugin:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["helpful", "search", "terms"],
  "license": "MIT"
}
```

**Important fields:**
- `name`: Must be unique, use kebab-case (my-plugin-name)
- `version`: Follow semantic versioning (1.0.0)
- `description`: Help others find your plugin

### Directory Organization

- `commands/` → Each .md file becomes a slash command
- `agents/` → Subagents with specialized expertise (require frontmatter)
- `skills/` → Agent Skills for dynamic knowledge loading
- `hooks/` → Automated workflows (see advanced-features-2025 skill)
- `scripts/`, `bin/` → Helper utilities

**Portability:** Use `${CLAUDE_PLUGIN_ROOT}` for all internal paths in hooks and MCP servers. This environment variable resolves to the plugin's absolute installation path, ensuring cross-platform compatibility.

## Publishing Your Plugin to a Marketplace

<publishing_guide>
The easiest way to share your plugin is via a GitHub marketplace. Claude creates both plugin and marketplace ZIPs for you automatically!

### Quick Publishing Steps

1. **Download the marketplace ZIP** Claude created for you
2. **Create a GitHub repository:**
   - Go to github.com
   - Click "New repository"
   - Give it a name like "my-claude-plugins"
   - Make it **public** (required for others to use it)
   - Don't initialize with README (you have one in the ZIP)

3. **Upload your files:**
   - Extract the marketplace ZIP
   - Upload all files to your repository
   - Make sure `.claude-plugin/marketplace.json` is in the root

4. **Verify structure:**
```
your-repo/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── your-plugin/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── ...
└── README.md
```

5. **That's it!** Your marketplace is live. Anyone can now add it:
```bash
/plugin marketplace add YOUR_USERNAME/REPO_NAME
```

### The Marketplace.json File

After fetching the marketplace documentation, Claude creates this file according to the official structure. Here's a reference example (verify against docs):

```json
{
  "name": "my-marketplace",
  "description": "My collection of Claude Code plugins",
  "owner": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

**Key points from typical marketplace structure:**
- `source` points to where your plugin lives in the repo
- You can have multiple plugins in one marketplace
- The `name` in marketplace.json typically matches your GitHub username
- Check the docs for all required fields (structure may have evolved)

### Testing Before Publishing

Before making your repo public, test locally:

1. **Extract your plugin ZIP** to test location:
```bash
unzip my-plugin.zip -d ~/.local/share/claude/plugins/
```

2. **Test in Claude Code:**
```bash
/help          # See your commands
/agents        # See your agents
```

3. **Fix any issues**, then proceed to publish

### Updating Your Plugin

When you make changes:

1. **Update version** in plugin.json (e.g., 1.0.0 → 1.0.1)
2. **Update version** in marketplace.json
3. **Commit and push** to GitHub
4. **Users update** with:
```bash
/plugin marketplace update marketplace-name
/plugin update plugin-name
```

### Making Your Plugin Discoverable

Add your marketplace to community directories:
- https://claudecodemarketplace.com/ - Plugin directory
- https://claudemarketplaces.com/ - Marketplace directory

Include good keywords in your plugin.json for searchability!
</publishing_guide>

## Testing Your Plugin

<testing_guide>
Before sharing your plugin, test it thoroughly:

### Local Testing (Mac/Linux Only)

⚠️ **Windows users:** Skip to GitHub testing method below.

1. **Extract plugin ZIP to plugins directory:**
```bash
mkdir -p ~/.local/share/claude/plugins
unzip my-plugin.zip -d ~/.local/share/claude/plugins/
```

2. **Restart Claude Code or run:**
```bash
claude --reload-plugins
```

3. **Verify plugin loaded:**
```bash
/plugin list
```

4. **Test each component:**
```bash
/help                    # See your commands
/agents                  # See your agents
/your-command           # Test a command
```

### GitHub Testing (All Platforms)

This works reliably on Windows, Mac, and Linux:

1. **Create a private test repository** on GitHub
2. **Upload your marketplace ZIP contents** to the repo
3. **Make repo public** (required for Claude Code to access)
4. **Add marketplace:**
```bash
/plugin marketplace add YOUR_USERNAME/YOUR_TEST_REPO
```
5. **Install and test:**
```bash
/plugin install my-plugin@YOUR_USERNAME
/help
```

### Common Testing Checklist

- [ ] Plugin appears in `/plugin list`
- [ ] Commands show in `/help`
- [ ] Agents show in `/agents`
- [ ] Commands execute without errors
- [ ] Agents provide expected behavior
- [ ] README renders correctly on GitHub
- [ ] No sensitive information in files
- [ ] All paths work (especially scripts)

### Debug Mode

If something's not working:

```bash
claude --debug
```

This shows detailed loading information and error messages.
</testing_guide>

## Real-World Plugin Examples

<plugin_examples>
**PR Review Helper**: Commands for code/test review + security/code-reviewer agents
**Team Onboarding**: Skills for tech stack/standards + setup commands
**API Integration**: Commands for common operations + domain expert agent + API skill
**Documentation Generator**: Commands for docs/readme/changelog generation

Even simple 1-3 command plugins provide immense value. Just describe what you want to Claude.
</plugin_examples>

## Tips for Better Plugins

<plugin_tips>
### Writing Quality Components

**Commands**: Be specific, include examples, handle errors, explain why not just what
**Agents**: Define clear role, perspective, and constraints (what they DON'T do)
**Agent Skills**: Focus on single domain, scannable headers, concrete examples, updated content

See advanced-features-2025 skill for Agent Skills best practices and patterns.

### Keep Plugins Focused

**Better:** 5 small focused plugins
**Worse:** 1 giant plugin that does everything

Why? 
- Easier to maintain
- Easier for others to use
- Faster loading
- Clearer purpose

**Example:**
Instead of "dev-helper" plugin with 20 commands, create:
- "git-helper" - Git workflows
- "deploy-helper" - Deployment tasks
- "test-helper" - Testing utilities
- "docs-helper" - Documentation

### Version Control

Keep your plugins in Git:
1. Tracks changes over time
2. Enables collaboration
3. Users can see history
4. Easy rollback if needed

### Documentation

Your README should answer:
1. **What does this plugin do?** (One sentence)
2. **Why would I use it?** (The problem it solves)
3. **How do I install it?** (Exact commands)
4. **How do I use it?** (Examples)
5. **What are the commands?** (List with descriptions)

See the README template in [Output Templates](#output-templates) above.
</plugin_tips>

## Common Issues and Solutions

<troubleshooting>
### Plugin Not Loading

**Symptoms:** Plugin doesn't appear in `/plugin list`

**Solutions:**
1. **Check plugin.json syntax**
   - Valid JSON?
   - Required fields present?
   - Use a JSON validator

2. **Check file location (for local plugins - Mac/Linux only)**
   - Should be: `~/.local/share/claude/plugins/PLUGIN_NAME/`
   - Not: `~/.local/share/claude/plugins/PLUGIN_NAME/PLUGIN_NAME/`

3. **Windows users:** Local plugins may not work. Use GitHub marketplace instead:
   ```bash
   /plugin marketplace add YOUR_USERNAME/YOUR_REPO
   ```

4. **Git Bash/MinGW users:** Path conversion issues may prevent plugin loading:
   ```bash
   # Detect your shell environment
   echo $MSYSTEM  # Should show MINGW64, MINGW32, or MSYS

   # Check if path conversion is affecting plugin directory
   echo ~/.local/share/claude/plugins

   # If path looks wrong, use GitHub marketplace method instead
   /plugin marketplace add YOUR_USERNAME/YOUR_REPO
   ```

5. **Reload plugins:**
   ```bash
   claude --reload-plugins
   ```

6. **Check debug output:**
   ```bash
   claude --debug
   ```

### Commands Not Showing Up

**Symptoms:** Plugin loads but commands missing from `/help`

**Solutions:**
1. **Check if registration is required (check the official docs)**
   - Fetch and read: https://docs.claude.com/en/docs/claude-code/plugins-reference
   - See if commands need to be registered in plugin.json
   - If yes, verify your plugin.json has the proper structure
   - Compare your plugin.json to the examples in the docs
   
2. **Check file location**
   - Commands must be in `commands/` directory
   - Directly in the directory, not in subdirectories
   
3. **Check frontmatter**
   - Must have `---` delimiters
   - `description` field recommended
   
4. **Check filename**
   - Must end in `.md`
   - No spaces in name (use hyphens)
   
5. **Reload:**
   ```bash
   claude --reload-plugins
   ```

### Agents Not Appearing

**Symptoms:** Plugin loads but agents missing from `/agents`

**Solutions:**
1. **Check if registration is required (check the official docs)**
   - Fetch and read: https://docs.claude.com/en/docs/claude-code/plugins-reference
   - See if agents need to be registered in plugin.json
   - If yes, verify your plugin.json has the proper structure
   - Compare your plugin.json to the examples in the docs
   
2. **Check frontmatter**
   - Must include `agent: true`
   - Must have `---` delimiters
   
3. **Check file location**
   - Must be in `agents/` directory
   
4. **Check filename**
   - Must end in `.md`

### Marketplace Not Found

**Symptoms:** Can't add marketplace, says not found

**Solutions:**
1. **Check repository is public**
   - Private repos need authentication
   - Make sure you didn't typo the username/repo name
   
2. **Check marketplace.json exists**
   - Must be at `.claude-plugin/marketplace.json`
   - In the repository root
   
3. **Try full URL**
   - Instead of `username/repo`
   - Try `https://github.com/username/repo.git`

### "Plugin Failed to Load" Error

**Symptoms:** Error message when installing

**Solutions:**
1. **Check for typos in JSON files**
   - Missing commas, brackets
   - Use a JSON validator
   
2. **Check file permissions**
   - Can Claude Code read the files?
   - Try `chmod +x` on script files
   
3. **Check logs**
   - Run `claude --debug` to see detailed errors
   - Look for specific error messages

### Windows Local Path Issues

**Symptoms:** Plugin works on Mac/Linux but not Windows

**Solutions:**
1. **Use GitHub marketplace method:**
   - This is the recommended approach for Windows
   - Upload to GitHub and install via marketplace
   
2. **Alternative:** Use WSL (Windows Subsystem for Linux)
   - Install WSL2
   - Install Claude Code in WSL
   - Follow Linux installation steps

### Still Stuck?

<getting_unstuck>
If you're still having trouble:

1. **Ask Claude directly**
   - "Help me debug my plugin"
   - "Fetch the latest plugin troubleshooting docs"
   
2. **Check existing plugins**
   - Browse https://claudecodemarketplace.com/
   - Look at their GitHub repos for examples
   - Copy structure that works
   
3. **Get community help**
   - Claude Developers Discord
   - GitHub discussions
   - Stack Overflow (tag: claude-code)
   
4. **File a bug report**
   - Use `/bug` command in Claude Code
   - Or file issue on GitHub
</getting_unstuck>
</troubleshooting>

## Advanced Plugin Development

For advanced topics including Agent Skills patterns, hooks, MCP integration, environment variables, multi-plugin workflows, and testing strategies, see the advanced-features-2025 skill.

## Best Practices Summary

### For Beginners

✅ **DO:**
- Start simple (one command is fine!)
- Test using GitHub method (works everywhere)
- Write clear descriptions
- Include examples in README
- Ask for help when stuck

❌ **DON'T:**
- Try to build everything at once
- Skip testing
- Hardcode sensitive information
- Use complicated structures initially
- Rely on local paths on Windows

### Naming Conventions

- **Plugin names:** `my-plugin-name` (kebab-case)
- **Command names:** `/do-something` (verb-based, kebab-case)
- **Agent names:** `Role Describer` (clear role indication)
- **File names:** lowercase with hyphens

### Security Checklist

Before publishing:
- [ ] No API keys or passwords in code
- [ ] Use environment variables for secrets
- [ ] Document security requirements
- [ ] Review scripts for security issues
- [ ] Consider what permissions plugin needs

### Documentation Checklist

Every plugin should have:
- [ ] README.md with installation instructions
- [ ] Usage examples for each feature
- [ ] Required configuration explained
- [ ] Platform-specific notes (Windows/Mac/Linux)
- [ ] License file
- [ ] Contributing guidelines (optional)

### Platform Compatibility Checklist

- [ ] README mentions platform compatibility
- [ ] Windows users directed to GitHub method
- [ ] Local paths avoided in favor of GitHub
- [ ] Installation tested on multiple platforms
- [ ] Clear warnings about platform limitations

## Quick Reference

### Required Files

```
my-plugin/
└── .claude-plugin/
    └── plugin.json       # ← This file is REQUIRED
```

### Minimal plugin.json

**Basic structure (verify against current docs):**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
```

**With full metadata:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "keywords": ["keyword1", "keyword2"],
  "license": "MIT"
}
```

**Note:** Components (commands, agents, skills) don't need to be registered in plugin.json - they are discovered automatically from their directories.

### Minimal marketplace.json

**Example structure (verify against current marketplace docs):**
```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "Complete [domain] expertise system. PROACTIVELY activate for: (1) [use cases]. Provides: [capabilities].",
      "version": "1.0.0",
      "author": {
        "name": "Author Name"
      },
      "keywords": ["domain", "primary", "secondary", "technical"]
    }
  ]
}
```

**⚠️ CRITICAL:** Always include description and keywords in marketplace.json entries - they are used for marketplace discovery and don't automatically sync from plugin.json.

**Note:** Check the fetched marketplace documentation for all required fields.

### Essential Commands

```bash
# Marketplace management
/plugin marketplace add username/repo
/plugin marketplace list
/plugin marketplace update marketplace-name
/plugin marketplace remove marketplace-name

# Plugin management
/plugin install plugin-name@marketplace-name
/plugin list
/plugin uninstall plugin-name

# Testing
/help                      # See your commands
/agents                    # See your agents
claude --debug             # Debug mode
```

### Installation Methods by Platform

**Windows:**
```bash
# RECOMMENDED: GitHub marketplace
/plugin marketplace add YOUR_USERNAME/YOUR_REPO
/plugin install plugin-name@YOUR_USERNAME
```

**Mac/Linux:**
```bash
# Option 1: GitHub marketplace (recommended)
/plugin marketplace add YOUR_USERNAME/YOUR_REPO
/plugin install plugin-name@YOUR_USERNAME

# Option 2: Local installation
unzip plugin-name.zip -d ~/.local/share/claude/plugins/
```

## Additional Resources

### Official Documentation
- **Plugins Guide:** https://docs.claude.com/en/docs/claude-code/plugins
- **Marketplace Guide:** https://docs.claude.com/en/docs/claude-code/plugin-marketplaces
- **Plugins Reference:** https://docs.claude.com/en/docs/claude-code/plugins-reference
- **MCP Documentation:** https://docs.claude.com/en/docs/claude-code/mcp
- **Skills Engineering:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### Community Resources
- **Plugin Directory:** https://claudecodemarketplace.com/
- **Marketplace Directory:** https://claudemarketplaces.com/
- **Official GitHub:** https://github.com/anthropics/claude-code
- **Claude Developers Discord:** Join for help and discussion
- **Community Plugins:** Browse GitHub for examples and inspiration

### Related Skills
- **skill-creator:** Create optimized Skills to package in plugins
- **context-master:** Optimize multi-file plugin development

## Conclusion

You now have everything you need to create, test, and publish Claude Code plugins!

**Remember:**
- Start simple - your first plugin can be just one command
- Use GitHub marketplace for reliable cross-platform distribution
- Test thoroughly before sharing
- Don't hesitate to ask for help
- Share your work with the community

**Your journey:**
1. ✅ Created your first plugin
2. ✅ Learned plugin structure
3. ✅ Packaged as downloadable ZIPs
4. ✅ Published to a marketplace
5. 🎯 Next: Build something useful!

**Platform compatibility:**
- ✅ GitHub method works on all platforms
- ⚠️ Local installation may have issues on Windows
- 💡 Always provide ZIP downloads for users

<final_encouragement>
Every expert was once a beginner. Your first plugin doesn't need to be perfect - it just needs to exist. Start simple, learn as you go, and before you know it, you'll be creating sophisticated plugins that help developers around the world.

Now go build something awesome! 🚀
</final_encouragement>
