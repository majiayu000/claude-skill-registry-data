---
name: curate-genome-assembly
description: Process genome assembly datasets for VEuPathDB resources
---

# Genome Assembly Dataset Curation

This skill guides processing of genome assembly datasets for VEuPathDB resources.

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

**Branch Confirmation:** After verifying repositories exist, check their current branches and status using `git -C <path>`, then confirm with the user before proceeding. Users typically create dataset-specific branches (see [curator branching guidelines](resources/curator-branching.md)).

Example:
```bash
git -C veupathdb-repos/ApiCommonPresenters branch --show-current
git -C veupathdb-repos/ApiCommonPresenters status -sb
```

## Working Directory (Curation Workspace Directory)

**IMPORTANT**: All commands in this workflow must be run from your curation workspace directory (the directory that contains `veupathdb-repos/` as a subdirectory).

**For Claude Code**:
- DO NOT use `cd` commands to change into `veupathdb-repos/` subdirectories
- Use `git -C <path>` for git operations in subdirectories
- Use absolute paths or relative paths from the curation workspace directory
- Example: `git -C veupathdb-repos/ApiCommonPresenters status` instead of `cd veupathdb-repos/ApiCommonPresenters && git status`

The workflow will create a `tmp/` subdirectory in the curation workspace directory for intermediate files.

## Required Information

Gather the following before starting:

- **VEuPathDB project** - Valid projects listed in [resources/valid-projects.json](resources/valid-projects.json)
- **Assembly GenBank accession** (e.g., `GCA_000988875.2` including version)

## Workflow Overview

### Step 1: Fetch Assembly Metadata from NCBI

Fetch assembly metadata from NCBI using the GenBank accession.

**Command:**
```bash
curl -X GET "https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/<ASSEMBLY_ACCESSION>/dataset_report" \
  -H "Accept: application/json" > tmp/<ASSEMBLY_ACCESSION>_dataset_report.json
```

**Detailed instructions:** [Step 1 - Fetch NCBI Metadata](resources/step-1-fetch-ncbi.md)

### Step 2: Fetch BioProject Metadata

Extract the BioProject accession from the assembly report and fetch additional details.

**Command:**
```bash
node scripts/fetch-bioproject.js <BIOPROJECT_ACCESSION>
```

This retrieves the BioProject title and description, saved to `tmp/<BIOPROJECT>_bioproject.json`.

**Detailed instructions:** [Step 2 - Fetch BioProject](resources/step-2-fetch-bioproject.md)

### Step 3: Fetch PubMed Data

Find and fetch publications for the genome assembly.

**Command:**
```bash
node scripts/fetch-pubmed.js <ASSEMBLY_ACCESSION>
```

Results saved to `tmp/<ASSEMBLY_ACCESSION>_pubmed.json`.

**Detailed instructions:** [Step 3 - Fetch PubMed](resources/step-3-fetch-pubmed.md)

### Step 4: Curate Contacts

Identify and curate contact entries for the genome submission.

**Contact identification priority:**
1. Named submitter from assembly metadata
2. Senior/last author from PubMed publications (if available)
3. Curator judgment for additional contacts

**Actions:**
- Search existing contacts in `veupathdb-repos/EbrcModelCommon/Model/lib/xml/datasetPresenters/contacts/allContacts.xml`
- Create new contact entries if needed
- Present choices to curator for review

**Detailed instructions:** [Step 4 - Curate Contacts](resources/step-4-curate-contacts.md)

### Step 5: Generate and Insert Presenter XML

Generate the datasetPresenter XML and insert it into the appropriate presenter file.

**Command:**
```bash
node scripts/generate-presenter-xml.js <ASSEMBLY_ACCESSION> <PROJECT> <PRIMARY_CONTACT_ID> [ADDITIONAL_CONTACT_IDS...]
```

**Target file:** `veupathdb-repos/ApiCommonPresenters/Model/lib/xml/datasetPresenters/<PROJECT>.xml`

**Detailed instructions:** [Step 5 - Update Presenter Files](resources/step-5-update-presenter.md)

## Next Steps

After completing this workflow:
1. Review generated XML for TODO fields that require curator input
2. Commit changes to dataset branch (curator handles git operations)
3. Create pull request for review (curator handles PR creation)

## Resources

- [Step 1 - Fetch NCBI Metadata](resources/step-1-fetch-ncbi.md)
- [Step 2 - Fetch BioProject](resources/step-2-fetch-bioproject.md)
- [Step 3 - Fetch PubMed](resources/step-3-fetch-pubmed.md)
- [Step 4 - Curate Contacts](resources/step-4-curate-contacts.md)
- [Step 5 - Update Presenter Files](resources/step-5-update-presenter.md)
- [Curator Branching Guidelines](resources/curator-branching.md)
- [Valid VEuPathDB Projects](resources/valid-projects.json)

## Scripts

- `scripts/fetch-bioproject.js` - Fetches BioProject metadata from NCBI (esearch + esummary)
- `scripts/fetch-pubmed.js` - Fetches PubMed records linked to a BioProject (elink + esummary)
- `scripts/generate-presenter-xml.js` - Generates datasetPresenter XML from fetched metadata
- `scripts/check-repos.sh` - Validates veupathdb-repos/ repository setup (synced from shared/)
