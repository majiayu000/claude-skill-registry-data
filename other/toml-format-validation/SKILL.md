---
name: toml-format-validation
description: Use when you are setting up a new LipoCLEAN analysis for MS-DIAL output and need to create a configuration file tailored to your MS-DIAL version (4 or 5).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  tools:
  - LipoCLEAN
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.4c04040
  title: lipoclean
evidence_spans:
- LipoCLEAN is a command line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipoclean
    doi: 10.1021/acs.analchem.4c04040
    title: lipoclean
  dedup_kept_from: coll_lipoclean
schema_version: 0.2.0
---

# Generate and validate TOML configuration files for MS-DIAL version-specific pipelines

## Summary

Generate default TOML-formatted options files for MS-DIAL 4 or 5 using LipoCLEAN's `--print` argument, then validate the file structure and content before editing for downstream lipid quality filtering. This ensures version-specific configuration keys and syntax are correct before customization.

## When to use

You are setting up a new LipoCLEAN analysis for MS-DIAL output and need to create a configuration file tailored to your MS-DIAL version (4 or 5). The tool will not accept mismatched or malformed options files, so generating a validated default is essential before editing parameters like data paths or filtering thresholds.

## When NOT to use

- You have an existing, manually validated options.txt file and only need to customize data paths — regenerating the default will overwrite your edits.
- Your MS-DIAL version is not 4 or 5, as LipoCLEAN provides default options only for these versions and models are not portable across versions.

## Inputs

- MS-DIAL version identifier (4 or 5)
- LipoCLEAN command-line interface

## Outputs

- TOML-formatted options.txt file with version-specific default configuration keys
- Validation confirmation (presence of expected keys, correct syntax)

## How to apply

Execute LipoCLEAN with the `--print MSD4` or `--print MSD5` argument (depending on your MS-DIAL version) to generate a default `options.txt` file in TOML format. Verify that the file is created in the output directory and parse it to confirm the presence of all expected configuration keys required for the analysis (e.g., input file paths, model selection, filtering parameters). After validation, edit the file to customize analysis-specific settings such as the location of MS-DIAL export files and desired output directory, keeping the TOML syntax intact.

## Related tools

- **LipoCLEAN** (Command-line tool that generates and validates TOML configuration files via --print MSD4/MSD5 arguments) — https://github.com/stavis1/LipoCLEAN
- **MS-DIAL** (Upstream data source; generates alignment results that LipoCLEAN processes; version must match the configuration file)

## Examples

```
LipoCLEAN.exe --print MSD5
```

## Evaluation signals

- An options.txt file is created in the output directory after running the --print command
- The file is valid TOML syntax (parseable by a TOML parser without errors)
- All expected version-specific configuration keys are present (e.g., model path, input/output directories, filtering parameters)
- The options file can be passed to LipoCLEAN via the `--options` flag without triggering validation errors
- After user edits (e.g., updating data paths), the file remains valid TOML and LipoCLEAN processes it successfully

## Limitations

- Default options files are specific to MS-DIAL versions 4 and 5; other versions are not supported.
- Models trained on one MS-DIAL version's data are incompatible with the other version; the options file and model must match the target MS-DIAL version.
- Generated default file must be edited manually to point to actual MS-DIAL export files; the generic default will not run a meaningful analysis without customization.

## Evidence

- [readme] Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively. These will create an `options.txt` file that you can edit.: "Default options files for MS-DIAL 4 and 5 can be obtained using the `--print MSD4` or `--print MSD5` command line arguments, respectively. These will create an `options.txt` file that you can edit."
- [readme] All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file.: "All options, including the location of MS-DIAL export files to analyze, are given to the tool in a TOML formatted text file."
- [readme] Both the options file and the model are specific to a version of MS-DIAL. We provide separate default options files for each version that can be obtained with the `--print MSD4` and `--print MSD5` command line arguments, respectively.: "Both the options file and the model are specific to a version of MS-DIAL. We provide separate default options files for each version that can be obtained with the `--print MSD4` and `--print MSD5`"
- [intro] Configuration is provided via TOML formatted text files with default options available for MS-DIAL versions 4 and 5: "Configuration is provided via TOML formatted text files with default options available for MS-DIAL versions 4 and 5"
