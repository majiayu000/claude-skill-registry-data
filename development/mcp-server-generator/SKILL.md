---
name: mcp-server-generator
description: Generate complete, production-ready MCP (Model Context Protocol) servers with automatic setup, configuration, and Claude Code integration
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# MCP Server Generator

Expert skill for generating complete, production-ready MCP (Model Context Protocol) servers. Specializes in automated server generation, setup, configuration, and seamless integration with Claude Code.

## Core Capabilities

### 1. Complete Server Generation
- Full TypeScript MCP server with all boilerplate
- Tool implementations (not just templates)
- Type-safe interfaces and schemas
- Error handling and validation
- Logging and debugging support
- Production-ready code quality

### 2. Automatic Setup & Installation
- Generate server code
- Install dependencies (npm/pnpm/yarn)
- Build TypeScript project
- Configure Claude Code integration
- Test server connection
- Start server automatically

### 3. Tool Categories Support
- **Browser Automation**: Playwright, Puppeteer
- **Testing**: Visual regression, E2E, accessibility
- **Development**: Live preview, hot reload, DevTools
- **Performance**: Profiling, metrics, Core Web Vitals
- **Utilities**: File operations, data processing, API calls
- **Custom**: Any tool category you need

### 4. Smart Configuration
- **Zero Config**: Works out of the box with sensible defaults
- **Auto-Detection**: Detects project type, framework, tools
- **Optional Override**: JSON/TypeScript config for customization
- **Environment Variables**: Support for secrets and configuration
- **Multiple Profiles**: Dev, staging, production configs

### 5. Claude Code Integration
- Automatic `.claude/config.json` configuration
- Server registration and startup
- Health check and monitoring
- Automatic restart on failure
- Logging to Claude Code console

### 6. Template Library
- Pre-built server templates for common use cases
- UI Testing Server (Playwright + visual regression)
- API Testing Server (HTTP client + validation)
- File Processing Server (read/write/transform)
- Web Scraping Server (browser automation + parsing)
- Custom template creation

## Workflow

### Phase 1: Analysis & Planning
1. **Understand Requirements**
   - What tools does the server need to provide?
   - What technologies to use? (Playwright, Puppeteer, etc.)
   - Integration requirements (APIs, databases, etc.)
   - Performance and scalability needs

2. **Select Template**
   - Use pre-built template if available
   - Identify closest template and customize
   - Create from scratch if needed

3. **Plan Architecture**
   - Tool organization (categories, naming)
   - Configuration strategy (zero-config vs explicit)
   - Dependencies and external services
   - Error handling approach

### Phase 2: Generation
1. **Generate Server Structure**
   - Create directory structure
   - Generate package.json with dependencies
   - Create tsconfig.json for TypeScript
   - Set up build scripts

2. **Implement Tools**
   - Generate tool implementations
   - Add input validation and schemas
   - Implement error handling
   - Add logging and debugging

3. **Create Configuration**
   - Auto-detection logic
   - Default configuration
   - Override mechanism
   - Environment variable support

4. **Add Documentation**
   - README with setup instructions
   - Tool documentation (inputs, outputs, examples)
   - Troubleshooting guide
   - API reference

### Phase 3: Setup & Integration
1. **Install & Build**
   - Run npm install
   - Compile TypeScript
   - Run tests (if present)
   - Verify build output

2. **Configure Claude Code**
   - Add server to `.claude/config.json`
   - Set up environment variables
   - Configure auto-start
   - Set up logging

3. **Test & Verify**
   - Start server
   - Test connection
   - Verify tool registration
   - Run sample tool calls
   - Check error handling

4. **Documentation & Handoff**
   - Generate usage examples
   - Document configuration options
   - Provide troubleshooting steps
   - Create quick start guide

## MCP Server Architecture

### Standard Structure
```
mcp-server-name/
├── package.json              # Dependencies and scripts
├── tsconfig.json             # TypeScript configuration
├── .env.example              # Environment variables template
├── src/
│   ├── index.ts             # Server entry point
│   ├── config/
│   │   ├── auto-detect.ts   # Auto-detection logic
│   │   ├── defaults.ts      # Default configuration
│   │   └── schema.ts        # Config validation schema
│   ├── tools/
│   │   ├── category1/
│   │   │   ├── tool1.ts     # Tool implementation
│   │   │   └── tool2.ts
│   │   └── category2/
│   │       └── tool3.ts
│   ├── utils/
│   │   ├── logger.ts        # Logging utility
│   │   ├── errors.ts        # Error handling
│   │   └── validation.ts    # Input validation
│   └── types/
│       └── index.ts         # TypeScript types
├── scripts/
│   ├── setup.sh             # Setup automation
│   └── configure-claude.sh  # Claude Code config
├── tests/
│   └── server.test.ts       # Server tests
└── README.md                # Documentation
```

### Server Entry Point Template
```typescript
// src/index.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js'

import { loadConfig } from './config/auto-detect.js'
import { registerTools } from './tools/index.js'
import { logger } from './utils/logger.js'

const server = new Server(
  {
    name: 'mcp-server-name',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
)

// Load configuration
const config = await loadConfig()
logger.info('Configuration loaded', config)

// Register all tools
const tools = registerTools(config)
logger.info(`Registered ${tools.length} tools`)

// Handle tool list request
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: tools.map(tool => ({
    name: tool.name,
    description: tool.description,
    inputSchema: tool.inputSchema,
  })),
}))

// Handle tool execution request
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const tool = tools.find(t => t.name === request.params.name)

  if (!tool) {
    throw new Error(`Tool not found: ${request.params.name}`)
  }

  logger.info(`Executing tool: ${tool.name}`, request.params.arguments)

  try {
    const result = await tool.execute(request.params.arguments)
    logger.info(`Tool completed: ${tool.name}`)
    return result
  } catch (error) {
    logger.error(`Tool failed: ${tool.name}`, error)
    throw error
  }
})

// Start server
const transport = new StdioServerTransport()
await server.connect(transport)
logger.info('MCP Server started')
```

### Tool Implementation Template
```typescript
// src/tools/category/example-tool.ts
import { z } from 'zod'
import { Tool } from '../../types/index.js'

// Input validation schema
const inputSchema = z.object({
  param1: z.string().describe('Description of param1'),
  param2: z.number().optional().describe('Optional param2'),
  options: z.object({
    option1: z.boolean().default(true),
  }).optional(),
})

export const exampleTool: Tool = {
  name: 'example_tool',
  description: 'Does something useful',

  inputSchema: {
    type: 'object',
    properties: {
      param1: { type: 'string', description: 'Description of param1' },
      param2: { type: 'number', description: 'Optional param2' },
      options: {
        type: 'object',
        properties: {
          option1: { type: 'boolean', default: true },
        },
      },
    },
    required: ['param1'],
  },

  async execute(args: unknown) {
    // Validate input
    const params = inputSchema.parse(args)

    // Implement tool logic
    try {
      const result = await doSomething(params)

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2),
          },
        ],
      }
    } catch (error) {
      throw new Error(`Tool execution failed: ${error.message}`)
    }
  },
}

async function doSomething(params: z.infer<typeof inputSchema>) {
  // Implementation here
  return { success: true, data: params }
}
```

### Auto-Detection Example
```typescript
// src/config/auto-detect.ts
import { existsSync, readFileSync } from 'fs'
import { join } from 'path'

export async function loadConfig() {
  const cwd = process.cwd()

  // Detect package.json
  const packageJsonPath = join(cwd, 'package.json')
  const packageJson = existsSync(packageJsonPath)
    ? JSON.parse(readFileSync(packageJsonPath, 'utf-8'))
    : {}

  // Detect framework
  const framework = detectFramework(packageJson)

  // Detect test runner
  const testRunner = detectTestRunner(packageJson)

  // Detect available ports
  const port = await findAvailablePort(3000)

  // Load user config (if exists)
  const userConfig = loadUserConfig()

  // Merge with defaults
  return {
    port,
    framework,
    testRunner,
    ...getDefaults(),
    ...userConfig,
  }
}

function detectFramework(packageJson: any): string {
  if (packageJson.dependencies?.react) return 'react'
  if (packageJson.dependencies?.vue) return 'vue'
  if (packageJson.dependencies?.svelte) return 'svelte'
  return 'unknown'
}

function detectTestRunner(packageJson: any): string {
  if (packageJson.devDependencies?.vitest) return 'vitest'
  if (packageJson.devDependencies?.jest) return 'jest'
  return 'unknown'
}

function loadUserConfig() {
  // Try .claude/mcp-config.json
  const configPath = join(process.cwd(), '.claude', 'mcp-config.json')
  if (existsSync(configPath)) {
    return JSON.parse(readFileSync(configPath, 'utf-8'))
  }

  // Try package.json mcp-server field
  const packageJsonPath = join(process.cwd(), 'package.json')
  if (existsSync(packageJsonPath)) {
    const pkg = JSON.parse(readFileSync(packageJsonPath, 'utf-8'))
    if (pkg['mcp-server']) {
      return pkg['mcp-server']
    }
  }

  return {}
}
```

## Claude Code Integration

### Configuration File
```json
// .claude/config.json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["./path/to/server/dist/index.js"],
      "env": {
        "NODE_ENV": "development",
        "LOG_LEVEL": "info"
      },
      "autoStart": true
    }
  }
}
```

### Setup Script
```bash
#!/bin/bash
# scripts/setup.sh

set -e

echo "🚀 Setting up MCP Server..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build TypeScript
echo "🔨 Building server..."
npm run build

# Configure Claude Code
echo "⚙️  Configuring Claude Code..."
./scripts/configure-claude.sh

# Test server
echo "🧪 Testing server..."
node dist/index.js --test

echo "✅ Setup complete!"
echo "Server is ready to use."
```

### Configure Claude Script
```bash
#!/bin/bash
# scripts/configure-claude.sh

CLAUDE_CONFIG=".claude/config.json"
SERVER_NAME="$1"
SERVER_PATH="$(pwd)/dist/index.js"

# Create .claude directory if not exists
mkdir -p .claude

# Add server to config
if [ -f "$CLAUDE_CONFIG" ]; then
  # Update existing config
  jq ".mcpServers[\"$SERVER_NAME\"] = {
    \"command\": \"node\",
    \"args\": [\"$SERVER_PATH\"],
    \"autoStart\": true
  }" "$CLAUDE_CONFIG" > "$CLAUDE_CONFIG.tmp"
  mv "$CLAUDE_CONFIG.tmp" "$CLAUDE_CONFIG"
else
  # Create new config
  cat > "$CLAUDE_CONFIG" << EOF
{
  "mcpServers": {
    "$SERVER_NAME": {
      "command": "node",
      "args": ["$SERVER_PATH"],
      "autoStart": true
    }
  }
}
EOF
fi

echo "✅ Claude Code configured"
```

## Pre-built Templates

### UI Testing Server
Complete server for UI component testing with:
- Visual regression (screenshot, compare, baseline)
- E2E testing (navigate, click, type, forms)
- Component preview (live server, hot reload)
- Performance monitoring (render time, Core Web Vitals)
- Accessibility auditing (WCAG, keyboard nav, ARIA)

**Location:** `templates/ui-testing-server/`

### API Testing Server
Server for API testing and validation with:
- HTTP client (GET, POST, PUT, DELETE, etc.)
- Request validation (schema, headers, auth)
- Response assertion (status, body, headers)
- Mock server setup
- Load testing support

### File Processing Server
Server for file operations with:
- Read/write operations
- Format conversion (JSON, CSV, YAML, XML)
- Data transformation
- Archive operations (zip, tar)
- File watching

### Web Scraping Server
Server for web scraping with:
- Page navigation and rendering
- Element selection and extraction
- Data parsing and cleaning
- Pagination handling
- Anti-bot bypass techniques

## Best Practices

### Server Design
1. **Single Responsibility**: One server, one domain
2. **Tool Granularity**: Fine-grained tools over monolithic ones
3. **Input Validation**: Always validate and sanitize inputs
4. **Error Handling**: Descriptive errors with context
5. **Logging**: Comprehensive logging for debugging

### Configuration
1. **Zero Config First**: Work without configuration
2. **Smart Defaults**: Sensible defaults for common cases
3. **Easy Override**: Simple config file structure
4. **Env Variables**: Support for secrets and sensitive data
5. **Validation**: Validate configuration at startup

### Performance
1. **Lazy Loading**: Load dependencies only when needed
2. **Resource Pooling**: Reuse expensive resources (browsers, connections)
3. **Timeouts**: Set reasonable timeouts for all operations
4. **Cleanup**: Properly dispose resources after use
5. **Caching**: Cache when appropriate

### Security
1. **Input Sanitization**: Never trust user input
2. **File System Access**: Restrict to safe directories
3. **Network Calls**: Validate URLs and domains
4. **Secrets**: Use environment variables, never hardcode
5. **Error Messages**: Don't leak sensitive information

## Tool Naming Conventions

### Naming Rules
- Use `snake_case` for tool names
- Start with verb (action): `create_`, `get_`, `update_`, `delete_`
- Be specific and descriptive
- Group related tools with prefixes

### Examples
```typescript
// Good
'screenshot_component'
'navigate_to_url'
'audit_accessibility'
'measure_performance'
'compare_visual_diff'

// Bad (too vague)
'take_pic'
'go'
'check'
'test'
```

### Category Prefixes
```typescript
// Visual
'visual_screenshot'
'visual_compare'
'visual_baseline'

// Performance
'perf_measure'
'perf_profile'
'perf_trace'

// Accessibility
'a11y_audit'
'a11y_check_wcag'
'a11y_keyboard_nav'
```

## Troubleshooting

### Common Issues

**Server Won't Start**
```bash
# Check Node version (requires 18+)
node --version

# Check dependencies
npm install

# Rebuild
npm run build

# Check logs
tail -f .claude/logs/mcp-server-name.log
```

**Tool Not Found**
```typescript
// Verify tool registration
server.setRequestHandler(ListToolsRequestSchema, async () => {
  console.log('Registered tools:', tools.map(t => t.name))
  return { tools }
})
```

**Connection Issues**
```bash
# Test server manually
echo '{"jsonrpc":"2.0","method":"initialize","id":1}' | node dist/index.js

# Check Claude Code config
cat .claude/config.json
```

**Performance Issues**
```typescript
// Add timeouts
const result = await Promise.race([
  tool.execute(args),
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Timeout')), 30000)
  )
])

// Profile execution
console.time('tool-execution')
const result = await tool.execute(args)
console.timeEnd('tool-execution')
```

## When to Use This Skill

Activate this skill when you need to:
- Generate a new MCP server from scratch
- Create custom tools for Claude Code
- Automate server setup and configuration
- Integrate external services with Claude Code
- Build browser automation tools
- Create testing infrastructure
- Implement file processing pipelines
- Set up web scraping capabilities
- Extend Claude Code with new capabilities

## Output Format

When generating MCP servers, provide:
1. **Complete Server Code**: Production-ready, type-safe implementation
2. **Configuration Files**: package.json, tsconfig.json, config templates
3. **Setup Scripts**: Automated installation and configuration
4. **Documentation**: README, tool docs, troubleshooting guide
5. **Usage Examples**: How to use each tool
6. **Integration Guide**: How to add to Claude Code

Always generate complete, working code that can be installed and used immediately with minimal configuration.
