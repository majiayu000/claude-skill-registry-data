---
name: proof-calculus
description: >-
  Develop operations that generate whole families of mathematical arguments,
  together with composition laws and a theorem establishing their validity in
  concrete models. Use when recurring estimates, constructions, substitutions,
  or local-to-global arguments suggest a reusable calculus, or when designing
  such a calculus is the research objective. Goes beyond importing an existing
  technique or introducing another invariant.
---

# Proof Calculus

Ask what operations could produce the arguments we want, and what theorem would
make those operations reliable. Develop a mathematical method that supports new
constructions and proofs. Its value can lie in a family of applications or a new
theory even while the initiating conjecture remains open.

In a campaign, `honest-conjecture-resolution` selects the objective and integrates
the results; this skill owns development of the calculus. Return its proved laws,
models, open obligations, and theory value to that driver without restarting the
campaign workflow.

This can start from repeated proofs, a promising analogy, or operations that do
not yet have a satisfactory interpretation. A large formalized corpus is not a
prerequisite. The operations, admissible models, and central theorem may emerge
together; do not require a finished master theorem before exploration begins.

## Discover The Operations

Recover relevant results and corrections in the current campaign, sibling
repositories, and shared literature before rebuilding a known method. Inspect
actual proofs and constructions, including their hypotheses and failure cases.

Look for actions: composing, substituting, gluing, conditioning, changing base
point, rescaling, decoupling, transporting, completing, or reconstructing. Identify
what the action consumes and produces, why it is useful, and what information
must survive. An invariant can help control an operation; a new name or statistic
alone does not supply a calculus.

Compare representative arguments at the level of mathematical dependencies,
not repeated text or tactic syntax. Apparent duplication may hide different
independence, regularity, positivity, compactness, or cancellation assumptions.
Keep such distinctions visible while seeking a common structure.

## Develop Syntax, Models, And Validity Together

Use these as interacting parts of the research, not a fixed sequence of gates:

- **Expressions and operations.** Specify objects, admissible inputs, outputs,
  and side conditions. Work out composition, substitution, units, relations,
  and interactions where they have mathematical meaning. Operations may be
  partial, noncommutative, or valid only up to a controlled error.
- **Concrete models.** Define how expressions are interpreted in the original
  mathematics. Construct examples and verify the defining assumptions. Include
  quantitative data such as constants, norm scales, error terms, domains, and
  dependencies; an algebraic identity does not provide an analytic bound.
- **Validity theorem.** Seek the theorem that connects admissible expressions
  to actual conclusions: soundness, reconstruction, realization, stability,
  extension, or another appropriate statement. State its quantifiers and
  hypotheses precisely. Separate formal consequences of composition from the
  substantive estimates or existence arguments that make the theorem true.
- **Applications and limits.** Recover known arguments with their exact scope,
  then try different compositions or models. Check equality cases, degenerate
  parameters, order of operations, and accumulation of losses. A failure can
  identify a missing operation or a natural boundary of the theory.

Prove primitive validity and compatibility laws before claiming that arbitrary
composites work. Structural induction may then establish validity for finite
expressions; infinite compositions require their own convergence or continuity
theorem. A rule preserving an inequality can have a different status from a rule
preserving equality. Equivalent expressions need not yield equally sharp bounds.

Choose algebraic or categorical machinery because the operations call for it.
Trees can record nested substitutions; overlapping substitutions need additional
compatibility data. Do not prescribe a Hopf algebra, operad, category, or
cohomology theory before identifying what its laws would express and proving
those laws in the intended models.

## Keep The Difficult Mathematics Visible

A class whose field is the desired inequality offers an interface to that
inequality. It becomes a usable theorem for a concrete model only after the field
has been proved there. Trace where each substantial input enters, and distinguish
an organizational reformulation from a new proof or stronger result.

Soundness is different from expressive completeness and from optimality. A
calculus may certify only some valid arguments and may lose sharp constants.
Do not promise the best bound because a search or type-class engine can compose
the available rules. Track model-construction effort and prerequisites alongside
the apparent shortening of individual proofs; description length is a heuristic
for useful reuse, not a measure of mathematical truth or significance.

In formal code, predicates must express the intended mathematical conditions.
Empty interfaces, `True` witnesses, assumed conclusions, `sorry`, and new axioms
are not implementations of the missing mathematics. Check the statement as well
as its proof and report assumptions and formalization status accurately.

Read [the examples](references/examples.md) when designing an algebra/analysis
interface or evaluating a proposed calculus. They include the regularity-structure
analogy, an elementary composition example, and examples of unsupported transfers.

## Consolidate And Continue

Develop an actual part of the calculus during the work period: a construction,
model, composition law, validity argument, or informative counterexample. Keep
definitions, proofs, remaining obligations, and worked applications together in
the campaign's theory documents. A diagram of proposed operations is a research
plan until its mathematical content has been established.

At natural reviews, assess what can now be constructed or proved systematically,
what examples have become connected, and which hypotheses or losses remain.
Foundations may warrant substantial work before broad applications appear.
Compare with existing methods before claiming novelty, and keep the conjecture's
status separate from the calculus's development. Seek independently interesting
results and propose standalone papers or theory branches when warranted; mere
growth of a case census is insufficient.

Use `grothendieck-rising-sea` for the wider theory programme, `alon-method` for an
existing method import, and `mathematical-framework-design` when the objects or
ambient setting need reconstruction. These are compatible research directions;
none makes an unproved transfer automatic.
