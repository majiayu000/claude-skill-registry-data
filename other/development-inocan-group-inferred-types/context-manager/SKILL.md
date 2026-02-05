---
name: context-manager
description: Comprehensive context and token usage management for Claude Code. Use this skill when working with large codebases, managing context window budget, optimizing file loading strategies, or when responses indicate context limitations. Helps with token analysis, file organization, query optimization, and context-efficient development workflows.
---

# Context Manager

Skill for managing context window and token usage in Claude Code sessions.

## Overview

Claude Code has a context budget of approximately **190,000 tokens**. This skill helps manage this budget effectively through:
- Token usage analysis and monitoring
- Context-efficient query patterns
- Strategic file loading
- Optimization strategies for large codebases

## Quick Start

### Analyze Current Token Usage

Run the token analysis script to understand context usage:

```bash
python scripts/analyze_tokens.py .
```

This provides:
- Total token count estimation
- Budget usage percentage
- Largest files by token count
- Optimization recommendations

### For Specific Directories or Files

```bash
python scripts/analyze_tokens.py /path/to/directory
python scripts/analyze_tokens.py src/large_file.py
python scripts/analyze_tokens.py . --budget 190000
```

## When to Use This Skill

Use this skill when:
- Starting work on a large codebase (>50 files)
- Noticing performance degradation or incomplete responses
- Planning context-heavy operations (multi-file refactoring)
- Setting up a new project for optimal Claude Code usage
- Claude mentions being near context limits

## Core Principles

### 1. Load Only What's Needed

**DO:**
- Request specific files by name
- Use line ranges for large files: `view(path, [start, end])`
- Load files sequentially for related changes
- Work on one module/component at a time

**DON'T:**
- Load entire directories without filtering
- Keep unnecessary files in context
- Load the same file multiple times
- Request vague "show me everything" queries

### 2. Use Targeted Queries

**Good queries:**
```
"Update the timeout value in config.py line 45 to 30 seconds"
"Show me the login function in auth.py"
"Fix the validation bug in user.py lines 120-135"
```

**Poor queries:**
```
"Help me with this project"
"Load all the code"
"Show me everything related to authentication"
```

### 3. Monitor and Optimize

File size guidelines:
- **Small (<1K tokens)**: Load freely
- **Medium (1-5K tokens)**: Load when needed
- **Large (5-20K tokens)**: Use line ranges
- **Very large (>20K tokens)**: Split or load sections only

Budget zones:
- **Green (<70%)**: Normal operation
- **Yellow (70-85%)**: Be selective
- **Red (>85%)**: Load essentials only, consider reset

## Progressive File Loading

Follow this pattern for efficient context usage:

```
1. Structure → "Show me the project structure"
2. Module → "Show me files in the auth module"  
3. Load → "Load auth.py"
4. Target → "Show me lines 100-150 where the login logic is"
5. Action → "Update line 120 to add validation"
```

## Working with Large Files

### Strategy 1: Line Ranges

Instead of loading entire files:

```python
# Load only relevant section
view("src/api.py", view_range=[100, 200])
view("src/models.py", view_range=[1, 50])
```

### Strategy 2: Progressive Disclosure

```
1. "What functions are in auth.py?"
2. "Show me just the validate_token function"
3. "Now show me where it's called"
```

### Strategy 3: Targeted Modifications

```python
# Precise changes without loading full file
str_replace(
    "Update timeout configuration",
    "config.py",
    old_str="TIMEOUT = 10",
    new_str="TIMEOUT = 30"
)
```

## Context Budget Management

### Understanding Token Distribution

Typical session breakdown:
- System prompts & skills: ~40K tokens (21%)
- Conversation history: ~30K tokens (16%)  
- Available for files: ~120K tokens (63%)

### Monitoring Usage

Run periodic checks:
```bash
# Quick check
python scripts/analyze_tokens.py .

# Detailed analysis with JSON output
python scripts/analyze_tokens.py . --json > token_report.json
```

### Warning Signs

Start a new session or reduce context when:
- Claude asks to see previously loaded files
- Responses become incomplete or generic
- Performance noticeably degrades
- Token usage >85% for multiple messages
- Switching to a completely different feature

## Bash Command Optimization

Commands add output to context. Minimize verbose output:

```bash
# Heavy output ❌
npm install
pip list
git log

# Optimized ✅  
npm install --silent
pip list --format=freeze | head -n 20
git log --oneline -10
```

Use output redirection:
```bash
# Suppress unnecessary output
command > /dev/null 2>&1
command --quiet
command | head -n 20
```

## Project Setup for Context Efficiency

### Step 1: Create Context Guidelines

Add a `.context-notes.md` to your project:

```markdown
## Context Management

### Key Files
- `src/api.py` (large - use line ranges)
- `src/config.py` (small - load freely)

### Context Strategy  
- Work on one module at a time
- Exclude test fixtures (context-heavy)
- Load models individually

### Exclude Patterns
- `data/` directory (large datasets)
- `legacy/` directory (old code)
```

### Step 2: Add Exclusion Patterns

Copy the `.claudeignore` template:

```bash
cp assets/claudeignore-template.txt .claudeignore
```

Edit to add project-specific exclusions.

### Step 3: Organize Code

Structure for selective loading:
```
src/
├── core/       # Core logic (load as needed)
├── api/        # API routes (load by route)
├── models/     # Data models (load individually)
└── utils/      # Utilities (load specific files)
```

Avoid flat structures with many large files.

## Advanced Techniques

### Technique 1: Component-Based Loading

Work on one component at a time:
1. Identify the component
2. Load only relevant files
3. Complete the work
4. Move to next component

### Technique 2: Reference Documentation

For large reference files, create summaries:
- Link to external documentation
- Create concise internal docs
- Use code comments for context

### Technique 3: Context Checkpoints

For long tasks:
1. Summarize progress periodically
2. Start fresh session with minimal context
3. Continue with only essential files loaded

### Technique 4: Split Large Files

When a file exceeds 500-1000 lines:
- Split by functionality
- Separate frequently changed from stable code
- Group by dependencies

Example:
```
Before: api.py (2000 lines, ~15K tokens)

After:
api/
├── routes.py (~2K tokens)
├── handlers.py (~3K tokens)  
├── validation.py (~1.5K tokens)
└── utils.py (~750 tokens)
```

## Reference Documentation

For detailed information, see:

- **[optimization_strategies.md](references/optimization_strategies.md)**: Comprehensive context optimization techniques, file loading best practices, and directory structure guidelines
- **[claude_code_specifics.md](references/claude_code_specifics.md)**: Claude Code-specific patterns, tool usage best practices, and session management strategies
- **[quick_reference.md](references/quick_reference.md)**: Quick reference cheat sheet with token budget rules, essential commands, and common patterns

## Common Patterns

### Pattern 1: Bug Fixing
```
"What file contains the authentication logic?"
"Show me the login function in auth.py"
"Update line 45 to fix the validation check"
```

### Pattern 2: Feature Development
```
"What's the structure of the API routes?"
"Show me an example route handler"
"Create a new /users route following that pattern"
```

### Pattern 3: Refactoring
```
"List files in the models/ directory"
"Load models/user.py"
"Refactor to use dataclasses"
[Repeat for each file]
```

### Pattern 4: Code Review
```
"Review auth.py for security issues (lines 1-100)"
"Now review lines 100-200"
[Continue in sections]
```

## Troubleshooting

### Issue: Context Feels Heavy

**Solutions:**
1. Run `python scripts/analyze_tokens.py .`
2. Start new session if usage >85%
3. Load only essential files
4. Use line ranges for large files

### Issue: Claude Asks for Previously Loaded Files

**Solutions:**
1. Acknowledge context limitations
2. Start fresh session
3. Load files more selectively
4. Use explicit file references

### Issue: Slow Performance

**Solutions:**
1. Check token usage with analysis script
2. Reduce loaded file count
3. Use view ranges instead of full files
4. Exclude unnecessary directories

### Issue: Need to Work on Large File

**Solutions:**
1. Use line ranges to load sections
2. View structure first, then load relevant parts
3. Make targeted str_replace edits
4. Consider splitting if frequently modified

## Best Practices Summary

1. **Analyze first**: Run token analysis before major work
2. **Load selectively**: Request specific files, not directories
3. **Use line ranges**: For files >500 lines
4. **Query precisely**: Targeted questions get targeted responses
5. **Monitor budget**: Check usage regularly
6. **Reset when needed**: Start fresh for new features
7. **Optimize structure**: Organize code for selective loading
8. **Document strategy**: Create project context guidelines
9. **Exclude appropriately**: Use .claudeignore for vendor code
10. **Think incrementally**: One component at a time

## Integration with Development Workflow

### Daily Development
- Quick token check at start: `python scripts/analyze_tokens.py .`
- Work on one module per session
- Use line ranges for large files
- Start fresh session for new features

### Code Reviews
- Load files individually
- Review in sections for large files
- Focus on changed files only

### Refactoring
- Analyze token usage first
- Plan component-by-component approach
- One file at a time
- Test each file before moving on

### Debugging
- Identify relevant files first
- Load only those files
- Use line ranges for context
- Make precise changes

## Additional Resources

Run analysis script with options:
```bash
# Basic analysis
python scripts/analyze_tokens.py .

# Custom budget
python scripts/analyze_tokens.py . --budget 150000

# JSON output for integration
python scripts/analyze_tokens.py . --json

# Exclude additional patterns
python scripts/analyze_tokens.py . --exclude build dist
```
