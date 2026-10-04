---
name: phronesis
category: strategy
description: "AI-native advisory practice for the Broomva ecosystem. Encodes top-firm consulting methodology (Three Horizons, MIT CISR digital maturity, JTBD, Value Proposition Canvas, RICE/ICE/WSJF, NPV + Real Options, QuantumBlack ML lifecycle, Wardley Mapping) as runnable typed primitives. Produces 7 Discovery-grade deliverables in two modes — consultant CLI or autonomous Life Runtime endpoint. Use when: (1) running an AI/digital consulting engagement, (2) building a maturity assessment, (3) generating prioritized use-case dossiers, (4) designing an innovation roadmap, (5) modeling ROI for AI initiatives, (6) designing controlled pilots, (7) extracting reusable IP from completed engagements. Triggers on 'consulting', 'consultancy', 'advisory', 'fast discovery', 'discovery sprint', 'AI maturity', 'digital maturity', 'use case ideation', 'use case prioritization', 'innovation roadmap', 'roi model', 'consultoría', 'evaluación de madurez', 'hoja de ruta'."
---

# phronesis — AI-native Advisory Practice

> **Status:** Phase 1 complete (`v0.1.2-pre`) — substrate + 15 active frameworks + 5 stages + 7 deliverables + L1–L5 linter + M7 extraction pipeline. Phase 2 engagement-driven (M4 stage CLI + M5 autonomous-mode stub-to-real path).
> Track progress: [`docs/methodology.md`](docs/methodology.md) (canonical reference), `docs/adr/0001-0008`, and the design spec at `~/broomva/docs/superpowers/specs/2026-05-06-phronesis-design.md`.

## What it does

Runs AI/digital consulting engagements through 5 stages:

1. **Intake** — stakeholder map, interview guide, **strategic thesis** (kills "hagamos algo de IA" — Bision empirical 100% failure)
2. **Maturity Scan** — MIT CISR + Gartner AI dimensions, gap analysis, capability heatmap
3. **Use-Case Ideation** — JTBD + VPC, with `IdeationSource` diversity check
4. **Prioritization** — RICE/ICE/WSJF, ROI Model with sensitivity, Impact-Effort Matrix
5. **Roadmap Synthesis** — Three Horizons, QuantumBlack ML lifecycle pilots, baselines captured

Each stage has a non-negotiable human-review gate.

## When to invoke this skill

* User asks for AI/digital consulting work — maturity assessment, roadmap, use-case prioritization
* User mentions Spanish-language equivalents: "consultoría", "evaluación de madurez", "hoja de ruta"
* User describes a Fast Discovery, discovery sprint, or strategic-thesis-finding engagement
* User wants to extract reusable IP from a completed engagement (cross-engagement learning)

## When NOT to invoke this skill

* User wants generic "do AI for me" without scope — phronesis explicitly refuses to start without a strategic thesis
* User wants implementation work, not advisory — phronesis produces *plans* and *recommendations*, not running systems
* User wants change-management or organizational design — that's D-scope (deferred to a later phase)
* User wants only personal-decision support — use [strategy-skills](https://github.com/broomva/strategy-skills) instead

## Commands (CLI mode — most land in M4)

```bash
phronesis init <tenant> --industry <industry> --region <iso> --sponsor "Name (Role)" --scope "..."
phronesis intake --interview "..." --transcript path/to/file.md
phronesis intake --thesis "..."         # captures StrategicThesis (L1)
phronesis review intake --approve | --revise
phronesis scan --frameworks mit-cisr-digital,gartner-ai
phronesis ideate --frameworks jobs-to-be-done,value-prop-canvas
phronesis prioritize --frameworks rice --roi unit-economics,real-options
phronesis roadmap --frameworks three-horizons --pilot-design quantumblack-ml
phronesis render --all
phronesis lint                          # P3, P7, P8, L1-L5 enforcement (blocking)
phronesis status
phronesis bookkeep <slug>               # extract anonymized learnings to research/entities/
```

## Five C-level failure modes structurally prevented

| Bision-observed | Frequency | Linter rule | Type primitive |
|---|---|---|---|
| Sin tesis estratégica | 100% | L1 STRATEGIC_THESIS_REQUIRED | `StrategicThesis` |
| Casos mal priorizados | 87% | L2 DIVERSE_IDEATION_SOURCES | `IdeationSource` |
| Datos no preparados | 74% | L3 DATA_READINESS_GATE | `DataReadinessAssessment` |
| Desconexión negocio-tech | 61% | L4 ADOPTION_METRIC_REQUIRED | `AdoptionMetric` |
| Sin medición de ROI | 48% | L5 BASELINE_REQUIRED | `BaselineSection` |

## Documentation

* **Methodology:** [`docs/methodology.md`](docs/methodology.md) — canonical methodology reference (10 sections: stages, deliverables, frameworks, gates, linter, anonymization, modes, discovery loop, IP extraction)
* **ADRs:** [`docs/adr/0001-`](docs/adr/) through `0008-`
* **Design spec:** `~/broomva/docs/superpowers/specs/2026-05-06-phronesis-design.md`
* **Linear:** [Phronesis project](https://linear.app/broomva/project/phronesis-ai-native-advisory-practice-8007a216a186)
* **Quickstart:** *(M4 — pending stage CLI commands)* `docs/quickstart.md`
