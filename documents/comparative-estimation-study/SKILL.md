---
name: Comparative Estimation Study
description: Compare AI-generated estimations with actual company PDFs to identify price differences and new items. Use when users need to validate estimations against real company quotes.
---

# Comparative Estimation Study

Compare AI-generated baseline estimations with actual company PDFs to identify pricing differences and detect new items.

## When to Use This Skill

Use this skill when the user asks about:
- Comparing AI estimations with company quotes
- Validating baseline estimations against actual PDFs
- Finding price differences between baseline and company data
- Identifying new items in company estimates
- Reconciling estimation data with supplier quotes

## Function Signature

```python
def process_comparative_study(file_urls: List[str], output_path: str) -> str:
    """
    Compare baseline JSON estimation with company PDF quotes

    Matching Rules:
    - Two-layer designation matching: string comparison → semantic similarity (embeddings)
    - Pre-filters: number + unit + quantity must match
    - is_new = False: For all items that exist in baseline JSON
    - is_new = True: ONLY for items in PDF with 'number' not in baseline
    - Prices updated if different or if baseline has null values
    - Section totals automatically recalculated

    Args:
        file_urls: List of URLs (first must be JSON baseline, rest are PDFs)
        output_path: Path to save output JSON

    Returns:
        str: Path to output JSON file with is_new flags (includes UUID in filename)

    Raises:
        ValueError: If no JSON or no PDFs found in URLs
        Exception: For download or processing errors
    """
```

## CLI Usage

```bash
# Compare baseline JSON with company PDFs
python comparative_study.py \
  --file-urls https://storage.com/baseline.json https://storage.com/quote1.pdf https://storage.com/quote2.pdf \
  --output-path temp_files/temp_project_123/comparison_result.json

# Note: The script automatically appends a UUID to the output filename
# Example output: comparison_result_a1b2c3d4-5678-90ab-cdef-1234567890ab.json
```

**⏱️ Important:** When using this skill programmatically (not CLI), ensure timeout is set to at least **3 minutes** to allow sufficient time for PDF extraction and semantic matching operations.

## Input Format

### File URLs (Required Order)
1. **First URL**: Baseline JSON (AI estimation output)
2. **Remaining URLs**: Company PDF quotes (1 or more)

### Baseline JSON Structure
```json
{
  "projectId": "123",
  "projectName": "Construction Project",
  "pricingLines": [
    {
      "type": "line",
      "number": "1.1",
      "designation": "Installation de chantier",
      "unit": "F",
      "quantity": "1",
      "unitPrice": 24000,
      "totalPrice": 24000
    }
  ]
}
```

### PDF Content
Company estimate documents with pricing tables containing:
- Designation (item description)
- Unit (measurement unit)
- Quantity
- Unit price
- Total price

## Matching Logic

### Two-Layer Designation Matching

**Pre-filters (must pass first):**
1. **Number**: Must match or either is null (e.g., "1.1" = "1.1")
2. **Unit**: Must match or either is null (e.g., "F" = "F")
3. **Quantity**: Must match or either is null (e.g., "1" = "1")

**Layer 1 - String Matching (Fast):**
- Designation matches via string comparison (exact or substring)
- Normalized text (lowercase, no accents, no special chars)

**Layer 2 - Semantic Matching (Fallback):**
- If string match fails, use Voyage AI embeddings
- Computes cosine similarity between designations
- Threshold: 0.8 (80% semantic similarity)
- Example: "Installation de chantier" ≈ "Installation chantier principal"

### Price Update Logic
- **Baseline has null, PDF has values**: Always update with PDF values
- **Both have values and differ**: Update with PDF values
- **Both have same values**: Keep baseline values unchanged

### is_new Flag Rules
- **is_new = False**: All items that exist in baseline JSON (by number)
- **is_new = True**: ONLY items in PDF whose 'number' doesn't exist in baseline
- Applies to all types: line, section, titre

### Special Features
- **Null value handling**: Null/empty values treated as wildcards in matching
- **Section totals**: Automatically recalculated for type="titre" items
- **Type flexibility**: Matches across different types (section → line)

## Output Format

Updated JSON with `is_new` field added to each pricing line:

```json
{
  "projectId": "123",
  "pricingLines": [
    {
      "type": "line",
      "number": "1.1",
      "designation": "Installation de chantier",
      "unit": "F",
      "quantity": "1",
      "unitPrice": 24000,
      "totalPrice": 24000,
      "is_new": false
    },
    {
      "type": "line",
      "number": "1.2",
      "designation": "Signalisation de chantier",
      "unit": "F",
      "quantity": "1",
      "unitPrice": 5000,
      "totalPrice": 5000,
      "is_new": true
    }
  ]
}
```

## Processing Pipeline

1. **Download Files** - Fetches JSON and PDFs from URLs
2. **Load Baseline** - Parses baseline JSON estimation
3. **Extract PDFs** - Uses LlamaExtract to parse PDF pricing tables
4. **Merge PDF Data** - Combines pricing lines from all PDFs
5. **Build Baseline Numbers** - Collects all 'number' fields from baseline (all types)
6. **Match & Update** - Applies two-layer matching (string → embeddings) and updates prices
7. **Add New Items** - Adds PDF items whose numbers don't exist in baseline
8. **Recalculate Totals** - Updates section/titre totalPrice based on child lines
9. **Save Output** - Writes updated JSON with is_new flags (UUID automatically appended to filename)

## Error Handling

- No JSON URL ValueError
- No PDF URLs ValueError
- Download failure Exception with URL details
- Invalid file format Logs error and skips
- PDF extraction failure Exception

## Environment Variables

```bash
# Required for PDF extraction
LLAMA_CLOUD_API_KEY=llx-...   # For LlamaExtract PDF parsing

# Required for semantic similarity matching
VOYAGE_API_KEY=pa-...          # For Voyage AI embeddings
```

## Examples

### Programmatic Usage

```python
from comparative_study import process_comparative_study

file_urls = [
    "https://storage.com/baseline.json",
    "https://storage.com/company_quote1.pdf",
    "https://storage.com/company_quote2.pdf"
]
output_path = "temp_files/temp_project_456/comparison.json"

result = process_comparative_study(file_urls, output_path)
# Returns: "temp_files/temp_project_456/comparison_<uuid>.json"
# Example: "temp_files/temp_project_456/comparison_a1b2c3d4-5678-90ab-cdef-1234567890ab.json"
```

## Notes

- **URL Order**: JSON must be first, followed by PDFs
- **Multiple PDFs**: All PDF pricing lines are merged before matching
- **Text Normalization**: Removes accents, special chars, common French stop words
- **Price Tolerance**: 1% tolerance for floating-point precision
- **Temporary Files**: Auto-cleaned after processing
- **Designation Priority**: Uses PDF designation when is_new = True
