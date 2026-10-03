---
name: pwn-ai-cli
description: Drive PWN::AI::CLI from pwn_eval.
license: MIT
allowed-tools: [pwn, pwn_eval]
metadata:
  bundled: true
  generated: true
  module: PWN::AI::CLI
  source: pwn/ai/cli.rb
---

# PWN::AI::CLI

Explicit standalone entrypoint; help and parsing never load a vault.

## When to use

Call `PWN::AI::CLI` from `pwn_eval` when the task needs this module.
Do not reimplement it in shell.

## Methodologies

Generated from `pwn/ai/cli.rb`. Prefer the public class methods below.
Class methods take `(opts = {})` and read `opts`.

## How to call

```ruby
PWN::AI::CLI.help
PWN::AI::CLI.parse(opts)
```

## Public methods

- `parse`
- `run`
- `authors`
- `help`

## Source

`pwn/ai/cli.rb`

## Verification

`PWN::AI::CLI.respond_to?(:parse)` after the
module is loaded. Read the source for parameter names.
