---
name: test-data
description: Use when a new function or a new table needs tests, to write test data with the edge cases and the expected result written first, never from production data.
argument-hint: "[function or table]"
---

# Test data

The job: small test files with the edge cases, and the expected result decided first.

Input: the function or the table under test.

## Steps

1. Name the function or the table under test, and what it must do with each edge case.
2. Synthetic rows from the metadata, in the source's own format. Never real data.
3. The expected result first: what the output must hold, written before the code.
4. Injected faults, each with its expected result: a broken line, a new column, broken bytes, a child row before its parent.
5. A second delivery with drift: a renamed column that the schema check must stop.
6. The fixtures beside the tests, never in the data folders.
7. Run the tests and report which passed.

## Output

The test files beside the tests: the input rows, the injected faults, the expected result written first, and the test that compares them.

## Reads

- the metadata of the table, the file parsers of the source's format

## Writes

- the fixtures of the test, and the test

## Never

- Never reads production data for a test.
- Never writes under the data folders.
