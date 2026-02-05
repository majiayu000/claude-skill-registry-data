---
name: marketing-experimentation
description: Systematic marketing experimentation process - discover concepts, generate hypotheses, coordinate multiple experiments, synthesize results, generate next-iteration ideas through rigorous validation cycles
---

# Marketing Experimentation

## Overview

Use this skill when you need to validate marketing concepts or business ideas through rigorous experimental cycles. This skill orchestrates the complete Build-Measure-Learn cycle from concept to data-driven signal.

**When to use this skill:**
- You have a marketing concept or business idea that needs validation
- You want to test multiple related hypotheses systematically
- You need to integrate results across multiple experiments
- You're designing the next iteration based on experimental evidence
- You're conducting qualitative market research combined with quantitative testing

**What this skill does:**
- Validates concepts through market research before experimentation
- Generates multiple testable hypotheses from marketing ideas
- Coordinates multiple experiments: quantitative (hypothesis-testing) and qualitative (qualitative-research)
- Synthesizes results across experiments using interpreting-results and creating-visualizations
- Produces clear signals (positive/negative/null/mixed) for each campaign
- Generates actionable next-iteration ideas based on experimental evidence

**What this skill does NOT do:**
- Design individual experiments (delegates to hypothesis-testing or qualitative-research)
- Execute statistical analysis directly (uses hypothesis-testing for quantitative rigor)
- Conduct interviews/surveys/observations directly (uses qualitative-research for qualitative rigor)
- Operationalize successful ideas (focuses on validation, not scaling)
- Platform-specific implementation (tool-agnostic techniques only)

**Integration with existing skills:**
- **Delegates to `hypothesis-testing`** for quantitative experiment design and execution (metrics, A/B tests, statistical analysis)
- **Delegates to `qualitative-research`** for qualitative experiment design and execution (interviews, surveys, focus groups, observations)
- **Uses `interpreting-results`** to synthesize findings across multiple experiments
- **Uses `creating-visualizations`** to communicate aggregate results
- **Invokes `market-researcher` agent** for concept validation via internet research

**Multi-conversation persistence:**
This skill is designed for campaigns spanning days or weeks. Each phase documents completely enough that new conversations can resume after extended breaks. The experiment tracker (04-experiment-tracker.md) serves as the living coordination hub.

## Prerequisites

**Required skills:**
- `hypothesis-testing` - Quantitative experiment design and execution (invoked for metric-based experiments)
- `qualitative-research` - Qualitative experiment design and execution (invoked for interviews, surveys, focus groups, observations)
- `interpreting-results` - Result synthesis and pattern identification (invoked in Phase 5)
- `creating-visualizations` - Aggregate result visualization (invoked in Phase 5)

**Required agents:**
- `market-researcher` - Concept validation via internet research (invoked in Phase 1)

**Required knowledge:**
- Understanding of Lean Startup Build-Measure-Learn cycle
- Familiarity with marketing tactics (landing pages, ads, email, content)
- Basic experimental design principles (control/treatment, signals, metrics)
- Understanding of qualitative vs quantitative research methods

**Data requirements:**
- None initially (market research is qualitative)
- Data requirements emerge from experiment design in Phase 4
- Quantitative experiments (hypothesis-testing): SQL databases, analytics data, A/B test results
- Qualitative experiments (qualitative-research): Interview transcripts, survey responses, observation notes

## Mandatory Process Structure

**CRITICAL:** This is a 6-phase process skill. You MUST complete all phases in order. Use TodoWrite to track progress through each phase.

**TodoWrite template:**

When starting a marketing-experimentation session, create these todos:

```markdown
- [ ] Phase 1: Discovery & Asset Inventory
- [ ] Phase 2: Hypothesis Generation
- [ ] Phase 3: Prioritization
- [ ] Phase 4: Experiment Coordination
- [ ] Phase 5: Cross-Experiment Synthesis
- [ ] Phase 6: Iteration Planning
```

**Workspace structure:**

All work for a marketing-experimentation session is saved to:
```
analysis/marketing-experimentation/[campaign-name]/
├── 01-discovery.md
├── 02-hypothesis-generation.md
├── 03-prioritization.md
├── 04-experiment-tracker.md
├── 05-synthesis.md
├── 06-iteration-plan.md
└── experiments/
    ├── [experiment-1]/               # hypothesis-testing session
    ├── [experiment-2]/               # hypothesis-testing session
    └── [experiment-3]/               # hypothesis-testing session
```

**Phase progression rules:**
1. Each phase has a CHECKPOINT with verification requirements
2. You MUST satisfy all checkpoint requirements before proceeding to the next phase
3. Document every decision with rationale in the numbered markdown files
4. Commit markdown files after each phase completes
5. The experiment tracker (04-experiment-tracker.md) is a LIVING DOCUMENT - update it throughout Phase 4

**Multi-conversation resumption:**
- At the start of any conversation, check if an experiment tracker exists for this campaign
- If it exists, read it first to understand current experiment status
- Update the tracker as experiments progress
- All phases should be complete enough to resume after days or weeks

---

## Phase 1: Discovery & Asset Inventory

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Gathered business concept description from user
- [ ] Invoked market-researcher agent and documented findings
- [ ] Completed asset inventory (content, campaigns, audiences, data)
- [ ] Defined success criteria and validation signals
- [ ] Documented known constraints
- [ ] Saved to `01-discovery.md`

### Instructions

1. **Gather the business concept**
   - Ask user to describe the marketing concept or business idea to validate
   - What problem does it solve? Who is the target audience?
   - What's the desired outcome? (awareness, leads, conversions, etc.)
   - What stage is this idea at? (new concept, existing campaign, iteration)

2. **Invoke market-researcher agent for concept validation**

   Dispatch the `market-researcher` agent with the concept description:
   - Agent will research market demand signals
   - Agent will identify similar solutions and competitors
   - Agent will analyze audience needs and pain points
   - Agent will find validation evidence (case studies, reviews, testimonials)

   Document agent findings in `01-discovery.md` under "Market Research Findings"

3. **Conduct asset inventory**

   Work with user to inventory existing assets that could be leveraged:

   **Content Assets:**
   - Blog posts, case studies, whitepapers
   - Video content, webinars, tutorials
   - Social media presence and following
   - Email lists and subscriber segments

   **Campaign Assets:**
   - Existing ad campaigns and performance data
   - Landing pages and conversion rates
   - Email campaigns and open/click rates
   - SEO performance and keyword rankings

   **Audience Assets:**
   - Customer segments and personas
   - Audience data (demographics, behaviors, preferences)
   - Customer feedback and reviews
   - Support tickets and common questions

   **Data Assets:**
   - Analytics platforms (Google Analytics, Mixpanel, etc.)
   - CRM data (Salesforce, HubSpot, etc.)
   - Ad platform data (Google Ads, Facebook Ads, etc.)
   - Email platform data (Mailchimp, SendGrid, etc.)

4. **Define success criteria and validation signals**

   Work with user to define:
   - What metrics indicate success? (CTR, conversion rate, CAC, LTV, etc.)
   - What magnitude of change is meaningful? (practical significance thresholds)
   - What signal types are acceptable?
     - Positive: Validates concept, proceed to scale
     - Negative: Invalidates concept, pivot or abandon
     - Null: Inconclusive, needs refinement or more data
     - Mixed: Some aspects work, some don't, iterate strategically

5. **Document known constraints**

   Capture any constraints that will affect experimentation:
   - Budget constraints (ad spend limits, tool costs)
   - Time constraints (launch deadlines, seasonal factors)
   - Resource constraints (team capacity, content production)
   - Technical constraints (platform limitations, integration issues)
   - Regulatory constraints (GDPR, CCPA, industry regulations)

6. **Create `01-discovery.md`** with: `./templates/01-discovery.md`

7. **STOP and get user confirmation**
   - Review discovery findings with user
   - Confirm asset inventory is complete
   - Confirm success criteria are appropriate
   - Do NOT proceed to Phase 2 until confirmed

**Common Rationalization:** "I'll skip discovery and go straight to testing - the concept is obvious"
**Reality:** Discovery surfaces assumptions, constraints, and existing assets that dramatically affect experiment design. Always start with discovery.

**Common Rationalization:** "I don't need market research - I already know this market"
**Reality:** The market-researcher agent provides current, data-driven validation signals that prevent building experiments around false assumptions. Always validate.

**Common Rationalization:** "Asset inventory is busywork - I'll figure out what's available as I go"
**Reality:** Existing assets can dramatically reduce experiment cost and time. Inventorying first prevents reinventing wheels and enables building on proven foundations.

---

## Phase 2: Hypothesis Generation

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Generated 5-10 testable hypotheses from the concept
- [ ] Each hypothesis maps to a specific tactic/channel
- [ ] Each hypothesis has expected outcome and rationale
- [ ] Hypotheses cover multiple tactics (not all ads or all email)
- [ ] Referenced relevant frameworks (Lean Startup, AARRR, ICE/RICE)
- [ ] Saved to `02-hypothesis-generation.md`

### Instructions

1. **Generate 5-10 testable hypotheses**

   For each hypothesis, use this format:

   **Hypothesis [N]: [Brief statement]**
   - **Tactic/Channel:** [landing page | ad campaign | email sequence | content marketing | social media | SEO | etc.]
   - **Expected Outcome:** [Specific, measurable result]
   - **Rationale:** [Why we believe this will work based on discovery findings]
   - **Variables to Test:** [What will we manipulate/measure]

   **Example hypothesis:**

   **Hypothesis 1: Value proposition clarity drives conversion**
   - **Tactic/Channel:** Landing page A/B test
   - **Expected Outcome:** 15%+ increase in conversion rate from landing page variant with simplified value proposition
   - **Rationale:** Market research showed audience confusion about product benefits. Discovery found existing landing page has 8 different value propositions competing for attention.
   - **Variables to Test:** Headline clarity, benefit hierarchy, CTA prominence

2. **Ensure tactic coverage**

   Verify hypotheses cover multiple marketing tactics:

   **Acquisition Tactics:**
   - Landing pages (conversion optimization, value prop testing, layout)
   - Ad campaigns (targeting, creative, messaging, platforms)
   - Content marketing (blog posts, videos, webinars, lead magnets)
   - SEO (keyword targeting, content optimization, technical SEO)

   **Activation Tactics:**
   - Email sequences (onboarding, nurture, activation)
   - Product tours (in-app guidance, feature discovery)
   - Social proof (testimonials, case studies, reviews)

   **Retention Tactics:**
   - Email campaigns (engagement, re-activation, upsell)
   - Content (newsletters, educational content, community)

   Don't generate 10 ad hypotheses. Aim for diversity across tactics.

3. **Reference experimentation frameworks**

   **Lean Startup Build-Measure-Learn:**
   - Build: What's the minimum viable test? (landing page, ad, email, etc.)
   - Measure: What metrics indicate success/failure?
   - Learn: What will we learn regardless of outcome?

   **AARRR Pirate Metrics:**
   - Acquisition: How do users find us?
   - Activation: Do they have a great first experience?
   - Retention: Do they come back?
   - Referral: Do they tell others?
   - Revenue: Do they pay?

   Map each hypothesis to one or more AARRR stages.

   **ICE/RICE Prioritization (used in Phase 3):**
   - Impact: How much will this move the metric?
   - Confidence: How sure are we this will work?
   - Ease: How easy is this to implement?
   - Reach: How many users will this affect? (RICE only)

4. **Create `02-hypothesis-generation.md`** with: `./templates/02-hypothesis-generation.md`

5. **STOP and get user confirmation**
   - Review all hypotheses with user
   - Confirm hypotheses are testable and meaningful
   - Confirm tactic coverage is appropriate
   - Do NOT proceed to Phase 3 until confirmed

**Common Rationalization:** "I'll generate hypotheses as I build experiments - more efficient"
**Reality:** Generating hypotheses before prioritization enables strategic selection of highest-impact tests. Generating ad-hoc leads to testing whatever's easiest, not what matters most.

**Common Rationalization:** "I'll focus all hypotheses on one tactic (ads) since that's what we know"
**Reality:** Tactic diversity reveals which channels work for this concept. Single-tactic testing creates blind spots and missed opportunities.

**Common Rationalization:** "I'll write vague hypotheses and refine them during experiment design"
**Reality:** Vague hypotheses lead to vague experiments that produce vague results. Specific hypotheses with expected outcomes enable clear signal detection.

**Common Rationalization:** "More hypotheses = better coverage, I'll generate 20+"
**Reality:** Too many hypotheses dilute focus and create analysis paralysis in prioritization. 5-10 high-quality hypotheses enable strategic selection of 2-4 tests.

---

## Phase 3: Prioritization

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Scored all hypotheses using ICE or RICE framework with computational method
- [ ] Created prioritized backlog (highest to lowest score) using Python script
- [ ] Selected 2-4 highest-priority hypotheses for testing
- [ ] Documented prioritization rationale
- [ ] Identified any dependencies or sequencing requirements
- [ ] Saved to `03-prioritization.md`

### Instructions

**CRITICAL:** You MUST use computational methods (Python scripts) to calculate scores. Do NOT estimate or manually calculate scores.

1. **Choose prioritization framework**

   **ICE Framework** (simpler, faster):
   - **Impact:** How much will this move the success metric? (1-10 scale)
   - **Confidence:** How confident are we this will work? (1-10 scale)
   - **Ease:** How easy is this to implement? (1-10 scale)
   - **Score:** (Impact × Confidence) / Ease

   **RICE Framework** (more comprehensive):
   - **Reach:** How many users will this affect? (absolute number or percentage)
   - **Impact:** How much will this move the metric per user? (1-10 scale: 0.25=minimal, 3=massive)
   - **Confidence:** How confident are we in our estimates? (percentage: 50%, 80%, 100%)
   - **Effort:** Person-weeks to implement (absolute number)
   - **Score:** (Reach × Impact × Confidence) / Effort

   Choose ICE for speed, RICE for precision when reach varies significantly.

2. **Score each hypothesis using Python script**

   **For ICE Framework:**

   Create a Python script to compute and sort ICE scores:

   ```python
   #!/usr/bin/env python3
   """
   ICE Score Calculator for Marketing Experimentation

   Computes ICE scores: (Impact × Confidence) / Ease
   Sorts hypotheses by score (highest to lowest)
   """

   hypotheses = [
       {
           "id": "H1",
           "name": "Value proposition clarity drives conversion",
           "impact": 8,
           "confidence": 7,
           "ease": 9
       },
       {
           "id": "H2",
           "name": "Ad targeting refinement",
           "impact": 7,
           "confidence": 6,
           "ease": 5
       },
       {
           "id": "H3",
           "name": "Email sequence optimization",
           "impact": 6,
           "confidence": 8,
           "ease": 8
       },
       {
           "id": "H4",
           "name": "Content marketing expansion",
           "impact": 5,
           "confidence": 4,
           "ease": 3
       },
   ]

   # Calculate ICE scores
   for h in hypotheses:
       h['ice_score'] = (h['impact'] * h['confidence']) / h['ease']

   # Sort by ICE score (descending)
   sorted_hypotheses = sorted(hypotheses, key=lambda x: x['ice_score'], reverse=True)

   # Print results table
   print("| Hypothesis | Impact | Confidence | Ease | ICE Score | Rank |")
   print("|------------|--------|------------|------|-----------|------|")
   for rank, h in enumerate(sorted_hypotheses, 1):
       print(f"| {h['id']}: {h['name'][:30]} | {h['impact']} | {h['confidence']} | {h['ease']} | {h['ice_score']:.2f} | {rank} |")
   ```

   **Usage:**
   ```bash
   python3 ice_calculator.py
   ```

   **For RICE Framework:**

   Create a Python script to compute and sort RICE scores:

   ```python
   #!/usr/bin/env python3
   """
   RICE Score Calculator for Marketing Experimentation

   Computes RICE scores: (Reach × Impact × Confidence) / Effort
   Sorts hypotheses by score (highest to lowest)
   """

   hypotheses = [
       {
           "id": "H1",
           "name": "Value proposition clarity drives conversion",
           "reach": 10000,        # users affected
           "impact": 3,           # 0.25=minimal, 1=low, 2=medium, 3=high, 5=massive
           "confidence": 80,      # percentage (50, 80, 100)
           "effort": 2            # person-weeks
       },
       {
           "id": "H2",
           "name": "Ad targeting refinement",
           "reach": 50000,
           "impact": 1,
           "confidence": 50,
           "effort": 4
       },
       {
           "id": "H3",
           "name": "Email sequence optimization",
           "reach": 5000,
           "impact": 2,
           "confidence": 80,
           "effort": 3
       },
       {
           "id": "H4",
           "name": "Content marketing expansion",
           "reach": 20000,
           "impact": 1,
           "confidence": 50,
           "effort": 8
       },
   ]

   # Calculate RICE scores
   for h in hypotheses:
       # Convert confidence percentage to decimal
       confidence_decimal = h['confidence'] / 100
       h['rice_score'] = (h['reach'] * h['impact'] * confidence_decimal) / h['effort']

   # Sort by RICE score (descending)
   sorted_hypotheses = sorted(hypotheses, key=lambda x: x['rice_score'], reverse=True)

   # Print results table
   print("| Hypothesis | Reach | Impact | Confidence | Effort | RICE Score | Rank |")
   print("|------------|-------|--------|------------|--------|------------|------|")
   for rank, h in enumerate(sorted_hypotheses, 1):
       print(f"| {h['id']}: {h['name'][:30]} | {h['reach']} | {h['impact']} | {h['confidence']}% | {h['effort']}w | {h['rice_score']:.2f} | {rank} |")
   ```

   **Usage:**
   ```bash
   python3 rice_calculator.py
   ```

   **Scoring Guidance:**

   **Impact (1-10 for ICE, 0.25-5 for RICE):**
   - ICE: 1-3 minimal, 4-6 moderate, 7-8 significant, 9-10 transformative
   - RICE: 0.25 minimal, 1 low, 2 medium, 3 high, 5 massive

   **Confidence (1-10 for ICE, 50-100% for RICE):**
   - ICE: 1-3 speculative, 4-6 uncertain, 7-8 likely, 9-10 validated
   - RICE: 50% low confidence, 80% high confidence, 100% certainty

   **Ease (1-10 for ICE):**
   - 1-3: Complex, significant resources
   - 4-6: Moderate effort, some obstacles
   - 7-8: Straightforward, few dependencies
   - 9-10: Trivial, immediate execution

   **Effort (person-weeks for RICE):**
   - Estimate total person-weeks required
   - Include design, implementation, monitoring time
   - Examples: 1w (simple landing page), 4w (complex ad campaign), 8w (content series)

3. **Run scoring script and document results**

   1. Create the Python script (ice_calculator.py or rice_calculator.py)
   2. Update the `hypotheses` list with actual hypothesis data from Phase 2
   3. Run the script: `python3 [ice|rice]_calculator.py`
   4. Copy the output table into `03-prioritization.md`
   5. Include the script in the markdown file for reproducibility:

   ```markdown
   ## Prioritization Calculation

   **Method:** ICE Framework

   **Calculation Script:**
   ```python
   [paste full script here]
   ```

   **Results:**

   [paste output table here]
   ```

4. **Select 2-4 highest-priority hypotheses**

   Considerations for selection:
   - **Don't test everything:** Focus on highest-scoring 2-4 hypotheses
   - **Resource constraints:** Match selection to available time/budget/capacity
   - **Learning value:** Sometimes lower-scoring hypothesis with high uncertainty is worth testing
   - **Dependencies:** Test prerequisites before dependent hypotheses
   - **Sequencing:** Consider whether experiments need to run sequentially or can run in parallel

   **Selection criteria:**
   - Primary: Top 2-4 by ICE/RICE score from computational results
   - Secondary: Balance quick wins vs. high-impact long-term bets
   - Tertiary: Ensure tactic diversity (don't test 3 ad variants if other tactics untested)

5. **Document experiment sequence**

   Determine execution strategy:
   - **Parallel:** Multiple experiments running simultaneously (faster results, higher resource needs)
   - **Sequential:** One experiment at a time (slower, easier to manage)
   - **Hybrid:** Run independent experiments in parallel, sequence dependent ones

   **Example sequence plan:**
   ```
   Week 1-2: Launch H1 (landing page) and H3 (email) in parallel
   Week 3-4: Analyze H1 and H3 results
   Week 5-6: Launch H2 (ads) based on H1 learnings
   Week 7-8: Analyze H2 results
   ```

6. **Create `03-prioritization.md`** with: `./templates/03-prioritization.md`

7. **STOP and get user confirmation**
   - Review computed scores and prioritization with user
   - Confirm selected hypotheses are appropriate
   - Confirm experiment sequence is feasible
   - Do NOT proceed to Phase 4 until confirmed

**Common Rationalization:** "I'll test all hypotheses - don't want to miss opportunities"
**Reality:** Resource constraints make testing everything impossible. Prioritization ensures highest-value experiments get resources. Unfocused testing produces weak signals across too many fronts.

**Common Rationalization:** "Scoring is subjective and arbitrary - I'll just pick what feels right"
**Reality:** Scoring frameworks force explicit reasoning about trade-offs. "Feels right" selections optimize for recency bias and personal preference, not business value. Computational methods ensure consistency.

**Common Rationalization:** "I'll skip prioritization and go straight to easiest test"
**Reality:** Easiest test rarely equals highest value. Prioritization prevents optimizing for ease at the expense of impact.

**Common Rationalization:** "I'll estimate scores mentally instead of running the script"
**Reality:** Manual estimation introduces calculation errors and inconsistency. Python scripts ensure exact, reproducible results that can be audited and verified.

---

## Phase 4: Experiment Coordination

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Created experiment tracker with all selected hypotheses
- [ ] Determined experiment type for each hypothesis (Quantitative or Qualitative)
- [ ] Invoked appropriate skill for each hypothesis (hypothesis-testing OR qualitative-research)
- [ ] Updated tracker with experiment status (Planned, In Progress, Complete)
- [ ] Documented location of each experiment session
- [ ] Saved experiment tracker to `04-experiment-tracker.md`
- [ ] Note: This phase may span multiple days/weeks and conversations

### Instructions

**CRITICAL:** This phase is designed for multi-conversation workflows. The experiment tracker is a LIVING DOCUMENT that you will update throughout experimentation. New conversations should ALWAYS read this file first.

1. **Determine experiment type for each hypothesis**

   **CRITICAL:** Before creating the tracker, classify each hypothesis as Quantitative or Qualitative.

   **Quantitative experiments** use hypothesis-testing skill:
   - Measure **numeric metrics**: CTR, conversion rate, bounce rate, time on page, revenue, CAC, LTV, etc.
   - Rely on **existing data sources**: Google Analytics, ad platforms, CRM, email platforms, database queries
   - Test using **A/B tests, multivariate tests, or time-series analysis**
   - Require **statistical significance testing**
   - **Examples:**
     - Landing page A/B test measuring conversion rate
     - Ad campaign comparing CTR across different creatives
     - Email sequence measuring open rate and click-through rate
     - SEO experiment tracking organic traffic changes

   **Qualitative experiments** use qualitative-research skill:
   - Gather **non-numeric insights**: opinions, experiences, needs, pain points, motivations
   - Collect through **interviews, surveys, focus groups, or observations**
   - Analyze using **thematic analysis** rather than statistical tests
   - Focus on **understanding why** behaviors occur
   - **Examples:**
     - Customer discovery interviews to understand pain points
     - Open-ended survey asking about product needs
     - Focus group discussing ad creative perceptions
     - Observational study of how users interact with product

   **Decision criteria:**

   Ask: "What do we need to learn?"
   - If answer is "Does X increase metric Y by Z%?" → **Quantitative** (hypothesis-testing)
   - If answer is "Why do users do X?" or "What do users think about Y?" → **Qualitative** (qualitative-research)

   Ask: "What data will we collect?"
   - If answer is "Metrics from analytics" → **Quantitative** (hypothesis-testing)
   - If answer is "Interview transcripts, survey responses, or observation notes" → **Qualitative** (qualitative-research)

   **Mixed methods:**
   - Some hypotheses may require BOTH quantitative and qualitative experiments
   - Example: "Value prop clarity drives conversion" could test:
     - Quantitatively: A/B test landing page, measure conversion rate (hypothesis-testing)
     - Qualitatively: Interview users about which value prop resonates (qualitative-research)
   - Track these as separate experiments with linked hypotheses in the tracker

2. **Create experiment tracker**

   The tracker is your coordination hub for managing multiple experiments over time.

   Create `04-experiment-tracker.md` with: `./templates/04-experiment-tracker.md`

   **Tracker format:**

   For each selected hypothesis, create an entry:

   ```markdown
   ### Experiment 1: [Hypothesis Brief Name]

   **Status:** [Planned | In Progress | Complete]
   **Hypothesis:** [Full hypothesis statement from Phase 2]
   **Tactic/Channel:** [landing page | ads | email | etc.]
   **Priority Score:** [ICE/RICE score from Phase 3]
   **Start Date:** [YYYY-MM-DD or "Not started"]
   **Completion Date:** [YYYY-MM-DD or "In progress"]
   **Location:** `analysis/marketing-experimentation/[campaign-name]/experiments/[experiment-name]/`
   **Signal:** [Positive | Negative | Null | Mixed | "Not analyzed"]
   **Key Findings:** [Brief summary when complete, "TBD" otherwise]
   ```

2. **Invoke appropriate skill for each experiment**

   For each hypothesis marked "Planned" or "In Progress":

   **Step 1:** Read the hypothesis details from `02-hypothesis-generation.md`

   **Step 2a:** If **Quantitative experiment**, invoke `hypothesis-testing` skill:
   ```markdown
   Use hypothesis-testing skill to test: [Hypothesis statement]

   Context for hypothesis-testing:
   - Session name: [descriptive-name-for-experiment]
   - Save location: analysis/marketing-experimentation/[campaign-name]/experiments/[experiment-name]/
   - Success criteria: [From Phase 1 discovery]
   - Expected outcome: [From Phase 2 hypothesis]
   - Metric to measure: [CTR, conversion rate, etc.]
   - Data source: [Google Analytics, database, etc.]
   ```

   **Step 2b:** If **Qualitative experiment**, invoke `qualitative-research` skill:
   ```markdown
   Use qualitative-research skill to conduct: [Hypothesis statement]

   Context for qualitative-research:
   - Session name: [descriptive-name-for-experiment]
   - Save location: analysis/marketing-experimentation/[campaign-name]/experiments/[experiment-name]/
   - Research question: [From Phase 2 hypothesis]
   - Collection method: [Interviews | Surveys | Focus Groups | Observations]
   - Success criteria: [What insights validate/invalidate hypothesis?]
   ```

   **Step 3:** Update experiment tracker:
   - Change status from "Planned" to "In Progress"
   - Add start date
   - Update location with actual path
   - Document experiment type (Quantitative or Qualitative)

   **Step 4a:** Let **hypothesis-testing** skill complete its 5-phase workflow:
   - Phase 1: Hypothesis Formulation
   - Phase 2: Test Design
   - Phase 3: Data Analysis
   - Phase 4: Statistical Interpretation
   - Phase 5: Conclusion

   **Step 4b:** Let **qualitative-research** skill complete its 6-phase workflow:
   - Phase 1: Research Design
   - Phase 2: Data Collection
   - Phase 3: Data Familiarization
   - Phase 4: Systematic Coding
   - Phase 5: Theme Development
   - Phase 6: Synthesis & Reporting

   **Step 5:** When skill completes, update tracker:
   - Change status to "Complete"
   - Add completion date
   - Document signal (Positive/Negative/Null/Mixed)
   - Summarize key findings

   **Step 6:** Commit tracker updates after each status change

3. **Handle multi-conversation resumption**

   **At the start of EVERY conversation during Phase 4:**

   1. Check if `04-experiment-tracker.md` exists
   2. If it exists, READ IT FIRST before doing anything else
   3. Review experiment status:
      - Planned: Ready to launch
      - In Progress: Check hypothesis-testing session for current phase
      - Complete: Ready for synthesis (Phase 5)
   4. Ask user which experiment to continue or which new experiment to launch
   5. Update tracker with new status/dates/findings
   6. Commit tracker updates

   **Example resumption:**
   ```markdown
   I've read the experiment tracker. Current status:
   - Experiment 1 (H1: Value prop): Complete, Positive signal
   - Experiment 2 (H3: Email sequence): In Progress, currently in hypothesis-testing Phase 3
   - Experiment 3 (H2: Ad targeting): Planned, not yet started

   What would you like to do?
   a) Continue Experiment 2 (in hypothesis-testing Phase 3)
   b) Start Experiment 3
   c) Move to synthesis (Phase 5) since Experiment 1 is complete
   ```

4. **Coordinate parallel vs. sequential experiments**

   **Parallel execution (multiple experiments simultaneously):**
   - Launch multiple hypothesis-testing sessions
   - Track each separately in experiment tracker
   - Update tracker as each progresses independently
   - Requires managing multiple analysis directories

   **Sequential execution (one at a time):**
   - Complete one experiment fully before starting next
   - Simpler tracking, easier to manage
   - Can incorporate learnings between experiments

   **Hybrid execution:**
   - Run independent experiments in parallel
   - Sequence dependent experiments (e.g., H2 depends on H1 insights)

5. **Progress through all experiments**

   Continue invoking hypothesis-testing and updating the tracker until:
   - All selected experiments have status "Complete"
   - All experiments have documented signals
   - All findings are summarized in tracker

   Only when ALL experiments are complete should you proceed to Phase 5.

**Common Rationalization:** "I'll keep experiment details in my head - the tracker is just busywork"
**Reality:** Multi-day campaigns lose context between conversations. The tracker is the ONLY source of truth that persists across sessions. Without it, you'll re-ask questions and lose progress.

**Common Rationalization:** "I'll wait until all experiments finish before updating the tracker"
**Reality:** Batch updates create opportunity for lost data. Update the tracker IMMEDIATELY after status changes. Real-time tracking prevents confusion and missed experiments.

**Common Rationalization:** "I'll design the experiment myself instead of using hypothesis-testing"
**Reality:** hypothesis-testing skill provides rigorous experimental design, statistical analysis, and signal detection. Skipping it produces weak experiments with ambiguous results.

**Common Rationalization:** "All experiments are done, I don't need to update the tracker before synthesis"
**Reality:** The tracker is your input to Phase 5. Incomplete tracker means incomplete synthesis. Update ALL fields (status, dates, signals, findings) before proceeding.

---

## Phase 5: Cross-Experiment Synthesis

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] ALL experiments from Phase 4 marked "Complete" with signals documented
- [ ] Created aggregate results table across all experiments
- [ ] Invoked presenting-data skill to synthesize findings with visualizations
- [ ] Documented what worked, what didn't, and what's unclear
- [ ] Classified overall campaign signal (Positive/Negative/Null/Mixed)
- [ ] Saved to `05-synthesis.md`

### Instructions

**CRITICAL:** This phase synthesizes results ACROSS multiple experiments. Do NOT proceed until ALL Phase 4 experiments are complete with documented signals.

1. **Verify experiment completion**

   Read `04-experiment-tracker.md` and verify:
   - All experiments have Status = "Complete"
   - All experiments have Signal documented (Positive/Negative/Null/Mixed)
   - All experiments have Key Findings summarized

   If any experiments are incomplete, return to Phase 4 to finish them.

2. **Create aggregate results table**

   Compile findings from all experiments into a summary table:

   **Example Aggregate Table (Mixed Quantitative & Qualitative):**

   | Experiment | Type | Hypothesis | Tactic | Signal | Key Finding | Confidence |
   |------------|------|------------|--------|--------|-------------|------------|
   | E1 | Quant | Value prop clarity | Landing page A/B test | Positive | Conversion rate +18% (p<0.05) | High |
   | E2 | Qual | Customer pain points | Discovery interviews | Positive | 8 of 10 cited onboarding complexity | High |
   | E3 | Quant | Ad targeting | Ads | Null | CTR +2% (not sig., p=0.12) | Medium |
   | E4 | Qual | Ad message resonance | Focus groups | Negative | 6 of 8 found messaging confusing | High |

   **For Quantitative experiments (hypothesis-testing):**
   - Signal classification (Positive/Negative/Null/Mixed)
   - Key metric measured (CTR, conversion rate, etc.)
   - Magnitude of effect with statistical significance (e.g., "+18%, p<0.05")
   - Confidence level from statistical analysis

   **For Qualitative experiments (qualitative-research):**
   - Signal classification (Positive/Negative/Null/Mixed)
   - Key themes identified with prevalence (e.g., "8 of 10 participants mentioned X")
   - Representative quotes or patterns
   - Confidence assessment (credibility, dependability, transferability)

3. **Invoke presenting-data skill for comprehensive synthesis**

   Use the `presenting-data` skill to create complete synthesis with visualizations and presentation materials:

   ```markdown
   Use presenting-data skill to synthesize marketing experimentation results:

   Context:
   - Campaign: [campaign name]
   - Experiments completed: [count]
   - Results table: [paste aggregate table]
   - Audience: [stakeholders/decision-makers]
   - Format: [markdown report | slides | whitepaper]
   - Focus: Pattern identification across experiments (what works, what doesn't, what's unclear)
   ```

   **presenting-data skill will handle:**
   - Pattern identification (using interpreting-results internally)
   - Visualization creation (using creating-visualizations internally)
   - Synthesis documentation (markdown, slides, or whitepaper format)
   - Citation of sources (individual hypothesis-testing sessions)
   - Reproducibility (references to experiment locations)

   **Focus areas for synthesis:**
   - **What worked:** Experiments with Positive signals (both quantitative and qualitative)
   - **What didn't work:** Experiments with Negative signals (both quantitative and qualitative)
   - **What's unclear:** Experiments with Null or Mixed signals
   - **Cross-experiment patterns:** Do results cluster by tactic? By audience? By timing? Do quantitative and qualitative findings align or conflict?
   - **Triangulation:** Do qualitative findings explain quantitative results? (e.g., interviews reveal WHY conversion rate increased)
   - **Confounding factors:** Are there external factors affecting multiple experiments?
   - **Confidence assessment:** Which findings are robust? Which are uncertain? How do qualitative and quantitative confidence levels compare?

4. **Document patterns and insights**

   The presenting-data skill will create `05-synthesis.md` (or slides/whitepaper) with:

   **What Worked (Positive Signals):**
   - List experiments with positive results
   - Explain WHY these worked (based on analysis)
   - Identify commonalities across successful experiments

   **What Didn't Work (Negative Signals):**
   - List experiments with negative results
   - Explain WHY these failed (based on analysis)
   - Identify lessons learned

   **What's Unclear (Null/Mixed Signals):**
   - List experiments with inconclusive results
   - Explain potential reasons (insufficient power, confounding factors, etc.)
   - Identify what additional investigation is needed

   **Cross-Experiment Patterns:**
   - Do results cluster by tactic, audience, timing, or other factors?
   - Are there confounding variables affecting multiple experiments?
   - What overarching insights emerge?

   **Visualizations (created by presenting-data):**
   - Signal distribution (bar chart: Positive/Negative/Null/Mixed counts)
   - Effect sizes (bar chart: metric changes by experiment)
   - Confidence levels (scatter plot: effect size vs. confidence)
   - Tactic performance (grouped by channel/tactic)

5. **Classify overall campaign signal**

   Based on aggregate analysis (from presenting-data output), classify the campaign:

   **Positive:** Campaign validates concept, proceed to scaling
   - Multiple experiments show positive signals
   - Successful tactics identified for scale-up
   - Clear path to ROI improvement

   **Negative:** Campaign invalidates concept, pivot or abandon
   - Multiple experiments show negative signals
   - No successful tactics identified
   - Concept doesn't resonate with audience

   **Null:** Campaign results inconclusive, needs refinement
   - Most experiments show null signals
   - Insufficient power or confounding factors
   - Needs redesigned experiments or longer observation

   **Mixed:** Some aspects work, some don't, iterate strategically
   - Mix of positive and negative signals across experiments
   - Some tactics work, others don't
   - Selective scaling + pivots needed

6. **Review presenting-data output and finalize synthesis**

   After presenting-data skill completes:
   - Review generated synthesis document
   - Verify all experiments are covered
   - Confirm visualizations are appropriate
   - Ensure signal classification is documented
   - Make any necessary edits for clarity

7. **STOP and get user confirmation**
   - Review synthesis findings with user
   - Confirm pattern interpretations are accurate
   - Confirm overall signal classification is appropriate
   - Do NOT proceed to Phase 6 until confirmed

**Common Rationalization:** "I'll synthesize results mentally - no need to document patterns"
**Reality:** Mental synthesis loses details and creates false confidence. Documented synthesis with presenting-data skill ensures intellectual honesty and identifies confounding factors you'd otherwise miss.

**Common Rationalization:** "I'll skip synthesis for experiments with clear signals"
**Reality:** Individual experiment signals don't reveal cross-experiment patterns. Synthesis identifies why some tactics work while others don't - the strategic insight that guides iteration.

**Common Rationalization:** "Visualization is optional - the data speaks for itself"
**Reality:** Tabular data obscures patterns. Visualization reveals signal distribution, effect size clusters, and confidence patterns that inform strategic decisions. presenting-data handles this systematically.

---

## Phase 6: Iteration Planning

**CHECKPOINT:** Before proceeding, you MUST have:
- [ ] Generated 3-7 new experiment ideas based on synthesis findings
- [ ] Categorized ideas (scale winners, investigate nulls, pivot from failures, explore new)
- [ ] Documented campaign-level signal and strategic recommendation
- [ ] Explained feed-forward pattern (ideas → new marketing-experimentation sessions)
- [ ] Saved to `06-iteration-plan.md`
- [ ] Campaign complete - ready for next cycle or conclusion

### Instructions

**CRITICAL:** Phase 6 generates experiment IDEAS, NOT hypotheses. Ideas feed into new marketing-experimentation sessions where Phase 2 formalizes hypotheses. Do NOT skip the discovery and hypothesis generation steps.

1. **Generate 3-7 new experiment ideas**

   Based on Phase 5 synthesis, generate ideas for next iteration:

   **Idea Format:**

   **Idea [N]: [Brief descriptive name]**
   - **Rationale:** [Why this idea based on current findings]
   - **Expected Learning:** [What we'll learn from testing this]
   - **Category:** [Scale Winners | Investigate Nulls | Pivot from Failures | Explore New]

   **Example Ideas:**

   **Idea 1: Scale value prop landing page to paid ads**
   - **Rationale:** E1 showed +18% conversion from simplified value prop. Apply winning message to ad creative.
   - **Expected Learning:** Does simplified value prop improve ad CTR and cost-per-conversion?
   - **Category:** Scale Winners

   **Idea 2: Investigate email sequence timing sensitivity**
   - **Rationale:** E3 showed negative result for email sequence, but timing may be a confound (sent during holidays).
   - **Expected Learning:** Is the email sequence inherently weak, or was timing the issue?
   - **Category:** Investigate Nulls

   **Idea 3: Pivot from broad ad targeting to lookalike audiences**
   - **Rationale:** E2 showed null result for ad targeting. Broad targeting may dilute signal. Pivot to lookalike audiences based on E1 converters.
   - **Expected Learning:** Do lookalike audiences outperform broad targeting?
   - **Category:** Pivot from Failures

2. **Categorize ideas by strategy**

   **Scale Winners:**
   - Double down on successful tactics
   - Apply winning patterns to new channels
   - Increase budget/effort on validated approaches
   - Examples: Winning landing page → ads, winning ad → email, winning message → content

   **Investigate Nulls:**
   - Redesign experiments with null/mixed results
   - Address confounding factors identified in synthesis
   - Increase statistical power (larger sample, longer duration)
   - Examples: Retest with better timing, retest with clearer treatment, retest with focused audience

   **Pivot from Failures:**
   - Abandon unsuccessful approaches
   - Try alternative tactics for same goal
   - Apply learnings to avoid similar failures
   - Examples: Broad targeting failed → try lookalike, generic message failed → try personalization

   **Explore New:**
   - Test entirely new tactics not in original hypothesis set
   - Investigate new audience segments
   - Explore new channels or platforms
   - Examples: Add referral program, test new platform, try new content format

3. **Document campaign-level signal and strategic recommendation**

   **Campaign Summary:**
   - **Overall Signal:** [Positive | Negative | Null | Mixed]
   - **Key Wins:** [List successful tactics]
   - **Key Learnings:** [List insights regardless of signal]
   - **Strategic Recommendation:** [What to do next]

   **Strategic Recommendations by Signal:**

   **Positive Signal:**
   - Proceed to scaling: Increase budget/effort on winning tactics
   - Optimize: Refine winning approaches for incremental gains
   - Expand: Apply winning patterns to new channels/audiences

   **Negative Signal:**
   - Pivot: Major change in approach, audience, or value proposition
   - Pause: Reassess concept before additional investment
   - Abandon: Consider alternative concepts if no viable path forward

   **Null Signal:**
   - Refine: Redesign experiments with better power/clarity
   - Investigate: Address confounding factors before new tests
   - Extend: Continue observation period if time-dependent

   **Mixed Signal:**
   - Selective scaling: Double down on winners
   - Selective pivots: Abandon or redesign losers
   - Strategic iteration: Focus next tests on promising areas

4. **Explain feed-forward pattern**

   **CRITICAL:** Ideas from Phase 6 are NOT ready for testing. They MUST go through a new marketing-experimentation session:

   **Feed-Forward Cycle:**
   ```
   Phase 6 generates IDEAS
          ↓
   Start new marketing-experimentation session with idea
          ↓
   Phase 1: Discovery (validate idea with market-researcher)
          ↓
   Phase 2: Hypothesis Generation (formalize idea into testable hypotheses)
          ↓
   Phase 3-6: Complete full experimental cycle
   ```

   **Why this matters:**
   - Ideas need market validation (Phase 1) before testing
   - Ideas need formalization into specific hypotheses (Phase 2)
   - Skipping discovery leads to untested assumptions
   - Skipping hypothesis generation leads to vague experiments

   **Example:**
   Phase 6 generates "Scale value prop to ads" (idea)
   → New session Phase 1: Market research on ad platform best practices
   → New session Phase 2: Generate hypotheses like "H1: Simplified value prop in ad headline increases CTR by 10%+" (specific, testable)
   → Continue with Phase 3-6 to test formal hypotheses

5. **Create `06-iteration-plan.md`** with: `./templates/06-iteration-plan.md`

6. **STOP and review with user**
   - Review all iteration ideas with user
   - Confirm strategic recommendation is appropriate
   - Confirm understanding of feed-forward cycle
   - Discuss whether to start new marketing-experimentation session or conclude campaign

**Common Rationalization:** "I'll turn ideas directly into experiments - skip the new session"
**Reality:** Ideas need discovery and hypothesis generation. Skipping these steps leads to untested assumptions and vague experiments. Always run ideas through a new marketing-experimentation session.

**Common Rationalization:** "I'll generate hypotheses in Phase 6 for efficiency"
**Reality:** Phase 6 generates IDEAS, Phase 2 (in a new session) generates hypotheses. Conflating these skips critical validation and formalization steps. Ideas → new session → hypotheses.

**Common Rationalization:** "Campaign signal is obvious from results, no need to document strategic recommendation"
**Reality:** Documented recommendation provides clear guidance for stakeholders and future sessions. Without it, insights are lost and decisions become ad-hoc.

---

## Common Rationalizations

These are rationalizations that lead to failure. When you catch yourself thinking any of these, STOP and follow the skill process instead.

### "I'll skip discovery and just start testing - the concept is obvious"

**Why this fails:** Discovery surfaces assumptions, constraints, and existing assets that dramatically affect experiment design. "Obvious" concepts often hide critical assumptions that need validation.

**Reality:** Market-researcher agent provides current, data-driven validation signals. Asset inventory reveals resources that reduce experiment cost and time. Success criteria definition prevents ambiguous results. Always start with discovery.

**What to do instead:** Complete Phase 1 (Discovery & Asset Inventory) before generating hypotheses. Invoke market-researcher agent. Document all findings.

---

### "I'll design the experiment myself instead of using hypothesis-testing or qualitative-research"

**Why this fails:** The research skills provide rigorous experimental design, analysis, and signal detection. hypothesis-testing ensures statistical rigor for quantitative experiments. qualitative-research ensures systematic rigor for qualitative experiments. Skipping them produces weak experiments with ambiguous results.

**Reality:** Marketing-experimentation is a meta-orchestrator that coordinates multiple experiments. It does NOT design experiments itself. Delegation to appropriate skills (hypothesis-testing or qualitative-research) ensures methodological rigor.

**What to do instead:** Determine experiment type (quantitative or qualitative) in Phase 4. Invoke hypothesis-testing skill for quantitative experiments. Invoke qualitative-research skill for qualitative experiments. Let the appropriate skill handle all design, execution, and analysis.

---

### "One experiment is enough to draw conclusions"

**Why this fails:** Single experiments miss cross-experiment patterns. Some tactics work, others don't. Single-experiment campaigns can't identify which channels/tactics are most effective.

**Reality:** Marketing-experimentation tests 2-4 hypotheses to reveal strategic insights. Synthesis (Phase 5) identifies patterns across experiments - which tactics work, which don't, and why.

**What to do instead:** Follow Phase 3 prioritization to select 2-4 hypotheses. Complete all experiments before synthesis. Use Phase 5 to identify patterns.

---

### "I'll wait until all experiments complete before updating the tracker"

**Why this fails:** Batch updates create opportunity for lost data. Multi-day campaigns lose context between conversations. Incomplete tracker leads to missed experiments and confusion.

**Reality:** The experiment tracker (04-experiment-tracker.md) is the ONLY source of truth that persists across sessions. Update it IMMEDIATELY after status changes.

**What to do instead:** Update tracker after every status change (Planned → In Progress, In Progress → Complete). Commit tracker updates to git. Read tracker FIRST in every new conversation.

---

### "Results are obvious, I don't need to document synthesis"

**Why this fails:** Individual experiment signals don't reveal cross-experiment patterns. "Obvious" interpretations miss confounding factors and alternative explanations.

**Reality:** Documented synthesis with presenting-data skill ensures intellectual honesty. Visualization reveals patterns. Statistical assessment identifies robust vs uncertain findings.

**What to do instead:** Always complete Phase 5 (Cross-Experiment Synthesis). Invoke presenting-data skill. Document patterns, visualizations, and signal classification. Get user confirmation.

---

### "I'll form hypotheses in Phase 6 for efficiency"

**Why this fails:** Phase 6 generates IDEAS, not hypotheses. Ideas need discovery (Phase 1) and hypothesis generation (Phase 2) in new sessions. Skipping these steps leads to untested assumptions and vague experiments.

**Reality:** Feed-forward cycle: Phase 6 ideas → new marketing-experimentation session → Phase 1 discovery → Phase 2 hypothesis generation → Phase 3-6 complete cycle.

**What to do instead:** Generate IDEAS in Phase 6. Start NEW marketing-experimentation session with selected idea. Complete Phase 1 and Phase 2 to formalize idea into testable hypotheses.

---

### "I'll estimate ICE/RICE scores mentally instead of running the script"

**Why this fails:** Manual estimation introduces calculation errors and inconsistency. Mental math is unreliable for multiplication and division.

**Reality:** Python scripts ensure exact, reproducible results that can be audited and verified. Computational methods eliminate human error.

**What to do instead:** Use Python scripts (ICE or RICE calculator) from Phase 3 instructions. Update hypothesis data in script. Run script and document exact scores. Copy output table to prioritization document.

---

### "I'll synthesize results mentally - no need to use presenting-data"

**Why this fails:** Mental synthesis loses details and creates false confidence. Cross-experiment patterns require systematic analysis.

**Reality:** presenting-data skill handles pattern identification (via interpreting-results), visualization creation (via creating-visualizations), and synthesis documentation. It ensures intellectual honesty and reproducibility.

**What to do instead:** Always invoke presenting-data skill in Phase 5. Provide aggregate results table. Request pattern analysis and visualizations. Document all findings from presenting-data output.

---

## Summary

The marketing-experimentation skill ensures rigorous, evidence-based validation of marketing concepts through structured experimental cycles. This skill orchestrates the complete Build-Measure-Learn loop from concept to data-driven signal.

**What this skill ensures:**

1. **Validated concepts through market research** - market-researcher agent provides current demand signals, competitive landscape analysis, and audience insights before experimentation begins.

2. **Strategic hypothesis generation** - 5-10 testable hypotheses spanning multiple tactics (landing pages, ads, email, content) grounded in discovery findings and mapped to experimentation frameworks (Lean Startup, AARRR).

3. **Data-driven prioritization** - Computational methods (ICE/RICE Python scripts) ensure exact, reproducible scoring. Selection of 2-4 highest-value hypotheses optimizes resource allocation.

4. **Multi-experiment coordination** - Experiment tracker (living document) enables multi-conversation workflows spanning days or weeks. Status tracking (Planned, In Progress, Complete) maintains visibility across all experiments. Supports both quantitative and qualitative experiment types.

5. **Methodological rigor through delegation** - hypothesis-testing skill handles quantitative experiment design (statistical analysis, A/B tests, metrics). qualitative-research skill handles qualitative experiment design (interviews, surveys, focus groups, observations, thematic analysis). Marketing-experimentation coordinates multiple tests without duplicating methodology.

6. **Cross-experiment synthesis** - presenting-data skill identifies patterns across experiments (what works, what doesn't, what's unclear). Aggregate analysis reveals strategic insights invisible in single experiments.

7. **Clear signal generation** - Campaign-level classification (Positive/Negative/Null/Mixed) with strategic recommendations (Scale/Pivot/Refine/Pause) provides actionable guidance for stakeholders.

8. **Systematic iteration** - Phase 6 generates experiment IDEAS (not hypotheses) that feed into new marketing-experimentation sessions. Feed-forward cycle maintains rigor through repeated discovery and hypothesis generation.

9. **Multi-conversation persistence** - Complete documentation at every phase enables resumption after days or weeks. Experiment tracker serves as coordination hub. All artifacts are git-committable.

10. **Tool-agnostic approach** - Focuses on techniques (value proposition testing, targeting strategies, sequence optimization) rather than specific platforms. Applicable across marketing tools and channels.

**Key principles:**
- Discovery before experimentation (Phase 1 always first)
- Hypothesis generation separate from idea generation (Phase 2 vs Phase 6)
- Multiple experiments for pattern identification (2-4 minimum)
- Computational scoring for objectivity (Python scripts)
- Delegation for methodological rigor (hypothesis-testing for quantitative, qualitative-research for qualitative)
- Mixed-methods integration (quantitative metrics + qualitative insights for complete picture)
- Synthesis for strategic insight (presenting-data skill handles both quantitative and qualitative results)
- Documentation for reproducibility (numbered markdown files, git commits)
- Iteration through validated cycles (ideas → new sessions → discovery → hypotheses)
