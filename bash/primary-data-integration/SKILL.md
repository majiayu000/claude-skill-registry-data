---
name: primary-data-integration
version: 1.0.0
description: Use when ingesting primary research data (transcripts, survey logs, lab notes) to apply AI Ignore rules, mask PII via mapping files, and bind data to manuscript claims
---

# Primary Research Data & Fieldwork Integration Skill

## Purpose
Catalog (`docs/data/research-data-index.md`) and directly bind primary empirical research data to manuscript claims, backed by automated **AI Ignore rules** and **PII masking** to protect sensitive participant data and credentials.

## Trigger Conditions
- When raw research data (experiment logs, survey results, interview transcripts, archival documents) is collected and ready for analysis
- When binding primary data to specific claims in the manuscript

## Security & Privacy Protections

### 1. AI Ignore Setup
Run [`scripts/setup_ai_ignore.py`](../../../scripts/setup_ai_ignore.py) to exclude raw research directories (`raw_data/`, `transcripts_raw/`) from AI Agent context:
```bash
# Basic run (Submodule: python3 .scholarly-agent-skills/scripts/setup_ai_ignore.py)
python3 scripts/setup_ai_ignore.py
```
(Configures `.cursorignore`, `.claudeignore`, `.agentsignore`, and `.ignore` automatically)

### 2. Automated PII Masking
Run [`scripts/mask_pii_data.py`](../../../scripts/mask_pii_data.py) using a JSON mapping file (`mapping.json`) to prevent real names from remaining in shell history or process listings:
```bash
# Run with a mapping file
python3 scripts/mask_pii_data.py data/raw_interview.txt --names-file mapping.json
```
*(Example `mapping.json`: `{"John Doe": "Participant_A", "Jane Smith": "Participant_B"}`. Keep `mapping.json` gitignored / AI ignored.)*
(Saves anonymized data in `data/anonymized/` safe for AI Agent analysis)

> [!NOTE]
> When running inside a submodule deployment, prefix script paths with `.scholarly-agent-skills/` (e.g. `python3 .scholarly-agent-skills/scripts/setup_ai_ignore.py`).

## Workflow

### Step 1: Create Research Data Inventory (`docs/data/research-data-index.md`)
Catalog all anonymized research data with unique IDs:

```markdown
### Data ID: [e.g., DATA-2024-01]
- **Title**: 2024 Summer Urban Commerce Perception Survey (Anonymized)
- **Data Type**: Quantitative (N=350, valid response rate 82%)
- **Collection Method & Period**: July–August 2024 / In-person interviews
- **Storage Path**: `data/anonymized/2024_summer_survey.csv`

### Data ID: [e.g., INTERVIEW-03]
- **Title**: Senior Engineer Interview Transcript (PII-Masked)
- **Data Type**: Qualitative (Verbatim transcription / Names and phone numbers anonymized)
- **Storage Path**: `data/anonymized/transcript_B.md`
```

### Step 2: Bind Claims to Primary Data
When drafting the manuscript, the AI Agent references data IDs from `docs/data/research-data-index.md` to embed primary evidence immediately after each claim.

### Step 3: Format Qualitative Blockquotes
Format anonymized interview quotes or archival text as academic blockquotes, followed by the researcher's interpretation.

## Outputs
- `.cursorignore`, `.claudeignore`, `.agentsignore`, `.ignore` (AI Ignore Configuration)
- `data/anonymized/` (PII-Masked Safe Data)
- `docs/data/research-data-index.md` (Primary Data Inventory)

