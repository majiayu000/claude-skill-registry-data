---
name: physio-evidence-search
description: "Search physiotherapy evidence with PubMed/PEDro, PICO and GRADE. Use for etkililik, doz and güncel literatür; prefer medical-evidence-research when available."
---

# Physio Evidence Search

Original standalone scope and trigger coverage: Search, synthesize, and clinically translate current physiotherapy and rehabilitation evidence. Use for effectiveness, comparative interventions, harms, dose/frequency, guidelines, prognosis, PICO/PICOTS/PIRD/PECO, PubMed, PEDro, Cochrane, systematic reviews, GRADE, newest literature, or older-versus-newer contradictions. Use for kanıta dayalı FTR, güncel literatür, doz, etkililik, karşılaştırma. Do not use as the primary workflow for one supplied paper; use physio-study-appraisal.

## Compatibility and one-workflow routing

When `medical-evidence-research` is actually available, let its matching evidence-answer, search, appraisal or update track own that work and return one integrated answer. A named handoff is not proof that the host loaded the skill. Do not run two complete research workflows or produce duplicate outputs. If the canonical skill is unavailable, complete this skill's original standalone workflow using its local safety and method references below; do not require a paid tool or a sibling package.

For database searches, read [native search strategy](references/search-strategy.md) and [retrieval integrity](references/tool-routing.md). For paper effects and bias, read [appraisal and synthesis](references/appraisal-and-synthesis.md). For a requested evidence update/watch, read [literature watch](references/literature-watch.md). Apply independent human final eligibility for formal reviews, keep found/retrieved/reviewed counts distinct, and retain changed publication records even when an identifier was already seen. The skill itself does not schedule future runs.

## Mandatory first reads

Read [safety core](references/safety-core.md) and [methods and sources](references/methods-and-sources.md). Run the safety gate before searching; an urgent presentation must not wait for literature retrieval.

## Workflow

1. **Classify the decision.** Use PICO/PICOTS for interventions; PIRD for diagnostic accuracy; PECO or a prognostic frame for exposure/prognosis; and a construct-population-purpose frame for measurement. Do not force every question into PICO.
2. **Resolve only decisive ambiguity.** Ask one short question if its answer would materially change safety or eligibility. Otherwise state a reasonable assumption and continue.
3. **Write a mini-protocol first.** Define population, intervention/index factor, comparator, critical outcomes, time points, setting, eligible designs, date/language limits, and exclusions.
4. **Search by evidence layer.** Retrieve current guidelines, high-quality syntheses, primary studies published after the synthesis search date, harms/prognosis evidence, and trial registries as appropriate.
5. **Use parallel tracks when depth matters.** If tools permit, independently search: (a) authoritative guidelines/syntheses, (b) recent primary studies, and (c) contradiction, harms, retraction, or applicability signals. Reconcile the tracks rather than pooling them blindly.
6. **Document the search.** Record source/database, full query, filters, date, result count reviewed, access limitation, and full-text status. Use MeSH plus free-text synonyms when relevant.
7. **Open and verify.** Inspect the source, supplement, protocol, registry, correction, and retraction status when available. Never use a snippet as the evidence.
8. **Handle access failure honestly.** If live browsing, full text, or a required database is unavailable, stop any claim of current or comprehensive coverage. Synthesize only supplied/accessible material, show a reproducible search plan for missing sources, label paywall/abstract-only limits, and list the verification still required.
9. **Extract a clinical evidence ledger.** Population, sample, setting, intervention components, comparator, follow-up, adherence, co-interventions, effect with uncertainty, harms, funding, risk of bias, and directness.
10. **Assess certainty by outcome.** Use a design-appropriate risk-of-bias method and GRADE principles across the body of evidence. Do not call a single study “high-level evidence.”
11. **Interpret effects.** Pair relative and absolute effects for binary outcomes; preserve scale direction and clinical thresholds for continuous outcomes; distinguish statistical from clinical importance.
12. **Resolve apparent contradictions.** Compare population, stage, intervention components/dose, comparator, outcome definition, time point, bias, missing data, sample size, analysis, and publication status.
13. **Translate to practice.** State who the evidence fits, who was excluded, feasible delivery conditions, study dose, monitoring, harms, patient burden, preferences, resources, and uncertainty.

## Contradiction labels

Use one label with a short rationale:

- supports;
- narrows applicability;
- identifies a subgroup hypothesis;
- conflicts;
- supersedes—only when stronger, more direct evidence justifies it.

Newer is not automatically better.

## Output

1. Bottom-line decision
2. Structured question and assumptions
3. Search methods and date
4. Evidence table or ledger
5. Effect, clinical meaning, and certainty for each critical outcome
6. Evidence timeline and conflict analysis
7. Applicability, study dose, harms, and implementation conditions
8. Practical next step
9. Direct links and access limitations

Never state that all literature was searched. State exactly what was searched.
