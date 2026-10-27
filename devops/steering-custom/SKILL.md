---
name: kiro-steering-custom
description: Create custom steering documents for specialized project contexts. Use when creating domain-specific steering files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
metadata:
  shared-rules: "steering-principles.md"
---

> **移植说明**｜本文件是 `kiro` skill 的阶段规范（源自 `kiro-steering-custom` skill），由 kiro 总控按需读取并就地执行。
> 文中出现的 `kiro-xxx` / `/kiro-xxx` skill 引用，一律按 `kiro/SKILL.md` 的「阶段解析规则」处理：
> 宿主已注册同名 skill → `Skill(kiro-xxx)`；否则读 `phases/xxx/SKILL.md` 就地执行。
> 相对路径（`rules/`、`templates/`）一律相对本文件所在目录 `phases/steering-custom/`。

# kiro-steering-custom Skill

## Role
You are a specialized skill for creating custom steering documents beyond core files (product, tech, structure).

## Core Mission
**Role**: Create specialized steering documents beyond core files (product, tech, structure).

**Mission**: Help users create domain-specific project memory for specialized areas.

**Success Criteria**:
- Custom steering captures specialized patterns
- Follows same granularity principles as core steering
- Provides clear value for specific domain

## Execution Steps

### Step 1: Gather Context

If steering context is already available from conversation, skip redundant file reads.
Otherwise:
- Check `.kiro/settings/templates/steering-custom/` for available templates
- Read `rules/steering-principles.md` from this skill's directory for steering principles

## Workflow

1. **Ask user** for custom steering needs:
   - Domain/topic (e.g., "API standards", "testing approach")
   - Specific requirements or patterns to document

2. **Check if template exists**:
   - Load from `.kiro/settings/templates/steering-custom/{name}.md` if available
   - Use as starting point, customize based on project

3. **Analyze codebase** (JIT) for relevant patterns:

#### Parallel Research (concurrent subagent dispatch)

Follow `../../rules/parallel-dispatch.md`. Dispatch as **concurrent subagents in a single message** (`subagent_type: "Explore"`):

1. **Template & principles**: Load the matching template and `rules/steering-principles.md`, return the structure to follow
2. **Domain patterns**: Survey the codebase for this domain's actual patterns (Glob/Grep/Read), return patterns with example paths, under ~100 lines — patterns, not catalogs

When the requested domain is broad (e.g. "testing" across several stacks), split area 2 further — one subagent per stack/package — instead of one subagent sweeping everything.

Two areas is the minimum worth a fan-out; if the template is already in context, just do the domain survey inline.

After all return, synthesize and write the document in the parent context.

4. **Generate custom steering**:
   - Follow template structure if available
   - Apply principles from `rules/steering-principles.md` from this skill's directory
   - Focus on patterns, not exhaustive lists
   - Keep to 100-200 lines (2-3 minute read)

5. **Create file** in `.kiro/steering/{name}.md`

## Available Templates

Templates available in `.kiro/settings/templates/steering-custom/`:

1. **api-standards.md** - REST/GraphQL conventions, error handling
2. **testing.md** - Test organization, mocking, coverage
3. **security.md** - Auth patterns, input validation, secrets
4. **database.md** - Schema design, migrations, query patterns
5. **error-handling.md** - Error types, logging, retry strategies
6. **authentication.md** - Auth flows, permissions, session management
7. **deployment.md** - CI/CD, environments, rollback procedures

Load template when needed, customize for project.

## Steering Principles

From `rules/steering-principles.md` (in this skill's directory):

- **Patterns over lists**: Document patterns, not every file/component
- **Single domain**: One topic per file
- **Concrete examples**: Show patterns with code
- **Maintainable size**: 100-200 lines typical
- **Security first**: Never include secrets or sensitive data

## Tool Guidance

- **Read**: Load template, analyze existing code
- **Glob**: Find related files for pattern analysis
- **Grep**: Search for specific patterns
- **Bash** with `ls`: Understand relevant structure

**JIT Strategy**: Load template only when creating that type of steering.

## Output Description

Chat summary with file location (file created directly).

```
Custom Steering Created

## Created:
- .kiro/steering/api-standards.md

## Based On:
- Template: api-standards.md
- Analyzed: src/api/ directory patterns
- Extracted: REST conventions, error format

## Content:
- Endpoint naming patterns
- Request/response format
- Error handling conventions
- Authentication approach

Review and customize as needed.
```

## Examples

### Success: API Standards
**Input**: "Create API standards steering"
**Action**: Load template, analyze src/api/, extract patterns
**Output**: api-standards.md with project-specific REST conventions

### Success: Testing Strategy
**Input**: "Document our testing approach"
**Action**: Load template, analyze test files, extract patterns
**Output**: testing.md with test organization and mocking strategies

## Safety & Fallback

- **No template**: Generate from scratch based on domain knowledge
- **Security**: Never include secrets (load principles)
- **Validation**: Ensure doesn't duplicate core steering content

## Notes

- Templates are starting points, customize for project
- Follow same granularity principles as core steering
- All steering files loaded as project memory
- Custom files equally important as core files
- Avoid documenting agent-specific tooling directories (e.g. `.cursor/`, `.gemini/`, `.claude/`)
- Light references to `.kiro/specs/` and `.kiro/steering/` are acceptable; avoid other `.kiro/` directories
