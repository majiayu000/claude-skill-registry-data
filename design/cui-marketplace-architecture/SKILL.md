---
name: cui-marketplace-architecture
description: Architecture rules and validation patterns for Claude Code marketplace components ensuring self-contained skills, proper skill usage, and clean reference patterns
allowed-tools: [Read, Grep, Glob]
---

# CUI Marketplace Architecture Skill

Standards for marketplace component architecture ensuring self-contained skills, proper skill usage in agents/commands, clean reference patterns, and bundle organization principles.

## Workflow

### Step 1: Load Architecture Standards

**CRITICAL**: Load all architecture standards based on validation context.

1. **Always load core architecture rules**:
   ```
   Read: standards/architecture-rules.md
   Read: standards/reference-patterns.md
   ```
   These provide fundamental marketplace architecture principles always needed.

2. **Conditional loading based on context**:

   - If validating skills for self-containment:
     ```
     Read: standards/self-containment-validation.md
     ```

   - If validating agents/commands for skill usage:
     ```
     Read: standards/skill-usage-patterns.md
     ```

   - If calculating compliance scores:
     ```
     Read: standards/scoring-criteria.md
     ```

### Step 2: Apply Architecture Rules

**When to Execute**: During component creation or validation

**What to Validate**:

1. **Skill Self-Containment**:
   - All standards content in skill's standards/ directory
   - No external file references (../../../../)
   - No absolute paths (~/git/cui-llm-rules/)
   - Only external URLs and skill references allowed

2. **Agent/Command Skill Usage**:
   - Agents using standards must invoke Skills
   - Skill tool in tools list if invoking skills
   - No direct standards file references
   - Proper skill invocation pattern in workflow

3. **Reference Pattern Compliance**:
   - Categorize all references (internal/external/skill)
   - Validate allowed patterns only
   - Report prohibited patterns with fixes

4. **Bundle Architecture Compliance**:
   - All bundle skills self-contained
   - All bundle agents use skills properly
   - Bundle follows cohesion principles
   - Components properly organized

### Step 3: Calculate Compliance Scores

**When to Execute**: After validation

**Scoring Logic**:

1. **Skill Self-Containment Score** (0-100):
   - Base: 100 points
   - Deduct 20 points per external file reference
   - Deduct 10 points per documentation-only external ref
   - Minimum: 0

2. **Agent Skill Usage Score** (0-100):
   - Only if agent uses standards
   - Base: 100 points
   - Deduct 30 points if missing Skill in tools
   - Deduct 30 points if no Skill: invocations
   - Deduct 20 points per direct file reference

3. **Bundle Architecture Score**:
   - Weighted average: Skills 60%, Agents 30%, Commands 10%

### Step 4: Generate Fix Recommendations

**When to Execute**: After detecting violations

**Fix Strategies**:

1. **Internalize External Content**:
   - Copy external files to skill/standards/
   - Convert .adoc to .md if needed
   - Update references to internal paths

2. **Convert to Skill Usage**:
   - Add Skill to agent tools list
   - Replace direct refs with Skill: invocations
   - Remove obsolete Read: statements

3. **Remove Documentation Links**:
   - If reference only in ## References section
   - If not actually loaded in workflow
   - Replace with external URL if available

## Common Validation Patterns

### Pattern 1: Validate Skill Self-Containment
```bash
# Scan for external references
grep -E "(\.\.){3,}|~/git/cui-llm-rules" skill/SKILL.md

# Should return nothing for compliant skill
```

### Pattern 2: Check Agent Skill Usage
```bash
# If agent uses standards
grep -i "standard\|pattern" agent.md

# Then verify uses Skill
grep "Skill:" agent.md
grep "tools:.*Skill" agent.md
```

### Pattern 3: Categorize References
```
In ## References section:
✅ https://external-url.com (allowed)
✅ Skill: cui-other-skill (allowed)
✅ standards/internal.md (allowed)
❌ ../../../../standards/external.adoc (prohibited)
```

## Quality Verification

All marketplace components must pass:
- [x] Skills are self-contained (no external refs)
- [x] Agents use Skills (not direct refs)
- [x] Only allowed reference patterns used
- [x] Bundle architecture follows design principles
- [x] All standards content internalized

## References

* Claude Code Plugin System: https://docs.claude.com/en/docs/claude-code/plugins
* Architecture rules: standards/architecture-rules.md
* Reference patterns: standards/reference-patterns.md
* Self-containment validation: standards/self-containment-validation.md
* Skill usage patterns: standards/skill-usage-patterns.md
* Scoring criteria: standards/scoring-criteria.md
