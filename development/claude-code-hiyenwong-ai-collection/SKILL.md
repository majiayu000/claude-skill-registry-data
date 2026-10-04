---
name: claude-code
version: v2.1.84
last_updated: 2026-03-27
description: Anthropic's official AI-powered coding companion. Use when user wants to run claude-code CLI, needs help with code using Anthropic's Claude, or mentions claude-code, anthropic coding, claude cli, or claude terminal.
platforms: [claude-code, codex, hermes, opencode, openclaw]
---

# Claude Code

## Description
Anthropic's official AI-powered coding companion. A command-line tool that integrates with your Claude subscription and helps you write, debug, and understand code with natural language commands.

## Version Status

**Skill Version:** v2.1.84 (2026-03-27)
**Latest Release:** [Check GitHub](https://github.com/anthropics/claude-code/releases/latest)

### Version Check
When user activates this skill, check their installed version:
```bash
claude --version
```

**If version differs from skill version (v2.1.84):**
- ⚠️ If older: Suggest updating with `npm update -g @anthropic-ai/claude-code`
- ℹ️ If newer: Note that skill may need updating to reflect new features

### Update Prompt Template
```
⚠️ Your Claude Code version ({installed_version}) differs from this skill's documented version (v2.1.84).

{installed_version < v2.1.84}:
  建议更新: npm update -g @anthropic-ai/claude-code
  新功能包括: PowerShell Tool、Transcript Search、TaskCreated Hook 等

{installed_version > v2.1.84}:
  您的版本更新，本技能文档可能需要更新以反映新功能。
```

## Activation Keywords
- claude-code
- claude code
- @anthropic
- anthropic coding
- claude cli
- claude terminal
- claude --allow-dangerously-skip-permissions
- claude --enable-auto-mode

## Tools Used
- exec: Run claude-code CLI
- read: Read code files
- write: Write code files
- edit: Edit code files
- process: Manage long-running sessions

## Installation

### Install via npm
```bash
npm install -g @anthropic-ai/claude-code
```

### Verify Installation
```bash
claude --version
```

### Authentication
```bash
claude auth
```
Follow the instructions to sign in with your Claude account.

### Quick Start
```bash
# Navigate to your project
cd /path/to/project

# Start Claude Code
claude
```

## Usage Patterns

### Reading and Understanding Code

**Explain specific file:**
```
Explain how the authentication middleware works in src/middleware/auth.ts
```

**Understand project structure:**
```
Give me an overview of this project's architecture
```

**Explain complex logic:**
```
Walk me through the algorithm in src/utils/data-processing.js
```

### Writing Code

**Create new feature:**
```
Add error handling to the user authentication function in src/auth.js
```

**Implement specific functionality:**
```
Create a REST API endpoint for getting user profile
```

**Generate boilerplate:**
```
Create a React component for a user profile card with TypeScript
```

### Debugging

**Debug an error:**
```
I'm getting a 500 error when calling /api/users. Help me debug it.
```

**Fix a bug:**
```
The login form isn't submitting. Find and fix the issue.
```

**Investigate unexpected behavior:**
```
The data isn't rendering correctly in the dashboard. Help me troubleshoot.
```

### Refactoring

**Refactor code:**
```
Refactor the database connection logic to use a connection pool
```

**Improve code quality:**
```
Review and improve the code in src/services/api.ts
```

**Apply patterns:**
```
Refactor the authentication logic to follow the pattern used in src/middleware/auth.ts
```

### Testing

**Generate tests:**
```
Generate unit tests for the user service in src/services/user.service.ts
```

**Run tests:**
```
Run the test suite and fix any failing tests
```

**Debug test failures:**
```
The user login test is failing. Help me fix it.
```

## Instructions for Agents

When user mentions Claude Code or related tasks:

### 1. Verify Installation
Check if claude-code is installed:
```bash
claude-code --version
```

If not installed, guide user through:
```bash
npm install -g @anthropic-ai/claude-code
claude-code auth
```

### 2. Navigate to Project
Always work in the project directory:
```bash
cd /path/to/project
```

### 3. Start Claude Code
Start a session:
```bash
claude-code
```

For long-running tasks, consider using background mode:
```bash
claude-code &
```

### 4. Use Natural Language Commands
Claude Code understands natural language. Be specific:
- "What" questions: "What does this function do?"
- "How" questions: "How do I add error handling?"
- Action requests: "Add X to Y"
- Debugging: "Why is this happening?"

### 5. Iterate and Refine
Claude Code learns from context:
- Ask follow-up questions
- Provide feedback on results
- Request changes or alternatives

### 6. Manage Context
Claude Code maintains context:
- Mention relevant files
- Reference previous work
- Describe project structure

## Context Files

Claude Code automatically reads these when available:

### README.md
Project overview and setup instructions

### package.json
Dependencies and scripts

### tsconfig.json / jsconfig.json
TypeScript/JavaScript configuration

### AGENTS.md
Agent instructions (OpenCode format, also works)

### .clauderc / claude.json
Claude Code project configuration

## Configuration

### Project Config (.clauderc or claude.json)
```json
{
  "model": "claude-sonnet-4.5",
  "maxTokens": 200000,
  "temperature": 0.3,
  "tools": ["file_operations", "git", "testing"],
  "skills": ["typescript", "react"],
  "hooks": {
    "preToolUse": "hooks/pre-tool-use.js",
    "postToolUse": "hooks/post-tool-use.js"
  }
}
```

### Environment Variables
```bash
# Set default model
export CLAUDE_MODEL="claude-sonnet-4.5"

# Set API key (alternative to auth)
export ANTHROPIC_API_KEY="your-api-key"
```

## Advanced Features

### 🆕 Latest Features (v2.1.84, 2026-03-26)

#### PowerShell Tool (Windows Preview)
Windows 用户可以使用 PowerShell 工具：
```bash
# 在 managed-settings.json 中启用
{
  "tools": {
    "bash": true,
    "powershell": true  // 预览功能
  }
}
```

#### Transcript Search (历史搜索)
在会话历史中搜索：
- 按 `Ctrl+O` 进入 transcript mode
- 按 `/` 开始搜索
- 按 `n/N` 浏览匹配项

#### Environment Variables (新环境变量)
```bash
# 自定义模型支持检测
ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTS=1
ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTS=1
ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTS=1

# 流式空闲超时（默认 90s）
CLAUDE_STREAM_IDLE_TIMEOUT_MS=90000

# 清理子进程环境变量中的敏感信息
CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1
```

#### New Hooks
- **TaskCreated**: 任务创建时触发
- **WorktreeCreate**: 支持 HTTP 类型
- **CwdChanged**: 工作目录改变时触发
- **FileChanged**: 文件改变时触发

#### Idle-Return Prompt
75 分钟无操作后，系统会提示使用 `/clear` 清理上下文，减少不必要的 token 重新缓存。

#### Deep Links 改进
`claude-cli://` 链接现在会在首选终端中打开，而不是随机选择。

#### Managed Settings 增强
```bash
# drop-in 目录支持
~/.claude/managed-settings.d/
```
多个团队可以独立部署策略片段，按字母顺序合并。

### /loop Command (v2.1.71+)
Run a prompt or slash command on a recurring interval:

```bash
# Check deployment every 5 minutes
/loop 5m check the deploy status

# Run tests every 30 seconds
/loop 30s run the test suite

# Monitor logs every minute
/loop 1m show recent error logs
```

**Interval formats:**
- `30s` - 30 seconds
- `5m` - 5 minutes
- `1h` - 1 hour

### Cron Scheduling (New in v2.1.71)
Schedule recurring prompts within a session:

```javascript
// In claude.json or .clauderc
{
  "cron": {
    "jobs": [
      {
        "schedule": "0 9 * * *",  // Every day at 9 AM
        "prompt": "Check for outdated dependencies"
      },
      {
        "schedule": "0 */6 * * *",  // Every 6 hours
        "prompt": "Run the test suite and report failures"
      }
    ]
  }
}
```

### Voice Push-to-Talk Keybinding (New in v2.1.71)
Rebindable voice activation key in `keybindings.json`:

```json
{
  "voice": {
    "pushToTalk": "space"  // Default: space
  }
}
```

**Note:** Modifier+letter combos like `meta+k` have zero typing interference.

### MCP (Model Context Protocol)
Extend Claude Code with MCPs:

**Tool MCP:**
```json
{
  "name": "my-tool",
  "type": "tool",
  "path": "./mcp/tools/my-tool.js"
}
```

**Resource MCP:**
```json
{
  "name": "my-resource",
  "type": "resource",
  "path": "./mcp/resources/my-resource.js"
}
```

**Prompt MCP:**
```json
{
  "name": "my-prompt",
  "type": "prompt",
  "path": "./mcp/prompts/my-prompt.js"
}
```

### Hooks System
Extend behavior with hooks:

**PreToolUse:** Before tool execution
**PostToolUse:** After tool execution
**UserPromptSubmit:** Before sending user message
**Stop:** On session termination

### Skills
Create reusable skills for common tasks:

**Command skill:**
```javascript
// skills/create-component.js
module.exports = {
  name: "create-component",
  description: "Create a React component",
  execute: (context) => {
    // Component generation logic
  }
};
```

### Agents
Specialized agents for different tasks:

**Coding agent:** Write and implement code
**Review agent:** Review code quality
**Testing agent:** Generate and run tests

## Common Commands

### File Operations
- `@file.txt` - Read specific file
- "Create file X" - Create new file
- "Delete file X" - Remove file
- "Move file X to Y" - Move/rename file

### Git Operations
- "Create a commit" - Commit changes
- "Review changes" - Show git diff
- "Create a branch" - Create new branch
- "Merge X into Y" - Merge branches

### Testing
- "Run tests" - Execute test suite
- "Generate tests for X" - Create tests
- "Debug failing tests" - Fix test failures

### Build Process
- "Build the project" - Run build command
- "Fix build errors" - Resolve build issues

## Error Handling

### Authentication Issues
```
If you see "Not authenticated":
  1. Run: claude-code auth
  2. Follow browser authentication
  3. Retry your request
```

### API Errors
```
If you see API rate limit errors:
  1. Wait a moment and retry
  2. Reduce request frequency
  3. Consider using a different model
```

### Context Limit
```
If you see context limit errors:
  1. Ask Claude to summarize current context
  2. Focus on specific files
  3. Reduce prompt complexity
```

### Installation Issues
```
If claude-code won't install:
  1. Check Node.js version (requires Node 16+)
  2. Clear npm cache: npm cache clean --force
  3. Try with verbose: npm install -g @anthropic-ai/claude-code --verbose
```

## Best Practices

### 1. Be Specific
Clear, specific requests get better results:
- ✅ "Add error handling to the login function"
- ❌ "Make the code better"

### 2. Provide Context
Give Claude context about your code:
- Mention the programming language
- Reference related files
- Describe the project structure

### 3. Iterate Effectively
- Start with a simple request
- Review and provide feedback
- Ask for changes or improvements

### 4. Use Files
- Use @ to reference specific files
- Let Claude read code naturally
- Don't paste large code blocks

### 5. Review Before Committing
- Test generated code
- Review for security issues
- Check edge cases

## Examples

### Example 1: Adding a Feature

**User:** Add error handling to the user authentication function in src/auth.js

**Agent:**
1. Reads src/auth.js
2. Identifies the authentication function
3. Adds try-catch blocks with logging
4. Adds user-friendly error messages
5. Suggests testing approach

Result: Updated src/auth.js with comprehensive error handling

### Example 2: Debugging

**User:** I'm getting a 500 error when calling /api/users. Help me debug it.

**Agent:**
1. Reads the API endpoint code
2. Checks database queries and error logs
3. Identifies missing error handling
4. Adds proper error handling and logging

Result: Fixed API endpoint with proper error handling

### Example 3: Understanding Code

**User:** Explain how the middleware chain works in server.js

**Agent:**
1. Reads server.js
2. Identifies middleware functions and execution order
3. Describes what each middleware does
4. Provides examples of adding new middleware

Result: Clear explanation of middleware architecture with examples

## Limitations

- Requires active Claude subscription for full access
- Model choice is limited to Claude models
- Context window depends on model (up to 200K tokens for Opus)
- Some advanced features may require additional setup

## Resources

- **Official Docs:** https://platform.claude.com/docs
- **Pricing:** https://claude.com/pricing
- **Claude Website:** https://claude.com
- **GitHub:** https://github.com/anthropics/claude-code

## Related Skills
- **coding-agent:** Generic coding agent with multiple tool support
- **opencode:** Open source coding agent with plugin system
- **obsidian:** For documentation and note-taking in code projects

## OpenClaw AI Collection Integration

Claude Code works seamlessly with the **OpenClaw AI Collection** - a curated set of specialized agents and skills that extend your coding capabilities with domain expertise and specialized workflows.

### Available Agents for Enhanced Coding

| Agent | Specialization | When to Invoke |
|-------|----------------|----------------|
| **fullstack-engineer** | Senior full-stack development | "使用 fullstack-engineer 构建完整应用" |
| **algorithm-engineer** | Algorithms & ML | "Use algorithm-engineer for this optimization" |
| **tech-cofounder** | Product & MVP building | "Use tech-cofounder for rapid prototyping" |
| **stock-analyst** | Financial data & trading | "Use stock-analyst for trading algorithms" |
| **research-agent** | Deep research & documentation | "Use research-agent for technical documentation" |

### Complementary Skills

| Skill | Purpose | Activation Keywords |
|-------|---------|-------------------|
| **openspec** | Spec-driven development | openspec, gherkin, BDD |
| **skill-extractor** | Create skills from patterns | 提炼技能, extract skill |
| **skill-rag-indexer** | Semantic skill search | 搜索技能, skill search |
| **stock-analysis** | Technical indicators | 股票分析, MACD, KDJ |

### Using AI Collection with Claude Code

#### Method 1: Agent Context

Create a `.claude/AGENTS.md` file to inject agent expertise:

```markdown
# Default Agent Configuration

For specialized tasks, reference these agents:

## Fullstack Engineer
Location: /path/to/collection/agents/fullstack-engineer/
Use for: Complete web applications, architecture design

## Algorithm Engineer
Location: /path/to/collection/agents/algorithm-engineer/
Use for: Complex algorithms, optimization, ML models

## Tech Co-Founder
Location: /path/to/collection/agents/tech-cofounder/
Use for: MVP development, product planning

## Research Agent
Location: /path/to/collection/agents/research-agent/
Use for: Documentation, research, technical investigation
```

#### Method 2: Direct Invocation

```
Use the fullstack-engineer approach to build this React application with TypeScript, Tailwind, and Supabase.
```

Claude Code will incorporate the agent's methodology and best practices.

#### Method 3: Skill Combination

```
First use openspec to define the requirements in Gherkin syntax, then implement them using testing best practices.
```

Combines spec-driven development with TDD methodology.

### Example Workflows

#### Full-Stack Development
```
Use fullstack-engineer to build a task management SaaS with:
- React + TypeScript frontend
- Node.js + Express backend
- PostgreSQL database
- JWT authentication
- Real-time updates with Socket.io
```

#### Algorithm Optimization
```
Use algorithm-engineer to optimize the sorting algorithm in src/utils/sort.js:
- Analyze current complexity
- Propose O(n log n) alternative
- Implement with proper testing
- Benchmark improvements
```

#### Product Building
```
Use tech-cofounder to rapidly build an MVP for:
- AI writing assistant
- 2-week timeline
- Claude API integration
- Supabase backend
- Deploy on Vercel
```

#### Documentation Generation
```
Use research-agent to create comprehensive documentation for the API:
- Endpoint descriptions
- Authentication flow
- Rate limiting info
- Code examples
- Error handling
```

### Quick Reference Commands

| Task | Command |
|------|---------|
| **Full-stack app** | "Use fullstack-engineer approach" |
| **Algorithm work** | "Use algorithm-engineer optimization" |
| **MVP development** | "Use tech-cofounder rapid build" |
| **Documentation** | "Use research-agent investigation" |
| **Stock/finance** | "Use stock-analyst data analysis" |
| **Spec definition** | "Use openspec gherkin syntax" |
| **Skill creation** | "Use skill-extractor to extract skill" |

### Installation Path

The OpenClaw AI Collection is available at:
- **GitHub:** https://github.com/hiyenwong/ai_collection
- **Local:** `/path/to/ai_collection`

To use with Claude Code:
1. Ensure collection is accessible locally
2. Reference agents/skills in your prompts
3. Or create `.claude/AGENTS.md` with agent references
4. Use activation keywords to trigger specialized behavior

### Benefits of Integration

- **Domain Expertise**: Specialized knowledge for specific fields
- **Proven Methodologies**: Battle-tested workflows and best practices
- **Efficiency**: Skip trial-and-error, use proven approaches
- **Consistency**: Standardized code quality and patterns
- **Extensibility**: Easy to add new specialized capabilities

---

*For more information, see the [AI Collection README](https://github.com/hiyenwong/ai_collection)*

## Notes

- Claude Code uses your existing Claude subscription
- Usage counts towards your Claude API limits
- Best for users primarily using Claude models
- Integrates seamlessly with Claude's other tools and services
