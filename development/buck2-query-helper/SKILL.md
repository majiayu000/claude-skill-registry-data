---
name: buck2-query-helper
description: Runs common Buck2 queries for dependency analysis, target inspection, and build graph exploration. Use when investigating dependencies, finding reverse dependencies, filtering by rule type, or understanding target relationships in the monorepo.
---

# Buck2 Query Helper

## Overview

This skill provides enhanced Buck2 query capabilities with better formatting, common query shortcuts, and pattern matching. It helps you understand the build graph, analyze dependencies, and investigate target relationships without memorizing complex query syntax.

**Use this skill when:**
- Finding what depends on a target (reverse dependencies)
- Listing all dependencies of a target
- Filtering targets by rule type (all rust_binary, all deno targets, etc.)
- Inspecting target attributes (srcs, deps, visibility)
- Understanding why a target is being built
- Finding cycles in the dependency graph
- Exploring the build graph structure

**This skill provides:**
- `scripts/query_helper.py` - Enhanced query runner with shortcuts
- `references/query_patterns.md` - Common query examples and patterns
- Better formatted output for large query results
- Shortcuts for frequently used queries

## Quick Start

Common queries made simple:

```bash
# Find what depends on a target
python3 scripts/query_helper.py rdeps //src/lib/mylib

# List all dependencies
python3 scripts/query_helper.py deps //src/tools/mytool

# Find all Rust binaries
python3 scripts/query_helper.py kind rust_binary //src/...

# Inspect target attributes
python3 scripts/query_helper.py attrs //src/lib/mylib
```

## Common Query Patterns

### Finding Dependencies

**Direct dependencies:**
```bash
# All direct dependencies
python3 scripts/query_helper.py deps //src/tools/quicktd

# Formatted output with types
python3 scripts/query_helper.py deps --show-kind //src/tools/quicktd
```

**Transitive dependencies:**
```bash
# All transitive dependencies
python3 scripts/query_helper.py deps --transitive //src/tools/quicktd

# Limit depth
python3 scripts/query_helper.py deps --transitive --depth 2 //src/tools/quicktd
```

### Finding Reverse Dependencies

**What depends on this target:**
```bash
# Direct reverse deps
python3 scripts/query_helper.py rdeps //src/lib/common

# Within a specific scope
python3 scripts/query_helper.py rdeps --scope //src/... //src/lib/common

# Show why each target depends on it
python3 scripts/query_helper.py rdeps --explain //src/lib/common
```

### Filtering by Type

**Find targets by rule type:**
```bash
# All Rust binaries
python3 scripts/query_helper.py kind rust_binary //src/...

# All Rust libraries
python3 scripts/query_helper.py kind rust_library //src/...

# All Deno targets
python3 scripts/query_helper.py kind deno //src/tools/...

# Multiple types
python3 scripts/query_helper.py kind "rust_binary|rust_test" //src/...
```

### Inspecting Attributes

**View target configuration:**
```bash
# All attributes
python3 scripts/query_helper.py attrs //src/lib/mylib

# Specific attributes
python3 scripts/query_helper.py attrs --fields srcs,deps //src/lib/mylib

# JSON output for scripting
python3 scripts/query_helper.py attrs --json //src/lib/mylib
```

## Understanding Buck2 Query Language

### Basic Queries

Buck2 queries work on sets of targets:

```bash
# Single target
buck2 query //src/lib:mylib

# All targets in package
buck2 query //src/lib:

# All targets recursively
buck2 query //src/...

# Pattern matching
buck2 query "//src/lib/...:test"  # All targets named 'test'
```

### Query Functions

**deps() - Find dependencies:**
```bash
# Direct dependencies
buck2 query "deps('//src/tools:quicktd')"

# With depth limit (1 = direct deps)
buck2 query "deps('//src/tools:quicktd', 1)"

# Filter results
buck2 query "deps('//src/tools:quicktd') ^ //third-party/..."
```

**rdeps() - Find reverse dependencies:**
```bash
# What depends on this target
buck2 query "rdeps('//src/...', '//src/lib:common')"

# With depth limit
buck2 query "rdeps('//src/...', '//src/lib:common', 1)"
```

**kind() - Filter by rule type:**
```bash
# All Rust binaries
buck2 query "kind('rust_binary', '//src/...')"

# Regex patterns
buck2 query "kind('rust_.*', '//src/...')"
```

**attrfilter() - Filter by attribute:**
```bash
# Targets with specific visibility
buck2 query "attrfilter(visibility, PUBLIC, //src/...)"

# Targets with specific source files
buck2 query "attrfilter(srcs, main.rs, //src/...)"
```

### Set Operations

Combine queries with set operators:

```bash
# Union (either A or B)
buck2 query "//src/lib/... + //src/tools/..."

# Intersection (both A and B)
buck2 query "deps('//src/tools:mytool') ^ //third-party/..."

# Difference (A but not B)
buck2 query "//src/... - //src/tests/..."
```

## Script Usage Guide

### query_helper.py Commands

**deps - Show dependencies:**
```bash
# Basic usage
python3 scripts/query_helper.py deps TARGET

# Options:
--transitive          Include all transitive dependencies
--depth N             Limit to N levels deep
--show-kind          Show rule type for each target
--exclude PATTERN    Exclude targets matching pattern
```

**rdeps - Show reverse dependencies:**
```bash
# Basic usage
python3 scripts/query_helper.py rdeps TARGET

# Options:
--scope PATTERN      Search within this scope (default: //...)
--depth N            Limit to N levels
--explain            Show dependency chain
--show-kind          Show rule type
```

**kind - Filter by type:**
```bash
# Basic usage
python3 scripts/query_helper.py kind TYPE_PATTERN SCOPE

# Examples:
python3 scripts/query_helper.py kind rust_binary //src/...
python3 scripts/query_helper.py kind "rust_.*" //src/...
python3 scripts/query_helper.py kind deno //src/tools/...
```

**attrs - Inspect attributes:**
```bash
# Basic usage
python3 scripts/query_helper.py attrs TARGET

# Options:
--fields F1,F2       Show only specific fields
--json               Output as JSON
--raw                Show raw Buck2 output
```

**path - Find dependency path:**
```bash
# Find how TARGET1 depends on TARGET2
python3 scripts/query_helper.py path TARGET1 TARGET2
```

**cycles - Detect dependency cycles:**
```bash
# Check for cycles in scope
python3 scripts/query_helper.py cycles //src/...
```

## Common Use Cases

### Investigating Build Failures

**Why is this target being built?**
```bash
# Find what pulled it in
python3 scripts/query_helper.py rdeps --explain --scope //src/... //target
```

**What are all the dependencies?**
```bash
# See full dependency tree
python3 scripts/query_helper.py deps --transitive --show-kind //target
```

### Refactoring Analysis

**What will break if I change this?**
```bash
# Find all reverse dependencies
python3 scripts/query_helper.py rdeps //src/lib/old-api

# Limit to specific scope
python3 scripts/query_helper.py rdeps --scope //src/apps/... //src/lib/old-api
```

**Can I make this internal?**
```bash
# See who depends on it
python3 scripts/query_helper.py rdeps //src/lib/maybe-private

# If output is empty or only same package, can make it private
```

### Dependency Auditing

**Find all third-party dependencies:**
```bash
# For a specific target
python3 scripts/query_helper.py deps --transitive //target | grep third-party

# All third-party deps in a scope
buck2 query "deps('//src/...') ^ //third-party/..."
```

**Find unused dependencies:**
```bash
# List all deps
python3 scripts/query_helper.py attrs --fields deps //target

# Compare with actual usage in source files
```

### Performance Investigation

**Find large dependency trees:**
```bash
# Count transitive dependencies
python3 scripts/query_helper.py deps --transitive //target | wc -l

# Compare across targets to find heavy ones
for target in $(buck2 targets //src/tools:); do
  count=$(python3 scripts/query_helper.py deps --transitive $target | wc -l)
  echo "$count $target"
done | sort -rn
```

## Advanced Patterns

### Finding Bottlenecks

Targets with many reverse dependencies might be bottlenecks:

```bash
# Find most depended-on targets
for target in $(buck2 targets //src/lib:); do
  count=$(python3 scripts/query_helper.py rdeps --scope //src/... $target | wc -l)
  echo "$count $target"
done | sort -rn | head -10
```

### Analyzing Test Coverage

```bash
# Find all tests
python3 scripts/query_helper.py kind ".*_test" //src/...

# Find code with no tests
# (targets with no reverse deps that are tests)
```

### Understanding Visibility

```bash
# Who can see this target?
python3 scripts/query_helper.py attrs --fields visibility //target

# Find all PUBLIC targets
buck2 query "attrfilter(visibility, PUBLIC, //src/...)"
```

## Integration with Other Tools

### With Target Determination

```bash
# Find affected tests for changed targets
CHANGED=$(buck2 run root//buck/tools/quicktd -- '@-' '@' //src/...)
for target in $(cat $CHANGED); do
  python3 scripts/query_helper.py rdeps --scope //src/... $target | \
    grep _test
done | sort -u
```

### With jj Version Control

```bash
# Find what changed between commits
jj diff --stat | cut -f2 | while read file; do
  # Find which targets own this file
  buck2 query "owner('$file')"
done | while read target; do
  # Find tests for each target
  python3 scripts/query_helper.py rdeps $target | grep test
done | sort -u
```

## Reference Quick Guide

### Most Common Queries

```bash
# Direct dependencies
buck2 query "deps('//target', 1)"

# All dependencies
buck2 query "deps('//target')"

# Reverse dependencies
buck2 query "rdeps('//...', '//target')"

# Filter by type
buck2 query "kind('rust_binary', '//src/...')"

# Find path between targets
buck2 query "allpaths('//from', '//to')"

# Targets owning files
buck2 query "owner('src/lib/foo.rs')"
```

### Output Formats

```bash
# Default (list of targets)
buck2 query "deps('//target')"

# JSON for scripting
buck2 query "deps('//target')" --json

# Show attributes
buck2 query "deps('//target')" --output-attribute srcs,deps
```

## Troubleshooting

### Query Takes Too Long

**Problem:** Query on `//...` is very slow

**Solutions:**
- Narrow the scope: `//src/...` instead of `//...`
- Use depth limits: `deps('//target', 2)` instead of `deps('//target')`
- Exclude third-party: `deps('//target') - //third-party/...`

### No Results Found

**Problem:** Query returns empty set

**Verify:**
```bash
# Target exists?
buck2 targets //path:target

# Scope includes target?
buck2 targets //scope/...

# Query syntax correct?
buck2 query "kind('type', '//scope/...')"  # Note the quotes
```

### Unexpected Results

**Problem:** Query includes unexpected targets

**Debug:**
```bash
# Use --output-attribute to see why
buck2 query "deps('//target')" --output-attribute deps

# Visualize dependency graph
buck2 query "deps('//target')" --dot | dot -Tpng > deps.png
```

## Tips and Best Practices

1. **Start narrow, expand if needed** - Begin with specific scopes and widen as necessary
2. **Use depth limits** - Especially for rdeps() to avoid massive result sets
3. **Combine with grep** - Filter query results with standard Unix tools
4. **Save common queries** - Create shell aliases for frequently used patterns
5. **Use JSON output for scripting** - More reliable than parsing text output
6. **Visualize complex graphs** - Use `--dot` output with Graphviz for visualization

### Shell Aliases

Add to your shell rc file:

```bash
alias bq='buck2 query'
alias bqdeps='python3 /path/to/scripts/query_helper.py deps'
alias bqrdeps='python3 /path/to/scripts/query_helper.py rdeps'
alias bqkind='python3 /path/to/scripts/query_helper.py kind'
```
