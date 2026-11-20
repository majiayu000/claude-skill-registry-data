---
name: lean-formalize
description: "Formalize a mathematical claim in Lean, continue an incomplete Lean proof, or audit whether a Lean project proves the original statement. Connect actual inputs to intermediate lemmas, assemble the target theorem, check its transitive axioms, and provide a reproducible handoff. Use for Lean proof work; use proof-writer for ordinary mathematical drafting."
---

# Lean Formalize

Turn the user's mathematical statement into a checked Lean theorem with its
meaning preserved. A compiled conditional lemma is progress; completion concerns
the original statement and the trust basis actually used.

## Scope and entry

Follow the requested scope: implement, continue, audit, or package. For an audit,
inspect and report rather than silently repairing or weakening the theorem.
For implementation, continue through the remaining interfaces and top-level
assembly; do not stop after the first successful compilation.

Read the authoritative statement, existing Lean entry point, toolchain and
lockfile, and latest progress record. Reuse the project and its document names.
Do not reinstall tools, change dependencies, or start a new proof framework when
the existing environment is suitable. Resolve APIs against the pinned library.

Use the existing proof route when it works. If the mathematical argument itself
is missing, isolate that obligation and use `proof-writer` or ordinary proof work;
syntax automation cannot discharge an unproved premise. Do not promise that an
arbitrary open problem can be formalized or solved.

## 1. Fix meaning before implementation

Record a short mathematical specification, or reference the existing one:

- Objects, domains, quantifiers, original hypotheses, and conclusion.
- Equivalence of convenient representations to the original objects.
- User constraints on computation, external certificates, and logical foundations.
- The Lean declarations intended to express and prove the result.

Separate original hypotheses from properties introduced by a reduction. Identify
where finiteness, nonemptiness, decidability, normalization, and index conventions
change the statement or require a bridge. Check plausible vacuity and quantifier
failures in the actual theorem, rather than inventing unrelated edge cases.

Keep specification changes explicit. If a repair needs stronger hypotheses or a
weaker conclusion, record the changed theorem and which original obligation is
still open. A proved variant does not complete the original request.

For a substantial new formalization, obtain an independent back-translation of
the definitions and target when review resources are available. Give the reader
the actual declarations, not just an explanation of their intended meaning.

## 2. Design the connections, then build useful pieces

Map the path from an arbitrary original input to the conclusion. For every
substantial interface, record:

| Declaration / obligation | What it assumes | Where actual inputs come from | Evidence / remaining gap |
|---|---|---|---|
|A conditional result|Its extra hypotheses|A named construction or theorem from the original input|Actual state|

Prioritize the highest unclosed connection. In particular, distinguish:

1. A formula or certificate computes the desired number.
2. The actual mathematical object realizes that formula or certificate.
3. The computed fact implies the original conclusion.

All three may require separate proofs. A structure that stores its desired
properties as fields, a supplied probability bound, or an assumption equivalent
to the conclusion does not remove the obligation to construct that input.

Use conditional lemmas as development interfaces, explicitly marked as such.
Keep incomplete experiments outside the certified target's dependency chain;
any temporary `sorry` remains visible as unfinished work and cannot survive the
final target audit. Prefer enough intermediate compilation to localize errors,
without interpreting file counts or proved arithmetic statements as completion.

Split parallel work along stable lemma signatures and module ownership. Give
each worker its assumptions, conclusion, dependencies, and concrete compile
target. Integrate its result against the actual caller before closing the ledger.
Do not let parallel workers silently redefine shared objects to suit their proofs.

## 3. Use computation with a proved interpretation

Distinguish finite examples, exhaustive computation over a proved domain,
checked certificates, and symbolic/general proof. A bounded search is evidence
about its searched inputs. Exhaustive finite verification can be a proof when
coverage, encoding correspondence, and the verification procedure are established
and the user's constraints permit it.

For numeric arguments, use exact arithmetic where the claim needs exactness.
Prove the connection between actual objects/events and the finite data before
using the numeric conclusion. Document conventions that matter: ordered versus
unordered pairs, multiplicities, indices, zero cases, and rounding.

Agree on the intended trust basis from the specification and project conventions.
Do not silently introduce axioms or compiler-backed computation to make an
otherwise incomplete kernel-level proof appear complete. Conversely, do not turn
one project's prohibition on enumeration or `native_decide` into a universal
ban. Explain any extra trust assumption and whether it satisfies this task.

## 4. Review the mathematical obligations that remain uncertain

Use `proof-checker` for the existing ARIS proof-audit/submission role. This skill
does not replace its artifact or reviewer contract. Where installed, use
`research-review` / `auto-review-loop` for targeted discussion and repair, with
the current host's reviewer routing.

For direct model consultations, use available authorized tools and their actual
contracts. A Grok or Antigravity MCP consultation is not automatically an ARIS
reviewer overlay. Do not hard-code vendor availability, quotas, retry counts,
proxy settings, or a particular model into the portable workflow.

Ask concrete questions: translate this declaration; discharge these caller
hypotheses; find a counterexample to this new lemma; check this reduction's
coverage. Preserve raw responses, actual reading/execution scope, and the
executor's disposition of each issue. Model agreement is not a proof. Same-family
opinions remain provisional; cross-family opinions are additional review
evidence, not mathematical truth certificates.

Failed, empty, interrupted, or timed-out calls supply no review verdict. Retry
only within current authorization and provider rules. A later success does not
retroactively turn a failed call into a pass. If a specifically requested review
remains unavailable, report it separately from the formal proof's actual status.

Review at meaningful boundaries: initial statement alignment, a new high-risk
lemma or substantive repair, and final assembly when required by the task.
Stop when the obligations and requested checks are closed. Do not seek repeated
agreement without a concrete unresolved question.

## 5. Verify the actual final target

Use [references/verification-and-handoff.md](references/verification-and-handoff.md)
when preparing the final build, trust audit, or portable package.

For completed delivery, establish the applicable evidence below. Keep a proved
theorem distinct from any still-pending reproduction or review requirement:

- **A theorem exists:** the target has a proof, not only a `def ... : Prop`.
- **Statement alignment:** its expanded type and definitions express the original
  claim; no internal profile, certificate-validity, coverage, or success premise
  is left for the user to supply unless the original claim included it.
- **Actual assembly:** reductions, cases, witnesses, and return to the original
  conclusion are connected, with all caller hypotheses discharged.
- **Executed verification:** explicitly build the module that proves the target
  and print its type and transitive axioms. For a multi-module project, also
  independently import the actual entry point to check its exported result.
  Direct compilation plus type/axiom output suffices for a small self-contained
  file; do not build a new project just to create another import. Save commands,
  exit status, and output. A successful build of a different root module does
  not count.
- **Trust accounting:** no `sorryAx` or unapproved extra axiom lies on the target's
  dependency chain. Explain the actual dependencies against the intended basis;
  the required list need not be exactly any fixed set of axiom names.
- **Reproducibility:** retain the relevant source and pinned environment, and
  provide commands that another reader can run.

These checks establish the formal result under its stated foundations. A prose
proof or HTML edition requires its own correspondence check; Lean does not certify
every sentence in a separate exposition. An explicitly required import audit,
external reproduction, or review may remain pending even after the formal theorem
is checked. Report that missing evidence as such, not as a newly discovered
mathematical gap.

## 6. Persist and hand off the evidence actually obtained

Reuse the existing specification, proof ledger, and continuation file. A short
progress report plus Lean sources, lockfiles, an audit entry point, and logs is
usually enough. Add new files only for a concrete reader or execution need.

Report distinct facts rather than a single ambiguous PASS:

- Original theorem: checked, partial, changed claim only, or disproved by a
  verified counterexample; name the declaration and any remaining obligation.
- Statement alignment and the actual logical trust basis.
- Reproduction: existing/incremental build, clean project rebuild, or another
  person's independent reproduction—whichever actually happened.
- Reviews: who read what, who ran code, and any requested review still pending.

For unfinished work, save the smallest remaining mathematical/Lean obligation,
its known dependencies, the last useful error, and the next action. For completed
work, record completion so the next session does not revive obsolete gaps.

If a research wiki is active, update the affected claim through the existing
`research-wiki` / `proof-checker` workflow with precise evidence and scope; do not
overwrite its generated graph or invent a second acceptance format. Literature
search should resolve a mathematical gap, API question, or relevant prior result,
not become an unrelated requirement to exhaust the literature.

For handoff, provide a reader-oriented proof, source, pinned dependencies,
independent audit command, and known trust boundary. Use `render-html` when a
single-file reading edition would help. Source changes require appropriate
rebuild and statement/axiom checks; presentation-only changes require presentation
checks. Do not restart completed proof work solely to satisfy a workflow ritual.
