---
name: fprime-component
description: "Use when designing or reviewing an F Prime topology, checking opcode and port-type consistency, or generating the component scaffold manifest. Model and validate a NASA JPL F Prime (F´) flight software component architecture: define components as active, queued or passive, attach typed input and output ports plus serial interfaces, register commands with unique opcodes, declare telemetry channels and severity-flagged events, connect producer outputs to consumer inputs across a topology, schedule component input ports in rate groups, and run a deterministic clocked dispatch simulation that records invocations, deliveries, command log entries and telemetry samples with per-channel sequence counters. Produces the validated component model, the connection and rate group report, and a scaffold manifest for code generation. Trigger: F Prime, F´, component framework, topology, rate group, command dispatch, telemetry channel, port connection, flight software modeling."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-178c
    reference-only: true
gated: false
domain: avionics
pack: fsw
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: fsw
  tags: [fprime-component, active-component, queued-component, passive-component, typed-port, command-opcode, rate-group, telemetry-channel]
  version: 0.1.0
  author: Aero Agent Skills
---

# F Prime Component Framework (avionics/fsw/fprime-component)

Use when the task is NASA JPL F Prime (F´) flight software architecture:
component kinds, typed input and output ports, command registration by
opcode, telemetry channels, severity-flagged events, the topology that
connects components, or the rate group schedule that drives them. The
module validates a component model and runs a deterministic clocked
dispatch simulation in pure Python: you define components, connect
producer outputs to consumer inputs, schedule input ports in rate
groups, and the simulation records invocations, deliveries, commands
and telemetry samples with sequence counters, then expands any clean
definition into a scaffold manifest for code generation. F´ is NASA
JPL open-source flight software (github/nasa/fprime, Apache-2.0), a
typed-port framework; the sibling avionics/fsw/cfs-architecture leaf
models NASA cFS, the publish/subscribe software bus framework. The two
mechanisms differ: cFS routes messages by message ID over a central
bus, F´ invokes typed ports along direct point-to-point connections
scheduled by rate groups.

## Domain quick reference

- Component kinds: an active component owns a thread and a message
  queue, so the framework dispatches it; a queued component owns a
  queue without a thread, so its input invocations are dispatched in
  arrival order by the clocked framework; a passive component owns
  neither, so its handlers run inline in the caller context.
- Ports: typed input and output ports carry one payload type from the
  supported set U8/U16/U32/I32/F32/F64/string; an input port may
  declare data_type "serial", a serial interface whose dynamic payload
  matches any partner type. Connections run output to input only.
- Dispatch drivers: every input port of an active or queued component
  must be dispatched by exactly one driver, either one incoming
  connection (data-driven) or membership in exactly one rate group
  (time-driven). A port with zero drivers is orphaned; more than one
  is double dispatch. Passive input ports run inline, so a passive
  port invoked by two rate groups only warns (two timing contexts),
  and a passive port nothing calls is dead code (warning).
- Active rule: an active component must declare at least one input
  port, because the framework can only dispatch it through an input.
  Queued components may be pure command sinks.
- Commands: registered per component with unique opcodes in
  0x0000..0xFFFF and dispatched asynchronously on the command path,
  which requires a queue; passive components must not declare
  commands. Components receive commands by name or opcode.
- Telemetry: declared channels carry typed samples; the simulation
  stamps a monotonic sequence counter per channel, so the ground can
  detect dropped samples. Events carry an F´ style severity from
  (FATAL, HIGH, LOW, INFO, DEBUG).
- Rate groups: a group ticks its listed input ports every period
  derived from base_hz / hz master clock ticks. The master clock runs
  at the fastest declared group rate by default (base_hz = max hz).
- Scaffold manifest: generate_manifest expands a clean definition into
  the class name, header guard, port method stubs, command dispatch
  entries and telemetry channel list a developer would codegen from.
  This proves the model; it is not full F´ code generation.

## Workflow

1. Classify each software unit: active when it needs its own dispatch
   thread, queued when it buffers async input work, passive when it is
   pure logic called inline. Build definitions with
   validate_component (or the component() builder) and fix every
   issue: missing name, unsupported kind, duplicate port names,
   duplicate command opcodes or names, telemetry types outside the
   supported set, event severities outside FATAL/HIGH/LOW/INFO/DEBUG,
   an active component with no input port, or a passive component
   that owns commands.
2. Connect the topology with conn() and validate_connections: every
   connection must run output to input, both ends must exist, data
   types must match (serial interfaces match anything), and self-loops
   are rejected.
3. Schedule dispatch with rate_group() and validate_rate_groups:
   list the input port each group ticks at its hz rate, then check
   the (issues, warnings) pair. Every active or queued input port must
   have exactly one dispatch driver; passive ports invoked from two
   groups or invoked by nothing warn.
4. Run the umbrella check validate_topology over all three artifacts;
   a clean verdict means issues and warnings are both empty (or only
   warnings when passive timing is accepted).
5. Simulate deterministically: build Simulation(defs, connections,
   rate_groups), call run(cycles) for the master clock, then read
   invocations (rate group dispatches), deliveries (connection data
   flow), samples (telemetry with per-channel sequence counters),
   command_log and event_log. Deliver commands with send_command and
   raise declared events with raise_event; record extra telemetry with
   record_telemetry.
6. Codegen from a clean definition: generate_manifest returns the
   scaffold files (model text, header, implementation) plus the
   structured class name, header guard, stubs, dispatch entries and
   channel list.
7. Confirm the deterministic checks with the contract test
   scripts/test_fprime_component.py.

## Worked example

A 1 Hz topology: active SignalGen ticks its run input at 1 Hz and
emits a U32 ramp on tlmOut; queued DataLogger receives each value on
logIn and logs it to telemetry.

```python
import fprime_component_logic as fprime

sg = fprime.component("SignalGen", "active",
    ports=[{"direction": "input", "name": "run", "data_type": "U32"},
           {"direction": "output", "name": "tlmOut", "data_type": "U32"}],
    commands=[{"name": "reset", "opcode": 0x01}],
    events=[{"name": "fault", "severity": "HIGH"}])
dl = fprime.component("DataLogger", "queued",
    ports=[{"direction": "input", "name": "logIn", "data_type": "U32"}],
    telemetry=[{"name": "logIn", "type": "U32"}])

defs = [sg, dl]
conns = [fprime.conn("SignalGen", "tlmOut", "DataLogger", "logIn")]
groups = [fprime.rate_group("1Hz", 1.0, [("SignalGen", "run")])]

fprime.validate_topology(defs, conns, groups)
# {'issues': [], 'warnings': []}
```

Simulation over three master cycles, base clock 1 Hz:

```python
sim = fprime.Simulation(defs, conns, groups)
sim.run(3)
[(i["cycle"], i["comp"], i["port"]) for i in sim.invocations]
# [(0, 'SignalGen', 'run'), (1, 'SignalGen', 'run'), (2, 'SignalGen', 'run')]
[(d["cycle"], d["to_comp"], d["value"]) for d in sim.deliveries]
# [(0, 'DataLogger', 0), (1, 'DataLogger', 1), (2, 'DataLogger', 2)]
[(s["cycle"], s["channel"], s["value"], s["seq"]) for s in sim.samples]
# [(0, 'logIn', 0, 0), (1, 'logIn', 1, 1), (2, 'logIn', 2, 2)]
sim.send_command("SignalGen", "reset")
# {'cycle': 3, 'comp': 'SignalGen', 'name': 'reset', 'opcode': 1}
```

Negative checks: registering a second command with opcode 0x01 raises
the issue "duplicate command opcode 0x0001 (commands 'reset' and
'reboot')"; retyping DataLogger.logIn as F32 raises "connection type
mismatch 'SignalGen.tlmOut' (U32) -> 'DataLogger.logIn' (F32)".

Manifest for SignalGen:

```python
m = fprime.generate_manifest(sg)
m["class_name"]       # 'SignalGenComponent'
m["header_guard"]     # 'SIGNALGEN_COMPONENT_HPP'
[f["path"] for f in m["files"]]
# ['SignalGen.fpp', 'SignalGenComponentBase.hpp', 'SignalGenComponentBase.cpp']
```

## Verification checklist

- Every active component declares at least one input port; passive
  components declare no commands; command opcodes are unique and in
  0x0000..0xFFFF; telemetry types and event severities come from the
  supported sets.
- Every connection runs from a declared output to a declared input
  with matching data types (serial matches any); no dangling
  components or ports; no self-loops.
- Every active and queued input port has exactly one dispatch driver:
  one incoming connection or one rate group. A passive input port in
  two rate groups, or in none, warns.
- Simulation construction raises ValueError listing every topology
  issue, so the clocked loop only ever runs over a clean model.
- run(cycles) is deterministic: invocations and deliveries are
  recorded in schedule order, emitted output values equal the master
  cycle index, and telemetry samples carry a monotonic per-channel
  sequence counter.
- ValueError rejections: Simulation on an invalid topology,
  send_command to an unknown component, unknown command, unknown
  opcode, or a passive component, raise_event on an undeclared event,
  record_telemetry on an undeclared channel or a value that does not
  fit the declared type, and generate_manifest on an unclean
  definition.
- generate_manifest expands a clean definition only, and its header
  guard, port stubs, opcode entries and channel list match the
  definition exactly.

## Pitfalls

- Mixing up the component kinds: an active component owns a thread
  and message queue, a queued component owns a queue without a
  thread, and a passive component runs its handlers inline in the
  caller context - the framework requires every active component to
  declare at least one input port (it can only be dispatched through
  an input) and forbids commands on passive components, whose
  handlers have no queue to receive them.
- Breaking command uniqueness: opcodes must be unique per component
  in 0x0000..0xFFFF and names unique too - registering a second
  command at opcode 0x01 raises the "duplicate command opcode
  0x0001" issue naming both commands, and components receive commands
  by name or opcode, so a collision silently routes to the wrong
  handler.
- Connecting ports carelessly: connections run output to input only,
  both ends must exist, and the payload types must match - retyping
  DataLogger.logIn as F32 raises the connection type mismatch issue
  against SignalGen.tlmOut (U32), while a "serial" data_type matches
  any partner; self-loops are rejected outright.
- Leaving dispatch drivers ambiguous: every active or queued input
  port needs exactly one dispatch driver, one incoming connection or
  one rate group - zero drivers orphan the port and more than one
  double-dispatches it (both are issues), while a passive port in two
  rate groups or in none only warns, because passive handlers run
  inline.
- Driving the simulation blindly: Simulation construction raises
  ValueError listing every topology issue, send_command rejects
  unknown components, commands, opcodes, and passive components, and
  raise_event or record_telemetry on undeclared targets - or a value
  that does not fit the declared channel type - fails, so the clocked
  loop only ever runs over a clean model.
- Treating the manifest as full code generation: generate_manifest
  expands a clean definition into the scaffold (class name, header
  guard, stubs, dispatch entries, channel list) that proves the
  model - it is not the F´ codegen pipeline, and it refuses unclean
  definitions.

## Behavior contract (gate 3)

The component rules, connection checks, rate group coverage, dispatch
simulation and manifest generator are exercised by the contract test:
scripts/test_fprime_component.py against scripts/fprime_component_logic.py
(stdlib unittest, offline, deterministic). Run:
python3 scripts/test_fprime_component.py

## References

- scripts/fprime_component_logic.py: validate_component,
  validate_connections, validate_rate_groups, validate_topology,
  Simulation, generate_manifest, and the component(), conn(),
  rate_group() builders.
- scripts/test_fprime_component.py: contract test, 35 cases.

## Related skills

- avionics/fsw/cfs-architecture: NASA cFS sibling in the same pack;
  cFS routes messages by message ID over a software bus, F´ invokes
  typed ports along direct connections. Route software bus questions
  there, topology and rate group questions here.
- avionics/do178c/development and avionics/do178c/software-testing:
  F´ flight software is developed and verified under DO-178C; the
  requirements traceability and test case flows start there.
- avionics/ima/ima-partitioning: ARINC 653 partitioning is the
  hardware-level isolation context in which component topologies run
  on integrated avionics platforms.

## Compliance

- Standards referenced, not reproduced: F´ is NASA JPL open-source
  software (Apache-2.0), not a certification standard; this leaf keys
  to do-178c (the governing airborne software standard for flight
  software built on F´) listed reference-only per standards-map.yaml.
- The model implements the F´ component vocabulary in summary form:
  component kinds, ports, commands, telemetry, events, rate groups.
  No proprietary standard text is reproduced.
- compliance: STANDARDS-REF, gated: false.
