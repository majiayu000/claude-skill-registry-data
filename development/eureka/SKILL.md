---
name: eureka
description: >
  Trigger word — when the user types "eureka" after finishing a piece of work,
  review the just-completed changes and surface concrete refactor opportunities.
  Nimbus post-implementation retrospective in one shot.

  Trigger this skill when:
  - User says the word "eureka" in a message that follows a completed task.
  - User invokes `/eureka`.
---

## Behavior

1. **Identify the recent work.** Sources in order:
   - Staged + unstaged diff.
   - Last commit(s) on the current branch (since the last common ancestor with
     the default branch).
   - The current conversation's implemented changes.
2. **Review the diff** through a refactor lens:
   - Duplication that could be a helper.
   - Cross-cutting concerns that could be extracted (S3 I/O, SQS send, magic-byte
     sniff, payload build — from cidca-services convention).
   - Long functions (>50 lines) → suggest split.
   - Repeated patterns across files → consider a shared abstraction.
   - Dead code / unreachable branches.
   - Missing types / `any` / `Any`.
   - Uncovered code paths that would benefit from a test.
   - Comments explaining WHAT (should be code) vs comments explaining WHY (keep).
3. **Emit findings** as a short prioritized list. Each finding:
   ```
   <path>:<line>: <one-line opportunity>. <suggested change>.
   ```
4. **End** with a one-line summary: `N opportunities. Ordered by ROI.`

## Do not

- Suggest a full rewrite. Small, incremental refactors only.
- Suggest refactors that would require follow-up in another repo unless the
  user asks.
- Suggest style / format changes — that's `preflight`'s job.
- Praise the work. Just findings.
- Fire eureka unprompted. The user must say the word.

## Nimbus-specific "always-check" refactor smells

- **cidca-services `lambda_handler.py`** methods > 50 lines → mandatory split.
- **cidca-platform ecg_auto** views > 50 lines → same, delegate to `services/`.
- **horus services/api** business logic in routers instead of `services/` → move.
- **All Nimbus repos**: `TODO` / `FIXME` without owner or date → suggest owner.
- **cidca-platform ecg-ui**: hardcoded `#fff` / `#000` where theme tokens exist.
- **horus web**: hardcoded Tailwind color classes bypassing dark-mode tokens.

## Length cap

Max 15 findings. If more, top 15 by ROI. Anything below that isn't worth a
retrospective.
