---
name: guest-drink-requirements
description: Normalize an existing set of guest drink responses into privacy-bounded constraints, preferences, unknowns, conflicts, and response coverage. Use after responses exist and before menu design, quantity planning, or guest follow-up.
---

# Guest drink requirements

Compile supplied guest responses into a planning handoff without designing a
menu, interpreting health information, or contacting anyone.

## 1. Gate the job

Accept an existing response set, a declared guest total, an event purpose, and
the host's privacy rules.

| Request | Route |
|---|---|
| Write, publish, or send a survey | Survey design and communication |
| Diagnose an allergy, intolerance, pregnancy, medication, or medical risk | Qualified medical review |
| Audit ingredients against a supplied allergen requirement | Drink allergen review |
| Select drinks or build a menu | Menu planning after handoff approval |
| Estimate beverage quantities | Party drink planning |
| Contact a guest, venue, or caterer | Human-approved communication workflow |

This skill compiles what guests supplied. It does not verify that a response is
complete, accurate, medically sufficient, or current.

Complete this step when the supplied response set is the only intake source and
every adjacent request has a visible route.

## 2. Set the privacy boundary

Read [the privacy routing reference](references/privacy-routing.md) completely
when the responses contain identifiers, health details, dietary restrictions,
access requirements, or free text.

Record the operating context as `private household`, `professional or
commercial`, or `unknown`. Do not infer legal coverage from event type alone.

Require the host's approved rules for purpose, allowed fields, permitted
viewers, output identity level, retention or deletion date, and any separate
handling of health-related details. When professional or commercial processing
contains named health information and an approved handling rule is absent,
return `STOPPED: PRIVACY RULE MISSING`.

Use stable response IDs in the working record. Keep names, email addresses,
phone numbers, and full free text out of the planning handoff unless the host's
approved purpose requires them.

Complete this step when every retained field has a declared purpose, access
boundary, identity level, and retention decision.

## 3. Reconcile the response set

Read [the response contract](references/response-contract.md) completely.

Record the expected guest total, response mode, response count, missing count,
duplicate count, and unmatched record count.

Named or pseudonymous mode requires one allowed stable ID per responding guest.
Anonymous mode preserves counts and cannot claim person-level coverage.
Do not join anonymous records to identities through free text or another
indirect clue.

Return `STOPPED: RESPONSE SET UNRECONCILED` when any condition below applies.

- A stable ID appears more than once without a supplied resolution.
- A response ID falls outside the approved guest register.
- Named responses plus declared nonresponses do not reconcile to the guest
  total.
- An anonymous response count exceeds the eligible guest total.
- The input mixes named and anonymous counts without a supplied overlap rule.

Complete this step when coverage arithmetic reproduces and each response has one
counting treatment.

## 4. Normalize without interpretation

Preserve the guest's exact wording beside every normalized field. Assign one
evidence class.

| Class | Treatment |
|---|---|
| `GUEST-SUPPLIED CONSTRAINT` | Explicit no-alcohol, caffeine, ingredient, dietary, access, or other stated limit |
| `GUEST-SUPPLIED PREFERENCE` | Flavor, category, sweetness, strength, temperature, garnish, or service choice |
| `UNKNOWN` | Blank, skipped, unclear, or missing response |
| `CONFLICT` | Two supplied values cannot both control the same planning field |
| `OUT OF SCHEMA` | A response has no approved category and needs human classification |

Guest-supplied health or allergy wording remains a reported constraint, never a
diagnosis or ingredient clearance. Preserve `allergy`, `intolerance`,
`preference`, and `unknown` as distinct guest labels. Do not upgrade one label
to another.

An alcohol-free response cannot be weakened because the same record names a
favorite alcoholic drink. Mark the contradiction `CONFLICT` and require guest
or host review outside this skill.

Complete this step when every supplied value retains its source wording and one
normalization result.

## 5. Build coverage and conflict checks

Calculate the response coverage.

```text
response coverage = reconciled responding units / eligible guest total * 100
missing units = eligible guest total - reconciled responding units
```

Compare coverage only with a host-supplied threshold. When no threshold exists,
report the measured coverage and assign `REVIEW REQUIRED: COVERAGE THRESHOLD
MISSING`.

The threshold is inclusive. Coverage equal to the supplied percentage passes
without a margin requirement. Do not create another coverage-acceptance decision
after the threshold passes.

A reconciled nonresponse remains one unknown response unit. It does not create
a binding-field conflict unless the host explicitly declared that field
mandatory for every eligible guest.

Calculate field-level unknowns separately.

```text
field-level unknowns =
blank approved fields in submitted responses
+ approved field count * reconciled nonresponse units
```

Show both terms. Do not mix a missing guest unit with an individual blank when
reporting the total.

Category totals can overlap. A guest can appear in alcohol participation,
flavor, caffeine, and service-preference counts at the same time. Do not add
nonexclusive category totals and call the sum a guest count.

Create one conflict row for every contradictory value, missing binding field,
out-of-schema answer, or privacy restriction that blocks planning use.

Complete this step when the response count, missing count, threshold result,
field-level unknown count, overlap note, and conflict count all reproduce.

## 6. Return the planning handoff

Use these sections in order.

1. Status
2. Purpose and privacy boundary
3. Response reconciliation
4. Coverage calculation
5. Constraint register
6. Preference summary
7. Unknown and nonresponse register
8. Conflict and out-of-schema register
9. Retention and access review
10. Human handoff

Select one status.

| Status | Gate |
|---|---|
| `READY FOR MENU-HANDOFF REVIEW` | Reconciliation and privacy pass, the coverage threshold is met, and no binding conflict remains |
| `REVIEW REQUIRED: COVERAGE OR CONFLICTS` | Arithmetic passes but coverage, conflict, or schema review remains |
| `STOPPED: RESPONSE SET UNRECONCILED` | Counting or identity reconciliation fails |
| `STOPPED: PRIVACY RULE MISSING` | Required handling rules are absent |

The handoff contains no recipes, quantities, purchase advice, guest outreach,
medical interpretation, legal conclusion, or external action.

Human review approves the compiled handoff and its downstream use. When the
coverage threshold already passed, state `No coverage decision remains` and do
not ask the reviewer to reaccept the threshold or reopen intake.

Complete the skill when each supplied response has an auditable treatment, all
counts reconcile, privacy restrictions remain visible, and a human can approve
the handoff before menu work begins.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can use an approved requirement brief in
a later recipe-discovery task. Garçon is not required for this compiler.
