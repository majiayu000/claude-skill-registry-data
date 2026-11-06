---
name: literature-wos-analysis
description: Analyze WoS cited references to build co-citation clusters, annual local citation series, bursts, and frontier candidates.
---

# WoS Citation Analysis

Read [shared contract](../../references/shared-contract.md) and [WoS methods](../../references/wos-methods.md).

Run `wos_analysis.py --input SAVEDRECS --output OUTPUT`. Both WoS tab-separated and tagged plain text are supported. Require TI/PY/CR; check UT uniqueness, reference coverage and export date. Preserve raw reference variants; normalize single unambiguous DOI, leave multi-DOI references unresolved.

Default analysis selects the top 80 references cited by at least 3 sample documents, with at least 3 co-citing documents per edge. Cosine-normalized weights feed seeded Louvain clustering. Bursts analyze every reference meeting the citation threshold, not just displayed nodes. Default s=2, gamma=1, duration=1; report the accompanying gamma/duration sensitivity table. Review short windows, edge censoring, incomplete final years and weak modularity.

Run test_wos.py and test_wos.py --output OUTPUT. Route wos_figures.py through literature-figures and tables through literature-export. Finally run `wos_report.py --output OUTPUT` to refresh the English report and file-hash manifest after all artifacts are saved.

frontier-candidates.json contains references with bursts touching the final observation year. These are candidates for source review, not validated frontiers. Combine their citing-paper titles/abstracts, cluster context and reading evidence before proposing a substantive frontier interpretation. If no robust signal exists, report that result.
