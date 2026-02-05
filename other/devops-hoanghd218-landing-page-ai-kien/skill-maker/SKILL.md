---
name: skill-maker
description: Use when creating new skills or editing existing skills - combines official skill authoring best practices with TDD methodology (test with subagents before deployment, iterate until bulletproof). Activates when user wants to create/update a skill that extends Claude's capabilities.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Skill Maker

## Overview

**Creating skills IS Test-Driven Development applied to process documentation.**

This skill combines official Anthropic skill authoring best practices with TDD methodology. Write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

## What is a Skill?

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

**Skills provide:**
1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex tasks

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once, one-off solutions, or project-specific conventions

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit
- You want to ensure consistent behavior across Claude instances

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put those in project CLAUDE.md)

## Skill Types

### Technique
Concrete method with steps to follow (testing patterns, refactoring workflows)

### Pattern
Way of thinking about problems (architectural approaches, design principles)

### Reference
API docs, syntax guides, tool documentation (library references, command docs)

### Discipline-Enforcing
Rules and requirements (TDD enforcement, code quality standards)

---

## Skill Anatomy

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required, lowercase-with-hyphens)
│   │   ├── description: (required, max 1024 chars)
│   │   └── allowed-tools: (optional, restricts tool access)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded as needed
    └── assets/           - Files used in output (templates, icons)
```

### SKILL.md (required)

**Frontmatter requirements:**
- `name`: Letters, numbers, hyphens only (max 64 chars)
- `description`: Third-person, includes BOTH what it does AND when to use it (max 1024 chars)
- `allowed-tools`: Optional list restricting tool access for safety

**Writing style:** Use **imperative/infinitive form** (verb-first instructions), not second person
- ✅ Good: "To accomplish X, do Y"
- ❌ Bad: "You should do X"

### Bundled Resources (optional)

#### Scripts (`scripts/`)
**When to include:** When the same code is rewritten repeatedly or deterministic reliability is needed
- Token efficient (not loaded unless referenced)
- Deterministic behavior
- May be executed without loading into context
- Example: `scripts/rotate_pdf.py`

#### References (`references/`)
**When to include:** For documentation that Claude should reference while working
- Database schemas, API documentation
- Domain knowledge, company policies
- Detailed workflow guides
- Keeps SKILL.md lean (<5k words)
- **Best practice:** If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication:** Information should live in either SKILL.md or references, not both

#### Assets (`assets/`)
**When to include:** Files used within the output Claude produces
- Templates, images, icons
- Boilerplate code (React templates, HTML starters)
- Sample documents
- Not loaded into context, just used directly

### Progressive Disclosure Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words, keep lean)
3. **Bundled resources** - As needed by Claude (scripts, references, assets)

---

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.
Edit skill without testing? Same violation.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Delete means delete

---

## RED-GREEN-REFACTOR for Skills

Follow the TDD cycle adapted for documentation:

### RED: Write Failing Test (Baseline)

Run pressure scenario WITHOUT the skill. Document exact behavior:
- What choices did the agent make?
- What rationalizations did they use (verbatim)?
- Which pressures triggered violations?

**How to test:**
1. Create a new conversation/subagent
2. Present a scenario that would benefit from the skill
3. Apply pressure (time constraints, sunk cost, complexity)
4. Document failures, workarounds, rationalizations

This is "watch the test fail" - you must see what agents naturally do before writing the skill.

### GREEN: Write Minimal Skill

Write skill that addresses those specific rationalizations. Don't add extra content for hypothetical cases.

Run same scenarios WITH skill present. Agent should now comply.

**Verification:**
1. Create a new conversation with skill loaded
2. Run identical scenarios
3. Agent should follow skill guidance
4. Document any new violations

### REFACTOR: Close Loopholes

Agent found new rationalization? Add explicit counter. Re-test until bulletproof.

**For discipline-enforcing skills:**
- Build rationalization table from all test iterations
- Create "Red Flags" list of common violations
- Add explicit "No exceptions" counters
- Address "spirit vs letter" arguments upfront

---

## Skill Creation Process

### Step 1: Understanding with Concrete Examples

To create an effective skill, clearly understand concrete examples of how it will be used.

**Ask questions like:**
- "What functionality should this skill support?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"
- "Are there other ways you imagine this skill being used?"

**Avoid overwhelming:** Ask most important questions first, follow up as needed.

**Conclude when:** Clear sense of the functionality the skill should support.

**UltraThink Skill Design:**
Before creating skill structure, activate deep thinking:

> 🗣 Say: "Let me ultrathink what this skill should really accomplish and how it fits the ecosystem."

**Question fundamentals:**
- Is this really a skill, or project-specific documentation?
- What's the reusable pattern vs. one-off solution?
- How will future Claude discover and activate this skill?
- What could go wrong if agents misinterpret this skill?
- Are we solving the right problem?
- What similar skills exist, and how does this differ?
- What are we NOT including, and why?

**For discipline-enforcing skills, ultrathink:**
- What rationalizations will agents use to circumvent this?
- How can we make the "right thing" the easy thing?
- What pressure scenarios will test this skill?

**After UltraThink:** Create skill that addresses reusable patterns with clear activation triggers.

### Step 2: Planning Reusable Contents

For each concrete example, analyze:
1. How would you execute this from scratch?
2. What scripts, references, and assets would help when executing repeatedly?

**Examples:**

**PDF editing:** "Rotate this PDF"
- Analysis: Rotating requires re-writing same code each time
- Resource: `scripts/rotate_pdf.py`

**BigQuery queries:** "How many users logged in today?"
- Analysis: Requires re-discovering table schemas each time
- Resource: `references/schema.md`

**Frontend apps:** "Build me a todo app"
- Analysis: Requires same boilerplate HTML/React each time
- Resource: `assets/hello-world/` template

### Step 3: Initialize Skill Structure

Create skill directory manually:

```bash
mkdir -p dev-workflow/skills/skill-name/{scripts,references,assets}
```

Create `SKILL.md` with frontmatter template:

```markdown
---
name: skill-name
description: Use when [specific triggers] - [what it does and how it helps]
allowed-tools: Read, Write, Edit, Glob, Grep  # Adjust as needed
---

# Skill Name

## Overview
[Core principle in 1-2 sentences]

## When to Use
[Activation triggers and symptoms]
[When NOT to use]

## [Main content sections]
...
```

### Step 4: Baseline Testing (RED Phase)

**BEFORE writing skill content:**

1. Create pressure scenarios (3+ combined pressures for discipline skills)
2. Run scenarios WITHOUT skill present
3. Document baseline behavior verbatim:
   - What did agent do?
   - What rationalizations did they use?
   - What mistakes were made?

**Pressure types:**
- Time constraints ("quickly", "urgent")
- Sunk cost ("already spent X hours")
- Authority ("the client insists")
- Exhaustion ("we're almost done, just...")

### Step 5: Write Skill Content (GREEN Phase)

Answer these three questions in SKILL.md:

1. **What is the purpose?** (A few sentences in Overview)
2. **When should it be used?** (Activation triggers)
3. **How should Claude use it?** (Procedural instructions, reference bundled resources)

**Address specific baseline failures** identified in RED phase.

**Structure recommendation:**

```markdown
## Overview
Core principle

## When to Use
- Trigger 1
- Trigger 2
- When NOT to use

## Core Pattern/Process
[Main methodology or workflow]

## Quick Reference
[Table or bullets for scanning]

## Implementation/Examples
[Inline code or link to separate file]

## Common Mistakes
What goes wrong + fixes

## Red Flags (for discipline skills)
- Flag 1
- Flag 2
```

### Step 6: Verify Testing (GREEN Phase)

Run same scenarios WITH skill present:
- Agent should now comply with guidance
- Document any new violations or gaps
- Verify skill addresses original baseline failures

### Step 7: Close Loopholes (REFACTOR Phase)

For each new violation:
1. Identify the rationalization
2. Add explicit counter in skill
3. Re-test until bulletproof

**For discipline-enforcing skills, add:**

**Rationalization Table:**
```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
```

**Red Flags Section:**
```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**
```

**Principle Statement:**
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

### Step 8: Iteration

After deploying:
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Run baseline tests again (RED phase)
5. Update skill (GREEN phase)
6. Verify fixes (REFACTOR phase)

---

## Claude Search Optimization (CSO)

**Critical for discovery:** Future Claude needs to FIND your skill.

### 1. Rich Description Field

**Format:** Start with "Use when..." to focus on triggering conditions

**Content:**
- Use concrete triggers, symptoms, and situations
- Describe the *problem* not language-specific symptoms
- Keep triggers technology-agnostic unless skill is tech-specific
- Write in third person

```yaml
# ❌ BAD: Too abstract, doesn't include when to use
description: For async testing

# ❌ BAD: First person
description: I can help you with async tests when they're flaky

# ✅ GOOD: Starts with "Use when", describes problem and solution
description: Use when tests have race conditions or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests

# ✅ GOOD: Technology-specific with explicit trigger
description: Use when using React Router and handling authentication redirects - provides patterns for protected routes and auth state management
```

### 2. Keyword Coverage

Use words Claude would search for:
- Error messages: "Hook timed out", "race condition"
- Symptoms: "flaky", "hanging", "inconsistent"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown"
- Tools: Actual commands, library names, file types

### 3. Descriptive Naming

**Use active voice, verb-first:**
- ✅ `creating-skills` not `skill-creation`
- ✅ `testing-async-code` not `async-code-testing`
- ✅ `condition-based-waiting` not `waiting-conditions`

**Gerunds (-ing) work well for processes:**
- `creating-skills`, `testing-skills`, `debugging-with-logs`

### 4. Token Efficiency

**Target word counts:**
- Frequently-loaded skills: <500 words
- Other skills: <1000 words (still be concise)
- Getting-started workflows: <200 words

**Techniques:**

**Move details to references:**
```markdown
# ❌ BAD: All details in SKILL.md
[50 lines of API documentation]

# ✅ GOOD: Reference external file
For complete API documentation, see references/api-docs.md
```

**Cross-reference skills:**
```markdown
# ❌ BAD: Repeat workflow details
When testing, follow these 20 steps...

# ✅ GOOD: Reference other skill
Use test-driven-development skill for testing workflow.
```

**Compress examples:**
- One excellent example beats many mediocre ones
- Complete and runnable
- Well-commented explaining WHY
- From real scenario

---

## Testing Different Skill Types

### Discipline-Enforcing Skills

**Examples:** TDD enforcement, code quality requirements

**Test with:**
- Academic questions: Do they understand the rules?
- Pressure scenarios: Do they comply under stress?
- Multiple pressures combined: time + sunk cost + exhaustion

**Success criteria:** Agent follows rule under maximum pressure

### Technique Skills

**Examples:** Refactoring patterns, debugging workflows

**Test with:**
- Application scenarios: Can they apply correctly?
- Variation scenarios: Do they handle edge cases?
- Missing information tests: Do instructions have gaps?

**Success criteria:** Agent successfully applies technique to new scenario

### Pattern Skills

**Examples:** Architectural approaches, design principles

**Test with:**
- Recognition scenarios: Do they recognize when pattern applies?
- Application scenarios: Can they use the mental model?
- Counter-examples: Do they know when NOT to apply?

**Success criteria:** Agent correctly identifies when/how to apply pattern

### Reference Skills

**Examples:** API documentation, command references

**Test with:**
- Retrieval scenarios: Can they find the right information?
- Application scenarios: Can they use what they found correctly?
- Gap testing: Are common use cases covered?

**Success criteria:** Agent finds and correctly applies reference information

---

## File Organization Patterns

### Self-Contained Skill
```
skill-name/
  SKILL.md    # Everything inline
```
**When:** All content fits, no heavy reference needed

### Skill with Reusable Tool
```
skill-name/
  SKILL.md    # Overview + patterns
  helpers.ts  # Working code to adapt
```
**When:** Tool is reusable code, not just narrative

### Skill with Heavy Reference
```
skill-name/
  SKILL.md         # Overview + workflows
  references/
    api-docs.md    # 600 lines API reference
    schemas.md     # 500 lines database schemas
  scripts/
    helper.py      # Executable tools
```
**When:** Reference material too large for inline

---

## Common Rationalizations for Skipping Testing

| Excuse | Reality |
|--------|---------|
| "Skill is obviously clear" | Clear to you ≠ clear to other agents. Test it. |
| "It's just a reference" | References can have gaps. Test retrieval. |
| "Testing is overkill" | Untested skills have issues. Always. 15 min testing saves hours. |
| "I'll test if problems emerge" | Problems = agents can't use skill. Test BEFORE deploying. |
| "Too tedious to test" | Testing is less tedious than debugging bad skill in production. |
| "I'm confident it's good" | Overconfidence guarantees issues. Test anyway. |
| "Academic review is enough" | Reading ≠ using. Test application scenarios. |
| "No time to test" | Deploying untested skill wastes more time fixing it later. |

**All of these mean: Test before deploying. No exceptions.**

---

## Skill Creation Checklist

Use TodoWrite to create todos for EACH checklist item below.

**RED Phase - Write Failing Test:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill - document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase - Write Minimal Skill:**
- [ ] Name uses only letters, numbers, hyphens (max 64 chars)
- [ ] YAML frontmatter with name, description, allowed-tools (max 1024 chars total)
- [ ] Description starts with "Use when..." and includes specific triggers/symptoms
- [ ] Description written in third person
- [ ] Keywords throughout for search (errors, symptoms, tools)
- [ ] Clear overview with core principle
- [ ] Address specific baseline failures identified in RED
- [ ] Code inline OR link to separate file
- [ ] One excellent example (not multi-language)
- [ ] Run scenarios WITH skill - verify agents now comply

**REFACTOR Phase - Close Loopholes:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table from all test iterations
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Quality Checks:**
- [ ] Overview answers: What? When? How?
- [ ] Quick reference table or bullets
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference
- [ ] Token count <500 words for frequent skills, <1000 for others

**Deployment:**
- [ ] Commit skill to git
- [ ] Update skill documentation if needed
- [ ] Consider adding slash command if skill warrants it

---

## Anti-Patterns to Avoid

### ❌ Narrative Example
"In session 2025-10-03, we found empty projectDir caused..."
**Why bad:** Too specific, not reusable

### ❌ Multi-Language Dilution
example-js.js, example-py.py, example-go.go
**Why bad:** Mediocre quality, maintenance burden

### ❌ Generic Labels
helper1, helper2, step3, pattern4
**Why bad:** Labels should have semantic meaning

### ❌ Untested Skills
Writing skill without baseline testing
**Why bad:** Guarantees issues in production use

### ❌ Vague Descriptions
"Helps with coding tasks"
**Why bad:** Claude won't know when to activate it

---

## Integration with Dev-Workflow

Skills created with this skill-maker should integrate with dev-workflow ecosystem:

**Leverage existing skills:**
- Use `test-driven-development` for testing methodology examples
- Use `code-quality` for code review patterns
- Use `documentation` for documentation examples
- Use `brainstorming` for design exploration patterns

**Consider activation context:**
- When should skill activate in the workflow?
- Does it fit planning, implementation, or quality phase?
- Should it auto-activate or require explicit invocation?

**Tool restrictions:**
- Planning skills: `Read, Write, Glob, Grep` (docs only)
- Implementation skills: `Read, Write, Edit, Glob, Grep, Bash` (full access)
- Quality skills: `Read, Grep, Glob` (analysis only)

---

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).
Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation.
