---
name: verify-behavior-preserved
description: >-
  Load this skill before a change meant to alter no behavior (a refactor, rename, dependency
  upgrade, or port): pin a baseline first, then diff old against new. Trigger on "refactor this",
  "clean this up", "upgrade this dependency", "make sure nothing broke".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree, to compare before and after the refactor,
  plus the target project's own test runner (`pytest` via `uv run`, or `vitest` via `bun`) since
  the whole method is running the same suite on both sides. Neither is assumed installed.
license: Apache-2.0
---

# Verify Behavior Was Preserved

A refactor has a property no feature has: you know the correct answer before you start — it is
whatever the code does today. That makes the strongest oracle in testing available for free, and
almost nobody uses it.

The failure mode is refactoring against a thin suite, watching it stay green, and shipping a silent
behavior change. Green on a suite that never covered the region proves nothing.

The task is done when the pins were committed before the change, the suite is green with no test
edits, and the differential run shows no divergence or each divergence is declared.

## What waits for a request

Writing and running the tests that prove the refactor preserved behavior is part of the refactor, so
the steps below apply without being asked: the coverage check on the region, characterization tests,
golden files, the separate commit of the pins on the feature branch, and the differential run. Only a
slow or paid run waits for a request: the full suite, coverage beyond the region being changed,
mutation testing, or repeated passes over the whole suite. When one of those would help and was not
requested, name the command and what it would reveal, and state what stays unverified.

## Procedure

### 0. Name the fact the change's safety rests on

Before the steps below, write one sentence: the fact that, if false, makes this refactor break
something ("`total()` is the only caller of `round_cents()`"). Then prove it at the highest rung
that is cheap, and say which rung you reached:

| Rung | Evidence                                                 |
| ---- | -------------------------------------------------------- |
| 1    | Said so                                                  |
| 2    | Pointed at the line that makes it true                   |
| 3    | Walked the failure: traced what happens if it were false |
| 4    | Ran code that shows it                                   |
| 5    | Reproduced it in the running app                         |

Rungs 1 and 2 are claims, not proof. Steps 1 to 4 below are how you reach rung 4.

### 1. Check the baseline before touching anything

```bash
pytest --cov=app.pricing --cov-report=term-missing     # the region you are about to change
```

**If coverage of that region is at or near zero, writing tests is the first task**, not the
refactor. Refactoring uncovered code is editing blind.

### 2. Pin current behavior with characterization tests

Where the suite is thin, capture what the code does **right now** — feed it realistic inputs, record
the actual outputs, assert them.

You are pinning, not judging. If current behavior looks wrong, pin it anyway and note it: a refactor
is not the place to fix it, and if it turns out to be load-bearing for a caller you will be glad the
test caught the change.

```python
# characterization — asserts today's behavior, including the odd rounding
@pytest.mark.parametrize(
    "total,tier,expected",
    [
        (100.00, "gold", Decimal("85.00")),
        (100.005, "gold", Decimal("85.01")),  # banker's rounding — pinned deliberately
        (0.00, "gold", Decimal("0.00")),
        (
            -5.00,
            "gold",
            Decimal("-5.00"),
        ),  # negative passes through today; pinned, not endorsed
    ],
)
def test_discount_current_behavior(total, tier, expected):
    assert discount(total, tier) == expected
```

Generate the input list from real data where you have it — production samples, fixtures, a log
replay — because hand-picked inputs cluster on the paths you already have in mind.

### 3. Golden files for large or structured output

When the output is a document, a rendered page, a query plan, or a large object, assert against a
recorded file rather than inline literals.

```bash
python -m app.render sample_input.json > tests/golden/report.expected.json   # BEFORE the change
git add tests/golden/report.expected.json && git commit -m "test: pin render output"
```

Commit the golden file **before** the refactor, on its own. Then the refactor's diff shows whether
the output moved, and the review sees it.

### 4. Differential run — the strongest check

Run the old and new implementations over the same inputs and compare. No expectations to write, no
oracle to invent.

```bash
git worktree add /tmp/before HEAD              # pristine pre-change copy
# ... do the refactor in the working tree ...

python - <<'PY'
import json, subprocess
cases = [json.loads(l) for l in open("tests/fixtures/replay.jsonl")]
for c in cases:
    before = subprocess.run(["python","-m","app.cli"], cwd="/tmp/before",
                            input=json.dumps(c), capture_output=True, text=True).stdout
    after  = subprocess.run(["python","-m","app.cli"],
                            input=json.dumps(c), capture_output=True, text=True).stdout
    if before != after:
        print("DIVERGED:", c); print(" before:", before); print(" after:", after)
PY

git worktree remove /tmp/before
```

For an in-process version, import both implementations and compare directly — keep the old one under
a temporary name until the diff run passes, then delete it.

Feed it generated inputs if you have no corpus: a property-based generator comparing old against new
is the cheapest high-coverage differential test there is (see `ceh-testing:design-test-cases`, rung 6, "oracle").

### 5. The rule that makes all of it worth something

**If you had to edit a characterization test or update a golden file to get green, behavior
changed.**

That is the entire signal. When it fires, exactly two responses are legitimate:

1. Revert — the change was supposed to preserve behavior and did not.
2. Declare it — the change is intentional. Say so explicitly, in the commit body and the PR, showing
   the before/after values and why the new one is correct.

Silently regenerating the golden file because the new output "looks fine" throws away the only
protection the process gave you. Treat an unexplained snapshot update in review as blocking.

### Dependency and runtime upgrades

Same protocol, and the divergences are subtler: serialization format, float formatting, default
timezone, sort stability, regex engine behavior, error types and messages, default timeouts.

Run the differential (step 4) with the lockfile as the only difference between the two worktrees.
Pay attention to anything you serialize, persist, or hash — a changed representation of the same
logical value still breaks stored data and cache keys.

## Rules

### Sequencing

Baseline first, always: (1) coverage check → (2) characterization tests / golden files → (3) **commit
those on their own** → (4) refactor → (5) suite green with **no test edits** → (6) differential run
for anything risky.

Committing the tests separately is what lets a reviewer see that the pins predate the change. Tests
written in the same commit as the refactor cannot prove they were not shaped by it.

Pairs with `ceh-coding-conduct:shrink-diff` and `ceh-coding-conduct:refactor-repo` — both change
working code with no behavior change intended, and neither carries a verification step of its own.
