---
name: thermal-machinery-dynamic-modeling
description: Guide AI agents to build, inspect, debug, or review dynamic thermodynamic models for thermal-power and energy-conversion machinery. Use when a task involves Brayton, Rankine, refrigeration, heat-pump, compressor, turbine, combustor, heat-exchanger, recuperator, reactor, process-heat, integrated-power, or coupled thermo-fluid dynamic systems; node-by-node thermodynamic ledgers; component balance equations; design-point to dynamic initialization; MATLAB/Simulink implementation; or validation of mass, species, energy, pressure, and dynamic-state consistency.
---

# Thermal Machinery Dynamic Modeling

## Purpose

Use this skill to make AI modeling of thermal machinery staged, traceable, and physically checkable. Treat a thermal system as a graph of working-fluid streams, components, states, balances, and dynamic storage terms, not as a formula dump or a block diagram.

This is a general workflow skill. Domain-specific skills such as gas-turbine, refrigeration, heat-pump, boiler, or process-system skills may add specialized equations and validation checks. For a gas-turbine subsystem, use `gas-turbine-ai-modeling` when available after the whole-system topology and stream ledger are clear.

## Core Workflow

Always work in this order unless the user explicitly narrows the task:

1. Identify the application, system boundary, working fluids, modeling depth, fidelity target, available data, and control objective.
2. Create a depth and simplification contract: topology screen, design point, executable design reproduction, steady plant, reduced dynamic plant, detailed dynamic plant, or controlled/optimized plant.
3. Select or ask for the topology before equations: components, stream paths, split/merge points, heat-transfer pairings, pressure sources/losses, energy-quality paths, and environment boundaries.
4. Build a thermodynamic node and stream ledger. Every working fluid at every node must carry temperature, pressure, mass flow, molar flow when relevant, composition or quality, unit, basis, source, and calculation status.
5. Define component contracts: inputs, outputs, parameters, states, residuals, assumptions, closure depth, and validation checks.
6. Build or inspect a design-point or steady solver before adding dynamics.
7. Map the design/steady result into dynamic initial conditions, lookup tables, controller references, and logged validation signals.
8. Add dynamic states only where physical storage or actuator/control dynamics require them.
9. Validate each stage before adding complexity: topology -> ledger -> component balances -> steady state -> dynamic initialization -> transient/control.

Do not jump directly to Simulink, Python, or MATLAB implementation when the topology, node ledger, component contracts, or validation standard are missing.

Do not overbuild by default. A reduced design-point or steady model can be the correct deliverable when the user only needs feasibility, but it must not be presented as a validated dynamic plant.

## Mandatory Evidence

For a full build or strict review, produce or reference:

1. `scope_and_topology.md`: system boundary, working fluids, topology, components, heat-transfer pairs, split/merge points, and control objective.
2. `model_depth_contract.md`: requested depth, fidelity target, simplifications, missing evidence, and claims allowed at that stage.
3. `thermodynamic_node_stream_ledger.csv`: node-by-node stream ledger with temperature, pressure, flow, composition or quality, units, source, and calculation status.
4. `component_contracts.csv`: each component's ports, equations, parameters, states, residuals, and checks.
5. `state_point_table.csv`: filtered design or steady state table derived from the ledger.
6. `design_to_dynamic_map.csv`: mapping from steady variables to dynamic states, initial conditions, lookup tables, and logged signals.
7. `initial_condition_audit.csv`: relevant integrators, delays, memories, transfer functions, thermal capacities, volume states, rotor states, and controller states.
8. `validation_report.md`: mass, species or element, energy, pressure, phase/composition, dynamic initialization, constraints, and source-provenance checks.

If the user only asks for a quick answer, provide reduced versions of these artifacts in Markdown and state which gates remain open.

## Reference Selection

Load only the references needed for the current task:

- For intake and staged workflow, read `references/workflow-and-scope.md`.
- Before writing component equations, read `references/thermodynamic-node-stream-ledger.md` and `references/component-contracts.md`.
- For compact blank artifact templates, read `references/artifact-templates.md`.
- Before adding dynamic states or Simulink blocks, read `references/dynamic-initialization.md`.
- Before generating or reviewing a Simulink implementation, read `references/simulink-implementation-standards.md`.
- Before claiming completion, read `references/validation-and-deliverables.md`.
- When testing this skill or preparing external review, read `references/skill-validation-tasks.md`.

## Modeling Discipline

Before writing or changing code, state:

- task goal;
- known facts;
- necessary assumptions;
- missing data;
- verification standard.

Also state whether the chosen topology has enough physical authority for any proposed control variable. A controller cannot regulate a variable through an actuator, heat source, shaft, load, or storage term that is absent from the selected topology.

Keep units explicit. Do not mix Pa, kPa, MPa, kg/s, kmol/s, mol fraction, mass fraction, vapor quality, power, heat rate, and stored energy based only on variable names.

When source formulas are missing, use literature, standards, project documents, or explicitly marked assumptions. Do not hide guessed thermodynamic properties, kinetics, maps, or losses inside tuning constants.

## Output Expectations

For thermal-machinery modeling tasks, produce artifacts another engineer or AI can audit:

- topology and stream-routing description;
- thermodynamic node and stream ledger;
- component contracts;
- state-point table;
- mass/species/energy/pressure residuals;
- dynamic-state and initial-condition registry;
- design/steady/dynamic comparison;
- open assumptions and required user decisions.

For domain-specific systems, defer specialized equations to the relevant skill or source. This skill supplies the modeling discipline and validation gates.
