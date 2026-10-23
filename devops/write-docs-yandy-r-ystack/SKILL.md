---
name: write-docs
description: Coordinates parallel documentation agents to audit and improve project
  docs. Use when generating codebase documentation, filling documentation gaps, or
  updating existing docs.
---

# Documentation Orchestration Skill

You are a documentation orchestrator deploying specialized agents to analyze the codebase and create comprehensive, consistent documentation. **Your role is to coordinate agents, not write documentation yourself.**

## Current Project Context

When the skill starts, run these commands to gather project context:

```bash
pwd                                    # Working directory
test -d docs && echo "yes" || echo "no"               # docs/ exists
test -f README.md && echo "yes" || echo "no"          # README.md exists
test -f AGENTS.md && echo "yes" || echo "no"          # AGENTS.md exists
test -f package.json && echo "yes" || echo "no"       # Node.js project
test -f go.mod && echo "yes" || echo "no"             # Go project
test -f requirements.txt && echo "yes" || echo "no"   # Python project (pip)
test -f pyproject.toml && echo "yes" || echo "no"     # Python project (poetry)
test -f Cargo.toml && echo "yes" || echo "no"         # Rust project
```

Use this information to understand the project structure and determine the documentation strategy.

## Arguments

**Target**: `$ARGUMENTS`

Parse arguments:

- **scope**: Any non-flag argument (e.g., "auth system", "api", "frontend")
- **--update**: Enhance existing documentation without restructuring
- **--fresh**: Create fresh documentation, ignoring existing structure
- **--dry-run**: Show what would be done without making changes

If no arguments provided, analyze the entire codebase and create a full documentation plan.

---

## Phase 0: Documentation Audit

### Step 1: Run Documentation Audit Script

Execute the audit script to inventory existing documentation:

```bash
~/.agents/skills/write-docs/scripts/audit-documentation.sh
```

This script scans:

- `docs/` directory structure and files
- All `README.md` files (root and subdirectories)
- All `AGENTS.md` files
- API specifications (OpenAPI, GraphQL schemas)
- Inline documentation density (JSDoc, docstrings)

### Step 2: Infrastructure Setup

If `docs/` doesn't exist or is minimal, create the documentation infrastructure:

```
docs/
├── README.md              # Main documentation index
├── plans/
│   └── documentation-strategy.md
├── architecture/          # System design docs
├── api/                   # API reference
├── features/              # Feature guides
├── development/           # Developer guides
└── reference/             # Technical reference
```

### Step 3: Gap Analysis

Based on audit results, identify:

- Undocumented code modules and features
- Outdated documentation (compare timestamps vs code changes)
- Missing API documentation
- Incomplete architecture diagrams
- Code without inline documentation

Write findings to `docs/plans/documentation-strategy.md` using the template.

---

## Phase 1: Strategy & Prioritization

### Step 4: Define Scope

Based on `$ARGUMENTS`:

- **Specific scope** (e.g., "auth system"): Focus agents on named feature/module
- **Full codebase** (no scope): Assign agents to different areas
- **--update mode**: Focus on gaps identified in Phase 0
- **--fresh mode**: Full documentation regeneration

### Step 5: Create Task Plan

Use the task tools (`TaskCreate`) to create a prioritized task list:

1. Critical documentation gaps (public APIs, core features)
2. Architecture and system design
3. Feature documentation
4. Developer guides
5. Code-level documentation

Map: code areas → documentation needs → agent assignments

---

## Phase 2: Parallel Agent Deployment

### Step 6: Check for Dry Run

If `--dry-run` is in `$ARGUMENTS`:

- Display the documentation strategy
- Show which agents would be deployed
- List files that would be created/modified
- **STOP HERE** - do not deploy agents or make changes

### Step 7: Deploy Documentation Agents

**CRITICAL**: Deploy all 5 agents in a **SINGLE message** with **MULTIPLE Agent tool calls**.

| Agent                    | Plugin Agent Name      | Output Location      | Focus                                                         |
| ------------------------ | ---------------------- | -------------------- | ------------------------------------------------------------- |
| **Architecture Analyst** | `architecture-analyst` | `docs/architecture/` | System diagrams, component relationships, data flow (Mermaid) |
| **API Documenter**       | `api-documenter`       | `docs/api/`          | Endpoint specs, request/response examples, OpenAPI            |
| **Feature Writer**       | `feature-writer`       | `docs/features/`     | User-facing feature guides, tutorials, use cases              |
| **Code Documenter**      | `code-documenter`      | Source files         | JSDoc, type docs, inline comments for complex logic           |
| **README Generator**     | `readme-generator`     | `README.md` files    | Project/directory READMEs, setup, usage                       |

### Agent Deployment Instructions

Each agent receives:

1. **Context**: The `docs/plans/documentation-strategy.md` file
2. **Scope**: Their specific documentation mandate
3. **Style Guidelines**:
   - Clear, concise language
   - Include code examples from actual codebase
   - Use Mermaid syntax for all diagrams
   - Cross-reference related documentation
4. **Output**: Specific file paths and format requirements
5. **Mode**:
   - **Default/--update**: Enhance existing docs, preserve structure
   - **--fresh**: Create new documentation, may restructure

### Placeholder Substitution

Before deploying agents, replace runtime placeholders in the task prompts:

- **`[SCOPE]`**: Replace with the parsed scope argument (e.g., "auth system", "api") or "the entire codebase" if no scope was provided
- **`[update|fresh]`**: Replace with "update" (default) or "fresh" if the `--fresh` flag is present

### Agent Task Prompts

**Architecture Analyst**:

```
Analyze the codebase architecture and create documentation in docs/architecture/.

Read docs/plans/documentation-strategy.md for context.

Create:
- docs/architecture/overview.md: High-level system overview with Mermaid diagram
- docs/architecture/components.md: Component descriptions and relationships
- docs/architecture/data-flow.md: Data flow patterns with Mermaid sequence diagrams

Use Mermaid syntax for all diagrams. Focus on [SCOPE] if specified.
Mode: [update|fresh]
```

**API Documenter**:

```
Create API documentation in docs/api/.

Read docs/plans/documentation-strategy.md for context.

Create:
- docs/api/README.md: API overview and quick reference
- docs/api/endpoints.md: Detailed endpoint documentation
- docs/api/authentication.md: Auth methods and examples
- docs/api/errors.md: Error codes and handling

Include request/response examples with realistic data.
Focus on [SCOPE] if specified.
Mode: [update|fresh]
```

**Feature Writer**:

```
Create user-facing feature documentation in docs/features/.

Read docs/plans/documentation-strategy.md for context.

Create feature guides with:
- Overview and purpose
- Step-by-step usage instructions
- Code examples
- Common use cases
- Troubleshooting tips

Focus on [SCOPE] if specified.
Mode: [update|fresh]
```

**Code Documenter**:

```
Add inline documentation to source files.

Read docs/plans/documentation-strategy.md for context.

Add:
- JSDoc/docstrings to exported functions and classes
- Type documentation for complex types
- Inline comments for non-obvious logic
- Module-level documentation headers

Focus on [SCOPE] if specified.
Do NOT over-document obvious code.
Mode: [update|fresh]
```

**README Generator**:

```
Create/update README.md files throughout the project.

Read docs/plans/documentation-strategy.md for context.

Update:
- Root README.md: Project overview, setup, usage
- Directory READMEs: Purpose of each major directory

Include:
- Quick start guide
- Installation instructions
- Basic usage examples
- Links to detailed documentation

Focus on [SCOPE] if specified.
Mode: [update|fresh]
```

---

## Phase 3: Integration & Index Generation

### Step 8: Generate Documentation Index

After agents complete, run:

```bash
~/.agents/skills/write-docs/scripts/generate-doc-index.sh
```

This creates/updates `docs/README.md` with:

- Quick links to main sections
- Complete navigation tree
- Recently updated files

### Step 9: Cross-Link Documentation

Ensure documentation is interconnected:

- Add "See Also" sections where appropriate
- Create category indexes (api/README.md, features/README.md, etc.)
- Link from code comments to detailed docs

---

## Phase 4: Quality Assurance

### Step 10: Verify Links

Run link verification:

```bash
~/.agents/skills/write-docs/scripts/verify-links.sh
```

Report and fix any broken internal links.

### Step 11: Verification Checklist

Before finalizing, verify:

- [ ] All gaps from Phase 0 audit are addressed
- [ ] Architecture diagrams render correctly (valid Mermaid syntax)
- [ ] API documentation includes request/response examples
- [ ] Code examples are accurate and from actual codebase
- [ ] Cross-references and internal links are valid
- [ ] Consistent style across all documentation
- [ ] README files explain purpose and setup clearly
- [ ] No duplicate content between agents' outputs

### Step 12: Final Summary

Provide completion summary:

1. **Files Created**: List of new documentation files
2. **Files Updated**: List of existing files enhanced
3. **Coverage Summary**: Documentation coverage by area
4. **Remaining Gaps**: Any areas that couldn't be addressed
5. **Maintenance Notes**: Recommendations for keeping docs current

---

## Quality Standards

### Style Guidelines

- Use clear, concise language
- Provide working code examples that can be copy-pasted
- Use Mermaid syntax for all diagrams
- Structure with proper headings (H1 for title, H2 for sections, H3 for subsections)
- Include "Prerequisites" and "Next Steps" where appropriate

### Diagram Standards (Mermaid)

- Use `graph TD` for hierarchies and flows
- Use `sequenceDiagram` for API/process flows
- Use `classDiagram` for type relationships
- Keep diagrams focused and readable

### Code Example Standards

- Use actual code from the codebase, not hypotheticals
- Include necessary imports and context
- Show both input and expected output where relevant
- Annotate complex parts with comments

---

## Important Notes

- **You are the orchestrator** - delegate writing to agents
- **Deploy agents in parallel** - single message with multiple Agent calls
- **Respect existing work** - enhance, don't replace (unless --fresh)
- **Quality over quantity** - focused docs are better than comprehensive but vague
- **Verify before completing** - run all checks before marking done
