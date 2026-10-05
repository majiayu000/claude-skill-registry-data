---
name: review-08-literature-classifier
description: Classify retrieved papers into review themes and screening categories. Use when grouping references by clinical question, mechanism, method, evidence level, or manuscript section.
---

# Review 08 Literature Classifier

## Purpose

Turn a reference list into a usable thematic map for screening, reading, and outline building.

## Required Inputs

- Deduplicated citation export.
- Locked question and inclusion/exclusion criteria.
- Benchmark review architecture if available.

## Output

Create `05_screening_prisma/literature_classification.csv` with:

- Citation key.
- Title.
- Study type.
- Population/model.
- Theme.
- Screening status.
- Full-text status.
- Notes and priority.

## Completion Gate

Pass only when every record has a screening status and at least one theme or exclusion reason.

## Stop Rules

Do not infer detailed methods or results from titles alone. Mark uncertain fields as `needs_abstract` or `needs_full_text`.
