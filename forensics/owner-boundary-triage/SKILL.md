---
name: owner-boundary-triage
description: Use when an AI must decide whether a failure belongs to a feature owner, shared capability owner, data owner, environment owner, or verifier.
---

# Owner Boundary Triage

## Core Principle

Owner conclusions require both reproduction breadth and mechanism attribution. A shared-looking source file is not proof that every consumer belongs to the shared owner.

## Required Signals

- Where the failure reproduces.
- Where it does not reproduce.
- Which mechanism appears responsible.
- Which owner controls that mechanism.
- Which consumers are affected.
- Which evidence is missing.

## Triage Flow

1. Define the failing behavior in one sentence.
2. Map reproduction breadth:
   - single route or surface,
   - multiple consumers of one capability,
   - all consumers of a shared capability,
   - data-source-specific,
   - environment-specific.
3. Attribute mechanism:
   - feature composition,
   - shared component,
   - data schema,
   - permissions,
   - environment or harness,
   - acceptance wording.
4. Assign owner only when breadth and mechanism agree.
5. If they do not agree, return `owner_boundary_unclear` with the smallest next check.

## Verdict Vocabulary

| Verdict | Use When |
| --- | --- |
| `feature_owner` | Failure is isolated to a feature composition or route-specific integration. |
| `shared_capability_owner` | Failure reproduces across consumers and mechanism is in the shared capability. |
| `data_owner` | Failure depends on data schema, lifecycle, or seed shape. |
| `environment_owner` | Failure depends on setup, harness, browser, network, or fixture availability. |
| `verifier_owner` | Failure is in the evidence, receipt wording, or acceptance procedure. |
| `owner_boundary_unclear` | Reproduction breadth or mechanism attribution is insufficient. |

## Output Contract

```md
verdict:
failure_summary:
reproduction_breadth:
mechanism_attribution:
excluded_owners:
missing_checks:
next_owner:
return_gate:
return_owner_on_fail:
```

## Common Mistakes

- Assigning a shared owner because code lives in a shared folder.
- Assigning a feature owner because the bug was first seen on one page.
- Ignoring negative reproduction evidence.
- Treating verifier wording mistakes as runtime defects.
- Asking one owner to fix another owner's missing evidence.

## Minimum Owner Claim

Use the narrowest owner conclusion that the evidence supports. If one more reproduction check would change the owner, do that check or return `owner_boundary_unclear`.
