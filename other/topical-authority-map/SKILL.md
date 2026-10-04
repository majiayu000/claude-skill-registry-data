---
name: topical-authority-map
description: Builds a 4-cluster Topical Authority Map from a seed keyword. Outputs an .xlsx spreadsheet with five tabs (Core Pages, AOR Pages, Linking Map, Buyer Journey, Publishing Order) plus a markdown strategy document. Interactive, asks the user to confirm central entity, source context, persona, classification, and gaps at five checkpoints. Trigger when the user provides a seed keyword, niche, business type, or asks for a topical map, content plan, site architecture, topic cluster, or publishing roadmap.
---

You are building a Topical Authority Map. This is a structured site architecture that mirrors how Google and AI search engines decide which sites are the specialist on a topic. It is NOT a keyword list. It is NOT a list of topics. It is the blueprint for an entire website's content strategy, built around a single central entity and routed through four connected clusters.

The four clusters:

1. **Core Pages** (the money pages users buy from)
2. **AOR Pages** (Areas of Relevance, the supporting authority articles)
3. **Linking Map** (which page links to which page, with what anchor text)
4. **Buyer Journey** (every page tagged TOFU, MOFU, or BOFU)

Plus a fifth output: a 12-week Publishing Order with content briefs that turns the map into a content plan.

**Output:** Two deliverables.

1. `.xlsx` spreadsheet with five tabs: Core Pages, AOR Pages, Linking Map, Buyer Journey, Publishing Order.
2. `.md` strategy document covering central entity, source context, persona, folder structure, linking rules, NLP alignment, and quality standards.

**Mode:** Interactive. Pause at the five checkpoints marked with the checkpoint emoji to confirm decisions with the user before proceeding. Do not skip checkpoints.

---

## Why topical maps work

Topical maps work because of five mechanics, not because of E-E-A-T marketing:

1. **Historical user data accumulation.** Every visitor adds data to Google's view of your site. A topical map concentrates that data on one topic so Google has more evidence you satisfy users on that topic. Spread the data across four unrelated topics and you lose on all four.
2. **Knowledge Graph alignment.** Google has entities with attributes and relationships. Your map configures the site to MATCH what Google already knows about your entity. Match the structure and Google retrieves your pages cheaply.
3. **Lower cost of retrieval.** Every title, heading, paragraph, and image should map to a real query. Cheap-to-retrieve pages outrank expensive-to-retrieve pages on every relevance signal.
4. **Satisfaction signal transfer.** When an AOR page satisfies a user, that signal transfers to the core pages it links to. More AOR pages, more satisfaction signals, stronger core pages.
5. **Index construction efficiency.** It is cheaper for Google to rank one site for a million related queries than to rank a million different sites for one query each. Deep architecture lets Google serve the whole topic from your domain.

**Critical warning:** A topical map filled with low-quality content hurts the whole site. Bad pages drag every other page down. Do not publish to fill the map. Every article must be quality work. If you cannot write a good article on a topic, leave it out.

---

## Execution order

Load reference files as you progress through each phase. Complete every checkpoint before moving on.

**Phase 1: Research and classification** (load `references/01-research-and-classify.md`)
- Step 1: Define the central entity (Checkpoint 1)
- Step 2: Source context plus persona (Checkpoint 2)
- Step 3: Deep research on Knowledge Graph, competitors, client situations, attributes (Checkpoint 3)
- Step 4: Classify each attribute as Core or AOR
- Step 5: Merge and split decisions plus depth calibration (Checkpoint 4)

**Phase 2: Architecture and keywords** (load `references/02-architecture-and-keywords.md`)
- Step 6: Define folder structure
- Step 7: Map every page to TOFU, MOFU, or BOFU (Checkpoint 5)
- Step 8: Query expansion plus cost of retrieval scoring
- Step 9: Keyword selection for page titles
- Step 10: Define the linking architecture

**Phase 3: Execution and output** (load `references/03-execution-and-output.md`)
- Step 11: Central entity sitewide presence
- Step 12: NLP category alignment check
- Step 13: Content briefs for the first 30 articles
- Step 14: Publishing order across 12 weeks
- Generate the .xlsx with five tabs
- Generate the strategy .md document

When you finish, present both deliverables to the user with a one-paragraph summary of what to read first (Core, then AOR, then Linking, then Buyer Journey, then Publishing Order) and where to start writing this week.

**The map is dynamic, not static.** Google's indexes change. Review and update the map quarterly.
