---
name: chef-lifetime-ontology
description: Weighs ChefFlow plans, builds, audits, research, and product surfaces against the full chef day-to-day and lifetime business/personal ontology. Use when mapping work to CLO-40, checking cohesiveness, finding chef-world blind spots, evaluating queue items, or asking whether ChefFlow covers the whole chef reality.
user-invocable: true
---

# Chef Lifetime Ontology

Use this skill to reason against **CLO-40**, ChefFlow's canonical 40-category model of what chefs deal with across day-to-day work, business operations, personal life, and lifetime arc.

## Core Rule

Do not treat a feature, queue item, research finding, or product gap as coherent until it has been checked against the relevant CLO-40 categories and its blind spots are named.

This skill is for reasoning, audits, specs, and queue shaping. Do not implement code unless the user explicitly authorizes a queue fire or direct hotfix under the repo rules.

## CLO-40 Categories

1. Culinary Craft
2. Training and Skill Development
3. Cuisine Identity and Creative Style
4. Recipe Development
5. Menu Design
6. Ingredients and Sourcing
7. Dietary Needs, Allergies, and Nutrition
8. Food Safety and Sanitation
9. Kitchen Execution and Service Flow
10. Equipment, Tools, and Facilities
11. Quality Control and Feedback
12. Waste, Sustainability, and Ethics
13. Career Path and Professional Growth
14. Reputation, Brand, and Public Image
15. Sales, Leads, and Client Acquisition
16. Client Discovery and Relationship Memory
17. Client Communication
18. Proposals, Contracts, and Scope
19. Pricing, Profit, and Cost Control
20. Invoicing, Payments, and Bookkeeping
21. Taxes, Legal, Insurance, and Compliance
22. Licensing, Permits, and Regulation
23. Operations and Logistics
24. Scheduling and Time Management
25. Vendors, Partners, and Professional Network
26. Hiring, Training, Leadership, and Team Culture
27. Conflict, Complaints, Recovery, and Crisis Handling
28. Technology, Data, Automation, and AI
29. Marketing, Media, PR, and Social Platforms
30. Expansion, Products, Teaching, and New Revenue Streams
31. Business Ownership, Assets, Exit, and Succession
32. Personal Health, Injury, Sleep, and Aging
33. Mental Health, Burnout, Addiction Risk, and Recovery
34. Family, Relationships, Parenting, and Caregiving
35. Personal Finances, Housing, Debt, and Stability
36. Geography, Migration, Travel, and Relocation
37. Macroeconomic and Industry Forces
38. Workplace Power, Exploitation, Discrimination, and Safety
39. Personal Identity, Values, Faith, Sobriety, and Transformation
40. Legacy, Retirement, Death, and Exceptional Events

## When To Use

Use for:

- "Map this to CLO-40" or "weigh this against the chef ontology."
- Build queue shaping, PRDs, specs, research-to-build work, and product gap mining.
- Cohesion checks before or after building a ChefFlow surface.
- Auditing whether a feature only handles operational workflow while ignoring personal, financial, legal, relationship, health, or lifetime realities.
- Comparing two possible product directions by chef-world coverage and depth.

## Reasoning Workflow

1. Name the artifact being checked: feature, route, workflow, queue item, insight, research finding, or product strategy.
2. Identify the primary CLO-40 categories it directly serves.
3. Identify secondary categories it touches indirectly or creates obligations for.
4. Name missing categories that would make the work feel incoherent, shallow, or disconnected from a chef's real life.
5. Separate day-to-day coverage from lifetime coverage.
6. State the minimum integration needed for ChefFlow coherence: data, UI affordance, reminder, automation, memory, privacy rule, lifecycle state, or queue item.
7. Recommend one of: keep narrow, deepen now, queue follow-up, reject as noise, or require research.

## Output Format

Use this structure:

```md
## CLO-40 Check

Artifact:
Verdict: coherent | partial | shallow | risky | not worth building

Primary categories:

- #{n} {Category}: {why it matters}

Secondary categories:

- #{n} {Category}: {implication}

Blind spots:

- #{n} {Category}: {what is missing or under-modeled}

Day-to-day coverage:
Lifetime coverage:

Cohesion move:
Recommendation:
```

## Quality Bar

A good CLO-40 pass does not list all 40 categories by default. It selects the categories that matter, explains why, and names the hidden chef realities that would otherwise be missed.
