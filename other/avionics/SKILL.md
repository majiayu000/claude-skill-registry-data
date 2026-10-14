---
name: avionics
description: "Use when a task concerns avionics and flight software assurance for civil aircraft: guide the router to the avionics pack, whose DO-178C software lifecycle sub-skills cover planning, development, verification, and configuration management, whose DO-254 sub-skills cover airborne electronic hardware planning and verification, whose DO-330 tool-qualification sub-skill covers software tool credit, whose DO-160 environmental-qualification sub-skill covers equipment test conditions, and whose far-cs25 airworthiness sub-skill covers the transport-category certification basis. This pack is the airborne software and hardware certification spine. Trigger: avionics, airborne software, flight software, DO-178C, DO-254, DO-330, DO-160, airborne electronic hardware, airworthiness certification, software levels, tool qualification, environmental qualification."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-178c
    reference-only: true
  - id: do-254
    reference-only: true
  - id: do-330
    reference-only: true
  - id: do-160
    reference-only: true
  - id: far-25
    reference-only: true
  - id: cs-25
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; router/entry point for the avionics domain pack"
metadata:
  domain: avionics
  tags: []
  version: 0.1.0
  author: Aero Agent Skills
---

# Avionics domain pack (router)

Route here when the task is avionics and flight software assurance for
civil aircraft. This pack is the certification spine for airborne
software and hardware.

## Domain

Avionics and flight software assurance: airborne software lifecycle
certification (DO-178C), software tool qualification (DO-330),
airborne electronic hardware design assurance (DO-254),
environmental qualification (DO-160), and transport-category
airworthiness certification (FAR-25/CS-25).

## Sub-skills in this pack

| Path | Skill | When to route to it |
|---|---|---|
| avionics/do178c/planning | DO-178C planning | software level/DAL, PSAC, planning artifacts |
| avionics/do178c/development | DO-178C development | requirement-to-code traceability, derived requirements |
| avionics/do178c/verification | DO-178C verification | structural coverage, MC/DC, independence |
| avionics/do178c/software-testing | DO-178C software testing | requirements-based test case generation, MC/DC test case count, coverage objectives per level |
| avionics/do178c/configuration-management | DO-178C configuration management | baselines, problem reports, release gate |
| avionics/do178c/tool-qualification | DO-330 tool qualification | TQL per tool criterion, tool credit, TOR |
| avionics/do178c/airworthiness-liaison | DO-178C airworthiness liaison | certification basis coverage, SOI audits, open items |
| avionics/do160/environmental-qualification | DO-160 environmental qualification | test matrix per equipment category, temperature/vibration/EMC |
| avionics/do160/lightning-protection | DO-160 lightning protection | section 22 induced transients, lightning protection zones |
| avionics/do160/electrostatic-discharge | DO-160 electrostatic discharge | section 25 ESD air discharge level, 150 pF / 330 ohm generator model, test point applicability |
| avionics/do160/radio-frequency-susceptibility | DO-160 RF susceptibility | RS103 radiated immunity, CS114 conducted immunity, field strength |
| avionics/do160/power-input | DO-160 power input | section 16 voltage limits, sag/surge transients, frequency tolerance |
| avionics/do254/hardware-planning | DO-254 hardware planning | simple vs complex AEH, PHAC |
| avionics/do254/hardware-verification | DO-254 verification | verification methods per AEH class, independence, coverage |
| avionics/do254/hardware-configuration-management | DO-254 configuration management | baselines, ECR/ECO, change class, hardware configuration index |
| avionics/do254/requirements-capture | DO-254 requirements capture | requirement characteristics, derived requirements, trace links |
| avionics/far-cs25/airworthiness | FAR-25/CS-25 airworthiness | certification basis, means of compliance, 25.1309 |
| avionics/far-cs25/special-conditions | FAR-25/CS-25 special conditions | novel design features, FAR 25.17, special-condition scope |
| avionics/flight-management/flight-planning | FMS flight planning | great-circle track distance, waypoints, leg geometry |
| avionics/flight-management/vertical-navigation | FMS vertical navigation | top of descent, descent gradient, altitude constraints, VNAV path |
| avionics/data-bus/arinc429-protocol | ARINC 429 protocol | ARINC 429 word format, octal label, SDI, BNR, BCD, SSM, odd parity, 12.5 or 100 kbps, transmitter receiver topology |
| avionics/data-bus/mil-std-1553 | MIL-STD-1553 data bus | command word, remote terminal, bus controller, Manchester II, dual redundant bus, message format |
| avionics/data-bus/arinc664-afdx | ARINC 664 AFDX network | virtual link, BAG, frame size, jitter, end system, switched ethernet, latency |
| avionics/ima/ima-partitioning | IMA partitioning | ARINC 653 partition, major frame, partition schedule, sampling port, queuing port, inter-partition communication, health monitoring |
| avionics/ima/do297 | IMA architecture and acceptance | integrated modular avionics, DO-297, module acceptance, incremental certification, partition allocation, resource budget, CPU memory I/O, integrity requirements, IMA architecture, shared resources |
| avionics/flight-management/performance-computation | Performance computation | FMS performance, cost index, ECON, cruise Mach, step climb, top of descent, fuel time trade, VNAV |
| avionics/fsw/cfs-architecture | Cfs Architecture | cFS, core flight software, cFE, OSAL, PSP, software bus, publish subscribe, app skeleton, telemetry pipeline. |
| avionics/fsw/fprime-component | F Prime component | F Prime, F-prime component framework, topology, rate group, command dispatch, port connection |
| avionics/do160/radio-frequency-emissions | RF emissions (DO-160 sec 21) | radio frequency emissions, DO-160 section 21, conducted emissions, radiated emissions, CE102, RE102, emission limit, emission margin, dBuV, dBuV/m, EMC qualification |
| avionics/flight-management/lateral-navigation | Lateral navigation (LNAV) | lateral navigation, LNAV, cross-track error, track angle error, great-circle track, turn anticipation, fly-by waypoint, fly-over waypoint, intercept heading, FMS lateral guidance |
| avionics/flight-management/radio-navigation-aids | Radio navigation aids | VOR radial, DME slant range, ILS localizer deviation, glideslope deviation, radio navigation geometry, bearing to the navaid station, approach course offset |
| avionics/flight-management/rnp-anp-containment | RNP/ANP containment | required navigation performance, actual navigation performance, RNP containment, ANP comparison, lateral position error sigma, 95 percent containment, performance based navigation |
| avionics/flight-management/rta-time-control | RTA time control | required time of arrival, RTA time constraint, speed adjustment, arrival window, time error, 4D trajectory, FMS time control |
| avionics/surveillance/tcas-resolution-advisory | TCAS resolution advisory | TCAS II, traffic alert and collision avoidance, resolution advisory, modified tau, DMOD, sensitivity level, intruder threat logic, climb descend advisory |
| avionics/surveillance/ads-b-surveillance | ADS-B surveillance | ADS-B, ADS-B Out, ADS-B In, extended squitter, NIC containment radius, NACp accuracy, SIL integrity, ADS-B range |
| avionics/surveillance/airborne-weather-radar | Airborne weather radar | weather radar tilt, reflectivity rainfall, Marshall-Palmer, echo level, ground clutter check |

| avionics/do178c/data-control-coupling-analysis | Data and control coupling (DO-178C) | data coupling analysis, control coupling analysis, shared variable pairs, coupling coverage evidence, level A objectives |
| avionics/fsw/real-time-scheduling | Real-time scheduling | rate monotonic scheduling, response time analysis, earliest deadline first, Liu Layland bound, CPU utilization, fixed priority schedulability |
| avionics/flight-management/radius-to-fix-leg | Radius-to-fix leg | radius to fix leg, RF leg, RNP AR procedure, turn center, arc length, path terminator, flyable arc check |
| avionics/do178c/previously-developed-software | Previously developed software | previously developed software, PDS qualification, software reuse credit, delta objective analysis, modified software scope, reuse classification |

| avionics/data-bus/arinc429-bus-loading | ARINC 429 bus loading | ARINC 429 bus loading, label rate budget, percent utilization, word rate capacity, transmit schedule headroom |
| avionics/data-bus/mil-std-1553-bus-loading | MIL-STD-1553 bus loading | MIL-STD-1553 bus loading, 1553 minor frame load, wire word time, 1553 bus utilization, bc-rt message overhead, schedule headroom |
| avionics/flight-management/holding-pattern-entry | Holding pattern entry | holding pattern entry, direct teardrop parallel entry sector, outbound leg timing, holding wind correction, entry lap time |
| avionics/fsw/shared-resource-access-control | Shared resource access control | shared resource access control, priority ceiling protocol, priority inheritance, worst case blocking, stack resource policy, blocking time bound, schedulability with blocking |
| avionics/flight-management/dme-arc-leg | DME arc leg | dme arc leg, VOR DME arc, arc length in nautical miles, arc bank angle, radial intercept, arc chord, DME radius |
| avionics/flight-management/rhumb-line-leg | Rhumb line leg | rhumb line leg, constant course leg, Mercator course, parallel leg length, rhumb versus great circle, long range leg, FMS leg geometry |

| avionics/fsw/aperiodic-server-scheduling | Aperiodic server scheduling | aperiodic server scheduling, sporadic server, deferrable server, polling server, server capacity, aperiodic response time, fixed priority aperiodic service |

| avionics/fsw/deadline-monotonic-scheduling | Deadline Monotonic Scheduling | deadline-monotonic-scheduling, constrained-deadline-rta, arbitrary-deadline-rta, release-jitter-rta, dm-priority-assignment, shorter-deadline-order |
| avionics/fsw/mixed-criticality-scheduling | Mixed Criticality Scheduling | mixed-criticality-scheduling, amc-rtb-analysis, dual-criticality-execution-time, hi-criticality-mode-rta, lo-criticality-mode-rta, criticality-mode-change-rta |
| avionics/fsw/virtual-deadline-scheduling | Virtual Deadline Scheduling | virtual-deadline-scheduling, edf-vd, virtual-deadline-scaling, dual-criticality-schedulability, mode-switch-feasibility |
| avionics/fsw/cyclic-executive-scheduling | Cyclic Executive Scheduling | cyclic-executive-scheduling, time-triggered-frame-schedule, hyperperiod-major-cycle, frame-length-admissibility, per-frame-capacity, frame-table-slack |
## Routing guidance

- Software certification questions (levels, PSAC, coverage, traceability,
  baselines) route to the DO-178C sub-skills.
- Requirements-based test case generation and structural coverage
  measurement questions (MC/DC t- Cfs questions route to the fsw cfs-architecture sub-skill.
est case count, coverage objectives per
  level) route to the DO-178C software-testing sub-skill; verification
  process questions (reviews, analyses, independence) stay with the
  verification sub-skill.
- Tool credit and qualification questions route to the DO-330 sub-skill.
- Environmental test questions (temperature, vibration, EMC, lightning,
  RF immunity) route to the DO-160 sub-skills.
- Electrostatic discharge questions (section 25 air discharge level,
  150 pF / 330 ohm generator model, discharge counts, test point
  applicability from personnel accessibility) route to the DO-160
  electrostatic-discharge sub-skill, not to lightning-protection or
  power-input.
- Power-input questions (section 16 voltage limits, sag/surge transients,
  frequency tolerance, emergency power) route to the DO-160 power-input
  sub-skill.
- Hardware assurance questions (AEH classification, PHAC, verification,
  requirements capture) route to the DO-254 sub-skills.
- Hardware configuration and change-control questions (baselines,
  ECR/ECO, HCI) route to the DO-254 configuration-management sub-skill.
- Type-certification basis questions (FAR-25 vs CS-25, 25.1309) route to
  the far-cs25 airworthiness sub-skill.
- Novel-feature questions (special conditions, FAR 25.17, equivalent
  safety) route to the far-cs25 special-conditions sub-skill.
- FMS route questions (waypoints, leg geometry, TOD, VNAV constraints)
  route to the flight-management sub-skills.
- ARINC 429 word encoding and decoding, octal label, SDI, BNR and BCD
  data fields, SSM, and odd parity questions route to the data-bus
  arinc429-protocol sub-skill.
- System-level engineering and safety questions route to the
  systems-engineering-safety pack instead.
- MIL-STD-1553 command word encoding, remote terminal and bus controller architecture, Manchester II, and dual redundant bus questions route to the data-bus mil-std-1553 sub-skill.
- ARINC 664 AFDX virtual link bandwidth, BAG, jitter, end-to-end latency, and switched network configuration questions route to the data-bus arinc664-afdx sub-skill.
- ARINC 653 partition scheduling, major frame feasibility, sampling and queuing ports, and IMA health monitoring questions route to the ima ima-partitioning sub-skill.
- Integrated modular avionics architecture planning, partition allocation with resource budgets, and module acceptance criteria route to the ima do297 sub-skill.
- FMS performance computation, cost index and ECON cruise speed, fuel-time trade, step-climb logic, and VNAV top-of-descent questions route to the flight-management performance-computation sub-skill.
- DO-160 section 21 conducted and radiated emission limits, CE102 and RE102 margins, and dBuV emission checks route to the do160 radio-frequency-emissions sub-skill.
- LNAV lateral guidance, cross-track error, track angle error, great-circle track, turn anticipation, and fly-by and fly-over transition questions route to the flight-management lateral-navigation sub-skill.
- RTA time control questions (required time of arrival, rta time constraint, speed adjustment, arrival window, time error, 4d trajectory, fms time control) route to the rta-time-control sub-skill.
- TCAS II threat detection, modified tau, DMOD, and resolution advisory sense questions route to the surveillance tcas-resolution-advisory sub-skill.
- Weather radar operating questions (antenna tilt to cell top, reflectivity rainfall Z-R, echo level, ground clutter check) route to the surveillance airborne-weather-radar sub-skill.
- ADS-B equipage and reception questions (ADS-B Out, extended squitter, NIC containment radius, NACp accuracy, SIL integrity, ADS-B range) route to the surveillance ads-b-surveillance sub-skill.

- Data and control coupling analysis questions (inter-component shared variable pairs, call edge coupling, level A coupling coverage evidence) route to the do178c data-control-coupling-analysis sub-skill.

- Real-time scheduling feasibility questions (rate monotonic, response time analysis, earliest deadline first, Liu-Layland bound) route to the fsw real-time-scheduling sub-skill.
- Radius-to-fix (RF) leg construction questions (turn center, arc length, exit track, RNP AR flyable arc) route to the flight-management radius-to-fix-leg sub-skill.

- DO-178C previously developed software reuse questions (reuse classification, delta objective coverage, modified software regression scope) route to the do178c previously-developed-software sub-skill.
- ARINC 429 bus loading questions (per-label rate schedule, percent utilization of the 100 kbps link, capacity and headroom) route to the data-bus arinc429-bus-loading sub-skill.

- Time-triggered cyclic executive scheduling questions (hyperperiod frame table, admissible frame length dividing every task period, per-frame capacity, FITS or no-admissible-frame verdict) route to the fsw cyclic-executive-scheduling sub-skill; priority-driven feasibility (RM bound, RTA, EDF, AMC-rtb, EDF-VD) stays with the fsw real-time-scheduling family.

## Install

To install only this pack, copy or symlink each leaf folder above into
your host's skills directory (see README Install for per-host commands).
- F Prime component and topology questions route to the fsw fprime-component sub-skill.
- VOR radial, DME slant range, ILS localizer and glideslope deviation geometry questions route to the flight-management radio-navigation-aids sub-skill.
- RNP/ANP containment, actual navigation performance versus required navigation performance, and 95 percent lateral error checks route to the flight-management rnp-anp-containment sub-skill.
- MIL-STD-1553 bus loading questions (minor frame wire-word time budget, percent utilization, 80 percent loading guideline verdict) route to the data-bus mil-std-1553-bus-loading sub-skill, not to the 1553 protocol leaf.

- Holding pattern questions (direct, teardrop and parallel entry classification from the approach angle, outbound leg timing from altitude, 1-in-60 wind-corrected outbound heading) route to the flight-management holding-pattern-entry sub-skill.
- Shared-resource blocking questions (priority ceiling protocol ceilings, worst-case blocking from lower-priority critical sections, response-time analysis with the blocking term, stack-resource-policy schedulability) route to the fsw shared-resource-access-control sub-skill.
- Constant-DME arc questions (arc length between radials, bank angle to hold the arc, point on the arc, chord between arc fixes) route to the flight-management dme-arc-leg sub-skill.
- Aperiodic/event-driven job service questions (sporadic server, deferrable server, polling server capacity and period, server budget replenishment, aperiodic worst-case response time) route to the fsw aperiodic-server-scheduling sub-skill.
- Deadline-monotonic and constrained/arbitrary-deadline response-time questions (deadline-monotonic priority assignment, shorter-deadline order, per-task relative deadlines, release jitter in the response-time iteration) route to the fsw deadline-monotonic-scheduling sub-skill; classic implicit-deadline periodic feasibility stays with real-time-scheduling.
- Mixed-criticality scheduling questions (AMC response-time analysis with a dual-criticality execution-time estimate per task, hi- and lo-criticality-mode response times, criticality mode change) route to the fsw mixed-criticality-scheduling sub-skill; single-execution-time implicit-deadline feasibility stays with real-time-scheduling.
- Virtual-deadline scheduling questions (EDF-VD virtual deadline scaling factor, dual-criticality schedulability under virtual deadlines, mode-switch feasibility) route to the fsw virtual-deadline-scheduling sub-skill; AMC-rtb fixed-priority analysis stays with mixed-criticality-scheduling.
- Constant-course rhumb-line leg questions (Mercator course, rhumb distance, along-parallel leg length, rhumb versus great-circle delta for long legs) route to the flight-management rhumb-line-leg sub-skill.
