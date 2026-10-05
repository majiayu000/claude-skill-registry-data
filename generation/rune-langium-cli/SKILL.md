---
description: "Command-line entry points for parsing, validating, and generating code from\nRune DSL workspaces."
name: rune-langium-cli
---

# @rune-langium/cli

Command-line entry points for parsing, validating, and generating code from
Rune DSL workspaces.

Use the CLI when you need batch validation in CI, ad-hoc parsing from a
terminal, or code generation without embedding the libraries directly in a
Node.js tool. The `generate` command delegates to the codegen toolchain while
`parse` and `validate` provide lightweight syntax and diagnostics checks.

## Links

- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)