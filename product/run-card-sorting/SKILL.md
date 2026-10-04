---
name: run-card-sorting
description: Use when designing or evaluating information architecture — navigation structure, menu labels, content categorization — to align the organization with how users mentally group and label concepts.
source: "NNG \"Card Sorting\" guideline; Spencer \"Card Sorting: Designing Usable Categories\" (Rosenfeld Media, 2009); IBM Design Thinking IA practices"
tags: [user-research, information-architecture, card-sorting, navigation, ia, ux-research, mental-models]
---

# Run Card Sorting

Have users group and label concepts on cards to reveal how they mentally organize the subject matter — then use those patterns to structure navigation, menus, and content hierarchies.

## Why This Is Best Practice

**Adopted by:** NNG positions card sorting as the primary research method for information architecture decisions; IBM Design Thinking uses open card sorting as the standard IA input method; OptimalSort (Optimal Workshop), Maze, and UserZoom include card sorting as a core research tool, reflecting widespread adoption across product and UX teams
**Impact:** NNG: card sorting with 15 users identifies 80%+ of IA problems before development; Spencer (2009) documents that navigation redesigns informed by card sorting reduce findability failures by 40–60% compared to designer-led IA; fixing IA post-launch — after content, nav, and URLs are established — costs 10–100× more than validating IA during design
**Why best:** Designer-led IA reflects the organization's internal structure (product features, team ownership) rather than users' mental models; analytics show where users go but not why they struggle; only card sorting reveals the categories users expect and the labels they use — inputs that cannot be inferred from usage data or expert review alone

Sources: NNG "Card Sorting" (Nielsen Norman Group, 2023); Spencer "Card Sorting: Designing Usable Categories" (Rosenfeld Media, 2009); Optimal Workshop "The Research Practice Guide: Card Sorting" (2022)

## Steps

### 1. Choose the study type

| Type | How it works | When to use |
|------|-------------|-------------|
| **Open** | Users create their own groups and labels | Designing IA from scratch; understanding users' mental model |
| **Closed** | Users sort cards into predefined categories | Validating existing IA; testing whether nav labels match expectations |
| **Hybrid** | Users sort into predefined categories; can create new ones | Evaluating existing IA while remaining open to gaps |

Default to open card sorting for new IA design. Use closed when you have a candidate structure and want to validate it before building.

### 2. Write the cards

Cards represent the content, features, or concepts users need to navigate to. Each card should be:
- One concept only — not a page title or a category label
- Written in user language, not product or technical language
- Distinct — no two cards should mean the same thing

```
✅ "Pay a bill"
✅ "Download my account history"
✅ "Change my password"
❌ "Account Management" — this is a category, not a concept
❌ "Billing" — too vague; could mean multiple things
```

**Card count:** 30–60 cards. Fewer than 30 produces insufficient data to identify patterns; more than 80 causes participant fatigue and noise in results.

Pilot the card list with 1–2 colleagues to catch ambiguous language before running real participants.

### 3. Recruit participants

- **Count:** 15–20 participants for quantitative pattern analysis; 5–8 if purely qualitative
- **Profile:** representative of actual users — same recruiting criteria as other research methods
- **Do not recruit** UX practitioners, designers, or people who have seen the current product IA — they will impose familiar structures rather than reveal mental models

### 4. Run the study

**Digital tools (recommended for scale):** OptimalSort, Maze, Condens, Dovetail
**Physical (recommended for depth):** index cards, a table, and a facilitator

**For each participant (open card sorting):**
1. Shuffle cards and present them in random order
2. Ask participant to group cards that belong together into piles
3. When grouping is complete, ask participant to label each pile with a name they would use
4. Optionally: ask "what would you call this section of a website?"

**Moderated session tips:**
- Do not suggest groupings or react to choices
- Ask "tell me why you put those together" after the sort completes — post-sort rationale reveals mental model logic
- If participant is stuck: "There's no right answer — put them wherever feels most natural"

### 5. Analyze results

**Similarity matrix:** for each pair of cards, how often did participants put them in the same group? High co-occurrence (>70%) = strong signal to group together; low co-occurrence (<30%) = users don't see a relationship.

**Dendrogram:** hierarchical clustering visualization showing which cards naturally cluster. Use OptimalSort's built-in dendrogram or export data to a clustering tool.

**Contested items:** cards with inconsistent placement across participants are navigation risk zones — users have fundamentally different mental models for these concepts. These items need either clearer labeling or additional research.

**Participant-generated labels:** review the names participants gave to groups — these are the nav labels users expect to see. Frequency of similar label types indicates preferred terminology.

### 6. Extract IA recommendations

Translate card sort findings into a draft IA:
- Items that clustered together → propose as a navigation section
- Participant-generated labels → propose as nav labels (use user language, not product language)
- Contested items → add to usability test task list to validate placement

Document findings as:
```
Finding: "Pay a bill", "View payment history", and "Set up autopay" were grouped together 
by 16 of 18 participants. Participants labeled this group "Payments" (12/18) or "Billing" (4/18).

Recommendation: Create a "Payments" section containing these three items. 
Use "Payments" as the nav label; avoid "Billing" which participants associated with 
receiving bills, not managing payment methods.
```

### 7. Validate the IA with tree testing

Card sorting reveals how users group concepts but not whether they can find items in your proposed IA. After building the IA from card sort data, run a tree test (also called reverse card sorting) to validate findability before development.

Tree testing tools: Treejack (Optimal Workshop), UXtweak Tree Testing.

## Rules

- Cards must use user language — product feature names and technical terms produce sorting patterns that reflect familiarity with terminology, not mental models
- Run card sorting before building navigation — retrofitting IA after development is expensive and rarely happens thoroughly
- Analyze the full similarity matrix, not just the top clusters — contested items (inconsistent placement) are as valuable as strong clusters
- Never use card sorting to validate internal team terminology ("do users understand our naming?") — use a comprehension test instead
- Report contested items explicitly; do not silently assign them to a group based on plurality — contested placement is a design risk that should be surfaced

## Common Mistakes

- **Using product/feature names as cards**: "Analytics Dashboard", "Campaign Manager" — these test familiarity with existing terminology, not users' mental models; rewrite as tasks or concepts
- **Too many cards**: 80+ cards produce fatigue; later placements are less thoughtful; cap at 60
- **Recruiting too few participants**: 5 participants produces a dendrogram that looks meaningful but has insufficient statistical power; 15–20 minimum for quantitative analysis
- **Ignoring contested items**: cards with inconsistent placement across participants represent real ambiguity; assigning them to a group by plurality hides a UX risk
- **Skipping tree testing**: card sorting reveals grouping preferences but not findability; validate the resulting IA before building it

## When NOT to Use

- When the IA already exists and is performing well by findability metrics — use tree testing or analytics to confirm, not card sorting
- When the product has fewer than 15 distinct content items — the sorting pattern won't provide enough signal to justify the study overhead
- When users are highly domain-specific (e.g., air traffic controllers, clinical specialists) — their mental models may be shaped by professional training that does not generalize; conduct contextual inquiry alongside card sorting to understand the domain model first