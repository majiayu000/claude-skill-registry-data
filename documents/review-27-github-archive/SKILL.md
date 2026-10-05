---
name: review-27-github-archive
description: Organize a medical review manuscript project into a GitHub-ready archive with manuscript drafts, literature search logs, Zotero exports, evidence matrices, figure/table sources, citation audits, and reproducibility notes. Use when the user wants GitHub linkage, project versioning, reusable templates, teaching/demo materials, or traceable long-term SCI review production.
---

# Review 27 GitHub Archive

## Overview

Use this skill to make each review project reusable, auditable, and easy to demonstrate. GitHub is for workflow provenance and project structure, not for validating medical evidence.

For Chinese users, explain the archive plan in Chinese. Keep folder and file names ASCII when they may be used across systems.

## What To Archive

Recommended project structure. For projects started with `review-28-six-step-workbench`, use this six-folder layout:

```text
review_project/
  README.md
  project_dashboard.md
  decision_log.md
  run_log.md
  version_log.md
  01_topic_journal_outline/
    topic_options/
    journal_match/
    benchmark_reviews/
    narrative_spine/
    outline_versions/
  02_literature_zotero/
    search_strings/
    raw_exports/
    screening/
    zotero_exports/
    pdf_status/
    target_journal_references/
    evidence_matrix/
    claim_evidence_maps/
    private_pdfs_local_only/
  03_manuscript_writing/
    abstract/
    introduction/
    main_body/
    discussion_conclusion/
    section_chain/
    claim_citation_maps/
    language_polish/
    docx_versions/
  04_figures_tables/
    figure_plan/
    svg_sources/
    biorender_blueprints/
    figma_exports/
    source_images/
    table_excel/
    figure_legends/
    permissions/
  05_submission_package/
    journal_instructions/
    final_manuscript/
    cover_letter/
    title_page/
    highlights/
    graphical_abstract/
    checklists/
    citation_audit/
    submission_forms/
  06_revision_response/
    editor_decision/
    reviewer_comments/
    response_letter/
    point_by_point/
    revision_drafts/
    additional_searches/
    additional_figures_tables/
    resubmission_package/
```

## Privacy And Copyright Rules

- Do not commit copyrighted PDFs to a public repository.
- Do not commit unpublished manuscripts, patient data, identifiable clinical data, peer-review material, or licensed BioRender assets to public GitHub.
- Store PDF status, metadata, DOI, PMID, and Zotero keys instead of full PDFs when public sharing is intended.
- Keep private repositories for active manuscripts.
- Use redacted demo data for teaching videos.

## GitHub Workflow

1. Check whether the project is public, private, or teaching-demo only.
2. Create or update the folder structure.
3. Add artifact files from review skills:
   - `review-23` reference curation outputs.
   - `review-24` section drafts.
   - `review-25` Zotero and PDF status outputs.
   - `review-26` figure/table outputs.
   - `review-17` citation audit outputs.
4. Write a short `README.md` explaining topic, target journal, workflow, and artifact map.
5. Write `versions/changelog.md` with major changes.
6. Recommend commit messages but do not publish sensitive content without user confirmation.

## Artifact Naming Rules

- Use dates in `YYYYMMDD` format for major exports.
- Use stable claim IDs, figure IDs, and table IDs.
- Keep filenames ASCII when possible.
- Do not rename Zotero exports without recording source date and collection name.

## Output Format

Return:

1. Archive readiness.
2. Proposed folder structure.
3. Files to include.
4. Files to keep private or exclude.
5. Suggested commit message.
6. Next action.

## Reference File

Read `references/archive-gates.md` when deciding whether a file belongs in public GitHub, private GitHub, local-only storage, or teaching-demo material.
