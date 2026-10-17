---
name: electrical-safety
description: Electrical safety discipline — LOTO, test-before-touch, arc-flash awareness, PPE per site procedures and standards.
version: 1
triggers: electrical safety, loto, lockout tagout, arc flash, test before touch, ppe
category: Electrical & energy
blurb: Electrical safety discipline — lockout, test-before-touch, arc-flash awareness and the right PPE.
archetype: knowledge
example: Write the safety steps before we open this MCC bucket.
---

# Electrical Safety (LOTO · Arc Flash)

This skill structures the discipline and the paper trail. It supports — never replaces — site procedures, CSA Z462 / NFPA 70E-style standards, OEM manuals, and qualified judgment.

## When to use
- Any work near exposed energized parts, or that could release stored energy.
- Planning isolation, verification, or restoration (LOTO).
- Reviewing permits/JHAs for electrical work.

## Method
1. **Site rules first**: confirm current procedures, PPE requirements, and the permit path before planning; when anything conflicts — stop and resolve.
2. **Identify ALL energy**: electrical + mechanical + stored — capacitors, **drive DC buses (wait OEM discharge time)**, UPS, batteries, springs, gravity, pressure, thermal.
3. **LOTO**: lock + tag each isolation point per procedure; one lock per worker; no shared locks; locks stay until the owner removes them.
4. **Verify zero-energy (test-before-touch)**: rated, calibrated instrument (correct CAT rating); test on a known live source first, test the target, re-test the instrument; prove the absence you claim.
5. **Arc-flash awareness**: know the study/labels for the equipment; respect approach boundaries; PPE per site standard for the task; energized work only under the permitted, justified process — rare by design.
6. **Restoration**: walk-down before re-energizing (tools, personnel, barriers clear); controlled sequence, documented; re-energization is its own checklist.
7. **Records**: permit, JHA, isolation list, verification results, deviations — recorded (`electrical-test-records`).

## Quality gates
- [ ] Permit/JHA in place; isolations listed and locked.
- [ ] Zero-energy verification documented (instrument + method).
- [ ] PPE/barriers per site standard for the task.
- [ ] Restoration walk-down + sequence documented.

## Red lines
- Never bypass, share, or shortcut LOTO; no energized work without the authorized process; when unsure — stop, isolate, ask.

## Related
`power-distribution-equipment` · `electrical-machinery-engineering` · `electrical-test-records`.
