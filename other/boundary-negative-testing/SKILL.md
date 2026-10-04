---
name: boundary-negative-testing
category: qa
description: Use when building cases for any input, form, endpoint or state change - boundary values, invalid and hostile data, authz and concurrency cases with a worked example
---
# Boundary and Negative Testing

## Data catalogue

- **Strings:** empty, whitespace-only, 1 char, max, max+1, 10x max, leading/trailing spaces, emoji/ZWJ, RTL text, combining marks, `<b>x</b>` and `<img src=x onerror=alert(1)>` (must render as inert text, never execute), `' OR 1=1 --` (as literal data), `../../etc/passwd` in a filename-ish field.
- **Numbers:** −1, 0, 1, max, max+1, a decimal where an integer is expected, `1e309`, `NaN`.
- **Dates:** leap day, a DST transition, a timezone boundary, past/future limits the domain implies.
- **Files:** 0 bytes, just over the size limit, wrong MIME type with a correct-looking extension.
- **Collections:** 0 items, 1 item, exactly the page size, page size + 1.
- **Concurrency:** double submit, two sessions editing the same record.
- **Dependency down:** the stubbed dependency returns 5xx/timeout (test-data-and-stubs), or `route "**/api/<dep>/**" --status=500` for a UI-only case.

## Flow-level cases

Unauthorized access, missing resources (404 paths), concurrent/duplicate submission, partial failure of a dependency.

## Recording

Record every boundary you probed as its own test case on the task, passing ones included — absence of evidence is not evidence of absence, and a boundary nobody can see you tried is one the next reader has to try again. A boundary that cannot exist here (the field is an enum, the endpoint is internal-only) is a case too: record it `invalid` with that reason.
