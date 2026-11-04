---
name: nhtsa-vehicle
description: "Synthesized reference notes from three US Government vehicle-safety sources: NHTSA Cybersecurity Best Practices for the Safety of Modern Vehicles (updated 2022, final), NHTSA Automated Driving Systems 2.0: A Vision for Safety (2017), and a 16-section selection of 49 CFR Part 571 (FMVSS) pinned at eCFR versioner date 2025-01-01. Use for voluntary vehicle cybersecurity practices, the ADS 2.0 twelve priority safety design elements, and FMVSS occupant protection, brakes/stability/lighting, and fuel/EV integrity requirements. Not ISO 26262, not ASPICE, not ISO/SAE 21434, not UNECE R155/R156, not SAE J3016, and not the full Part 571; the FMVSS material is a selection of vehicle-level minimum performance standards, not a process standard."
---

# NHTSA Vehicle Safety
**Source**: NHTSA (US Department of Transportation) | **Chapters**: 6

## When to use
Use this skill when work touches modern road vehicles in the United States and you need what NHTSA actually publishes: the voluntary 2022 cybersecurity best practices for vehicle makers and their suppliers, the ADS 2.0 safety-design elements for automated driving systems, or the selected FMVSS performance requirements for occupant protection, brakes, stability, lighting, fuel integrity, and electric-vehicle shock protection. It is a synthesized reference for engineers who need the shape and content of these sources quickly, with the pinned FMVSS date stated up front.

**Prerequisites:** none. Plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments**: read the core frameworks below (the cyber guidance's practice structure, the ADS 2.0 twelve priority safety design elements, and the FMVSS selection as vehicle-level minimum performance standards).
- **With a topic**: ask about a practice or requirement directly, e.g. "OTA update security", "operational design domain", "FMVSS 208 occupant crash protection", "EV electrolyte spillage and shock protection".
- **With a chapter number**: `ch02` (cybersecurity practices), `ch03` (ADS safety vision), `ch04` through `ch06` (the FMVSS selection by hazard group).

## Core Frameworks & Mental Models

### Voluntary Cybersecurity Best Practices (2022 Guidance)

NHTSA's 2022 document is non-binding, voluntary guidance organized as a risk-based practice structure, not a management-system standard and not a checklist with pass/fail criteria. Its own structure:

- **General best practices**: leadership priority on product cybersecurity; a risk-based approach tied to the vehicle development process; information sharing across the industry; a security vulnerability reporting program; an organizational incident-response process; and self-auditing of cybersecurity processes.
- **Aftermarket and serviceability**: practices for aftermarket devices and diagnostic service access.
- **Technical best practices**: controlled developer and debugging access on production devices; cryptographic techniques and credential management; vehicle diagnostic functionality; event logs and fleet trend review; protection of wireless paths into the vehicle; and software update processes, including over-the-air updates.

The framing to keep: cybersecurity weaknesses can become safety problems, so the guidance treats the vehicle as a cyber-physical system and encourages each organization to decide how to apply the practices.

### ADS 2.0: Twelve Priority Safety Design Elements

*Automated Driving Systems 2.0: A Vision for Safety* (2017) is voluntary guidance for SAE J3016 Level 3 through 5 ADS. Its core framework is twelve priority safety design elements an entity designing an ADS should address:

1. System safety
2. Operational Design Domain (ODD)
3. Object and Event Detection and Response (OEDR)
4. Fallback (Minimal Risk Condition)
5. Validation methods
6. Human Machine Interface (HMI)
7. Vehicle cybersecurity
8. Crashworthiness
9. Post-crash ADS behavior
10. Data recording
11. Consumer education and training
12. Federal, State, and local laws

Around the elements, the document introduces the **Voluntary Safety Self-Assessment (VSA)** as the entity-produced public artifact, and guidance for States on distinguishing vehicle performance (NHTSA's lane) from licensing and operation (the States' lane). See ch03 for the currency caveat before relying on this as current federal ADS policy.

### FMVSS: Vehicle-Level Minimum Performance Standards

The FMVSS material is a 16-section selection of 49 CFR Part 571, pinned at eCFR versioner date 2025-01-01. FMVSS are **minimum performance requirements for the vehicle (or specified equipment)**: each states what must be achieved under defined applications and test conditions. They are not process standards, not software assurance schemes, and not hazard-analysis methods. The selection groups by hazard:

- **Occupant protection** (ch04): interior impact (201), occupant crash protection (208), seat belt assemblies (209), seat belt assembly anchorages (210), side impact protection (214), ejection mitigation (226).
- **Brakes, stability, and lighting** (ch05): transmission shift position/braking effect (102), windshield defrosting and defogging (103), hydraulic and electric brake systems (105), lighting and reflective devices (108), electronic stability control (126), automatic emergency braking (127), light-vehicle brake systems (135).
- **Fuel integrity, EV, and minimum sound** (ch06): fuel system integrity (301), electric-powered vehicle electrolyte spillage and electrical shock protection (305), quiet-vehicle minimum sound (141).

---

## Chapter Index

| Chapter | Section | Key content |
|---|---|---|
| [ch01](chapters/ch01-nhtsa-vehicle-introduction.md) | Introduction | What the pack is, the three sources, the pinned date, what it refuses |
| [ch02](chapters/ch02-nhtsa-cyber-practices.md) | Cybersecurity practices | Synthesized notes from the 2022 final guidance |
| [ch03](chapters/ch03-nhtsa-ads-vision.md) | ADS safety vision | Synthesized notes from ADS 2.0, with the currency caveat |
| [ch04](chapters/ch04-nhtsa-fmvss-occupant.md) | Occupant protection | FMVSS 201, 208, 209, 210, 214, 226 |
| [ch05](chapters/ch05-nhtsa-fmvss-brakes-lighting.md) | Brakes, stability, lighting | FMVSS 102, 103, 105, 108, 126, 127, 135 |
| [ch06](chapters/ch06-nhtsa-fmvss-fuel-ev.md) | Fuel integrity and EV | FMVSS 301, 305, and 141 (minimum sound for hybrid and electric vehicles) |

## Topic Index

- **ADS safety vision (twelve priority safety design elements, VSA)** → ch03
- **Aftermarket devices and serviceability** → ch02
- **Automatic emergency braking (FMVSS 127)** → ch05
- **Brake systems (FMVSS 105, 135)** → ch05
- **Crashworthiness and post-crash ADS behavior** → ch03
- **Cybersecurity practices (voluntary, 2022 guidance)** → ch02
- **Data recording for ADS** → ch03
- **Electronic stability control (FMVSS 126)** → ch05
- **EV electrical shock protection (FMVSS 305)** → ch06
- **Fuel system integrity (FMVSS 301)** → ch06
- **Incident response and vulnerability reporting (vehicle makers)** → ch02
- **Lighting and reflective devices (FMVSS 108)** → ch05
- **Minimum sound for hybrid and electric vehicles (FMVSS 141)** → ch06
- **Occupant crash protection (FMVSS 208)** → ch04
- **Operational Design Domain (ODD) and OEDR** → ch03
- **Over-the-air and software updates** → ch02
- **Seat belt assemblies and anchorages (FMVSS 209, 210)** → ch04
- **Side impact protection and ejection mitigation (FMVSS 214, 226)** → ch04
- **Transmission shift position and braking effect (FMVSS 102)** → ch05
- **Windshield defrosting and defogging (FMVSS 103)** → ch05

## Supporting Files

None. No glossary, no patterns, no cheatsheet. The pack spec makes these optional and this pack does not need them: the chapters carry the reference content and the Topic Index above routes to them.

## Scope & Limits

**Covers**: the three sources named above, at their stated versions. The cyber material is NHTSA's 2022 final guidance and is **guidance, not a regulation and not a mandate**: it imposes no obligation and has no conformity scheme. The ADS 2.0 material carries a currency caveat: current as of the 2026-09-25 vetting check per `docs/SOURCE-VETTING.md` post-v1.21.0 row (FR action of 2026-07-31); a successor exists in draft; do not treat ADS 2.0 as final federal ADS policy.

**FMVSS**: this pack is a **16-section selection, not all of Part 571**. The FMVSS are **vehicle-level minimum performance standards, not a process standard**: they say what the vehicle must achieve under test, not how to organize engineering work to get there. The selection omits most of Part 571's other bands, including school bus, motorcycle, and heavy-truck specific standards; make no completeness claim for those vehicle classes.

**Not covered, and where to look instead**:
- Functional safety per **ISO 26262**: see the `functional-safety-signpost` skill.
- Automotive process capability per **ASPICE** and cybersecurity engineering per **ISO/SAE 21434**: see the `automotive-signpost` skill.
- Type-approval cybersecurity regulation per **UNECE R155/R156**: see the `automotive-signpost` skill.
- SAE driving-automation level definitions per **SAE J3016**: ADS 2.0 references the levels but this pack does not reproduce the standard; see the `automotive-signpost` skill.

**Third-party material**: the NHTSA sources cite ISO, SAE, and UNECE standards by name. This pack names them and reproduces none of their text; pages carrying verbatim third-party standard text were dropped at build time (see PACK.yaml). The FMVSS text is US Government public domain; the pack restates and synthesizes it rather than reprinting section text.
