---
name: msp-file-format-parsing
description: Use when you have acquired EI or MS2 library files in MSP format (e.g., from NIST via Lib2NIST export, RIKEN, MoNA, SWGDRUG, or GNPS) and need to read them into R to assign SMILES, retention indices, or combine multiple libraries into a single consolidated MSP file for MS-DIAL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS-DIAL
  - MoNA
  - RIKEN
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
- you can transformed it into a msp file by *Lib2NIST*
- MS-DIAL friendly msp file
- both positive and negative modes are in a single file as well. Therefore, we need to separated the polarity
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
schema_version: 0.2.0
---

# msp-file-format-parsing

## Summary

Parse mass spectral library files in MSP (NIST text) format into structured R objects for downstream enrichment, validation, and conversion. This skill transforms human-readable MSP text files into machine-manipulable library objects that preserve spectral metadata, molecular structure information, and retention indices.

## When to use

You have acquired EI or MS2 library files in MSP format (e.g., from NIST via Lib2NIST export, RIKEN, MoNA, SWGDRUG, or GNPS) and need to read them into R to assign SMILES, retention indices, or combine multiple libraries into a single consolidated MSP file for MS-DIAL. Use this skill as the first step in any mspcompiler workflow before structural annotation or RI assignment.

## When NOT to use

- Input file is in MGF format (e.g., GNPS All_GNPS.mgf)—use read_lib() with format='mgf' instead
- Input is already a parsed R library object from a prior read_lib() call—no re-parsing needed
- You need to read vendor-specific binary library formats (e.g. Agilent .L files)—use Lib2NIST to convert to MSP first

## Inputs

- MSP file (NIST text format) exported from Lib2NIST, RIKEN, MoNA, SWGDRUG, or GNPS
- Folder path containing multiple MSP files (for read_multilibs)
- type parameter: 'EI' or 'MS2'
- remove_ri parameter: logical (default TRUE, set FALSE for RIKEN to retain existing Kovats RI)

## Outputs

- Parsed library object: R list of spectral records with fields: Name, Synon, DB#, InChIKey, SMILES (if present), Precursor_type, Spectrum (peak list), and RI (if retained)
- Merged library object (when using read_multilibs)

## How to apply

Load the mspcompiler package and call read_lib() with the path to the MSP file and specify type='EI' or type='MS2' depending on the ionization mode. For RIKEN libraries that already contain Kovats RI, set remove_ri=FALSE to preserve existing RI values; otherwise the function will strip RI fields. If you are processing multiple MSP files from the same source folder (e.g., an in-house library with one file per standard batch), use read_multilibs() instead, passing only the folder path—this function automatically discovers and merges all MSP files in that directory. For most sources (NIST, SWGDRUG, MoNA), the parsed library object will lack SMILES or have SMILES in non-standard fields (e.g., MoNA stores SMILES in Comment); subsequent steps will reorganize or assign these. The resulting R object is a library list structure suitable for assign_smiles(), assign_ri(), and combine operations.

## Related tools

- **mspcompiler** (R package providing read_lib() and read_multilibs() functions for MSP parsing and library assembly) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Pre-processing tool to export NIST and SWGDRUG binary library formats to MSP text + MOL folder structure for input to read_lib()) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **R** (Runtime environment for executing read_lib() and read_multilibs() calls)
- **MS-DIAL** (Downstream GC-MS/LC-MS analysis platform that consumes the output MSP files for library matching and annotation) — http://prime.psc.riken.jp/compms/msdial/main.html#MSP

## Examples

```
nist_ei <- read_lib("D:/MS_libraries/NIST.MSP", type = "EI")
riken_ei <- read_lib("D:/MS_libraries/GCMS DB-Public-KovatsRI-VS3.msp", type = "EI", remove_ri = FALSE)
in_house <- read_multilibs("D:/MS_libraries/in_house")
```

## Evaluation signals

- Parsed library object is non-NULL and contains > 0 spectral records with Name, Spectrum fields populated
- All spectral peaks in the Spectrum field are numeric (mass/intensity pairs) and match the Num Peaks declaration
- For EI libraries, Precursor_type field is absent or consistent; for MS2, Precursor_type is present with ionization mode (e.g., [M+H]+)
- When remove_ri=FALSE, RI field is preserved in output; when remove_ri=TRUE (default), RI field is absent
- For read_multilibs on a folder, total record count equals sum of record counts from all constituent MSP files (no loss or duplication)

## Limitations

- read_lib() requires exact type specification ('EI' or 'MS2'); ambiguous formats may fail to parse correctly
- MGF-format libraries (GNPS) cannot be parsed with read_lib() at type='EI' or type='MS2'—require format='mgf' and separate handling via complete_mgf() and separate_polarity()
- SMILES and RI fields are often missing or malformed after initial parsing; subsequent assign_smiles() and assign_ri() steps are required before library is usable for MS-DIAL matching
- read_multilibs() discovers only MSP files in the specified folder; nested subdirectories are not recursively scanned
- Very large MSP files (hundreds of MB) may consume significant RAM; the article recommends parallel processing via plan(multisession()) for time-consuming enrichment steps that follow parsing

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS"
- [other] Read the msp file into R using read_lib() function: "Read the msp file into R. read_lib()"
- [readme] Once you have the *.MSP file (normally hundreds megabytes) and the correspondent *.MOL folder (hundreds thousands .MOL files inside the folder) exported, you can use the following code to add SMILES and Retention Index (RI).: "Once you have the *.MSP file (normally hundreds megabytes) and the correspondent *.MOL folder (hundreds thousands .MOL files inside the folder) exported"
- [readme] As it contains Kovats RI, we can set remove_ri to FALSE to keep original RI in this file.: "As it contains Kovats RI, we can set remove_ri to FALSE to keep original RI"
- [readme] When you have multiple libraries to be read in, for instance if you are building your in-house library and you have one msp file for each batch of standards, then you will have many msp files to combine. The read_multilibs function give you an easy way to read all of them at once.: "The read_multilibs function give you an easy way to read all of them at once. In this case, what you need to input is the folder that contain all these msp files"
