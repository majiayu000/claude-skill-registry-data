---
name: solution-spec
description: Closes a spec before shark:code-writer builds it - the guards on the path, the input classes, the operations on the state, a behaviour table with one test for each row, the decided questions, and an adversarial check. Use after a root cause analysis, or before a round of code-writer lanes.
---

# Solution spec

A spec is closed when the writer has no behaviour decision left. Then a fast writer model builds it well. A spec
that is not closed makes the writer guess, and each guess can break a rule next to the change.

The kit measured this on a real defect (Payload CMS, localized drafts). With a closed spec, `shark:code-writer` on
Sonnet fixed the most tests with no regression. With an open spec, the same writer broke 6 field-access tests. Opus
avoided them only because it made the missing decision itself: "when field access removes `_status`, the save
writes no status". That decision belongs in the spec, with a test.

**The rule.** Each decision that changes observable behaviour is in the spec, as a row with a test. The writer
decides only the structure: names, the location of the code, helpers, the existing pattern to follow.

## Who closes the spec, and when

| Who | When | Where the closed spec goes |
| --- | --- | --- |
| `shark:code-debugger` | After the completeness gate of `shark:debug-rca`, before the hand-off | The RCA file: the sections below, then the Fix spec |
| `shark:architect` | When a design becomes a build | The spec or the design note of the build |
| `shark:lead-engineer`, the operator | Before a round of `shark:code-writer` lanes | The round contract: one closed spec for each lane |

Close the spec with the strongest model of the session (Opus by default). A closed spec goes to `shark:code-writer`
on Sonnet. An open spec, or a Sonnet run that broke a guard test, goes to Opus.

## Method

Work from the code and the data model, not from memory. Read each function that the change will run through, and
the schema of the data that it reads.

### 1. Guards on the path

List each condition that can stop or limit the new behaviour: an access check, a field-access check, a filter of
the records or locales that the actor can reach, a validation, an early return, a feature flag, a transaction
boundary. Read the callers too: a guard in a caller limits the callee.

For each guard, decide what the new behaviour does when the guard fires, and name a test. "Do not change this
branch" is not enough: the new code can run around a branch that it does not change.

**A guard keeps its effect by default.** The new behaviour reaches only what the guard allows: the records, the
locales, the fields that the actor can reach. A shared change marks only the locales that the actor can reach; a
bulk operation changes only the rows that the filter returns. To let the new behaviour pass a guard, the report or
the owner must ask for it. Then it is an ask-first decision (operator §9), never a default.

| # | Guard | Location | When it fires | The new behaviour when it fires | Test |
| --- | --- | --- | --- | --- | --- |
| G1 | `_status` field access | `update.ts:210` | the actor cannot update `_status` | writes no status for any locale | `<test name>` |

### 2. Input classes

From the schema, list each kind of value that the change reads, and each form of it:

- **Kinds:** a scalar, a list, a block list, a group, a relation; and a child with a different property than its
  parent (a localized field in a shared list, a shared field in a localized group).
- **Forms:** absent, `null`, empty, the same value sent again, a changed value, a value of another type (an ID as
  a number or a string).

A kind or a form that the change treats in a different way is a row of the behaviour table.

- **Repeat each input-class row for each twin path** (collection and global, single and bulk), with its own test.
  A twin can read, compare or merge the value with other code, so one twin's test does not cover the other.
- **Send the realistic payload in one row of each twin.** A client often sends the whole document: the changed
  field, and the unchanged values of every other field. A test that sends only the changed field misses the case
  where an unchanged value looks like a change.

### 3. Operations on the state

List each operation that can run while the state of the change exists, and its expected outcome. For a defect,
the state is the defect's state (a pending shared draft). For a feature, it is the new data. Examples: create,
update, draft save, publish, unpublish one, unpublish all, the "all" scope (all locales, all tenants, bulk),
autosave, restore, delete, read in another scope.

### 4. Behaviour table

The behaviour table is the spec. Each row is one case: the condition (a guard, an input class, an operation and a
scope), the expected outcome that a caller can observe, and the test that proves it.

| # | Condition | Expected outcome | Test | Kind |
| --- | --- | --- | --- | --- |
| B1 | draft save, one locale, a shared field changes | every locale is `draft` in the new version | `<test name>` | regression |
| B2 | draft save, one locale, only a localized child of a shared list changes | only that locale is `draft` | `<test name>` | guard |
| B3 | G1 fires | no locale status changes | `<test name>` | guard |

- **Kind:** `regression` fails now and must pass after the change; `guard` passes now and must still pass; `new`
  is a test that the writer writes first (a feature).
- Each guard of step 1, each input class of step 2 for each twin, and each operation of step 3 that the change can
  reach has a row, or a reason in the row why the change cannot reach it.
- A sentence "must not change X" is a row with a test, or it is not part of the spec.

### 5. Decisions

Decide each open behaviour question here. The writer must not decide one.

| # | Question | Decision | Reason | Status |
| --- | --- | --- | --- | --- |
| D1 | `locale: 'all'` with only localized changes: do the unchanged locales stay `published`? | yes | the report asks that a localized change leaves other locales | taken by default, owner to confirm |

A decision that changes a business rule, a permission or a public interface is an ask-first item (operator §9).
Mark it, give your recommendation, and build the rows on the recommendation.

A decision on a guard follows step 1: the default keeps the guard's effect. "Does the new step ignore the access
filter?" has the default answer "no".

### 6. Adversarial check

Write, in a few lines, the simplest patch that passes every test of the table. Then find a row that it breaks, or a
rule of `## Invariants` that it breaks. Typical finds: the patch skips a guard, treats `null` as absent, compares
the top field and not its children, changes one twin only, or treats an unchanged value in a full payload as a
change. A patch that respects a guard is never the rejected patch, unless the report asks to pass the guard. For each find, add a row and a test, and do the check
again. Record the last check:

| Simplest patch | What it breaks | Row added |
| --- | --- | --- |
| mark all locales `draft` when any non-localized key is in `data` | B2: the admin UI sends every field | B2 |

### 7. Check the spec

```bash
node "${CLAUDE_PLUGIN_ROOT:-<directory of this skill>/../..}/skills/solution-spec/scripts/spec-check.mjs" <spec.md>
```

It finds a missing section, a guard with no outcome or no test, a behaviour row with no test, an open decision, and
a "must not change" sentence with no test. Exit 0 means the spec is closed. For an RCA, `rca-gate.mjs check` runs
the same checks.

## The writer contract

Put this in the brief of `shark:code-writer`:

- Implement each row of the behaviour table. The tests are the acceptance.
- Decide the structure yourself: names, the location of the code, helpers, the pattern to follow.
- If the code needs a behaviour that no row decides, stop and report the case to the caller. Do not choose.
