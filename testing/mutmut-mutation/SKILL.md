---
name: mutmut-mutation
description: "Configures mutmut for Python mutation testing - `pip install mutmut`, runs via `mutmut run`, browses results via `mutmut browse` or `mutmut results`, applies surviving mutants to disk via `mutmut apply {id}`, suppresses with `# pragma: no mutate` annotations. Configures via `setup.cfg` / `pyproject.toml` with `source_paths` + per-test selection. Use for Python codebases needing mutation-quality verification of pytest / unittest suites."
---

# mutmut-mutation

## Overview

Per [mutmut-docs][md]:

[md]: https://mutmut.readthedocs.io/en/latest/

> "Mutmut is a mutation testing system for Python, with a strong
> focus on ease of use." ([mutmut-docs][md])

Key features per [mutmut-docs][md]:

- "Found mutants can be applied on disk with a simple command making
  it very easy to work with the results"
- "Remembers work that has been done, so you can work incrementally"
- "Knows which tests to execute, speeding up mutation testing"
- "Interactive terminal based UI"
- "Parallel and fast execution"

## When to use

- A Python codebase has a pytest / unittest suite with high coverage
  and the team wants to verify the assertions.
- A specific module needs mutation-quality verification before
  shipping a release.
- The team is debating "should we add another test?" - surviving
  mutants tell you where.

## How to use

1. `pip install mutmut` and confirm the pytest / unittest suite is green before mutating.
2. Scope the run in `setup.cfg` or `pyproject.toml` (`source_paths` + test selection) so only project source is mutated.
3. Run `mutmut run` - the first run is slow; state is cached so later runs are incremental.
4. Read the score with `mutmut results`; open survivors interactively with `mutmut browse`.
5. For each survivor, write a test that kills it; verify with `mutmut apply <id>`, re-run that test, then revert.
6. Reserve `# pragma: no mutate` for genuinely unreachable lines only.
7. Wire a weekly full run plus PR-scoped runs into CI, uploading `mutmut results` as an artifact.

## Step 1 - Install + first run

Per [mutmut-docs][md]:

```bash
pip install mutmut
mutmut run
```

`mutmut run` "automatically detects test folders ('tests' or
'test') and locates source code" ([mutmut-docs][md]).

The first run is slow (full suite per mutant); subsequent runs use
the cached state.

## Step 2 - Configure

Per [mutmut-docs][md], settings go in `setup.cfg` or
`pyproject.toml`:

```ini
[mutmut]
source_paths=src/
pytest_add_cli_args_test_selection=tests/
```

Or in `pyproject.toml`:

```toml
[tool.mutmut]
source_paths = ["src/"]
pytest_add_cli_args_test_selection = "tests/"
```

Common config:

| Setting                                | Use                                                       |
|----------------------------------------|-----------------------------------------------------------|
| `source_paths`                          | Which files to mutate.                                     |
| `pytest_add_cli_args_test_selection`    | Which tests to run per mutant.                            |
| `runner`                                | `pytest` (default) or `python -m unittest`.               |
| `tests_dir`                             | Override auto-detected test directory.                     |
| `do_not_mutate`                         | Regex of files / lines to skip.                            |

## Step 3 - Browse results

Per [mutmut-docs][md], "Results are explored via `mutmut browse`,
where mutants can be retested or written to disk using `mutmut
apply <mutant>`."

```bash
mutmut browse        # interactive TUI
mutmut results       # summary table
mutmut show <id>     # show specific mutant diff
```

Output:

```
Total: 142
Killed: 119 (83.8%)
Survived: 23 (16.2%)
Timeout: 0
Suspicious: 0
```

## Step 4 - Mutators

Per [mutmut-docs][md], common mutations include:

> "Integer literals are changed by adding 1. So 0 becomes 1, 5
> becomes 6, etc."
>
> `<` becomes `<=`
>
> `break` converts to `continue` and vice versa

Other mutators: arithmetic (`+` → `-`), comparison flipping,
constant replacement, statement removal.

## Step 5 - Suppress with pragmas

Per [mutmut-docs][md]:

> Use code comments to skip specific areas:
> - `# pragma: no mutate` (single line)
> - `# pragma: no mutate block` (indentation blocks)
> - `# pragma: no mutate start/end` (arbitrary ranges)

```python
def divide(a, b):
    if b == 0:                  # pragma: no mutate
        raise ZeroDivisionError("intentional unreachable")
    return a / b
```

Use sparingly - each pragma is a confession that a line isn't
mutation-tested. Reviewable in PRs.

## Step 6 - Apply a survivor

Once a surviving mutant is identified, write a test that catches
it. To verify the test catches this specific mutation:

```bash
mutmut apply <mutant-id>     # writes the mutant to disk
pytest tests/affected_test.py # the new test should fail
git checkout src/             # revert the mutant
```

This proves the test catches the specific bug class.

## Step 7 - CI integration

```yaml
- name: Mutation testing
  if: github.event_name == 'schedule'   # weekly
  run: |
    pip install -e '.[dev]'
    pip install mutmut
    mutmut run --max-children 4
- name: Surface results
  if: always()
  run: mutmut results > mutation-summary.txt
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: mutation-results
    path: mutation-summary.txt
```

For PRs, mutmut doesn't have native incremental mode; use
`source_paths` to scope to changed files via a wrapper script:

```bash
CHANGED=$(git diff --name-only origin/main...HEAD | grep '^src/')
mutmut run --paths-to-mutate "$CHANGED"
```

## Worked example

A team wants to verify the pytest suite for `src/discounts.py` before a release.

1. Scope the run in `setup.cfg`:
   ```ini
   [mutmut]
   source_paths=src/discounts.py
   pytest_add_cli_args_test_selection=tests/test_discounts.py
   ```
2. `mutmut run`, then `mutmut results`:
   ```
   Total: 142
   Killed: 119 (83.8%)
   Survived: 23 (16.2%)
   ```
3. `mutmut browse` shows a survivor: the boundary `if total > 100:` mutated to `if total >= 100:` - the suite never exercises `total == 100`.
4. Add a test for the no-discount path at `total == 100`, then confirm it catches the mutant:
   ```bash
   mutmut apply <id>                 # id from the browse listing
   pytest tests/test_discounts.py    # now fails on the mutated line
   git checkout src/                 # revert the mutant
   ```
5. Re-running `mutmut run` shows the mutant killed and the score up by one mutant.

## Pitfalls and limitations

Anti-patterns (pragma escape hatches, full-mutation-per-PR, third-party `source_paths`, unrealistic gates) and mutmut's limitations (slow runs, no native PR diff scoping, equivalent mutants) are catalogued in [references/mutmut-pitfalls.md](references/mutmut-pitfalls.md).

## References

- [md][md] - mutmut overview: ease of use, incremental work,
  intelligent test selection, parallel execution, configuration via
  `setup.cfg` / `pyproject.toml`, mutator examples (integer
  literals, comparison flipping, break/continue).
- `stryker-mutation`,
  `stryker-net-mutation`,
  `pitest-mutation`,
  `mull-mutation` - per-language
  siblings.
