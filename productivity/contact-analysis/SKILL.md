---
name: contact-analysis
description: "Use when the task is FEA contact, penalty or Lagrange methods, contact stiffness, penetration, friction, stick-slip, master-slave contact, node-to-surface, or tied interfaces in bolted joints and bearing contacts. Compute finite element contact analysis quantities for aircraft structure: determine normal contact forces with the penalty method from contact stiffness and penetration, estimate penalty stiffness from the contacting element properties, check Lagrange multiplier enforcement of zero penetration, apply Coulomb friction to categorize stick or slip, and run penetration control until penetration is under tolerance. The skill covers master-slave and node-to-surface gaps, tie constraints, and bolted joint and bearing contacts. Trigger: contact analysis, fea contact, penalty method, lagrange multiplier, contact stiffness, penetration, coulomb friction, stick-slip, master-slave, node-to-surface, tie constraint, bolted joint, bearing contact."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [contact-analysis, fea-contact, penalty-method, lagrange-multiplier, contact-stiffness, penetration, coulomb-friction, stick-slip, master-slave, node-to-surface, tie-constraint, bolted-joint, bearing-contact]
  version: 0.1.0
  author: Aero Agent Skills
---

# Contact Analysis (structures/fem/contact-analysis)

Use when the task is finite element contact analysis of aircraft
structure: penalty versus Lagrange enforcement, contact stiffness and
penetration control, Coulomb friction with stick-slip states,
master-slave and node-to-surface formulation, tie constraints, and
typical bolted joint and bearing contact applications. This leaf sits
beside structures/fem/calculix-nonlinear (which owns the nonlinear
solver workflow into which contact runs are fed) and
structures/fem/calculix-linear (linear static checks); it computes the
contact mechanics quantities, not the global solve.

## Domain quick reference

- Penalty method: the normal contact force is the penalty stiffness
  times the penetration, F_n = k_pen * p. Contact is soft: a small
  penetration is always present, and larger stiffness drives it down
  at the cost of ill-conditioning.
- Lagrange method: the zero penetration constraint is enforced exactly
  with a Lagrange multiplier (the contact pressure). No penetration
  parameter is tuned, but the active set must be iterated and the
  method can introduce zero-energy modes and convergence cost.
- Penalty stiffness estimate: k_pen = alpha * E * A / L from the
  softer contacting member (E modulus, A contact area, L
  characteristic length), with alpha typically 10 to 1000 times the
  underlying element stiffness scale.
- Penetration control: for an applied normal load F, penetration
  p = F / k_pen; raise the stiffness by a factor and re-check until
  p falls under the accepted tolerance.
- Master-slave (node-to-surface): slave nodes are projected onto the
  master surface; the signed gap is the projection distance along the
  master surface normal. A negative gap is penetration, a positive gap
  is separation.
- Coulomb friction: the maximum tangential (shear) force is
  f_max = mu * |F_n|. When the trial shear is below f_max the
  interface sticks (elastic shear, no relative sliding); at f_max it
  slips (sliding with frictional resistance at the limit).
- Tie constraints: rigidly bond two surfaces (no separation, no
  sliding) within a relative displacement tolerance, for example
  bonded patch doublers or potted inserts.
- Typical aerospace applications: bolted joint lug-to-bolt bearing
  contact, bushing-sleeve interfaces, and fastener head-to-structure
  clamping; FAR-25 and CS-25 set the certification context for the
  strength checks that follow the contact solution.

## Workflow

1. Identify the contacting pairs and the softer member; record the
   unit convention (N/mm is assumed here).
2. Estimate the penalty stiffness with contact_stiffness_estimate.
3. Compute the signed gap of each slave node against its master
   surface with node_to_surface_gap.
4. Get the normal force from the gap with penalty_contact_force, or
   check exact enforcement with lagrange_contact_check when the
   constraint must hold with zero penetration.
5. If penetration exceeds the accepted tolerance, raise the stiffness
   with penetration_control until the penetration is under tolerance.
6. Compute the tangential (shear) response with friction_force: the
   result is categorized as sticking or slipping.
7. Check tied interfaces with tie_constraint_check where the joint is
   bonded.
8. Confirm the deterministic checks with the contract test
   scripts/test_contact_analysis.py.

## Penalty versus Lagrange

The penalty method converts the contact inequality constraint into a
spring: F_n = k_pen * p with penetration p. It is simple to implement
and keeps the tangent stiffness positive definite, but the result
depends on the user-chosen stiffness and always shows a small,
non-physical penetration. The Lagrange method carries the penetration
to zero by treating the contact pressure as an unknown, at the cost of
active-set iteration and possible ill-conditioning. In practice,
augmented Lagrange methods combine both: a Lagrange multiplier base
with a small penalty regularizer that stabilizes the iteration. This
leaf implements the two pure methods and lets the caller compare them
on the same gap input.

## Friction and stick-slip

Coulomb friction caps the tangential force at mu times the absolute
normal force. The interface is categorized as sticking when the trial
shear stays below the cap (the tangential force equals the trial
value, relative sliding is zero) and slipping when the trial exceeds
it (the tangential force saturates at the cap and sliding occurs).
Because the cap scales with the normal force, a joint carrying a high
clamping load resists far more shear before it slips than the same
joint unloaded in the normal direction.

## Worked example

Steel bolt bearing contact: E = 200,000 N/mm^2, contact area
A = 100 mm^2, characteristic length L = 10 mm, alpha = 100:

- k_pen = 100 * 200,000 * 100 / 10 = 2.0e8 N/mm.
- Applied bearing load F = 100 kN: penetration p = F / k_pen
  = 100,000 / 2.0e8 = 5.0e-4 mm, well under the 0.01 mm tolerance.
- Penalty force check: k_pen * p = 2.0e8 * 5.0e-4 = 100 kN, matching
  the applied load (equilibrium).
- Friction with mu = 0.2: f_max = 0.2 * 100 kN = 20 kN. A trial shear
  of 8 kN sticks (friction force 8 kN, no sliding); a trial shear of
  25 kN slips (friction force saturates at 20 kN).
- Lagrange on the same pair: penetration enforced to zero; the gap
  check reports enforced when the penetration is within 1e-9.


## Pitfalls

- Tuning only the penetration and ignoring conditioning: the penalty
  force F_n = k_pen * p depends on the user-chosen stiffness, and a
  stiffness raised far above the element scale (alpha of 10-1000)
  drives penetration down at the cost of ill-conditioning - the
  penalty method never gives exact zero penetration.
- Expecting zero penetration from the penalty method: penetration is
  always present and only Lagrange (or augmented Lagrange) enforces
  the constraint exactly; the worked 5.0e-4 mm penetration is under
  tolerance, not zero.
- Reading the gap sign backwards: node-to-surface gaps are signed
  along the master normal - negative is penetration, positive is
  separation - so a flipped sign turns a penetrating node into an
  open contact.
- Using the wrong friction branch: the interface sticks when the
  trial shear is below mu * |F_n| and slips when it reaches the cap;
  a high clamping load resists far more shear than the same joint
  unloaded in the normal direction, and the cap uses the absolute
  normal force.
- Mixing units at the interface: the module assumes N/mm (the worked
  bolt case uses E in N/mm^2 and A in mm^2); feeding SI Pa and m
  shifts the stiffness estimate by the unit ratio.
- Confusing contact with the global solve: this leaf computes
  contact quantities (forces, gaps, friction, tie checks); the
  nonlinear solver workflow that carries a contact run belongs to
  calculix-nonlinear.
## Related leaves

- structures/fem/calculix-linear: linear static stress and margin of
  safety checks downstream of the contact solution.
- structures/fem/calculix-nonlinear: nonlinear solver workflow where
  contact runs live.
- structures/fem/truss-analysis: simple element-level checks for the
  members the contact model connects.
- structures/composites/composite-bolted-joints: bolted joint strength
  evaluation that consumes bearing contact forces.

## Behavior contract (gate 3)

Run the deterministic contract test (stdlib unittest, offline):

    python3 scripts/test_contact_analysis.py

The test covers the penalty stiffness estimate, penalty force at zero
penetration and at finite penetration, Lagrange enforcement tolerance,
Coulomb stick and slip states, friction with zero and negative normal
force, penetration control convergence, node-to-surface signed gaps,
tie constraint tolerance, and invalid-input edge cases.

## Compliance

- Standards referenced, not reproduced: FAR-25 and CS-25 are public
  airworthiness regulations, named for certification context only;
  both resolve in standards-map.yaml with reference-only: true.
- compliance: STANDARDS-REF, gated: false.
