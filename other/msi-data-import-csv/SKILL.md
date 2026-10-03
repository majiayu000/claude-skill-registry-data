---
name: msi-data-import-csv
description: Use when you have MSI intensity data exported from MSiReader or SCiLS
  software as a plain-text CSV file (with peaks as columns and pixels/spots as rows),
  and you need to import it into R to perform pairwise mass difference calculations
  and adduct identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - mass2adduct
  - R
  - MSiReader
  - SCiLS
  - Cardinal
  - msimunging.pl
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS
  data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into
  memory during an R session.
- corrPairsMSI(d,d.diff.annot)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct_cq
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04720
  all_source_dois:
  - 10.1021/acs.analchem.0c04720
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Import MSI intensity data from CSV into matrix format

## Summary

Load mass spectrometry imaging (MSI) intensity data exported from MSiReader or SCiLS as plain-text CSV files into an R data.frame object using the msimat() function, preparing it for downstream adduct analysis. This is the essential entry point for all mass2adduct workflows.

## When to use

You have MSI intensity data exported from MSiReader or SCiLS software as a plain-text CSV file (with peaks as columns and pixels/spots as rows), and you need to import it into R to perform pairwise mass difference calculations and adduct identification. Use this when you have tabular intensity matrices where each mass peak is a separate column and each imaging pixel/spot is a separate row.

## When NOT to use

- Your data is already in Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment format—use cardinal2msimat() conversion function instead.
- You only have a simple list of mass values (no intensity or pixel information)—use scan() to load as numeric vector directly.
- Your CSV file is >40 GB and your available RAM is <40 GB—pre-convert to triplet format using msimunging.pl first.
- Data is in binary or proprietary formats (imzML, Analyze, etc.)—export to CSV from the originating software or use Cardinal's readImzML() first.

## Inputs

- Plain-text CSV file exported from MSiReader or SCiLS
- String: file path to CSV
- String: field separator (e.g., ';' or ',')

## Outputs

- msimat object (subclass of data.frame with intensity matrix)
- Numeric matrix: rows=imaging pixels/spots, columns=mass peaks

## How to apply

Call msimat() with the file path to your CSV file and specify the correct field separator (e.g., sep=';' or sep=','). The function reads the CSV into a data.frame and returns an object of class 'msimat'. Before importing very large files (several GB), consider using the msimunging.pl Perl script to convert to triplet format to avoid memory exhaustion. After import, verify the object with class(), print(), and plot() to confirm the mass spectrum shape is as expected—plotting should show total intensities per peak consistent with your instrument's performance.

## Related tools

- **mass2adduct** (R package containing msimat() function for CSV import and entire downstream adduct analysis pipeline) — https://github.com/kbseah/mass2adduct
- **MSiReader** (MSI software that exports intensity data as plain-text CSV for input to msimat())
- **SCiLS** (MSI software that exports intensity data as plain-text CSV for input to msimat())
- **Cardinal** (Alternative R package for MSI processing; data can be converted to msimat format via cardinal2msimat() after peak binning) — http://cardinalmsi.org/
- **msimunging.pl** (Perl script to convert large CSV files to triplet format before R import to reduce memory footprint) — https://github.com/kbseah/mass2adduct

## Examples

```
d <- msimat("msi.csv", sep=";")
class(d)
plot(d)
```

## Evaluation signals

- Returned object has class 'msimat' and inherits from data.frame; verified with class(d)
- plot(d) produces a sensible mass spectrum with peaks at expected m/z values and intensity distribution consistent with instrument sensitivity
- print(d) outputs a summary showing correct number of pixels/spots (rows) and mass peaks (columns)
- Object can be successfully passed to massdiff() function without error; massdiff(d) returns a massdiff-class object with three columns (parent A, adduct B, mass difference)
- No NA or infinite values in intensity matrix; spot-check with summary(d) shows numeric ranges appropriate for MS intensities

## Limitations

- CSV files must be exported from standard MSI software (MSiReader, SCiLS) as plain-text delimited tables; other formats (binary, proprietary) require prior conversion.
- Very large CSV files (several GB) may exceed available RAM; msimunging.pl triplet format conversion is recommended but requires additional Perl setup and runs serially.
- The function assumes a rectangular matrix structure (all rows same length); corrupted or irregularly formatted CSV files will fail or produce silent errors.
- Cardinal objects must be pre-processed with peakBin() function before conversion; raw Cardinal imzML imports cannot be directly converted to msimat.
- No built-in error handling or validation for separator character mismatch; wrong sep= parameter will produce truncated or malformed columns without clear diagnostic.

## Evidence

- [readme] MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format): "MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format)"
- [readme] d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";"): "d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";")"
- [readme] class(d) # "msimat" print(d) # Report a summary plot(d) # Mass spectrum of total intensities per peak: "class(d) # "msimat" print(d) # Report a summary plot(d) # Mass spectrum of total intensities per peak"
- [other] If the data matrix is very large, it may need to be reformatted to be loaded into memory during an R session: "If the data matrix is very large, it may need to be reformatted to be loaded into memory during an R session"
- [readme] Plain-text CSV files of MSI data exported by software such as SCILS or MSIreader can be large, on the order of several Gb: "Plain-text CSV files of MSI data exported by software such as SCILS or MSIreader can be large, on the order of several Gb"
- [readme] Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format: "Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format"
- [readme] The data must first be pre-processed, with peaks already binned with the `peakBin()` function from Cardinal: "The data must first be pre-processed, with peaks already binned with the `peakBin()` function from Cardinal"
