---
name: recipe
version: 0.1.0
license: MIT
description: Use when an approved spec or design needs to become an implementation plan, after mise and before any code. Also use when the user says "write the plan", "plan this out", or the work will be executed later, by someone else, or in a fresh session.
---

# recipe

A recipe card is written so a cook who has never seen the dish can plate it exactly: exact quantities, exact pan, exact minutes, steps in order. "Season to taste" is how the same dish comes out different every night. This skill turns an approved spec into that card: an implementation plan a zero-context engineer or fresh agent session can execute with you unavailable for questions.

Assume the implementer is skilled but knows nothing about this codebase or problem domain, and has questionable taste in tests. The plan carries everything: which files each task touches, the actual code, the exact commands, the output to expect. DRY, YAGNI, test-first, frequent commits.

## Preconditions

- An approved design or spec exists ([mise](../mise/SKILL.md)'s output, or equivalent). No spec? Run mise first. Recipe shapes decided work; it does not decide.
- One plan per subsystem. If the spec spans several independent subsystems, say so and split before going deep; each plan must produce working, testable software on its own.

## Steps

1. **Read the code you are planning against.** The files the spec touches, one neighboring module that shows the house pattern, the test layout. A plan written from memory or a description of the codebase hedges ("if main returns the code, leave it; otherwise wrap it"), and every hedge is a decision forwarded to the implementer.
2. **Map the file structure.** Before any tasks: every file the plan creates or modifies, and the one responsibility each holds. Prefer small focused files with clear boundaries; in an existing codebase, follow its patterns instead of restructuring. This map locks the decomposition. A file whose purpose needs "and" probably wants splitting.
3. **Open with the header.** Goal in one sentence, architecture in two or three, key tech, and an instruction to agentic workers to execute task-by-task tracking the checkboxes.
4. **Decompose into tasks, each task into bite-size steps.** A step is one action of a few minutes, written as a checkbox (`- [ ]`): write the failing test (the actual test code), run it and watch it fail (the exact command and the expected failure), implement the minimal change (the actual code), run to green (command and expected output), commit (the command). Every task names its exact file paths up front.
5. **Pin every decision.** Exit-code orderings, edge-case behavior, naming, where a helper lives: decided in the plan, with the reason when it is not obvious. A plan that says "your call", "adapt to taste", or ends with an open-questions section has pushed design onto the person with the least context. A decision that genuinely cannot be made yet goes back to [pressure-test](../pressure-test/SKILL.md) or the spec's author now, not into the plan.
6. **Self-review with fresh eyes**, then fix inline:
   - Spec coverage: every requirement in the spec points to a task that implements it.
   - Placeholder scan: hunt the patterns under No placeholders below.
   - Consistency: names, signatures, and types used in later tasks match where earlier tasks defined them.
7. **Save to `docs/plans/YYYY-MM-DD-<topic>.md`, commit, and hand off to [fire](../fire/SKILL.md).** It executes in two shapes: a fresh subagent per task with review between tasks (preferred), or inline in one session with checkpoints. Either way the plan, not memory of this conversation, is the source of truth.

## Task format

````markdown
### Task N: <component>

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/test_file.py`

- [ ] Write the failing test

```python
def test_specific_behavior(tmp_store):
    result = function(input)
    assert result == expected
```

- [ ] Run it, watch it fail: `pytest tests/exact/path/test_file.py::test_specific_behavior -v` - expect FAIL, "function not defined"
- [ ] Implement the minimal change

```python
def function(input):
    return expected
```

- [ ] Run to green: same command - expect PASS
- [ ] Commit: `git add -A && git commit -m "feat: <effect>"`
````

## No placeholders

Each of these in a plan is a plan failure, not a shortcut:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "handle edge cases" without the cases and the handling
- "Write tests for the above" without the test code
- "Similar to Task N" instead of repeating the code; tasks get read out of order
- A step that says what to do without showing how; code steps carry code blocks
- A name, type, or function referenced but defined in no task

## Rules

- Exact paths, complete code, exact commands with expected output. Every step, no exceptions for the "obvious" ones.
- The implementer makes zero design decisions. If writing a step surfaces an undecided question, decide it in the plan or take it back upstream; never forward it.
- Test-first inside every task that changes behavior. The failing run is a step of its own, not an assumption.
- Don't relitigate the spec. Decisions mise and pressure-test pinned arrive here settled; the plan implements them.
- Scale ceremony to the work: a one-task plan still gets the header, the file map, and real code in its steps. What it skips is task count, not rigor.

## Common mistakes

- Describing tests in prose ("test that add is idempotent") instead of writing the test. The executor inherits a design job, not a recipe.
- Steps without run commands or expected output, so the executor cannot tell a broken step from a broken codebase.
- Component-sized "steps" that hide ten decisions, instead of checkbox actions of a few minutes each.
- An "open questions" or "decide while building" section. That is the tell the planning was not finished.
- Hedged structure: "put it in store.py, or a new helpers module if you prefer". The file map exists to settle exactly this.
- Writing the plan for yourself-tomorrow instead of a stranger, leaning on context only this conversation holds.
