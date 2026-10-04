---
name: shaping-and-betting-work
kind: skill
status: ready
provenance:
  principles:
  - P038
  - P051
  - P062
  - P063
  - P067
  - P104
  - P105
  - P106
  claims:
  - C01466
  - C01492
  - C01493
  - C01495
  - C01496
  - C01497
  - C01498
  - C01499
  - C01615
  - C01616
  - C01617
  - C01618
  - C01619
  - C01620
  - C01621
  - C01511
  evidence:
  - E00479
  - E00486
  - E00487
  - E00488
  - E00489
  - E00490
  - E00491
  - E00492
  - E00509
  - E00510
  - E00511
  - E00512
  - E00513
  - E00514
  - E00515
  - E00493
  source_anchors:
  - 47d5381bbc36-c0000
  - 47d5381bbc36-c0001
  - 47d5381bbc36-c0004
  authored_from_digest: e9d895e952a289483dace8078a4220d287902ac6a5f51677418501c12843f1ce
---

# Shape and bet fixed-appetite work

## Purpose

Turn a raw idea into a bettable piece of work bounded by a fixed *appetite* — the amount of time
the idea is worth — rather than an open-ended estimate, and write it up as a pitch a team can bet
on with confidence. This skill keeps shaping at the right level of abstraction (concrete enough to
make trade-offs, loose enough to leave the team room), surfaces feasibility "time bombs" before the
bet, and judges "good enough" by comparing down to how customers cope today rather than up to an
ideal. It advises, reviews, and compares options; it does not produce the visual/UI design or the
production build, nor does it make the bet for the team.

## When to use

- The caller has a raw idea or feature request and wants it shaped into a bettable scope bounded by
  a fixed appetite before any build commitment (P038).
- A spec, mockup, or requirements document needs reviewing for big design up front or
  over-specification that freezes scope too early (P063, P067).
- The caller wants a concept walked past technical experts to surface feasibility risk *within the
  appetite* before betting (P104).
- The caller is writing or reviewing a pitch and wants it checked for the five ingredients and for
  pairing each problem with a solution (P105).
- The caller is judging whether a project is "good enough to ship" and wants the call framed against
  the baseline customers cope with today rather than against an ideal (P106).
- Do not invoke when the caller wants the shaped work turned into production code or the finished
  UI/visual design, or wants the bet itself made for them — hand those to the owning product team
  and its leadership; to slice a bet into thin end-to-end increments use
  `story-mapping-and-workshops`, and to validate the underlying assumption cheaply before betting
  use `assumptions-hypotheses-and-mvp-experiments`.

## Procedure

Work through the steps in order. Each step names the principle(s) it rests on and states the
trade-off the caller must accept, because every practice here buys one thing at the cost of another.

1. **Scope by appetite, not estimate (P038).** Instead of asking "how long will this take?", fix
   the *appetite* — how much time the idea is worth to the business, set as a time budget for a
   standard-size team. Treat time as fixed and scope as variable, and use the appetite as a creative
   constraint that pushes the team toward a smaller, sharper solution. **Trade-off:** a fixed
   deadline is what forces genuine time/quality/scope trade-offs, and "good" is only relative to the
   time spent — so you deliberately give up the open-ended estimate and the certainty that every
   desirable detail will fit.

2. **Shape at the right level of abstraction (P063).** Keep the concept concrete enough that the
   team can make trade-offs and see what is out of scope, yet loose enough to leave room for their
   creativity. Avoid wireframes or high-fidelity mockups that over-specify the solution too early —
   they are harder to estimate, leave the team no room to solve the problem, and freeze the scope
   you wanted to keep variable. Equally avoid a few vague words that leave the team unable to weigh
   trade-offs or know the boundaries. **Trade-off:** staying at this middle level sacrifices the
   false reassurance of a detailed mockup, but it preserves the variable scope and design freedom
   the appetite depends on.

3. **Eliminate Big Design Up Front; put speed first, aesthetics second (P067).** Do not hand
   engineering a fixed, complete up-front specification, and do not require complete mockups and
   specs before building — a frozen spec cannot adapt when it proves unworkable, when the market
   shifts, or when a lab-perfect concept turns out to lack commercial appeal. Use whatever early
   artifact is fastest to create and communicate, and treat it as transient; reserve polish for the
   later visual-design refinement stage. **Trade-off:** skipping up-front polish feels less
   finished, but over-polishing early artifacts wastes time and makes people less willing to rework
   them.

4. **Find solution elements by moving fast with the right small group (P062).** Explore many
   directions quickly rather than perfecting one, working alone or with a single trusted partner of
   the same background rather than a large committee. Stay at the right abstraction with
   words-not-pictures notation: breadboard the flow as places, affordances, and connection lines,
   and drop to coarse fat-marker sketches only when the idea is fundamentally visual, so the sketch
   stays too rough to over-specify. **Trade-off:** a small, fast group and coarse notation trade
   breadth of early buy-in and visual fidelity for speed and the freedom to discard directions
   cheaply.

5. **Organize the work into independently finishable scopes — by project structure, not by person
   (P051).** Break the shaped work into *scopes*: integrated front-end-and-back-end slices that can
   each be finished independently, rather than task lists handed out per person or role. Capture the
   granular tasks first and factor them into scopes only after real work reveals the true
   interdependencies; the scopes, tracked as to-do lists, then become the project's shared language.
   **Trade-off:** waiting for real work to reveal the boundaries means you cannot draw the final
   scope map up front, but the scopes then reflect how the pieces actually connect rather than an
   org chart.

6. **Walk the concept past technical experts as "just an idea" (P104).** Before writing the pitch
   up, take the concept to people who know the technical terrain, but frame it as "just an idea" so
   they feel free to challenge it, and ask "is this possible *within the appetite*?" rather than the
   open-ended "is this possible?" Actively hunt for time bombs — the parts that could blow the
   budget — and keep the concept malleable by rebuilding it live in front of them and inviting
   radical simplifications. **Trade-off:** exposing an unfinished idea to challenge risks seeing it
   dismantled, but it surfaces the appetite-breaking risks while they are still cheap to design
   around.

7. **Write the pitch with the five ingredients, pairing every problem with a solution (P105).**
   Write the pitch up with all five ingredients: the **problem**, the **appetite**, the
   **solution**, the **rabbit holes** (risky details worth flagging), and the **no-gos** (what is
   explicitly out of scope). Always pair a problem with its solution: never pitch a solution with no
   problem behind it (there is no fitness test for whether it is worth doing), and never bet on a
   problem whose solution is still unshaped (there is nothing concrete to bet on). Define the problem
   as a single, specific story of why the status quo fails. **Trade-off:** naming rabbit holes and
   no-gos up front takes discipline and narrows the apparent flexibility, but it is what makes the
   work safe to bet a fixed appetite on.

8. **Decide when to stop by comparing down to the baseline, not up to an ideal (P106).** Judge
   "good enough" by whether the work already beats how customers cope today — compare *down* to that
   baseline rather than *up* to an imagined ideal. Because shipping on time means shipping something
   imperfect, frame the stop decision as customer value ("this is better than what they have now")
   rather than personal perfection. **Trade-off:** shipping against the baseline means accepting
   known imperfections to hit the date, so name which ones you are choosing to live with — while
   still refusing to lower standards or ship something that fails to beat the status quo.

## Inputs

- The raw idea, feature request, spec, mockup, or draft pitch under review.
- The customer or business outcome it should serve, and the problem story behind it.
- The appetite — how much time the idea is worth — and the team size that budget assumes.
- Constraints: which technical experts are reachable to test feasibility, and what is already known
  versus still assumed.

## Output

A shaping / betting recommendation or critique that:

- states the appetite and confirms scope is being treated as the variable and time as fixed;
- checks the shaped concept sits at the right level of abstraction — concrete enough to trade off,
  loose enough to leave room — and flags big design up front or over-specification;
- names the feasibility "time bombs" surfaced, or still to surface with technical experts, within
  the appetite;
- checks the pitch carries all five ingredients and pairs each problem with a solution;
- frames the good-enough / stop call against the baseline customers cope with today; and
- makes each recommendation's trade-off explicit and ends with a next step tied to the caller's
  appetite.

In **review** mode this is a findings list with remediations; in **advise** mode a single shaping
recommendation; in **compare** mode a side-by-side of scope or bet options ending in an
appetite-weighted pick. The bet, the build, and the visual/UI design stay with the owning product
team and its leadership.

## References

- [`references/product-principles-index.md`](../../references/product-principles-index.md) — full
  statements for the principles this skill applies (P038, P051, P062, P063, P067, P104, P105, P106)
  and their claim/evidence trail.
- Related skills for hand-off:
  [`story-mapping-and-workshops`](../story-mapping-and-workshops/SKILL.md) for slicing a bet into
  thin end-to-end increments, and
  [`assumptions-hypotheses-and-mvp-experiments`](../assumptions-hypotheses-and-mvp-experiments/SKILL.md)
  for validating the underlying assumption cheaply before betting.

## Provenance

Distilled and paraphrased from this package's principles P038, P051, P062, P063, P067, P104, P105,
and P106 (all distillation-only sources — no verbatim text), which synthesise the
shaping-and-betting guidance anchored in Ryan Singer, *Shape Up* (2019), together with related
product-design works. Full principle statements and their claim/evidence trail live in
`references/product-principles-index.md` and the package provenance ledger.
