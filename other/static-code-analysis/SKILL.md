---
name: static-code-analysis
description: Use when when preparing to submit a pull request to a collaborative Python
  project (like BiG-SCAPE) that mandates PEP8 compliance, or when establishing quality
  gates for a codebase that has adopted linters as part of its contribution guidelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0081
  tools:
  - flake8
  - black
  - PlantUML
  - Git
  - Docker
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-019-0400-9
  title: BiG-SCAPE biosynthetic diversity
- doi: 10.1021/acs.jproteome.2c00602
  title: ''
evidence_spans:
- uses flake8 for linting
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_scape_biosynthetic_diversity_cq
    doi: 10.1038/s41589-019-0400-9
    title: BiG-SCAPE biosynthetic diversity
  - build: coll_clomet_cq
    doi: 10.1021/acs.jproteome.2c00602
    title: CloMet
  dedup_kept_from: coll_big_scape_biosynthetic_diversity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-019-0400-9
  all_source_dois:
  - 10.1038/s41589-019-0400-9
  - 10.1021/acs.jproteome.2c00602
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# static-code-analysis

## Summary

Apply automated linting tools to enforce code style standards (PEP8 compliance) across a Python source tree without executing the code. This skill ensures consistent code quality and catches style violations early in development workflows.

## When to use

When preparing to submit a pull request to a collaborative Python project (like BiG-SCAPE) that mandates PEP8 compliance, or when establishing quality gates for a codebase that has adopted linters as part of its contribution guidelines. Use this skill before committing work to ensure your changes pass the project's linting checks.

## When NOT to use

- Input is already formatted and linting checks have already passed upstream (e.g., in CI/CD).
- Project does not enforce linting standards or uses a different linting tool (e.g., pylint, ruff).
- You need to enforce runtime behavior or logic errors—flake8 is a style checker, not a type checker or behavioral validator.

## Inputs

- Python source tree (directory of .py files)
- flake8 configuration file (optional, e.g., .flake8 or setup.cfg)

## Outputs

- Structured lint report (file location, line number, violation code, description)
- Exit code indicating pass/fail status

## How to apply

Obtain the Python source tree from the target repository (e.g., medema-group/BiG-SCAPE). Run flake8 across all Python source files to detect PEP8 violations—flake8 will parse the code statically without execution and report violations by file location and line number. Review the structured lint report to identify style violations, then correct them (or use complementary auto-formatting tools like black to remediate issues automatically). Re-run flake8 to verify violations are resolved before submitting changes.

## Related tools

- **flake8** (Static linter that detects PEP8 style violations across Python source files)
- **black** (Complementary auto-formatter to remediate PEP8 violations identified by flake8)

## Examples

```
flake8 .
```

## Evaluation signals

- flake8 exits with code 0 (no violations detected) after running across the full source tree
- Lint report contains zero violations, or all reported violations have been addressed and lint report is empty on re-run
- All flagged violations match known PEP8 error codes (e.g., E501 for line too long, F401 for unused import)
- File locations and line numbers in the report are accurate and correspond to actual violations in the source code

## Limitations

- flake8 checks style compliance only; it does not detect logical errors, type mismatches, or runtime exceptions.
- Project configuration (setup.cfg, .flake8, pyproject.toml) may override default PEP8 rules, so violations reported depend on the repository's specific linting policy.
- Some PEP8 violations may be intentional or contextually acceptable; developers must review and judge violations before auto-formatting.

## Evidence

- [other] The BiG-SCAPE project uses flake8 for linting to enforce PEP8 standards across the source tree.: "The BiG-SCAPE project uses flake8 for linting to enforce PEP8 standards across the source tree."
- [other] Run flake8 linter across all Python source files in the repository to detect PEP8 violations.: "Run flake8 linter across all Python source files in the repository to detect PEP8 violations."
- [other] Generate and save a structured lint report documenting all identified violations, their file locations, and line numbers.: "Generate and save a structured lint report documenting all identified violations, their file locations, and line numbers."
- [readme] We use black for auto formatting: "We use black for auto formatting"
