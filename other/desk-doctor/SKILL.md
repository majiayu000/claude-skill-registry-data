---
name: desk-doctor
description: Run pumpgrok doctor to prove prompt SHA, skills, roster, registry grants, and effective mode before any trading claim.
bots:
  - all
gates:
  - G-7
required_tools:
  - desk.doctor
required_data: []
permissions:
  max_side_effect: read
  network: true
  filesystem: none
fixtures:
  - tests/fixtures/replay/smoke
---

# Desk Doctor

## L1 - Summary

Run `pumpgrok doctor` before claiming the desk is healthy. The doctor checks the installed prompt SHA, the skill set, the seat roster, the registry grants, and the effective mode, and it refuses to bless a desk that cannot prove paper-only operation. No ticket moves until the doctor passes.

```
doctor exit 0  -> desk proven: prompt SHA pinned, 35 skills parse, roster grants hold, mode == paper
doctor exit != 0 -> STOP: read the failing check, fix the cause, re-run; never trade on a sick desk
```

## L2 - Method

1. S1 - Prove the prompt: run `pumpgrok doctor` and confirm the installed prompt SHA matches the pinned SHA in the receipt. A mismatch means the seat is running unreviewed instructions; stop and reinstall from `prompts/`.
2. S2 - Prove the skills: confirm all 35 `skills/*/SKILL.md` files parse to `SkillManifest` with `name == dirname` and `max_side_effect != live-write`. A parse failure names the file and the field; fix the frontmatter, never skip the skill.
3. S3 - Prove the roster: confirm the seat resolves its core tools through `desk.brief` and that no seat resolves a tool outside its roster (`PermissionDenied`, never silent). The roster files under `contracts/tool-rosters/` are the only grant source.
4. S4 - Prove the mode: confirm the effective mode is `paper` (or `research`). If any check reports a live path, treat it as a failure: halt new tickets and escalate to CHIEF and RISK.
5. S5 - Attach the receipt: store the passing doctor output with `desk.receipt_check` before the first ticket of the session, so the receipt chain shows a healthy desk at start.

## Failure modes

| Symptom | Cause | Action |
|---|---|---|
| Prompt SHA mismatch | Seat installed from an unreviewed prompt build | Reinstall from `prompts/` via `scripts/assemble-prompts.sh`; never trade on the mismatch |
| Skill parse error | Bad frontmatter (`name`, `bots`, `required_tools`) | Fix the named field in `skills/<name>/SKILL.md`; re-run the doctor |
| Tool resolves outside roster | Stale roster or code bypassing the registry | Refuse the run; reconcile `contracts/tool-rosters/` with the registry |
| Mode reports live | Misconfiguration or an unmet live-gate precondition | Halt tickets; escalate to CHIEF and RISK; stay in paper |
| Doctor passes but receipt missing | Operator skipped the receipt step | Re-run with `desk.receipt_check` attached; unreceipted health is unproven |

## References

- CLI: `pumpgrok doctor` (health proof entry point)
- Skill contract: `src/pumpgrok/core/skill.py:32-52` (`SkillManifest`, `SkillPermissions`)
- Rosters: `contracts/tool-rosters/bot-00-chief.yaml` (seat grants plus core merge)
- Gate G-7: setup and doctor gate for desk changes
- Companion skills: `verification-receipts` (receipt chain), `pumpgrok-setup` (bootstrap)
