---
name: bug-report-writing
category: qa
description: Use when any case fails or you reject a criterion - what goes in the review_criterion note, the failed case and the numbered need_revision comment, with severity
---
# Bug Report Writing

A defect's evidence lives in three places, each with its own job — never duplicate the full report into all three:

| Place | Contents |
|---|---|
| Failed case | `actual` = the observed output, verbatim. `evidence` = exact command/flow plus frequency, e.g. "3/3". |
| Rejected criterion note | Expected (quote the criterion), actual, reproduction, environment: short SHA, URL/base, width or device, browser/runtime. |
| need_revision comment | A numbered **index**, one line per defect: `1. [AC2 · case "export rejects >10k rows"] 500 instead of 422 — S2`. Keep it inside the 15-line comment budget (concise-board-comments) — the reproduction lives in the criterion note and case evidence, not here. |

## What fails the task

A task fails when:
- (a) a criterion or a human requirement comment is unmet;
- (b) the team UI floor is broken, by a measured threshold: horizontal overflow at any of 360/768/1024/1440, a touch target <44px at 360, an input font <16px at 360, body contrast <4.5:1, a missing loading/empty/error state on a changed view, an uncaught console error or failed request in the flow, a broken image/icon, a critical/serious axe violation inside a changed screen;
- (c) a crash, data loss, a security or authz hole, or a regression of adjacent behaviour.

Anything else — taste, polish beyond the floor — is a note on the criterion, never a failure.

## Rules

- **Title** names the problem, not the fix, under 60 characters: "Export of >10k rows returns 500", not "Fix export pagination".
- **Isolate** to the first failing step; give the minimal reproduction, not the whole scenario.
- **Separate observation from speculation.** A location from a stack trace or a `grep_code` hit is fine (the named debugging exception); a proposed fix is not your job.
- **Severity**, worst wins: S1 data loss/security hole > S2 broken flow (criterion unmet) > S3 degraded UX (UI-floor violation) > S4 cosmetic (never fails the task on its own — see qa-criterion-verdicts).
- **Never invent a file path.** A screenshot has none; describe width/URL/what-it-showed instead (ui-visual-evidence).
- **One defect per case/criterion entry** — do not bundle unrelated failures into one note.

## Worked Example

❌ `"Export broken"` — no repro, no expected, no severity.

✅
```
Case: export-pagination-10k (failed, 3/3)
actual: HTTP 500, body {"error":"internal"}
evidence: curl -X GET "$BASE/api/export?limit=10001" -H "Authorization: Bearer $TOKEN" — ran 3x, same result

Criterion note (AC2, rejected):
Expected: "requests over the 10,000-row limit return 422 with a clear message" (AC2)
Actual: 500 with no message, see case export-pagination-10k
Repro: curl -X GET "$BASE/api/export?limit=10001" ...
Env: SHA a1b2c3d, http://localhost:5173, desktop 1440

need_revision comment:
1. [AC2 · case "export-pagination-10k"] 500 instead of 422 at limit+1 — S2
```
