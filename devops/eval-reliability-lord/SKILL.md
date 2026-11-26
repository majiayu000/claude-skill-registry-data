---
name: eval-reliability-lord
description: Lord skill for reliability@k and security-adjusted reliability@k evaluation of AI coding agents. Replaces the misapplied pass@k metric with correct multi-rollout scoring.
triggers:
  - eval reliability lord
  - reliability
  - reliability@k
  - security-adjusted
  - eval scoring
  - multi-rollout
  - موثوقية
  - تقييم الوكلاء
personas:
  - QA
  - ML
  - MLOPS
  - ARCH
tech_stack: []
lord: true

---

# Eval Reliability Lord

[OBJ] Correct reliability scoring for AI coding agents. pass@k is misapplied — reliability@k is the fix.

## Problem

Current AI coding agent benchmarks rank with the pass@k estimator but misapply it: they set n = number of unit tests in a single submission rather than n = independent rollout attempts. This conflates test-suite size with attempt independence, inflating reported scores by 0.85–0.97 in absolute terms (0.96–0.98 reported vs 0.00–0.12 corrected).

## Rules

1. [REQ] **n = independent rollouts.** reliability@k uses n = number of independent rollout attempts per (task, agent) pair. NOT test-suite size.
2. [REQ] **c = fully-passing rollouts.** c = rollouts where ALL tests pass. Partial pass = fail.
3. [REQ] **Formula.** `reliability@k = 1 - C(n-c, k) / C(n, k)`. When n < k, use `c/n`. When n == 0, return 0.0. Clamp to [0, 1].
4. [REQ] **Security-adjusted.** `security_adjusted_reliability@k` counts only rollouts that are BOTH functionally correct AND free of high-severity insecure patterns. A rollout that passes tests but has a critical vuln = SECURITY_FAIL, not PASS.
5. [REQ] **Multi-rollout mandatory.** Single-rollout scores are NOT reliability. A cheap single-rollout proxy fails to substitute (Spearman ρ = 0.417). Minimum 5 rollouts for a reliability score.
6. [REQ] **Report both.** Every eval report must include reliability@k AND security_adjusted_reliability@k. Reporting only one = incomplete.
7. [REQ] **Docker reproducibility.** Rollouts must run in isolated, deterministic Docker containers (SWE-bench pattern). Flaky local deps = invalid score.
8. [REQ] **Task-level resolution.** Report per-task resolution, not just macro-averaged pass rate. Macro-averaged hidden-test pass rate (0.80) diverges sharply from strict task resolution (0.20).
9. [REQ] **No recall contamination.** Tasks mined from public GitHub merges may have been seen during pretraining. Prefer original tasks (DeepSWE pattern) whose reference solutions stay out of the public record.
10. [REQ] **Verifier quality.** Inherited tests from merged PRs fail correct alternatives or pass incomplete fixes. Use hand-written verifiers that accept any correct implementation.
11. [REQ] **Score band separation.** A good benchmark separates frontier agents across a wide score band. Clustering at 95%+ = benchmark saturation, not agent excellence.
12. [REQ] **Cost-aware.** Report tokens + duration per rollout. Reliability without cost = misleading. A 99% reliable agent at 10x cost may be worse than 90% at 1x.
13. [REQ] **Rollout independence.** Rollouts must be independent: different seeds, fresh context, no shared state. Shared context = correlated failures = inflated score.
14. [REQ] **aiZee eval harness.** Use `eval/reliability.py` for scoring. `eval/harness.py` for end-to-end evidence gates. Never hand-compute reliability.
15. [PROHIBIT] Reporting pass@k as reliability without n = independent rollouts.
16. [PROHIBIT] Counting a rollout with a high-severity vuln as PASS for security-adjusted scoring.
17. [PROHIBIT] Single-rollout "reliability" claims.
18. [PROHIBIT] Using inherited PR tests as the sole verifier without checking they accept correct alternatives.
19. [REQ] **ReliabilityBench.** Evaluate agents across three dimensions: consistency (k-trial pass rates), robustness (ε-perturbation levels), fault tolerance (λ-infrastructure failures). Agents drop from 96.9% pass@1 to 88.1% at ε=0.2.
20. [REQ] **Deployment Decision Reliability (DDR).** Use Generalizability Theory. Agent main effect <3% of variance; agent-by-task interaction 7-23%. Leaderboards rank specialization, not pure capability. Training-cell reliability can negatively correlate with held-out reliability.
21. [REQ] **Beyond pass@1 metrics.** Report Reliability Decay Curve (RDC), Variance Amplification Factor (VAF), Graceful Degradation Score (GDS), and Meltdown Onset Point (MOP) for long-horizon agents.
22. [REQ] **agentrel library.** Use `agentrel` open-source library for reproducibility stats, ICC, pass@k/pass^k confidence intervals, and flakiness detection.
23. [REQ] **SWE-bench Verified gap.** Macro-averaged hidden-test pass rate (0.80) diverges sharply from strict task resolution (0.20). Report both metrics.
24. [REQ] **CI-integrated eval gates.** Block deployment on reliability@k < threshold. Use Braintrust or custom CI gates. RDC, VAF, GDS, MOP reporting mandatory for long-horizon agents.
25. [PROHIBIT] Reporting pass@1 as reliability without multi-rollout validation and DDR analysis.

## References

- arXiv 2608.14711 "Beyond Pass@k": reliability@k + security-adjusted reliability@k.
- DeepSWE: original long-horizon tasks, hand-written verifiers, no recall contamination.
- SWE-bench Verified: Docker-based reproducible evaluation.
- aiZee `eval/reliability.py`: implementation of reliability@k + security_adjusted.
