---
name: panel-method
description: "Use when the task is panel method setup, source or doublet panels, Neumann or Dirichlet boundary conditions, Kutta condition enforcement, pressure distribution on an airfoil or fuselage, or potential flow over 3D bodies. Compute the surface pressure distribution and force coefficients for an airfoil or body in incompressible potential flow with a panel method: build panel geometry from a closed point list, assemble the source panel influence matrix for the Neumann boundary condition, assemble the doublet panel influence matrix for the Dirichlet boundary condition, solve the linear system, evaluate the surface velocity and pressure coefficient, integrate pressure for lift and drag, and apply the Kutta condition to fix trailing-edge circulation. Trigger: panel method, source panel, doublet panel, kutta condition, neumann boundary condition, dirichlet boundary condition, pressure coefficient, potential flow, 3d body."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: naca-tr-824
    reference-only: true
gated: false
domain: aerodynamics
pack: aerodynamics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: aerodynamics
  subdomain: cfd
  tags: [panel-method, source-panel, doublet-panel, vortex-panel, potential-flow, neumann-boundary-condition, dirichlet-boundary-condition, kutta-condition, pressure-coefficient, surface-velocity, incompressible-flow, 3d-body-aerodynamics, trailing-edge-circulation, sphere-validation]
  version: 0.1.0
  author: Aero Agent Skills
---

# Surface Panel Method (aerodynamics/cfd/panel-method)

Use when the task is a surface panel method for incompressible
potential flow: discretizing an airfoil or body into source or doublet
panels, applying the Neumann or Dirichlet boundary condition, enforcing
the Kutta condition, or computing the pressure distribution and force
coefficients.

## Domain quick reference

- Panel methods replace the body surface with flat panels carrying
  constant-strength singularities. Source panels model thickness and
  non-lifting bodies; doublet panels (or vortex panels) model lifting
  surfaces; the singularity strengths are the unknowns of a linear
  system assembled from influence coefficients.
- Neumann boundary condition (source panel method): the total velocity
  normal to the surface is zero at each control point (panel midpoint),
  sum_j A_ij sigma_j = -(V_inf dot n_i), with the source self-influence
  A_ii = 1/2. The source panel method reproduces the analytic cylinder
  pressure coefficient Cp = 1 - 4 sin^2(theta) to machine precision
  for an inscribed polygon.
- Dirichlet boundary condition (doublet panel method): the interior
  velocity potential is zero at each control point, sum_j D_ij mu_j =
  -phi_inf_i with D_ii = 1/2. The doublet strength equals the surface
  velocity potential, so the surface velocity is the surface derivative
  of the doublet distribution.
- Kutta condition: for a lifting body with a sharp trailing edge, the
  tangential velocities on the upper and lower trailing-edge panels
  must be equal, which fixes the circulation. Thin-airfoil theory gives
  the flat plate result Gamma = pi c V_inf sin(alpha), so
  c_l = 2 pi sin(alpha); the Kutta-Joukowski relation converts
  circulation to lift with c_l = 2 Gamma / (c V_inf).
- Pressure: the Bernoulli relation for incompressible potential flow
  gives Cp = 1 - (V/V_inf)^2. Integrating Cp times the panel outward
  normal over the closed surface yields the lift and drag coefficients;
  d'Alembert's paradox states the drag is zero in inviscid potential
  flow, so a symmetric body at zero angle of attack must show zero lift
  and near-zero drag.
- 3D bodies: the sphere is the standard validation anchor for 3D panel
  codes. Potential flow over a sphere gives Cp = 1 - (9/4) sin^2(theta)
  and the exact source strength 2 V_inf cos(theta). Quadrilateral
  surface panels need area, centroid, and unit normal checks.

## Workflow

1. Build the panel geometry with build_panels from a closed,
   counter-clockwise point list (first point equals last). Each panel
   gets its midpoint, length, outward normal, and tangent.
2. For a non-lifting body, assemble the influence matrix with
   source_influence_matrix and solve for the source strengths with
   neumann_source_solution, which applies the Neumann boundary
   condition at the control points.
3. For the Dirichlet form, assemble the doublet influence matrix with
   dirichlet_doublet_matrix and solve with dirichlet_doublet_solution,
   then recover the surface velocity with
   surface_velocity_from_doublets.
4. Evaluate the surface velocity and pressure coefficient with
   surface_velocity_and_cp, then integrate with force_coefficients for
   the lift and drag coefficients.
5. For lifting cases, apply the Kutta condition: check trailing-edge
   velocity equality with kutta_condition_check and estimate the
   circulation with flat_plate_circulation and cl_from_circulation.
6. For 3D bodies, check the panel bookkeeping with
   quad_panel_properties and validate against the sphere solution with
   sphere_potential_flow_cp and sphere_source_strength.
7. Solve any assembled system with solve_linear_system (Gaussian
   elimination with partial pivoting).

## Pitfalls

- Wrong boundary condition: the Neumann form works on velocities
  (zero normal velocity), the Dirichlet form works on potentials (zero
  interior potential); mixing the two assemblies produces a wrong
  system.
- Forgetting the doublet self-influence: the half-space solid angle
  D_ii = 1/2 is required for the Dirichlet matrix, and the source
  self-influence A_ii = 1/2 for the Neumann matrix.
- Computing the subtended panel angle from principal-value atan2
  differences: endpoint directions wrap at 180 degrees and break the
  influence matrix; use the signed cross and dot product angle instead.
- Ignoring the Kutta condition on a lifting airfoil: without it the
  circulation is undetermined and the lift is wrong.
- Treating potential-flow drag as physical: the panel method returns
  zero inviscid drag by construction (d'Alembert); viscous drag needs
  a boundary-layer or CFD treatment.
- Clockwise point ordering flips the normals inward and inverts the
  boundary condition signs; require a positive signed area.

## Behavior contract (gate 3)

The panel geometry, influence, boundary condition, Kutta, pressure, and
3D body logic is exercised by the gate 3 contract test:
scripts/test_panel_method.py against scripts/panel_method_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_panel_method.py

## Compliance

- NACA Report 824 is US government work (public domain); summary and
  reference data only, per standards-map.yaml. The panel method
  methodology here is common potential-flow practice, not reproduced
  text.
- compliance: STANDARDS-REF, gated: false.
