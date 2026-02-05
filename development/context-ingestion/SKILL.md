---
name: context-ingestion
description: Scan project folder structure, validate organization, clone GitHub repository, and generate an inventory of available materials. First step of writer workflow. Use when starting a new manuscript project.
---

# Context Ingestion

Scans the project folder, validates structure, fetches the GitHub repository, and generates an inventory of all available materials.

## Input

User provides path to project folder (or current directory if already there).

## Workflow

```
[Receive project path]
     │
     ▼
[Validate Folder Structure] ─── Check required folders exist
     │
     ▼
[Parse config.md] ─── Extract GitHub URL, constraints
     │
     ▼
[Clone GitHub Repository] ─── Fetch code for analysis
     │
     ▼
[Inventory Materials] ─── List all available files
     │
     ▼
[Extract Ethics Content] ─── If ethics/ exists, generate notes/ethics-summary.md
     │
     ▼
[Generate inventory.md] ─── Structured summary
```

## Step 1: Validate Folder Structure

Check that required folders exist:

```bash
# Required structure
project/
├── papers/       # Must exist (can be empty)
├── data/         # Must exist (can be empty)
├── figures/      # Must exist (can be empty)
├── ethics/       # Optional - Ethics/governance documents (IRB, IACUC, etc.)
└── config.md     # Must exist
```

Validation:

```bash
cd /path/to/project

# Check required folders
[ -d "papers" ] || echo "ERROR: papers/ folder missing"
[ -d "data" ] || echo "ERROR: data/ folder missing"
[ -d "figures" ] || echo "ERROR: figures/ folder missing"
[ -f "config.md" ] || echo "ERROR: config.md missing"
```

If validation fails, inform user what's missing and provide the expected structure template.

## Step 2: Parse config.md

Extract configuration values:

```markdown
# Expected config.md format

## GitHub Repository
url: https://github.com/username/repo-name
branch: main
access: private

## Constraints
word_limit: 3500
target_journal: [Target Journal]
citation_style: AMA

## Additional Notes
[Free text notes]
```

Parse and store:
- `github_url`: Repository URL
- `github_branch`: Branch to clone (default: main)
- `github_access`: public or private
- `word_limit`: Target word count
- `target_journal`: Journal name for formatting
- `citation_style`: AMA, Vancouver, APA, etc.

## Step 3: Clone GitHub Repository

For public repositories:

```bash
git clone --depth 1 --branch main https://github.com/username/repo-name.git code/
```

For private repositories, user must have GitHub CLI authenticated:

```bash
gh repo clone username/repo-name code/ -- --depth 1 --branch main
```

If clone fails:
1. Check if `gh` is authenticated: `gh auth status`
2. Provide instructions: "Run `gh auth login` to authenticate"
3. Allow user to proceed without code (Methods section will be limited)

Store cloned repo at: `project/code/`

## Step 4: Inventory Materials

Scan each folder and catalog contents:

### Papers Inventory

```bash
ls -la papers/*.pdf 2>/dev/null | wc -l  # Count PDFs
```

For each PDF, extract basic info:
- Filename
- File size
- (Attempt to extract title from first page if possible)

### Data Inventory

```bash
ls -la data/*.csv data/*.xlsx 2>/dev/null
```

For each data file:
- Filename
- File size
- Row/column count (for CSVs)
- Sheet names (for Excel)

Preview CSV structure:

```bash
head -5 data/results.csv
```

### Figures Inventory

```bash
ls -la figures/*.png figures/*.jpg figures/*.svg 2>/dev/null
```

For each figure:
- Filename
- Dimensions (if determinable)
- File size

### Code Inventory

If GitHub clone succeeded:

```bash
find code/ -name "*.py" -o -name "*.ipynb" -o -name "*.R" | head -20
```

Identify:
- Primary language (Python, R, etc.)
- Notebook files (.ipynb)
- Key script files
- Requirements/dependencies file

### Ethics Inventory (Optional)

If `ethics/` folder exists, scan for governance documents:

```bash
ls -la ethics/*.pdf ethics/*.docx ethics/*.md 2>/dev/null
```

Supported formats:
- `.md` - Read directly with Read tool
- `.pdf` - Read with Claude's native PDF capability
- `.docx` - Extract text using `document-skills:docx` skill

## Step 5: Extract Ethics Content

**Skip this step if `ethics/` folder does not exist or is empty.**

For each document in `ethics/`:

1. Read the document content using appropriate method for format
2. Extract comprehensive study information
3. Generate `notes/ethics-summary.md`

### Ethics Summary Template

Create `notes/ethics-summary.md`:

```markdown
# Ethics/Governance Document Summary

**Source**: [filename]
**Extracted**: [timestamp]

## Study Identification
- **Protocol Title**: [extracted or "[not found]"]
- **Approval Number**: [extracted or "[not found]"]
- **Approving Body**: [IRB, IACUC, Ethics Committee, etc.]
- **Principal Investigator**: [extracted or "[not found]"]
- **Approval Date**: [extracted or "[not found]"]

## Study Design
- **Study Type**: [interventional/observational/retrospective/computational/etc.]
- **Design**: [RCT, cohort, case-control, cross-sectional, simulation, etc.]
- **Duration**: [study period]

## Population/Subjects
- **Target Population**: [description]
- **Inclusion Criteria**:
  - [criterion 1]
  - [criterion 2]
  - ...
- **Exclusion Criteria**:
  - [criterion 1]
  - [criterion 2]
  - ...
- **Sample Size**: [N with justification if provided]

## Procedures & Interventions
- [Procedure 1]
- [Procedure 2]
- ...

## Endpoints/Outcomes
- **Primary**: [endpoint]
- **Secondary**: [endpoints]

## Statistical Considerations
- **Power Analysis**: [if provided or "[not found]"]
- **Planned Analyses**: [if provided or "[not found]"]

## Notes
[Any additional relevant context, caveats, or sections that were unclear]
```

Mark fields as `[not found]` if not present in the document.

## Step 6: Generate inventory.md

Create structured inventory document:

```markdown
# Project Inventory

Generated: [timestamp]
Project: [folder name]

## Configuration

- **GitHub**: [url] (branch: [branch])
- **Target Journal**: [journal]
- **Word Limit**: [limit]
- **Citation Style**: [style]

## Papers ([count] files)

| Filename | Size | Notes |
|----------|------|-------|
| smith-2023.pdf | 1.2 MB | |
| jones-2022.pdf | 0.8 MB | |

## Data ([count] files)

| Filename | Size | Rows | Columns | Preview |
|----------|------|------|---------|---------|
| results.csv | 45 KB | 156 | 12 | patient_id, age, sex, ... |
| demographics.csv | 12 KB | 156 | 8 | patient_id, age, sex, ... |

## Figures ([count] files)

| Filename | Dimensions | Size |
|----------|------------|------|
| figure1.png | 1200x800 | 340 KB |
| figure2.png | 1000x600 | 210 KB |

## Code Repository

- **URL**: [github url]
- **Language**: Python
- **Key Files**:
  - `analysis.ipynb` - Main analysis notebook
  - `preprocessing.py` - Data preprocessing
  - `models.py` - ML models
- **Dependencies**: pandas, scikit-learn, matplotlib, ...

## Ethics Documents

| Filename | Format | Status |
|----------|--------|--------|
| protocol.pdf | PDF | ✓ Extracted to notes/ethics-summary.md |

*Or: "No ethics documents provided"*

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Papers | [n] | ✓ Ready |
| Data files | [n] | ✓ Ready |
| Figures | [n] | ✓ Ready |
| Code repo | 1 | ✓ Cloned |
| Ethics documents | [n] | ✓ Extracted / Not provided |

## Missing/Warnings

- [List any issues found]
```

## Output

Save to: `project/inventory.md`

Create notes directory structure:

```bash
mkdir -p notes/papers notes/papers-library drafts
```

Return to parent skill with inventory summary.
