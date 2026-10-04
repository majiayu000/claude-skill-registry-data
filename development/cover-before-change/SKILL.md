---
name: cover-before-change
kind: skill
status: ready
provenance:
  principles:
  - P047
  - P048
  - P011
  - P108
  - P141
  - P134
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00027
  - C00028
  - C00029
  - C00031
  - C00010
  - C00011
  source_anchors:
  - 1d83dc6f489c-c0001
  - 1d83dc6f489c-c0002
  authored_from_digest: 8b85c97cc7001527010df82a6b42c0a46fea6c622ab467998142e09027896b5b
---

# Cover before change

## Purpose

Decide, before touching legacy code, whether the change area is protected by tests, and if
not, put a test safety net in place first. Legacy code is code without tests, and getting
tests in place is the prerequisite for changing behaviour quickly and safely (P047). Changing
untested code carefully and hoping — "Edit and Pray" — is the central risk; the safe
discipline is "Cover and Modify": cover the code with tests, then change it, letting test
feedback catch mistakes (P048).

## When to use

- A change (feature, fix, or refactor) must be made to code that has no or insufficient
  automated tests over the change area.
- A reviewer must judge whether it is safe to proceed with a change given current coverage.

Do **not** apply when the change area is already covered by adequate automated tests — the
safety net exists, so go straight to making the change.

## Procedure

1. **Locate the change area.** Identify the exact methods/classes the change will touch.
   Understand what behaviour is at risk, since in every modification far more behaviour must
   be preserved than is altered (P011).
2. **Check for existing coverage of that area.** Ask whether tests exist that would fail if
   the planned change altered behaviour. Coverage that does not exercise the change area
   does not count.
3. **If coverage is adequate → stop here.** Proceed to make the change under the existing
   safety net; this skill does not apply.
4. **If coverage is missing or insufficient → do not Edit-and-Pray.** Treat the absence of
   tests as the risk to retire first. The up-front cost of breaking dependencies and writing
   tests usually pays back by avoiding unknown debugging time (P108). Hand off to the
   dependency-breaking and characterization-testing workflow:
   - break dependencies only as far as needed to get the area into a harness, applying the
     rare test-first exception deliberately and conservatively (P134; see
     `sensing-and-separation`),
   - write characterization tests that pin current behaviour (see
     `characterization-testing`),
   - then make the change ("Cover and Modify").
5. **Re-check after covering.** Confirm the new tests actually exercise the change area
   before modifying it. Pair on the risky dependency-breaking work, since it is easy to break
   software unknowingly (P141).

## Inputs

- The code unit to be changed and the nature of the planned change.
- Knowledge of which existing tests (if any) exercise the change area.

## Output

A go/no-go judgement: either "covered — proceed", or "not covered — cover first", naming
which part of the change area lacks a safety net and what must be tested before editing.

## References

- `characterization-testing` — how to write the safety-net tests.
- `legacy-code-change-algorithm` — the full five-step change flow this skill opens.

## Provenance

Derived from principles P047 (legacy = untested code), P048 (Cover and Modify vs Edit and
Pray), P011 (behaviour preservation is the primary constraint), P108 (up-front cost pays
back), P141 (pair on dependency-breaking), and P134 (dependency-breaking as the deliberate
test-first exception). Source is distillation-only; paraphrased, not quoted.
