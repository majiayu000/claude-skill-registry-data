---
name: mcp-server-design
description: Use when designing or reviewing MCP servers and MCP-exposed capabilities used by PonyBunny.
---

# MCP Server Design

## Use this skill when
- designing a new MCP integration
- exposing local or remote capabilities safely
- reviewing trust boundaries
- deciding capability scope

## Goals
- expose useful capabilities safely
- keep interfaces narrow
- reduce privilege
- improve agent-side reliability and auditability

## Process
1. Define the capability.
2. Define trust boundaries.
3. Define authentication and authorisation expectations.
4. Define request and response schemas.
5. Define side effects and limits.
6. Define logging and audit requirements.
7. Define failure behaviour.

## Output contract
Return:
- capability overview
- trust boundaries
- schema summary
- safety notes
- audit notes
- operational risks
