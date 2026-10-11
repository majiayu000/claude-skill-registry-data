---
name: diagram
description: 'Generate a specific diagram — architecture, flow, db, sequence, deps Arguments: <type> [scope] — types: architecture, flow <feature>, db, sequence <endpoint>, deps <module>.'
---

# Generate Diagram

Create a visual diagram for the specified aspect of the codebase. Request: $ARGUMENTS

## Instructions

1. Read the primary skill:
   - `${CLAUDE_PLUGIN_ROOT}/skills/codemap-diagram/SKILL.md` — diagram generation rules and types

2. Parse `$ARGUMENTS` for diagram type and optional scope:
   - `architecture` → C4 container diagram of the entire system
   - `flow <feature>` → flowchart of a specific feature
   - `db` → ERD of all database tables
   - `sequence <endpoint>` → sequence diagram for a request
   - `deps <module>` → dependency graph for a module
   - If no argument or unrecognized → ask user which type they want

3. Launch the **diagrammer** agent with the diagram type, scope, and any additional context from the user's message.

The agent analyzes code, builds mxGraph XML using templates, saves .drawio files, and calls drawio-mcp for a preview (rendered inline only in clients that support MCP Apps).