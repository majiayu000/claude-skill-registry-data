---
name: truss-analysis
description: "Use when a truss model must be solved by hand or in a stdlib-only environment without FEA software. Compute the response of a 2D pin-jointed truss with the direct stiffness method: build each element stiffness matrix from E, A, L and orientation, assemble the global stiffness matrix, apply support conditions, solve the nodal displacements by Gaussian elimination, then recover member axial forces and support reactions. Units are SI. Trigger: truss analysis, direct stiffness method, element stiffness matrix, global stiffness matrix, nodal displacements, member forces, reaction forces, Gaussian elimination, pin-jointed, support conditions."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: mmpsd
    reference-only: true
gated: false
domain: structures
pack: structures
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: structures
  subdomain: fem
  tags: [truss-analysis, direct-stiffness-method, nodal-displacements, member-forces, gaussian-elimination, element-stiffness-matrix, global-stiffness-matrix, support-conditions, reaction-forces, plane-truss]
  version: 0.1.0
  author: Aero Agent Skills
---

# Truss Analysis (structures/fem/truss-analysis)

Use when the task is a 2D pin-jointed (plane) truss solve with the
direct stiffness method: building the element stiffness matrix of
each bar from E, A, L and its orientation, assembling the global
stiffness matrix, applying the support conditions, solving the nodal
displacements by Gaussian elimination, and recovering member axial
forces and support reactions. The logic module is pure Python
standard library (no numpy); the dense linear solve is implemented
here. Units are SI: coordinates in m, E in Pa, A in m^2, forces in N,
displacements in m.

## Domain quick reference

- A pin-jointed truss bar carries only axial load. With direction
  cosines c = cos(theta), s = sin(theta) of the bar axis (measured
  counterclockwise from global +x), the 4x4 element stiffness matrix
  in global coordinates, over degrees of freedom
  [u_xi, u_yi, u_xj, u_yj], is

      k = (E A / L) * [[ c^2,  c s, -c^2, -c s],
                       [ c s,  s^2, -c s, -s^2],
                       [-c^2, -c s,  c^2,  c s],
                       [-c s, -s^2,  c s,  s^2]]

- Global assembly: each element scatters into the global K of size
  2N x 2N over dofs [2i, 2i+1, 2j, 2j+1] (0-based node indices), so
  the global displacement vector is
  [u_x0, u_y0, u_x1, u_y1, ...].
- Support conditions: remove every constrained dof, solve the reduced
  system K_red u_free = F_red by Gaussian elimination with partial
  pivoting, then expand back (constrained entries stay 0).
- Member axial force, tension positive:
  F = (E A / L) * ((u_xj - u_xi) c + (u_yj - u_yi) s).
- Reaction at a constrained dof d: R_d = sum_c K[d][c] u_c, the
  force the support exerts on the structure, positive along +x/+y.

Worked example (verified by running scripts/truss_analysis_logic.py):
the symmetric three-bar truss with nodes (0,0), (4,3), (8,0) m, bars
0-1, 1-2 and 0-2 of E = 200 GPa, A = 1e-3 m^2, a downward load of
100 kN at the apex node 1, a pin at node 0 (x and y fixed) and a
vertical roller at node 2 (y fixed) gives

    displacements: [0, 0, 1.3333e-3, -5.25e-3, 2.6667e-3, 0] m
    member forces: [-83.333e3, -83.333e3, +66.667e3] N
    reactions:     R_0x = 0, R_0y = +50e3 N, R_2y = +50e3 N

The two inclined bars are in compression (83.3 kN each), the bottom
chord carries 66.7 kN tension, and the vertical reactions split the
100 kN load evenly. The same two bars without the bottom chord, pin
plus vertical roller, is a mechanism: K_red is singular and the
solve raises ValueError.

## Workflow

1. List the nodes as (x, y) coordinates in m; the list position is
   the 0-based node index.
2. List the elements as (i, j, E, A): 0-based node indices, Young's
   modulus in Pa, cross-section area in m^2.
3. List the loads as {(node, axis): force} with axis 'x' or 'y'
   (positive along +x/+y) and the supports as [(node, axis)] pairs to
   fix to zero displacement.
4. Check determinacy first: m bars + r support reactions >= 2 j
   nodes is necessary for stability; a singular solve later means a
   mechanism.
5. Solve the whole model with truss_analysis(nodes, elements, loads,
   constraints), which returns displacements, member_forces and
   reactions in one dict.
6. Or step through the method: element_stiffness_matrix(E, A, L,
   theta_deg) per bar, assemble_global_stiffness(nodes, elements),
   solve_displacements(K, F, constraints), member_forces(nodes,
   elements, displacements), reaction_forces(nodes, elements,
   displacements, constraints).
7. Sanity check: the sum of all reactions plus all applied loads must
   be zero in both directions (global equilibrium).

## Pitfalls

- Confusing truss-analysis with fem/modal-analysis: modal-analysis
  computes natural frequencies and mode shapes of 2-DOF mass-spring
  systems (eigenvalue problem); truss-analysis is static, has no
  masses and never solves an eigenvalue problem.
- Confusing truss-analysis with fem/calculix-linear: calculix-linear
  drives continuum FEA in CalculiX (ccx) with element-basis stress
  checks and margins of safety; truss-analysis is a hand-scale 2D
  bar solve with its own Gaussian elimination and no FEA software.
- Confusing truss-analysis with the vehicle-design
  structures-integration wing-box-sizing leaf: wing-box-sizing sizes
  spars, stringers and covers of a transport wing box under bending
  and torsion; truss-analysis only solves pin-jointed bar models.
- Picking an unstable support set: a two-bar V arch with a vertical
  roller is a mechanism (m + r = 5 < 2 j = 6); the reduced system is
  singular and solve_displacements raises ValueError. Add a third
  bar or a second horizontal reaction to stabilize it.
- Mixing up the sign conventions: member force positive means
  tension and negative means compression; reactions are the force the
  support exerts on the structure, positive along the +x/+y axes.
- Using 1-based node numbers or a different dof ordering: indices are
  0-based and the dof of (node, axis) is 2*node + (0 for 'x', 1 for
  'y').
- Mixing units: everything is SI (m, Pa, m^2, N, m of displacement);
  feeding mm^2 for A with Pa for E scales every stiffness by 1e6 and
  corrupts the displacements.
- Forgetting that adding a bar changes the load path: with the bottom
  chord present the apex drops 5.25 mm and the chord takes 66.7 kN
  tension; without it the structure is a mechanism. Always recheck
  determinacy when the model changes.

## Behavior contract (gate 3)

The truss logic is exercised by the gate 3 contract test:
scripts/test_truss_analysis.py against
scripts/truss_analysis_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_truss_analysis.py

## Compliance

- FAR-25 and MMPDS are referenced, not reproduced: standards-map.yaml
  marks them gated: false and reference-only: true; only the summary
  paraphrase above is used, never standard text.
- compliance: STANDARDS-REF, gated: false.
