---
name: lbh-customize
version: 1.0.0
description: Customize an installed legal skill's settings — jurisdiction defaults, tone, autonomy, and enforced conditions — without weakening its security posture.
author: matrixx0070
tags: [legal, customization, configuration, tuning, autonomy]
capabilities: []
---

## When to use

Use this when a user wants an installed legal skill tuned to their situation — set a default jurisdiction, adjust drafting tone, cap autonomy to suggest-only, or narrow trigger phrases. You change configuration, not the skill's vetted body.

**Not for:** editing the skill's instructions or code (that would invalidate its QA verdict — re-vet via `lbh-skills-qa` instead), installing (`lbh-skill-installer`), or updating versions (`lbh-auto-updater`).

## Method

1. List the skill's exposed, safe-to-change settings: default jurisdiction, doc-type defaults, tone/formality, autonomy level, and trigger scope.
2. Confirm you are changing settings only. If the request needs a body change, stop and route to re-vetting — customization must not alter the reviewed artifact.
3. Never relax an enforced security condition. A "no-network" or "sandbox-only" constraint from the gate is not a user-tunable setting.
4. Apply the change as configuration layered over the immutable skill, so the vetted body and its checksum are unchanged.
5. Validate the new config: jurisdiction is real, autonomy is within the user's tolerance from intake, triggers don't collide with another installed skill.
6. Record the config delta with a timestamp so it can be reviewed or reverted independently of the skill version.

## Example

User wants `employment-contract-draft` to default to US-California, formal tone, suggest-only. You set those as layered config, leave the skill body untouched, and confirm the checksum is unchanged. They also ask to "let it fetch salary data online" — that would relax the gate's no-network condition, so you refuse and explain the condition is fixed by security review.

## Pitfalls

- Editing the skill body to customize. That breaks the QA guarantee; use layered config only.
- Loosening an enforced security condition on user request. Conditions from the gate are locked, not preferences.
- Setting an autonomy level above the intake tolerance, so the skill edits documents a suggest-only user never sanctioned.
- Creating trigger overlaps with another installed skill, causing ambiguous firing.

## Output format

```
# Customize — <name>@<version>
CHANGED (config only):
- jurisdiction default: <old> -> <new>
- tone: <...>  autonomy: <suggest|edit>  triggers: <scope>
LOCKED (unchanged): security conditions=<no-network|sandbox|...>
BODY: unchanged (checksum=<hash> stable)
VALIDATION: jurisdiction-real=<y> autonomy<=intake=<y> trigger-collision=<none>
RECORDED: config-delta at=<ts>
```

## Reference

**Skill-vetting checklist (customize link):** customization must leave the vetted body and checksum intact; only declared, safe settings are tunable, and the QA verdict remains valid.

**Security-review gate criteria:** conditions imposed by the gate (no-network, sandbox-only, no-write, disclaimer) are locked and cannot be relaxed through customization; any request to do so is refused and routed back to review.

**Versioning / rollback:** store config deltas separately from the skill version so a config change can be reverted without a version rollback, and a version rollback preserves or re-applies the intended config.
