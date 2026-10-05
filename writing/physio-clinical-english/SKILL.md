---
name: physio-clinical-english
description: "Read, translate, and deeply teach English physiotherapy and rehabilitation language without losing scientific detail. Use for an English article, abstract, guideline, report, table, clinical note, acronym, or term; Turkish contextual explanation; sentence-by-sentence reading; academic/statistical language; or physiotherapy terminology. Trigger on İngilizce FTR, makale çevirisi, terim, kısaltma, ne demek, contextual translation. Preserve numbers, uncertainty, methods, and official instrument names. Translation is not endorsement."
---

# Physio Clinical English

## Mandatory first reads

Read [safety core](references/safety-core.md) and [contextual teaching method](references/contextual-teaching.md). Translation does not certify that a clinical claim or instruction is correct. If the supplied text contains possible emergency symptoms or dangerous instructions, translate faithfully, activate the safety gate, and do not turn it into an actionable treatment plan.

## Choose one or more modes

- **Contextual translation:** accurate Turkish or requested-language rendering with methods and nuance preserved.
- **Annotated close reading:** paragraph or sentence, followed by “what it says,” “why it matters,” and “what it does not imply.”
- **Deep terminology teaching:** term, expansion, plain meaning, clinical meaning, word family/collocations, common confusion, and example.
- **Methods-language decoder:** RCT, bias, causal wording, effect measures, confidence intervals, measurement properties, and statistical claims.
- **Visual concept explanation:** when three or more concepts interact, add a compact comparison table, hierarchy, flow, or Mermaid concept map without replacing the full explanation.

Do not reduce detail unless the user explicitly asks for a summary.

## Workflow

1. Identify document type, section, clinical field, audience level, and requested output language.
2. Preserve heading hierarchy, tables, footnotes, symbols, numbers, units, time points, scale direction, and uncertainty.
3. Expand every acronym at first use: `Full English term (ABBR; concise contextual meaning)`.
4. Preserve the original technical term at first use: `Minimal Detectable Change (MDC; the smallest change likely to exceed measurement error)`.
5. Explain the operational meaning in this paper—not only a dictionary equivalent. Label unusual author-specific use as “in this paper.”
6. Deconstruct statistical sentences into population/comparison, outcome/time, effect measure/direction, estimate, interval, clinical threshold, and causal limit.
7. Keep official instrument, classification, protocol, and guideline names. Verify a validated Turkish version before naming one as official.
8. If an acronym is ambiguous, list plausible expansions and the context needed to decide; never guess silently.
9. Preserve hedging and causal boundaries: `may`, `might`, `suggests`, and `associated with` must not become certainty or causation.
10. Invoke `$physio-study-appraisal` if the user asks whether the claim is trustworthy, and `$physio-evidence-search` if they ask whether it reflects current evidence.
11. Respect copyright. Explain externally sourced text in your own words and quote only short necessary excerpts.

## Non-negotiable distinctions

- association ≠ causation;
- no statistically significant difference ≠ equivalence or no effect;
- non-inferiority ≠ equivalence;
- reliability ≠ validity;
- responsiveness ≠ diagnostic sensitivity;
- SEM (measurement) ≠ standard error of the mean;
- MDC/SDC ≠ MIC/MCID;
- impairment ≠ activity limitation ≠ participation restriction;
- absence of evidence ≠ evidence of absence.

## Output

1. Contextual translation or annotated close reading
2. “What is this section actually saying?”
3. Clinical and methodological significance
4. Deep mini-glossary only for necessary terms
5. Optional comparison/flow/concept map when it improves learning
6. Ambiguous acronyms, instrument-version limits, and safety/endorsement caveats

For a one-term question, answer that term deeply but concisely; do not appraise the entire paper unless asked.

