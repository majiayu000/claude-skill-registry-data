---
name: sc-analyze
description: Comprehensive code analysis, quality assessment, and issue diagnosis. Use when analyzing code quality, security vulnerabilities, performance bottlenecks, architecture reviews, or troubleshooting bugs and build failures.
---

# Analysis & Troubleshooting Skill

Multi-domain code analysis with issue diagnosis and resolution capabilities.

## Quick Start

```bash
# Quality analysis
/sc:analyze [target] --focus quality|security|performance|architecture

# Troubleshooting mode
/sc:analyze [issue] --troubleshoot --focus bug|build|performance|deployment

# With auto-fix
/sc:analyze "TypeScript errors" --troubleshoot --focus build --fix
```

## Behavioral Flow

1. **Discover** - Categorize source files, detect languages
2. **Scan** - Apply domain-specific analysis techniques
3. **Evaluate** - Generate prioritized findings with severity
4. **Recommend** - Create actionable recommendations
5. **Report** - Present comprehensive analysis with metrics

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--focus` | string | quality | quality, security, performance, architecture, bug, build, deployment |
| `--troubleshoot` | bool | false | Enable issue diagnosis mode |
| `--trace` | bool | false | Detailed trace analysis for debugging |
| `--fix` | bool | false | Auto-apply safe fixes |
| `--depth` | string | standard | quick, standard, deep |
| `--format` | string | text | text, json, report |

## Analysis Domains

### Quality Analysis
- Code smells and maintainability issues
- Pattern violations and anti-patterns
- Technical debt assessment

### Security Analysis
- Vulnerability scanning
- Compliance validation
- Authentication/authorization review

### Performance Analysis
- Bottleneck identification
- Resource utilization patterns
- Optimization opportunities

### Architecture Analysis
- Component coupling assessment
- Dependency analysis
- Design pattern evaluation

## Troubleshooting Mode

When `--troubleshoot` is enabled:

| Focus | Behavior |
|-------|----------|
| bug | Error analysis, stack traces, code inspection |
| build | Build logs, dependencies, config validation |
| performance | Metrics analysis, bottleneck identification |
| deployment | Environment analysis, service validation |

## Examples

### Security Deep Dive
```
/sc:analyze src/auth --focus security --depth deep
```

### Build Failure Fix
```
/sc:analyze "compilation errors" --troubleshoot --focus build --fix
```

### Performance Diagnosis
```
/sc:analyze "slow API response" --troubleshoot --focus performance --trace
```

## Tool Coordination

- **Glob** - File discovery and structure analysis
- **Grep** - Pattern analysis and code search
- **Read** - Source inspection and config analysis
- **Bash** - External tool execution
- **Write** - Report generation
