---
name: cx-criterion-library
description: Use to build and maintain a reusable bank of QA criteria as observable decision rules shared across scorecards. Trigger for "criterion library", "standardise our QA criteria", "write better rubric items", "was professional is too vague", versioning criteria across teams, or turning adjectives into pass/fail decision rules with examples.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Criterion library

Individual scorecards drift into duplicate, vague criteria because each team writes
their own rubric in a workshop. "Was professional", "showed empathy", and "good
tone" multiply — and graders cannot agree on any of them.

A **criterion library** is a versioned bank of observable decision rules, with
examples, that scorecards **compose from** rather than reinvent. It is not a template
pack of generic virtues.

## Diagnose library need

| Symptom | Fix the library addresses |
| --- | --- |
| Same criterion worded three ways across teams | Canonical definition + version |
| Calibration fails on "tone" criteria | Replace adjectives with decision rules |
| New scorecard takes months to draft | Reuse proven criteria by intent |
| AI grader hallucinates on vague items | Observable evidence requirements |
| Criteria updated in one team, not others | Central changelog and propagation |

## Step 1: Define what belongs in the library

**In:**

- Criteria reused across 2+ queues, channels, or scorecards.
- Criteria tied to outcome evidence (resolution, compliance, repeat contact drivers).
- Auto-fail rules with regulatory or policy backing.

**Out:**

- Queue-specific procedural checks ("used macro X") — keep local unless truly shared.
- Weighting and thresholds — those live on the scorecard, not the criterion.
- One-off coaching prompts.

Library entries are **ingredients**. Scorecards are **recipes**.

## Step 2: Write each criterion as a decision rule

Every library entry follows the same schema:

```
Id:           CR-RES-001
Name:         Resolution accuracy
Category:     Resolution
Version:      1.2.0
Verdict:      Met | Not met          (prefer binary)
Evidence:     Quote the message stating the resolution.
Decision rule:
  Met     — Stated resolution is correct and complete for the customer's
            actual problem; no foreseeable follow-up required on same intent.
  Not met — Incorrect, incomplete, or addresses a different problem than raised.
Pass example: [anonymised quote + brief context]
Fail example: [anonymised quote + brief context]
Outcome link: Repeat contact on same intent within 7 days
Notes:        Partial resolution → see CR-RES-002 (Follow-up anticipation)
```

**Four tests** (same as scorecard design): observable, controllable, decidable,
discriminating. Fail any test → do not publish to library.

### Rewrite vague criteria

| Vague (cut or rewrite) | Observable decision rule |
| --- | --- |
| Was professional | No profanity, slurs, or dismissive language directed at customer |
| Showed empathy | Acknowledged stated impact before next procedural step |
| Good tone | No sarcasm, caps-lock emphasis, or blame-shifting phrasing |
| Went above and beyond | Identified unstated need and resolved without customer re-asking |

Adjectives describe summaries. Decision rules describe **what a grader marks up in
the transcript**.

## Step 3: Version and change control

Semantic versioning per criterion:

- **Major** — pass/fail boundary moved; not comparable — scorecards must pin new major.
- **Minor** — clarified examples or evidence; same boundary.
- **Patch** — typo, anonymisation refresh.

Each scorecard records **criterion id + version pinned**. Evaluations store the pin —
not "whatever the library said that day".

Changelog entry required:

```
CR-RES-001 v1.1.0 → v1.2.0 (major)
Reason: Include partial resolution as Not met (was Met with note)
Effective: 2026-09-01
Scorecards affected: SC-UK-VOICE-3, SC-UK-CHAT-2
Action: Re-calibrate; dual-run recommended
```

## Step 4: Organise for discovery

Tag entries so scorecard authors find them:

| Dimension | Examples |
| --- | --- |
| Category | Resolution, Compliance, Security, Communication, Process |
| Channel applicability | Voice, chat, email, async — note transcript limitations |
| Regulatory | FCA, HIPAA, PCI — link to policy ref, not full policy text |
| Severity potential | Scored vs auto-fail candidate |
| Maturity | Draft, calibrated, deprecated |

**Deprecated** criteria stay readable for historical evaluations but cannot be added
to new scorecards.

## Step 5: Governance — who owns the library

Minimum roles:

- **Curator** — accepts submissions, enforces schema, publishes versions.
- **Adjudication panel** — resolves disputed examples (QA + ops + compliance as
  needed).
- **Consumers** — scorecard owners pin versions; propose new criteria from production
  evidence.

Submission workflow:

1. Propose with **real conversation evidence** — not workshop brainstorm.
2. Pilot on gold set — measure agreement before library publish.
3. Publish or return with rewrite notes.
4. Notify scorecard owners if their pinned version is superseded by major bump.

No criterion enters the library without **at least one pass and one fail example**
from real (anonymised) conversations.

## Step 6: Compose scorecards from the library

Scorecard spec references library ids:

```
Scorecard: UK Voice Coaching v4
Criteria:
  CR-RES-001 @ 1.2.0  weight 3
  CR-COM-003 @ 2.0.0  weight 2
  CR-REG-007 @ 1.0.0  auto-fail
Local only:
  L-UK-001 Macro compliance (queue-specific)
```

Local criteria must still follow the schema. If a local criterion appears in 2+
scorecards, promote it to the library.

## Step 7: Keep AI and human graders aligned

Library entries are the **single source** for:

- Human rubric text in QA UI.
- AI grader prompt blocks (criterion + decision rule + examples).

When library version bumps, AI prompt config must bump together. Divergence creates
systematic human/AI disagreement that looks like model failure but is a spec fork.

## Step 8: Retire criteria honestly

Deprecate when:

- Never fails in production and carries no compliance weight — ceremony.
- Outcome link disproven — criterion does not predict what it claimed.
- Absorbed into another criterion (document merge mapping).
- Policy removed — regulatory criterion no longer applies.

Retired ≠ deleted. Historical evaluations reference old ids.

## Present results to the user

1. **Library scope** — what belongs central vs local, with current duplication
   diagnosis if auditing existing rubrics.
2. **Entry schema** — template with required fields and example filled entry.
3. **Rewrite table** — vague criteria found → proposed decision rules (or cuts).
4. **Versioning and governance model** — roles, submission workflow, major/minor
   rules.
5. **Initial catalogue** — prioritised criteria to centralise first (highest reuse or
   worst agreement).
6. **Scorecard composition example** — how pins and weights reference library ids.
7. **Propagation plan** — how scorecard and AI grader configs stay synced on change.
