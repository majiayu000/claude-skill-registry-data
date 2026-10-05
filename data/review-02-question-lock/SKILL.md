---
name: review-02-question-lock
description: Narrow and lock the scientific question for a medical review. Use when converting a broad topic into PICO/PECO, PCC, or mechanism-focused review questions and choosing a stable manuscript angle.
---

# Review 02 Question Lock

## Purpose

Turn a broad direction into a review question that can guide search, screening, evidence synthesis, and writing.

## Required Inputs

- Project brief from `$review-01-project-init`.
- User preference on review type if available.
- Known constraints: deadline, target journal tier, disease area, model system, or clinical population.

## Output

Create `01_question_scope/question_lock.md` with:

- One primary question.
- Up to three secondary questions.
- PICO/PECO/PCC table when applicable.
- Inclusion boundary and exclusion boundary.
- Three candidate titles: conservative, balanced, high-impact.
- Recommended final choice with rationale.

## Completion Gate

Pass only when the final question is narrow enough to generate database-specific search strings and broad enough to support a full review.

## Stop Rules

Do not claim novelty. Phrase gaps as "candidate gap requiring literature verification" until search evidence is available.
