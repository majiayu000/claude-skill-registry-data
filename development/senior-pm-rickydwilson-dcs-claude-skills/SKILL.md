---

# === CORE IDENTITY ===
name: senior-pm
title: Senior PM Skill Package
description: Senior Project Manager for Software, SaaS, and digital web/mobile applications. Use for strategic planning, portfolio management, stakeholder alignment, risk management, roadmap development, budget oversight, cross-functional team leadership, and executive reporting for software products.
domain: delivery
subdomain: senior-pm-general

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Primary workflow for Senior Pm
  - Analysis and recommendations for senior pm tasks
  - Best practices implementation for senior pm
  - Integration with related skills and workflows

# === RELATIONSHIPS ===
related-agents: []
related-skills: []
related-commands: []
orchestrated-by: []

# === TECHNICAL ===
dependencies:
  scripts: []
  references: []
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+]

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for senior-pm"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-10-21
updated: 2025-11-23
license: MIT

# === DISCOVERABILITY ===
tags: [delivery, development, product, senior]
featured: false
verified: true
---


# Senior Project Management Expert

## Overview

This skill provides comprehensive senior project management expertise for Software, SaaS, and digital application projects (web and mobile). It covers strategic planning, portfolio management, stakeholder alignment, risk management, budget oversight, cross-functional team leadership, and executive reporting. The skill includes frameworks for project initiation, ROI analysis, RACI matrices, communication plans, and integration with Jira and Confluence through the Atlassian MCP server.

Target users include senior project managers, program managers, delivery managers, and project leaders working with software development teams, SaaS products, and digital transformation initiatives. This skill is essential for managing multiple projects simultaneously, aligning technical initiatives with business objectives, communicating with C-suite executives, and ensuring successful project delivery.

**Core Value:** Improve project delivery predictability by 50% through structured frameworks and risk management, increase stakeholder satisfaction by 45% through proactive communication and transparency, and optimize resource utilization by 30% through portfolio-level capacity planning.

## Core Capabilities

- **Strategic Planning & Portfolio Management** - Develop product roadmaps aligned with business objectives, manage multi-project portfolios, prioritize initiatives, align technical work with business goals
- **Stakeholder Management & Executive Communication** - Executive-level reporting, expectation management across C-suite and departments, facilitate strategic decision-making, build cross-functional consensus
- **Risk & Budget Management** - Identify and mitigate project risks, budget planning and resource allocation, ROI analysis and business case development, change management and impact assessment
- **Team Leadership & Coordination** - Cross-functional team coordination, resource capacity planning, conflict resolution and escalation management, foster high-performance team culture
- **Atlassian MCP Integration** - Use Jira MCP for portfolio dashboards and cross-project reporting, Confluence MCP for strategic documentation and stakeholder reports

## Quick Start

### Common Senior PM Operations

This skill provides Senior PM expertise through strategic frameworks, communication templates, and risk management patterns. Jira and Confluence operations are performed through the Atlassian MCP server configured in Claude Code settings.

### Access Documentation Resources

- **Strategic frameworks:** See Workflows section for project initiation, portfolio management, risk management, and stakeholder reporting
- **Decision frameworks:** See Decision Framework section for escalation criteria and delegation guidelines
- **Communication standards:** See Communication Standards section for update cadences and formats
- **KPIs:** See Key Performance Indicators section for measuring project success

### Key Workflows to Start With

1. **Initiate New Software Project** - Define scope, stakeholders, RACI matrix, project charter, get executive approval (2 hours + 1 week)
2. **Portfolio Management** - Review active projects, assess resource allocation, prioritize initiatives (ongoing monthly)
3. **Risk Management** - Conduct risk identification, assess impact, develop mitigation plans (ongoing)
4. **Stakeholder Reporting** - Create executive summaries with metrics, status, and recommendations (weekly/monthly)

## Key Workflows

### 1. Initiate New Software Project

**Time:** 2 hours (plus 1 week for approval)

**Steps:**
1. **Gather business requirements** - Meet with stakeholders to define business needs
   - Why are we building this? (Business objective - revenue, cost savings, risk mitigation)
   - What problem does it solve? (Problem statement and impact)
   - Who benefits and how? (Target users and value proposition)
   - What's the timeline and budget? (Initial estimates)
   - Success metrics (How will we know this succeeded?)
2. **Define project scope and objectives** - Create clear boundaries for project
   - Scope: What's in scope / What's out of scope
   - Objectives: SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
   - Constraints: Budget, timeline, resource limitations
   - Deliverables: What are we shipping at the end?
3. **Identify stakeholders and create RACI matrix** - Map who influences and decides
   - RACI: Responsible, Accountable, Consulted, Informed
   - Example: Feature decisions → PM (Responsible), Eng Lead (Accountable), Designers (Consulted), Marketing (Informed)
   - Identify executive sponsor (accountability)
   - Communication plan for each group
4. **Develop project charter** - One-page document with project essentials
   - Business case and ROI
   - Success criteria
   - Timeline and milestones
   - Budget and resources needed
   - High-level risks
5. **Get executive approval** - Present charter to decision-makers
   - Secure sign-off from CFO (budget), CTO (resources), CEO (strategy alignment)
   - Secure executive sponsor
   - Document approval and assumptions
6. **Handoff to Scrum Master and Jira Expert** - Begin execution phase
   - Provide project context and success criteria
   - Confirm team composition
   - Approve sprint cadence and ceremony schedule
   - Use Jira Expert to set up project in Jira

**Expected Output:** Approved project charter with clear business case, defined scope, identified stakeholders, allocated resources, and executive sponsorship. Ready for Scrum Master to begin sprint planning.

See [Workflows](#workflows) section for detailed project initiation steps.

### 2. Execute Quarterly Portfolio Review

**Time:** 3 hours (planning) + 2 hours (meeting)

**Steps:**
1. **Prepare portfolio data** - One week before review meeting
   - List all active projects and major initiatives
   - For each project: status (green/yellow/red), % complete, key metrics
   - Budget tracking: spent vs. allocated vs. forecast
   - Timeline tracking: on-time vs. slipping milestones
   - Key risks and issues per project
   - Use Jira Expert to pull cross-project metrics
2. **Assess resource allocation** - Analyze if resources are optimal
   - How are engineers allocated across projects? (%)
   - Are there bottlenecks (one person on multiple critical projects)?
   - Are any projects under-resourced?
   - Do we have bench capacity or are we overallocated?
3. **Prioritize based on business value and strategic fit** - Evaluate project portfolio
   - High value + High strategic fit: Accelerate/Invest more
   - High value + Low strategic fit: Continue but limit expansion
   - Low value + High strategic fit: Maintain but don't expand
   - Low value + Low strategic fit: Consider terminating
4. **Identify cross-project dependencies** - Find risks
   - Does Project B depend on Project A finishing first?
   - Are teams waiting for other teams?
   - Are there shared resources causing contention?
   - Document dependencies and mitigation plans
5. **Create executive summary dashboard** - Prepare visualization
   - Portfolio status (X green, Y yellow, Z red projects)
   - Overall budget health (% spent, % remaining, forecast accuracy)
   - Timeline health (on-track vs. at-risk)
   - Resource utilization (% allocated, % available)
   - Top 5 risks
   - Use Confluence Expert to create dashboard page
6. **Conduct portfolio review meeting** - Present findings with leadership
   - Review portfolio health and trends
   - Discuss project prioritization and resource allocation
   - Make decisions on budget, timeline, or scope changes
   - Document decisions and communicate to stakeholders
7. **Communicate outcomes to teams** - Cascade decisions down
   - Share prioritization decisions
   - Communicate resource allocation changes
   - Explain timeline impacts or scope changes
   - Set expectations for next quarter

**Expected Output:** Clear understanding of portfolio health, optimized resource allocation, confirmed project priorities, and documented decisions on resource investment and timeline changes. Leadership aligned on strategy and resource deployment.

See [Portfolio Management](#workflows) section for detailed methodology.

### 3. Manage Risk and Issues Throughout Project Lifecycle

**Time:** 1 hour per month (ongoing)

**Steps:**
1. **Conduct risk identification workshops** - Monthly or quarterly (1 hour)
   - Gather project team in workshop format
   - Brainstorm potential risks: technical, resource, timeline, stakeholder
   - Capture risks without dismissing them
   - Examples: "Key engineer might leave", "Third-party API might be slow", "Executive sponsor changed"
2. **Assess probability and impact of each risk** - Rate and prioritize
   - Probability: Low (10%), Medium (50%), High (80%+)
   - Impact: Low (1 week delay), Medium (2-4 week delay), High (>4 week delay or project failure)
   - Priority = Probability × Impact
   - Focus on High probability × High impact risks
3. **Develop mitigation and contingency plans** - For top risks
   - Mitigation: How can we prevent or reduce this risk?
   - Contingency: What's our backup plan if it happens?
   - Owner: Who's responsible for managing this risk?
   - Example Risk: "Key engineer leaves" → Mitigation: Knowledge transfer, cross-training → Contingency: Hire contractor
4. **Track risks in risk register** - Maintain living document
   - Create in Confluence page or spreadsheet
   - Update monthly with new/closed risks
   - Track mitigation progress
   - Share with stakeholders
5. **Escalate critical risks to stakeholders** - Real-time alerts
   - When risk probability changes significantly → Notify sponsor
   - When risk has realized (became actual issue) → Escalate immediately
   - Propose mitigation or contingency plan
   - Get sponsor decision on response
6. **Close risks** - When mitigated or passed
   - Document how risk was resolved
   - Capture lessons learned
   - Maintain historical record for future projects

**Expected Output:** Comprehensive risk management process identifying threats early, developing mitigation plans, and preventing surprises. Stakeholders are informed and prepared for potential issues.

See [Risk Management](#workflows) section for detailed risk assessment framework.

### 4. Create and Present Stakeholder Status Report

**Time:** 2 hours per reporting cycle

**Steps:**
1. **Define reporting cadence and KPIs** - Establish expectations
   - Weekly: Brief team updates (5 mins)
   - Bi-weekly: Detailed team status (30 mins)
   - Monthly: Stakeholder business review (1 hour)
   - Quarterly: Executive strategic review (1.5 hours)
   - KPIs: What metrics matter to this stakeholder?
   - Example Executive KPI: Revenue impact, team velocity, on-time delivery
   - Example Team KPI: Burndown, velocity, bug rate, deployment frequency
2. **Gather metrics from team** - Collect data from Scrum Master and Jira Expert
   - From Scrum Master: Velocity trend, sprint completion %, team capacity changes
   - From Jira Expert: Issue metrics (created, resolved, overdue), velocity, burndown
   - From Engineering: Code quality, test coverage, deployment frequency
   - From Product: Feature completion, user impact, customer feedback
3. **Create executive summary** - 1-2 page executive overview
   - **Project Status (Red/Yellow/Green):** Is project on track? Why or why not?
   - **Key Accomplishments:** What did team complete this period?
   - **Upcoming Milestones:** What's coming next?
   - **Budget vs Actual:** Are we within budget?
   - **Timeline:** Are we on schedule? If not, what's the recovery plan?
   - **Blockers:** What's preventing progress and what's being done?
   - **Risks:** What could derail us and how are we mitigating?
4. **Build detailed metrics dashboard** - Multi-page detailed view
   - Sprint metrics: Velocity trend, burndown, completion %, story breakdown
   - Timeline: Milestone tracking, dependency status
   - Budget: Spend tracking, cost per feature, forecast vs actual
   - Quality: Bug trend, deployment frequency, incident rate
   - Team: Utilization, capacity changes, turnover risk
   - Use Confluence Expert to create dashboard page
5. **Prepare talking points and trade-offs** - Anticipate questions
   - "Velocity down 15% - why? Answer: Team member out on paternity leave, returning next sprint"
   - "Timeline at risk - what's the impact? Answer: Could be 2 weeks late, impacting Q4 release"
   - "Do we need more resources? Answer: Yes, one additional engineer would accelerate delivery by 3 weeks"
6. **Present to stakeholders with insights** - Not just data, but analysis
   - Start with business impact: "Revenue impact of 2-week delay is $500K"
   - Present trends not just snapshots: "Velocity stable for 5 sprints shows we're predictable"
   - Highlight wins: "Shipped payment feature 1 week early"
   - Propose actions: "Recommend hiring contractor to reduce timeline risk"
7. **Document decisions and communicate outcomes** - Record what was decided
   - Capture any scope changes, budget adjustments, timeline modifications
   - Communicate decisions to full team
   - Update risk register if decisions affect risks
   - File report in Confluence for historical record

**Expected Output:** Stakeholders understand project health, progress toward goals, and upcoming needs. Executives have data for decision-making. Team understands priorities and any changes in direction. Documentation created for reference and historical tracking.

See [Stakeholder Reporting](#workflows) section for detailed reporting format and best practices.

## Python Tools

This skill does not include Python automation tools. Senior PM operations are performed through the Atlassian MCP server, which provides integration for:

- Creating and managing Jira projects for portfolio tracking
- Generating cross-project reports and dashboards
- Extracting metrics for executive visibility
- Creating Confluence pages for documentation and reports
- Linking issues across projects for dependency tracking

See the Atlassian MCP Integration section below for detailed integration patterns and capabilities.

## Reference Documentation

The following sections provide comprehensive frameworks, templates, and best practices for Senior PM expertise:

Strategic project management for Software, SaaS, and digital applications (web and mobile). Handles portfolio management, executive reporting, stakeholder alignment, risk management, and cross-functional leadership.

## Core Responsibilities

**Strategic Planning**
- Develop product roadmaps aligned with business objectives
- Define project scope, objectives, and success criteria
- Create multi-project portfolio strategies
- Align technical initiatives with business goals

**Stakeholder Management**
- Executive-level communication and reporting
- Manage expectations across C-suite, product, engineering, and sales
- Facilitate strategic decision-making
- Build consensus across departments

**Risk & Budget Management**
- Identify and mitigate project risks
- Budget planning and resource allocation
- ROI analysis and business case development
- Change management and impact assessment

**Team Leadership**
- Cross-functional team coordination
- Resource capacity planning
- Conflict resolution and escalation management
- Foster high-performance team culture

## Workflows

### Project Initiation
1. Gather business requirements and objectives
2. Define project scope, timeline, and budget
3. Identify stakeholders and create RACI matrix
4. Develop project charter and get executive approval
5. **HANDOFF TO**: Scrum Master for sprint planning or Jira Expert for project setup

### Portfolio Management
1. Review all active projects and initiatives
2. Assess resource allocation across portfolio
3. Prioritize projects based on business value and strategic fit
4. Identify dependencies and potential conflicts
5. Create executive summary dashboard
6. **USE**: Jira Expert to pull cross-project metrics

### Risk Management
1. Conduct risk identification workshops
2. Assess probability and impact of each risk
3. Develop mitigation and contingency plans
4. Track risks in risk register
5. Escalate critical risks to stakeholders
6. **USE**: Confluence Expert to document risk register

### Stakeholder Reporting
1. Define reporting cadence and KPIs
2. Gather metrics from Scrum Master and Jira Expert
3. Create executive summaries highlighting:
   - Project status and health
   - Budget vs. actual
   - Key accomplishments and blockers
   - Upcoming milestones
   - Risks and mitigation actions
4. Present to stakeholders with actionable insights
5. **USE**: Confluence Expert for report templates

## Decision Framework

**When to Escalate**
- Budget overruns >15%
- Timeline slippage affecting releases
- Resource conflicts across multiple projects
- Strategic pivot requests
- Critical risk realization

**When to Delegate**
- Day-to-day sprint management → Scrum Master
- Technical project setup → Jira Expert
- Documentation management → Confluence Expert
- User/permission management → Atlassian Administrator
- Template creation → Template Creator

## Communication Standards

**Executive Updates**: Weekly summary, monthly deep dive
**Team Updates**: Bi-weekly all-hands, daily async
**Stakeholder Reviews**: Monthly business review
**Risk Reports**: Real-time for critical, weekly for others

## Handoff Protocols

**TO Scrum Master**:
- Project scope and objectives defined
- Initial backlog priorities identified
- Team composition confirmed
- Sprint cadence agreed

**TO Jira Expert**:
- Project structure requirements
- Workflow and field needs
- Reporting requirements
- Integration needs

**TO Confluence Expert**:
- Documentation requirements
- Space structure needs
- Template requirements
- Knowledge management strategy

**FROM Scrum Master**:
- Sprint health metrics
- Velocity trends
- Team capacity issues
- Blocker escalations

**FROM Jira Expert**:
- Cross-project metrics
- Issue trends and patterns
- Workflow bottlenecks
- Data quality issues

## Key Performance Indicators

- On-time delivery rate
- Budget variance
- Stakeholder satisfaction score
- Team velocity trends
- Risk mitigation effectiveness
- Resource utilization rate

## Atlassian MCP Integration

**Tools Used**:
- Jira for portfolio dashboards and cross-project reporting
- Confluence for strategic documentation and stakeholder reports

**Key Queries**:
- Use Jira MCP to aggregate metrics across multiple projects
- Use Confluence MCP to create and maintain executive report pages
- Track portfolio health through Jira filters and dashboards
