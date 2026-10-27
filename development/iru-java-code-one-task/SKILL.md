---
name: iru-java-code-one-task
description: "Invoked as /iru-java-code-one-task <task description> (the task's text with its implementation_plan.md checkbox lines) via Skill. Implements one Java/Maven plan task and its tests, compile-checks, ticks the checkbox with a group-validation-pending note; no baseline or full gates, which iru-java-code-one-task-group runs."
model: sonnet
allowed-tools: Read Edit Write Bash(mvn *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *)
---

# Implement one plan task

Carry out a single task's implementation, tests, and checkbox update against the real codebase — nothing else.
This is the narrowest execution unit in the `iru-code` pipeline: `iru-java-code-one-task-group` calls it once per
task in a bucket (potentially many at once, in parallel agents), then handles license headers, Javadoc, and all
test/coverage/quality validation itself, once for the whole bucket, instead of repeating that validation here for
every single task. It uses a medium model on purpose — the plan already carries the hard reasoning; this skill
just executes one task's implementation, against code agreements that live in `reference/` rather than being
re-derived per task.

## Step 1 — Read only the reference material this task needs

This skill ships a `reference/` directory next to this file, holding this catalog's general Java code
agreements. Read `reference/README.md` first — it is short and routes you to the rest — then read only what it
points at for this task. The routing, restated:

| Read | When |
|---|---|
| `reference/mandatory-rules.md` | **Always** — the non-negotiable rules for production and test code (JUnit not AssertJ, Mockito not fakes, test naming and one test class per public class, type witnesses, record defensive copies, `final` parameters, Javadoc on every member, constants, modern idioms, LF line endings). |
| `reference/code-style.md` | **Always** — `var` type inference, `final` wherever possible, immutability, visibility, naming, exceptions, null. |
| `reference/class-member-ordering.md` | The task adds a new type, or adds/moves a constant, field, constructor, method, or nested type in an existing one. Skip it only for a change confined to an existing method body. |
| `reference/javadoc.md` | The task adds or changes a type, or any public/protected member. |
| `reference/testing.md` | The task writes or updates tests — nearly every task, since Step 4 is part of implementing it. |

Don't read the optional files speculatively — for a change inside one existing method, `mandatory-rules.md`,
`code-style.md`, and `testing.md` are the whole list.

If `reference/` is missing (e.g. the skill directory was copied without it), proceed using this repository's own
`CLAUDE.md` conventions and the surrounding code's existing style, and say so in Step 7's report — don't guess at
what the reference would have said.

## Step 2 — Re-check the current code state

Read the actual current content of the file(s) the task touches before editing — don't assume any "current code
state" notes passed in with the task are still accurate; other tasks in the same bucket may be landing
concurrently, or the file may have changed for unrelated reasons.

Also note what the surrounding file and package already do about the things `reference/` has opinions on:
whether `var` is used, how members are ordered, how errors are reported. The reference's rules are the default
for new code; a file that consistently does something else wins, and the divergence goes in Step 7's report
rather than becoming an unrequested restyle. The one exception is `reference/mandatory-rules.md`: the code you
write follows it even where the surrounding file doesn't (while still leaving the file's untouched code alone),
and any pre-existing violation you notice goes in the report.

## Step 3 — Implement exactly what the task specifies

The named file(s), the described class/method/field, the behavior, the hook/interface it implements. Apply
`reference/code-style.md` and whichever files Step 1 selected, plus this repository's own `CLAUDE.md`
conventions where they are more specific (Java version, license header expectations, banned dependencies).

Non-negotiable, because a later gate enforces them:

- **`reference/mandatory-rules.md`, in full**, for every line written or rewritten — production and test code.
- **Full Javadoc** on every type, method, constructor, and field (private ones included), with `@param`
  (including every record component and type parameter), `@return`, and `@throws` for every exception a caller
  can handle. The `@throws` list is what Step 4's tests are written against.
- **Declaration order** within any type you create or add to: constants, then fields, then constructors, then
  methods, then nested types — each band ordered public → protected → package-private → private, with
  overloads kept contiguous. Insert new members in their correct band; never reorder an existing file wholesale
  for an unrelated task.
- **`final` and `var` as the defaults for new code** — `final` fields and locals, `final` on every parameter
  (Checkstyle `FinalParameters`); `final` on a
  class or method not meant to be overridden (minding the proxy/mocking caveats in `reference/code-style.md`);
  `var` for locals wherever the type is inferable and nothing is hidden by it.
- **No new runtime dependency** unless the task explicitly calls for it. If one seems unavoidable, that's a
  blocker to report (Step 5), not a decision to make quietly.

Don't add anything the task didn't ask for — no speculative abstractions, no unrelated cleanup, no restyling of
code the task doesn't touch.

## Step 4 — Write or update the tests

Follow `reference/mandatory-rules.md` and `reference/testing.md`, and the existing test style in the same
package for anything those leave open. That means: JUnit 5 assertions (never AssertJ); Mockito mocks or spies for
collaborators (never a hand-written fake); one `<ClassName>Test` per public class (`<ClassName>IT` for an
integration test), never one test class shared across several implementations; test methods named
`methodBeingTested_whenCondition_expectedResult`; and full Javadoc on the test class and every member. Cover the
new/changed behavior, including the edge cases implied by the Javadoc `@throws` contracts (e.g.
null/invalid-argument cases). Do not run the test suite yourself — `iru-java-code-one-task-group`
runs it once for the whole bucket in its own consolidated validation pass.

## Step 5 — When to interrupt the user

Keep interruptions rare — most tasks should complete unattended. Stop and use `AskUserQuestion` (or plain text if
no real choice is being offered) only when:

- Implementing the task reveals it's ambiguous in a way that changes correctness or scope and can't be safely
  inferred — conflicting instructions, a choice only the user can make (e.g. which of two APIs to break), or a
  missing decision. Don't ask about things with an obvious best-practice answer.
- The task's described approach appears infeasible against the real code as it stands (e.g. it names a type or
  member that doesn't exist and isn't a trivial typo) — not something you can resolve by writing the code
  slightly differently.

Do not stop merely because the task is nontrivial — implement it. Do not report the task done to work around a
blocker; report it as blocked instead (Step 7), with enough detail — what was tried, what failed, why — for the
caller to surface it. A conflict between `reference/` and the surrounding code is *not* a reason to stop: follow
the surrounding code and report the divergence.

## Step 6 — Check off this task's checkbox now

If this task did not stop on a blocker (Step 5), update `implementation_plan.md` at the repository root before
reporting back — don't leave this for the caller. Re-read the file fresh (not any earlier cached view — other
tasks in the same bucket may be landing concurrently) and locate this task's own checkbox line by the exact text
passed in with the task. Flip its `[ ]` to `[x]`, and do the same for every sub-task checkbox that was part of
the work just completed, adding a short note naming the files touched, e.g. `- [x] Task 2. **Implement
`SimpleWidget`** — implemented, tests added; group validation pending.` — the same "pending" wording
`iru-java-code-one-task-group` uses, since the coverage/quality outcome isn't known until it validates the whole
bucket in its own Step 3/4. Edit only this task's own line(s) — never rewrite surrounding lines or other tasks'
checkboxes, since sibling tasks in a parallel bucket may be editing this same file at nearly the same moment.
This is what lets an interrupted run resume without re-attempting a task whose implementation and tests already
landed, even if the interruption happened before `iru-java-code-one-task-group` got to run its own group-wide
validation.

If this task stopped on a blocker instead, leave its checkbox untouched — there's nothing finished to mark done.

## Step 7 — Report the outcome

Hand control back to the caller with a short summary:

- **The file(s) touched** and **the tests added/updated** (not run — see Step 4).
- **Whether this task stopped on a blocker** per Step 5, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`** — e.g. matching a file that doesn't use `var`, leaving a class
  non-final because a framework proxies it or the project's Mockito can't mock it, or adding a member to a file
  whose existing order is already wrong — so the caller can see it was a decision rather than an oversight. Say
  so here too if `reference/` was missing entirely (Step 1).
- **Pre-existing violations of `reference/mandatory-rules.md`** noticed in the files touched (AssertJ, fakes,
  shared test classes, platform line endings, …) and left alone because they were outside the task's scope.

This is what `iru-java-code-one-task-group` records for this task before running its own consolidated
license/Javadoc/test/coverage/quality validation across the whole bucket; this skill has already checked off this
task's own checkbox with a pending-validation note (Step 6) — the caller only needs to replace that note with the
final validation outcome once the whole bucket passes, not create the checkbox entry itself. This skill itself
never captures a quality baseline and never runs tests/coverage/quality checks.
