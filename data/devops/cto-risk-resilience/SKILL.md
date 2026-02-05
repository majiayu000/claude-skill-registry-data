---
name: cto-risk-resilience
description: Expert methodology for identifying, assessing, and mitigating technical and operational risks including security, incidents, compliance, and disaster recovery.
---

# CTO Risk & Resilience Skill

## Purpose

This skill provides a comprehensive framework for managing technical risk and building resilient systems. Use it to conduct risk assessments, plan incident response, achieve compliance certifications, and ensure business continuity.

## When to Use

Trigger this skill when you need to:

- Conduct security risk assessments
- Plan for compliance certifications (SOC 2, ISO 27001, GDPR, HIPAA)
- Design incident response processes and runbooks
- Create disaster recovery and business continuity plans
- Assess vendor and third-party risks
- Define SLAs, SLOs, and SLIs
- Prepare for security audits or penetration testing
- Implement chaos engineering and resilience testing
- Respond to security incidents or breaches

## Core Methodology

Follow this systematic approach to risk and resilience:

### Phase 1: Risk Identification

1. **Categorize Risks**

   **Technical Risks**:

   - System failures and outages
   - Data loss or corruption
   - Performance degradation
   - Scalability limitations
   - Technical debt accumulation

   **Security Risks**:

   - Unauthorized access
   - Data breaches
   - DDoS attacks
   - Malware and ransomware
   - Supply chain vulnerabilities

   **Operational Risks**:

   - Human error
   - Process failures
   - Knowledge gaps (bus factor)
   - Inadequate monitoring
   - Poor change management

   **Compliance Risks**:

   - Regulatory violations (GDPR, CCPA, HIPAA)
   - Certification failures (SOC 2, ISO 27001)
   - Contract breaches (SLA violations)
   - Audit findings

   **Business Risks**:

   - Vendor dependencies
   - Technology obsolescence
   - Team attrition
   - Budget constraints

2. **Conduct Risk Assessment**

   Use `references/frameworks/risk-assessment-matrix.md` to systematically identify and score risks.

   For each risk:

   - Describe the risk scenario
   - Assess probability (High/Medium/Low)
   - Assess impact (Critical/High/Medium/Low)
   - Calculate risk score
   - Identify existing controls
   - Define mitigation strategies

---

### Phase 2: Risk Prioritization

1. **Create Risk Matrix**

   ```
   High Impact (Critical)
        |
        |  [Low Priority]    |  [Medium Priority]  |  [HIGH PRIORITY]
        |  Low Prob          |  Medium Prob        |  High Prob
        |  High Impact       |  High Impact        |  High Impact
     (5)|___________________|_____________________|____________________
        |                    |                     |
        |  [Low Priority]    |  [Medium Priority]  |  [High Priority]
        |  Low Prob          |  Medium Prob        |  High Prob
        |  Medium Impact     |  Medium Impact      |  Medium Impact
     (3)|___________________|_____________________|____________________
        |                    |                     |
        |  [Very Low]        |  [Low Priority]     |  [Medium Priority]
        |  Low Prob          |  Medium Prob        |  High Prob
        |  Low Impact        |  Low Impact         |  Low Impact
   Low (1)|___________________|_____________________|____________________
   Impact
           Low (1)            Medium (3)            High (5)
                           Probability
   ```

2. **Priority Levels**

   **Critical (Priority 1)**: Address immediately

   - High probability + High impact
   - Example: Known security vulnerability in production

   **High (Priority 2)**: Address within 30 days

   - Medium probability + High impact, OR High probability + Medium impact
   - Example: Single point of failure in critical system

   **Medium (Priority 3)**: Address within 90 days

   - Low probability + High impact, OR Medium probability + Medium impact
   - Example: Lack of disaster recovery testing

   **Low (Priority 4)**: Monitor and address opportunistically

   - Any low impact scenarios
   - Example: Minor technical debt in non-critical systems

Use `references/templates/risk-register.md` to maintain ongoing risk inventory.

---

### Phase 3: Security & Compliance

#### Security Framework

Implement security controls across multiple layers:

1. **Preventive Controls** (Stop threats before they happen)

   - Access control (MFA, RBAC, least privilege)
   - Network security (firewalls, VPNs, segmentation)
   - Encryption (at rest and in transit)
   - Secure coding practices
   - Security awareness training

2. **Detective Controls** (Identify threats quickly)

   - Logging and monitoring
   - Intrusion detection systems (IDS)
   - Security information and event management (SIEM)
   - Vulnerability scanning
   - Penetration testing

3. **Responsive Controls** (React to incidents)
   - Incident response plan
   - Automated threat response
   - Backup and recovery procedures
   - Communication protocols

Use `references/frameworks/security-controls-framework.md` for comprehensive checklist.

---

#### Compliance Roadmaps

**SOC 2 Type II Certification**

Timeline: 12-18 months (9 months preparation + 3-6 months audit period + 3 months report)

Use `references/templates/soc2-roadmap.md` for detailed plan:

**Phases**:

1. Gap assessment (Month 1-2)
2. Control implementation (Month 3-9)
3. Evidence collection period (Month 10-15)
4. Audit (Month 16-18)

**Key Areas**:

- Security: Access controls, encryption, monitoring
- Availability: Uptime, incident response, disaster recovery
- Confidentiality: Data protection, privacy controls
- Processing Integrity: Data accuracy, error handling
- Privacy: GDPR/CCPA compliance (if applicable)

---

**ISO 27001 Certification**

Timeline: 12-24 months

Use `references/templates/iso27001-roadmap.md`:

**Phases**:

1. Gap analysis (Month 1-3)
2. ISMS implementation (Month 4-15)
3. Internal audit (Month 16-18)
4. Certification audit (Month 19-24)

**Key Requirements**:

- 114 controls across 14 domains
- Risk assessment methodology
- Information security policies
- Employee training and awareness
- Continuous improvement process

---

**GDPR / CCPA Compliance**

Timeline: 6-12 months

Use `references/templates/data-privacy-compliance.md`:

**Key Areas**:

- Data inventory and mapping
- Consent management
- Data subject rights (access, deletion, portability)
- Data processing agreements
- Privacy policy and notices
- Breach notification procedures

---

### Phase 4: Incident Response

Create structured incident response capability:

#### Incident Response Framework

**1. Preparation**

- Define incident severity levels
- Create on-call rotation
- Develop runbooks for common scenarios
- Set up communication channels
- Train team on procedures

**2. Detection**

- Monitoring and alerting
- User reports
- Security scanning
- Automated anomaly detection

**3. Triage**

- Assess severity (P0/P1/P2/P3)
- Assign incident commander
- Assemble response team
- Begin communication

**4. Investigation**

- Gather data and logs
- Identify root cause
- Assess blast radius
- Document timeline

**5. Containment**

- Stop the bleeding
- Isolate affected systems
- Prevent further damage
- Implement temporary fixes

**6. Resolution**

- Deploy permanent fix
- Verify resolution
- Monitor for recurrence
- Update systems

**7. Post-Mortem**

- Blameless retrospective
- Document what happened
- Identify improvements
- Create action items

Use `references/templates/incident-response-playbook.md` for detailed procedures.

---

#### Incident Severity Levels

| Level             | Definition                                              | Response Time     | Escalation                     |
| ----------------- | ------------------------------------------------------- | ----------------- | ------------------------------ |
| **P0 - Critical** | Complete service outage, data breach, security incident | Immediate         | All-hands, exec team notified  |
| **P1 - High**     | Major feature broken, significant degradation           | <15 minutes       | On-call team, manager notified |
| **P2 - Medium**   | Partial functionality impaired, workaround exists       | <2 hours          | On-call team                   |
| **P3 - Low**      | Minor issue, minimal customer impact                    | Next business day | Normal ticket queue            |

---

#### On-Call Best Practices

**Structure**:

- Primary and secondary on-call rotation
- 1-week rotations (avoid burnout)
- Compensate with time off or pay
- Maximum 2-3 incidents per week on average

**Tools**:

- PagerDuty, Opsgenie, or similar
- Automated escalation
- Mobile app for notifications
- Integration with monitoring systems

**Health Metrics**:

- On-call incidents per week
- Time spent on-call
- Sleep disruption frequency
- On-call satisfaction score

Use `references/frameworks/on-call-framework.md` for detailed guidance.

---

### Phase 5: Business Continuity

Ensure critical business functions can continue during disruptions:

#### Disaster Recovery Planning

**Recovery Objectives**:

**RTO (Recovery Time Objective)**: How long can we be down?

- Critical systems: 1 hour
- Important systems: 4 hours
- Standard systems: 24 hours

**RPO (Recovery Point Objective)**: How much data can we lose?

- Financial data: 0 (real-time replication)
- Customer data: 15 minutes (frequent backups)
- Analytics data: 24 hours (daily backups)

**Disaster Scenarios**:

1. Single server failure
2. Availability zone outage
3. Regional outage
4. Complete cloud provider outage
5. Ransomware attack
6. Accidental data deletion
7. Key personnel unavailable

For each scenario:

- Detection method
- Recovery procedure
- Responsible team
- Expected RTO/RPO
- Testing frequency

Use `references/templates/disaster-recovery-plan.md` for comprehensive planning.

---

#### Business Continuity Testing

**Regular Drills**:

- Quarterly: Tabletop exercises (discuss scenarios)
- Bi-annually: Simulated incidents (practice procedures)
- Annually: Full disaster recovery test (actual failover)

**Game Days**:

- Chaos engineering exercises
- Intentional failure injection
- Test recovery procedures
- Identify weaknesses

**Documentation**:

- Keep runbooks updated
- Document lessons learned
- Update procedures based on findings
- Share knowledge across team

---

### Phase 6: Resilience Engineering

Build systems that gracefully handle failures:

#### Resilience Patterns

**1. Circuit Breakers**

- Detect failing services
- Prevent cascade failures
- Automatic recovery attempts
- Fallback behavior

**2. Retry with Exponential Backoff**

- Handle transient failures
- Avoid overwhelming systems
- Progressive delay between attempts
- Maximum retry limits

**3. Timeout and Bulkheads**

- Prevent resource exhaustion
- Isolate failures
- Limit blast radius
- Protect critical paths

**4. Graceful Degradation**

- Continue with reduced functionality
- Non-critical features can fail
- User experience maintained
- Clear communication to users

**5. Rate Limiting and Load Shedding**

- Prevent overload
- Protect system stability
- Prioritize critical requests
- Fair resource allocation

Use `references/frameworks/resilience-patterns.md` for implementation guidance.

---

#### Service Level Objectives (SLOs)

Define reliability targets:

**SLI (Service Level Indicator)**: What we measure

- Availability: % of successful requests
- Latency: % of requests under threshold
- Throughput: Requests per second handled
- Error rate: % of failed requests

**SLO (Service Level Objective)**: Our target

- Availability: 99.9% (43 minutes downtime/month allowed)
- Latency: 95% of requests < 200ms
- Error rate: < 0.1%

**SLA (Service Level Agreement)**: Promise to customers

- Usually more lenient than internal SLO
- Has financial consequences if missed
- Example: 99.5% uptime guarantee with credits

**Error Budget**:

- Amount of allowed unreliability
- 99.9% SLO = 0.1% error budget = 43 minutes/month
- Can "spend" budget on releases, changes, experiments
- When exhausted, focus shifts to reliability

Use `references/templates/slo-definition.md` for framework.

---

## Key Principles

- **Prevention Over Reaction**: Build security and resilience from the start
- **Defense in Depth**: Multiple layers of security controls
- **Assume Breach**: Plan for when (not if) defenses fail
- **Blameless Culture**: Learn from incidents without blame
- **Continuous Improvement**: Regular testing and refinement
- **Clear Communication**: Transparent about risks and incidents

## Bundled Resources

**Frameworks** (`references/frameworks/`):

- `risk-assessment-matrix.md` - Systematic risk identification and scoring
- `security-controls-framework.md` - Comprehensive security checklist
- `on-call-framework.md` - Sustainable on-call practices
- `resilience-patterns.md` - Architecture patterns for resilience
- `chaos-engineering.md` - Controlled failure testing

**Templates** (`references/templates/`):

- `risk-register.md` - Ongoing risk tracking
- `incident-response-playbook.md` - Step-by-step incident procedures
- `soc2-roadmap.md` - SOC 2 certification plan
- `iso27001-roadmap.md` - ISO 27001 certification plan
- `data-privacy-compliance.md` - GDPR/CCPA compliance guide
- `disaster-recovery-plan.md` - DR procedures and testing
- `slo-definition.md` - Service level objective framework
- `security-audit-checklist.md` - Pre-audit preparation
- `post-mortem-template.md` - Incident analysis format

**Examples** (`references/examples/`):

- Real post-mortems from major incidents (anonymized)
- Security audit results and remediation
- Compliance certification timelines
- DR testing scenarios and results

## Usage Patterns

**Example 1**: User says "We need to get SOC 2 certified for enterprise sales"

→ Load `references/templates/soc2-roadmap.md`
→ Conduct gap assessment against SOC 2 requirements
→ Create 12-18 month roadmap with phases
→ Identify control implementations needed
→ Estimate costs (audit fees, tools, consulting)
→ Assign ownership and timeline
→ Provide monthly checklist for evidence collection

---

**Example 2**: User says "Create incident response process for my 30-person team"

→ Load `references/templates/incident-response-playbook.md`
→ Define severity levels (P0-P3) with examples
→ Design on-call rotation structure
→ Create runbooks for common scenarios
→ Set up communication channels (Slack, status page)
→ Define escalation paths
→ Schedule incident response training

---

**Example 3**: User says "Conduct security risk assessment for Series B due diligence"

→ Load `references/frameworks/risk-assessment-matrix.md`
→ Inventory all systems and data
→ Identify risks across security, compliance, operational
→ Score by probability and impact
→ Document existing controls
→ Create risk mitigation roadmap
→ Prepare executive summary for investors

---

**Example 4**: User says "We had a major outage, help with post-mortem"

→ Load `references/templates/post-mortem-template.md`
→ Document incident timeline
→ Identify root cause(s)
→ Analyze what went well and poorly
→ Create blameless narrative
→ Generate action items with owners
→ Share with team and stakeholders
→ Track action item completion

---

## Risk Management by Company Stage

### Early Stage Startup (Pre-PMF)

**Focus**: Security basics, avoid catastrophic risks

**Priorities**:

1. Basic security (encryption, access control)
2. Data backup and recovery
3. Privacy compliance basics
4. Simple incident response

**Avoid**: Over-investing in compliance certifications too early

---

### Growth Stage (Post-PMF, Scaling)

**Focus**: Scalability, reliability, security hardening

**Priorities**:

1. SOC 2 preparation (if selling B2B)
2. Comprehensive monitoring and alerting
3. Incident response process
4. On-call rotation structure
5. DR planning and testing

**Investment**: 10-15% of engineering time on resilience

---

### Scale Stage (Enterprise)

**Focus**: Compliance, resilience, enterprise security

**Priorities**:

1. Multiple compliance certifications (SOC 2, ISO 27001)
2. Advanced security (SIEM, threat detection)
3. Chaos engineering and resilience testing
4. Comprehensive BC/DR
5. Security team and CISO

**Investment**: 20-25% of engineering time on reliability/security

---

## Warning Signs

| Indicator                           | Risk                                | Action                                       |
| ----------------------------------- | ----------------------------------- | -------------------------------------------- |
| No monitoring on production         | High - can't detect issues          | Immediate: Implement basic monitoring        |
| No backup/DR tested in 6+ months    | High - recovery may fail            | Test DR procedures this quarter              |
| Single person knows critical system | High - bus factor = 1               | Document and cross-train immediately         |
| Increasing incident frequency       | Medium-High - system degrading      | Root cause analysis, resilience improvements |
| Failed security scan findings       | High - vulnerable to attack         | Remediate critical/high findings in 30 days  |
| Compliance deadline <6 months       | High - may not certify in time      | Accelerate roadmap, consider consultant      |
| On-call team burned out             | Medium - quality and retention risk | Reduce incident load, improve tooling        |

---

## Communication Templates

### For Board/Investors

**Security & Risk Update**

**Status**: 🟢 Secure and compliant

**Key Metrics**:

- System uptime: 99.87% (target: 99.9%)
- Security incidents: 0 critical, 2 low (resolved)
- Compliance: SOC 2 on track for Q3 certification

**Top Risks & Mitigations**:

1. Single cloud provider dependency → Implementing multi-region DR
2. Growing on-call burden → Hiring SRE, improving automation
3. Compliance timeline tight → Weekly checkpoint, external consultant engaged

**Investment Request**: $150K for penetration testing and SOC 2 audit

---

### For Engineering Team

**Incident Review - Service Outage Feb 15**

**What Happened**: Database connection pool exhaustion caused 45-minute outage

**Timeline**:

- 2:15 PM: Increased load from marketing campaign
- 2:22 PM: First alerts fired
- 2:25 PM: Team paged, investigation started
- 2:40 PM: Root cause identified
- 3:00 PM: Service restored

**What Went Well**:

- ✅ Alerts fired within 7 minutes
- ✅ Team assembled quickly
- ✅ Clear communication to customers

**What We'll Improve**:

- ⚠️ Auto-scaling for connection pool
- ⚠️ Load testing before campaigns
- ⚠️ Better runbook documentation

**Action Items**: [See detailed list]

No blame - systems fail, we learn and improve.

---

## Writing Style

All outputs should be:

- **Risk-Aware**: Identify and communicate risks clearly
- **Action-Oriented**: Focus on concrete mitigation steps
- **Balanced**: Realistic about risk vs. cost/effort
- **Empathetic**: Blameless culture, learning mindset
- **Transparent**: Honest about gaps and limitations

---

**Version**: 1.0.0
**Philosophy**: Prevent where possible, detect quickly, respond effectively, learn continuously
