---
name: concentration-inequalities
description: Prove and audit moment or tail bounds for dependent sums, stable functionals, and Rademacher/Walsh chaos. Use when choosing among martingale, decoupling, hypercontractive, bounded-difference, Stein, cumulant, transport, or coefficient methods, especially when a proxy may be lossy or a structural hypothesis may have been mistranslated.
---

# Concentration inequalities for dependent sums and chaos

Use this skill to choose a concentration mechanism and to keep its hypotheses,
norms, and losses aligned with the native problem.  Its main purpose is to
prevent a theorem for a stronger coefficient model or a lossy proxy from being
reported as a theorem under pointwise stability.

## Source of truth and synchronization

This route map is synchronized with dashboard v401, the P219 closure round,
the sharp all-moment saturation round, and the separate small-failure
stable-generalization campaign of the cleaned
StabilityExploration campaign on 2026-07-23.  Before doing
project-specific work, read the current theorem-status ledger and the P219
closure packet.  The complete reader-facing proofs are in `main.tex` and its listed input modules.
Exact reusable counterexamples are in `ROUTE_TOMBSTONES.md`.  Historical
drafts and Git history are provenance only.

The universal linear rate is now proved.  P219 closes P14 through the
capacity-obstacle relocation, sparse obstacle support, and a
support-localized \(L^1\)-\(L^2\) Hessian estimate.  The route map below is
retained as proof provenance and as a catalogue of reusable class theorems
and method walls.  Any phrases such as ``active target'' inside that
pre-closure catalogue are historical unless a later post-closure project
explicitly reopens them.

The full moment-order saturation is also closed.  If
\(q=\min\{p,n\}\), then the sharp worst-case envelope under the BKZ
hypotheses is

    ||sum_i g_i||_p \asymp n beta q + M sqrt(n q).

For \(p\ge n\), the upper cap follows from
\(|g_i|\le M+(n-1)\beta\), obtained by averaging the outside-coordinate
telescoping bound at fixed \(Z_i\).  The BKZ quadratic Rademacher example
reaches \(Mn+\beta n^2\) on the all-positive atom of probability \(2^{-n}\),
so the same family supplies the matching lower bound.  This settles the
\(p\gg n\) moment question.  The distinct sharp
small-failure-probability lower bound for actual uniformly stable algorithms
is now also proved by the winner-margin construction described below.

The small-failure theorem is maintained separately in
`SMALL_DELTA_STABILITY_STATUS.md` and `small_delta_lower_bound.tex`.  Its
exact native object is a bounded sample-dependent query

    q_S : Z -> [0,L],   ||q_S-q_S'||_infinity <= gamma

under one sample replacement, with discrepancy `P q_S-P_n q_S`.  The
formerly unmatched parameter region was

    L^2/(gamma^2 n) <= t <= L/gamma,   gamma >= L/n.

The first lower calibrator is the clipped signed-coordinate construction

    G=(gamma/(2n)) sum_k |D_k| min(|D_k|,L/gamma),

which proves exactly why the elementary quadratic mechanism saturates at
the sampling scale before entering that region.  The decisive construction
instead takes exponentially many independent Rademacher score coordinates
and selects the unique empirical winner with amplitude equal to its
truncated top-two margin.  The map

    W_r(x) = min(x_(1)-x_(2),r) e_w

at a unique winner, and zero at a tie, satisfies

    ||W_r(x)-W_r(y)||_1 <= 2 ||x-y||_infinity.

For a suitable number of scores, a winner above `n/4` with margin `2r`
has probability at least `3^(-r)/20`; the associated bounded stable query
has gap at least `gamma r/16`.  This proves the sharp lower scale

    min(L, gamma t + L sqrt(t/n))

up to universal constants and confidence rescaling, and refutes a universal
improvement to `gamma + L sqrt(t/n)`.

On the class-theorem side, bounded range forces every symmetric additive query
`q_S=b+sum_i h(Z_i,.)` to have actual stability at most `L/n`.  Hence a
sharp lower example must use nonlinear sample interactions.  This theorem
explains the structure of the winner-margin example; it does not extend to
all bounded stable queries.

The final tree is deliberately compressed:

- one closed exact cube target: P14 set transport, proved by P219;
- two exact representations of that same target: P80 cut towers and the
  P83/P85 matched-section endpoint;
- one secondary explicit sufficient successor: P138 Euclidean row transport.  If
  (t_i(f)=\|\partial_i f-\mathbb E\partial_i f\|_{\mathrm{KR}}), it asks for

      (sum_i t_i(1_A)^2)^(1/2) <= C sqrt(n) a log(e/a).

  This implies P14 by Cauchy--Schwarz and is equivalent to the anisotropic
  residual estimate

      ||sum_i Z_i q_i||_p
        <= C (p-1) sqrt(n) (sum_i Lip(q_i)^2)^(1/2).

  P89 implies P138, but twisted majority times a two-bit parity has bounded
  Euclidean row transport and P89 compatible cost of order `sqrt(n)`.
  Therefore independent exact row transports cannot be glued back into one
  dimension-free compatible P89 flow; simultaneous compatibility is excess
  structure for the direct P138 route.  No separation between P138 and P14
  is known.  P89 is now a stronger parked successor.  Its fixed-orbit joint Calderón bilinear
  form is equivalent to P89, not a smaller active crux.  P133 tangent
  recoupling is likewise equivalent to the centered two-scale endpoint and
  is parked.  P134's bounded biased-sign preflight is also complete and
  parked: it proves the sharp \(p=2\) derivative estimate and the all-\(p\)
  common-phase class, but its scalar unsigned transfer loses \(\sqrt n\)
  exactly where cyclic phases cancel the true derivative, while complete
  quadratics saturate the proposed \(p^2\) scale.  A purely skew five-row
  field with zero symmetric Jacobian nevertheless has increasing eighth
  moment under biased-sign interpolation, so symmetric-Jacobian domination
  is false; the full signed rectangle gate remains open.  P135's
  fresh-generation audit adds three exact preflight walls: bounded-order
  labelled Fourier/dual-check data miss an \(\Omega(n)\) separation in
  exact P14 cost; the plain \(L^1\) norm of the exact scalar aggregate
  \(\mathcal LP_{\ge2}f\) loses a linear factor on antipodal and simplex
  codes, although the aggregate itself remains information-complete on the
  relevant degrees; and rectangle holonomy misses the additive transport
  baseline.  A new direct state must see unbounded global section geometry
  and either preserve row-indexed phase or use a genuinely nonlocal,
  degree-sensitive functional of the scalar aggregate.  P141 has now audited
  the three immediate P138 continuations.  Exponentially sparse
  fixed-cardinality fibers satisfy P138, but positive graph assembly loses
  linearly on ordinary majority.  Full random-deletion telescoping forces
  both negative savings with coefficient one and is then exactly the parent
  energy.  Signed resolvent--carré repairs the P140 witness, but the exact
  cube chain rule uses edge-dependent divided differences and becomes P138
  itself.  Finally, thresholding long rows gives a valid diagnostic
  inequality, but separate entropy packing is false: an indexed-majority
  selector has arbitrarily many high rows and constant total entropy while
  its P138 ratio tends to zero.  The shared latent majority transport is
  charged once per label.  Do not continue with separate one-row entropy
  allocation, full-order scalar deletion, or an unweighted signed chain
  rule.  P142 strengthens this wall.  If

      e_i=D(nu||mu)-D(nu_-i||mu_-i),
      r_i=t_i/a,

  then the universal one-row theorem

      r_i^2 <= (n-1) L e_i / log 2

  holds, but an imbalanced equality of two majority signs has arbitrarily
  many high rows with `sum e_i ~ sqrt(k)` at fixed entropy while
  `(K_n/a)^2 <= n/4`.  Thus even native deletion entropy cannot be summed
  rowwise.  P143 has completed the bounded same-geometry preflight for the
  threshold-localized joint-rank estimate

      sum_(i in I_lambda) r_i^2
        <= C n L R_nu(I_lambda),
      R_nu(H)=D(nu||mu)-D(nu_(H^c)||mu_(H^c)).

  With h=|H|, d=n-h, R=R_nu(H), and
  S=log(1/a)-R, the proved conditional split is

      (sum_(i in H) r_i^2)^(1/2)
        <= C [sqrt(d R (1+S))
              + min(h sqrt(R), sqrt(h R)+h^(3/2) R)].

  Therefore joint rank closes when h^2 <= C nL or h^3 R <= C nL.
  Balanced monotone equality compositions obey the stronger bound

      sum_(i in I) r_i^2 <= (n/2) R_nu(I)

  for every I.  The unrestricted internal field is nevertheless an
  arbitrary P138 residual on Q_h.  Conditional descent gives

      sqrt(sum_(i in H) r_i^2)
        <= C_h sqrt(h L R)+C sqrt(d R (1+S)),

  whose cross term is not constant-preserving when h=n-1.  Thus the
  universal joint-rank leaf is parked as circular.

  P144 completes the proposed structural walkback.  Directed row-divergence
  Beckmann flow without reciprocity has the exact value

      2 K_n(f)
        = inf_U [sum_i (sum_(j!=i) ||U_ij||_1)^2]^(1/2).

  Its feasible set factors over rows, so this is P138 itself; reciprocity is
  P89, electrical selection loses the sparse scale, and common-base
  randomness glues every row optimum without contraction.  Static global
  contact is also exact P138 duality:

      max_(mu(A)=a) K_H(1_A)/a
        = max_q AVaR_a(sum_(i in H) Z_i q_i).

  The KKT laws are only rowwise.  For singleton or repetition-code contact,

      U=(S_H^2-h)/(2 sqrt(h)),
      M=S_H S_(H^c)/(2 sqrt(h))

  are reference-orthogonal but have aligned conditioned expectations.
  Therefore Hilbert, martingale, entropy-chain, and static-contact
  orthogonality do not produce a no-cross theorem.  Universal no-cross is
  not a strict child because H=[n] is P138.  The positive boundary is exact:
  every affine code satisfies

      sum_(i in H) r_i^2
        <= [h L R_nu(H)+d L^2]/[4 (log 2)^2].

  Park bare directed flow, static KKT/contact, and orthogonality-based
  no-cross.  Re-enter only with genuinely new common-indicator
  integrability, second-order stability of global maximizers, or nonlinear
  entropy-weighted directed geometry.  The surviving falsifier must have a
  dense, nonmonotone, non-affine, large high-row block.

  P145 completes that re-entry audit.  For centered rows h_i=h_i(Z_-i),
  the laws partial_j h_i=partial_i h_j are equivalent to a unique common
  scalar potential Z_i h_i=D_i f_>=2; this exhausts linear common-origin
  information.  Booleanity adds f^2=f and the pointwise same-orthant law
  D_i f=(2f-1)b_i/2, but parity refutes unsigned-curvature aggregation.
  At a global fixed-density maximizer, every normer lies in the
  hypersimplex normal cone and

      E[(1_A-1_B)F] >= ||v||_2^2/(2T).

  Opposite singleton maximizers share the same unique normers and have an
  exactly flat chord, so local second-order stability is parked.  The exact
  lower-dimensional fiber ceiling is

      |I| <= C_h sqrt(h) (1+R).

  A constant-preserving induction would follow from the full gate

      2 I M + M^2 + sum_(j in Hc) r_j^2
        <= C_*^2 h (1+R)^2 - I^2 + C_0 d L^2,

  with C_0<=C_*^2, already for d=1.  At best-constant calibration,
  repetition shows that O(dR) and O(dL) are insufficient and O(dL^2) has
  the required debt scale unless an independent constant gap supplies the
  slack; the removed-row energy cannot be omitted.  Tilted thresholds have an exact
  positive conditional optimizer deficit away from repetition.  The
  antipodal simplex-star family is a scalable, nonmonotone, non-affine
  all-high calibrator with every row

      r_i=((n-2)(n-3)+2)/(2n)

  and P138 ratio tending to 1/(2 log 2).  Its exact dimension-six normers
  have nonlinear degrees 1,3,5 and all positive saturated cross contacts.
  Do not assume sparse contact, negative pairwise cancellation, or
  deficient Hessian interaction.

  P146 sharpens the codimension-one contract using the actual child optima.
  For sections A_r^+ and A_r^-, put

      E=K_n(1_A)^2,
      E_r^s=K_(n-1)(1_(A_r^s))^2 for s in {+,-},
      B_r=(sqrt(E_r^+)+sqrt(E_r^-))/(2a),
      Delta_r=E/a^2-B_r^2.

  Then the exact P139 signed-defect identity is

      Delta_r=r_r^2+D_r/a^2
        +(sqrt(E_r^+)-sqrt(E_r^-))^2/(4a^2).

  The sole active child is the adaptive theorem

      min_r Delta_r <= C_0 log(e/a)^2.

  It closes P138 by constant-preserving induction.  Prescribed deletion is
  false: for balanced majority equality A={X S_h>=1}, deleting X has
  Delta_X asymptotic to a positive constant times h, whereas deleting any
  majority coordinate has Delta tending to 1/pi.  Antipodal repetition
  forces C_0 at least 3/[4(log 2)^2] asymptotically.  Generic averaging is
  circular because its first term is E/(na^2).  Reopen only with a Boolean
  signed-defect coordinate-selection principle or a scalable counterexample
  for which min_r Delta_r/log(e/a)^2 diverges.

  P147 proves the first strict contraction inside this leaf.  With

      c_ir=|fhat({i,r})|/a,
      c_r^2=sum_(i!=r)c_ir^2,

  the child-norm imbalance cancels the complete J-debt, and

      Delta_r <= r_r^2+c_r B_r+c_r^2/4,
      Delta_r <= r_r^2+sum_(i!=r)c_ir r_i,
      Delta_r <= r_r^2+c_r R,  R^2=sum_i r_i^2.

  Hypercontractivity gives `sum_r c_r^2 <= 2 e^2 L^2`.  Under the
  lower-dimensional P138 theorem, this closes the induction whenever a
  fixed positive fraction of rows satisfy `r_r <= lambda L`.  Therefore a
  remaining obstruction must be almost-all-high, level-two-pseudorandom,
  and simultaneously near equality in the exact binary KR chain rule.
  Ordinary spectral averaging of the weighted-star majorant leaves
  `R^2/n+O(LR/sqrt(n))` and is circular.  The next admissible moves are a
  rigidity/inverse theorem for simultaneous chain-rule near-equality or a
  high-degree counterexample to adaptive deletion.

  In particular, c_r=0 gives Delta_r <= r_r^2.  Exact bent-quadratic,
  complete-quadratic, resilient-composition, cyclic-phase, and affine-code
  assays found no growing deletion debt.  Treat these as counterexample
  diagnostics, not theorem evidence: a genuine level-two-free failure
  would need almost every row itself to be super-entropic.

  P148 audits equality rigidity.  If U is the constant-vertical binary
  chain cost, t the exact parent row cost, and Omega=U^2-t^2, then every
  parent normer has horizontal child deficits satisfying

      delta_+ + delta_- <= 2 Omega/(U+t) <= Omega/t.

  Thus Omega=0 makes the normer hereditarily exact on both faces.  Equality
  alone is nevertheless structure-blind: lifting an arbitrary Boolean g
  through disjoint parity blocks of size at least three gives c_r=S_r=0 for
  every physical coordinate, while every normalized row is at most 1/2.
  The high-row hypothesis is load-bearing.  The active inverse problem is
  hereditary near-optimality plus row-normer oscillation much larger than L,
  not bare equality classification.

  P149 replaces raw oscillation by a gauge-invariant transport certificate.
  For one row/deletion pair, at least

      2t-q-2a ell-Omega/(epsilon t)

  units of child cost lie on pairs of length at least ell whose relative
  dual calibration is at least 1-epsilon.  At ell=r_i/2, small q/t and
  Omega/t^2 force a positive fraction of the row cost onto Hamming
  intervals of dimension at least r_i/2 where the normer is nearly oriented
  distance.  Small c_r and S_r make the number of exceptional high rows
  bounded independently of n.  Raw oscillation is false as a rigidity
  state because dummy-coordinate affine gauges enlarge it arbitrarily with
  zero rerouting.  The active lemma is simultaneous interval overlap or
  packing across the high rows of one common indicator.

  P150 gives an exact orientation export for any optimal row coupling:

      beta_i = t_i-(1/2)sum_(j!=i)|fhat({i,j})|
             = 2 sum_(j!=i) min(p_ij^+,p_ij^-).

  Thus beta_i is precisely bidirectional coordinate cancellation.  It
  vanishes exactly when the signed affine level-two potential is an exact
  row normer.  The zero-cancellation sector obeys P138 with constant
  e/sqrt(2), and generally

      K_n <= (e/sqrt(2))sqrt(n-1) a L + ||beta||_2.

  The target bound on ||beta||_2 is P138-equivalent, so this is structural
  information rather than a smaller universal endpoint.  Combine it with
  P149: oppositely oriented exactly calibrated interval families cannot
  share an edge in that coordinate.  The active target is simultaneous
  oriented packing across almost all high rows.  The simplex-star has only
  beta_i/a=2/n, so the decomposition absorbs the nonlinear all-high
  calibrator.  A balanced central-slice/remote-tail fiber construction has
  one row with beta_i/a growing as sqrt(log n), refuting every one-row
  beta_i <= C a L claim.  Multirow common-indicator structure is essential.

  P151 gives the exact common-origin recursion

      beta_i(parent)
        = average_child beta_i + higher_order_exposure - sigma_i|r,

  and after a random deletion order

      beta_i = V_i-S_i.

  Here V_i is stopped absolute variation of conditional mixed derivatives
  and S_i is accumulated exact rerouting.  The exact energy audit is

      sum_(i!=j) E M_ij^2 = sum_T |T| fhat(T)^2
                           = (1/4) sum_i Inf_i(f).

  Dropping S and bounding V positively loses sqrt(n) at balanced density.
  Plain Shapley variation, unsigned Hessian activity, and separate
  higher-order exposure are parked.  Retain activity minus rerouting
  pathwise and jointly across rows.

  P152 subtracts the symmetric affine level-two potential from exact row
  normers.  The residual potentials
  satisfy

      -1 <= epsilon_ij partial_j psi_i <= 0,
      epsilon_ij=epsilon_ji,

  and beta_i=E[h_i psi_i].  Primal-dually beta_i is minimum wrong-way
  transport relative to the symmetric orientation matrix.  The associated
  gate is

      ||sum_i Z_i q_i||_p <= C p sqrt(n)

  for centered rows with
  `-w_i <= epsilon_ij partial_j q_i <= 0` and sum w_i^2<=1.
  It implies P138.  The p=2 constant sqrt(2) is proved, as are the full
  gate for at most p active rows, affine rows, the strip
  `2 <= p <= 2+c/log(n)`, and p>=n.

  P154 proves that this uniform sign-coherent gate is not strict.  For
  arbitrary centered rows u_i of edge-Lipschitz scale w_i, set

      q_i = u_i - (w_i/2) sum_(j!=i) Z_j.

  Then -w_i <= partial_j q_i <= 0, while the two divergences differ by

      Q_w = (1/2) sum_(i<j) (w_i+w_j) Z_i Z_j,
      ||Q_w||_p <= p sqrt((n-1)/2).

  Conversely, sign-coherent rows have edge-Lipschitz scale at most 2w_i.
  Thus the sign gate is gauge-equivalent to the full arbitrary-row P138
  theorem.  Keep the exact common-indicator normal form, but do not attack
  the nonlinear intermediate-p strip as a contracted leaf.  Return to
  P146 and the P149--P151 contact/activity-minus-rerouting structure.

  P153 closes an adversarial class.  If A is invariant under translations
  by K and d=d_min(K^perp)>=3, exact row transport descends to the quotient
  by K_i^0.  The quotient coordinate walk has conductance at least
  (d-1)/(n-1), so

      r_i <= min{ell_i/2, C (n-1)/(d-1) L},

  where ell_i is the least punctured weight of a kernel word through i.

  Therefore every arbitrary nonlinear union of K-cosets with d>=delta n
  satisfies P138.  Random/high-dual-distance quotient-code counterexamples
  are closed, as are short-local-generator kernels.  Only
  low-dual-distance, large-local-distance translation quotients and
  trivial-kernel transitive OA2 sets remain on that adversarial lane.

  P155 is the mandatory Hadamard calibrator.  Puncturing the constant
  column of an order-N normalized Hadamard matrix gives an OA2 set with

      r_i = (N-2)/4, beta_i=t_i,

  in every row and P138 ratio tending 1/(4 log 2).  Dense long
  bidirectional contact in every row is therefore compatible with P138,
  including exact trivial-kernel Paley instances.  Do not charge raw
  interval count or total calibrated length.

  P156 is the two-point Hall-incidence wall.  Two cyclic balanced OA2 sets
  in Q7 with trivial translation kernel have identical global and
  coordinate-oriented P-N, P-P, and N-N distance enumerators, but exact
  normalized rows 5/16 and 3/8.  One- and two-point distance histograms
  cannot determine row transport.  Retain higher-order Hall incidence or
  joint matching compatibility.

  P157 closes every one-pairing simplex phase.  For an odd Boolean h on
  q=2^(m-1)-1 pair parities,

      A_(i,h) = {Z_i h((Z_v Z_(v+i))_pairs)=1}

  is balanced, simplex-invariant, and OA2, with exact energy

      R^2 = (1/4) W1(mu_h+,mu_h-)^2
            + (1/2) sum_p Inf_p(h)^2
          <= q(1+log 2)/2.

  Majority gives one row of order sqrt(n) but total energy asymptotic to
  n/(4 pi).  Therefore one-row entropy control is false even in the sharp
  simplex quotient, while the whole one-pairing class satisfies P138.
  Attack only aggregate compatibility across incompatible projective pair
  decompositions.

  P158 is a proved identity/majorant and a refuted pair of gates.  For the
  exact row-source laws and exact KR normers,

      H_i^2 = t_i^2/2
        + m_i^2 inf_exact(Var_(rho_i+) phi + Var_(rho_i-) phi),
      Delta_r <= 2 H_r^2/a^2 + sqrt(2) c_r H/a.

  Either entropy-scale control of the minimum majorant or
  H <= C sqrt(n) a L would imply P146, but both statements are false.
  On n=16r^2, the radial set of odd weights outside the central
  sqrt(n) band has constant density, every H_i^2 of order sqrt(n),
  and H^2 of order n^(3/2), while every true row KR cost is O(1) and
  P138 energy is O(n).  A flux of order n^(-1/2) crossing a source-free
  plateau of length sqrt(n) forces an exact normer to accumulate a long
  slope; quadratic source variance charges its endpoint separation rather
  than the small transported flux.  Retain the identity as a diagnostic,
  but do not reopen either P158 gate.  A repair must be flux-weighted or
  truncated and must still retain cross-row common-indicator/Hall structure
  so that it does not collapse to P138 itself.

  P159 is the active dual/coarea preflight.  Exact KR contact gives the
  nonnegative profile

      j_i(s)=m_i[rho_i+(phi_i>s)-rho_i-(phi_i>s)],
      integral j_i = t_i.

  If j_i^down is decreasing rearrangement, define

      F_n(A)=inf_exact integral_0^infinity
             (sum_i j_i^down(u)^2)^(1/2) du.

  Minkowski and a dyadic decomposition of integral extreme normers give

      K_n <= F_n <= C sqrt(log(en)) K_n.

  Native indicator profiles also satisfy the width envelope

      measure{s:j_i(s)>u} <= C sqrt(n log(C/u)).

  The open gate

      F_n(A) <= C sqrt(n) a L

  implies P146 with
  min_r Delta_r <= (C^2+sqrt(2)eC)L^2, hence P138.  The P158 plateau
  contributes its true flux times length, not squared endpoint separation.
  Generic scale-separated signed rows separate F_n from K_n by an
  unbounded factor.  More sharply, disjoint radial point-to-sphere blocks
  give the same sqrt(log n) loss for curl-free derivatives of one bounded
  edge-Lipschitz real scalar.  Thus curl-freeness and bounded range do not
  suffice, but no indicator separation is known.  Treat P159 as a sharply
  falsifiable Boolean preflight, not yet as a certified contraction.  The
  missing Boolean lemma must remove the dyadic sqrt(log n) loss.

  P160 is the active primal/four-point sibling.  For a coupling pi of the
  Jordan source laws, let q_ij=pi(X_j!=Y_j) and

      C_i=(m_i/a)^2 inf_pi sum_(j!=i) q_ij^2.

  Two independent pairs identify the unnormalized cost with expected reuse
  of discrepancy coordinates.  Sion minimax gives

      sqrt(C_i)=(m_i/a) sup_(lambda>=0, ||lambda||_2<=1)
                W_(d_lambda)(rho_i+,rho_i-),

  while Cauchy gives r_i^2<=(n-1)C_i.  Therefore the open gate

      sum_(i:r_i>L) C_i <= C L^2

  implies P138.  This preserves the higher-order Hall incidence required by
  P156 and reduces the simplex remainder to collision packing across
  incompatible projective pairings.

  The Hilbert endpoint now proves the universal dense bound

      sum_i C_i <= (1-a)/(2a).

  Hence P138 is closed on every class whose density is bounded below.  For
  H={i:r_i>L}, normalize maximizing anisotropic exact normers into the
  contact field G_H.  Then E_A G_H=sqrt(sum_(i in H) C_i), and the sparse
  gate follows from the restricted moment estimate

      ||G_H||_p <= C p,  p=max(2,L).

  This is much narrower than the parked arbitrary-row P133 endpoint:
  only high exact contacts of one indicator are admitted, with coefficients
  fixed by their Hall costs.

  The sparse contact moment is proved under four structural conditions.
  If H is the high set and D_H has an arc j->i when psi_i depends on Z_j,

      ||G_H||_p <= C min(sqrt(p|H|), p sqrt(chi_ac(D_H))).

  For collision-minimizing incidences q_ij, the canonical KKT choice is

      lambda_ij=q_ij/||q_i||_2,
      w_ij=gamma_i lambda_ij=(m_i/a)q_ij/sqrt(S_H),
      sum_ij w_ij^2=1.

  If a feedback arc set R has weighted energy

      epsilon_R=sum_((j->i) in R) w_ij^2,

  then

      ||G_H||_p <= C[p+sqrt(p|H| epsilon_R)].

  Thus |H|=O(p), bounded acyclic partition number, or
  epsilon_R=O(p/|H|) closes P160.  Conditional high-block degree at most
  one also closes by Khintchine plus Hanson--Wright, even with dense
  bidirected feedback.

  Fully nonlinear low-phase feedback also closes.  If H is partitioned
  into s blocks, S_b is the sign sum on block b, and each row i in B_b
  depends on the high signs only through

      (S_1,...,S_b-Z_i,...,S_s),

  then conditioning on the Hamming-slice scores gives

      ||G_H||_p <= C[p+sqrt(p s)].

  Thus arbitrary row-dependent nonlinear functions of s=O(p) collective
  scores are good even with complete bidirected dependency and unbounded
  Walsh degree.  Approximation error of weighted size epsilon adds only
  C sqrt(p|H| epsilon).

  A quotient-first common-channel theorem now closes overlapping phases as
  well.  Remove the high-affine part and write eta_i for the nonlinear
  residual.  If T is a randomized channel with averaged posterior
  chi-square information

      I_2=E_(W,T)||dP(Z_H|W,T)/dmu_H||_2^2 <= exp(kappa p),

  and Z_H' is an independent posterior replica, then

      ||G_H||_p <= C(1+exp(kappa/2))p
        + sqrt(|H|) [sum_i gamma_i^2
          ||eta_i(W,Z_H)-eta_i(W,Z_H')||_p^2]^(1/2).

  For deterministic T, I_2 is exactly the expected number of nonempty
  attained values; no minimum-fiber hypothesis is needed.  Thus exact
  rank-O(p) affine syndromes close even when their parity checks overlap.
  The constructive crux is to find an exp[O(p)]-chi-square-information
  channel with weighted replica disagreement O(p/sqrt(|H|)).

  This certificate is not a consequence of rowwise contact.  For the
  projective one-pairing normers, sqrt(8) psi_i are orthonormal and

      A_(p,T)^2 >= (1/4)[1-(I_2(T)-1)/|H|],
      || |H|^(-1/2) sum_i Z_i psi_i ||_2^2=3/8.

  Each row is an exact normer for a different majority indicator.  Hence
  this is a proxy wall, not a P160 counterexample.  Universality requires a
  new common-indicator inverse theorem forcing collision-weighted residual
  effective rank at most exp[O(p)], or a direct bypass of the agreement
  certificate.

  Coordinate transcripts do not provide that inverse theorem.  If a
  depth-k adaptive transcript queries Q(T), its residual KKT edge energy is

      E_(p,T)^2 >= E_0-sum_(ell<=k) c_(ell)^2,
      c_j^2=sum_i gamma_i^2 lambda_ij^2.

  Uniform columns leave E_0(1-k/|H|), whereas closure needs O(p/|H|).
  Aggregate hashes are essential.

  Marginal collision is also insufficient for positive curvature
  coverage.  In the same projective majority plan, each changed pair
  parity is lifted by flipping only one physical endpoint.  Thus no
  same-plan discrepancy contains both endpoints of a pair, although those
  pairs are exactly the nonzero Hessian directions and both marginals are
  positive.  A surviving curvature route must preserve signed cross-row
  phase.  The natural within-one-plan quadratic state does not repair this:
  its transport cost is nonmetric, metric closure deletes off-diagonal
  terms, and its exact two-potential dual cannot assemble into
  E[h_i psi_i]=E[f Z_i psi_i].  Signed second moments are diagonal on the
  projective lift.  Park second-moment joint-discrepancy states.

  P161 is now the primary strict child.  On the fixed-density hypersimplex
  define

      c_i(f)=a^(-1) sup_(lambda,psi) E[h_i(f) psi],
      tau=L/sqrt(n-1),
      Q_tau(f)=||(c_i(f)-tau)_+||_2.

  This functional is convex, and

      sum_(r_i>L) C_i <= 2 Q_tau(f)^2+4L^2.

  A maximum may be chosen at an indicator A.  With
  u_i=(c_i-tau)_+/Q_tau and exact potentials,

      G_tau=sum_i u_i Z_i psi_i,
      G_tau/a in partial Q_tau(A),
      E[(g-A)G_tau]<=0 for every equal-density g,
      E_A G_tau=Q_tau(A)+O(L),
      ||G_tau||_2^2<=1/2.

  More strongly, with I={i:c_i(A)>tau}, X_i=Z_i psi_i, and
  m_i(g)=a^(-1)E[gX_i], global extremality gives

      ||((m_i(g)-tau)_+)_(i in I)||_2 <= Q_tau(A)

  for every equal-density fractional g.  If
  delta_i=m_i(g)-c_i(A), uniform convexity gives

      ||(delta_i)_+||_2^2
      <=(2 Q_tau(A)/a) E[(A-g)G_tau].

  Hence A is a top level set of its own contact field and simultaneously
  supports the full positive cone of its active contacts.  The active
  target is Q_tau(A)<=C L only for these nonlinear fixed points.  Point
  swaps lose the cardinality |A|, and top-level contact plus the L2 bound
  alone admits abstract spiky countermodels; use a macroscopic competitor.
  This is strictly stronger structural input than rowwise contact and
  excludes the projective proxy wall unless its rows can be realized by
  one such A.

  Two further common-indicator facts sharpen the surviving sector.  If
  eta_i=P_(>=2)^H psi_i, xi_i=Z_i eta_i, sigma_i=||xi_i||_2,
  Y_i=xi_i/sigma_i, s_i=E_A xi_i/sigma_i, and
  R_ij=E[Y_iY_j], then

      s^T R^dagger s <= (1-a)/a,
      ||P_[0,lambda](R)s||_2^2 <= lambda(1-a)/a.

  This controls contact-visible spectral mass but retains the exact loss
  r_eff(R)<=|H|(1-a)/(a||s||_2^2).  The cone certificate does not remove
  it: a common-atom character model saturates both inequalities while
  Q_tau>>L, although that abstract model is not an exact cube-KR row
  realization.  Positive low-eigenvalue selection is therefore parked
  unless paired with new variance-sensitive concentration using row
  provenance.

  Also, for b_i=1_{f differs across its i-edge}, Booleanity gives

      E(D_iD_j f)^2=(1/4)E[b_i b_j].

  Exact potentials can be selected with dependency graph contained in the
  simultaneous-boundary graph.  Bounded chromatic number therefore closes
  P160.  A surviving obstruction must have high-chromatic boundary
  entanglement.

  The projective high-rank wall is now fully closed at the signed-cone
  level.  For the projective one-pairing normers,

      ||sum_i u_i Z_i psi_i||_p <= C p       (||u||_2<=1).

  The proof uses heavy/light row splitting, exact order-three tensor
  partition norms, fixed-order decoupling, and Latala's Gaussian-chaos
  theorem.  Therefore every indicator whose active exact contacts are
  these projective normers has Q_tau<=C L; uniform cubic thresholds and
  all weighted projective top-level analogues are benign.  Do not treat
  high projective effective rank as a surviving P161 obstruction.

  There is a second strict closure localized to the actual nonlinear
  contact signal.  Put eta_i=P_(>=2)^I psi_i and
  d_i=E_A[Z_i eta_i].  On every induced DAG V of the residual dependency
  graph and for every w supported on V,

      ||sum_(i in V) w_i Z_i eta_i||_p
      <= C[sqrt(p Var(sum_(i in V) w_i Z_i eta_i))+p||w||_2].

  Hence ||(d_i^+)_(i in V)||_2<=C L.  The high-affine contact vector is
  also O(L) in ell2.  If kappa_ac(d) is total positive nonlinear signal
  divided by its largest induced-DAG portion, then

      Q_tau(A) <= C(1+kappa_ac(d))L,
      kappa_ac(d) <= sqrt(chi_ac(D_eta)).

  This closes bounded signal-local acyclic ratio even when the unweighted
  graph has large coloring complexity.  Random-order predictable projection
  yields the stronger degree-resolved curve

      bar d_i(t)=sum_(k>=2) t^k d_i^(k)/(k+1),
      ||bar d(t)||_2 <= C L.

  Hence bounded random-order recovery ratio closes P161, and Vandermonde
  inversion closes every fixed active-block residual degree without a graph
  hypothesis.  A transverse anisotropic square-field theorem proves

      ||sum_i u_i Z_i psi_i||_p <= C_D p

  whenever the combined contact field has fixed aggregate Walsh degree D.
  Individual rows may have arbitrarily high degree and cancel in the
  aggregate.  Thus a survivor must have unbounded active-block degree and
  unbounded aggregate degree, in addition to diffuse high-dichromatic
  positive signal.  Literal complete bidirectedness is not necessary.

  Do not try to recover the endpoint signal from the scalar random-order
  curve alone.  For D=4m+2, the positive Chebyshev profile
  F_D=(T_D+1)/2 has sup_[0,1] F_D<=1 but
  F_D'(1)+F_D(1)=D^2/2+1.  This is an abstract degree-signal wall, not a
  cube-contact counterexample.  Scalar Abel/Tauberian inversion must be
  replaced by an argument retaining common-indicator, Walsh-support, or
  exact Kantorovich provenance.

  Every cube translate of a P161 maximizer has nonpositive response in
  every fixed active contact coordinate.  Hence so does every translation
  mixture, heat/noise smoothing, subgroup average, or radial interpolation;
  the uniform-convexity remainder is identically vacuous on those routes.
  P162 gives an exact threshold-band/lock analysis, but not an exhaustive
  dichotomy.  For B_eta={|G_tau-theta|<=eta}, the localized rotation has an
  exact positive-orthant support formula and normal cost at most

      2 eta min(p_eta,q_eta).

  An affordable band with fixed-fraction rotation closes P161.  If every
  active row is strictly locked, A={Z_i psi_i>s_i}, then

      ||(c_i-s_i)_i||_2^2 <= |I|/(|I|-1),

  and the remaining row is the weighted coordinate-code margin

      ||((s_i-tau)_+)_i||_2 <= C L.

  Balanced tie-free strict locks close.  Repetition cylinders refute the
  implication from long exact KR intervals to positive rotation, while
  Gilbert--Varshamov codes refute replacing the row-dependent metrics by
  Hamming distance.  More decisively, an abstract near-band spike model
  obeys the convex, top-level, cone-certificate, uniform-convexity, and
  `L2` hypotheses while every individual support defect is one.  Thus
  ``no macroscopic band rotation'' does not imply aggregate approximate
  locks from those abstract data: it loses the sharp factor `sqrt(|I|)`.
  This is a proxy wall, not an exact cube/KR counterexample.

  The strict-lock remainder has an exact forbidden-difference Cayley
  representation, but its unrestricted independence-number/Delsarte gate
  is false on pinned faces.  After separating the coordinates which vary
  on the code, put

      E_i={(x,y) in A^2:x_i!=y_i},
      rho_i^2=min_(p_i in Prob(E_i))
                sum_(j!=i) Pr_(p_i)(x_j!=y_j)^2.

  This is an exact fractional multicommodity code SOCP, with dual

      rho_i=max_(lambda_i>=0, ||lambda_i||_2<=1)
              min_((x,y) in E_i)
              sum_(j!=i) lambda_ij 1_(x_j!=y_j).

  Strict locks give `2(s_i-tau)_+<rho_i`; pinned active coordinates cost
  `O(L^2)` by the face-codimension and subgaussian-tail bounds.  The
  formerly proposed pure code gate

      sum_(i in V(A)) rho_i^2 <= C L^2

  would close every strict lock, but it is false.  Repetition and parity
  calibrate benign sectors, and exhaustive tests through `n=4` pass, but
  the outlier half-ball below gives the first failure in dimension five.

  Random priorities now give an exact nonlinear reduction.  Let
  `k=log_2(1/a)` and let `S(U)` contain coordinates which are not the unique
  priority maximum of any incident difference support.  Projection off
  `S(U)` is injective, so `|S(U)|<=k`.  If `q_i` is the closest fractional
  link-incidence vector, `ell_i=||q_i||_1`, and
  `p_i=Pr(i in S(U))`, threshold integration gives

      rho_i^2 <= 2 p_i ell_i,
      sum_i rho_i^2 <= 2(n-1)k.

  For every binary linear code of parity-check rank `r`, circuit
  minimality makes every link size at most `r` and `S(U)` matroid-
  independent.  Therefore

      sum_i rho_i^2 <= 2 r^2.

  The same holds for affine cosets and has the target quadratic scale.
  An arbitrary-hypergraph extension by independence number is false: all
  two-edges on `m` old vertices plus one redundant edge containing a new
  distinguished vertex have independence number two but distinguished
  row value `rho_i^2=m`.  Matroid circuit descent is load-bearing.

  The proposed sharp nonlinear transfer

      rho_i^2 <= (k+1) p_i.

  would sum to `k(k+1)`, but it is also false.  For even `m>=4`, let

      A_m={(0,b):wt(b)<=m/2} union {(1,1^m)}.

  Its density tends to `1/4`, so `k<2`, while the distinguished row has

      rho_i^2=m/4,
      p_i=m/[2(m+1)],
      ell_i=m/2.

  Already at `m=4`, `rho_i^2>(k+1)p_i`; asymptotically one row refutes
  both the pure code gate and the aggregate priority-length gate.  The exact
  entropy--Shapley relaxation also fails: if
  `d_i=E_U[1-H_2(X_i|X_{H_i(U)})]`, then `p_i<=d_i<=1` and
  `sum_i d_i=k`, but `rho_i^2` still grows like `m`.

  The missing datum is section mass.  If the two section densities are
  `alpha_0,alpha_1` and
  `theta_i=min(alpha_0,alpha_1)/(alpha_0+alpha_1)`, applying
  bounded-difference concentration to the weighted distance from one
  section gives

      rho_i^2 <= log(1/(alpha_0 alpha_1))
                =2 log(1/a)+log(1/[4 theta_i(1-theta_i)]),
      theta_i rho_i^2 <= C L.

  Marginal entropy also pays all strict-lock thresholds with
  `theta_i<=delta` by `O_delta(L^2)`.  Thus only a quantitatively
  section-balanced code statement which retains the actual lock thresholds
  can be reopened.  The explicit repaired candidate is

      sum_i theta_i rho_i^2 <= C k^2.

  It would close every strict lock after the near-pinned/balanced split.
  It holds with sharp constant one for affine codes, vanishes for
  coordinate-flipped down-sets, and is stable under Cartesian products of
  those classes.  Exact tests through `n=4` have sharp ratio one and the
  outlier wall has large slack, but the universal statement remains open.

  Do not try to prove it from the mass-weighted projection probability

      theta_i rho_i^2 <= C (k+1) p_i.

  This is false even for equal sections.  Take antipodal Hamming balls of
  radii `m/2-t` in the two sections.  Their separation is `d=2t`, and
  the distinguished row has

      theta_i=1/2,  rho_i^2=4t^2/m,  p_i=2t/(m+1).

  If `t` tends to infinity with `t=o(sqrt(m))`, then `a->1/2`,
  `k->1`, and the row ratio diverges like `t/2`, although the aggregate
  weighted value is only `2t^2/m->0`.  Exact support separation is too
  coarse.

  The sharper information-weighted assay

      theta_i rho_i^2 <= C k d_i,
      d_i=E_U[1-H_2(X_i|X_{H_i(U)})],
      sum_i d_i=k,

  has the exact erasure representation

      d_i=int_0^1 E[1-H_2(X_i|X_(R_t),R_t)] dt,
      J_i=int_0^1 E|E[(-1)^X_i|X_(R_t),R_t]|^2 dt,
      J_i/(2 log 2) <= d_i <= J_i,

  where `R_t` retains tail coordinates independently with probability `t`.
  For section projection counts `N_b(S,z)`,

      E M_S^2
        =(1/|A|) sum_z (N_0(S,z)-N_1(S,z))^2
                          /(N_0(S,z)+N_1(S,z)).

  Thus the assay is exactly, up to constants, a beta-averaged triangular-
  discrimination comparison with the fractional cross-difference distance.
  It holds with constant one for affine codes and for every full Boolean
  graph `{(f(y),y)}`.  If `f` has `s` relevant coordinates, its graph row
  has `rho_i^2=1/s` and `d_i>=1/(s+1)`.  The universal statement is still
  unproved.  The count-level lift is exact: with

      I_S=(1/N) sum_z (N_0-N_1)^2/(N_0+N_1),
      Omega_S=(4/N) sum_z N_0 N_1/(N_0+N_1),

  one has `I_S+Omega_S=1`, `J=sum_S w(S)I_S`, and a harmonic common-fiber
  subprobability mixture of mass `1-J`.  But overlap counts do not choose
  economical geometry inside the fibers.  On balanced parity, every proper
  projection has full overlap, while independent uniform fiber coupling
  gives each coordinate load tending to `1/4` and total square `~m/16`;
  the optimum is `1/m`.  Pairing through one uniformly chosen unrevealed
  coordinate recovers that optimum.

  The surviving stronger assay is coherent beta-harmonic fiber selection:
  choose all common-fiber couplings jointly across scales so their final
  coordinate loads square-sum to `O(k J_i/theta_i)`.  This now has an exact
  convex dual.  If `alpha_(S,z)` are the normalized harmonic common-fiber
  masses and

      d_(S,z)(lambda)
        =min_(x in B_z,y in C_z) sum_j lambda_j 1_(x_j != y_j),

  then

      sqrt(L_sel)
        =sup_(lambda>=0, ||lambda||_2<=1)
           sum_(S,z) alpha_(S,z) d_(S,z)(lambda).

  The same anisotropic direction `lambda` is load-bearing across every scale
  and fiber.  Separate local optimization followed by square aggregation is
  not merely circular; it is false at target scale.  On parity the average
  local squared norm is `H_m/m`, while `k J_i/theta_i=2/(m+1)`, a logarithmic
  loss.  The exact shared-direction quantity is `1/m`, so parity remains
  benign.  The stronger common-direction second-moment assay is

      sup_(lambda>=0, ||lambda||_2<=1)
        sum_(S,z) alpha_(S,z) d_(S,z)(lambda)^2
        <= C k J_i/theta_i.

  P171 proves this with constant one for every affine code, without a
  symmetry hypothesis.  Run random-greedy on the parity-check matroid, use
  the final fundamental circuit, and swap the distinguished coordinate
  with a circuit element.  If `J` is circuit nonavailability, the
  inclusion probabilities `q_j` satisfy `sum q_j<=r` and
  `max q_j<=min(1,J/(1-J))`.

  P172 closes a strictly larger class: every Boolean graph over every
  affine domain `D=u+V`, with arbitrary nonlinear labels.  On a
  projection fiber use the quotient Fourier characters of
  `V_S={v in V:v_S=0}`.  For each global character `chi`, form the
  virtual linear graph code

      L_chi={(ell_chi(v),v):v in V}.

  P171 bounds its available weighted circuit cost.  Quotient Parseval then
  sums the characterwise charges to

      E[v_(S,z) d_(S,z)(lambda)^2]
        <= k min(J_i,1-J_i).

  After harmonic normalization this is at most `k J_i/theta_i`.

  Do not continue searching for asymmetric affine codes or nonlinear
  labels on affine supports; those classes are closed.  For a native row,
  nonzero fractional cross-distance forces disjoint sections, hence a
  partial Boolean graph.  The unresolved selected-lift profile is therefore
  a partial graph on a proper nonlinear domain.  The missing mechanism is a
  replacement for common affine-coset Fourier decomposition and
  characterwise circuit descent.  Do not equate maximal projected overlap,
  independent coupling, local-square Jensen aggregation, or independently
  optimized dual directions with a proof of the information-weighted gate.
  The unweighted code gate, its unweighted priority/entropy variants,
  mass-weighted support-priority repair, and rank-only repairs are
  tombstoned.

  Affine completion is now fully tombstoned.  P173 refutes coefficient-one
  information/energy monotonicity on a three-point domain.  More decisively,
  P174 takes

      D_m={0} union {x: |x|>=floor(m/4)}

  with the origin carrying the minority label.  Its affine-hull density
  defect is exponentially small, but at the uniform direction every partial
  mixed fiber has distance `r/sqrt(m)`, whereas every completed mixed fiber
  has distance `1/sqrt(m)`.  The best signed completion defect is at least
  `(r^2/m-1)m_D` for every extension.  Thus no universal constant repairs
  the transfer.  The family is benign for the true target because
  `theta_D=1/|D_m|`; completion failed by discarding this section-mass
  normalization.

  Immediate or bounded-depth information swaps are also closed.  On

      B={000,111}, C={001,010,101,110},

  both children of every coordinate retain the root `1:2` label ratio, so
  all one-step information increments vanish, while the root harmonic
  distance energy is `2/27`.  Orthogonal-array variants give the same wall
  at every fixed depth.

  A further global assay chooses all fiber pair laws jointly and defines
  coordinate loads `q_j`.  The unweighted first proposal

      ||q||_1 <= C k

  is also refuted by the P174 radial family: every selected pair has at
  least `r` mismatches, so every selection has `||q||_1>=r` while `k->1`.
  Even the weighted first bound is false: balanced antipodal balls have
  `theta=1/2`, `k->1`, and minimum cross-distance `2t->infinity`, so every
  selection has `||q||_1>=2t`.  Separate universal load caps are closed.

  The final same-selection product preflight

      inf_sigma ||q(sigma)||_1 ||q(sigma)||_infinity
        <= C k J/theta.

  is also false.  Add a tag bit to balanced antipodal balls.  Every selected
  pair differs in the tag and at least `2t` tails, so `q_tag=1` and the
  product is at least `1+2t`.  An equivariant selection has
  `q=(1,2t/n,...,2t/n)` and quadratic load `1+4t^2/n -> 1`, while the target
  right side stays above `2`.  Thus the actual `l2` target has fixed slack.
  All `l1`/`linfinity` factorization routes are closed.  The nonlinear
  selected lift has returned to its native quadratic/SOCP selection problem;
  any successor needs structure acting directly on that geometry.

  The raw positive-superlevel square self-bound

      sum_j (G_tau(z)-G_tau(z^(j)))_+^2
        <= C[(G_tau(z))_+ + L]

  is false from exact one-row provenance plus the fixed-contact
  certificates.  On a projective one-pairing majority contact
  `F=Z_i psi_i`, the common indicator is `{F>0}`, the row is an exact KR
  normer, and the top-level cone and remainder hold.  At the all-positive
  vertex, however,

      F=sqrt(h-1)/4,
      sum_j (F-F^(j))_+^2=(h-1)/4+1.

  The loss is `sqrt(h)`.  This is not a counterexample for global P161
  maximizers; it proves that only a new maximizer-driven cross-row
  compensation theorem could rescue the square gate.

  The calibrated one-row replacement uses
  `Phi(s)=s_+^2/(1+s_+)`:

      sum_j Phi(F-F^(j)) <= 2 F_+ + 1.

  The front flip has linear cost and the transverse flips use the native
  squared oscillation budget.  The smaller live analytic question is a
  dimension-free assembly of this truncated carre, or an equivalent
  first-power nested-superlevel flux, for a full globally maximizing
  contact field.

  The next native moves are therefore a section-balanced,
  provenance-preserving lock theorem, the maximizer-only truncated-carre
  assembly, or a realizable unbounded-degree counterexample.  Keep a
  P138-versus-P14 separation attack parallel because P161 is only a strict
  sufficient row.

  Distinct simplex-majority pairing phases have exact covariance
  asymptotic 8/(pi n) but Dirichlet overlap tending to 4/pi; the shared
  projective-line and full-parity modes must be quotiented first in a
  Dirichlet phase-rank diagnostic.  For
  k=o(n) the phases still retain genuine L2 rank.  The one-pairing
  distinguished collision is exactly q p_q^2/8 -> 1/(4pi).  No mixed
  counterexample follows: stability of diffuse row couplings under
  simultaneous projective conditioning is the missing theorem.

  For the nonlinear remainder, define

      Theta_(p,H)^2=sum_i gamma_i^2 || |D_H^2 psi_i|_HS ||_p^2.

  Two cube Poincare inequalities give

      ||G_H||_p <= C[p+p sqrt(|H|) Theta_(p,H)].

  Exact normers are affine on every optimal transport interval, so this
  Hessian vanishes on contacted two-faces.  The open crux is a
  collision-weighted contact-coverage theorem for the remaining nonlinear,
  many-row, irreducibly cyclic, high-phase-rank case.  Do not replace it by an unweighted
  global Hessian bound without testing the P158 plateau.

  P136 sharpens the earlier
  admission test.  Positive heat/Bessel smoothing of
  \(\mathcal LP_{\ge2}f\) followed by one scalar \(L\log L\) norm has the
  correct automatic indicator upper bound but loses
  \(\sqrt n/\log n\) against P14 on balanced majority.  Independently
  optimizing Hall matchings at every distance threshold can be linearly
  smaller than row \(W_1\), while forcing one common matching reconstructs
  \(W_1\) exactly by layer cake.  Ordinary coordinate compression is also
  nonmonotone already on four points in \(Q_4\).  Reopen these directions
  only with signed/derivative-sensitive multiscale structure, an
  entropy-sized correction, or a genuinely simultaneous row repair.  P137
  audits exactly those immediate survivors.  The exposed-face extension
  defect has a complementary-slack/Hall normal form, but local optimum values
  plus the defect reconstruct the original transport; splitting the P123
  matched core into its Hall core and matching-incompatibility defect leaves
  two independent entropy bounds.  The vertical Poisson square has the
  correct indicator \(L\log L\) budget, yet its dimension-free \(L^2\)
  normalization makes it smaller than P14 by \(n^{1/4}\) on majority.
  Therefore reject every dimension-free \(L^2\)-bounded scalar square as a
  direct P14 dominator.  The half-derivative square has degree-`k` response
  `sqrt(k)|F|/2`, but no ambient normalization satisfies both contracts:
  full parity forces `c_n=O(n^(-1/2))`, while embedded two-bit parity forces
  `c_n=Omega(1)`.  Degree-adaptive squares, signed cross-scale pairings, and
  adaptive scale/test couplings remain open.  The row-indexed survivor is
  precisely P138.  The P103
  transfer identity is proved,
  but P105 refutes its stronger scale-by-scale compatible variation bound.
  The SF-P89 predictable reveal-square estimate is a strict sufficient
  statement.  P106 proves it for linear-hypergraph supports and for the
  combined P105 affine family.  P107 proves weighted binary backward peeling
  and identifies the exact local condition as a Rudin-scale
  `Lambda(p)` estimate for every last-pivot residual spectrum.  P108 proves
  that compatible potentials may have unbounded local `Lambda(4)` constants
  while their full reveal square is pointwise target-good.  P109 gives the
  exact fresh-endpoint/inherited-coefficient reveal recursion and refutes the
  natural resolvent/P30 occupation lift at the fractional-cover scale; that
  lift can be large even when the scalar output vanishes.  Thus local
  good-pivot deletion and pre-quotient occupation are both refuted.  For a
  fixed/random order the invariant scalar bracket is the P82 chronological
  square object, while its Carleson dual is the desired norm restated.
  SF-P89 is parked unless a genuinely smaller quotient-sensitive adaptive
  state is found.  P110 proves P89 for every binary quotient factor with at
  most `O(p)` singly occurring nonzero label classes, and gives the sharper
  all-moment square-root bound when every nonzero class repeats.  It also
  refutes two proposed architectures: independently optimizing the P89
  quotient on homogeneous levels can lose exponentially on a bent quadratic
  phase, and controlling the exact compatible matrix transform before taking
  its scalar trace costs a sharp extra `sqrt(p)`.  These are a class theorem
  and method walls, not a universal proof.  P131 adds a rank--trace
  globalization wall: if the identity on the nonaffine scalar range is a
  finite signed mixture of binary-quotient conditional expectations, the
  total P110 component cost is at least
  `n(1-(n+1)/2^n)`.  Thus componentwise P110 plus triangle inequality cannot
  yield `O(p)` when `p << n`.  This does not exclude adaptive, nonlinear,
  input-dependent, or martingale-difference quotient assemblies.
  P111 iterates repeated-label
  quotients as a reverse martingale: deterministic conditional subgaussian
  proxies square-sum with no collision-depth loss.  P112 upgrades this to
  the conditional Bernstein class

      ||F_0||_p <= ||F_T||_p + C(sqrt(pV)+pL).

  The P111 rare-event family passes this sharper variance/peak gate.
  Nevertheless P113's depth-one repeated-core/leaf family has chord graph
  K_(N,2m), native budget n tau_2(c)^2=2mN, but deterministic conditional
  variance N^2.  Thus worst-coset Bernstein transfer loses N/(2pm) even
  though the native P89 ratio is small.  Keeping the bracket random either
  pays a generic maximal-increment loss or returns to SF-P89/P82; park the
  quotient-flag continuation.  Independently, P112 proves every canonical
  Boolean corrected gradient P89-good, for all degrees, labels, and
  multiplicities.  P114 proves the arbitrary-gauge half-space barrier and
  exact representative-blindness calibrations.  P115 sharpens this to
  rho_n(F)>=S(S-1)/(2(n-1)sqrt(n)), adds an averaged-Hessian certificate,
  proves the exact symmetric real quotient (with a sharper Boolean
  consequence), and proves exact disjoint-
  output tensorization.  Any Boolean pointwise survivor must have sublinear
  maximum sensitivity and |F(x)|/sqrt(E[k(k-1)]) tending to infinity along
  offending vertices.  Full permutation symmetry and additive repetition of
  a fixed disjoint output cannot create the amplification.  This bounded
  Boolean assay is parked; its fixed-output dual still has the full P89 ball.
  P116--P121 audit the universal fixed-orbit continuation.  P116 defines an
  exact one-orbit envelope `C<=O<=D` and a correlated Gamma-moment multiplier
  hull.  It contracts the false P103 norm by `sqrt(M)` on the full P105
  affine-spread witness, but `sigma=1` recovers `P_(>=2)` and hence P89
  itself: this repairs a proxy without producing a smaller P89 crux.  P117
  proves that every unweighted separated
  `L^r_mu(L^p) x L^(r')_mu(L^(p'))` factorization loses an extra `sqrt(n)`,
  uniformly for `1<=r<=infinity`.  P119 shows that positive adaptivity does
  not repair the wall: the optimal pointwise positive weight equals the
  absolute-product integral, which loses `sqrt(n)` on the simultaneous
  complete-quadratic/point-mass pair; positive stopped local Hölder sums have
  the same loss, while unrestricted signed stopping is tautological.  P118 gives the exact signless-incidence
  factorization `F=R^* I A`, with squared support norm `k/(2(k-1))` and
  transverse-gauge contraction at most `1/4`; common-core, matching,
  quadratic, and degree-three tournament tests close pointwise and generic
  two-stage continuations.  P120 strengthens P110's phase wall: aligned and
  quadratic-bent flat spectra have identical canonical unsigned per-support
  incidence data but exponentially separated native quotients and moments.
  Thus the active P89 proof must remain signed, quotient-aware, and genuinely
  bilinear before norming either heat-orbit leg.  P116 and P118 are bounded
  parked assays, not new active leaves.
  A focused branch audit found no named post-P89 formulation with a proved
  strict contraction.  One bounded assay remains under the existing P89
  node: with the norming functional
  `J_p F=sgn(F)|F|^(p-1)/||F||_p^(p-1)`, test

      V_p(F)=integral |E[(K_q F)(K_q J_p F)]| dmu
             <= C p sqrt(n) rho_n(F).

  Exact Calderón reproduction makes this sufficient for P89.  It is a
  diagonal restriction of P116 and genuinely stronger than P89, but the
  norming-functional/extremizer reduction is generic until quotient KKT
  contacts produce a scale-variation contraction.  It is exact at `p=2`,
  for homogeneous outputs, and for one-signed Fourier data at even `p`.
  Bounded bent/aligned, radial, design-like, random, and exact-LP tests found
  no counterexample.  P121 completes the bounded analytic/KKT iteration.
  The norming map is surjective on dual classes modulo affine functions;
  global extremal coupling is a strict subset and yields singleton exposed
  faces plus exact sign-support, tight-cover, and proportional-degree
  contacts.  Those contacts are complementary slackness for existing P89
  duality and give no nonconstant-scale transition.  For the normalized
  scalar contact polynomial `P_F`, shifted heat gives only `|P_F(s)|<=1`
  and `P_F(1)=1`, while shifted Chebyshev polynomials satisfying those
  conditions have Gamma variation of order the square of their degree.
  This refutes the scalar heat-profile compression, not the full variation
  estimate, because the Chebyshev data are not shown realizable by cube
  extremizers.  Treat P121 as `PARKED`: reopen only with a contact-set
  Gamma-multiplier contraction or deletion map, not with more static KKT or
  scalar heat arguments.
  P131 reopened exactly one bounded continuation under the same P89 node.
  At every genuine global extremizer, the tight chord-contact sets
  injectively sample the full nonaffine quotient-Hodge range through
  `2 D_i D_j L^(-1)`, forcing total normalized contact mass

      sum_{tight {i,j}} mu(E_ij) >= 4(1-(n+1)/2^n).

  The optimal dual flow defines a probability law `Pi` supported on signed
  tight contacts with first-endpoint marginal `u_i^2`.  This is a strict
  extremizer restriction, not a moment estimate.  A positive/Hadamard
  complete-quadratic pair has identical static Hilbert-endpoint contact data
  but high moments separated by `sqrt(n)`.  Therefore do not continue with
  unweighted contact counts, separate edgewise entropy, or `p=2` flow
  magnitudes.
  P132 completes the permitted target-`p` preflight.  Symmetrizing the
  optimal flow gives a contact-frame seminorm `s_(p,barPi)` with exact signed
  mean `E_(barPi) T G=E[hG]/M_(p,n)` and `s(F)=1`; an inverse bound

      ||G||_p <= C p sqrt(n) s_(p,barPi)(G)

  would imply P89.  Existing KKT data do not supply it: normalized local
  perfect-matching primal/dual data satisfying the same contact identities
  support the flow only on the matching and annihilate the nonmatching
  quadratic `Z_1 Z_3`.  They are not claimed globally extremal.  At `p=2`,
  the complete quadratic has the exact frame weights
  `(|S|-1)/(|S|(n-1))`, so the full `sqrt(n)` scale is
  intrinsic.  Ordinary Lewis weights, operator scaling, and
  Bourgain--Tzafriri selection see unsigned Gram geometry; isometric
  equal-leverage frames can still have zero signed first moment.  For the
  actual analysis operator the missing signed angle is `1/M_(p,n)`, so the
  desired lower bound is P89 itself.  Treat the contact branch as `PARKED`.
  Reopen only with a new quantitative consequence of global
  exposed-singleton extremality, not another KKT or frame reformulation.
  P133 is the post-contact branch audit.  Do not promote the rowwise
  optimal-KR exponential-tail statement: after inactive rows are normalized,
  entropy duality and the residual moment theorem make it equivalent to P14.
  Do not continue the P90-coloring/conditional-Hanson--Wright proof template
  either.  Coloring leaves at most one edge from each Walsh support and hence
  erases the compatible four-cycle identity; R=p=k disjoint rooted
  k-stars force a sqrt(k) loss in the reconstructed operator term.
  This is a method wall, not a counterexample to an uncolored compatible
  Hanson--Wright estimate.

  The separate sufficient program is the two-scale Bernoulli divergence

      ||sum_i Z_i u_i||_p
        <= C(sqrt(p) ||u||_(L^p(ell_2))
             + p ||D u||_(L^p(HS))).

  It is equivalent to the centered derivative-only form.  Centered rows
  satisfy the exact range identity

      sum_i Z_i u_i
        = sum_(i!=j) Z_i Z_j (I+L_(-ij))^(-1) D_j u_i.

  Thus full parity refutes the unrestricted unsmoothed double divergence but
  not this compatible smoothed range.  Direct tangent recoupling,

      ||sum_i Z_i u_i(Z)||_p
        <= ||sum_i eps_i u_i(Z)||_(L^p(Z,eps))
           + C p ||D u||_(L^p(HS)).

  is equivalent up to constants to the centered two-scale endpoint:
  conditional Khintchine and Hilbert-valued cube Poincare give one
  implication, while the endpoint gives recoupling because the tangent term
  is nonnegative.  Do not promote it as a smaller crux.

  A column-coupled common-conductance primal is also parked.  Its exact
  dual is a quotient of the pointwise column-ell2 norm by the annihilator of
  the componentwise edge-range and row-independence constraints; the raw
  max-column norm is only a lower dual subclass, not the polar.  Balanced
  majority of disjoint pair-products separates this conductance functional
  from P138 by exactly sqrt(n), although it remains target-sharp.  Do not
  promote the raw column estimate as an upper bound for the primal, and do
  not present the functional as a P138-level reformulation.

  P134 completed one local proof/falsifier preflight.  With independent
  biased signs of mean t, put

      X_t = sum_i Y_i(t) Z_i u_i,
      M_p(t) = E |X_t|^p.

  Russo differentiation followed by pairing Z_i=+-1 gives an exact signed
  mixed-rectangle sum for M_p'(t).  The required one-sided differential gate

      M_p'(t) <= C p^2 ||D u||_(L^p(HS)) M_p(t)^(1-1/p)

  would integrate to the centered endpoint.  Absolute derivative control is
  false already for u_1=Z_2, u_2=-Z_1: then
  M_p(t)=2^(p-1)(1-t^2) and M_p'(t)=-2^p t.  The negative derivative is
  harmless for the required upper bound.  After preserving this sign,
  termwise vectorization of the cross-column half-slope still recreates the
  dimensionally false nonpredictable-column-divergence proxy.

  The completed audit proves

      M_2'(t) <= 2 ||D u||_(L^2(HS)) M_2(t)^(1/2)

  universally, with normalized constant \(1/2\) asymptotically sharp on
  full parity, and

      M_p'(t) <=
        2 p ||sum_i |u_i|||_p M_p(t)^(1-1/p)

  for every \(p\ge2\).  The latter closes common-Walsh-phase rows but cannot
  be transferred to the Hilbert--Schmidt budget: on \(u_i=Z_{i+1}\) it loses
  \(\sqrt n\), whereas the exact derivative vanishes for every even \(p<n\).
  Complete quadratic rows give normalized positive derivative
  \(||G^2-1||_p/(2p)\) after \(n\to\infty\), tending to \(1/e\); hence the
  conjectured \(p^2\) scale is sharp.  P134 is parked without a proof or
  counterexample to the universal one-sided gate.  Reopen only with a new
  phase-sensitive cancellation principle for the total rectangle sum, not
  with unsigned majorization, vectorization, or another diagonal
  integration-by-parts pass.  The neighboring Gaussian
  Meyer--Skorohod results are stored durably in
  literature/nualart2006malliavindivergence/ and
  literature/pisier1988meyer/; their derivation/rotation arguments are
  precedent, not cube transfer.  Independently, interpolation closes P89 on
  2 <= p <= 2+1/log(n), so a P89 falsifier must satisfy
  (p-2)log(n) -> infinity.
  P122 completes the bounded deletion/state audit of the parked P11/P82
  invariant square.  If \(r\) is last, its bracket obeys the exact recursion

      V_(pi'+r)(R) = V_(pi')(E_r R) + |partial_r R|^2,

  and order averaging gives the signed collision weight
  \(|T\cap U|/|T\cup U|\).  Neither is a contraction: a
  three-coordinate two-root collision forces first-child row parameter
  \(3\beta/2\), Jensen controls the collision kernel in the wrong direction,
  and P108 gives

      Gamma(E_pi V_pi)/(beta^2 n^2 E_pi V_pi) ~ n/12

  at the all-positive vertex even though its true square is uniformly
  bounded.  Exact even-moment diagrams also fail to tensorize their
  permutation charge: repeating one last-vertex constraint costs \(1/|T|\),
  not \(|T|^{-m}\).  Kill noninflating scalar deletion, fixed-order or
  order-averaged carré self-bounds, collision-only upper states, and absolute
  diagrams.  Park exact Bellman and signed-diagram forms as restatements.
  Reopen P11/P82 only with a signed scalar-output parent-to-child
  contraction; otherwise attack P14 directly.
  P123 gives the current direct-P14 normalization.  For a set \(B\) of
  density \(a\), let \(q_i\) be the smaller front-bit mass and
  \(\rho_i^\pm\) the two conditional opposite-section laws.  Then

      |T_n(1_B)/a - sum_i q_i W1(rho_i^+,rho_i^-)|
          <= sqrt(2n(n-1)) log(1/a).

  The error is proved at the target entropy scale, so the matched dependence
  endpoint is equivalent to P14, not a smaller leaf.  Exact binary
  Wasserstein disintegration creates diagonal cross-corner transports under
  deletion.  Dropping them fails on two-bit parity; retaining all corners
  reconstructs the original coupling LP; comparing corners separately to
  the ambient cube loses \(\sqrt n\) on majority.  Scalar mutual information
  is metrically blind: parity and a majority graph can have identical scalar
  information but conditional \(W_1\) distances \(1\) and
  \(\asymp\sqrt n\).  Two further exact adversaries are mandatory.  For
  quadratic tails \(A=\{(\sum_iZ_i)^2\ge t\}\),

      T_n(1_A) = L_2(1_A) = E[1_A((sum_i Z_i)^2-n)/2],

  while every coordinate section has the parent density; scalar deletion is
  therefore blind on the strongest known finite P14 calibrators.  Conversely,
  a full-support binary code has

      T_n(1_C) = (mu(C)/2) sum_i(d_i-1),

  and simplex codes have \(L_2=0\) but
  \((T_n-L_2)/(n\mu(C))\to\infty\).  Kill any universal
  \(T_n\le L_2+Cna\) repair.  A valid continuation needs a signed,
  cycle-coherent cross-corner state with a strict parent-to-child gain that
  retains both quadratic alignment and global section-support separation.
  A direct total-correlation assay has now been audited.  If
  `pi=product_i nu_i`, oriented exact row KR potentials produce

      E_nu F_phi = M_n(B),
      E_pi F_phi = 0,
      D(nu||pi) = TC(nu).

  The linear claim `M_n<=C n TC` is false on a punctured subcube, where
  `M_n` has an extra factor `m`.  The scale-compatible replacement

      M_n <= C n (sqrt(TC)+TC)

  would follow by entropy duality if one could select centered exact normers
  satisfying a product-law mgf estimate at the single scale

      lambda_D=(c/n) min(1,sqrt(TC)).

  Do not quantify over every exact normer.  Without centering, additive
  constants make every dimension-only mgf envelope false.  After centering,
  all-normer quantification is circular: on a coordinate halfcube every
  centered one-Lipschitz row function is an exact normer for a zero row, so
  the contact field contains arbitrary native residuals.

  The current canonical repair is strictly stronger than existential
  selection but avoids both walls.  On the centered exposed KR face
  `K_i^0`, select the unique minimizer

      phi_i^o = argmin_(phi in K_i^0) E_(pi_-i) phi^2.

  Product-law centering removes additive gauge; if the row cost is zero,
  strict convexity selects `phi_i^o=0`, so the halfcube circularity
  disappears.  For `F^o=sum_i A_i phi_i^o`, test

      log E_pi exp(lambda_D F^o) <= C lambda_D^2 n^2,
      lambda_D=(c/n) min(1,sqrt(TC)),  0<c<1.

  P177 now supplies proof-grade structure.  For every centered
  one-Lipschitz selection, not only the canonical one,

      Var_pi(F) <= n(n-1)/2.

  Thus the target has the correct quadratic scale at the origin; the
  missing content begins in higher cumulants at distance `1/n`.  Canonical
  KKT gives an exact potential--flow identity.  More sharply, every
  connected component of the saturated-edge graph of `phi_i^o` is centered
  separately.  If all such component diameters are at most `d`, then

      log E_pi exp(lambda F^o) <= (d^2/2) lambda^2 n^2

  for every real `lambda`.

  The selector mgf is proved for every permutation-invariant set:

      log E_pi exp(lambda F^o) <= 256 lambda^2 n^2,
      |lambda| <= 1/(16n).

  This closes full parity, antipodal repetition, every radial shell union,
  and P158's radial plateau as selector classes.  Repetition still shows
  that `c=1` is a genuine radius-of-convergence wall.  Certified exhaustive
  QP tests through dimension three find no violation, but are
  falsification evidence only.

  The coordinatewise-positive Green route is closed.  It used

      G^o = L_pi^{-1} F^o,
      V_+^o = (1/2) sum_j E_j' [(Delta_j G^o)(Delta_j F^o)]_+.

  Both the tilted mean condition and P178's untilted exponential
  strengthening are valid sufficient statements, but their universal
  premises are false.  On the canonical P158 plateau, with
  `n=h^2=16r^2`, the lower-tail gradients are

      Delta_k G^o = -2h-(-1)^k,
      Delta_k F^o = -2h-n(-1)^k.

  Thus one parity of edges has positive product of order `h n`, and on a
  fixed-probability binomial band

      V_+^o / n^2 >= h/8.

  Consequently `E V_+^o/n^2` grows like `sqrt(n)` and every fixed
  exponential moment of `V_+^o/n^2` diverges.  The actual P177 mgf remains
  uniformly bounded on this family.  Taking the positive part coordinate
  by coordinate has deleted essential alternating cancellation.  Retire
  semigroup moment, self-bound, and KKT-to-codimension attacks on `V_+`.

  P179 is an exact signed-secant implication, but no longer a live
  universal premise.  Set

      kappa(x)=(1-exp(-x))/x,
      W_t=(1/2) sum_j E_j'
          [(Delta_j G^o)(Delta_j F^o) kappa(t Delta_j F^o)],
      Q_t=exp(tF^o-m(t)) pi.

  Exchangeability gives the exact identity

      m'(t)=t E_(Q_t) W_t.

  Therefore the aggregate-positive estimate

      E_(Q_t) [W_t]_+ <= C_c n^2,   |t|<=c/n,

  implies the P177 one-scale mgf.  P158 passes this condition for every
  fixed `c<1`, but universal validity is false even at `t=0`.  For
  complement-symmetric Boolean shell bits with `b_0=0,b_1=1`, the exact
  prefix signs force every minimum-`L^2` canonical KR slope to be

      phi_(r+1)-phi_r = 1-2 b_(r+1).

  Random central shell bits therefore create iid saturated slopes in the
  actual canonical selector.  The exact radial Green expansion and
  Khintchine give

      E [W_0]_+ >= c n^(9/4).

  These sets are permutation invariant, so their true P177 mgf is uniformly
  bounded.  P179 has lost essential cancellation only at the final positive
  truncation.  Retire P179, its `F`-conditioned positive repair unless a
  separate asymptotic theorem is proved, and every claim that canonical KKT
  provenance alone forbids independent cross-scale radial slopes.

  P182 is the primary strict successor.  For centered `X`, define

      b_+(X)=sup_(u>=0) E[(X-u)_+]/P(X>u),
      b_-(X)=b_+(-X),  b=max(b_+,b_-).

  Layer cake gives the exact recursion

      E|X|^k <= (k!/2) b^(k-2) Var(X),

  and hence

      log E exp(tX) <= Var(X)t^2/[2(1-b|t|)].

  Therefore `b(F^o)<=C n`, together with the P177 variance theorem, closes
  the one-scale mgf.  Repetition forces `C>=2`.  The statement is genuinely
  stronger than the mgf: a sufficiently rare scalar `n^2` spike separates
  them.

  P182 is proved for every permutation-invariant canonical field:

      b_+(F^o), b_-(F^o) <= 10000 n.

  The proof is uniform in the common bias and in arbitrary radial
  one-Lipschitz slope patterns.  It decomposes the field into a product term
  satisfying a quadratic binomial envelope plus an `O(n)` oscillatory
  perturbation.  Every superlevel component is an interval; monotone
  adjacent binomial-mass ratios control its conditional overshoot.  No
  monotonicity of the potential or its slopes is used.

  The nonradial interaction theorem is sharper.  For

      D_i={j: Delta_j phi_i is not identically zero},

  hub conditioning gives an explicit certificate

      b_+(F), b_-(F) <= min_H Gamma(H) <= sum_i |D_i|.

  Thus O(n) total directed interaction incidence, bounded average row
  width, bounded interaction components, and fixed active-row width are
  closed, even without canonical selection.  The fixed-k bound is
  k(n-1).  A complementary weighted theorem uses

      ell_ij=sup |Delta_j phi_i|.

  Bounded two-sided row/column load gives P182.  Exact dependency
  components of size at most sqrt(n) give P177, and so does any partition
  into sub-root blocks whose total weighted cross-load is O(n).

  Without any sparsity, a near-maximal residual creates a long
  weak-expansion ladder and a boundary band with large aggregate row
  amplitude.  Product expansion lower-bounds the band mass; event-localized
  McDiarmid bounds its conditional row amplitude.  The resulting bootstrap
  proves the strict universal estimate

      b_+(F), b_-(F) <= C n^(7/5)

  for every centered contact field.  If b(F)=kappa n, some near-maximal
  band crosses Omega(kappa^2) rows and meets a canonical saturated
  component of diameter Omega(kappa^2).  This is a genuine exponent and
  falsifier-profile contraction, not the desired linear closure.

  The current inverse-ladder package is idempotent at exponent 7/5.
  Optimizing the threshold approximation, using all ladder rungs, or
  feeding back the hub and long-component conclusions returns the same
  exponent.  Its exact exponent formula is

      beta=(a+gamma+mu theta)/(2+nu theta),

  and a dense affine-row family makes the unsigned event-local amplitude
  estimate sharp at the critical mass scale.  That family is not an
  arbitrary-row artifact: the antipodal repetition set has the unique
  centered exact canonical rows

      phi_i^o=(1/2) sum_(j!=i) Z_j,

  and saturates the same amplitude scale on an actual O(n)-width band of
  its contact field.  Boolean common provenance, minimum-L2 selection, KKT
  contact, full saturation, and thin-band localization therefore do not
  improve the unsigned input.  Repetition itself has linear mean residual
  life, so the missing estimate must also be aligned to a near-maximal
  residual band.  Do not relaunch a scalar bootstrap without a genuinely
  new signed, residual-aligned estimate.

  Every centered row selection also has

      max_edge |Delta F| <= 3(n-1).

  Exhaustive canonical search through `n=4` and a certified adversarial
  `n=5` packet leave repetition extremal.  This is evidence only.  A
  failure must be robustly dense under the hub and weighted-partition
  certificates, and must sustain diffuse signed threshold contact across a
  long nested superlevel ladder.  The exact next object is

      C_i(eps,u)
        =eps(1-p_i) E[phi_i
          (1_{Q_{i,s_i}}-1_{Q_{i,-s_i}})],
      Q={eps F>u},

  with target sum_i C_i <= (u+C n) P(Q).  Taking absolute values returns
  to P14 and loses the threshold rebate.  The contacts are not individually
  nonnegative: an exact canonical five-cube witness has a negative row at
  its unique maximizing prefix.  What remains true is the transverse
  transfer

      sum_i (-C_i)_+
        <= E[1_Q sum_i 1_{X_i}|R_i|],

  so wrong-sign contact must be created by cross-row derivative
  interference on the same threshold boundary.

  Truncation exposes the exact signed first-power identity.  For
  `a_u=(eps F-u)_+`,

      sum_i theta_i E[eps phi_i D_i a_u]
        = u E a_u + E a_u^2.

  Equivalently, this is the integral over levels of the signed P187
  contacts.  It retains precisely the threshold rebate lost by unsigned
  amplitude bounds.  But do not take positive parts rowwise or fiberwise:
  canonical radial shell unions make that positive truncated flux at least
  order n^(9/4), while n E(F^o)_+=O(n^2) and the true P182 bound is linear.
  Cancellation must occur before positive localization or be charged by an
  equally signed transverse term.

  Raw matrix structure does not close that load.  Every balanced Boolean
  graph has b_+,b_- <= n-1, even though explicit members have complete
  interaction and maximal signed-Jacobian stable rank.  Parity makes the
  outward-drop and cross-interaction terms n^2 and n^2-n separately.
  Therefore stable rank, cut norm, pairwise phase, and separate operator
  control are parked.  The primary continuation must retain the total
  threshold rebate and nonlinear common-source KR structure.

  Do not infer P182 from variance and edge oscillation alone.  If
  `H~Bin(n,1/2)`, `a=ceil(sqrt(n log n))`, and
  `X=(H-n/2-a)_+ - E(H-n/2-a)_+`, then `Var(X)<=1`, the edge oscillation is
  one, but `b_+(X)>=c sqrt(n/log n)`.  The surviving descent theorem must
  use exact common-indicator KR contact to exclude a scaled version of
  this moderate-deviation ramp.  The active problem is the universal
  nonradial P182 bound under that provenance.

  Two parallel post-P179 attacks are admissible.  First, seek an
  exponential `n^2`-scale bound for the predictable Doob bracket of
  `F^o`.  Bennett's supermartingale and the universal canonical reveal
  bound `|d_k|<=3(n-1)` prove that this bracket estimate implies P177.  It
  is proved for the entire permutation-invariant canonical class.
  Pointwise bracket control is false on repetition, whose maximum bracket
  is order `n^3` but whose bracket has a uniform exponential moment at
  scale `n^2`.  On the fair cube the bracket is exactly the old P82
  chronological square, so canonical provenance must supply the genuinely
  new nonradial estimate.  Direct local conditional-variance depletion is
  false already for an exact canonical three-coordinate set: every first
  reveal has zero bracket but unequal child variances.  A time-reserved
  curvature hypothesis does imply the exponential bracket, but exact
  canonical radial shell unions violate that local hypothesis by an
  unbounded factor while their actual bracket remains good.  The same wall
  survives every fixed correction by conditional row-square energy.
  Therefore only a rarity-weighted path argument or accumulated-bracket
  descent remains credible; worst-node variance depletion is closed.

  The exact accumulated object is now known.  If

      Y_k=Var(F^o | F_k),
      Delta_k=Y_k^+-Y_k^-,
      e_k=Y_k-E[Y_k|F_(k-1)],

  then

      V=Y_0+sum_k e_k.

  With

      psi_p(x)=log((1-p)e^(-px)+p e^((1-p)x)),
      Psi_(rho,lambda)=sum_k psi_(p_k)(2 lambda Delta_k/n^2),

  one has the exact one-way reduction

      log E exp(lambda V/n^2)
        <= lambda Y_0/n^2 + (1/2) log E exp(Psi_(rho,lambda)).

  The square gate `sum_k Delta_k^2/n^4` is a stronger fair-cube assay.
  Variance-monotone reveal trees satisfy the bracket gate; parity has zero
  cost and repetition satisfies the square gate.  The universal Psi gate
  is valid but is not yet a strict contraction: no canonical bound or
  quantitative separation currently makes it easier than the bracket.
  Rarity of the single P185 node does not control the whole tilted path.

  An event-local entropy formulation does not shrink this debt.  The bound

      E[Psi_(rho,lambda) | A]
        <= K + eta log(1/P(A)),   eta<1,

  for every terminal event implies `log E exp(Psi)<=O(1)`.  Conversely, a
  P192 exponential bound at parameter `Lambda` implies this condition at
  `lambda=t Lambda` with `eta=t<1`, because
  `Psi_(rho,t Lambda)<=t Psi_(rho,Lambda)`.  Thus path-space entropy is an
  exact rarity interpretation but is equivalent to P192 after parameter
  rescaling.  Do not promote it without a strictly smaller canonical
  information functional.

  P190 and P192 admit one exact scalar profile synthesis.  For

      K_X(u)=E(X-u)_+-(E X-u)_+,

  predictable reveal tents define a nonnegative random profile `Lambda`
  such that

      E Lambda(u)=K_X(u),
      2 integral Lambda(u) du = V

  pathwise.  P190 is the upper-tail Hardy transform of `E Lambda`; P192 is
  the scalar-area projection of the associated profile martingale.  This
  does not retain P190's row provenance and is not a contraction.  The P185
  three-point field has both child means zero, hence zero mean-splitting
  tent, but child variances 8/9 and 20/9, hence nonzero profile-shape area
  2/3.  Direct pointwise or area domination of fixed-mean shape exchange by
  mean splitting is closed.  Only a global reach-weighted canonical bound
  on accumulated shape exchange remains conceivable in this language.

  The full-profile candidate makes that remaining direction precise.  Put

      Q_k=2 integral |K_k^+-K_k^-|.

  Since `|Delta_k|<=Q_k`, an exponential bound for
  `n^(-4) sum_k Q_k^2` implies the P192 square gate.  An exact canonical
  Q_10 shell has zero tent and `Delta_k=0` but `Q_k=3/2`, so local convex
  order, tent, and signed-area comparison are false even under exact
  provenance.  A generic rare-trigger martingale with variance at most
  n^2 and reveal increments at most n makes the reach-weighted Q-gate
  diverge, so scalar profile/entropy/reach data cannot prove it.  That
  martingale is not a canonical contact field; the full-profile gate is not
  refuted.  Reopen it only with the original minimum-L2 rowwise KR/KKT
  currents retained inside the accumulated second-order transport estimate.

  A fixed-density native walkback also closes a common loop.  At a global
  P14 maximizer every exact aggregate normer lies in the normal cone, so the
  set is a top-level set; maximizing its threshold plus overshoot is exactly
  the fixed-density P14/AVaR dual.  The outer l1 norm is flat under tangent
  redistribution among positive row costs and has no Euclidean swap square.
  Static top-level contact is therefore an equivalent reformulation, not a
  contraction.  Re-entry at P14 needs a dynamic Boolean exchange principle.

  The first three provenance-preserving continuations have now been audited.
  P197 expands the signed threshold flux into ordered row pairs:

      u E a_u + E a_u^2 = D_u - J_u.

  Antisymmetric curl cancels exactly and only symmetric row strain remains.
  Every negative front contact has a congestion-one local transfer, but
  canonical pairwise strain positivity and generic total positivity are
  false; the unrestricted all-cuts condition is the P182 second-residual
  target itself.  P198 shows that parity and repetition have identical signed
  threshold interaction matrices but incompatible rebate accounting.  Thus
  Hodge/cycle control and matrix-only signed expansion are closed.  Re-enter
  the threshold-current route only with front anchors, threshold level, and
  original KKT source provenance retained simultaneously.

  P199 lifts the scalar threshold-profile descent to row-labelled currents
  `c_(r,i)` and areas `d_(r,i)`, with

      Delta_r = sum_i d_(r,i).

  The lift resolves further into the original KKT source currents and excludes
  the generic rare-trigger architecture for `n>=17`.  Its natural Hilbertian
  gate is nevertheless false on canonical repetition:

      E[n sum_k ||d_k||_2^2]
        = n^2(n-2)(n-1)(n+1)/3,

  one factor `n` too large.  Continue only through signed cancellation,
  conditional low rank, or a smaller source-flow norm before squaring.

  P200 gives the first strict fixed-density walkback below the static AVaR
  equivalence.  Put

      H_n(m)=(2^n/m) max_(|A|=m) T_n(1_A).

  If `A` is a maximizer and `F_A` is any exact aggregate normer, then
  `H_n(m)=AVaR_(m/2^n)(F_A)`.  The dyadic increment

      AVaR_a(F_A)-AVaR_(2a)(F_A) <= C n

  for `a<=1/4` iterates directly to P14.  An exterior edge injection
  `A -> A^c` proves this with `C=1`, because every admissible contact changes
  by at most `2(n-1)` on a cube edge.  Literal matching is a strong sufficient
  certificate, not the native target: Hall-deficient radial sets can already
  be exact local P14 maximizers.  Bounded average Hamming length is also
  miscalibrated: deep exact quadratic tails force length
  `sqrt(n/log n)` while retaining the desired linear contact increment.

  P202 supplies the calibrated replacement.  Give an oriented edge the cost

      c_F(u,v)=[F(u)-F(v)]_+

  and let `D_F(A)` be the minimum capped exterior path-transport cost.  If at
  every sparse cardinality some P14 maximizer admits an exact normal field
  with `D_F(A)<=C n`, then P14 follows.  This normer-descent exterior-flow
  condition allows long paths and charges only downward variation; the
  quadratic calibrator satisfies it with linear cost.  Pair cost
  `F(x)-F(y)` without pathwise positive variation is exactly the dyadic AVaR
  gap and is circular.  The active missing theorem must convert a weighted
  Hall/min-cost-flow obstruction into a global cardinality-preserving set
  exchange and control row-normer rotation or reoptimization.  One-swap or
  another fixed-normer AVaR calculation is insufficient.

  P201 makes the rotation debt exact.  For a same-cardinality exchange,

      T(B)-T(A)=E[(1_B-1_A)F_A]+sum_i R_i,

  where `R_i>=0` is the slack of the new optimal row flow against the old
  exact potential.  A Hall-rooted `Q_6` swap has frozen gain `-15/256`,
  rotation reserve `35/512`, and actual gain `5/512`.  Therefore frozen
  normal scores can miss a genuine improving exchange.  A maximality-to-NDEF
  theorem must lower-bound the new-row flow slack from the deficient-flow
  certificate; formal first variation or normer uniqueness does not suffice.

  P206 gives the exact NDEF dual geometry.  Dual potentials are graphwise
  isotone one-contractions of `F`; after scalar uncrossing their value is a
  weighted packing of nested `F`-oriented cuts with positive `A`-imbalance.
  Lexicographic minimization among maximizing set--normer pairs controls only
  the threshold plateau.  Repetition has a unique top set and an optimal cut
  in the strict core.  Pointwise weighted Hall at radius `O(n)` is false on
  deep quadratic tails even though their average NDEF cost is linear.

  P204 rewrites the P201 reserve as a row-residual min-cost flow with arc
  cost `1-(phi_i(u)-phi_i(v))`.  A singleton exact contact has raw dyadic gap
  zero and NDEF `2(n-1)`, while every singleton exchange has reserve exactly
  equal to frozen loss.  Therefore a positive cut cannot by itself force
  improvement; a valid OCX/coupled-flow theorem must first pay an `O(n)`
  baseline and use only superlinear aggregate cut mass.

  P207 audits the first direct row-shadow shortcut.  On a directed
  `j`-edge,

      F(z)-F(z^j)
        =2 z_j phi_j(z_-j)+(n-1)-sum_(i!=j) s_i(a_ij,b_ij).

  Aggregate descent therefore favors small sign-corrected forward residual
  slacks, and the direct term has no row-edge analogue.  P208 proves that
  strict cheap-reachability closure turns every expensive reverse arc into a
  feasible residual cut certificate.  Check the native normalization before
  using it: since

      h_i(B)=1/2 (g_i^B-E g_i^B),

  a point swap contributes `2^(-n)`, not `2^(-(n-1))`, to one row cut.  The
  corrected edge gain is

      T(B_e)-T(A) >= (|I_e|-c_e)/2^n-sum_i d_(i,e).

  It is vacuous on singleton/repetition first exits.  P209 additionally
  refutes automatic one-signed-shadow extraction for one selected exact
  `Q_4` pair/dual, without refuting full multi-shadow packing or
  existence-form OCX.  Exact P205/P209 data remain finite evidence; ordinary
  concavity and log-concavity of the maximum envelope are refuted by a
  written `Q_3` orbit calculation.

  P210 gives an independent direct walkback.  For a maximizer `A`, a
  coordinate translate, collision `I_j=A intersect tau_j A`, and a
  fractional exterior relocation `d`,

      2 K_n(m)-K_n(2m)
        <= 4 n m/2^n + T_n(d-1_(I_j)).

  Hence `T_n(d-1_(I_j))<=C n m/2^n` for one admissible `(j,d)` at every
  sparse cardinality closes the P200 increment and P14.  Low overlap merges
  with bounded Hamming assignment.  P211 proves the genuinely large-overlap
  nearest-shell theorem for every sparse one-sided and symmetric two-sided
  threshold:

      T_n(d-1_(I_j)) <= 33 (n-1) mu(I_j).

  P213 gives the exact collision--exterior AVaR dual and the universal
  quadratic-overlap estimate

      inf_d T_n(d-1_(I_j)) <= (sqrt(3)/2) n sqrt(mu(I_j)).

  Thus overlap `O(a^2)` closes FCR, complementing the old `O(a/n)` regime.
  The hybrid near-maximal-influence condition

      min_j mu(A intersect tau_j A) <= C a (a+1/n)

  for one maximizer at every sparse cardinality would close P14, but remains
  open universally.  P216 gives the exact erasure identity

      mu(A intersect tau_j A)/a = H(X_j | X_-j)/log(2)

  and the collision-sensitive row ceiling

      t_j(1_A) <= ((n-1)/2)(a-mu(A intersect tau_j A)).

  For a fixed-cardinality maximizer, comparison with the quadratic
  antipodal contact proves

      min_j mu(A intersect tau_j A) <= 4 a r_m/(n-1),

  where `r_m` is the least radius whose two antipodal Hamming balls contain
  `m` points.  Hence NMI holds when `r_m=O(1+na)`, including each fixed
  polynomial cardinality scale and densities bounded away from zero, with
  parameter-dependent constants.  Growing-radius antipodal balls violate
  arbitrary-set NMI by ratio asymptotic to `2 r_m` while having the
  quadratic field as an exact top-level normer.  This threatens NMI, not
  FCR: P211 already proves FCR for those radial thresholds.  One bad
  maximizing orbit would refute only an every-maximizer form; the
  existential P213 lemma fails only if every maximizer at a sequence of
  cardinalities is bad.

  P217 gives a canonical strict child of FCR.  If `u>=0` is the unique
  capacity-obstacle odometer for collision `I` and empty fibers `E`, then
  `d=1_I-(I-P)u` is admissible and

      C(I,E)
        <= T_s(d-1_I)
        <= (2/s) sum_(i!=j) E |partial_i partial_j u|.

  This reduces the CEAG supremum to the off-diagonal `L^1` Hessian of one
  nonnegative obstacle solution.  P218 proves the formerly open radial
  child.  In cumulative radial flux variables,

      sum_(k=0)^(D-1) |D-2-2k| |Q_k| <= 2(D+1)a,

  and consequently the radial obstacle Hessian is at most `10Da`.
  The proof uses contact-component envelopes and binomial hazard bounds.

  P219 then closes the nonradial problem by a different, shorter
  mechanism.  Obstacle complementarity gives

      p=mu_s{u>0} <= 2a,
      ||L_s u||_2 <= (s/2) sqrt(2b),   b=mu_s(I)<=a.

  For every function supported on a set of mass `p`,

      sum_(r!=t) ||D_r D_t u||_1
        <= 2s sqrt(p) ||L_s u||_2.

  Indeed each mixed derivative is supported on four translates of
  `supp(u)`, Cauchy--Schwarz localizes its `L1` norm, and Walsh
  orthogonality gives

      sum_(r!=t) ||D_r D_t u||_2^2
        <= ||L_s u||_2^2.

  Therefore

      sum_(r!=t) E|partial_r partial_t u| <= 2s^2 a,
      T_s(d-1_I) <= 4sa.

  The lift to the ambient cube preserves `T`, so P210 gives

      H_n(m)-H_n(2m) <= 4n-2.

  P200 iteration proves P14, exact transport duality proves the
  Rademacher derivative-budget rate, and P88 gives the general-product
  BKZ rate.

  Keep the proof/wall distinction explicit.  P219 does not bound total
  occupation and does not prove obstacle relocation is FCR-optimal.
  First-quartile thresholds still have `E u/a` of order `s`, and the exact
  radial `Q_10` witness still makes heat balayage more than `2.28` times an
  explicit admissible competitor.  Those facts refute the occupation and
  optimality proxies, not the sparse-support Hessian proof.  Conversely,
  do not apply the P219 conclusion to an arbitrary Hessian field: the
  support bound and the source `L2` bound come specifically from obstacle
  complementarity, capacity, and mass balance.

  P215 exhaustively certifies `K_5(6)=1`, one maximizing isometry orbit, and
  collision profile `(4,4,0,0,0)` for every maximizer.  Thus the exact
  disjoint-coordinate evidence reaches size six in `Q_5`; sizes seven and
  eight are the next finite layers.  P212/P214 refute both
  coordinate-compression monotonicity directions, even after minimizing the
  FCR defect over the coordinate.  Do not use ordinary polarization to
  reduce FCR to radial sets.

  Second, test separate
  upper stop-loss domination of `F^o` and `-F^o` by a universal dilation of
  the repetition field `(S_n^2-n)/2`.  Full convex order is false on the
  iid-shell witness, and ordinary coordinate compression is nonmonotone.
  Uniform Hanson--Wright for deterministic matrix families and fixed-degree
  higher-derivative inequalities do not transfer to the state-dependent,
  degree-`n` field; a viable theorem must retain pair-exclusion or equivalent
  canonical cancellation.

  The unaveraged double-KKT geometry is now closed.  At a global
  mgf-minimizing selector the exact saddle is

      tau_tilde_i + b_i sigma_i + B q_i = 0.

  If `H_i` is a native optimal contact flow, then

      (b_i,q_i) -> (b_i-c,q_i+cH_i)

  is an exact gauge.  Raw mass, overlap, and domination are therefore not
  invariant.  Gauge fixing by the largest feasible multiplier yields a
  maximal upper-cut ratio `gamma_i`, and `sum_i gamma_i W_i <= C t n^2`
  would imply the selected mgf.  P158 refutes this proxy exponentially:
  its singleton tail cut has `gamma_i(c/n) >= C_c exp(c sqrt(n))` while
  P179 stays bounded.  Retire raw paired-flow, worst-cut, and codimension
  attacks.  Only an averaged signed, mass-sensitive use of the exact
  saddle and common-density curl survives.
  P124 tests the exact signed binary-cycle continuation.  Its common-order
  bicausal cost is a genuine restricted coupling class, dominates the P123
  matched core, and passes parity, majority, twisted fibers, and quadratic
  tails.  It still has total child coefficient one: opposite parity has
  zero cycle curvature, zero scalar entropy decrement, and two copies of
  the parent.  A \(1-1/m\) deletion identity holds for the realized cost of
  one common optimal coupling, but it does not recurse on the original
  sections: conditioning on both exposed signs changes both tail marginals.
  On \(P=\operatorname{Unif}\{01,10\}\) and
  \(Q=\operatorname{Unif}\{00,01,10\}\), the weighted original-section
  cost is \(1/3\) while the deleted realized cost is \(1/6\).  Park
  bicausal deletion.  Reopen only with a signed state that controls these
  cross-conditioning marginal corrections at the target scale.
  P125 closes the natural order-flexible variants.  Exogenous order
  mixtures minimize at one deterministic order; marginally faithful
  adaptive trees retain the coefficient-one Bellman recursion, and the
  same two-bit pair refutes their \(1-1/m\) continuation contraction.
  Endpoint-informed seeds recover every coupling.  Plans bicausal in every
  order do contract under deletion, but opposite majority forces
  \(K_{\rm all}\ge(m+1)(1+\lambda_m/m)/4\) while
  \(W_1=\lambda_m\le\sqrt m\).  Hence all-order faithfulness loses
  \(\sqrt m\).  Do not reopen random/adaptive/all-order bicausal deletion
  without a new signed cross-row invariant.
  P126--P130 give the first all-order native affine/common-core contraction
  and its post-P130 branch audit.
  For an output `F=chi_C H`, projection onto the common-core character and
  permutation averaging give an exact quotient normal form: one scalar
  transfer row `A`, outside rows `B_i`, and precisely the core--core,
  core--outside, and outside--outside chord constraints.  This is a genuine
  smaller state for the subclass, not a universal P89 reformulation.  For
  the signed P105 affine packets, every four-block xor relation is paired;
  every genuine six-block relation is either a six-line affine-plane circuit
  or a level-two block with its five lines through a point.  At length eight,
  a maximum-block cover proves that no distinct zero-xor support can meet a
  level `m>=3`.  After repeated-pair reduction, the high levels therefore
  have exactly the joint eighth moments of independent Rademachers relative
  to the two low levels.  Consequently arbitrary signed weights and any
  disjoint common core satisfy native P89 through `p=8`, uniformly in the
  number of levels.  P129 then supplies two exact all-order reductions.
  Arbitrary coefficient phases are dominated with constant one in every
  even moment by the positive packet.  At order `s`, every level above
  `floor(log_2(s-1))` can be replaced exactly by independent block signs
  relative to the lower levels.  Combining the remaining `O(log s)` levels
  by P106 and Cauchy--Schwarz proves

      ||sum_m t_m h_m||_s <= s sqrt(log_2(2s)) ||t||_2.

  This is substantive all-order subclass progress, not universal closure
  and not yet the linear rate.  The exact residual is positive convolution
  flattening.  Its correct combinatorial language is the weighted activity
  of inclusion-minimal binary incidence cycles (matroid circuits), not
  ordinary connected covers.  P130 proves both directions: exponential
  primitive activity implies linear moments by the cosh--tanh expansion,
  while every primitive `r`-circuit contributes `r!` positive ordered terms,
  so linear moments imply exponential primitive activity.  Thus AOE is an
  equivalent target up to constants, not a smaller crux.

  Do not project only to traces at one maximum block.  With equal
  `l2`-normalized weights across the first `m` levels, the exact
  singleton-trace polynomial has root growth at least `sqrt(m)` after
  exterior parity is discarded.  Also do not seek the one-level transition
  through `||Gamma||_q <= C(k+q)` or through
  `||S_pi||_p <= C(1+sqrt(p/k))`: a low-rank incidence-kernel atom on
  `AG(2,4^m)` refutes both by unbounded factors, for every fixed or
  predictable adaptive order, while remaining harmless for the terminal
  polynomial.  These are proxy walls, not counterexamples to the affine
  moment estimate.

  The affine branch is parked after the bounded audit.  Re-entry requires a
  strict `l2`-anchored exterior-parity estimate, for example

      sum_{C primitive, A(C)=A} prod_{B in C} u_B
      <= K^r u_A^2 (sum_B u_B^2)^((r-2)/2),

  proved through a full paired-incidence/nonbacktracking closure or an
  affine-code shortening recursion.  Do not make either a live route before
  its bounded preflight proves a strict contraction.  Do not substitute generic four-circuit freeness or
  a dissociated-set partition: APN Sidon caps have no nonpaired
  four-relations but exponentially large high moments, and a level-one
  affine packet requires order `n` dissociated classes.  Also do not treat
  the subfields as a nested chain, condition on the full level-one algebra,
  reconstruct from one independent spread, use only whole-affine-block
  exchangeable flips, or close multiplication in the span of the original
  level sums.  The gcd intersection law, deterministic level-one
  reconstruction, top-parity zero mode, and six/eight-point product orbits
  close those mechanisms exactly.
  The durable P124 literature packet confirms that no standard import fills
  this gap.  Bicausal dynamic programming gives the fixed-order recursion
  without contraction; Marton/Dobrushin entropy contraction excludes hard
  parity constraints; trajectory-coupling theorems require a dependence
  matrix whose control is the missing geometry; and nonnegative weak-cost
  tensorization through the ambient reference repeats the majority-refuted
  triangle step.  Do not open a generic Marton/Knothe/Bellman route without
  a new signed, order-flexible contraction.
  P111 also identifies the exact quotient-Hodge matrix
  H(F)=2(D_iD_jL^(-1)F)_(ij), but its natural bilinear estimate is P89
  itself.  Common-core fields refute local differential subordination, and
  Hutchinson, sparse-diagonal, and pointwise Schatten scalarizations fail at
  the target scale.  These are strict class/structure gains and decisive
  branch walls, not universal closure.
  P87 mixed shifted Hessian is P89's stronger
  canonical-tensor child and also implies the stronger P22/P24 Green route,
  but P102 shows that the P100--P101 rooted phase of its fixed canonical
  representative is not invariant under the P89 zero-divergence quotient.
  Treat P87/P99 as stalled unless a new quotient-invariant gain appears.
  P131 also closes the most direct stochastic import: every exact linear
  full-space semigroup representation of the P87 pair trace has coefficient
  norm at least `sqrt(n-1)/2`; the natural shared-coefficient representation
  is sharp up to `sqrt(2)`.  A black-box full-space differential-subordination
  bound on one shared path therefore retains the forbidden `sqrt(n)` loss.
  This wall does not cover restricted gradient-range estimates, several
  coupled transforms, or nonlinear/input-dependent constructions.
  Inside P87,
  P97 gives the exact common-circle range and P98 proves its sharp
  half-derivative; P99 records a generic candidate random-insertion
  factorization but no structural contraction, so the coherent
  cycle--Riesz multiplier remains active;
  P78 is parked;
- one proved bridge: P88 dimension-neutral transfer from the Rademacher
  residual theorem to arbitrary product spaces;
- one parked native-compatible strengthening: P11/P82 random-order square
  function.

Do not create a new active branch merely by renaming P14, P22, or P11.  A new
branch must supply a strict gain, a counterexample, or a smaller native lemma
with a decisive promote/kill test.

## Native theorem and closure

The BKZ conjecture asks for

    ||sum_i g_i||_p <= C (p n beta + M sqrt(p n)),   p >= 2,

under

    |E[g_i | Z_i]| <= M,
    E[g_i | Z_{-i}] = 0,
    changing Z_j, j != i, changes g_i by at most beta.

The independent one-coordinate main effects already give the
`M sqrt(p n)` term.  For Rademacher inputs, the residual problem is

    R = sum_i Z_i q_i(Z_{-i}),
    E q_i = 0,
    ||Delta_m q_i||_infinity <= beta/2  for m != i,

and the required estimate is

    ||R||_p <= C p n beta.

P219 proves this estimate through P14 and exact transport duality.  P88
then transfers the Rademacher theorem to the general-product theorem, with
only a universal change of constants.  Thus the native BKZ linear rate is
proved.

For the sharp all-moment formulation, put \(q=\min\{p,n\}\).  The proved
linear rate for \(p\le n\), the generic pointwise cap
\(|g_i|\le M+(n-1)\beta\) for \(p\ge n\), and the saturated quadratic
Rademacher example give

    sup_(BKZ class) ||sum_i g_i||_p
      \asymp n beta q + M sqrt(n q).

Do not continue treating \(p\gg n\) as an open lower-bound regime.  The
separate small-\(\delta\) lower bound for learning-algorithm generalization
remains open.

The proved P88 bridge is the dimension-neutral black-box implication

    Rademacher derivative-budget rate
      => general-product residual rate.

Its proof uses one independent pair and one orientation sign per original
coordinate.  After centering the induced cube rows, the Rademacher theorem
controls the centered part and bounded differences plus Khintchine control
the empirical row means at cost \(Cpn\beta\).  No atom count or encoding
depth enters.  Naive finite-atom or binary randomization remains invalid if
it replaces the original coordinate count n by the number of auxiliary
bits.

The bridge has been independently re-audited through v304.  The exact
orientation identity is obtained by swapping the two members of every pair
according to the orientation sign; the product pair law is invariant under
that swap.  After averaging an outside orientation, replacing the whole
outside pair changes a row mean by at most `beta`, not `2 beta`.  These are
the two delicate constants to recheck in any future modification.

## The two budgets must not be conflated

For

    q_i = sum_A qhat_i(A) chi_A,

pointwise stability controls

    ||Delta_m q_i||_infinity
      = ||sum_(A contains m) qhat_i(A) chi_A||_infinity.

The coefficient-slice hypothesis instead controls

    Lambda_(i,m) = sum_(A contains m) |qhat_i(A)|.

The coefficient condition implies the pointwise one, but the converse is
false.  Bent phases have bounded pointwise derivatives and exponentially
large Fourier `l1` slices.  Therefore:

- coefficientwise martingale, cumulant, or decoupling estimates may prove a
  genuine stronger-model theorem;
- they do not prove the native BKZ rate without a new, separately audited
  bridge;
- taking Fourier absolute values before using pointwise cancellation is a
  known fatal move.

## Exact native spine

### P14: transport endpoint

For a cube function `f`, let

    T_n(f) = sum_i ||partial_i f - E partial_i f||_(KR,n-1).

Exact duality and layer cake show, up to universal constants,

    Rademacher derivative-budget rate
      <=> T_n(1_A) <= C n a log(e/a),

where `a=min(mu(A),1-mu(A))`.  This set endpoint is the last exact native
layer.  It is proved by P219.  P138 below remains an informative stronger
strict sufficient formulation, but it is no longer load-bearing for the
linear-rate theorem.

### P80: exact cut-tower representation, no gain

Each row KR norm is exactly a maximum over an admissible nested cut tower,
equivalently a finite maximum-weight-closure/min-cut problem.  Summing rows
gives a signed laminar-discrepancy formulation with the same endpoint
constant as P14.

This preserves compatibility and is useful for exact falsification.  It does
not supply an entropy estimate or a smaller quantitative target.  Treat P80
as a representation attached to P14, not as another open leaf.

### P83/P85: matched sections, endpoint-equivalent

For `B` of density `a<=1/2`, let `M(B)` be the matched-section certificate
defined in the paper.  P83 gives the lower comparison and P85 proves

    T_n(1_B)/a <= M(B)
      <= T_n(1_B)/a + 2 (n-1) log(1/a).

Hence the universal entropy-scale endpoint for `M` is equivalent to P14 up to
constants.  The coefficient of the unknown `T_n/a` on the right is one, so
the comparison is not a contraction and cannot close the theorem by itself.

Two different losses must remain distinguished:

- transporting the two sections separately to the ambient cube loses
  `Theta(sqrt(n))` on balanced majority;
- comparing P83 to exact P14 coordinate by coordinate loses
  `Theta(sqrt(n))` in one row of the composed-majority example.

Neither example refutes the total P83 endpoint or P14.  P85 works globally.
The smaller Lipschitz constant of the cross-section Kantorovich potential
does not produce a bias contraction: composed majority gives an unbounded
violation if the marginal correction is deleted, and zero-barycenter quadratic thresholds
make the proposed gain identically zero.

### P86: nonlinear fixed-fiber closure

If a cube set has constant-cardinality fibers over a P14-good base, its P14
cost is bounded by the base matched certificate plus a target-scale fiber
error.  Fibers that are exponentially sparse in the added block preserve the
P14 endpoint.  In particular, graphs of arbitrary nonlinear vector-valued
Boolean maps cannot amplify a P14 defect.  This is a proved class closure,
not a reduction of arbitrary sets to systematic form.

Do not extrapolate this theorem by graph-layer atomization or by summing
transport between adjacent fibers.  The first proxy assigns total exact
graph cost `k(k-1)/4` to the half-cube
`{x_1=1} x Q_m`, although its native P14 cost is zero.  The second loses
`Theta(sqrt(k))` on

    B = {(x,y): H_k(x) P_m(y) = 1},

where `H_k` is odd-dimensional majority and `P_m` is base parity.  Adjacent
fibers are opposite majority halfspaces at Wasserstein distance
`E|S_k|`, but the full cube routes every base row at cost one by flipping a
different base coordinate.  Exact block/entropy decompositions remain valid,
but they retain lower-dimensional P14 with coefficient one plus a global
interaction norm.  Classify this as bookkeeping without descent.  A viable
fiber argument must preserve joint base-cube cycle coherence before taking
KR norms or absolute values.

### P74: exact chain rule with load-bearing child slack

The binary KR infimal-convolution identity yields

    (n-1) T_n = n average(T_(n-1)) + L_2 - Sigma.

Keeping the child Bellman slack merely rewrites the parent target.  Deleting
it is false already for two-bit parity.  Any inductive successor must add a
genuinely stronger state; the exact recurrence alone is not descent.

## One-way sufficient routes

### P138: Euclidean row transport

For a cube function `f`, set

    t_i(f) = ||partial_i f - E partial_i f||_(KR,n-1),
    K_n(f) = (sum_i t_i(f)^2)^(1/2).

The set gate

    K_n(1_A) <= C sqrt(n) a log(e/a)

is equivalent by layer cake and duality to

    ||sum_i Z_i q_i||_p
      <= C (p-1) sqrt(n) (sum_i Lip(q_i)^2)^(1/2).

Cauchy--Schwarz gives `T_n(f)<=sqrt(n)K_n(f)`, while every compatible P89
flow gives `K_n(f)<=C_n(f)/2`.  Hence

    P87 => P89 => P138 => P14.

This is a strict functional contraction from P89.  For odd `m`, put

    F_m=Z_1 Z_2 sgn(sum_(r=3)^(m+2) Z_r).

Independent exact row flows give `K_n(F_m)=O(1)`, whereas the rigid
degree-three coefficients force `C_n(F_m)>=c sqrt(m)`.  Do not attempt to
reconstruct a common P89 optimizer from the P138 row optimizers.  The live
mathematical target is still their anisotropic Euclidean moment gate, but
the P141 audit leaves no immediate same-direction child.  Mandatory tests are singleton,
antipodal, full and fixed-degree parity, majority, quadratic tails,
simplex/affine codes, this twisted-majority family, and the indexed-majority
multiplexer below.

P139 narrows the adversary space.  Every nonlinear systematic graph

    A_F = {(F(y),y): y in Q_m}

of codimension `k` satisfies P138 uniformly, and every affine code has exact
row energy

    K_n(1_C) = (a/2) (sum_i (d_i-1)^2)^(1/2).

The diagnostic identity

    R_138 = R_14 sqrt(n/N_eff),
    N_eff = T_n^2/K_n^2,

shows that a remaining obstruction must make
R_14 sqrt(n/N_eff) unbounded.  Strong anisotropy may compensate even a
vanishing P14 ratio, so do not add a near-extremality hypothesis.  This is a
class/adversary contraction, not a universal proof.

P141 adds one class theorem and four method walls.  If every base fiber has
fixed cardinality R and R <= 2^((1-delta)k), disjoint graph enumeration
proves P138 with a constant depending only on delta.  Positive graph
assembly is not universal: every systematic graph contained in odd majority
has more output than base coordinates, so graph bounds plus Minkowski lose
Theta(n) although majority itself is P138-benign.

The exact thresholded diagnostic is

    K_n(1_A)^2
      <= lambda^2 n a^2 L^2
         + a^2(n-1)/2 sum_(i:t_i>lambda a L) (ell-d_i),

where ell=log(1/a), L=1+ell, and d_i=D(nu_i||uniform).  Do not conjecture a
separate bound on the last sum.  For k=2^q, a label V in Q_q, outputs U in
Q_k, odd-majority input Y in Q_M, and

    B = {U_(J(V)) = sgn(sum_j Y_j)},

all marginals are uniform and every output row has

    t_(U_i)/a = E|S_M|/(2k).

Choosing M >> lambda^2 k^2 makes all k output rows high, so the separate
entropy charge is k log 2, while the actual P138 ratio is O(k^(-1/2)).  The
proxy has charged one shared latent majority transport once per label.  No
fixed threshold or weak-type count repairs it.  A joint entropy-rank quantity

    R_nu(H)=D(nu||mu)-D(nu_(H^c)||mu_(H^c))

survives this witness but is only an unproved preflight direction, not a
proved lemma.

P142 proves the exact individual deletion-entropy control

    e_i = D(nu||mu)-D(nu_-i||mu_-i)
        = log 2-H_nu(Z_i|Z_-i),
    (t_i/a)^2 <= (n-1) L e_i / log 2.

Do not sum these charges.  For odd \(k,M\), the half-density set

    B_(k,M)={Maj_k(U)=Maj_M(Y)}

has, for every \(U_i\),

    t_(U_i)/a=p_(k-1) E|S_M|/2,
    e_(U_i)=p_(k-1) log 2.

Taking \(M/k\) large makes all \(k\) rows high, but their deletion charges
sum to order \(\sqrt{k}\), while the exact total energy satisfies
\((K_n/a)^2\le n/4\).  This refutes deletion-entropy packing for every
fixed threshold.

For \(H\subseteq[n]\), joint rank has the exact localized interpretation

    R_nu(H)=D(nu||nu_(H^c) tensor mu_H),
    (sum_(i in H) r_i^2)^(1/2)
      = sup |(E_nu-E_(nu_(H^c) tensor mu_H))
               sum_(i in H) Z_i q_i|.

The threshold-selected estimate

    sum_(i in I_lambda) r_i^2
      <= C n L R_nu(I_lambda)

has completed its bounded P143 audit.  If \(h=|H|\), \(d=n-h\),
\(R=R_\nu(H)\), and \(S=\log(1/a)-R\), then

    sqrt(sum_(i in H) r_i^2)
      <= C [sqrt(d R (1+S))
            + min(h sqrt(R),sqrt(h R)+h^(3/2)R)].

This proves the gate for \(h^2\lesssim nL\) or \(h^3R\lesssim nL\).
Balanced monotone equality compositions satisfy

    sum_(i in I) r_i^2 <= (n/2) R_nu(I)

for every subset \(I\).  In general, however, the internally centered
conditional field is exactly P138 on \(Q_h\).  Importing lower-dimensional
P138 produces a fiber term plus a latent term whose cross product is not
constant-preserving.  The full-block case is P138 itself, while parity
refutes chain-increment allocation from submodularity.  Park unrestricted
joint rank; retain the proved regimes and the dense nonmonotone
large-high-block falsifier profile.

P144 audits both proposed repairs.  Bare directed Beckmann flow is exactly
P138, while reciprocity is P89.  Static global contact is the exact AVaR
dual of P138 and has no cross-row KKT equation.  Repetition-code contact
makes the P143 internal and external fields orthogonal under the reference
law but aligns their expectations under the conditioned law, so
orthogonality does not remove the cross.  Universal no-cross contains P138
at H=[n], although every affine code obeys

    sum_(i in H) r_i^2
      <= [h L R_nu(H)+d L^2]/[4 (log 2)^2].

Park bare flow, static contact, and orthogonality-based no-cross as smaller
routes.  A future re-entry needs common-indicator integrability,
second-order optimizer stability, or a nonlinear entropy-weighted directed
constraint.

P145 completes the first two re-entry checks.  Curl is the complete linear
common-origin law; Booleanity adds nonlinear convolution and same-orthant
gradient identities.  Global maximizers satisfy the all-normers normal-cone
and swap-square theorem, but opposite singleton maximizers have an exactly
flat chord.  Local curvature is therefore parked.  The exact surviving
induction contract is

    |I| <= C_h sqrt(h)(1+R),

followed by the open full defect gate

    2 I M + M^2 + sum_(j in Hc) r_j^2
      <= C_*^2 h(1+R)^2-I^2+C_0 dL^2.

Its d=1 case closes P138 with the same constant.  Repetition forces the
dL^2 order and the removed-row term.  The antipodal simplex-star family
forces dense, nonlinear, all-positive saturated contact while keeping the
P138 ratio bounded.  This full extension-defect inequality remains the
active induction framework below P138; do not replace it by a weaker
no-cross inequality which omits removed rows.

P146 isolates its sharpest normer-independent codimension-one child.  With
actual section energies E_r^+ and E_r^- and

    B_r=(sqrt(E_r^+)+sqrt(E_r^-))/(2a),
    Delta_r=E/a^2-B_r^2,

the active theorem is `min_r Delta_r <= C log(e/a)^2`.  This closes P138 by
induction.  Balanced majority refutes choosing r in advance but has bounded
debt on every majority coordinate.  The averaged exact identity begins with
E/(na^2), so scalar entropy or unsigned averaging is circular.  The missing
step is adaptive signed-defect coordinate selection.

The exact squared-row deletion law
has a positive defect that exceeds every local one-step scalar entropy reserve
by order n on antipodal pairs.  Full random-restriction telescoping does
not repair it: singleton and radius-one families force both negative savings
with coefficient one, at which point the state is exactly K_n^2/n.
The exact row-divergence quotient and
the scalar integration-by-parts inequality remain valid, but the absolute
resolvent--carre estimate is false: a complete quadratic plus scaled full
parity loses sqrt(n) after the cross-degree product is put inside absolute
values, while its actual P138 ratio is bounded.  Retaining signs repairs that
witness, but the cube chain rule then carries edge-dependent divided
differences; the weighted estimate is P138 itself.  The unweighted signed
field can be negative and has no diffusion chain rule.  Do not reopen
absolute mixed-scale products, scalar full-order deletion, or separate
high-row entropy packing.

### P89: quotient before norm

For a cube function `f`, put

    H_i(f) = D_i f - fhat({i}) Z_i.

Minimize over all symmetric compatible pair arrays

    U_ij = U_ji,       D_i D_j U_ij = U_ij,
    sum_(j != i) D_j U_ij = H_i(f),

and define

    C_n(f) = inf_U [sum_i (sum_(j != i) ||U_ij||_1)^2]^(1/2).

The canonical choice `U_ij=R_ij f` is always admissible.  P89 asks for

    C_n(f) <= C sqrt(n)/(s-1) ||f||_s,                1<s<=2.

Its set form and strong-`L^s` form are equivalent to the exact dual

    ||sum_i psi_i||_p
      <= C (p-1) sqrt(n) tau_2(c),
    c_ij = ||D_j psi_i + D_i psi_j||_infinity,

where `D_i psi_i=psi_i`, `hat psi_i({i})=0`, and

    tau_2(c) = inf { ||u||_2 : u_i>=0, c_ij <= u_i+u_j }.

The exact Fourier Euler identity

    sum_i psi_i
      = (L-I)^(-1)_(>=2) sum_(i<j)(D_j psi_i+D_i psi_j)

shows why the symmetrized derivative field, rather than the individual
derivatives, is the native datum.  Pair-array norm duality identifies its
dual norm exactly with the Euclidean fractional vertex-cover norm `tau_2`.

The proved arrows are

    P87 => P89 => P138 => P14.

The `s=2` endpoint and dual range `p>=n` are proved.  Singleton sets are
asymptotically sharp, and on disjoint parity checks the optimized compatible
flow gives `C_n(1_A)=sqrt(n) a`, avoiding the known divergent canonical
Green/transport ratio.  The live range is `2<p<n`.

For a fixed cyclic order, an exact selector identity splits `sum_i psi_i`
into an extreme-pair half and a co-interval half.  Two nested predictable
Rademacher inequalities prove the target bound for the extreme-pair half.
The compatible co-interval estimate is quantitatively equivalent to P89.
A parity selector reduces sufficiency to a matching field and its `p=2`
bound follows from averaging over every additive chord on each Walsh
support.  This is not yet a contraction: on every even Walsh level the
matching selector equals the full P89 scalar field.

Never drop the common-potential form
`A_ij=D_j psi_i+D_i psi_j`.  A unit-edge arithmetic-progression array in the
pair ranges violates the generic co-interval/matching estimate by
`sqrt(log n)` in `L2`; the amplification is entirely in a forbidden curl
component and disappears under the additive chord identities
`b_ij=a_i+a_j`.  Pointwise splitting according to a fractional vertex cover
also destroys these identities.  Every single-Walsh-support compatible
field is target-good, so a real falsifier must mix supports and use
cross-support `L-infinity` cancellation.

P90 now supplies large proved sectors.  The P89 target holds when the
output has binary basis degree at most two, partitions into `O(p)`
binary-independent families, or has `O(p^2)` active characters.  An
optimized three-color restriction proves every homogeneous degree with
universal constant `2e`.  Normalizing two color scales at their respective
levels proves any two arbitrary degrees with constant `4e`, independently
of parity and separation; antipodal projection closes at most two even and
two odd levels with constant `8e`.  Positive two-node quadrature closes
every three-term arithmetic progression of output levels with universal
constant `225`.  A matched-scale Neumann argument closes `m`
`64`-lacunary levels with constant `32 e m/15`, uniformly in their
locations.  Bounded mixed degree and phase-aligned spectra of mean degree
at least order `n/p` are also safe.  P91 closes arbitrary-degree
multi-core gradient--quadratic towers.  P93 proves much more: for every
fixed `m`, a confluent Muntz endpoint compactness theorem and
finite-dimensional polar synthesis close every spectrum supported on any
`m` arbitrary output levels, with a constant depending only on `m`.
Colliding rates are handled by Hermite divided differences and separated
log-scale clusters localize independently.  A surviving obstruction must
therefore have an unbounded number of interacting output levels.  It must
also remain nonlinear across every core/outside split and retain sign
frustration, overlapping circuits, cross-edge `L-infinity` cancellation,
and a heavy output.

The homogeneous coloring does not combine by scalar triangle estimates.
Any signed mixture reproducing levels through degree `D+2` has weighted
variation at least `2 H_(D+1)`.  Therefore seek cancellation across the
color/scale parameter; do not report degreewise recombination as a
dimension-free proof.  On `m` `64`-lacunary levels every exact scalar
mixture has total variation greater than `1.14m`, although their Calderon
Gram matrix is almost diagonal.  Scalar scale stopping is therefore
provably linear in the number of separated levels.  In particular the P93
constants produced by its scalar-synthesis proof cannot be uniform in `m`;
positive
lacunary coefficients force at least linear growth.  This is a method
wall, not a counterexample to P89.

The normalized color family has an exact Calderon isometry under
`dmu(q)=16 q log(1/q)/(1-q)^2 dq`; on degree parameters `r,s` its Gram
kernel is `4rs/(r+s)^2`.  This is the correct multilevel language, but do
not stack a one-sided edge-square estimate with a generic reconstruction
theorem.  Geometrically separated independent degree levels force a
`sqrt(p)` synthesis cost, while a single quadratic level forces the full
`p` edge cost and has synthesis constant one.  Their product `p^(3/2)` is
artificial.  The live P89 contract is the joint edge/test-function
bilinear embedding under the Calderon reproducing formula, with moment
budget allocated by scale.

Do not separate the dual test function through a pointwise Tent--Schatten
functional and then integrate linearly in the color scale.  At `p=2`, take
disjoint Walsh supports with degree parameters `r_m=4^(m-1)`.  The input
has `L2` norm `sqrt(m)`, whereas each Hessian block contributes a unit-mass
scale bump to the operator-norm leg; the lacunary bumps occupy disjoint
scale windows and accumulate as `m`.  Thus the proposed test-only
`S2/S1` interpolation estimate is false.  The compatible edge field and
the test function must remain jointly coupled across scales.

Standard Clifford or Haagerup linearization does not create this coupling.
For the Calderon embedding `J`, the Clifford field satisfies
`|gamma(Jf)|=|Jf|_(ell_2) I`, so noncommutative Holder reduces exactly to
the separated square-function product
`||JF||_(L^p(ell_2)) ||Jh||_(L^(p')(ell_2))`.  The lacunary reconstruction
witness then restores the same artificial `p^(3/2)` loss.  Treat this as
the existing separation wall in different notation, not as a new route.

Do not try to obtain that allocation from pointwise semigroup-variance
BMO along a fixed radial noise filtration.  For the compatible common-core
field `F=chi_C sum_(l in L) Z_l`, with `|C|=m` and `|L|=N`, the chord graph
is the unit `K_(m,N)` and `n tau_2^2=mN`, but at the all-one point its
noise-semigroup variance is at least `N^2/4`.  The BMO/native-scale ratio
is therefore at least `(1/2) sqrt(N/m)`.  This kills pointwise
radial/Carleson conditional-variance allocation only.  An `L^p` square
estimate, a spatial exposure of the core, or the joint test-function
bilinear integral remains viable.

Optimizing a coordinate reveal order does not repair this endpoint.  For
the complete quadratic P89 output
`F=sum_(i<j) Z_i Z_j`, every chord norm is one and
`sqrt(n) tau_2=n/2`.  For every order, reveal `r=floor(2n/3)` coordinates
and condition on their all-positive atom.  With `m=n-r` and `U` the unseen
sign sum,

    F-E_r F = r U + (U^2-m)/2,
    E_r |F-E_r F|^2 = r^2 m + binom(m,2).

Thus the best-order coordinate-martingale BMO norm is order `n^(3/2)`, an
extra `sqrt(n)` over the native budget, even though the homogeneous
quadratic class is P89-good.  Treat every essential-supremum filtration BMO
proposal as refuted unless it uses a genuinely different, moment-averaged
state rather than merely choosing or randomizing the coordinate order.

Do not replace the compatible quotient by rowwise Hilbertization: the cube
transportation space contains isometric `l1` stars, which lose `sqrt(n)`.
Do not infer P89 from scalar `L2/L-infinity` interpolation: a compatible
star forces the resulting `n^(1-1/p)` loss.  These are mechanism failures,
not counterexamples to P89.

Supportwise graph orthogonalization is also exhausted.  Degree-regular
selectors are exactly the P89 scalar in each realization; rooted stars lose
`sqrt(k)` through degree fluctuation; and the Hamilton path is
`Q_pi=2F-W_pi`, hence equivalent to the existing co-interval crux.  A
compatible common-core field shows that taking a local Korn trace after row
summation loses `sqrt(n)`, or `sqrt(n/k)` even relative to one derivative
square tensor.  A new route must use cancellation jointly across Walsh
supports before scalar trace, or be genuinely non-graphical.

P110 sharpens both the quotient and matrix boundaries.  For a binary quotient
map `Pi(x)=sum_i x_i gamma_i`, let `s` be the number of nonzero label classes
which occur exactly once.  Quotient conditioning and within-class
symmetrization prove

    ||F||_p <= C(1+K)(p-1) sqrt(n) tau_2(c),

whenever `s<=Kp`; if `s=0`, then
`||F||_p<=sqrt(n) tau_2(c)` for every `p`.  A scalable quotient-code falsifier
must therefore have `s/p` tending to infinity.  Repeated-column amplification
is not a survivor.

Do not turn this into a homogeneous atomization.  For the even-dimensional
bent quadratic phase `g=(-1)^(sum_(i<j)x_i x_j)` and
`F=L P_(>=2)g`, the full quotient norm is at most `sqrt(n)/2`, while

    [sum_(k>=2) rho_n(P_k F)^2]^(1/2) / rho_n(F)
      >= c 2^(n/2) n^(-1/4).

Thus even square-summing independently optimized homogeneous quotient norms
destroys mixed-degree cancellation exponentially.  Mixed-degree atoms remain
logically possible.

The exact compatible matrix reconstruction

    K(A)_(i,l) = sum_(j!=l) D_i D_j (L-I)^(-1)_(>=2) A_(j,l)

satisfies `Tr K(A)=2F`.  On complete quadratic chaos,

    ||Tr K||_p >= c p n,
    ||K||_(L^p(S_2)) <= C n sqrt(p)

for a universal range `p_0<=p<=cn`.  Therefore a separate trace after an
universal separate trace comparison must lose at least `sqrt(p)`.  Appending
it after an already order-`p` black-box matrix estimate cannot recover an
order-`p` budget; its factor accounting has a `p^(3/2)`-scale lower
requirement.  A viable structure-sensitive matrix proof must couple transform
and trace or improve the first-stage moment cost.

P111 gives the exact multistage quotient upgrade.  At quotient stage t,
write a_t for repeated-row cover mass, v_t for total singleton cover mass,
b_t for the dimension of the repeated-label span, s_t for the number of
singleton labels, and rho_t for the minimum cover mass of a repeated-label
basis.  The discarded pieces are reverse martingale differences and satisfy

    ||F_0||_p <= ||F_T||_p
      + C sqrt(p) [sum_t(a_t^2+b_t v_t^2+s_t^2 rho_t^2)]^(1/2).

Thus the terminal high-moment endpoint closes P89 whenever its active count
is O(p) and the displayed square charge is O(p n tau_2(c)^2).  The charges
square-sum because the one-stage moment-generating bounds are conditional
with deterministic proxies; never replace this by a triangle sum over flag
depth.

This subgaussian gate is sufficient, not necessary.  On the depth-one family with
singleton labels g+a over H=F_2^b and doubled basis labels, the output is

    F = 2^b 1_{0} - 1.

Its actual normalized P89 ratio is O(1/p), but every fractional cover gives
a P111 bounded-difference charge whose normalized excess is at least
sqrt(b/(16p)).  The discarded increment lives on a rare point, which a
worst-case derivative proxy does not see.  P112 gives the correct general
upgrade: if every reverse increment has conditional Bernstein parameters
sigma_t^2 and L_t, then

    ||F_0||_p <= ||F_T||_p
      + C(sqrt(p sum_t sigma_t^2) + p max_t L_t).

The canonical choices are the essential supremum of the conditional variance
and one third of the increment peak.  They handle the preceding rare-event
family, but they are not universally controlled by the original cover.  For
the P113 repeated-core/leaf potential,

    n tau_2(c)^2 = 2mN,
    E(Delta_0^2 | F_1) = (sum_(a=1)^N Z_a)^2,

so every deterministic variance parameter is at least N^2 and loses
N/(2pm).  The output itself satisfies the P89 target with room.  Do not take
conditional-variance suprema before the outer moment.  Keeping the bracket in
L^(p/2) is useful only if compatible structure also controls the maximal
increment; generic Burkholder--Rosenthal fails here, and symmetric one-bit
refinement returns to SF-P89/P82.

A separate P112 theorem closes every canonical Boolean corrected gradient:
for f in {-1,1},

    psi_i = D_i f - fhat({i}) chi_i

obeys

    ||sum_i psi_i||_p <= (2+sqrt(2)) sqrt(n) tau_2(c).

At each vertex the sensitive coordinates form a clique of unit chord
constraints.  This includes all Boolean quotient phases, degrees, label
multiplicities, and the former quadratic-bent class.  A Boolean-derived
survivor must use a noncanonical compatible gauge with a substantially
smaller chord cover.

P114 audits that caveat under the full zero-output gauge.  If
F=L P_(>=2) f, f is Boolean, and k_x is the local sensitivity, then every
compatible representative satisfies

    tau_2(c) >= (2 k_x - n)_+ / (2 sqrt(n)).

The proof uses the exact gauge normal form
A_ij=2D_iD_j f+D_j r_i+D_i r_j, the pointwise identity
sum_(i<j)(D_j r_i+D_i r_j)=0, and the Boolean face-sign trichotomy.  Thus
the desired pointwise scale holds whenever k_x>=3n/4.  The remaining
balanced Boolean--Korn region is strict but Boolean-only.

Do not infer that the canonical Boolean cover is the native quotient.
Already at n=3 there is an exact Boolean output with
tau_can=sqrt(2) and rho=2/sqrt(3).  Its common-core extension has
tau_can/rho=sqrt((m+1)/m), so this natural gap tends to one.  The exact
fixed-output dual keeps the full P89/P102 feasible ball and changes only the
exposed Boolean objective.  Re-dualizing it or maximizing tau_can/rho is not
a new concentration route.

P115 completes the bounded follow-up.  If S=max_x k_x, then every compatible
representative satisfies

    rho_n(L P_(>=2) f) >= S(S-1)/(2(n-1)sqrt(n)).

The proof pairs the pointwise Boolean two-face graph at a maximum-sensitivity
vertex with P114's exact zero-gauge cancellation.  A second, global
gauge-annihilating pairing with C_ij=2D_iD_j f gives

    rho_n(L P_(>=2) f) >= sqrt(E[k(k-1)]/(n-1)).

Full coordinate symmetrization forces the canonical allocation for every
  real permutation-invariant function (with a sharper Boolean consequence),
  and on disjoint scalar outputs the
native quotient obeys the exact Euclidean tensor law

    rho(F_I+F_J)^2 = rho(F_I)^2+rho(F_J)^2.

These are genuine quotient theorems, not canonical-cover estimates.  They
close all Boolean families with S>=delta n, all signed unions of Hamming
layers, and additive repetition of a fixed disjoint output.  They do not
localize the offending value: a remaining counterexample sequence must have
S/n tending to zero and |F(x)|/sqrt(E[k(k-1)]) tending to infinity.  Park
this Boolean-only branch unless a new localized gauge-annihilating
certificate is supplied.

P116--P120 give the fixed-orbit follow-up.  The orbit-absolute envelope

    C_n(h) <= O_n(h) <= D_n(h)

has the exact representation

    O_n(h) = sup_(||sigma||_infinity<=1) C_n(M_sigma h),

where the degree-k symbols are correlated Gamma moments and adjacent
high-degree symbols differ by `O(1/k)`.  It contracts the full P105
affine-spread proxy by `sqrt(M)`, but `sigma=1` gives `M_sigma=P_(>=2)`.
Therefore it is not a smaller P89 obligation.  More decisively, complete
quadratic chaos and a normalized point mass prove that every unweighted
separated conjugate mixed-norm factorization of the two fixed-orbit legs
loses `sqrt(n)`, for every time exponent.  Any viable scale allocation must
pair the two orbits before taking norms.

Positive joint reweighting is still too coarse.  For the complete quadratic
paired with a normalized point mass at `p=n/4`, the optimal positive density
on the full `(q,z)` orbit space satisfies

    inf_W ||W^(1/2)U||_2 ||W^(-1/2)V||_2 = integral |UV|

and the right side is at least `c n^(5/2)`, versus native budget `2n^2`.
Positive stopped local Hölder sums inherit the same bound.  Unrestricted
signed partitions reduce to the one-cell exact pairing and hence merely
restate P89.  Therefore a viable stopping/corona state must be constrained,
phase-sensitive, and cancellation-preserving.  Modulus-only conclusions
apply only on sign-closed input classes; do not overstate this wall against
structure-sensitive Calderón-orbit forms.

The exact signless-incidence coordinate

    F = R^* I A

has squared support norm `k/(2(k-1))` and contracts the transverse gauge
mode by at most `1/4`.  This is a useful Hilbert identity, not an all-moment
gain.  Common-core stars refute pointwise domination, matchings refute
operator-norm-only input, and complete quadratics plus a degree-three
tournament force both `sqrt(p)` moment stages.  Keep the joint incidence
estimate as a bounded assay only; generic two-stage Riesz estimates reopen a
closed wall.

Unsigned supportwise spectral data are also insufficient.  An aligned flat
Walsh spectrum and a nondegenerate quadratic bent spectrum have identical
canonical labelled support incidence, coefficient magnitudes, and radial
Hodge data, but their exact native quotient and pointwise edge-Hilbert ratios
are `2^(n/2-1)`.  Retire only phase-blind/supportwise association-scheme,
Grothendieck, and independent-randomization implementations.  Some
cross-support phase information is necessary, but the full signed Gram field
is only one complete repair, not a uniquely forced one; quotient-aware and
globally signed encodings remain open.

The same round sharpens the matrix audit.  Right Helmholtz projection gives

    H(F) = P_R K(A) = 2(D_iD_j L^(-1)F)_(ij),
    Tr H(F)=2F,
    ||H(F)||_(L2(S2))=2||F||_2.

This removes all trace-null representative gauge before taking norms.
Nevertheless the natural H(F)--H(h) pairing is exactly P89, while a
common-core family makes both pointwise and coordinate carré-du-champ
comparisons lose sqrt(N/k).  Hutchinson scalarization reproduces the scalar
G plus an off-diagonal chaos; unbiased sampling of n/p diagonals loses
sqrt(p) on the complete quadratic; and disjoint Walsh characters refute the
pointwise Schatten-to-scalar dual step.  Use the quotient compression in
future matrix work, but do not claim local differential subordination,
standard scalarization, or a new contraction.

### P87/P22/P24/P78: mixed and signed Green route

The canonical signed Green flow obeys

    T_n(f) <= G_n(f).

Thus

    G_n(1_A) <= C n a log(e/a)                         (P22)

would imply P14.  P22 is equivalent up to universal constants to the global
shifted-Hessian estimate

    sum_(i != j) ||R_ij f||_1 <= C n/(s-1) ||f||_s,   1<s<=2,

and to its bounded two-index dual P24, with the shifted resolvent retained.
These statements are stronger than P14, not equivalent to it.

The universal antipodal extremality statement P78 is open, but the implication

    P78 => P22 <=> P24 => P14

is proved.  P78 is proved for every affine set and every set of at most three
vertices.  A sequence with divergent normalized P22 ratio would have to be
nonlinear, asymmetric, have density tending to zero, and have
`|A|=2^(n-o(n))`.  One-level atom pairing is `sqrt(n)` short in exactly that
window, so a viable kernel proof needs multilevel cancellation stable under
cluster merging.

P64 shows that `G_n/T_n` can diverge on disjoint parity checks while the P22
endpoint itself remains valid.  This kills constant-factor Green/transport
faithfulness, not P22.  P89 repairs this particular gap by optimizing over
compatible flows before taking row norms.  The direct P78 extremality attack
is operationally parked.  P87 remains a valid stronger child of P89, but
P102 shows that its canonical rooted phase is not quotient-invariant; treat
this route as stalled unless a new quotient-preserving gain is found.

P87 asks for the exterior mixed endpoint

    E_n(f) := (sum_(i != j) ||R_ij f||_1^2)^(1/2)
              <= C/(s-1) ||f||_s,                    1<s<=2.

Its set form, this `L^s -> ell_2(L^1)` form, and the exact dual

    ||sum_(i != j) R_ij a_ij||_p
      <= C(p-1) (sum_(i != j) ||a_ij||_infinity^2)^(1/2)

are equivalent up to universal constants.  Cauchy--Schwarz across the
ordered pairs supplies the single ambient factor `n`, so

    P87 => P89 => P138 => P14,
    P87 => P22 <=> P24 => P14.

At `s=2` the exact square sum is at most `2 ||f||_2^2`.  In the
bounded-field dual, the current concrete crux is a resolvent-compensated
trace from a fully decoupled marked field to the coupled two-front field.  It
is bounded in `L2` and `L-infinity`; ordinary interpolation on the marked
subspace is not dimension-free, as a complemented first-chaos retract
proves.  The witness is mapped isometrically, so this kills only
interpolation.

A random-linear-order wrap identity now proves the all-degree estimate one
number-operator inverse below P87:

    ||L^(-1) S_b||_p <= C p beta_2(b),
    beta_2(b) = (sum_(i != j) ||b_ij||_infinity^2)^(1/2).

It follows that outside degree at most `D` costs `C p (D+2)^2 beta_2`,
while one homogeneous outside level of degree `d` costs
`C p (d+2) beta_2`.  Any counterexample therefore needs unbounded
outside-degree complexity.  The exact remaining operation is recovery of
one number-operator derivative using cancellation among the complete pair
field.  Do not estimate the exact cyclic selector one order at a time: an
aligned full-parity witness loses `sqrt(n)` in `L2`, even though its order
average has constant scale.  Scalar coloring mixtures also cannot close the
gap; their total variation grows at least quadratically in the degree and
no finite-total-variation selector reproduces all degrees.

The cyclic order average has a stronger square gate

    H_b = (E_sigma |T_b^sigma|^2)^(1/2),
    ||H_b||_p <= C p beta_2(b).

This gate is sufficient for P87 and is proved when the output supports
partition into at most `p` binary-independent families, for affine
quadratic support clouds, at every fixed outside degree, and at arbitrary
degree whenever one coordinate order places every dependency of `b_ij`
before both endpoints.  Two nested predictable Rademacher martingales prove
the full cyclic-square estimate on this forward-dependency class.  Pointwise
order variance is not controlled: a one-core tournament loses order `n`,
although its averaged square gate is target-good.  Levelwise homogeneous
aggregation is also false: odd majority on one edge has actual `H_b<=1`
but a degree-one row projection of `L-infinity` size `Theta(sqrt(m))`.

Generate the order by iid circle angles.  Conditional on two endpoints, the
mean arc selector on row `b_ij` is exactly `T_q b_ij`, with `q` the
complementary arc length.  Pairwise independence of distinct circle
differences proves the pointwise identity

    |S_b|^2 <= E_angle |M_b|^2 <= |S_b|^2+2 beta_2(b)^2.

Thus the positive-noise square is equivalent to P87, not a separate
Carleson debt.  The sole new cyclic-square obligation is the conditionally
centered shared-angle fluctuation `X_b` in
`L^p(Z;L^2(angle))`, only for `2<p<n`.  Its rows are not mutually
independent, and pointwise Efron--Stein is unavailable.

Each fluctuation row nevertheless has an exact Bernoulli-restriction
martingale telescope with total conditional energy at most
`||b_ij||_infinity^2`.  P97 strictly sharpens this averaged, ordered fact.
Along the symmetric radial path from the noise point `(q,...,q)` to the
realized restriction, it gives

    X_ij = sum_k (eta_ij,k-q_ij) Gamma_ij,k,
    q_ij(1-q_ij) sum_k |Gamma_ij,k|^2
      <= 2 ||b_ij||_infinity^2

pointwise, with `Gamma_ij,k` independent of its current marked angle.  The
formula retains every Hoeffding order and uses no revealing order.  Its
innovation is the common-circle coboundary
`eta_ij,k-q_ij=rho_k(j)-rho_k(i)`.  Fourier expansion in one marked angle
has weights `1/(4 pi^2 m^2)` of total mass `1/12` and turns the field into
an endpoint graph divergence.  The precise open operation is assembly of
the jointly radial-path-generated coefficients over the shared marked
angles with the `Z` moment outside the angle square.
Generic centered-row/predictable assembly is false by `sqrt(n)`, and
pointwise incidence assembly fails on the tournament; neither wall refutes
the generated common-circle field, for which common cycle weights
telescope and the tournament has the stronger `C sqrt(p) beta_2` bound.
Even the exact normalized circle innovations plus pointwise row `ell_2`
energy are insufficient for arbitrary coefficients: nested intervals
sharing one mark have positive covariance and aligned Walsh fronts of size
`N` against budget `sqrt(N)`.  The radial-path range relation across all
marked directions of each Walsh monomial is therefore load-bearing; never
replace P97 by a generic row-energy lemma.

P98 proves that this generated range has a strict quantitative gain.  On
each full Walsh support S, the genuine angle operator satisfies

    ||A_S c||_(L2(angle)) <= 3 / sqrt(|S|-1) ||c||_2,

and Walsh orthogonality yields the sharp-scale global endpoint

    ||L_Z^(1/2) X_b||_(L2(Z,angle))
      <= (1+3/sqrt(2)) beta_2(b).

The |S|^(-1/2) scale is already sharp on one edge.  In one row, the exact
cross-support Gram law is

    <Phi_(ij,A), Phi_(ij,B)>
      = |A intersect B|
        / [ (|A union B|+1) (|A|+|B|+1) ],

so disjoint outside supports are orthogonal.  The tower also obeys the
deletion identity

    E_(Theta_k) Phi_(ij,A)
      = q_ij Phi_(ij,A minus {k}).

The same-row normalized tower factors exactly as a
double-random-restriction square, equivalently

    2 int_(0<v<u<1) T_u [
      sum_k |D_k (I+L)^(1/2) T_v g|^2
    ] dv du.

This is useful only before row aggregation.  The normalized common-core
star g_(0,l)=N^(-1/2) Z_1 has global angle square (N+1)/6 at the all-one
cube point, while the sum of its individual-row angle squares is 1/3.
Its actual mixed Lp norm is at most sqrt((p-1)/3).  Thus pointwise
aggregation of the exact rowwise conical squares is another lossy proxy;
the global proof must retain cross-edge angle covariance coupled to the
front signs.

Normalize with

    g_ij = (I+L_(-ij))^(-1/2) b_ij.

Use the shifted resolvent, not the unshifted half inverse: it is the positive
probability mixture

    pi^(-1/2) int_0^infinity t^(-1/2) e^(-t)
      e^(-t L_(-ij)) dt,

so |g_ij|<=||b_ij||_infinity pointwise.  Exactly X_b=N g, where the
coherent cycle--Riesz multiplier N multiplies outside degree d by
sqrt(d+1) Phi_(ij,A).  Thus the current sufficient contract is

    ||N g||_(L^p_Z(L2_angle))
      <= C p ||(sum_(i!=j) |g_ij|^2)^(1/2)||_p.

This is one joint multiplier inequality, not two iterated first-order
Riesz estimates.  P98 supplies its dimension-free L2 support symbols,
but generic block-multiplier promotion is false: artificial sign symbols
on a bent phase have exponentially growing L^p norm.  Standard
coordinate-martingale and noise-semigroup BMO endpoints are also false by
sqrt(n) on the target-good one-core tournament.  These failures are
lossy-proxy walls, not counterexamples to N.  A proof must keep the actual
radial deletion/insertion coherence and average rare configurations rather
than take an essential supremum over stopping states.

P99 records one symmetric sufficient insertion architecture.  Write each multiplier term as

    a_alpha chi_(S_alpha) psi_alpha,   psi_alpha in L2(angle).

For a reveal set `R` and a fresh coordinate `k`, let `V_(R,k)` sum precisely
the terms with `k in S_alpha` and `S_alpha minus {k} subset R`, after removing
the final sign `Z_k`.  For a uniform permutation `pi`,

    V_pi^2 = sum_m ||V_(R_(m-1),pi_m)||_(L2(angle))^2

is the pathwise square of a conditionally symmetric Hilbert-valued
martingale.  The sharp martingale square theorem spends only `sqrt(p)`, so
the averaged candidate contract

    (E_pi E_Z (V_pi^2)^(p/2))^(1/p)
      <= C sqrt(p) ||(sum_(i!=j) |g_ij|^2)^(1/2)||_p.

Do not replace this by the quadratic order average.  Pointwise in `Z`, that
average has the exact identity

    E_pi V_pi^2
      = 2 int_0^infinity e^(-tL)
          [sum_k ||D_k e^(-tL) N g||_(L2(angle))^2] dt,

but Jensen runs in the wrong direction for the required `p/2` moment.
Pointwise reveal-state contraction is also false on the common-mark star.
The factorization itself is generic for every Hilbert-valued Walsh
polynomial, and the martingale argument needs only an infimum over reveal
orders whereas P99 averages them all.  Thus this is a candidate proof gate,
not a strict reduction.  A successful use would have to estimate the rare
coherent fronts in mixed `L^(p/2)` using the signed cross-edge circle Gram
matrix.  P98 already closes `p=2`; the live range is `2<p<n`.

P100 sharpens the endpoint-conditioning state below P99.  For one fixed
root and orientation, define

    B_(j,A)^(r)
      = integral_0^1 t^r [1_(M_(j,A)<t)-t^|A|] dt.

Then outside-angle deletion is exactly

    E_(Theta_y) B_(j,A)^(r) = B_(j,A minus {y})^(r+1),

and the same-root Gram law is

    <B_(j,A)^(r),B_(j,C)^(s)>
      = |A intersect C|
        / [ (|A|+r+1)(|C|+s+1)
            (|A union C|+r+s+2) ].

The normalized reverse-martingale increment energies telescope without a
harmonic loss.  Endpoint averaging maps the generalized arc-power state
q_e^r(I_(e,A)-q_e^|A|) into this rooted tower and gains the expected half
derivative.  On one full support, the two incident orientations have an
exact Dirichlet-gap projection.  In one row, the first boundary is also an
exact shifted inverse-gradient conical square.  Direct Minkowski and Riesz
give a coarse O(p) bound; P101 below gives the sharp O(sqrt(p)) bound.

This does not close P99.  The desired insertion-energy subcontract is
O(sqrt(p)), but rowwise assembly is the already-refuted common-core-star
proxy.  The entire
fresh-angle residual can be written as one signed interval covariance form

    Delta_x = integral h_I(Theta_x) d mu_x(I),
    E_(Theta_x)|Delta_x|^2
      = double_integral (|I intersect J|-|I||J|)
          d mu_x(I) conjugate(d mu_x(J)),

which retains endpoint/outside cross terms.  A Bellman state containing
only the original radial atom and the first centered maximum is exactly
nonclosed: at outside degree two its first descendant leaves residual
energy 1/720, one sixteenth of its norm.  Deleting a root creates the new
gap potential s^2-s+1/6.  Thus the live state must retain the full power
tower, signed interval covariance, and root-collision descendants.  No
L^(p/2)_Z inequality for that state is known.

P101 sharpens the quantitative boundary conclusion.  If B_a denotes any
family of rooted boundary operators and g_a their row inputs, then

    || (sum_a ||B_a g_a||_(L2(angle))^2)^(1/2) ||_p
      <= C sqrt(p) (sum_a ||g_a||_infinity^2)^(1/2).

After h_a=(I+L_a)^(-1/2)g_a, the sum of the exact P100 conical squares is
pointwise dominated by the average coordinate-Doob square of the bounded
Hilbert-valued terminal vector h=(h_a).  Conditional future square energy is
at most its terminal bound squared, so a stopping-time argument gives an
exponential tail and the sharp sqrt(p) moment.  Thus the earlier O(p)
one-row estimate is lossy; same-root and external-direct-sum moment growth
are closed at the scale P99 needs.

Do not infer the actual incident-boundary estimate from this direct sum.
For a fresh endpoint x, the true field is

    sum_(j!=x) Z_j (B_j^+ g_(xj) + B_j^- g_(jx)).

Each coefficient is independent of its own front sign but can depend on all
the others, so this is a nonpredictable divergence.  A second Khintchine or
martingale estimate spends another sqrt(p).  The lost phase is already full
size on two coordinates:

    B_(j,{k})^(0),+ = -B_(k,{j})^(0),+,
    ||B_(j,{k})^(0),+||_2^2=1/12.

The signed interval covariance has the exact phase-sensitive form

    double_integral kappa(I,J) dmu(I) conjugate(dmu(J))
      = ||rho_mu||_(Hdot^(-1)(circle))^2,

where rho_mu is the distributional derivative of
`integral h_I dmu(I)`.  Outside intervals give atomic graph-divergence
charges, an endpoint residual gives `delta_M-d u^(d-1)du`, and the first
root-collision descendant `s^2-s+1/6` is twice the circle Green kernel.

P99 itself holds for every fixed reveal order on the generated one-core
tournament.  Its insertion square is a positive-semidefinite degree-two
Rademacher form; the PSD fourth-moment identity and Bonami give

    ||V_pi||_p <= sqrt(p) B

uniformly in the order and dimension.  Together with the exact common-mark
star formula, this clears the two strongest rare-front/BMO adversaries but
does not control general interacting root-collision states.

The all-degree forward theorem is now extended by the dependency-digraph
audit.  If deleting `f` coordinates makes the graph acyclic, conditioning
on them gives

    ||T_b||_(L^p_Z(L^2_Theta)) <= C (p+f) beta_2.

If every strongly connected component has size at most `s`, block
martingale concentration gives

    ||T_b||_(L^p_Z(L^2_Theta))
      <= C (p sqrt(s) + s sqrt(p)) beta_2.

Thus every fixed feedback number and every fixed SCC size is closed at
arbitrary outside degree.  P94 improves this structural boundary.  If the
dependency digraph partitions into `r` induced acyclic subdigraphs, two
nested predictable Rademacher estimates on each color pair give

    ||T_b||_(L^p_Z(L^2_Theta))
      <= K_H^2 p sqrt(r(r+1)) beta_2.

The centered field costs at most twice this.  This bounded-dichromatic
closure applies even when SCC size and feedback number both diverge, as in
the complete bidirected bipartite example.  Consequently only arrays of
unbounded dichromatic number remain in the universal cyclic subroute.
Endpoint signs do not remove this loss.  On the native array
`b_ij=chi_([r] minus {i,j})` for `i<j`, the dependency graph is complete
bidirected and de-randomizing independent endpoint signs loses exactly
`sqrt(binomial(r,2))`, even though the uncolored field is target-good.
Vector endpoint colors have the same square-gain/reconstruction tradeoff.
Any improvement must preserve the common-circle coboundary before color
recombination.  P95 closes the native P87 field on a genuine
complete-bidirected outside-majority family with every odd output level
active.  The rows are the pair Hessian of the radial potential
`H(Sigma)=(Sigma |Sigma|-sgn(Sigma))/2`, and the shifted-Hessian trace is
exactly `(1/2) L P_{>=2}H`; hence `||S_b||_p <= 4p beta_2`.  This proves
that neither unbounded dichromatic number nor unbounded level count alone
is an obstruction, but it does not prove the centered common-circle gate.
The latter remains supported only by finite angle diagnostics on this
family.

Do not extend P95 by first taking the trace-preserving pair-Hessian
projection.  P96 identifies the unique supportwise orthogonal projection,
but on a legal degree-four core/leaf array both its Hessian piece and its
trace-null complement enlarge the native row-`L-infinity` square budget by
order `n`.  The input dependency graph is acyclic and its shifted trace is
already target-good.  The exact Hodge identity is useful structure, but the
projection is a closed universal mechanism.

Do not linearize the common-circle covariance to its first Hodge layer.  A
degree-`d` monomial row on an arc of length `q` has variance
`q^d(1-q^d)`, whereas the singleton-mark layer has energy
`d q^(2d-1)(1-q)`.  Their ratio diverges as `q` tends to zero.  Thus all
shared-mark Hoeffding orders must remain visible; this wall does not refute
the generated telescope, integration before domination, or joint bilinear
cancellation.
Averaging forward
projections over random orders has exact
outside-degree multiplier `2/((d+1)(d+2))`, so scalar inversion merely
recreates a two-derivative loss.

There is an exact two-half-resolvent factorization into derivative-range
first-order divergences.  Applying a first-order Riesz theorem twice spends
two first-order constants.  Deleting the derivative-range condition to
avoid one stage is invalid: Ivanisvili--Volberg's duality argument reduces
that generic divergence estimate to Lamberton's false below-two vector-Riesz
bound.  Therefore attack the compensated two-front composition directly;
do not cite a black-box first-order iteration as P87.

### P11/P82: invariant random-order square function

For a uniform reveal order `pi`, the aggregate residual has exact Doob
coefficient field `A^pi+B^pi`.  The leading field is already controlled:

    ||A^pi||_(L^p(l2)) <= C n beta sqrt(p).

The correction gate

    ||B^pi||_(L^p(l2)) <= C n beta sqrt(p)

is equivalent, modulo that proved term, to the invariant square-function
bound

    ||S_pi(R)||_p <= C n beta sqrt(p).

Either bound would imply the Rademacher rate, but the native scalar moment
bound is not known to imply this sharper square-function estimate.  The route
is therefore sufficient and parked, not an exact alternative to P14.

The exact coherent/transverse formula is only an `L2` identity.  Separately
projecting the two sectors need not preserve the native `L-infinity`
derivative budget.  Sparse source support, winner occupancy, dependency
coloring, fractional conflict, and affine-control theorems are subclass
closures beneath P11, not independent universal routes.

P81 proves that universal target-scale fractional conflict is false: its
complexity is `Theta(n^(3/2))` on a symmetric quadratic family whose actual
correction remains at the target scale.  A separate four-dimensional example
shows that random stopping-line conditional expectation is not an
`L^p(l2)` contraction.  Neither example refutes P11.

P122 adds the exact last-deletion and signed collision laws, an exact
\(3/2\) first-child obstruction, and the signed linear-extension diagram
expansion.  P108 refutes pointwise and natural averaged carré compression,
including after averaging the reveal order.  These are method walls, not a
P11 counterexample: finite and scalable searches found no growing normalized
P11 ratio, and the complete quadratic remains the strongest recorded
calibration with exact \(Q_2\to1/2\).  Do not promote this numerical evidence
to a theorem.

## Established theorem-level outputs

The current paper proves the following reusable results.

- P1--P2: for every centered Walsh polynomial,

      ||R||_p <= C (sigma sqrt(p) + p iota),

  with no degree dependence.  This is a coefficient-budget theorem.
- P3: every native Rademacher residual has variance at most
  `n(n-1) beta^2/2`.
- P4: the stronger coefficientwise slice hypothesis gives the native target
  rate.
- P33: at `p=3`, the native BKZ logarithm improves to
  `[log(en)(1+log log(en))]^(1/3)` in the stated regime.
- P34: if every summand is additionally bounded by `L`, exchangeable-pair
  concentration gives

      ||sum_i g_i||_p <= C sqrt(p)(n sqrt(beta L)+L sqrt(n)).

- P35: the native Rademacher rate holds at every fixed aggregate Walsh degree,
  with a degree-dependent constant.
- P70: sparse Cartesian products of uniformly P14-good factors remain
  P14-good; products do not amplify a hidden P14 defect.
- P16/P29: permutation-invariant functions satisfy P14, and their signed Green
  flow is KR-optimal.
- P26: asymmetric product-Riesz families satisfy P24.
- P28: pairwise-independent random set membership satisfies the Green endpoint
  in expectation only.
- P77: every binary affine subspace or coset satisfies P22 and sharp P78.
- P84: exact two-atom Green cancellation, P78 for every three-point set, and
  the divergent-P22-ratio window.
- P217: the capacity-obstacle odometer is a canonical admissible
  collision relocation and satisfies the exact transfer

      T_s(d-1_I)
        <= (2/s) sum_(r!=t) E|partial_r partial_t u|.

  Total occupation is not a valid replacement, and obstacle relocation
  need not be FCR-optimal.
- P218: every sparse radial shell profile satisfies the weighted cumulative
  flux bound `sum |D-2-2k||Q_k|<=2(D+1)a` and hence the radial obstacle
  Hessian bound `10Da`.  This is a sharper one-dimensional structural
  theorem, not the universal proof mechanism.
- P219: complementarity gives `mu{u>0}<=2a`; support-localized
  Cauchy--Schwarz and the exact Walsh Hessian square sum give
  `sum_(r!=t) E|partial_r partial_t u|<=2s^2a`.  Thus
  `T_s(d-1_I)<=4sa`, the ambient lift closes P210, and density doubling
  proves P14 and the Rademacher/general-product linear rate.
- Sharp all-moment saturation: with `q=min(p,n)`, every BKZ family obeys
  `||sum_i g_i||_p<=C[n beta q+M sqrt(nq)]`, and the single quadratic
  Rademacher family matches this scale for every `p>=2`.  For `p>=n`,
  use the all-positive atom for the lower bound and the implied generic
  pointwise cap for the upper bound.
- P86: sparse fixed-cardinality fibers over a P14-good base remain P14-good;
  arbitrary nonlinear graph extensions do not amplify a defect.
- P87: the mixed shifted-Hessian set, strong-`L^s`, and bounded-field dual
  formulations are equivalent; its exact `L2` square sum is at most
  `2 ||f||_2^2`; the degree-free once-smoothed trace is proved, and its
  cyclic square gate has binary-matroid, affine-quadratic, fixed-degree, and
  arbitrary-degree forward, bounded-feedback, and bounded-SCC dependency
  closures plus the P94 bounded-dichromatic closure and an exact
  random-arc/noise decomposition.
- P94: the P87 cyclic square gate holds when the coordinate-dependency
  digraph has dichromatic number `r`, with bound
  `K_H^2 p sqrt(r(r+1)) beta_2`; bounded dichromatic number strictly crosses
  the earlier bounded-feedback and bounded-SCC boundary.
- P95: the native P87 field holds with constant `4` on the complete
  odd-majority clique, whose dependency digraph is complete bidirected and
  whose output contains every odd degree from `3` through `n`; this is a
  radial-Hessian class theorem, not the universal centered square gate.
- P96: the unique trace-preserving pair-Hessian projection is exact in
  `L2(ell_2)` but unbounded in the native row-supremum budget; both projected
  pieces lose order `n` on a legal target-good forward array.
- P97: the centered common-circle row has an exact symmetric all-order
  radial-path representation with pointwise normalized coefficient energy
  at most `2 ||b_ij||_infinity^2`; only assembly for the jointly generated
  coefficient range remains, and arbitrary coefficients with that row
  energy fail already in `L2`.
- P98: the genuine generated support operator has norm of order
  |S|^(-1/2), sharply; globally the half number-operator derivative is at
  most (1+3/sqrt(2)) beta_2.  Its exact same-row Gram kernel and deletion
  hierarchy reduce the remaining centered gate to one normalized coherent
  cycle--Riesz all-moment multiplier.  Generic bounded block symbols and
  standard BMO endpoints cannot promote this L2 result.
- P99: random coordinate insertion realizes that coherent multiplier as a
  conditionally symmetric Hilbert-valued martingale.  The averaged
  insertion-square condition is sufficient and has an exact semigroup
  first-moment identity, but the construction is generic and stronger than
  the minimal infimum over orders.  It is a candidate architecture, not a
  strict successor; Jensen and pointwise reveal-state bounds do not close
  the higher moment.
- P100: endpoint conditioning enters an exact rooted maximum-power tower,
  with same-root Gram/deletion identities, an orthogonal energy telescope,
  an exact incident-edge Dirichlet projection, and a one-row shifted
  conical-square factorization.  This is proved state compression, not an
  all-moment estimate.  The first-maximum-only state and scalar-energy
  Bellman functions are too small, while cross-root signed interval
  covariance remains open.
- P101: the P100 boundary has the sharp O(sqrt(p)) moment bound in one row
  and in arbitrary external Hilbert direct sums, by random-priority
  domination with a bounded-terminal Doob square.  The covariance is exact
  circle Hdot^(-1) Green energy, and P99 holds for every order on the
  one-core tournament.  The actual incident sum remains a nonpredictable
  cross-root divergence and is not controlled by the direct-sum theorem.
- P102: every compatible flow is the canonical shifted-Hessian flow plus a
  symmetric pair-range zero-divergence gauge, and compatible chord fields
  annihilate that gauge.  Equal disjoint parity blocks make the
  canonical/optimal congestion ratio grow like the number of blocks.  Thus
  canonical rooted phase is not a native P89 obstruction.
- P103/P105: delaying compatible-flow minimization until after Calderón
  scale gives the exact pairing

      |E Fh| <= tau_2(c) D_n(h),
      D_n(h) = int C_n((L-I)K_q h) dnu(q).

  Here K_q annihilates degrees at most one and the sufficient gate must be
  stated for every ambient test h:

      D_n(h) <= C p sqrt(n) ||h||_(p').

  Restricting to high-degree tests with their inherited norm leaves a
  quotient-duality gap.  P105 proves the displayed gate false for every
  fixed p.  Affine-spread Steiner designs of degrees k_m=4^m on one common
  n-coordinate set give, for h=sum_m h_m,

      ||h||_2 = sqrt(M),
      C_n(h) <= sqrt(4M(n-1)/3),
      D_n(h) >= c_0 M sqrt(n-1).

  Each component is a sharp homogeneous P89 L2 configuration, and all
  components even have the same uniform optimal fractional cover.  The loss
  comes from choosing a different dual extremizer on each disjoint scale
  window.  This refutes independent L1-in-scale quotient minimization, not
  P89.  A single compatible potential and its fixed heat orbit reproduce
  C_n(h) exactly; preserve that orbit in every future Calderón argument.
- P104: same-core root-collision replication obeys the target
  O(sqrt(p)) moment bound, and the collision operator has sharp norm at
  most 1/sqrt(60) when distinct supports meet in at most one coordinate.
  Pointwise covariance domination is false, while dense overlaps of size
  at least two and cross-pair phases remain open.  Keep this assay stalled,
  not as an extra active leaf.
- P137: the optimizer-extension defect has an exact
  complementary-slack/Hall normal form.  Coordinate atoms recover the
  dependence remainder and radius atoms recover W1-H; for equal uniform
  sections the defect is exactly the incompatibility of maximum matchings
  across nested radius graphs.  This compresses several walls but does not
  contract P14.  The subordinated Poisson square satisfies the correct
  indicator LlogL-to-L1 budget and has exact L2 norm ||F||_2/2;
  balanced majority separates it from P14 by n^(1/4).  Hence every
  dimension-free L2-normalized scalar square is retired as a direct
  dominator.
- P138: the Euclidean norm of the exact row KR transports is equivalent to
  the anisotropic residual gate and satisfies
  `P89 => P138 => P14`.  Twisted majority times a two-bit parity separates
  P89 from P138 by `sqrt(n)`, refuting dimension-free gluing of independent
  row optimizers into a compatible symmetric flow.  A purely skew
  biased-sign field refutes symmetric-Jacobian domination, and the
  half-derivative Poisson square admits no fixed ambient normalization that
  has both the indicator budget and P14 domination.  None of these walls
  refutes P138.
- P145: curl-free reconstruction exhausts linear common-indicator
  integrability, while opposite singleton maximizers park local
  second-order stability.  Lower-dimensional P138 gives the
  coefficient-one fiber ceiling \(C_h\sqrt h(1+R)\).  The full
  extension-defect inequality, including removed-row energy and an
  \(O(dL^2)\) remainder, is the sole active induction gate.  At sharp
  calibration repetition forces this debt scale absent an independent
  constant gap; tilted thresholds and the
  antipodal simplex-star family are its mandatory positive calibrators.
- P146: actual-fiber deletion gives an exact signed coordinate defect.
  Prescribed deletion is false on balanced majority, but the adaptive gate
  `min_r Delta_r <= C log(e/a)^2` survives repetition, parity, majority, and
  simplex-star and would close P138 by induction.  Generic averaging retains
  the full normalized parent energy and is circular; seek signed Boolean
  coordinate selection or a growing best-coordinate counterexample.
- P147: child-norm imbalance cancels the full J-debt.  The exact column and
  weighted-star majorants, together with the global level-two budget, close
  every fixed-positive-low-row regime.  The residual profile is
  almost-all-high, level-two-pseudorandom, and chain-rule-near-extremal.
  Generic spectral averaging is circular; attack simultaneous near-equality
  rigidity or construct a genuine high-degree counterexample.
- P148: zero rerouting makes parent row normers hereditarily exact, but
  arbitrary parity-block lifts show that equality alone has no structural
  classification.  These lifts have all rows at most 1/2.  Equality-only
  classification is parked; use P149's source-weighted successor.
- P149: small level-two contact and rerouting force source-weighted
  calibrated long Hamming intervals for every high row outside a bounded
  exceptional set.  Raw normer oscillation is gauge-dependent.  Attack
  simultaneous interval overlap/packing, not generic concentration.
- P150: optimal row transport splits exactly into its affine level-two
  part and bidirectional orientation cancellation.  The zero-cancellation
  sector is P138-good.  The full cancellation norm is equivalent to P138;
  use oriented edge-disjointness together with P149 rather than renaming it.
- P151: bidirectional cancellation is exactly stopped absolute-Hessian
  variation minus accumulated rerouting.  Its unsigned energy loses
  sqrt(n).  Attack the signed activity--rerouting pairing only.
- P152: the signed residual lies in a symmetric sign-coherent derivative
  class and is exact wrong-way transport.  Retain this common-indicator
  geometry, but P154 parks its unrestricted divergence gate.
- P153: nonlinear unions of cosets satisfy
  `r_i <= min{ell_i/2, C(n-1)L/(d-1)}`.  Do not reopen high-dual-distance
  or short-local-generator quotient codes; test low-dual-distance,
  large-local-distance or trivial-kernel OA2 geometry.
- P154: the P152 uniform sign gate is affine-gauge equivalent to the full
  arbitrary-row P138 theorem.  Do not reopen fixed-sign concentration
  without exact shared-indicator optimizer contact.
- P155: normalized Hadamard arrays have r_i=(N-2)/4 and bounded P138 ratio
  despite long bidirectional contact in every row.  They are mandatory
  benign calibrators for overlap/packing arguments.
- P156: exact Q7 OA2 sets with identical two-point distance data have
  different row W1.  Park association-scheme or histogram-only proxies;
  preserve higher-order Hall incidence.
- P157: every odd one-pairing simplex phase satisfies P138 by an exact
  transport-plus-influence formula.  Its majority member refutes rowwise
  entropy control.  The residual simplex theorem is aggregate across
  incompatible projective pairings.
- P158: exact-source quadratic spread gives a valid deletion majorant, but
  both proposed entropy-scale controls are refuted by the constant-density
  radial odd-tail family.  It has H_i^2 much larger than one in every row
  while actual row transport stays bounded.  Use it as a mandatory benign
  calibrator and do not reopen quadratic exact-source variance.
- P159: decreasing rearrangements of exact nonnegative contact-flux profiles
  define an L1(ell2) functional between K_n and sqrt(log(en)) K_n.  Its
  target bound closes P146 and native profiles obey a subgaussian width
  envelope.  The dyadic loss is sharp for one bounded curl-free real scalar,
  but indicator separation from P138 is unknown.  Treat it as a Boolean
  preflight and attack the idempotent dyadic-scale upgrade.
- P160: high-row weak Hall collision has an exact anisotropic transport dual
  and implies P138.  Its cost is four-point generator reuse, not a
  two-point distance histogram.  The theorem sum C_i<=(1-a)/(2a) closes
  fixed positive density.  Small/acyclic high blocks, low-energy feedback
  deletion, conditional high-block affinity, nonlinear O(p)-block score
  phases, and common posterior channels with chi-square information
  exp[O(p)] and weighted replica disagreement O(p/sqrt(|H|)) are also
  closed.  The last theorem includes exact rank-O(p) overlapping affine
  syndromes.  Rowwise projective normers refute deriving the channel from
  separate exact contacts.  Bounded-chromatic simultaneous-boundary graphs
  are closed.  Common-indicator spectral signal obeys
  s^T R^dagger s<=(1-a)/a but retains the |H| effective-rank loss.  The
  full projective contact cone nevertheless has linear moments and closes.
  Variance-sensitive AVaR also closes bounded signal-local acyclic ratio.
  Random-order projection closes bounded recovery ratio and every fixed
  active-block degree; anisotropic square-field concentration independently
  closes fixed aggregate contact-field degree.  The survivor is diffuse,
  high-dichromatic, and unbounded-degree in both senses.
- P161: the soft-threshold collision norm is convex and recovers the P160
  high-row sum up to O(L^2).  At a maximizing indicator, its normalized
  contact field is a subgradient, the indicator is a top level set of that
  same field, its conditional contact mean is Q_tau+O(L), and its L2 norm
  is at most 1/sqrt(2).  The fixed active potentials also obey the exact
  cone-wide bound ||((a^(-1)E[gZ_i psi_i]-tau)_+)||_2<=Q_tau(A) for every
  equal-density fractional g, with a uniform-convexity remainder.  Point
  swaps lose |A|; translation mixtures and heat smoothing have nonpositive
  response coordinatewise; cone plus spectral signal alone has an abstract
  common-atom wall.  Projective contacts, bounded signal-local acyclic or
  random-order recovery ratio, bounded active-block degree, and bounded
  aggregate degree are proved benign.  The remaining exact-contact row is
  diffuse and unbounded-degree.  Do not return to arbitrary row fields,
  marginal curvature, quadratic joint-discrepancy states, or scalar
  random-order Tauberian recovery.
- P162: threshold-band redistribution has an exact support formula and
  normal-cost bound; a macroscopic rotation in an affordable band closes
  P161.  Strict individual locks reduce, up to a universal additive term,
  to a weighted coordinate-code margin, and balanced tie-free locks close.
  These alternatives are not proved exhaustive.  An abstract near-band spike
  model refutes deriving aggregate approximate locks from the convex/top-level
  data alone by a sharp `sqrt(|I|)` factor.  Repetition refutes long-interval
  rotation and GV codes refute Hamming-only margins.  The unrestricted
  Cayley/Delsarte independence gate is also false because pinned faces retain
  density `1/2` regardless of a charged coordinate.  Random priorities
  prove the dimension-dependent `2(n-1)k` bound and the target `2r^2`
  bound for codimension-`r` affine codes.  But the outlier half-ball
  refutes both the universal fractional code-SOCP gate and
  `rho_i^2<=(k+1)p_i` at constant density; the SOCP forgot section mass.
  Near-pinned strict-lock thresholds are paid by marginal entropy.  The
  repaired candidate `sum_i theta_i rho_i^2<=Ck^2` would close the
  section-balanced remainder, but remains unproved; it is sharp for affine
  codes, zero for coordinate-flipped down-sets, and product-stable.  Even
  after multiplying by `theta_i`, the rowwise priority shortcut is false
  on balanced antipodal Hamming balls.  The information-weighted
  `theta_i rho_i^2<=C k d_i` is the smaller surviving assay; its exact
  harmonic overlap lift still needs coherent geometric selection inside
  the common projection fibers.  The
  raw positive-superlevel square self-bound is false by `sqrt(h)` on an
  exact projective one-row KR/top-set contact satisfying the fixed-contact
  cone and remainder.  It remains open only whether global P161 maximality
  forces cross-row compensation.  The calibrated replacement is a
  truncated-carre or first-power nested-superlevel assembly.
- P163: for normalized exact row costs `r_i=t_i/a`, the separation ratio is
  exactly `R_138/R_14=RMS(r)/mean(r)=sqrt(1+CV(r)^2)`.  Transitive families
  have equality and uniformly macroscopic coordinate orbits give only a
  bounded separation.  If `R_14<=C`, `R_138=rho` tends to infinity, and
  `H={i:r_i>sqrt(rho)L}`, then

      rho sqrt(nL) <= C |H| <= C n/sqrt(rho),
      R_nu(H) >= c n rho^2 L^2/|H|^2,
      rho^2 L/C <= max_i r_i <= sqrt(nL),
      rho^4 L <= C^2 n.

  Thus a separator needs a growing but vanishing, joint-entropy-rich
  mesoscopic spike block; neither finitely many spikes nor a macroscopic
  symmetric block can work.  Products of P138-good factors remain
  P138-good with a factor-count-free constant, and first-order-resilient
  product profiles concatenate exactly.  Sparse fixed-cardinality grafts,
  including every deterministic systematic graft, preserve P138 over a
  good core.  A candidate must instead use variable/dense fibers or
  overlapping nonproduct constraints, with a multi-pairing construction
  in the mesoscopic window as the clean falsifier assay.

  The first dense-fiber class is now exact.  For a surjective binary
  generator `G` and `A={x:Gx in B_r}`, deleting column `g_i` gives

      r_i=(1/2) W1_(d_i)(Unif(B_r),Unif(B_r+g_i))

  whenever the remaining columns span the quotient; `d_i` is their Cayley
  word metric.  The nonsurjective formula uses the centered difference of
  the two section indicators on the leave-one-out span.  When `d_i` is
  Hamming, the transport reduces exactly to two radial/binomial orbit
  coordinates.

  For `G=[I_k|M]`, codensity `ell=o(k)`, and `m` approximately equal high
  generator rows of size `q`, P14 and the mesoscopic entropy ceiling force

      q <= C k ell/m,
      q <= C sqrt(m ell).

  The only critical balance is

      m ~ k^(2/3) ell^(1/3),
      q ~ k^(1/3) ell^(2/3),
      R_138 ~ (k/ell)^(1/6).

  A separator must have full-span mixing of the ball but strong failure of
  mixing after almost every one-column deletion.  Random dense blocks tend
  to mix both; structured blocks tend to have duplicates, short circuits,
  products, or insufficient joint entropy.  Bounded exact tests through
  quotient dimension eight are benign, but this is not closure.

  This remains a
  falsifier-profile contraction, not a proof of P138.  The scalable
  nonlinear antipodal three-pair family has unbounded Walsh degree but both
  normalized ratios tend to `1/(2 log 2)`, so it is benign.
- P106: if distinct active Walsh supports meet in at most one coordinate,
  then every fixed reveal order satisfies

      ||S_pi(F)||_p <= sqrt(p-1) ||F||_2.

  The P89 L2 endpoint converts this to the native SF-P89 scale.  Levelwise
  assembly also proves the SF-P89 target on the full combined P105 affine
  design family, whose exact chord supremum charges the number of levels.
  This is stronger square-function structure on proved classes, not a
  universal last-pivot theorem.
- P107: write `A_V(x)={S subset V:x in S}` during backward coordinate
  deletion.  If every selected pivot satisfies either

      (sum_(S in A_V(x)) |r_S|)^2 <= p sum_(S in A_V(x)) |r_S|^2

  or its residual incidence vectors `1_(S\{x})` are independent over
  `F_2`, then the reverse reveal order obeys

      ||S_pi(F)||_p <= sqrt(p) ||F||_2
                    <= sqrt(2p(n-1)) tau_2(c).

  More generally it is enough that each residual frequency family have
  `Lambda(p)` constant `O(sqrt(p))`; the coefficient-specific version is
  enough for the given potential.  A failed safe-deletion process leaves a
  hereditary local `Lambda(p)`-bad core.  At constant one every vertex in
  that core has effective coefficient multiplicity `>p` and a residual
  binary circuit.  This is a necessary falsifier profile, not a
  counterexample and not a derivation from the compatible chord budget.
- P108: the single-exceptional-shell compatible potential

      F_n = 2^(1-n) sum_(|S|>=2) chi_S

  has, at every first backward pivot,

      Q_x = 2^(1-n) (prod_(j!=x)(1+Z_j)-1),
      (||Q_x||_4/||Q_x||_2)^4
        = 2^(n-1)-2+1/(2^(n-1)-1).

  Nevertheless every predictable tree obeys

      S_T(F_n) < 2/sqrt(3) < 2 sqrt(n) tau_2(c)

  pointwise for `n>=4`.  This exactly refutes universal local
  `Lambda(4)` deletion, not SF-P89.  Large pivot spikes are nested on rare
  all-positive prefixes; worst-local summation is therefore unavailable.
- P109: if `A_ij=Z_i Z_j a_ij` are compatible chords, the invariant reveal
  coefficient at state `(R,x)` is exactly the joint sum of

      sum_(j in R) Z_j P_R B_xj

  and

      sum_({i,j} subset R) Z_i Z_j partial_x P_(R union {x}) B_ij,

  where `B_ij=(I+L_-ij)^(-1)a_ij`.  The second, inherited-coefficient
  channel is load-bearing.  The natural P30 occupation lift formed from
  the chords before quotienting is false: on the unit full-parity star its
  normalized loss is at least

      n^(1/2-1/p)/(2 sqrt(p)),

  and a transverse allocation has scalar output zero but occupation norm
  `gtrsim n^(1-1/p)` with `tau_2(c)=O(1)`.  Never replace the invariant
  scalar bracket by this pre-quotient field.  Calling the scalar bracket's
  exact `L^(p/2)` dual ``global packing'' supplies no contraction by itself.
- P110: quotient-measurable P89 outputs with at most `Kp` singly occurring
  nonzero label classes satisfy the target with constant `C(1+K)`, and fully
  repeated label systems satisfy the sharper all-moment square-root bound.
  Independent homogeneous quotient assembly can exceed the full quotient
  exponentially on a bent phase.  The exact matrix reconstruction has trace
  `2F`, but separating trace from its `S_2` norm costs `sqrt(p)` on complete
  quadratic chaos.  The first statement is a class theorem; the latter two
  are architecture walls.
- P111: successive repeated-label quotient increments form a reverse
  martingale and obey a depth-free conditional subgaussian estimate with
  square charge sum_t(a_t^2+b_t v_t^2+s_t^2 rho_t^2).  The corresponding
  gate closes a strict zero-cover class with order-n initial singleton
  labels.  Right-Hodge compression removes the matrix representative gauge
  exactly, but the resulting tensor is not locally subordinate to the chord
  field.
- P112: conditional Bernstein composition gives
  `||F_0||_p<=||F_T||_p+C(sqrt(pV)+pL)` and handles P111's rare-event
  calibration.  Every canonical Boolean corrected gradient is P89-good,
  uniformly over degree, quotient labels, and multiplicities.  The exact
  joint-Hodge audit closes Hutchinson, sparse-diagonal, and pointwise
  Schatten scalarizations.
- P113: the depth-one repeated-core/leaf family has chord graph `K_(N,2m)`
  and native variance budget `2mN`, but conditional-variance essential
  supremum `N^2`.  This refutes deterministic Bernstein transfer from the
  original cover.  Moment-averaged generic repair either loses through its
  maximal increment or returns to SF-P89/P82.
- P114--P115: arbitrary gauges for Boolean-generated outputs obey both the
  local half-space barrier and the maximum-sensitivity bound
  rho_n(F)>=S(S-1)/(2(n-1)sqrt(n)); the canonical Boolean Hessian also
  yields the gauge-annihilating average certificate
  rho_n(F)>=sqrt(E[k(k-1)]/(n-1)).  Permutation-invariant Boolean outputs
  have an exact canonical quotient, and disjoint outputs tensorize exactly.
  Canonical sensitive cliques remain non-native.  The sublinear-sensitivity
  localization remainder is parked as a strict special case.
- P116: the orbit-absolute envelope satisfies `C<=O<=D` and equals
  `sup_sigma C(M_sigma h)` for correlated Gamma-moment symbols.  It repairs
  P103 on the P105 witness by `sqrt(M)`, but its constant symbol is P89
  itself, so it is not a contracted crux.
- P117: all unweighted separated fixed-orbit conjugate mixed norms lose an
  extra `sqrt(n)` at `p=n/4`; do not separate the edge and test legs before
  scale allocation.
- P118: `F=R^* I A` is an exact signless support-incidence factorization with
  a strict Hilbert contraction away from degree two.  Its joint `Cp`
  edge-Hilbert estimate is sufficient but stronger than P89 and unproved;
  pointwise, operator-norm-only, and generic two-stage versions are closed.
- P119: arbitrary positive pointwise weights and positive stopped local
  Hölder sums still lose `sqrt(n)`; unrestricted signed stopping is exactly
  the original pairing.  Preserve signed spatial cancellation through a
  genuinely smaller state.
- P120: canonical unsigned per-support incidence/Hodge summaries are
  exponentially phase-blind on aligned versus bent flat spectra.  This is a
  strengthened P110 wall, not a ban on quotient-aware or globally signed
  methods.
- P88: the Rademacher residual theorem and the general-product BKZ theorem
  are equivalent up to universal constants by two-copy orientation.
- P89: the compatible-flow endpoint and Euclidean fractional-vertex-cover
  dual are equivalent; `P87 => P89 => P138 => P14`, with the `s=2` and dual `p>=n`
  ranges, the target all-`p` extreme-pair selector, the matching `p=2`
  chord estimate, and the sharp singleton/disjoint-parity calibrations proved.
- P90: P89 is proved for low binary support complexity, every homogeneous
  degree with constant `2e`, any two arbitrary degrees with constant `4e`,
  every three-term arithmetic progression with constant `225`, `m`
  `64`-lacunary levels with constant `32em/15`, at most two even plus
  two odd levels, bounded mixed degree, and sufficiently high-mean-degree
  phase-aligned spectra; the color family has an exact Calderon isometry.
- P91: arbitrary-degree multi-core gradient--quadratic towers satisfy P89
  uniformly.
- P92: uniformly P89-good potentials on disjoint coordinate blocks glue
  without a block-count loss.  With

      B_a = sqrt(|V_a|-1) tau_a,

  independent subexponential Bernstein gives

      ||sum_a F_a||_p
        <= C [sqrt(p) (sum_a B_a^2)^(1/2) + p max_a B_a],

  while the block-diagonal cover splits exactly as
  `tau_global^2=sum_a tau_a^2`.  This permits arbitrarily many irregular
  global degree levels, but independence of the coordinate blocks is
  load-bearing.
- P93: for each fixed `m`, every P89 output supported on any `m` arbitrary
  degree levels satisfies the target with a constant `C_m`, uniformly in
  dimension, maximal degree, level locations, and separation.  The proof
  uses a fixed-order Muntz endpoint inequality, confluent Newton
  compactification, and at most `m+1` signed color scales with the native
  cover norm.  Lacunary witnesses force `C_m` to grow at least linearly
  for scalar synthesis.

Finite enumeration remains evidence only even when it supports one of these
universal conjectures.

## Tool selection and accuracy walls

| Tool | Reliable use | Wall to record before applying it |
|---|---|---|
| Martingale square functions | Predictable decompositions and `sqrt(p)` upgrades when the square field is controlled in the same native model | A scalar moment bound does not imply the stronger square-function bound; random stopping-line conditioning is not an `L^p(l2)` contraction; fixed radial pointwise variance allocation is false at the P89 scale on common-core stars; even the best coordinate order has BMO `asymp n^(3/2)` on the target-good complete quadratic chaos against native scale `asymp n`. P106 proves the `L^p` reveal square on linear supports and the combined affine stress family. P107 extends this by weighted backward peeling and local `Lambda(p)` spectra, but P108 refutes local good-pivot deletion universally. P109 refutes pre-quotient occupation. P113 additionally refutes deterministic quotient-flag variance transfer; generic random-bracket repair loses through its maximal increment, while symmetric refinement returns to P82. Only a smaller quotient-sensitive adaptive state would be new. |
| Bounded differences / Efron--Stein / Bernstein | Variance, subgaussian or subexponential concentration of a single stable functional, and depth-free conditional-mgf composition | It does not control Fourier `l1` slices. Keep variance and peak separate, but never infer deterministic worst-coset variance from an average chord budget: P113 loses `N/(2pm)` on a native-benign common-core family. Conditional variance alone also misses rare spikes. |
| Hypercontractivity | Fixed degree, low-level Fourier mass, radial/binomial reductions | Degree growth or absolute aggregation can reintroduce logarithmic or polynomial losses. P110 shows that even native quotient optimization on each homogeneous level followed by `ell_2` assembly can lose exponentially; mixed-degree cancellation must be retained |
| Decoupling / random selectors | Conditional expectations that leave genuinely independent front signs, with the reconstruction multiplier and selector probability both audited | P93 makes the optimized P89 color selector uniform on every fixed-cardinality degree spectrum, but its constant necessarily grows with the number of levels; scalar mixtures across many levels lose logarithmically on intervals and linearly on lacunary sets. P105 additionally refutes taking an independent optimal compatible-flow selector at every Calderón scale, even under one common fractional cover. Preserve one fixed compatible heat orbit in the joint bilinear contract. Degree-free front-sign decoupling loses `sqrt(n)` on full parity, endpoint-color randomization has an exact order-`r` reconstruction loss on a native complete-bidirected P87 array, and P161 random-order resolvents attenuate degree `k` by `1/(k+1)`. Chebyshev profiles show that even a positive bounded scale curve can hide endpoint signal of order `D^2`; scalar Tauberian recovery is not a degree-free continuation. |
| Green/Riesz resolvents | Canonical compatible flow, exact shifted-Hessian identities, and a nonempty feasible point for P89 | Keep the shifted resolvent for P87. For P89 first quotient the symmetrized derivative field over all compatible pair flows; ambient Hilbert--Schmidt replacements attack a different proxy. P110's exact matrix reconstruction has trace `2F`, but any universal separate trace comparison must lose at least `sqrt(p)`. After P111 right-Hodge compression, P112 still closes Hutchinson, sparse-diagonal, and pointwise Schatten scalarizations. |
| KR transport / cut towers | Exact native duality, finite counterexample search, compatibility-preserving representations, P138 Euclidean row transport, and P89 pair-array duality | A second exact representation is not a quantitative estimate. Rowwise scalar summation loses `sqrt(n)`, while P138 shows that Euclidean aggregation can be sufficient without P89 compatibility. Twisted majority refutes dimension-free gluing of the independent row optimizers back into one P89 flow. |
| Sparse-support obstacle Hessian | For the capacity-obstacle odometer, first use complementarity to prove `mu{u>0}<=2a`, then localize each mixed derivative to four support translates, square-sum by Walsh orthogonality, and use `L_su=(s/2)(1_I-d)` | The support and source bounds are obstacle-specific. Do not replace them by total occupation, which loses a factor `s`, or by a claim that heat balayage minimizes FCR, which is false. Do not export the conclusion to arbitrary Hessian fields without separately proving both sparse support and the source `L2` estimate. |
| Transportation--entropy | Controlling one law against the ambient product law with the correct dimension factor | Applied after lossy section splitting it cannot restore cancellation already discarded |
| Stein / exchangeable pairs | Bounded-summand theorems with an explicit conditional variance proxy | The BKZ hypotheses imply only the generic bound `|g_i|<=M+(n-1)beta`. An application-specific `L` can be much smaller and then gives a genuinely different subgaussian scale; substituting the generic cap does not recover the sharp linear rate |
| Cumulants / diagrams | Fixed orders or absolutely summable coefficient models | Absolute diagram assembly can lose cancellation and does not give all-`p` control from finitely many orders |

## Mandatory adversaries

Test the actual target and every proxy on the relevant structured families.

- Full parity: coherent high degree; checks the resolvent and defeats
  degree-free front-sign decoupling.
- Bent phase: bounded pointwise derivatives with exponentially large Fourier
  `l1` mass.  The symmetric quadratic bent phase is also the mandatory P110
  test for homogeneous quotient atomization: its degreewise native square
  budget is exponentially larger than its full quotient norm.
- Singleton: sparse endpoint and exact `n^2 2^{-n}` scale.
- Balanced majority and middle slices: radial positive controls for P14/P22,
  but destructive for separate-section and local entropy allocations.
- Twisted majority times a two-bit parity: separates P138's independent
  Euclidean row transports from P89's simultaneous compatible flow by
  `sqrt(n)`.  It is the mandatory gluing and row-indexed-state adversary.
- Disjoint parity checks: unbounded canonical Green/transport ratio while P22
  remains within its entropy budget; P89 must and does repair this family by
  an optimized compatible flow of exact scale `sqrt(n) a`.
- Shared-core parity sunflowers and all affine systems: proved P22/P78 classes,
  not live falsifiers.
- Asymmetric product-Riesz sets and sparse Cartesian products: intermediate
  densities and product-depth calibration.
- Quadratic-chaos upper tails: strongest current finite P14 ratios under the
  script normalization.
- For all-moment sharpness, use the BKZ quadratic family
  `g_i=M Z_i+(beta/2)Z_i sum_(j!=i)Z_j`.  Its moderate moments calibrate
  `p<=n`, while the all-positive atom of mass `2^(-n)` calibrates every
  `p>=n`.  Any proposed improvement for `p>>n` must first confront the
  resulting `Mn+beta n^2` saturation.
- Positive versus Walsh--Hadamard complete quadratics: both have unit chord
  contacts, the same optimal cover, and identical separate `p=2` edge-flow
  magnitude data, but their normalized moments at `p=n/4` differ by
  `sqrt(n)`.  This is the mandatory test for any contact count, contact
  entropy, or edgewise uncertainty summary.  Passing it requires
  target-`p`, jointly signed, flow-weighted information.
- Composed majority: one matched-section row is `sqrt(n)` larger than the
  corresponding exact transport row; tests false coordinatewise faithfulness.
- Symmetric quadratic P81 family: fractional conflict is maximally lossy while
  the true random-order correction is target-benign.
- Four-dimensional stopping-line field: defeats the false
  `L^p(l2)`-contraction shortcut.
- Dyadic mixed-degree staircases and quadratic-plus-parity mixtures: detect
  premature absolute aggregation across scales or degrees.
- Affine-spread Steiner resolutions at degrees \(4,16,\ldots,4^M\) on one
  common finite-field coordinate set: every component sharply calibrates
  P89 in \(L^2\), while disjoint Calderón windows make independent
  scale-by-scale quotient selection lose \(\sqrt M\).  This is the mandatory
  P103/P105 proxy test; a common fractional cover does not repair it.
- For affine-incidence moment routes, first reduce an ordered even tuple to
  its odd-multiplicity support.  Apply the maximum-block intersection cover
  before enumerating circuits.  At order eight this isolates levels one and
  two and makes all higher levels relatively independent exactly.  At
  general order it only reduces to logarithmically many low levels; a crude
  triangle inequality there is not an all-moment proof.  Distinguish
  primitive binary circuits from geometric connectedness, retain exterior
  parity after every root trace, and never record primitive AOE as a strict
  reduction because it is equivalent to the positive moment target.  The
  full coordinate carré and sharpened reveal square are scalably false on
  affine planes.  Always test generic
  Sidon/Rudin proposals on APN Sidon caps and dissociated-coloring proposals
  on the full level-one affine packet.
- For SF-P89, reuse the complete quadratic, common-core, disjoint/full parity,
  Fano/affine-plane, and combined affine-spread tests.  Complete quadratic
  refutes BMO but is target-scale for the reveal square.  A meaningful new
  stress family must combine dense support intersections with load-bearing
  cancellation in the chord `L-infinity` norm and must survive the P107
  deletion screen.  At even `p=2q`, compute local zero-sum `2q`-tuple
  weights, equivalently the coefficient-specific local `Lambda(p)` quotient,
  at every induced core, but also compute the full bracket: P108 shows that
  even an unbounded local quotient can be harmless when its high values are
  nested on rare prefixes.  Testing only overlap, cancellation, or local
  `Lambda(p)` growth is no longer discriminating.  Also test the P109
  full-parity unit star and its transverse zero-output allocation.  They
  separate the invariant scalar Doob square from every pre-quotient
  resolvent occupation field by a polynomial factor.
- For binary quotient-code proposals, record the multiplicities of nonzero
  label classes.  P110 closes every model with at most `O(p)` singleton
  types, so a meaningful survivor must have `s/p` unbounded.  Repeated-column
  replication alone is no longer a discriminating stress test.
- For quotient flags, test both P111's depth-one rare event and P113's
  repeated common core with independent leaves.  The first distinguishes a
  Bernstein variance/peak split from a worst-case subgaussian charge.  The
  second distinguishes valid conditional-mgf composition from the false
  deterministic transfer of worst-coset variance from the original cover.
  Report the actual output ratio, the random bracket in `L^(p/2)`, and the
  maximal increment separately.  Do not use canonical Boolean phases as
  prospective falsifiers: P112 closes every canonical Boolean corrected
  gradient, including all degrees and label multiplicities.  For a
  noncanonical Boolean proposal, first apply P114--P115.  Families with
  maximum sensitivity S>=delta n are already safe for every gauge.  Full
  permutation symmetry is closed exactly, and additive repetition of a fixed
  disjoint output cannot amplify the ratio.  Only sublinear-S examples with
  |F(x)|/sqrt(E[k(k-1)]) large test the unresolved pointwise claim.  Report
  the native ratio itself, not only tau_can/rho, because finite optimization
  shows that gauge separation and target ratio need not correlate.
- For matrix routes, first apply the exact P111 right-Hodge compression.
  Then test the common-core leaf family, which defeats pointwise,
  carré-du-champ, and coordinate-martingale subordination by sqrt(N/k).
  Complete quadratic and P105 affine blocks have no removable gauge and
  remain mandatory tests of trace and scale separation.  Also test:
  Hutchinson scalarization for circular reproduction of the scalar input;
  sampling n/p diagonals on complete quadratic for a sqrt(p) loss; and
  pointwise Schatten dualization on many disjoint Walsh characters.

For every claimed failure, print or prove both

    actual target / target budget

and

    proxy / proxy budget.

Growth of only the second ratio kills the proxy, not the theorem.

## Literature imports

- Domelevo--Ivanisvili--Petermichl--Volberg26: the new commutative
  two-point Bellman proof gives the known dimension-free first-order Riesz
  bound only for \(p\ge2\).  Its edge symmetrization is a useful method
  precedent, but black-box iteration returns to the audited ambient-Riesz
  wall and does not supply the P14 endpoint or simultaneous row geometry.
- Borichev--Volberg24: finite-cotype vector-valued cube concentration
  requires one Banach-valued map with a controlled pointwise strong
  gradient.  P14 is a sum of rowwise transport optima and presently has no
  such encoding; packaging every optimizer merely reconstructs the gluing
  problem.  Do not import the theorem without an explicit native map and
  dimension-uniform target geometry.

Use the durable packets in `literature/` before searching again.

- DPMS94 and OZ16: decoupling directions and their degree dependence.
- Adamczak--Latala12: coupled/decoupled comparison and exact mixed-norm
  moment formulas through order three for tetrahedral chaoses.  The durable
  packet is useful for auditing fixed-order tensor partitions, but it does
  not remove the unbounded-degree P161 reconstruction wall.
- Cassese26: a dimension-free variational Korn proof whose
  compatibility-preserving quadratic-variation idea is relevant, but whose
  diagonal strain is circular for P89; the natural local off-diagonal trace
  is refuted by the common-core field.
- Spector--Spector20 and Van Schaftingen13: Euclidean BMO Korn and canceling-
  operator endpoint theorems.  The former uses the full symmetric gradient
  with a dimension-dependent constant; the latter gives a symbol-level
  `L1` Sobolev criterion.  Neither controls P89's off-diagonal Boolean
  quotient or its cross-support `L-infinity` cancellation.
- Junge--Mei--Parcet14: crossed-product tangent modules keep row/column
  geometry together, but the recorded constants grow like `p^(3/2)` and
  the general module norm does not preserve the scalar chord
  `L-infinity` cancellation.  Use it as a language/method audit, not an
  order-`p` P89 theorem.
- Ben-Efraim--Lust-Piquard08: cube/CAR Poincare theory and its native
  row--column decomposition are useful precedents for quotienting before an
  embedding.  Their input is the full one-index gradient, not P89's
  off-diagonal compatible chord quotient, and the CAR/Khintchine passage
  pays the extra `sqrt(p)`.  Use the durable packet as an ordering warning,
  not a P89 theorem.
- Cassese26 minimal Korn: the rank-one criterion rules out a black-box Korn
  inequality which measures only arbitrary off-diagonal matrices, because
  the unmeasured diagonal contains rank-one matrices.  P89 removes the
  corresponding singleton sector and imposes additive chord identities, so
  this is not a theorem counterexample.  Any Korn import must use those two
  structures before applying the matrix theorem.
- OSSS05 and Schramm--Steif10: adaptive revealment theorems are diagnostic
  analogues, not SF-P89 inputs.  A full coordinate tree has revealment one;
  OSSS's generic real-valued squared-distance form also pays the path length,
  and Schramm--Steif controls terminal `L2` Fourier mass rather than the
  `L^(p/2)` moment of the realized bracket.  Read the durable packets before
  invoking decision-tree literature.
- Sherstov--Storozhenko--Wu23: their adaptive coordinate-decision-tree
  theorems give strong levelwise Fourier `l1` bounds.  For a full depth-`n`
  reveal, however, they are policy-blind and do not control the realized
  bracket or the compatible-chord quotient.  This is not an SF-P89 input.
- Lai15 and Muller97: sharp general-filtration Bellman/Carleson embedding and
  fixed Haar-rearrangement boundedness both assume or characterize a
  Carleson packing constant.  Neither derives that constant from `tau_2(c)`
  or chooses a sign-adaptive policy.  Feeding squared reveal increments into
  Lai requires the already-refuted conditional future-energy/BMO gate;
  Muller's theorem is fixed and linear.  Generic ``global Carleson packing''
  is therefore not a new proof contract.
- Pisier16, Malliavin--Malliavin, and Horn: on the binary group, a character
  set is subgaussian exactly when it is a finite union of binary-independent
  sets, and Horn's rank-density formula gives the minimum number of such
  classes.  This yields the native class bound

      ||S_pi(F)||_p <= sqrt(q_pi(p-1)) ||F||_2,

  where `q_pi` is the maximum last-pivot binary-matroid covering number.
  Use this as P107's structured certificate.  P108 shows that bounded
  `q_pi`, or even a locally bounded `Lambda(4)` constant, is not necessary
  for a target-good global square function.
- Caro--West--Yuster11, Kallenberg05, and Pozdnyakov--Steele13: equitable
  hyperedge orientations, predictable sampling, and scalar random-
  permutation maximal inequalities are exact adjacent results but do not
  solve SF-P89.  Respectively, they use an edgewise rather than global order,
  preserve selected-sign laws rather than order-dependent brackets, and
  treat value-independent scalar `L2` maxima rather than adaptive
  `L^(p/2)` bracket moments.  Consult their durable packets before reopening
  these directions.
- Chatterjee07: the exact exchangeable-pair lemma used by P34.
- Ivanisvili--Volberg22, DIPV26, and Chen--Dai26: derivative-range,
  dimension-free Riesz/Bellman, and randomized-projection results, with the
  exact exponent, norm-order, two-index, and resolvent mismatches with P87/P24
  recorded.
- Ivanisvili--Xie--Zhang26: Beckmann--Talagrand results and why their Euclidean
  lower/quotient formulations do not supply P14's entrywise transport upper
  bound.
- Hytönen--Naor13: Pisier inequalities and their mismatch with the native
  P11/P14/P22 contracts.
- Naor16: the sharp-scaling metric X_p theorem controls balanced coordinate
  restrictions of one scalar function by its ordinary derivative norms.
  It suggests quotient-filtration architecture but does not convert P89's
  symmetric chord quotient to those derivatives, and its analytic
  p-dependence is not the desired linear one.
- Eskenazis--Ivanisvili20: low-degree, tail-space, and narrow-spectrum
  polynomial inequalities rigorously support the bounded-degree and
  narrow-band P89 sectors.  Their degree or bandwidth dependence prevents
  universal mixed-degree assembly.
- Cano-Marmol--Conde-Alonso--Parcet24: balanced Fourier truncations over
  discrete groups and noncommutative X_p inequalities preserve row/column
  geometry, but still begin with one scalar/operator input and its ordinary
  cocycle derivatives.  Passing from P89 chords to those derivatives loses
  the quotient and the known extra moment factor.
- Banuelos--Kim25: sharp O(p) probabilistic discrete second-order Riesz
  transforms are bounded matrix multipliers acting on a controlled scalar
  martingale.  In P89 the chord field is the source datum and the scalar
  potential is unknown; using it as the martingale input is circular.
  Import only the joint martingale-transform architecture unless an exact
  chord-to-predictable-integrand factorization is supplied.
- BBLM05, APS22, and Fitzsimmons--Pitman99: historical P30/P51 imports; their
  exact translations and the reasons those retired proxy routes did not close
  are already recorded.  Do not reopen them without one new native transfer
  lemma.

For new literature work, store metadata, source or durable extraction, and
`key-results.md` under `literature/<key>/`, then regenerate the literature
index.  Do not leave theorem extraction only in `/tmp`.

## Workflow

1. State the native hypotheses and every stronger auxiliary assumption.
2. Name the exact target and classify the route as equivalent, sufficient,
   necessary, special-case, or heuristic.
3. Locate the last exact arrow.  If the current object is only a reformulation,
   return to that arrow before adding another proxy.
4. Record the tool's dimension, degree, exponent, norm, and envelope losses.
5. Test the mandatory adversaries that match those losses.
6. Distinguish failure of the actual target from failure of the tool.
7. Promote only a complete proof, exact counterexample, exact reformulation,
   or sharper falsifier profile.
8. Synchronize the proof spine, `LINEAR_RATE_STATUS.md`, `dashboard.json`,
   `dashboard.html`, relevant scripts, and this skill when the proof contract
   changes.  Bump the dashboard only for such a change, not for repeated
   numerics or cosmetic prose.

## Output standard

Every concentration proof report must end with four explicit lines:

    Native theorem status: proved / open / refuted
    Additional hypotheses used: ...
    Strongest proved bound: ...
    Remaining loss or exact counterexample: ...

Never claim the native rate from lower bounds, finite numerics, a stronger
coefficient hypothesis, a route-equivalent representation, or the failure of
a particular upper-bound method.
