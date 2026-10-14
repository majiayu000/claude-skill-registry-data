---
name: flight-mechanics
description: "Use when a task concerns aircraft flight mechanics: guide the router to the flight-mechanics pack. breguet-range cruise range, breguet-endurance loiter endurance, specific-range cruise fuel economy, takeoff-performance takeoff distance, climb-performance rate of climb, oei-climb-gradient OEI climb gradient, energy-height specific excess power, descent-performance descent, turn-performance turn rate and load factor, glide-performance glide ratio and sink rate, wind-effects wind triangle and groundspeed, longitudinal-stability neutral point and static margin, lateral-directional-stability dihedral and Dutch roll, dynamic-stability short period and phugoid, trim-analysis stick trim, aileron-reversal control reversal speed. Trigger: flight mechanics, breguet range, loiter endurance, fuel flow, takeoff, rate of climb, OEI, engine out, energy height, specific excess power, descent, turn rate, glide ratio, sink rate, static margin, Dutch roll, phugoid, trim, aileron reversal."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: flight-mechanics
pack: flight-mechanics
compatibility: "agentskills.io SKILL.md; router/entry point for the flight-mechanics domain pack"
metadata:
  domain: flight-mechanics
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Flight mechanics domain pack (router)

Route here when the task is aircraft performance, range, endurance,
glide, takeoff, climb, descent, turn, or static and dynamic stability.

## Domain

Flight mechanics: cruise performance (Breguet range and endurance),
takeoff performance, climb and descent performance, turn performance,
glide performance, static longitudinal stability,
lateral-directional stability, and dynamic stability modes analysis.

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| flight-mechanics/performance/breguet-range | Breguet range | cruise range, TSFC, lift-to-drag, fuel fraction, cruise time |
| flight-mechanics/performance/propeller-range | Propeller range | propeller range, PSFC, power specific fuel consumption, propeller efficiency, turboprop range, fuel fraction |
| flight-mechanics/performance/breguet-endurance | Breguet endurance | loiter endurance, holding time, SFC, fuel burn, final weight |
| flight-mechanics/performance/specific-range | Specific air range | specific air range, fuel flow, instantaneous range, fuel burn per sector |
| flight-mechanics/performance/takeoff-performance | Takeoff performance | ground roll distance, lift-off speed, stall speed from wing loading |
| flight-mechanics/performance/landing-performance | Landing performance | landing distance, approach speed, flare, ground roll, stopping distance, reverse thrust, braking coefficient |
| flight-mechanics/performance/climb-performance | Climb performance | rate of climb, excess thrust, climb gradient, time to climb, service ceiling |
| flight-mechanics/performance/descent-performance | Descent performance | descent profiles, glide range, rate of descent, energy management, VNAV step-down planning |
| flight-mechanics/performance/turn-performance | Turn performance | turn rate, turn radius, bank angle, load factor, sustained turn |
| flight-mechanics/performance/glide-performance | Glide performance | glide ratio, descent angle, sink rate, time to descend, unpowered range |
| flight-mechanics/performance/wind-effects | Wind effects | headwind, tailwind, crosswind, wind correction angle, groundspeed, enroute time |
| flight-mechanics/stability-control/longitudinal-stability | Longitudinal stability | neutral point, static margin, pitch stability coefficient |
| flight-mechanics/stability-control/lateral-directional-stability | Lateral-directional stability | dihedral effect, directional stability, vertical tail volume, Dutch roll, roll mode, spiral mode |
| flight-mechanics/stability-control/dynamic-stability | Dynamic stability | short period, phugoid, Dutch roll, spiral, roll subsidence, stability derivatives, damping and frequency |
| flight-mechanics/stability-control/trim-analysis | Trim analysis | stick fixed trim, trim lift coefficient, elevator deflection, trim speed, pitching moment closure |
| flight-mechanics/performance/oei-climb-gradient | OEI climb gradient | OEI thrust, second segment, engine out, approach climb, landing climb gradient |
| flight-mechanics/performance/energy-height | Energy height | specific excess power, energy height, climb/cruise trade, Ps |
| flight-mechanics/stability-control/aileron-reversal | Aileron reversal | control reversal speed, reversal dynamic pressure, torsional stiffness |
| flight-mechanics/stability-control/control-surface-effectiveness | Control surface effectiveness | elevator authority, hinge moment, stick force, elevator deflection, tail volume coefficient, rotation authority |
| flight-mechanics/stability-control/spin-recovery | Spin recovery | spin recovery, autorotation, spin modes, flat spin, incipient spin, post stall departure, anti-spin controls |
| flight-mechanics/handling-qualities/cooper-harper-rating | Cooper-Harper rating | Cooper-Harper rating scale, pilot opinion, handling qualities level, adequate performance, desired tolerances, pilot compensation |
| flight-mechanics/handling-qualities/pilot-induced-oscillation | Pilot-induced oscillation | PIO category, phase lag at crossover, actuator rate limiting, pilot-in-the-loop coupling, phase compensation |
| flight-mechanics/performance/thrust-required | Thrust required | thrust required, power required, level flight drag polar, minimum drag speed, equivalent power |
| flight-mechanics/flight-dynamics-sim/six-dof-simulation | Six-DOF simulation | six degree of freedom, body axis equations of motion, Euler angle rates, quaternion, RK4 propagation, rigid body state |
| flight-mechanics/stability-control/stability-derivatives-avl | Stability derivative estimation | stability derivatives, lift curve slope, wing planform, aspect ratio, sweep effect, Mach correction, tail volume, neutral point, static margin, AVL-style estimation |
| flight-mechanics/stability-control/short-period-mode-analysis | Short-period mode analysis | short period mode, short-period, natural frequency, damping ratio, stability derivatives, flying qualities, level 1 |
| flight-mechanics/handling-qualities/mil-std-1797a | Mil Std 1797a | mil-std-1797a, flying qualities, handling qualities levels, short period damping, dutch roll, phugoid, spiral mode, roll mode, roll performance, flight phase category, aircraft class, cooper-harper band. |
| flight-mechanics/stability-control/phugoid-mode-analysis | Phugoid mode analysis | phugoid period, Lanchester approximation, long-period oscillation, time to half amplitude, airspeed oscillation |
| flight-mechanics/flight-dynamics-sim/point-mass-trajectory | Point-mass trajectory | point-mass trajectory, flight-path angle, RK4 integration, speed-altitude history, vertical-plane profile, climb path integration |
| flight-mechanics/performance/windshear-analysis | Windshear analysis | windshear, microburst, F-factor, downdraft, headwind shear, wind shear hazard, escape guidance, energy height loss, shear encounter |
| flight-mechanics/performance/speed-stability | Speed stability | speed stability, back side of the thrust required curve, region of reversed command, minimum drag speed boundary, trim speed classification, slow flight stability margin |
| flight-mechanics/stability-control/deep-stall-analysis | Deep stall analysis | deep stall, T-tail blanking, alpha lock, post-stall trim, tail blanking factor, separated flow pitch-up, pitch-down recovery authority |
| flight-mechanics/handling-qualities/pitch-bandwidth-criteria | Pitch bandwidth criteria | pitch bandwidth criterion, phase delay tau, bandwidth frequency, phase margin 45 degrees, MIL-STD-1797A bandwidth, short period transfer function, actuator lag, flying qualities level |
| flight-mechanics/performance/rotorcraft-hover-performance | Rotorcraft hover performance | rotorcraft hover, momentum theory, induced velocity, figure of merit, profile power, disk loading, rotor solidity, hover power |
| flight-mechanics/performance/rotorcraft-forward-flight-performance | Rotorcraft forward flight performance | rotorcraft forward flight, Glauert inflow, induced power, parasite power, equivalent flat plate area, best endurance speed, best range speed |
| flight-mechanics/performance/rotorcraft-vertical-climb-performance | Rotorcraft vertical climb performance | rotorcraft vertical climb, climb induced velocity, climb power, maximum vertical rate of climb, axial momentum theory |
| flight-mechanics/performance/rotorcraft-hover-ground-effect | Rotorcraft hover in ground effect | hover in ground effect, IGE induced power, ground effect factor, rotor height over radius, ige hover ceiling |
| flight-mechanics/performance/rotorcraft-tail-rotor-sizing | Rotorcraft tail rotor sizing | tail rotor, anti-torque rotor, main rotor torque, tail rotor thrust, tail rotor power, disk loading |
| flight-mechanics/performance/rotorcraft-blade-flapping-dynamics | Rotorcraft blade flapping dynamics | blade Lock number, hover coning angle, flap frequency ratio, rotor blade flapping, hinge offset, rotor dynamics |
| flight-mechanics/performance/rotorcraft-autorotative-descent | Rotorcraft autorotative descent | autorotative descent, power-off descent, minimum descent rate, rotor energy balance, engine failure descent |
| flight-mechanics/performance/rotorcraft-blade-element-hover-performance | Rotorcraft blade element hover performance | blade element theory, thrust coefficient, torque coefficient, collective pitch, tip loss factor, hover figure of merit |
| flight-mechanics/performance/rotorcraft-axial-descent-flow-states | Rotorcraft axial descent flow states | axial descent flow, vortex ring state, windmill brake state, descent induced velocity, torque reversal, momentum theory reachability |
| flight-mechanics/performance/rotorcraft-lead-lag-dynamics | Rotorcraft lead-lag dynamics | lead lag frequency, lag hinge offset, regressing lag mode, ground resonance clearance, coincidence rotor speed, multiblade modes |
| flight-mechanics/performance/balanced-field-length | Balanced field length | balanced field length, V1 decision speed, accelerate-stop distance, accelerate-go distance, engine-out field length |
| flight-mechanics/performance/rotorcraft-range-endurance | Rotorcraft range endurance | rotorcraft range endurance, hover endurance, cruise endurance, power required fuel closure, best range speed |
| flight-mechanics/performance/rotorcraft-turn-performance | Rotorcraft turn performance | rotorcraft turn performance, helicopter banked turn, turning flight inflow, sustained load factor, power limited bank angle, turn rate |
| flight-mechanics/performance/rotorcraft-main-rotor-sizing | Rotorcraft main rotor sizing | main-rotor disk loading ceiling, radius and solidity closure, ct-over-sigma design point, blade chord, tip Mach |
| flight-mechanics/performance/rotorcraft-forward-flight-flapping | Rotorcraft forward flight flapping | forward-flight-flapping, tip-path-plane-tilt, first-harmonic-flap-response, longitudinal-flapping-angle, lateral-flapping-angle, advance-ratio-flapping, flap-equilibrium-tilt |
| flight-mechanics/performance/rotorcraft-cyclic-pitch-trim | Rotorcraft cyclic pitch trim | rotorcraft-cyclic-pitch-trim, cyclic-pitch-control, tip-path-plane-tilt, trim-inversion, swashplate-cyclic-input, longitudinal-cyclic, lateral-cyclic |

## Routing guidance

- Cruise range and fuel-fraction questions route to the
  breguet-range sub-skill; loiter endurance and holding questions
  route to the breguet-endurance sub-skill; specific air range,
  fuel flow, and sector fuel burn questions route - Mil-std-1797a questions route to the handling-qualities mil-std-1797a sub-skill.
to the
  specific-range sub-skill.
- Propeller and turboprop cruise range questions (power-specific fuel
  consumption and propeller efficiency with the propeller Breguet
  range equation) route to the performance propeller-range sub-skill.
- Takeoff and ground-roll questions route to takeoff-performance.
- Landing distance, approach speed, flare, ground roll, and stopping
  distance questions route to the landing-performance sub-skill.
- Rate of climb, excess thrust, climb gradient, time to climb, and
  service ceiling questions route to the climb-performance sub-skill.
- Descent profile, glide-descent range, sink-rate, and energy
  management questions route to the descent-performance sub-skill.
- Turn rate, turn radius, bank angle, and sustained turn questions
  route to the turn-performance sub-skill.
- Glide ratio, descent angle, sink rate, and time-to-descend
  questions route to the glide-performance sub-skill.
- Headwind, crosswind, wind correction angle, groundspeed, and
  enroute time questions route to the wind-effects sub-skill.
- Neutral point, CG margin, and pitch stability questions route to
  the longitudinal-stability sub-skill.
- Dihedral effect, directional stability, Dutch roll, roll mode, and
  spiral mode questions route to the lateral-directional-stability
  sub-skill.
- Short period, phugoid, mode damping, and dynamic stability
  derivative questions route to the dynamic-stability sub-skill.
- Stick fixed trim, elevator deflection, trim speed, and pitching
  moment closure questions route to the trim-analysis sub-skill.
- Propulsion, structures, and certification questions route to their
  domain packs (propulsion, structures, avionics).

- One-engine-inoperative, second segment, approach climb, and landing climb gradient questions route to the oei-climb-gradient sub-skill.
- Energy height and specific excess power questions route to the performance energy-height sub-skill.
- Control reversal speed and reversal dynamic pressure questions route to the stability-control aileron-reversal sub-skill.
- Elevator authority, hinge moment, stick force, and takeoff rotation controllability questions route to the stability-control control-surface-effectiveness sub-skill.
- Spin entry, autorotation, spin modes, flat spin, incipient spin, and anti-spin recovery control questions route to the stability-control spin-recovery sub-skill.
- Cooper-Harper rating scale, pilot opinion ratings, handling qualities level, and pilot compensation assessment questions route to the handling-qualities cooper-harper-rating sub-skill.
- PIO category assessment, phase lag at crossover, actuator rate limiting, pilot-in-the-loop coupling, and phase compensation questions route to the handling-qualities pilot-induced-oscillation sub-skill.
- Thrust-required and power-required curves for level unaccelerated flight, minimum-drag speed, and the drag polar force balance route to the performance thrust-required sub-skill.
- Six-degree-of-freedom rigid body simulation, body-axis equations of motion, Euler angle integration, and RK4 propagation questions route to the flight-dynamics-sim six-dof-simulation sub-skill.
- Stability-derivative estimation from wing and tail geometry, lift curve slope with sweep and Mach corrections, and geometry-to-neutral-point questions route to the stability-control stability-derivatives-avl sub-skill.
- Short-period natural frequency and damping from stability derivatives, dimensionless derivative conversion, and Level 1 flying qualities checks route to the stability-control short-period-mode-analysis sub-skill.
- Windshear and microburst F-factor hazard, downdraft out-climb, energy height loss, and recovery thrust questions route to the performance windshear-analysis sub-skill.
- Rotorcraft hover performance questions (rotorcraft hover, momentum theory induced velocity, figure of merit, profile power, disk loading, rotor solidity) route to the performance rotorcraft-hover-performance sub-skill.
- Rotorcraft tail rotor and anti-torque questions (main rotor torque, tail rotor thrust, tail rotor radius, tail rotor power) route to the performance rotorcraft-tail-rotor-sizing sub-skill.
- Rotorcraft hover-in-ground-effect questions (ground effect factor, IGE induced power, ige-hover-ceiling, rotor height over radius) route to the performance rotorcraft-hover-ground-effect sub-skill.
- Rotorcraft vertical climb questions (vertical climb momentum theory, climb induced velocity, climb power required, maximum vertical rate of climb) route to the performance rotorcraft-vertical-climb-performance sub-skill.
- Rotorcraft forward flight questions (Glauert inflow, induced power, parasite power, equivalent flat plate area, best endurance speed, best range speed) route to the performance rotorcraft-forward-flight-performance sub-skill.
- Rotorcraft blade dynamics questions (blade Lock number, hover coning angle, flap frequency ratio, blade flapping, rotor dynamics) route to the performance rotorcraft-blade-flapping-dynamics sub-skill.
- Rotorcraft autorotative descent questions (power-off descent, minimum descent rate, rotor energy balance, engine failure descent) route to the performance rotorcraft-autorotative-descent sub-skill.

- Rotorcraft blade-element hover performance questions (thrust coefficient, torque coefficient, collective pitch, tip loss factor, hover figure of merit) route to the performance rotorcraft-blade-element-hover-performance sub-skill.
- Rotorcraft axial-descent flow-state questions (vortex-ring band, windmill-brake state, descent induced velocity, torque reversal) route to the performance rotorcraft-axial-descent-flow-states sub-skill.
- Rotorcraft lead-lag dynamics questions (lag frequency ratio, regressing lag mode, ground-resonance clearance, coincidence rotor speed) route to the performance rotorcraft-lead-lag-dynamics sub-skill.
- main-rotor disk loading ceiling, radius and solidity closure, ct-over-sigma design point, blade chord, tip Mach questions route to the performance rotorcraft-main-rotor-sizing sub-skill.
- Steady forward-flight rotor flapping questions (first-harmonic flap equilibrium, tip-path-plane tilt, longitudinal and lateral flapping angles vs advance ratio, flap-equilibrium tilt) route to the performance rotorcraft-forward-flight-flapping sub-skill; hover-state coning, Lock number and flap frequency ratio stay with rotorcraft-blade-flapping-dynamics.
- Rotorcraft cyclic trim questions (longitudinal and lateral cyclic pitch inputs, swashplate cyclic, cyclic required to hold a target tip-path-plane attitude, trim inversion) route to the performance rotorcraft-cyclic-pitch-trim sub-skill; collective-only flap equilibrium stays with rotorcraft-forward-flight-flapping.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- Phugoid period, damping, and time to half amplitude questions route to the stability-control phugoid-mode-analysis sub-skill.
- Point-mass climb trajectory and flight-path-angle history questions route to the flight-dynamics-sim point-mass-trajectory sub-skill.
- Speed stability, the back side of the thrust-required curve, the region of reversed command, and slow-flight trim stability questions route to the performance speed-stability sub-skill.
- Deep stall, T-tail blanking, alpha lock, and post-stall trim recovery questions route to the stability-control deep-stall-analysis sub-skill.
- Pitch bandwidth and phase-delay flying qualities criterion questions route to the handling-qualities pitch-bandwidth-criteria sub-skill.

- Balanced-field-length questions (V1 decision-speed balance between the accelerate-stop and the accelerate-go distance over the obstacle, engine-out field length) route to the performance balanced-field-length sub-skill.

- Rotorcraft fuel-closure questions (hover endurance from the weight-decay power integration, cruise range and endurance over the power-required curve, best-range speed pick) route to the performance rotorcraft-range-endurance sub-skill.

- Rotorcraft banked-turn questions (momentum-theory turning-flight inflow at n-times weight, banked-turn power breakdown, sustained load factor from available power, turn rate and radius) route to the performance rotorcraft-turn-performance sub-skill.
