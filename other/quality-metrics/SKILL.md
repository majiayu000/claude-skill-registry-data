---
name: quality-metrics
description: Define and interpret quality metrics that connect defects, test evidence, release outcomes, escapes, reliability, support, and recovery to decisions without rewarding vanity test counts or gaming.
---
# Quality Metrics

Use when a team needs ongoing evidence about product/release quality, test effectiveness, defect flow, or where validation investment should change.

## Procedure
1. Start from the decisions metrics must support: release confidence, risk hotspots, escaped defects, validation effectiveness, cycle time, reliability, support burden, or improvement priorities.
2. Choose a small set of measures with clear definitions and data sources, such as escaped defect rate/severity, reopen rate, defect age, failure/flake rate, critical-journey pass health, incident/support linkage, time to detect/reproduce/verify, or release rollback/regression frequency.
3. Define denominators and scope so comparisons are meaningful across teams/releases of different size and duration. Avoid raw counts without context.
4. Separate leading indicators from outcomes. Test pass/flake/coverage metrics describe the validation system; escaped defects and user-impact incidents describe actual quality outcomes.
5. Segment by severity, component, journey, platform, change type, root-cause class, or detection layer when aggregation would hide actionable patterns.
6. Track trends over enough time/release samples to distinguish normal variation from a real shift. Annotate major process/architecture/product changes that alter the population.
7. Investigate metric changes qualitatively before prescribing action. A rise in reported defects can reflect better detection rather than worse product quality.
8. Avoid targets that encourage hiding bugs, inflating test counts, marking flakes ignored, or splitting/merging defects to improve numbers.
9. Connect findings to specific improvements in test strategy, engineering controls, design review, observability, or release practice and then monitor whether outcomes change.
10. Review and retire metrics that no longer inform decisions or whose definitions have drifted.

## Decision rules
- Metrics are evidence for judgment, not substitutes for reading severe defects and incidents.
- Coverage/test counts without risk context are weak quality measures.
- Optimize user/system outcomes, not the metric itself.
- Distributed Fleet execution may add useful dimensions such as node/profile/revision when diagnosing escapes, but those dimensions should explain quality rather than become placement policy inside QA.

## Quality gate
The metric set is useful when definitions and sources are stable, denominators/scope make trends interpretable, leading indicators are separated from product outcomes, severe cases remain visible, incentives do not reward hiding problems, and metric changes lead to testable quality improvements rather than dashboard decoration.