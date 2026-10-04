---
name: bdbmediastorm
description: "Use when brainstorming or planning live event technology, show control, and real-time media systems (TouchDesigner, Resolume, grandMA3)."
category: media-eventtech
---

# ⚡ BDB MediaStorm: Live Show & Event-Tech Ideation Engine

> **Domain Scope:** `/bdbmediastorm` is exclusively the brainstorming entry point for **Event Technology, Live Show Control, and Real-Time Performance Systems**. It handles signal routing, hardware limits, network protocols, and real-time graphics engines (TouchDesigner, Resolume, grandMA3, Unreal Engine live production). For media asset creation (video pipelines, timeline assembly), use `godmode-media-creation`. For 3D mesh generation, use `godmode-3d-creation`.

When `/bdbmediastorm` is invoked, you MUST initiate a rigorous multi-agent show-control planning session. Reject standard web-development or static software assumptions: think strictly in terms of **live stage environments, framerate guarantees, latency budgets, physical control protocols, and failover topologies.**

---

## 1. Core Workflow & Multi-Agent Architecture

Ideation must never be performed in isolation. Spawn specialized subagents to analyze the show architecture from opposing technical angles:

### Subagent Roles
1. **"Real-Time Architect"**
   - Focus: TouchDesigner TOP/CHOP pipelines, Resolume clip management, framerate preservation (60fps/120fps lock), Spout/Syphon video sharing, GPU VRAM budgets.
2. **"Show-Control & Protocol Specialist"**
   - Focus: Protocol routing over Ethernet/Serial: OSC network topologies, Art-Net / sACN universe counts, DMX patching, MIDI hardware binding, SMPTE Timecode synchronization.
3. **"Hardware & Failover Engineer"**
   - Focus: Network bandwidth (1GbE/10GbE limits), hardware failover switching, main/backup redundancy, safety blackout chains, signal distribution (SDI, HDMI 2.1, DisplayPort).

---

## 2. Interactive Technical Interview

Before drafting signal flow diagrams or system configs, **invoke the `grill-with-docs` skill** (or `grill-me` when there is no working directory) and run it to completion. Those skills hold the interview protocol — design tree, frontier rounds, numbered questions each with a recommended answer — and it is not restated here.

What this domain adds to that protocol: deeply challenge the user's technical assumptions and hardware readiness. The frontier questions for a show-control build are:

* **Signal & Network Protocols:**
  - What protocols govern data movement? (OSC, Art-Net, sACN, MIDI, SMPTE Timecode, NDI)?
  - How many DMX universes are required, and what is the network subnet architecture?
* **Hardware Constraints & Bandwidth:**
  - What are the GPU/CPU specs of the primary and backup media servers?
  - What is the total video canvas resolution and output count (e.g., 4x 4K @ 60Hz via DisplayPort/SDI)?
  - Are signal paths running via uncompressed video (SDI/HDMI) or networked video (NDI/ST 2110)?
* **Software Integration & Show Control:**
  - Is grandMA3 triggering TouchDesigner via OSC/Art-Net, or is TouchDesigner driving Resolume via Spout/Syphon?
  - How is timecode distributed across audio playback, lighting consoles, and media servers?
* **Failover & Safety Mechanisms:**
  - What is the redundant backup plan if the primary TouchDesigner/Resolume server crashes mid-show?
  - Is there an automated hardware A/B switch or safety blackout macro?

---

## 3. Target Directory & Scaffolding

After aligning on system architecture through the grilling interview:
1. **Confirm Output Directory:** Ask the user: *"In which project directory should the output show-control plan and architecture files be stored?"*
2. **Scaffold Foundational Files:** Once confirmed, write the core show specification files (`agent.md`, `signal-flow.md`, `network-patch.json`, `failover-matrix.md`).

---

## 4. Signal Flow & Architecture Artifacts

The final output of a MediaStorm session must produce:

### A. Signal Flow Diagram (Mermaid.js)
Define hardware and software nodes as strict bounded contexts:
- Protocol paths (OSC, Art-Net, SMPTE)
- Video transport (Spout, Syphon, NDI, SDI)
- Control paths (MIDI, grandMA3 DMX, TouchDesigner CHOPs)

### B. Live Show Ergonomics & Control Panels
- If designing TouchOSC, StreamDeck, or web control panels, enforce high-contrast dark-mode ergonomics suited for live FOH (Front of House) environments.

### C. Redundancy & Failover Matrix
- Document main/backup failover triggers, manual blackout keys, and watchdog ping intervals.

---

## 5. Mandatory — Plan Canvas Review

Before this session concludes, choose the planning mode by running `aos-plan-canvas modes` and presenting available modes to the user (see the "Planning mode choice" section in the `plan-canvas` skill). Then run `aos-plan-canvas open <file> --mode <choice>` against `signal-flow.md` (or the combined show-control spec), then `aos-plan-canvas await <file>` and leave it running. The user reviews the signal flow diagram, hardware topology, and failover matrix in the browser (Mermaid renders live, click-to-annotate, chat rail). Do not consider the show architecture finalized before an `approve` verdict. A `request_changes` verdict means revise the artifact and reopen — it live-reloads. This is a plain CLI tool, identical regardless of which agent harness runs this skill. See the `plan-canvas` skill. If a build follows the approve, Trigger A starts the live map (`agenttrail` skill); `aos-archify` can render the signal flow as a workflow or architecture diagram for the review.

---

## 6. Execution Rules

1. **Strict Focus:** Never include video generation tools (like OpenMontage) or generative 3D modelers (like TRELLIS) here. Keep `/bdbmediastorm` strictly focused on live show control and real-time event technology.
2. **Subagents Mandatory:** Delegate technical feasibility checks to specialized subagents.
3. **No Web-Dev Assumptions:** Force thinking in DMX universes, frame latency, CHOP channels, OSC port bindings, and hardware redundancy.
4. **Hardware Validation:** Always question VRAM, network bandwidth, and physical cabling limits before signing off on an architecture.


## Overview
BDB MediaStorm is the master ideation and brainstorming engine for live show-control and event technology, focusing strictly on hardware constraints, signal routing, and protocol topologies.

## When to Use
- **Trigger:** The user asks to plan a live show, design a hardware topology, or route signals (OSC, DMX, Art-Net) between media servers.
- **Exclude:** Do not use for generating video timelines or 3D meshes.

## Core Process
1. Run `grill-with-docs` (or `grill-me`) to challenge assumptions about protocols, hardware, and bandwidth.
2. Scaffold foundational files (`agent.md`, `signal-flow.md`, `network-patch.json`).
3. Generate a strict Mermaid.js signal flow diagram mapping all protocols.
4. Document a main/backup redundancy and failover matrix.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We can just run NDI over the venue's Wi-Fi for testing." | NDI requires a dedicated gigabit hardwired LAN; Wi-Fi will drop frames and cause stutter. |
| "A 60fps UI is fine, we don't need a strict lock." | Frame drops in show control cause visible desyncs in lighting and video; 60fps lock is mandatory. |
| "I'll skip the blackout macro, it's just a small show." | Every generative live show requires an instant hardware or software safety blackout chain. |

## Red Flags

- Recommending generative video tools (TRELLIS, OpenMontage) during the planning phase.
- Failing to ask about GPU VRAM or network bandwidth limits.
- Designing a TouchDesigner pipeline without explicit frame-latency boundaries or failover paths.

## Verification

- [ ] The grilling interview was completed with answers regarding protocols and bandwidth.
- [ ] Output includes a Mermaid.js signal flow diagram.
- [ ] A dedicated failover/blackout mechanism is documented.

