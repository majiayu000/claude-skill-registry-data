---
name: claude-code-design-guide
description: Comprehensive guide to understanding and implementing AI agent systems using Claude Code architecture patterns
triggers:
  - how does Claude Code agent system work
  - explain AI agent runtime architecture
  - show me Claude Code context engineering patterns
  - help me build an AI agent with tools
  - what are Claude Code design principles
  - implement MCP protocol for AI agents
  - create multi-agent coordination system
  - design AI agent tool system
---

# Claude Code Design Guide

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill provides deep expertise in AI agent system design based on Claude Code's architecture. Learn how to build production-grade AI agents with proper tool systems, context engineering, multi-agent coordination, and extensibility.

## What is Claude Code?

Claude Code is Anthropic's official AI programming assistant CLI tool. It's not just a "chatbot that writes code" but a complete **Agent Runtime System** that includes:

- **Tool calling system** - 43+ built-in tools with permission models
- **Context Engineering** - System prompts, memory management, auto-compaction
- **Multi-agent architecture** - Task coordination and agent orchestration
- **Extension system** - MCP protocol, Skills, and plugins
- **State management** - Message loops and streaming processing

## Installation

This is a learning resource, not an installable package. Clone the repository to study the design patterns:

```bash
git clone https://github.com/6551Team/claude-code-design-guide.git
cd claude-code-design-guide
```

## Key Architecture Concepts

### 1. Query Engine - The Heart of Agent Interaction

The query engine manages the core conversation loop:

```typescript
// Simplified query engine pattern
class QueryEngine {
  async processQuery(userMessage: string) {
    // 1. Build context from memory and system prompts
    const context = await this.buildContext(userMessage);
    
    // 2. Send to LLM with available tools
    const response = await this.llm.complete({
      messages: context,
      tools: this.getAvailableTools(),
      stream: true
    });
    
    // 3. Process tool calls if any
    if (response.toolCalls) {
      const results = await this.executeTools(response.toolCalls);
      return this.processQuery(results); // Recurse with tool results
    }
    
    return response;
  }
}
```

### 2. Tool System Design

Tools follow a standardized schema with permission controls:

```typescript
// Tool definition pattern
interface Tool {
  name: string;
  description: string;
  parameters: {
    type: "object";
    properties: Record<string, any>;
    required: string[];
  };
  permission: "always" | "ask" | "never";
  execute: (params: any) => Promise<any>;
}

// Example: File system tool
const readFileTool: Tool = {
  name: "read_file",
  description: "Read contents of a file",
  parameters: {
    type: "object",
    properties: {
      path: { type: "string", description: "File path to read" }
    },
    required: ["path"]
  },
  permission: "ask", // User must approve
  async execute({ path }) {
    return await fs.readFile(path, "utf-8");
  }
};
```

### 3. Context Engineering

Build effective system prompts and manage context:

```typescript
// System prompt construction
function buildSystemPrompt(config: AgentConfig): string {
  return `You are an AI programming assistant with these capabilities:

TOOLS AVAILABLE:
${config.tools.map(t => `- ${t.name}: ${t.description}`).join('\n')}

PROJECT CONTEXT:
${config.memory?.claudemd || 'No CLAUDE.md found'}

CURRENT TASK:
${config.currentTask || 'General assistance'}

GUIDELINES:
- Always use tools when you need to read files or execute commands
- Ask for permission before making destructive changes
- Keep context compact - summarize long conversations
- Focus on the user's current goal
`;
}

// Context compaction for long conversations
async function compactContext(messages: Message[]): Promise<Message[]> {
  if (messages.length < 50) return messages;
  
  // Keep first 5 messages (system setup)
  // Summarize middle messages
  // Keep last 20 messages (recent context)
  const summary = await summarizeMessages(messages.slice(5, -20));
  
  return [
    ...messages.slice(0, 5),
    { role: "system", content: `Previous conversation summary: ${summary}` },
    ...messages.slice(-20)
  ];
}
```

### 4. Multi-Agent Coordination

Implement coordinator pattern for complex tasks:

```typescript
// Multi-agent coordinator
class AgentCoordinator {
  private agents: Map<string, Agent> = new Map();
  
  async coordinateTask(task: Task) {
    // 1. Analyze task and determine required agents
    const plan = await this.planTask(task);
    
    // 2. Spawn specialized agents
    for (const step of plan.steps) {
      const agent = this.getOrCreateAgent(step.agentType);
      const result = await agent.execute(step);
      
      // 3. Share results with other agents via shared memory
      await this.updateSharedMemory(step.id, result);
    }
    
    // 4. Aggregate results
    return this.aggregateResults(plan);
  }
  
  private getOrCreateAgent(type: string): Agent {
    if (!this.agents.has(type)) {
      this.agents.set(type, new Agent({
        type,
        tools: this.getToolsForAgent(type),
        memory: this.sharedMemory
      }));
    }
    return this.agents.get(type)!;
  }
}
```

### 5. MCP Protocol - Tool Interoperability

The Model Context Protocol enables tool sharing across agents:

```typescript
// MCP server implementation
interface MCPServer {
  name: string;
  version: string;
  tools: Tool[];
  
  // Lifecycle hooks
  initialize(): Promise<void>;
  shutdown(): Promise<void>;
}

// Example MCP server for database operations
class DatabaseMCPServer implements MCPServer {
  name = "database-server";
  version = "1.0.0";
  
  tools = [
    {
      name: "query_db",
      description: "Execute SQL query",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string" },
          params: { type: "array" }
        },
        required: ["query"]
      },
      async execute({ query, params }) {
        return await db.query(query, params);
      }
    }
  ];
  
  async initialize() {
    await db.connect(process.env.DATABASE_URL);
  }
  
  async shutdown() {
    await db.disconnect();
  }
}
```

### 6. Permission Model

Implement layered permission controls:

```typescript
// Permission system
enum PermissionLevel {
  ALWAYS = "always",     // Execute without asking
  ASK = "ask",          // Ask user first
  NEVER = "never"       // Blocked
}

class PermissionManager {
  private rules: Map<string, PermissionLevel> = new Map();
  
  async checkPermission(
    toolName: string,
    params: any
  ): Promise<boolean> {
    const level = this.rules.get(toolName) || PermissionLevel.ASK;
    
    switch (level) {
      case PermissionLevel.ALWAYS:
        return true;
        
      case PermissionLevel.NEVER:
        return false;
        
      case PermissionLevel.ASK:
        // Check for dangerous operations
        if (this.isDangerous(toolName, params)) {
          return await this.promptUser(
            `Allow ${toolName} with ${JSON.stringify(params)}?`
          );
        }
        return true;
    }
  }
  
  private isDangerous(toolName: string, params: any): boolean {
    const dangerousPatterns = [
      { tool: "execute_command", check: (p: any) => p.command.includes("rm -rf") },
      { tool: "write_file", check: (p: any) => p.path.startsWith("/etc/") },
      { tool: "network_request", check: (p: any) => !p.url.startsWith("https://") }
    ];
    
    return dangerousPatterns.some(
      p => p.tool === toolName && p.check(params)
    );
  }
}
```

### 7. State Management

Handle conversation state and streaming:

```typescript
// Message loop with state management
class MessageLoop {
  private state: ConversationState = {
    messages: [],
    activeTools: [],
    memory: {}
  };
  
  async *processStream(userInput: string) {
    // Add user message to state
    this.state.messages.push({
      role: "user",
      content: userInput
    });
    
    // Stream LLM response
    const stream = await this.llm.streamComplete({
      messages: this.state.messages,
      tools: this.getAvailableTools()
    });
    
    let accumulatedResponse = "";
    
    for await (const chunk of stream) {
      if (chunk.type === "content") {
        accumulatedResponse += chunk.text;
        yield { type: "text", content: chunk.text };
      }
      
      if (chunk.type === "tool_call") {
        // Execute tool and continue stream
        const result = await this.executeTool(chunk.tool);
        yield { type: "tool_result", result };
        
        // Add to state for next iteration
        this.state.messages.push({
          role: "assistant",
          content: accumulatedResponse,
          toolCalls: [chunk.tool]
        });
        this.state.messages.push({
          role: "tool",
          content: result
        });
        
        // Continue conversation with tool result
        yield* this.processStream("");
      }
    }
    
    // Save final response
    this.state.messages.push({
      role: "assistant",
      content: accumulatedResponse
    });
  }
}
```

## Common Patterns

### Pattern 1: CLAUDE.md Memory System

Create a project memory file that agents can read:

```markdown
<!-- CLAUDE.md -->
# Project Context

## Architecture
- Next.js 14 app with TypeScript
- Tailwind CSS for styling
- Prisma + PostgreSQL database

## Conventions
- Use kebab-case for file names
- API routes in app/api/
- Components in components/ with .tsx extension

## Current Focus
Working on user authentication system.
Using next-auth with GitHub provider.
```

### Pattern 2: Task Decomposition

Break complex tasks into agent-manageable steps:

```typescript
async function decomposeTask(task: string): Promise<Step[]> {
  const decomposition = await llm.complete({
    messages: [{
      role: "system",
      content: "Break this task into concrete, tool-executable steps"
    }, {
      role: "user",
      content: task
    }]
  });
  
  return parseSteps(decomposition);
}

// Example usage
const steps = await decomposeTask(
  "Add authentication to the app"
);
// Returns:
// 1. Read current app structure
// 2. Install next-auth package
// 3. Create auth configuration file
// 4. Add API route for auth
// 5. Update middleware for protection
```

### Pattern 3: Tool Chaining

Chain tools together for complex operations:

```typescript
async function analyzeAndRefactor(filePath: string) {
  // 1. Read file
  const content = await tools.read_file({ path: filePath });
  
  // 2. Analyze code
  const analysis = await tools.analyze_code({ code: content });
  
  // 3. Generate refactoring plan
  const plan = await llm.complete({
    messages: [{
      role: "user",
      content: `Analyze this code and suggest refactoring:\n${analysis}`
    }]
  });
  
  // 4. Apply changes
  const newCode = await tools.apply_diff({
    path: filePath,
    changes: plan.changes
  });
  
  return newCode;
}
```

## Configuration

### Agent Configuration

```typescript
interface AgentConfig {
  // Model settings
  model: string;
  temperature: number;
  maxTokens: number;
  
  // Tools
  tools: Tool[];
  toolPermissions: Record<string, PermissionLevel>;
  
  // Context
  systemPrompt: string;
  memoryPath?: string; // Path to CLAUDE.md
  maxContextTokens: number;
  
  // Behavior
  autoCompact: boolean; // Auto-compress long contexts
  confirmDangerous: boolean; // Ask before dangerous operations
  
  // Multi-agent
  coordinatorMode?: boolean;
  agentTypes?: string[];
}

// Example configuration
const config: AgentConfig = {
  model: "claude-3-5-sonnet-20241022",
  temperature: 0.7,
  maxTokens: 4096,
  
  tools: [
    readFileTool,
    writeFileTool,
    executeCommandTool,
    searchCodeTool
  ],
  
  toolPermissions: {
    "read_file": PermissionLevel.ALWAYS,
    "write_file": PermissionLevel.ASK,
    "execute_command": PermissionLevel.ASK
  },
  
  systemPrompt: buildSystemPrompt({ /* ... */ }),
  memoryPath: "./CLAUDE.md",
  maxContextTokens: 100000,
  
  autoCompact: true,
  confirmDangerous: true
};
```

## Troubleshooting

### Issue: Context Window Exceeded

**Problem:** Agent hits token limit in long conversations.

**Solution:** Implement auto-compaction:

```typescript
// Monitor token usage
if (currentTokens > maxTokens * 0.8) {
  messages = await compactContext(messages);
}
```

### Issue: Tool Execution Failures

**Problem:** Tools fail or return errors.

**Solution:** Add retry logic and error handling:

```typescript
async function executeToolWithRetry(
  tool: Tool,
  params: any,
  maxRetries = 3
): Promise<any> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await tool.execute(params);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      // Let LLM fix the parameters
      const fixed = await llm.complete({
        messages: [{
          role: "user",
          content: `Tool ${tool.name} failed with: ${error.message}. Fix parameters: ${JSON.stringify(params)}`
        }]
      });
      
      params = JSON.parse(fixed);
    }
  }
}
```

### Issue: Permission Deadlocks

**Problem:** Agent gets stuck asking for permissions repeatedly.

**Solution:** Remember user preferences:

```typescript
class PermissionCache {
  private cache = new Map<string, boolean>();
  
  async check(tool: string, params: any): Promise<boolean> {
    const key = `${tool}:${JSON.stringify(params)}`;
    
    if (this.cache.has(key)) {
      return this.cache.get(key)!;
    }
    
    const allowed = await promptUser(`Allow ${tool}?`);
    this.cache.set(key, allowed);
    return allowed;
  }
}
```

### Issue: Multi-Agent Coordination Conflicts

**Problem:** Multiple agents modify the same files simultaneously.

**Solution:** Implement locking mechanism:

```typescript
class ResourceLock {
  private locks = new Map<string, string>(); // resource -> agentId
  
  async acquire(resource: string, agentId: string): Promise<boolean> {
    if (this.locks.has(resource)) {
      return false; // Already locked
    }
    
    this.locks.set(resource, agentId);
    return true;
  }
  
  release(resource: string, agentId: string) {
    if (this.locks.get(resource) === agentId) {
      this.locks.delete(resource);
    }
  }
}
```

## Key Takeaways

1. **Agent Runtime**: Build complete systems, not just chatbots
2. **Tool Design**: Create focused, composable tools with clear permissions
3. **Context Engineering**: Manage memory, prompts, and compaction strategically
4. **Multi-Agent**: Coordinate specialized agents for complex tasks
5. **Extensibility**: Use MCP protocol for tool sharing and interoperability
6. **Safety**: Always implement permission models and dangerous operation checks

This guide is based on the open-source analysis of Claude Code's architecture. Study the full documentation at https://github.com/6551Team/claude-code-design-guide for deeper implementation details.
