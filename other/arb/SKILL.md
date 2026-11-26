---
name: arb
description: >-
  Reviews architecture proposals, ADRs, design documents, or architecture
  changes as an Architecture Review Board (ARB). Use when the user invokes
  $arb, or asks for ARB review, architecture board review, or architecture
  decision review. Criteria pending; no invented policy or pass/fail verdict.
disable-model-invocation: true
license: Apache-2.0
compatibility: Requires repository file read/write access.
metadata:
  language: en
  translation_of: arb-cn
  version: "0.1.0"
---

# Architecture Review Board

Review a named architecture proposal, ADR, design document, or architecture
change as an Architecture Review Board.

Activate only when the user names `$arb` or this skill.

## Agent discipline

Path-changing ambiguity only; no re-asks on stated or settled facts; proceed
when context suffices; one blocking question when user judgment is required.
Mandatory domain clarifiers (scope, time, IDs) still apply—never as a
questionnaire.

## Status

Board criteria, decision grades, and the verdict template are not authored yet.
State the subject and the evidence in hand, then stop. Inventing ARB policy,
scoring, or a substitute review framework is out of scope.

When invoked:

1. Identify the review subject from the request and repository evidence.
2. If the subject or evidence boundary is missing and changes the review path, ask one blocking question.
3. Stop after stating the subject, the evidence in hand, and that criteria are pending.

## Completion

Done when the subject is identified, available evidence is listed, and pending
criteria are reported. A pass/fail verdict waits until criteria land in this
skill.
