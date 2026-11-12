---
name: ak-cti-expert
description: "Analyze threat intel and OSINT: domain and tenant recon, breach checks, username/email/phone lookups, image forensics, blockchain tracing, darknet checks."
when_to_use: "Invoke for exposure reviews, CVE lookup, threat models or reports."
category: engineering
keywords: [osint, cti, threat-intelligence, recon, investigation, darknet, breach, forensics]
argument-hint: "[target] [--yolo] [--case|--sweep|--query|--flow] [--format html|md] [--no-antv|--no-diagram-design|--no-editorial-visuals]"
license: Proprietary; includes MIT-licensed third-party material, see LICENSE
metadata:
  version: "2.1.2"
  author: "Hieu Ngo - chongluadao.vn"
  source: "https://github.com/7onez/cti-expert"
---

# CTI Expert (`ak-cti-expert`)

Cyber threat intelligence and open-source intelligence analysis skill. Generates precision search queries, interprets public threat data, builds case timelines, and delivers structured intelligence products.

## Route the requested investigation

Select acquire, enrich, assess, or deliver from the request; load only that branch’s references. A single IOC lookup returns sources, observation time, confidence, and uncertainty without starting a case or generating a report bundle. Explicit `/case`, `/report`, and `/brief` retain the dual Markdown/Word deliverable below; `--format html` adds its mirror. Do not silently remove the Word artifact from that established contract.

## AEAD Case Lifecycle

1. **Acquire**: Collect raw intelligence (`/case`, `/sweep`, `/query`, `/username`, `/phone`, `/email-deep`, `/subdomain`, `/docleak`, `/vuln-check`, `/threat-check`). See `references/commands.md`.
2. **Enrich**: Expand leads, detect connections (`/branch`, `/timeline`, `/crossref`, `/link-subjects`, `/graph`, `/pathfind`). See `engine/finding-framework.md`, `engine/conflict-resolver.md`.
3. **Assess**: Score risk and verify findings (`/exposure`, `/threat-model`, `/signatures`, `/validate`, `/coverage`, `/verify-finding`). See `analysis/weight-engine.md`, `analysis/exposure-model.md`.
4. **Deliver**: Package intelligence products (`/report`, `/report brief`, `/report legal`, `/report ioc`, `/workspace save`). Auto-saves `.md` and `.docx`. See `references/report-templates.md`, `output/reports/format-catalog.md`.

## Core Commands Quick Reference

| Phase | Core Commands | Purpose |
|---|---|---|
| **Acquire** | `/case [target]`, `/sweep [target]`, `/query [target]` | Full pipeline recon and dork generation |
| **Identity** | `/username [handle]`, `/phone [num]`, `/email-deep [email]` | Footprint enumeration through available passive sources |
| **Infra** | `/subdomain [domain]`, `/msftrecon [domain]`, `/threat-check [ip]` | Certificate logs, tenant discovery, threat scoring |
| **Leaks** | `/docleak [target]`, `/secrets [target]`, `/breach-deep [email]` | Credential and document leak monitoring |
| **Assess** | `/exposure [target]`, `/threat-model`, `/validate` | Exposure scoring (0–100) and evidence auditing |
| **Deliver** | `/report`, `/brief`, `/workspace save [name]` | Structured intelligence reports & workspace persistence |

See `references/commands.md` for the exhaustive command catalog.

## Guided Flows & Workflows

Activate interactive walkthroughs via `/flow [type]`:
- **Threat Analyst**: `workflows/wf-threat-analyst.md`
- **Journalist Source Verification**: `workflows/wf-journalist.md`
- **HR / Background Screening**: `workflows/wf-hr-screening.md`
- **Private Investigator**: `workflows/wf-private-investigator.md`

## Output Formats & HTML Mirror (`--format html`)

Every `/report`, `/brief`, and `/case` auto-saves two files to disk:
1. Markdown report: `CTI-REPORT-<CASE-ID>-<YYYY-MM-DD>.md`
2. Word document: `CTI-REPORT-<CASE-ID>-<YYYY-MM-DD>.docx`

### HTML Output Mode (`--format html`)

When `--format html` is specified, generate a self-contained, offline editorial HTML mirror (`CTI-REPORT-<CASE-ID>-<YYYY-MM-DD>.html`):

- Follow the shared HTML composition contract in `../ak-preview/references/html-skill-composition.md` and `references/html-mirror.md`:
  1. Activate `ak-frontend-design` first for layout, typography, responsive containers, and dark/light styling.
  2. Activate `ak-diagram` second (when installed) to compile typed JSON IR for entity relationships, threat models, and sequence timelines.
  3. If `ak-diagram` is absent, produce a clean semantic inline SVG/CSS fallback with `<title>/<desc>`.
- **Zero Outbound Requests**: All assets must be inlined or vendored locally (0 CDN calls).
- **Evidence Integrity**: Distinguish verified indicators from analyst hypotheses; sanitize internal credentials and private IPs.

## Visual Outputs & Connectors

- **ASCII-First Default**: All visualization commands (`/graph`, `/render entities`, `/render timeline`, `/render risk`, `/render network`) produce clean ASCII box-drawing art by default. Mermaid output is produced only on explicit `--mermaid` flag.
- **Export Connectors**: Maltego (`connectors/maltego-export.md`), Obsidian (`connectors/obsidian-setup.md`), Notion (`connectors/notion-schema.md`).

## Ethics, OPSEC & Prohibited Uses

- **Passive OSINT Only**: Never perform active network penetration, unauthorized port scanning, brute-forcing, credential stuffing, or vulnerability exploitation.
- **Privacy & Compliance**: Respect GDPR, CCPA, and applicable legal privacy boundaries. Do not dox private individuals or investigate targets for harassment or stalking.
- **Tool Cascade**: `ak-agent-browser` (when installed) $\rightarrow$ direct web fetch $\rightarrow$ search dorks. See `references/tool-cascade.md` and `handbook/tool-cascade-reference.md`.
