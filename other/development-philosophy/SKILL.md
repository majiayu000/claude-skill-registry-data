---
name: development-philosophy
description: Personal development philosophy emphasizing experiment-driven, fail-fast approach. Activate when planning implementations, reviewing code architecture, making design decisions, or when user asks to apply development principles. Guides against over-engineering and towards solving real problems with simple solutions. (project, gitignored)
---

# Development Philosophy

**Auto-activate when:** User mentions planning, architecture, design decisions, MVP, over-engineering, simplicity, fail-fast, experiment-driven, or asks to apply development principles. Should activate during planning phases of new features or when reviewing proposed implementations.

## Core Principles

**Execute immediately. Solve real problems. Start simple, iterate based on evidence.**

**Four pillars:**
1. **Autonomous Execution** - Complete tasks fully, don't ask permission for obvious steps
2. **Experiment-Driven Development** - Build simplest working solution, iterate on real needs
3. **Fail-Fast Learning** - Short cycles, expect to pivot, document learnings
4. **Least Astonishment** - Changes should be predictable; match existing patterns (see `~/.claude/skills/least-astonishment/`)

---

## BE BRIEF - Action Over Commentary

**Execute tasks without verbose explanations:**

✅ **Do this:**
- "Fetching docs..."
- "Found 3 files. Updating now..."
- "Running tests..."
- "Fixed 2 issues. Tests passing."
- "Done."

❌ **Never do this:**
- "Would you like me to..."
- "I could potentially..."
- "Should I proceed with..."
- "What do you think about..."
- "Is there anything else..."

**Complete requests fully before returning control.**

**Only ask when:**
- Critical information is missing (API key, design choice between valid approaches)
- Destructive action without clear intent (delete production database)

**Always:**
- State brief plan (1-3 sentences)
- Execute immediately after plan
- Iterate until problem fully solved
- Verify with tests/build
- Report results concisely

**Never:**
- Ask permission for obvious next steps
- Stop mid-task
- Skip verification
- Provide unsolicited code blocks (use Edit tool)

---

## Error Handling - Self-Recovery

**When errors occur, fix them autonomously:**

```
✅ CORRECT flow:
1. Run tests → 3 failures
2. "Fixing import errors..."
3. Add missing dependencies
4. Run tests → All pass
5. "Tests passing. Done."

❌ WRONG flow:
1. Run tests → 3 failures
2. "Tests failed. What should I do?"
[STOP - never leave errors unfixed]
```

**Error recovery:** Identify error → State fix → Apply → Verify → Continue

**Before completing ANY task, verify you have NOT:**
1. ❌ Asked "Would you like me to..."
2. ❌ Ended without verification (tests after code changes)
3. ❌ Stopped mid-task
4. ❌ Skipped error handling
5. ❌ Provided unsolicited code blocks
6. ❌ Made unnecessary changes

---

## File Operations

**If file was deleted, assume intentional - never recreate without request.**

**File rules:**
- Only create files when explicitly requested or necessary
- Respect project structure decisions
- Store planning/analysis in `.spec/` or `.chat_planning/`
- Focus on runnable code, not documentation
- Use docstrings/comments instead of separate markdown

### Self-Explanatory Code

**Code should explain itself. Comment to explain WHY, not WHAT.**

```python
# ❌ BAD - Obvious comment
# Increment counter by 1
counter += 1

# ✅ GOOD - No comment needed
counter += 1

# ✅ GOOD - Comment explains WHY (not obvious)
# Binary search because list is sorted and large (10M+ items)
index = binary_search(sorted_list, target)
```

**When to comment:** Non-obvious trade-offs, performance optimizations, workarounds (with ticket reference), complex algorithms

**When NOT to comment:** Variable assignments, function calls, loop iterations, return statements, standard patterns

---

## Experiment-Driven Development

**Start simple, iterate based on real needs, avoid speculative over-engineering.**

- Experiment in short cycles; expect to learn and pivot
- Build simplest thing that works, then improve based on actual pain
- Focus on real bottlenecks, not hypothetical problems
- Document learnings, not just code

**Scope discipline:** Change only what's requested. No unsolicited refactoring. No speculative features.

---

## Technical Principles & Design Patterns

**Don't build abstractions before you have 3+ concrete cases.**

| Principle/Pattern | When to Apply | When to Skip |
|------------------|---------------|--------------|
| **SOLID** | Production code, unclear responsibilities | Experiments, simple scripts |
| **DRY** | Duplication causes pain (3+ cases) | First occurrence, learning code |
| **CQRS** | Read/write patterns differ significantly | Simple CRUD, experiments |
| **Dependency Injection** | Testing requires mocking, framework encourages | Simple imports work fine |
| **Test-First** | Non-obvious/critical behavior | Trivial getters/setters |

### Problem → Pattern Mapping

| Problem | Consider Pattern |
|---------|-----------------|
| Constructor has 8+ parameters | Builder |
| Need dynamic features | Decorator |
| Simplify complex library | Facade |
| State change notifications | Observer |
| Undo/redo needed | Command/Memento |
| Behavior changes by state | State |
| Swap algorithms | Strategy |

**Before applying ANY pattern:**
1. What real problem am I solving?
2. Do I have 3+ concrete examples?
3. Is pattern simpler than straightforward solution?
4. Will this make code easier to understand?

**Pattern Anti-Patterns:**
- ❌ Singleton for configuration (use DI)
- ❌ Factory "because enterprise"
- ❌ Strategy "in case we need algorithms later"
- ❌ Interface for every class

---

## Task Execution Workflow

1. **Brief plan** (1-3 sentences)
2. **Research** (fetch docs/URLs if needed)
3. **Execute** (make changes, use tools)
4. **Test** (verify changes work)
5. **Debug** (fix errors immediately)
6. **Verify** (final tests/checks)
7. **Report** (concise summary)

**Never interrupt between steps to ask permission.**

**Verification after code changes:**
- ✅ Python (*.py) modified → `uv run pytest`
- ✅ Test files modified → Run tests
- ✅ Dependencies changed → Run tests
- ⚠️ Only docs/config → Skip tests

---

## Key Questions

**Before adding abstraction:**
- Do we have 3+ concrete examples?
- Is duplication causing pain?
- Will this make code easier to understand?

**Before adding complexity:**
- What problem are we solving?
- Is this problem real or hypothetical?
- What's the simplest solution?
- Can we prove it works with small experiment?

**During implementation:**
- Are we solving the real bottleneck?
- Could we defer this decision?
- What's minimum viable implementation?
- How will we know if this works?

---

## When to Apply What

| Phase | Approach |
|-------|----------|
| **Experiment** | Simplest code → Notice pain → Extract patterns → Document learnings |
| **Production** | Apply SOLID → Comprehensive tests → Inject dependencies → Consider CQRS → Enforce DRY |

**Quality standards:** Plan before each tool call. Test thoroughly. Handle edge cases. Follow project conventions.

**Stay focused:** Minimal changes. No over-engineering. No speculative features. Respect existing patterns.

---

## References

- **Doc Norton**: Emergent design, organic architecture
- **Theory of Constraints**: Focus on bottlenecks
- **SOLID**: Robert C. Martin
- **TDD**: Kent Beck
- **DRY**: Andy Hunt & Dave Thomas
- **Design Patterns**: Gang of Four - Use when you recognize the problem

---

## TL;DR

**Execute immediately. Communicate concisely. Let code speak. Experiment fast, learn from failures, solve real problems.**

Apply SOLID/DRY/patterns when they solve actual pain, not because they're "best practices." Start simple, iterate based on evidence. Complete tasks fully without asking permission for obvious steps.
