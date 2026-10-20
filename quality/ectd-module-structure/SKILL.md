---
name: ectd-module-structure
description: eCTD module structure and file naming (ICH M4 / eCTD v3.2.2 and v4.0, FDA and EU regional M1) for placing, naming and validating documents in a sequence. Use when asked where a document belongs in the CTD, how to name an eCTD leaf or folder, whether a sequence structure is valid, or to file a draft into a sequence through the Concept2Cure connector.
---

# eCTD module structure and naming

Concept2Cure holds the truth about a sequence; this skill tells you how to ask
it and how to read the answer. Never assert that a structure is valid, a
section is present, or a document is filed unless a connector tool said so.

## The five modules (ICH M4)

| Module | Content | Regional? |
|---|---|---|
| 1 | Administrative information and prescribing information (cover letter, forms, labeling, environmental assessment, …) | Yes — FDA `m1/us`, EU `m1/eu` |
| 2 | Summaries: 2.2 Introduction, 2.3 QOS, 2.4 Nonclinical overview, 2.5 Clinical overview, 2.6 Nonclinical summaries, 2.7 Clinical summaries | No |
| 3 | Quality: 3.2.S drug substance, 3.2.P drug product, 3.2.A appendices, 3.2.R regional, 3.3 literature | No (3.2.R regional) |
| 4 | Nonclinical study reports (4.2.1 pharmacology, 4.2.2 PK, 4.2.3 toxicology), 4.3 literature | No |
| 5 | Clinical study reports (5.3.1 biopharmaceutic, 5.3.3 PK, 5.3.4 PD, 5.3.5 efficacy/safety by indication, 5.3.6 post-marketing), 5.4 literature | No |

A **section code** names a place a document can go: `1.2`, `2.5`, `2.7.3`,
`3.2.S.4.2`, `5.3.5.1`. A bare module (`3`) is a container, never a leaf; the
connector refuses it.

## Naming rules the validators enforce

* Files and folders: lowercase letters, digits, hyphen, underscore, dot; no
  spaces; PDF leaves; keep paths short and stable across sequences.
* Sequence numbers are four digits (`0000`, `0001`, …); lifecycle operators
  are `new`, `replace`, `append`, `delete` and a replace/append must reference
  the leaf it modifies in the prior sequence.
* Every leaf carries an MD5 checksum in `util/index-md5.txt`; empty files are
  rejected by FDA.
* Regional backbone: `us-regional.xml` (FDA), `eu-regional.xml` (EMA),
  `jp-regional.xml` (PMDA), beside the ICH `index.xml`.

## Workflow with the connector

1. **Find the sequence**: `c2c_list_submissions` → `c2c_list_sequences` →
   `c2c_get_sequence_status` (shows existing leaves and the release-signature
   state).
2. **Check the proposed structure** before filing: `c2c_validate_ectd_structure`
   with `sequence_id` (stored leaves) or an explicit `leaves[]`. Report the
   engine's `valid`, `score`, missing required sections and the external
   validator posture verbatim. Passing the built-in check is not passing the
   agency validator; say so when `externalValidator.configured` is false.
3. **File the draft**: `c2c_file_draft_for_review` with `sequence_id`,
   `section_code`, `title`, a document pointer (`vault_document_id` from
   `c2c_list_vault_documents`, or `document_table` + `document_id`) and a
   `reason`. It creates a DRAFT leaf and returns the Submission Center link.
   Tell the user a named person must review, freeze and sign there; you
   cannot.
4. **Re-validate** after filing with `c2c_validate_ectd_structure`
   (`sequence_id`) and report the delta.

## What to do with refusals

A refusal names its cause: the sequence is frozen or dispatched, the document
belongs to another organisation, the section code is not a CTD section, the
scope was not granted. Relay it; do not retry with a different section or
document to "make it work".
