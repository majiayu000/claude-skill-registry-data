---
name: fit-probe-and-splice
description: "Before porting a module from another source tree, measure whether and at what cost it builds under your resource cap (fit probe), then import it verbatim through an adapter that remaps its resources and asserts its contract, instead of rewriting it. Use when a rival's or a library's routine is cheaper than yours, is self-contained, and shares your artefact's op format: a circuit gadget, a prover gadget, a contract library under a size cap."
---

Paths such as `scripts/...`, `references/...` and `assets/...` are relative to this skill's folder.

# Umchleidikabine (fit-probe-and-splice)

A **fit probe** builds a foreign module alone at a list of resource caps and prints, per cap: builds or does not
build, peak resource use, expected cost. A **splice** imports the module's output verbatim through an **adapter**
that runs the module in a private builder, remaps every resource it touched onto the caller's, and asserts the
module's contract. The module's source is copied by closure and not rewritten.

## Use it / leave it

- Use when a routine in another tree is cheaper than yours, is self-contained, and emits the same op format.
- Leave it when the module depends on global layout decisions of its home tree (a fixed register map, a global
  schedule). The closure script's "outside root" and "unresolved" lists are the first test of that.
- Leave it when the module's licence forbids copying. Check before step 2.

## Inputs

- The module's source tree at a pinned commit.
- Your cap and your live resource count at each call site.
- A gate-level or unit test harness.
- A cost counter for the module alone (its own static proxy, or a small judge run).

## Procedure

1. **Fit probe in the donor tree.** Write a test or command that builds the module alone at a given cap and prints
   peak and expected cost. Run it over the caps you care about:
   ```bash
   python3 scripts/fit_probe.py --cmd '<build module alone at cap {cap}>' --caps 825,830,840,852,870,900,975 \
     --label standard-square --tsv fit.tsv
   ```
   Worked example: a standard square "does not build" at six caps from 825 to 900 and costs 50,376 at 975; a flat
   variant builds at 825 for 59,580.5 with peak exactly 825; the routine it would replace cost 89,480 at that site.
   Decide from this table. Done when the table is saved and the decision cites its rows.

2. **Copy by closure.** Copy the module and every file it references transitively:
   ```bash
   python3 scripts/closure.py <donor>/src/module/mod.rs <your-tree>/src/port/ --root <donor>/src > MANIFEST.tsv
   ```
   Edit only paths and visibility, and list each edit in the note. Stub what the module reads from its home tree
   (the cap, a peak constant) in one place. Make unused entry points fail loudly when called.
   Done when the script exits 0, the manifest is committed, and the list of edits has no logic change.

3. **Write the adapter call** `call(kind, registers..., cap)`. The seven parts, in order:
   1. room = cap minus live resources at this site;
   2. **dry build** in a throwaway builder to measure the module's true peak at a given pool; pick the largest pool
      whose measured peak fits the room (`fit_probe.py --room <room>` with the pool as the swept value);
   3. private build with stand-in registers; set the module's cap through its own mechanism;
   4. restore output order when the module may hand results back on permuted wires;
   5. rewrite every op: stand-ins to the caller's registers, every other wire to a fresh caller wire, a shared
      scratch receipt to the caller's, every persistent classical id to a fresh one;
   6. assert that the private builder's live count is back to its base and that no sentinel id reached the stream;
   7. append the ops verbatim with their cost, then free the fresh wires.
   Read `references/adapter-contract.md` before writing it: it gives the reason for each part and the assertion
   that guards it. Done when the adapter builds and its assertions hold at every call site.

4. **Gate test of the adapter** on random inputs for every kind: result exact, inputs restored, all other wires
   zero, every side property the judge checks at zero. Run it at pool sizes on both sides of every cost cliff the
   probe flagged (44 to 48 and 55 in the worked example, around a cliff at 47).
   Done when the test passes at each pool size tried and the sizes are listed.

5. **One switch returns every call site to the old routine.** With the switch off, the build reproduces the
   previous artefact hash (see `lever-switches-and-break-controls`).
   Done when switch-off equals the previous hash.

6. **Inherit and disclose.** List the module's own approximations with their rates, as its authors state them.
   Re-measure the whole artefact's failure rate on salts shared with the base. Recalibrate any static cost proxy:
   foreign ops with unbalanced conditions moved one proxy by 1.5% (see `calibrated-static-cost-proxy`).
   Done when the note carries the inherited approximations and a paired failure-rate table.

7. **Credit the module's authors per routine** in the note, by name and source commit.

## Checks that say it worked

- The fit-probe table is saved.
- `closure.py` exits 0 and a clean checkout builds with no reference into the donor tree.
- The adapter test passes at every pool size tried.
- Switch-off reproduces the previous artefact hash.
- A clean-checkout rebuild reproduces the stamped hash.

## Failure modes

- **A fixed reservation rule instead of a dry build.** In the worked example the rule was one lane too pessimistic,
  pushed several calls under a cost cliff, and cost about 50,000 units.
- **Classical-id collisions between builders.** Remap every persistent id; assert on a sentinel.
- **A module that silently reads a global of its home tree.** Closure by file does not see a global constant
  inside a copied file. Grep the copied files for the home tree's shell items and stub each.
- **Call sites that hold scratch the module could have used.** Release your own scratch before the call.
- **Pool sizes just under a cliff.** One unit of room can cost tens of percent. Probe densely near every cliff.
- **Rewriting "just a little".** A changed line breaks the equivalence with the donor's tested code.

## Bundled files

- `scripts/closure.py` (Python 3 standard library): follows Rust `#[path]`, `mod x;`, `include!`, `include_str!`,
  `include_bytes!`, C `#include "..."`, and extra `--pattern` regexes; copies referenced directories whole; prints
  a sha256 manifest; exits 1 and lists unresolved or outside-root references. `--dry-run`, `--selftest`.
- `scripts/fit_probe.py` (Python 3 standard library): runs a build command per cap or pool size, tabulates builds,
  peak and cost, flags cost cliffs, and with `--room` picks the largest value whose measured peak fits.
  `--selftest`.
- `references/adapter-contract.md`: the adapter's seven parts with reasons and assertions, the gate-test contract,
  and a fit-probe test skeleton for a compiled tree. Read it before step 3.

## Transfer

- Provers: importing a gadget into a circuit with wire and column remapping; the probe asks whether it fits the
  column budget.
- Contracts: inlining a library under a byte cap with a pre-measured byte and gas cost and a storage-slot remap.
- Proof benchmarks: weaker; import plus rename, with the probe asking whether a lemma fits the resource limit.

## Evidence this pays

Citation key: `N:<id8>:<line>` is a public submission note of the source campaign (solver BitWonka, ecdsa.fail)
by id prefix. Numbers are quoted; none was re-measured for this skill.

- Two rows: products and square swapped to routines from other solvers' public trees took a base of 5,304,290
  charged gates at 821 qubits to 4,854,905 and then 4,824,587 at 825 qubits (N:e26536bc heading, N:29c85603:5, 19).
- The square swap alone was -30,317 on the judge (N:29c85603:15).
- Fit-probe table: N:29c85603:57-67. Closure copy of a module file and the 44 files it references, with two listed edits: N:29c85603:69-75, 174-180.
- Adapter: N:29c85603:144-170; dry-build sizing against a fixed rule: :149-153. Gate test on both sides of the
  cliff: :193-200. Switch: :189. Inherited approximations: :202-209. Paired salted panels: :211-218.
- The imported routines are other solvers' work and are credited to them in those notes; the adapter and the
  measurement-first procedure are what this record adds. The adapter source and the closure script are described in
  notes only; the bundled scripts are independent implementations.
