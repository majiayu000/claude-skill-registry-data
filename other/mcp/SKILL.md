---
name: pwn-ai-mcp
description: Drive PWN::AI::MCP from pwn_eval.
license: MIT
allowed-tools: [pwn, pwn_eval]
metadata:
  bundled: true
  generated: true
  module: PWN::AI::MCP
  source: pwn/ai/mcp.rb
---

# PWN::AI::MCP

Autoload MCP client modules that speak JSON-RPC 2.0 to local MCP servers. Session state lives here so pwn-ai Registry tools persist across turns.

## When to use

Call `PWN::AI::MCP` from `pwn_eval` when the task needs this module.
Do not reimplement it in shell.

## Methodologies

Generated from `pwn/ai/mcp.rb`. Prefer the public class methods below.
Class methods take `(opts = {})` and read `opts`.

## How to call

```ruby
PWN::AI::MCP.help
PWN::AI::MCP.backends(opts)
```

## Public methods

- `backends`
- `resolve`
- `use`
- `current`
- `connect`
- `disconnect`
- `ping`
- `list_tools`
- `call_tool`
- `poll_until`
- `invoke`
- `reset`
- `authors`
- `help`
- `reset!`

## Source

`pwn/ai/mcp.rb`

## Verification

`PWN::AI::MCP.respond_to?(:backends)` after the
module is loaded. Read the source for parameter names.
