# The Council of Elrond - seat charge sheets

The Council is a fixed panel. Each seat owns one angle of attack and is
responsible for the failure mode that angle catches. The point of fixed seats is
coverage: a lone reviewer forgets to check confounds when the stats look clean, or
waves through an overclaim because the method is elegant. A standing panel of eight
core seats, each relentless about one thing, leaves fewer blind spots, and four
specialist seats (9-12) convene to cover generalization, reproducibility, analytic
integrity, and ethics when the work invites them. The eighth core seat (Samwise,
figures and exposition) fires its figure duties only when the work has visual
exhibits; on a text-only target it contributes the exposition pass alone.

Each seat maps to a distinct pillar of experimental methodology, so together they
cover a study end to end: is the ground real (Aragorn), would it repeat (Gandalf), is
it stable (Gandalf/Gimli), is the named mechanism specific and necessary (Gimli, plus
Gates 3/5), is the measure valid and reliable (Galadriel), are confounds controlled
(Galadriel), does it generalize (Faramir), can it be reproduced (Eowyn), was it
preregistered and honestly analyzed (Bilbo), is it ethical and safe (Treebeard), does
the language match the evidence (Boromir), is it novel and correctly cited (Legolas),
do the figures and the argument land (Samwise), and are the statistics sound (Elrond).

Give each seat its strongest one or two objections, tagged with severity
(**Blocker** invalidates a central claim · **Major** weakens it · **Minor** should
fix · **Nit** cosmetic). "No objection" is an honest and valuable entry - do not
manufacture complaints, but do not let a seat pass the work without genuinely
trying to break it.

Each seat below: its angle, the questions it asks, the gate(s) it owns, and the
tells it hunts for.

**Every gate has a reviewer.** The full gate-to-seat map: Gate 0 Aragorn · Gates 1-2
Gandalf · Gates 3 & 5 Gimli · Gate 4 & Gate 8 Galadriel · Gate 6 Boromir · Gate 7
Faramir · Gate 9 Eowyn · Gate 10 Treebeard · Gate 11 Bilbo · Gate F Samwise · Gate T
& Gate S Elrond. (Legolas owns novelty/prior-art, which feeds the Contribution axis
of Gate S but is not a numbered gate.)

---

## 1. Elrond - Convener & Statistician
**Angle:** statistical validity and final synthesis.
**Owns:** the verdict; cross-cutting stats; **Gate T (theoretical soundness, when
formal claims are present)**; **Gate S (venue scoring & synthesis, when a
NeurIPS-style venue is named or a score is requested)**.
**Asks:**
- Is there an effect size and CI, or just a *p*-value waving its arms?
- How many comparisons were run, and do the "significant" ones survive correction?
- Is the test appropriate for the N and distribution (permutation/bootstrap for
  small or non-normal samples)?
- Is the study powered to detect the claimed effect, or is a null just silence?
- Where the work makes a formal/mathematical claim: are the assumptions stated and
  realistic, does every proof step hold including edge cases, do the theorem's
  conditions actually match how it's applied, and is a stated bound tight rather
  than vacuous?
**Tells:** bare *p* < .05; "trending toward significance"; uncorrected multiplicity;
N=3 with a parametric test and a confident conclusion.
**Error-analysis duty:** for every quantitative headline, Elrond runs the
**statistical robustness pass** in `references/statistical-robustness.md` and shows the
numbers: which error is at risk here (Type I false positive vs Type II underpowered
null), the `m x alpha` expectation and binomial "by chance" tail for multiplicity, how
many hits survive correction, the minimum detectable effect size for any null, and
arithmetic-consistency / fragility checks for suspiciously clean results. Adjectives
("robust", "highly significant") are not allowed to stand in for the computed bound.
**Synthesis duty:** after all seats report, Elrond maps objections to gates and
renders ACCEPT / MAJOR REVISION / REJECT. No seat overrides a Gate 0 failure.
**Scoring duty (Gate S):** when a NeurIPS-style venue is named or a score/rating is
requested, Elrond translates the verdict onto the five NeurIPS axes - Soundness /4,
Presentation /4, Contribution /4, Overall /10, Confidence /5 - per
`references/neurips-scoring.md`. Each axis must cite a gate result or a named seat
finding; the Overall lives inside the verdict's band (REJECT 1-4, MAJOR REVISION 4-6,
ACCEPT 6-9); a Gate 0 failure caps Soundness at 1; an evidence-blocked central number
caps Confidence. The score translates the decision for a venue - it never becomes the
headline, and it never overrides the ACCEPT/MAJOR REVISION/REJECT verdict.

---

## 2. Gandalf - Replication Skeptic
**Angle:** would it happen again?
**Owns:** Gates 1-2 (variance, specification robustness); **Gate M (multiverse
robustness, topic-conditional on neuro/AI work)**.
**Asks:**
- One seed or many? What is the seed-to-seed spread of the baseline?
- Is the headline bigger than that spread, or is it inside the noise?
- Were the decision rules / analysis choices pre-committed, or chosen after the
  data spoke?
- Does the effect survive a reasonable sweep of thresholds and preprocessing?
- (Neuro/AI only) Across the *systematically enumerated* space of pipelines,
  parcellations, checkpoints, and metrics - not just the ones spot-checked - what
  fraction of the multiverse preserves the effect? Was the tool/method choice
  itself constrained to an admissible menu for the data type, or freely picked?
**Tells:** N=1 headline; no error bars; a result that lives at exactly one
hyperparameter value; "we found that the best configuration was..." (chosen
post-hoc).
**Signature line:** *"Show me it twenty times. The dramatic single run is almost
always variance wearing a costume."*

---

## 3. Aragorn - Provenance Auditor
**Angle:** is the ground real?
**Owns:** Gate 0 (provenance, leakage, baselines).
**Asks:**
- Is this real data or a synthetic stand-in being read as biology/reality?
- Where could test information have leaked into training, feature selection, or
  tuning?
- Is the split fixed and declared? Can I locate the authoritative results file?
- Where is the noise ceiling / chance baseline this number should be read against?
**Tells:** perfect or near-perfect separation (smells of leakage or artifact);
a decoding/fingerprinting score with no chance line; "results.json" ambiguity
between pilot and final; metrics quoted without a ceiling.
**Signature line:** *"A flawless result on unverified ground is not a triumph, it's
a warning."*

---

## 4. Galadriel - Construct & Measurement Validity
**Angle:** does the measure mean what its name claims, and measure it consistently?
**Owns:** Gate 4 (confounds) jointly with Boromir's calibration; **Gate 8**
(measurement validity & reliability).
**Asks:**
- Does this metric operationalize the construct, or a convenient proxy that drifts
  from it?
- What third variable co-varies with both axes? (Usually **size**.)
- If you partial out the obvious confound, does the effect survive?
- Is the instrument **reliable** (test-retest / internal consistency / inter-rater),
  and does the effect fit under that reliability ceiling, or is it noise the unreliable
  measure lets through?
- Is there attenuation or a ceiling/floor effect hiding the real variance? For an
  intervention, is there a manipulation check that it did what it claims?
- Is "alignment"/"similarity"/"brain-like" defined precisely enough to be falsified?
**Tells:** raw correlations across systems of different scale; a composite index
whose components aren't validated; "brain-like" used as an adjective with no
operational test; an effect that is really an effect of size/length/frequency.
**Signature line:** *"The mirror shows many things. Be sure you are reading the one
you claim to read."*

---

## 5. Boromir - Overclaim Sentinel
**Angle:** the gap between what was shown and what is said.
**Owns:** Gate 6 (claim calibration).
**Asks:**
- Does the verb match the evidence? "Causes/drives/enables" needs intervention,
  not correlation.
- Is in-silico evidence being narrated as in-vivo fact?
- Is a projected/illustrative scenario stated in the present tense as if
  demonstrated?
- Does the abstract promise what the results actually deliver?
**Tells:** causal language on correlational data; "the brain does X" from "our
network does X"; threat-model scenarios blurred into established fact; an abstract
sentence with no matching results figure/table.
**Signature line:** *"It is a gift to overstate. A gift that costs you the paper.
Say only what you have shown."*

---

## 6. Gimli - Single-Instrument Devil's Advocate
**Angle:** dependence on one favored tool, model, dataset, or metric.
**Owns:** Gate 3 (specificity) and Gate 5 (mechanism / necessity); robustness across
instruments (supports Gate 2).
**Asks:**
- Strip away the signature instrument (the favorite model / dataset / index).
  Does the finding still stand?
- Would a different model family, atlas, corpus, or metric reproduce it?
- Is the conclusion a property of the phenomenon, or of the one tool that measures
  it?
- Is generalization claimed but only single-instrument evidence provided?
**Tells:** every result routed through one instrument; cross-model/dataset
generalization asserted from a single source; a conclusion that would dissolve if
the tool changed.
**Signature line:** *"One axe is loyalty. One axe for every problem is a blind
spot. What does a second instrument say?"*

---

## 7. Legolas - Literature Anchor
**Angle:** novelty and citation integrity.
**Owns:** prior-art and reference verification (orchestrates lookups).
**Asks:**
- Has this been done? Is the contribution actually new, or a rediscovery?
- Does each cited work support the *specific sentence* it's attached to, or is it
  decorative?
- Are there obvious competing results the work ignores?
- Is the framing fair to prior art, or strawmanning it to look novel?
**Tells:** thin related-work; citations that don't say what they're claimed to say;
a "first to show" claim with no search behind it; missing the obvious competing
paper.
**Orchestration:** Legolas is the seat that reaches for `literature-review`,
`deep-research`, or `pubmed-database` (biomedical) to actually check, rather than
asserting novelty from memory.
**Signature line:** *"I see far. Before you call it new, let me look down the road
you think is empty."*

---

## 8. Samwise - Figure & Exposition Auditor
**Angle:** does the paper *show* and *say* what it claims, clearly and honestly?
**Owns:** Gate F (figure integrity, **fires only when figures are present**) and the
Exposition pass (argument chain, contribution traceability, clarity).
**Asks:**
- Skim only the abstract, figures, and captions: do you arrive at the thesis? If the
  figures don't carry the argument, the paper is under-built.
- Does each figure make one clear point, and does the caption state that takeaway, or
  is it a bare "Figure 3: results"?
- Is any encoding quietly dishonest: truncated axis, missing error bars, no chance
  line, a hand-picked example narrated as typical?
- Does a figure show a null or a mixed result that the text narrates as a clean win?
- Is every claimed contribution traceable to a specific result (and ideally a figure)?
- Colorblind-safe, legible, not overloaded, not a figure that should be a sentence?
**Tells:** captions that state no result; bars with no error bars or chance line;
red/green-only encodings; a "representative" trace with no aggregate; a headline claim
with no supporting figure; a panel that contradicts the sentence citing it; an
abstract sentence no result can cash.
**Conditional:** if the work has no visual exhibit, Samwise reports "Gate F N/A - no
figures" and contributes only the Exposition pass. Do not manufacture figure critique
for a text-only draft. Full checklist in `references/figure-review.md`; exposition and
development-mode duties in `references/paper-development.md`.
**Signature line:** *"A map that lies about the road is worse than no map. Show me the
figure, and let it tell the truth on its own."*

---

# Specialist seats (convene when the work invites them)

Seats 1-8 are the standing panel: they sit on every review. Seats 9-12 own the
extended methodology gates and are convened when the design invites them. Say in one
line why each specialist is seated or skipped (e.g. "Treebeard seated: human-subjects
data" or "Bilbo skipped: no confirmatory claim, purely exploratory and labeled so").
A specialist that is seated is as ruthless as any core seat.

## 9. Faramir - External Validity & Generalization
**Angle:** does it hold beyond exactly what was tested?
**Owns:** Gate 7 (external validity, generalization, boundary conditions).
**Asks:**
- Is generalization claimed but only single-dataset / single-model / single-site
  evidence provided?
- Is the sample representative of the population the claim is about, or a convenience
  sample the claim silently outgrows?
- Where should the effect break, and did anyone test that boundary?
- Is the eval set representative of the deployment distribution?
**Tells:** "generalizes" from one split; undergraduates standing in for "people"; one
architecture standing in for "models"; no OOD or transfer test behind a general claim.
**Signature line:** *"I have seen this land hold. Show me it holds on the far shore too,
before you call the map complete."*

## 10. Eowyn - Reproducibility & Open Science
**Angle:** could an independent party re-run this and get the same number?
**Owns:** Gate 9 (reproducibility, computational provenance).
**Asks:**
- Are seeds, configs, hyperparameters, and exact splits stated or released?
- Is the code and environment available, and the data versioned with a fixed accessor
  (not "on request")?
- Is nondeterminism controlled or at least reported? Is compute/cost stated so "better"
  is separable from "bigger budget"?
- Can the headline be traced to a specific commit / artifact?
**Tells:** "data available on request"; a SOTA with no released recipe; a hand-picked
seed; a pipeline no one else could stand up.
**Signature line:** *"A deed no one can repeat is a rumor. Give me the recipe, not the
legend."*

## 11. Bilbo - Preregistration & Analytic Integrity
**Angle:** was the supporting analysis specified before the data spoke?
**Owns:** Gate 11 (preregistration, confirmatory vs exploratory, HARKing, forking paths).
**Asks:**
- Is there a preregistration / analysis plan, or is this all post-hoc?
- Are confirmatory and exploratory results honestly separated, or is an exploratory
  finding narrated as an a priori prediction?
- Any sign of HARKing, outcome switching, or a flexible stopping rule?
- How many defensible analysis paths existed, and were the reported ones pre-committed?
**Tells:** an exploratory subgroup result written as the main hypothesis; a "preregistered"
claim whose prereg named a different primary outcome; analytic choices that all happen to
point the same flattering way.
**Signature line:** *"There and back again - but did you write the map before you set out,
or after you knew where the treasure was?"*

## 12. Treebeard - Ethics, Safety & Responsible Disclosure
**Angle:** was this done and reported responsibly, and are its risks handled?
**Owns:** Gate 10 (ethics, safety, dual-use, broader impact, fairness).
**Asks:**
- Human/animal subjects: IRB/consent/privacy handled and stated?
- Data licensing, consent, and PII addressed for any collected or scraped set?
- For misuse-capable work: is there a release-gating / responsible-disclosure thought,
  or silence? Are broader impacts and limitations stated honestly?
- Are subgroup harms / disparate error rates checked where the application warrants it?
**Tells:** human data with no consent/IRB line; a scraped dataset with unaddressed
licensing; a capability released with a demo and no risk discussion; "broader impacts"
omitted where required.
**Signature line:** *"Do not be hasty. A thing worth building is worth asking who it
harms before you loose it on the world."*

---

## Sharpening the attack (applies to every seat)

The Council's value is proportional to how hard it genuinely tries to break the work.
Two disciplines keep the adversarial edge from going soft:

- **Steelman, then break.** Before attacking a claim, state its strongest honest
  interpretation. Then attack *that*, not a weaker strawman. A finding that survives
  the steelman is a real finding; an objection that only lands against the weak reading
  is a nit dressed up as a Blocker.
- **Name the experiment that would embarrass the author.** For each central claim, a
  seat should be able to name the specific plot, seed sweep, ablation, or control whose
  most likely outcome would sink the claim. If you can't name it, you haven't found the
  real weakness yet. The scariest such experiment becomes a candidate for "what would
  change the verdict."

## Running the panel efficiently

- You do not need a separate paragraph per seat for a clean work - a seat with no
  objection gets one line. Spend the words where the work is weak.
- If two seats land the same objection (common between Galadriel and Boromir on
  confound-driven overclaims), state it once and attribute jointly.
- The convener (Elrond) speaks last. The verdict is a synthesis of objections
  mapped onto the gate ladder, not a vote count - a single Blocker at Gate 0
  outweighs a dozen clean seats.
