---
name: ecosim-pftpar-extractor
description: Extract one EcoSIM PFT parameter record from a PFT-parameter NetCDF file into a standalone NetCDF. Use when Codex needs to isolate all parameters for a given EcoSIM six-character PFT code such as ndlf34, or a four-character pfts_short value plus Koppen climate code, while preserving all non-PFT-specific variables such as pfts_short, pfts_long, and Koppen metadata.
---

# EcoSIM PFT Parameter Extractor

Use this skill to create a single-PFT parameter NetCDF from an EcoSIM
`ecosim_pftpar_*.nc` file.

## Workflow

1. Identify the source PFT parameter NetCDF from the user request. If omitted,
   search under `data/`, then under the repo, then ask for the file.
2. Identify the target PFT:
   - Prefer an exact six-character `pfts` code such as `ndlf34`.
   - If only a four-character `pfts_short` code such as `ndlf` is supplied,
     require a two-digit `--koppen-code` unless exactly one matching `pfts`
     record exists.
3. Run the bundled extractor with the repo NetCDF-capable Python environment:

   ```bash
   .venv-cmip6/bin/python .agents/skills/ecosim-pftpar-extractor/scripts/extract_pftpar_record.py \
     --input /path/to/ecosim_pftpar_YYYYMMDD.nc \
     --pft ndlf34 \
     --output result/pftpar_extracts/ndlf34.nc
   ```

4. Verify the output summary reports `npfts=1`, the selected `pfts` code, and
   preserved non-PFT metadata dimensions such as `npft` and `nkopenclms`.

## Extraction Contract

- Slice every variable with dimension `npfts` to the selected record only.
- Preserve all variables without `npfts` unchanged, including `pfts_short`,
  `pfts_long`, `koppen_clim_no`, `koppen_clim_short`, and
  `koppen_clim_long`.
- Preserve variable attributes, global attributes, fill values, and dimension
  names. Keep the output `npfts` dimension length at one record.
- Write the default output basename as `<selected-pft>.nc`; for example,
  `ndlf34` becomes `ndlf34.nc`.

## Notes

- Do not use regex or text parsing for NetCDF extraction when `netCDF4` is
  available; preserve numeric dtypes and metadata directly.
- If `.venv-cmip6/bin/python` is unavailable, use any Python environment with
  `netCDF4` installed. The base desktop Python may not include NetCDF support.
- If the requested PFT is missing, list exact available codes with the same
  four-character prefix and do not create an output file.
