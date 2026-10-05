---
name: physio-study-appraisal
description: "Appraise rehabilitation PDFs, DOI/PMID, bias, effects and clinical relevance. Use for makale değerlendirme; prefer medical-evidence-research when available."
---

# Physio Study Appraisal

Original standalone scope and trigger coverage: Critically appraise a named or supplied physiotherapy, rehabilitation, or clinical study with design-appropriate methods. Use for a PDF, DOI/PMID, RCT, cohort, diagnostic/prognostic/measurement study, systematic review, meta-analysis, or guideline; and for sample, randomization, blinding, bias, statistics, effect size, clinical significance, MCID, harms, limitations, and applicability. Turkish triggers: çalışma değerlendirmesi, makale kritik analizi, kanıt kalitesi, PEDro, RoB 2, ROBINS-I, AMSTAR, QUADAS, AGREE. Do not confuse reporting checklists with risk-of-bias tools.

## Compatibility and one-workflow routing

When `medical-evidence-research` is actually available, let its matching evidence-answer, search, appraisal or update track own that work and return one integrated answer. A named handoff is not proof that the host loaded the skill. Do not run two complete research workflows or produce duplicate outputs. If the canonical skill is unavailable, complete this skill's original standalone workflow using its local safety and method references below; do not require a paid tool or a sibling package.

For database searches, read [native search strategy](references/search-strategy.md) and [retrieval integrity](references/tool-routing.md). For paper effects and bias, read [appraisal and synthesis](references/appraisal-and-synthesis.md). For a requested evidence update/watch, read [literature watch](references/literature-watch.md). Apply independent human final eligibility for formal reviews, keep found/retrieved/reviewed counts distinct, and retain changed publication records even when an identifier was already seen. The skill itself does not schedule future runs.

## Mandatory first reads

Read [safety core](references/safety-core.md) and [design and appraisal map](references/design-and-appraisal.md). Appraising a study does not validate it for a specific patient. If the request contains urgent clinical features, stop the appraisal-to-treatment handoff and escalate first.

## Workflow

1. **Verify identity and status.** Confirm title, authors, year, journal, DOI/PMID, version, correction/retraction/expression of concern, registration, protocol, funding, and conflicts. If live verification is unavailable, label publication/correction/retraction/registration status **not live-verified**, appraise only the supplied packet, and list the exact checks still required; never infer current status from the PDF alone.
2. **Determine the actual design.** Infer design from methods—not the title or author label. Extract the causal/diagnostic/prognostic/measurement question and unit of allocation/analysis.
3. **Collect the full evidence packet.** Use full text, supplement, protocol, statistical analysis plan, registry, and linked reports when available. Label abstract-only, paywalled, missing-supplement, and offline-status limitations separately.
4. **Separate reporting from validity.** CONSORT, STROBE, PRISMA, STARD, TRIPOD, and RIGHT assess reporting. Apply a design-appropriate risk-of-bias or methodological tool separately.
5. **Audit the sample.** Source population, sampling, eligibility, representativeness, baseline imbalance, sample-size calculation, attrition, exclusions, and vulnerable populations omitted.
6. **Audit intervention/index and comparator.** Components, provider, standardization, study dose, adherence, fidelity, contamination, co-interventions, reference standard, and implementation context.
7. **Audit outcomes.** Prespecification, hierarchy, construct, instrument/version/language, validity, time point, assessor blinding, selective reporting, and multiplicity.
8. **Audit analysis.** Estimand, analysis population, missing-data assumptions, clustering/repeated measures, model assumptions, baseline adjustment, multiple testing, interaction tests, sensitivity analyses, and overfitting.
9. **Interpret effect and uncertainty.** Point estimate, 95% interval, absolute and relative effect, scale direction, clinical threshold, responder analysis, harms, burden, and precision. A p value is not a quality or benefit score.
10. **Apply the method tool transparently.** For every domain, show the source passage/location, rationale, judgment, and missing information. Do not make a confident judgment without the required material.
11. **Assess transportability.** State which people, setting, provider, dose, equipment, follow-up, and co-interventions match—and which do not.
12. **Give a bounded clinical implication.** Classify as supports, conditionally supports, does not change, or argues against practice. Do not prescribe from one paper alone.

## Clinical importance

When MIC/MCID is used, verify construct, instrument/version/language, population, baseline severity, follow-up, direction, anchor, method, and uncertainty. Distinguish MDC/SDC from MIC/MCID. A mean group difference is not an individual response rate.

## Harms

Check how adverse events were defined, solicited, adjudicated, timed, denominated, and reported; whether withdrawals were harm-related; and whether high-risk groups were excluded. **Not reported** is not **none occurred**.

## Output

1. One-sentence verdict: what the study shows and does not show
2. Study map
3. Main effects, uncertainty, clinical meaning, and harms
4. Design-appropriate domain judgments with evidence locations
5. Statistical audit
6. Reporting gaps versus validity threats
7. Applicability and excluded/high-risk groups
8. Limitations and missing information
9. Practice implication and required corroborating evidence
10. Publication status and direct sources

Never collapse reporting quality, risk of bias, certainty of a body of evidence, clinical importance, and applicability into one “scientific quality score.”
