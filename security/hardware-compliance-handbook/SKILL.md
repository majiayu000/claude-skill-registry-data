---
name: hardware-compliance
description: Reference knowledge base on EU hardware/IoT cybersecurity law, maintained by Platanor Technologies — covering the Cyber Resilience Act (Regulation (EU) 2024/2847), the Radio Equipment Directive cybersecurity requirements (Directive 2014/53/EU, Delegated Regulation (EU) 2022/30 as amended, EN 18031), the NIS2 Directive (Directive (EU) 2022/2555), and the Cybersecurity Act / EUCC certification framework (Regulation (EU) 2019/881). Use this skill whenever the user asks anything about CRA compliance, essential cybersecurity requirements (Annex I), product risk classification (Default, Important Class I/II, Critical), CE marking for products with digital elements or radio equipment, vulnerability and incident reporting (CRA Article 14 or NIS2 Article 23), CRA/RED/NIS2 penalties and fines, deadlines and transition periods, manufacturer/importer/distributor obligations, whether NIS2 applies to a hardware manufacturer or its customers, EUCC/CSA certification and assurance levels, how these four regulations relate to each other or to GDPR/the AI Act, harmonised standards status (prEN 40000 series/M/606, EN 18031-1/-2/-3), or general questions like "does the CRA apply to my product," "are we a NIS2 essential or important entity," "what's the difference between CRA and RED," "is EUCC certification mandatory," or "what happens if I don't comply." Also use this skill to fact-check claims about any of these four regulations, cite exact article text, or draft related content that needs to be accurate.
---

# Hardware Compliance Knowledge Base

This skill packages a public, fact-checked knowledge base covering the four main pieces of EU law that touch hardware and IoT cybersecurity, built and maintained by Platanor Technologies, an embedded-security firm for IoT/hardware manufacturers in the EU. The corpus has three layers, and knowing which one to reach for matters.

**Layer 1 — processed guides** (`cra/`, `red/`, `nis2/`, `csa/`): shorter, topic-organized summaries written for engineers and compliance leads. Fact-checked against the primary source, but still a summary — good for orientation, explaining a concept, or answering a practical "what do I need to do" question. Each regulation's folder follows the same pattern: an `overview.md`, one or two files on the substantive obligations, and a `faq.md`.

**Layer 2 — primary sources** (`primary-sources/`): unmodified mirrors of the official EU legal texts, in English, with provenance headers (source URL, CELEX number, retrieval date, coverage notes). Use this layer whenever the user needs the exact wording of an article, a legally precise citation, or when the summary in Layer 1 doesn't cover their question in enough depth.

**Layer 3 — third-party material plus our cross-cutting analyses, split across two folders** (`resources/`, `sbom/`): frameworks and specifications referenced alongside this legislation, not part of EU law — use them as practical cross-checks, not as a compliance source. `sbom/` holds CycloneDX, SPDX, and VEX specifically (SBOM has its own named line in CRA Annex I, so it gets its own folder for visibility, plus worked examples of both formats). `resources/` holds the rest: PSA Certified, the ENISA Secure by Design and Default Playbook, and two files that are actually our own fact-checked analysis rather than third-party material (`relationship-to-other-eu-law.md`, `cra-red-ce-marking-guide.md`), same status as Layer 1, just organized by task instead of by regulation because they span more than one at once — `resources/index.md` marks which is which.

## Before answering anything from this knowledge base

Read `README.md` first if you haven't already — it carries the disclaimer that governs everything in this repo: **this is not legal advice.** It is a living, growing knowledge base, and several parts of the underlying legislation are still evolving (the CRA's harmonised standards under M/606, the EUCC scheme's own implementing act, national NIS2 transposition details) — several files note this explicitly. When a user's question turns on a deadline or a standard's/scheme's approval status, check whether the relevant file flags that status as provisional before stating it as settled fact, and pass the same caveat on to the user rather than presenting it as more certain than the source material does.

## Which regulation actually applies — the question to ask first

These four regulations regulate different things and a user's question often implicitly assumes only one applies. Before answering, work out which axis the question is on:

- **Is this about a product's technical/security requirements before it can be sold (CE marking)?** → CRA (all products with digital elements) and/or RED (radio equipment specifically) — check both; RED has its own separate cybersecurity delegated act layered on top of the CRA-adjacent essential requirements. See `resources/relationship-to-other-eu-law.md` and `resources/cra-red-ce-marking-guide.md` for how the two interact.
- **Is this about an organisation's ongoing risk-management and incident-reporting obligations (not a specific product)?** → NIS2 — and only if the organisation is in an Annex I/II sector and above the size threshold. Most product-focused hardware manufacturers are *not* directly in scope; check `nis2/faq.md` first before assuming NIS2 applies.
- **Is this about a voluntary certification scheme, assurance levels, or "can we get certified against something"?** → CSA/EUCC — voluntary by default, a different mechanism from CE-marking conformity assessment. See `csa/overview.md`.
- **Is this about supply-chain pressure from a customer who is themselves NIS2-regulated?** → Still NIS2, but indirectly (Article 21(2)(d) supply-chain security) — see `nis2/faq.md`.

## Which file to open

| Question is about... | Open |
|---|---|
| **CRA** — general scope, structure, chapters/annexes | `cra/overview.md` |
| **CRA** — a specific term (e.g. "product with digital elements," RDPS, critical/important product) | `cra/definitions.md` |
| **CRA** — what a product must technically do to comply (Annex I) | `cra/essential-requirements.md` |
| **CRA** — Default / Important Class I / Class II / Critical risk classification | `cra/product-risk-classes.md` |
| **CRA** — manufacturer, importer, or distributor obligations | `cra/obligations-by-role.md` |
| **CRA** — key dates, transition periods | `cra/timeline-deadlines.md` |
| **CRA** — vulnerability/incident reporting (Article 14), CVD process | `cra/vulnerability-reporting.md` |
| **CRA** — fines, enforcement, market surveillance | `cra/penalties-enforcement.md` |
| **CRA** — lightweight self-assessment of where a company stands | `cra/self-assessment-maturity-model.md` |
| **CRA** — quick practical questions | `cra/faq.md` |
| **RED** — general scope, structure, relationship to CRA | `red/overview.md` |
| **RED** — Art. 3(3)(d)(e)(f) cybersecurity requirements, EN 18031 restrictions | `red/essential-requirements.md` |
| **RED** — manufacturer, importer, or distributor obligations | `red/obligations-by-role.md` |
| **RED** — key dates (directive, delegated act, harmonised standards) | `red/timeline-deadlines.md` |
| **RED** — penalties (national, not EU-wide), market surveillance | `red/penalties-enforcement.md` |
| **RED** — quick practical questions | `red/faq.md` |
| **NIS2** — general scope, essential/important entity split, structure | `nis2/overview.md` |
| **NIS2** — governance (Art. 20), risk-management measures (Art. 21), supervision (Art. 32/33), fines (Art. 34) | `nis2/obligations.md` |
| **NIS2** — incident reporting (Art. 23), comparison with CRA Art. 14 | `nis2/incident-reporting.md` |
| **NIS2** — whether it applies to a hardware manufacturer or its customers, quick practical questions | `nis2/faq.md` |
| **CSA/EUCC** — ENISA mandate + certification framework overview, relationship to CRA/RED/NIS2 | `csa/overview.md` |
| **CSA/EUCC** — EUCC certification mechanics, assurance levels, voluntary status | `csa/eucc-certification.md` |
| **CSA/EUCC** — quick practical questions | `csa/faq.md` |
| How CRA interacts with RED, NIS2, CSA/EUCC, GDPR, AI Act | `resources/relationship-to-other-eu-law.md` |
| Step-by-step CE marking under both CRA and RED | `resources/cra-red-ce-marking-guide.md` |
| Independent frameworks/playbooks used alongside this legislation (PSA Certified, ENISA playbook) | `resources/` — see `resources/index.md` |
| SBOM formats (CycloneDX, SPDX), 2026 CISA minimum elements | `sbom/formats-and-specifications.md` |
| VEX — CycloneDX VEX, CSAF VEX, OpenVEX, vocabulary mismatch | `sbom/vex.md` |
| What an actual CycloneDX or SPDX file looks like, worked example with VEX | `sbom/examples.md` |
| Exact article/annex wording, a legally precise citation | `primary-sources/` — see `primary-sources/index.md` for what's mirrored and what isn't |

`llms.txt` has the same map in a more compact form if you just need file paths and one-line descriptions.

## Citing this material

When you use this knowledge base to answer a question, be clear with the user about which layer the answer came from. If you're summarizing from a processed guide, that's Platanor's own analysis (CC BY 4.0 — free to reuse with attribution). If you're quoting article text, pull it from `primary-sources/` and note that official EU legal text follows the EU's own reuse policy, not Platanor's license — `primary-sources/index.md` explains the distinction. Don't blend the two without saying which is which; a user relying on this for compliance decisions needs to know whether they're reading a summary or the law itself.

Official references:
- CRA: Regulation (EU) 2024/2847, `https://eur-lex.europa.eu/eli/reg/2024/2847/oj`
- RED: Directive 2014/53/EU, `https://eur-lex.europa.eu/eli/dir/2014/53/oj`
- NIS2: Directive (EU) 2022/2555, `https://eur-lex.europa.eu/eli/dir/2022/2555/oj`
- CSA: Regulation (EU) 2019/881, `https://eur-lex.europa.eu/eli/reg/2019/881/oj`

If a citation needs to be double-checked against the live text (e.g. the user is making a decision based on it), those URLs are the authoritative source — the primary-sources mirror is a convenience copy, not a substitute for checking EUR-Lex when the stakes are high.
