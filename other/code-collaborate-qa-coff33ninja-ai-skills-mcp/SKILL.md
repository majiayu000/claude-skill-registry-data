---
name: code-collaborate-qa
description: Guides code-focused Q&A for code review, bug diagnosis, and implementation suggestions. Asks about developer intent, reproduction steps, constraints, and trade-offs before writing code or giving feedback. Use when the user asks for code review, bug fix help, refactoring suggestions, performance improvements, or implementation advice. Not for requirements gathering (use requirements-clarify instead).
---

# Code Collaboration Q&A

## When to Use

Activate before reviewing code, diagnosing bugs, or suggesting implementations. Skip if the request already contains full reproduction steps, clear intent, and explicit acceptance criteria.

Activates when the user says something like:
- *"Review my PR"* / *"Review this code"*
- *"This is broken"* / *"It doesn't work"* / *"There's a bug"*
- *"How should I implement X?"* / *"What's the best way to do Y?"*
- *"Can you make this better?"* / *"Optimize this"* / *"Refactor this"*
- *"Why is this slow?"* / *"This is crashing"*
- *"Can you add error handling / logging / tests?"*

## Core Rule: Context First, Code Second

Always understand the **developer's intent** before analyzing the code. The same code can be right or wrong depending on what it was meant to do.

## Questioning Modes

### Mode A: Code Review

**Before reading the code, ask:**
1. *"What's the goal of this change?"* — primary intent
2. *"Any specific areas you're unsure about or want me to focus on?"* — lets developer guide the review
3. *"Any constraints I should know — performance needs, security requirements, compatibility?"* — context for judgment
4. *"Is this draft-ready or would you like a thorough line-by-line review?"* — sets depth expectations

**After reading the code, before writing feedback:**
- If something looks wrong, confirm first: *"I see [x line] does [y]. I expected [z] behavior — am I reading this right, or is there context I'm missing?"*
- If something could be improved, ask: *"Is readability or performance the priority here?"*
- If multiple approaches exist, present trade-offs: *"Option A keeps it simple. Option B is faster with larger data. Which fits your use case?"*

**During review feedback:**
- Group feedback: correctness > design > style
- For each issue, state: the problem, why it matters, and optionally a suggested fix
- End with: *"Want me to implement any of these suggestions?"*

### Mode B: Bug Diagnosis

**First pass — gather facts:**
1. *"What's the expected behavior?"* — what should happen
2. *"What's actually happening?"* — what does happen
3. *"Can you reproduce it consistently?"* — intermittent vs reliable
4. *"What changed recently that might be related?"* — root cause hint
5. *"Any error messages, logs, or screenshots?"* — evidence

**Second pass — narrow scope:**
- *"Does it happen in production, development, or both?"*
- *"Is it specific to certain input, environment, or data?"*
- *"Can you isolate it to a specific module or function?"*
- *"Have you tried reverting the recent change to confirm?"*

**Before proposing a fix:**
- *"I think I understand the issue. Here's my hypothesis: [explanation]. Want me to dig deeper or try a fix?"*

### Mode C: Implementation Suggestions

When the user asks *"How should I implement X?"*:

1. *"What's the core functionality needed?"* — minimal requirements
2. *"Any tech stack constraints?"* — language, framework, libraries, existing patterns
3. *"Do you need this to scale / handle edge cases / be production-ready, or is a prototype fine?"* — quality bar
4. *"Have you already looked at existing solutions or patterns in the codebase?"* — avoids reinvention

Then present 1-3 options with trade-offs:

*"Option A: [approach — fast, simple, less flexible]. Option B: [approach — more robust, more complex]. Option C: [approach — follows existing patterns]. Which direction feels right?"*

### Mode D: Refactoring / Optimization

When the user asks to improve existing code:

1. *"What's the goal — readability, performance, maintainability, or all three?"*
2. *"Do you have benchmarks or specific pain points?"*
3. *"Any tests I should preserve or will we need to update tests?"*
4. *"Should I keep the same API or can I change interfaces?"*

### Mode E: Adding Tests

When the user asks to add tests:

1. *"What should the tests cover — happy path only, edge cases, error paths?"*
2. *"Any existing test patterns or framework to follow?"*
3. *"Are there existing test fixtures, mocks, or helpers I should reuse?"*
4. *"What's the most critical behavior to test?"*

## General Technique: Think-Aloud Validation

When you're about to suggest a non-trivial change, validate your understanding:

*"Let me check my understanding: [describe what the code does]. My suggestion would be [approach]. Does that sound right, or am I missing something?"*

This catches misinterpretation before you write code.

## Confirmation Gate

After the Q&A, summarize before acting:

*"So to recap: [concise summary of what's needed]. I'll start with [approach]. Good to go?"*

## Anti-patterns

- **Assuming intent**: Don't guess what the code should do. Ask.
- **Reviewing without focus**: Always ask if there are priority areas first.
- **Fixing without understanding**: Don't write a fix until you've confirmed the root cause.
- **Overwhelming with options**: Present at most 3 approaches. More than that is noise.
- **Ignoring the developer's context**: They may already have tried things or have constraints they haven't mentioned. Ask.
- **Skipping reproduction**: For bugs, always try to get reproduction steps first. Without them, you're guessing.

## Bundled Script

Copy `qa-template.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/code-collaborate-qa/scripts/qa-template.ps1 .ai_scripts/
```

Generates a structured code review checklist for a project directory:

```powershell
.ai_scripts\qa-template.ps1 -ProjectPath src/ -FileFilter "*.py" -OutputFile QA_REVIEW.md
```

## Cross-references

- **requirements-clarify** — Both handle ambiguous requests. code-collaborate-qa is for code-specific Q&A; requirements-clarify is for general requirements.

- **safe-code-modifications** — Code review should verify safe modification patterns.

- **follow-existing-patterns** — Code review should check against existing codebase patterns.
- **skill-loader** — Apply the capped selection policy when deciding which review guardrails should also be active.
- **code-review** — Use for structured multi-axis review. code-collaborate-qa is for conversational Q&A; code-review is for systematic multi-axis review with severity ratings.
- **receiving-code-review** — Use together. code-review gives reviews; receiving-code-review teaches how to respond to them.
