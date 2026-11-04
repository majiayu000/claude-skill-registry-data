---
name: se-standards-signpost
kind: signpost
description: "Signpost (not a knowledge pack) for the systems-engineering standards landscape — ISO/IEC/IEEE 15288, 24748, 29148, 42010, 15026, 24765; INCOSE SE Handbook & Vision 2035; OMG SysML; SAE/EIA 1001/649/748; ECSS space standards; NATO AAP-48; CMMI; NIST SP 800-160; and more. Contains NO source content: it lists each standard's designation, title, purpose, owning SDO, whether it's redistributable, and where to get it. Use when you need to identify or locate an SE standard — most are paywalled/all-rights-reserved and cannot be packaged, so this points you to the owner (and to the open packs where one exists)."
---

<!-- argument-hint: [standard designation or topic, e.g. 15288 / requirements / architecture / risk / SoS / security] -->

# Systems Engineering Standards Landscape — Signpost (pointers only)

**This is a signpost, not a knowledge pack.** It carries **no standards-body content** —
no reproduced clauses, no synthesised summaries of the normative text. Almost every
SE-related standard is paywalled and/or all-rights-reserved (ISO/IEC/IEEE, INCOSE, OMG,
SAE/EIA, ECSS, NATO, CMMI, CEN, AIAA), so they cannot be reconstituted into a
redistributable pack — see this repo's `docs/SOURCE-VETTING.md`. What this skill does:
tell you which standard you want, who owns it, whether it *can* be packaged, and where to
get the authentic copy.

## When to use
You need to identify, cite, or locate an SE standard (e.g. "what's the system life-cycle
process standard?" → ISO/IEC/IEEE 15288; "the requirements engineering standard?" →
ISO/IEC/IEEE 29148). This routes you to the authoritative source. For the topics covered
by **genuinely open** sources, it points you at the installable pack instead.

**Prerequisites:** none — plain Markdown.

## How to use
Find your standard or topic below. The **Status** column tells you whether it's
redistributable:
- 🔴 **Excluded** — paywalled or no redistribution grant; buy/download from the owner. *Cannot* be packaged here.
- 🟢 **Open** — public-domain or open-licensed; an installable pack exists or is planned (named in the row).

Where a licence permits citation, the owner's catalogue/abstract page is given; for ISO,
every standard has a page at `iso.org/standard/<number>.html`.

## Foundations — vocabulary & bodies of knowledge

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **SEBoK** | Guide to the SE Body of Knowledge | BKCASE (Stevens) | 🟢 Open — pack: `sebok` (CC BY-NC-SA) |
| **INCOSE SE Handbook (5th Ed)** | Breadth-of-SE reference; basis for SE certification | INCOSE (Wiley) | 🔴 Excluded — copyrighted; buy from INCOSE/Wiley |
| **SE Vision 2035** | INCOSE strategic vision for SE | INCOSE | 🔴 Excluded — free download, no redistribution grant; get from incose.org |
| **ISO/IEC/IEEE 24765** | Systems & software engineering — Vocabulary (also online as SEVOCAB at pascal.computer.org) | ISO/IEC/IEEE | 🔴 Excluded — iso.org (SEVOCAB browsable free) |

## Life-cycle processes & concepts

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **ISO/IEC/IEEE 15288** | System life cycle processes — *the* core SE process standard | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/81702.html |
| **ISO/IEC/IEEE 24748-1** | Guidelines for life cycle management | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/84709.html |
| **ISO/IEC/IEEE 24748-2** | Guide to applying 15288 | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/84661.html |
| **ISO/IEC/IEEE 24748-4** | SE management planning (SEMP) | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/56887.html |
| **ISO/IEC/IEEE 24748-6** | System & software integration | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/81563.html |
| **ISO/IEC/IEEE 24748-7** | SE on defense programs (was IEEE 15288.1) | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/90139.html |
| **ISO/IEC/IEEE 24748-8** | Technical reviews & audits on defense programs (was IEEE 15288.2) | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/91563.html |
| **ISO/IEC/IEEE 24748-10** | Guidelines for SE agility | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/90086.html |
| **SAE 1001** | Integrated project processes for engineering a system (replaced ANSI/EIA 632) | SAE | 🔴 Excluded — sae.org |
| **NATO AAP-48** | NATO system life cycle processes | NATO | 🔴 Excluded — NATO/standards portals |
| **ISO/IEC 29110** | Life-cycle profiles for very small entities (VSEs) | ISO/IEC | 🔴 Excluded — iso.org/standard/82669.html *(some 29110 parts are free from ISO — check the series)* |

## Process elaborations (one process each)

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **ISO/IEC/IEEE 29148** | Requirements engineering | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/72089.html · **open alternative: pack `requirements-writing`** (EARS + quality, original CC BY 4.0) |
| **ISO/IEC/IEEE 42010** | Architecture description | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/74393.html |
| **ISO/IEC/IEEE 42020** | Architecture processes | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/68982.html |
| **ISO/IEC/IEEE 42024** | Architecture fundamentals | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/87510.html |
| **ISO/IEC/IEEE 42030** | Architecture evaluation framework | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/73436.html |
| **ISO/IEC/IEEE 42042** | Reference architectures | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/87310.html |
| **ISO/IEC/IEEE 15939** | Measurement process | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/71197.html |
| **ISO/IEC/IEEE 16085** | Risk management (life-cycle) | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/74371.html |
| **ISO/IEC/IEEE 16326** | Project management | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/75276.html |
| **ISO/IEC/IEEE 15289** | Content of life-cycle information items | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/74909.html |
| **ISO 31000** | Risk management — guidelines | ISO | 🔴 Excluded — iso.org/standard/65694.html *(open alternatives for risk: NASA packs `nasa-risk`, `nasa-system-safety`; DoD `mil-std-882`)* |
| **IEC 31010** | Risk assessment techniques | IEC | 🔴 Excluded — iso.org/standard/72140.html |
| **ISO 10007** | Configuration management guidelines | ISO | 🔴 Excluded — iso.org/standard/70400.html |
| **IEEE 828** | Configuration management in systems & software | IEEE | 🔴 Excluded — standards.ieee.org |
| **ANSI/EIA-649C** | National consensus standard for configuration management | SAE/EIA | 🔴 Excluded — sae.org |
| **EIA 748D** | Earned value management system | SAE/EIA | 🔴 Excluded — sae.org |
| **ANSI/AIAA G-043B** | Guide to preparing operational concept (ConOps) documents | AIAA | 🔴 Excluded — arc.aiaa.org |

## Assurance, security & dependability

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **ISO/IEC/IEEE 15026-1..4** | Systems & software assurance — concepts/vocab (-1), assurance case (-2), integrity levels (-3), assurance in the life cycle (-4) | ISO/IEC/IEEE | 🔴 Excluded — iso.org (89808 / 80625 / 84444 / 74396) |
| **IEC 62853** | Open systems dependability | IEC | 🔴 Excluded — webstore.iec.ch |
| **NIST SP 800-160 Vol 1** | Systems Security Engineering — engineering trustworthy secure systems | NIST | 🟢 Open — US-gov public domain · **planned pack `nist-sse`** (note: contains some reprinted IEEE material) |
| **NIST SP 800-160 Vol 2** | Developing cyber-resilient systems — an SSE approach | NIST | 🟢 Open — US-gov public domain · **planned pack `nist-sse`** |

*(Adjacent open NIST packs already shipped: `nist-csf`, `nist-ssdf`, `nist-ai-rmf`.)*

## Modelling, MBSE & product-line

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **OMG SysML v2.0** | Systems Modeling Language | OMG | 🔴 Excluded — omg.org/spec/SysML · **see also pack `omg-signpost`** |
| **ISO/IEC/IEEE 24641** | Methods & tools for model-based systems & software engineering | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/79111.html |
| **ISO 19450** | Object Process Methodology (OPM) | ISO | 🔴 Excluded — iso.org/standard/84612.html |
| **ISO 10303-233** | Product data representation & exchange — AP233 (systems engineering) | ISO | 🔴 Excluded — iso.org/standard/55257.html |
| **ISO/IEC/IEEE 26550** | Reference model for product-line engineering & management | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/69529.html |
| **ISO/IEC/IEEE 26580** | Feature-based product-line engineering | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/43139.html |

## Systems of systems

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **ISO/IEC/IEEE 21839** | SoS considerations in life-cycle stages | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/91120.html |
| **ISO/IEC/IEEE 21840** | Utilizing 15288 in the context of SoS | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/71956.html |
| **ISO/IEC/IEEE 21841** | Taxonomy of SoS | ISO/IEC/IEEE | 🔴 Excluded — iso.org/standard/79111.html |

## Assessment, governance & enterprise/quality

| Standard | Title / purpose | Owner | Status |
|----------|-----------------|-------|--------|
| **ISO/IEC TS 33060** | Process assessment model for system life-cycle processes | ISO/IEC | 🔴 Excluded — iso.org/standard/87701.html |
| **CMMI-DEV V3.0** | Capability Maturity Model Integration for development | ISACA/CMMI Institute | 🔴 Excluded — cmmiinstitute.com |
| **ISO 9001** | Quality management systems — requirements | ISO | 🔴 Excluded — iso.org/standard/62085.html |
| **ISO 15704** | Requirements for enterprise reference architectures & methodologies | ISO | 🔴 Excluded — iso.org/standard/71890.html |
| **ISO 19439** | Framework for enterprise modelling | ISO | 🔴 Excluded — iso.org/standard/33833.html |
| **CEN EN 9277** | Programme management — guide for the management of SE | CEN | 🔴 Excluded — CEN/national bodies |

## Space-sector SE (ECSS)

All ECSS standards are **🔴 Excluded**: ESA holds copyright, no reproduction without explicit
consent, and non-members are directed to *cite* rather than rewrite. Download (free, with
registration) from `ecss.nl`.

| Standard | Title / purpose |
|----------|-----------------|
| **ECSS-E-ST-10C** | SE general requirements |
| **ECSS-E-ST-10-02** | Verification |
| **ECSS-E-ST-10-06** | Technical requirements specification |
| **ECSS-E-ST-10-24** | Interface management/control |
| **ECSS-M-ST-10** | Project planning & implementation |
| **ECSS-M-ST-40** | Configuration & information management |
| **ECSS-M-ST-60** | Cost & schedule management |
| **ECSS-M-ST-80 / M-00-03** | Risk management |

## Topic → standard quick map

- **Vocabulary** → ISO/IEC/IEEE 24765 (SEVOCAB)
- **Life-cycle processes** → ISO/IEC/IEEE 15288 (+ 24748 series for guidance)
- **Requirements** → ISO/IEC/IEEE 29148 *(open: `requirements-writing`)*
- **Architecture** → ISO/IEC/IEEE 42010 / 42020 / 42030
- **MBSE / modelling** → OMG SysML, ISO/IEC/IEEE 24641, ISO 19450 (OPM)
- **Risk** → ISO 31000 / IEC 31010 / ISO-IEC-IEEE 16085 *(open: `nasa-risk`, `mil-std-882`)*
- **Configuration management** → IEEE 828 / ANSI-EIA-649C / ISO 10007
- **Measurement** → ISO/IEC/IEEE 15939
- **Assurance / security** → ISO/IEC/IEEE 15026 series; **NIST SP 800-160 v1/v2 (open → `nist-sse`)**
- **Systems of systems** → ISO/IEC/IEEE 21839 / 21840 / 21841
- **Defense application** → ISO/IEC/IEEE 24748-7 / 24748-8 *(open DoD-process: `dau-se-guidebook`)*
- **Maturity assessment** → ISO/IEC TS 33060, CMMI-DEV *(open TRL maturity: `gao-tra`)*
- **Quality / enterprise** → ISO 9001 / ISO 15704 / ISO 19439
- **Space** → ECSS series (ecss.nl)

## Why most of these can't be packaged
A knowledge pack *reproduces and transforms* a source into new published files — that's
redistribution plus derivative work, which needs an actual grant. ISO/IEC/IEEE, SAE/EIA,
INCOSE, CMMI, CEN, AIAA, and IEC standards are paywalled and all-rights-reserved. OMG and
ECSS are downloadable but their licences forbid network-posting and/or modification. None
of those grant what a pack needs, so they sit on this repo's Excluded list. This signpost
stays clean by holding only **designations, titles, purposes, owners, and citation URLs** —
facts and citations, never the normative text. Where a source *is* open (NIST public-domain;
original CC-BY guidance), there's a real pack and this points to it.

---
*Signpost content © JG Systems Consulting Ltd. (MIT). Standard designations and titles are
identified for reference only; "INCOSE", "SysML", "CMMI", "ECSS", and standard numbers are
the property of their respective owners (ISO, IEC, IEEE, INCOSE, OMG, SAE, ESA, NATO, CEN,
AIAA, ISACA, NIST). Named here for identification, not endorsement.*
