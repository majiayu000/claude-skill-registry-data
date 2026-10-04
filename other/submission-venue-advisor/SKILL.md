---
name: submission-venue-advisor
version: 1.1.0
description: Use when a paper draft is complete or when planning preprint publication, to select a venue and draft field-level deposit metadata for the publication form
---

# Submission Venue Advisor Skill

## Purpose
When publishing or submitting a completed paper, recommend the optimal preprint server or open-access repository based on research field, manuscript language, and publication goals (establishing priority, gathering pre-review feedback, outreach). After venue selection and quality gates, draft **per-field** metadata that the author can copy into a typical paper-deposit form.

The field inventory follows [Zenodo Describe records](https://help.zenodo.org/docs/deposit/describe-records/) (CERN-operated general repository: all fields, multilingual metadata, automatic DOI). Write proposals in generic names so they map to other repositories (OSF, institutional repositories). If a venue uses different labels, keep the generic name and put the local label in parentheses.

The agent does not press Publish. It drafts values and waits for author confirmation.

## Trigger Conditions
- When a first draft is complete and publication venue is being considered
- When considering preprint publication (priority claim, pre-review feedback)
- When registering a thesis or working paper in a repository
- When the author wants field-by-field values for a deposit form (Zenodo or similar)

## Venue Classification Matrix

### General-Purpose (All Fields)

| Server | Features | Languages | Cost |
|---|---|---|---|
| **Zenodo** | Operated by CERN. All fields and file formats. Automatic DOI. GitHub integration | Multilingual | Free |
| **OSF (Open Science Framework)** | Project management built in. Strong data/code integration | Multilingual | Free |
| **Research Square** | Interdisciplinary. Optional preprint peer review | Primarily English | Free |

### Field-Specific Preprint Servers

| Field | Recommended Server | Notes |
|---|---|---|
| Economics, Social Sciences, Law | **SSRN** (Elsevier) | Strong working-paper culture; well suited to policy research |
| Physics, Math, CS, Statistics, Econometrics | **arXiv** | Oldest and most influential; includes an econ category |
| Life Sciences | **bioRxiv** | Standard for biology |
| Medicine & Health Sciences | **medRxiv** | Clinical focus; disclaimer required |
| Psychology | **PsyArXiv** | OSF-based |
| Social Sciences (General) | **SocArXiv** | OSF-based; sociology, political science |
| Chemistry | **ChemRxiv** | ACS-affiliated |
| Earth & Environmental Sciences | **EarthArXiv** | Geoscience focus |
| Humanities | **Humanities Commons (CORE)** | MLA-affiliated; accepts short-form works |

### Japanese-Language / Domestic Venues

| Venue | Use Case |
|---|---|
| **J-STAGE** | Electronic platform for Japanese society journals (via society submission) |
| **Zenodo** | Accepts Japanese-language papers; multilingual metadata |
| Institutional repositories | University repositories (e.g., JAIRO Cloud) |

## Selection Criteria

Narrow candidates in this order:

1. **Field convention**: Which server does your field actually read? (Where your reviewers and colleagues look)
2. **Language compatibility**: Non-English manuscripts are safest on Zenodo / OSF / Humanities Commons. SSRN, medRxiv, etc. assume English
3. **DOI assignment**: All major servers above issue DOIs (guarantees citability)
4. **License selection**: CC-BY 4.0 is the standard recommendation; use CC-BY-ND etc. if derivatives should be restricted
5. **Compatibility with future journal submission**: Check the target journal's preprint policy via **SHERPA/RoMEO** (most major publishers permit preprints)

## Pre-Submission Checklist (Quality Gates)

Complete all of the following before submitting:

- [ ] Passed the [`claim-evidence-gate`](../claim-evidence-gate/SKILL.md) quality gate
- [ ] Verified 1-to-1 citation correspondence via [`citation-traceability-audit`](../citation-traceability-audit/SKILL.md)
- [ ] References list fully matches in-text citations
- [ ] Generated the final PDF with `scripts/convert_markdown_to_pdf.py` and visually inspected layout
- [ ] Abstract, keywords, and author information (ORCID recommended) are up to date
- [ ] License (e.g., CC-BY) is stated explicitly
- [ ] Conflict-of-interest and research-ethics statements included (IRB approval number where applicable)

## Multi-Server Deployment (e.g., Zenodo + SSRN)

Registering the same paper on multiple servers is generally acceptable, with these caveats:

- **Version control**: Keep the same version (revision date/number) on every server; update all when revising
- **Cross-linking**: Add the other server's DOI/URL to the related-identifiers field so the records are linked as the same work
- **Distinguish from duplicate submission**: Multiple preprint registrations are fine, but simultaneous submission to peer-reviewed journals violates publication ethics

## Deposit Metadata Draft (Per Field)

Once the venue is chosen (or the author asks to draft form values), propose **one field at a time**. Do not stop at a summary paragraph.

### Procedure

1. Lock the venue (if unset, run the first half of this skill and wait for author confirmation).
2. Read SoT. Do not fill fields by guessing from the prose.
   - `docs/design/paper-outline.md` or `docs/<paper-id>/design/sot/paper-outline.md` (title, subtitle, abstract, keywords, author, version)
   - `docs/design/research-plan.md` or equivalent (audience, venue type, out-of-scope)
   - `docs/literature/literature-matrix.md` (prior DOIs, related works)
   - Final PDF / HTML under `docs/manuscript/`
   - Existing `submission-plan.md` and author settings (ORCID, etc.) if present
3. Fill every row in the inventory: proposed value, source path, status.
4. Write `docs/design/deposit-metadata.md` (or `docs/<paper-id>/design/deposit-metadata.md` in multi-paper repos).
5. Ask the author only about `needs-author` rows. Leave `blank` rows blank.
6. Do not transcribe into the live form until the author approves.

### Status labels

| Label | Meaning |
|---|---|
| `locked` | Copied verbatim from SoT |
| `proposed` | Drafted from SoT (abstract formatting, keyword order) |
| `needs-author` | Author decision required (ORCID, community, funding, publication-date interpretation) |
| `blank` | Not applicable. Do not invent |

### Forbidden

- Do not invent ORCID, affiliation, funding, or community names. If absent from SoT, mark `needs-author` or `blank`.
- Do not write an unissued DOI. Use a reserved DOI only if the author reserved it in the form.
- Do not list a prior paper as merely “related”. Always add a relation type (cites / version of / supplement, etc.).
- Do not perform Publish on the author's behalf.

### Field inventory

Source: Zenodo Describe records and Create new upload ([describe-records](https://help.zenodo.org/docs/deposit/describe-records/), [create-new-upload](https://help.zenodo.org/docs/deposit/create-new-upload/)). Propose generic names; typical form labels are in parentheses. Required = citation minimum; recommended = findability.

| # | Generic name (typical label) | Priority | How to propose |
|---|---|---|---|
| 1 | Files | required | Primary file is the final PDF. Ask before adding HTML / Markdown. Many repositories freeze files after publish |
| 2 | DOI (Digital Object Identifier) | recommended | First public release with no existing DOI: let the repository mint it, or reserve first. Ask whether to embed a reserved DOI in the PDF |
| 3 | Resource type | required | Independent pre-review release: Publication → Preprint (or Working paper). Thesis, data, and software often deserve separate records |
| 4 | Title | required | Main title in the manuscript language. Whether the subtitle shares this field depends on the UI; if additional titles exist, keep this field as the main title only |
| 5 | Additional titles (subtitle / translated title / alternative title) | recommended | Subtitle → subtitle. Parallel-language title → translated title with a language tag. `blank` if SoT has no translation |
| 6 | Publication date | required | First date the work was made public. Today if this is the first release. If already public elsewhere, that earlier date. Do not use a future date or the draft-creation date |
| 7 | Creators | required | Authors who appear in the citation. Split family / given names. Affiliation as in SoT (empty is valid when there is none). ORCID only if provided. Leave role blank (optional; creators already are the citing authors. There is no Author option. Editor etc. belong on contributors) |
| 8 | Description (abstract) | recommended | Abstract from the outline or manuscript, verbatim. Do not add bold or links even if the UI allows HTML. A translated abstract is an additional description |
| 9 | Additional descriptions (notes / methods / technical info) | optional | Version notes, relation to prior work, missing-data caveats — not the abstract. `blank` if none |
| 10 | Licenses and rights | required | License from SoT. If unset, propose CC BY 4.0 as `needs-author`. Do not confuse this with the metadata license (Zenodo metadata is CC0) |
| 10b | Copyright | recommended | Current Zenodo (InvenioRDM) has a free-text field separate from the license. Form: `© {publication year} {creator display name}`. Rights holder matches the creator. May be left blank. Do not add a RightsHolder contributor just for this |
| 11 | Contributors | optional | Editors, funders, etc. who must not appear as citing authors. Do not duplicate creators |
| 12 | Keywords and subjects | recommended | Prefer outline keywords. Add controlled terms (EuroSciVoc, MeSH, GEMET, etc.) only when they fit; do not force a match |
| 13 | Language | recommended | Manuscript language (ISO 639). Bilingual files still pick one body language; translations go in additional titles / descriptions |
| 14 | Version | recommended | Version from outline / manuscript (e.g. `v0.1.0`). If missing, propose a date-based version and confirm |
| 15 | Publisher | optional | Repository default is fine (Zenodo → Zenodo). Do not put a journal publisher on a preprint |
| 16 | Funding | optional | Only with a grant number in SoT. Otherwise `blank` |
| 17 | Related identifiers / Related works | recommended | Prior papers, data, code, other-server copies. Relation type is mandatory (`cites`, `isNewVersionOf`, `isSupplementTo`, `isIdenticalTo`, etc.). Bare URLs are a last resort |
| 18 | Communities / collections | optional | Only collections the author already joined or explicitly chose. Do not invent or pick a community by guess |
| 19 | Visibility / Access right | required | Default for a paper preprint is open. Embargo only when a target journal policy requires it (`needs-author`) |
| 20 | References | optional | Only if the form has a separate box. Duplicating the manuscript reference list is not required; related identifiers often suffice |

### Relation types (common)

| Relation | When |
|---|---|
| `cites` | Prior paper or dataset this work cites |
| `isNewVersionOf` / `isPreviousVersionOf` | Revision of the same work |
| `isIdenticalTo` | Same version on another server |
| `isSupplementTo` / `isSupplementedBy` | Paper ↔ data / appendix pair |
| `isPartOf` / `hasPart` | Part of a series or collection |

If the author has a prior series, list only rows whose DOI is already in the matrix or outline. Do not add “probably related” papers without a DOI.

### Output template

`deposit-metadata.md` uses this shape. In chat, show the same table and a copy-ready code block per field.

```markdown
# Deposit metadata draft

- Venue:
- Drafted:
- Status: draft | author-approved
- SoT:

| # | Field | Status | Proposed value | Source |
|---|---|---|---|---|
| 4 | Title | locked | … | `docs/.../paper-outline.md` |

## Copy-ready

### Title
…
```

Lead with the table, then ask the `needs-author` questions. Do not end by dumping the whole file again.

## Outputs
- `docs/design/submission-plan.md` (venue rationale, procedure, schedule)
- `docs/design/deposit-metadata.md` (per-field deposit draft; `docs/<paper-id>/design/` in multi-paper repos)
