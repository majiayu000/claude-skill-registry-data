---
name: service-journeys
description: >-
  Design and model one official matter (sprawa) end to end: the docs/services/<matter>.md template, today's
  real-world steps vs ours, once-only data reuse, confirmations, edge cases, the state machine in
  packages/core and scenario scripts in packages/content, and how to count "fewer steps" for the pitch. Use
  for "design the meldunek flow", "add a matter", "how many steps", "journey", "sprawa".
---

# Service journeys

A matter done end to end with fewer steps is the most convincing thing a jury can click through. Design owner:
the `service-designer` agent. Model and data owner: the `domain-engineer` agent. Screens: the `ui-engineer`
agent. Copy rules: the `plain-polish` skill.

## Candidate matters

| Matter                                  | Persona fit        | Why it demos well                                                  |
| --------------------------------------- | ------------------ | ------------------------------------------------------------------ |
| Meldunek (registration of residence)    | young adult moving | today: office visit or ePUAP form; we: 3 taps                      |
| Lost wallet → zastrzeż / zablokuj dowód | anyone             | urgent, emotional, reference does it: beat it on speed and clarity |
| New ID card when it expires             | senior             | reminder → application → appointment for fingerprints              |
| Vehicle sale / registration (zbycie)    | car owner          | two parties, deadlines, many documents today                       |
| 800 plus                                | parent             | eligibility in one screen, reuses family data                      |
| OC / przegląd reminders                 | car owner          | proactive: tile → one tap to the right action                      |
| Zastrzeżenie PESEL                      | anyone             | privacy story, instant, reversible                                 |

Pick 2–3 and make them excellent. Breadth comes after depth.

## Design doc template: `docs/services/<matter>.md`

```markdown
---
matter: <slug>
status: draft | designed | built
sources: [<gov.pl URL> (accessed YYYY-MM-DD), ...]
---

# <Matter in plain words>

## Trigger — what brings the user here (reminder, life event, assistant question)

## Persona — who, situation, constraints (senior? on the phone in a hurry?)

## Today — numbered real-world steps: where, what documents, how long, cost (with sources)

## Reference — how the reference prototype does it (steps / taps / messages), if it does

## Ours — numbered steps, each one screen or one assistant turn

## Data reused — what we already know (once-only) and from which simulated registry

## User confirms — exactly what the ConfirmCard shows

## Outputs — what the user gets (status, document, appointment, reminder set)

## Edge cases — not eligible, missing data, a deadline passed, someone else must act, offline

## Not in the prototype — what a real system would need (signature, payment, identity check)

## Step count — today N / reference N / ours N (method below)
```

Every fact about law, fees or deadlines carries a source and an access date. If there's no source, mark it
_assumption_ and keep it out of the UI.

## Modelling in `packages/core`

- One module per matter: `packages/core/src/matters/<matter>/` with `machine.ts` (states, events, guards),
  `types.ts` and `machine.test.ts`.
- A plain TypeScript state machine (a reducer with a `state` enum) unless the architect picks a library. No
  React and no browser APIs. Time is injected (`now: () => Date`) so tests are deterministic.
- Simulated registries are ports (`RegistryPort`) with in-memory adapters fed from `packages/content`. The UI
  and the assistant call the same machine, so chat and taps never disagree.
- Every action-taking transition requires a `CONFIRMED` event. The machine refuses to act without it.

## Scenario scripts in `packages/content`

- `packages/content/src/scenarios/<matter>.ts`: the scripted assistant path (turns, chips, cards) that drives
  the machine. Text follows the `plain-polish` skill. The data is fictional (the `prototype-guardrails`
  skill).
- Personas in `packages/content/src/personas/<id>.ts` hold the documents, vehicles, reminders and suggestion
  chips that open each matter.

## Counting "fewer steps" (a number the pitch can use)

Count the same unit across all three versions:

- **Steps** = user decisions or inputs (a tap that chooses, a field filled, a message sent). Scrolling and
  reading don't count. A confirmation counts as one.
- **Today:** from the sources (forms, visits, documents to bring). Count each visit separately and note the
  time.
- **Reference:** walk the reference's scripted flow at mobywatel.ai/aplikacja and count. Record the date.
- **Ours:** count from the Playwright flow, which doubles as proof.

Write the numbers in the design doc. The `product-manager` agent turns them into a single claim ("Meldunek: 3
kroki zamiast wizyty w urzędzie"). Claims without a measured flow don't go in the pitch.

## Done means

Design doc `status: built`, machine tests green, scenario plays offline, Playwright flow passes with axe, step
count recorded, and copy reviewed by the `service-designer` agent.
