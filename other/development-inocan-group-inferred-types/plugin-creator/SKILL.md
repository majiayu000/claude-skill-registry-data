---
name: plugin-creator
description: Comprehensive plugin development skill for Claude Code. Analyzes business requirements and creates complete plugins including MCP servers, skills, slash commands, or combinations thereof. Supports TypeScript, Python, and any other language. Provides architecture guidance, templates, and end-to-end implementation.
---

# Plugin Creator

This skill guides the creation of complete, production-ready plugins for Claude Code by analyzing business requirements and architecting appropriate solutions.

## Purpose

Transform business requirements into fully-functional Claude Code plugins by:
1. Analyzing the business problem and technical requirements
2. Recommending optimal plugin architecture (MCP servers, skills, slash commands, or combinations)
3. Providing templates and implementation guidance
4. Creating complete, tested, and packaged plugins ready for distribution

## When to Use This Skill

Use this skill when:
- Creating new Claude Code plugins from business requirements
- Needing architectural guidance for plugin structure
- Requiring templates for MCP servers, skills, or slash commands
- Building plugins that combine multiple component types
- Packaging and distributing Claude Code plugins

## Plugin Architecture Analysis Workflow

### Step 1: Business Requirements Analysis

When a user requests a plugin, systematically analyze their needs:

**Key Questions:**
1. **What problem does this solve?** - Understand the business value
2. **What are the core operations?** - Identify main capabilities needed
3. **What tools/services are involved?** - External integrations (APIs, databases, etc.)
4. **What's the interaction model?** - How will users invoke functionality?
5. **What data needs to be managed?** - State, configuration, persistence requirements

**Example Analysis:**

```
Request: "Create a plugin for database schema management"

Analysis:
- Problem: Developers need to manage database schemas efficiently
- Core operations: View schemas, run migrations, generate models, validate changes
- Tools: Database connections (PostgreSQL, MySQL, etc.), migration tools
- Interaction: Commands for quick actions, skill for complex workflows
- Data: Connection configs, migration history, schema snapshots
```

### Step 2: Architecture Recommendation

Based on the analysis, recommend plugin components:

**Decision Matrix:**

| Component Type | When to Use |
|---------------|-------------|
| **MCP Server** | External tool/service integration, stateful operations, complex APIs, real-time data access |
| **Skill** | Procedural workflows, domain knowledge, multi-step processes, bundled resources |
| **Slash Command** | Quick actions, command shortcuts, user-facing operations |
| **Combination** | Complex plugins needing multiple interaction patterns |

**Architecture Patterns:**

1. **Pure MCP Server** - External service integration (e.g., database connector, API client)
2. **Pure Skill** - Knowledge/workflow only (e.g., code review guidelines, deployment procedures)
3. **Pure Slash Command** - Simple command shortcuts (e.g., `/format`, `/lint`)
4. **MCP + Skill** - Tool integration + procedural knowledge (e.g., testing framework + testing best practices)
5. **MCP + Commands** - Tool integration + quick shortcuts (e.g., database MCP + `/db:migrate`, `/db:seed`)
6. **Skill + Commands** - Workflows + shortcuts (e.g., deployment skill + `/deploy:prod`, `/deploy:staging`)
7. **Full Plugin** - All three (e.g., comprehensive development environment)

**Example Recommendations:**

```
For "database schema management":
Recommended Architecture: MCP Server + Skill + Slash Commands

Components:
1. MCP Server (TypeScript or Python)
   - Tools: connect_db, get_schema, run_migration, generate_model
   - Resources: schema definitions, migration history

2. Skill (Markdown)
   - Migration best practices
   - Schema design patterns
   - Rollback procedures
   - References: migration_guide.md, schema_patterns.md

3. Slash Commands
   - /db:migrate - Run pending migrations
   - /db:rollback - Rollback last migration
   - /db:schema - View current schema
   - /db:seed - Seed database
```

### Step 3: Implementation Guidance

For each recommended component, provide implementation path:

#### MCP Server Implementation

**Language Selection:**
- **TypeScript/Node.js** - Best for: JavaScript ecosystem integration, npm packages, web APIs
- **Python/FastMCP** - Best for: Data science, ML tools, Python library integration

**Use templates from `assets/templates/`:**
- `mcp-server-typescript/` - Full TypeScript MCP server template
- `mcp-server-python/` - Full Python FastMCP server template

**Implementation steps:**
1. Copy appropriate template to plugin directory
2. Define tools (functions Claude can call)
3. Define resources (data Claude can read)
4. Implement tool handlers with error handling
5. Add configuration management
6. Write tests
7. Create documentation

**Detailed guidance:** See `references/mcp_server_guide.md`

#### Skill Implementation

**Use template from `assets/templates/skill/`**

**Implementation steps:**
1. Create SKILL.md with proper frontmatter
2. Define when skill should be used (triggers)
3. Write procedural instructions
4. Add bundled resources:
   - `scripts/` - Executable helpers
   - `references/` - Documentation to load as needed
   - `assets/` - Files used in output
5. Test with realistic scenarios
6. Package with validation

**Detailed guidance:** See `references/skill_guide.md`

#### Slash Command Implementation

**Use template from `assets/templates/slash-command/`**

**Implementation steps:**
1. Create command file in `.claude/commands/`
2. Define command name and description
3. Write command prompt
4. Add parameter handling
5. Test command execution
6. Document usage

**Detailed guidance:** See `references/slash_command_guide.md`

### Step 4: Plugin Integration

For multi-component plugins, ensure proper integration:

**Integration Checklist:**
- [ ] MCP server tools are referenced in skill instructions
- [ ] Slash commands call appropriate MCP tools or use skill knowledge
- [ ] Skill provides context for when to use which component
- [ ] All components share consistent naming and terminology
- [ ] Configuration is unified (single config file where possible)
- [ ] Documentation covers the complete plugin workflow

**Example Integration:**

```markdown
In SKILL.md:

## Using the Database Plugin

This plugin combines an MCP server, skill knowledge, and quick commands.

### Quick Operations (Slash Commands)
- Use `/db:migrate` for running migrations quickly
- Use `/db:schema` to view current schema

### MCP Server Tools
The database MCP server provides these tools:
- `connect_db` - Establish database connection
- `get_schema` - Retrieve schema information
- `run_migration` - Execute migration files

### Workflow Guidance
For complex operations, follow these procedures:
[Reference migration_guide.md for detailed procedures]
```

### Step 5: Testing and Validation

Before packaging, validate the plugin:

**Validation Steps:**
1. Run `scripts/validate_plugin.py <plugin-path>`
2. Test each component individually
3. Test component integration
4. Verify documentation completeness
5. Check error handling
6. Validate configuration management

**Testing Checklist:**
- [ ] MCP server tools work correctly
- [ ] Skill triggers appropriately
- [ ] Slash commands execute as expected
- [ ] Error messages are clear and helpful
- [ ] Documentation is accurate and complete
- [ ] Examples work as documented

### Step 6: Packaging and Distribution

Package the complete plugin:

**Using the packaging script:**
```bash
python scripts/package_plugin.py <plugin-path> [output-dir]
```

**Plugin structure for distribution:**
```
my-plugin/
├── README.md (installation and usage)
├── mcp-server/ (if applicable)
│   ├── package.json or requirements.txt
│   ├── src/ or app/
│   └── tests/
├── skill/ (if applicable)
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
└── commands/ (if applicable)
    ├── command1.md
    └── command2.md
```

**Distribution outputs:**
1. `my-plugin.zip` - Complete plugin package
2. `my-plugin/README.md` - Installation instructions
3. `my-plugin/ARCHITECTURE.md` - Technical documentation

## Best Practices

Refer to `references/best_practices.md` for comprehensive guidelines including:
- Error handling patterns
- Configuration management
- Security considerations
- Performance optimization
- Documentation standards
- Testing strategies

## Architecture Patterns

Refer to `references/architecture_patterns.md` for detailed patterns:
- Single-responsibility plugins
- Multi-component plugins
- Plugin composition strategies
- Integration patterns
- Scalability patterns

## Helper Scripts

### Initialize Plugin
```bash
python scripts/init_plugin.py <plugin-name> --type <mcp|skill|command|full>
```

Creates plugin scaffolding with appropriate templates.

### Validate Plugin
```bash
python scripts/validate_plugin.py <plugin-path>
```

Validates plugin structure, code quality, and documentation.

### Package Plugin
```bash
python scripts/package_plugin.py <plugin-path> [output-dir]
```

Creates distributable plugin package with validation.

## Example Workflow

**Request:** "Create a plugin for API testing"

**Analysis:**
- Problem: Developers need to test REST APIs efficiently
- Operations: Send requests, validate responses, manage test suites
- Tools: HTTP client, assertion library
- Interaction: Commands for quick tests, skill for test strategies
- Data: API configurations, test suites, response schemas

**Architecture:**
```
Recommended: MCP Server + Skill + Slash Commands

1. MCP Server (TypeScript)
   - Tools: send_request, validate_response, run_test_suite
   - Resources: api_configs, test_results

2. Skill
   - API testing best practices
   - Test strategy guidance
   - References: rest_api_guide.md, assertion_patterns.md

3. Slash Commands
   - /api:test <endpoint> - Quick endpoint test
   - /api:suite <suite-name> - Run test suite
   - /api:validate <response> - Validate response format
```

**Implementation:**
1. Initialize with `init_plugin.py api-testing --type full`
2. Implement MCP server using TypeScript template
3. Create skill with testing best practices
4. Add slash commands for quick operations
5. Integrate components in skill documentation
6. Validate with `validate_plugin.py`
7. Package with `package_plugin.py`

**Output:** Complete, tested, documented `api-testing.zip` plugin ready for installation.
