---
name: ai-readiness-assessor
description: "Assess organizational AI readiness — capabilities, gaps, adoption roadmap for strategic planning."
tags: [planning, strategy, assessment, ai, organizational-readiness]
inherits: planner-base-protocol
version: 0.1.0
---

# AI Readiness Assessor

## JTBD (Jobs To Be Done)

### Primary Job
When my organization wants to invest in AI but I can't tell whether the enthusiasm is grounded or whether we're about to buy expensive infrastructure that sits idle,
I want a structured readiness assessment across data, infrastructure, capability, strategy, use cases, and culture,
so I can make investment decisions based on evidence of actual organizational readiness rather than vendor pressure or competitor anxiety.

### Secondary Jobs
- When leadership has approved an AI budget but no one has verified whether the organization has the data governance, MLOps maturity, or change management capacity to actually use AI tools, I want those gaps quantified before procurement starts, so the investment doesn't stall at implementation.
- When an AI pilot succeeded in one team but the organization is debating whether to scale it, I want a readiness assessment that distinguishes pilot conditions from enterprise conditions, so the scaling decision accounts for what the pilot had that other teams don't.

### Job Layers
- Functional: Assess organizational AI readiness across six dimensions (data maturity, infrastructure, capability, strategy alignment, use case viability, cultural readiness) and produce a prioritized roadmap with sequenced recommendations.
- Emotional: Reduce the anxiety of committing significant AI investment before understanding whether the organization can absorb it — the fear of being the person who championed the AI platform that nobody uses.
- Social: Helps the user present a credible, structured assessment to leadership, board members, and vendors that shows the organization evaluated readiness systematically rather than following hype.

### This Skill Is For
- An organization considering significant AI investment that needs to know where the real readiness gaps are before committing budget.
- A leader who needs to distinguish genuine AI readiness from enthusiasm — whether the org has the data, skills, and processes to actually operationalize AI.
- A team that ran a successful AI pilot and needs to assess whether the conditions that made it work exist across the broader organization.

### This Skill Is NOT For
- A user with an existing AI strategy or readiness report who needs a quality verdict on it; use `proposal-critic` instead.
- A user who needs to plan a specific AI/ML implementation rather than assess organizational readiness; use a domain-specific planner instead.

### Paired With
- `proposal-critic`: After the readiness assessment is complete, use it to stress-test the recommendations and roadmap.
- `stakeholder-report-writer`: Use this when the assessment is done but needs to be translated into audience-specific reporting for leadership, board, or technical teams.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Organization wants AI but hasn't assessed readiness | The skill evaluates all six dimensions and scores maturity levels | A prioritized roadmap with sequenced recommendations and quick wins |
| AI budget approved but implementation readiness unknown | The skill identifies specific gaps (data governance, MLOps, change management) blocking implementation | A gap analysis with the specific capabilities to build before procurement |
| Successful pilot needs scaling decision | The skill compares pilot conditions to enterprise conditions | An honest assessment of what scales and what doesn't, with prerequisites |

### When to Escalate
- If the user already has an AI strategy document and needs a quality verdict, escalate to `proposal-critic`.
- If the user needs the assessment translated into stakeholder-specific reports, escalate to `stakeholder-report-writer`.

## Purpose

Most organizations that fail at AI adoption don't lack technical capability—they lack readiness across the full organizational ecosystem. This skill conducts a structured assessment across six critical dimensions, producing a prioritized roadmap that prevents costly missteps and accelerates time-to-value.

**Why structured assessment matters:**
- Organizations that bought expensive ML platforms without data governance infrastructure (wasted 40-60% of budget)
- Teams with pristine data but no MLOps practices (models trained but never deployed)
- Technical readiness achieved but change management failed (adoption rates under 30%)
- Regulatory blindness leading to compliance violations during pilot phases
- Use case selection without ROI validation (high-effort, low-impact projects consuming 18+ months)

This skill aligns business goals, technical reality, organizational capability, and governance requirements into a coherent roadmap with sequenced milestones.

## Use_When

- **Strategic AI Planning**: Organization is deciding whether/how to adopt AI, or scaling from pilot to enterprise
- **Investment Validation**: Before committing significant budget to AI platforms, vendors, or teams
- **Pre-Engagement Assessment**: Consulting engagement kickoff to establish baseline and roadmap
- **Organizational Transformation**: Simultaneous technology and capability building initiatives
- **Compliance & Risk**: Organizations in regulated industries (healthcare, finance, legal) needing governance frameworks
- **Talent & Capability Building**: Organizations planning to build internal AI/ML centers of excellence

## Do_Not_Use_When

- Assessing readiness for **specific projects** already approved (use project-scope-analyzer instead)
- Evaluating individual **technical tools or platforms** (use tool-evaluation-framework)
- Focused solely on **data infrastructure** without organizational scope (use data-infrastructure-assessor)
- Organizations not ready to act on recommendations (assessment requires commitment to roadmap)
- Technical deep-dives into model performance or ML system design

## Why_This_Exists

### Common AI Adoption Failures & Prevention

**Failure Pattern 1: Technology-First Trap**
- Organization: "We'll buy a best-in-class ML platform and hire data scientists"
- Reality: Without data governance, clean data pipelines, and business prioritization, expensive tools sit idle
- Prevention: Assess data readiness first, align technology investments to capability gaps

**Failure Pattern 2: Data Infrastructure Without Governance**
- Organization: "We have great data lakes and APIs"
- Reality: Without naming standards, lineage tracking, and stewardship models, data scientists spend 80% of time data wrangling
- Prevention: Score governance maturity alongside infrastructure maturity; de-risk before scaling

**Failure Pattern 3: Technical Success, Adoption Failure**
- Organization: "We trained an amazing churn prediction model"
- Reality: Marketing teams don't trust the model; sales doesn't change workflows; model rots in production
- Prevention: Build use-case validation and change management into the roadmap from discovery

**Failure Pattern 4: Isolated Center of Excellence**
- Organization: "We hired 5 PhD data scientists"
- Reality: Teams can't collaborate with domain experts; no pathway to push models into production; talent burns out
- Prevention: Assess cross-functional capability and MLOps maturity; identify collaboration dependencies

**Failure Pattern 5: Regulatory Blind Spot**
- Organization: "We're deploying customer-facing models"
- Reality: Model bias triggers fair lending violations; no audit trail for explainability; GDPR deletion requests fail
- Prevention: Assess governance and compliance posture before pilot; build guardrails into roadmap

## Companion_Skills

- **stakeholder-report-writer**: Convert assessment output into executive summaries for specific stakeholder audiences (C-suite, board, technical team)
- **proposal-critic**: Validate AI proposals against readiness assessment; identify high-risk initiatives
- **data-strategy-planner**: Deep-dive into data governance and architecture recommendations from the assessment
- **talent-acquisition-advisor**: Define hiring profiles and contracting models based on capability gaps
- **change-management-designer**: Operationalize the culture and change management roadmap

## Steps

### Phase 1: Organization Context & Goals (Gather)

**Inputs to collect:**
1. **Organization Profile**
   - Industry vertical and segment (enterprise SaaS, healthcare, retail, financial services, manufacturing, etc.)
   - Company size (headcount, revenue)
   - Geographic footprint and data residency requirements
   - Current technology stack (legacy systems, cloud platforms, custom applications)
   - Reporting structure and decision-making authority

2. **AI Aspirations & Drivers**
   - Primary business objectives (revenue growth, cost reduction, risk mitigation, customer experience, competitive positioning)
   - Specific use cases under consideration (prioritized or exploratory list)
   - Stakeholder appetite for AI (enthusiastic, cautious, skeptical by function)
   - Existing AI investments or failed initiatives
   - Competitive landscape pressures

3. **Constraints & Guardrails**
   - Budget ceiling for AI programs (Year 1, 3-year)
   - Regulatory environment (HIPAA, GDPR, FCA, sector-specific rules)
   - Data residency/sovereignty requirements
   - Risk tolerance (conservative vs aggressive)
   - Timeline expectations (pilot in 6 months vs 18+ months transformation)

**Assessment technique**: Structured interview with business sponsor, CTO/CIO, and domain leaders. Document as narrative + structured JSON.

---

### Phase 2: Current State Assessment (Score)

Evaluate each of 6 dimensions on a 1-5 maturity scale with evidence. Score reflects **actual capability today**, not aspirations.

#### Dimension 1: Data Readiness
**Definition**: Quality, accessibility, governance, and organizational literacy around data assets

**1 - Ad-hoc**:
- Data lives in silos (departmental databases, spreadsheets, email)
- No data dictionary or cataloging; teams don't know what data exists
- Data quality issues are frequent and reactively fixed
- No formal data governance; data stewardship is informal
- Data literacy is low; most non-technical stakeholders can't query data
- *Evidence*: "Data requests take 3+ weeks" / "We discovered duplicate customer records after 6 months"

**2 - Managed**:
- Centralized data warehouse or lake exists; core business data is accessible
- Basic cataloging effort underway; some metadata tracked
- Data quality rules exist for critical datasets; issues caught in reporting
- Data governance committee meets quarterly; roles assigned informally
- Finance and marketing can run SQL; broader org needs analyst support
- *Evidence*: "We have a Snowflake data warehouse but no lineage tracking" / "Data governance is in someone's job description"

**3 - Standardized**:
- Data warehouse/lake with automated pipelines; most operational data flows daily
- Data catalog with 70%+ coverage; lineage tracking for critical pipelines
- Data quality metrics defined and monitored; automated alerts for anomalies
- Formal data stewardship model with owner-per-dataset; governance council reviews policies quarterly
- Self-service BI tools widely adopted; data engineering and analytics teams collaborate on standards
- *Evidence*: "We have dbt documentation" / "Data quality dashboards show SLAs met 98% of time"

**4 - Optimized**:
- Real-time and batch pipelines orchestrated; data latency measured and guaranteed
- Data catalog integration with discovery tools; data lineage includes impact analysis
- Data quality platform (Great Expectations, Soda) in use; automated remediation for known issues
- Formal data contracts between producers and consumers; governance enforced in tooling
- Most analysts and business users can self-serve on structured queries; advanced analytics done by specialists
- *Evidence*: "Data freshness SLAs are <4 hours" / "We have data contracts in place"

**5 - Innovating**:
- Federated data architecture with real-time integration; data mesh principles applied
- AI-driven data discovery and anomaly detection; automatic lineage and impact recommendations
- Data quality prediction and prevention (modeling data issues before they impact production)
- Data governance automated through metadata platforms; compliance validation built into pipelines
- Entire organization (product, marketing, finance, operations) uses data in decision-making daily
- *Evidence*: "We use data contracts and federated governance" / "Data quality issues are predicted 80% of the time"

**Scoring Evidence Checklist**:
- How long do data requests take? (weeks vs days vs hours)
- What % of your data is cataloged and searchable?
- What's your data quality SLA and how often is it met?
- Who owns data governance? Full-time role or add-on responsibility?
- Can non-technical stakeholders access data or do they need analyst translation?

---

#### Dimension 2: Technical Infrastructure
**Definition**: Compute capacity, architecture, MLOps practices, API/integration design, security and privacy controls

**1 - Ad-hoc**:
- On-premises infrastructure or legacy cloud (single vendor, limited flexibility)
- No ML platform; models trained in notebooks and exported manually
- APIs are few and inconsistent; integrations are point-to-point scripts
- Security is perimeter-based; no data encryption in transit/at rest
- Privacy by default doesn't exist; no PII handling policy
- *Evidence*: "We train models in Excel/Python locally" / "Models deploy by copying files to a server"

**2 - Managed**:
- Mix of on-premises and cloud (AWS/Azure/GCP); some modernization started
- ML development tools exist (Jupyter, scikit-learn); no production ML framework
- Some APIs built using frameworks (REST/gRPC); 20-30% of integrations API-first
- Security basics: firewalls, VPNs, some encryption; compliance standards known but not fully implemented
- Privacy by design limited; PII handling is manual and inconsistent
- *Evidence*: "We use AWS but don't have automated model training" / "We have some APIs but many batch jobs"

**3 - Standardized**:
- Hybrid cloud strategy defined; cloud-native architecture adopted (containers, microservices)
- MLOps platform in use (SageMaker, Datadog, Kubeflow, or similar); model versioning and experiment tracking
- API-first architecture for 50%+ of integrations; API gateway and standards documented
- Data encryption standard for all new systems; identity and access management (IAM) in place
- Privacy impact assessments required for new data uses; PII masking/anonymization in dev/test environments
- *Evidence*: "We use Kubernetes and Docker" / "We have a model registry and CI/CD for models"

**4 - Optimized**:
- Multi-cloud or cloud-agnostic architecture; infrastructure as code and GitOps practices
- MLOps fully automated: model training on schedule, A/B testing, automated retraining, monitoring/alerting
- API-first, 80%+ of integration; API contracts and versioning; gateway with rate limiting and auth
- Zero-trust security model; encryption throughout; secrets management (Vault, AWS Secrets Manager)
- Privacy embedded: PII detection, differential privacy, federated learning experimentation, audit logs for all data access
- *Evidence*: "Our models retrain on schedule and we A/B test in production" / "All APIs are versioned with OpenAPI specs"

**5 - Innovating**:
- Autonomous infrastructure management; AI-driven resource optimization and auto-scaling
- MLOps on automated data pipelines; models deployed to edge; continuous learning with human-in-the-loop feedback
- Real-time event-driven APIs; GraphQL and API composition patterns; microgateway architecture
- Decentralized identity and privacy-preserving ML (federated, differential privacy); automated compliance validation
- Privacy-first data architecture; data minimization enforced; regulatory compliance automated
- *Evidence*: "We deploy models to edge devices" / "We use differential privacy in our ML pipeline"

**Scoring Evidence Checklist**:
- Where does your compute live (on-prem, single cloud, multi-cloud)?
- How do you train, version, and deploy ML models? (Manual vs automated)
- What % of integrations are API-based?
- Is encryption in place for data in transit and at rest?
- Who can access production data and how is it audited?

---

#### Dimension 3: Organizational Capability
**Definition**: In-house AI/ML talent, cross-functional collaboration, leadership literacy, change management capacity, training programs

**1 - Ad-hoc**:
- No dedicated AI/ML team; technical staff build models part-time
- Single data scientist or no one; external consultant engaged ad-hoc
- Siloed departments; business and engineering don't collaborate on problems
- Leadership views AI as a technology problem, not a business transformation
- No formal training; learning is self-directed
- *Evidence*: "Our database admin builds models as a side project" / "We bring in consultants for each project"

**2 - Managed**:
- 1-2 dedicated data scientists/engineers; mostly hire contractors
- Part-time product-data analytics team; some business analysts
- Cross-functional projects happen; collaboration is informal and reactive
- Leadership believes in AI potential but delegates execution to technical team
- Training offered but not mandatory; YouTube and conferences are primary sources
- *Evidence*: "We have one senior data scientist" / "We use Upwork for specialized skills"

**3 - Standardized**:
- 3-5 dedicated AI/ML engineers; mix of internal and contract talent
- Dedicated analytics platform team; data engineers focused on pipeline quality
- Cross-functional product/analytics/engineering teams meet regularly; standard processes for collaboration
- Leadership participates in quarterly AI planning; business sponsorship for projects
- Internal training programs established (lunch-and-learns, courses); certifications encouraged
- Change management plan documented for major AI rollouts
- *Evidence*: "We have a 4-person ML team and a data engineer" / "We run monthly cross-functional planning meetings"

**4 - Optimized**:
- 8-12 person AI/ML team; specialized roles (platform engineers, MLOps, domain experts); strategic hiring plan
- Multiple squads aligned to business domains; strong partnership with product and operations
- Formal governance: technical review boards, architecture decisions, standards and best practices documented
- CIO/CTO owns AI roadmap; board-level reporting on AI metrics and ROI
- Formal training program: internal university, vendor certifications, conference attendance budget; internal knowledge sharing forums
- Dedicated change management and organizational development resources
- *Evidence*: "We have data scientists, ML engineers, and platform engineers with specialized roles" / "We have a formal AI governance board"

**5 - Innovating**:
- 15+ person AI/ML organization including researchers, platform engineers, domain specialists
- Distributed model with AI embedded in every product squad; centralized platform and research teams
- Continuous talent development; partnerships with universities and research institutions
- CEO/board actively engaged in AI strategy; quarterly business reviews on AI portfolio
- Internal research track alongside product delivery; patents and open source contributions
- Organizational structures redesigned around AI capabilities; change management is embedded in culture
- *Evidence*: "We hire PhDs and fund research" / "We contribute to open source ML projects"

**Scoring Evidence Checklist**:
- How many dedicated AI/ML staff do you have (headcount and full-time equivalent)?
- How easily can data scientists, engineers, and business stakeholders collaborate?
- Does leadership actively sponsor AI initiatives or delegate?
- What % of staff participate in formal AI/ML training annually?
- Who is accountable for change management in major AI rollouts?

---

#### Dimension 4: Strategy & Governance
**Definition**: AI strategy aligned to business goals, ethical frameworks, responsible AI policies, regulatory compliance, risk management

**1 - Ad-hoc**:
- No formal AI strategy; projects initiated by individuals
- No ethics or responsible AI framework; fairness/bias not discussed
- Compliance reactive; only legal escalations trigger governance
- Risk management for AI absent; models deployed without review
- No audit trail or explainability requirements
- *Evidence*: "We don't have an AI strategy; we do AI projects as they come up" / "We've never discussed model bias"

**2 - Managed**:
- AI strategy exists but not formally written or communicated; leadership aware but not actively driving
- Basic fairness discussion; awareness that bias could be a problem; no systematic testing
- Compliance known; some policies drafted; audit trail incomplete
- Risk register for AI exists; some model review before production (technical review only)
- Explainability discussed for high-risk models but not enforced
- *Evidence*: "We have AI goals but no written strategy" / "We've done one bias audit"

**3 - Standardized**:
- AI strategy written and communicated; aligned to business goals; reviewed annually
- Responsible AI framework documented; fairness, transparency, accountability, and privacy principles defined
- Compliance requirements mapped; policies for GDPR, CCPA, sector-specific rules (HIPAA, FCA) drafted and communicated
- Risk governance: design review, model cards, fairness testing before production; incident response plan
- Audit trail for model decisions (especially high-stakes: lending, healthcare, hiring); explainability standard for regulated models
- *Evidence*: "We have a documented AI ethics policy" / "Models require fairness testing before deployment"

**4 - Optimized**:
- AI strategy integrated with business strategy; quarterly business reviews on AI portfolio performance and risk
- Responsible AI maturity model in place; fairness, privacy, security, and explainability tested routinely
- Compliance automated where possible (data discovery, PII handling); audit trails comprehensive; quarterly compliance review
- Risk governance embedded in development: automated fairness checks, model monitoring for drift/bias, guardrails in production
- Explainability and audit trails automatic for all models; customer-facing decisions always explainable on request
- Third-party audits or certifications pursued (AI audits, industry standards)
- *Evidence*: "We have automated bias detection in our CI/CD" / "We maintain audit trails for all model decisions"

**5 - Innovating**:
- AI strategy drives competitive advantage; AI organizational transformation underway
- Responsible AI embedded in culture; proactive design for fairness, transparency; external thought leadership
- Compliance preventive; regulatory changes anticipated and built into standards; collaboration with regulators
- Risk anticipation through scenario modeling; adversarial testing; continuous governance improvement
- Explainability by design; models built with interpretability; compliance automation extends to ethics and fairness
- Industry leadership on responsible AI; public commitment and accountability
- *Evidence*: "We publish our responsible AI principles" / "We participate in AI governance working groups"

**Scoring Evidence Checklist**:
- Is there a written AI strategy aligned with business goals?
- What responsible AI principles are documented (fairness, privacy, transparency, accountability)?
- What compliance frameworks apply to your industry and which have you addressed?
- What's your process for reviewing models before production?
- Can you explain the reasoning behind high-stakes model decisions?

---

#### Dimension 5: Use Case Readiness
**Definition**: Problem-solution fit, ROI estimation, prioritization rigor, pilot design, success metrics definition

**1 - Ad-hoc**:
- Use cases identified informally by stakeholders; little validation
- ROI guessed; business impact not quantified
- Priority based on interest or loudest voice; no portfolio management
- Pilots are one-offs; success criteria vague ("see if it works")
- Metrics reactive; chosen after results are in
- *Evidence*: "We want a chatbot because competitors have one" / "We'll know if the model is good when we see the results"

**2 - Managed**:
- Use cases documented; basic problem statement written
- ROI estimated roughly (cost of vendor/team vs rough savings)
- Prioritization criteria discussed; not formally scored
- Pilot scope defined; success criteria written but vague
- Some metrics defined upfront; focus on model accuracy
- *Evidence*: "We want to reduce churn by 5%" / "We'll measure F1 score and AUC"

**3 - Standardized**:
- Use case template; problem statement, success criteria, and metrics documented
- ROI estimation systematic: baseline cost, expected lift, implementation cost; 3-year model built
- Prioritization matrix: impact × feasibility × alignment scoring; portfolio view of top 10 use cases
- Pilot scope limited; 3-month runway; success criteria include business metrics and adoption
- Metrics balanced: model performance (accuracy, precision, recall), business impact (revenue, cost, time saved), and adoption metrics
- *Evidence*: "We scored each use case on impact, feasibility, and alignment" / "Pilot success includes business metrics and technical metrics"

**4 - Optimized**:
- Use case assessment deep: customer research, competitive analysis, build-vs-buy evaluation
- ROI comprehensive: includes implementation cost, ongoing operations, change management, risk discount; sensitivity analysis
- Prioritization sophisticated: considers dependencies, sequencing, and capability building; portfolio balancing (quick wins vs strategic)
- Pilot design rigorous: control group, A/B testing, clear launch criteria, rollback plan
- Metrics comprehensive: technical (model performance), business (revenue, cost, velocity), operational (latency, uptime), and adoption metrics with targets
- *Evidence*: "We evaluated 3 vendors and 2 build options" / "We run A/B tests for all pilots with control groups"

**5 - Innovating**:
- Use case discovery continuous; machine learning applied to problem identification
- ROI dynamic; models updated as new data arrives; value realization tracked continuously
- Portfolio optimization automated; machine learning used to recommend next priorities
- Pilot design adaptive; continuous experimentation and iteration; rapid learning
- Metrics real-time and predictive; leading indicators of success; automatic alerts and optimizations
- *Evidence*: "We use ML to predict which use cases will succeed" / "Metrics update hourly and feed model retraining"

**Scoring Evidence Checklist**:
- How do you select AI/ML use cases? (Formal scoring or informal?)
- Can you articulate the ROI for each major initiative (baseline, lift, costs)?
- How many AI projects are in your pipeline and how are they prioritized?
- What does a pilot look like? (Timeframe, success criteria, adoption metrics)
- How do you measure success? (Model performance alone or business impact too?)

---

#### Dimension 6: Culture & Change Management
**Definition**: Innovation culture, fear/resistance awareness, communication readiness, stakeholder engagement, learning culture

**1 - Ad-hoc**:
- Innovation culture weak; change is feared
- Resistance to AI widespread (job loss fears, trust issues, skill anxiety) but not surfaced or addressed
- Communication ad-hoc; AI benefits not clearly articulated
- Stakeholder engagement reactive; affected teams learn late
- Learning culture weak; training is optional and not valued
- *Evidence*: "People worry AI will replace their jobs" / "We don't talk much about AI unless management brings it up"

**2 - Managed**:
- Innovation encouraged but inconsistently; some teams embrace change, others skeptical
- Resistance awareness emerging; some fear/anxiety heard but not systematically addressed
- Communication happening; quarterly town halls on AI; some FAQs and resource centers
- Early stakeholder engagement with champions; late involvement of affected users
- Learning available; online courses, but participation low; no budget for conferences
- *Evidence*: "We have some innovation pilots" / "People are curious but skeptical about AI"

**3 - Standardized**:
- Innovation culture active; experimentation expected; safe-to-fail frameworks
- Resistance mapping done for major initiatives; concerns documented and addressed
- Communication plan standard: vision, benefits, timeline, skill requirements, role changes clearly stated
- Stakeholder engagement early; working groups form for major initiatives; affected users participate in design
- Learning culture emerging; annual training budget per employee; internal communities of practice
- Change management support: dedicated roles, training, clear ownership
- *Evidence*: "We run regular hackathons and innovation sprints" / "We have a communication plan and FAQ for each major AI initiative"

**4 - Optimized**:
- Innovation culture strong; risk-taking normalized; failure is learning opportunity
- Resistance understood deeply through surveys and interviews; proactive mitigation (role expansion, retraining, career paths)
- Communication multilayered: exec messaging, team updates, 1:1 conversations; feedback loops built in
- Stakeholder engagement continuous; steering committees form early; user research and testing integrated
- Learning culture embedded; career development plans include AI/ML skills; mentorship and peer learning active
- Change management integrated with project delivery; dedicated change managers for large initiatives
- *Evidence*: "We celebrate experiments that fail" / "We've reskilled 20% of the workforce for AI roles"

**5 - Innovating**:
- Innovation mindset pervasive; continuous experimentation; failure not just tolerated but leveraged
- Resistance prevention through culture building; teams proactively develop new skills; career ladders built
- Communication transparent and two-way; employees co-create vision and roadmap
- Stakeholder engagement participatory; affected teams design solutions alongside AI/ML experts
- Learning ecosystem comprehensive; internal academy, external partnerships, research projects; continuous skill building
- Change management predictive; culture shifts anticipated and designed for; organizational structure evolves with strategy
- *Evidence*: "Employees drive half the AI use case ideas" / "We have internal AI research projects"

**Scoring Evidence Checklist**:
- How are new ideas and innovations encouraged or discouraged in your organization?
- Are people worried about job security due to AI? How are those concerns being addressed?
- How do employees learn about major AI initiatives and changes coming?
- How involved are affected teams in designing AI solutions before rollout?
- Is there budget and time for learning and skill development in AI/ML?

---

### Phase 3: Gap Analysis (Analyze)

For each dimension, compare current state (Phase 2) to required state for their priority use cases and business goals.

**Gap Analysis Framework**:
1. **Define Target Maturity**: For each use case (e.g., "predictive churn model"), what maturity level is required?
   - Data-heavy personalization: Data Readiness 4+, Use Case Readiness 4+
   - Regulatory compliance (healthcare ML): Strategy & Governance 4+
   - Customer-facing recommendation engine: Culture 3+, Organizational Capability 3+

2. **Calculate Gaps**: Where current maturity < required, define the gap
   - Example: Data Readiness 2 → 4 required (gap of 2 levels)
   - Example: Culture & Change Management 2 → 3 required (gap of 1 level)

3. **Dependency Analysis**: Which gaps must be addressed before others?
   - Data governance (Dimension 1) enables technical infrastructure (Dimension 2)
   - Organizational capability (Dimension 3) enables governance (Dimension 4)
   - Strategy & governance (Dimension 4) informs use case prioritization (Dimension 5)

4. **Risk Register**: For each significant gap, identify:
   - What could go wrong if we skip this?
   - Timeline to close the gap
   - Cost and resource requirements
   - Dependencies and blockers

---

### Phase 4: Roadmap Design (Plan)

Create a phased roadmap with sequenced recommendations.

**Roadmap Structure**:

**Quick Wins (0-3 months)**
- High impact, low effort initiatives that build momentum and demonstrate progress
- Examples: Establish data governance committee, hire first ML engineer, launch AI literacy program, audit compliance readiness
- Builds confidence and funds later initiatives

**Foundation Building (3-9 months)**
- Address critical gaps in data, infrastructure, or organizational capability
- Examples: Implement data cataloging, establish MLOps practices, build initial cross-functional teams, document AI strategy
- These enable larger initiatives

**Scaling Phase (9-18 months)**
- Deploy multiple use cases in parallel; operationalize governance; embed AI in business processes
- Examples: Production ML systems, expanded team, automated compliance checks, advanced analytics platform
- Return on investment begins

**Optimization Phase (18+ months)**
- Continuous improvement; advanced capabilities; organizational transformation
- Examples: Real-time ML, edge deployment, research partnerships, customer-facing AI products
- Competitive advantage solidified

**Recommendations by Dimension**:
- **Data Readiness**: Implement data cataloging → data governance policy → data quality platform → federated data architecture
- **Technical Infrastructure**: Cloud modernization → containerization and APIs → MLOps platform → edge/real-time capabilities
- **Organizational Capability**: Hire core ML team → build cross-functional squads → establish centers of excellence → embed AI in every team
- **Strategy & Governance**: Write AI strategy → responsible AI framework → compliance policies → automated governance
- **Use Case Readiness**: Document use cases and prioritize → run pilots → scale successful pilots → continuous use case discovery
- **Culture & Change Management**: Launch AI literacy program → establish communities of practice → reskill and rehire → transform organizational culture

---

### Phase 5: Implementation Planning (Execute)

Create detailed implementation plan with timelines, budgets, resource needs, and success metrics.

**Implementation Plan Components**:

1. **Timeline**: Quarters/milestones with clear start/end dates and deliverables
2. **Budget**: Cost ranges for each phase (personnel, tools, training, consulting)
3. **Resource Plan**: Headcount and skills needed (data engineers, ML engineers, data scientists, product managers, change managers)
4. **Success Metrics**: How will we know the roadmap is working? (adoption rates, time-to-value, quality improvements, employee engagement)
5. **Review Checkpoints**: When will we assess progress and adjust? (monthly, quarterly, semi-annually)
6. **Risk Mitigation**: For each major risk from the risk register, define how it will be managed
7. **Sponsorship & Governance**: Who owns each phase? Who makes decisions? Escalation paths

---

## Full_AI_Readiness_Protocol

The skill implements a 5-phase planning protocol embedded in the prompt that will be invoked by the agent:

```
PHASE 1: ORGANIZATION CONTEXT & GOALS
├─ Gather industry, company size, tech stack
├─ Understand AI aspirations and drivers
├─ Document constraints (budget, regulatory, risk tolerance)
└─ Output: Context narrative + structured data

PHASE 2: CURRENT STATE ASSESSMENT
├─ Score Data Readiness (1-5) with evidence
├─ Score Technical Infrastructure (1-5) with evidence
├─ Score Organizational Capability (1-5) with evidence
├─ Score Strategy & Governance (1-5) with evidence
├─ Score Use Case Readiness (1-5) with evidence
├─ Score Culture & Change Management (1-5) with evidence
└─ Output: Maturity Scorecard + spider diagram data

PHASE 3: GAP ANALYSIS
├─ Define target maturity for each dimension
├─ Calculate gaps (current vs target)
├─ Analyze dependencies
├─ Build risk register
└─ Output: Gap summary + risk register

PHASE 4: ROADMAP DESIGN
├─ Quick Wins (0-3 months)
├─ Foundation Building (3-9 months)
├─ Scaling Phase (9-18 months)
├─ Optimization Phase (18+ months)
└─ Output: Sequenced recommendations by dimension

PHASE 5: IMPLEMENTATION PLANNING
├─ Timeline with milestones
├─ Budget estimates (personnel, tools, consulting)
├─ Resource plan (headcount, skills, hiring)
├─ Success metrics and review checkpoints
├─ Risk mitigation strategies
└─ Output: Detailed implementation roadmap
```

---

## Tool_Usage

This skill is **read-only and planning-focused**. It does not:
- Modify documents or code
- Execute changes to systems
- Make purchasing decisions or vendor selections
- Commit budget or resources

It **does**:
- Conduct interviews and assessments
- Analyze organizational documents (tech stack, org charts, strategic plans)
- Synthesize input into structured recommendations
- Output detailed roadmaps ready for executive review and decision-making

**Ideal workflow**:
1. Use this skill to assess readiness and create roadmap
2. Use **stakeholder-report-writer** to tailor output for board, C-suite, or technical teams
3. Use **proposal-critic** to validate AI proposals against readiness findings
4. Use **change-management-designer** to operationalize the roadmap

---

## Examples

### Example 1: Mid-Market SaaS Company (Series B)

**Organization Profile**:
- 80 employees, $15M ARR, 5-year-old SaaS platform
- Current tech stack: Node.js/React frontend, PostgreSQL database, basic analytics
- Industry: HR technology (recruiting/onboarding)

**AI Aspirations**:
- Build resume screening and candidate matching features (core product differentiation)
- Reduce customer support volume through smart ticketing and routing
- Predictive analytics for customer churn and upsell opportunities

**Assessment Results** (from Phase 2):
```
Data Readiness                    : 2/5 (Managed)
  - PostgreSQL is robust but no data warehouse
  - No data governance; analytics team manually builds reports

Technical Infrastructure          : 2/5 (Managed)
  - AWS-based but no containerization or MLOps
  - APIs exist but not comprehensive; integrations are custom

Organizational Capability         : 1/5 (Ad-hoc)
  - No dedicated data/ML team; VP Engineering manages analytics part-time
  - Single analyst; no cross-functional collaboration structure

Strategy & Governance             : 1/5 (Ad-hoc)
  - No formal AI strategy
  - Fairness/bias not discussed; compliance aware but reactive

Use Case Readiness                : 2/5 (Managed)
  - Use cases identified but not formally prioritized
  - ROI guessed for resume screening feature

Culture & Change Management       : 2/5 (Managed)
  - Engineering team is innovative; product team skeptical
  - No formal communication about AI plans
```

**Gap Analysis for Resume Screening Use Case**:
- Target: Data 3, Technical 3, Capability 3, Governance 2, Use Case 3, Culture 2
- Gaps: Data (+1), Technical (+1), Capability (+2), Governance (+1), Use Case (+1)

**Roadmap Excerpt**:
```
Quick Wins (0-3 months):
  - Hire first ML engineer (part-time contractor → full-time)
  - Build basic data pipeline from Postgres to Redshift
  - Document AI strategy and responsible AI principles

Foundation (3-9 months):
  - Implement data governance (data catalog, naming standards)
  - Build resume screening MVP using existing candidate data
  - Create cross-functional product-data-ML team

Scaling (9-18 months):
  - Deploy resume screening to production; A/B test with customers
  - Build support ticket routing ML model in parallel
  - Expand ML team; establish data engineering role
```

---

### Example 2: Enterprise Healthcare Organization

**Organization Profile**:
- 500+ employees, healthcare provider, 3 hospital systems
- Current tech stack: Legacy EHR system, multiple data silos, limited cloud use
- Regulatory environment: HIPAA, state licensing requirements

**AI Aspirations**:
- Predictive ICU admissions (identify high-risk patients early)
- Clinical decision support (drug interaction alerts, diagnosis suggestions)
- Administrative ML (claims processing, billing optimization)

**Assessment Results** (Phase 2):
```
Data Readiness                    : 2/5 (Managed)
  - Data scattered across EHR, pharmacy, lab systems
  - No centralized patient data repository
  - Data quality issues common; limited governance

Technical Infrastructure          : 1/5 (Ad-hoc)
  - On-premises infrastructure; limited cloud
  - No APIs; system integrations are batch files
  - Security and privacy basics in place; encryption partial

Organizational Capability         : 2/5 (Managed)
  - One bioinformaticist; no data engineering or ML team
  - Clinical staff and IT don't collaborate on requirements

Strategy & Governance             : 2/5 (Managed)
  - AI strategy not formal; regulatory compliance is focus
  - Fairness in medicine discussed informally
  - Risk management exists (medical errors) but not AI-specific

Use Case Readiness                : 2/5 (Managed)
  - Multiple use cases identified; ROI unclear
  - No prioritization; clinical leadership wants everything

Culture & Change Management       : 2/5 (Managed)
  - Clinicians fear automation will replace judgment
  - Resistance to change is cultural; training is minimal
```

**Gap Analysis for ICU Admissions Prediction**:
- Target: Data 4, Technical 3, Capability 3, Governance 4 (regulatory), Use Case 3, Culture 3
- Gaps: All dimensions have gaps (+2 to +3)
- Unique risks: Patient privacy, model bias in healthcare, regulatory approval before deployment

**Roadmap Excerpt**:
```
Quick Wins (0-3 months):
  - Form clinical-IT steering committee
  - Conduct bias/fairness audit on historical ICU data
  - Document AI governance and responsible AI principles for healthcare
  - Hire clinical informatics consultant

Foundation (3-9 months):
  - Establish Health Information Exchange (HIE); begin data consolidation
  - Launch AI literacy program for clinical staff (focus on explainability and trust)
  - Build robust data governance with patient privacy as foundation
  - Develop regulatory compliance and explainability requirements

Scaling (9-18 months):
  - Deploy ICU prediction model with clinical review workflow
  - Conduct fairness validation across patient populations
  - Pilot administrative ML models
  - Expand clinical informatics and data engineering teams
```

---

## Notes

- **Assessment is not one-time**: Organizational readiness evolves. Re-assess annually or when major strategic changes occur.
- **Maturity levels are relative**: A score of 2 for a healthcare org might be acceptable; same score for a tech company might be a critical gap.
- **Dependencies matter**: Trying to scale ML models (Dimension 2) without data governance (Dimension 1) typically fails. The roadmap sequence honors these dependencies.
- **Culture is hardest to change**: Technical capability can be hired or built in 6-12 months. Culture and change management require 18-24+ months.
- **Governance is not optional**: Any regulated industry (healthcare, finance, legal) requires strong governance before scaling. Strategy & Governance should never be < 3 for production systems.
- **Use case selection drives everything**: Pick the right first use case and momentum builds. Pick wrong and the AI initiative loses credibility.
- **Budget varies widely**: A mid-market SaaS company might spend $500K-$1M in Year 1 (team + tools). An enterprise might spend $2-5M. Healthcare and finance often spend more due to compliance and integration complexity.
- **Timeline is realistically 18-24 months** from strategy to scaled operations. Anything faster typically sacrifices governance or quality.

---

## Related Resources

- **AI/ML Maturity Models**: NIST AI Risk Management Framework, SEI CMMI for ML, Gartner AI Maturity Model
- **Responsible AI Frameworks**: Partnership on AI Responsible AI Practices, IEEE Ethically Aligned Design
- **MLOps References**: ML Model Ops Manifesto, Google's Rules of ML, MLOps.community
- **Change Management**: Prosci ADKAR Model, Kotter's 8-Step Process, McKinsey Change Management Framework
- **Data Governance**: DAMA Data Management Body of Knowledge, Gartner Data Governance
