---
name: curate-bulk-rnaseq
description: Process bulk RNA-seq datasets for VEuPathDB resources
---

# Bulk RNA-seq Dataset Curation

This skill guides processing of bulk RNA-seq datasets for VEuPathDB resources.

## Prerequisites Check

This workflow requires the following repositories in `veupathdb-repos/`:
- ApiCommonPresenters
- EbrcModelCommon

**First, run the repository status check** to verify repositories are present:

_Note: this script is located in the skill directory_

```bash
bash scripts/check-repos.sh ApiCommonPresenters EbrcModelCommon
```

If repositories are missing, the script will provide clone instructions.

**Branch Confirmation:** After verifying repositories exist, check their current branches and status using `git -C <path>`, then confirm with the user before proceeding.

Example:
```bash
git -C veupathdb-repos/ApiCommonPresenters branch --show-current
git -C veupathdb-repos/ApiCommonPresenters status -sb
```

## Working Directory (Curation Workspace Directory)

**IMPORTANT**: All commands in this workflow must be run from your curation workspace directory (the directory that contains `veupathdb-repos/` as a subdirectory).

**For Claude Code**:
- DO NOT use `cd` commands to change into subdirectories
- Use `git -C <path>` for git operations in subdirectories
- Use absolute paths or relative paths from the curation workspace directory

The workflow creates:
- `tmp/` - Intermediate files (gitignored)
- `delivery/bulk-rnaseq/<BIOPROJECT>/` - Pipeline outputs (gitignored)

## Required Information

Gather the following before starting:

- **VEuPathDB project** - Valid projects listed in [resources/valid-projects.json](resources/valid-projects.json)
- **BioProject accession** (e.g., `PRJNA1018599`)

## Optional: Journal Article PDF

If a journal article is available for this dataset, providing it enhances the curation workflow:

- **Better descriptions**: Abstract and introduction provide richer experiment context
- **Strandedness detection**: Methods section reveals library prep protocol
- **Contact identification**: Author affiliations clarify roles (experimentalist, analyst, submitter)
- **Sample annotation context**: Methods help decode unclear sample metadata

**To include a PDF:**
1. Download the article PDF
2. Copy it to `tmp/<BIOPROJECT>_article.pdf` (e.g., `tmp/PRJNA1018599_article.pdf`)
3. Tell Claude the PDF is available when starting Step 1

The PDF will be processed by a subagent once in Step 1 and extracted data saved to `tmp/<BIOPROJECT>_pdf_extracted.json` for use throughout the workflow.

## Workflow Overview

### Step 1: Fetch Metadata (and Extract PDF)

Fetch run-level metadata from ENA and sample attributes from NCBI BioSample. If a journal article PDF is available, extract key information for use in later steps.

**Commands:**
```bash
node scripts/fetch-sra-metadata.js <BIOPROJECT>
```

**Output:** `tmp/<BIOPROJECT>_sra_metadata.json`

**Optional - Fetch MINiML for GEO-linked datasets:**
```bash
node scripts/fetch-miniml.js <BIOPROJECT>
```

**Output:** `tmp/<GSE>_family.xml` (if GEO-linked)

**Optional - Extract PDF data:**

If `tmp/<BIOPROJECT>_article.pdf` is present, a subagent will extract it (do not read it yourself).

**Output (on success):** `tmp/<BIOPROJECT>_pdf_extracted.json`

**Detailed instructions:** [Step 1 - Fetch Metadata](resources/step-1-fetch-metadata.md)

### Step 2: Analyze Samples

Claude analyzes the fetched metadata to:
1. Identify experimental factors (attributes that vary between samples)
2. Generate sample annotations with meaningful labels
3. Group technical replicates
4. Determine strand specificity

**Output:** `tmp/<BIOPROJECT>_sample_annotations.json`

**Detailed instructions:** [Step 2 - Analyze Samples](resources/step-2-analyze-samples.md)

### Step 3: Curate Contacts

Identify and curate contact entries from GEO contributors or BioProject submitters.

**Actions:**
- Search existing contacts in `veupathdb-repos/EbrcModelCommon/Model/lib/xml/datasetPresenters/contacts/allContacts.xml`
- Create new contact entries if needed
- Present choices to curator for review

**Detailed instructions:** [Step 3 - Curate Contacts](resources/step-3-curate-contacts.md)

### Step 4: Generate Presenter XML

Generate the datasetPresenter XML, review/edit it, then insert into the presenter file.

**Command:**
```bash
node scripts/generate-presenter-xml.js <BIOPROJECT> <PROJECT> <PRIMARY_CONTACT_ID> [ADDITIONAL_CONTACT_IDS...]
```

**Output:** `tmp/<BIOPROJECT>_presenter.xml`

**Workflow:**
1. Generate initial XML with script (saves to tmp/)
2. Review and edit the temp file to fill in TODOs (shortDisplayName, pubmedIds, etc.)
3. Insert finalized XML into presenter file

**Target file:** `veupathdb-repos/ApiCommonPresenters/Model/lib/xml/datasetPresenters/<PROJECT>.xml`

**Detailed instructions:** [Step 4 - Generate Presenter](resources/step-4-generate-presenter.md)

### Step 5: Generate Delivery Outputs

Generate pipeline configuration files for the data processing team.

**Commands:**
```bash
bash scripts/check-delivery-dirs.sh bulk-rnaseq <BIOPROJECT>
node scripts/generate-analysis-config.js <BIOPROJECT> [--strand-specific]
node scripts/generate-samplesheet.js <BIOPROJECT> [strandedness]
```

The `strandedness` argument accepts: `stranded`, `unstranded`, or `auto`. If omitted, the script checks `_pdf_extracted.json` and `_sample_annotations.json` before falling back to `auto`.

**Outputs in `delivery/bulk-rnaseq/<BIOPROJECT>/`:**
- `analysisConfig.xml` - Pipeline configuration
- `samplesheet.csv` - Also for the processing pipeline

**Detailed instructions:** [Step 5 - Generate Outputs](resources/step-5-generate-outputs.md)

## Next Steps

After completing this workflow:
1. Review generated XML for TODO fields that require curator input
2. Commit changes to dataset branch (curator handles git operations)
3. Create pull request for review (curator handles PR creation)
4. Deliver output files from `delivery/bulk-rnaseq/<BIOPROJECT>/` to data processing team

## Resources

- [Step 1 - Fetch Metadata](resources/step-1-fetch-metadata.md)
- [Step 2 - Analyze Samples](resources/step-2-analyze-samples.md)
- [Step 3 - Curate Contacts](resources/step-3-curate-contacts.md)
- [Step 4 - Generate Presenter](resources/step-4-generate-presenter.md)
- [Step 5 - Generate Outputs](resources/step-5-generate-outputs.md)
- [PDF Extraction](resources/pdf-extraction.md)
- [Editing Large XML Files](resources/editing-large-xml.md)
- [Valid VEuPathDB Projects](resources/valid-projects.json)

## Scripts

- `scripts/fetch-sra-metadata.js` - Fetches SRA run metadata from ENA + BioSample attributes from NCBI
- `scripts/fetch-miniml.js` - Fetches MINiML XML for GEO-linked datasets
- `scripts/generate-presenter-xml.js` - Generates RNA-seq datasetPresenter XML
- `scripts/generate-analysis-config.js` - Generates analysisConfig.xml for pipeline
- `scripts/generate-samplesheet.js` - Generates/delivers samplesheet.csv and sampleAnnotations.json
- `scripts/check-repos.sh` - Validates veupathdb-repos/ repository setup (synced from shared/)
- `scripts/check-delivery-dirs.sh` - Creates delivery directory structure (synced from shared/)
