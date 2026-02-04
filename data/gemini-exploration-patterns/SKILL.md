---
name: gemini-exploration-patterns
description: Strategic patterns for codebase exploration using Gemini's large context window. Covers token thresholds, model routing, and exploration strategies. Use when deciding between Claude and Gemini for exploration, analyzing large codebases, or choosing between Flash and Pro models for context size.
allowed-tools: Read, Glob, Grep, Skill
---

# Gemini Exploration Patterns

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini exploration:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific exploration/context topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

This skill provides strategic guidance for leveraging Gemini CLI's large context window for codebase exploration. It covers when to delegate exploration to Gemini, which model to use, and how to structure outputs for Claude to consume.

## When to Use This Skill

**Keywords:** explore codebase, analyze architecture, large context, token limit, gemini exploration, codebase analysis, when to use gemini, model selection

**Use this skill when:**

- Deciding whether to explore with Claude or Gemini
- Planning a large codebase analysis
- Choosing between Flash and Pro models
- Structuring exploration output for cross-CLI consumption
- Optimizing exploration for cost vs quality

## Token Threshold Decision Matrix

| Codebase Size | Tokens | Recommended Agent | Rationale |
| --- | --- | --- | --- |
| Small | <50K | Claude native | Claude's tools are faster |
| Medium | 50K-500K | Gemini Flash | Good balance of speed/cost |
| Large | 500K-1M | Gemini Flash + chunking | Stay within Flash limits |
| Very Large | 1M-2M | Gemini Pro | Need extended context |
| Massive | >2M | Gemini Pro + progressive | Multi-pass exploration |

### Token Estimation

```bash
# Quick estimation: 1 token ~ 4 characters
chars=$(find . -name "*.ts" -o -name "*.py" | xargs wc -c | tail -1 | awk '{print $1}')
tokens=$((chars / 4))
echo "Estimated tokens: $tokens"
```

### Decision Rule

```text
IF estimated_tokens < 50,000:
    USE Claude's native Explore agent

ELIF estimated_tokens < 1,000,000:
    USE Gemini Flash via /gemini-explore

ELIF estimated_tokens < 2,000,000:
    USE Gemini Pro via /gemini-explore --pro

ELSE:
    USE Progressive exploration (chunk by module)
```

## Model Selection Guide

### Gemini Flash (gemini-2.5-flash)

**Context:** Large (exact limits set by Google, check current API docs)
**Cost:** Lower
**Speed:** Faster

**Best for:**

- Bulk file analysis
- Pattern detection across codebase
- Dependency mapping
- Initial exploration passes
- Log file analysis
- Documentation generation

### Gemini Pro (gemini-2.5-pro)

**Context:** Very large (exact limits set by Google, check current API docs)
**Cost:** Higher
**Speed:** Slower

**Best for:**

- Complex architectural reasoning
- Security-critical analysis
- Nuanced code quality assessment
- Very large codebases (>1M tokens)
- Tasks requiring deep understanding

## Exploration Strategies

### Strategy 1: Full Codebase Sweep

Best for: Understanding overall architecture

```bash
# Collect all source files
find . -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  | xargs cat | gemini "Analyze architecture" --output-format json
```

### Strategy 2: Module-by-Module

Best for: Very large codebases (>2M tokens)

```bash
# Explore each top-level module separately
for dir in src/*/; do
  echo "=== Exploring $dir ==="
  find "$dir" -name "*.ts" | xargs cat | gemini "Analyze this module" --output-format json
done
```

### Strategy 3: Entry-Point Focused

Best for: Understanding execution flow

```bash
# Focus on entry points and their dependencies
cat package.json src/index.ts src/main.ts | gemini "Analyze entry points and startup flow" --output-format json
```

### Strategy 4: Dependency-First

Best for: Understanding relationships

```bash
# Package manifests + import statements
find . -name "package.json" -o -name "requirements.txt" -o -name "go.mod" | xargs cat
grep -r "^import\|^from" src/ | head -1000
```

### Strategy 5: Progressive Depth

Best for: Iterative understanding

1. **Pass 1:** File tree + READMEs only
2. **Pass 2:** Package manifests + configs
3. **Pass 3:** Entry points + main modules
4. **Pass 4:** Deep dive on specific areas

## Output Format Standards

All Gemini exploration outputs should follow this format for Claude consumption:

### YAML Frontmatter (Required)

```yaml
---
generated-by: gemini-cli
model: gemini-2.5-flash
timestamp: 2025-11-30T12:00:00Z
tokens: 150000
scope: architecture|dependencies|patterns|all
---
```

### Machine-Readable Summary (Required)

```json
{
  "type": "exploration",
  "scope": "architecture",
  "tokens_used": 150000,
  "model": "gemini-2.5-flash",
  "key_findings": [
    "Uses Clean Architecture pattern",
    "React frontend with Express backend",
    "PostgreSQL database with Prisma ORM"
  ],
  "files_analyzed": 245,
  "entry_points": ["src/index.ts", "src/server.ts"]
}
```

### Human-Readable Content (Required)

Structured markdown with clear sections:

- **Overview**: 2-3 sentence summary
- **Architecture**: Directory structure, patterns
- **Key Components**: Core modules and responsibilities
- **Dependencies**: External and internal
- **Patterns**: Conventions and style
- **Recommendations**: What to read first, areas of concern

### Recommendations for Claude (Required)

Specific, actionable guidance:

```markdown
## Recommendations for Claude

### Files to Read First
1. `src/index.ts` - Main entry point
2. `src/config/index.ts` - Configuration patterns
3. `CLAUDE.md` - Project conventions

### Patterns to Follow
- Use dependency injection for services
- Follow the existing error handling pattern in `src/errors/`

### Areas of Concern
- Complex state management in `src/store/` - read carefully
- Database migrations in `prisma/migrations/` - check before schema changes
```

## File Filtering Patterns

### Include Patterns

```bash
# Source code
-name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx"
-name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java"

# Configuration
-name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml"

# Documentation
-name "*.md" -o -name "README*"
```

### Exclude Patterns

```bash
-not -path "*/node_modules/*"
-not -path "*/.git/*"
-not -path "*/dist/*"
-not -path "*/build/*"
-not -path "*/__pycache__/*"
-not -path "*/.next/*"
-not -path "*/coverage/*"
-not -path "*/.cache/*"
```

## Cost Optimization

### Reduce Token Usage

1. **Filter aggressively**: Only include relevant file types
2. **Limit file count**: Use `head -500` for file lists
3. **Truncate large files**: Cap individual files at reasonable sizes
4. **Exclude generated code**: dist/, build/, vendor/

### Batch Efficiently

```bash
# Bad: Many small calls
for file in *.ts; do gemini "analyze $file"; done

# Good: One large call
cat *.ts | gemini "analyze all files"
```

## Related Skills

- `gemini-delegation-patterns` - When to delegate any task to Gemini
- `gemini-token-optimization` - Cost optimization strategies
- `gemini-cli-execution` - CLI invocation patterns
- `gemini-workspace-bridge` - Artifact storage and exchange

## Related Commands

- `/gemini-explore` - Execute exploration with standard output
- `/gemini-plan` - Generate implementation plans

## Keyword Registry

| Topic | Keywords |
| --- | --- |
| Token limits | `context window`, `token limit`, `large context` |
| Model selection | `flash vs pro`, `which model`, `model routing` |
| Exploration | `explore codebase`, `analyze architecture`, `understand code` |
| Cost | `reduce tokens`, `optimize cost`, `batch calls` |
| Output | `exploration format`, `cross-cli artifact`, `claude readable` |

## Test Scenarios

### Scenario 1: Token Threshold Decision

**Query**: "Should I use Claude or Gemini to explore this codebase?"
**Expected Behavior**:

- Skill activates on "explore codebase" or "large context"
- Provides token threshold decision matrix
**Success Criteria**: User receives clear guidance based on codebase size

### Scenario 2: Model Selection

**Query**: "Should I use Flash or Pro for codebase analysis?"
**Expected Behavior**:

- Skill activates on "flash vs pro" or "which model"
- Provides model comparison and use cases
**Success Criteria**: User receives model recommendation with rationale

### Scenario 3: Exploration Strategy

**Query**: "How do I analyze a very large codebase with Gemini?"
**Expected Behavior**:

- Skill activates on "very large" or "analyze architecture"
- Provides progressive exploration strategy
**Success Criteria**: User receives module-by-module or chunking approach

## Version History

- v1.1.0 (2025-12-01): Added MANDATORY section, Test Scenarios, Version History
- v1.0.0 (2025-11-25): Initial release
