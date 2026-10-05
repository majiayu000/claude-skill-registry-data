---
name: "security-findings-link"
description: "Link two or more security-review findings (possibly from different capabilities) as the same underlying issue, so the consolidated report collapses them into one entry instead of presenting them as unrelated. Trigger phrases: link findings, same issue, duplicate finding, merge findings, related finding."
argument-hint: "<finding-id> <finding-id> [finding-id...]"
user-invocable: true
---

## Instructions

Contract: `specs/008-adversarial-security-review/contracts/skill-commands.md` (`/security-findings-link`).
Rationale: `specs/008-adversarial-security-review/spec.md` Edge Cases §2 — "the same underlying issue... found by more than one review capability... the consolidated view MUST make it clear these are the same underlying issue rather than presenting them as two unrelated findings."

1. Parse `$ARGUMENTS` for two or more finding IDs (e.g. `code-0007 adv-0002`). If fewer than two are given, ask the user for at least one more — linking a single ID is meaningless.
2. Before linking, briefly confirm with the user (in your response, not by re-asking) that the findings genuinely describe the same underlying issue — e.g. by reading each finding's `description`/`evidence` from `specs/008-adversarial-security-review/findings/findings.json` and summarizing why they look like duplicates. This is a judgment call the maintainer should be able to sanity-check, not a fully automatic decision.
3. Run:

   ```bash
   .specify/scripts/bash/security-findings-store.sh \
     --findings-dir specs/008-adversarial-security-review/findings \
     link --finding-ids <id1>,<id2>[,<id3>...]
   ```

4. If the script errors with "unknown finding id", tell the user which ID wasn't found and suggest `/security-report` to see valid IDs.
5. On success, tell the user the findings are now linked and will render as a single consolidated entry (with a "Detected by" line listing every contributing capability) next time `/security-report` runs — suggest running it now if they want to see the result immediately.

## User Input

```text
$ARGUMENTS
```
