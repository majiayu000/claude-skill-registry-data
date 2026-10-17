---
name: kvasir-research-decomposition
description: Decompose and cluster complex research tasks for systematic parallel investigation.
---

# Research Decomposition

## Purpose

Take complex research requirements and systematically decompose them into related clusters that enable parallel investigation while maintaining logical coherence and dependency awareness.

## When to Use

- Receive complex research requests needing decomposition
- Must organize research into decomposed clusters for parallel execution
- Research involves multi-repository codebase exploration
- Research targets a large set of similar, independent units (many repositories, services, packages, endpoints) that a single investigation pass cannot cover with per-unit rigor
- Need to maximize investigation efficiency through intelligent task clustering
- Research spans multiple systematic investigation phases

## Reconsideration Mode

This skill is also invoked on later rounds, given the prior round's reviewed findings, to decide whether research is sufficient for the report or further investigation is warranted. On reconsideration: adjust the existing cluster plan rather than re-decomposing from scratch — refine, drop, or add clusters as the findings warrant, preserving the original research question and scope.

## Workflow

1. **Understand research objectives and constraints.**
   - Analyze research questions and success criteria provided
   - Identify information dependencies and prerequisite knowledge
   - Map investigation scope and key entities involved

2. **Define research scope and formulate investigation questions.**
   - Cluster related investigation areas (e.g., service A architecture, service A integration points)
   - Example: "Service discovery" and "Registry setup" cluster together vs. separate from "API patterns"
   - Example: "Database schema" clusters with "ORM configuration" but separate from "caching layer"
   - Formulate specific, answerable questions for each cluster
   - List what each cluster needs to discover and how findings interconnect

3. **Cluster research into parallel-executable groups.**
    - Group investigations that can proceed independently
    - Ensure clusters have clear boundaries and minimal inter-dependencies
    - Example: "Authentication architecture" is separate from "User service implementation"
    - Example: "Database migrations" can run parallel with "API endpoint discovery"
    - Assign investigation priority and sequencing where needed

4. **Scale cluster count to target volume (volumetric batching).**
    - Clustering has two axes: topical (by subject) and volumetric (by count of independent units). When the scope enumerates many similar, independent units (repositories, services, packages, endpoints, files), batch the units — do not collapse them into one cluster because they share a topic. Topical unity is not a dependency.
    - Record an explicit one-line scaling verdict in the plan: `Scaling check: independent units=<N or estimate>, homogeneous=<yes/no>, per-unit depth=<deep/shallow> → <single cluster — reason | K batches of ~M units, grouped by <seam>>`.
    - Default to parallel batches whenever N exceeds what one research pass can cover at the required per-unit rigor (guideline: N > ~20 for per-unit analysis; higher for shallow scans). A single-cluster plan for such a set requires a stated one-sentence justification in the verdict — batching is the default posture, single-cluster is the exception.
    - Size batches from per-unit depth: deep per-unit analysis → ~10–30 units per batch; shallow scans (metadata, presence checks) → ~100–200 units per batch. Derive K = ceil(N / batch size).
    - Group by natural seams when they exist (owner, directory, language, domain, size); otherwise use deterministic slices (round-robin or lexicographic) so batch membership is unambiguous and reproducible.
    - Respect the requesting agent's practical dispatch limits: only a bounded number of subtasks can run concurrently, and each batch output requires review before the report consolidates it. When K is large, plan waves of parallel batches rather than inflating batch size.
    - Give every batch the same investigation questions and a uniform per-unit output schema so consolidation can aggregate mechanically; for exploratory scopes, consider a first-wave sample batch to validate the schema and effort estimate before dispatching all K.
    - Calibration: "analyze 770 repositories for CI configuration patterns" → `Scaling check: independent units=770, homogeneous=yes, per-unit depth=deep → 8 batches of ~96 repos, lexicographic slices`, executed in waves, plus one integration cluster. Counter-example: "compare build times across 12 repositories" → `Scaling check: independent units=12, homogeneous=yes, per-unit depth=deep → single cluster — one pass covers 12 units at full rigor`.

5. **Plan cross-cluster integration points.**
    - Identify where cluster findings must be integrated
    - Define validation criteria where results from different clusters intersect
    - Map dependency relationships for later integration

6. **Deliver decomposed research plan.**
     - Present clusters with clear investigation scope for each
     - Provide execution guidance and success criteria per cluster
     - Specify integration points where findings must be integrated
     - Include the scaling verdict, and when batching: list each batch with its membership rule, the shared question set, the per-unit output schema, and the integration point
     - State the expected round count in one line. If more than one round is plausible, name the specific finding or dependency that would trigger it (e.g., "round 2 likely if the auth cluster reveals a custom protocol"). Do not write generic sufficiency criteria — if no concrete trigger comes to mind, "expected rounds: 1" is the whole line.

## Quality Criteria

- Research scope is decomposed into minimally-dependent clusters
- Each cluster has specific, measurable investigation objectives
- Clustering enables genuinely parallel research (not artificial parallelization)
- Cluster boundaries are clear and unambiguous
- Integration points between clusters are explicitly identified and mapped
- Decomposition reduces total investigation time vs. sequential approach
- Cluster count scales with the number of independent units — large homogeneous target sets are batched, and the scaling verdict is recorded in the plan

## Anti-Patterns

- **Artificial clustering**: Creating separate clusters that share dependencies
- **Over-fragmentation**: Breaking research into too many small clusters
- **Volume collapse**: Folding a large set of independent, similar targets into a single cluster because they share a topic — the mirror image of over-fragmentation
- **Under-clustering**: Grouping unrelated investigations together
- **Missing integration**: Decomposing without planning cross-cluster integration
- **Unclear cluster scope**: Leaving investigators uncertain what each cluster covers
- **Ignoring dependencies**: Not mapping how findings feed into each other
