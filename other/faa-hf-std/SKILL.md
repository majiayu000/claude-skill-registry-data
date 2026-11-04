---
name: faa-hf-std
description: "Knowledge base from the FAA Human Factors Design Standard (HF-STD-001B, 2016) — the FAA's consolidated human-factors / human-systems-integration design criteria for systems it manages, operates, or maintains. Use for requirement-level design rules on: general human-factors design principles; automation and function allocation; designing equipment for maintenance; displays, controls, and visual indicators; alarms, audio, and voice communications; the computer-human interface (information presentation, coding, interaction styles, windows, dialogue); keyboards, input devices, and workstation/workplace ergonomics; system security, personnel safety, environment, anthropometry, and user documentation; plus intended-use and tailoring guidance. It is a quantified, source-attributed synthesis (heavily citing MIL-STD-1472G, MIL-HDBK-759C, DOD-HFDG-ATCCS, NUREG-0700, NASA-STD-3000, ANSI, OSHA, ISO 9241). Complements nasa-hsi as a parallel HSI tradition from the civil-aviation domain. Scope limits: it is design criteria, NOT an HSI lifecycle/process model (use nasa-hsi, nasa-npr-7123, or dau-se-guidebook for process); it does NOT reproduce the third-party standards it cites; it is FAA-acquisition-oriented (ATC, towers, TRACONs, airway facilities), not a general consumer-UX guide; and it is thin on modern touchscreen/mobile, web, and AI-driven interface patterns and on quantitative human-reliability analysis."
---

<!-- argument-hint: [design topic — automation, displays, controls, alarms, CHI/interface, input device, workstation, anthropometry, safety, environment, documentation, tailoring, or chapter number] -->

# FAA Human Factors Design Standard (HF-STD-001B)
**Source**: FAA (US Government work, approved for public release) | **Chapters**: 9

## When to use
Use this skill when you are specifying, designing, or evaluating the human-facing parts of an FAA-domain system — an air-traffic console, an airway-facility equipment rack, an operator display, an alarm scheme, a computer-human interface, an input device, or a workstation — and you need concrete, citable, quantified human-factors design criteria rather than a process narrative. It is the design-rule layer that sits beneath HSI lifecycle guidance.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the standard's design philosophy, the shall/should and order-of-precedence rules, the controlled vocabulary, and the recurring design moves (quantify the quality, two-layer error handling, reserved color/signal coding, consequence-scaled percentiles, design-for-maintenance).
- **With a topic** — ask about a design area (e.g. "automation authority", "alarm physics", "control-indicator integration", "anthropometric percentiles", "console geometry", "destructive-action confirmation") and route to the chapter via the Topic Index.
- **With a chapter** — `ch02` (automation), `ch04` (displays/controls), `ch05` (alarms/audio), `ch06`–`ch07` (computer-human interface), `ch08` (input devices/workstations), `ch09` (safety/anthropometry/documentation/tailoring).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **Design criteria, not a process model.** HF-STD-001B tells you *what an acceptable design must be* — the millimetres, newtons, decibels, contrast ratios, and percentile rules. It does not tell you *where in the lifecycle* to address human factors. Pair it with `nasa-hsi` (the HSI process layer) — the two interlock at the source level, since many HF-STD rules cite NASA-STD-3000A.

## Core Frameworks & Mental Models

### What the standard is
HF-STD-001B is the FAA's single consolidated reference of human-factors design criteria for systems the agency manages, operates, or maintains. Its defining feature is that it does **not invent** most of its rules: it aggregates and harmonizes prior human-engineering work — military standards (MIL-STD-1472G is the anchor, with MIL-HDBK-759C, MIL-STD-1800A, MIL-HDBK-761A, MIL-STD-411), agency handbooks (DOD-HFDG-ATCCS, NUREG-0700, NASA-STD-3000, UCRL, AFSC, EPRI, DISA), federal regulation (OSHA 29 CFR 1910/1926, FAA Orders), international ergonomics (ISO 9241), and human-factors literature — and re-states each requirement in FAA-applicable language with an explicit bracketed source. Read it as a *curated synthesis with provenance*, tuned to the FAA acquisition lifecycle.

### Reading the standard: three meta-rules
1. **Shall vs should is load-bearing.** A *shall* is binding; a *should* is a recommendation that holds in most cases but may involve trade-offs. Reading the verb is how you know what is contractually owed. Tailoring deliberately turns this dial up or down.
2. **Order of precedence.** Where the standard's text conflicts with a cited reference, the standard governs — but it never overrides applicable law or regulation. For safety and environment, OSHA and FAA health-and-safety provisions take precedence over the military-derived rules.
3. **The bracketed-source ledger.** Every rule carries its origin. That matters for precedence, for currency (at least one cited FAA Order is formally cancelled but still referenced), and for cross-pack linkage (NASA-STD-3000A brackets bridge to `nasa-hsi`).

### The recurring design philosophy
- **Quantify the quality.** "Legible", "reachable", "easy", "safe" all become numbers tied to a perceptual or biomechanical fact and verified against the worst-case condition.
- **The human (and the protective/environmental component) is a subsystem,** integrated technically from the concept phase forward, not bolted on at the end.
- **Two-layer error handling**: *resistance* (make errors hard to commit) plus *tolerance* (limit the damage of those that occur) — complements, never substitutes.
- **User-centered, human-centered.** Automate to support the operator, never to displace command; design within users' abilities; keep the user able to recover and override.
- **Absence is not a signal.** A dark light, a dimmed-off display, or a missing indication must never be the sole carrier of a critical condition.

### Automation framework (ch02)
Automation exists to support the operator. Two hard `shall` anchors: keep the user in command, and never become so automation-dependent that a person cannot recover or run the system by hand. Use the **levels-of-automation ladder** to match authority to task risk (cap high-risk decisions at "suggest, do not execute"); evaluate **function allocation** (manual / partial / full / adaptive); and design against the named failure modes — technology-centered automation, silent automation, mode errors, automation bias, complacency, and manual-skill decay. Build for **trust calibration** (not maximum trust) and engineer the failure path first (failure indication, graceful degradation, accessible override).

### Output and input loop (ch04)
Every display criterion descends from the eye (fovea, acuity, accommodation, dark adaptation) and every control criterion from the hand (reach, strength, dexterity). Display-type selection (flat-panel, large-screen, projection, stereoscopic, HUD, see-through, helmet-mounted) is an explicit engineering choice with when-to-use logic. Controls are systematized across a dozen-plus families, each with dimensions, forces, displacements, and a positive-feedback requirement. A single **reserved color-coding map** (flashing red / red / yellow / green / white / blue) spans displays and indicators. Bind every control to its indicator (proximity, standardized direction-of-movement, instantaneous feedback) and layer error-proofing onto critical controls (barriers, covers, interlocks, dead-man behavior).

### Auditory channel (ch05)
An alarm is an **information system**, not a noise: announce the problem, convey priority and nature, guide the first response, and confirm whether the response worked. Manage alarm load (prioritize, cap at four levels, validate inputs, distinguish *filtering* from *suppression*). For non-verbal alerts, audio is a **redundant pointer** to a visual indication that defines the condition. Hit the **salience window** (loud and distinct but capped and never startling), limit distinct signals (4 absolute / 12 relative), and engineer voice-communication intelligibility as a measured, verified property.

### Computer-human interface (ch06, ch07)
Presentation (ch06) treats the screen as a **scarce attention budget**: minimize information and screen density, match presentation to the task then to the user's scan path, and use **coding as a constrained vocabulary** with hard per-channel capacity caps. Interaction (ch07) is an **interaction stack**: choose the interaction type first (eight named styles against task/system/user-training), then its mechanics, then widgets, then the window system, then the system-level conversation of prompts/feedback/errors. Two motifs dominate: **consistency** (treated as a hard requirement, inconsistency as a defect) and **feedback with recoverability** (every action gets a response; destructive actions get explicit non-Enter confirmation; layered Undo/Cancel/Back).

### Fit: devices, workstations, bodies (ch03, ch08, ch09)
Maintainability (ch03) is designed in by **modular decomposition** with ready access and quantified handling limits, plus poka-yoke assembly and layered hazardous-energy control (interlocks never substitute for lockout/tagout). Input devices and workstations (ch08) are sized by **device-task fit** and a **consequence-scaled percentile convention**. Anthropometry (ch09) runs on the **design-limits approach**: there is no average person, never design to the 50th percentile, never treat one percentile as universal across dimensions, never sum like-percentiles across segments, and always reduce borrowed strength/reach data toward the weakest likely operator. Security, safety, environment, and documentation (ch09) are requirement streams integrated from concept, and **tailoring** is the discipline that makes the whole standard affordable — done early, in detail, by a skilled human-factors practitioner.

---

## Chapter Index

| # | Section(s) | Title | Key content |
|---|-----------|-------|-------------|
| [ch01](chapters/ch01-faa-hf-std-foundations-and-general-design.md) | 1–4 | Foundations: Scope, Definitions, General Design | Lifecycle-wide scope; shall/should; order of precedence; the controlled glossary (alert/caution/advisory/warning, automation taxonomy); the eight general-design themes; the curated-synthesis structure |
| [ch02](chapters/ch02-faa-hf-std-automation.md) | 5.1 | Automation | Keep-the-user-in-command anchors; levels-of-automation ladder; function allocation; trust/complacency/mode errors; information/control/adaptive automation; decision aids; fault management |
| [ch03](chapters/ch03-faa-hf-std-designing-equipment-for-maintenance.md) | 5.2 | Designing Equipment for Maintenance | Equipment decomposition hierarchy; modularization; quantified lift/carry/reach limits; access openings, covers, fasteners, connectors; hazardous-energy control; labeling |
| [ch04](chapters/ch04-faa-hf-std-displays-controls-and-visual-indicators.md) | 5.3–5.4 | Displays, Printers, Controls, and Visual Indicators | Viewing geometry; luminance/contrast/glare; display-type selection; control families; reserved color coding; accidental-actuation prevention; control-indicator integration; accessibility |
| [ch05](chapters/ch05-faa-hf-std-alarms-audio-and-voice-communications.md) | 5.5 | Alarms, Audio, and Voice Communications | Alarm as information system; caution/warning/advisory classes; prioritization, filtering vs suppression; signal physics and the salience window; voice signals; measured voice-communication intelligibility |
| [ch06](chapters/ch06-faa-hf-std-chi-information-presentation.md) | 5.6.1–5.6.6 | CHI: Information Presentation and Coding | Information vs screen density; task-driven layout and scan path; legibility figures; coding capacity caps; reserved color meanings and redundancy; concealed info; dynamic update; graphs and maps |
| [ch07](chapters/ch07-faa-hf-std-chi-interaction-and-dialogue.md) | 5.6.7–5.6.15 | CHI: Interaction, Windows, and Dialogue | Interaction-type selection; menus, function keys, command/query language, direct manipulation; selection model; windows and message-window family; response-time/feedback ladder; error management; log-on security |
| [ch08](chapters/ch08-faa-hf-std-input-devices-and-workplace-design.md) | 5.7–5.8 | Keyboards, Input Devices, Workstation/Workplace Design | Keyboard taxonomy and envelope; pointing-device model, hotspot, button mapping; mouse/joystick/trackball/stylus criteria; touch/OCR/voice; console families; seated/standing workstation ergonomics; accessibility |
| [ch09](chapters/ch09-faa-hf-std-safety-environment-anthropometry-documentation.md) | 5.9–5.13, 6 | Security, Safety, Environment, Anthropometry, Documentation, Tailoring | Security safeguards as subsystem; identification/authentication/authorization; quantified hazard limits; effective temperature and the comfort zone; the design-limits percentile rules; user documentation and IETMs; tailoring discipline |

## Topic Index

- **Accessibility / people with disabilities** → ch04, ch08, ch09
- **Adaptive automation** → ch01, ch02
- **Alarm filtering / suppression** → ch05, ch01
- **Alarms (as information system)** → ch05
- **Alert / caution / advisory / warning classes** → ch05, ch01
- **Anthropometry / percentile selection** → ch09, ch08, ch01
- **Audio signals / salience window** → ch05
- **Authentication / authorization / identification** → ch09
- **Automation (levels, authority)** → ch02
- **Automation bias / complacency** → ch02
- **Coding (color, brightness, shape, size, flash)** → ch06, ch04
- **Color reserved meanings** → ch06, ch04, cheatsheet
- **Command language / query language** → ch07
- **Connectors / fasteners** → ch03
- **Console geometry (wrap-around, stacked, team)** → ch08
- **Contrast / luminance / glare** → ch04, ch06
- **Controls (families, forces, coding)** → ch04
- **Control-indicator integration** → ch04
- **Dead-man control / accidental actuation** → ch04
- **Decision aids** → ch02
- **Design-limits approach** → ch09, ch01
- **Destructive-action confirmation** → ch07
- **Direct manipulation** → ch07
- **Displays (types, selection, geometry)** → ch04
- **Documentation / IETM** → ch09
- **Effective temperature / comfort zone** → ch09
- **Electrical / hazardous-energy safety** → ch09, ch03
- **Error resistance / error tolerance** → ch01, ch02
- **Fault management** → ch02
- **Feedback / response-time ladder** → ch07
- **Function allocation** → ch02
- **General design requirements** → ch01
- **Glossary (controlled vocabulary)** → ch01
- **Hotspot / pointing device** → ch08
- **Input devices (mouse, joystick, trackball, stylus)** → ch08
- **Interaction-type selection** → ch07
- **Interlock / lockout / tagout** → ch03, ch09
- **Keyboards (taxonomy, envelope)** → ch08
- **Levels of automation** → ch02
- **Maintenance (designing equipment for)** → ch03
- **Menus (variants, depth, sizing)** → ch07
- **Mental model (operator's)** → ch02
- **Modular decomposition / unitization** → ch03
- **Mode errors / mode awareness** → ch02
- **Monitoring / vigilance decrement** → ch02
- **Order of precedence** → ch01, ch06
- **Printers** → ch04
- **Reach / strength data reduction** → ch09
- **Screen design / density** → ch06
- **Security safeguards** → ch09
- **Shall vs should** → ch01, ch09
- **Tailoring** → ch09
- **Trust calibration** → ch02
- **Voice communications / intelligibility** → ch05
- **Windows / message windows** → ch07
- **Workstation / workplace design** → ch08

## Supporting Files

- [glossary.md](glossary.md) — key terms (alert classes, automation taxonomy, anthropometric and CHI vocabulary), alphabetical, with chapter references
- [patterns.md](patterns.md) — 16 reusable design techniques (quantify the quality, two-layer error handling, audio-as-pointer, design-for-maintenance, coding vocabulary, consequence-scaled percentiles, tailoring) with When / How / Trade-offs
- [cheatsheet.md](cheatsheet.md) — signal-class and reserved-color tables, coding capacity caps, legibility and keyboard figures, percentile-selection table, hazard limits, and tells-and-smells

---

## Scope & Limits

**Covers**: the design-criteria content of HF-STD-001B (December 30, 2016) — general human-factors design requirements; automation and function allocation; designing equipment for maintenance; displays, printers, controls, and visual indicators; alarms, audio, and voice communications; the computer-human interface (presentation, coding, interaction, windows, dialogue); keyboards, input devices, and workstation/workplace ergonomics; system security, personnel safety, environment, anthropometry and biomechanics, and user documentation; and the intended-use and tailoring guidance of Section 6. All of it synthesized in original words with the standard's bracketed source provenance preserved.

**Does not cover**: an HSI *lifecycle or process model* — this is the design-criteria layer; for process use `nasa-hsi`, `nasa-npr-7123`, or `dau-se-guidebook`. It does **not** reproduce the third-party standards it cites (MIL-STD-1472G, MIL-HDBK series, NUREG-0700, NASA-STD-3000, ISO 9241, OSHA regulations) — those remain their publishers' material and are named, not copied. It is **thin on**: modern touchscreen/gesture/mobile and web interface patterns, AI-driven and adaptive-UI design, and quantitative human-reliability analysis (for HRA-style methods see the system-safety packs). Some cited references are dated, and at least one cited FAA Order is formally cancelled but still referenced in the source — read the bracketed sources critically.

**Jurisdiction / provenance**: a US Government work prepared by the FAA Human Factors Branch, approved for public release with unlimited distribution (public domain). Guidance for FAA acquisition; broadly adoptable by analogy but not a regulation in itself. **Source version**: HF-STD-001B (December 30, 2016).
