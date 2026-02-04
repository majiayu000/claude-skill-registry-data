---
name: Construction Document Ingestion
description: Process construction estimate documents (Excel/CSV/PDF) from Supabase and convert them to EstimationElement format. Use when users need to ingest construction estimates, DQE (Descriptive Quantitative Estimate), or devis files.
---

# Construction Document Ingestion

Process construction estimate documents (Excel, CSV, PDF) and extract building elements into EstimationElement format for cost estimation.

## When to Use This Skill

Use this skill when the user asks about:
- Processing construction estimate documents (DQE, devis, BPU)
- Extracting building cost data from Excel/CSV/PDF files
- Converting construction estimates to estimation-ready format
- Ingesting data from Vectorworks, spreadsheets, or PDF estimates
- Downloading and processing files from Supabase storage

## Agent Integration (Recommended)

### Phase 1 of Estimation Workflow

This skill is **Phase 1** in the multi-phase estimation workflow:

```
Phase 0: file_manager creates workspace
   └─> temp_files/temp_project_{project_id}/

Phase 1: Ingestion processes document  ← THIS SKILL
   Input:  Supabase URL to Excel/CSV/PDF file
   Output: temp_files/temp_project_{project_id}/ingestion_uuid.json

Phase 2: context_extraction analyzes building
   └─> Uses ingestion output
```

### Function Signature

```python
def process_excel_input(supabase_url: str, output_path: str) -> str:
    """
    Agent-compatible entry point for construction document processing

    Phase 1 of Estimation Workflow:
    - Downloads file from Supabase URL
    - Converts to markdown using LlamaParse
    - Extracts structure with LLM (Claude Haiku)
    - Performs code-based data extraction
    - Transforms to EstimationElement format

    Args:
        supabase_url: Supabase public URL to Excel/CSV/PDF file
        output_path: Path to save output JSON (should be in temp directory)
                    Example: "temp_files/temp_project_{project_id}/ingestion_{uuid}.json"

    Returns:
        str: Path to processed output JSON file

    Raises:
        ValueError: If file type cannot be detected from URL
        FileNotFoundError: If download fails
        Exception: For processing errors
    """
```

### Usage in Agent Workflow

```python
# Phase 0: file_manager creates workspace
workspace_dir = file_manager.create_workspace(project_id="123")
# Returns: "temp_files/temp_project_123/"

# Phase 1: Ingestion downloads and processes file
supabase_url = "https://your-supabase-url.com/storage/v1/object/public/bucket/file.xlsx"
output_path = os.path.join(workspace_dir, f"ingestion_{uuid.uuid4()}.json")

result_path = ingestion.process_excel_input(supabase_url, output_path)
# Returns: "temp_files/temp_project_123/ingestion_xyz.json"

# Phase 2: context_extraction uses ingestion output
context = context_extraction.extract(result_path)
```

## CLI Usage (For Local Testing)

### Run the Script Directly

```bash
# Process file from Supabase URL (output to temp directory)
python process_vectorworks_input.py \
  --supabase-url https://your-supabase.com/storage/v1/object/public/bucket/estimate.xlsx \
  --output temp_files/temp_project_123/ingestion_abc.json

# Process CSV file
python process_vectorworks_input.py \
  --supabase-url https://your-supabase.com/storage/v1/object/public/bucket/devis.csv \
  --output temp_files/output.json

# Process PDF file
python process_vectorworks_input.py \
  --supabase-url https://your-supabase.com/storage/v1/object/public/bucket/dqe.pdf \
  --output temp_files/result.json
```

**Important**: Always specify the `--output` flag with a path in the `temp_files` directory to ensure proper workspace isolation.

### Call as Python Function

For programmatic use in other Python code:

```python
from process_vectorworks_input import process_excel_input

# Download from Supabase and process
supabase_url = "https://your-supabase.com/.../estimate.xlsx"
output_path = "temp_files/temp_project_123/ingestion_xyz.json"

result = process_excel_input(supabase_url, output_path)
# Returns: str (path to output file)
```

## Input Format

### Supported File Types

The script automatically detects file type from URL extension:
- **Excel**: `.xlsx`, `.xls`
- **CSV**: `.csv`
- **PDF**: `.pdf`

### Expected Document Structure

Construction estimate documents (DQE, devis, BPU) with:

#### Hierarchical Sections
```
I    - Section Title (e.g., "Préparation de chantier")
1.1  - Item description
1.2  - Item description
II   - Another Section
2.1  - Subsection
2.1.1 - Item description
```

#### Data Columns
The script looks for these columns (case-insensitive):
- **U** or **Unité**: Unit of measurement
- **Q** or **Quantité**: Quantity
- **PU** or **Prix Unitaire**: Unit price
- **Total HT** or **Total Hors Taxe**: Total price excluding tax
- **Limite de prestation**: Service limit/assignment

#### Example Excel/CSV Structure
```
Item ID | Description              | U  | Q   | PU      | Total HT | Limite de prestation
--------|--------------------------|----|----|---------|----------|---------------------
I       | Préparation de chantier  | U  | Q  | PU      | Total HT | Limite de prestation
1.1     | Installation de chantier | F  | 1  | 24000   | 24000.0  | ?
1.2     | Signalisation            | F  | -  | 0       | 0.0      | Hors lot
II      | Démolitions              | U  | Q  | PU      | Total HT |
2.1.1   | Dépose de bordures       | ml | 50 | 14      | 700.0    | Lot VRD
```

## Processing Pipeline

1. **Download from Supabase** - Fetches file and detects type (xlsx, csv, pdf)
2. **Convert to Markdown** - Uses LlamaParse to convert document
3. **Read XLSX Directly** - For Excel files, reads with pandas for accuracy
4. **Pre-process Markdown** - Cleans empty rows and formatting
5. **LLM Structure Extraction** - Claude Haiku extracts ToC and schema
6. **Column Filtering** - Keeps first 2 columns + columns with valid keywords (U, PU, Q, Total HT, etc.)
7. **Chunk by Sections** - Splits document using Table of Contents
8. **Code-based Extraction** - Extracts items matching patterns, skips subtotals
9. **Transform to EstimationElement** - Converts to final output format


## Field Mapping

### Project-Level Fields
- `project.name` ← Default: "Construction Project"
- `project.description` ← Default: "Extracted from construction estimate"

### Building Element Fields

#### Identity (Required)
- `project_id` ← Generated UUID
- `building_id` ← Item ID from document (1.1, 2.1.1, etc.)
- `building_name` ← Item description (or fallback to item_id)
- `building_description` ← Item description

#### Section Context
- `building_elm_section` ← Section ID + Section Title (e.g., "I - Préparation de chantier")

#### Quantities (Dynamic)
All other fields are prefixed with `building_elm_`:
- `building_elm_unit` ← U column (Unité)
- `building_elm_quantity` ← Q column (Quantité)
- `building_elm_unit_price` ← PU column (Prix Unitaire)
- `building_elm_total_ht` ← Total HT column
- `building_elm_total_price` ← Alternative total column
- `building_elm_lot_assignment` ← Limite de prestation
- ... and any other dynamic columns found in the document

## Validation

The script validates using Pydantic schemas:
- ✅ Document structure (TableOfContentsSection, DocumentSchema)
- ✅ Construction items (ConstructionItem)
- ✅ Output format (EstimationElement)
- ✅ Required fields (item_id, section_id, description)
- ✅ Data types (strings, floats, integers)

## Error Handling

The script handles:
- ❌ Invalid URL format → ValueError with details
- ❌ Download failure → Logs error, raises exception
- ❌ Unsupported file type → ValueError
- ❌ LlamaParse failure → Logs error, raises exception
- ❌ LLM extraction failure → Logs error, raises exception
- ❌ Invalid item data → Logs warning, skips item
- ❌ Column filtering issues → Logs details, continues

## Examples

### CLI Usage

```bash
# Process Excel file from Supabase
python process_vectorworks_input.py \
  --supabase-url https://your-supabase.com/.../estimate.xlsx \
  --output temp_files/temp_project_456/output.json

# Output:
# 2025-11-11 10:30:15 - INFO - Starting ingestion pipeline...
# 2025-11-11 10:30:15 - INFO - Downloading file from: https://...
# 2025-11-11 10:30:15 - INFO - Detected file type: xlsx
# 2025-11-11 10:30:15 - INFO - File downloaded to: /tmp/estimate.xlsx
# 2025-11-11 10:30:16 - INFO - Converting xlsx file to markdown
# 2025-11-11 10:30:16 - INFO - Reading XLSX directly for accurate data extraction...
# 2025-11-11 10:30:16 - INFO - Read 250 rows, 16 columns from XLSX
# 2025-11-11 10:30:16 - INFO - Filtering columns based on valid keywords...
# 2025-11-11 10:30:16 - INFO - Found keyword 'u' in column 3 at row 7
# 2025-11-11 10:30:16 - INFO - Found keyword 'q' in column 4 at row 7
# 2025-11-11 10:30:16 - INFO - Total columns after: 8
# 2025-11-11 10:30:17 - INFO - Extracting document structure with LLM...
# 2025-11-11 10:30:18 - INFO - Extracted 10 sections from ToC
# 2025-11-11 10:30:18 - INFO - Chunking DataFrame by sections...
# 2025-11-11 10:30:18 - INFO - Extracting items using code-based extraction...
# 2025-11-11 10:30:18 - INFO - Section I: extracted 6 items
# 2025-11-11 10:30:18 - INFO - Section II: extracted 15 items
# 2025-11-11 10:30:19 - INFO - Total extracted: 85 items
# 2025-11-11 10:30:19 - INFO - Transformed 85 elements
# 2025-11-11 10:30:19 - INFO - Pipeline complete. Output saved to: temp_files/temp_project_456/output.json
# 2025-11-11 10:30:19 - INFO - Extracted 85 elements
```

## Logging

The script provides detailed logging:
- **INFO**: Processing progress, entity counts, found keywords, column filtering
- **WARNING**: Missing data, fallback strategies used
- **ERROR**: Validation failures, processing errors
- **DEBUG**: Detailed extraction info, item-by-item logging

Log output goes to stderr (doesn't interfere with JSON output).

## Platform Compatibility

- ✅ Windows (UTF-8 encoding handled)
- ✅ macOS
- ✅ Linux
- ✅ Python 3.8+

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...  # For Claude Haiku LLM
LLAMA_CLOUD_API_KEY=llx-...   # For LlamaParse document conversion

# Optional
LOG_LEVEL=INFO  # Logging level (DEBUG, INFO, WARNING, ERROR)
```

## Notes

- **Supabase URLs**: Must be publicly accessible or properly authenticated
- **File Type Detection**: Automatic from URL extension
- **Column Filtering**: Always keeps first 2 columns, filters rest by keywords
- **LLM Usage**: Claude Haiku for structure extraction (cost-effective)
- **Excel vs CSV**: Excel preferred for numeric precision
- **PDF Support**: Works but may have OCR issues with complex layouts
- **Output Format**: Always pretty-printed JSON with indent=2
- **Workspace Isolation**: Output files saved in temp directories
- **File Naming**: Output files should use pattern `ingestion_{uuid}.json`
- **Path Handling**: Always use temp_files directory for output
- **Dynamic Fields**: All document-specific fields prefixed with `building_elm_`
