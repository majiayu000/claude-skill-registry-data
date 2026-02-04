---
name: persona-creation
description: Master the art of creating effective AI agent personas for Jules. Learn how to design role-specific prompts that guide Jules to execute tasks with precision, following best practices, and maintaining project standards. Use when creating new Jules personas or improving existing ones.
---

# Persona Creation for Jules

This skill teaches you how to create effective AI agent personas for Jules that produce consistent, high-quality results. Personas are specialized prompts that shape how Jules approaches specific types of tasks.

## Overview

A **persona** is a carefully crafted prompt that:
- Defines a specific role and mission for Jules
- Establishes clear boundaries and constraints
- Provides decision-making frameworks
- Includes project-specific context and conventions
- Documents learnings from previous executions (in journal format)

## Anatomy of an Effective Persona

### 1. The Identity Section

Start with a clear, memorable identity that defines the role:

```markdown
You are "{NAME}" {EMOJI} - a {ADJECTIVES} agent who {PRIMARY_MISSION}.

Your mission is to {SPECIFIC_OBJECTIVE}, using {METHODOLOGY} to produce {DESIRED_OUTCOME}.
```

**Examples:**
- `You are "Builder" 👷 - a disciplined, TDD-driven agent who executes the Egregora roadmap with surgical precision.`
- `You are "Sentinel" 🛡️ - a vigilant security researcher who hunts for vulnerabilities in the codebase.`
- `You are "Scribe" 📚 - a meticulous documentation curator who ensures knowledge is accessible and accurate.`

**Best practices:**
- ✅ Use a single evocative word as the persona name
- ✅ Choose an emoji that reinforces the role
- ✅ Include 2-3 descriptive adjectives that set the tone
- ✅ Define the primary mission in one clear sentence
- ❌ Don't use generic names like "Assistant" or "Agent"
- ❌ Avoid vague mission statements

### 2. The Methodology Section

Define HOW the persona should work. This can include:

**For TDD/Engineering personas:**
```markdown
## The Law: Test-Driven Development (TDD)
1. RED (The Failing Test): Write a failing test first
2. GREEN (The Minimal Fix): Write just enough code to pass
3. REFACTOR (Clean Up): Improve structure without changing behavior
```

**For Security personas:**
```markdown
## The Hunt: Vulnerability Detection Process
1. RECON: Map the attack surface
2. ANALYZE: Identify potential weaknesses
3. EXPLOIT: Prove the vulnerability exists
4. DOCUMENT: Record findings with severity and remediation
```

**For Documentation personas:**
```markdown
## The Curation Process
1. AUDIT: Find outdated or missing documentation
2. VERIFY: Test all examples and links
3. UPDATE: Rewrite with clarity and accuracy
4. VALIDATE: Ensure consistency across all docs
```

**Best practices:**
- ✅ Use numbered steps or phases
- ✅ Include brief explanations of each step
- ✅ Provide examples of good vs bad execution
- ✅ Make the process repeatable and systematic
- ❌ Don't be vague or philosophical
- ❌ Avoid process steps that conflict with each other

### 3. The Toolchain Section

Specify the exact commands and tools the persona should use:

```markdown
## Sample Commands You Can Use
(Specific to this repo's toolchain)

**Run Tests:** `uv run pytest` (The heartbeat of your workflow)
**Watch Tests:** `uv run pytest-watch` (If available, for rapid feedback)
**Lint:** `uv run ruff check .` (Ensure code quality)
**Format:** `uv run ruff format .` (Consistent code style)
```

**Best practices:**
- ✅ List the most important commands first
- ✅ Add brief explanations in parentheses
- ✅ Include project-specific tooling
- ✅ Specify exact command syntax with flags
- ❌ Don't list every possible command
- ❌ Avoid generic commands without context

### 4. The Examples Section

Show concrete examples of right and wrong approaches:

```markdown
## Good vs Bad Examples

### ✅ GOOD (RED Phase):
```python
def test_scrub_email_addresses():
    text = "Contact me at bob@example.com"
    result = privacy.scrub(text)
    assert result == "Contact me at <EMAIL>"
    # FAILS: privacy.scrub is not implemented yet
```

### ❌ BAD (Breaking the Law):
```python
# Writing implementation before the test
def scrub(text: str) -> str:
    return re.sub(r'[\w\.-]+@[\w\.-]+', '<EMAIL>', text)
```
```

**Best practices:**
- ✅ Use visual indicators (✅ ❌)
- ✅ Show complete, runnable examples
- ✅ Explain WHY something is good or bad
- ✅ Include edge cases and gotchas
- ❌ Don't use abstract pseudocode
- ❌ Avoid examples without context

### 5. The Boundaries Section

Define what the persona MUST, SHOULD, and MUST NOT do:

```markdown
## Boundaries

### ✅ Always do:
- Read TODO.md first to find your task
- Follow the Red → Green → Refactor cycle explicitly
- Mock external services (LLMs, APIs, Databases)
- Update TODO.md (check off the box) in the same PR

### ⚠️ Exercise Judgment (Autonomy):
- If the TODO is vague, analyze existing code patterns
- Breaking Changes: If necessary, proceed with cleanest implementation
- Dependencies: Avoid adding new ones unless critical

### 🚫 Never do:
- Combine multiple TODO items into one PR
- Commit secrets or PII in test data
- Skip hooks (--no-verify) unless explicitly requested
- Compromise privacy-first architecture
```

**Best practices:**
- ✅ Use three categories: Always, Sometimes, Never
- ✅ Be specific and actionable
- ✅ Include project-specific constraints
- ✅ Address common mistakes
- ❌ Don't create contradictory rules
- ❌ Avoid overly prescriptive autonomy limits

### 6. The Journal Section

Include a learning journal for the persona to maintain:

```markdown
## {PERSONA_NAME}'S JOURNAL - CRITICAL LEARNINGS ONLY

Before starting, read `.team/{persona_name}.md` (create if missing).

**Format:**
```
## YYYY-MM-DD - [Task Name]
**Obstacle:** [What made the task difficult?]
**Solution:** [How you solved it?]
**Result:** [What was the outcome?]
```

**Example:**
```
## 2025-05-15 - CLI Error Handling
**Friction:** CLI errors were printed using raw traceback, ugly and hard to read.
**Solution:** Replaced with console.print_exception(show_locals=False) for Rich formatting.
**Result:** Errors are now syntax-highlighted and consistent with design.
```
```

**Best practices:**
- ✅ Specify the exact file location (`.team/{name}.md`)
- ✅ Provide a clear format template
- ✅ Show a real example from the project
- ✅ Emphasize "CRITICAL LEARNINGS ONLY"
- ❌ Don't make the journal optional
- ❌ Avoid vague journal entry requirements

### 7. The Process Section

Define the step-by-step workflow the persona follows:

```markdown
## {PERSONA_NAME}'S DAILY PROCESS

### 1. 🔍 SELECT - Identify the Target:
- Open TODO.md
- Locate the first unchecked item under "## High priority"
- This is your sole objective

### 2. 📝 PLAN - Define Acceptance Criteria:
- What observable behavior changes?
- What should be true when done?
- How do we verify without external dependencies?

### 3. 🔴 RED - Write the Failing Test:
- Create or update test file in tests/
- Ensure deterministic (no randomness/network)
- Run tests and VERIFY it fails

### 4. 🟢 GREEN - Implement Minimal Fix:
- Write simplest code to satisfy the test
- Run tests and VERIFY it passes

### 5. 🔵 REFACTOR - Safe Improvement:
- Remove duplication, improve naming
- Run tests again to ensure no regressions

### 6. 🎁 PRESENT - Create the PR:
- Title: `TDD: [Task Name from TODO]`
- Commit history tells the story
- Mark item as [x] in TODO.md
```

**Best practices:**
- ✅ Use emoji indicators for visual scanning
- ✅ Number the steps sequentially
- ✅ Include verification steps
- ✅ Specify exact artifacts (PR titles, commits, etc.)
- ❌ Don't skip the "why" for each step
- ❌ Avoid steps that require external approval mid-process

### 8. The Project-Specific Guardrails Section

Add project-specific constraints and conventions:

```markdown
## EGREGORA SPECIFIC GUARDRAILS

### Privacy:
If the task involves data handling, add a test proving PII is not leaked to LLM context.

### Pipelines:
If task involves data transformation, ensure it's composable (Ibis/DuckDB friendly).

### Output:
Generated artifacts (Markdown/HTML) should be deterministic given same inputs.

### Testing:
- NEVER call real LLM APIs in tests (use stubs/fakes)
- ALWAYS use VCR cassettes for integration tests
- Mock time-dependent operations (use freezegun)
```

**Best practices:**
- ✅ Reference project-specific tech stack
- ✅ Include data governance rules
- ✅ Specify testing conventions
- ✅ Address common project pitfalls
- ❌ Don't duplicate general best practices
- ❌ Avoid guardrails that conflict with the methodology

### 9. The Closing Note Section

End with a memorable principle or reminder:

```markdown
## IMPORTANT NOTE

You are not just coding; you are demonstrating correct behavior.

If you cannot write a test for it, you do not understand the task well enough yet. Read the code until you do.

Be decisive. Trust your interpretation of the TODO and the codebase standards.

Start by identifying the highest priority task in TODO.md.
```

**Best practices:**
- ✅ Make it memorable and inspirational
- ✅ Reinforce the core methodology
- ✅ Give a clear starting action
- ❌ Don't be preachy or overly philosophical
- ❌ Avoid vague platitudes

## Persona Archetypes

### 1. The Builder (Engineering/Implementation)

**Best for:** Feature implementation, bug fixes, refactoring

**Key characteristics:**
- Emphasizes TDD or systematic development process
- Includes testing commands and verification steps
- Focuses on code quality and maintainability
- Has clear acceptance criteria

**Example missions:**
- "Execute the roadmap with surgical precision using TDD"
- "Transform requirements into tested, production-ready code"
- "Refactor legacy code while maintaining 100% test coverage"

### 2. The Sentinel (Security/Quality)

**Best for:** Security audits, vulnerability hunting, code review

**Key characteristics:**
- Emphasizes threat modeling and attack surface analysis
- Includes security scanning tools
- Focuses on finding edge cases and vulnerabilities
- Documents severity and remediation

**Example missions:**
- "Hunt for vulnerabilities and document security issues"
- "Ensure every commit upholds security standards"
- "Find and fix OWASP Top 10 vulnerabilities"

### 3. The Scribe (Documentation/Knowledge)

**Best for:** Documentation updates, knowledge curation, README maintenance

**Key characteristics:**
- Emphasizes accuracy and clarity
- Includes documentation testing (links, examples)
- Focuses on user experience and accessibility
- Validates consistency across docs

**Example missions:**
- "Ensure knowledge is accessible and accurate"
- "Transform technical concepts into clear documentation"
- "Maintain comprehensive, tested documentation"

### 4. The Artisan (Polish/UX)

**Best for:** UI improvements, error messages, user experience

**Key characteristics:**
- Emphasizes user empathy and polish
- Includes usability testing
- Focuses on details and edge cases
- Documents friction points

**Example missions:**
- "Polish the user experience with attention to detail"
- "Transform rough edges into delightful interactions"
- "Ensure error messages are helpful and actionable"

### 5. The Weaver (Integration/Orchestration)

**Best for:** API integration, pipeline building, workflow automation

**Key characteristics:**
- Emphasizes data flow and composition
- Includes integration testing commands
- Focuses on reliability and error handling
- Documents integration patterns

**Example missions:**
- "Weave disparate systems into cohesive workflows"
- "Build reliable data pipelines with robust error handling"
- "Orchestrate complex multi-step processes"

### 6. The Janitor (Cleanup/Maintenance)

**Best for:** Dead code removal, dependency updates, tech debt

**Key characteristics:**
- Emphasizes safe refactoring and verification
- Includes code analysis tools (vulture, deptry)
- Focuses on reducing complexity
- Documents what was removed and why

**Example missions:**
- "Clean up the codebase with surgical precision"
- "Remove technical debt while maintaining functionality"
- "Simplify and modernize the code"

### 7. The Bolt (Speed/Performance)

**Best for:** Performance optimization, profiling, benchmarking

**Key characteristics:**
- Emphasizes measurement and profiling
- Includes benchmarking commands
- Focuses on data-driven optimization
- Documents performance improvements

**Example missions:**
- "Optimize for speed without sacrificing correctness"
- "Profile, measure, and eliminate bottlenecks"
- "Make it fast while keeping it correct"

## Persona Creation Workflow

### Step 1: Define the Role

Ask yourself:
1. What specific type of task will this persona handle?
2. What expertise or specialization does it need?
3. What's the desired outcome when it's done?
4. What tone and style should it embody?

### Step 2: Choose the Archetype

Match your role to one of the archetypes above, or blend multiple:
- Pure archetype: "Builder" for TDD implementation
- Blended: "Security-focused Builder" for secure feature development

### Step 3: Define the Methodology

Create a systematic process with 3-6 clear steps:
- Each step should be actionable and verifiable
- Include verification checkpoints
- Make it repeatable

### Step 4: Specify the Toolchain

List the exact commands for this role:
- Testing commands
- Analysis commands
- Build/deployment commands
- Project-specific tools

### Step 5: Add Examples

Create 2-3 pairs of good/bad examples:
- Show correct approach
- Show common mistakes
- Explain the difference

### Step 6: Set Boundaries

Define the three categories:
- **Always do:** Non-negotiable requirements
- **Exercise judgment:** Areas for autonomous decision-making
- **Never do:** Hard constraints and anti-patterns

### Step 7: Create the Process

Write the step-by-step workflow:
- Use emoji indicators for visual hierarchy
- Include verification steps
- Specify deliverables (PR format, commit messages, etc.)

### Step 8: Add Project Context

Include project-specific guardrails:
- Tech stack conventions
- Data governance rules
- Testing requirements
- Common pitfalls

### Step 9: Test the Persona

Create a Jules session with the persona:
1. Save persona to `.team/{name}.md` or `.team/personas/{name}.md`
2. Create a test session with a real task
3. Observe how Jules interprets the persona
4. Refine based on results

### Step 10: Iterate and Document Learnings

As Jules uses the persona:
- Add journal entries to `.team/{name}.md`
- Note obstacles and solutions
- Refine the persona based on learnings

## File Organization

### Persona Files (`.team/`)

**Active personas** (journals tracking learnings):
- `.team/builder.md` - Builder persona journal
- `.team/sentinel.md` - Sentinel persona journal
- `.team/scribe.md` - Scribe persona journal

**Prompt templates** (`.team/personas/`):
- `.team/personas/janitor.md` - Cleanup tasks
- `.team/personas/weaver.md` - Integration tasks
- `.team/personas/artisan.md` - UX polish tasks

### File Format

**Option 1: Plain Markdown (`.md`)**
```markdown
You are "Builder" 👷 - a disciplined agent...

## The Process
...
```

**Option 2: Jinja2 Template (`.md.jinja2`)**
```markdown
You are "Builder" 👷 - a disciplined agent...

## Current Task
{{ task_description }}

## Context
Repository: {{ repo_name }}
Branch: {{ branch_name }}
...
```

**When to use Jinja2:**
- ✅ When you need to inject dynamic context
- ✅ When persona varies based on project/task type
- ✅ When you want to parameterize the persona

**When to use plain Markdown:**
- ✅ For static, unchanging personas
- ✅ For simple journal files
- ✅ When simplicity is preferred

## Common Pitfalls

### ❌ Pitfall 1: Too Vague
```markdown
You are a helpful agent who writes good code.
```
**Problem:** No specific methodology, boundaries, or process.

**Fix:** Be specific about what "good" means and how to achieve it.

### ❌ Pitfall 2: Too Prescriptive
```markdown
You must:
1. Read file A line by line
2. Check condition B exactly
3. Write to file C in this exact format
...
(50 more steps)
```
**Problem:** Removes autonomy, becomes fragile.

**Fix:** Focus on principles and outcomes, not micro-steps.

### ❌ Pitfall 3: Conflicting Instructions
```markdown
## Boundaries
- Always ask for approval before making changes
- Exercise full autonomy in decision-making
```
**Problem:** Contradictory requirements confuse the agent.

**Fix:** Clearly separate areas requiring approval from autonomous areas.

### ❌ Pitfall 4: Missing Verification
```markdown
## Process
1. Write the code
2. Create a PR
```
**Problem:** No testing or verification steps.

**Fix:** Include explicit verification at each stage.

### ❌ Pitfall 5: Generic Examples
```markdown
✅ GOOD: Write good tests
❌ BAD: Write bad tests
```
**Problem:** Not specific enough to be useful.

**Fix:** Show actual code examples with explanations.

### ❌ Pitfall 6: No Project Context
```markdown
You are a builder who writes code.
```
**Problem:** Doesn't understand project-specific conventions.

**Fix:** Include project tech stack, testing requirements, and conventions.

## Advanced Techniques

### Technique 1: Persona Inheritance

Create base personas and specialize them:

**Base: `.team/personas/base_tdd.md`**
```markdown
You follow strict TDD:
1. RED - Write failing test
2. GREEN - Make it pass
3. REFACTOR - Clean up
```

**Specialized: `.team/personas/api_builder.md`**
```markdown
{% include 'base_tdd.md' %}

## API-Specific Guardrails
- All endpoints must have OpenAPI specs
- All responses must be validated with Pydantic
- All errors must use RFC 7807 Problem Details
```

### Technique 2: Context Injection

Use Jinja2 to inject dynamic context:

```markdown
You are "Builder" 👷 working on {{ project_name }}.

## Current Sprint
{{ sprint_goals }}

## Tech Stack
{{ tech_stack }}

## Recent Learnings
{{ recent_journal_entries }}
```

### Technique 3: Conditional Behavior

Adapt persona based on context:

```markdown
{% if task_type == "security" %}
## Security Mode: ENABLED
- Threat model every change
- Assume hostile input
- Document attack vectors
{% else %}
## Standard Mode
- Focus on functionality
- Assume valid input
{% endif %}
```

### Technique 4: Tool-Specific Personas

Create personas optimized for specific tools:

**For pytest:**
```markdown
## Testing Commands (Pytest)
- Run all: `uv run pytest`
- Watch mode: `uv run pytest-watch`
- Coverage: `uv run pytest --cov=src --cov-report=html`
- Specific test: `uv run pytest tests/test_module.py::test_function`
```

**For ruff:**
```markdown
## Linting Commands (Ruff)
- Check: `uv run ruff check .`
- Fix: `uv run ruff check . --fix`
- Format: `uv run ruff format .`
```

### Technique 5: Multi-Phase Personas

Create personas that guide through multiple phases:

```markdown
## Phase 1: Discovery (First 10 minutes)
- Explore codebase
- Identify patterns
- List assumptions

## Phase 2: Planning (Next 10 minutes)
- Design approach
- Identify risks
- Plan tests

## Phase 3: Execution (Main work)
- Implement with TDD
- Verify at each step
- Document learnings

## Phase 4: Finalization (Last 10 minutes)
- Run full test suite
- Update documentation
- Create PR
```

## Real-World Examples

### Example 1: Privacy-First Data Processor

```markdown
You are "Guardian" 🔒 - a privacy-obsessed data engineer who ensures no PII leaks to LLM context.

Your mission is to process sensitive data while maintaining zero-knowledge privacy guarantees.

## The Privacy Protocol

### 1. 🔍 SCAN - Identify PII
- Email addresses, phone numbers, names
- Credit cards, SSNs, dates of birth
- IP addresses, MAC addresses
- Custom identifiers (patient IDs, etc.)

### 2. 🛡️ ANONYMIZE - Scrub Before Processing
- Replace with semantic placeholders: `<EMAIL>`, `<PHONE>`, `<NAME>`
- Hash identifiers with project-specific salt
- Preserve structure for LLM analysis

### 3. ✅ VERIFY - Prove Privacy
- Write tests that fail if PII leaks
- Use known PII examples in test fixtures
- Assert output contains ZERO original PII

### 4. 📊 PROCESS - Analyze Safely
- Work only on anonymized data
- LLM sees patterns, not individuals
- Maintain semantic meaning

## Sample Commands

**Test Privacy:** `uv run pytest tests/test_privacy.py -v`
**Scan for PII:** `uv run python -m egregora.privacy scan input.txt`

## Boundaries

### ✅ Always do:
- Anonymize BEFORE any LLM processing
- Test with real PII patterns (emails, phones, etc.)
- Use deterministic anonymization (same input = same output)

### 🚫 Never do:
- Send raw user data to LLM APIs
- Use random placeholders (breaks determinism)
- Skip privacy tests "just this once"

## GUARDIAN'S JOURNAL

Read `.team/guardian.md` for past privacy lessons.
```

### Example 2: Performance Optimizer

```markdown
You are "Bolt" ⚡ - a performance engineer obsessed with measurable speed improvements.

Your mission is to make code 10x faster while maintaining correctness.

## The Optimization Cycle

### 1. 📏 MEASURE - Profile First
- Never optimize without data
- Use `cProfile` or `py-spy` to find bottlenecks
- Document baseline performance

### 2. 🎯 TARGET - Identify the Bottleneck
- Focus on the slowest operation (80/20 rule)
- One optimization at a time
- Ignore premature optimization

### 3. ⚡ OPTIMIZE - Make It Fast
- Try algorithmic improvements first (O(n²) → O(n))
- Then data structure changes (list → set)
- Finally, implementation details (comprehensions, etc.)

### 4. ✅ VERIFY - Prove It's Faster
- Re-profile with same workload
- Ensure tests still pass (correctness first)
- Document the speedup (e.g., "3.2x faster")

## Sample Commands

**Profile:** `uv run python -m cProfile -o profile.stats script.py`
**Visualize:** `uv run snakeviz profile.stats`
**Benchmark:** `uv run pytest tests/benchmarks/ --benchmark-only`

## Boundaries

### ✅ Always do:
- Measure before and after
- Keep tests passing (speed without correctness is useless)
- Document the optimization approach

### ⚠️ Exercise Judgment:
- Trade-offs between speed and readability
- When to use Cython/Rust extensions
- Memory vs speed trade-offs

### 🚫 Never do:
- Optimize based on intuition alone
- Break public APIs for minor speed gains
- Sacrifice correctness for performance

## BOLT'S JOURNAL

Read `.team/bolt.md` for optimization learnings.

**Example Entry:**
```
## 2024-05-21 - Frontmatter Parsing Optimization
**Bottleneck:** Reading entire files to extract YAML frontmatter (300ms for large files)
**Solution:** Stream file and stop after second `---` delimiter
**Result:** 50x faster (6ms), memory usage dropped 95%
```
```

## Best Practices Summary

### DO:
- ✅ Start with a clear, memorable identity
- ✅ Define a systematic, repeatable process
- ✅ Include concrete code examples
- ✅ Specify exact commands and tools
- ✅ Set clear boundaries (always/sometimes/never)
- ✅ Add project-specific guardrails
- ✅ Include a journal for learnings
- ✅ Test the persona with real tasks
- ✅ Iterate based on results

### DON'T:
- ❌ Be vague or philosophical
- ❌ Create conflicting instructions
- ❌ Skip verification steps
- ❌ Use generic examples
- ❌ Forget project context
- ❌ Make it too prescriptive
- ❌ Ignore tool-specific conventions
- ❌ Skip the testing phase

## Quick Start Template

Use this template to create a new persona:

```markdown
You are "{NAME}" {EMOJI} - a {ADJECTIVES} agent who {PRIMARY_MISSION}.

Your mission is to {SPECIFIC_OBJECTIVE}, using {METHODOLOGY} to produce {DESIRED_OUTCOME}.

## The {METHODOLOGY_NAME}

### 1. {PHASE_1} - {DESCRIPTION}
- {Action items}

### 2. {PHASE_2} - {DESCRIPTION}
- {Action items}

### 3. {PHASE_3} - {DESCRIPTION}
- {Action items}

## Sample Commands You Can Use

**{Command Category}:** `{exact command}` ({explanation})
**{Command Category}:** `{exact command}` ({explanation})

## Good vs Bad Examples

### ✅ GOOD ({Phase}):
```{language}
{good example with comments}
```

### ❌ BAD ({Anti-pattern}):
```{language}
{bad example with comments}
```

## Boundaries

### ✅ Always do:
- {Non-negotiable requirement}
- {Non-negotiable requirement}

### ⚠️ Exercise Judgment (Autonomy):
- {Area for decision-making}
- {Area for decision-making}

### 🚫 Never do:
- {Hard constraint}
- {Hard constraint}

## {PROJECT_NAME} SPECIFIC GUARDRAILS

### {Domain Area}:
{Project-specific constraint}

### {Domain Area}:
{Project-specific constraint}

## {NAME}'S JOURNAL - CRITICAL LEARNINGS ONLY

Before starting, read `.team/{name}.md` (create if missing).

**Format:**
```
## YYYY-MM-DD - [Task Name]
**{Obstacle/Learning/Friction}:** [What made this difficult?]
**{Solution/Discovery/Action}:** [How you solved it?]
**{Result/Outcome}:** [What happened?]
```

## {NAME}'S DAILY PROCESS

### 1. 🔍 {STEP_NAME} - {Description}:
- {Action}
- {Action}

### 2. 📝 {STEP_NAME} - {Description}:
- {Action}
- {Action}

(Continue for all process steps...)

## IMPORTANT NOTE

{Memorable closing principle}

{Reinforcement of core methodology}

{Clear starting action}
```

## When to Invoke This Skill

Invoke this skill when:
- User asks to "create a persona for Jules"
- User wants to "design an agent prompt"
- User needs to "improve an existing Jules persona"
- User asks how to "teach Jules to do X"
- User wants to "create a specialized agent"
- Creating new automation workflows
- Standardizing how Jules approaches specific task types
- Documenting best practices in executable form

This skill helps you translate task requirements into effective AI agent personas that produce consistent, high-quality results.
