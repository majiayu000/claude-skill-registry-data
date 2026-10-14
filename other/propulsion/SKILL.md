---
name: propulsion
description: "Use when a task concerns aircraft or rocket propulsion: guide the router to the propulsion pack: gas-turbine-cycle Brayton, regenerative-cycle regenerator efficiency, real-cycle-effects component losses, turbofan-cycle turbofan parameters, bypass-ratio-trade bypass design, turbofan-off-design part-power behavior, free-turbine power turbine matching, turbine-stage stage velocity triangles, axial-compressor-stage compressor stage, compressor-map operating maps, multi-stage-compressor stacked stages, rocket-sizing rocket sizing, nozzle-design nozzles, propellant-selection propellant trade, ramjet-cycle ideal ramjet performance, ramjet-inlet supersonic inlet starting. Trigger: propulsion, gas turbine, Brayton cycle, regenerator, turbofan, bypass ratio, rocket equation, delta-v, rocket nozzle, area ratio, propellant, axial compressor, compressor map, multi-stage compressor, off-design turbofan, real cycle, free turbine, power turbine, turboshaft, ramjet, ramjet inlet, Kantrowitz, specific thrust, specific impulse."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: far-33
    reference-only: true
  - id: ecss
    reference-only: true
gated: false
domain: propulsion
pack: propulsion
compatibility: "agentskills.io SKILL.md; router/entry point for the propulsion domain pack"
metadata:
  domain: propulsion
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Propulsion domain pack (router)

Route here when the task is engine cycle analysis, turbofan
performance parameters, rocket sizing, rocket nozzles, rocket
propellant selection, or axial compressor maps and stages.

## Domain

Propulsion: gas turbine and turbofan thermodynamic cycle analysis
(simple and regenerative Brayton), turbofan bypass design trades,
launch-vehicle rocket sizing with the rocket equation and staging,
rocket nozzle design, rocket propellant selection, and axial
compressor stage and operating-map analysis.

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| propulsion/gas-turbine-cycle/gas-turbine-cycle | Gas turbine cycle | Brayton thermal efficiency, compressor/turbine exit temperatures, pressure ratio |
| propulsion/gas-turbine-cycle/regenerative-cycle | Regenerative cycle | regenerator effectiveness, regenerative cycle efficiency, optimum pressure ratio, efficiency gain |
| propulsion/gas-turbine-cycle/real-cycle-effects | Real cycle effects | component efficiency, isentropic efficiency, pressure loss, actual exit temperatures, real SFC |
| propulsion/gas-turbine-cycle/combustor-design | Combustor design | stoichiometric fuel-air-ratio, operating fuel-air-ratio, combustion efficiency, heat release, temperature rise, adiabatic flame temperature |
| propulsion/gas-turbine-cycle/afterburner-cycle | Afterburner cycle | afterburner cycle, reheat fuel air ratio, thrust augmentation ratio, reheat temperature rise, dry versus reheat thrust, reheat specific fuel consumption, afterburner nozzle exit velocity |
| propulsion/turbofan/turbofan-cycle | Turbofan cycle | bypass ratio, propulsive efficiency, specific thrust, fan/core mass flow |
| propulsion/turbofan/bypass-ratio-trade | Bypass ratio trade | BPR vs TSFC, thrust split, specific thrust, fan pressure ratio |
| propulsion/turbofan/turbofan-off-design | Turbofan off-design | corrected mass flow, corrected spool speed, altitude thrust, ram drag, cruise SFC, throttle setting |
| propulsion/turbofan/turbofan-design-point | Turbofan design point | turbofan design point, fan stream station states, two-spool work balance, separate-exhaust cycle, design point turbofan |
| propulsion/turboprop/free-turbine | Free turbine | power turbine exit temperature, shaft power, torque, gear ratio, flow function, spool matching |
| propulsion/turboprop/turboprop-cycle | Turboprop cycle | propeller efficiency, static thrust, equivalent shaft power, advance ratio, power and thrust coefficients, SFC on shaft power |
| propulsion/axial-compressor/axial-compressor-stage | Axial compressor stage | velocity triangle, specific work, flow coefficient, degree of reaction, stage pressure ratio, blade loading |
| propulsion/axial-compressor/compressor-map | Compressor map | surge line and margin, operating line, speed lines, corrected flow and speed, choke |
| propulsion/axial-compressor/multi-stage-compressor | Multi-stage compressor | overall pressure ratio, stage count, stage matching, reheat factor, annulus area, corrected speed |
| propulsion/axial-compressor/turbine-stage | Turbine stage | stage loading, flow coefficient, reaction, blade row losses, total-to-total efficiency, velocity triangles |
| propulsion/axial-compressor/turbine-blade-cooling | Turbine blade cooling | turbine blade cooling, cooling effectiveness, coolant flow fraction, film cooling, allowable metal temperature, coolant supply temperature, bleed limit, hot section cooling |
| propulsion/rocket/rocket-sizing | Rocket sizing | rocket equation delta-v, mass ratio, propellant mass, staging |
| propulsion/rocket/rocket-staging | Rocket staging | stage mass ratio allocation, payload fraction, structural index, stage count optimization, per-stage delta-v |
| propulsion/rocket/rocket-gravity-loss | Rocket gravity loss | rocket gravity loss, launch vehicle ascent, ascent delta v, powered ascent, burn time estimate, launch thrust to weight |
| propulsion/rocket/nozzle-design | Rocket nozzle design | area ratio, exit Mach, mass flow, ideal thrust, expansion |
| propulsion/rocket/propellant-selection | Propellant selection | propellant families, density impulse, mixture ratio, storability, mass fraction |
| propulsion/ramjet/ramjet-cycle | Ramjet cycle | ideal ramjet, fuel air ratio, total temperature ratio, specific thrust, specific impulse |
| propulsion/ramjet/ramjet-inlet | Ramjet inlet | supersonic inlet, Kantrowitz starting, normal shock pressure recovery, diffuser, contraction ratio |
| propulsion/engine-airframe/engine-airframe-integration | Engine-airframe integration | installed thrust, intake momentum drag, nozzle gross thrust, nacelle drag, pylon drag, bleed extraction, thrust-drag bookkeeping |
| propulsion/rocket/thrust-vector-control | Thrust vector control | gimbal deflection, side force, control torque, axial thrust loss, actuator authority, TVC |
| propulsion/rocket/combustion-chamber-design | Combustion chamber design | characteristic velocity, c-star, chamber pressure, throat area, chamber volume, residence time |
| propulsion/turbomachinery/centrifugal-compressor | Centrifugal compressor | impeller tip speed, slip factor, Wiesner, work input coefficient, stage pressure ratio, isentropic efficiency |
| propulsion/combustion/cea-rocket-combustion | Rocket combustion thermochemistry | rocket combustion, adiabatic flame temperature, characteristic velocity, specific impulse, mixture ratio, frozen flow, chamber pressure, thermochemistry, c-star, propellant selection |
| propulsion/rocket/solid-rocket-motor | Solid rocket motor | solid rocket motor, burn rate, chamber pressure, grain geometry, mass flow, thrust, total impulse, c star |
| propulsion/electric/hall-thruster | Hall Thruster | hall thruster, electric propulsion, specific impulse, thrust-to-power, beam current, discharge power, xenon, krypton, propellant mass, delta-v. |
| propulsion/electric/gridded-ion-thruster | Gridded ion thruster | gridded ion thruster, Kaufman thruster, accelerator grid, perveance limit, beam extraction, ion optics |
| propulsion/electric/electrothermal-thruster | Electrothermal thruster | electrothermal thruster, resistojet, arcjet, heated propellant, power to thrust |
| propulsion/rocket/rocket-engine-cycle | Rocket engine cycle | rocket engine cycle, feed cycle, gas-generator cycle, staged combustion, expander cycle, pressure-fed, pump-fed, pump power, turbine power |
| propulsion/rocket/hybrid-rocket-motor | Hybrid rocket motor | hybrid rocket motor, regression rate, oxidizer mass flux, solid fuel grain, oxidizer to fuel ratio, O/F shift, port area, HTPB, hybrid grain |
| propulsion/rocket/cold-gas-thruster | Cold gas thruster | cold gas thruster, nitrogen RCS, choked mass flow, plenum blowdown, total impulse, reaction control thruster sizing, isothermal blowdown time constant |
| propulsion/turbomachinery/rocket-turbopump | Rocket turbopump | rocket turbopump, pump specific speed, suction specific speed, net positive suction head, impeller tip speed, LOX pump sizing, cavitation margin |
| propulsion/rocket/thrust-chamber-cooling | Thrust chamber cooling | thrust chamber cooling, regenerative cooling, Bartz heat transfer, throat heat flux, coolant channel sizing, copper wall limit, film cooling rocket |
| propulsion/rocket/injector-design | Injector design | injector design, unlike doublet, impinging jet atomization, injector pressure drop, momentum flux ratio, orifice flow count |
| propulsion/gas-turbine-cycle/propelling-nozzle | Propelling nozzle | propelling nozzle, convergent jet nozzle, nozzle throat area, choked nozzle regime, gross thrust pressure term |
| propulsion/gas-turbine-cycle/subsonic-inlet-recovery | Subsonic inlet recovery | subsonic inlet recovery, ram recovery ratio, engine face total pressure, intake capture area, spillage verdict, duct total pressure efficiency |
| propulsion/gas-turbine-cycle/intercooled-cycle | Intercooled cycle | intercooled cycle, intercooler effectiveness, intercooler pressure ratio, two stage compression, compression work split, cycle work gain |
| propulsion/gas-turbine-cycle/turbojet-cycle | Turbojet cycle | turbojet cycle, ideal turbojet, compressor turbine matching, turbine inlet temperature, net specific thrust, turbojet TSFC, core engine matching |
| propulsion/rocket/rocket-nozzle-flow-separation | Rocket nozzle flow separation | rocket nozzle flow separation, separation pressure ratio, Summerfield criterion, overexpanded nozzle, separation altitude, separated thrust loss, side load regime |
| propulsion/rocket/rocket-nozzle-divergence-loss | Rocket nozzle divergence loss | rocket nozzle divergence loss, conical nozzle thrust correction, bell nozzle efficiency, nozzle delivered Isp |
| propulsion/axial-compressor/polytropic-efficiency | Polytropic efficiency | polytropic efficiency, isentropic efficiency conversion, stage count independent efficiency, per stage pressure ratio, reheat factor |
| propulsion/gas-turbine-cycle/brayton-optimum-pressure-ratio | Brayton optimum pressure ratio | max-work pressure ratio, maximum specific work, zero-work limiting ratio, ideal and lossy cycle |

| propulsion/turbofan/mixed-flow-exhaust | Mixed flow exhaust | mixed flow exhaust, turbofan mixing exhaust, constant area mixer, exhaust mixer, common nozzle, mixing loss, mixed versus separate exhaust |
| propulsion/rocket/nozzle-area-ratio-selection | Nozzle area ratio selection | nozzle area ratio selection, design altitude expansion ratio, matched expansion ratio, optimum area ratio, sea level vacuum Isp, expansion ratio selection |

| propulsion/electric/mpd-thruster | Mpd Thruster | mpd-thruster, magnetoplasmadynamic-thruster, self-field-thrust-law, electromagnetic-acceleration, discharge-current-scaling |
| propulsion/rocket/hydrazine-monopropellant-thruster | Hydrazine Monopropellant Thruster | hydrazine-monopropellant-thruster, catalytic-decomposition, ammonia-dissociation-fraction, monopropellant-rcs, decomposition-temperature |
| propulsion/rocket/hydrogen-peroxide-monopropellant-thruster | Hydrogen Peroxide Monopropellant Thruster | hydrogen-peroxide-monopropellant-thruster, peroxide-decomposition, steam-oxygen-mixture, silver-catalyst-bed, concentration-limited-decomposition |
| propulsion/reciprocating/piston-engine-cycle | Piston Engine Cycle | piston-engine-cycle, air-standard-otto-cycle, mean-effective-pressure, brake-specific-fuel-consumption, reciprocating-engine-powerplant, four-stroke-powerplant |
| propulsion/reciprocating/diesel-cycle | Diesel Cycle | diesel-cycle, compression-ignition-cycle, air-standard-diesel-cycle, cutoff-ratio, diesel-cycle-efficiency, compression-ignition-powerplant |
| propulsion/reciprocating/dual-cycle | Dual Cycle | dual-cycle, sabathe-cycle, limited-pressure-cycle, pressure-ratio, cutoff-ratio, dual-cycle-efficiency |
## Routing guidance

- Brayton/gas-turbine thermodynamics route to the gas-turbine-cycle
  sub-skill; regenerator and recuperator cycle questions route to the
  regenerative-cycle sub-skill.
- Turbofan bypass and efficiency questions route - Hall thruster questions route to the electric hall-thruster sub-skill.
- Magnetoplasmadynamic thruster questions (self-field electromagnetic thrust from the discharge-current-squared law, anode-to-cathode radius ratio, exhaust velocity and specific impulse from the mass flow, jet power, thrust-to-power band verdict) route to the electric mpd-thruster sub-skill.
to turbofan-cycle;
  BPR vs TSFC design-trade questions route to bypass-ratio-trade;
  off-design and altitude behavior questions route to
  turbofan-off-design.
- Free-turbine and power-turbine matching questions (shaft power,
  gear ratio, flow function) route to the free-turbine sub-skill;
  propeller-side cycle questions (propeller efficiency, static
  thrust, equivalent shaft power, advance ratio, power and thrust
  coefficients) route to the turboprop-cycle sub-skill.
- Rocket equation, delta-v, staging, and propellant mass questions
  route to the rocket-sizing sub-skill; rocket nozzle questions (area
  ratio, exit Mach, thrust, expansion) route to nozzle-design;
  propellant family, density impulse, and mixture ratio questions
  route to propellant-selection.
- Multi-stage rocket staging questions (per-stage delta-v, stage mass
  ratio and payload fraction allocation, structural index, stage count
  optimization for a target total delta-v) route to the rocket-staging
  sub-skill.
- Axial compressor stage questions (velocity triangles, degree of
  reaction, stage pressure ratio) route to the
  axial-compressor-stage sub-skill; turbine stage questions (stage
  loading, reaction, blade row losses, efficiency) route to the
  turbine-stage sub-skill.
- Compressor map questions (surge margin, operating line, speed
  lines, corrected flow and speed) route to the compressor-map
  sub-skill; multi-stage compressor questions (overall pressure
  ratio, stage count, stage matching, reheat factor, annulus area)
  route to the multi-stage-compressor sub-skill.
- Non-ideal cycle questions (component efficiencies, pressure loss,
  real SFC) route to the real-cycle-effects sub-skill.
- Combustor design questions (stoichiometric and operating
  fuel-air-ratio, combustion efficiency, heat release, temperature
  rise across the combustor, adiabatic flame temperature) route to
  the combustor-design sub-skill.
- Airframe, stability, and certification questions route to their
  domain packs (flight-mechanics, avionics).

- Ideal ramjet, fuel air ratio, and specific impulse questions route to the ramjet ramjet-cycle sub-skill.
- Supersonic inlet starting, Kantrowitz criterion, and diffuser pressure recovery questions route to the ramjet ramjet-inlet sub-skill.
- Installed thrust, intake momentum drag, nacelle and pylon drag, bleed extraction, and thrust-drag bookkeeping questions route to the engine-airframe engine-airframe-integration sub-skill.
- Gimbal deflection, side force, control torque, axial thrust loss, and actuator authority sizing questions route to the rocket thrust-vector-control sub-skill.
- Rocket combustion chamber sizing, characteristic velocity c-star, chamber pressure and throat area, and residence time questions route to the rocket combustion-chamber-design sub-skill.
- Centrifugal compressor impeller tip speed, slip factor, work input, stage pressure ratio, and isentropic efficiency questions route to the turbomachinery centrifugal-compressor sub-skill.
- Rocket combustion thermochemistry, adiabatic flame temperature, characteristic velocity, and ideal specific impulse from propellant and mixture ratio route to the combustion cea-rocket-combustion sub-skill.
- Solid rocket motor ballistics, burn-rate law, chamber pressure equilibrium, grain geometry, mass flow, thrust, and total impulse questions route to the rocket solid-rocket-motor sub-skill.
- Hybrid rocket motor regression rate, oxidizer mass flux, O/F shift, port area, and chamber pressure ballistics questions route to the rocket hybrid-rocket-motor sub-skill.
- Cold gas thruster choked flow, plenum blowdown, and total impulse questions route to the rocket cold-gas-thruster sub-skill.
- Hydrazine monopropellant thruster questions (catalytic decomposition energy balance, ammonia dissociation fraction, adiabatic decomposition temperature, nozzle expansion of the decomposed mixture, vacuum specific impulse for the RCS duty) route to the rocket hydrazine-monopropellant-thruster sub-skill.
- Hydrogen peroxide monopropellant thruster questions (peroxide decomposition temperature from the catalytic energy balance, steam-oxygen mixture state, silver-catalyst-bed decomposition, concentration-limited decomposition, vacuum specific impulse for the monopropellant RCS duty) route to the rocket hydrogen-peroxide-monopropellant-thruster sub-skill.
- Reciprocating aircraft powerplant questions (air-standard Otto cycle efficiency at the compression ratio, four-stroke indicated power from mean effective pressure and displacement, brake power at mechanical efficiency, brake specific fuel consumption) route to the reciprocating piston-engine-cycle sub-skill; gas-turbine and turboshaft shaft-power questions stay with the turbine packs.
- Compression-ignition powerplant questions (air-standard Diesel cycle efficiency at the compression ratio and cutoff ratio, diesel state points, brake specific fuel consumption of a compression-ignition engine) route to the reciprocating diesel-cycle sub-skill; spark-ignition Otto-cycle questions stay with piston-engine-cycle.
- Rocket turbopump specific speed, suction performance, and cavitation questions route to the turbomachinery rocket-turbopump sub-skill.

- Rocket thrust chamber regenerative cooling questions (Bartz hot gas coefficient, coolant side convection, wall heat flux and temperature, coolant mass flux for the wall limit, film cooling handoff) route to the rocket thrust-chamber-cooling sub-skill.

- Rocket engine injector element design questions (orifice discharge flow, injection velocity, unlike-doublet momentum flux ratio, fuel and oxidizer orifice counts, per-element flow balance) route to the rocket injector-design sub-skill.
- max-work pressure ratio, maximum specific work, zero-work limiting ratio, ideal and lossy cycle questions route to the gas-turbine-cycle brayton-optimum-pressure-ratio sub-skill.
- Dual-cycle powerplant questions (Sabathe limited-pressure air-standard cycle efficiency at the compression ratio, pressure ratio and cutoff ratio, dual-cycle state points) route to the reciprocating dual-cycle sub-skill; compression-ignition stays with diesel-cycle and spark-ignition Otto stays with piston-engine-cycle.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- Gridded ion thruster and ion-optics perveance questions route to the electric gridded-ion-thruster sub-skill.
- Resistojet and arcjet operating-point and power-to-thrust questions route to the electric electrothermal-thruster sub-skill.
- Liquid engine feed-cycle selection and pump-turbine power balance questions route to the rocket rocket-engine-cycle sub-skill.
- Afterburner reheat fuel-air ratio, dry versus reheat thrust, and augmentation ratio questions route to the gas-turbine-cycle afterburner-cycle sub-skill.
- Turbine blade cooling effectiveness, coolant flow fraction, and film-cooling metal temperature questions route to the axial-compressor turbine-blade-cooling sub-skill.
- Air-breathing propelling nozzle questions (choked or unchoked regime, throat area from design mass flow, gross thrust with the pressure term) route to the gas-turbine-cycle propelling-nozzle sub-skill.

- Subsonic turbofan intake questions (ram recovery from flight Mach, engine-face total pressure after duct efficiency, capture-area and spillage verdict against the highlight) route to the gas-turbine-cycle subsonic-inlet-recovery sub-skill.
- Intercooled Brayton questions (intercooler effectiveness, two-stage compression split, optimum intercooler pressure ratio, specific-work gain over the simple cycle) route to the gas-turbine-cycle intercooled-cycle sub-skill.
- Overexpanded rocket nozzle flow-separation questions (separation pressure ratio, Summerfield criterion, separation-station area ratio, separation altitude, separated thrust loss, side-load regime) route to the rocket rocket-nozzle-flow-separation sub-skill.
- Powered-ascent gravity-loss questions (burn time from propellant and mass flow, launch thrust-to-weight, gravity loss over the mean flight-path angle, effective ascent delta-v after the losses) route to the rocket rocket-gravity-loss sub-skill.
- Ideal single-stream turbojet core questions (compressor-turbine work-balance matching, turbine-inlet-temperature-driven specific thrust, turbojet TSFC and propulsive efficiency at flight Mach) route to the gas-turbine-cycle turbojet-cycle sub-skill.

- Compressor and turbine efficiency conversion questions (isentropic to polytropic and reverse at an overall pressure ratio, stage-count-independent polytropic efficiency, reheat-factor cross-check) route to the axial-compressor polytropic-efficiency sub-skill.
- Turbofan design-point questions (fan and core stream station states from OPR, turbine-inlet temperature, fan pressure ratio and bypass ratio, two-spool work balance, separate-exhaust net thrust and TSFC) route to the turbofan turbofan-design-point sub-skill.
- Mixed-flow exhaust questions (two-stream mixer energy and momentum balance, common nozzle, mixing loss) route to the turbofan mixed-flow-exhaust sub-skill; rocket nozzle design-altitude expansion-ratio selection (matched area ratio, delivered Isp at sea level and vacuum) routes to the rocket nozzle-area-ratio-selection sub-skill.
- Rocket nozzle delivered-thrust loss questions (conical-nozzle divergence factor, bell-contour efficiency, boundary-layer displacement effect, delivered Isp versus the ideal ceiling) route to the rocket rocket-nozzle-divergence-loss sub-skill.
