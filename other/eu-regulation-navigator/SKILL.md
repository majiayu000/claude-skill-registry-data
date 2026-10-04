---
name: eu-regulation-navigator
description: "Works out which EU regulations apply to a system, process, vendor, or organization (EU AI Act, NIS2, DORA, GDPR), classifies AI risk tier, NIS2 entity type, and DORA scope, lists the key obligations with article citations, and maps overlaps in incident reporting, security controls, management accountability, and penalties, including German works council co-determination for AI. Use when someone asks whether a regulation applies, how an AI system is classified, which incident deadlines run, or how these EU regimes interact. For hands-on GDPR work such as DPIAs or DSARs, use gdpr-operations-playbook."
---

# EU Regulation Navigator

You help users figure out which EU digital regulations reach a given scenario and what that means in practice. For the EU AI Act, NIS2, DORA, and GDPR you run the applicability tests, name the headline obligations with their articles, and show where the regimes overlap so compliance work can be consolidated. You orient and scope; you do not replace counsel.

> **Disclaimer.** What you provide is general legal information for research and orientation. It is not legal advice, and it establishes no attorney-client relationship. Before acting on any of it, the user should check the AI-generated output and get advice from a qualified legal professional.

## What this skill covers, and what it hands off

In scope: deciding whether the AI Act, NIS2, DORA, and GDPR apply; surfacing the key obligations under each; mapping how they overlap; and flagging German works council (Betriebsrat) rules for AI.

Out of scope: detailed operational GDPR workflows such as DPIAs, DSAR handling, breach notification, DPA review, and ROPA. Send those to the `gdpr-operations-playbook` skill.

## How to scope a scenario

1. **Pin down the facts.** Establish which system, process, or vendor is involved, what categories of data it touches, which sector it sits in, and which EU member states are concerned.
2. **Test each regulation in turn.** Apply the AI Act, NIS2, DORA, and GDPR checks set out below.
3. **Map the overlaps.** Identify which obligations are shared between regimes and which stack on top of each other (see "Where the regimes overlap").
4. **Rank by deadline.** Work out which deadlines are closest for this particular scenario.
5. **Deliver the scoping assessment.** List the regulations that apply, the key obligations under each, recommended next steps, and pointers to more detailed guidance.

For every regulation you conclude applies, cite the specific articles that make it applicable.

## Applicability tests

### EU AI Act (Regulation (EU) 2024/1689): which risk tier?

Place the AI system in one of the tiers below, checking from the top down.

**Prohibited practices (Article 5).** These are banned outright:

- Subliminal, manipulative, or deceptive techniques that cause significant harm (Article 5(1)(a))
- Exploiting the vulnerabilities of specific groups because of age, disability, or social or economic situation (Article 5(1)(b))
- Social scoring carried out by public authorities, or by others acting for them (Article 5(1)(c))
- Predictive policing where the prediction rests only on profiling a person or on their personality traits (Article 5(1)(d))
- Building facial recognition databases through untargeted scraping of facial images from the internet or CCTV (Article 5(1)(e))
- Emotion recognition in the workplace and in educational institutions (Article 5(1)(f))
- Biometric systems that categorize people by inferring sensitive attributes such as race, political opinions, religion, or sexual orientation (Article 5(1)(g))
- Law-enforcement use of real-time remote biometric identification in spaces open to the public, subject to narrow exceptions (Article 5(1)(h))

**High-risk systems (Annex III).** Annex III lists eight areas: education, employment, biometrics, essential services, critical infrastructure, law enforcement, administration of justice, and migration and border control. A system in one of these areas is high-risk when it meets the conditions in Article 6(2). Deployers must:

- put human oversight in place (Article 14);
- operate the system according to its intended use, keeping appropriate monitoring and logs (Article 26);
- carry out a fundamental rights impact assessment (FRIA) before first use of the high-risk system, in cases where one is required (Article 27).

Check the split between provider and deployer duties, the available conformity assessment routes, and borderline Annex III cases against the official AI Act text and the Commission's current guidance.

**General-purpose AI models (Articles 51–56).**

- Every GPAI model carries transparency obligations: technical documentation, a copyright policy, and a content summary (Article 53).
- A GPAI model with systemic risk, meaning training compute above 10^25 FLOPs or designation by the Commission, must additionally undergo model evaluation and adversarial testing, track incidents, and have cybersecurity protections (Article 55). The 10^25 FLOPs figure reflects the Act as first enacted; the Commission can revise it by delegated act under Article 51(2).

**Limited risk (Article 50).** Only transparency duties apply:

- Chatbots must tell users they are interacting with AI.
- Deepfakes and other synthetic content must be labeled as AI-generated.
- Emotion recognition systems must inform the people subject to them.

**Minimal risk.** There are no mandatory obligations; voluntary codes of conduct are encouraged (Article 95).

### NIS2 (Directive (EU) 2022/2555): what kind of entity?

Classify the entity by sector, then by size.

**Sectors**

- *Annex I (essential):* space; public administration; energy; health; banking; transport; financial market infrastructure; drinking water; wastewater; ICT service management (B2B); digital infrastructure.
- *Annex II (important):* research organizations; digital providers (search engines, online marketplaces, social networking platforms); postal and courier services; food (its production, processing, and distribution); waste management; manufacturing of machinery, electronics, medical devices, motor vehicles, and other transport equipment; chemicals (their manufacture, production, and distribution).

**Size (Article 2).** These are the Directive's thresholds; national transpositions may adjust them.

- **Medium:** 50 or more employees OR annual turnover of EUR 10M or more.
- **Large:** 250 or more employees OR annual turnover of EUR 50M or more.
- Entities under the medium threshold generally fall outside the Directive unless a member state designates them.
- Certain entities are caught whatever their size, for example sole DNS providers, TLD registries, and qualified trust service providers.

**Result**

| Classification | Sector list | Size | What follows |
|---|---|---|---|
| Essential | Annex I | Large, or designated | Every obligation applies; the higher penalty ceiling |
| Important | Annex II | At least medium | Every obligation applies; the lower penalty ceiling |
| Out of scope | On neither list, or too small | — | NIS2 imposes nothing |

**Core duties once in scope.** Article 21 expects documented policies and practices for: access control; business continuity; cryptography; human resources; incident handling; MFA, or an equivalent, where appropriate; risk analysis; security when network and information systems are acquired, developed, and maintained; and supply chain security. Article 23 lays down the reporting chain for incidents (early warning, notification, then intermediate and final reports). Article 20 places oversight duties and liability on the management body. Confirm the sector classification and the national transposition details for each member state involved.

### DORA (Regulation (EU) 2022/2554): is the entity in scope?

**Entities covered (Article 2)**, roughly 22,000 across the EU:

- *Banking and payments:* electronic money institutions, credit institutions, account information service providers, payment institutions.
- *Investment and market infrastructure:* trading venues, investment firms, central counterparties, trade repositories, crypto-asset service providers, central securities depositories, data reporting service providers, securitization repositories, administrators of critical benchmarks.
- *Funds:* management companies, managers of alternative investment funds.
- *Insurance and pensions:* insurance intermediaries, institutions for occupational retirement provision, insurance and reinsurance undertakings.
- *Others:* credit rating agencies, crowdfunding service providers, and ICT third-party service providers once they are designated as critical.

**Proportionality (Article 4).** How much is demanded depends on:

- the entity's size and overall risk profile;
- the nature, scale, and complexity of its services;
- its systemic significance.

Microenterprises get the simplified ICT risk management framework instead (Article 16).

**What DORA expects.** Its requirements are organized around five areas: governance and management of ICT risk; testing of digital operational resilience; handling and reporting of incidents; management of ICT third-party risk; and arrangements for sharing information (Articles 5–30 plus the related technical standards). For registers of information and for oversight of critical third parties, rely on the sector RTS/ITS and on guidance from the competent authorities.

### GDPR (Regulation (EU) 2016/679): quick applicability check

GDPR is engaged whenever personal data relating to people in the EU/EEA is part of the picture. The main triggers:

- An establishment in the EU/EEA that processes personal data (Article 3(1))
- Processing personal data about people living in the EU/EEA (Article 3(2))
- Offering goods or services to individuals in the EU/EEA
- Monitoring the behavior of individuals in the EU/EEA

Stop at applicability here. For DPIAs, DSARs, breach notification, DPA review, or ROPA, switch to the `gdpr-operations-playbook` skill.

## Where the regimes overlap

### Incident reporting clocks

| Regulation | First notice | Follow-up report | Final report |
|---|---|---|---|
| GDPR (Article 33) | Within 72h, addressed to the DPA | — | — |
| NIS2 (Article 23) | Early warning to the CSIRT within 24h | 72h incident notification | Final report at 1 month |
| DORA (Articles 19–20) | As set by the RTS classification criteria | 72h intermediate report | Final report at 1 month |
| AI Act (Article 26(5)) | Serious incident report to the market surveillance authority | — | — |

Keep in mind that one event can set off all four regimes at once. A cyberattack on a bank that exposes personal data and disrupts services is the classic example.

### Shared security obligations

The same core controls show up in several regulations, each with its own emphasis:

| Control area | GDPR | NIS2 | DORA |
|---|---|---|---|
| Risk assessment | Article 32 | Article 21(a) | Article 6 (framework), Article 8 (identification) |
| Incident handling | Articles 33–34 | Article 23 | Article 17 (process), Articles 19–20 (reporting) |
| Business continuity | — | Article 21(c) | Articles 11–12 |
| Supply chain security | Article 28 | Article 21(d) | Articles 28–30 |

Where obligations coincide, recommend running a single consolidated compliance program rather than parallel efforts.

### Who is accountable, and the maximum penalties

Penalty figures are the maximums as enacted; verify current amounts and how each member state has implemented them.

| Regulation | Accountability mechanism | Maximum penalty |
|---|---|---|
| GDPR | Controller accountability principle; requirements to designate a DPO (Articles 5(2), 24, 37) | EUR 20M or 4% of global annual turnover, whichever is higher (Article 83) |
| AI Act | Deployers are responsible for human oversight and for organizational measures (Articles 14, 26) | EUR 35M or 7% of global annual turnover, for prohibited practices (Article 99) |
| NIS2 | Personal liability for management bodies; cybersecurity training is mandatory (Article 20) | EUR 10M or 2% of turnover for essential entities; EUR 7M or 1.4% for important entities (Article 34) |
| DORA | Individual accountability for managing ICT risk; the ICT risk tolerance is defined and approved by the management body (Article 5) | Differs from one member state to another; critical ICT providers can face periodic penalty payments (Articles 35, 50) |

## Germany: works council co-determination for AI

**The trigger (BetrVG Section 87(1) No. 6).** Co-determination rights of the works council apply to any AI system that is *capable* of monitoring how employees behave, whether or not monitoring is its purpose. What counts is the system's objective capability to monitor, not anyone's subjective intent.

**When to bring in the Betriebsrat.** Treat any of these as a reason to involve it:

- introducing a new AI tool that employees interact with;
- changing the scope of an AI tool already in use;
- using AI in HR processes;
- deploying analytics or monitoring tools.

**What to record when co-determination applies:** what the tool does, which groups of employees it affects, what data it processes, and whether it could monitor behavior (what it could objectively do counts, not what it is said to be for). Involve the Betriebsrat from the start, both at introduction and whenever material changes are made. Recurring AI rollouts are often structured through framework agreements (Rahmen-Betriebsvereinbarungen). Have employment counsel validate the outcome of negotiations and local practice.

## Checking what is current

Whenever the user needs up-to-date specifics (recent amendments, implementing acts, where transposition stands, enforcement dates, current penalty amounts, or new case law), verify them online rather than relying on training data alone.

- **How:** use the web search tools available to find the current status or recent developments, and URL reading tools to open specific regulatory texts or guidance from authoritative sources.
- **If those tools aren't available:** web search and URL access are not enabled in every workspace. When they are missing, tell the user so plainly and advise them to check current details against the authoritative sources below.
- **Where to look first:** rank these authoritative sites above ordinary web results.

  | Need | Sites |
  |---|---|
  | Court rulings | curia.europa.eu for judgments of the CJEU; dejure.org for German judgments plus commentary on statutes |
  | DORA supervision | the three European Supervisory Authorities: eba.europa.eu, esma.europa.eu, eiopa.europa.eu |
  | German federal rules | bfdi.bund.de for the federal data protection authority; bsi.bund.de for the BSI and how NIS2 is implemented; gesetze-im-internet.de for the statutes themselves |
  | EU legislation and guidance | ec.europa.eu for Commission FAQs and guidance; eur-lex.europa.eu for the official legal texts |

- **Reconcile with this skill:** always check what you find online against the method and frameworks here. This skill supplies the analytical structure and decision trees; the search supplies current specifics such as dates, status, and recent changes. Point out any discrepancy between the two.

## Supporting reference files

If these reference files are bundled with the skill, load them when the matching question comes up:

- When the question is what a deployer owes under the AI Act: `references/ai-act-deployer.md`
- When you assess whether and how to consult the Betriebsrat on AI: `references/betriebsrat-ai.md`
- When you work through DORA obligations: `references/dora-overview.md`
- When you work through NIS2 obligations: `references/nis2-requirements.md`

## Ground rules

1. **Cite the article.** Every statement about a compliance obligation must name the article it comes from (for example, "per NIS2 Article 21(a)").
2. **No entity-specific compliance verdicts of your own.** Determinations about a particular organization must be based on that organization's own data.
3. **Assume things may have changed.** Adequacy decisions, enforcement actions, and deadlines move, so always flag them for verification of their current status.
4. **Point to specialist counsel** whenever a regulatory question is novel or the stakes are high.
