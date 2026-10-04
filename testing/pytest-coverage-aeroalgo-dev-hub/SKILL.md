---
name: pytest-coverage
description: 'Run pytest tests with coverage, discover lines missing coverage, and increase coverage on critical gaps. In this repo always use .venv/bin/pytest from repo root (never bare pytest).'
---

Find uncovered lines in modules under review. For BACK QA: spot-check packages touched by the epic diff; treat AC-critical uncovered paths as Issues. Do not claim PASS solely because coverage < 100%.

Generate a coverage report with (repo root):

.venv/bin/pytest --cov --cov-report=annotate:cov_annotate

If you are checking for coverage of a specific module, you can specify it like this:

.venv/bin/pytest --cov=your_module_name --cov-report=annotate:cov_annotate

You can also specify specific tests to run, for example:

.venv/bin/pytest tests/test_your_module.py --cov=your_module_name --cov-report=annotate:cov_annotate

Open the cov_annotate directory to view the annotated source code.
There will be one file per source file. If a file has 100% source coverage, it means all lines are covered by tests, so you do not need to open the file.

For each file that has less than 100% test coverage, find the matching file in cov_annotate and review the file.

If a line starts with a ! (exclamation mark), it means that the line is not covered by tests.
Add tests to cover the missing lines.

Keep running the tests and improving coverage until all lines are covered.
