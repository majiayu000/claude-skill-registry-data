---
name: entity-optimizer
description: 'Use when the user asks to "optimize entity presence", "build knowledge graph", "improve knowledge panel", "entity audit", "establish brand entity", "Google does not know my brand", "no knowledge panel", or "establish my brand as an entity". Works standalone with public search and AI query testing; supercharged when you connect ~~knowledge graph + ~~SEO tool + ~~AI monitor for automated entity analysis. For structured data implementation, see schema-markup-generator. For content-level AI optimization, see geo-content-optimizer.'
license: Apache-2.0
metadata:
  author: aaron-he-zhu
  version: "2.0.0"
  geo-relevance: "high"
  tags:
    - seo
    - geo
    - entity optimization
    - knowledge graph
    - knowledge panel
    - brand entity
    - entity disambiguation
    - wikidata
    - structured entities
  triggers:
    - "optimize entity presence"
    - "build knowledge graph"
    - "improve knowledge panel"
    - "entity audit"
    - "establish brand entity"
    - "knowledge panel"
    - "entity disambiguation"
    - "Google doesn't know my brand"
    - "no knowledge panel"
    - "establish my brand as an entity"
---

# Entity Optimizer

This skill audits, builds, and maintains entity identity across search engines and AI systems. Entities — the people, organizations, products, and concepts that search engines and AI systems recognize as distinct things — are the foundation of how both Google and LLMs decide *what you are* and *whether to cite you*.

**Why entities matter for SEO + GEO:**

- **SEO**: Google's Knowledge Graph powers Knowledge Panels, rich results, and entity-based ranking signals. A well-defined entity earns SERP real estate.
- **GEO**: AI systems resolve queries to entities before generating answers. If an AI can't identify your entity, it can't cite you — no matter how good your content is.

## When to Use This Skill

- Establishing a new brand/person/product as a recognized entity
- Auditing current entity presence across Knowledge Graph, Wikidata, and AI systems
- Improving or correcting a Knowledge Panel
- Building entity associations (entity ↔ topic, entity ↔ industry)
- Resolving entity disambiguation issues (your entity confused with another)
- Strengthening entity signals for AI citation
- After launching a new brand, product, or organization
- Preparing for a site migration (preserving entity identity)
- Running periodic entity health checks

## What This Skill Does

1. **Entity Audit**: Evaluates current entity presence across search and AI systems
2. **Knowledge Graph Analysis**: Checks Google Knowledge Graph, Wikidata, and Wikipedia status
3. **AI Entity Resolution Test**: Queries AI systems to see how they identify and describe the entity
4. **Entity Signal Mapping**: Identifies all signals that establish entity identity
5. **Gap Analysis**: Finds missing or weak entity signals
6. **Entity Building Plan**: Creates actionable plan to establish or strengthen entity presence
7. **Disambiguation Strategy**: Resolves confusion with similarly-named entities

## How to Use

### Entity Audit

```
Audit entity presence for [brand/person/organization]
```

```
How well do search engines and AI systems recognize [entity name]?
```

### Build Entity Presence

```
Build entity presence for [new brand] in the [industry] space
```

```
Establish [person name] as a recognized expert in [topic]
```

### Fix Entity Issues

```
My Knowledge Panel shows incorrect information — fix entity signals for [entity]
```

```
AI systems confuse [my entity] with [other entity] — help me disambiguate
```

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

**With ~~knowledge graph + ~~SEO tool + ~~AI monitor + ~~brand monitor connected:**
Query Knowledge Graph API for entity status, pull branded search data from ~~SEO tool, test AI citation with ~~AI monitor, track brand mentions with ~~brand monitor.

**With manual data only:**
Ask the user to provide:
1. Entity name, type (Person, Organization, Brand, Product, Creative Work, Event)
2. Primary website / domain
3. Known existing profiles (Wikipedia, Wikidata, social media, industry directories)
4. Top 3-5 topics/industries the entity should be associated with
5. Any known disambiguation issues (other entities with same/similar name)

Without tools, Claude provides entity optimization strategy and recommendations based on information the user provides. The user must run search queries, check Knowledge Panels, and test AI responses to supply the raw data for analysis.

Proceed with the audit using public search results, AI query testing, and SERP analysis. Note which items require tool access for full evaluation.

## Instructions

When a user requests entity optimization:

### Step 1: Entity Discovery

Establish the entity's current state across all systems.

```markdown
### Entity Profile

**Entity Name**: [name]
**Entity Type**: [Person / Organization / Brand / Product / Creative Work / Event]
**Primary Domain**: [URL]
**Target Topics**: [topic 1, topic 2, topic 3]

#### Current Entity Presence

| Platform | Status | Details |
|----------|--------|---------|
| Google Knowledge Panel | ✅ Present / ❌ Absent / ⚠️ Incorrect | [details] |
| Wikidata | ✅ Listed / ❌ Not listed | [QID if exists] |
| Wikipedia | ✅ Article / ⚠️ Mentioned only / ❌ Absent | [notability assessment] |
| Google Knowledge Graph API | ✅ Entity found / ❌ Not found | [entity ID, types, score] |
| Schema.org on site | ✅ Complete / ⚠️ Partial / ❌ Missing | [Organization/Person/Product schema] |

#### AI Entity Resolution Test

**Note**: Claude cannot directly query other AI systems or perform real-time web searches without tool access. When running without ~~AI monitor or ~~knowledge graph tools, ask the user to run these test queries and report the results, or use the user-provided information to assess entity presence.

Test how AI systems identify this entity by querying:
- "What is [entity name]?"
- "Who founded [entity name]?" (for organizations)
- "What does [entity name] do?"
- "[entity name] vs [competitor]"

| AI System | Recognizes Entity? | Description Accuracy | Cites Entity's Content? |
|-----------|-------------------|---------------------|------------------------|
| ChatGPT | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Claude | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Perplexity | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
| Google AI Overview | ✅ / ⚠️ / ❌ | [accuracy notes] | [yes/no/partially] |
```

### Step 2: Entity Signal Audit

Evaluate entity signals across 6 categories. For the detailed 47-signal checklist with verification methods, see [references/entity-signal-checklist.md](./references/entity-signal-checklist.md).

```markdown
### Entity Signal Audit

#### 1. Structured Data Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Organization/Person schema on homepage | ✅ / ❌ | [action] |
| sameAs links to authoritative profiles | ✅ / ❌ | [action] |
| logo, foundingDate, founder properties | ✅ / ❌ | [action] |
| Consistent @id across pages | ✅ / ❌ | [action] |
| Product/Service schema on relevant pages | ✅ / ❌ | [action] |
| Author schema with sameAs on articles | ✅ / ❌ | [action] |

#### 2. Knowledge Base Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Wikidata entry with complete properties | ✅ / ❌ | [action] |
| Wikipedia article (or notability path) | ✅ / ❌ | [action] |
| CrunchBase profile (organizations) | ✅ / ❌ | [action] |
| Industry directory listings | ✅ / ❌ | [action] |
| Government/official registries | ✅ / ❌ | [action] |

#### 3. Consistent NAP+E Signals (Name, Address, Phone + Entity)

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Consistent entity name across all platforms | ✅ / ❌ | [action] |
| Same description/tagline everywhere | ✅ / ❌ | [action] |
| Matching logos and visual identity | ✅ / ❌ | [action] |
| Social profiles all linked bidirectionally | ✅ / ❌ | [action] |
| Contact info consistent across directories | ✅ / ❌ | [action] |

#### 4. Content-Based Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| About page with entity-rich structured content | ✅ / ❌ | [action] |
| Author pages with credentials and sameAs | ✅ / ❌ | [action] |
| Topical authority (content depth in target topics) | ✅ / ❌ | [action] |
| Entity mentions in content (natural co-occurrence) | ✅ / ❌ | [action] |
| Branded anchor text in backlinks | ✅ / ❌ | [action] |

#### 5. Third-Party Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Mentions on authoritative sites (news, industry) | ✅ / ❌ | [action] |
| Co-citation with established entities | ✅ / ❌ | [action] |
| Reviews and ratings on third-party platforms | ✅ / ❌ | [action] |
| Speaking engagements, awards, publications | ✅ / ❌ | [action] |
| Press coverage with entity name | ✅ / ❌ | [action] |

#### 6. AI-Specific Entity Signals

| Signal | Status | Action Needed |
|--------|--------|--------------|
| Clear entity definition in opening paragraphs | ✅ / ❌ | [action] |
| Unambiguous entity name (or disambiguation strategy) | ✅ / ❌ | [action] |
| Factual claims about entity are verifiable | ✅ / ❌ | [action] |
| Entity appears in AI training data sources | ✅ / ❌ | [action] |
| Entity's content is crawlable by AI systems | ✅ / ❌ | [action] |
```

### Step 3: Report & Action Plan

```markdown
## Entity Optimization Report

### Overview

- **Entity**: [name]
- **Entity Type**: [type]
- **Audit Date**: [date]

### Signal Category Summary

| Category | Status | Key Findings |
|----------|--------|-------------|
| Structured Data | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Knowledge Base | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Consistency (NAP+E) | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Content-Based | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| Third-Party | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |
| AI-Specific | ✅ Strong / ⚠️ Gaps / ❌ Missing | [key findings] |

### Critical Issues

[List any issues that severely impact entity recognition — disambiguation problems, incorrect Knowledge Panel, missing from Knowledge Graph entirely]

### Top 5 Priority Actions

Sorted by: impact on entity recognition × effort required

1. **[Signal]** — [specific action]
   - Impact: [High/Medium] | Effort: [Low/Medium/High]
   - Why: [explanation of how this improves entity recognition]

2. **[Signal]** — [specific action]
   - Impact: [High/Medium] | Effort: [Low/Medium/High]
   - Why: [explanation]

3–5. [Same format]

### Entity Building Roadmap

#### Week 1-2: Foundation (Structured Data + Consistency)
- [ ] Implement/fix Organization or Person schema with full properties
- [ ] Add sameAs links to all authoritative profiles
- [ ] Audit and fix NAP+E consistency across all platforms
- [ ] Ensure About page is entity-rich and well-structured

#### Month 1: Knowledge Bases
- [ ] Create or update Wikidata entry with complete properties
- [ ] Ensure CrunchBase / industry directory profiles are complete
- [ ] Build Wikipedia notability (or plan path to notability)
- [ ] Submit to relevant authoritative directories

#### Month 2-3: Authority Building
- [ ] Secure mentions on authoritative industry sites
- [ ] Build co-citation signals with established entities
- [ ] Create topical content clusters that reinforce entity-topic associations
- [ ] Pursue PR opportunities that generate entity mentions

#### Ongoing: AI-Specific Optimization
- [ ] Test AI entity resolution quarterly
- [ ] Update factual claims to remain current and verifiable
- [ ] Monitor AI systems for incorrect entity information
- [ ] Ensure new content reinforces entity identity signals

### Cross-Reference

- **CORE-EEAT relevance**: Items A07 (Knowledge Graph Presence) and A08 (Entity Consistency) directly overlap — entity optimization strengthens Authority dimension
- **CITE relevance**: CITE I01-I10 (Identity dimension) measures entity signals at domain level — entity optimization feeds these scores
- For content-level audit: [content-quality-auditor](../content-quality-auditor/)
- For domain-level audit: [domain-authority-auditor](../domain-authority-auditor/)
```

## Validation Checkpoints

### Input Validation
- [ ] Entity name and type identified
- [ ] Primary domain/website confirmed
- [ ] Target topics/industries specified
- [ ] Disambiguation context provided (if entity name is common)

### Output Validation
- [ ] All 6 signal categories evaluated
- [ ] AI entity resolution tested with at least 3 queries
- [ ] Knowledge Panel status checked
- [ ] Wikidata/Wikipedia status verified
- [ ] Schema.org markup on primary site audited
- [ ] Every recommendation is specific and actionable
- [ ] Roadmap includes concrete steps with timeframes
- [ ] Cross-reference with CORE-EEAT A07/A08 and CITE I01-I10 noted

## Example

**User**: "Audit entity presence for CloudMetrics, our B2B SaaS analytics platform at cloudmetrics.io"

**Output**:

```markdown
## Entity Optimization Report

### Entity Profile

**Entity Name**: CloudMetrics
**Entity Type**: Organization (B2B SaaS)
**Primary Domain**: cloudmetrics.io
**Target Topics**: analytics platform, business intelligence, enterprise analytics

### AI Entity Resolution Test

Queries tested with results reported by user:

| Query | Result | Assessment |
|-------|--------|------------|
| "What is CloudMetrics?" | Described as "an analytics tool" with no further detail | Partial recognition -- generic description, no mention of B2B focus or key features |
| "Best analytics platforms for enterprises" | CloudMetrics not mentioned in any AI response | Not recognized as a player in the enterprise analytics space |
| "CloudMetrics vs Datadog" | Correctly identified as a competitor to Datadog, but feature comparison was incomplete and partially inaccurate | Partial -- entity is associated with the right category but attributes are thin |
| "Who founded CloudMetrics?" | No answer found by any AI system tested | Entity leadership not present in AI knowledge bases |

### Entity Health Summary

| Signal Category | Status | Key Findings |
|-----------------|--------|--------------|
| Knowledge Graph | ❌ Missing | No Wikidata entry exists; no Google Knowledge Panel triggers for branded queries |
| Structured Data | ⚠️ Partial | Organization schema present on homepage with name, url, and logo; missing Person schema for CEO and leadership team; no sameAs links to external profiles |
| Web Presence | ✅ Strong | Consistent NAP across LinkedIn, Twitter/X, G2, and Crunchbase; social profiles link back to cloudmetrics.io; branded search returns owned properties in top 5 |
| Content-Based | ⚠️ Partial | About page exists but opens with marketing copy rather than an entity-defining statement; no dedicated author pages for leadership |
| Third-Party | ⚠️ Partial | Listed on G2 and Crunchbase; 2 industry publication mentions found; no awards or analyst coverage |
| AI-Specific | ❌ Weak | AI systems have only surface-level awareness; entity definition is not quotable from any authoritative source |

### Top 3 Priority Actions

1. **Create Wikidata entry** with key properties: instance of (P31: business intelligence software company), official website (P856: cloudmetrics.io), inception (P571), country (P17)
   - Impact: High | Effort: Low
   - Why: Wikidata is the foundational knowledge base that feeds Google Knowledge Graph, Bing, and AI training pipelines; without it, the entity cannot be formally resolved

2. **Add Person schema for leadership team** on the About/Team page, including name, jobTitle, sameAs links to LinkedIn profiles, and worksFor pointing to the Organization entity
   - Impact: High | Effort: Low
   - Why: Addresses the "Who founded CloudMetrics?" gap directly; Person schema for key people creates bidirectional entity associations that strengthen organizational identity

3. **Build Wikipedia notability through independent press coverage** -- target 3-5 articles in industry publications (TechCrunch, VentureBeat, Analytics India Magazine) that mention CloudMetrics by name with verifiable claims
   - Impact: High | Effort: High
   - Why: Wikipedia notability requires coverage in independent reliable sources; press mentions simultaneously feed AI training data, build third-party entity signals, and create the citation foundation for a future Wikipedia article

### Cross-Reference

- **CORE-EEAT**: A07 (Knowledge Graph Presence) scored Fail, A08 (Entity Consistency) scored Pass -- entity optimization should focus on knowledge base gaps rather than consistency
- **CITE**: I-dimension weakest area is I01 (Knowledge Graph Presence) -- completing Wikidata entry and earning Knowledge Panel directly improves domain identity score
```

## Tips for Success

1. **Start with Wikidata** — It's the single most influential editable knowledge base; a complete Wikidata entry with references often triggers Knowledge Panel creation within weeks
2. **sameAs is your most powerful Schema.org property** — It directly tells search engines "I am this entity in the Knowledge Graph"; always include Wikidata URL first
3. **Test AI recognition before and after** — Query ChatGPT, Claude, Perplexity, and Google AI Overview before optimizing, then again after; this is the most direct GEO metric
4. **Entity signals compound** — Unlike content SEO, entity signals from different sources reinforce each other; 5 weak signals together are stronger than 1 strong signal alone
5. **Consistency beats completeness** — A consistent entity name and description across 10 platforms beats a perfect profile on just 2
6. **Don't neglect disambiguation** — If your entity name is shared with anything else, disambiguation is the first priority; all other signals are wasted if they're attributed to the wrong entity
7. **Pair with CITE I-dimension for domain context** — Entity audit tells you how well the entity is recognized; CITE Identity (I01-I10) tells you how well the domain represents that entity; use both together

## Entity Type Reference

### Entity Types and Key Signals

| Entity Type | Primary Signals | Secondary Signals | Key Schema |
|-------------|----------------|-------------------|------------|
| **Person** | Author pages, social profiles, publication history | Speaking, awards, media mentions | Person, ProfilePage |
| **Organization** | Registration records, Wikidata, industry listings | Press coverage, partnerships, awards | Organization, Corporation |
| **Brand** | Trademark, branded search volume, social presence | Reviews, brand mentions, visual identity | Brand, Organization |
| **Product** | Product pages, reviews, comparison mentions | Awards, expert endorsements, market share | Product, SoftwareApplication |
| **Creative Work** | Publication record, citations, reviews | Awards, adaptations, cultural impact | CreativeWork, Book, Movie |
| **Event** | Event listings, press coverage, social buzz | Sponsorships, speaker profiles, attendance | Event |

### Disambiguation Strategy by Situation

| Situation | Strategy |
|-----------|----------|
| **Common name, unique entity** | Strengthen all signals; let signal volume resolve ambiguity |
| **Name collision with larger entity** | Add qualifier consistently (e.g., "Acme Software" not just "Acme"); use sameAs extensively; build topic-specific authority that differentiates |
| **Name collision with similar entity** | Geographic, industry, or product qualifiers; ensure Schema @id is unique and consistent; prioritize Wikidata disambiguation |
| **Abbreviation/acronym conflict** | Prefer full name in structured data; use abbreviation only in contexts where entity is already established |
| **Merged or renamed entity** | Redirect old entity signals; update all structured data; create explicit "formerly known as" content; update Wikidata |

## Knowledge Panel Optimization

### Claiming and Editing

1. **Google Knowledge Panel**: Claim via Google's verification process (search for entity → click "Claim this knowledge panel")
2. **Bing Knowledge Panel**: Driven by Wikidata and LinkedIn — update those sources
3. **AI Knowledge**: Driven by training data — ensure authoritative sources describe entity correctly

### Common Knowledge Panel Issues

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| No panel appears | Entity not in Knowledge Graph | Build Wikidata entry + structured data + authoritative mentions |
| Wrong image | Image sourced from incorrect page | Update Wikidata image; ensure preferred image on About page and social profiles |
| Wrong description | Description pulled from wrong source | Edit Wikidata description; ensure About page has clear entity description in first paragraph |
| Missing attributes | Incomplete structured data | Add properties to Schema.org markup and Wikidata entry |
| Wrong entity shown | Disambiguation failure | Strengthen unique signals; add qualifiers; resolve Wikidata disambiguation |
| Outdated info | Source data not updated | Update Wikidata, About page, and all profile pages |

## Wikidata Best Practices

### Creating a Wikidata Entry

1. **Check notability**: Entity must have at least one authoritative reference
2. **Create item**: Add label, description, and aliases in relevant languages
3. **Add statements**: instance of, official website, social media links, founding date, founders, industry
4. **Add identifiers**: official website (P856), social media IDs, CrunchBase ID, ISNI, VIAF
5. **Add references**: Every statement should have a reference to an authoritative source

**Important**: Wikipedia's Conflict of Interest (COI) policy prohibits individuals and organizations from creating or editing articles about themselves. Instead of directly editing Wikipedia: (1) Focus on building notability through independent reliable sources (press coverage, industry publications, academic citations); (2) If you believe a Wikipedia article is warranted, consider engaging an independent Wikipedia editor through the Requested Articles process; (3) Ensure all claims about the entity are verifiable through third-party sources before any Wikipedia involvement.

### Key Wikidata Properties by Entity Type

| Property | Code | Person | Org | Brand | Product |
|----------|------|:------:|:---:|:-----:|:-------:|
| instance of | P31 | human | organization type | brand | product type |
| official website | P856 | yes | yes | yes | yes |
| occupation / industry | P106/P452 | yes | yes | — | — |
| founded by | P112 | — | yes | yes | — |
| inception | P571 | — | yes | yes | yes |
| country | P17 | yes | yes | — | — |
| social media | various | yes | yes | yes | yes |
| employer | P108 | yes | — | — | — |
| developer | P178 | — | — | — | yes |

## AI Entity Optimization

### How AI Systems Resolve Entities

```
User query → Entity extraction → Entity resolution → Knowledge retrieval → Answer generation
```

AI systems follow this pipeline:
1. **Extract** entity mentions from the query
2. **Resolve** each mention to a known entity (or fail → "I'm not sure")
3. **Retrieve** associated knowledge about the entity
4. **Generate** response citing sources that confirmed the entity's attributes

### Signals AI Systems Use for Entity Resolution

| Signal Type | What AI Checks | How to Optimize |
|-------------|---------------|-----------------|
| **Training data presence** | Was entity in pre-training corpus? | Get mentioned in high-quality, widely-crawled sources |
| **Retrieval augmentation** | Does entity appear in live search results? | Strong SEO presence for branded queries |
| **Structured data** | Can entity be matched to Knowledge Graph? | Complete Wikidata + Schema.org |
| **Contextual co-occurrence** | What topics/entities appear alongside? | Build consistent topic associations across content |
| **Source authority** | Are sources about entity trustworthy? | Get mentioned by authoritative, well-known sources |
| **Recency** | Is information current? | Keep all entity profiles and content updated |

### Entity-Specific GEO Tactics

1. **Define clearly**: First paragraph of About page and key pages should define the entity in a way AI can quote directly
2. **Be consistent**: Use identical entity description across all platforms
3. **Build associations**: Create content that explicitly connects entity to target topics
4. **Earn mentions**: Third-party authoritative mentions are stronger entity signals than self-description
5. **Stay current**: Outdated entity information causes AI to lose confidence and stop citing

## Reference Materials

Detailed guides for entity optimization:
- [references/entity-signal-checklist.md](./references/entity-signal-checklist.md) — Complete signal checklist with verification methods
- [references/knowledge-graph-guide.md](./references/knowledge-graph-guide.md) — Wikidata, Wikipedia, and Knowledge Graph optimization playbook

## Related Skills

- [content-quality-auditor](../content-quality-auditor/) — CORE-EEAT items A07 (Knowledge Graph Presence) and A08 (Entity Consistency) directly relate
- [domain-authority-auditor](../domain-authority-auditor/) — CITE I01-I10 (Identity dimension) measures entity signals at domain level
- [schema-markup-generator](../../build/schema-markup-generator/) — Generate Organization, Person, Product, and other entity schema
- [geo-content-optimizer](../../build/geo-content-optimizer/) — Entity signals feed AI citation probability
- [competitor-analysis](../../research/competitor-analysis/) — Compare entity presence against competitors
- [backlink-analyzer](../../monitor/backlink-analyzer/) — Branded backlinks strengthen entity signals
- [performance-reporter](../../monitor/performance-reporter/) — Track branded search and Knowledge Panel metrics
- [memory-management](../memory-management/) — Store entity audit results for tracking over time
