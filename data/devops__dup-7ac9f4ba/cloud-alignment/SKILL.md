---
name: cloud-alignment
description: Align with cloud architecture frameworks (Microsoft CAF, AWS Well-Architected). Check alignment with pillars, identify gaps.
allowed-tools: Read, Glob, Grep, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Cloud Alignment

## When to Use This Skill

Use this skill when you need to:

- Check alignment with Microsoft Cloud Adoption Framework (CAF)
- Validate against AWS Well-Architected Framework pillars
- Identify cloud architecture gaps
- Get cloud-specific best practice recommendations

**Keywords:** cloud adoption framework, caf, well-architected, azure, aws, landing zone, governance, security pillar, reliability, cost optimization, sustainability

## Microsoft Cloud Adoption Framework (CAF)

CAF provides comprehensive guidance for Azure cloud adoption through 7 methodologies:

### CAF Methodologies

| # | Methodology | Purpose | Key Activities |
| --- | --- | --- | --- |
| 1 | **Strategy** | Define business justification | Motivations, outcomes, business case |
| 2 | **Plan** | Create adoption plan | Digital estate, skills, timeline |
| 3 | **Ready** | Prepare environment | Landing zones, governance baseline |
| 4 | **Adopt** | Migrate/innovate workloads | Migration waves, modernization |
| 5 | **Govern** | Manage cloud governance | Policies, compliance, cost management |
| 6 | **Secure** | Implement security | Zero trust, identity, data protection |
| 7 | **Manage** | Operate cloud estate | Monitoring, optimization, resilience |

### CAF Alignment Checklist

#### Strategy

- [ ] Cloud motivations documented
- [ ] Business outcomes defined
- [ ] Financial considerations addressed
- [ ] Technical considerations documented

#### Plan

- [ ] Digital estate assessed
- [ ] Skills readiness evaluated
- [ ] Cloud adoption plan created
- [ ] Azure readiness confirmed

#### Ready

- [ ] Landing zone deployed
- [ ] Governance baseline established
- [ ] Network topology defined
- [ ] Identity management configured

#### Adopt

- [ ] Workload assessment complete
- [ ] Migration/modernization approach selected
- [ ] Testing and validation plan
- [ ] Cutover plan documented

#### Govern

- [ ] Governance policies defined
- [ ] Cost management implemented
- [ ] Compliance requirements mapped
- [ ] Security baselines established

#### Secure

- [ ] Identity and access management
- [ ] Network security configured
- [ ] Data protection implemented
- [ ] Threat protection enabled

#### Manage

- [ ] Monitoring configured
- [ ] Backup and recovery tested
- [ ] Operations procedures documented
- [ ] Optimization practices established

### MCP Integration

For current CAF documentation, use the microsoft-learn MCP server:

```text
mcp__microsoft-learn__microsoft_docs_search: "cloud adoption framework [topic]"
mcp__microsoft-learn__microsoft_docs_fetch: [specific URL]
```

**MCP Server Requirement**: This skill uses `mcp__microsoft-learn__*` tools for fetching current Microsoft documentation. If the microsoft-learn MCP server is not configured:

1. **Check availability**: The skill's `allowed-tools` includes MCP tools - if unavailable, queries will fail
2. **Fallback approach**: Use `WebSearch` or `WebFetch` to access Microsoft Learn documentation directly at `https://learn.microsoft.com/azure/cloud-adoption-framework/`
3. **Offline reference**: The `references/caf-pillars.md` file contains static CAF reference content

---

## AWS Well-Architected Framework

The Well-Architected Framework provides guidance through 6 pillars:

### Well-Architected Pillars

| Pillar | Focus | Key Questions |
| --- | --- | --- |
| **Operational Excellence** | Run and monitor systems | How do you manage workload and events? |
| **Security** | Protect data and systems | How do you manage identities and permissions? |
| **Reliability** | Recover from failures | How do you manage service failures? |
| **Performance Efficiency** | Use resources efficiently | How do you select appropriate resources? |
| **Cost Optimization** | Avoid unnecessary costs | How do you manage usage and cost? |
| **Sustainability** | Minimize environmental impact | How do you reduce carbon footprint? |

### Well-Architected Alignment Checklist

#### Operational Excellence

- [ ] Operations as code implemented
- [ ] Documentation maintained
- [ ] Small, frequent changes practiced
- [ ] Failure procedures tested
- [ ] Lessons learned captured

#### Security

- [ ] Strong identity foundation
- [ ] Traceability enabled
- [ ] Security at all layers
- [ ] Risk assessment automated
- [ ] Data protected in transit and at rest

#### Reliability

- [ ] Automatic recovery configured
- [ ] Recovery procedures tested
- [ ] Horizontal scaling enabled
- [ ] Capacity planning in place
- [ ] Change management automated

#### Performance Efficiency

- [ ] Right-sized resources
- [ ] Global reach where needed
- [ ] Serverless where appropriate
- [ ] Performance monitoring active
- [ ] Experimentation enabled

#### Cost Optimization

- [ ] Cloud financial management
- [ ] Expenditure awareness
- [ ] Cost-effective resources
- [ ] Demand management
- [ ] Optimization over time

#### Sustainability

- [ ] Region selection for carbon
- [ ] Resource efficiency
- [ ] Data management practices
- [ ] Software efficiency patterns
- [ ] Hardware lifecycle management

---

## Framework Comparison

| Aspect | Microsoft CAF | AWS Well-Architected |
| --- | --- | --- |
| Scope | End-to-end adoption | Workload design |
| Structure | 7 methodologies | 6 pillars |
| Focus | Journey/transformation | Design principles |
| Governance | Strong emphasis | Part of security |
| Sustainability | Part of manage | Dedicated pillar |

### When to Use Which

- **Starting cloud journey:** Microsoft CAF (comprehensive adoption guidance)
- **Designing workloads:** AWS Well-Architected (design review)
- **Both:** Use CAF for strategy/planning, Well-Architected for implementation

---

## Cloud Alignment Analysis

### Output Structure

```markdown
# Cloud Alignment Assessment: [System Name]

**Date**: YYYY-MM-DD
**Framework**: [CAF | Well-Architected | Both]
**Cloud Provider**: [Azure | AWS | Multi-cloud]

## Executive Summary
[High-level alignment status]

## Alignment Score

| Area | Status | Score |
| --- | --- | --- |
| [Pillar/Methodology 1] | [Aligned/Partial/Gap] | X/10 |
| [Pillar/Methodology 2] | [Aligned/Partial/Gap] | X/10 |
| ... | ... | ... |

## Detailed Assessment

### [Area 1]
**Status**: [Aligned | Partial | Gap]
**Current state**: [Description]
**Recommendation**: [Action]
**Priority**: [High | Medium | Low]

## Improvement Roadmap
[Prioritized list of improvements]

## References
[Links to relevant framework documentation]
```

---

## Integration with Other Skills

- **togaf-guidance**: Align CAF methodologies with TOGAF phases
- **gap-analysis**: Use cloud frameworks to identify gaps
- **architecture-documentation**: Document cloud architecture decisions
- **adr-management**: Record cloud platform decisions

## Version History

- **v1.0.0** (2025-12-05): Initial release
  - Microsoft Cloud Adoption Framework (CAF) alignment checklists
  - AWS Well-Architected Framework pillar checklists
  - Framework comparison and guidance
  - MCP integration with fallback documentation

---

## Last Updated

**Date:** 2025-12-05
**Model:** claude-opus-4-5-20251101
