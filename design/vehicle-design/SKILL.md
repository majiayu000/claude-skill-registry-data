---
name: vehicle-design
description: "Use when a task concerns aircraft or vehicle conceptual design and sizing: guide the router to the vehicle-design pack: tow-estimation takeoff gross weight, weight-estimation class-I weights, payload-range-diagram payload-range trade, fuselage-sizing cabin layout, tail-sizing tail volume coefficients, landing-gear-sizing strut loads, ws-tw-trade wing loading and thrust-to-weight, fuel-tank-sizing fuel volume and ullage, inertia-estimation moments of inertia, cg-envelope static margin, mass-budget mass rollup and growth allowance, wing-box-sizing spar sizing, fuselage-skin-stringer panel sizing, parametric-cost CERs, operating-cost DOC, life-cycle-cost LCC and learning curves. Trigger: vehicle design, sizing, weight estimation, takeoff gross weight, payload range, fuselage, tail volume, landing gear, strut loads, wing loading, thrust to weight, fuel tank, cg envelope, static margin, mass budget, growth allowance, wing box, spar, skin stringer, parametric cost, direct operating cost, life cycle cost, LCC."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: vehicle-design
pack: vehicle-design
compatibility: "agentskills.io SKILL.md; router/entry point for the vehicle-design domain pack"
metadata:
  domain: vehicle-design
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Vehicle design domain pack (router)

Route here when the task is aircraft or vehicle conceptual design,
sizing, mass properties, or cost estimation.

## Domain

Vehicle design and integration: class-I weight estimation, takeoff
gross weight estimation, fuselage and empennage sizing, landing gear
sizing, wing loading and thrust to weight matching, mass properties
(moments of inertia, CG envelope), and cost estimation (parametric
CERs, life cycle cost), tied to the sizing loop that brings
aerodynamic, structural, and performance disciplines together.

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| vehicle-design/conceptual/tow-estimation | Takeoff gross weight estimation | fuel-fraction method, empty-weight fraction, sizing iteration |
| vehicle-design/conceptual/payload-range-diagram | Payload-range diagram | payload vs range trade, max payload, max fuel, design range, ferry range, Breguet range, reserve fuel |
| vehicle-design/sizing/weight-estimation | Weight estimation | class-I weights, weight and balance sheets, component weights |
| vehicle-design/sizing/component-weight-estimation | Component weight estimation | component-weight-estimation, class-II-weight-estimation, airframe-group-weights, statistical-weight-regression, raymer-group-weight, group-weight-summary |
| vehicle-design/sizing/landing-gear-weight-estimation | Landing gear weight estimation | landing-gear-weight-estimation, class-II-gear-group-weight, gear-group-mass-regression, design-landing-weight, ultimate-landing-load-factor |
| vehicle-design/sizing/fuel-system-weight-estimation | Fuel system weight estimation | fuel-system-weight-estimation, class-II-fuel-system-group-weight, tankage-plumbing-pumps-mass, fuel-system-hardware-mass, fuel-weight-regression |
| vehicle-design/sizing/fuselage-sizing | Fuselage sizing | cabin length and width, fuselage diameter, L/D band, cargo volume check |
| vehicle-design/sizing/tail-sizing | Tail sizing | horizontal and vertical tail volume coefficients, required tail area, tail arm |
| vehicle-design/sizing/control-surface-sizing | Control surface sizing | aileron and elevator and rudder area from control power, roll rate requirement, pitch moment requirement, yaw moment requirement, hinge moment, deflection limits |
| vehicle-design/sizing/landing-gear-sizing | Landing gear sizing | strut load distribution, nose/main gear loads from CG and wheelbase, shock absorber stroke |
| vehicle-design/sizing/ws-tw-trade | W/S and T/W matching | wing loading, thrust-to-weight, matching chart, takeoff/climb/cruise constraints |
| vehicle-design/sizing/wing-planform-sizing | Wing planform sizing | wing area from wing loading and takeoff gross weight, aspect ratio and span, taper ratio and mean aerodynamic chord, sweep angle from cruise Mach |
| vehicle-design/sizing/engine-sizing | Engine sizing | sea-level static thrust, thrust lapse with altitude, takeoff thrust, top-of-climb margin, SFC fuel flow, engine weight |
| vehicle-design/sizing/fuel-tank-sizing | Fuel tank sizing | fuel volume from fuel mass, ullage allowance, required tank volume, wing/fuselage tank capacity fit |
| vehicle-design/mass-properties/inertia-estimation | Inertia estimation | moments of inertia, radius of gyration, parallel axis theorem |
| vehicle-design/mass-properties/cg-envelope | CG envelope | forward and aft limits, static margin from neutral point, envelope polygon, cg excursion with fuel burn |
| vehicle-design/mass-properties/mass-budget | Mass budget | subsystem masses, growth allowance, contingency margin, rollup, MTOW target check |
| vehicle-design/cost-estimation/parametric-cost | Parametric cost | CER, development cost, learning curve, unit cost, program cost |
| vehicle-design/cost-estimation/operating-cost | Operating cost | direct operating cost, block fuel cost, crew cost, maintenance cost, insurance, cost per flight hour |
| vehicle-design/cost-estimation/life-cycle-cost | Life cycle cost | LCC phases, power-law CERs, learning curve Nth unit, present value, inflation, uncertainty |
| vehicle-design/structures-integration/wing-box-sizing | Wing box sizing | root bending moment, spar cap area, shear flow, ultimate load, factor of safety |
| vehicle-design/structures-integration/fuselage-skin-stringer | Fuselage skin-stringer panel | skin thickness, hoop and longitudinal stress, stringer spacing, frame pitch, panel buckling |
| vehicle-design/mdo/multidisciplinary-optimization | Multidisciplinary optimization | MDO, design variables, objective function, constraints, discipline coupling, aero-structural loop, fixed point iteration, design space search |
| vehicle-design/sizing/propeller-sizing | Propeller sizing | propeller diameter, blade count, solidity, activity factor, disk loading, advance ratio, ground clearance |
| vehicle-design/sizing/tire-sizing | Tire sizing | tire diameter, tire width, static load per tire, gear load share, tire pressure, footprint |
| vehicle-design/conceptual/constraint-analysis | Constraint analysis | matching chart, thrust to weight ratio, wing loading, stall constraint, climb gradient, takeoff distance, feasible region |
| vehicle-design/conceptual/openvsp-geometry | Parametric aircraft geometry | parametric geometry, OpenVSP style, wing planform, mean aerodynamic chord, wetted area, fuselage geometry, component volume, sweep dihedral twist, mass properties input, conceptual design |
| vehicle-design/sizing/nacelle-sizing | Nacelle sizing | nacelle sizing, highlight area, fan mass flow, inlet capture, lip area, nacelle length, wetted area, cowl thickness |
| vehicle-design/conceptual/sizing-mission-profile | Sizing Mission Profile | mission profile, block fuel, block time, breguet range, breguet endurance, reserve fuel, loiter, hold, fuel fraction, required fuel, climb, cruise, descent, taxi, takeoff, FAR 121, payload range. |
| vehicle-design/mdo/design-of-experiments | Design of experiments | design of experiments, DOE, factorial design, latin hypercube, central composite, main effects |
| vehicle-design/sizing/ice-protection-sizing | Ice protection sizing | ice protection, anti-ice, de-ice, evaporative anti-icing, running wet, catch efficiency, protected area, heat flux, bleed air mass flow, electrothermal power, freezing fraction, MVD, liquid water content, Appendix C |
| vehicle-design/sizing/spoiler-sizing | Spoiler sizing | spoiler sizing, flight spoiler, ground spoiler, lift dump, speed brake, roll spoiler, roll assist share, spoiler panel area, lift dumper, spoiler deflection |
| vehicle-design/sizing/battery-sizing | Battery sizing | battery pack sizing, electric aircraft battery, eVTOL energy storage, traction battery, C-rate check, depth of discharge, series parallel cell count, pack voltage, discharge voltage drop |
| vehicle-design/mdo/surrogate-modeling | Surrogate modeling | surrogate model, metamodel, response surface, radial basis function, leave one out cross validation, approximation model, prediction error, expensive analysis replacement |
| vehicle-design/sizing/brake-energy-sizing | Brake energy sizing | brake energy sizing, rejected takeoff energy, wheel brake heat sink, brake temperature rise, carbon brake mass, braking distance at V1 |
| vehicle-design/sizing/canard-sizing | Canard sizing | canard sizing, canard volume coefficient, canard area, forward wing, stall precedence, canard configuration, trim lift share |
| vehicle-design/sizing/environmental-control-sizing | Environmental control sizing | environmental control sizing, cabin air conditioning, cabin heat load, ventilation flow, pack cooling flow, pressurization schedule, cabin altitude limit |
| vehicle-design/sizing/hydraulic-system-sizing | Hydraulic system sizing | hydraulic system sizing, hydraulic power, actuator flow demand, pump flow sizing, accumulator sizing, reservoir sizing, system pressure, emergency hydraulic |

| vehicle-design/sizing/landing-gear-retraction-sizing | Landing gear retraction sizing | landing gear retraction, retraction actuator force and stroke, linkage geometry, up-lock down-lock hold load, gear bay stowage fit |
| vehicle-design/sizing/aircraft-electrical-load-analysis | Aircraft electrical load analysis | aircraft electrical load analysis, electrical load rollup, duty cycle loading, generator rating check, essential load margin |
| vehicle-design/sizing/fuel-feed-system-sizing | Fuel feed system sizing | fuel feed system sizing, fuel boost pump, feed line pressure loss, engine feed NPSH, fuel pump power |
| vehicle-design/sizing/avionics-bay-cooling-sizing | Avionics bay cooling sizing | avionics bay cooling, equipment bay cooling airflow, LRU heat dissipation, LRU case temperature |
| vehicle-design/sizing/aircraft-oxygen-system-sizing | Aircraft oxygen system sizing | aircraft oxygen system sizing, supplemental oxygen, oxygen generator count, gaseous oxygen bottle volume, oxygen demand calculation |
| vehicle-design/sizing/fire-protection-sizing | Fire protection sizing | fire protection sizing, extinguishing agent mass, total flooding agent, cargo compartment fire, powerplant fire zone |
| vehicle-design/sizing/fuel-jettison-sizing | Fuel jettison sizing | fuel jettison sizing, fuel dump rate, jettison time to landing weight, fuel jettison mast |
| vehicle-design/sizing/bleed-air-system-sizing | Bleed air system sizing | bleed air system sizing, bleed offtake mass flow, bleed duct diameter, bleed thermal budget, pneumatic bleed manifold |
| vehicle-design/sizing/apu-fuel-burn-sizing | APU fuel burn sizing | APU fuel burn sizing, auxiliary power unit fuel burn, generator shaft power, bleed pumping power, apu fuel flow rate |
| vehicle-design/sizing/ram-air-turbine-sizing | Ram air turbine sizing | ram air turbine sizing, ram air turbine rotor, RAT disk diameter, emergency power extraction, rat swept area |
| vehicle-design/sizing/fuel-tank-inerting-sizing | Fuel tank inerting sizing | fuel tank inerting sizing, OBIGGS flow, ullage oxygen washout, nitrogen enriched air, ullage inerting |
| vehicle-design/sizing/cabin-outflow-valve-sizing | Cabin outflow valve sizing | cabin outflow valve sizing, outflow valve area, pressure relief valve, choked cabin flow, differential pressure clamp |
| vehicle-design/sizing/electrical-wire-sizing | Electrical wire sizing | electrical wire sizing, conductor ampacity, ampacity derating, wire voltage drop, percent drop bus tolerance, EWIS conductor selection |
| vehicle-design/sizing/hydraulic-actuator-sizing | Hydraulic actuator sizing | hydraulic actuator sizing, actuator bore diameter, piston area, rod buckling, annulus retract check, preferred actuator sizes, actuator mass |
| vehicle-design/sizing/cargo-compartment-sizing | Cargo compartment sizing | cargo compartment sizing, ULD layout, cargo door opening, unit load device |
| vehicle-design/sizing/window-aperture-sizing | Window aperture sizing | window aperture sizing, window pane thickness, pressure differential stress, circular pane |
| vehicle-design/sizing/emergency-exit-configuration | Emergency exit configuration | emergency exit configuration, exit type requirements, exit count check, exit placement |
| vehicle-design/sizing/air-cycle-machine-sizing | Air cycle machine sizing | air cycle machine sizing, bootstrap air cycle, ACM shaft balance, cooling turbine, heat exchanger effectiveness, required bleed flow |
| vehicle-design/sizing/v-tail-sizing | V tail sizing | v tail sizing, ruddervator, equivalent tail volume, V-tail dihedral, tail area from volume coefficient |
| vehicle-design/sizing/landing-gear-layout | Landing gear layout | tipback angle, tail strike clearance, lateral turnover angle, nose gear load fraction band, main gear position |
| vehicle-design/sizing/landing-gear-height-sizing | Landing gear height sizing | landing-gear-height-sizing, static-ground-line, main-gear-height-selection, nose-gear-height-selection, tail-cone-clearance, rotation-clearance-margin, waterline-leveling |


## Routing guidance

- Takeoff gross weight and fuel-fraction questions route to the
  conceptual tow-estimation sub-skill.
- Payload-range and Breguet-range trade questions route to the
  conceptual payload-range-diagram sub-skill.
- Weight and balance sheet questions route to the
  sizing weight-estimation sub-skill.
- Component group-weight and class-II statistical weight questions
  (Raymer/Torenbeek airframe group-weight regressions, group-weight
  rollup) route to the sizing component-weight-estimation sub-skill;
  class-I totals stay with weight-estimation.
- Mission profile questions route to the conceptual sizing-mission-profile sub-skill.
- Cabin layout and fuselage diameter questions route to the sizing
  fuselage-sizing sub-skill.
- Empennage sizing questions (tail volume coefficients, required tail
  area) route to the sizing tail-sizing sub-skill.
- Control surface sizing questions (aileron area from the roll rate
  requirement, elevator area from the pitch moment requirement,
  rudder area from the yaw moment requirement, hinge moment,
  deflection limits) route to the sizing control-surface-sizing
  sub-skill.
- Landing gear questions (strut loads, gear loads, shock absorber
  stroke) route to the sizing landing-gear-sizing sub-skill.
- Landing gear height and static-ground-line questions (tail-cone clearance at rotation attitude, main- and nose-gear height selection that levels the fuselage, waterline leveling, rotation clearance margin) route to the sizing landing-gear-height-sizing sub-skill; gear layout (tipback, turnover, load fraction) stays with landing-gear-layout.
- Wing loading and thrust to weight matching questions (the sizing
  matching chart, takeoff distance, climb gradient, and cruise
  constraints) route to the sizing/ws-tw-trade sub-skill.
- Wing planform questions (wing area from wing loading and takeoff
  gross weight, aspect ratio, span, taper ratio, mean aerodynamic
  chord, sweep angle from cruise Mach) route to the sizing
  wing-planform-sizing sub-skill.
- Sea level static thrust, thrust lapse, takeoff thrust, top of climb
  margin, SFC fuel flow, and engine weight questions route to the
  sizing engine-sizing sub-skill.
- Fuel volume, ullage, and tank capacity questions route to the
  sizing fuel-tank-sizing sub-skill.
- Moment of inertia and radius of gyration questions route to the
  mass-properties inertia-estimation sub-skill.
- CG envelope questions (forward/aft limits, static margin, envelope
  polygon, cg excursion) route to the mass-properties cg-envelope
  sub-skill.
- Mass rollup, growth allowance, and contingency margin questions
  route to the mass-properties mass-budget sub-skill.
- Cost estimating relationship and learning curve questions route to
  the cost-estimation parametric-cost sub-skill.
- Direct operating cost, fuel, crew, and maintenance cost questions
  route to the cost-estimation operating-cost sub-skill.
- Life cycle cost, LCC phase, present value, and uncertainty
  questions route to the cost-estimation life-cycle-cost sub-skill.
- Aerodynamic, structural, and certification questions route to their
  domain packs (aerodynamics, structures, avionics).

- Wing box, spar, shear web, and root bending moment sizing questions route to the structures-integration wing-box-sizing sub-skill.
- Fuselage skin thickness, stringer spacing, and frame pitch questions route to the structures-integration fuselage-skin-stringer sub-skill.
- Multidisciplinary optimization, aero-structural coupling loops, fixed-point discipline iteration, and design-space search questions route to the mdo multidisciplinary-optimization sub-skill.
- Propeller diameter, blade count, solidity, activity factor, disk loading, and advance ratio questions route to the sizing propeller-sizing sub-skill.
- Landing gear tire sizing, static load per tire, tire diameter and width, and tire pressure questions route to the sizing tire-sizing sub-skill.
- Constraint analysis matching chart, thrust to weight ratio, wing loading, stall, climb gradient, and takeoff distance constraint questions route to the conceptual constraint-analysis sub-skill.
- Parametric aircraft geometry building, mean aerodynamic chord and wetted area computation, and component volume estimation route to the conceptual openvsp-geometry sub-skill.
- Engine nacelle geometric sizing, highlight area from fan mass flow and Mach, inlet capture and lip areas, nacelle length, wetted area, and cowl thickness questions route to the sizing nacelle-sizing sub-skill.
- Thermal ice protection sizing, evaporative and running-wet anti-ice heat flux, catch efficiency from MVD and airspeed, protected area power and bleed flow questions route to the sizing ice-protection-sizing sub-skill.
- Flight and ground spoiler sizing, lift dump, speed brake drag, roll assist share, spoiler panel area and deflection questions route to the sizing spoiler-sizing sub-skill.
- Brake energy sizing questions (brake energy sizing, rejected takeoff energy, wheel brake heat sink, brake temperature rise, carbon brake mass, braking distance at v1) route to the brake-energy-sizing sub-skill.
- Canard sizing, canard volume coefficient, and stall-precedence questions route to the sizing canard-sizing sub-skill.

- Aircraft environmental control system sizing questions (cabin ventilation fresh air flow, cabin heat load, pack cooling airflow, pressurization schedule and cabin altitude limit) route to the sizing environmental-control-sizing sub-skill.

- Aircraft hydraulic power system sizing questions (actuator flow demand, pump flow and power, accumulator adiabatic gas volume, reservoir volume) route to the sizing hydraulic-system-sizing sub-skill.
- Landing gear retraction mechanism questions (retraction actuator force and stroke, linkage geometry, up-lock down-lock hold load, gear bay stowage fit) route to the sizing landing-gear-retraction-sizing sub-skill.
- Aircraft electrical load analysis questions (load rollup with duty cycles, generator rating check, single-generator-out essential load margin) route to the sizing aircraft-electrical-load-analysis sub-skill.
- Aircraft fuel feed system questions (boost pump sizing, feed line pressure loss, engine feed NPSH) route to the sizing fuel-feed-system-sizing sub-skill.
- Avionics and equipment bay cooling questions (bay cooling airflow from LRU heat dissipation, LRU case temperature check) route to the sizing avionics-bay-cooling-sizing sub-skill.
- Aircraft supplemental oxygen sizing questions (passenger oxygen generator count, crew gaseous oxygen bottle volume) route to the sizing aircraft-oxygen-system-sizing sub-skill.
- Fire protection and extinguishing agent questions (total flooding agent mass for cargo compartment or powerplant fire zone) route to the sizing fire-protection-sizing sub-skill.
- Fuel jettison questions (required dump rate to landing weight within 15 minutes, mast flow split) route to the sizing fuel-jettison-sizing sub-skill.
- tipback angle, tail strike clearance, lateral turnover angle, nose gear load fraction band, main gear position questions route to the sizing landing-gear-layout sub-skill.

- Landing gear group weight questions (class-II main and nose gear mass regressions from design landing weight and ultimate load factor, gear group total) route to the sizing landing-gear-weight-estimation sub-skill; gear geometry, retraction loads and layout stay with the landing-gear design leaves.
- Fuel system group weight questions (class-II tankage, plumbing and pumps hardware mass from total fuel weight and tank arrangement) route to the sizing fuel-system-weight-estimation sub-skill; tank volume and feed rates stay with the fuel-tank-sizing and fuel-feed leaves.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- DOE factorial and latin-hypercube design space screening questions route to the mdo design-of-experiments sub-skill.
- Battery pack sizing questions (traction battery for electric aircraft and eVTOL, C-rate, depth of discharge, series parallel cell count, voltage drop) route to the sizing battery-sizing sub-skill.
- Surrogate model questions (response surface and RBF metamodel fit with cross-validation for the MDO loop) route to the mdo surrogate-modeling sub-skill.
- Bleed air system questions (bleed offtake rollup, per-engine offtake, bleed duct diameter, precooler thermal budget) route to the sizing bleed-air-system-sizing sub-skill.
- APU fuel burn questions (generator shaft load, bleed pumping power, kg/h fuel flow at a fixed APU load point) route to the sizing apu-fuel-burn-sizing sub-skill.
- Ram air turbine questions (emergency RAT swept area and disk diameter from required power at a fixed airspeed) route to the sizing ram-air-turbine-sizing sub-skill.
- Fuel tank inerting questions (OBIGGS NEA flow, ullage oxygen washout time, SCFM flow for a target oxygen fraction) route to the sizing fuel-tank-inerting-sizing sub-skill.
- Cabin outflow and pressure relief valve questions (choked effective area at the cruise differential and the pressure clamp) route to the sizing cabin-outflow-valve-sizing sub-skill.

- Electrical wire run questions (conductor gauge selection from derated ampacity, round-trip voltage drop and percent-drop verdict against the bus tolerance) route to the sizing electrical-wire-sizing sub-skill.
- Hydraulic actuator questions (bore and piston area from load and system pressure, rod buckling diameter, annulus retract capability, preferred size selection and mass estimate) route to the sizing hydraulic-actuator-sizing sub-skill.

- Cargo compartment questions (standard-ULD layout and position count, cargo door opening fit, payload volume closure) route to the sizing cargo-compartment-sizing sub-skill.

- Passenger window aperture questions (pane thickness and stress from the pressure differential, design pressure factor, margin) route to the sizing window-aperture-sizing sub-skill.

- Emergency exit configuration questions (exit type dimensions and capacity bands, required exit count by passenger capacity, exit placement spacing) route to the sizing emergency-exit-configuration sub-skill.

- Bootstrap air-cycle pack questions (compressor and turbine exit states with efficiencies, heat-exchanger exit, two-wheel ACM shaft balance, delivered cooling power versus the ECS load and required bleed flow) route to the sizing air-cycle-machine-sizing sub-skill.
- V-tail empennage questions (equivalent horizontal and vertical tail-volume requirements, total V-tail area and dihedral angle, per-surface geometry and ruddervator area) route to the sizing v-tail-sizing sub-skill.
