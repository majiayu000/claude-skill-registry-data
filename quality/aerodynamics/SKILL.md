---
name: aerodynamics
description: "Use when a task concerns aerodynamics: guide the router to the aerodynamics pack: airfoil-selection family choice, xfoil-analysis polars, airfoil-geometry NACA geometry, airfoil-optimization shape trade, cfd-convergence residuals, cfd-turbulence-modeling model selection, cfd-mesh-generation grids and y-plus, vortex-lattice-method VLM, panel-method potential flow, normal-shock shock relations, oblique-shock theta-beta-M, prandtl-meyer expansions, swept-wing-aerodynamics sweep, transonic-similarity Karman-Tsien, supercritical-airfoil aft loading, wave-drag-area-rule area rule, drag-polar polar, parasite-drag zero-lift drag, lift-curve-slope lift slope, boundary-layer-theory flat-plate layers, ground-effect in-ground lift, high-lift-systems flap and slat clmax. Trigger: aerodynamics, airfoil, polar, drag polar, sweep, Mach, boundary layer, ground effect, high lift, vortex lattice, panel method, transonic."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: naca-tr-824
    reference-only: true
gated: false
domain: aerodynamics
pack: aerodynamics
compatibility: "agentskills.io SKILL.md; router/entry point for the aerodynamics domain pack"
metadata:
  domain: aerodynamics
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Aerodynamics domain pack (router)

Route here when the task is aerodynamic analysis, airfoil selection,
compressible flow, or validation of section data.

## Domain

Aerodynamics and CFD: airfoil section selection, geometry, and
analysis with XFOIL, viscous-inviscid modeling, turbulence modeling,
compressible flow (normal and oblique shocks, Prandtl-Meyer
expansions), drag polar construction, and wing lift curve slope
estimation, validated against classic reference data.

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| aerodynamics/airfoil/airfoil-selection | Airfoil selection | airfoil family choice, design lift coefficient, thickness ratio, camber, section constraints |
| aerodynamics/airfoil/xfoil-analysis | XFOIL airfoil analysis | polar generation, viscous analysis, lift/drag coefficients, validation bands |
| aerodynamics/airfoil/airfoil-geometry | Airfoil geometry | NACA 4/5/6-series geometry, camber and thickness distribution, leading-edge radius, naming decode |
| aerodynamics/airfoil/airfoil-optimization | Airfoil optimization | shape trade studies, thickness/camber objectives, drag bucket, L/D targets |
| aerodynamics/boundary-layer/boundary-layer-theory | Boundary layer theory | flat-plate thickness, displacement and momentum thickness, skin friction, transition |
| aerodynamics/boundary-layer/unsteady-laminar-stokes-layers | Unsteady laminar Stokes layers | unsteady laminar stokes layers, stokes first problem, oscillating plate layer, rayleigh layer |
| aerodynamics/cfd/cfd-convergence | CFD convergence | residual convergence, Courant number, mesh refinement, solver stability |
| aerodynamics/cfd/cfd-turbulence-modeling | Turbulence modeling | turbulence model selection, Reynolds number, near-wall treatment, y-plus |
| aerodynamics/cfd/cfd-mesh-generation | CFD mesh generation | grid types, structured/unstructured/hybrid, prism layers, cell quality, first cell height, y-plus target, domain sizing |
| aerodynamics/cfd/vortex-lattice-method | Vortex lattice method | horseshoe vortices, panel lattice, lift distribution, downwash, induced drag |
| aerodynamics/cfd/panel-method | Panel method | source/doublet panels, Neumann/Dirichlet boundary conditions, pressure distribution, potential flow |
| aerodynamics/drag-polars/drag-polar | Drag polar | parabolic polar CD0 + k, Oswald span efficiency, induced drag, maximum lift-to-drag |
| aerodynamics/drag-polars/parasite-drag | Parasite drag | zero-lift drag buildup, wetted-area method, flat-plate skin friction, form and interference factors, equivalent skin-friction coefficient |
| aerodynamics/drag-polars/lift-curve-slope | Lift curve slope | thin-airfoil 2pi, finite-aspect-ratio correction, sweep correction, Prandtl-Glauert Mach correction, lift coefficient from angle of attack |
| aerodynamics/ground-effects/ground-effect | Ground effect | in-ground-effect lift and drag, height-to-span ratio, takeoff and landing performance |
| aerodynamics/high-lift/high-lift-systems | High-lift systems | trailing-edge flaps, leading-edge devices, flap clmax increment, slat increment, wing CLmax, stall speed |
| aerodynamics/high-speed/normal-shock | Normal shock relations | downstream Mach, pressure/density/temperature ratios, stagnation pressure loss, supersonic flow |
| aerodynamics/high-speed/oblique-shock | Oblique shock relations | theta-beta-M solution, deflection limits, weak/strong solutions, pressure ratio across shock |
| aerodynamics/high-speed/prandtl-meyer | Prandtl-Meyer expansion | expansion angle, downstream Mach after turning, total-to-static ratios, expansion fan |
| aerodynamics/high-speed/swept-wing-aerodynamics | Swept wing aerodynamics | leading edge sweep, simple sweep theory, critical Mach increase, effective Mach |
| aerodynamics/high-speed/transonic-similarity | Transonic similarity | Karman-Tsien correction, critical Mach number, compressibility correction |
| aerodynamics/high-speed/supercritical-airfoil | Supercritical airfoil | aft loading, flat upper surface, wave drag reduction, drag divergence Mach |
| aerodynamics/high-speed/wave-drag-area-rule | Wave drag and area rule | transonic wave drag, cross-sectional area distribution, Sears-Haack body, area rule |
| aerodynamics/wing-design/wing-planform-design | Wing planform design | root chord, tip chord, mean aerodynamic chord, taper ratio, spanwise loading, washout |
| aerodynamics/wing-design/winglet-design | Winglet design | winglet design, wingtip device, induced drag reduction, effective aspect ratio, span efficiency, cant angle, root bending moment penalty, winglet height |
| aerodynamics/aeroelasticity/divergence-speed | Divergence speed | divergence dynamic pressure, torsional stiffness, shear center offset, aerodynamic center, divergence margin, dive speed |
| aerodynamics/wind-tunnel/windtunnel-data-reduction | Wind tunnel data reduction | wind tunnel data reduction, tare correction, blockage correction, wall interference, Reynolds correction, aerodynamic coefficients, pressure distribution, balance data, uncertainty estimation, experimental aerodynamics |
| aerodynamics/aeroelasticity/flutter-speed-prediction | Flutter speed prediction | flutter speed, v-g method, bending torsion, typical section, damping crossing, frequency coalescence, flutter margin, theodorsen |
| aerodynamics/cfd/cfd-validation | Cfd Validation | cfd validation, validation case selection, richardson extrapolation, grid convergence, naca 0012 drag, onera m6, dlr f6, error metrics, validation uncertainty, validation report. |
| aerodynamics/wind-tunnel/windtunnel-wall-corrections | Wind tunnel wall corrections | wall corrections, solid blockage, wake blockage, lift interference, test section constraint, corrected drag |
| aerodynamics/aeroelasticity/aeroelastic-gust-response | Aeroelastic gust response | aeroelastic gust response, dynamic gust response, Kussner function, Wagner function, indicial aerodynamics, dynamic magnification factor |
| aerodynamics/high-speed/shock-expansion-airfoil | Shock-expansion airfoil | shock expansion, supersonic airfoil, diamond airfoil, double wedge, surface pressure integration, wave drag coefficient |
| aerodynamics/high-speed/hypersonic-flow | Hypersonic flow | hypersonic flow, modified Newtonian theory, Newtonian impact pressure, stagnation pressure coefficient, blunt body drag, cone axial force |
| aerodynamics/wind-tunnel/wind-tunnel-model-design | Wind tunnel model design | wind tunnel model design, model scale selection, blockage ratio, Reynolds mismatch, force balance rating, sting sizing |
| aerodynamics/high-speed/aerodynamic-heating | Aerodynamic heating | aerodynamic heating, stagnation point heating, Sutton-Graves, radiation equilibrium temperature, nose radius, hypersonic heat flux |
| aerodynamics/boundary-layer/boundary-layer-transition | Boundary layer transition | boundary layer transition, transition location, Thwaites integral, Michel criterion, natural transition, momentum thickness Reynolds number |
| aerodynamics/cfd/delta-wing-vortex-lift | Delta-wing vortex lift | delta wing vortex lift, leading edge suction analogy, slender delta wing, Polhamus, vortex lift split, drag due to lift |
| aerodynamics/boundary-layer/boundary-layer-separation | Boundary layer separation | boundary layer separation, Thwaites lambda criterion, Stratford separation criterion, laminar separation point, turbulent separation station, separation margin, adverse pressure gradient |
| aerodynamics/high-speed/flat-plate-skin-friction-heating | Flat plate skin friction heating | flat plate skin friction heating, recovery factor, adiabatic wall temperature, cold wall heat flux, reference temperature method, Reynolds analogy factor, non-stagnation heating |
| aerodynamics/high-speed/bow-shock-standoff | Bow shock standoff | bow shock standoff, Billig correlation, blunt body shock distance, shock layer thickness, stagnation streamline standoff |
| aerodynamics/boundary-layer/rough-wall-skin-friction | Rough wall skin friction | rough wall skin friction, sand roughness, fully rough regime, roughness trip, skin friction regime |
| aerodynamics/boundary-layer/stagnation-flow-boundary-layer | Stagnation flow boundary layer | stagnation flow boundary layer, Hiemenz, Homann, stagnation velocity gradient, stagnation point wall shear, leading edge boundary layer |
| aerodynamics/high-speed/isentropic-flow-relations | Isentropic flow relations | isentropic flow relations, total to static ratio, area Mach relation, Mach from area ratio, choked mass flow, sonic throat |
| aerodynamics/high-speed/regular-shock-reflection | Regular shock reflection | regular shock reflection, reflected shock, shock impingement on a wall, Mach reflection, two shock interaction |
| aerodynamics/high-speed/shock-tube | Shock tube | shock-tube diaphragm pressure ratio, incident-shock Mach number, contact-surface velocity, expansion fan |
| aerodynamics/airfoil/thin-airfoil-section-theory | Thin airfoil section theory | camber-line glauert sine series, zero-lift angle, quarter-chord pitching moment, section lift coefficient |
| aerodynamics/high-speed/compressible-couette-flow | Compressible Couette flow | shear-driven high-Mach plate gap, Crocco energy integral, recovery factor, wall shear and heat flux |
| aerodynamics/high-speed/fanno-flow | Fanno flow | fanno flow, fanno line, friction duct choking, fL star over D, adiabatic duct friction |
| aerodynamics/high-speed/rayleigh-flow | Rayleigh flow | rayleigh flow, heat addition duct, thermal choking, rayleigh line |

| aerodynamics/high-speed/ackeret-linearized-supersonic | Ackeret linearized supersonic | ackeret linearized supersonic theory, biconvex airfoil, linear supersonic lift curve slope, supersonic wave drag, thin airfoil supersonic |
| aerodynamics/high-speed/hypersonic-piston-theory | Hypersonic piston theory | hypersonic piston theory, Lighthill piston, small perturbation hypersonic, unsteady hypersonic surface pressure, piston theory surface pressure |
| aerodynamics/aeroelasticity/added-mass-coefficients-potential-flow | Added mass coefficients potential flow | added mass coefficients, virtual mass, apparent mass, acceleration reaction, kinetic energy irrotational flow, added mass catalog |
| aerodynamics/boundary-layer/stokes-creeping-flow-drag | Stokes creeping flow drag | stokes creeping flow drag, creeping flow sphere, stokes drag law, Oseen correction, terminal velocity settling, low Reynolds body drag |

| aerodynamics/aeroelasticity/sears-function-gust-lift | Sears Function Gust Lift | sears-function, sinusoidal-gust, unsteady-gust-load, gust-transfer-function, reduced-frequency-gust |
| aerodynamics/boundary-layer/squire-young-profile-drag | Squire Young Profile Drag | squire-young-profile-drag, squire-young-formula, profile-drag-coefficient, trailing-edge-momentum-thickness, laminar-profile-drag, momentum-integral-drag |
| aerodynamics/boundary-layer/laminar-far-wake | Laminar Far Wake | laminar-far-wake, far-wake-velocity-defect, wake-momentum-integral, velocity-defect-profile, wake-survey-drag |
| aerodynamics/boundary-layer/mangler-axisymmetric-transform | Mangler Axisymmetric Transform | mangler-transformation, cone-boundary-layer, axisymmetric-body-boundary-layer, laminar-cone-factor, body-of-revolution-bl |
## Routing guidance

- Airfoil family and section constraint questions route to the
  airfoil-selection sub-skill; XFOIL runs and polar validation route
  to xfoil-analysis; NACA geometry and naming questions route to
  airfoil-geometry; shape trade and - Cfd validation questions route to the cfd cfd-validation sub-skill.
objective studies route to
  airfoil-optimization.
- CFD solver-convergence questions (residuals, Courant, mesh
  refinement) route to cfd-convergence; turbulence model and
  near-wall questions route to cfd-turbulence-modeling; grid type,
  prism layer, and first-cell-height questions route to
  cfd-mesh-generation; potential-flow and lift-distribution methods
  route to vortex-lattice-method and panel-method.
- Compressible-flow questions (Mach number, normal shock relations,
  stagnation pressure loss) route to the high-speed normal-shock
  sub-skill; oblique shock and turning questions (theta-beta-M,
  deflection angle, weak/strong solution) route to oblique-shock;
  expansion-fan questions (Prandtl-Meyer angle, downstream Mach)
  route to prandtl-meyer.
- Sweep, transonic scaling, wave drag, and critical Mach questions
  route to swept-wing-aerodynamics, transonic-similarity,
  supercritical-airfoil, and wave-drag-area-rule.
- Drag polar construction and peak lift-to-drag questions route to
  the drag-polars drag-polar sub-skill; zero-lift drag buildup and
  wetted-area parasite drag questions route to parasite-drag; wing
  lift curve slope questions (thin airfoil, aspect ratio, sweep, Mach
  correction) route to lift-curve-slope.
- Boundary layer thickness, transition, and skin friction questions
  route to boundary-layer-theory; in-ground-effect performance
  questions route to ground-effect; flap and slat clmax and stall
  speed questions route to high-lift-systems.
- Wing planform reference geometry, root and tip chord, mean aerodynamic chord, taper ratio, and spanwise loading questions route to the wing-design wing-planform-design sub-skill.
- Divergence dynamic pressure, torsional stiffness, aerodynamic center offset, and divergence margin questions route to the aeroelasticity divergence-speed sub-skill.
- Structural, control, and certification questions route to their
  domain packs (structures, gnc-autonomy, avionics).
- Wind tunnel test data reduction, tare, blockage, and wall interference corrections, and coefficient uncertainty estimation route to the wind-tunnel windtunnel-data-reduction sub-skill.
- Classical wing flutter of the two-DOF typical section, the V-g method, structural damping crossing, frequency coalescence, and flutter margin questions route to the aeroelasticity flutter-speed-prediction sub-skill.
- Hypersonic flow questions (hypersonic flow, modified newtonian theory, newtonian impact pressure, stagnation pressure coefficient, blunt body drag, cone axial force) route to the hypersonic-flow sub-skill.
- Wind tunnel model design questions (wind tunnel model design, model scale selection, blockage ratio, reynolds mismatch, force balance rating, sting sizing) route to the wind-tunnel-model-design sub-skill.
- Hypersonic stagnation heating questions (aerodynamic heating, Sutton-Graves heat flux, radiation equilibrium temperature, nose radius bluntness) route to the high-speed aerodynamic-heating sub-skill.
- Laminar-turbulent transition location questions (transition location, Thwaites integral, Michel criterion, natural transition) route to the boundary-layer boundary-layer-transition sub-skill.

- Delta-wing vortex-lift questions (leading edge suction analogy, slender delta wing, Polhamus vortex lift) route to the cfd delta-wing-vortex-lift sub-skill.
- Boundary-layer separation questions (Thwaites lambda criterion crossing minus 0.09, Stratford pressure-recovery criterion, laminar separation point, turbulent separation station, separation margin) route to the boundary-layer boundary-layer-separation sub-skill.
- Profile-drag questions (Squire-Young formula from the trailing-edge momentum thickness and edge-velocity ratio, laminar profile drag from the integral growth chain, Blasius flat-plate reduction) route to the boundary-layer squire-young-profile-drag sub-skill.
- Flat-plate surface skin heating questions (recovery factor, adiabatic wall temperature, cold wall heat flux, reference temperature method skin friction, non-stagnation heating) route to the high-speed flat-plate-skin-friction-heating sub-skill.
- shock-tube diaphragm pressure ratio, incident-shock Mach number, contact-surface velocity, expansion fan questions route to the high-speed shock-tube sub-skill.
- camber-line glauert sine series, zero-lift angle, quarter-chord pitching moment, section lift coefficient questions route to the airfoil thin-airfoil-section-theory sub-skill.
- shear-driven high-Mach plate gap, Crocco energy integral, recovery factor, wall shear and heat flux questions route to the high-speed compressible-couette-flow sub-skill.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- Wind tunnel wall and blockage correction questions route to the wind-tunnel windtunnel-wall-corrections sub-skill.
- Dynamic indicial gust response and magnification-factor questions route to the aeroelasticity aeroelastic-gust-response sub-skill.
- Frequency-domain gust questions (Sears function gain and phase versus reduced frequency, sinusoidal-gust unsteady lift on the rigid airfoil, gust-load amplitude against the quasi-steady reference) route to the aeroelasticity sears-function-gust-lift sub-skill; discrete-gust time-domain response stays with aeroelastic-gust-response.
- Shock-expansion surface-pressure integration and wave-drag questions route to the high-speed shock-expansion-airfoil sub-skill.
- Winglet sizing, tip-device induced-drag reduction, effective-aspect-ratio gain, and root bending moment penalty questions route to the wing-design winglet-design sub-skill.
- Blunt-nose detached bow-shock standoff questions (standoff ratio and shock-layer thickness on the stagnation streamline for sphere and cylinder noses from the Billig-form correlations) route to the high-speed bow-shock-standoff sub-skill.

- Rough-surface skin friction questions (sand-roughness regime classification, fully-rough turbulent skin friction, roughness trip criterion) route to the boundary-layer rough-wall-skin-friction sub-skill.

- Low-speed stagnation-point boundary layer questions (Hiemenz 2-D and Homann axisymmetric similarity, stagnation velocity gradient from body radius, wall shear and skin friction at a spinner, radome or leading edge) route to the boundary-layer stagnation-flow-boundary-layer sub-skill.
- Axisymmetric boundary-layer questions (Mangler transformation to an equivalent 2-D flow, sharp-cone thickness and wall-shear ratios against the flat plate, slender body-of-revolution laminar layer) route to the boundary-layer mangler-axisymmetric-transform sub-skill.
- Isentropic flow relation questions (total to static ratios from Mach number, Mach from a given area ratio on the subsonic or supersonic branch, choked mass flow at a sonic throat) route to the high-speed isentropic-flow-relations sub-skill.
- Shock-reflection questions (incident oblique shock impinging on a wall or symmetry plane, reflected shock turning the flow back parallel, regular versus Mach reflection verdict from the detachment limit) route to the high-speed regular-shock-reflection sub-skill.
- Fanno flow questions (adiabatic constant-area duct with friction, fL star over D integral, choking length, downstream Mach from a given friction length) route to the high-speed fanno-flow sub-skill.
- Rayleigh flow questions (constant-area frictionless duct with heat addition, thermal choking, maximum heat addition, rayleigh-line ratios) route to the high-speed rayleigh-flow sub-skill.
- Linearized supersonic thin-airfoil questions (Ackeret pressure coefficient, biconvex wave drag, supersonic lift curve slope) route to high-speed ackeret-linearized-supersonic; Lighthill piston-theory surface pressure (small-perturbation unsteady hypersonic surfaces) routes to high-speed hypersonic-piston-theory; added/virtual mass coefficient questions (accelerating bodies in inviscid flow) route to aeroelasticity added-mass-coefficients-potential-flow; steady low-Reynolds creeping flow sphere drag (Stokes drag, Oseen correction, terminal velocity) routes to boundary-layer stokes-creeping-flow-drag.
- Unsteady laminar Stokes layer questions (impulsively started plate, oscillating plate penetration depth, Stokes first and second problem velocity profiles and wall shear) route to the boundary-layer unsteady-laminar-stokes-layers sub-skill.
- Laminar far-wake questions (Goldstein similarity wake behind a flat plate, centerline defect decay, wake half-width growth, wake-momentum-integral drag from a velocity-defect traverse) route to the boundary-layer laminar-far-wake sub-skill.
