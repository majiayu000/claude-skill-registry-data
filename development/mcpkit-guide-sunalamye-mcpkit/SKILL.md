---
name: mcpkit-guide
description: Guide for using MCPKit Swift package to build MCP (Model Context Protocol) tool servers. Use when creating new MCP servers, defining tools, or integrating MCP into Swift projects.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# MCPKit Guide

This skill helps use the MCPKit Swift package to build MCP (Model Context Protocol) tool servers.

## Package Overview

**MCPKit** is a Swift implementation of Model Context Protocol for building AI tool servers.

- **Repository**: https://github.com/Sunalamye/MCPKit
- **Platforms**: macOS 13+, iOS 16+
- **License**: MIT

## Installation

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/Sunalamye/MCPKit.git", from: "1.0.0"),
]

targets: [
    .target(
        name: "YourApp",
        dependencies: ["MCPKit"]
    ),
]
```

## Architecture

```
MCPKit/
├── Core/
│   ├── MCPTool.swift          - Protocol & Schema types
│   ├── MCPContext.swift       - Execution context
│   ├── MCPToolRegistry.swift  - Tool registration
│   └── MCPHandler.swift       - JSON-RPC handler
├── Transport/
│   └── MCPHTTPServer.swift    - HTTP server
└── Tools/
    └── BuiltInTools.swift     - Basic tools
```

## Quick Start

### 1. Define a Tool

```swift
import MCPKit

struct MyTool: MCPTool {
    static let name = "my_tool"
    static let description = "Description for AI to understand when to use this tool"

    static let inputSchema = MCPInputSchema(
        properties: [
            "param1": .string("Parameter description"),
            "param2": .integer("Optional param description")
        ],
        required: ["param1"]
    )

    private let context: MCPContext

    init(context: MCPContext) {
        self.context = context
    }

    func execute(arguments: [String: Any]) async throws -> Any {
        guard let param1 = arguments["param1"] as? String else {
            throw MCPToolError.missingParameter("param1")
        }

        // Your logic here...

        return ["success": true, "result": "..."]
    }
}
```

### 2. Create Context

```swift
class MyContext: MCPContext {
    var serverPort: Int = 8080

    func executeJavaScript(_ script: String) async throws -> Any? {
        return nil
    }

    func getBotStatus() -> [String: Any]? {
        return ["status": "ready"]
    }

    func triggerAutoPlay() {}

    func getLogs() -> [[String: Any]] { logs }
    func clearLogs() { logs.removeAll() }
    func log(_ message: String) {
        logs.append(["message": message, "timestamp": Date()])
    }

    private var logs: [[String: Any]] = []
}
```

### 3. Register Tools & Start Server

```swift
import MCPKit

let context = MyContext()
let registry = MCPToolRegistry.shared

// Register built-in tools
registry.registerBuiltInTools(context: context)

// Register custom tools
registry.register(MyTool.self, context: context)

// Start HTTP server
let server = MCPHTTPServer(port: 8765, context: context)
try await server.start()
```

## Input Schema Types

```swift
// No parameters
static let inputSchema = MCPInputSchema.empty

// With parameters
static let inputSchema = MCPInputSchema(
    properties: [
        "stringParam": .string("String parameter"),
        "intParam": .integer("Integer parameter"),
        "numberParam": .number("Number parameter"),
        "boolParam": .boolean("Boolean parameter"),
        "objectParam": .object("Object parameter")
    ],
    required: ["stringParam"]
)
```

## Error Handling

```swift
throw MCPToolError.missingParameter("paramName")
throw MCPToolError.invalidParameter("paramName", expected: "string")
throw MCPToolError.executionFailed("Reason")
throw MCPToolError.notAvailable("Resource name")
```

## Built-in Tools

| Tool | Description |
|------|-------------|
| `get_status` | Get MCP server status |
| `get_help` | Get API documentation |
| `get_logs` | Get debug logs |
| `clear_logs` | Clear all logs |

## JSON-RPC Methods

```json
// Initialize
{"jsonrpc": "2.0", "method": "initialize", "id": 1}

// List tools
{"jsonrpc": "2.0", "method": "tools/list", "id": 2}

// Call tool
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {"name": "my_tool", "arguments": {"param1": "value"}},
  "id": 3
}
```

## Checklist for New Tools

- [ ] Unique `name` (snake_case format)
- [ ] Clear `description` (helps AI understand usage)
- [ ] Correct `inputSchema` definition
- [ ] Implement `execute()` method (async throws)
- [ ] Handle errors with MCPToolError
- [ ] Register in registry

## Reference Documentation

- [MCPKit Reference](references/reference.md) - Full protocol, context API, and examples
