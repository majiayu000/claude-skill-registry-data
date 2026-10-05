---
name: dm-data
description: Query DM/Innodealing quant data through dm_quant_api_client. Use when the user asks to call or fetch DM data, DM PythonAPI, DM EDB macro indicators, EDB level IDs, bond market data, bond basic info, yield curves, rolling bonds, money-market rates, futures data, equity bars, or trade calendars.
---

# DM Data

## Overview

Use this skill to call the local DM PythonAPI client and the bundled DM API catalog. The Skill wraps the generic SDK method `DMQuantApiClient.post_data(data, api_path)` so a future agent does not need to re-open the PDF manual for common calls.

## Quick Start

1. Confirm credentials are available before making live calls:

```bash
export INNO_APP_KEY="..."
export INNO_SM4_KEY="..."
```

2. Search EDB level IDs locally before calling the API:

```bash
python3 /Users/fanshengxia/.codex/skills/dm-data/scripts/dm_query.py search-edb GDP --limit 20
python3 /Users/fanshengxia/.codex/skills/dm-data/scripts/dm_query.py search-edb 社融 --limit 20
```

3. List supported API aliases:

```bash
python3 /Users/fanshengxia/.codex/skills/dm-data/scripts/dm_query.py list-apis
```

4. Call an API by alias and JSON params:

```bash
python3 /Users/fanshengxia/.codex/skills/dm-data/scripts/dm_query.py call bond_basic_info \
  --data '{"security_id_list":["2500005.IB","232580001.IB"]}' \
  --output /tmp/bond_basic_info.csv
```

## Workflow

1. For EDB/macro requests, first run `search-edb` against `references/edb_levels.csv` to find candidate `edb_level_id` values. Then call `edb_codes` to get `indicator_id`, and finally call `edb_data` for values.
2. For bond, money-market, futures, equity, and calendar requests, choose an alias from `references/dm_api_reference.md` or `list-apis`, then run `call`.
3. Prefer snake_case request fields and instantiate with `pythonic=True`; the SDK converts request keys to camelCase and response keys to snake_case.
4. Save nontrivial results to CSV using `--output`, then inspect the first rows before using them in analysis.
5. If the API returns `return_type=dict` with paginated `list` and `max_offset`, use `--return-type dict`; page manually by passing `offset`.

## Resources

- `scripts/dm_query.py`: executable helper for local EDB dictionary search and live DM API calls.
- `references/dm_api_reference.md`: concise API catalog, parameter constraints, and examples extracted from the local DM PythonAPI manual.
- `references/api_catalog.json`: machine-readable aliases used by the helper script.
- `references/edb_levels.csv`: searchable EDB level hierarchy with 3192 rows.
- `references/edb_levels.xlsx`: original EDB level hierarchy workbook.
- `assets/vendor/dm_quant_api_client-0.2.2-py3-none-any.whl`: local SDK wheel. The helper script installs it automatically if `dm_quant_api_client` is missing.

## Important Rules

- Do not hard-code credentials in scripts or outputs. Use `INNO_APP_KEY` and `INNO_SM4_KEY`, or pass temporary keys only when the user explicitly asks.
- Do not query wide date ranges blindly. Follow the manual limits in the reference: most intraday APIs have narrow windows; EDB values depend on frequency; trade calendar is at most 2 years.
- For production-looking outputs, keep numeric formatting to 2 decimals unless the downstream task requires raw precision.
- If live calls fail, report the exact SDK/API error. Common causes are missing credentials, HTTP non-200, decryption failure, no subscription package, quota exhaustion, or rate limiting.
