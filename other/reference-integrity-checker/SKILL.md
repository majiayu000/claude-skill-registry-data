---
name: reference-integrity-checker
description: Audit manuscript references, citation claims, DOI/PMID consistency, citation-to-claim alignment, and bibliography formatting risks without inventing missing sources. Use for reference check, citation audit, DOI check, PMID check, 参考文献核查, 引文真实性, bibliography cleanup, citation consistency, or when verifying whether cited papers support manuscript claims.
---

# Reference Integrity Checker

## Purpose

Audit references and citation claims for accuracy, consistency, and scientific support. This skill helps identify questionable citations, mismatched claims, missing metadata, duplicate references, and citation-format risks.

## Typical Inputs

- A reference list, BibTeX, RIS-like entries, or manuscript bibliography.
- Manuscript sentences with inline citations.
- DOI, PMID, PMCID, arXiv ID, trial ID, or database accession lists.
- Journal reference style requirements.

## Core Rules

- Do not fabricate references, titles, authors, journals, years, DOIs, PMIDs, PMCIDs, page numbers, or URLs.
- Do not silently "fix" a reference by inventing missing metadata.
- Do not claim a citation supports a manuscript statement unless the source content has been checked or the user provided enough evidence.
- Clearly separate metadata consistency checks from substantive evidence checks.
- Use live lookup only when browsing or external tools are available and appropriate; otherwise mark items as "needs verification."
- Recommend final human review before submission.

## Workflow

1. Identify the input type:
   - reference list
   - BibTeX/RIS
   - cited manuscript sentences
   - DOI/PMID list
2. Parse each reference into available metadata:
   - authors
   - year
   - title
   - journal
   - DOI/PMID/PMCID/URL
3. Check internal consistency:
   - duplicate references
   - missing DOI/PMID where expected
   - inconsistent author-year citations
   - malformed DOI or PMID patterns
   - citation keys that do not appear in the bibliography
   - bibliography entries that are never cited
4. Check claim alignment when manuscript sentences are provided:
   - whether the cited source type is appropriate for the claim
   - whether clinical, animal, in vitro, review, or database evidence is being overstated
   - whether a review is being used where a primary citation is needed
5. Produce a risk-ranked audit table and a correction checklist.

## Output Modes

Default output:

- A reference-integrity audit with severity labels and recommended actions.

For citation-to-claim checks:

- Return a table with claim, citation, evidence type, support status, and action.

For metadata cleanup:

- Return corrected formatting only for fields that are known from the provided input or verified lookup.
- Mark unresolved items as `needs verification`.

## Severity Labels

- Critical: likely fabricated, non-resolving, or claim unsupported by citation.
- Major: missing or inconsistent DOI/PMID, wrong article type for claim, or duplicate citation.
- Moderate: formatting or style issue that may affect submission quality.
- Minor: punctuation, capitalization, or style normalization.

## Quality Checklist

- No reference metadata was invented.
- DOI/PMID checks are labeled as verified or needs verification.
- Citation claims are not overstated.
- Reviews and primary studies are distinguished.
- The final bibliography requires human review before submission.
