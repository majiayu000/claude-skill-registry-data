---
name: review-01-project-init
description: Initialize a medical SCI review project. Use when setting up the review workbench, recording topic, disease/domain, review type, databases, target timeline, author role, and access conditions before literature searching.
---

# Review 01 Project Init

## Purpose

Create the minimum reliable project record before any search or writing starts.

## Required Inputs

- Disease, intervention, mechanism, population, or biomedical domain.
- Review type: narrative review, scoping review, systematic review, meta-analysis, or thesis review.
- Intended output: SCI manuscript, Chinese thesis, grant background, or presentation.
- Database access status: PubMed, Web of Science, Embase, Cochrane, Scopus, Zotero.

## Output

Create or update `01_question_scope/project_brief.md` with:

- Working title in Chinese and English.
- Research background in 3-5 restrained sentences.
- Candidate review type and rationale.
- Initial keywords and synonyms.
- Target journal or target tier if known.
- Decisions still requiring user confirmation.

## Completion Gate

Pass only when the project brief identifies the review type, topic boundary, and at least three searchable concepts.

## Stop Rules

Do not invent institutional access, journal targets, sample size, or preliminary findings.
