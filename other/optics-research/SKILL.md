---
name: optics-research
description: Guide optics and photonics research when planning experiments, calculating diffraction or imaging, simulating photonic systems, reproducing a paper, or reviewing optics claims. Covers traceable evidence, physical conventions, derivations, and scientific checks.
---

# Optics research

Use the smallest workflow that answers the research question. Do not run every section for every request, or create a research wiki for a one-off answer.

## Start from the question

1. Identify the requested result, available evidence, and observable that would support or refute the proposed explanation. Reuse the user's supplied context.
2. Ask only for missing information that changes the method or conclusion: for example wavelength, geometry, material, coherence, polarization, measured quantity, or an acceptance tolerance. If a symbolic or conditional answer suffices, proceed with explicit assumptions.
3. Choose the relevant workflow and load its guidance as needed. Delegate useful bounded work, including review; evaluate findings against sources, calculations, or measurements rather than model agreement.
4. Distinguish a mechanism explanation, an illustrative simulation, and a reproduction of a specific paper result. A paper used as background does not turn an educational demo into a reproduction audit. If reproduction is requested, keep its acceptance criteria and discrepancies substantive; otherwise build the requested explanation without a separate defense of what it is not.

## Literature and paper reading

Read [Literature and evidence](references/literature.md) for a topic survey, paper reproduction, or scientific review. Use `paper-lookup` to retrieve papers and `citation-management` when checking metadata or producing references. Follow the document-processing skill for PDFs, figures, tables, or OCR.

- For a survey, cover foundational work, recent developments, and relevant counterevidence. Keep search records when useful for ongoing work; include the search method in the deliverable when reproducibility or review scope calls for it.
- Distinguish what the paper reports from your interpretation. An abstract alone cannot verify methods, equations, or supplementary results.
- For reproduction, identify the specific figure or claim, required inputs, numerical conventions, and an acceptance criterion before implementing it.

## Theory and simulation

Read [Optical verification](references/verification.md) for derivations, numerical optics, or quantitative checks. Use `sympy` for symbolic work and `uncertainty-and-units` for dimensional and uncertainty analysis when needed.

- State the governing model, conventions, and approximation regime before applying an equation. Prefer the simplest model that can represent the required observable.
- Use dimensional, limiting-case, analytic, or numerical checks appropriate to the claim. Reuse checks on unchanged models; distinguish symbolic identities from numerical spot checks.
- Keep inputs, solver settings, and relevant convergence results with the calculation. Include method details needed to interpret or reproduce the result, rather than a checklist of performed and unperformed checks.
- Do not assume a commercial solver, GPU, installed package, API credential, or material database is available. Inspect the relevant environment before choosing executable steps; avoid new dependencies unless needed.

## Experiments and analysis

Use `experimental-design` to choose controls and independent replication; use `statistical-power` only when sample-size planning is relevant. Use `statistical-analysis` and `uncertainty-and-units` for inference and error budgets.

- Separate independent experimental repeats from repeated frames, pixels, or technical measurements. Include calibration, drift, background, detector linearity/saturation, and alignment sensitivity when they affect the result.
- Preserve raw measurements. Save processed data separately with units and an explicit transformation history; never silently discard outliers or select favorable runs.
- Test competing physical explanations and relevant controls before attributing a trend to the proposed mechanism. Report effect sizes, uncertainty, and unresolved confounders.
- Treat laser, high-voltage, and motion-control actions as physical operations requiring explicit authorization and applicable lab procedures. Do not infer safe exposure from nominal power alone, operate hardware implicitly, or bypass interlocks.

## Figures, review, and durable results

- Use `scientific-visualization` for data figures and `scientific-writing` for manuscripts. Generate quantitative plots from traceable data/code, with units, normalization, uncertainty where relevant, and processing disclosed. Label conceptual drawings as schematics; do not use generated pictures as evidence or fabricated measurements.
- Review the strongest claim against the actual evidence: identify a concrete failure mode, its consequence, and the check needed to resolve it. Do not invent criticism merely to fill a template.
- For ongoing research, update the project's existing notes with verified decisions, source locators, parameter conventions, reproduction commands, and unresolved questions. Separate hypotheses from established results; avoid creating a parallel notes hierarchy without need.
- Suggest a reusable skill only after a workflow has actually worked repeatedly or the user requests one. Use `workflow-skill-creator` for that task; do not save provisional scientific claims as durable facts.

## Deliver the requested result

Lead with the requested result or artifact. Apply these content decisions to pages, figures, manuscripts, and spoken explanations:

- Describe the implemented model directly: dimensions, propagation method, medium, relevant approximations, and observable. Put shared conditions in the methods or parameter area once; put a specific limitation beside the affected result. Retain source locators, normalization, and material limitations needed for interpretation.
- Distinguish paper-reported values from chosen example inputs at the point of use. For example, label a slider “Example wavelength” and cite the source for a paper-reported parameter. Do not use a generic disclaimer to compensate for misleading provenance or an unsupported quantitative claim.
- Do not introduce a “relationship to the paper,” “not a reproduction,” or verification-status panel by default. A requested comparison, reproduction assessment, or formal limitations section should instead present specific conditions and evidence. A simplified demo can say “One-dimensional scalar angular-spectrum propagation in air”; it does not need to say “explains the mechanism without pretending to reproduce the paper.”
- Omit routine process commentary. Necessary editorial decisions or unresolved production defects belong in native comments or a brief conversation handoff, not captions, footnotes, speaker notes, tooltips, or collapsible panels. Scientific limitations remain visible when they affect interpretation; comments must not conceal them.
- Inspect the rendered or spoken result, including secondary surfaces, for self-defense and editing history. Rewrite useful scope as model facts; remove the rest. Do not print this check. For an unresolved research question, identify a useful next measurement or calculation.

Validate imported measurements and API/file inputs at entry, then reuse normalized internal records and established contracts. Scientific checks of units, assumptions, and numerical accuracy still apply where the model or calculation changes.
