---
name: test-gaps
description: Detect missing test coverage and generate test suggestions
argument-hint: "[--path PATH] [--limit N]"
allowed-tools: Bash(npx *) mcp__claude-flow__hooks_worker-dispatch Read Grep
---
Find test coverage gaps via CLI:
```bash
npx @claude-flow/cli@latest hooks coverage-gaps --format table --limit 20
npx @claude-flow/cli@latest hooks coverage-route --task "add auth tests"
npx @claude-flow/cli@latest hooks coverage-suggest --path src/
```

Or dispatch the testgaps worker via MCP:
`mcp__claude-flow__hooks_worker-dispatch({ trigger: "testgaps" })`

For continuous detection, run the testgaps worker periodically via an external scheduler, CI job, or user-requested follow-up session.
