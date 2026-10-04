---
name: preregister
description: Draft a registry-ready preregistration or preanalysis plan for AsPredicted, OSF, or the AEA RCT Registry. TRIGGER on "preregister", "draft a preregistration", "AsPredicted form", "OSF prereg", "AEA RCT registry", "PAP", "preanalysis plan", or before launching a vignette, conjoint, MTurk/Prolific, or field experiment. Refuses to write one for analyses already run on data already seen.
---

# Preregistration

A preregistration is a written commitment to hypotheses, design, and analysis made before the data
exist or before the realized focal outcome has been seen. It separates confirmatory from
exploratory work and closes off p-hacking, HARKing, and forking paths. This skill writes the
document; the user submits it. To critique a preregistration that already exists, use the
council skill; this one drafts.

Structure and the MUST/SHOULD/MAY taxonomy adapted from `pedrohcgs/claude-code-my-workflow`.

## The refusal gate

Check this before reading anything else, and check it again if new information arrives mid-draft.

Refuse if the description contains realized results: "we found", "the estimate is", "p =", "the
effect was significant", "condition A scored higher", a coefficient, a sample mean, or a figure
of results. Say plainly that a preregistration is forward-looking, that writing one now would
misrepresent the analysis order, and offer instead to write it up as an exploratory analysis or a
methods section, clearly labeled as such.

Refuse in the same way if the user has run the focal analysis on data they hold, even without
stating the numbers. The gate is about analysis order, not about whether numbers appear in the
prompt. Ask directly: has the focal outcome been analyzed on these data yet? If the answer is yes
or evasive, do not write a preregistration.

Two things are not refusals. Preregistering a new confirmatory test on data the user holds but
has not examined for that outcome is legitimate; say so in the document under existing data, and
state what has already been seen. And a purely exploratory study does not need a preregistration
at all, it needs honest labeling, so offer the OSF exploratory variant instead.

## Arguments

- `--style aspredicted|osf|aea-rct`: override the registry choice.
- `--input <path>`: a study spec to read (Markdown draft, Notion export, planning doc section).
- `--format md|tex`: output format, default `md`.
- `--no-verify`: skip the citation checks in phase 5.

## Phase 1. Read the inputs

With `--input`, read the spec and pull out: research question, hypotheses, data source, design,
conditions, sample, primary analysis, any stated `paper_type`.

Without it, ask for a one-to-three paragraph description of the study. If no description comes
back, stop and ask again. Do not write a document made entirely of placeholders.

If the description has no directional hypothesis, ask once. Do not invent a direction.

## Phase 2. Pick the registry

| Signal | Style |
|---|---|
| Online vignette, MTurk or Prolific study, short lab experiment, 1 to 3 DVs | `aspredicted` |
| Conjoint, eye-tracking, multi-DV survey experiment, complex or stratified sampling | `osf` |
| Steering calibration study (confirmatory steering work) | `osf` |
| Field experiment or RCT (livestream pilot, retailer pilot, app A/B test) | `aea-rct` |
| Observational confirmatory analysis | `osf`, preanalysis-plan variant |
| Ambiguous | `aspredicted` |

The 1 to 3 DVs cut is a rule of thumb for form length, not a registry rule.

Steering calibration studies prespecify the sweep protocol, the quality gate, and the audit
battery, plus the primary construct instrument.

AEA RCT registration is required for field experiments at AEA journals (lab experiments are
exempt) and accepted by Marketing Science and Management Science; either OSF or AEA works for
the marketing journals. Clinical trials (ClinicalTrials.gov, ISRCTN) belong in their own
registries and are out of scope here. PROSPERO takes only reviews with health outcomes, so it is
not a destination for a marketing meta-analysis.

## Phase 3. Write the document

Every field gets one flag:

- MUST, the registry will not accept the submission without it
- SHOULD, reviewers and editors expect it even though the form does not force it
- MAY, include when relevant

For any MUST the input did not supply, write `[CLARIFY: <specific question>]`. Never fill a MUST
with plausible-sounding invention.

Common header for all three styles: title, authors, date, version (`v0.1` draft, `v1.0` at
upload), target journal, and a pointer back to the source spec if `--input` was given.

### AsPredicted, the nine questions

1. Have any data been collected for this study already? (MUST, and answer it honestly)
2. What is the main question or hypothesis? (MUST, directional)
3. Key dependent variable(s) and exactly how they are measured (MUST)
4. How many and which conditions participants are assigned to (MUST)
5. Exactly which analyses will test the main hypothesis (MUST, name the estimator)
6. Outliers and exclusions, decided now (MUST)
7. Sample size and stopping rule (MUST, see below)
8. Anything else (SHOULD, put the falsification criterion and power basis here)
9. Name of the study, not the paper (MUST)

### OSF preregistration

Study information (title, description, numbered directional hypotheses) · Design plan (study
type, blinding, design, randomization) · Sampling plan (existing data and what has been seen of
it, collection procedure, sample size, sample size rationale, stopping rule) · Variables
(manipulated, measured, indices, manipulation checks) · Analysis plan (statistical models,
transformations, inference criteria, data exclusion, missing data, exploratory analyses labeled
as exploratory) · Other. All MUST except blinding, indices, and transformations, which are SHOULD
where they apply.

### AEA RCT Registry

Title and abstract · Status (In development, Ongoing, Completed, Withdrawn) · Trial and
intervention start and end dates · Public intervention description (SHOULD; the form does not
star it) · Primary outcomes with how each is constructed · Secondary outcomes · Experimental
design and details · Randomization method and randomization unit · Whether treatment is
clustered · Planned number of clusters, planned number of observations, planned observations per
arm · Power calculation with the minimum detectable effect size for the main outcomes (SHOULD;
the form marks it optional, but the sample-size section below applies regardless) · IRB name,
approval date, approval number (conditional: the form requires them only when the IRB-approval
answer says one exists) · Analysis plan attachment (MAY, and it can be embargoed). Everything
not marked otherwise is MUST.

Do not merge sections across styles. The registries ask for different things.

### Sample size, power, and stopping rule

This field is MUST in every style. That elevation is our own requirement, deliberately
stricter than the registries' forms, kept because a preregistration without a number here
does not bind anything. Record all of:

- the effect size assumed, and where it comes from: a pilot, a prior study with a citation, or
  the smallest effect size of interest. Do not power off a published point estimate without
  saying so, since significance filtering inflates published estimates (Gelman and Carlin 2014 on
  Type S and Type M errors).
- alpha, target power, and the test being powered
- the resulting target N, per cell for experiments, and cluster N plus within-cluster N for field
  designs
- the tool: `pwr` or `simr` in R, `statsmodels.stats.power` in Python, or simulation. Simulate
  rather than use a closed form for clustered or multilevel designs, and carry the ICC and design
  effect.
- the stopping rule, stated so that it does not depend on the data: a fixed N, a fixed calendar
  window, or a quota. Optional stopping is allowed only with a sequential design and its
  correction, named here.

Flag it when the target is an interaction. Data Colada 17 (Simonsohn 2014) gives per-cell
multipliers relative to the two-cell study powered for the simple effect: a fully attenuated
interaction needs 2x the participants per cell, which across four cells is 4x the total N; a 70%
attenuation needs about 4x per cell; a crossover interaction needs only about 1.3-1.5x per cell.
Interactions need far more N than people expect, crossovers are the cheapest case, and an
attenuated interaction powered at main-effect N is underpowered, so preregistering that N locks
in the underpowering.

### What would falsify this

MUST in every style, written as its own field even though only OSF has an obvious slot for
it. This elevation too is our own requirement, deliberately stricter than the registries'
forms, kept because a preregistration that nothing could falsify does not constrain
anything. For each hypothesis, state the pattern of data that would count against it: the sign, the
confidence interval excluding the region of interest, the manipulation check failing, the
predicted moderation not appearing. For any hypothesis predicting no effect, give equivalence
bounds and a TOST test (Lakens 2017), because a non-significant test is not evidence of absence.

Writing this field usually exposes a hypothesis that cannot lose. Say so when it happens.

## Phase 4. Cross-checks

Run all of these before writing to disk. Each failure becomes a `[CLARIFY:]` in place, and the
document still gets written but is reported as INCOMPLETE with the count of unresolved MUSTs.

- Directionality. Every hypothesis carries a sign: "higher than", "increases", "negatively
  predicts". "Is associated with" fails. "No effect" passes only with equivalence bounds.
- Estimator named. The analysis plan names a specific estimator, the software, and the outcome
  variable: `fixest::feols()`, `lme4::lmer()`, `brms::brm()`, `lm()`, `statsmodels.OLS`,
  `linearmodels.PanelOLS`, or a Stata command. "Regression" alone fails.
- Standard errors specified. State the clustering level and why, or state that classical errors
  are appropriate. Follow Abadie, Athey, Imbens and Wooldridge (2023 QJE): cluster where the
  sampling or the treatment assignment is clustered, not by reflex.
- Sample plan numeric, per the section above. "As many as we can recruit" fails.
- Exclusions decided ex ante and stated concretely: attention check failures, completion time
  under a named threshold, duplicate IPs, incomplete responses. "We will deal with outliers"
  fails.
- Internal consistency. If randomized, the unit of randomization matches the unit of analysis or
  the analysis plan handles the clustering. If observational, the identification strategy is
  named.
- Manipulation checks. At least one is named for any lab or survey experiment, where a
  manipulated construct needs verification, and the plan says whether failing participants
  are excluded (decided now, not later). Natural field experiments and A/B tests of
  deployed treatments are exempt: the treatment is the deployed change itself, so there is
  no manipulated construct to check by design. A field study that does run one still
  decides the exclusion rule now.
- Exploratory analyses are in their own section and labeled as exploratory.

## Phase 5. Verify the citations

If the document cites prior literature, and `--no-verify` was not passed, spawn a general-purpose
subagent with the Agent tool and this prompt. Pass the citation strings and the claim each one
supports, not the draft, so the verifier judges the citation independently. Launch it as soon as
the draft's citation list is fixed and keep working: run the Phase 4 cross-checks and write the
file while it runs, then fold the verdict lines into the Phase 6 report when they arrive.

Two checks run on every citation, each with its own verdict line.

Metadata verification: does the cited paper exist, with these authors, year, and venue? This is
the same check `bibcheck` runs, at prereg scale (a handful of citations against a `.bib` of
hundreds), and it uses bibcheck's verdict vocabulary: PASS/WARN/FAIL. For a full `.bib` audit, use
the `bibcheck` skill.

Claim support: does the cited paper actually support the sentence citing it? This check lives
here; bibcheck declares it out of scope, since bibcheck verifies metadata only.

```
Verify these citations independently. For each one, run:

  ~/.claude/skills/reading-papers/scripts/paper.py resolve "<citation>" --json

(The script is a uv self-contained script; run the path directly, it handles its own deps.)

Return two rows per citation.

Metadata row: citation | PASS/WARN/FAIL | DOI | note.
  PASS  a record resolves and title, authors, year, and venue all match as written
  WARN  the paper exists but a field drifts (year, venue, author spelling or truncation)
  FAIL  nothing resolves, or the record is a different paper

Claim-support row: citation | SUPPORTED/UNCLEAR/UNSUPPORTED | note, judged from the resolved
record's title and abstract against the claim attached to the citation.
  SUPPORTED    the abstract is consistent with the claim
  UNCLEAR      the abstract does not settle it; say what would (reading the paper, a named
               section or table)
  UNSUPPORTED  the abstract contradicts the claim, or the paper is about something else
  Skip this row for a metadata FAIL; there is no paper to judge.

Do not read or edit any preregistration draft. Report only what resolve returned.

Citations and the claim each supports:
<list>
```

Surface every WARN, FAIL, UNCLEAR, and UNSUPPORTED in the final report with the offending
citation. Do not silently drop one. A metadata FAIL is either a hallucinated cite or a paper the
resolver could not reach, and the user has to look at it either way.

## Phase 6. Output

Default file: `<project>/prereg_<study-slug>_<YYYYMMDD>.md`. Markdown is the default because
AsPredicted, OSF, and AEA are all web forms the user pastes into, so the field headings should
survive a copy and paste. Use `--format tex` when the preregistration is going into a paper
appendix; then keep the preamble minimal and match whatever the target project already does.

Pick `<project>` by globbing `~/Library/CloudStorage/Dropbox*/Apps/Overleaf/*/` (this setup
assumes Overleaf projects sync there via Dropbox; adjust to your machine) and matching the study to a
directory. If nothing matches, ask where it should go rather than hiding it in a cache directory.

Report to chat:

```
Preregistration draft: <path>
  Style: <aspredicted|osf|aea-rct>   Target journal: <...>
  Status: READY | INCOMPLETE (<n> MUST items unresolved)
  [CLARIFY:] placeholders: <n>  ->  <list them>
  Cross-checks failed: <list, or none>
  Citation metadata: <n> PASS, <n> WARN, <n> FAIL  (or "none to verify")
  Claim support: <n> SUPPORTED, <n> UNCLEAR, <n> UNSUPPORTED
  Upload to: aspredicted.org | osf.io/registries | socialscienceregistry.org
```

## Failure modes

- Description contains results, or the focal analysis has already been run. Refuse, per the gate.
- No testable directional hypothesis and the user declines to give one. Switch to the OSF
  exploratory variant and say in the document header that it is not a confirmatory registration.
- The user wants to amend a preregistration already submitted. Registries handle this through
  formal amendments with a timestamped trail; out of scope.
- The user asks for the power calculation itself to be run. That is a separate job (an R or Python
  script); this skill records the inputs and the resulting N, it does not compute them silently.
- Pilot data exists and is being used for the effect size. Say so explicitly in the document and
  state that the pilot data will be excluded from the confirmatory sample.

## Out of scope

Submitting to any registry, clinical trial and meta-analysis registries, editing an already
submitted preregistration, and running the analysis itself.

Related: the `reading-papers` skill resolves and reads any paper cited here; `compile-latex`
builds the `.tex` output if `--format tex` was used.
