---
name: writing-skills
description: Creates and refines agent skills using TDD methodology with pressure testing and rationalization detection. Use when creating new skills, editing existing skills, testing skills with pressure scenarios, or verifying skills work before deployment.
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Personal skills live in agent-specific directories (`~/.claude/skills` for Claude Code, `~/.codex/skills` for Codex)** 

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand wrangler:practicing-tdd before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

**Official guidance:** For Anthropic's official skill authoring resources, see references/anthropic-resources.md for links to live documentation maintained by Anthropic.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools.

**Skills are:** Reusable techniques, patterns, tools, reference guides
**Skills are NOT:** Narratives about specific problem-solving sessions

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:** Not intuitively obvious, reusable across projects, broadly applicable
**Don't create for:** One-offs, standard practices, project-specific (use CLAUDE.md)

**Skill types:** Technique (concrete steps), Pattern (mental model), Reference (API docs)

## Directory Structure

```
skills/skill-name/
├── SKILL.md              # Required: Main skill content
├── templates/            # Optional: Template files for the skill
├── scripts/              # Optional: Executable scripts
├── references/           # Optional: Heavy reference material (100+ lines)
└── assets/               # Optional: Diagrams, config files, images
```

**Key principles:**
- Flat namespace (no nested skill directories)
- Keep principles and small code patterns (<50 lines) inline in SKILL.md
- Use subdirectories only when content is too large for inline inclusion
- Reference files should be loaded progressively, not automatically

## SKILL.md Structure

**Frontmatter:** `name` (letters, numbers, hyphens) and `description` (third-person, "Use when..." triggers). Max 1024 chars.

```markdown
---
name: skill-name
description: Use when [triggers] - [what it does]
---
# Skill Name
## Overview
Core principle in 1-2 sentences.
## When to Use
Symptoms and use cases
## Quick Reference
Table for common operations
## Implementation
Inline code or link to file
## Common Mistakes
What goes wrong + fixes
```

## Claude Search Optimization (CSO)

### 1. Rich Description Field

Start with "Use when..." for triggering conditions. Use concrete triggers/symptoms, describe problems not language-specific details, third person.

```yaml
# ❌ BAD: Too abstract
description: For async testing

# ✅ GOOD: Concrete trigger + what it does
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests
```

### 2. Keyword Coverage

Use words Claude would search for:
- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Tools: Actual commands, library names, file types

### 3. Descriptive Naming

Verb-first (creating-skills not skill-creation). Name by what you DO or core insight. Gerunds work well for processes.

### 4. Token Efficiency

Target: getting-started <150 words, frequently-loaded <200 words, others <500 words. Move details to tool help, use cross-references, compress examples, eliminate redundancy.

### 5. Cross-Referencing

Use skill name with explicit requirement markers: "REQUIRED: Use wrangler:practicing-tdd". Don't use @ links (force-loads context).

## Flowchart Usage

Use ONLY for: Non-obvious decision points, process loops, "A vs B" decisions.

Never for: Reference material (tables), code examples (markdown), linear instructions (lists).

See assets/graphviz-conventions.dot for style rules.

## Code Examples

One excellent example beats many mediocre ones. Choose relevant language, make it complete and runnable, comment WHY not what. Single language only.

## File Organization

Choose your organization strategy based on skill complexity and token efficiency:

### Self-Contained (Recommended Default)
**When:** Simple skills, <200 lines, no heavy reference material
**Structure:** Everything in SKILL.md
**Benefits:** Single file, fastest discovery

### Progressive Disclosure
**When:** Skills >300 lines, complex workflows, heavy reference docs
**Structure:** SKILL.md + references/ or templates/
**Benefits:** Frequently-needed content in SKILL.md, defer rarely-needed details

### With Executable Tools
**When:** Skill provides reusable code/scripts
**Structure:** SKILL.md + scripts/ or templates/
**Benefits:** Code can be directly used

### Decision Criteria

**Stay self-contained when**:
- Total content <200 lines
- All content is frequently needed
- No distinct "reference" vs "guidance" split

**Use progressive disclosure when**:
- SKILL.md would exceed 300 lines
- Skill has multiple distinct aspects (e.g., overview + API reference + examples)
- Reference material is heavy but rarely needed (API docs, lookup tables)
- Some content is "getting started" vs "advanced usage"

**Token efficiency considerations**:
- Only frequently-loaded content "costs" tokens in practice
- SKILL.md loads when skill is invoked
- Additional files load only when explicitly referenced
- Heavy reference material (>100 lines) should be in references/
- Templates should be in templates/, not inline

**Reference**: https://code.claude.com/docs/en/skills for progressive disclosure patterns

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Applies to NEW skills AND EDITS.

Write skill before testing? Delete it. Start over.

**No exceptions:** Not for "simple additions", "just adding a section", or "documentation updates". Don't keep untested changes as "reference". Delete means delete.

**REQUIRED BACKGROUND:** wrangler:practicing-tdd skill.

## Testing All Skill Types

Different skill types need different test approaches:

**Discipline Skills** (TDD, verification): Test with pressure scenarios combining time + sunk cost + exhaustion. Success = agent follows rule under maximum pressure.

**Technique Skills** (condition-based-waiting, tracing-root-causes): Test with application scenarios and variations. Success = agent applies technique correctly to new scenario.

**Pattern Skills** (reducing-complexity): Test with recognition and counter-examples. Success = agent knows when/how to apply pattern.

**Reference Skills** (API docs): Test retrieval and application. Success = agent finds and uses information correctly.

## Common Rationalizations for Skipping Testing

| Excuse | Reality |
|--------|---------|
| "Skill is obviously clear" | Clear to you ≠ clear to other agents. Test it. |
| "It's just a reference" | References can have gaps, unclear sections. Test retrieval. |
| "Testing is overkill" | Untested skills have issues. Always. 15 min testing saves hours. |
| "I'll test if problems emerge" | Problems = agents can't use skill. Test BEFORE deploying. |
| "Too tedious to test" | Testing is less tedious than debugging bad skill in production. |
| "I'm confident it's good" | Overconfidence guarantees issues. Test anyway. |
| "Academic review is enough" | Reading ≠ using. Test application scenarios. |
| "No time to test" | Deploying untested skill wastes more time fixing it later. |

**All of these mean: Test before deploying. No exceptions.**

## Bulletproofing Skills Against Rationalization

Skills that enforce discipline (like TDD) need to resist rationalization. Agents are smart and will find loopholes when under pressure.

**Psychology note:** Understanding WHY persuasion techniques work helps you apply them systematically. See references/persuasion-principles.md for research foundation (Cialdini, 2021; Meincke et al., 2025) on authority, commitment, scarcity, social proof, and unity principles.

### Close Every Loophole Explicitly

Don't just state rules - forbid specific workarounds. Add "No exceptions: Don't keep as 'reference', don't adapt, delete means delete."

Add foundational principle early: "Violating the letter of the rules is violating the spirit of the rules."

### Build Rationalization Table

Capture rationalizations from baseline testing (see Testing section below). Every excuse agents make goes in the table:

```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
```

### Create Red Flags List

Make it easy for agents to self-check when rationalizing:

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

### Update CSO for Violation Symptoms

Add to description: symptoms of when you're ABOUT to violate the rule:

```yaml
description: use when implementing any feature or bugfix, before writing implementation code
```

## RED-GREEN-REFACTOR for Skills

Follow the TDD cycle:

### RED: Write Failing Test (Baseline)

Run pressure scenario with subagent WITHOUT the skill. Document exact behavior:
- What choices did they make?
- What rationalizations did they use (verbatim)?
- Which pressures triggered violations?

This is "watch the test fail" - you must see what agents naturally do before writing the skill.

### GREEN: Write Minimal Skill

Write skill that addresses those specific rationalizations. Don't add extra content for hypothetical cases.

Run same scenarios WITH skill. Agent should now comply.

### REFACTOR: Close Loopholes

Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

**Testing details below** - see Testing Skills section for complete methodology:
- How to write pressure scenarios
- Pressure types (time, sunk cost, authority, exhaustion)
- Plugging holes systematically
- Meta-testing techniques

## Anti-Patterns

### ❌ Narrative Example
"In session 2025-10-03, we found empty projectDir caused..."
**Why bad:** Too specific, not reusable

### ❌ Multi-Language Dilution
example-js.js, example-py.py, example-go.go
**Why bad:** Mediocre quality, maintenance burden

### ❌ Code in Flowcharts
```dot
step1 [label="import fs"];
step2 [label="read file"];
```
**Why bad:** Can't copy-paste, hard to read

### ❌ Generic Labels
helper1, helper2, step3, pattern4
**Why bad:** Labels should have semantic meaning

## STOP: Before Moving to Next Skill

After writing ANY skill, STOP and complete the deployment process.

**Do NOT:**
- Batch create skills without testing each
- Move to next skill before verification
- Skip testing for "efficiency"

Deployment checklist below is MANDATORY for EACH skill.

## Skill Creation Checklist (TDD Adapted)

**RED:** Create pressure scenarios (3+ pressures) → Run WITHOUT skill → Document rationalizations → Identify patterns

**GREEN:** Name (letters/numbers/hyphens) → Frontmatter (name + "Use when..." description, max 1024 chars) → Clear overview → Address RED failures → Code inline or link → One excellent example → Run WITH skill, verify compliance

**REFACTOR:** Identify NEW rationalizations → Add explicit counters → Build rationalization table → Create red flags → Re-test until bulletproof

**Quality:** Flowchart if non-obvious, quick reference table, common mistakes, no narrative, supporting files only for tools/heavy reference

**Deploy:** Commit to git, consider PR if broadly useful

## Discovery Workflow

Encounters problem → Finds skill (description matches) → Scans overview → Reads quick reference → Loads example if implementing. Put searchable terms early.

## Testing Skills

Create pressure scenarios (3+ combined pressures: time, sunk cost, authority) → Run WITHOUT skill → Document rationalizations → Write skill to counter those specific rationalizations → Re-test → Plug new holes → Repeat until bulletproof.

**Detailed methodology**: See `references/testing-methodology.md` for complete pressure scenario patterns, verification process, and bulletproofing techniques.

## The Bottom Line

Creating skills IS TDD for process documentation.

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).

If you follow TDD for code, follow it for skills.
