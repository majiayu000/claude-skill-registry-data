---
name: ledger-to-journal-writeup
description: Convert mathematical proof ledgers, historical route notes, exploratory drafts, or campaign archives into journal-style self-contained LaTeX writeups. Use when Codex needs to clean a proof ledger into a polished theorem/proof note, remove chronology and campaign jargon, consolidate current results or chains of one-use lemmas, add definitions/examples/reading guides/dependency maps, audit proof contracts for gaps, extract a proof-only companion note from campaign history, or decide which results should be promoted to theorem-level statements.
---

# Ledger to journal writeup

Use this skill when a proof campaign has produced ledgers, route notes, archived explorations, partial drafts, or long technical proof surfaces, and the task is to produce a precise self-contained writeup suitable for a paper or companion note.

## Core rule

Do not polish chronology. Replace it with the current mathematical state.

A journal-style note should present definitions, statements, proof dependencies, examples, and proof contracts in logical order. Historical attempts, false routes, failed terminology, and old status comments should either disappear or be rewritten as short pedagogical remarks only when they help the reader understand an assumption or obstruction.

The conversion is a proof-audit task, not a prose-cleanup task. Every editorial
change should make one of these things more explicit: the formal data, the
dependency being invoked, the invariant preserved by a reduction, the failure
alternative, or the point where an auxiliary construction returns to the
original theorem.

## Conversion target

The output is not a cleaned diary. It is a reader-facing mathematical object.
For a long proof campaign, aim for these layers in order:

- A compact abstract or status paragraph saying exactly what is proved and what inputs are used.
- A reading guide explaining the proof in passes before technical sections begin.
- Self-contained definitions, with degenerate cases and small examples near the first use.
- A dependency map from the main theorem to the propositions and lemmas that prove it.
- Full proofs with explicit contracts for every nontrivial reduction, repair, quotient, or exactness handoff.
- A short archive or false-route section only when it prevents likely misreadings.

Prefer a proof-only companion note when the proof is long enough to obscure the
main paper. The companion note should still be self-contained: it may cite the
main paper for imported theorems, but not for definitions needed to parse its
own statements.

## Workflow

Use short, repeated passes rather than one large rewrite. A reliable order is:
freeze the source of truth, extract the theorem graph, rebuild definitions,
insert the reader path, audit proof contracts, add local examples, then remove
historical residue. Do not start smoothing prose before the theorem graph and
proof contracts are stable.

### 1. Freeze the source of truth

Before editing, identify the authoritative inputs.

- Current theorem or target statement.
- Clean proof draft or main TeX file.
- Active ledger or status file.
- Historical archive, if it contains provenance but is not itself source of truth.
- Generated artifacts that must stay synchronized, such as PDFs.

State which file will become the reader-facing source. Do not keep multiple parallel proof narratives unless one is explicitly an archive.

Before polishing, write down the current trust level of each source: proved,
conditional, computational evidence, false route, or archive-only. This avoids
quietly promoting old ledger language into theorem prose.

If two files both look authoritative, pick one reader-facing source before
rewriting. The other file should become an archive, a dependency, or a short
pointer; otherwise the proof will drift.

### 2. Extract the current mathematical state

Turn the ledger into a theorem graph.

- List proved statements with exact hypotheses and labels.
- List conditional statements with the missing hypothesis named.
- List open problems separately from proved results.
- List false routes only as exclusions or warnings, not as chronological diary entries.
- Identify proof dependencies: which definitions, lemmas, propositions, and external inputs each main theorem uses.

If a statement is not currently proved in the source text, do not phrase it as proved. If the proof uses a closed theorem from elsewhere, name it explicitly and state the needed form.

Use the theorem graph to decide what to promote. A strong intermediate theorem
should have a standalone statement, clear hypotheses, and a proof that can be
read without campaign context. Local bookkeeping should remain a lemma,
definition, or proof paragraph.

### 3. Build the reader path

Add orientation before technical material.

- Reading guide: explain the proof in a few layers or passes.
- Dependency map: name the formal sequence of lemmas/propositions proving the main theorem.
- Notation table: include symbols that occur across sections or change roles.
- Reusable outputs: identify results that may be cited independently.
- Archive map: tell readers where historical material lives and whether it is required.

Use roadmaps before dense proof blocks, especially before minimal-counterexample arguments, saturation/repair arguments, and long case splits.

For very long arguments, add an audit table with one row per proof stage:
checkpoint, invariant or contract, and what contradiction or output it supplies.
This is often more useful than another prose summary.

The reader path should be local as well as global. Before a dense proof section,
add a paragraph saying what the section proves, which definitions it depends on,
what the main obstruction is, and what the output will be used for.

A dependency map is orientation, not a template for fragmenting the full
proof. Once the reader reaches the proof, present it in mathematical order. If
several intermediate statements are short, consecutive, and used only once,
use descriptive proof steps rather than separate numbered results.

### 4. Rebuild definitions before use

For every technical term, check whether the reader can reconstruct the formal data without reading the history.

- Define objects by their data, not by campaign jargon.
- In notation tables, pair the plain-language interpretation with the actual
  formula, domain, constraints, and normalization. A phrase such as
  “transport cost of a row” does not define the quantity.
- Separate similar notions explicitly, for example graph boundary versus coordinate boundary versus auxiliary checked boundary.
- State degenerate cases and endpoint conventions.
- Give a small example immediately after definitions that encode a non-obvious convention.
- Avoid names like "recursive object", "packet", "row", "top", or "holonomy" unless the formal definition is nearby and self-contained.

A definition should say what counts as valid data and what failure looks like. If later proof steps branch on a failed construction, the failure branch must be part of the definition.

If a campaign term is kept because it is useful, rename it only once and then
define it formally. Do not allow multiple synonyms for the same object to
survive from different historical stages.

Apply a deletion test to coined terminology: if the term can be replaced
everywhere by “a function \(d\) satisfying [short displayed conditions]”
without losing content, delete the coined term and state the conditions
directly. For a standard specialist term, present the defining construction
first and mention the conventional name second.

Prefer definitions that expose the full input-output interface. For example,
when a construction can fail, define both a valid instance and a failure
certificate. When a quotient, boundary, row, top, packet, bridge, gauge, or
holonomy is used, state the underlying set, labels, equivalence relation, and
degenerate cases before using the term in a theorem.

### 5. Audit proof contracts, not just prose

For each nontrivial proof handoff, ask what contract is being used.

- Transport contract: what data is preserved, what auxiliary data is recorded, and what happens at the first failure?
- Reduction contract: does the exit give a strict smaller counterexample, a closed-range contradiction, or a same-support normalization? Keep these distinct.
- Saturation contract: what finite universe is fixed before elimination, and which boundaries/labels are preserved by repairs?
- Quotient contract: which relations are allowed in the quotient, and why are they actual certified relations rather than formal guesses?
- Exactness contract: when potentials exist, why do they define honest potentials on the original object rather than only on a quotient?
- Return contract: after proving a statement for an auxiliary graph, quotient,
  normal form, or repaired object, where exactly is the conclusion transferred
  back to the original theorem?

Replace vague phrases such as "this is harmless", "by transport", "after repair", or "a failed datum gives a reduction" by a cited definition or lemma with explicit alternatives.

Treat this as a correctness pass, not a style pass. The goal is to expose the
data preserved by each move, the finite universe on which a construction is
performed, the exact failure alternative, and the reason the final conclusion
returns to the original theorem.

When a proof uses a minimal counterexample, order the exits explicitly. Say
which exits strictly reduce the counterexample, which exits invoke an already
closed theorem, and which exits only normalize within the same support. This
prevents circular reductions disguised as bookkeeping.

### 6. Add examples and intuition without weakening rigor

Examples should clarify conventions and proof mechanisms.

- Use toy examples with actual finite sets, labels, or small graphs.
- Show both branches of a dichotomy when possible.
- Use examples to explain why a hypothesis is needed or why an invalid shortcut is not allowed.
- Keep intuition subordinate to formal statements: every informal explanation should point to the definition or lemma it illustrates.

Good examples for ledger-to-paper conversions include a square obstruction, an endpoint/gauge convention, a raw packet before saturation, a first-failure certificate, or a small normal-form survivor.

Place examples where they remove ambiguity, not in a separate gallery by
default. A useful example usually illustrates one definition, one convention, or
one proof mechanism, and explicitly says what it is not proving.

Prefer ambiguity-targeted examples over decorative examples. Good insertion
points are immediately after a definition whose name hides several pieces of
data, before a proof where a common shortcut would be invalid, or after a
quotient/exactness statement where the reader might confuse formal relations
with certified relations.

### 7. Promote and demote deliberately

Do not leave important reusable results buried as technical lemmas, but do not over-promote infrastructure.

Promote to theorem/proposition level when a statement:

- has a clean standalone formulation;
- may be cited outside the proof note;
- packages a reusable dictionary, exactness theorem, normal form, or obstruction-elimination result;
- has explicit hypotheses and a complete proof in the writeup.

Keep as lemmas or definitions when a statement is local proof plumbing, bookkeeping, or a one-use algebraic step.

Collapse a linear chain of one-use lemmas into one proof with numbered or
italicized steps. Preserve a named intermediate result only if it is reused,
independently citable, conceptually distinct, or needed to state an exact
handoff. The theorem graph should expose real mathematical dependencies, not
mirror every stage of the discovery process.

When unsure, add a short "Reusable outputs" guide first, then promote after the proof audit stabilizes.

### 8. Remove historical pollution

Delete or archive content that only records how the proof was discovered.

- Remove stale status boxes once results are proved and ported.
- Replace old conjecture language by theorem/proposition language only when proved.
- Move long false-route archaeology to an archive; keep only short warnings that prevent likely misreadings.
- Avoid repeated claims in multiple files. Pick one source of truth and point other files to it.

The active writeup should tell a coherent story, not preserve the campaign timeline.

### 9. Final synchronization

After the source is coherent, synchronize the reader-facing artifacts expected
by the repository.

- Rebuild tracked PDFs or HTML outputs.
- Update dashboards, inventories, or route ledgers so they point to the
  reader-facing source rather than stale historical notes.
- Commit source and generated artifacts together when the repository convention
  expects it.
- Do not leave two active files claiming to be the definitive proof of the same
  theorem.

## Gap-audit checklist

Before calling the writeup journal-ready, verify these items in the current source.

- Every theorem has explicit hypotheses and conclusion.
- Every central term is defined before use.
- Every proof branch has all cases covered.
- Every reduction names the exact order or closed result it invokes.
- Every quotient relation is certified and label-preserving.
- Every repair/saturation step fixes its finite universe before elimination.
- Every exactness conclusion returns to the original object, not only a quotient.
- Every example is consistent with the formal definitions.
- Historical notes are either removed, archived, or clearly marked as nonessential.
- Rendered artifacts are rebuilt when the project tracks them.

## Output discipline

For substantial conversions, produce these reader-facing elements in the TeX source.

- A compact abstract or status paragraph saying what the note proves.
- A reading guide near the beginning.
- A notation table when symbols are dense.
- Roadmaps before long technical sections.
- Self-contained definitions with small examples.
- A dependency map for the main theorem.
- A short archive/provenance map if historical material remains in the repository.

After significant source edits, follow the repository convention for compiling, committing, and pushing source plus generated artifacts.
