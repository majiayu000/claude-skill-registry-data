---
name: inert-op-screen-to-structural-rule
description: "Find charged operations that never act on the verifier's input distribution by bit-sliced screening over many seeds, ship their removal only under a re-verification gate, then replace the index list with a structural skip rule in the generator. Use when a benchmark's judge charges per executed op and verifies on a sample, and the artefact comes from a generator with conservative guards; on benchmarks with exact verification use the screen for discovery only."
---

# Fuulpelzfänger (inert-op-screen-to-structural-rule)

An **inert op** is a charged operation that the judge counts but that never changes state on any screened input: its
condition and controls are never all set. A **screen** finds such ops by simulation over many seeds. An **index
list** names them by position in one exact op stream. A **structural rule** is a condition in the generator that
stops emitting them, with a named invariant as the reason.

The screen is evidence, not proof. On a sampled verifier the removal ships under a final judge run. On an exact
verifier nothing ships without a proof.

## Use it / leave it

- Use when the judge charges per executed op and verifies on a sample, and the artefact comes from a generator
  whose guards are conservative (it emits ops for cases that cannot occur at that site).
- On benchmarks with exact verification (gas, proof checking, exhaustive tests) use steps 1 to 4 for discovery
  only, then go to step 7 and prove each rule. Ship nothing on a sampled "never fires".
- Leave it when op indices shift on every build and no structural cause can be named: the list would need a
  re-screen per build and step 7 has nothing to work with.
- Check the benchmark's written rules first. If a sampled removal conflicts with their intent, report it and do not
  use it (see `evaluator-scoring-surface-audit`, class "intent conflict").

## Inputs

- The final op stream exactly as judged, after every post-pass.
- A simulator with the judge's semantics.
- The judge's seed derivation.
- A baseline failure density for the artefact before any drop.

## Procedure

1. **Screen.** For every charged op, accumulate the OR over all screened inputs of its fire mask (enclosing
   conditions AND own condition AND every control). Inert = the accumulator is still zero after all seeds. Deadness
   is an intersection over seeds: one firing on one input removes the op from the set.
   Done when a run over one seed prints the count of never-fired charged ops.

2. **Two modes.** Read `references/screen-spec.md` before implementing; it specifies both modes and the taint pass.
   - **Fast:** force every measurement outcome to 0. That is one valid execution and skips all outcome randomness.
     It is wrong for exactly one family: ops that run under a measurement-dependent condition fire about half the
     time in reality and never under forced zeros. Exclude them by taint analysis and never drop them.
   - **Exact:** use the judge's real outcome randomness, read in bulk per batch.
   Iterate with fast. The list that ships comes from exact.
   Done when, on the same seeds, the fast set is a subset of the exact set.

3. **Engineer for scale.** Loop op-major over a wire-major state so the op list streams once per seed and the
   state stays in cache. Store only the classical bits that are ever read as conditions. In exact mode consume all
   outcome words for stream alignment but store only those that are read. Parallelise over seeds and OR-merge the
   accumulators.
   Done when a full screen fits the machine's memory and its time is written down.

4. **Converge.** Increase the number of screened inputs until the set stops shrinking. Record the set size at each
   doubling. Worked example: the set stabilised near 9 million inputs (1,000 seeds x 9,024). An under-screened set
   is inflated by coincidentally quiet ops and makes clean seeds rare.
   Done when the set size is unchanged across the last doubling.

5. **Screen with the drop disabled; verify with the drop enabled.** Removing ops changes the artefact's bytes, and
   so its seed-derived inputs. The passing seed must be found on the dropped stream. Correctness rests on that
   final judge run of the dropped artefact, not on the screen.
   Done when the dropped artefact passes the judge on its own seed.

6. **Bind the list to the stream.** Store the stream hash with the list and refuse to apply the list to any other
   hash. Any generator change means a re-screen from scratch.
   Done when applying the list to a different stream fails loudly.

7. **Structuralise.** Group the inert ops by the generator site that emitted them. For each group name the
   invariant that makes it inert ("this lane is zero whenever this flag is clear"). Replace the list by a skip rule
   at that site. Keep only rules that pass every channel the judge checks (value, phase, scratch in the worked
   example). Remove the list. Record what the rules do not recover against the list. On an exact benchmark, prove
   each invariant before shipping the rule.
   Done when the artefact builds with no index file and the note lists each rule with its invariant.

## Checks that say it worked

- Set size stable across the last doubling.
- Score drop about equal to the number of dropped ops (each is charged once per sample, so the average falls by
  about one per op).
- Failure density on unscreened seeds about equal to the baseline.
- After step 7 the artefact has no index file, and a generator edit no longer triggers a re-screen.

## Failure modes

- **Fast mode without the taint exclusion.** It drops ops that fire half the time.
- **Under-screening.** The set is too large and clean seeds become rare or absent.
- **A stale list after a generator edit.** Indices now name different ops. Step 6 is the guard.
- **Claiming the drop is exact.** It is exact on the screened support only. Say so in the note.
- **A small sample.** Another solver's note in the same field records ops that looked inactive on 512 samples and
  failed after reseeding.
- **Rules without a named cause.** A skip rule that matches the list but has no invariant is the list again.

## Bundled files

`references/screen-spec.md`: the specification of the fire-mask screen, the two modes, the taint pass, the memory
layout, the list format with its stream binding, and the validation protocol. No source is bundled: the source
campaign's finder is specific to one benchmark's crate and its repository carries no licence file. One companion
tool it references for validation is unpublished; the validation protocol in the reference is written against the
judge or an exact replica instead (see `exact-evaluator-replica`).

## Transfer

- Profile-guided discovery of dead branches in any generated artefact: unreachable guards in a generated contract,
  constraints that are never active in a prover circuit, cases never taken in a generated proof.
- Shipping requires step 7 plus a proof wherever verification is exact.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix; `T:` is a file in the public `ecdsafail-tools` repository. Numbers are quoted; none was re-measured
for this skill.

- The row that introduced the drop, together with one other lever, went from 1156 x 1,381,234 to
  1156 x 1,366,238 (N:66503c19, N:af65258d).
- The structural version held 1153 x 1,367,698 with no list (N:b7958275:4-9). That step is credited to Codex
  (OpenAI) in the note (:21).
- Screen with the drop disabled, hunt with it enabled: N:af65258d:22-26. A schedule change needing a fresh index:
  N:12e55298:19.
- Mechanism sources: T:dead-ccx-finder/find_dead_ccx.rs:1-18 (fire-mask intersection), :139-158 and :184-229
  (forced-zero mode and taint), :298-323 (real randomness, bulk read), README:20 (convergence), :24-34 (modes,
  downstream check), :107-108 (list bound to one stream).
- Provenance: the tool's README calls the lever a reimplementation of "the field's `drop_dead_robust`". The idea
  predates this record. The two-mode finder and the move from list to rules are what the record adds.
