---
name: cfs-architecture
description: "Use when designing a cFS app, explaining cFS layering, or simulating software bus routing for flight software. Model and simulate NASA core Flight Software (cFS) architecture: explain the cFE/OSAL/PSP layering (Executive Services, Software Bus, Event Services, Table Services, Time Services, File Services), structure apps with the classic APP_Init, APP_Execute, APP_Data pattern, and route messages by 16-bit message ID over a software bus publish/subscribe model, with a pure-Python simulation that registers apps, subscribes to message IDs, publishes payloads, routes queued messages in publish order, stamps telemetry sequence counters, and logs events by severity. Trigger: cFS, core flight software, cFE, OSAL, PSP, software bus, publish subscribe, app skeleton, telemetry pipeline."
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
  tags: [cfs, core-flight-software, cfe, osal, software-bus, publish-subscribe, app-skeleton]
  version: 0.1.0
  author: Aero Agent Skills
---

# cFS Architecture (avionics/fsw/cfs-architecture)

Use when the task is NASA core Flight Software (cFS) architecture: the
cFE/OSAL/PSP layering, the core flight executive (cFE) applications, the
classic app lifecycle pattern, or software bus publish/subscribe routing
by 16-bit message ID. The module simulates the software bus and event
service in pure Python: you register apps, subscribe to message IDs,
publish payloads, route queued messages in publish order, stamp telemetry
sequence counters, and log events by severity.

## Domain quick reference

- cFS is the NASA open-source flight software framework: an application
  platform (cFE), an OS abstraction layer (OSAL), and a board support
  layer (PSP), with flight apps running on top. Layering bottom to top:
  hardware, PSP, OSAL, cFE core, flight apps. cFE 6.x is the reference
  baseline; the project is maintained on GitHub (nasa/cFS, Apache-2.0).
- PSP (Platform Support Package) is the only board-specific layer: CPU
  reset, clock/timer, memory, EEPROM, and console support. One cFE binary
  tree, one PSP per target processor.
- OSAL (OS Abstraction Layer) wraps the real-time OS (RTEMS, VxWorks,
  POSIX) behind one API: tasks, semaphores, queues, timers, mutexes,
  filesystem, network. Apps never call the RTOS directly.
- cFE (core Flight Executive) provides the reusable services:
  - Executive Services (ES): app startup/stop, memory pools, housekeeping
    catalog, reset control.
  - Software Bus (SB): publish/subscribe message routing by message ID,
    the backbone of all inter-app communication.
  - Event Services (EVS): severity-filtered event log for operator and
    FDIR visibility.
  - Table Services (TBL): loadable configuration tables with validation.
  - Time Services (TIME): time source management, time sync messages.
  - File Services (FS): filesystem utilities, file headers, file/disk
    housekeeping.
- Software bus routing: a message ID (16-bit in classic cFS) selects the
  destination. Apps subscribe to message IDs; publishers call
  CFE_SB_SendMsg; SB copies the message to every subscriber's pipe.
  Command traffic occupies 0x0000-0x0FFF, telemetry 0x1000-0xFFFF, by
  convention. Classic cFS packs an app tag in the upper bits and a
  message number in the lower bits, e.g. 0x1900 = app 0x19, message 0x00.
  Modern cFE (6.7+) widened message IDs to 32 bits; see
  references/cfs-architecture-notes.md.
- Classic app lifecycle: every cFS app follows APP_Init, APP_Execute,
  APP_Data. APP_Init runs once (register with ES, subscribe to command
  message IDs); APP_Execute is the per-cycle main-loop body (route
  pending SB messages, run the cycle); APP_Data processes one received
  message or produces the cycle's telemetry. The loop is
  APP_Main: APP_Init(); while(1) { APP_Execute(); }.
- Telemetry convention: each telemetry message carries a sequence counter
  in its header (CFE_SB_TlmHdr.SeqCnt) that increments per message, so a
  ground station can detect dropped packets.
- Event severity levels (CFE_EVS): DEBUG, INFO, EVENT, ERROR, CRITICAL.
  Events are filtered by severity on the ground and by app at runtime;
  a flooded event log is a real operational hazard on orbit.

## Workflow

1. Identify the layer: hardware/PSP, OSAL, cFE service, or flight app.
   Board bring-up and CPU support belong to PSP; RTOS portability
   belongs to OSAL; app design belongs to the cFE service layer.
2. Design each app with the classic lifecycle: APP_Init for one-time
   registration and subscription, APP_Execute for the per-cycle body,
   APP_Data for per-message or per-cycle work.
3. Allocate message IDs: telemetry in 0x1000-0xFFFF, commands in
   0x0000-0x0FFF, one block per app, app tag in the upper bits.
4. Model the bus in the simulation: register_app() every app,
   subscribe(app, msg_id) each consumer, publish(msg_id, payload) each
   producer, then route_messages() to deliver in publish order.
5. Stamp telemetry sequence counters with telemetry_pipeline() so the
   ground station can verify continuity.
6. Log anomalies through the event service: EventLog.log(app, severity,
   message), choosing DEBUG for diagnostics, INFO/EVENT for normal
   milestones, ERROR for recoverable faults, CRITICAL for loss of
   function.
7. Verify the model: run the contract test, then check the event log
   and per-app delivery lists against the expected publish order.

## Worked example

A GNC app publishes attitude telemetry on a schedule; an ACS app and an
EPS app consume different message IDs from the same bus.

```python
import cfs_architecture_logic as cfs

bus = cfs.SoftwareBus()
bus.register_app("ACS"); bus.subscribe("ACS", 0x1900)
bus.register_app("EPS"); bus.subscribe("EPS", 0x1901)

bus.publish(0x1900, {"cmd": "rate_damp"})
bus.publish(0x1901, {"cmd": "battery_charge"})
bus.publish(0x1900, {"cmd": "slew"})
bus.route_messages()

bus.deliveries("ACS")  # [(ACS, 0x1900, rate_damp), (ACS, 0x1900, slew)]
bus.deliveries("EPS")  # [(EPS, 0x1901, battery_charge)] in publish order
```

Telemetry pipeline with sequence counters:

```python
stamped = cfs.telemetry_pipeline(bus, "GNC", 0x1902,
                                 ["quat1", "quat2", "quat3"])
# [(0x1902, "quat1", 0), (0x1902, "quat2", 1), (0x1902, "quat3", 2)]
```

Scheduled telemetry app (publishes every 2 cycles):

```python
gnc = cfs.ScheduledTelemetryApp("GNC", bus, 0x1800, 0x1902, period=2)
bus.register_app("TEL"); bus.subscribe("TEL", 0x1902)
gnc.APP_Init()
for _ in range(5):
    gnc.APP_Execute()
bus.route_messages()  # TEL receives seq 0,1,2 at cycles 0,2,4
```

## Verification checklist

- Every app registers exactly once; duplicate registration raises
  ValueError.
- Every consumer subscribes before any publish to its message ID;
  publishing to an unknown message ID raises ValueError.
- Message IDs are validated as 16-bit (0x0000-0xFFFF); out-of-range or
  non-integer IDs raise ValueError.
- After route_messages(), each app's delivery list contains only its
  subscribed message IDs, in publish order.
- Telemetry sequence counters are monotonic per message ID.
- Event log entries carry a valid severity; unknown severity raises
  ValueError.

## Pitfalls

- Confusing the cFS layers: PSP is the only board-specific layer
  (CPU reset, clock, memory, console), OSAL wraps the RTOS behind one
  API so apps never call it directly, and cFE provides the reusable
  services - board bring-up belongs to PSP, RTOS portability to OSAL,
  and app design to the cFE service layer, so routing an OSAL tasking
  question to the PSP leaf-side model misses the layer.
- Allocating message IDs against the ranges: commands occupy
  0x0000-0x0FFF and telemetry 0x1000-0xFFFF by convention, with the
  app tag in the upper bits and the message number below (0x1900 is
  app 0x19, message 0x00) - and the bus validates IDs as 16-bit, so
  out-of-range or non-integer IDs raise ValueError; note modern cFE
  6.7+ widened message IDs to 32 bits.
- Publishing before the consumer subscribes: every consumer must
  subscribe to its message ID before any publish to that ID, and
  publishing to an unknown message ID raises ValueError - a publisher
  that sends before subscription silently loses the first messages
  for that app.
- Misusing the app lifecycle: APP_Init runs once and does the
  registration and subscription, APP_Execute is the per-cycle body
  that routes pending messages, and every app registers exactly once -
  duplicate registration raises ValueError, and registering or
  subscribing inside the execute loop re-runs one-time work every
  cycle.
- Trusting delivery order or counters without the route: after
  route_messages() each app's delivery list holds only its subscribed
  message IDs in publish order, and telemetry sequence counters are
  monotonic per message ID via telemetry_pipeline() - the ground
  station detects drops from counter gaps, so a stamped pipeline is
  part of the design, not an afterthought.
- Treating the software bus as a network bus: SB routing is in-process
  publish/subscribe by message ID with copies to every subscriber's
  pipe - cross-box cFS traffic rides ARINC 664 / MIL-STD-1553 links
  (the data-bus leaves), and ARINC 653 partitioning is the
  hardware-level isolation sibling, not a message-routing service.

## Behavior contract (gate 3)

The software bus routing, event log, telemetry pipeline, and app
skeleton are exercised by the contract test:
scripts/test_cfs_architecture.py against scripts/cfs_architecture_logic.py
(stdlib unittest, offline, deterministic). Run:
python3 scripts/test_cfs_architecture.py

## References

- scripts/cfs_architecture_logic.py: SoftwareBus, EventLog,
  telemetry_pipeline(), app_skeleton_template(),
  ScheduledTelemetryApp.
- scripts/test_cfs_architecture.py: contract test, 15 cases.
- references/cfs-architecture-notes.md: cFE/OSAL/PSP facts, message ID
  layout, classic vs modern cFE API notes.

## Related skills

- avionics/do178c/planning: cFS flight apps are developed and
  certified under DO-178C; the DAL and PSAC flow starts there.
- avionics/data-bus/arinc664-afdx and avionics/data-bus/mil-std-1553:
  the software bus is in-process message passing, not a network data
  bus; AFDX/1553 carry cFS messages between boxes.
- avionics/ima/ima-partitioning: ARINC 653 partitioning is the
  hardware-level sibling of cFS app isolation.

## Compliance

- Standards referenced, not reproduced: cFS is NASA open-source software
  (Apache-2.0), not a certification standard; this leaf keys to
  do-178c (the governing airborne software standard for cFS flight
  apps) listed reference-only per standards-map.yaml.
- The simulation implements the classic cFE 6.x model; modern cFE API
  differences are noted in references/cfs-architecture-notes.md.
- compliance: STANDARDS-REF, gated: false.
