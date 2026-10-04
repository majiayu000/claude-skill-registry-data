---
name: discovery-toolbox
license: MIT
description: A routed repertoire of ~90 scientific thinking operators for biological research agents - visual reasoning, detectability and information budgets, search reframing, causal identification, competing explanations, observation and selection processes, pipeline artifact diagnosis, effort allocation, and confirmation hygiene. Use when a screen returns null or weak results, a result looks too good, search has stagnated, a causal claim is being made, an anomaly needs explaining, a pipeline is suspected, or a lead is about to be escalated. Load the smallest relevant section, activate 1-3 operators, then return to the research loop.
---

# DISCOVERY TOOLBOX

**Load on demand, never wholesale.** Route to the smallest relevant section. Usually activate
**1–3 operators**, execute them, then return to the research loop.

The toolbox is a repertoire, not a checklist.

---

## A · VISUAL REASONING

**Trigger:** shape, heterogeneity, ranking, trajectories, subsets, or individual observations may matter.

- **RAW + EXTREMES** — inspect representative raw units, argmax/argmin, and matched non-hits.
- **RANK / SHAPE VIEW** — inspect the full ordered profile or curve, not only thresholds or summary metrics.
- **SMALL MULTIPLES / MULTISCALE** — repeat the same view across subsets, clades, batches, quality strata, sources, time, and analysis scales.
- **RESIDUAL / INFLUENCE VIEW** — inspect residual structure and sensitivity to influential observations/groups.
- **PREDICTED FIGURES** — generate expected visual patterns under competing hypotheses before looking at decisive evidence.
- **CALIBRATED VISUAL INFERENCE** — important visual-only claim → declare the expected pattern, compare against matched nulls/line-ups, and calibrate the visual reader on pure nulls.
- **DISPLAY AUDIT** — if a conclusion depends on axes, aspect ratio, encoding, aggregation, or overplotting, compute it directly or re-render appropriately.

---

## B · INSTRUMENT / DETECTABILITY / INFORMATION

**Trigger:** new screen, weak/null result, uncertain calibration, lossy representation, or multi-fidelity pipeline.

- **PERMANENT CALIBRATION HARNESS** — reusable screen → maintain `structure-preserving null + spike-in/recovery + empirical decoys/negative controls`.
- **TARGET RELIABILITY** — estimate target noise, cross-source agreement, test–retest/version agreement, and effective independent units.
- **POINT → CURVE** — replace a weak point estimate with signal vs `n / noise / quality / aggregation / threshold / scale`.
- **EXISTENCE / INFORMATION BUDGET** — estimate expected detectable hits and whether target information × independent units can support the search space; insufficient capacity → change instrument/design, not estimator.
- **TOY TRUTH** — reproduce a known answer on a toy slice and/or generative simulation before interpreting large-scale nulls.
- **COMMON-CAUSE FIRST** — before explaining individual hits, test screen-wide technical or biological causes.
- **SIGNAL/NOISE AUTOPSY** — assume signal exists; identify what makes it unreadable: target noise, heterogeneity, wrong unit, aggregation, alignment, measurement error, etc.
- **DIFFUSE-SIGNAL SWITCH** — if individual hits fail but the statistic distribution shifts, use whole-distribution/set-level modeling.
- **INFORMATION-LOSS / RATE–DISTORTION AUDIT** — vary compression, aggregation, or preprocessing and locate where target-relevant information disappears.
- **DPI / PROVENANCE LEAKAGE CHECK** — derived features cannot legitimately contain target information unavailable in their declared inputs; violations trigger leakage/provenance investigation.
- **MULTI-FIDELITY RECALL** — cheap filters must preserve top-k/rank behavior at the real operating threshold and in important subgroups; otherwise hedge pruning aggressiveness.
- **UNDETERMINED ≠ NEGATIVE** — pipeline failure, missingness, timeout, or non-convergence is a third outcome; track its structure.

---

## C · SEARCH / REFRAMING

**Trigger:** ideas repeat, experiment space freezes, or marginal exploration yield falls.

- **DUAL-SPACE SEARCH** — track `hypothesis space` and `experiment/measurement space` separately; change whichever is stagnant.
- **LOCAL → STRUCTURAL ANALOGY** — search nearby mechanisms first, then search the relational skeleton of the problem across fields.
- **INVERSE SCREEN** — construct the feature/profile that would explain the phenomenon, then search for nearest real examples.
- **CHANGE THE UNIT** — move coarser/finer or to another causal/biological unit.
- **DECOMPOSE / RECOMBINE** — split composite targets/features; localize the informative component.
- **AUXILIARY TARGET** — solve a related quantity that can be measured better, then transfer back.
- **EINSTELLUNG BREAK / RANDOM RESTART** — run a branch where the dominant approach is forbidden, or restart in another region of search space.
- **BLIND / HIGH-UPSIDE VARIATION** — preserve some exploration not justified by the current model; require justification only before expensive escalation.
- **SPRAY-AND-CUT** — lower per-attempt cost → buy more independent attempts rather than only deeper attempts.
- **INTERMEDIATE MODEL CHAIN** — build a sequence of simplified models and treat the residual sequence as the discovery object.
- **POSE THE NEXT QUESTION** — after each useful screen, ask what sharper question or measurement it newly makes possible.

---

## D · CAUSAL IDENTIFICATION

**Trigger:** causal/mechanistic interpretation, comparative/natural experiment, or major covariate adjustment.

- **IDENTIFICATION BEFORE ESTIMATOR** — state the causal quantity, ideal experiment, identifying variation, and unit of inference. No identifying variation → descriptive claim.
- **EXOGENOUS-VARIATION SWEEP** — actively search thresholds, timing accidents, protocol/software changes, rollouts, natural discontinuities, independent transitions, and other quasi-experiments.
- **DESIGNED CONTRAST** — remove confounding by design when possible: matched pairs, within-unit changes, independent origins, decoupled subsets, change points.
- **BOUNDS FIRST** — weak identification → report what the data permit under minimal assumptions, then show what additional assumptions narrow.
- **ONTOLOGY / TARGET POPULATION** — state which unit and population the estimate actually describes; do not silently generalize beyond the identifying contrast.
- **PLACEBO / PRE-TREND BATTERY** — test outcomes, periods, populations, or thresholds the proposed mechanism should not affect.
- **CONFOUNDER-STRENGTH SENSITIVITY** — quantify how strong an unmeasured confounder must be to overturn the result.
- **SELECTION TRAJECTORY** — ask why units entered the exposed/selected group and whether they were already changing before selection.
- **NUISANCE-MODEL DISAGREEMENT** — result depends on adjustment choice → identify and test the assumption causing the disagreement.
- **COMPARISON-WEIGHT AUDIT** — pooled estimate → inspect which elementary comparisons actually contribute and with what weights.

---

## E · COMPETING EXPLANATIONS

**Trigger:** a lead may deserve concentration of resources.

- **ACH / NONE-OF-THE-ABOVE** — compare evidence across competing hypotheses; discard evidence compatible with all; retain an unconceived-alternative row.
- **DIAGNOSTICITY GATE** — if possible test outcomes do not separate hypotheses, choose another test.
- **DIFFERENTIAL MEASUREMENT** — find the measurement where the leading explanations predict different values.
- **LOCARD TRACE** — each mechanism/artifact should leave collateral traces elsewhere; search for them.
- **PAIRED ABLATIONS** — `destroy mechanism, preserve cue` + `destroy cue, preserve mechanism`.
- **PERTURBATION / SPECIFICATION STABILITY** — vary defensible subsets, transformations, nuisance models, thresholds, seeds, and analysis choices; distinguish robustness distribution from knob attribution.
- **ERROR BUDGET** — express plausible systematic errors in the effect's units.
- **SOURCE-INDEPENDENCE CHECK** — apparently independent evidence sharing collection, ontology, preprocessing, or labels counts as less than independent.
- **ELIMINATION LEDGER** — track `UNTOUCHED / ALIVE / WOUNDED / DEAD` and the observation that changed state.
- **ALTERNATIVE / COLD DERIVATION** — reproduce representative results by a structurally different route, or with artifacts stripped of the original narrative.

---

## F · OBSERVATION / SELECTION PROCESS

**Trigger:** filtering, missingness, uneven effort, curation, historical data, protocol drift, or provenance may shape the dataset.

- **OBSERVATION-PROCESS AUDIT** — map `generation → measurement → collection → inclusion → QC → preprocessing → loaded data`; record what each stage removes and what removal correlates with.
- **ABSENT / UNDETECTED / REMOVED** — distinguish these explicitly; recover upstream QC/filter information when needed.
- **CHAIN OF CUSTODY** — trace important derived variables/results back to raw measurements; broken provenance is a leakage/contamination alarm.
- **COVERAGE-STANDARDIZED COMPARISON** — unequal measurement/observation effort → compare equivalent coverage/information, not merely equal row count.
- **ACTUALISTIC CALIBRATION** — pass known/synthetic material through the real inclusion/QC/join pipeline and measure what survives.
- **PALIMPSEST / ERA DETECTION** — detect hidden protocol, schema, curator, or collection-era strata from missingness/provenance patterns.
- **PRESERVATION-PROXY CHECK** — test whether completeness, observation effort, metadata richness, collection date, or similar archive variables explain the result.
- **SAMPLING-INDUCED GRADIENT CHECK** — apparent gradual onset/decay or endpoints may arise from incomplete sampling; simulate abrupt truth through the observed sampling process.

---

## G · PIPELINE / ARTIFACT DIAGNOSIS

**Trigger:** spectacular result, unexplained change, replication failure, or suspicious software/data behavior.

- **CHECK THE PLUG** — files, row alignment, labels, units, joins, versions, executed code, and outputs.
- **DETERMINISTIC MINIMAL REPRODUCER** — fix randomness and reduce to the smallest input that reproduces the effect.
- **PIPELINE BISECTION** — inject known-good signal and bisect where it is lost/corrupted.
- **INVARIANTS + LOUD ASSERTIONS** — specify what each transformation must preserve and fail loudly when violated.
- **COUNT TWO WAYS** — derive headline quantities through another implementation/path.
- **FAULT TREE + FAULT INJECTION** — enumerate plausible failures, deliberately inject them, and identify silent holes.
- **REINTRODUCE / SAME-HOLE SWEEP** — restored bug should restore artifact; then inspect all prior results exposed to the same failure mode.
- **BISECT HISTORY** — binary-search changes when behavior shifted.
- **INHERITED-CONSTANT / VERSION AUDIT** — unexpected yield → inspect mappings, annotations, external constants, resource versions, and producer semantics.
- **TIME-REVERSE THE ANALYST** — trace backward from claim through every decision capable of changing it.

---

## H · ALLOCATION / DEPTH

**Trigger:** deciding breadth vs depth or where to spend scarce resources.

- **BINDING-RESOURCE COST** — price actions by what actually limits progress: attention, samples, experimental latency, compute, or wall time.
- **CAPABILITY-CALIBRATED COST** — do not import human labor estimates; prototype when uncertain and measure actual agent/tool cost.
- **OUTSIDE VIEW + EXPECTED YIELD** — use previous run/base-rate performance before detailed inside-view forecasting.
- **INFORMATION-GAIN ORDERING** — prefer tests that most efficiently partition the live hypothesis space.
- **MARGINAL-YIELD SWITCH** — continue an arm while its expected yield beats a fresh start.
- **DEPTH SWITCH** — a few leads dominate on `upside × evidence × discriminability` → stop widening and invest heavily.
- **ADVENTUROUS TAIL** — preserve capacity for coherent high-upside/high-variance research.
- **MARGINAL VALUE / REDUNDANCY** — value additions relative to capabilities already present, not in isolation.

---

## I · CONFIRMATION / HYGIENE

**Trigger:** a lead may become a scientific claim, or infrastructure is being reused long-term.

- **INDEPENDENT CONFIRMATION** — prefer a genuinely independent data-generating process; freeze the claim/analysis first.
- **CONFIRMATION DIVERSITY** — spend limited confirmation resources across different mechanisms/explanations, not redundant top ranks.
- **INVARIANCE / ORTHOGONAL CONSEQUENCE** — test properties predicted by the mechanism that leading artifacts have little reason to reproduce.
- **TRANSFER TEST** — check structure in a genuinely different regime, cohort, clade, source, or measurement system.
- **WINNER'S-CURSE AWARENESS** — discovery effect size is not the expected confirmation effect.
- **SUCCESS POST-MORTEM** — ask whether diagnostics would have caught an artifact version of a successful result.
- **ASSUMPTION REGISTER** — track consequential `chosen/inherited × tested/untested` assumptions.
- **OMITTED / FILTERED / EXCLUDED** — important removals must remain recoverable and auditable.
- **PROGRESSIVE vs DEGENERATING** — prefer modifications that predict something new over those that only rescue the existing claim.

---

## ROUTER

```
visual structure                          → A
calibration / weak signal / information / filters → B
search stagnation / reframing             → C
causal interpretation                     → D
competing explanations                    → E
selection / missingness / provenance      → F
pipeline suspicion                        → G
allocation / depth                        → H
confirmation / assumptions                → I
```

**Default: activate 1–3 operators.** More only when independently useful.

The toolbox exists to expose **non-obvious moves** the agent might otherwise miss. Standard methods
need not be restated unless a specific construction changes the reasoning.
