---
name: evo-citation-scorer
description: Compares parsed BibTeX citation metadata against API results using fuzzy string matching and multi-factor scoring to classify citations as real or fake, then outputs the final JSON report.
---

# evo-citation-scorer

Scores and classifies citations as real or fake.

## Key Functions

- `normalize_string(text)` - Normalize for comparison (lowercase, no punctuation)
- `calculate_title_similarity(title1, title2)` - Token-based title similarity (0-100)
- `compute_composite_score(citation, api_result)` - Multi-factor score (title 50%, author 30%, year 20%)
- `classify_citation(verification_result)` - Classify as Real/Fake based on scores
- `export_fake_citations_json(fake_titles, output_file)` - Write sorted JSON output

## Classification Logic

1. DOI resolves via CrossRef → Real
2. No DOI or DOI fails → search CrossRef by title
3. Best composite score >= 70 → Real
4. Below 70 → Fake

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-citation-scorer/scripts')
from utils import classify_citation, export_fake_citations_json

# After verification
status = classify_citation(verification_result)
if status == 'Fake':
    fake_titles.append(verification_result['title'])

export_fake_citations_json(fake_titles, '/root/answer.json')
```
