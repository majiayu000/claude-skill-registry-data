---
name: review-20-reviewer-response
description: Draft structured reviewer responses and revision plans for medical review manuscripts. Use after peer-review comments, editorial decisions, or pre-submission internal review.
---

# Review 20 Reviewer Response

## Purpose

Convert reviewer comments into a polite, specific, evidence-supported response and manuscript revision plan.

## Required Inputs

- Reviewer/editor comments.
- Current manuscript version.
- Files changed or planned changes.
- Evidence matrix and citation audit if claims are challenged.

## Output

Create files under `16_revision_response/`:

- `comment_response_table.md`.
- `revision_plan.md`.
- `tracked_change_summary.md`.
- `additional_evidence_needed.md`.

## Completion Gate

Pass only when every comment has a response, action, manuscript location, and evidence support if needed.

## Stop Rules

Do not promise experiments, analyses, or data that the user has not provided or approved.
