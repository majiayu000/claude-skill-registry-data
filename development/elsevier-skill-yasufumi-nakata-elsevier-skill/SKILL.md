---
name: elsevier-skill
description: Use Elsevier APIs (Scopus search / abstract / author / trends / institution / open access) via simple CLI scripts.
metadata:
  short-description: Academic literature lookup via Elsevier APIs
---

## Requirements
- Set environment variable `ELSEVIER_API_KEY`.

## What this skill can do
- Search papers (Scopus)
- Fetch abstract by EID or DOI
- Fetch author profile
- Analyze trends by year
- Count institution papers
- Search open access papers

## How to run (scripts)
All commands print JSON to stdout.

### Search papers
python scripts/elsevier.py search_papers --query "machine learning" --count 5 --year 2024

### Get abstract
python scripts/elsevier.py get_paper_abstract --doi "10.1016/j.artint.2023.103804"

### Get author info
python scripts/elsevier.py get_author_info --author_id "12345678900"

### Analyze trends
python scripts/elsevier.py analyze_research_trends --field "artificial intelligence" --years 2022 2023 2024

### Institution papers
python scripts/elsevier.py get_institution_papers --institution "MIT" --year 2024

### Open access search
python scripts/elsevier.py search_open_access_papers --field "quantum computing" --count 5 --year 2024
