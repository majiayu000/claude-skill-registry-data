---
name: pwn-ai-context
description: Drive PWN::AI::Context from pwn_eval.
license: MIT
allowed-tools: [pwn, pwn_eval]
metadata:
  bundled: true
  generated: true
  module: PWN::AI::Context
  source: pwn/ai/context.rb
---

# PWN::AI::Context

Attach files, hexdumps, disassembly, and HTTP transcripts to model context with auto-chunking. Oversize artifacts are summarized inline and persisted under ~/.pwn/artifacts/<session_id>/ with SHA-256.

## When to use

Call `PWN::AI::Context` from `pwn_eval` when the task needs this module.
Do not reimplement it in shell.

## Methodologies

Generated from `pwn/ai/context.rb`. Prefer the public class methods below.
Class methods take `(opts = {})` and read `opts`.

## How to call

```ruby
PWN::AI::Context.help
PWN::AI::Context.attach_file(opts)
```

## Public methods

- `attach_file`
- `attach_hexdump`
- `attach_disasm`
- `attach_http_transcript`
- `authors`
- `help`
- `ingest`
- `retrieve`

## Source

`pwn/ai/context.rb`

## Verification

`PWN::AI::Context.respond_to?(:attach_file)` after the
module is loaded. Read the source for parameter names.
