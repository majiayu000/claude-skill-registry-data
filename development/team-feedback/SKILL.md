---
name: team-feedback
description: >
  Format feedback for the Solum platform team — new rules (eligibility, insurance,
  copay), bug reports, and feature requests — using the WHEN/THEN/Example framework
  with Trading Partner IDs. Use this skill when the user wants to send feedback to
  the team or eng, report a platform bug, request a rule change, write a feature
  request, or convert raw clinic feedback into implementable rules. Triggers:
  "feedback for the team", "write this up for eng", "report this to the team",
  "new rule for the platform", "feature request", "convert this into a rule",
  "regla para la plataforma", or when the user pastes raw clinic feedback about
  eligibility, insurance, or copay behavior that needs to go to engineering.
---

# Team Feedback — WHEN/THEN/Example Framework

## Overview

Feedback to the platform team must be implementable without a single clarifying question: explicit condition + explicit behavior + evidence.

**Core principle: write the condition as the error you SEE, never the cause you assume.** "If MCO fails" forces eng to investigate what an MCO is; "el check automático da failed" does not.

## When to Use

- New platform rules (eligibility, insurance, copay behavior)
- Bug reports
- Feature requests
- NOT for: strategy discussions, prose emails, customer-facing messages

## The Output Contract

The message consists of, in order:
1. One template block per rule (below)
2. Optionally, ONE line starting with `Nota:` flagging a concern for eng to consider

Nothing else. No intro paragraphs, no root-cause analysis, no recommendations to "investigate first" — the rule as observed is the deliverable; a concern is one `Nota:` line.

```
WHEN (condición):
Insurance = [Trading Partner ID] ([nombre])
Y [el error/estado que se ve en la plataforma]

THEN (comportamiento):
[acción concreta]

Ejemplo (evidencia):
[clínica], paciente/check [ID]
```

## Rules

1. **Insurance = Trading Partner ID, always.** The TPID is the same across all clinics; display names are not. Name goes in parentheses for readability only. If the TPID is unknown, ask the user — never guess or substitute the name.
2. **Condition = observed error/state**, exactly as seen in the platform UI (e.g., "el check automático da failed", "la insurance tiene más de un copay").
3. **THEN = one concrete action** the platform should take (retry with X, choose Y, allow Z).
4. **Evidence required:** clinic + patient ID or check ID. If missing, ask for it.
5. **Feature requests state the behavior**, never a question or timeline ask: "Cuando los usuarios crean un Prior Auth, permitir agregar modifiers a los CPT codes."
6. **Language:** match the user's draft language (team usually writes Spanish); keep `WHEN`/`THEN` keywords as-is.
7. **Output as plain copy-paste-ready text** — no markdown formatting in the message itself.

## Example: Before → After

Raw feedback:
> "if MCO fails, run with straight Medicaid. Blossom: 10e9137f-2b13-4741-9372-528be4e7f6bc"

Formatted:
```
WHEN (condición):
Insurance = 68049 (Peach State Health Plan)
Y el check automático da failed

THEN (comportamiento):
Reintentar el check con Insurance = QBZJV

Ejemplo (evidencia):
Blossom, paciente 10e9137f-2b13-4741-9372-528be4e7f6bc
```

## Example: Non-Insurance Rule (Copays)

```
WHEN (condición):
La insurance tiene más de un copay

THEN (comportamiento):
Elegir el copay cuyo mensaje contenga "freestanding"

Ejemplo (evidencia):
POM MRI, check 5586d696-7063-4581-b379-c04b953edb7d
```

## Known Trading Partner IDs

| Payer | TPID | Notes |
|-------|------|-------|
| Peach State Health Plan (GA Medicaid MCO) | 68049 | On failed check → retry with QBZJV |
| Georgia straight Medicaid | QBZJV | Fallback payer for 68049 |

Add new mappings here as they come up.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Insurance referenced by name only | Always TPID; name in parentheses |
| Condition written as assumed cause ("if MCO fails") | Condition = visible error ("el check da failed") |
| Root-cause essay or pushback instead of the rule | Template block + at most one `Nota:` line |
| Feature request as a question or timeline ask | State the behavior: "Cuando [acción], [comportamiento]" |
| No evidence | Clinic + patient/check ID, always |
