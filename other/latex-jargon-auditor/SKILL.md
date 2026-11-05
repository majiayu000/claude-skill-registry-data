---
name: latex-jargon-auditor
description: Audit and revise mathematical LaTeX manuscripts for nonstandard, overloaded, vague, or misleading terminology. Use when a user asks to check or remove jargon, make terminology standard or self-explanatory, replace generic words used as technical labels, review theorem or proof names, or perform a focused readability pass on recurring mathematical language. Also use as the dedicated terminology subtask of a comprehensive LaTeX research review.
---

# Mathematical Jargon Audit

Make the manuscript say what its objects and arguments actually are. Do not
turn the audit into a forbidden-word search: retain terminology that is
standard in the relevant literature and used with its standard meaning.

## Governing principle

Do not assign a precise mathematical meaning to a generic word merely because
it is convenient shorthand. Prefer established terminology or a short phrase
that states the object, operation, hypothesis, or parameter range explicitly.

Coin a new term only when the object is genuinely reusable, the name saves a
substantial repeated definition, and a later mathematician might reasonably
state or cite results about it. A one-use function, event, minimizer, proof
step, or list of inequalities almost never needs a new name.

Terminology is part of correctness. A familiar mathematical word used with a
different meaning can make a true statement appear false or invoke unintended
theory. Treat such overloading as more serious than merely inelegant prose.

## Read before auditing

1. Read the root file and every relevant `\input` and `\include` in true
   reading order.
2. Identify the intended field and readership. A term can be standard in one
   field and misleading in another.
3. Read the definitions and proofs before renaming anything. Infer a term's
   meaning from formulas and logical use, not from its suggestive name.
4. If a current PDF exists, use it to distinguish rendered prose from internal
   labels, comments, and filenames.

## Classify every recurring candidate

For each candidate, record its first use, intended mathematical referent, and
one of the following dispositions.

1. **Standard and exact.** Retain it. Give a formula or short gloss at first
   use if readers from an adjacent field may not know it.
2. **Ordinary English.** Retain it when it is used literally in a sentence and
   is not carrying a hidden technical definition.
3. **Nonstandard shorthand.** Replace it by standard terminology or by the
   defining data or properties.
4. **Overloaded mathematical term.** Replace it when its established meaning
   differs from the manuscript's meaning.
5. **Justified new term.** Retain only after giving a formal definition,
   explaining why the object merits a name, and using the name consistently.
   Do not imply that the coinage is established terminology.

Do not assume a term is standard because the manuscript repeats it. If the
classification matters and is uncertain, check authoritative literature in
the relevant field.

## Decision tests

Apply these tests in context.

- **Literature test:** Would a specialist recognize this word with the exact
  definition used here?
- **Type test:** Does the noun identify the correct kind of object--set,
  function, measure, operator, norm, parameter range, or proof step?
- **Data-versus-name test:** If the name is deleted and its displayed
  properties are stated directly, is any mathematical information lost? If
  not, delete the name.
- **First-use test:** Can a reader understand the first occurrence without
  waiting for a later definition?
- **Substitution test:** Can the term be replaced by a short exact phrase
  everywhere without making the prose materially worse? If so, prefer that
  phrase.
- **Citation-value test:** Is the named object likely to be reused or cited
  independently? If not, describe it locally.
- **False-friend test:** Does the term already have a different standard
  meaning, such as endpoint, transport, slice, boundary, influence, capacity,
  orientation, residual, or obstacle problem? If so, require an exact match.
- **Standalone-summary test:** Would the term be intelligible in the abstract,
  introduction, theorem title, table, or conclusion without the nearby proof?

## High-risk vocabulary

The following are prompts for inspection, not automatic errors.

### Geometric and spatial metaphors

Audit `slice`, `section`, `locus`, `endpoint`, `boundary`, `region`, `sector`,
`layer`, `shell`, `fiber`, `bridge`, `frontier`, and `spine`.

- Use **slice** only for a standard slice, such as a Boolean-cube weight level,
  or define the actual intersection. Otherwise write `coordinate fiber`,
  `conditional event`, `level set`, `restriction with x_i fixed`, or the exact
  set.
- Replace **locus** by `zero set`, `solution set`, `support`, `equality set`,
  `set of maximizers`, or `parameter values satisfying ...`.
- Use **endpoint** for an endpoint of an interval or a limiting exponent in an
  interpolation theorem. An unresolved estimate is an `open inequality` or
  `open L^p bound`, not an endpoint merely because it is the final goal.
- Use **boundary** only after specifying which boundary: topological, graph,
  edge, measure-theoretic, a boundary operator, or a boundary condition.
- Retain **fiber** when it means an inverse image under a stated map; otherwise
  state the coordinate pair or level set directly.

### Proof-management and process metaphors

Audit `route`, `mechanism`, `engine`, `pipeline`, `architecture`, `package`,
`gate`, `certificate`, `obstruction`, `bottleneck`, `attack`, `campaign`,
`budget`, `debt`, `round`, `active`, `terminal`, and `odometer`.

Replace these by the mathematical action or status: `reduction`, `induction`,
`construction`, `necessary condition`, `counterexample family`, `remaining
lemma`, `upper bound`, `iteration r`, `event {tau=r}`, `continuing event`, or
`stopping index`. Keep a standard term such as obstruction or certificate only
when the relevant theory defines it.

### Analytical, probabilistic, and algebraic shorthand

Audit `profile`, `scale`, `regime`, `row`, `orientation`, `lift`, `transport`,
`flow`, `source`, `capacity`, `obstacle`, `residual`, `main effect`, `signal`,
and `noise`.

- Replace **profile** by the actual object: `the function q -> beta_q`, `the
  family of moment bounds`, `stability coefficients`, or `radial values`.
- Replace **scale** by `order`, `rate`, `threshold`, `standard deviation`,
  `metric parameter`, or the displayed expression.
- Replace **regime** by the actual parameter range.
- Replace **row** by `coordinate i`, `component`, or `centered derivative`
  unless an array or matrix row is literally present.
- Use **orientation** only for a standard geometric or combinatorial
  orientation. For pair symmetrization, write `selection sign` or state which
  member of each pair is chosen.
- Replace **lift** by `pullback under pi`, `extension constant on fibers`, or
  the exact construction unless lift is standard in the category at hand.
- Use **transport** only for an actual coupling, mass transportation problem,
  Wasserstein/Kantorovich quantity, or a defined flow minimization. Otherwise
  write `transfer`, `comparison`, or `reduction`.
- Use **flow**, **source**, and **capacity** only when tied to a stated
  divergence or network/variational formulation.
- Use **obstacle problem** only for the standard variational inequality with an
  obstacle. Otherwise say `constrained minimization` and state the constraints.
- Retain **residual** and **main effect** only when their decomposition is
  explicit and compatible with standard statistical or Fourier usage.

Also audit empty qualifiers such as `generic`, `natural`, `canonical`,
`appropriate`, `admissible`, `obvious`, and `standard`. Replace them with the
actual quantifier, property, or citation whenever they carry mathematical
content.

## Replacement workflow

1. Build a candidate inventory with contextual searches. Include headings,
   theorem names, captions, tables, proof maps, the abstract, and the
   conclusion. Do not rely on one fixed word list.
2. Group occurrences by meaning. The same word may be standard in one passage
   and misleading in another.
3. Make a replacement map before editing: old term, exact referent,
   disposition, preferred replacement, and any definition that must move.
4. Revise high-visibility prose first: title, abstract, introduction, main
   results, headings, tables, and conclusion.
5. Revise definitions and proofs. Replace proof-process labels by named steps
   that state their operation, hypotheses, or conclusion.
6. Search again for variants, plurals, hyphenations, and related expressions.
   Check terminology consistency across companion papers when relevant.
7. Avoid unnecessary reference churn. Internal filenames and label keys are
   not rendered jargon; rename them only when their old wording risks future
   confusion, and then update every reference systematically.

## Safe editing rules

- Preserve formulas, quantifiers, hypotheses, and logical status. A clearer
  noun phrase must not strengthen a theorem or conceal an open question.
- Do not replace a precise standard term with longer but less accurate prose.
- Define retained specialist terms at first use when they cross disciplinary
  boundaries.
- Avoid replacing one metaphor by another. Prefer the formula or construction.
- Do not introduce abbreviations merely to compensate for removing jargon.
- When one symbol already has a global definition, recall it rather than
  inventing a local synonym.

## Validation and deliverable

After implementation:

1. Rebuild the PDF and scan the log for undefined references, citations,
   overfull boxes, and rerun warnings.
2. Inspect every materially changed rendered page. Terminology changes often
   alter headings, line breaks, tables, and page breaks.
3. Extract or search rendered text for the audited terms. Distinguish surviving
   visible prose from harmless internal identifiers.
4. Review the diff for accidental mathematical changes.
5. Report the principal replacements, the standard terms deliberately
   retained and why, validation performed, and any uncertain term requiring a
   domain expert or literature check.

For a review-only request, provide the candidate map and recommended
replacements without editing. For a review-and-implement request, apply the
well-supported replacements and leave genuinely uncertain terminology flagged
rather than guessing.
