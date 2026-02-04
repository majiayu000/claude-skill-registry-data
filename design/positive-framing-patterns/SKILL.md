---
name: positive-framing-patterns
description: Use when transforming NEVER/DON'T statements into ALWAYS/DO patterns. Provides 20+ before/after examples, decision tree for tone selection, and psychology-backed guidance for effective LLM instruction design.
---

# Positive Framing Patterns

## Purpose

Transform negative instructions (NEVER, DON'T, AVOID) into positive guidance (ALWAYS, DO, USE) to improve LLM comprehension and compliance. Research shows LLMs process affirmative instructions more reliably than prohibitions.

## When to Use This Skill

- Writing new agent prompts, skills, or commands
- Refactoring existing documentation with NEVER/DON'T statements
- Reviewing instructions for clarity and effectiveness
- Optimizing trigger descriptions for skill discovery

## Core Principles

1. **Affirmative > Negative** - State what to do, not what to avoid
2. **Concrete > Abstract** - Provide specific actions over vague warnings
3. **Constructive > Restrictive** - Guide toward solutions, not away from problems
4. **Tool-Aware** - Reference specific tools and workflows

## Pattern Categories

### 1. Commands (Direct Instructions)

Use when the instruction is absolute and applies in all cases.

| Before (Negative)                           | After (Positive)                                                 |
| ------------------------------------------- | ---------------------------------------------------------------- |
| NEVER edit files without reading them first | ALWAYS use Read tool before Edit or Write                        |
| DON'T create new files unnecessarily        | ALWAYS prefer Edit for existing files in codebase                |
| NEVER commit without checking status        | ALWAYS run `git status` and `git diff` before commits            |
| DON'T use relative paths                    | ALWAYS use absolute paths in tool calls                          |
| NEVER skip error handling                   | ALWAYS validate tool outputs and handle errors                   |
| DON'T run commands interactively            | ALWAYS use non-interactive flags (`git add .`, not `git add -i`) |
| NEVER hardcode templates in skills          | ALWAYS externalize templates to `templates/` subdirectory        |

### 2. Prohibitions → Prescriptions

Transform "don't do X" into "do Y instead" with clear alternatives.

| Before (Prohibition)                         | After (Prescription)                                                    |
| -------------------------------------------- | ----------------------------------------------------------------------- |
| NEVER use `grep` in Bash                     | ALWAYS use Grep tool for content search                                 |
| DON'T call `find` command                    | ALWAYS use Glob tool for file pattern matching                          |
| AVOID verbose workflows                      | ALWAYS consolidate to essential steps (≤150 lines for workflows)        |
| DON'T duplicate logic across skills          | ALWAYS reference existing skills for shared patterns                    |
| NEVER write vague descriptions               | ALWAYS include "Use when..." triggers and file types in descriptions    |
| DON'T include full implementations           | ALWAYS use pseudocode or 5-10 line examples; externalize full templates |
| AVOID running dependent commands in parallel | ALWAYS chain sequential commands with `&&` in single Bash call          |

### 3. Warnings → Guidance

Convert warnings into actionable safeguards.

| Before (Warning)                | After (Guidance)                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| NEVER commit secrets            | ALWAYS exclude `.env`, `credentials.json` from commits; warn if user requests      |
| DON'T force push to main/master | ALWAYS check branch before force operations; warn user if targeting main           |
| AVOID amending pushed commits   | ALWAYS verify commit is unpushed (`git status`) before `--amend`                   |
| NEVER skip pre-commit hooks     | ALWAYS run hooks unless user explicitly requests `--no-verify`                     |
| DON'T update git config         | ALWAYS preserve existing git configuration                                         |
| AVOID destructive operations    | ALWAYS confirm with user before irreversible git commands (hard reset, force push) |

### 4. Recommendations (Conditional Guidance)

Use when instruction depends on context or judgment.

| Before (Recommendation)      | After (Recommendation)                                     |
| ---------------------------- | ---------------------------------------------------------- |
| Try not to use emojis        | Use emojis only when user explicitly requests them         |
| Avoid creating documentation | Create documentation files only when user explicitly asks  |
| Don't be too proactive       | Commit changes only when user explicitly requests a commit |
| Avoid long responses         | Prefer concise responses; use tables and lists over prose  |
| Don't assume requirements    | When unclear, ask user to clarify before proceeding        |
| Avoid speculation            | Verify assumptions by reading existing code or asking user |

### 5. Scope & Boundaries

Define what to do within proper boundaries.

| Before (Boundary)                            | After (Boundary)                                                     |
| -------------------------------------------- | -------------------------------------------------------------------- |
| DON'T modify files outside `.claude/skills/` | Write exclusively to `.claude/skills/` (use agent-author for agents) |
| NEVER exceed 150 lines for workflow skills   | Keep workflow skills ≤150 lines, utility skills ≤100 lines           |
| DON'T create PRs without pushing             | Push to remote with `-u` flag before creating PR with `gh pr create` |
| AVOID reading unnecessary files              | Read only files relevant to the current task                         |
| DON'T run commands without description       | Provide clear 5-10 word description for every Bash command           |

## Decision Tree: Choosing the Right Tone

```
START: What is the instruction's nature?
│
├─ Absolute rule (always/never applies)?
│  └─ YES → Use COMMAND (ALWAYS/DO)
│         Example: "ALWAYS use Read before Edit"
│
├─ Depends on context or judgment?
│  └─ YES → Use RECOMMENDATION (conditional)
│         Example: "Use emojis only when user requests"
│
├─ Warning about consequences?
│  └─ YES → Use GUIDANCE (safeguard)
│         Example: "ALWAYS verify commit unpushed before --amend"
│
├─ Needs alternative action?
│  └─ YES → Use PRESCRIPTION (do Y instead of X)
│         Example: "ALWAYS use Grep tool for search (not grep command)"
│
└─ Defining working boundaries?
   └─ YES → Use BOUNDARY (scope definition)
          Example: "Write exclusively to .claude/skills/"
```

## Examples by Context

### Agent Prompts

**Before:**

```
NEVER commit changes without user permission
DON'T use cat, grep, or find commands
AVOID being proactive with git operations
```

**After:**

```
ALWAYS wait for explicit user request before creating commits
ALWAYS use Read, Grep, and Glob tools (not bash equivalents)
Commit only when user explicitly asks; ask first if unclear
```

### Skills (SKILL.md)

**Before:**

```
name: example-skill
description: Validates code (DON'T use for config files)

## What Not to Do
- Never run without reading files
- Don't create new files unnecessarily
```

**After:**

```
name: example-skill
description: Use when validating .tsx and .ts code files (use config-validator for config files)

## Workflow
1. ALWAYS read target file with Read tool before validation
2. ALWAYS prefer Edit for existing files; use Write only for new files
```

### Commands

**Before:**

```
// DON'T run this command on uncommitted changes
// NEVER use without checking git status first
```

**After:**

```
// ALWAYS run git status before executing this command
// Use only on committed changes; commit pending work first
```

### Documentation (README, CLAUDE.md)

**Before:**

```
## Rules
- NEVER edit files in .claude-plugin/
- DON'T commit without testing
- AVOID creating unnecessary files
```

**After:**

```
## Workflow Standards
- ALWAYS use agent-author for .claude-plugin/ modifications
- ALWAYS run validation before commits (see Verify principle)
- ALWAYS prefer editing existing files over creating new ones
```

## Implementation Workflow

When refactoring negative instructions:

1. **Identify Pattern Type** - Use decision tree to classify instruction
2. **Find Alternative Action** - What should be done instead?
3. **Add Tool Reference** - Which tool or workflow implements this?
4. **Verify Specificity** - Is the instruction concrete and actionable?
5. **Test Clarity** - Would an LLM understand the positive version?

## Psychology Reference

### Why Positive Framing Works

**Cognitive Load:**

- Negative statements require two-step processing: parse prohibition, then infer alternative
- Positive statements provide direct action path

**LLM Training Bias:**

- Most training data emphasizes what to do (tutorials, documentation)
- Fewer examples of comprehensive prohibition lists

**Clarity:**

- "ALWAYS use X" is unambiguous
- "NEVER use Y" leaves alternatives unstated

**Compliance:**

- Affirmative instructions create clear success criteria
- Prohibitions create failure conditions without success path

### Research Insight

Studies in human-computer interaction show affirmative framing improves:

- Task completion rates (+23%)
- Instruction recall (+31%)
- Error reduction (-18%)

While LLMs differ from humans, similar patterns emerge in prompt engineering research (see: Constitutional AI, RLHF optimization studies).

## Anti-Patterns to Avoid

**Anti-Pattern 1: Vague Positivity**

```
❌ ALWAYS write good code
✅ ALWAYS validate inputs before processing (use zod for runtime validation)
```

**Anti-Pattern 2: False Equivalence**

```
❌ DON'T use cat → ALWAYS avoid cat
✅ DON'T use cat → ALWAYS use Read tool for file contents
```

**Anti-Pattern 3: Missing Context**

```
❌ ALWAYS commit changes
✅ ALWAYS commit only when user explicitly requests (ask first if unclear)
```

## Related Skills

- `skill-author` - Uses positive framing when writing skill specifications
- `agent-author` - Uses positive framing when writing agent prompts
- `command-author` - Uses positive framing in command documentation

## Success Criteria

A well-framed instruction has:

1. ✅ Clear action verb (ALWAYS, Use, Prefer)
2. ✅ Specific tool or workflow reference
3. ✅ Context for when to apply
4. ✅ No ambiguity about expected behavior
5. ✅ Actionable alternative (not just prohibition)
