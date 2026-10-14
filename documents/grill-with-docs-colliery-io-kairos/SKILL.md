---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also grows the docs — glossary terms and Kairos ADRs — as decisions crystallise.
disable-model-invocation: true
---

Invoke the `grilling` skill, applying the `domain-modeling` skill throughout the session.

## How the artefacts are written

This skill produces two kinds of text, and they follow opposite rules.

**Glossary terms are reference text**, so they follow Simplified Technical English: [the STE reference](../../../references/simplified-technical-english.md) (KAIROS-S-0009) is the source of truth. A definition is one sentence, present tense, active voice, and it uses the Technical Names in section 4 rather than a synonym. A glossary that calls the same concept two things is the defect the glossary exists to prevent.

**ADRs are explicitly out of STE's scope** — section 1.2 of that reference. An ADR records why a decision beat its alternatives, and a ~900-word controlled vocabulary cannot carry "this amends an absolute into a default" or "that argument did not survive a second issuer". Write ADRs in full English. Constraining them would flatten the reasoning they exist for, which is the whole point of the scope split.

If a sentence resists STE, the first question is whether it is procedural at all. If it is argument, it belongs in an ADR or an explanation page, and STE does not apply to it.
