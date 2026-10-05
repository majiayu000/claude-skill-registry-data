---
name: "security-report"
description: "Regenerate and show the consolidated security-review findings report across all three review capabilities (code, dependency/CVE, adversarial), prioritized together. Trigger phrases: security report, findings report, show findings, consolidated security review, what security issues exist."
argument-hint: "(no arguments)"
user-invocable: true
---

## Instructions

Contract: `specs/008-adversarial-security-review/contracts/skill-commands.md` (`/security-report`).
Requirements satisfied: FR-007, FR-009, SC-001, SC-005, Edge Case §2.

1. Run:

   ```bash
   .specify/scripts/bash/security-report-render.sh \
     --findings-dir specs/008-adversarial-security-review/findings \
     --out specs/008-adversarial-security-review/findings/report.md
   ```

2. Read the regenerated `specs/008-adversarial-security-review/findings/report.md` and present it to the user (do not just say "done" — show the actual findings, since the point of this command is visibility).
3. If the report shows zero findings across all three capabilities, say so explicitly — do not treat this as an error or omit output. This is expected the first time any of the three review capabilities is run.
4. If the report shows findings from only one or two of the three capabilities, that's expected too if the others haven't been run yet — do not imply the missing capabilities found nothing; say they simply haven't been run.
5. If any finding's severity is `critical`, call it out explicitly at the top of your response before the full report, so the maintainer doesn't have to scan for it.

## User Input

```text
$ARGUMENTS
```
