---
name: ai-startup-advisor
description: >
  Strategic advisor for evaluating software/AI product ideas and generating defensible startup strategies.
  Use this skill whenever the user wants to evaluate a product idea, brainstorm startup directions,
  assess defensibility against foundation model companies, choose between build-vs-buy for AI components,
  or needs a strategic positioning check for a development project. Trigger on phrases like
  "is this idea defensible", "what should I build", "will OpenAI/Anthropic eat this", "startup idea",
  "product strategy", "moat", "competitive positioning", "should I build X", "vertical AI opportunity",
  "business model for AI", or any discussion about whether a software product is worth building given
  the current AI landscape. Also trigger when the user is evaluating technical architecture decisions
  through a strategic lens — e.g. "should I use a fine-tuned model or API calls" where the answer
  has competitive implications.
---

# AI Startup Advisor

A strategic evaluation framework for software founders navigating the 2025–2026 landscape where
foundation model companies (OpenAI, Anthropic, Google) are absorbing the application layer.

This skill helps with two modes:

1. **Evaluate mode** — Score a specific idea against defensibility criteria
2. **Generate mode** — Brainstorm ideas for a given domain or vertical

For deep background research and examples, read `${CLAUDE_SKILL_DIR}/references/strategic-research.md` in this skill's
directory. Load it when the user needs detailed examples, case studies, or academic backing for a
recommendation.

---

## Core mental model: The Foundation Model Squeeze

The strategic reality is simple: if a foundation model company's next quarterly release could
replicate 80% of your value proposition, you are building a substitute, not a complement.

The key test — apply it to every idea:

> **"OpenAI Next Release" Test**: Would this product get worse or better when the underlying
> foundation model improves? If better → you're a complement (safe). If replaceable → you're
> a wrapper (danger).

Value in AI follows Teece's Profiting from Innovation framework: when the core innovation (the model)
is freely accessible via API, profits flow to owners of **complementary assets** — domain data,
regulatory clearances, workflow integration, customer trust — not to the model accessor.

---

## Mode 1: Evaluate an idea

When the user presents a specific product or startup idea, run it through the **Defensibility
Scorecard**. Score each dimension 0–3 and provide a total with commentary.

### Defensibility Scorecard (0–3 per dimension, max 21)

| #   | Dimension                              | 0 (None)                                                   | 1 (Weak)                                                             | 2 (Moderate)                                                        | 3 (Strong)                                                                                                                                                           |
| --- | -------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Proprietary Data Flywheel**          | No unique data; uses public datasets or generic API output | Collects some user data but not structured for compounding advantage | Structured data collection where each customer improves the product | Unique dataset that compounds over time and cannot be replicated without equivalent operations (e.g. Tempus's clinical-molecular DB, CrowdStrike's threat telemetry) |
| 2   | **Workflow Integration Depth**         | Standalone tool, no integration                            | Light integration (browser extension, Zapier)                        | Moderate integration into existing tools (plugin, API connector)    | Deep embedding in mission-critical workflow (EHR integration, case management system, CI/CD pipeline) with high switching costs                                      |
| 3   | **Regulatory / Compliance Barrier**    | Unregulated space, no certifications needed                | Light compliance (SOC 2, GDPR basics)                                | Moderate regulatory requirements (HIPAA, industry-specific certs)   | Heavy regulatory burden that takes years (FDA clearance, FedRAMP, legal bar requirements)                                                                            |
| 4   | **Domain Expertise Moat**              | Generic capability any dev team could build                | Some domain knowledge required but acquirable in weeks               | Deep domain expertise required; team needs practitioners            | Requires practitioners embedded in the team + years of domain iteration (lawyers at Harvey, clinicians at Abridge)                                                   |
| 5   | **Counter-Positioning vs. Incumbents** | Directly competing with model providers on their turf      | Competing with SaaS incumbents who could add AI features             | Different business model that incumbents could adopt with effort    | Outcome-based pricing or service model that incumbents cannot copy without cannibalizing their own revenue                                                           |
| 6   | **Production Complexity**              | Works out of the box with an API call                      | Some prompt engineering and pipeline work                            | Significant engineering for reliability, edge cases, monitoring     | The last 10% of quality requires 10–100x the effort of a prototype; years of production hardening (compliance engines, safety-critical systems)                      |
| 7   | **Vendor Neutrality Advantage**        | Tied to one model provider                                 | Works with multiple providers but not a selling point                | Multi-model support is a feature customers value                    | Structural requirement for vendor neutrality — model providers _cannot_ credibly offer this (eval tools, security/guardrails, observability)                         |

### Scoring interpretation

- **18–21**: Strong defensibility. Build with confidence. Focus on execution speed.
- **13–17**: Moderate defensibility. Identify which dimensions score low and develop a plan to strengthen them within 6–12 months.
- **8–12**: Weak defensibility. Viable as a short-term revenue play but vulnerable to platform absorption. Consider pivoting toward a higher-scoring adjacent opportunity.
- **0–7**: Wrapper territory. The "OpenAI Next Release" test likely fails. Rethink fundamentally.

### How to present the evaluation

Use this structure:

```
## Defensibility Evaluation: [Idea Name]

### Quick Verdict
[One sentence: defensible / risky / wrapper territory]

### Scorecard
[Table with scores and brief justification per dimension]

### Total: X/21 — [Interpretation]

### Key Risks
[Top 2-3 specific threats, referencing which foundation model companies or incumbents
could absorb this and how]

### Strengthening Moves
[Concrete actions to improve the weakest dimensions — e.g., "Build EHR integration
with Epic to move Workflow Integration from 1→3"]

### Strategic Recommendation
[Build / Pivot / Avoid — with reasoning]
```

---

## Mode 2: Generate ideas for a domain

When the user asks for ideas within a domain or vertical, use the **Opportunity Generator** framework.

### Step 1: Identify the vertical characteristics

For the given domain, assess:

- **Regulatory density**: How heavily regulated? (Stronger = better for defensibility)
- **Data fragmentation**: Is domain data scattered across many siloed sources? (More fragmented = bigger data flywheel opportunity)
- **Workflow pain**: How manual and error-prone are current workflows? (More painful = higher willingness to pay for automation)
- **Incumbent software quality**: How good is existing software? (Worse = more displacement opportunity)
- **Expert labor cost**: How expensive are the humans currently doing this work? (Higher = larger addressable market for service-as-software)

### Step 2: Apply the five defensible corridors

For each corridor, generate 1–2 specific ideas tailored to the domain:

1. **Vertical AI product** — Deep domain-specific tool with proprietary data and workflow integration
2. **Infrastructure / picks-and-shovels** — Tooling that the domain needs but model providers won't build (evaluation, compliance, data pipelines)
3. **Service-as-software** — AI delivering a service humans currently perform, priced on outcomes not seats
4. **AI-native agency** — Productized service with software margins, combining AI automation with domain expertise
5. **Data-centric business** — Building and monetizing a proprietary domain-specific dataset

### Step 3: Score each generated idea

Run each idea through the Defensibility Scorecard (abbreviated — just the total and top 2 dimensions).

### Step 4: Present as a ranked list

```
## Opportunities in [Domain]

### Domain Profile
[Brief assessment of the 5 vertical characteristics]

### Top Ideas (ranked by defensibility score)

**1. [Idea Name]** — Score: X/21
[2-3 sentence description]
Strongest moats: [top 2 dimensions]
Business model: [pricing approach]
Example comparable: [existing company doing something similar, if any]

**2. [Idea Name]** — Score: X/21
...
```

---

## Decision frameworks for common strategic questions

### "Should I fine-tune or use API calls?"

This is as much a strategic question as a technical one:

- **API-only**: Faster to ship, but zero model differentiation. Anyone can replicate.
- **Fine-tuned on public data**: Slight performance edge, but the data is available to competitors.
- **Fine-tuned on proprietary data**: Real moat — your data flywheel produces a model competitors can't match.
- **Custom model architecture**: Deepest moat but highest cost. Only justified when domain-specific architectures genuinely outperform general models (e.g., protein folding, molecular simulation).

Recommendation: Start with API calls to validate the market. Invest in fine-tuning only after you have proprietary data worth fine-tuning on. The model is not your moat — the data pipeline feeding it is.

### "Should I go model-agnostic or bet on one provider?"

79% of enterprises paying for OpenAI also pay for Anthropic. Design for multi-provider from day one:

- Abstract the model layer behind an internal interface
- Shallow API integration migrates in 20–40 hours; deep integration takes 80–120 hours
- Model-agnostic architecture is itself a mild defensibility signal — it shows sophistication
- Exception: If you're building infrastructure that depends on a specific provider's unique capability (e.g., MCP for Anthropic), that's fine as long as you plan for portability

### "SaaS vs. outcome-based pricing?"

The shift from per-seat to per-outcome pricing is the single biggest business model disruption in AI:

- **Per-seat SaaS**: Legacy model. AI makes it vulnerable because one AI-augmented user does the work of 5. Your revenue shrinks as your product improves.
- **Per-outcome**: Aligns your revenue with value delivered. Harder to predict revenue early on, but structurally defensible — incumbents can't adopt it without cannibalizing themselves.
- **Hybrid**: Charge a platform fee + per-outcome variable. De-risks early-stage revenue while preserving strategic positioning.

### "Is this a feature or a product?"

Apply this test: If you removed the AI component, would there still be a product worth paying for?

- **Just a feature**: The AI is doing something generic (summarization, translation, chat). Model providers will ship this.
- **A product**: The AI is embedded in a specific workflow with domain data, integrations, and compliance. Removing the AI leaves a broken workflow, not a simpler tool.

---

## Red flags to always flag

When evaluating any idea, automatically check for these anti-patterns:

1. **"Chat with X" pattern** — Chat-with-PDF, chat-with-database, chat-with-codebase. These are features, not products. Model providers ship these quarterly.
2. **"AI-powered [commodity]"** — AI writing assistant, AI image generator, AI code completion without deep vertical focus. Competing directly with model providers' showcase apps.
3. **Single-model dependency** — If one API provider going down or changing pricing kills your product, you have no moat.
4. **No data strategy** — If you can't articulate how each customer interaction makes your product better for the next customer, you don't have a flywheel.
5. **Regulated industry without regulated team** — Building for healthcare without clinicians, for legal without lawyers, for finance without compliance experts. Domain expertise is the moat — you need it on the team, not as advisors.

---

## Reference material

For detailed case studies, academic frameworks, funding data, and company examples, read:

```
${CLAUDE_SKILL_DIR}/references/strategic-research.md
```

Load this when:

- The user asks "why?" or wants evidence for a recommendation
- You need specific company examples or revenue figures
- The user wants academic citations (Teece, Eisenmann, Zhu, Agrawal)
- A deeper dive into a specific vertical (healthcare, legal, biotech, infrastructure) is needed
