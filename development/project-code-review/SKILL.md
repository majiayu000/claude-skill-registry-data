---
name: project-code-review
description: Review a diff against dynamic-neural-field-composer's own standards - backwards compatibility, Clean Code, tools/ helper reuse, C++20 idiom, hot-path performance, and test coverage. Use before opening a PR or when asked to review a branch or change.
---

# Project code review

Review `git diff origin/main...HEAD` (or the diff you were given) against the checks below.
This deliberately overlaps `.coderabbit.yaml` so problems surface locally before CodeRabbit
posts them on the PR.

## 1. Backwards compatibility (highest severity)

Not a finding to note - a **stop condition**. If the diff breaks compatibility, say so
first and stop; do not continue reviewing style.

Look for: changed public signatures in `include/`, altered default parameter values,
changed behaviour of an existing element, and any change to the `.dnf` serialization
format that older files would not survive.

## 2. Clean Code

Per `CONTRIBUTING.md`:

- Names that read like prose. `n`, `tmp`, `data2` are findings.
- Small, single-responsibility functions. A function that needs a comment to explain its
  sections wants to be several functions.
- **No raw owning pointers.** `shared_ptr` / `unique_ptr` only.
- No comments that explain *what* the code does. Only *why*, and only when non-obvious.
- Clarity over cleverness - if a reader has to stop and decode a line, it is a finding.

## 3. Helper reuse

Every new free function: does something equivalent already live in `tools/`?

Search `include/tools/math.h`, `utils.h`, `profiling.h`, `logger.h`, `fft_convolution.h`,
`simd_dispatch.h`, and `include/exceptions/exception.h` before accepting it.

Also flag helpers defined at a call site that *should* move into `tools/` - a numeric or
utility function sitting in an element `.cpp` is misplaced.

## 4. Modern C++20

Flag missed opportunities where they genuinely improve the code:

- `std::span` instead of `const std::vector<double>&` for read-only array views
- `std::string_view` for read-only string parameters
- `[[nodiscard]]` on accessors and anything whose result must not be dropped
- ranges, structured bindings, `std::format` over manual concatenation
- `enum class` over bare `enum`

Do not flag idiom for its own sake. If the change is cosmetic and the file is consistent
as-is, leave it.

## 5. Performance

This is a simulation library; the step loop runs thousands of times a second.

- Copies of heavy objects - field matrices, kernel vectors, `std::vector<double>` returned
  by value from an accessor
- `shared_ptr` copies (atomic refcount) inside `step()` or any per-iteration path
- Allocation inside the step loop that could be hoisted or reused
- Repeated map/string lookups in a hot path

## 6. Tests

- New or changed behaviour in `elements/`, `simulation/` or `tools/` with no test
- **A new test file not added to `tests/CMakeLists.txt`** - it is silently never compiled
  and the suite goes green having never run it. Check this explicitly every time.
- Floating-point assertions without an explicit tolerance
- A test that would pass against the unfixed code, i.e. does not actually pin the bug

## Output

Order findings most severe first. For each: file:line, one sentence on what is wrong, and
the concrete failure it causes or the standard it violates.

Say "clean" when it is clean. Do not manufacture findings to look thorough - a short honest
review beats a padded one.
