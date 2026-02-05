---
name: cloud-sandbox
description: E2B sandbox deployment and management in Flow Nexus cloud. Use for creating isolated execution environments, running code safely, and managing development workflows.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - sandbox_creation
  - code_execution
  - file_management
  - environment_configuration
  - lifecycle_management
  - resource_monitoring
tools:
  - mcp__flow-nexus__sandbox_create
  - mcp__flow-nexus__sandbox_execute
  - mcp__flow-nexus__sandbox_list
  - mcp__flow-nexus__sandbox_stop
  - mcp__flow-nexus__sandbox_delete
  - mcp__flow-nexus__sandbox_status
  - mcp__flow-nexus__sandbox_upload
  - mcp__flow-nexus__sandbox_logs
  - mcp__flow-nexus__sandbox_configure
  - mcp__flow-nexus__template_list
  - mcp__flow-nexus__template_get
  - mcp__flow-nexus__template_deploy
related_skills:
  - cloud-swarm
  - cloud-workflow
  - cloud-neural
---

# Cloud Sandbox

> Create, configure, and manage isolated E2B execution environments for secure code development and testing.

## Quick Start

```javascript
// Create a Node.js sandbox
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "node",
  name: "dev-environment",
  env_vars: { NODE_ENV: "development" },
  install_packages: ["express", "lodash"],
  timeout: 3600
});

// Execute code
const result = await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: "console.log('Hello from sandbox!');",
  language: "javascript"
});
```

## When to Use

- Running untrusted or experimental code in isolation
- Testing code changes before production deployment
- Creating reproducible development environments
- Executing CI/CD pipeline steps safely
- Prototyping with different language runtimes
- Running code with specific package dependencies

## Prerequisites

- Flow Nexus account with active session
- MCP server `flow-nexus` configured
- Sufficient rUv credits for sandbox usage

## Core Concepts

### Sandbox Templates

| Template | Description | Runtime |
|----------|-------------|---------|
| `node` | Node.js with npm | Node.js LTS |
| `python` | Python 3.x with pip | Python 3.x |
| `react` | React development | Node.js + React |
| `nextjs` | Full-stack Next.js | Node.js + Next.js |
| `vanilla` | Basic HTML/CSS/JS | Browser environment |
| `base` | Minimal Linux | Custom setup |
| `claude-code` | Claude Code integration | Node.js + Anthropic |

### Lifecycle States

- **running**: Sandbox active and accepting commands
- **stopped**: Sandbox paused, can be resumed
- **terminated**: Sandbox removed, resources freed

## MCP Tools Reference

### Sandbox Creation

```javascript
mcp__flow-nexus__sandbox_create({
  template: "node",              // node, python, react, nextjs, vanilla, base, claude-code
  name: "my-sandbox",            // Optional custom name
  env_vars: {                    // Environment variables
    API_KEY: "key",
    NODE_ENV: "development"
  },
  install_packages: ["express", "lodash"],  // Packages to install
  startup_script: "npm run setup",           // Script to run on creation
  timeout: 3600,                 // Timeout in seconds (default: 3600)
  metadata: { project: "demo" }, // Additional metadata
  anthropic_key: "key"           // For claude-code template
})
// Returns: { sandbox_id, status, template, created_at }
```

### Code Execution

```javascript
mcp__flow-nexus__sandbox_execute({
  sandbox_id: "sandbox_id",
  code: "console.log('Hello');",  // Code to execute
  language: "javascript",          // Programming language
  capture_output: true,            // Capture stdout/stderr (default: true)
  timeout: 60,                     // Execution timeout in seconds
  working_dir: "/app",             // Working directory
  env_vars: { DEBUG: "true" }      // Execution-specific env vars
})
// Returns: { output, error, exit_code, execution_time }
```

### File Operations

```javascript
// Upload file to sandbox
mcp__flow-nexus__sandbox_upload({
  sandbox_id: "sandbox_id",
  file_path: "/app/config.json",
  content: JSON.stringify({ key: "value" })
})

// Get logs
mcp__flow-nexus__sandbox_logs({
  sandbox_id: "sandbox_id",
  lines: 100                      // Max 1000
})
```

### Sandbox Management

```javascript
// List all sandboxes
mcp__flow-nexus__sandbox_list({
  status: "running"               // running, stopped, all
})

// Get sandbox status
mcp__flow-nexus__sandbox_status({
  sandbox_id: "sandbox_id"
})

// Configure existing sandbox
mcp__flow-nexus__sandbox_configure({
  sandbox_id: "sandbox_id",
  env_vars: { NEW_VAR: "value" },
  install_packages: ["new-package"],
  run_commands: ["npm run migrate"]
})

// Stop sandbox
mcp__flow-nexus__sandbox_stop({
  sandbox_id: "sandbox_id"
})

// Delete sandbox
mcp__flow-nexus__sandbox_delete({
  sandbox_id: "sandbox_id"
})
```

### Template Deployment

```javascript
// List templates
mcp__flow-nexus__template_list({
  category: "backend",
  featured: true,
  limit: 20
})

// Get template details
mcp__flow-nexus__template_get({
  template_name: "express-api-starter"
})

// Deploy template
mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-api",
  variables: {
    api_key: "key",
    database_url: "postgres://..."
  },
  env_vars: { PORT: "3000" }
})
```

## Usage Examples

### Example 1: Python Data Analysis Environment

```javascript
// Create Python sandbox with data science packages
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "python",
  name: "data-analysis",
  install_packages: ["pandas", "numpy", "matplotlib", "scikit-learn"],
  env_vars: { PYTHONPATH: "/app" }
});

// Upload dataset
await mcp__flow-nexus__sandbox_upload({
  sandbox_id: sandbox.sandbox_id,
  file_path: "/app/data.csv",
  content: "id,value,category\n1,100,A\n2,200,B\n3,150,A"
});

// Execute analysis
const result = await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: `
import pandas as pd
import numpy as np

df = pd.read_csv('/app/data.csv')
summary = df.groupby('category')['value'].agg(['mean', 'sum', 'count'])
print(summary.to_json())
  `,
  language: "python"
});

console.log("Analysis result:", result.output);

// Cleanup
await mcp__flow-nexus__sandbox_delete({
  sandbox_id: sandbox.sandbox_id
});
```

### Example 2: Node.js API Development

```javascript
// Create Node.js sandbox
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "node",
  name: "api-dev",
  install_packages: ["express", "cors", "helmet"],
  env_vars: {
    PORT: "3000",
    NODE_ENV: "development"
  }
});

// Upload server code
await mcp__flow-nexus__sandbox_upload({
  sandbox_id: sandbox.sandbox_id,
  file_path: "/app/server.js",
  content: `
const express = require('express');
const app = express();

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: Date.now() });
});

app.listen(3000, () => console.log('Server running on port 3000'));
  `
});

// Run server
const result = await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: "require('./server.js')",
  language: "javascript",
  timeout: 120
});

// Check logs
const logs = await mcp__flow-nexus__sandbox_logs({
  sandbox_id: sandbox.sandbox_id,
  lines: 50
});
```

### Example 3: React Development with Hot Reload

```javascript
// Create React sandbox
const sandbox = await mcp__flow-nexus__sandbox_create({
  template: "react",
  name: "react-app",
  install_packages: ["axios", "react-router-dom"],
  startup_script: "npm install"
});

// Upload component
await mcp__flow-nexus__sandbox_upload({
  sandbox_id: sandbox.sandbox_id,
  file_path: "/app/src/App.jsx",
  content: `
import React, { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <h1>Counter: {count}</h1>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
  `
});

// Start development server
await mcp__flow-nexus__sandbox_execute({
  sandbox_id: sandbox.sandbox_id,
  code: "npm start",
  timeout: 300
});
```

### Example 4: Template-Based Deployment

```javascript
// List available templates
const templates = await mcp__flow-nexus__template_list({
  category: "backend",
  featured: true
});

// Deploy Express API template
const deployment = await mcp__flow-nexus__template_deploy({
  template_name: "express-api-starter",
  deployment_name: "my-production-api",
  variables: {
    database_url: process.env.DATABASE_URL,
    jwt_secret: process.env.JWT_SECRET
  },
  env_vars: {
    NODE_ENV: "production",
    PORT: "3000"
  }
});

console.log("Deployed:", deployment.url);
```

## Execution Checklist

- [ ] Choose appropriate template for project requirements
- [ ] Plan environment variables and secrets
- [ ] Create sandbox with proper configuration
- [ ] Install required packages
- [ ] Upload project files
- [ ] Execute code and verify output
- [ ] Monitor logs for errors
- [ ] Stop sandbox when not in use
- [ ] Delete sandbox when project complete

## Best Practices

1. **Use Specific Templates**: Choose the template closest to your needs rather than `base`
2. **Environment Variables**: Never hardcode secrets; use `env_vars`
3. **Timeout Management**: Set appropriate timeouts to prevent resource waste
4. **Resource Cleanup**: Always stop/delete sandboxes when done
5. **Package Caching**: Install packages during creation, not execution
6. **Log Monitoring**: Regularly check logs during development

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `sandbox_create_failed` | Invalid template or quota exceeded | Verify template name, check sandbox limits |
| `execution_timeout` | Code exceeded timeout | Increase timeout or optimize code |
| `package_install_failed` | Invalid package name or version | Verify package exists in registry |
| `file_upload_failed` | Path issues or size limits | Check path format and file size |
| `sandbox_not_found` | Invalid or deleted sandbox_id | Use `sandbox_list` to verify |

## Metrics & Success Criteria

- **Creation Time**: Sandbox ready <30 seconds
- **Execution Latency**: Code execution starts <5 seconds
- **Resource Utilization**: <80% CPU/memory during normal operation
- **Cleanup Rate**: 100% of temporary sandboxes deleted after use

## Integration Points

### With Swarms

```javascript
// Deploy coder agent with sandbox capability
await mcp__flow-nexus__agent_spawn({
  type: "coder",
  name: "Sandbox Developer",
  capabilities: ["sandbox_execution", "code_testing"]
});
```

### With Workflows

```javascript
// CI/CD workflow with sandbox testing
await mcp__flow-nexus__workflow_create({
  name: "Test Pipeline",
  steps: [
    { id: "create", action: "sandbox_create", template: "node" },
    { id: "test", action: "sandbox_execute", code: "npm test", depends: ["create"] },
    { id: "cleanup", action: "sandbox_delete", depends: ["test"] }
  ]
});
```

### Related Skills

- [cloud-swarm](../cloud-swarm/SKILL.md) - Multi-agent orchestration
- [cloud-workflow](../cloud-workflow/SKILL.md) - Workflow automation
- [cloud-neural](../cloud-neural/SKILL.md) - Neural network training

## References

- [Flow Nexus Sandbox Documentation](https://flow-nexus.ruv.io)
- [E2B Documentation](https://e2b.dev/docs)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-sandbox agent
