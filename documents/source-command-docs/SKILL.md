---
name: "source-command-docs"
description: "Fetch Rust API documentation from docs.rs"
---

# source-command-docs

Use this skill when the user asks to run the migrated source command `docs`.

## Command Template

# /docs Command

Fetch API documentation for Rust crates from docs.rs.

## Usage

```
/docs <crate_name> [item]
```

## Examples

```
/docs snafu              # Get snafu crate overview
/docs tokio spawn        # Get tokio::spawn documentation
/docs serde Serialize    # Get serde::Serialize trait docs
```

## Workflow

1. Use actionbook MCP to get docs.rs selectors
2. Launch `docs-researcher` agent with target URL
3. Wait for agent to complete
4. Return formatted API documentation

## Target URLs

- Overview: `https://docs.rs/<crate>/latest/<crate>/`
- Function: `https://docs.rs/<crate>/latest/<crate>/fn.<name>.html`
- Struct: `https://docs.rs/<crate>/latest/<crate>/struct.<Name>.html`
- Trait: `https://docs.rs/<crate>/latest/<crate>/trait.<Name>.html`
- Macro: `https://docs.rs/<crate>/latest/<crate>/macro.<name>.html`
- Module: `https://docs.rs/<crate>/latest/<crate>/<module>/`

## Output Format

```
# <crate_name> API Documentation

## Overview
<crate description>

## Key Types
- `TypeName`: <description>

## Key Functions
- `fn_name`: <description>

## Key Traits
- `TraitName`: <description>

Source: docs.rs
```
