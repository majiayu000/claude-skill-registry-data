---
name: command-audit
description: Validates command frontmatter, delegation patterns, simplicity guidelines, and documentation proportionality. Use when reviewing, auditing, analyzing, evaluating, improving, or fixing commands, validating official frontmatter (description, argument-hint, allowed-tools, model), checking delegation clarity or standalone prompts, assessing simplicity guidelines (6-15 simple, 25-80 documented), validating argument handling, or assessing documentation appropriateness. Distinguishes official Anthropic requirements from custom best practices. Also triggers when user asks about command best practices, whether a command should be a skill instead, or needs help with command structure.
allowed-tools: [Read, Grep, Glob, Bash]
---

## Reference Files

Command validation guidance (official requirements + custom best practices):

**Quick Start**:

- [INDEX.md](INDEX.md) - **Start here**: Navigation guide mapping
  use cases to reference files
- [audit-checklist.md](audit-checklist.md) - Quick validation
  checklist for rapid reviews
- [audit-workflow-steps.md](audit-workflow-steps.md) - Complete
  7-step audit process

**Detailed Validation**:

- [frontmatter-validation.md](frontmatter-validation.md) - Official
  Anthropic frontmatter features and validation rules (OFFICIAL)
- [delegation-patterns.md](../../references/delegation-patterns.md) -
  Delegation clarity and target selection validation (BEST PRACTICE)
- [simplicity-enforcement.md](simplicity-enforcement.md) -
  Simplicity vs complexity assessment and skill migration criteria (GUIDELINES)
- [argument-handling.md](argument-handling.md) - Argument parsing
  patterns and default value validation (BEST PRACTICE)
- [documentation-proportionality.md](documentation-proportionality.md) -
  Documentation level appropriateness (minimal vs full) (BEST PRACTICE)

**Common Issues & Reporting**:

- [common-issues-and-antipatterns.md](common-issues-and-antipatterns.md) -
  9 frequent issues with examples and fixes
- [report-format.md](report-format.md) - Standardized audit report
  structure and template
- [examples.md](examples.md) - Good vs poor command comparisons and
  full audit reports

---

## Official Requirements vs Custom Best Practices

This auditor validates both **official Anthropic requirements** and **custom best practices**:

**Official Anthropic Requirements** (from Claude Code documentation):

- **Frontmatter features**: `description` (required), `argument-hint`, `allowed-tools`, `model`, `disable-model-invocation` (optional)
- **Command patterns**: Delegation OR standalone prompts OR bash execution (!) OR file references (@)
- **Multiple valid patterns**: Commands can delegate to skills/agents OR provide inline instructions
- **No official line count limits**: Simplicity is conceptual, not numeric

**Custom Best Practices** (recommended patterns from this codebase):

- **Delegation clarity**: Descriptive delegation to skills/agents using natural language (preferred pattern)
- **Simplicity guidelines**: 6-15 lines (simple), 25-80 lines (documented) - guidelines not hard limits
- **Documentation proportionality**: Match documentation level to command complexity
- **Single responsibility**: One clear purpose per command
- **Argument handling**: Pass user input to delegation targets or use in instructions

**Audit reports will distinguish** between violations of official requirements (CRITICAL) and deviations from custom best practices (IMPORTANT or NICE-TO-HAVE).

---

# Command Auditor

Validates command configurations for delegation clarity, simplicity, and
documentation proportionality.

## Quick Start

**New to command auditing?** Start with
[INDEX.md](INDEX.md) for navigation guidance.

**For quick validation**: Use
[audit-checklist.md](audit-checklist.md)

**For comprehensive audit**: Follow the 7-step process in
[audit-workflow-steps.md](audit-workflow-steps.md):

1. Read command file
2. Validate frontmatter features (description required, optional fields valid)
3. Identify command pattern (delegation, standalone prompt, bash, file
   reference)
4. Assess simplicity guidelines (6-15 simple, 25-80 documented)
5. Validate argument handling
6. Check documentation proportionality
7. Decide: Should this be a skill instead?
8. Generate audit report

**Common issues?** See
[common-issues-and-antipatterns.md](common-issues-and-antipatterns.md)
for 9 frequent problems with fixes.

## Command-Specific Validation

### Delegation Clarity

**Assessment criteria**:

1. **Target explicit**: Clearly names agent/skill
2. **Invocation clear**: Uses Task/Skill tool
3. **Arguments passed**: Delegates user input
4. **Single responsibility**: One delegation target

**Red flags**:

- No explicit target ("do some analysis")
- Multiple delegations in one command
- Complex logic instead of delegation

### Simplicity Guidelines

**File size guidelines** (not hard limits):

- **6-15 lines**: Typical simple command (frontmatter + minimal content)
- **25-80 lines**: Typical documented command (frontmatter + docs + content)
- **>80 lines**: Consider skill migration (evaluate complexity)

**Complexity indicators**:

- Line count >80
- Multiple tool calls
- If/else logic
- Loop constructs
- Extensive processing

### Argument Handling

**Patterns**:

**Pass-through**:

```markdown
{Task prompt="$ARGUMENTS"}
```

**With defaults**:

```markdown
{Task prompt="${ARGUMENTS:-default value}"}
```

**Positional**:

```markdown
{Task prompt="File: $1, Action: $2"}
```

**Validation**:

- Arguments are used (not ignored)
- Defaults make sense
- Usage documented (for documented commands)

### Documentation Proportionality

**Simple commands**: Minimal docs

- Name and description in frontmatter
- Optional: One-line explanation
- No usage section, no examples

**Documented commands**: Full docs

- Name and description in frontmatter
- Usage section with syntax
- "What It Does" explanation
- Examples section
- Optional: Tips or notes

**Rule**: Documentation should match complexity

See
[documentation-proportionality.md](documentation-proportionality.md)
for detailed guidelines and examples.

## Integration with audit-coordinator

**Invocation pattern**:

```text
User: "Audit my command"
→ audit-coordinator invokes command-auditor
→ command-auditor performs specialized validation
→ Results returned to audit-coordinator
→ Consolidated with claude-code-evaluator findings
```

**Sequence**:

1. command-auditor (primary) - Command-specific validation
2. claude-code-evaluator (secondary) - General structure validation

**Report compilation**:

- command-auditor findings (delegation, simplicity, arguments, docs)
- claude-code-evaluator findings (frontmatter, markdown, structure)
- Unified report with reconciled priorities

## Examples

For complete command examples and full audit reports, see
[examples.md](examples.md).

**Quick examples**:

- **Good command**: audit-bash (8 lines, clear delegation, proper arguments,
  minimal docs)
- **Needs work**: 95-line command with unclear delegation, ignored arguments,
  excessive docs

Each example in the reference file includes status, findings, scores, and
specific fixes.

---

For detailed guidance on each validation area, consult the reference files linked at the top of this document.
