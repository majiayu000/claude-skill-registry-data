---
name: ms-ms-spectrum-parsing
description: Use when you have raw or preprocessed MS/MS spectra in one of the supported formats (MGF, mzML, mzXML, JSON, MSP, mzXML, pickled matchms objects, or USI) and need to extract peak lists (m/z and intensity pairs) along with metadata (precursor m/z, charge, ionization mode) to feed into MS2Query or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - matchms
  - MZMine
  - RDKit
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
---

# MS/MS Spectrum Parsing

## Summary

Parse MS/MS spectral data from standard formats (MGF, mzML, mzXML, JSON, MSP, USI) into normalized m/z–intensity pairs suitable for library matching and analogue search. This skill is essential for preparing query spectra before applying MS2Query's machine learning-based ranking and candidate retrieval.

## When to use

You have raw or preprocessed MS/MS spectra in one of the supported formats (MGF, mzML, mzXML, JSON, MSP, mzXML, pickled matchms objects, or USI) and need to extract peak lists (m/z and intensity pairs) along with metadata (precursor m/z, charge, ionization mode) to feed into MS2Query or other spectral similarity workflows. Particularly relevant when processing FBMN/MZMine outputs that may contain many MS2 spectra per feature.

## When NOT to use

- Spectra are already in the form of pre-computed embeddings or vectors; parsing is unnecessary.
- Input is a pre-filtered, merged consensus spectrum rather than individual MS/MS records; MS2Query expects separate spectra for ranking.
- Spectral data lacks precursor m/z or ionization mode annotation; MS2Query ranking depends on these metadata fields.

## Inputs

- MGF files (Mascot Generic Format)
- mzML files (mass spectrometry markup language)
- mzXML files
- JSON spectral records
- MSP (NIST MS Search) format files
- USI (Universal Spectrum Identifier) strings
- pickled matchms Spectrum objects

## Outputs

- Parsed Spectrum objects (matchms format) with m/z, intensity, precursor m/z, charge, and ion mode
- Peak lists as m/z–intensity pairs
- Spectral metadata (compound name, SMILES, InChI, InChIKey, retention time, feature ID)

## How to apply

Load spectrum files using matchms or MS2Query's built-in parsers, which handle format detection automatically. Extract the m/z and intensity arrays for each spectrum along with precursor m/z and ionization mode from metadata. If your input contains multiple MS2 spectra per feature (common in FBMN outputs), first apply clustering or feature selection (e.g., via MZMine) to reduce redundancy before parsing. Validate that all spectra have non-empty peak lists and that precursor m/z values and ion modes are annotated; missing metadata will prevent downstream ranking in MS2Query. The parsed spectra become input to MS2Deepscore embedding calculation and the random-forest re-ranking step.

## Related tools

- **matchms** (Core library for parsing, normalizing, and storing MS/MS spectra in memory; used internally by MS2Query to load from MGF, mzML, mzXML, JSON, and MSP formats)
- **MS2Query** (Downstream tool that consumes parsed spectra and applies MS2Deepscore embedding + random forest ranking for library matching) — https://github.com/iomega/ms2query
- **MZMine** (Preprocessing tool for peak picking, feature detection, and clustering of redundant MS/MS spectra before parsing; recommended for FBMN/feature-based workflows) — https://mzmine.github.io/mzmine_documentation/index.html
- **RDKit** (Optional dependency for extracting molecular classes and computing chemical descriptors from SMILES/InChI metadata during library creation)

## Examples

```
from ms2query.ms2library import create_library_object_from_one_dir; from ms2query.run_ms2query import run_complete_folder; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- All spectra have non-empty peak lists with valid m/z (numeric, > 0) and intensity values (numeric, ≥ 0).
- Precursor m/z and ionization mode (positive/negative) are present in metadata for all spectra; no null or missing values.
- Peak lists are sorted by m/z in ascending order and contain no duplicate m/z values.
- Intensity values are normalized (e.g., to relative intensity with max = 100 or max = 1) if required by downstream matching algorithm.
- Metadata fields (compound name, SMILES, InChI, InChIKey, retention time, feature ID) are preserved when available and match the schema expected by MS2Query or the target library format.

## Limitations

- MS2Query does not perform peak picking or spectral denoising; input should be preprocessed to remove noise and cluster redundant spectra per feature.
- Spectra without SMILES, InChI, or InChIKey annotations cannot be included in custom library creation (only library-search mode is available).
- Parser support is limited to the listed formats (MGF, mzML, mzXML, JSON, MSP, USI, pickled matchms); other proprietary formats require conversion.
- Ion mode must be explicitly specified or inferred from metadata; mismatched ion modes between query and library will reduce match quality.

## Evidence

- [readme] Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object: "Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object"
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [other] Parse input query spectra in standard MS/MS format (m/z and intensity pairs).: "Parse input query spectra in standard MS/MS format (m/z and intensity pairs)."
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library.: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library."
- [readme] One reliable method is using MZMine for preprocessing, https://mzmine.github.io/mzmine_documentation/index.html. As input for MS2Query you can use the MGF file of the FBMN output of MZMine: "One reliable method is using MZMine for preprocessing, https://mzmine.github.io/mzmine_documentation/index.html. As input for MS2Query you can use the MGF file of the FBMN output of MZMine"
