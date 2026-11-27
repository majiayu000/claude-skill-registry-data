---
name: ai-product-strategy
description: "Produces an Artificial Intelligence (AI) product strategy: a scored map of AI opportunities, a build-buy-partner recommendation per opportunity, a data moat assessment, trust and user experience requirements, a phased roadmap, and a risk register. Use when evaluating where AI could add value to a product; deciding whether to build, buy, or partner for an AI capability; assessing whether proprietary data creates a defensible advantage; planning an AI feature roadmap; or evaluating AI vendors and partners."
---

# AI Product Strategy

> Find the AI opportunities worth pursuing, and the ones that will still be defensible in two years.

## What this skill is

A structured workflow for deciding where Artificial Intelligence (AI) belongs in a product and how to deliver it. It moves from opportunity discovery through build-buy-partner analysis, data moat assessment, and trust design to a phased roadmap with explicit risks. It draws on Marty Cagan's four product risks (value, usability, feasibility, viability), Andrew Ng's AI Transformation Playbook, Benedict Evans's writing on AI moats, and Julie Zhuo's approach to product strategy.

## What it solves

- AI features chosen because competitors announced them, not because they solve a user problem
- Build decisions made without comparing the cost and speed of buying or partnering
- Strategies that assume a data advantage without testing whether the data is proprietary or replicable
- AI features that fail user trust because errors, confidence, and control were never designed
- Roadmaps that jump to differentiation before a minimum viable version has proven value
- Risk reviews that cover model accuracy but ignore viability, cost, and regulatory exposure

## When to invoke

- Leadership asks "what is our AI strategy?" and the team needs a structured answer
- A team is deciding whether to build an AI capability in-house, buy a vendor solution, or partner
- A product manager needs to judge whether the company's data creates a lasting advantage
- Planning the next two to four quarters of AI features
- Evaluating AI vendors or model providers for a specific use case

## Phase 1: Product and market baseline

Capture the context the strategy depends on. Ask for anything missing.

| Input | Why it matters |
|-------|----------------|
| Product, users, and core jobs | AI must serve an existing job, not invent one |
| Current pain points and workarounds | The best opportunities sit where users spend effort today |
| Data assets | What data the product generates, owns, and can legally use |
| Competitive AI moves | What is becoming table stakes versus differentiating |
| Team capability | Machine learning (ML), data engineering, and evaluation skills in house |
| Constraints | Budget, latency, privacy, regulatory, and brand risk tolerance |

## Phase 2: Identify AI opportunity areas

Generate candidates across six categories, then score each.

| Category | Typical pattern |
|----------|-----------------|
| Automation | Remove repetitive manual steps |
| Prediction | Forecast an outcome the user currently guesses |
| Personalization | Tailor content, ranking, or defaults per user |
| Content generation | Draft text, images, code, or summaries |
| Data analysis | Surface patterns users cannot see manually |
| Decision support | Recommend an action with reasoning |

Score each opportunity 1-5 on user value, frequency of the job, data availability, technical feasibility, and tolerance for error. Shortlist the top three to five.

## Phase 3: Build, buy, or partner

For each shortlisted opportunity:

| Factor | Favors build | Favors buy | Favors partner |
|--------|--------------|------------|----------------|
| Strategic differentiation | Core to the product's advantage | Commodity capability | Adjacent capability |
| Proprietary data | Unique and essential | Not required | Partner holds it |
| Time to market | Can wait | Needed now | Needed soon |
| In-house capability | Strong | Weak | Mixed |
| Total cost over 3 years | Lower at scale | Lower at low volume | Shared |
| Control and lock-in risk | Full control | Vendor dependency | Contractual dependency |

Record the recommendation and the condition that would flip it.

## Phase 4: Data moat assessment

Test whether the data advantage is real.

| Question | Strong moat | Weak moat |
|----------|-------------|-----------|
| Is the data proprietary? | Generated only by our product | Publicly available or purchasable |
| Is there a flywheel? | Usage improves the model, which drives more usage | Model quality is static |
| How replicable is it? | Years of accumulated, labeled data | A competitor could gather it in months |
| Time to defensibility | Advantage compounds within 12-24 months | No clear compounding |

Rate the moat as strong, moderate, or weak and say what would strengthen it.

## Phase 5: User experience and trust design

Specify how each AI feature earns and keeps trust:
- **Transparency** - show why the system produced a result and how confident it is
- **User control** - let users edit, override, undo, or opt out
- **Graceful failure** - define what happens when the model is wrong or unavailable
- **Progressive disclosure** - start with assistive suggestions before autonomous actions
- **Trust building** - expand autonomy only as measured accuracy and user acceptance rise

## Phase 6: Implementation roadmap

| Stage | Goal | Exit criteria |
|-------|------|---------------|
| Stage 1: Minimum Viable Product (MVP) | Prove user value for one opportunity | Adoption and quality targets met |
| Stage 2: Expansion | Extend to adjacent workflows and segments | Unit cost and reliability within targets |
| Stage 3: Differentiation | Build the data flywheel and proprietary capability | Measurable gap versus alternatives |

## Phase 7: Risk and mitigation planning

Assess each opportunity against Cagan's four risks plus AI-specific exposure.

| Risk | Question | Mitigation example |
|------|----------|--------------------|
| Value | Will users choose to use it? | Prototype test before build |
| Usability | Can users understand and control it? | Trust patterns from Phase 5 |
| Feasibility | Can we reach the needed quality and latency? | Offline evaluation set and quality bar |
| Viability | Does it work for the business, including inference cost? | Cost per action model and pricing review |
| Responsible AI | Bias, privacy, safety, or regulatory exposure | Review gate and monitoring |

## Output

- Product and market baseline
- Scored AI opportunity map with a shortlist
- Build, buy, or partner recommendation per shortlisted opportunity, with flip conditions
- Data moat rating and strengthening actions
- Trust and user experience requirements per feature
- Three-stage roadmap with exit criteria
- Risk register with mitigations and owners

## Operating rules

**Always**
- Start from a user job and pain point, not from a model capability
- Compare build, buy, and partner explicitly for every shortlisted opportunity
- Test the data moat against replicability, not just volume
- Design failure modes and user control before launch
- Include inference cost in the viability assessment

**Never**
- Recommend an AI feature because a competitor shipped one
- Claim a data moat without evidence that the data is proprietary
- Skip the minimum viable stage and jump straight to differentiation
- Give an AI feature autonomy before its accuracy is measured
- Treat responsible AI review as optional
