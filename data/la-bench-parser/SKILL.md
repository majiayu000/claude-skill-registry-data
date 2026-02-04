---
name: la-bench-parser
description: Parse LA-Bench format JSONL files to extract experimental protocol data by ID. This skill should be used when working with LA-Bench datasets to retrieve structured experimental instructions, materials, protocol steps, expected outcomes, and references for a specific experiment entry.
---

# LA-Bench Parser

## Overview

Parse LA-Bench format JSONL files and extract structured experimental protocol data for specific entries. Extract instruction, mandatory_objects, source_protocol_steps, expected_final_states, and references fields from LA-Bench dataset entries.

## When to Use This Skill

Use this skill when:
- Working with LA-Bench format JSONL files (e.g., `data/private_test_input.jsonl`, `data/public_test.jsonl`)
- Needing to extract experimental protocol data for a specific entry ID
- Processing multiple LA-Bench entries programmatically
- Integrating LA-Bench data into other workflows or skills

## Usage

### Input Requirements

Provide two pieces of information:
1. **JSONL file path**: Path to the LA-Bench format JSONL file
2. **Entry ID**: The ID of the specific entry to extract (e.g., `private_test_1`, `public_test_5`)

### Execution

Execute the parser script using the Bash tool and save output to standardized location:

```bash
python scripts/parse_labench.py <jsonl_path> <entry_id> > workdir/<filename>_<entry_id>/input.json
```

**Example:**
```bash
# For file: data/public_test.jsonl, entry: public_test_1
# Output path: workdir/public_test_public_test_1/input.json
mkdir -p workdir/public_test_public_test_1
python .claude/skills/la-bench-parser/scripts/parse_labench.py data/public_test.jsonl public_test_1 > workdir/public_test_public_test_1/input.json
```

**Directory naming convention:**
- Extract filename (without extension) from JSONL path: `public_test` from `data/public_test.jsonl`
- Combine with entry ID: `public_test_public_test_1`
- Create directory: `workdir/public_test_public_test_1/`
- Save output as: `input.json`

### Output Format

The script outputs structured JSON data to stdout, which should be redirected to `workdir/<filename>_<entry_id>/input.json`. The JSON contains:

- **id**: Entry identifier
- **instruction**: High-level experimental instruction in Japanese
- **mandatory_objects**: List of required materials and equipment
- **source_protocol_steps**: Array of protocol steps with id and text fields
- **expected_final_states**: List of expected experimental outcomes
- **references**: Array of reference materials with id and text fields

**Example output structure:**
```json
{
  "id": "private_test_1",
  "instruction": "1枚の384-well plateで培養している細胞に対して、cellpaintingを実施してください。",
  "mandatory_objects": [
    "全wellが40 µl/well の培地で細胞が培養されている384-well plate",
    "MitoTracker Deep Redの1 mM ストック溶液",
    ...
  ],
  "source_protocol_steps": [
    {
      "id": 1,
      "text": "生細胞染色液を調製する。100 mlの生細胞染色液を作るには..."
    },
    ...
  ],
  "expected_final_states": [
    "蛍光顕微鏡での撮影可能な染色処置のされた384-well plate。"
  ],
  "references": [
    {
      "id": 1,
      "text": "Cimini, Beth A., et al. \"Optimizing the Cell Painting assay...\""
    },
    ...
  ]
}
```

### Error Handling

The script handles common errors:
- **File not found**: Returns error if JSONL file doesn't exist
- **Entry not found**: Returns error if specified ID doesn't exist in the file
- **Invalid JSON**: Skips malformed lines and continues parsing
- **Exit codes**: Returns 0 on success, 1 on error

### Integration with Parent Skills

When integrating this skill into parent workflows:

1. Call the parser script using the Bash tool
2. Capture the JSON output from stdout
3. Parse the JSON output to extract specific fields as needed
4. Use the structured data in subsequent workflow steps

**Integration example:**
```bash
# Execute parser and capture output
output=$(python /path/to/parse_labench.py data/input.jsonl test_id)

# The output is valid JSON that can be parsed programmatically
# or passed to other tools/agents for further processing
```

## Resources

### scripts/parse_labench.py

Executable Python script that performs the parsing operation. The script:
- Reads JSONL files line by line for memory efficiency
- Extracts entries matching the specified ID
- Outputs clean, structured JSON to stdout
- Writes errors to stderr for proper error handling
- Can be executed directly without loading into context
