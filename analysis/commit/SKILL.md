---
name: commit
description: Use before writing any git commit message or reviewing one, and when the user asks for "commit requirements", "commit message guidelines", "/ar:commit", or "/ar:gc". Carries the 17-step pre-commit analysis, the concrete-subject rules that ban vague verbs and session-internal jargon, and the checks that keep a message reviewable from the repository alone.
aliases: [gc]
---

# Git Commit Requirements

<purpose>

**Third-party repos**: Use `.git/info/exclude` for local-only ignores (e.g., `notes/`) without modifying `.gitignore`.

**IMPORTANT: Read this entire process (steps 1-17) before starting any git commit work and you must carefully re-analyze the actual for regressions and errors and complete each numbered item and sub-item step-by-step.**

</purpose>

---

<requirements>

## Pre-Git Commit Analysis Process

### 1. Command Execution

- `git status` - see all untracked files
- `git diff --staged` - see exactly what changes will be committed
- `git log -5` - see recent commit messages for style consistency and for context

### 2. Complete Change Analysis

Must analyze **ALL commits and changes** that will be included:
- **Not just latest commit** - analyze entire scope
- Both staged and unstaged changes
- All commits from branch divergence point (for PRs)
- Previously staged work, not just immediate changes

### 3. Mandatory Regression Check

Before writing commit message, review `git diff --staged` to ensure:
- Every claim in commit message has evidence in the actual diff
- No assumptions about previous behavior - only describe what the diff shows changed
- Subject line accurately reflects the files and scope of actual changes
- All described functionality changes match what's visible in the code diff
- **If regressions found**: record a task with the harness's task tool and fix it before writing the message

---

## Pre-Git Commit Structure & Format

### 4. Subject Line Format

- **Few/grouped files**: `<files>: concrete description of what specifically changed`
  - Example: `scoped_allow.py,test_scoped_allow.py: accept day units in scope durations`
  - Example: `test_install_*.py: pin tree publication under two processes` (pattern grouping)
  - Example: `plugins/autorun/commands/*.md: run every bash block through uv run --project` (directory grouping)
- **Many files**: `type(scope): concrete description of what specifically changed` (scope can be app name)
  - Example: `fix(installer): retire a hashless legacy tree under --force after a backup`
- **Mixed**: `type(scope) <files>: concrete description`
  - Example: `fix(installer) fs.py: republish a hashless legacy tree after backing it up`
- **Always include**: Concrete and actionable description of what specifically changed
- **Avoid vague terms**: "improve performance" → "hydrate ThreadSafeDB once per session instead of once per hook", "enhance security" → "reject relative export paths in plan_export before writing", "update system" → "default the cache gate to off in its FeatureToggle"

### 5. Message Structure

- **Summary first**: Concise summary line at top (following format above)
- **Previous behavior**: Describe what existed before (based on actual git diff, not assumptions)
- **What changed**: Specific changes made
- **Why**: Rationale for the changes
- **Specific files**: List affected files and what changed in each

---

## Pre-Git Commit Content Requirements

### 6. Concrete & Actionable

- Use specific, measurable descriptions
- Describe functionality that can be tested/verified
- **AVOID vague terms**: "improved", "enhanced", "HYBRID approach", invented jargon
- **USE concrete action words**: "fix", "add", "remove", "enable", "disable"
- **"update" requires specificity**: Use "update X to Y" or "update X by doing Y" - never just "update"
- Include actionable details about what the code now does
- **Show exact changes**: Before/after comparisons with specific file paths, line numbers

### 7. Technical Specificity

- Name specific functions, classes, methods affected
- Include file paths and what changed in each file
- Describe technical implementation details
- Mention configuration changes, new dependencies, etc.

### 8. Accurate Change Classification

- "add" = wholly new feature
- "update X to Y" or "update X by doing Y" = enhancement to existing feature (must specify what changed)
- "fix" = bug fix
- "refactor" = code restructuring
- Must accurately reflect the nature of changes

---

## Pre-Git Commit Context & Documentation

### 9. Complete Context

- Describe both before/after states
- Explain the problem being solved
- Include enough detail for future developers to understand
- Connect changes to overall system architecture
- Show how changes fit into broader development work

### 10. Repository Consistency

- Follow existing commit message style from `git log`
- Match repository's commit message patterns
- Focus on "why" rather than "what" (1-2 sentences for summary)

---

## Pre-Git Commit Security & Quality

### 11. Security Check

Explicitly check for and prevent committing:
- Secrets or API keys
- Passwords or tokens
- Any sensitive information

### 12. Testable Outcomes

- Include specific ways to verify changes work
- Mention new functionality that can be tested
- Reference specific commands or use cases enabled

---

## Pre-Git Commit Validation & Quality Control

### 13. Accuracy Validation Checklist

Before committing, verify:
- [ ] Subject format matches `<files>:`, `type(scope):`, or `type(scope) <files>:` convention
- [ ] Every "previous behavior" claim is supported by git diff evidence
- [ ] All "what changed" statements match actual lines in git diff --staged
- [ ] No claims about functionality that isn't visible in the diff
- [ ] Testable outcomes can be verified by running the described commands
- [ ] File paths and line numbers are accurate
- [ ] Technical details (function names, configurations) match the actual code changes

---

## Pre-Git Development Process Exclusions

### 14. Avoid Development Methodology References

- Don't mention Claude or AI assistance in development process
- Don't mention multi-agent development methodology used to create the code
- Don't describe HOW the code was developed by assistants
- Don't describe conversational changes or internal commit development process
- Focus on WHAT was built and WHY (multi-agent systems as software features are fine)

### 15. Avoid Overconfidence & Vague Language

- **Never use vague qualifiers**: "comprehensive", "complete", "thorough", "HYBRID approach"
- **Don't invent terminology**: Avoid made-up technical terms that aren't standard
- **Avoid abstract descriptions**: Use concrete language instead of conceptual descriptions
- **Don't bury the main point**: Put the key change upfront, not buried in paragraphs
- Avoid absolute claims unless verifiable in the diff
- Don't claim to have "fixed all issues" or "improved everything"
- Use specific, measurable language about actual changes made
- **Balance user impact with technical details**: Describe both what broke/was fixed AND the implementation approach used
- Acknowledge limitations and scope of changes when relevant

### 16. Focus on Commit Outcome vs Process

- Describe the **whole commit outcome** compared to the previous commit state
- Avoid describing incremental conversation steps or iterative development
- Present the final state achieved rather than the journey to get there
- Focus on the complete functional change delivered

---

## Pre-Git Commit Hook Handling

### 17. Hook Integration

- If pre-commit hooks modify files during commit, retry commit ONCE
- If commit succeeds but hooks modified files, MUST amend commit
- Never use interactive git commands (`-i` flag)

</requirements>

---

<pitfalls>

## Common Git Commit Message Pitfalls & Solutions

Based on analysis of problematic commit messages, avoid these common mistakes:

### ❌ Bad Commit Message Patterns

1. **Vague subject lines**: "HYBRID approach", "improve system", "enhance features"
   - **Problem**: Meaningless to someone reading git log
   - **Solution**: Use concrete actions like "fix authentication", "add config validation"

2. **Invented jargon**: Creating terms like "HYBRID approach" that aren't standard
   - **Problem**: Readers can't understand what was actually implemented
   - **Solution**: Use established technical terms or explain new concepts clearly

3. **Missing application context**: Subject could apply to any project
   - **Problem**: Lost context about which application was changed
   - **Solution**: Name the component in the scope or lead with its files: `fix(installer): ...`, `fs.py,traversal.py: ...`

4. **Buried file impact**: Mentioning files deep in message body
   - **Problem**: Hard to understand scope of changes
   - **Solution**: List affected files prominently with brief descriptions

5. **Abstract problem descriptions**: Conceptual language instead of concrete issues
   - **Problem**: Unclear what the fix actually accomplished
   - **Solution**: Describe specific symptoms and measurable outcomes

### ✅ Good Git Commit Message Template

```
type(scope) <files>: [concrete action] [specific component] by [exact method]

Summary: [Concrete action oriented brief high-level description of the change and why it matters]

Previous behavior: [Concrete description of observable behavior and/or limitation(s) being addressed based on git diff]

What changed: [Bulleted list of exact changes with file paths]
- file1.ext: [specific change made]
- file2.ext: [specific change made]

Why: [Root cause explanation in simple terms]

Files affected:
- [list of all modified files with brief description]

Testable: [Specific commands to verify the fix works]
```

This process ensures git commits are **self-documenting**, **technically precise**, **security-conscious**, and **contextually complete** while maintaining proper git workflow practices.

</pitfalls>
