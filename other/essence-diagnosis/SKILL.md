---
name: essence-diagnosis
version: "1.1.0"
user-invocable: true
description: Use when a complex problem seems unsolvable and needs digging to the essence — diagnosis only, not fixing. Symptoms include massive logs with no root cause surfaced, complex crashes, architectural essence analysis, requirement authenticity verification, systemic chronic issues, information overload, disconnect between symptoms and essence, multiple intertwined factors, or premature-convergence tendencies — even when the user never explicitly says "diagnose". Also triggers on 本质诊断, 根因诊断, 深度诊断, 诊断问题本质, 梳理问题逻辑, 证据链分析, 逻辑链分析, essence-diagnosis.
dependencies:
  - multi-agent-debate
  - report-output-discipline
---

# Essence Diagnosis

> **Role**: Performs essence analysis and diagnosis of complex problems only. Produces a complete evidence chain + logic chain + hypothesis list. **Does NOT solve the problem** (no solutions, no execution, no fixes). Must orchestrate `multi-agent-debate` for adversarial verification.
>
> **Output templates and formats** are in [reference.md](reference.md).

## Prerequisite skill check

On load, verify `multi-agent-debate` and `report-output-discipline` are available. If either is missing, abort and print:

`npx skills add FuDesign2008/open-skills -g --skill '*' --yes`

Do not silently fall back.

## Why this skill exists

Faced with complex problems (massive logs, intertwined factors, disconnect between symptoms and essence), both humans and AI tend to make the same mistake: **stopping at the first explanation that looks like a root cause**. This is premature convergence. Once converged, all subsequent analysis becomes "proving myself right" — confirmation bias kicks in, counterexamples are ignored, alternative explanations are discarded.

The sole value of this skill is to fight these two cognitive traps with a structured process, turning "I think it's X" into "the evidence chain points to X, and Y/Z have been falsified". It does not do repair. It delivers a diagnosis report that survives adversarial verification.

## Relationship to other skills

| Skill | Responsibility | Relationship to this skill |
|-------|---------------|----------------------------|
| `solve-workflow` | Full workflow (analyze → solution → execute → verify → recap) | This skill is the heavy-weight deep-dive of its phase 1.2, focused purely on analysis/diagnosis; can also be used standalone |
| `multi-agent-debate` | Three-agent adversarial verification of existing conclusions | This skill's output = its input; **one-way orchestration**, debate does not call back into this skill |
| `diagnose` / `debug-workflow` | Single-bug diagnosis/debugging | They assume "known to be a bug"; this skill makes no such assumption and fits the foggy state of "not even sure what the problem is yet" |
| `hybrid-debug` | Hybrid app (WebView/WKWebView/Electron + H5) four-layer debugging | Domain-specific pre-filter: for hybrid problems, apply its four-layer model first; escalate to this skill only when the problem is still foggy after structured layer-by-layer analysis |

## Triggers and mode

**Triggers**: 本质诊断, 根因诊断, 深度诊断, 诊断问题本质, 梳理问题逻辑, 证据链分析, 逻辑链分析, essence-diagnosis

**Default**: When the user invokes it, the problem is assumed to be complex — no complexity-threshold gate is applied.

## Methodology backbone

Three-source fusion (all backed by mature industry practice, not invented from scratch):

| Source | Borrowed mechanism | Role in this skill |
|--------|--------------------|--------------------|
| Medical differential diagnosis (DDx) | SOAP format + parallel hypotheses + VINDICATE categorization | Process backbone (S/O/A three sections) + forced exhaustive hypotheses |
| Strong inference (Platt) | Parallel hypothesis **falsification** (not confirmation), falsifiability (Popper) | Hypothesis-testing mechanism — hunt counterexamples, not supporters |
| Fault tree / accident investigation | Top-down causal backtracking, evidence-support matrix | Logic-chain visualization |

## Core flow: S → O → A → Debate

### S — Subjective: information-field collection and denoising

Goal: extract structurally from a chaotic information field — **do not accept everything wholesale**. The essence of a complex problem is that signal is drowned by noise; denoising is step one.

1. **Source inventory**: logs, code, docs, metrics, configs, user feedback, meeting notes, git history… list every available information source
2. **Denoising**: dedupe, align by time, sort by relevance, flag obvious noise
3. **Output**: a list of objective facts (each with a source `file:line` / `cmd` / `N samples`)

> Why denoise before forming hypotheses? Because reading logs with a head full of hypotheses, you only see the lines that support them — that is the entry point for confirmation bias. Forming hypotheses during denoising is strictly forbidden.

### O — Objective: multi-hypothesis generation and evidence-chain construction

Goal: **force multiple hypotheses** to fight premature convergence.

1. **Hypothesis generation (≥3)**: walk each category of the VINDICATE general taxonomy (see reference.md); at least one hypothesis per category
2. **Build an evidence chain for each hypothesis**: use the Toulmin argument model (see reference.md); all 6 elements must be complete
3. **Evidence-hypothesis separation**: collect evidence first, then match to hypotheses; never "form a hypothesis then hunt for evidence"
4. **No source, no conclusion**: every piece of evidence must cite the original text + line number / command output / sample count, otherwise it is discarded

> Why ≥3? With only one hypothesis you unconsciously collect only supporting evidence; with two you pick the more comfortable one; with three or more you actually compare. This is a century-old rule of thumb in differential diagnosis.

### A — Assessment: logic-chain assembly and bias counter-attack

Goal: assemble the evidence chain into a logic chain, and actively look for flaws in your own work.

1. **Logic-chain construction**: top-down causal backtracking (fault tree, see reference.md); every causal link needs evidence support
2. **Bias counter-attack check**: for each hypothesis, walk through the 4-item bias checklist (below)
3. **Weakest-link identification**: pick the 2-3 weakest links in the logic chain — these are the targets handed to debate
4. **Physical verification design**: every conclusion must map to an executable verification command or experiment

### Orchestrate multi-agent-debate (hard constraint, not optional)

After S/O/A complete, **must** invoke `multi-agent-debate` for adversarial verification. This is a hard constraint of this skill.

**Handoff package** (format in reference.md):
- One-paragraph primary hypothesis
- Evidence list (each with a source tag)
- 2-3 weakest links

When debate returns its conclusions, update the "Confirmed Facts / Reasonable Inferences / Unresolved Disputes" sections of the diagnosis report.

> Why must it go through debate? No matter how rigorous S/O/A are, they are pushed by a single analyst and will have blind spots. Debate uses three adversarial perspectives (Defender / Challenger / Evidence Hunter) to forcibly break the single viewpoint and adjudicate reasoning disputes with physical evidence.

## Evidence-chain hard constraints

| Rule | Why |
|------|-----|
| **No source, no conclusion** | "Evidence" without an original-text citation is a hotbed of hallucination — LLMs will fabricate plausible-looking citations |
| **Toulmin 6 elements** (Claim / Data / Warrant / Backing / Qualifier / Rebuttal) | Forces every conclusion to be decomposed to an auditable granularity; Rebuttal forces you to actively imagine counterexamples |
| **Evidence tags**: `[FACT:file:line]` `[FACT:cmd]` `[FACT:N samples]` `[INFERENCE]` `[UNRESOLVED]` | Facts and inferences must be visually separable, otherwise inferences quietly mutate into "facts" |
| **Evidence-hypothesis separation** | Evidence first, hypotheses second — avoids hypothesis contamination of evidence collection |

## Bias counter-attack checklist

In phase A, check each hypothesis against every item:

| Bias | Symptom | Counter-measure |
|------|---------|-----------------|
| **Confirmation bias** | Only collecting evidence that supports the hypothesis | Force each hypothesis to list ≥2 counter-evidence items; finding no counter-evidence is itself a danger signal |
| **Premature convergence** | Stopping at the first plausible-looking one | Force all ≥3 hypotheses through the full evidence chain; no mid-way abandonment |
| **Anchoring effect** | Anchored by the first piece of info / first stack trace | Before phase S denoising completes, forming hypotheses is forbidden |
| **Correlation as causation** | A and B co-occur, therefore A causes B | Demand a mechanistic explanation (by what mechanism does A cause B) + hunt for counterexamples |

## Output format

The complete SOAP diagnosis report + evidence-chain table + logic-chain diagram + debate handoff package — templates are in [reference.md](reference.md).

**Sink**: write the report to `docs/reports/diagnosis/<YYYY-MM-DD>-<topic>.md`, where `<topic>` is a lowercase kebab-case slug. When that file already exists from an earlier run, append `-2`, `-3`, and so on — never overwrite. A rewrite within the same run writes back to the same file. Registry row: `诊断报告` in `report-output-discipline/reference.md` (`human` + `接入`).

After writing, derive `<same-base-name>.html` beside the Markdown source following `report-output-discipline`, and report both paths. When the renderer is unavailable, write only the Markdown source and state why.

The final deliverable of this skill is a **diagnosis report**, not a fix plan. The report must end with the note "This report covers diagnosis only and has not entered the resolution phase."

## Red Flags (non-intuitive traps)

- ❌ Skipping S and jumping to hypotheses — forming hypotheses on un-denoised information is building on noise
- ❌ Mixing inferences into evidence collection — inferences treated as facts pollute the evidence chain and become hard to trace
- ❌ Building an evidence chain only for the most likely hypothesis — leaving the others unfinished = premature convergence, exactly what this skill fights
- ❌ A logic chain longer than 5 steps with no intermediate evidence — long reasoning chains are a hotbed of hallucination; every step needs an anchor
- ❌ Failing to identify the weakest links before orchestrating debate — debate loses its targets and becomes empty argument
- ❌ Treating this skill as a repair tool — after delivering the diagnosis report, if the user wants a fix, hand off to `solve-workflow` or a specialized skill
