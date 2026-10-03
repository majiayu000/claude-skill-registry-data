---
name: sr-improve
description: >
  Phase 8 of the SRS workflow. Generates an improvement report covering
  deferred features, technical risks, validation warnings, and next-version
  candidates. No word limit.
---

# sr-improve

Goal: produce a candid improvement report — what was deferred, what carries risk,
what should be resolved before development starts. Reference specific FR/NFR IDs.

---

## Step 0 — Identify Project

```
Ask the user: "Which project? (slug)"
```

Read from `projects/{slug}/`:
- `spec.md` (for deferred features and open items)
- `srs/appendix-b-open-issues.md` (for all [TBD] items)
- `srs/03-03-performance.md` (for [TBD] NFRs)
- Validator output if available (WARNs from `$sr-validate`)

---

## Step 1 — Write improvement-report.md

Write `projects/{slug}/improvement-report.md`. No word limit.

### §1 — Deferred Features (Next Version Candidates)

List every feature marked OUT of scope in spec.md that the user mentioned but deferred.
For each:
- Feature name
- Why deferred (user's reason from brainstorm, if stated)
- Estimated effort level (low | medium | high) — AI estimate only, not a commitment
- Suggested version: v1.1 | v2.0 | unknown

### §2 — Technical Risks

For each unresolved [TBD] in NFRs:
- NFR-ID + description
- What data is needed to set the target
- Risk if unresolved: (A) test cannot be written (B) SLA cannot be committed (C) architecture decision blocked
- Suggested owner + resolve-by milestone

For each external integration in §3.1:
- Integration name + system
- Risk: dependency on third-party uptime / API versioning / rate limits
- Mitigation suggestion

### §3 — FR Refinement Suggestions

Identify FRs that are:
- Too broad (combines multiple behaviors that should be separate FRs)
- Missing negative cases (what happens when it FAILS?)
- Missing actor variants (same action, different permission level)

List each with the suggested split or addition.

### §4 — NFR Gaps

NFRs with [TBD] Response Measure → list with: what benchmark test would produce the real number.
NFRs with adjective-only measure (should have been caught by validator) → rewrite suggestion.

### §5 — Validation Warnings

Enumerate every WARN from `$sr-validate` with:
- Warning text
- Which file/FR/NFR it refers to
- Recommended resolution (specific action, not "review this")
- Urgency: must resolve before dev | should resolve before QA | can defer

### §6 — Process Recommendations

Observations about the requirements process itself:
- Rounds where user input was vague → note the topic area for follow-up workshop
- Assumptions that carry high invalidation risk → flag for stakeholder sign-off
- Missing subject-matter expert input (e.g., "no security architect reviewed NFR-02")

---

## Step 2 — Handoff

Output:
```
Improvement report: projects/{slug}/improvement-report.md

Deferred features:      {count}
Technical risks:        {count}
FR refinement items:    {count}
NFR gaps:               {count}
Validation warnings:    {count}
Process recommendations:{count}

Next: $sr-save → saves project context files for future sessions
```
