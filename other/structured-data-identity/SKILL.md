---
name: structured-data-identity
description: Selection-stage audit for machine-readable brand identity. Use when AI answers confuse a brand, fail to recognize its publisher, or structured data may be weak. Checks schema presence, validity and page-type fit; Organization completeness, sameAs, conflicting identities, and inconsistent business details.
license: MIT
---

# Structured Data & Identity (selection layer)

The selection layer decides whether a page is *eligible* to be chosen as a
source. arXiv:2604.25707 §7 finds that layer highly concentrated: official,
news and vertical sources account for **79.12% to 87.52%** of all citations
across the three platforms, with official sources alone at 34.22% (ChatGPT),
46.35% (Google AIO) and 44.07% (Perplexity).

Being recognised as the official source for an entity is therefore an entry
condition. This skill audits whether a machine can establish that identity at
all.

Note the boundary carefully: the paper is equally clear that identity does
**not** determine absorption. News media is selected constantly and absorbed
weakly (0.0726 mean influence against 0.2144 for encyclopedia pages, §8.4).
Fixing identity gets a brand into the pool; it does not make its pages matter
once they are there. That is `evidence-density`'s job.

## When to use

After `crawl-reachability` has built the page inventory. Run standalone when a
brand is being confused with something else, or when its pages are read but the
organisation behind them is not recognised.

```
python3 scripts/check_structured_data.py [--workspace PATH] [--json]
```

## Inputs

- **Required** — a workspace directory written by `url-validation` and
  `crawl-reachability`: `preflight.json` supplies the scope domain, and
  `reachability.json` supplies the page inventory.
- **Optional** — `--config` (an `AuditConfig` JSON) and `--strictness`
  (`lenient` | `balanced` | `strict`) to override the page-type expectation
  table. Defaults come from `AuditConfig`.
- **Not consumed** — no network access, no prior stage's findings. This layer
  reads only the pages `crawl-reachability` already fetched, so it is
  re-runnable offline and cheap.

```
python3 scripts/check_structured_data.py [--workspace PATH] [--json]
```

## Procedure

Deterministic, in this order. Each step is a pure function of the fetched
markup and the config — no sampling, no randomness, no wall-clock input.

1. **Load the inventory and pages.** Resolve the scope domain from `preflight`,
   then read every fetched page. Emit a coverage limitation for pages whose
   HTML is missing rather than silently skipping them.
2. **Presence (`SD001`, `SD008`).** Count pages whose type is expected to
   declare a machine-readable entity against pages that declare none, and
   separately detect identity carried only as microdata or RDFa.
3. **Parse validity (`SD002`).** Record which `application/ld+json` blocks fail
   to parse. Malformed blocks are *not* discarded silently — that is the
   finding.
4. **Type appropriateness (`SD003`).** Compare declared types against
   `expectations_for(page_type)`; skip page types with no enforced expectation.
5. **Completeness (`SD007`).** For each type actually present, check its
   required properties.
6. **Single-page conflicts (`SD011`).** Detect one page declaring two
   conflicting primary entity types.
7. **Organisation identity (`SD004`, `SD005`, `SD006`).** Check required
   `Organization` properties, whether any organisation entity is declared in
   the sample at all, and whether `sameAs` breadth is sufficient to
   disambiguate.
8. **Name disambiguation (`SD009`).** Flag common-noun brand names that are
   under-disambiguated.
9. **NAP consistency (`SD010`, `SD012`).** Normalise names, addresses and
   phones across pages; report cross-page contradictions and conflicting
   organisation names on a single page.
10. **Attach the sample caveat.** Any population claim carries the sample size
    it was drawn from, for the advisory layer to verify.

| Check | Detects | Severity | Claim level |
|---|---|---|---|
| `SD001` | Pages with no machine-readable entity declaration at all | high/medium | 1 |
| `SD002` | JSON-LD blocks that fail to parse and are silently discarded | high | 1 |
| `SD003` | Schema type inappropriate for the page type | medium | 1 |
| `SD004` | `Organization` node missing required properties | medium | 1 |
| `SD005` | No organisation entity declared anywhere in the sample | high | 1 |
| `SD006` | Too few `sameAs` references to disambiguate the entity | medium | 1 |
| `SD007` | Required properties missing for a declared type | medium | 1 |
| `SD008` | Structured data present only as microdata/RDFa, never JSON-LD | low | 3 |
| `SD009` | Common-noun brand name that is under-disambiguated | medium | 3 |
| `SD010` | Name, address or phone inconsistent across pages | medium | 1 |
| `SD011` | One page declaring two conflicting primary entity types | medium | 1 |
| `SD012` | Conflicting organisation names on the same page | medium | 1 |

`SD002` is rated above `SD001` deliberately. A page with no JSON-LD is
*ambiguous*; a page with malformed JSON-LD is *silently discarded*, so the site
believes it has structured data and does not.

## Page-type expectations

Type appropriateness is checked against `AuditConfig.expectations_for(page_type)`,
never against a universal list. A privacy policy is not expected to carry
`Product`; a contact page is not expected to carry `Article`. Flagging those is
the most common false positive in structured-data auditing, and the check is
skipped entirely for page types with no enforced expectation.

## Entity disambiguation

`sameAs` is the strongest available disambiguation signal: it links the entity
to identities elsewhere (Wikidata, LinkedIn, Crunchbase, official social
accounts). Handout appendix D describes the underlying problem directly — when
several things share a name, a system can mix them up unless something clearly
distinguishes one from the others.

`SD009` raises the bar for brands whose name is a common noun or a generic
word. Such a brand needs *more* corroborating identity signal than a
distinctive one, not the same amount, because the ambiguity is inherent to the
name rather than incidental. This is a mechanism-level claim and is capped at
`medium` accordingly.

## Output

`03-structured-data-identity.json` with per-page schema inventory, the entity
graph, the `sameAs` host list, NAP values observed per page, and the findings.

## Guardrails

Read-only; consumes saved HTML only and issues no requests of its own.

## Grounding

§7 source-type concentration (official + news + vertical = 79.12%–87.52% of
citations; `Final_DR` medians 526–592 indicating authority signals still gate
pool entry); §8.4 domain-type influence, which is what separates this skill's
job from `evidence-density`'s. Details in `references/schema-requirements.md`
and `references/entity-disambiguation.md`.
