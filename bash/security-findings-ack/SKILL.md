---
name: "security-findings-ack"
description: "Acknowledge a security-review finding (code/dependency/adversarial) so it stops resurfacing as new on future runs while staying visible in the historical record. Trigger phrases: acknowledge finding, accept risk, dismiss finding, false positive, ack finding."
argument-hint: "<finding-id> [reason]"
user-invocable: true
---

## Instructions

Contract: `specs/008-adversarial-security-review/contracts/skill-commands.md` (`/security-findings-ack`).
Schema: `specs/008-adversarial-security-review/data-model.md` (`Finding.status`).

1. Parse `$ARGUMENTS` for a `finding-id` (e.g. `code-0007`, `dep-0003`, `adv-0002`). If missing, ask the user for it — do not guess.
2. Run:

   ```bash
   .specify/scripts/bash/security-findings-store.sh \
     --findings-dir specs/008-adversarial-security-review/findings \
     ack --finding-id <finding-id> --by "$(git config user.name || echo maintainer)"
   ```

3. If the script errors with "unknown finding id", tell the user the ID wasn't found in `specs/008-adversarial-security-review/findings/findings.json` and suggest running `/security-report` to see valid IDs. Do not create a placeholder finding.
4. On success, report the new status (`acknowledged`) to the user. The finding is **not** deleted — it remains in `findings.json` and will still appear in `/security-report`, just grouped as acknowledged rather than new.
5. Note for the user: if this finding is later not reconfirmed by a subsequent full run of its source capability, it will automatically transition to `resolved` (not back to `new`) — this is expected behavior, not a bug.

## User Input

```text
$ARGUMENTS
```
