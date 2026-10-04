---
name: rseng-provenance
description: >-
  Covers capturing and packaging the provenance of software and data: which
  inputs, code versions, parameters, environments and agents produced each
  result, recorded run by run; the W3C PROV model for describing it, RO-Crate
  for packaging research objects with their provenance, embedding provenance
  in file metadata, and data-flow lineage across pipelines. Use when the user
  asks where a result came from or whether it can be traced, wants provenance
  capture, lineage or an RO-Crate, or mentions PROV, research objects or audit
  trails; use PROACTIVELY when a pipeline produces results whose origins must
  be reconstructable long after the run.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Software and data provenance

Provenance answers the question every published number eventually
faces: where did this come from, exactly? The complete answer
names the input data (which version), the code (which commit),
the parameters, the environment, who or what ran it, and when -
for every derivation step from raw data to figure. This pack
already records provenance in layers (seeds and configs in
rseng-reproducibility, environment lockfiles, AI contributions in
rseng-ai-declaration, file-level origin attributes in
rseng-scientific-file-formats); this skill makes the capture
systematic, standard and packaged.

## Capture at run time, not from memory

Provenance reconstructed after the fact is testimony; provenance
captured at run time is evidence. Instrument the pipeline so
every run writes its own record:

- Per run, record automatically: input paths WITH checksums or
  dataset versions (rseng-data-management), the code identity
  (commit hash, dirty-tree flag), the resolved configuration
  (the actual parameters, not the defaults file), the
  environment (lockfile hash or container digest), seeds, start/
  end times, and the executing agent - human, scheduler or AI
  (rseng-ai-declaration's runtime counterpart). For the code side,
  lean on git's own metadata rather than restating it: authorship
  is the commit author/committer fields and trailers, and a SIGNED
  release tag is a cryptographic provenance anchor
  (rseng-version-control-review) - reference the tag, do not copy
  names and dates into the manifest by hand.
- Write the record NEXT TO the outputs (a run manifest per
  results directory - JSON or YAML), so results and their origin
  travel together; a results file without its manifest is an
  orphan.
- Workflow engines do much of this for free: their run logs and
  hashes are provenance capture (rseng-workflows); the manifest
  distills what the engine knows into what a stranger can read.
- Chain the steps: each derived artifact's record names its
  direct inputs, so lineage from figure back to raw data is a
  walk, not an investigation - the data-flow diagram
  (rseng-data-management) is this chain drawn once.

## Speak the standard: W3C PROV

PROV is the vocabulary that makes provenance interoperable -
three concepts carry almost everything: Entities (data, files,
results), Activities (runs, transformations) and Agents (people,
software, organizations), linked by relations like wasGeneratedBy,
used, wasDerivedFrom and wasAttributedTo. Use the model even in
plain-JSON manifests (name fields after it), and emit PROV-O
(the RDF/JSON-LD form) when tools or repositories consume it -
handwritten triples are rarely needed; the mapping from a good
run manifest is mechanical.

## Package it: RO-Crate

RO-Crate packages a research object - data, code, workflow,
results AND their provenance - as a directory with one
ro-crate-metadata.json (schema.org-based JSON-LD, human-editable):

- Use it when results ship as a unit: replication packages
  (rseng-reproducibility's compendium gains machine-readable
  structure), workflow deposits (WorkflowHub speaks RO-Crate
  natively), archive deposits (rseng-archiving - a crate is
  exactly what a Zenodo deposit wants to be).
- The crate names each file's role (dataset, software, result),
  its origins (wasDerivedFrom chains), licenses per part
  (rseng-licensing) and identifiers (DOIs, ORCIDs -
  rseng-citation-metadata); profiles exist for common shapes
  (workflow runs, datasets).
- Start minimal - a crate with root metadata beats no crate; add
  detail where reuse demands it (rseng-fair-software's
  proportionality).

## Provenance hygiene across the pack

- Embedded beats adjacent where formats allow: self-describing
  files carry their own origin attributes
  (rseng-scientific-file-formats); the manifest aggregates, not
  replaces, them.
- Honest gaps: when a step was manual or a record is missing,
  say so in the record ("digitized by hand from lab notebook,
  2026-03") - a stated gap is provenance too; an invented link
  is corruption (rseng-honesty).
- Verify like everything else: a provenance spot-check - pick a
  published figure, walk its chain to raw data - belongs in the
  milestone review (rseng-code-review); a chain that breaks is a
  finding.
- AI in the loop is provenance: agent contributions to code,
  data transformations and documents are Agents in the PROV
  sense and belong in both the run records and aidecl.yaml
  (rseng-ai-declaration) - one practice, two granularities.

## Working with this skill

This skill is source-independent: its authority is the W3C PROV
specifications and the RO-Crate community standard linked below.
It systematizes what rseng-reproducibility, rseng-data-management and
rseng-ai-declaration record layer by layer.

Learn more (verified):
  - https://www.w3.org/TR/prov-overview/ - W3C PROV overview
  - https://www.w3.org/TR/prov-o/ - PROV-O ontology
  - https://www.researchobject.org/ro-crate/ - RO-Crate
  - https://workflowhub.eu - WorkflowHub (RO-Crate-native
    workflow registry)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - agents are PROV Agents too
- rseng-archiving - RO-Crate is the deposit shape
- rseng-data-management - dataset versions and checksums in records
- rseng-honesty - stated gaps beat invented links
- rseng-reproducibility - same promise at a different layer
- rseng-scientific-file-formats - embedded origin metadata in files

<!-- related-skills:end -->
