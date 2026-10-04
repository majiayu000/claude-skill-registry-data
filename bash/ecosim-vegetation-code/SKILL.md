---
name: ecosim-vegetation-code
description: "Map observed site vegetation, species lists, land-cover descriptions, or plant management PFTs to EcoSIM vegetation codes using templates/ecosim_pftpar_20260303.nc.cdl. Use when choosing or validating EcoSIM pft_type values, pfts entries, pfts_short categories, pfts_long plant type meanings, or the combined short-code plus Koppen climate numerical code used by plant management inputs."
---

# EcoSIM Vegetation Code

## Overview

Use this skill to translate real site vegetation into the six-character EcoSIM vegetation/PFT code used in plant management data. The authoritative code scheme is the EcoSIM PFT parameter CDL, especially variables `pfts`, `pfts_short`, `pfts_long`, `koppen_clim_no`, `koppen_clim_short`, and `koppen_clim_long`.

## Workflow

1. Locate the scheme file. Prefer the user's requested CDL; otherwise use `templates/ecosim_pftpar_20260303.nc.cdl` from the EcoSIM workspace. If the file is missing, ask for the current PFT parameter CDL.
2. Identify the site vegetation. Extract growth form, dominant taxa, crop identity, leaf type, life cycle, wetland status, N fixation, and whether the vegetation is C3/C4 or annual/perennial when applicable.
3. Map the vegetation to `pfts_short` using `pfts_long` as the meaning of each short code. Read `references/pft_mapping_reference.md` when the mapping is not obvious.
4. Determine the Koppen numerical code. Use a provided EcoSIM grid/Koppen code if available. If the user provides a Koppen class like `Cfb`, map it through `koppen_clim_short`; if they provide only coordinates or a place name, use project data first and ask before relying on external climate lookup.
5. Compose the candidate code as `<pfts_short><koppen_clim_no>`, such as `ndlf34` or `gr3s62`.
6. Validate the exact six-character code against `pfts`. Never invent a code that is not present in `pfts`; if the exact candidate is missing, report the closest available codes for the selected `pfts_short` and say that adding a PFT parameter record may be required.
7. Return a compact table with site vegetation, selected `pfts_short`, `pfts_long`, Koppen class/number, final EcoSIM code, and any uncertainty.

## Lookup Script

Use `scripts/ecosim_pft_lookup.py` to validate the current CDL rather than copying tables by hand.

Examples from an EcoSIM repository root:

```bash
python3 /path/to/skill/scripts/ecosim_pft_lookup.py --cdl templates/ecosim_pftpar_20260303.nc.cdl --search spruce
python3 /path/to/skill/scripts/ecosim_pft_lookup.py --cdl templates/ecosim_pftpar_20260303.nc.cdl --short ndlf --koppen Csa
python3 /path/to/skill/scripts/ecosim_pft_lookup.py --cdl templates/ecosim_pftpar_20260303.nc.cdl --list-koppen
```

## EcoSIM Input Note

When preparing `pft_type` in plant management input, remember that `PlantInfoMod.F90` reads the PFT string and, when `KoppenClimZone_col > 0`, uses the first four characters of `pft_type` plus the grid's two-digit Koppen climate code. If `KoppenClimZone_col == 0`, the code path preserves the characters provided in `pft_type`. Still validate the final six-character code against `pfts`.

## Mapping Guidance

- Use specific crop codes when the site vegetation is a crop: `maiz`, `rice`, `soyb`, `swhe`, `barl`, `oats`, `alfa`, `clva`, or `clvs`.
- Use tree codes by leaf type and special taxa: broadleaf general `bdlf`, broadleaf wetland `bdlw`, N-fixing broadleaf `bdln`, evergreen needleleaf `ndlf`, deciduous needleleaf `ndld`, Douglas fir `dfir`, jack pine `jpin`, loblolly pine `lpin`, black spruce `bspr`, aspen `tasp`, oak `woak`.
- Use herbaceous codes by functional group: perennial C3 grass `gr3s`, perennial C4 grass `gr4s`, annual C3 grass `gr3a`, sedge `sedg`, brome `brom`, deer grass `dgra`, wild oats `woat`.
- Use lower plant codes directly when observed: lichen `lich`, sphagnum moss `moss`, feather moss variants `mosf` or `fmos`, sphagnum near sedge `smos`.
- For ambiguous shrub/bush descriptions, present candidates rather than forcing one code: `shru`, `bush`, or N-fixing `busn`.
