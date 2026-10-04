---
name: ast-grep
description: Structural code search and rewriting using AST patterns. Use when user mentions "ast-grep", "sg", or needs to search codebases using Abstract Syntax Tree patterns, find specific code structures, perform complex queries beyond text search, or rewrite code at scale. Triggers on requests for pattern matching, code analysis, linting rules, or automated refactoring.
allowed-tools: Read, Write, Grep, Glob, Bash(ast-grep:*), Bash(sg:*), WebSearch, WebFetch
---

# ast-grep Skill

Structural code search using AST patterns. Use this skill when text-based search (grep/ripgrep) is insufficient.

## When to Use This Skill

Activate when user asks to:

- Find code patterns with structural constraints ("async functions without try-catch")
- Locate nested or relational code ("await inside loops")
- Search with negation ("functions that don't have X")
- Rewrite code patterns at scale
- Write custom lint rules

**Prefer ast-grep over grep when:**

- Pattern involves parent-child or sibling relationships
- Need "contains X but not Y" logic
- Text matching would have too many false positives

## Workflow

### Step 1: Clarify Requirements

Ask user if unclear:

- What code pattern to find?
- Which programming language?
- Simple match or complex structural query?
- Find only, or also rewrite?

**Supported languages:** JavaScript, TypeScript, TSX, Python, Rust, Go, Java, C, C++, C#, Kotlin, Swift, Ruby, Lua,
HTML, CSS, JSON, YAML

### Step 2: Choose Approach

```
Is it a simple, single-node pattern?
├─ YES → Use `ast-grep run --pattern`
│        Example: ast-grep run --pattern 'console.log($ARG)' --lang javascript .
│
└─ NO → Does it need relational logic (inside/has/precedes/follows)?
        ├─ YES → Create YAML rule with `ast-grep scan --inline-rules`
        │        Consult: references/relational-rules.md
        │
        └─ NO → Does it need composite logic (all/any/not)?
                ├─ YES → Create YAML rule
                │        Consult: references/composite-rules.md
                │
                └─ NO → Use pattern with constraints
                        Consult: references/yaml-config.md
```

### Step 3: Build the Pattern

**For simple patterns:**

```bash
ast-grep run --pattern 'PATTERN' --lang LANGUAGE /path
```

Meta-variable syntax (consult `references/metavariables.md` for details):

- `$VAR` — matches single node
- `$$$VAR` — matches zero or more nodes
- `$_` — matches but doesn't capture

**For complex rules, build YAML:**

```yaml
id: rule-name
language: javascript
rule:
  # Start simple, add complexity
  pattern: TARGET_PATTERN
  # Add relational rules if needed
  inside:
    kind: CONTAINER_KIND
    stopBy: end  # CRITICAL: always use for deep search
```

### Step 4: Test Before Searching

**ALWAYS test the pattern first.** Never run on full codebase without verification.

**Quick inline test:**

```bash
echo "TEST_CODE" | ast-grep scan --inline-rules "id: test
language: LANG
rule:
  RULE_HERE" --stdin
```

**If no matches:**

1. Simplify the rule (remove sub-rules one by one)
2. Check AST structure: `ast-grep run --pattern 'CODE' --lang LANG --debug-query=cst`
3. Verify `kind` names match tree-sitter grammar
4. Ensure `stopBy: end` on all relational rules

**If wrong matches:**

1. Add `constraints` to filter meta-variables
2. Add `not` rules to exclude unwanted patterns
3. Use more specific `kind` instead of `pattern`

Consult `references/atomic-rules.md` for pattern debugging.

### Step 5: Search Codebase

Once pattern works on test code:

```bash
# Simple pattern
ast-grep run --pattern 'PATTERN' --lang LANG /path/to/project

# Complex rule
ast-grep scan --inline-rules "YAML_RULE" /path/to/project

# With JSON output for processing
ast-grep scan --inline-rules "..." --json /path/to/project
```

### Step 6: Rewrite (If Requested)

**Simple rewrite:**

```bash
ast-grep run --pattern 'OLD' --rewrite 'NEW' --lang LANG .
```

**With confirmation:**

```bash
ast-grep run --pattern 'OLD' --rewrite 'NEW' --lang LANG --interactive .
```

**Complex rewrite (YAML):**

```yaml
rule:
  pattern: $OBJ && $OBJ.$PROP
fix: $OBJ?.$PROP
```

Consult `references/yaml-config.md` for transform operations.

## Quick Reference

### CLI Commands

| Command                          | Use When                    |
|----------------------------------|-----------------------------|
| `ast-grep run --pattern`         | Simple single-node search   |
| `ast-grep scan --rule FILE`      | Complex YAML rule from file |
| `ast-grep scan --inline-rules`   | Complex rule without file   |
| `ast-grep run --debug-query=cst` | Debug: see AST structure    |

### Common Patterns

**Find X inside Y:**

```yaml
rule:
  pattern: X
  inside:
    kind: Y
    stopBy: end
```

**Find Y containing X:**

```yaml
rule:
  kind: Y
  has:
    pattern: X
    stopBy: end
```

**Find X but not inside Y:**

```yaml
rule:
  pattern: X
  not:
    inside:
      kind: Y
      stopBy: end
```

**Match alternatives:**

```yaml
rule:
  any:
    - pattern: A
    - pattern: B
```

### Critical Rules

1. **Always use `stopBy: end`** for relational rules (`inside`, `has`, `precedes`, `follows`)
2. **Always test first** — never search full codebase without verifying pattern
3. **Escape `$` in shell** — use `\$VAR` in double quotes or single-quote the YAML
4. **Meta-variables must be entire nodes** — `$VAR` works, `prefix$VAR` doesn't

## Debugging Decision Tree

```
Pattern not matching?
├─ Is pattern valid code? → Test with --debug-query=pattern
├─ Using relational rule without stopBy: end? → Add it
├─ Wrong kind name? → Check with --debug-query=cst
└─ Meta-variable in wrong position? → Consult references/metavariables.md

Wrong matches?
├─ Pattern too broad? → Add kind constraint
├─ Need to exclude cases? → Add not rule
└─ Need to filter captured value? → Add constraints
```

## References

Load these when detailed syntax needed:

| Reference                        | When to Load                         |
|----------------------------------|--------------------------------------|
| `references/rule_reference.md`   | Quick syntax lookup                  |
| `references/atomic-rules.md`     | Pattern/kind/regex not working       |
| `references/relational-rules.md` | inside/has/precedes/follows issues   |
| `references/composite-rules.md`  | all/any/not/matches logic            |
| `references/metavariables.md`    | $VAR capture problems                |
| `references/yaml-config.md`      | Full rule with fix/transform/linting |

## External Resources

- **Playground** (for debugging): https://ast-grep.github.io/playground.html
- **Rule Catalog** (examples): https://ast-grep.github.io/catalog/
- **Official Docs**: https://ast-grep.github.io/
