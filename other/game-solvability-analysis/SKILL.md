---
name: "game-solvability-analysis"
description: "Method for exact answers about games: which states are unsolvable or optimal, with exact counts, invariants, certificates, two independent solvers and machine-checked lemmas, plus techniques for dice, solitaire, hidden-information and symmetry problems."
---

# Game solvability analysis

Worked out on the card game Erase (make 10 with +, −, ×), and since applied to every game in
this repository. Sections 1 to 8 are the Erase method; section 9 gives the techniques that
other kinds of games needed, and section 10 the mistakes made along the way.

## 1. Pin down the rules

- Write the rules as a precise model, and list each reading of an ambiguous rule (pairs only,
  addition only, + and −, + − ×, with division, any number of shared cards). Answer each reading
  separately; the answer can change from "very often stuck" to "never stuck".
- Check the source rules (instruction and teacher pages) for the deck composition and scoring.
  Scrape them and quote what they actually say before writing "the authors suggest" or "the
  intended reading is"; a heading such as "Addition and Subtraction" fact set changes what the
  likely intent is. Read every listed variation, not only the one you are studying.
- Settle each ambiguous rule with a test case that pins the behavior down, the way Wordle's
  reply for a guess with repeated letters is fixed by one example (Norvig's Jotto notebook).
- Variations that add jokers or wild cards often reduce to the base game: look for a one-line
  rescue (for make-a-target games, a wild card worth target minus the alternating sum of the
  other cards, sorted, always lies in range), then the stuck count is the base count over a
  larger total.

## 2. Estimate the search and look for a proof

- Follow the evidence order in the root guide. An independent evaluator catches invalid witnesses; a coverage check catches omitted cases. Test a deliberately corrupted witness with optimized Python.

- Solve the general problem first (every value a multiset of cards can make, as in Norvig's
  Countdown notebook), so each specific question becomes a lookup.
- Look at a small slice by hand before the full enumeration (a few dozen deals, every k-th
  pattern), and print it.
- Enumerate value patterns (multisets of values), not ordered deals, and weight each pattern by the
  number of deals it stands for: ∏_v C(4, h_v) · C(4 − h_v, c_v) for hand counts h_v and center
  counts c_v. Check the weights sum to the total number of deals. An unweighted count was 10× off.
- Prune: a hand that clears with no center help clears with any center.
- Use target-directed search (split into a small part A, list A's values, ask whether the rest
  makes the missing value) instead of full value-set enumeration, which runs out of memory around
  seven or eight cards.
- Keep at least two independently written engines and require agreement. Validate the engine on
  published counts (24 game: 1,362 of 1,820 hands; Make 10: 552 of 715 four-digit sets).
- Label exact numbers and simulated ones (sample size and interval) everywhere.
- Recheck any floating-point result near the target exactly with `Fraction` before counting it.
- Define what makes two solutions or deals "different" before counting them, and print that
  definition with the count.
- Put every simulation in one committed script with fixed seeds (`simulate.py`), and quote its
  output in the paper. One-off scripts get lost, and then a printed figure cannot be reproduced.
  Erase used 30,000 deals for its simulations. For another game, size the run for the difference the study needs to resolve and report the number of trials. Cross-check any shortcut solver against
  the general one on a few thousand deals before trusting it.
- Shortcuts that make restricted readings fast: with + only a group is a set that sums to the
  target; with + and −, brackets reach every choice of signs with at least one plus, so a set
  makes the target exactly when some of its cards sum to (total + target) / 2. For "how many
  cards are left under best play", run a bitmask dynamic program over the groups.
- When adding division to a solver, guard every inverse step: never divide by a value that is 0,
  and never ask the other part to make x / t or t · x when x is 0. Two such slips made every
  deal look solvable. Assert a few known impossible sets (6677, and the same with 0s added).
- When a derived notion (here "ten-free") is used both in the prose and in an enumeration script,
  copy its definition from the script, including edge cases (does a single card count as a part?),
  and re-derive one printed number from the stated definition as a check.

## 3. Explain the counts with invariants

- Look at residues mod m. Cards divisible by m are silent. With at most one loud card the value is
  ≡ 0 or ±x; with two, it lies in S(x, y) = {0, ±x, ±y, ±x±y, ±xy}. This gives a congruence
  test; find the few moduli that suffice and show each is needed with a witness deal.
- Look for absorbing elements: a real 0 throws away any cards (the "wastebasket"); two equal cards
  make a homemade 0; cards differing by 1 make a homemade 1.
- Negatives can usually be flipped (if −v is reachable with nonnegative leaves, so is v).
- Bound magnitudes: replacing − by + never decreases |value|; small cases reduce to integer
  complexity (10 needs seven 1s).
- Read-once expressions are affine in each input; that is why one loud card is so weak.

## 4. Reduce the rest to a finite certified statement

- State the remaining fact as a theorem over an explicit finite set of cases, sized to cover the
  game (Erase reserves witnesses outside the two families, then removes a neutral pair. Only sizes 7 and 8 need certificates: 32,939 cases including a subset witness for the exception).
- Emit one certificate per case (an expression string). Check them with a separate program that
  shares no code with the search: enumerate the cases itself, parse with `ast`, allow only the
  permitted operators and card values, compare the multiset of leaves with the case.
- Write generated artifacts deterministically (`gzip.GzipFile(..., mtime=0)`), and do not commit
  large generated files; commit the generator and the checker.
- For impossibility of small cases, encode straight-line programs in z3 bit-vectors with a width
  justified by a magnitude lemma, or run a state-space search (combine two values, repeat).

## 5. Machine-check the hand proofs

- State each induction step for all integers and ask z3 for a counterexample. Write congruences as
  a − b = m·k with an explicit witness k so every goal is quantifier-free.
- Enumerate small finite steps (for example all 121 hand/center residue pairs) directly.
- Say exactly what the machine checked and what the human argument adds (the induction itself).
- Before citing a certified theorem for a new case, check its hypotheses still hold (multiplicity
  limits, value ranges). A wild card can create a fifth copy of a value that the certificates
  never covered.

## 6. Practical play and strategies

- Simulate realistic strategies (greedy pairs first, then arithmetic) and report how often they
  fail on solvable deals; give one concrete trap deal.
- When the cases can be listed, score a strategy on every case rather than a sample, and
  report median, mean, worst case and the cumulative share within each budget of moves.
- Name the proxy metric a strategy optimizes when the true objective cannot be computed
  directly (largest branch, expected branch size, entropy), and compare the metrics.
- Test the "reasonable" restriction for counterexamples: guessing only codes consistent with
  the replies so far is not always best.
- Seed every random choice behind a printed figure.
- Convert per-deal rates to per-game rates for the actual number of players and rounds, and say
  what approximation that needs.

## 7. Repository conventions

- Standard-library solver and counter; z3 scripts separate and optional.
- ruff check and format, pytest smoke tests (a dead deal, a cleared deal with its groups
  re-evaluated, the exception, a slice of freshly generated certificates through the checker).
- When writing up the result, use `results-readme`. Keep the rules and information assumptions that the solver used.
- One commit on a feature branch; amend rather than stack while the PR is unpublished.
- Code a notebook relies on lives in a module that both the notebook and the tests import;
  tests that execute notebook cells break silently when a cell is renamed.
- A small test for the simulation helpers (a parity deal leaves one card, a deal of pairs
  clears), so the seeded script cannot rot unnoticed.

## 8. Final recount

Before release, recompute every printed figure with freshly written scripts that reuse only the
solver, and compare with the text:

- Totals, pattern counts and the split of stuck deals (with a 0 or without, caught by the
  congruence test or not), and "no deal is stuck without being dead" by brute force.
- Every table row: shape shares, the list of hands the test misses with their deal counts, the
  hand-size table for each size, the bar chart, the sample certificates (evaluate each
  expression and compare its cards).
- Every worked example and witness deal: check the claimed moves or obstructions. Distinguish a least blocking modulus from a unique one. Test uniqueness only when the claim requires it.
- Closed forms (parity, pairs only by inclusion and exclusion per hand, any-center, wild cards).
- Rounded statements: compute the unrounded value and round it yourself.
- Outside results: a published count, board or sequence (OEIS) that the same code reproduces.
  Agreement is evidence; disagreement is a finding to explain.
- The facts quoted about related games, recomputed where a short script can do it (how many
  solvable sets need a fraction, whether distinct digits always work), and checked against
  their sources otherwise.
## 9. Other kinds of games

- **Dice and other chance solitaire** (Yahtzee, Tenzi, Peggle's stopping rules): dynamic
  programming over states reduced by symmetry, such as dice as multisets, open boxes as a
  set and the upper total capped at the bonus.
  - Give the whole distribution, not only the mean.
  - Price each rule by solving again without it.
  - Check against the published value (Yahtzee 254.5896), in exact fractions where it is
    feasible, as Kelly and Liese did.
  - Error rates of a stopping rule come exactly from a dynamic program over (games, wins),
    not from simulation.
- **Solitaire search** (FreeCell):
  - Reproduce the published deal generator exactly, and check it against published layouts.
  - Hash a canonical form of the state, and keep a transposition table.
  - Allow only automatic moves that are proved never to lose.
  - Check a second, independently written solver on decks with fewer ranks or suits, where
    brute force decides every deal.
  - A lost deal gets a checkable reason where one exists.
- **Hidden information, cooperation** (Hanabi): the open-hand optimum on a deal bounds every
  convention from above, so it is the ceiling to report scores against.
  - Below the maximum, emit a certificate per deal.
  - Report deals where the solver gave up as undecided, never as lost.
- **Counting up to symmetry** (Drive Ya Nuts, Spot It):
  - Burnside's lemma, weighted by any statistic that is constant on orbits.
  - Check it against direct orbit listing on smaller sizes. Also check that every weighted
    sum is divisible by the group's order.
  - Say which symmetries are counted, such as rotation, relabeling and reflection.
- **Equilibria and optimization** (Pokémon type chart, EV Nova trade routes):
  - Solve linear programs in floats, then verify the solution in exact rationals.
  - Treat best routes as maximum-ratio cycles. Check any published route against the solver.
- **Termination** (Egyptian Ratscrew, beggar-my-neighbour): detect cycles in the full state.
  Look up current results before claiming an open problem: the beggar-my-neighbour question
  was settled by Casella et al. in 2024.
- **What can appear at all** (Boggle):
  - A word is possible exactly when its faces can be matched to distinct cubes.
  - Build a witness board for each possible word, and run the solver on it.
  - Chances of an exact board come from a permanent of face counts (Ryser's formula).

## 10. Mistakes made here

- A critique's script mirrored the Drive Ya Nuts pieces and reported a wrong mean. Rerun any
  objection on the original definitions before acting on it.
- Task briefs carried errors: a wrong co-author, a wrong parameter value, and "every state
  ends", which is false for Ratscrew. Check a brief's factual claims against primary sources,
  as against any other source.
- Simulations meant as independent checks shared their seeds, which made them one check. See
  the `preregistered-experiments` skill.
- A guess on Math StackExchange about which symmetries fix a set was wrong, and the exact
  count showed it. A published or posted claim is evidence, not proof.
