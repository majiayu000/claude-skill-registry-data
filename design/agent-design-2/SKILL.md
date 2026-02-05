---
name: Agent Design 2
description: This skill should be used when the user asks to "configure agent profile", "add skills to agent", "set up MCP servers", "configure agent tools", "write system prompt", "create agent workflow", "define agent commands", "add subagents", or needs to define what capabilities an agent has and how to orchestrate complex workflows in the runtime.
---

# Agent Design

## Overview

Agent profiles define what an agent can do - its personality, tools, skills, subagents, commands, and integrations. The runtime is architecture-agnostic, supporting both Claude Agent SDK and OpenCode.

## AgentProfile Structure

```typescript
interface AgentProfile {
  // Identity
  id: string;                      // Unique identifier
  name: string;                    // Display name
  description?: string;            // Human-readable description

  // Behavior
  systemPrompt?: string;           // Agent's system prompt
  agentMDFile?: string;            // Memory file content (CLAUDE.md/AGENT.md)

  // Capabilities
  tools?: string[];                // Available tools
  skills?: ClaudeSkill[];          // Skill definitions
  subagents?: ClaudeSubagent[];    // Subagent definitions
  commands?: AgentCommand[];       // Command definitions

  // Integrations
  bundledMCPs?: LocalMcpServer[];  // MCP servers bundled with agent
  externalMCPs?: McpServerConfig[];// External MCP servers

  // Environment
  npmDependencies?: string[];      // npm packages to install
  pipDependencies?: string[];      // pip packages to install
  environmentVariables?: Record<string, string>;
  defaultWorkspaceFiles?: WorkspaceFile[];
}
```

## System Prompt vs Agent Memory File

Both can be used together:

| Field | Purpose | Analogy |
|-------|---------|---------|
| `systemPrompt` | Core personality and instructions | The agent's "DNA" |
| `agentMDFile` | Contextual memory and project knowledge | The agent's "CLAUDE.md" or "AGENT.md" |

**Example:**

```typescript
const profile: AgentProfile = {
  id: "code-assistant",
  name: "Code Assistant",

  // Core behavior - who the agent is
  systemPrompt: `You are a senior software engineer. You write clean,
tested code. You explain your reasoning before making changes.`,

  // Project context - what the agent knows about this workspace
  agentMDFile: `# Project: E-commerce API

## Tech Stack
- Node.js + TypeScript
- PostgreSQL + Prisma
- Jest for testing

## Conventions
- Use kebab-case for files
- All API routes in src/routes/
- Run tests before committing`,
};
```

## Tools Configuration

Available tools for Claude Agent SDK:

```typescript
tools: [
  "Read",    // Read files
  "Write",   // Create new files
  "Edit",    // Edit existing files
  "Bash",    // Execute shell commands
  "Grep",    // Search file contents
  "Glob",    // Find files by pattern
]
```

## Skills

Skills provide specialized knowledge and workflows:

```typescript
interface ClaudeSkill {
  name: string;              // Skill identifier
  description: string;       // When to use this skill
  skillMd: string;           // Main skill content (markdown)
  supportingFiles?: {        // Additional resources
    relativePath: string;
    content: string;
  }[];
  npmDependencies?: string[];
  pipDependencies?: string[];
}
```

**Example skill:**

```typescript
skills: [{
  name: "api-testing",
  description: "Testing REST APIs with curl and validation",
  skillMd: `# API Testing Skill

## When to Use
Use this skill when testing API endpoints.

## Process
1. Identify endpoint and method
2. Construct curl command
3. Validate response structure
4. Check status codes

## Common Patterns
\`\`\`bash
# GET request
curl -X GET http://localhost:3000/api/users

# POST with JSON
curl -X POST http://localhost:3000/api/users \\
  -H "Content-Type: application/json" \\
  -d '{"name": "John"}'
\`\`\``,
  supportingFiles: [{
    relativePath: "templates/test-script.sh",
    content: "#!/bin/bash\ncurl -v $1"
  }]
}]
```

## Subagents

Subagents handle delegated tasks during a session:

```typescript
interface ClaudeSubagent {
  name: string;           // Subagent identifier
  description: string;    // When main agent should use this
  prompt: string;         // Subagent's instructions
  model?: string;         // "sonnet" | "opus" | "haiku" | "inherit"
  tools?: string[];       // Allowed tools (subset of main agent)
}
```

**Example:**

```typescript
subagents: [{
  name: "test-writer",
  description: "Delegate test writing to this subagent",
  prompt: `You are a test-writing specialist. Given code, write
comprehensive unit tests. Use Jest. Cover edge cases.`,
  model: "haiku",  // Use faster model for focused task
  tools: ["Read", "Write", "Bash"]
}, {
  name: "code-reviewer",
  description: "Delegate code review to this subagent",
  prompt: `You are a code reviewer. Analyze code for bugs,
security issues, and style problems. Be thorough but constructive.`,
  model: "sonnet",
  tools: ["Read", "Grep"]
}]
```

## Commands

Commands enable the calling application to trigger specific agent workflows by sending command text as a prompt:

```typescript
interface AgentCommand {
  name: string;     // Command identifier
  prompt: string;   // Instructions executed when command is invoked
}
```

**Example:**

```typescript
commands: [{
  name: "review-pr",
  prompt: `Review the current pull request:

1. Use the code-reviewer subagent to analyze changes
2. Check for security issues using the security-audit skill
3. Verify tests pass by running: npm test
4. Generate a summary with:
   - Overview of changes
   - Issues found (critical/warning/info)
   - Recommendations

Output a structured review report.`
}, {
  name: "deploy-staging",
  prompt: `Deploy to staging environment:

1. Run all tests: npm test
2. Build the project: npm run build
3. Use the deployment MCP server to push to staging
4. Verify deployment with health check
5. Report deployment status`
}]
```

**Invoking commands:** The calling application sends the command name as a message:

```typescript
// In your React app
const { sendMessage } = useMessages(sessionId);
await sendMessage("/review-pr");  // Triggers the review-pr command
```

## MCP Servers

### Bundled MCP Servers

MCP servers packaged with the agent:

```typescript
interface LocalMcpServer {
  name: string;              // Server identifier
  description: string;       // What this server provides
  localProjectPath: string;  // Path to MCP server project
  startCommand: string;      // Command to start server
  installCommand: string;    // Command to install dependencies
}
```

**Example:**

```typescript
bundledMCPs: [{
  name: "github-tools",
  description: "GitHub API integration for PRs, issues, repos",
  localProjectPath: "./mcps/github-server",
  startCommand: "tsx src/index.ts",
  installCommand: "npm install"
}]
```

### External MCP Servers

Pre-existing MCP servers:

```typescript
externalMCPs: [{
  name: "filesystem",
  command: "npx",
  args: ["-y", "@anthropic-ai/mcp-server-filesystem", "/workspace"]
}]
```

## Workflow Patterns

### Pattern 1: Command-Driven Workflows

Define commands that orchestrate skills, subagents, and tools:

```typescript
commands: [{
  name: "full-feature",
  prompt: `Implement the requested feature:

Phase 1 - Planning:
- Use the architecture skill to design the approach
- Create a task breakdown

Phase 2 - Implementation:
- Implement core functionality
- Use test-writer subagent for unit tests

Phase 3 - Review:
- Use code-reviewer subagent for review
- Address any critical issues

Phase 4 - Finalize:
- Run full test suite
- Update documentation`
}]
```

### Pattern 2: Skill Chains

Skills that reference other skills:

```typescript
skills: [{
  name: "bug-fix",
  description: "Systematic bug fixing process",
  skillMd: `# Bug Fix Process

1. **Reproduce** - Verify the bug exists
2. **Locate** - Use the debugging skill to find root cause
3. **Fix** - Implement minimal fix
4. **Test** - Use the testing skill to verify
5. **Document** - Update changelog`
}]
```

### Pattern 3: MCP-Enhanced Workflows

Commands that leverage MCP servers:

```typescript
commands: [{
  name: "sync-docs",
  prompt: `Synchronize documentation:

1. Use the notion-mcp server to fetch latest specs
2. Update local markdown files
3. Use the github-mcp server to create PR
4. Post summary to slack-mcp`
}]
```

## Complete Example

```typescript
const fullAgentProfile: AgentProfile = {
  id: "full-stack-dev",
  name: "Full Stack Developer",
  description: "Complete development assistant",

  systemPrompt: `You are a senior full-stack developer. You write
clean, tested, documented code. You think before coding.`,

  agentMDFile: `# Project Context
TypeScript monorepo with React frontend and Node.js backend.
Use pnpm. Follow existing patterns.`,

  tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],

  skills: [{
    name: "testing",
    description: "Write and run tests",
    skillMd: "# Testing\nUse Jest. Cover edge cases. Mock externals."
  }],

  subagents: [{
    name: "reviewer",
    description: "Code review",
    prompt: "Review code for bugs and style issues.",
    model: "haiku",
    tools: ["Read", "Grep"]
  }],

  commands: [{
    name: "implement",
    prompt: "Plan, implement, test, and review the feature."
  }],

  bundledMCPs: [{
    name: "db-tools",
    description: "Database operations",
    localProjectPath: "./mcps/db",
    startCommand: "node index.js",
    installCommand: "npm install"
  }],

  npmDependencies: ["lodash", "zod"],
  environmentVariables: {
    NODE_ENV: "development"
  }
};
```

## Related Skills

- **overview** - Understanding the runtime architecture
- **backend-setup** - Setting up the backend server
- **react-integration** - Building React frontends
