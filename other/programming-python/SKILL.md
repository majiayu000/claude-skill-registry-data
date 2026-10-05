---
name: programming-python
description: >-
  Guides Python work under the Python standard: annotating every signature for Pyright in strict mode, handling paths as
  pathlib values, placing tests by the boundary they touch, and judging data shapes, failures, and async code.
when_to_use: >-
  Use when writing, changing, or reviewing Python code, before the first test of the change.
compatibility: Requires a Python project with Pyright and its recorded linter, formatter, and test runner.
---

# Python Programming

Every Python rule is owned by
[Python Standards](../../../repo-governance/development/quality/stacks/python-standards.md).
[Test-Driven Development](../../../repo-governance/development/tdd-policy.md) and
[Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md) govern tests and gates,
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) runs each cycle, and
[Developing Applications](../developing-applications/SKILL.md) carries the judgement on layers, errors, logs, and input
that holds in every language. This skill adds only the procedure and judgement of applying them in Python. Where a
sentence here seems to state a rule, the standard decides.

## Start From What the Project Records

Read the Pyright configuration, the linter's rule selection, and the recorded choices for boundary validation and
expected failures. Run Pyright, the linter, the formatter check, and the unit tests with coverage on the untouched tree.
A gate already failing is handled under
[Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md). A path left outside
strict mode without a stated reason is a finding to raise, not a place to add code.

## Make the Type Checker Mean Something

Annotate a function's signature before writing its body. When Pyright rejects a change, fix the code; the standard lists
what counts as a waiver, and reaching for one means the design needs attention.

| While writing, you meet                         | Ask                                                      |
| ----------------------------------------------- | -------------------------------------------------------- |
| a value whose shape is not known yet            | can it be `object`, narrowed, or a `Protocol`?           |
| a library returning unknown types               | does a stub exist, or should one be written?             |
| parsed input with an annotation on it           | where is the check that makes the annotation true?       |
| a string that names a file                      | should it have become a `pathlib.Path` where it came in? |
| a function returning one of two unrelated types | should it be two functions, or return one shape?         |

## Place a Test by What It Touches

Fixtures that create a temporary directory or set an environment variable reach a real filesystem or environment, which
the unit layer excludes, so a test using one belongs to the integration suite. To keep a decision under unit test, pass
in the text, the parsed value, or the setting, and let the shell do the reading.

Parametrize rows of one behaviour, giving each row an id that names its case, and add a row for a new behaviour only
after watching it fail.

## Shape Data Deliberately

Before adding a class, ask whether its instances have identity or are values; a value is the frozen dataclass the
standard names. A default argument that is a list or a dictionary is shared by every call that omits it, so look for one
in every signature you touch.

## Keep the Event Loop Moving

- A synchronous call inside `async def`, such as a file read, `time.sleep`, or a synchronous client, stalls every task
  on the loop. Move it off the loop, for example with `asyncio.to_thread`.
- `asyncio.run` belongs at the program's entry point only.
- Hold a reference to every task created, or create it inside a task group. The loop keeps only a weak reference, and an
  unreferenced task can vanish before it finishes.

## Before Handing Off

- Pyright in strict mode, the linter, and the formatter report nothing;
- every new signature is annotated, and every waiver carries its reason;
- no unit test writes a file, reads the environment, or waits on a real clock;
- no synchronous call blocks inside async code; and
- each recorded red failed on an assertion about the missing behaviour.
