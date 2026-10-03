---
name: c-module-integration
description: Use when you have raw mass spectrometry data in mzML or mzXML format
  and need to compress it using a format-agnostic compressor that expects a standardized
  spectral data contract.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mspack
  - msconvert
  - tinyxml2
  - gzip / bsc
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab636
  title: mspack
evidence_spans:
- mspack is a C++ program for lossless and lossy mass spectrometry data compression
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspack_cq
    doi: 10.1093/bioinformatics/btab636
    title: mspack
  dedup_kept_from: coll_mspack_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab636
  all_source_dois:
  - 10.1093/bioinformatics/btab636
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# c++-module-integration

## Summary

Integrate a format-specific adapter layer into a format-agnostic C++ API to enable lossless and lossy compression of mass spectrometry data in heterogeneous file formats (mzML, mzXML). This skill bridges the gap between standardized mass spectrometry schemas and a unified internal data representation.

## When to use

You have raw mass spectrometry data in mzML or mzXML format and need to compress it using a format-agnostic compressor that expects a standardized spectral data contract. The adapter is necessary when the compressor's internal representation differs from the on-disk XML schema, requiring explicit mapping of spectral arrays (m/z and intensity) and metadata.

## When NOT to use

- The input mass spectrometry data is already in the compressor's native internal format or in a non-XML binary format (e.g., NetCDF, HDF5) without conversion via msconvert first.
- The m/z arrays in the source file are not monotonically increasing (a current implementation limitation that will cause incorrect compression behavior).
- The mzXML file uses block-based I/O or 64-bit representation, which is not supported by the current mzXML adapter.
- The spectral arrays are pre-compressed (e.g., with zlib or msnumpress) and have not been decompressed or converted using msconvert.

## Inputs

- mzML file (XML-formatted mass spectrometry data with spectral records containing m/z and intensity arrays)
- mzXML file (XML-formatted mass spectrometry data, precursor to mzML, limited to 32-bit representation)
- C++ source code defining the format-agnostic API interface
- Example mzML/mzXML handler implementations

## Outputs

- Adapter layer (C++ code) mapping mzML/mzXML spectral records to the compressor's internal data representation
- Validated compressed spectra ready for lossless or lossy compression stage
- Decoded mzML/mzXML file (functionally equivalent to input, whitespace-normalized)

## How to apply

First, load and review the format-agnostic API interface (defined in include/mspack.h) to understand the expected spectral data contract—specifically the field names, types, and invariants for m/z and intensity arrays. Second, examine the provided mzXML and mzML handler examples to identify the reader/writer patterns used to parse XML and extract spectral records. Third, implement or instantiate an adapter layer that maps parsed mzML/mzXML spectral records (including raw, uncompressed m/z and intensity arrays) to the compressor's internal representation. Fourth, validate that spectra from both formats parse without schema errors and that m/z arrays are monotonically increasing (a requirement in the current implementation). Finally, confirm that no data loss occurs during the round-trip: compress and decompress a test file, and verify that the output XML is functionally equivalent to the input (allowing for whitespace normalization and SHA1 recalculation).

## Related tools

- **mspack** (C++ program providing the format-agnostic compression API and reference mzML/mzXML adapter implementations; target system for integration) — https://github.com/fhanau/mspack
- **msconvert** (Utility to decompress pre-compressed spectral arrays (zlib, msnumpress) before mspack adapter ingestion)
- **tinyxml2** (C++ XML parsing library used by mspack to read and write mzML/mzXML files)
- **gzip / bsc** (Compression backends available to mspack; gzip is default, bsc improves compression ratio at the cost of speed) — https://github.com/IlyaGrebnov/libbsc

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz
```

## Evaluation signals

- Spectra from both mzML and mzXML formats are successfully parsed by the adapter without schema validation errors or exceptions.
- m/z arrays extracted from source files are monotonically increasing; any violation is logged and prevents compression.
- Round-trip test (compress → decompress) produces an output XML file that is functionally equivalent to the input (diffable after whitespace normalization and SHA1 recalculation).
- Compression ratio and performance metrics (speed, file size reduction) for adapted spectra match or exceed baseline results for native mzML/mzXML compression in mspack examples.
- No data loss in spectral intensity or m/z values when comparing input and decoded output (bit-level equivalence for lossless mode, specified error tolerance for lossy mode).

## Limitations

- Whitespace is not preserved in decoded files due to the XML library; however, this does not cause functional differences as XML is invariant to whitespace.
- The current implementation requires m/z values to be monotonically increasing; files with additional dimensions (e.g., ion mobility) in addition to m/z and intensity may violate this assumption.
- Only raw, uncompressed m/z and intensity arrays are supported; files with zlib or msnumpress compression must first be converted using msconvert.
- mzXML support is limited compared to mzML: mzXML is restricted to 32-bit files and does not support block-based I/O.
- SHA1 checksum tags in XML are recalculated during compression/decompression, so byte-for-byte round-trip equivalence is not guaranteed.

## Evidence

- [other] mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression.: "mspack provides both a format-agnostic API and example implementations for mzXML and mzML formats to adapt spectra for compression"
- [readme] The API is defined in include/mspack.h. Users are encouraged to use the API for advanced usage.: "The API is defined in ```include/mspack.h```. Users are encouraged to use the API for advanced usage"
- [readme] The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert.: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert"
- [readme] The current implementation depends on the mz values being increasing.: "The current implementation depends on the mz values being increasing"
- [readme] Due to the XML library we use, whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace.: "whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant"
- [readme] mzXML is limited to 32-bit files and does not support the block-based I/O feature.: "mzXML is limited to 32-bit files and does not support the block-based I/O feature"
