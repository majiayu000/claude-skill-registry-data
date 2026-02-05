---
name: amp-skill-creator
description: Create Amp-native skills with proper SKILL.md format, optional bundled tools, MCP servers, and directory structure. Use this skill as the default skill creation skill, unless specifically told to create a generic or Claude code-specific skill. Activates with phrases like "create a skill", "new skill", "skill for amp", or when user wants bundled tools, mcp.json servers, or toolbox-compatible skills.
argument-hint: "[skill-name] [objective]"
---

# Amp Skill Creator

This skill teaches you how to create **Amp-native skills** - specialized instruction packages that teach the agent how to perform specific tasks within the Amp ecosystem.

## When to Use This Skill

✅ **Use for Amp skills when:**

- User asks to create a skill specifically for Amp
- Skill needs bundled executable tools in `tools/` subdirectory
- Skill needs bundled MCP servers via `mcp.json`
- Skill will live in `.agents/skills/` or `~/.config/amp/skills/`

❌ **Use generic agent-skill-creator instead when:**

- Creating Claude Code plugins with marketplace.json
- Cross-agent requirements (Amp and Claude code)

## Amp Skill Format

### Directory Structure

```sh
skill-name/
├── SKILL.md              # Required: Main skill definition
├── tools/                # Optional: Bundled executable tools
│   ├── analyze           # Executable script (receives JSON stdin, outputs JSON stdout)
│   └── transform
├── mcp.json              # Optional: Bundled MCP servers
└── references/           # Optional: Documentation, templates
```

### SKILL.md Format (Required)

Every Amp skill MUST have a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill-name
description: A description of what this skill does and when to use it (shown in skill list)
---

# My Skill Instructions

Detailed instructions for the agent...
```

**Required frontmatter fields:**

- `name`: Skill identifier (lowercase, hyphens allowed)
- `description`: What the skill does (shown in `/skill-list`)

**Optional frontmatter fields:**

- `argument-hint`: Hint shown in skills list (e.g., `"[query]"`, `"[repo] [issue]"`)
- `disable-model-invocation`: If `true`, hides skill from agent's auto-detection

### Bundled Executable Tools

Skills can include executable tools in a `tools/` subdirectory:

```sh
skill-name/
├── SKILL.md
└── tools/
    ├── analyze        # Must be executable
    └── transform
```

**Tool requirements:**

- Tools receive JSON input on stdin
- Tools output JSON to stdout
- Tools are hidden until skill is loaded
- Follow same format as toolbox tools

> If you believe a tool would be helpful for this skill, invoke the `amp-tool-creator` skill to create it

### Bundled MCP Servers

Skills can bundle MCP servers via `mcp.json`:

```json
{
  "local-server-name": {
    "command": "npx",
    "args": ["-y", "some-mcp-server@latest"],
    "includeTools": ["tool_a", "tool_b", "navigate_*"]
  },
  "remote-server-name": {
    "url": "https://some-mcp-server.com/mcp",
    "headers": {
      "Authorization": "Bearer <token>"
    },
    "includeTools": ["tool_a", "tool_b", "navigate_*"]
  }
}
```

**local mcp.json fields:**

- `command`: Command to run (required)
- `args`: Array of command arguments
- `env`: Environment variables for the server
- `includeTools`: Glob patterns to filter exposed tools (e.g., `["navigate_*", "click"]`, or `["*"]` for all)

**remote mcp.json fields:**

- `url`: URL of the MCP server
- `headers`: Headers to send with requests

**Environment variables:** Use `${VAR_NAME}` syntax in any field to reference environment variables.

#### OAuth for Remote MCP Servers

Some remote MCP servers support OAuth authentication. There are two flows:

**Dynamic Client Registration (DCR):**
Servers like Linear support automatic OAuth registration. Users just add the server and Amp handles auth automatically:

```sh
amp mcp add linear https://mcp.linear.app/sse
# Browser opens for auth on startup
```

**Manual OAuth Registration:**
For servers requiring manual setup:

1. User creates OAuth client in the server's admin interface:

   - Redirect URI: `http://localhost:8976/oauth/callback`
   - Configure required scopes

2. User adds the MCP server:

   ```sh
   amp mcp add my-server https://example.com/.api/mcp/v1
   ```

3. User registers OAuth credentials:
   ```sh
   amp mcp oauth login my-server \
     --server-url https://example.com/.api/mcp/v1 \
     --client-id your-client-id \
     --client-secret your-client-secret \
     --scopes "openid,profile,email"
   ```

OAuth tokens are stored in `~/.amp/oauth/` and auto-refresh.

**When bundling OAuth-required servers:** Document the OAuth setup steps in your SKILL.md prerequisites section—users must complete OAuth before the skill works.

> Typically, you should only include an MCP server if the user explicitly mentions that they want to use it. If they do, feel empowered to web search for details on the particular MCP server to understand how to invoke it and what tools it exposes. Prefer limiting the number of tools from the MCP server to the minimum necessary for the purposes of this skill, as each additional tool consumes a potentially significant amount of context.

---

## Skill Creation Protocol

### Phase 1: Requirements Analysis

Extract from user input:

- **Domain**: What area does this skill cover?
- **Objective**: What should the agent be able to do?
- **Tools needed**: Does it need bundled executables?
- **MCP servers**: Does it need external tool servers?
- **Complexity**: Simple instructions vs. complex workflow?

### Phase 2: Architecture Decision

**Simple Skill** (most common):

```sh
skill-name/
└── SKILL.md
```

**Skill with Tools**:

```sh
skill-name/
├── SKILL.md
└── tools/
    └── executable-tool
```

**Skill with MCP Servers**:

```sh
skill-name/
├── SKILL.md
└── mcp.json
```

**Complex Skill**:

```sh
skill-name/
├── SKILL.md
├── tools/
│   └── ...
├── mcp.json
└── references/
    └── ...
```

### Phase 3: SKILL.md Creation

#### Frontmatter Template

```yaml
---
name: skill-name
description: Comprehensive description with keywords for auto-activation. Include domain terms, action verbs, and use cases so the agent knows when to load this skill.
argument-hint: "[optional-args]"
---
```

#### Content Structure

The SKILL.md content should provide **high-level orchestration guidance**. When the skill includes bundled tools or MCP servers, those will auto-inject their own detailed instructions into context when loaded. Focus on:

- **When and why** to use the skill
- **Workflow orchestration** - how to combine tools/capabilities
- **Domain knowledge** the agent needs
- **Error handling patterns**

Avoid duplicating tool-specific invocation details that will be auto-injected.

````markdown
# Skill Name

Brief overview of what this skill enables.

## When to Use

Describe scenarios where this skill should be loaded.

## Prerequisites

Any setup, API keys, OAuth, or dependencies needed.

## Workflows

### Workflow 1: [Common Task]

High-level steps describing the orchestration:

1. **Step 1**: What to accomplish (tools will provide invocation details)
2. **Step 2**: Next logical step
3. **Step 3**: Verification/validation

### Workflow 2: [Another Task]

...

## Domain Knowledge

Context, terminology, or background the agent needs to make good decisions.

## Error Handling

Common errors and resolution patterns.

## Examples

**Example 1: [Scenario]**

```markdown
User: "..."
Agent approach: [high-level description of what agent does]
```
````

### Phase 4: Tool Implementation (if needed)

If the skill needs bundled executable tools, invoke the **toolbox-creator** skill to create them. Tools will be placed in the skill's `tools/` subdirectory.

### Phase 5: MCP Server Configuration (if needed)

```json
{
  "service-name": {
    "command": "npx",
    "args": ["-y", "package-name@latest"],
    "env": {
      "API_KEY": "${SERVICE_API_KEY}"
    },
    "includeTools": ["relevant_tool_*", "specific_tool"]
  }
}
```

### Phase 6: Validation

#### Validation Checklist

- [ ] SKILL.md exists with valid frontmatter
- [ ] `name` field is lowercase with hyphens only
- [ ] `description` includes activation keywords
- [ ] All tools in `tools/` are executable
- [ ] mcp.json is valid JSON (if present)

---

## Quality Standards

### SKILL.md Requirements

**Minimum length**: 1000+ words for substantial skills

**Must include:**

- ✅ Clear "When to Use" section
- ✅ Step-by-step workflows
- ✅ Real examples (not placeholders)
- ✅ Error handling guidance
- ✅ Domain-specific keywords in description

**Never include:**

- ❌ `# TODO` placeholders
- ❌ "See external docs" without content
- ❌ Generic advice without specifics

### Description Optimization

The `description` field is critical for auto-activation. Include:

- **Domain terms**: Specific technologies, services, concepts
- **Action verbs**: "analyze", "deploy", "configure", "monitor"
- **Use cases**: Specific scenarios the skill handles
- **Tool mentions**: If bundling tools, mention their purpose

**Good description example:**

```yaml
description: Manage Kubernetes deployments including pod scaling, rollout status, debugging crashloops, viewing logs, and applying manifests. Use for k8s, kubectl, container orchestration, deployment troubleshooting.
```

---

## Example: Complete Skill Creation

### User Request

"Create an Amp skill for managing tmux sessions"

### Created Structure

```sh
# Workspace-local (if in a project):
.agents/skills/tmux-manager/
└── SKILL.md

# Or user global:
~/.config/amp/skills/tmux-manager/
└── SKILL.md
```

### SKILL.md Content (use as inspiration, this is not a definitive template)

```markdown
---
name: tmux-manager
description: Manage tmux sessions for running background processes, servers, and long-running tasks. Spawn processes, capture output, send commands. Use for background jobs, dev servers, parallel tasks.
---

# Tmux Session Manager

Manage concurrent processes using tmux from within Amp.

## When to Use

- Running dev servers that need to persist
- Background builds or watchers
- Parallel task execution
- Capturing long-running output

## Prerequisites

Verify tmux is available and you're running inside a tmux session.

## Workflows

### Start Dev Server

1. Create a named window for the server
2. Send the start command to that window
3. Periodically capture output to check status

### Run Background Build

1. Create detached window
2. Send build command
3. Capture output when complete

## Patterns

### Chaining Commands

Multiple tmux operations can be chained with `';'` for efficiency.

### Output Capture

- Use `-p` flag to print to stdout
- Use `-S -` to capture full scrollback history

## Error Handling

- If window doesn't exist, create it first
- Always check `$TMUX` to verify you're in a tmux session
- Use `tmux list-windows` to verify window state
```

---

## Troubleshooting

### Skill Not Loading

1. Check SKILL.md exists and has valid frontmatter
2. Verify `name` and `description` fields present
3. Check skill location is in search path

### Tools Not Appearing

1. Verify tools are executable: `chmod +x tools/*`
2. Skill must be loaded for tools to appear
3. Check tool outputs valid JSON

### MCP Server Not Starting

1. Validate mcp.json syntax
2. Check command is available
3. Verify environment variables set

---

## Delivery Checklist

After creating a skill, verify:

- [ ] SKILL.md has valid frontmatter
- [ ] Description optimized for activation
- [ ] All workflows have complete examples
- [ ] Tools are executable and tested
- [ ] mcp.json is valid (if present)

**Inform user:**

```markdown
✅ Skill created: ./skill-name/

📁 Structure:

- SKILL.md (X words)
- tools/ (if applicable)
- mcp.json (if applicable)

💡 The skill will auto-load when you mention: [keywords]
```
