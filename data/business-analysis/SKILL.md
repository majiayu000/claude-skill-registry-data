---
name: business-analysis
description: Business analysis skill for requirements gathering, market research, strategic analysis, and project brief creation. Use when users need to (1) Create comprehensive project briefs, (2) Conduct market or competitive analysis, (3) Facilitate brainstorming sessions, (4) Define problems and validate assumptions, (5) Elicit requirements through structured questioning, (6) Create user personas, or (7) Analyze project feasibility and scope
---

# Business Analysis Skill

This skill provides Business Analyst expertise for requirements gathering, strategic analysis, and project brief creation following the BMAD Method.

## Core Workflows

### 1. Project Brief Creation

Create comprehensive 10-15 page project briefs through this five-phase process:

1. **Discovery Phase**: Use strategic questioning to understand project vision
   - Ask context questions to understand current state
   - Use clarifying questions to eliminate ambiguity
   - Employ probing questions to understand deeper motivations
   - Reference: `references/question-patterns.md` for question templates

2. **Exploration Phase**: Facilitate brainstorming to generate and evaluate ideas
   - Select appropriate brainstorming techniques based on the challenge
   - Use divergent techniques to generate ideas (Classic Brainstorming, SCAMPER, Mind Mapping)
   - Use convergent techniques to evaluate and prioritize (Dot Voting, 2×2 Matrix)
   - Reference: `references/brainstorming-techniques.md` for 30+ techniques with "when to use" guidance

3. **Analysis Phase**: Conduct market research and competitive analysis
   - Research market size, trends, and dynamics
   - Analyze competitors (features, pricing, positioning, strengths/weaknesses)
   - Understand user behavior and preferences
   - Assess regulatory and compliance requirements
   - Reference: `references/market-research-framework.md` for complete research structure

4. **Synthesis Phase**: Structure findings into comprehensive brief
   - Use the project brief template to organize all information
   - Create 2-3 detailed user personas based on research
   - Define clear success criteria and metrics
   - Assess risks and dependencies
   - Determine preliminary scope (MVP vs future phases)
   - Reference: `references/project-brief-template.md` for complete structure
   - Asset: `assets/project-brief.md` (copy and populate this template)

5. **Validation Phase**: Stress-test assumptions and validate with stakeholders
   - Use validation questions to confirm understanding
   - Challenge key assumptions with stakeholders
   - Verify market research findings
   - Ensure all sections are complete and consistent
   - Get stakeholder sign-off

**Output**: Complete project brief document ready to hand off to Product Manager for PRD creation.

### 2. Brainstorming Facilitation

Facilitate structured brainstorming sessions to generate and evaluate ideas:

**Select Appropriate Technique Based on Context**:
- **Divergent thinking** (generating many ideas):
  - Classic Brainstorming: Quick ideation in groups
  - SCAMPER: Improving existing products/processes
  - Mind Mapping: Exploring connections and relationships
  - Random Word: Breaking mental blocks
  - Brain Writing: Balanced participation, quiet ideation
  
- **Convergent thinking** (narrowing to best options):
  - Dot Voting: Democratic prioritization
  - 2×2 Matrix: Evaluating on two dimensions (Effort vs Impact, etc.)
  - Affinity Mapping: Organizing ideas into categories
  - Multi-Voting: Reducing long lists to manageable options
  
- **Structured exploration** (systematic analysis):
  - How Might We: Reframing problems as opportunities
  - Five Whys: Finding root causes
  - SWOT Analysis: Strategic assessment
  - Starbursting: Exploring all angles (Who, What, When, Where, Why, How)

**Facilitation Pattern**:
1. Frame the challenge clearly
2. Set ground rules (no criticism, build on ideas, time limits)
3. Select and apply appropriate technique(s)
4. Capture all ideas visibly
5. Synthesize and organize results
6. Prioritize using convergent techniques
7. Document actionable insights

Reference: `references/brainstorming-techniques.md` for detailed guidance on 30+ techniques.

### 3. Requirements Elicitation

Systematically elicit requirements through structured questioning:

**Question Types and When to Use Them**:

1. **Context Questions**: Early discovery, understand current state
   - "Who are the main users?"
   - "Walk me through your current process"
   - "How do users currently solve this problem?"

2. **Clarifying Questions**: Eliminate ambiguity
   - "Can you elaborate on [term]?"
   - "When you say [X], do you mean [A] or [B]?"

3. **Probing Questions**: Understand the "why"
   - "Why is [feature] important?"
   - "What problem does this solve?"
   - "What happens if we don't include this?"

4. **Validation Questions**: Confirm understanding
   - "Let me make sure I understand: [summary], correct?"
   - "How would you verify that [requirement] has been met?"

5. **Priority Questions**: Determine scope
   - "If you could only build three features, which three?"
   - "What's the minimum you need to get value?"

6. **Constraint Questions**: Identify boundaries
   - "What limitations should I be aware of?"
   - "Are there compliance requirements?"

7. **Scenario Questions**: Explore use cases
   - "Walk me through a typical day using this"
   - "What would you do if [edge case]?"

8. **Quantitative Questions**: Get measurable data
   - "How many users/transactions are we talking about?"
   - "What's an acceptable response time?"

Reference: `references/question-patterns.md` for comprehensive question patterns and sequencing guidance.

### 4. Market Research

Conduct thorough market research covering six key areas:

**Research Areas**:

1. **Market Size & Dynamics**
   - Total Addressable Market (TAM), SAM, SOM
   - Market growth rate and maturity stage
   - Key market drivers and trends
   
2. **Competitive Analysis**
   - Direct competitors (same solution, same market)
   - Indirect competitors (different solution, same problem)
   - Feature comparison matrix
   - Pricing analysis
   - Strengths/weaknesses assessment
   - Asset: `assets/competitor-matrix.md` (use this template)

3. **Technology Landscape**
   - Enabling technologies and trends
   - Technical risks and opportunities
   - Infrastructure options

4. **Regulatory & Compliance**
   - Data privacy (GDPR, CCPA, HIPAA)
   - Security standards (SOC 2, ISO 27001)
   - Industry-specific requirements

5. **User Behavior & Trends**
   - Current solutions and workarounds
   - Pain points and preferences
   - Adoption barriers
   - Decision criteria

6. **Pricing Analysis**
   - Common pricing models in the space
   - Price points across tiers
   - Value metrics
   - Freemium strategies

**Research Process**:
1. Define research questions (what decisions depend on this?)
2. Identify sources (primary, secondary, tertiary)
3. Gather data systematically
4. Analyze findings (patterns, gaps, contradictions)
5. Synthesize into report
6. Validate with stakeholders

Reference: `references/market-research-framework.md` for detailed research guidance and output formats.

### 5. User Persona Creation

Create 2-3 detailed user personas based on research (not assumptions):

**Persona Components**:
- Demographics and professional context
- Goals, motivations, and success metrics
- Pain points and frustrations (with frequency and impact)
- Behaviors, preferences, and work style
- User journey (awareness, consideration, decision, adoption, ongoing use)
- Key quote that captures their perspective
- Implications for product design

**Persona Development Process**:
1. Conduct user research (interviews, surveys, analytics)
2. Identify patterns across users
3. Create 2-3 distinct personas (primary and secondary)
4. Validate personas with real users
5. Document using comprehensive template

Reference: `references/persona-template.md` for complete persona structure and validation guidance.

## Key Decision Points

When creating project briefs, make explicit decisions about:

1. **Scope Determination**: MVP vs full feature set
   - What must be in version 1 to provide value?
   - What can wait for later phases?
   - Use priority questions and 2×2 matrix (Effort vs Impact)

2. **Timeline Estimation**: Realistic vs aspirational
   - What's achievable given resources?
   - What dependencies affect timeline?
   - What risks could cause delays?

3. **Resource Assessment**: What's needed vs what's available
   - Team size and expertise required
   - Budget constraints
   - Technology and infrastructure needs

4. **Risk Prioritization**: Which risks need immediate attention
   - What could cause project failure?
   - What risks have highest impact?
   - What mitigation strategies are most important?
   - Asset: `assets/risk-assessment-matrix.md` (use this template)

## Output Quality Standards

Project briefs must include:

- **Clear problem definition** with current state and opportunity
- **Market analysis** with competitor comparison matrix
- **2-3 detailed user personas** based on research (not assumptions)
- **Measurable success criteria** with KPIs and validation methods
- **Risk assessment** with mitigation strategies for top risks
- **Explicit scope boundaries** (in-scope MVP, should-have features, out-of-scope items)
- **Validated assumptions** with confidence levels indicated
- **Next steps** with clear ownership and deadlines

## Best Practices

### Conversation Management
- Ask 2-3 questions at a time (avoid overwhelming users)
- Use open questions for discovery, closed questions for validation
- Listen actively and follow interesting threads
- Summarize periodically to confirm understanding
- Circle back to missed topics

### Research Quality
- Use multiple sources for critical facts
- Note confidence levels for key findings
- Identify and document gaps in research
- Look for contradictions between sources
- Stop researching when additional research won't change decisions

### Brainstorming Facilitation
- Create safe environment for sharing ideas
- Defer judgment during idea generation
- Build on ideas rather than criticize
- Keep energy high with variety of techniques
- Capture all ideas visibly

### Persona Development
- Base personas on real research, not assumptions
- Make personas specific and concrete
- Include both positive traits and pain points
- Validate personas with real users
- Update personas as you learn more

## Integration with BMAD Method

**This skill is the foundation of the BMAD Method**:

**Outputs from this skill feed into**:
- **Product Manager**: Project brief becomes input for PRD creation
- **Technical Architect**: Market research and personas inform solution design
- **UX Designer**: User personas and user journey inform UX design

**This skill produces**:
- Validated project brief with clear problem definition
- Market context and competitive landscape
- User personas grounded in research
- Initial scope and success criteria
- Risk assessment and mitigation strategies

**Handoff checklist** before moving to next phase:
- [ ] Problem clearly defined with evidence
- [ ] Market research completed and synthesized
- [ ] 2-3 personas created and validated
- [ ] Success criteria measurable and agreed upon
- [ ] Top risks identified with mitigation plans
- [ ] Preliminary scope defined (MVP and future phases)
- [ ] Stakeholders have reviewed and approved brief

## When NOT to Use This Skill

Skip or abbreviate this analysis when:
- Building a simple bug fix or small enhancement (not a new project)
- Requirements are already well-documented
- Time constraints don't allow for full analysis
- Project is internal tool with well-understood users
- This is an iteration on existing product with known market

Even for smaller projects, consider using:
- Question patterns for requirements gathering
- Quick brainstorming for ideation
- Light competitive research to check for new threats

## Tips for Efficient Use

**Time Management**:
- Set time boxes for each research area
- Start broad, then go deep on promising areas
- Good enough is often better than perfect
- Don't get lost in research rabbit holes

**Documentation**:
- Track sources meticulously as you research
- Capture exact quotes and data points
- Screenshot or save important data
- Organize by research question or topic

**Stakeholder Management**:
- Involve stakeholders early and often
- Get feedback at each phase
- Validate assumptions continuously
- Manage expectations about timeline and scope

## Quick Reference

**Starting a new project?**
1. Read `references/project-brief-template.md` to understand structure
2. Use `references/question-patterns.md` to elicit requirements
3. Facilitate brainstorming with `references/brainstorming-techniques.md`
4. Conduct research using `references/market-research-framework.md`
5. Create personas with `references/persona-template.md`
6. Copy `assets/project-brief.md` and populate it
7. Use `assets/competitor-matrix.md` and `assets/risk-assessment-matrix.md` as needed

**Need to facilitate brainstorming?**
- Go to `references/brainstorming-techniques.md`
- Find technique matching your context
- Follow the process steps
- Capture and synthesize results

**Need to gather requirements?**
- Go to `references/question-patterns.md`
- Follow the question sequencing guidance
- Use appropriate question types for each phase
- Validate understanding continuously
