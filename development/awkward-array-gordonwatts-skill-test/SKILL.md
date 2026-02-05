---
name: awkward-array
description: Guidance for working with Awkward Array 2.0 jagged arrays and records in Python. Use when building or debugging `awkward` workflows, including record construction with `ak.zip`, adding fields with `ak.with_field`, filtering/aggregation, combinatorics (`ak.cartesian`/`ak.combinations`), `argmin`/`argmax` slicing, flattening, sorting, and NumPy interop or common Awkward pitfalls.
---

# Awkward Array

## Overview

Use this skill to apply Awkward 2.0 best practices for jagged arrays, especially in HEP-style event data models. Keep guidance lean in this file and load reference notes only when needed.

## Core workflow

1. Build an event data model (records) with `ak.zip`.
2. Filter early at the event level.
3. Perform combinatorics or derived calculations.
4. Add derived fields back into the record with `ak.with_field`.
5. Repeat until the final values are present in the EDM.

## Reference guide

Load only the reference files that matches the task:

- `references/best-practices.md`: use when setting overall approach or reminding about Awkward 2.0 usage and axes.
- `references/records.md`: use when building records or adding fields.
- `references/filtering-aggregation.md`: use for boolean masking, `ak.sum`/`ak.count`/`ak.num`, and axis guidance.
- `references/sorting.md`: use for `ak.sort`.
- `references/combinatorics.md`: use for pairings or n-way combinations (`ak.cartesian`, `ak.combinations`).
- `references/argmin-argmax.md`: use when selecting min/max elements in jagged lists.
- `references/flattening.md`: use for `ak.flatten` behavior and axis rules.
- `references/numpy-interop.md`: use when mixing NumPy operations with Awkward arrays.
- `references/pitfalls.md`: use for common API mistakes and missing functions.
- `references/awkward-files.md`: use for file I/O patterns (read/write) with Awkward arrays.

## Constraints

- Use Awkward 2.0 APIs and syntax only.
- Avoid `axis=None` unless the function explicitly supports it.
- Ensure `awkward` is listed as a dependency in the active environment (venv plus `pyproject.toml` or `requirements.txt`).
