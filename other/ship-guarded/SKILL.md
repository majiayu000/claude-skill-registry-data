---
name: ship-guarded
description: Production-guard ship pipeline for tools where change-failure cost is real (the user relies on the tool day-to-day, breakage hurts). Same as ship-auto, but inserts a regression / UX-break risk assessment before merge — pauses only when the change actually touches risk surface (user-facing flows, removed features, schemas, perf-sensitive paths). Otherwise ships autonomously.
---

# Ship Guarded

For repos where the change-failure cost is real because the user relies on the tool in production. Same pipeline as `ship-auto` (code review → PR → CI → Copilot), with one extra step before merge: a structured risk assessment. The assessment is the gate, not "want me to merge?". If assessment shows no risk surface, merge without asking.

## Pipeline

### 1–5. Same as ship-auto

Code review (Claude + codex parallel), DoD, create PR, monitor CI, monitor Copilot. See `ship-auto` for details.

### 6. Risk assessment (the guard)

Before merging, evaluate the diff against these risk surfaces:

| Risk surface | Examples |
|---|---|
| **User-facing flow** | Routes, page renders, form behavior, navigation, key UI states |
| **Removed feature** | Deleted endpoint, removed prop, dropped CLI flag, removed config key |
| **Schema / storage** | Migration, JSON shape change in saved data, breaking format change |
| **Perf-sensitive path** | Code in a hot loop, request handler, render path, index/query change |
| **External integration** | Auth flow, payment, third-party API contract, webhook payload |

**If the diff touches none of those:** merge without asking. Proceed to step 7.

**If the diff touches one or more:** surface to the user in a single message:
- Which risk surface(s) the change touches
- The specific lines/files implicated
- A 1-2 sentence assessment of likely failure modes
- Suggested manual smoke test (one or two specific user paths to verify in dev)
- Recommendation: merge / hold / split

Wait for the user's greenlight, then merge.

### 7. Merge

`gh pr merge <pr-url> --squash --delete-branch`.

### 8. Deploy (if applicable)

Same as `ship-auto` step 7.

## D-class — same as ship-auto

Pause on the immovable gates: breaking-change merges to default branch, public deploys of breaking changes, external sends, irreversible deletes, force-pushes. The risk assessment in step 6 is *additional* to D-class, not a replacement.

## Principles

- **Risk assessment runs always; pause only on real risk.** Don't pause for "what if?" — evaluate the diff against the surfaces above; if nothing matches, ship.
- **Specific surfaces, not vibes.** A change that doesn't touch any of the listed risk surfaces is auto-mergeable. A change that touches `src/routes/` or `prisma/schema.prisma` or auth code definitely surfaces.
- **One message, not a back-and-forth.** When you do pause, give the user everything he needs to decide in a single surface (assessment + smoke test + recommendation).
- Same channel-events / fix-forward / batch-notifications principles as `ship-auto`.
