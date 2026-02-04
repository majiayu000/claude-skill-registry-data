---
name: core
description: Core development principles and guidelines covering security, QA, performance, documentation, and coding standards. Used by all agents to ensure consistent quality across the Orchestra system.
---

# Core Development Skills

This skill provides essential development principles and checklists that all Orchestra agents follow to maintain high-quality standards across security, testing, documentation, performance, and code quality.

## Overview

The core skills provide:
- **Security principles** (security.yaml) - Secure coding practices and vulnerability prevention
- **QA guidelines** (qa.yaml) - Testing standards and quality assurance procedures
- **Release procedures** (release.yaml) - Deployment and release management
- **Performance standards** (performance.yaml) - Optimization and efficiency guidelines
- **Documentation standards** (documentation.yaml) - Technical writing and documentation best practices
- **Coding standards** (coding-standards.yaml) - Code style and structure conventions
- **Review checklist** (review-checklist.yaml) - Pre-merge code review requirements
- **Clarification guidelines** (clarify.yaml) - Requirements clarification procedures
- **Token efficiency** (token-efficiency.md) - Guidelines for minimizing token usage

## When to Use

Agents automatically reference these guidelines when:
- **Iris** - Applies security.yaml for security audits
- **Finn** - Uses qa.yaml and review-checklist.yaml for testing
- **Eden** - Follows documentation.yaml for technical writing
- **Kai** - References performance.yaml and coding-standards.yaml for architecture
- **Blake** - Uses release.yaml for deployment coordination
- **Riley** - Applies clarify.yaml for requirements clarification
- **All agents** - Follow token-efficiency.md to optimize responses

## Usage

Agents can reference specific guidelines:

```markdown
See `skills/core/security.yaml` for security best practices
See `skills/core/qa.yaml` for testing requirements
See `skills/core/token-efficiency.md` for response optimization
```

## File Structure

```
skills/core/
├── SKILL.md (this file)
├── security.yaml          # Security principles
├── qa.yaml                # QA and testing standards
├── release.yaml           # Release management
├── performance.yaml       # Performance optimization
├── documentation.yaml     # Documentation standards
├── coding-standards.yaml  # Code style conventions
├── review-checklist.yaml  # Pre-merge checklist
├── clarify.yaml           # Requirements clarification
└── token-efficiency.md    # Token usage optimization
```

## Best Practices

1. **Consistency** - All agents follow the same core principles
2. **Reference, don't duplicate** - Agents link to guidelines rather than copying them
3. **Update centrally** - Guidelines are maintained in one place
4. **Agent-agnostic** - Principles apply across all specialized agents
5. **Token efficient** - Guidelines are concise and focused

## Integration

These core skills are automatically available to all Orchestra agents. No explicit invocation is needed - agents reference them as part of their standard operating procedures.
