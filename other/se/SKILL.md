---
name: se
kind: orchestrator
disable-model-invocation: true
description: "Orchestrator (not a knowledge pack): routes a free-text systems-engineering question to the right catalogue pack(s), reads them with you, and answers with pack and chapter citations. Runs only on explicit `/se <question>`; carries no source content. Use when you do not know which `/pack` to ask."
---

<!-- argument-hint: [free-text systems-engineering question] -->

# SE Orchestrator: routes questions to the right knowledge packs

**This is an orchestrator, not a knowledge pack.** It carries **no source content**.
On explicit `/se <question>` it matches your question to installed catalogue packs,
reads them, and answers with pack and chapter citations.

## When to use
**Prerequisites:** none: plain Markdown; works on any host that loads Agent Skills. Pair it with the packs it routes to.

`/se` answers systems-engineering questions by consulting installed packs. It is an
entry point, not a knowledge base. Use it when you do not already know which `/<slug>`
to open.

## How /se answers

### Modes

| Mode | When | Gate |
|---|---|---|
| Narrow consult | One Topics row matches, at most one agency named, no compare/contrast/survey verb | None. Best single pack. End with "Also relevant" runners-up. |
| Broad consult | Two or more Topics rows, two or more agencies, or a compare/contrast/survey verb | One plan approval naming packs and why, then run to done. Disagreements under "Where the sources differ"; never average or blend. |
| Deliverable | An artifact verb (draft, write, produce, prepare, build, review, verify) plus a Deliverables row name or keyword | Plan approval, then stage pauses after Draft and after Review (Verify is last). |

### Routing

1. Match Topics keywords case-insensitively, with synonym judgement (e.g. "V&V" hits verification and validation rows).
2. Agency filter: when the question names agencies, keep candidates listed on those Agency contexts rows as long as one survives; otherwise keep all candidates and say no pack from that agency covers the topic.
3. Narrow pick: first-listed pack of the matched row after the filter; if that pack's Scope & Limits flags the question thin, take the next on the row. The consult stays narrow (no gate).
4. Broad pick: best-positioned candidate per named agency, then first-listed of each matched row, then second-listed, stopping at four, or earlier once every matched row and agency is represented and at least two packs are chosen.
5. No match: name the three closest Topics rows, suggest a rephrase or a direct `/<slug>`, and make **no SE claims**.

### Reading

A pack lives at `../<slug>/` from this folder (native installs put members side by side). For each selected pack: read its `SKILL.md` index; open at most two chapters from its Topic Index / Chapter Index; open one support file (`glossary.md`, `patterns.md`, or `cheatsheet.md`) only for term, technique, or decision-rule questions. At most four packs total. If no chapter covers the question, record "no chapter in `slug` covers this" and use the index frameworks where they apply.

Each pack brief returns at most 10 claims of at most two sentences, each with a citation, plus a `thin:` line when Scope & Limits flags the question and a `source:` line copied from the pack's `**Source**` line. No claim from outside its pack.

### Citations and Sources

Cite only files read this session, in these forms: `[slug chNN]`, `[slug index]`,
`[slug glossary|patterns|cheatsheet]`. Drop uncited claims. Agreeing claims merge into one statement carrying every citation. Where the packs are silent, say so; no fallback to model memory. Every answer ends with a **Sources** block listing each pack's slug, its `**Source**` line, and its licence. Content-pack licences come from the Licences table, else the label `Public Domain (US Government work)`. Signpost lines read `MIT (signpost)`. Non-commercial and share-alike terms appear in full.

### Deliverable stage chains

The matched Deliverables row is the chain. Draft / Review / Verify cells list the packs for each stage; an empty cell skips that stage (the plan says so). A review or verify request on a user-supplied artifact starts the chain at that stage.

- **Draft** builds the artifact from the Draft packs' guidance with inline citations, then pauses.
- **Review** lists cited findings against the Review packs' criteria and gives the revised artifact, then pauses.
- **Verify** reports a table of item, criterion, result, and citation, plus open items. It edits nothing and offers fixes as a follow-up.

Output goes in the reply unless the user names a file. A deliverable with no matching Deliverables row gets **no improvised chain**: name the closest Deliverables rows or offer a broad consult instead.

### Edge cases

- Bare `/se` with no argument: print usage and three example questions (e.g. requirements quality, NASA risk process, hazard analysis draft).
- Sub-agent failure: rerun that brief in the main thread.
- Thin-pack step-down: if the selected pack's Scope & Limits flags the question thin, take the next pack on the row; the consult stays narrow.

## Routing map

<!-- ROUTING-MAP:BEGIN -->
### Topics
| Topic | Keywords | Packs (best first) |
|---|---|---|
| SE fundamentals & systems thinking | systems engineering, lifecycle, systems thinking, SE process, what is SE | `sebok`, `nasa-se-handbook`, `dau-se-guidebook`, `nist-cps` |
| Requirements engineering | requirements, shall statements, EARS, requirement quality, weak words, verifiable requirements | `requirements-writing`, `faa-req-handbook`, `nasa-se-handbook` |
| Requirements traceability & allocation | traceability, allocation, flow-down, bidirectional traceability | `faa-req-handbook`, `requirements-writing`, `faa-std-025` |
| Architecture & design | architecture, architecture framework, design solution, MOSA, modular open systems | `dodaf`, `dod-mosa`, `nasa-se-handbook`, `sebok` |
| Interface management | interfaces, ICD, interface control, ICID, interface definition | `is-gps-200n`, `faa-std-025`, `nasa-se-handbook`, `faa-sem` |
| Integration | integration, assembly, integration readiness, integration planning | `nasa-se-handbook`, `nasa-se-expanded`, `doe-sem`, `dafman-63-119` |
| Verification | verification, verification methods, test/analysis/inspection/demonstration, verifiability | `faa-ams-vv`, `dod-vva-rpg`, `nasa-se-handbook`, `dote-te-guidebook` |
| Validation | validation, effectiveness, operational suitability, user needs | `dod-vva-rpg`, `faa-ams-vv`, `nasa-se-handbook`, `dote-te-guidebook` |
| Test & evaluation | test and evaluation, T&E, developmental test, operational test, test readiness | `dod-te-guidebook`, `dote-te-guidebook`, `dafman-63-119`, `dod-vva-rpg` |
| Modeling, MBSE & simulation | MBSE, SysML, modelling, simulation credibility, M&S | `nasa-systems-modeling`, `nasa-ms-7009`, `dod-vva-rpg`, `dodaf` |
| Digital engineering | digital engineering, digital twin, digital thread, model-centric acquisition | `dod-digital-engineering`, `digital-systems-engineering`, `nasa-de-acquisition` |
| Configuration management | configuration management, baselines, change control, CM plans | `mil-hdbk-61`, `nasa-se-handbook`, `faa-std-025` |
| Data & information management | data management, technical data, data rights, information models | `mil-hdbk-61`, `dodaf`, `nasa-de-acquisition`, `nasa-npr-7150`, `nist-cps` |
| Risk management | risk, risk register, risk matrix, likelihood, consequence, risk acceptance, continuous risk management | `nasa-risk`, `dod-rio`, `nist-ai-rmf` |
| Opportunity & benefit management | opportunity, benefit, benefit-cost analysis, cost-effectiveness, BCA | `federal-bca`, `dod-rio` |
| Trade studies & decision analysis | trade study, decision analysis, alternatives, selection criteria, weighting | `nasa-se-handbook`, `federal-bca`, `nasa-ceh`, `dod-vva-rpg` |
| Work breakdown & technical planning | WBS, work breakdown structure, technical plans, SOW, planning packages | `mil-std-881f`, `nasa-se-handbook`, `nasa-npr-7123`, `doe-sem` |
| Technical measurement & assessment | TPM, technical performance measures, TRL, MRL, readiness assessment, statistical methods | `gao-tra`, `mrl-deskbook`, `nist-stat-handbook`, `nasa-ms-7009` |
| Quality assurance & airworthiness | QA, quality assurance, process compliance, airworthiness certification | `mil-hdbk-516`, `gao-agile`, `nist-stat-handbook` |
| System safety & hazards | safety, system safety, hazard analysis, fault management, PRA, mishap | `mil-std-882`, `nasa-system-safety`, `faa-system-safety`, `nasa-pra`, `nasa-fault-management` |
| Reliability & maintainability | reliability, maintainability, availability, RMA, R&M, failure rates | `mil-hdbk-338`, `faa-rma`, `nasa-rm-standard` |
| Cybersecurity & security engineering | cybersecurity, security engineering, RMF, incident response, CUI, secure software, CSF | `nist-csf`, `nist-sse`, `nist-800-37`, `nist-800-171`, `nist-800-61`, `nist-ssdf` |
| Cyber performance goals & infrastructure | critical infrastructure, performance goals, sector security, CPS | `cisa-cpg`, `nist-csf`, `nist-cps` |
| Human factors & HSI | human factors, HSI, usability, workload, crew stations, anthropometry | `faa-hf-std`, `nasa-hsi`, `mil-hdbk-516` |
| Logistics, sustainment & obsolescence | logistics, sustainment, supportability, DMSMS, obsolescence, parts management | `sd-22-dmsms`, `dote-te-guidebook` |
| Orbital debris & end-of-life disposal | orbital debris, passivation, reentry, disposal, spacecraft end-of-life | `nasa-std-8719-14`, `nasa-se-handbook` |
| Technical documentation & manuals | technical manuals, documentation standards, page-based documentation | `mil-std-40051`, `faa-std-025` |
| Cost & schedule | cost estimating, schedule, EVM, budget, program cost, schedule margin | `gao-cost`, `gao-schedule`, `nasa-schedule`, `nasa-ceh`, `gao-agile` |
| Manufacturing & quality engineering | manufacturing readiness, MRL, production, quality engineering, factory | `mrl-deskbook`, `dod-mq-bok` |
| Agile in government programs | agile, incremental delivery, iterative development, scrum oversight | `gao-agile` |
| Acquisition & suppliers | acquisition, procurement, supplier, contract, sourced approval | `doe-o-413-3`, `nasa-de-acquisition`, `dod-mosa`, `mrl-deskbook`, `nasa-npr-7123` |
| Governance, reviews & gates | reviews, gates, KDPs, milestones, certification, test readiness certification | `dafman-63-119`, `eu-ai-act`, `doe-o-413-3`, `nasa-npr-7123`, `dau-se-guidebook` |
| SE standards & process models | SE standards, ISO 15288, tailoring, lifecycle models, NPR requirements | `sebok`, `nasa-npr-7150`, `nasa-npr-7123`, `dau-se-guidebook`, `nasa-se-handbook` |
| AI & cyber-physical systems | AI, AI risk management, autonomous systems, cyber-physical, CPS, EU AI Act | `nist-ai-rmf`, `nist-cps`, `eu-ai-act`, `jsp-936` |
| Modelling language specifications | SysML spec, UML, UAF, BPMN, OMG specifications | `omg-signpost`, `nasa-systems-modeling` |
| SE standards landscape lookup | ISO/IEC/IEEE standards, INCOSE handbook, ECSS, SAE, where to get a standard | `se-standards-signpost`, `sebok` |
| Vehicle safety & automotive | vehicle safety, automotive, FMVSS, ADS, automated driving, vehicle cybersecurity | `nhtsa-vehicle`, `automotive-signpost`, `functional-safety-signpost` |
| Civil infrastructure & ITS | intelligent transportation, ITS, systems engineering analysis, 23 CFR 940, ConOps | `fhwa-its-se` |
| GPS & GNSS interfaces | GPS, GNSS, NAVSTAR, space segment interface, ranging signal | `is-gps-200n`, `faa-std-025` |
| Medical device software | FDA, QMSR, 510(k), device software, SaMD, eSTAR, MDR, IVDR, MHRA, UKCA, MDCG | `fda-med-device`, `med-device-eu` |
| Avionics software assurance | DO-178C, DO-254, 8110.49, airborne software, AEH, conformity | `faa-8110-49`, `avionics-signpost`, `easa-rules` |
| Railway RAMS & signalling assurance | EN 50126, EN 50128, EN 50129, railway RAMS, CSM, signalling assurance, RSSB | `rail-signpost` |
| Space standards (ECSS) | ECSS, space standards, E-ST-10, E-ST-40, Q-ST-30, space environment, product assurance | `space-signpost` |
| Maritime safety and class rules | SOLAS, ISM, ISPS, COLREGS, USCG, class rules, MCA | `maritime-signpost` |
| Defence safety management | JSP 815, JSP 376, JSP 912, acquisition safety, defence safety, SMS, safety case, assurance, dependable AI, AI assurance, human factors, HFI, human component | `jsp-815`, `jsp-376`, `jsp-936`, `jsp-912` |
| Nuclear software assurance | NRC, regulatory guide, NUREG, digital safety systems, software assurance, BTP 7-14 | `nrc-nuclear` |

### Agency contexts
| Agency | Keywords | Packs |
|---|---|---|
| NASA | NASA, NPR, NASA-STD, NASA-HDBK, mission | `nasa-se-handbook`, `nasa-npr-7123`, `nasa-npr-7150`, `nasa-risk`, `nasa-system-safety`, `nasa-hsi` |
| DoD / DAU / OSD | DoD, MIL-STD, MIL-HDBK, DAU, OSD, DOT&E, DAF, SD-22, MRL | `dau-se-guidebook`, `dod-rio`, `mil-std-882`, `dod-te-guidebook`, `mil-hdbk-61`, `dodaf` |
| NIST | NIST, SP 800, framework, FIPS | `nist-csf`, `nist-sse`, `nist-800-37`, `nist-800-171`, `nist-ai-rmf`, `nist-stat-handbook` |
| FAA | FAA, AMS, air traffic, civil aviation | `faa-sem`, `faa-ams-vv`, `faa-req-handbook`, `faa-system-safety`, `faa-hf-std`, `faa-rma` |
| GAO | GAO, schedule assessment, cost assessment, agile assessment, TRA | `gao-cost`, `gao-schedule`, `gao-tra`, `gao-agile` |
| DOE | DOE, department of energy, order 413 | `doe-sem`, `doe-o-413-3` |
| CISA / DHS | CISA, DHS, critical infrastructure, performance goals | `cisa-cpg` |
| OMB | OMB, circular A-94, federal benefit-cost | `federal-bca` |
| EU | EU, European Union, AI Act, regulation | `eu-ai-act` |
| NHTSA / USDOT | NHTSA, USDOT, FMVSS, vehicle safety standard, automated driving systems | `nhtsa-vehicle` |
| FHWA / USDOT ITS | FHWA, ITS, systems engineering analysis | `fhwa-its-se` |
| FDA | FDA, CDRH, QMSR, 21 CFR 820, 510(k) | `fda-med-device` |
| NRC | NRC, regulatory guide, NUREG, BTP 7-14 | `nrc-nuclear` |
| EASA | EASA, AMC 20-115D, AMC 20-152A, Easy Access Rules | `easa-rules` |
| EU / MHRA | MDCG, MDR, IVDR, MHRA, UKCA, SaMD | `med-device-eu` |

### Deliverables
| Deliverable | Keywords | Draft | Review | Verify |
|---|---|---|---|---|
| Requirements specification | requirements doc, SRD, shall statements, spec tree | `requirements-writing`, `faa-req-handbook` | `requirements-writing` | `faa-ams-vv` |
| ConOps | concept of operations, ConOps, operational concept, scenarios | `nasa-se-handbook`, `sebok` | `nasa-se-handbook` | `faa-ams-vv` |
| Risk register | risk register, risk log, risk statement, mitigation plan | `nasa-risk`, `dod-rio` | `nasa-risk` | `dod-rio` |
| Verification plan | verification plan, V&V plan, verification matrix | `faa-ams-vv`, `dod-te-guidebook` | `faa-ams-vv` | `dote-te-guidebook` |
| Hazard analysis | hazard analysis, hazard log, safety assessment, FMEA | `mil-std-882`, `nasa-system-safety` | `mil-std-882` | `faa-system-safety` |
| Interface control document | ICD, interface control document, interface definition | `faa-std-025`, `is-gps-200n` | `faa-std-025` | |
| Trade study | trade study, trade-off analysis, alternatives evaluation | `nasa-se-handbook`, `federal-bca` | `nasa-se-handbook` | |
| Work breakdown structure | WBS, work breakdown structure, WBS dictionary | `mil-std-881f`, `nasa-se-handbook` | `mil-std-881f` | |

### Licences
| Pack | Licence |
|---|---|
| `sebok` | CC BY-NC-SA 3.0 |
| `requirements-writing` | Original guidance (CC BY 4.0); cited methods not reproduced |
| `digital-systems-engineering` | CC BY 4.0 |
| `eu-ai-act` | EU Official Journal — reproduction authorised with source acknowledgement (Decision 2011/833/EU) |
| `jsp-815` | Open Government Licence v3.0 |
| `jsp-376` | Open Government Licence v3.0 |
| `jsp-936` | Open Government Licence v3.0 |
| `jsp-912` | Open Government Licence v3.0 |
| `easa-rules` | Per-document: EASA site reproduction-with-acknowledgement grant, qualified by ED Decision all-rights-reserved footers; reconstructed notes with attribution; official PDFs not redistributed; commercial use pending per-document determination |
| `med-device-eu` | Per-document: European Commission reuse policy (Decision 2011/833/EU, CC BY 4.0, attribution and indication of changes) for the MDCG documents; Open Government Licence v3.0 for the MHRA guidance; reconstructed notes with attribution; official PDFs not redistributed |
<!-- ROUTING-MAP:END -->

## Host modes

Pick the highest mode the host can run:

| Mode | When | Behaviour |
|---|---|---|
| Fan-out | Sub-agents available | One brief per pack in parallel; main thread composes the answer. On sub-agent failure, rerun that brief in the main thread. |
| Sequential | No sub-agents, member files readable | Same briefs one at a time; write each pack's notes before opening the next. |
| Index-only | Transform installs (Codex, Gemini, Cursor rules) | Read sibling index files when readable. Cite `[slug index]` only, name chapters as follow-ups, and label the answer `index-level: chapter bodies not installed`. |
| Route-only | No member file readable | Report the routing decision and the `/slug` commands only. Make **no SE claims**. |

**Native-root fallback.** When the skill folder is not revealed, try
`~/.claude/skills/`, `~/.openclaw/skills/`, `~/.copilot/skills/`, each with and
without the `jgs-se-knowledge-packs/` namespace. Transform index files live at
`~/.codex/prompts/<slug>.md`, `~/.gemini/commands/jgs-se-knowledge-packs/<slug>.toml`,
and `./.cursor/rules/<slug>.mdc`.

Narrow consults read in the main thread on every host. A missing routed pack is
noted and skipped; if none remain, fall back to route-only.

## Scope & Limits

- No SE claim without a citation from a pack file read this session.
- The map is curated, not exhaustive. Agency rows are a filter, not an endorsement.
- At most six packs per Topics row. At most four packs read per answer.
- Deliverable stage chains come only from Deliverables rows; empty cells skip that stage.
- `/se` never overwrites an existing file without a yes at a gate.

---
*Orchestrator content © JG Systems Consulting Ltd. (MIT). Pack names and source titles
are identified for routing only; each pack keeps its own licence.*
