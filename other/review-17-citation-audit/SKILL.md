---
name: review-17-citation-audit
description: Verify citations, reference formatting, DOI/PMID accuracy, source quality, publication year, and claim-citation alignment. Use before submission, major revision, or when adding/replacing references in a medical review manuscript, especially when each reference must be recent, PubMed-verifiable, DOI/PMID-complete, and suitable for a high-quality SCI review.
---

# Review 17 Citation Audit

## Purpose

Prevent fabricated, mismatched, outdated, or unsupported citations.

References are a priority evidence layer, not decorative support. Treat every added, replaced, or retained citation as a claim-level evidence decision.

## Required Inputs

- Full manuscript draft.
- Reference library export.
- Evidence matrix.
- Target citation style.
- User's journal/source exclusions, if any.

## Output

Create `13_citation_audit/citation_audit_report.md` and `13_citation_audit/claim_citation_check.csv` with:

- Missing citation list.
- DOI/PMID checks.
- Citation-to-claim alignment.
- Reference style issues.
- Papers requiring replacement or stronger support.
- Source quality and publication-year risks.

## Strict Reference Rules

- Do not invent references, DOI, PMID, author names, journal names, volume, issue, pages, article numbers, or publication years.
- Prefer references from 2021-2026. If the user explicitly allows a 2020 start year, keep 2020 papers only when they are high-impact foundational evidence, guidelines, consensus statements, or major reviews.
- Require DOI and PMID for core biomedical references unless the user explicitly approves an exception. Flag any missing DOI or PMID for replacement.
- Verify existence through PubMed and publisher/DOI sources first. Use Web of Science or Google Scholar only as additional support or fallback discovery, not as the sole final proof when PubMed/publisher data are available.
- Prefer high-impact, field-relevant journals, JCR Q1-Q2, CAS high-partition sources, guidelines, consensus statements, and major original studies or authoritative reviews.
- Avoid MDPI, Frontiers, Scientific Reports, Medicine, and similar user-excluded or quality-risk sources for this user's SCI review work unless no credible alternative exists and the user explicitly accepts the risk.
- Check whether each reference supports the exact claim, not merely the broad topic.
- Do not use correlation evidence to support causal wording.
- Do not use basic/mechanistic evidence as direct support for clinical efficacy unless the sentence is explicitly framed as mechanistic or hypothesis-generating.
- For paragraph-level citation insertion, ensure every substantive paragraph has at least one appropriate citation and key factual claims have direct support.

## Completion Gate

Pass only when every key claim has an appropriate citation; no reference is knowingly fabricated, unverifiable, mismatched, outdated without justification, or inconsistent with the user's source-quality rules; and all core references have DOI/PMID or documented user-approved exceptions.

## Stop Rules

Do not invent citations to fill gaps. Mark gaps as citation needed.
If no suitable reference can be found under the required year, DOI/PMID, and journal-quality constraints, report the gap and propose a replacement search strategy instead of lowering the evidence standard silently.
