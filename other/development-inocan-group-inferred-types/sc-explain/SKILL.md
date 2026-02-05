---
name: sc-explain
description: Provide clear explanations of code, concepts, and system behavior with educational clarity. Use when understanding code, learning concepts, or knowledge transfer.
---

# Code & Concept Explanation Skill

Educational explanations with adaptive depth and format.

## Quick Start

```bash
# Basic code explanation
/sc:explain authentication.js --level basic

# Framework concept
/sc:explain react-hooks --level intermediate --context react

# System architecture
/sc:explain microservices-system --level advanced --format interactive
```

## Behavioral Flow

1. **Analyze** - Examine target code or concept
2. **Assess** - Determine audience level and depth
3. **Structure** - Plan explanation with progressive complexity
4. **Generate** - Create clear explanations with examples
5. **Validate** - Verify accuracy and educational effectiveness

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--level` | string | intermediate | basic, intermediate, advanced |
| `--format` | string | text | text, examples, interactive |
| `--context` | string | - | Domain context (react, security, etc.) |

## Personas Activated

- **educator** - Learning-optimized explanations
- **architect** - System design context
- **security** - Security practice explanations

## MCP Integration

- **PAL MCP** - Cross-perspective validation for complex topics

## Evidence Requirements

This skill does NOT require hard evidence. Focus on:
- Clear, accurate explanations
- Appropriate examples
- Progressive complexity

## Explanation Levels

### Basic (`--level basic`)
- Foundational concepts
- Simple examples
- Beginner-friendly language

### Intermediate (`--level intermediate`)
- Implementation details
- Common patterns
- Best practices

### Advanced (`--level advanced`)
- Deep technical details
- Edge cases and trade-offs
- Performance implications

## Format Options

### Text (`--format text`)
- Written explanations
- Step-by-step breakdowns
- Conceptual overviews

### Examples (`--format examples`)
- Code samples
- Before/after comparisons
- Real-world applications

### Interactive (`--format interactive`)
- Progressive disclosure
- Follow-up suggestions
- Exploration paths

## Examples

### Code Explanation
```
/sc:explain src/auth/jwt.js --level basic
# What the code does, how it works, why it's structured this way
```

### Framework Concept
```
/sc:explain useEffect --level intermediate --context react
# Hook lifecycle, dependency arrays, cleanup patterns
```

### Architecture Explanation
```
/sc:explain event-driven-architecture --level advanced
# Patterns, trade-offs, implementation strategies
```

### Security Concept
```
/sc:explain oauth2-flow --level basic --context security
# Authorization flow, tokens, security considerations
```

## Tool Coordination

- **Read/Grep/Glob** - Code analysis
- **TodoWrite** - Multi-part explanation tracking
- **Task** - Complex explanation delegation
