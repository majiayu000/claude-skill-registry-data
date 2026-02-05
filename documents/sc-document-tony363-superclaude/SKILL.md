---
name: sc-document
description: Generate focused documentation for components, functions, APIs, and features. Use when creating inline docs, API references, user guides, or technical documentation.
---

# Documentation Generation Skill

Focused documentation for code, APIs, and features.

## Quick Start

```bash
# Inline documentation
/sc:document src/auth/login.js --type inline

# API reference
/sc:document src/api --type api --style detailed

# User guide
/sc:document payment-module --type guide
```

## Behavioral Flow

1. **Analyze** - Examine component structure and functionality
2. **Identify** - Determine documentation requirements and audience
3. **Generate** - Create appropriate documentation content
4. **Format** - Apply consistent structure and patterns
5. **Integrate** - Ensure compatibility with existing docs

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | inline | inline, external, api, guide |
| `--style` | string | detailed | brief, detailed |

## Evidence Requirements

This skill does NOT require hard evidence. Deliverables are:
- Generated documentation files
- Inline code comments
- API reference materials

## Documentation Types

### Inline (`--type inline`)
- JSDoc/docstring generation
- Parameter and return descriptions
- Function-level comments

### External (`--type external`)
- Standalone documentation files
- Component overviews
- Integration guides

### API (`--type api`)
- Endpoint documentation
- Request/response schemas
- Usage examples

### Guide (`--type guide`)
- User-focused tutorials
- Implementation patterns
- Common use cases

## Style Options

### Brief (`--style brief`)
- Concise descriptions
- Essential information only
- Quick reference format

### Detailed (`--style detailed`)
- Comprehensive explanations
- Extended examples
- Edge case coverage

## Examples

### Inline Code Docs
```
/sc:document src/auth/login.js --type inline
# JSDoc with @param, @returns, @throws
```

### API Reference
```
/sc:document src/api --type api --style detailed
# Full endpoint docs with examples
```

### User Guide
```
/sc:document payment-module --type guide --style brief
# Quick-start tutorial with common patterns
```

### Component Docs
```
/sc:document components/ --type external
# README.md for component library
```

## Tool Coordination

- **Read** - Component analysis
- **Grep** - Reference extraction
- **Write** - Documentation creation
- **Glob** - Multi-file documentation
