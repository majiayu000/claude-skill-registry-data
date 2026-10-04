---
name: sflow-knowledge
description: List, inspect, record, harvest, or resolve governed knowledge and remote assets with provenance.
disable-model-invocation: true
argument-hint: "list|show|record|harvest|resolve"
---
# Manage governed knowledge

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Start with `singularity-flow knowledge list` and inspect a selected record with `singularity-flow knowledge show`.
2. Before record, harvest, or resolve, show the exact source, destination, content hash, trust state, and remote/network requirement.
3. Require explicit consent for the selected mutation and never broaden an allowlist or trust an unpinned remote implicitly.
4. Report immutable provenance and every changed file. Knowledge is evidence; it does not become an approved requirement or authority decision by being recorded.
