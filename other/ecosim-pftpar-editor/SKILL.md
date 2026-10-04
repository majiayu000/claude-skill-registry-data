---
name: ecosim-pftpar-editor
description: Edit EcoSIM PFT-parameter NetCDF files such as ecosim_pftpar_20260303.nc with the ParEditor class from applications/notebooks/scripts/ParamEditor.py. Use when asked to modify, scale, copy, compare, or delete PFT parameter records for a plant functional type (six-character pfts code such as gr3s43 or ndlf34), update microbe parameter NetCDF values, or maintain the JSONL change log that records past parameter changes. Never modify plant_trait.*.desc files; they are read-only references.
---

# EcoSIM PFT Parameter Editor (ParamEditor.py)

Use this skill to edit EcoSIM `ecosim_pftpar_*.nc` PFT-parameter NetCDF files
with the bundled `ParEditor` class. The canonical tool is
`applications/notebooks/scripts/ParamEditor.py`; treat it as the source of
truth. Do not reimplement NetCDF editing when this skill applies.

## File boundary

Treat every `plant_trait.*.desc` file as read-only, including when the request is
phrased as editing plant trait parameters. Use a `.desc` file only for inspection
or validation. Apply requested parameter changes to the corresponding
`ecosim_pftpar_*.nc` file with `ParamEditor.py`. Never patch, overwrite, or emit a
replacement `.desc` file.

## Locate the target file

1. PFT-parameter NetCDF files usually live in EcoSIM run folders, for example
   `~/work/github/ecosim_workspace/<case>/input_data/ecosim_pftpar_YYYYMMDD.nc`.
   Search the user-supplied run folder first, then `ecosim_workspace/*/input_data/`,
   then the repository (`data/`, `templates/`).
2. If the user gives only a date such as `20260303`, match
   `ecosim_pftpar_<date>.nc`. If several run folders contain it, ask which case
   to edit, or edit all cases only when explicitly requested.
3. Templates exist as `.cdl` text; do not edit `.cdl` files with this skill.

## Environment and import pattern

Use the repository NetCDF-capable environment and import `ParamEditor` as a
package module (it does `from . import stringTools` internally, so it must be
imported as `scripts.ParamEditor` with `applications/notebooks` on `sys.path`):

```python
# run with .venv-cmip6/bin/python from the repo root, or set cwd accordingly
import sys
sys.path.insert(0, 'applications/notebooks')
from scripts.ParamEditor import ParEditor
```

If `.venv-cmip6/bin/python` is unavailable, use any Python that can
`import netCDF4`.

## Core API

| Method | Purpose |
| --- | --- |
| `ParEditor(pftparfile=path)` | Bind the editor to a PFT-parameter file. Optional `micparfile=` binds a microbe-parameter file. The change-log stem is the first dot-token of the file basename (for `ecosim_pftpar_20260303.nc` it is `ecosim_pftpar_20260303`); records are appended to `<stem>.jsonl` **in the current working directory**. |
| `reset(sure=True)` | Delete the recorded `.jsonl` change-log files. Call only when the user wants to clear history. |
| `PlantParamModify(pft, pars, iscale=False, verbose=True)` | Set parameters for one PFT. `pars` is a dict `{varname: value}` using exact NetCDF variable names such as `VCMX`, `ETMX`, `RRAD1M`. With `iscale=False` the value replaces the current value; with `iscale=True` the value multiplies the current value (a factor of 1.0 leaves it unchanged). |
| `CopyPlantPft(pft_from, pft_to)` | Copy all parameters from one PFT to another. If `pft_to` does not exist it is appended to the unlimited `npfts` dimension as a new record. |
| `PlantParCompare(pft1, pft2)` | Print parameters that differ between two PFTs. Use before copying to confirm the archetype. |
| `delete_pft_records(input_file, output_file, names_to_delete)` | Write a **new** NetCDF with the listed `pfts` codes removed; the input file is not modified. |
| `MicrobeParamModify(pars, iscale=False, verbose=True)` | Modify variables in the microbe-parameter file for all records (`variable[:]`). |

## Workflow

1. List available PFT codes and locate the record before editing:

   ```python
   from netCDF4 import Dataset

   def pft_codes(pftparfile):
       with Dataset(pftparfile) as nc:
           return ["".join(c.decode('utf-8') if isinstance(c, bytes) else c
                           for c in row).strip()
                   for row in nc.variables['pfts'][:].filled(" ")]
   print(pft_codes(pftparfile))
   ```

   Use the exact six-character code. If the user names a plant, map it to a
   `pfts` code and confirm the match (for example, ponderosa pine as `ndlf34`).

2. Back up before any in-place edit, because `PlantParamModify` and
   `CopyPlantPft` open the file in `r+` mode and save immediately:

   ```bash
   mkdir -p result/pftpar_editor
   cp /path/to/ecosim_pftpar_20260303.nc result/pftpar_editor/ecosim_pftpar_20260303_backup_$(date +%Y%m%d_%H%M%S).nc
   ```

3. Read the pre-edit values, apply changes, and read back the post-edit values
   in one session:

   ```python
   from netCDF4 import Dataset

   parEditor = ParEditor(pftparfile=pftparfile)
   pft = 'ndlf34'

   def pft_index(pftparfile, pft):
       with Dataset(pftparfile) as nc:
           codes = ["".join(c.decode('utf-8') if isinstance(c, bytes) else c
                            for c in row).strip()
                    for row in nc.variables['pfts'][:].filled(" ")]
           return codes.index(pft)

   def show(names):
       with Dataset(pftparfile) as nc:
           i = pft_index(pftparfile, pft)
           for n in names:
               print(n, nc.variables[n][i])

   show(['VCMX', 'ETMX', 'RSRR'])  # before

   # absolute replacement
   parEditor.PlantParamModify(pft, {'VCMX': 35.0, 'ETMX': 500.0}, iscale=False, verbose=True)

   # multiplicative scaling (factor)
   parEditor.PlantParamModify(pft, {'RSRR': 1.10}, iscale=True, verbose=True)

   show(['VCMX', 'ETMX', 'RSRR'])  # after
   ```

4. To create a new PFT from an archetype, compare first, then copy and adjust:

   ```python
   parEditor.PlantParCompare('ndlf34', 'ndlf32')
   parEditor.CopyPlantPft('ndlf34', 'ndlf36')
   parEditor.PlantParamModify('ndlf36', {'VCMX': 40.0}, verbose=True)
   ```

5. To remove PFTs, always write to a new file (default under `result/`), never
   overwrite the run-folder input in place:

   ```python
   parEditor.delete_pft_records(input_file, 'result/pftpar_editor/ecosim_pftpar_pruned.nc',
                                ['gr3s32', 'maiz31'])
   ```

6. Verify and report:
   - Re-open the file and print the edited variables for the target PFT.
   - Report the change-log path (for example `./ecosim_pftpar_20260303.jsonl`
     in the working directory) and its latest records.
   - Report the backup file path under `result/pftpar_editor/`.
   - Warn that other run folders keep their own copy of
     `ecosim_pftpar_<date>.nc`; propagate the same edit to other cases only on
     request.

## Contract and cautions

- Never fabricate variable names: read them from the file first. A wrong name
  raises `KeyError` from `nc_file.variables[parnm]`; stop and list the
  available variables instead of guessing.
- `PlantParamModify` writes values with broadcasting; scalars are safe for
  `npfts`-leading variables.
- The `pfts` variable is a character array `(npfts, nchars1=10)`; strip
  padding when matching codes.
- Keep the JSONL change log; it is the audit trail of every modify call
  (`{'pft':..., 'parvarnames':[...], 'parvals':[...]}`).
- Only call `reset()` when the user explicitly asks to clear history, because
  it deletes the `.jsonl` files.
- Do not use regex or text editing on NetCDF; edit variables directly through
  `netCDF4` as ParamEditor.py does.
