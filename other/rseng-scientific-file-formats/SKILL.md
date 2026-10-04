---
name: rseng-scientific-file-formats
description: >-
  Covers choosing and handling scientific data formats in code: HDF5 and
  NetCDF for array data, CF conventions and standard metadata, Parquet for
  tabular data, domain standards (NeXus and similar), self-describing files,
  chunking and compression choices, and migrating away from fragile formats
  like pickles and ad-hoc binaries. Use when the user chooses a file format
  for research data, reads or writes HDF5/NetCDF/Parquet/zarr-style stores,
  asks about chunking, compression or metadata embedding, or ships data in
  CSV, pickle, MAT or homegrown binary formats that deserve scrutiny. (The
  surrounding data practice - versioning, deposit, licensing, documentation -
  is rseng-data-management.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Scientific file formats in code

File formats are decade-scale decisions: data outlives the code that
wrote it, and a format choice made in a script today determines
whether a dataset is readable, FAIR and efficient in ten years. The
guiding principle is SELF-DESCRIBING data: a file a stranger can open
and understand - variables named, units attached, provenance noted -
without emailing the author (rseng-data-management owns the
surrounding practice; this skill owns the format engineering).

## Choosing a format

- Multidimensional arrays (grids, time series stacks, images,
  simulation output): NetCDF (atmosphere/ocean/climate lingua
  franca, built on HDF5) or HDF5 directly; both hierarchical,
  self-describing, partial-read capable and language-portable.
- Tabular data at scale: Parquet - columnar, typed, compressed,
  schema-carrying; the upgrade path from CSV when files grow or
  types matter.
- Small human-facing tables and interchange: CSV is fine - WITH a
  stated dialect (delimiter, encoding, quoting) and a data
  dictionary alongside (rseng-data-management).
- Domain standards first: if the field has one (NeXus for photon/
  neutron science, CF-governed NetCDF in climate, community formats
  generally), emitting it beats inventing anything - it is what
  colleagues' tools already read (rseng-fair-software's I).

Formats to migrate away from when encountered: pickles as storage
(unreadable outside Python, version-fragile, unsafe to load from
strangers), unversioned homegrown binaries, MAT files as long-term
archives, spreadsheets as databases. Flag them, explain the failure
mode, offer the migration.

## Metadata: the self-describing part

- Attach units, long names and fill values to every variable at
  write time - in code, not in a README written later. CF
  conventions define exactly how for NetCDF and are checkable with
  automated compliance checkers; run one in CI when a project's
  outputs claim CF compliance (rseng-ci-cd).
- Record provenance in file attributes: producing software and
  version, input identifiers, creation time, configuration
  hash - the file should testify about its own origin.
- Keep schemas versioned: when a project's file layout evolves, add
  a format-version attribute, and keep readers for old versions or
  a migration script (rseng-legacy-code discipline applied to data).

## Performance engineering: chunking and compression

- Chunk to match access patterns: time-slice reads want chunks along
  time; map reads want spatial chunks. Wrong chunking makes reads
  orders of magnitude slower on large stores - decide from how the
  data will be READ, not written.
- Compression is usually free performance for scientific data
  (gzip/zstd-class codecs); test level trade-offs on real data, and
  prefer bit-shuffle-style filters for floats where available.
- For cloud or parallel access, chunked stores (HDF5/NetCDF-4 and
  their cloud-optimized descendants in the Pangeo ecosystem) enable
  partial and concurrent reads - the pattern behind scalable
  analysis (rseng-big-data-processing).

## Testing format code

Round-trip tests (write, read back, compare with tolerances -
rseng-numerical-accuracy), a checked-in small golden file to catch
accidental format changes, and reading files produced by OTHER tools
in the ecosystem as compatibility tests (rseng-testing).

## Working with this skill

This skill is source-independent: its authority is the format
specifications and community conventions linked below.

Learn more (verified):
  - https://cfconventions.org - CF metadata conventions
  - https://www.unidata.ucar.edu/software/netcdf/ - NetCDF
  - https://www.hdfgroup.org/solutions/hdf5/ - HDF5
  - https://parquet.apache.org - Apache Parquet
  - https://www.nexusformat.org - NeXus domain format
  - https://pangeo.io - Pangeo community (cloud-optimized scientific
    data practice)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-big-data-processing - chunked stores enable scalable reads
- rseng-data-management - surrounding dataset practice and deposit
- rseng-fair-software - domain standards serve interoperability
- rseng-legacy-code - schema versioning and old-format readers
- rseng-numerical-accuracy - round-trip tests need float tolerances
- rseng-testing - golden-file and compatibility tests

<!-- related-skills:end -->
