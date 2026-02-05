---
name: Nodes Node Structure
description: Structure n8n nodes correctly with INodeTypeDescription, resource-operation patterns, and proper package.json configuration. Use this skill when creating new *.node.ts files, defining INodeTypeDescription properties, implementing resource and operation parameters, building trigger nodes, organizing complex nodes into actions folders, or configuring the n8n section in package.json. Apply when choosing between declarative and programmatic styles, setting up node metadata, or structuring community node packages.
---

## When to use this skill:

- When creating new n8n node files (*.node.ts)
- When defining INodeTypeDescription (displayName, name, icon, group, version)
- When setting up resource and operation parameters with noDataExpression: true
- When using displayOptions to conditionally show fields
- When adding action fields to operations for future compatibility
- When building trigger nodes (polling or webhook-based)
- When organizing complex nodes with actions/ folders by resource
- When defining userOperations and userFields arrays
- When configuring the "n8n" section in package.json (nodes, credentials paths)
- When setting subtitle templates for dynamic node labels
- When specifying inputs, outputs, and credential requirements
- When deciding between declarative style (REST APIs) and programmatic style (triggers, GraphQL)

# Nodes Node Structure

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle nodes node structure.

## Instructions

For details, refer to the information provided in this file:
[nodes node structure](../../../agent-os/standards/nodes/node-structure.md)
