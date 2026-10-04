---
name: emperor-capture
description: >-
  Emperor Time — CAPTURE / Chain Jail. Hunt, adapt, or author a missing skill,
  then pin, get consent, trial, register. Use when a needed capability is
  absent from this harness. Never bind an unpinned web skill.
license: MIT
metadata:
  version: 0.4.13
  chain: chain-jail
---

# Emperor Capture (Chain Jail wrapper)

1. Read `chains/chain-jail/SKILL.md` → `absence-check.md` first.
2. Hunt / adapt / author per router.
3. **Authoring iron law:** before writing or substantively editing a skill,
   open `chains/chain-jail/authoring-checklist.md` and/or run
   `scripts/emperor author` (HARD-GATE: no skill body without a failing
   baseline). Jumping to prose → `scripts/emperor author --reject-untested`.
4. **Testing-skills companion:** before trial/register of a discipline skill,
   open `chains/chain-jail/testing-skills.md` and/or run
   `scripts/emperor skill-test` (HARD-GATE: combined pressure + watch baseline
   FAIL). Academic-only → `scripts/emperor skill-test --reject-academic-only`.
5. **Persuasion-principles companion:** when wording critical / discipline
   practices, open `chains/chain-jail/persuasion-principles.md` and/or run
   `scripts/emperor persuasion` (HARD-GATE: Authority + Commitment + boost).
   Hedge language → `scripts/emperor persuasion --reject-hedge`.
6. **Skill-discovery (SDO) companion:** when writing YAML `description`,
   open `chains/chain-jail/skill-discovery.md` and/or run
   `scripts/emperor sdo` (HARD-GATE: description = when to use, not workflow).
   Workflow summary → `scripts/emperor sdo --reject-workflow-summary`.
7. **Pin + consent + trial are mandatory** before the captured skill may fire:
   read `chains/chain-jail/pin-and-consent.md` then `trial-and-register.md`.
   HARD-GATE: `scripts/emperor pin-and-consent <task-dir>` (`pin_consent.py`
   `--reject-unpinned` / `--reject-no-skill-consent` / `--check-pin-consent`).
   Soft theater without exit code → refuse bind.
8. Captured skills live in `.emperor/captured-skills/` with provenance headers.
9. A captured skill that fails trial stays quarantined. Using it is a Vow of
   Evidence + Vow of Consent breach.
