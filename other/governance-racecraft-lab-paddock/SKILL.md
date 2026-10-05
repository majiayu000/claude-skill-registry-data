---
name: governance
description: "Skill for the Governance area of paddock. 28 symbols across 23 files."
---

# Governance

28 symbols | 23 files | Cohesion: 75%

## When to Use

- Working with code in `src/`
- Understanding how WipIndicatorPanel, SystemHealthCard, PolicyEditor work
- Modifying governance-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `src/components/panels/cost-tracker-panel.tsx` | normalizePolicy, systemHealthTestId, GovernanceSubviewContent, openPolicyEditor, submitRecoveryAction |
| `src/components/governance/budget-utilization-chart.tsx` | severityColor, BudgetUtilizationChart |
| `src/components/governance/wip-indicator-panel.tsx` | WipIndicatorPanel |
| `src/components/governance/system-health-card.tsx` | SystemHealthCard |
| `src/components/governance/policy-editor.tsx` | PolicyEditor |
| `src/components/governance/override-grant-form.tsx` | OverrideGrantForm |
| `src/components/governance/modal-error-summary.tsx` | ModalErrorSummary |
| `src/components/governance/incident-recovery-modal.tsx` | IncidentRecoveryModal |
| `src/components/governance/etag-conflict-toast.tsx` | EtagConflictToast |
| `src/components/governance/calibration-progress.tsx` | CalibrationProgress |

## Entry Points

Start here when exploring this area:

- **`WipIndicatorPanel`** (Function) — `src/components/governance/wip-indicator-panel.tsx:28`
- **`SystemHealthCard`** (Function) — `src/components/governance/system-health-card.tsx:42`
- **`PolicyEditor`** (Function) — `src/components/governance/policy-editor.tsx:42`
- **`OverrideGrantForm`** (Function) — `src/components/governance/override-grant-form.tsx:65`
- **`ModalErrorSummary`** (Function) — `src/components/governance/modal-error-summary.tsx:34`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `WipIndicatorPanel` | Function | `src/components/governance/wip-indicator-panel.tsx` | 28 |
| `SystemHealthCard` | Function | `src/components/governance/system-health-card.tsx` | 42 |
| `PolicyEditor` | Function | `src/components/governance/policy-editor.tsx` | 42 |
| `OverrideGrantForm` | Function | `src/components/governance/override-grant-form.tsx` | 65 |
| `ModalErrorSummary` | Function | `src/components/governance/modal-error-summary.tsx` | 34 |
| `IncidentRecoveryModal` | Function | `src/components/governance/incident-recovery-modal.tsx` | 57 |
| `EtagConflictToast` | Function | `src/components/governance/etag-conflict-toast.tsx` | 27 |
| `CalibrationProgress` | Function | `src/components/governance/calibration-progress.tsx` | 36 |
| `BulkPromoteModal` | Function | `src/components/governance/bulk-promote-modal.tsx` | 43 |
| `BreakerOpenBanner` | Function | `src/components/governance/breaker-open-banner.tsx` | 29 |
| `AegisEmergencyReserveBadge` | Function | `src/components/governance/aegis-emergency-reserve-badge.tsx` | 29 |
| `WindowsSubview` | Function | `src/components/governance/windows-subview.tsx` | 32 |
| `SystemHealthSubview` | Function | `src/components/governance/system-health-subview.tsx` | 23 |
| `PolicyRow` | Function | `src/components/governance/policy-row.tsx` | 34 |
| `PoliciesSubview` | Function | `src/components/governance/policies-subview.tsx` | 36 |
| `OverridesSubview` | Function | `src/components/governance/overrides-subview.tsx` | 37 |
| `FeatureFlagDisabledShim` | Function | `src/components/governance/feature-flag-disabled-shim.tsx` | 39 |
| `DiagnosticsSubview` | Function | `src/components/governance/diagnostics-subview.tsx` | 25 |
| `DiagnosticFeed` | Function | `src/components/governance/diagnostic-feed.tsx` | 47 |
| `DiagnosticFeedRow` | Function | `src/components/governance/diagnostic-feed-row.tsx` | 29 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Panels | 5 calls |

## How to Explore

1. `gitnexus_context({name: "WipIndicatorPanel"})` — see callers and callees
2. `gitnexus_query({query: "governance"})` — find related execution flows
3. Read key files listed above for implementation details
