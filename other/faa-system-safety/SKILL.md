---
name: faa-system-safety
description: "Knowledge base from the FAA System Safety Handbook (Dec 30, 2000). Use for system safety as a specialty within systems engineering: the five-step safety risk management process (mandated by FAA Order 8040.4 and the AMS), the severity-by-likelihood risk matrix and acceptance bands, the Safety Order of Precedence, system-description models (5M, SHEL(L)), the hazard-analysis activities (PHL/PHA/RHA/SSHA/SHA/O&SHA/HHA), integrated system hazard analysis, the analysis techniques (FTA, FMEA/FMECA, Fault Hazard, Common Cause, Sneak Circuit, Energy Trace), closed-loop hazard tracking (Safety Action Record), and the specialty domains the handbook covers — acquisition-lifecycle safety and contracting (OSA/CSA/SSPP/ISSPP), software safety (control-capability ranking, SHCM, DO-178B), test & evaluation safety, facilities safety, commercial launch safety (AST licensing, expected casualty, MPL/DAMP), system safety training, and Operational Risk Management (ORM) with human/organizational factors. Scope limits: this is a year-2000 FAA how-to; it predates the modern FAA/ICAO Safety Management System (SMS) and Just Culture regulatory frameworks, and many cited orders, advisory circulars, and launch-licensing rules have since been restructured. It is FAA/NAS-centric, leans on MIL-STD-882C, and does not define the SE life-cycle processes themselves (use nasa-npr-7123 / dau-se-guidebook) or reproduce third-party standard text (MIL-STD-882, DO-178B, ISO/IEC/IEEE)."
---

<!-- argument-hint: [risk management step, hazard analysis activity, analysis technique, risk matrix, order of precedence, software/launch/facility/ORM domain, chapter number] -->

# FAA System Safety Handbook
**Source**: FAA (US Government work, public domain) | **Chapters**: 7

## When to use
Use this skill to run system safety as a specialty *within* systems engineering: framing safety risk
management around stated acceptance criteria, describing the system, identifying and analyzing
hazards by severity and likelihood, choosing controls down a fixed order of precedence, selecting
the right analytical technique, and tracking every hazard to verified closure. It also covers the
handbook's specialty domains — acquisition-lifecycle safety and contracting, software safety, test
and facilities safety, commercial launch licensing, training, and field-level Operational Risk
Management. It is the FAA's "how-to" companion to the policy in FAA Order 8040.4 and the Acquisition
Management System.

**Prerequisites:** none — plain Markdown; no MCP server, API key, or licence tier needed at runtime.

## How to Use This Skill
- **Without arguments** — load the core frameworks below: the five-step process, the risk matrix,
  the Safety Order of Precedence, the 5M/SHEL(L) models, the hazard-analysis activities, and the
  analysis-technique toolkit.
- **With a topic** — ask about a risk management step, a hazard-analysis activity (PHA, SSHA, SHA,
  O&SHA…), an analysis technique (FTA, FMECA, CCFA, Sneak Circuit, Energy Trace), the risk matrix,
  the order of precedence, or a specialty domain (software, launch, facilities, ORM).
- **With a chapter** — `ch01` (foundations), `ch03` (integrated hazard analysis + activities),
  `ch04` (analysis techniques), `ch07` (ORM and human factors).

Supporting files: `glossary.md`, `patterns.md`, `cheatsheet.md`.

> **One engine, many casings.** The whole handbook runs one loop: describe the system, identify
> hazards, characterize risk by severity and likelihood, control it down the order of precedence,
> verify, and track to closure. Chapters 1–4 establish that engine; chapters 5–7 apply it to
> software, test, facilities, launch, training, and operations.

## Core Frameworks & Mental Models

### What system safety is (FAA framing)

In the FAA's view, system safety is a specialty *within* systems engineering whose job is to support
program risk management — find the risks that matter, then eliminate or control them through design
and procedure, in a defined order of preference, across the whole life cycle. It is made mandatory
by **FAA Order 8040.4** (1998) and carried into acquisition by the **Acquisition Management System
(AMS)**. The handbook is deliberately a "how-to"; the *when/who/why* live in the safety plans it
points to (SSMP / SSPP / ISSPP). Safety is balanced against cost, schedule, and performance — there
is no zero-risk goal; some risk must be accepted, and that is management's decision.

### The five-step safety risk management process

Order 8040.4 frames the discipline as five steps: **Plan** (set the process and fix the
risk-acceptability criteria up front), **Identify** the hazards, **Analyze** them by severity and
likelihood, **Assess** them against the plan's criteria (the Comparative Safety Assessment), and
**Decide** — with management owning the residual risk. Qualitative or quantitative assessment is
allowed, with a stated preference for quantitative; assumptions must be conservative and documented.

### Risk = severity × likelihood → acceptance band

A *hazard* is a condition that could lead to an undesired event; *risk* couples severity of
consequence with likelihood of occurrence, and both must be characterized. The FAA AMS severity
scale runs Catastrophic → Hazardous → Major → Minor → No Safety Effect; the likelihood scale runs
Probable → Remote → Extremely Remote → Extremely Improbable. The two combine in a **Risk
Acceptability Matrix** yielding High / Medium / Low bands — High is tracked until reduced, Medium is
acceptable only with management review, Low needs no further tracking. (MIL-STD-882C renames the
bands R1–R4.) The coupling matters: the more catastrophic the outcome, the lower its allowable
probability — fix severity first, then read across to the probability the design must achieve.

### The Safety Order of Precedence

The fixed hierarchy for treating any hazard: (1) **design for minimum risk** (eliminate by design),
(2) incorporate **safety devices**, (3) provide **warning devices**, (4) develop **procedures and
training**. Procedures/training is the least-preferred option for severe hazards and normally needs
concurrence of authority. For a *fielded* system, redesign is often not cost-effective, so revising
procedures becomes the fastest route — but it only cuts likelihood or severity, it does not remove
the hazard.

### System-description models: 5M and SHEL(L)

Before any risk work, describe the system. The **5M model** decomposes it into Mission, Man,
Machine, Management, and Media; the **SHEL(L) model** uses Software, Hardware, Environment, and
Liveware (human). Both force the analyst to examine every element *and every interface* — interface
matches and mismatches matter as much as the elements themselves. Description trades breadth against
depth: a wide system (the NAS) gets a general description; a narrow component gets a detailed one.

### The hazard-analysis activities (lifecycle order)

Seven design-phase activities run in lifecycle order: **PHL** (early hazard seed list carried into
the RFP) → **PHA** (the foundational analysis, before preliminary design review) → **RHA** (turns
hazards into design requirements) → **SSHA** (component → whole) → **SHA** (whole + interfaces →
subsystem safety) → **O&SHA** (procedurally controlled operation/support, usually completed last) →
**HHA** (hazardous materials). A *proactive* program shapes the design via the PHL before it starts;
a *reactive* one justifies redesign after milestones.

### Integrated system hazard analysis

An accident in a complex system is almost never a single failure, so neither a single technique nor a
single analysis can capture the risk. **Integrated system hazard analysis** logically combines the
separate analyses around human–machine–environment interactions — reasoned integration, not stapled
reports. Risk is a chain: an initiating hazard plus contributory hazards (unsafe acts, unsafe
conditions) leads to a primary catastrophic/critical event. A failed safeguard is itself a hazard.
Reliability and safety are complementary but not interchangeable — a reliability failure rate is
usually too coarse to satisfy a safety requirement.

### The analysis-technique toolkit

Hazards present from two directions, so the techniques are chosen to cover each other's blind spots:
- **Event-driven / top-down (deductive)** — **Fault Tree Analysis (FTA)** maps failure paths down
  from one defined undesired event; **Fault Hazard Analysis** is a safety-focused subset of an FMEA.
- **Consequence-driven / bottom-up (inductive)** — **FMEA / FMECA** walk component failures up to
  their effects; FMECA adds a purpose-specific criticality figure of merit (hardware/software only).
- **Specialty** — **Common Cause Failure Analysis (CCFA)** extends FTA to test whether redundancy is
  real; **Sneak Circuit Analysis** finds latent conditions that misbehave with no component failing;
  **Energy Trace** inventories controlled/uncontrolled energy and seeds fault-tree top events.

Always do the qualitative pass first; quantify only when the value justifies the cost and the limits
of the numbers are explicit. A recurring caution: false precision — chasing exact numbers from
inexact data — is one of the field's biggest pitfalls.

### Closed-loop hazard tracking

Hazard Tracking and Risk Resolution makes risk control a closed loop, gated by explicit management
risk acceptance. The **Safety Action Record (SAR)** carries each hazard's description, causes, initial
and residual risk, suggested and implemented controls, verification and validation, and the
concurrences required to close it. A hazard is closed only after its controls are verified, and
residual risk is knowingly accepted and documented.

### Operational Risk Management (the operational counterpart)

Where the hazard analyses engineer safety *into* a system before it is fielded, **ORM** manages risk
while the system is *operated*, run pre-emptively (e.g., before each flight). It is a six-step loop —
identify, assess, analyze controls, decide, implement, supervise/review — governed by four principles
(accept no unnecessary risk; decide at the level that controls the resources; accept risk only when
benefits outweigh costs; integrate into planning at every level). Match rigor to the situation
(time-critical / deliberate / strategic), drive controls up the user-involvement ladder toward user
ownership, and measure risk directly rather than waiting on accident statistics. The 5M model and the
human-as-most-variable-element framing carry into human factors and organizational data-sharing
(GAIN, FOQA).

---

## Chapter Index

| # | Section | Key content |
|---|---------|-------------|
| [ch01](chapters/ch01-faa-system-safety-foundations-policy-process-principles.md) | Foundations: policy, process, principles | Order 8040.4 / AMS / FAST chain; the five-step process; hazard vs. risk; severity/likelihood scales; the risk matrix and acceptance bands; CSA; the Safety Action Record; cost-vs-safety balance; Safety Order of Precedence; behavioral-based safety; 5M and SHEL(L) |
| [ch02](chapters/ch02-faa-system-safety-acquisition-lifecycle-assessments-contracting.md) | Acquisition lifecycle, assessments & contracting | OSA (OSED/OHA) and CSA; ASOR and the Target Level of Safety; the SSPP as a binding baseline; the ISSPP; tailoring; GFE and COTS/NDI; the specification/SOW/CDRL/bidders'-instructions contract hooks |
| [ch03](chapters/ch03-faa-system-safety-integrated-hazard-analysis-tasks.md) | Integrated hazard analysis & analysis tasks | Integrated system hazard analysis; initiating/contributory hazards; risk as a chain; safety vs. reliability; the seven activities (PHL/PHA/RHA/SSHA/SHA/O&SHA/HHA); qualitative-before-quantitative; FTA mechanics, gates, and cut sets |
| [ch04](chapters/ch04-faa-system-safety-analysis-techniques.md) | Analysis techniques | Fault Hazard Analysis; Fault Tree Analysis (symbology, cut sets); Common Cause Failure Analysis; Sneak Circuit Analysis; Energy Trace; FMECA; the deductive-vs-inductive axis; named pitfalls |
| [ch05](chapters/ch05-faa-system-safety-software-test-facilities-safety.md) | Software, test & facilities safety | The five-step software safety process; Software Safety Working Group; control-capability ranking and the SHCM; DO-178B levels; test as both evidence and hazard; the Facility Acquisition Life Cycle; ORMG; facility risk categories; conformance-is-a-floor |
| [ch06](chapters/ch06-faa-system-safety-launch-safety-and-training.md) | Commercial launch safety & training | AST licensing; expected casualty; Maximum Probable Loss and DAMP; the Validation Acceptance Matrix (analysis/ground test/flight test); the Systematic Software Safety Process; the training method (needs → task → objectives → delivery → learning styles) |
| [ch07](chapters/ch07-faa-system-safety-orm-human-organizational-factors.md) | Operational Risk Management & human/organizational factors | The six-step ORM process and four principles; types-of-risk taxonomy; the 5-M model; three levels of risk management; user-involvement and command-involvement ladders; GAIN, FOQA, ASPRAM; human factors and the Total System Concept |

## Topic Index

- **Acquisition lifecycle / AMS / IPDS** → ch01, ch02
- **ASOR / Target Level of Safety** → ch02
- **Behavioral-based safety / safety culture** → ch01
- **Comparative Safety Assessment (CSA)** → ch02, ch01
- **Common Cause Failure Analysis (CCFA)** → ch04
- **Contracting / SOW / CDRL / specification** → ch02
- **Contributory and initiating hazards** → ch03, ch01
- **Cost-versus-safety balance** → ch01
- **Cut sets / minimal cut sets** → ch04, ch03
- **DAMP / Maximum Probable Loss (MPL)** → ch06
- **Energy Trace** → ch04
- **Expected casualty** → ch06
- **Facilities safety / Facility Acquisition Life Cycle** → ch05
- **Fault Hazard Analysis** → ch04
- **Fault Tree Analysis (FTA)** → ch04, ch03
- **FMEA / FMECA** → ch04, ch03
- **Hazard versus risk** → ch01
- **Hazard analysis activities (PHL/PHA/RHA/SSHA/SHA/O&SHA/HHA)** → ch03
- **Hazard tracking / Safety Action Record (SAR)** → ch01
- **Health Hazard Assessment (HHA)** → ch03
- **Human factors / Total System Concept** → ch07
- **Integrated system hazard analysis** → ch03
- **Launch licensing / AST** → ch06
- **Operational Risk Management (ORM)** → ch07
- **Operational Safety Assessment (OSA / OSED / OHA)** → ch02
- **Order 8040.4 / policy spine** → ch01
- **Preliminary Hazard Analysis (PHA)** → ch03, ch01
- **Preliminary Hazard List (PHL)** → ch03, ch01
- **Reliability versus safety** → ch03
- **Risk matrix / acceptance bands** → ch01
- **Safety Order of Precedence** → ch01, ch03, ch02
- **Severity and likelihood scales** → ch01
- **SHEL(L) model** → ch01
- **Sneak Circuit Analysis** → ch04
- **Software safety / control capability / SHCM** → ch05, ch06
- **Software safety process (five-step)** → ch05
- **System Safety Program Plan (SSPP) / ISSPP** → ch02, ch01
- **Test and evaluation safety** → ch05
- **Training / learning objectives** → ch06
- **Voluntary safety data sharing (GAIN / FOQA / ASPRAM)** → ch07
- **5M model** → ch01, ch07, ch03

## Supporting Files

- [glossary.md](glossary.md) — key system-safety terms, alphabetical, with chapter references
- [patterns.md](patterns.md) — reusable patterns (the five-step process, 5M/SHEL(L) description,
  coupling severity to probability, working the order of precedence, integrated hazard analysis,
  technique selection, software safety, ORM) with When / How / Trade-offs
- [cheatsheet.md](cheatsheet.md) — quick decision rules, the five-step process, the risk matrix, the
  hazard-analysis activities, the technique table, acquisition hooks, and tells & smells

---

## Scope & Limits

**Covers**: system safety as the FAA practiced and taught it in the *System Safety Handbook* (Dec 30,
2000) — the policy spine (Order 8040.4, the AMS), the five-step safety risk management process, the
severity/likelihood scales and Risk Acceptability Matrix, the Safety Order of Precedence, the 5M and
SHEL(L) system-description models, the seven hazard-analysis activities, integrated system hazard
analysis, the analysis-technique toolkit (FTA, FMEA/FMECA, Fault Hazard, CCFA, Sneak Circuit, Energy
Trace), closed-loop hazard tracking via the Safety Action Record, and the specialty domains the
handbook addresses (acquisition-lifecycle safety and contracting, software safety, test and
facilities safety, commercial launch licensing, training, and Operational Risk Management with human
and organizational factors).

**Thin on / does not cover**: the source is a year-2000 how-to and predates the modern **FAA/ICAO
Safety Management System (SMS)** and **Just Culture** regulatory frameworks — it gestures at the
underlying ideas (non-punitive reporting, positive culture) but does not present SMS as later
formalized. Many cited **FAA orders, advisory circulars, and commercial-launch-licensing rules date
to 2000 and have since been restructured** — confirm current citations before relying on them. It is
**FAA/NAS-centric** and leans heavily on **MIL-STD-882C**. It does **not** define the systems-
engineering life-cycle processes themselves (use `nasa-npr-7123` / `dau-se-guidebook` /
`nasa-se-handbook`), nor does it reproduce third-party standard text — **MIL-STD-882**, **RTCA
DO-178B**, **NASA 8719.13A**, and **ISO/IEC/IEEE** material is named and described in original words
but not reprinted (for the broader landscape see `se-standards-signpost`; for the FAA's general SE
process see `faa-sem`; for the defense severity matrix lineage see `mil-std-882`).

**Source version**: FAA *System Safety Handbook*, December 30, 2000 (the full 17-chapter handbook;
this pack synthesizes it into 7 chapters). It is a US Government work in the public domain.
