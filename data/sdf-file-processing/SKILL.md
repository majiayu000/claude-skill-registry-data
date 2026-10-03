---
name: sdf-file-processing
description: Use when you have molecular structures (from databases, design tools,
  or literature) that need to be analyzed for CYP reactivity or metabolic properties,
  and you must convert them into a format compatible with the CypReact command-line
  tool.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2275
  tools:
  - CypReact
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  dedup_kept_from: coll_cypreact_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sdf-file-processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and format molecular structure data as .sdf (structure data format) files for input to computational chemistry tools like CypReact. SDF files are the standard interchange format for encoding 2D/3D molecular geometries and properties.

## When to use

You have molecular structures (from databases, design tools, or literature) that need to be analyzed for CYP reactivity or metabolic properties, and you must convert them into a format compatible with the CypReact command-line tool. Use this skill when your source data is in a different format (e.g., SMILES strings, CSV) or needs validation before submission to CypReact.

## When NOT to use

- Input is already a validated .sdf file ready for CypReact — proceed directly to CypReact invocation.
- Your molecules are already embedded in a database or molecular management system that can export directly to .sdf format.
- You intend to analyze only a single molecule and prefer SMILES string input over batch file processing.

## Inputs

- molecular structure files in .sdf format (structure data format with 2D or 3D coordinates)
- alternatively, .csv files containing SMILES strings separated by commas (to be converted to .sdf)

## Outputs

- .sdf file formatted and validated for input to CypReact
- confirmation that the file is readable and contains valid molecular data

## How to apply

Obtain or generate .sdf files containing molecular structures with 2D or 3D coordinates. If you have a CSV file with SMILES strings, convert each row to an SDF entry using chemical informatics libraries (e.g., RDKit). Ensure the .sdf file is well-formed and contains valid molecular geometry. Verify that the file path is correctly specified in the CypReact command-line invocation (e.g., java -jar cypreact.jar [bundle_path] [input.sdf] [output.sdf] [isoform_id]). The .sdf format allows batch processing of multiple molecules in a single run, making it more efficient than processing individual SMILES strings.

## Related tools

- **CypReact** (Command-line tool that consumes .sdf files to predict CYP metabolism and reactivity; .sdf is the primary input format.) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
java -jar cypreact.jar /path/to/CypReactBundle /path/to/molecules.sdf /path/to/results.sdf 1A2
```

## Evaluation signals

- The .sdf file is generated without write errors and is readable by a text editor or molecular visualization tool.
- Each molecule in the .sdf file has valid bond and atom connectivity (no broken valence rules or orphaned atoms).
- The file is successfully parsed by CypReact without format errors in the stderr/stdout output.
- The output result file is generated and contains predictions for all molecules in the input .sdf.
- Spot-check: manually verify that a known molecule (e.g., a positive control compound) appears in the output results.

## Limitations

- SDF files are human-readable but verbose; large batches (>10,000 molecules) may consume significant disk space.
- 3D coordinates must be pre-generated externally; CypReact does not perform conformer generation.
- Some specialized molecular properties (e.g., charge state, stereoisomers) require careful SDF encoding; malformed entries will cause CypReact to skip them silently.
- No changelog or version tracking is documented for the CypReact tool, making it difficult to assess breaking changes between releases.

## Evidence

- [intro] input_format: "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] invocation_example: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
- [intro] output_format: "The user can output a .sdf file or a .csv file."
- [intro] workflow_context: "To run the CypReact tool, the user should use command in the terminal as: ->java -jar "PathOfCypReactBundle""
