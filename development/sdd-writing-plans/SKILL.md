---
name: sdd-writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
disable-model-invocation: true
metadata:
    opencode/autoinvoke: false
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the sdd-writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `sdd-using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

**Seams.** Reconcile the plan's seams with the spec's Testing Decisions: prefer seams that already exist, use the highest seam that covers the behavior, and keep the count low — one is ideal. Name where each new module's interface lives. The interface is the test surface: callers and tests cross the same seam, so if a test needs to reach past the interface, the module is the wrong shape.

**Depth.** A module is deep when a lot of behavior sits behind a small interface. Check each new module:

- Can a caller use it knowing only its interface — signature, invariants, error modes?
- The deletion test: if deleting the unit makes complexity vanish, it was a pass-through; if the complexity reappears across callers, it was earning its keep.
- One adapter means a hypothetical seam. Don't introduce a seam until something actually varies across it.

**Design it twice (architectural plans only).** For the riskiest interface in the plan, dispatch 2-3 `sdd-designer` agents in parallel to sketch radically different shapes, then compare on depth, locality, and seam placement before locking the winner into the plan.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Slicing Strategy and Order

Choose how tasks cut through the work before writing them, and say which strategy the plan uses:

- **Vertical tracer bullets (default).** Each task cuts a narrow but complete path through every affected layer — schema, logic, API, UI, tests — and is verifiable on its own. Never build all of one layer and then all of the next; no task is verifiable until the last one, and failures surface late.
- **Contract-first.** When two tasks meet at an interface, freeze the interface in an earlier task, then let both sides build against it.
- **Risk-first.** The task with the highest uncertainty goes first. If it fails, the plan changes before anything is built on top of it.
- **Prefactor first.** Make the change easy, then make the easy change: schedule the enabling refactor as its own task before the feature that needs it.
- **Wide mechanical refactors are the exception.** One edit whose blast radius fans across many call sites cannot land green as a vertical slice. Sequence it expand → migrate → contract: add the new form beside the old, migrate call sites in batches that stay green, delete the old form only when no caller remains. When even the batches cannot stay green alone, keep the sequence but have them share an integration branch, with every batch blocking a final integrate-and-verify task — green is promised only at that task.

Order tasks by dependency, blockers first, and give every task explicit `Depends on` edges. Every task leaves the system compiling with its tests green — the one exception is a batched refactor on a shared integration branch, which goes green at its integrate-and-verify task.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a
fresh reviewer's gate. When drawing task boundaries: fold setup,
configuration, scaffolding, and documentation steps into the task whose
deliverable needs them; split only where a reviewer could meaningfully
reject one task while approving its neighbor. Each task ends with an
independently testable deliverable.

Size signals for splitting further: the task needs more than one focused
session, would change more than ~5 files, cannot be summarized in one
sentence without "and", or its brief would not fit comfortably in one
fresh implementer context. High-uncertainty work is the exception — keep
it whole enough to answer its question, and order it first (see Slicing
Strategy and Order).

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sdd-subagent-driven-development (recommended) or sdd-executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach, and which slicing
strategy the tasks use]

**Tech Stack:** [Key technologies/libraries]

**Commands:**

- Test: [exact command]
- Build: [exact command]
- Lint: [exact command]
- Typecheck: [exact command, or "none"]

**Spec:** [path to the spec/design doc this plan implements — the plan
argues from the spec, so the spec travels with it; executors read both]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits,
naming and copy rules, platform requirements — one line each, with exact
values copied verbatim from the spec. Every task's requirements implicitly
include this section.]

## Review Focus

[The five input classes or failure modes the spec is silent on but that
are most likely to bite a person using this software — one line each,
naming the input or condition and the behavior a reasonable person would
expect, most likely first. The spec is a vision document: it says what
the software must do, not everything it will meet, and its silence on an
input is not permission for that input to break the program. Write the
list here, once, with the spec in front of you, then add the test that
pins each line to the task that owns the code, in that task's own step
style. The section is the final reviewer's checklist of spec-silent
cases now covered by tests — not a list of open gaps.]

---
```

## Commands, Sources, and Verification Placement

**Discover, don't guess.** Read the repo's tooling (package.json scripts, Makefile, CI config, existing test files) and record the exact commands in the header before writing tasks. Every task step uses the commands verbatim from that block — drift between tasks means one of them is lying. Success criteria that need their own command or procedure get it in the task that owns them, so the spec's criteria always map to runnable evidence.

**Place each check at the cheapest stage that catches it.** Fast checks (typecheck, lint, focused test) belong in the step loop; the full suite belongs at task end; slow or environment-hungry checks (integration, end-to-end, performance) belong at branch end. A slow check in the step loop is a check people turn off.

**Cite framework-specific APIs.** When a task's code depends on a library or framework API, verify it against that version's official documentation and cite the source in the plan; if you cannot verify it, mark it unverified rather than writing it from memory. A hallucinated signature in a plan is copied faithfully by every implementer.

## The Code in the Plan

<HARD-GATE>
Before writing any code into the plan, read `code-guidance.md` in full.
Every code block in every task — implementation and test alike — must
comply with it; test-specific design stays with the downstream test skills.
A snippet that violates the guidance is a plan failure on the same footing
as a placeholder: rewrite it before the plan leaves your hands. The
self-review and the adversarial plan reviewer both audit against the
guidance, and neither may approve a plan containing a violation.
</HARD-GATE>

The code inside a plan's fences is the code that ships: the implementer
transcribes it, and it reaches review having never been read by anyone but
you. The rules in brief — the full rules and their examples are in
`code-guidance.md`:

- **Climb the ladder before writing:** does this need to exist → already in
  this repo → standard library → native platform → installed dependency →
  one line → minimum code. Never add a dependency for what a few lines can
  do.
- **No unrequested abstraction:** no interface with one implementation, no
  factory for one product, no config for a value that never changes. Add the
  abstraction at the third use.
- **Match the project:** read neighboring code first; conventions beat
  preferences.
- **Stay in scope:** the snippet solves this task; unrelated cleanup is a
  note in the plan text, never a drive-by edit.
- **Never simplify away:** trust-boundary validation, error handling that
  prevents data loss, security, accessibility, or anything the spec
  requires.
- **Mark deliberate simplifications** with a comment naming the ceiling and
  the upgrade path.

## Task Structure

````markdown
### Task N: [Component Name]

**Depends on:** [Task numbers that must complete first, or "None — can
start immediately"]

**Files:**

- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**

- Consumes: [what this task uses from earlier tasks — exact signatures,
  including the invariants and error modes it must handle]
- Produces: [what later tasks rely on — exact function names, parameter
  and return types, plus invariants callers may rely on and error modes
  callers must handle. A task's implementer sees only their own task;
  this block is how they learn the contracts neighboring tasks use.]

**Testing seam:** [the public boundary this task's tests cross — the
interface named by the spec's Testing Decisions and this plan's File
Structure; name the exact function or entry point, or "none — no test
surface" for a documentation- or config-only task]

**Done when:** [one line: the state of the world that makes this task
acceptable — the reviewer's contract, in addition to the steps below]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## No Placeholders

Every step must contain the actual content an engineer needs, and every code
block must comply with `code-guidance.md`. Complete is not the same as good:
a violation of the guidance is a **plan failure** on the same footing as a
placeholder. These are **plan failures** — never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself; for architectural plans, follow it with the adversarial reviewer dispatch below.

**1. Spec coverage and intent traceability:** Skim each section/requirement in the spec. Can you point to a task that implements it? Every promise in the spec's Confirmed Intent (Outcome / User / Success / Constraint / Out of scope) needs a task too, and nothing outside that intent should have snuck in. For every Success Criterion, can you point to the command or recorded procedure that verifies it? A criterion with no evidence path is a gap to close here, not at verification time. List any gaps.

**2. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

**4. Review Focus:** For each input class or failure mode the spec implies, is there a task whose tests exercise it? The five the spec is silent on that are most likely to bite a person go in the Review Focus section, and each line must name the test pinned to the owning task — a line with no test is an open gap, not a focus item. An empty section means you checked and found none, not that you skipped the check.

**5. Interface and dependency consistency:** For every `Produces`/`Consumes` pair, does the consumer's use match the producer's exact signature, invariants, and error modes? Do the `Depends on` edges form a valid order — no cycles, no task consuming a value that only exists in a later task? Does every task that adds or changes behavior name a `Testing seam`, and does each seam match the spec's Testing Decisions and the File Structure — a caller-visible boundary, not a test-only entrance? Does every task's `Done when` name a checkable end state the reviewer can confirm from the diff? The execution skills' pre-flight scan catches these eventually; catch them here, where fixing is cheap.

**6. Brief self-containment:** Does each task carry every exact value its implementer needs — signatures, test cases, commands, paths — without reading another task? Any "similar to Task N" fails this check.

**7. Code quality (blocking):** Walk every code block in every task against `code-guidance.md`. Any violation — a lower ladder rung that would hold, an abstraction before its second user, names that obscure content, validation or error handling weakened, an unrelated change — is fixed before the handoff. This is a gate, not a preference: the plan does not proceed to review with a known violation.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement with no task, add the task.

**Adversarial plan review (architectural plans).** Dispatch the
`sdd-plan-reviewer` agent with `plan-document-reviewer-prompt.md`, giving it
the plan, the spec, and the path to `code-guidance.md` — never your own
reasoning. Reconcile its findings against the plan text using
this precedence: contract misread (fix the plan or spec text that misled it),
actionable (fix the plan), valid trade-off (document it in the plan), noise
(note and move on). A finding that conflicts with the spec is your human
partner's call, not a silent edit.

## Plan File Safety

A plan is execution state, not just a document. Before saving, check whether
the target file already exists with unchecked steps:

- Same work, being revised or extended → update it in place.
- Different work → write a new file. Never overwrite a plan that may be
  mid-execution in another session; if the filename collides, stop and ask.

An overwritten plan destroys work state that exists nowhere else.

## Execution Handoff

After saving and self-reviewing the plan, link it for your human partner
to read. If they have already explicitly supplied an execution method, ask
them to review the plan and confirm it captures what they want; wait for that
review before implementation, then use the preserved method. Otherwise, ask
them to review the plan and choose an execution method before implementation.

**When no execution method has already been supplied:**

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Please review the plan — does the granularity feel right, and are the `Depends on` edges correct? Which execution approach would you prefer?**

- **Subagent-driven** - A fresh subagent implements each task and a fresh reviewer checks it before the next one starts, then a whole-branch review at the end. Most thorough; costs a fresh context per task and per review.
- **Inline** - I implement every task myself in this session, the way this harness runs work, then one fresh `sdd-final-reviewer` checks the whole branch. Cheapest and fastest; no independent review until the end. Runs well with a mid-tier session model, since the plan carries the design.

**For this plan I recommend <one of the two>, because <one sentence from the plan: how much the tasks depend on each other's interfaces, how many there are, what a shipped mistake would cost>. Does the plan capture what you want, and which approach should we use?"**

**When an execution method has already been supplied:**

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Please review the plan — does it capture what you want, is the granularity right, and are the `Depends on` edges correct?"**

**If Subagent-driven chosen:**

- **REQUIRED SUB-SKILL:** Use sdd-subagent-driven-development

**If Inline chosen:**

- **REQUIRED SUB-SKILL:** Use sdd-executing-plans

## Common Rationalizations

| Excuse                                                    | Reality                                                                                                                                 |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| "I'll figure it out as I go"                              | Planning is the task; implementation without a plan is guessing, and guessing gets more expensive with every file touched.              |
| "The tasks are obvious, writing them down is overhead"    | Explicit tasks surface the interfaces, dependencies, and exact values you would otherwise discover mid-build.                           |
| "Build all the schema, then all the API, then all the UI" | Horizontal slicing: no task is verifiable until the last one, and failures surface late. Cut tracer bullets through the layers instead. |
| "Add appropriate error handling"                          | That is a placeholder. Show the code, or it is not a plan yet.                                                                          |
| "The plan passed self-review, so I can start"             | Self-review is the author checking their own work. The gate is your human partner's review and execution choice.                        |
| "I'll overwrite the old plan file, it's stale"            | Unchecked steps may be mid-build in another session. Revise in place or ask.                                                            |
| "Dependencies will emerge during implementation"          | They emerge as interface mismatches and rework. Declare `Depends on` now; the pre-flight scan and the task reviewer bill you otherwise. |
| "The API is probably the same as I remember"              | A hallucinated signature is copied faithfully by every implementer. Verify against docs and cite, or mark it unverified.                |
