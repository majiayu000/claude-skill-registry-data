---
name: job-tuple-enumeration
description: Use when when initializing MSMetaEnhancer or extending it with new converters,
  you need to discover all available (source_attribute, target_attribute, converter_name)
  conversion triples to build a complete job registry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3070
  - http://edamontology.org/topic_0081
  tools:
  - MSMetaEnhancer
  - Python
  - CIR
  - CTS
  - IDSM
  - PubChem
  - BridgeDb
  - RDKit
  - ConverterBuilder
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- '**MSMetaEnhancer** is a tool used for `.msp` files annotation'
- '`MSMetaEnhancer/libs/converters/web/` named after your service'
- 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
- Create a new Python file in `MSMetaEnhancer/libs/converters/web/`
- 'fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation)'
- __all__ = ['IDSM', 'CTS', 'CIR', 'PubChem', 'BridgeDb', 'MyService']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer_cq
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Job-tuple enumeration

## Summary

Systematically discover and enumerate all available conversion jobs from plugin converters (both web-based and compute-based) by introspecting their metadata and dynamically generating conversion methods. This skill enables comprehensive cataloging of source-to-target chemical identifier conversion routes available within MSMetaEnhancer.

## When to use

When initializing MSMetaEnhancer or extending it with new converters, you need to discover all available (source_attribute, target_attribute, converter_name) conversion triples to build a complete job registry. This is essential before dispatching annotation tasks, to ensure the requested jobs are actually available and to validate that all discovered conversions have executable corresponding methods on their converter instances.

## When NOT to use

- If you have a pre-built, static job configuration file and do not need to discover converters dynamically at runtime.
- If your annotation workflow only uses a fixed subset of converters and manually specifies jobs inline (bypassing auto-discovery).
- If all converter plugins have already been validated and methods already exist—enumeration is then redundant unless new converters are added.

## Inputs

- Converter class definitions from MSMetaEnhancer/libs/converters/web/ (CIR, CTS, IDSM, PubChem, BridgeDb)
- Converter class definitions from MSMetaEnhancer/libs/converters/compute/ (RDKit)
- Converter __init__ method metadata specifying conversions tuples (source_attr, target_attr, method_name)

## Outputs

- Unified Job registry: aggregated collection of (source_attribute, target_attribute, converter_name) tuples
- Serialized Job manifest file listing all available conversions with validation status
- Dynamically instantiated converter instances with generated conversion methods

## How to apply

Load the ConverterBuilder module, which automatically scans the MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories to discover all converter classes. For each discovered converter, extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name). Call create_top_level_conversion_methods() on each converter to trigger dynamic method generation. Aggregate all discovered Job tuples across web and compute converters into a unified Job registry. Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance. Finally, serialize and output the complete Job manifest as a structured file for downstream annotation workflows.

## Related tools

- **ConverterBuilder** (Auto-discovers and instantiates all converter classes; orchestrates conversions list extraction and Job registry aggregation) — https://github.com/RECETOX/MSMetaEnhancer
- **CIR** (Web converter providing chemical identifier conversions (e.g., InChI → SMILES)) — https://cactus.nci.nih.gov/chemical/structure_documentation
- **CTS** (Web converter providing chemical structure transformations) — https://cts.fiehnlab.ucdavis.edu/
- **IDSM** (Web converter providing chemical metadata enrichment (name, InChI, formula, InChI key)) — https://idsm.elixir-czech.cz/
- **PubChem** (Web converter providing chemical identifier and metadata lookups) — https://pubchem.ncbi.nlm.nih.gov/
- **BridgeDb** (Web converter providing cross-database chemical identifier mapping) — https://bridgedb.github.io/
- **RDKit** (Compute converter providing local chemical structure transformations without external service calls) — https://github.com/RECETOX/MSMetaEnhancer

## Examples

```
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM')]
```

## Evaluation signals

- All converter classes in web/ and compute/ directories are discovered and no converters are silently skipped.
- Each Job tuple in the registry has a corresponding, executable conversion method (async for web converters, sync for compute converters) on its converter instance.
- The conversions list from each converter's __init__ is fully reflected in the Job registry—no (source, target, method) triples are omitted.
- Serialized Job manifest is valid JSON or structured format with no missing or malformed entries; each job triple is normalized and unique.
- Validation passes for all Job entries: method resolution succeeds, signature is correct, and no orphaned conversions exist.

## Limitations

- Job enumeration requires all converter classes to follow the MSMetaEnhancer plugin interface convention (conversions list in __init__, dynamic method generation via create_top_level_conversion_methods)—non-compliant custom converters may not be discovered.
- Web-based converters are dependent on external service availability and API rate limits; enumeration does not validate service health, only method existence.
- The Job registry reflects converter capabilities at discovery time; if external services change their API or remove conversion routes, the registry may list stale jobs that fail at runtime.
- Async method validation for web converters may not fully exercise error handling—a method may be present but fail during actual annotation due to API errors, network issues, or malformed responses.

## Evidence

- [other] Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/ directories.: "Load the ConverterBuilder module which automatically discovers and instantiates all available converters from MSMetaEnhancer/libs/converters/web/ and MSMetaEnhancer/libs/converters/compute/"
- [other] For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute, target_attribute, conversion_method_name).: "For each discovered converter (CIR, CTS, IDSM, PubChem, BridgeDb, RDKit, and any custom converters), extract the conversions list defined in its __init__ method as tuples of (source_attribute,"
- [other] Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple.: "Aggregate all discovered Job tuples across web and compute converters into a unified Job registry, where each Job represents one (source_attr, target_attr, converter_name) triple."
- [other] Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance.: "Validate that each Job's conversion_method exists as an async method (for WebConverters) or sync method (for ComputeConverters) on the corresponding converter instance."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [IDSM](https://idsm.elixir-czech.cz/), and [BridgeDb](https://bridgedb.github.io/).: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]."
- [readme] The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.: "The app uses asynchronous implementation of annotation process allowing for optimal fetching speed."
