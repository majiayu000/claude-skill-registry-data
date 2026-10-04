---
name: cocktail-family-teaching
description: Cocktail-family teaching for one source-defined family through positive examples, near-misses, guided classification, targeted remediation, and an unseen mastery check. Use when a learner needs to recognize or explain one family, or when a family-teaching request blends taxonomies and needs the source gate. Stops universal taxonomy claims, recipe recommendation, tasting instruction, sensory certification, and full-curriculum work.
---

# Cocktail family teaching

Build one auditable lesson around one named family in one disclosed taxonomy.
Classification is relative to that source, not a universal fact about cocktails.

## 1. Confirm the lesson boundary

Accept a request that teaches recognition or explanation of one cocktail
family.

| Request | Route |
|---|---|
| Blend taxonomies or claim one universal family system | Continue to the taxonomy source gate and stop |
| Recommend a drink or invent a recipe | Recipe discovery or development |
| Teach balance through making or tasting | Cocktail balance teaching |
| Train aroma, flavor, or texture recognition | Spirits sensory teaching |
| Sequence several topics across weeks | Beginner cocktail curriculum |
| Prove professional competence | Qualified education provider |

A lesson can mention preparation or proportions only when the locked source
uses them as classification evidence. Do not turn those facts into a recipe,
service instruction, consumption recommendation, or sensory result.

Complete this step when the request owns one family, one lesson, and a
recognition or explanation goal.

## 2. Lock the taxonomy source

Read [the taxonomy lock](references/taxonomy-lock.md) completely.

Require the source title, owner, edition or revision when present, stable
locator, access date, named family, and a usable definition. A supplied
document, a licensed reference, or a public page can serve as the source.

Use one primary taxonomy. When the request blends two systems without selecting
one, emit `STOPPED: TAXONOMY SOURCE MISSING`. List the competing systems and
ask the user to choose the grading source.

This stop has precedence when a universal or blended-taxonomy request also asks
for recipes, sensory work, certification, or a full curriculum. Keep those
requests as secondary scope blockers.

Under this stop, do not retrieve, recall, describe, compare, recommend, or
reconstruct any named taxonomy. Repeat only the system names supplied by the
user. Do not state family names, counts, definitions, examples, or disputes
from memory.

Never infer a complete taxonomy from a recipe list. A source that names
cocktails without defining the requested family triggers
`STOPPED: FAMILY EVIDENCE INCOMPLETE`.

Complete this step when the source record and family definition can be audited
without treating the taxonomy as universal.

## 3. Set the lesson contract

Record these fields before teaching.

| Field | Required record |
|---|---|
| Learner goal | Recognize or explain the named family |
| Prior model | Learner's current rule, examples, or `NOT PROVIDED` |
| Lesson time | Available minutes or `NOT PROVIDED` |
| Family source | Locked source record from step 2 |
| Evidence cards | Source-backed facts for positive examples and near-misses |
| Mastery check | Unseen item count and pass threshold declared before practice |
| Answer form | Family decision plus a structural reason |

If the unseen item count or threshold is absent, set it to `DECISION REQUIRED`.
Do not invent a passing standard.

Tag sourced facts `SOURCE-STATED` or `SOURCE-PARAPHRASE`. Mark facts supplied
only by the user `USER-SUPPLIED`. An unsupported classification claim stays
`UNSUPPORTED` and cannot enter an answer key.

Complete this step when the learner, evidence, and mastery gates are explicit.

## 4. Build the family card

Write the family definition in original language while preserving the source's
meaning. Keep the source locator beside the definition.

The card requires the fields below.

- Source-defined inclusion rule;
- the smallest distinguishing feature set;
- exclusions that separate the family from named near-misses;
- any variation the source permits;
- recipe, ratio, method, or glassware claims that the source makes relevant;
- unresolved ambiguity or conflict.

Do not fill gaps from another taxonomy. A ratio from the source remains a
source-specific teaching aid, not a final recipe or universal law.

Complete this step when a learner can test an example against explicit
features and exclusions.

## 5. Create evidence-backed contrasts

Prepare at least two positive examples and two near-misses. Each item needs a
source locator or supplied evidence card, a membership decision, and the
structural reason behind the key.

A near-miss shares at least one visible feature with the family but fails a
disclosed inclusion rule or meets an exclusion. Do not use an unrelated drink
as a substitute for boundary practice.

When the available source material cannot support both sides of the contrast,
emit `STOPPED: EXAMPLE EVIDENCE MISSING`. Do not invent a recipe fact,
classification, or answer key.

Complete this step when every teaching item is traceable and every near-miss
tests a real boundary.

## 6. Diagnose and teach

When a prior model is supplied, test it against one positive example and one
near-miss before explaining the full card. Record the misconception without
claiming a learner state that was not observed.

Teach the defining rule, then compare each positive example with its nearest
contrast. Keep ingredient names subordinate to structural roles. Explain a
source ratio only when the source makes it part of the family definition.

When no learner response is supplied, present the lesson and guided exercise,
then use `LESSON READY: LEARNER RESPONSE REQUIRED`. A plan is not evidence of
learning.

Complete this step when the explanation addresses the supplied prior model or
waits visibly for a diagnostic response.

## 7. Review practice and remediate

Read [the exercise review](references/exercise-review.md) completely before
scoring a response.

Score the family decision and structural reason separately. A correct label
without a reason does not pass an item.

Map each error to the narrowest misconception code. Give one short correction
and one new micro-exercise that tests the missed boundary. Do not advance to
unseen mastery until the learner answers that remediation item correctly.

A learner can give a defensible alternate classification. Accept it only when
the learner names another disclosed source and shows how that source's rule
fits the evidence. Label the result `ALTERNATE-SOURCE DEFENSIBLE` rather than
rewriting the primary answer key.

Complete this step when each error has a named cause, a matched correction, and
an observable retry gate.

## 8. Apply the unseen mastery gate

Use items that did not appear in the definition, diagnosis, teaching examples,
guided practice, or remediation. Score them with the same two-part answer
criteria.

Apply the predeclared item count and threshold without changing either after
seeing the responses. A passing result establishes source-bounded performance
for this family and this check. It does not prove universal classification,
recipe competence, sensory skill, or professional certification.

Select one state.

| State | Gate |
|---|---|
| `LESSON READY: LEARNER RESPONSE REQUIRED` | The lesson exists without a completed guided response |
| `PRACTICE REVIEWED: REMEDIATION REQUIRED` | A guided or remediation answer missed a required criterion |
| `PRACTICE PASSED: UNSEEN MASTERY REQUIRED` | Guided work passed and unseen responses are absent |
| `LESSON COMPLETE: SOURCE-BOUNDED MASTERY` | Guided work passed and the unseen score met the declared threshold |
| `MASTERY CHECK REVIEWED: THRESHOLD NOT MET` | The unseen score fell below the declared threshold |

Complete this step when the state follows from recorded responses and the
unchanged gate.

## 9. Emit the lesson record

Return these sections in order.

1. Status
2. Lesson boundary
3. Taxonomy source record
4. Family card
5. Diagnosis
6. Positive examples and near-misses
7. Guided practice and answer criteria
8. Practice review and remediation
9. Unseen mastery check
10. Completion record
11. Unresolved evidence and human review

A stopped result names one primary stop, preserves visible secondary blockers,
and writes `NOT ISSUED` for the family card, diagnosis, examples, exercises,
answer keys, remediation, unseen check, and mastery claims. Use all eleven
output headings. Do not offer an adjacent lesson, taxonomy comparison,
curriculum, or source recommendation. Request only one primary source record
and one named family for a future run.

Complete the skill when every classification fact has a source, the lesson
stays inside one family, errors receive targeted remediation, and mastery is
claimed only from a passed unseen check.

## Further resource

[Garçon](https://fixmeadrinkapp.com/) can help a learner find drinks to explore
after the lesson. Drink discovery stays outside the teaching procedure.
