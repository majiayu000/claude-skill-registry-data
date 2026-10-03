---
name: ci-workflow-execution
description: Use when you have a GitHub repository with published CI workflow badges
  (e.g., unit test or package test badges in the README) and need to independently
  verify that the workflows execute successfully, reproduce the pass/fail status,
  and collect structured test results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MassQL
  - pytest
  - GitHub Actions
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02785-1
  title: MassQL
evidence_spans:
- The Mass Spec Query Language (MassQL) is a domain specific language meant to be
  a succinct way to express a query in a mass spectrometry centric fashion.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massql
    doi: 10.1038/s41592-025-02785-1
    title: MassQL
  dedup_kept_from: coll_massql
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02785-1
  all_source_dois:
  - 10.1038/s41592-025-02785-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ci-workflow-execution

## Summary

Execute and validate CI workflows (unit tests, package integration tests) defined in a repository's GitHub Actions configuration to confirm that the software's automated test suite passes and meets documented success criteria. This skill verifies reproducibility of test results and the integrity of CI badges reported in project documentation.

## When to use

You have a GitHub repository with published CI workflow badges (e.g., unit test or package test badges in the README) and need to independently verify that the workflows execute successfully, reproduce the pass/fail status, and collect structured test results. Use this skill when assessing software reliability, reproducing published CI claims, or establishing a baseline for test coverage before making changes.

## When NOT to use

- The repository does not have CI workflows defined (no .github/workflows/ directory or CI configuration files present).
- You only need to check the current badge status in the README without executing tests locally; use the badge link directly instead.
- The repository is private or requires authentication not available in your environment; adjust credentials or use published CI reports instead.

## Inputs

- GitHub repository URL or cloned local repository directory
- CI workflow definition file(s) (.github/workflows/test-unit.yml, test-package.yml, etc.)
- Repository configuration files (requirements.txt, setup.py, pyproject.toml, tox.ini)
- Test fixtures and data (may require separate fetch step, as documented in README)
- Published CI badge link(s) from project README

## Outputs

- Structured test execution report (JSON or CSV format)
- Pass/fail status for unit test suite (test-unit.yml or equivalent)
- Pass/fail status for package integration tests (test-package.yml or equivalent)
- Individual test case results with execution time and error logs
- Comparison document linking observed results to published badge claims

## How to apply

Clone the target repository from GitHub (e.g., mwang87/MassQueryLanguage). Inspect the CI workflow definition files (.github/workflows/*.yml) to identify test targets, success criteria, and test runners used (e.g., pytest, GitHub Actions environment). Install dependencies and runtime environment as specified in the repository configuration (e.g., requirements files, setup.py, setup.cfg). Execute the test suite using the specified runner or by replicating the workflow steps locally. Collect structured test results including overall pass/fail status, individual test case outcomes, execution time, and error logs. Generate a structured report (JSON or CSV) documenting test suite status and compare badge status with observed results to confirm reproducibility.

## Related tools

- **MassQL** (The reference implementation and Python package being tested; installed from pip or cloned repository for test execution) — https://github.com/mwang87/MassQueryLanguage
- **pytest** (Inferred test runner for executing unit tests and integration tests; specified in CI workflow definitions)
- **GitHub Actions** (The CI/CD platform that defines and executes workflows; workflow files are parsed and replicated locally) — https://github.com/mwang87/MassQueryLanguage/actions

## Examples

```
cd tests && sh ./get_data.sh && pip install -r requirements_test.txt && pytest -v --tb=short > test_results.txt 2>&1
```

## Evaluation signals

- Overall test suite pass/fail status matches the badge status reported in the README (unit-test.yml and test-package.yml badges).
- All individual test cases execute without fatal errors; test counts and pass/fail distribution are recorded in structured format.
- Structured report is generated in documented format (JSON or CSV) with consistent schema across multiple workflow executions.
- Error logs are captured for any failed tests; stack traces and assertion failures are preserved for debugging.
- Test execution completes without requiring manual intervention or undocumented environment setup beyond steps listed in README.

## Limitations

- Test fixtures may not be bundled with the repository; a separate download step (e.g., 'cd tests && sh ./get_data.sh') may be required before tests can execute, as noted in the MassQL README.
- Python version compatibility is limited and may vary; MassQL README explicitly states testing in Python 3.9 only, so test results on other versions may differ.
- Additional test dependencies (e.g., requirements_test.txt) must be installed separately; missing these will cause test failures unrelated to the main package.
- Local test execution may differ from GitHub Actions environment due to OS, Python version, or system library differences; CI workflows may contain environment-specific configurations not easily replicated locally.

## Evidence

- [other] The MassQL repository maintains a unit testing CI workflow (test-unit.yml) with an associated passing badge, indicating that the unit test suite executes successfully.: "The MassQL repository maintains a unit testing CI workflow (test-unit.yml) with an associated passing badge, indicating that the unit test suite executes successfully."
- [other] The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation.: "The MassQL repository includes a periodic package-testing CI workflow (test-package.yml) distinct from unit tests, as indicated by the badge link in the project documentation."
- [other] Execute the unit test suite defined in the test-unit.yml CI workflow. Collect test execution results (pass/fail status, test counts, error logs) into a structured report file.: "Execute the unit test suite defined in the test-unit.yml CI workflow. Collect test execution results (pass/fail status, test counts, error logs) into a structured report file."
- [readme] To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: cd tests && sh ./get_data.sh: "To run tests, you'll need to first fetch some fixtures that are not bundled with the git repo: cd tests && sh ./get_data.sh"
- [readme] We currently test massql in python 3.9, but are figuring out other versions if they work or not.: "We currently test massql in python 3.9, but are figuring out other versions if they work or not."
- [readme] You will also want to install the extra requirements for the test suite: pip install -r requirements_test.txt: "You will also want to install the extra requirements for the test suite: pip install -r requirements_test.txt"
