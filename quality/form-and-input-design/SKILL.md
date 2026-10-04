---
name: form-and-input-design
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P003
  - P006
  - P008
  - P017
  - P019
  - P020
  - P031
  - P038
  - P040
  - P059
  - P060
  - P062
  - P063
  - P065
  - P066
  - P086
  claims:
  - C00667
  - C00668
  - C00781
  - C00782
  - C00627
  - C00628
  - C00673
  - C00676
  - C00751
  - C00752
  - C00721
  - C00722
  - C00847
  - C00848
  - C00706
  - C00707
  - C00868
  - C00869
  - C00887
  - C00888
  - C00637
  - C00638
  - C01419
  - C01420
  - C00830
  - C00831
  - C00842
  - C00843
  - C00882
  - C00883
  authored_from_digest: 461a5de5896a67d385e447f8746712ca57acfb708506292ac6e0e520bdfb327b
---

# Form and Input Design

Design forms that respect the user's time and prevent errors at the source.

## When this applies

- You can reasonably guess a field's value (P002).
- Selecting an input control (P003).
- Designing a form that collects information (P006).
- A form has required fields or constrained inputs (P008).

## Procedure

Apply these principles to the situation under review; for each, name the user goal at stake and the trade-off the choice carries.

1. Use smart defaults and prefills deliberately to reduce user work, deriving them from context and choosing them in users' interests, but omit defaults for sensitive choices or when no option fits most people. (P002)
2. Match selection and input controls to the question type, expected behavior, and learned conventions, respecting the trade-offs of radio buttons, checkboxes, drop-downs, list controls, and explicit commit actions. (P003)
3. Design forms to respect the user's time: make them short, minimize and deduce inputs, make the purpose clear (why, how used, what the user gets), minimize clutter, and confirm success with a clear next step. (P006)
4. Solve input validation at the source by using bounded controls that communicate the acceptable boundaries and make an invalid entry impossible (a drop-down of months rather than requiring the user to spell February), rather than an unbounded field that accepts anything only to reject it afterward with a rude error; and where values are finite use a bounded numeric control such as a slider — good for relative or zoom values by analogy of position but poor for precise numbers, for which a spinner is better — or a list control, so users are not forced to type. (P008)
5. Design accessible forms by getting semantic content and structure right first (so assistive tech can convey them) and following core rules: text alternatives and labels for everything, unique meaningful links, never color alone, sufficient contrast, full keyboard operability, no seizure-risk flashing, adjustable timing, skip links, and naming objects by function—benefits reach all users. (P017)
6. Ruthlessly minimize the questions you ask—fewer questions mean faster completion: test every question (need it, infer it, better time), infer answers where possible (e.g., card type from number), challenge legacy paper questions, and apply Keep/Cut/Postpone/Explain. (P019)
7. Use inline validation only where users may need help, time feedback after the answer is complete, and provide suggestions, reformatting, counters, or quality indicators from data already given. (P020)
8. Minimize optional fields, and when marking required/optional status indicate only the minority case with clear text (not just an asterisk), placing indicators next to labels for easy scanning. (P031)
9. Serve minority needs with additional inputs that don't burden the majority: map inputs to prioritized use cases, expose extras via clearly worded user-activated triggers with easy removal, keep the approach consistent, and minimize page jumping. (P038)
10. Choose the selection-dependent pattern by scale: page-level for large dependent sets, vertical tabs over horizontal, a drop-down list for more than 4–5 initial options, expose-within/below for only 1–3 dependents, and avoid exposed-inactive and exposed-groups. (P040)
11. Prevent input errors and validate as early as possible: accept forgiving formats (echoing back the interpreted value) or structured-format fields for predictable data, offer input hints, prompts, autocompletion, and good defaults, and give actionable field-level validation before submission. (P059)
12. Prefer data immunity over data integrity: do not validate and reject imperfect data at the point of entry (which puts the database's needs before the user's and treats the user as working for the application), but build applications smart enough to handle all permutations by looking before they leap, seeking help elsewhere in the system, and annotating problems; assume the user entered what he meant, and since incorrect input is often nearly correct, provide as much correction assistance and visual feedback on suspect entries as possible. (P060)
13. Show form errors in context next to the responsible inputs with actionable guidance and double visual emphasis; when multiple errors may occur, add a prominent top-level summary that matches the per-input styling. (P062)
14. Make success messages non-blocking and in-context, matching the completed task, consider animated auto-removal when only confirmation is needed, and avoid dead ends by offering relevant next steps. (P063)
15. Handle selection-dependent inputs with these tested core rules: hide irrelevant controls until needed, keep initial options and their dependents in close proximity, maintain a clear association to the trigger, and avoid page jumping—these drive speed and satisfaction. (P065)
16. Where possible eliminate the sign-up form via gradual engagement: let people use the service first and defer account creation, which teaches value and boosts adoption—give easy access to auto-created accounts, and don't just split a sign-up form across pages. (P066)
17. Build forms on rich semantic HTML (LABEL for a control, LEGEND/FIELDSET for a group), use CSS for layout, decompose complex structures into simple ones, avoid pixel-perfection across browsers, and separate a form's behavior from its presentation. (P086)

## Principles applied

- **P002** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P003** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P006** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P008** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P017** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P019** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P020** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P031** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P038** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P040** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P059** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P060** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P062** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P063** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P065** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P066** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P086** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P002, P003, P006, P008, P017, P019, P020, P031, P038, P040, P059, P060, P062, P063, P065, P066, P086, their backing claims and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-report.yaml`.
