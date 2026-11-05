---
name: proof-exegesis
description: >-
  Extract conceptual understanding and reusable mathematics from an opaque,
  computational, formal, or highly elaborate proof. Identify its elementary
  mechanism, portable methods, and possible structural generalization while
  preserving assumptions and proof status. Use for understanding and distilling
  proofs, rather than routine exposition editing or generating a new proof.
---

# Proof Exegesis

Treat an existing argument as mathematical evidence to interpret. The aim is to
understand why it works, which ideas can be reused, and what broader structure
it suggests. A short final theorem or a successful formal check does not by
itself provide that understanding.

For a campaign assignment, `honest-conjecture-resolution` selects the question
and integrates the interpretation; return mechanisms, verified claims, and
candidate extensions to that driver. A standalone explanation needs no campaign.

## Recover What Was Actually Proved

Read the exact statement, definitions, assumptions, and substantive dependencies.
For formal proofs, inspect the encoded statement and its axioms; for computational
proofs, identify the enumeration, certificates, coverage, and checking procedure.
Keep a claimed result, a verified derivation under assumptions, and a theorem
about the intended objects distinct. Use the relevant formalization or review
workflow when checking those details is part of the task.

Recover prior interpretations and corrections from the campaign, sibling
repositories, and shared literature. Preserve original proof and source links.
If a gap prevents treating the argument as established, explain the gap and keep
any useful conditional mechanism explicit.

## Read The Argument At Three Levels

Choose the levels that illuminate the proof; not every argument has a useful
description at all three.

- **Elementary mechanism.** Seek the cancellation, bijection, extremal choice,
  convexity argument, or other small mechanism doing the work. Unfold wrappers
  and choose a toy example that retains it. Separate notation and automation
  overhead from essential mathematical prerequisites. A simpler example can
  explain the mechanism without proving the full theorem.
- **Reusable methods.** Isolate constructions and transformations with explicit
  inputs, hypotheses, outputs, and losses. Locate where methods interact and
  why their assumptions are compatible. Test whether a proposed reusable lemma
  genuinely covers different instances. Use `alon-method` for importing a known
  technique and `proof-calculus` if the operations themselves deserve a theory.
- **Structural explanation.** Ask which definitions or laws account for the
  mechanism across a larger class. Formulate the proposed generalization and
  check that the original argument realizes its assumptions. Universal properties,
  dualities, or cohomology can explain something only after their relation to the
  proof is established. Use `grothendieck-rising-sea` when this becomes a sustained
  theory programme.

Move between these views. A small example may reveal a missing hypothesis in a
generalization; a structural theorem may explain an initially mysterious local
identity. Avoid forcing a categorical explanation or elementary proof that the
evidence does not support.

## Check The Distillation

Map each decisive step of the new account to the original argument or supply a
new proof. Preserve quantifiers, constants, conventions, and exceptional cases.
If hypotheses are weakened or the domain enlarged, that is a new mathematical
claim requiring proof. Separately state what is established, what is explanatory
analogy, and what is a candidate extension.

Count imported foundations and the work of checking assumptions when assessing
simplicity. Fewer lines can hide the whole difficulty in a definition or theorem
call. Conversely, substantial infrastructure can be valuable through reuse across
many arguments. Do not equate minimum length with understanding or significance.
An exhaustive proof may remain the available justification even when only part
of its conceptual structure has been recovered; say so without inventing one.

## Produce An Account Others Can Use

Provide the exact theorem and its status, a readable explanation of the central
mechanism, a representative example, and links to the full justification. Add
reusable lemmas or proposed generalizations only with their hypotheses and status.
Keep the original proof accessible so the explanation can be checked against it.

Interpretation or a new presentation is not automatically a new theorem. Record
what the account adds: simpler dependencies, a new proof, a wider scope, a useful
operation, or improved understanding. Independently interesting methods and
structural consequences can justify a separate paper or exploration branch;
distinguish proved contributions from the work such a proposal still needs.

Keep research-specific findings in the campaign's writeups and result records.
Contribute a new generic skill only when the extracted method has a distinct,
reusable workflow, rather than turning every local proof trick into another skill.
