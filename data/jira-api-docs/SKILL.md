---
name: jira-api-docs
description: Complete Jira Cloud REST API documentation for v2 and v3 endpoints. Use when working with Jira APIs, making Jira API calls, troubleshooting Jira integrations, or needing endpoint details. DO NOT use for general Jira usage questions or Jira web UI help.
version: 1.1.0
---

# Jira Cloud REST API Documentation

Complete reference documentation for Jira Cloud REST API v2 and v3 endpoints, including all models, parameters, and response formats.

> **Usage Priority**: When working with Jira APIs, follow this order:
> 1. **Quick Reference + Scripts** - Check `quick-reference/` for your task, then **read and run the scripts**
>    - To find quick-references: `Glob(pattern: "*.md", path: ".claude/skills/jira-api-docs/quick-reference")`
>    - To find scripts: `Glob(pattern: "*<keyword>*", path: ".claude/skills/jira-api-docs/scripts")`
> 2. **MCP Server Search** - If no script exists, query `jira-docs` MCP server for endpoint details
> 3. **Full API Reference** - Consult `api-reference/` only if MCP doesn't cover your need
> 4. **REQUIRED: Save your work** - Save new scripts to `scripts/` and add them to quick-reference

## Documentation Paths

**All paths are under `~/.claude/skills/jira-api-docs/`**:

```
~/.claude/skills/jira-api-docs/
├── quick-reference/           # Task → script mappings (check FIRST)
│   ├── workflows.md
│   └── ...
├── scripts/                   # Working scripts (READ AND USE THESE)
│   ├── fetch-workflow-table.sh
│   └── ...
└── api-reference-guide.md     # Navigation guide for Task agents (last resort)
```

## When to Use This Skill

✅ **Use when:**
- Making Jira API calls or HTTP requests
- Looking up specific Jira API endpoints
- Understanding Jira API request/response formats
- Troubleshooting Jira API integrations
- Finding API endpoint parameters and options
- Working with Jira webhooks or automation
- Building Jira integrations or scripts

❌ **Don't use when:**
- General Jira usage questions (use Jira UI instead)
- Jira administration via web interface
- JQL query help (unless related to API endpoints)
- Jira workflow configuration via UI

## Common API Tasks

### Workflows

**Quick Reference**: `./quick-reference/workflows.md` — **read this first, use the scripts**

### Everything Else

1. Query the `jira-docs` MCP server
2. If MCP fails after 2-3 attempts, launch a **Task agent** — the raw API docs are thousands of lines and tens of thousands of tokens; tell the agent your requirements and to read `./api-reference-guide.md`

## Test Sandbox

Safe resources for testing — do NOT use production projects/objects:
- **Projects**: `TESTPROJ` (Service Desk), `HSP` (Software)
- **Issues**: Create new in HSP/TESTPROJ (don't rely on existing)
- **Filter**: "Test Filter" (ID: 12229)
- **Dashboard**: "Test Dashboard" (ID: 10275)
- **Group**: "Test Group" (ID: 60870276-7f12-4367-af84-23903ab1553c)
- **Custom fields**: Use existing `TestField_*` or create with that prefix
- **Sprints/Boards**: Use or create in HSP/TESTPROJ

## Before Finishing

⚠️ **STOP: Before marking a Jira task complete:**
- New script? → Save to `scripts/` + add to quick-reference
- Fixed a script? → Update script + add lesson learned
