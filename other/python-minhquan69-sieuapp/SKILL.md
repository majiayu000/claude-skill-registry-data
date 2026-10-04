---
name: python
description: "Skill for the Python area of iVista-Client-Application. 21 symbols across 3 files."
---

# Python

21 symbols | 3 files | Cohesion: 100%

## When to Use

- Working with code in `V3SClient/`
- Understanding how image_to_data_url, parse_json, parse_json_with_repair work
- Modifying python-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `V3SClient/python/llm_client.py` | image_to_data_url, _get_content, _call_api, parse_json, _repair_json_text (+4) |
| `V3SClient/python/sync_client_test (2).py` | auth_headers, load_state, write_state, safe_output_path, iter_files (+4) |
| `V3SClient/python/database.py` | Base, Record, Image |

## Entry Points

Start here when exploring this area:

- **`image_to_data_url`** (Function) — `V3SClient/python/llm_client.py:410`
- **`parse_json`** (Function) — `V3SClient/python/llm_client.py:496`
- **`parse_json_with_repair`** (Function) — `V3SClient/python/llm_client.py:542`
- **`classify_document`** (Function) — `V3SClient/python/llm_client.py:553`
- **`detect_bbox`** (Function) — `V3SClient/python/llm_client.py:575`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `Base` | Class | `V3SClient/python/database.py` | 107 |
| `Record` | Class | `V3SClient/python/database.py` | 111 |
| `Image` | Class | `V3SClient/python/database.py` | 164 |
| `image_to_data_url` | Function | `V3SClient/python/llm_client.py` | 410 |
| `parse_json` | Function | `V3SClient/python/llm_client.py` | 496 |
| `parse_json_with_repair` | Function | `V3SClient/python/llm_client.py` | 542 |
| `classify_document` | Function | `V3SClient/python/llm_client.py` | 553 |
| `detect_bbox` | Function | `V3SClient/python/llm_client.py` | 575 |
| `ocr_document` | Function | `V3SClient/python/llm_client.py` | 616 |
| `auth_headers` | Function | `V3SClient/python/sync_client_test (2).py` | 17 |
| `load_state` | Function | `V3SClient/python/sync_client_test (2).py` | 21 |
| `write_state` | Function | `V3SClient/python/sync_client_test (2).py` | 29 |
| `safe_output_path` | Function | `V3SClient/python/sync_client_test (2).py` | 36 |
| `iter_files` | Function | `V3SClient/python/sync_client_test (2).py` | 49 |
| `download_file` | Function | `V3SClient/python/sync_client_test (2).py` | 66 |
| `sync_once` | Function | `V3SClient/python/sync_client_test (2).py` | 115 |
| `build_arg_parser` | Function | `V3SClient/python/sync_client_test (2).py` | 183 |
| `main` | Function | `V3SClient/python/sync_client_test (2).py` | 197 |
| `_get_content` | Function | `V3SClient/python/llm_client.py` | 428 |
| `_call_api` | Function | `V3SClient/python/llm_client.py` | 456 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Safe_output_path` | intra_community | 4 |
| `Main → Auth_headers` | intra_community | 4 |
| `Classify_document → _get_content` | intra_community | 3 |
| `Detect_bbox → _get_content` | intra_community | 3 |
| `Ocr_document → _get_content` | intra_community | 3 |
| `Ocr_document → Parse_json` | intra_community | 3 |
| `Ocr_document → _repair_json_text` | intra_community | 3 |

## How to Explore

1. `context({name: "image_to_data_url"})` — see callers and callees
2. `query({search_query: "python"})` — find related execution flows
3. Read key files listed above for implementation details
4. `explain({target: "<file or symbol>"})` — persisted taint findings (source→sink data flows), when indexed with `--pdg`
