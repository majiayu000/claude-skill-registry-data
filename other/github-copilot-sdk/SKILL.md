---
name: github--copilot-sdk
description: "GitHub Copilot SDK — embed Copilot agent runtime vào app: Node/Python/Go/.NET/Java/Rust. JSON-RPC tới Copilot CLI. Custom agents + tools + model selection. MIT."
allowed-tools: Bash, Read, Write
user-invocable: true
---

GitHub Copilot SDK: expose Copilot's agent runtime (planning + tool invocation + file edits) dưới dạng library — dùng trong Node, Python, Go, .NET, Java, Rust.

## Install

```bash
# Node.js
npm install @github/copilot-sdk

# Python
pip install github-copilot-sdk

# Go
go get github.com/github/copilot-sdk/go

# .NET
dotnet add package GitHub.Copilot.SDK

# Rust
cargo add github-copilot-sdk

# Java (Maven)
# groupId: com.github, artifactId: copilot-sdk-java
```

## Architecture

```
Your App
  ↓
SDK Client (npm/@github/copilot-sdk)
  ↓ JSON-RPC
Copilot CLI (server mode — managed by SDK)
```

SDK tự quản lý CLI lifecycle — không cần spawn thủ công.

## Key Features

```
Custom agents + skills + tools
Multiple auth: GitHub OAuth, BYOK (Bring Your Own Key), env vars
First-party Copilot CLI tools enabled by default
Model selection at runtime
```

## Basic Usage (Node.js)

```typescript
import { CopilotClient } from '@github/copilot-sdk'

const client = new CopilotClient()
await client.connect()

const result = await client.runAgent({
  prompt: "Add error handling to this function",
  files: ['src/api.ts']
})

console.log(result.edits)
await client.disconnect()
```

## Khi nào dùng

- Muốn embed Copilot agent vào yamtam workflow
- Build tool sử dụng Copilot's planning + file edit capabilities
- Alternative cho Claude API khi cần GitHub Copilot-specific features

## Source

https://github.com/github/copilot-sdk · MIT · +309⭐/week
