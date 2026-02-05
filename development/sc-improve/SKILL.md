---
name: sc-improve
description: Apply systematic improvements to code quality, performance, maintainability, and cleanup. Use when refactoring code, optimizing performance, removing dead code, or improving project structure.
---

# Code Improvement & Cleanup Skill

Systematic improvements with multi-persona expertise and safety validation.

## Quick Start

```bash
# Quality improvement
/sc:improve src/ --type quality --safe

# Performance optimization
/sc:improve api-endpoints --type performance

# Dead code cleanup
/sc:improve src/ --cleanup --type code --safe

# Import optimization
/sc:improve --cleanup --type imports
```

## Behavioral Flow

1. **Analyze** - Examine codebase for improvement opportunities
2. **Plan** - Choose approach and activate relevant personas
3. **Execute** - Apply systematic improvements
4. **Validate** - Ensure functionality preservation
5. **Document** - Generate improvement summary

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | quality | quality, performance, maintainability, style, code, imports, files, all |
| `--cleanup` | bool | false | Enable cleanup mode |
| `--safe` | bool | true | Conservative with safety validation |
| `--aggressive` | bool | false | Thorough cleanup (use with caution) |
| `--preview` | bool | false | Show changes without applying |
| `--interactive` | bool | false | Guided decision mode |

## Personas Activated

- **architect** - Structure and design improvements
- **performance** - Optimization expertise
- **quality** - Code quality and maintainability
- **security** - Security pattern application

## MCP Integration

- **PAL MCP** - Consensus validation for complex changes
- **Rube MCP** - Follow-up coordination (tickets, notifications)

## Evidence Requirements

This skill requires evidence. You MUST:
- Show before/after code comparisons
- Run tests to verify functionality preservation
- Report metrics (lines removed, complexity reduction)

## Improvement Types

### Quality (`--type quality`)
- Technical debt reduction
- Code structure improvements
- Readability enhancements

### Performance (`--type performance`)
- Bottleneck resolution
- Algorithm optimization
- Resource efficiency

### Maintainability (`--type maintainability`)
- Complexity reduction
- Documentation improvements
- Modular restructuring

### Style (`--type style`)
- Formatting consistency
- Naming conventions
- Pattern alignment

## Cleanup Mode (`--cleanup`)

### Code Cleanup (`--type code`)
- Dead code detection and removal
- Unused variable elimination
- Unreachable code removal

### Import Cleanup (`--type imports`)
- Unused import removal
- Import organization
- Dependency optimization

### File Cleanup (`--type files`)
- Empty file removal
- Orphaned file detection
- Structure optimization

### Full Cleanup (`--type all`)
- Comprehensive cleanup
- All categories combined
- Multi-persona coordination

## Safety Modes

### Safe Mode (`--safe`)
- Conservative changes only
- Automatic safety validation
- Preserves all functionality

### Aggressive Mode (`--aggressive`)
- Thorough cleanup
- Framework-aware patterns
- Requires careful review

## Examples

### Safe Quality Improvement
```
/sc:improve src/ --type quality --safe
# Technical debt reduction with safety validation
```

### Performance Optimization
```
/sc:improve api-endpoints --type performance --interactive
# Guided optimization with profiling analysis
```

### Dead Code Cleanup
```
/sc:improve src/ --cleanup --type code --safe
# Remove unused code with dependency validation
```

### Preview Changes
```
/sc:improve --cleanup --type imports --preview
# Show what would be removed without executing
```

## Tool Coordination

- **Read/Grep/Glob** - Code analysis
- **Edit/MultiEdit** - Safe modifications
- **TodoWrite** - Progress tracking
- **Task** - Large-scale improvement delegation
