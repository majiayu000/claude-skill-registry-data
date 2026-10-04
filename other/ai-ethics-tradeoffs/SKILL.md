---
name: ai-ethics-tradeoffs
description: "Framework for navigating AI safety, ethics, and capability trade-off discussions. Covers responsible scaling, content policy, bias, privacy, dual-use, and alignment."
argument-hint: "[ethical dilemma, safety question, or policy decision]"
---

# AI Ethics & Trade-offs Skill

Generate structured, nuanced analysis of AI safety, ethics, and capability trade-off questions — increasingly central to product decisions at AI companies.

## When to Use
- User asks about AI safety trade-offs
- User asks about content policy decisions
- User asks "How would you handle [ethical dilemma in AI]?"
- User says `/ai-ethics-tradeoffs` followed by a question
- Any question about responsible AI development, deployment, or governance
- Especially relevant for safety-focused AI companies

## Why This Matters

**At safety-focused labs**: Safety is core to the company's identity. Every PM must reason about safety-capability trade-offs fluently.

**At capability-focused labs**: Under increasing scrutiny for safety practices. PMs must articulate how to "move fast" responsibly.

**At research-first labs**: Deep commitment to responsible AI development. PMs bridge research safety work and product decisions.

These questions increasingly distinguish good product thinking from great at any frontier AI company.

## Framework: SAFE Method (5 Sections)

### Section 1: Scope the Dilemma
Before analyzing, clearly define:
- **The tension**: What two (or more) values are in conflict?
- **The stakeholders**: Who is affected? (users, society, the company, specific communities, future generations)
- **The timeframe**: Short-term vs. long-term implications
- **The reversibility**: Can this decision be undone if wrong?

Common tension patterns in AI:
- Safety vs. Capability (restricting model vs. making it more useful)
- Access vs. Control (open-source vs. closed, free vs. gated)
- Privacy vs. Personalization (user data vs. better experience)
- Speed vs. Caution (shipping fast vs. thorough safety testing)
- Transparency vs. Security (model details public vs. preventing misuse)

### Section 2: Analyze Perspectives
For each stakeholder, articulate their legitimate concerns:
- **Users**: What do they want? What risks do they face?
- **Society**: What are the broader implications?
- **Developers**: How does this affect those building on the platform?
- **Researchers**: What does the scientific community need?
- **Regulators**: What are the legal/compliance requirements?
- **The company**: What are the business and reputational stakes?

**Do NOT strawman any perspective.** The best answers demonstrate you can hold multiple valid viewpoints simultaneously.

### Section 3: Framework Application
Apply one or more ethical frameworks:

**Consequentialism**: What action produces the best outcome for the most people?
- Expected value calculation (probability of harm x severity)
- Short-term vs. long-term consequences
- Direct vs. indirect effects

**Deontological**: What are our obligations regardless of outcome?
- User rights (privacy, autonomy, informed consent)
- Company commitments (terms of service, safety pledges)
- Professional ethics (do no harm, transparency)

**Virtue Ethics**: What would a responsible AI company do?
- Intellectual honesty (acknowledge uncertainty)
- Precautionary principle (when in doubt, err on safety)
- Proportionality (response matches the risk level)

### Section 4: Evaluate Options
Present 3 approaches (spectrum from cautious to permissive):

**Option A: Conservative / Safety-First**
- What it looks like in practice
- What you gain (safety, trust, regulatory goodwill)
- What you lose (capability, user value, competitive position)

**Option B: Balanced / Nuanced**
- What it looks like in practice
- How it threads the needle
- What monitoring/adjustment mechanisms exist

**Option C: Permissive / Capability-First**
- What it looks like in practice
- What you gain (innovation, user value, market position)
- What you risk (harm, reputation, regulatory action)

### Section 5: Recommend & Monitor
- **Recommendation**: Pick an approach with clear reasoning
- **Implementation**: How to execute it in practice
- **Monitoring**: What signals would indicate it's working/failing
- **Escalation criteria**: When would you revisit the decision?
- **Communication**: How to explain this decision to different audiences

## Key AI Ethics Topics

### Content Policy & Moderation
- Where to draw the line on model outputs
- False positive refusals vs. harmful content getting through
- Cultural context and global deployment
- User expectations vs. safety requirements

### Responsible Scaling
- Responsible Scaling Policies (RSPs)
- Preparedness Frameworks for frontier model deployment
- Frontier AI safety approaches across major labs
- When to slow down or stop scaling
- Eval-gated deployment (capability thresholds that trigger safety reviews)

### Bias & Fairness
- Model bias in outputs (stereotyping, underrepresentation)
- Training data bias and mitigation
- Fairness across languages, cultures, and demographics
- The tension between "helpful" and "harmless"

### Privacy & Data
- Training on user data (opt-in vs. opt-out)
- Conversation privacy and data retention
- Enterprise data isolation guarantees
- Right to deletion and data portability

### Dual-Use Concerns
- Models that can help with both beneficial and harmful tasks
- Biosecurity, cybersecurity, and weaponization risks
- The "publish or perish" dilemma in AI research
- Information hazards and responsible disclosure

### Alignment & Control
- How to ensure AI systems do what we intend
- The principal-agent problem with AI assistants
- Sycophancy vs. honest disagreement
- When AI should refuse instructions

### Economic Impact
- Job displacement and workforce transition
- Concentration of AI power in a few companies
- Pricing and access (who gets to use AI?)
- Impact on creative professions

## Output Format
Write as a thoughtful, balanced analysis — not a sermon. Show you can reason about multiple perspectives without being paralyzed by them. Be opinionated but humble. Aim for ~2000 words.

## Research-First Workflow
1. **Research** — Search for recent incidents, policy decisions, research papers, and thought leader perspectives on the specific topic. Do 5-10 searches.
2. **Cite sources** — Include `[linked source](url)` inline, especially for specific policies and incidents.
3. **Display** the complete analysis.

## What Good Looks Like
- Identifies the core tension clearly (doesn't oversimplify)
- Articulates multiple perspectives genuinely (not strawmanning)
- Applies structured reasoning (not just gut feelings)
- Makes a recommendation with conviction AND humility
- Shows awareness of real-world examples and precedents
- Connects ethical reasoning to product decisions (not just philosophy)
- Demonstrates awareness of company-specific safety values and approaches
