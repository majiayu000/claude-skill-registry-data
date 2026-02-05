---
name: security-frameworks
description: Security framework alignment including ISO 27001, SOC 2, NIST CSF 2.0, and CIS Controls mapping
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Security Frameworks Planning

Comprehensive guidance for security framework alignment and control mapping before development begins.

## When to Use This Skill

- Preparing for ISO 27001 certification
- Planning SOC 2 Type I or Type II audits
- Implementing NIST Cybersecurity Framework 2.0
- Mapping CIS Controls to your environment
- Creating cross-framework control mappings

## Framework Comparison

### When to Use Which Framework

| Framework | Best For | Certification? | Geography |
|-----------|----------|---------------|-----------|
| **ISO 27001** | Enterprise ISMS, international recognition | Yes (3rd party) | Global |
| **SOC 2** | SaaS/Cloud providers, customer trust | Yes (CPA firm) | Primarily US |
| **NIST CSF** | Risk management, federal requirements | No | US-focused |
| **CIS Controls** | Tactical implementation, prioritization | No | Global |

### Framework Relationships

```text
                    ┌─────────────────┐
                    │   Regulations   │
                    │ (GDPR, HIPAA)   │
                    └────────┬────────┘
                             │ drives
                    ┌────────▼────────┐
                    │   Frameworks    │
                    │(ISO, NIST, CIS) │
                    └────────┬────────┘
                             │ implements
                    ┌────────▼────────┐
                    │    Controls     │
                    │ (specific tech) │
                    └────────┬────────┘
                             │ evidenced by
                    ┌────────▼────────┐
                    │    Audits       │
                    │ (SOC 2, ISO)    │
                    └─────────────────┘
```

## ISO 27001:2022

### Structure Overview

```text
Clauses 4-10: Management System Requirements
├── 4. Context of the organization
├── 5. Leadership
├── 6. Planning
├── 7. Support
├── 8. Operation
├── 9. Performance evaluation
└── 10. Improvement

Annex A: 93 Controls in 4 Themes
├── A.5 Organizational controls (37)
├── A.6 People controls (8)
├── A.7 Physical controls (14)
└── A.8 Technological controls (34)
```

### Key Controls for Development

| Control | Title | Implementation |
|---------|-------|----------------|
| A.5.1 | Policies for information security | Document security policies |
| A.5.15 | Access control | RBAC, least privilege |
| A.5.23 | Information security for cloud services | Cloud security controls |
| A.8.4 | Access to source code | Git access, code review |
| A.8.8 | Management of technical vulnerabilities | Vulnerability scanning |
| A.8.9 | Configuration management | IaC, hardening |
| A.8.25 | Secure development lifecycle | SSDLC |
| A.8.28 | Secure coding | OWASP, static analysis |
| A.8.29 | Security testing | DAST, penetration testing |
| A.8.31 | Separation of environments | Dev/Test/Prod isolation |

### ISMS Implementation Approach

```csharp
// Control implementation tracking
public class IsmsControlTracker
{
    public record ControlStatus
    {
        public required string ControlId { get; init; } // e.g., "A.8.28"
        public required string ControlTitle { get; init; }
        public required ImplementationStatus Status { get; init; }
        public required string Owner { get; init; }
        public required List<string> Evidence { get; init; }
        public required DateTimeOffset LastReviewDate { get; init; }
        public required DateTimeOffset NextReviewDate { get; init; }
        public string? GapDescription { get; init; }
        public string? RemediationPlan { get; init; }
    }

    public enum ImplementationStatus
    {
        NotApplicable,
        NotImplemented,
        PartiallyImplemented,
        FullyImplemented
    }

    public GapAnalysisReport GenerateGapAnalysis(
        IEnumerable<ControlStatus> controls)
    {
        var gaps = controls
            .Where(c => c.Status != ImplementationStatus.FullyImplemented
                     && c.Status != ImplementationStatus.NotApplicable)
            .OrderBy(c => c.ControlId);

        return new GapAnalysisReport
        {
            TotalControls = controls.Count(),
            FullyImplemented = controls.Count(c =>
                c.Status == ImplementationStatus.FullyImplemented),
            PartiallyImplemented = controls.Count(c =>
                c.Status == ImplementationStatus.PartiallyImplemented),
            NotImplemented = controls.Count(c =>
                c.Status == ImplementationStatus.NotImplemented),
            NotApplicable = controls.Count(c =>
                c.Status == ImplementationStatus.NotApplicable),
            Gaps = gaps.ToList()
        };
    }
}
```

## SOC 2

### Trust Services Criteria (TSC)

| Category | Description | Key Criteria |
|----------|-------------|--------------|
| **Security** (Required) | System protected against unauthorized access | CC6.x |
| **Availability** | System available for operation | A1.x |
| **Processing Integrity** | System processing is complete, accurate | PI1.x |
| **Confidentiality** | Confidential information protected | C1.x |
| **Privacy** | Personal information protected | P1.x-P8.x |

### Common Criteria (Security)

```text
CC1 - Control Environment
CC2 - Communication and Information
CC3 - Risk Assessment
CC4 - Monitoring Activities
CC5 - Control Activities
CC6 - Logical and Physical Access Controls
CC7 - System Operations
CC8 - Change Management
CC9 - Risk Mitigation
```

### SOC 2 Control Examples

```markdown
## CC6.1 - Logical Access Security

### Control Description
The entity implements logical access security software, infrastructure,
and architectures over protected information assets to protect them
from security events to meet the entity's objectives.

### Implementation
- Authentication via Azure AD with MFA required
- RBAC with least privilege principle
- Service accounts with managed identities
- API access via OAuth 2.0 tokens

### Evidence
- Azure AD configuration export
- Role assignment documentation
- Access review reports (quarterly)
- MFA enforcement policy
```

### Type I vs Type II

| Aspect | Type I | Type II |
|--------|--------|---------|
| **Scope** | Point in time | Period of time (6-12 months) |
| **Focus** | Design of controls | Design AND operating effectiveness |
| **Evidence** | Policies, configurations | Logs, samples, testing |
| **Use Case** | First audit, quick report | Customer assurance, ongoing |

## NIST Cybersecurity Framework 2.0

### Core Functions

```text
┌────────────────────────────────────────────────────┐
│                      GOVERN                         │
│   Organizational context, strategy, oversight       │
├────────────┬────────────┬────────────┬─────────────┤
│  IDENTIFY  │  PROTECT   │   DETECT   │   RESPOND   │
│  Assets &  │ Safeguards │ Continuous │  Incident   │
│   Risks    │            │ Monitoring │  Response   │
├────────────┴────────────┴────────────┴─────────────┤
│                      RECOVER                        │
│             Resilience & Recovery                   │
└────────────────────────────────────────────────────┘
```

### Function Breakdown

| Function | Category | Key Activities |
|----------|----------|---------------|
| **GOVERN** | Organizational Context | Establish risk management strategy |
| | Risk Management Strategy | Define risk tolerance |
| | Roles & Responsibilities | Assign accountability |
| | Policy | Document policies |
| | Oversight | Board/executive involvement |
| **IDENTIFY** | Asset Management | Inventory systems and data |
| | Risk Assessment | Identify and assess risks |
| | Improvement | Continuous improvement |
| **PROTECT** | Identity Management | Access control, authentication |
| | Awareness & Training | Security training |
| | Data Security | Encryption, classification |
| | Platform Security | Secure configurations |
| | Technology Infrastructure | Secure architecture |
| **DETECT** | Continuous Monitoring | Security monitoring |
| | Adverse Event Analysis | Threat detection |
| **RESPOND** | Incident Management | Incident response |
| | Incident Analysis | Root cause analysis |
| | Incident Response | Containment, eradication |
| | Incident Mitigation | Limit impact |
| **RECOVER** | Incident Recovery | Restore operations |
| | Improvements | Post-incident learning |

### Implementation Tiers

| Tier | Name | Description |
|------|------|-------------|
| 1 | Partial | Ad hoc, reactive |
| 2 | Risk Informed | Risk aware but informal |
| 3 | Repeatable | Formal policies, consistent |
| 4 | Adaptive | Continuous improvement, predictive |

## CIS Controls v8

### Control Categories

```text
Implementation Groups (IG):
IG1 - Essential Cyber Hygiene (56 safeguards)
IG2 - IG1 + Enhanced (130 safeguards)
IG3 - IG1 + IG2 + Advanced (153 safeguards)
```

### 18 Control Areas

| # | Control | IG1 | Key Safeguards |
|---|---------|-----|----------------|
| 1 | Inventory of Enterprise Assets | ✓ | Asset discovery, inventory |
| 2 | Inventory of Software Assets | ✓ | Software inventory |
| 3 | Data Protection | ✓ | Classification, encryption |
| 4 | Secure Configuration | ✓ | Hardening, baselines |
| 5 | Account Management | ✓ | Centralized auth, MFA |
| 6 | Access Control Management | ✓ | Least privilege, RBAC |
| 7 | Continuous Vulnerability Management | ✓ | Scanning, patching |
| 8 | Audit Log Management | ✓ | Centralized logging |
| 9 | Email and Web Browser Protections | ✓ | Filtering, sandboxing |
| 10 | Malware Defenses | ✓ | Anti-malware, EDR |
| 11 | Data Recovery | ✓ | Backups, testing |
| 12 | Network Infrastructure Management | | Segmentation, hardening |
| 13 | Network Monitoring and Defense | | IDS/IPS, NDR |
| 14 | Security Awareness and Skills Training | ✓ | Training program |
| 15 | Service Provider Management | | Vendor assessment |
| 16 | Application Software Security | | SSDLC, testing |
| 17 | Incident Response Management | | IR plan, testing |
| 18 | Penetration Testing | | Annual pen test |

### Priority Implementation

```markdown
## CIS IG1 Priority Controls

### Start Here (Quick Wins)
1. **Control 1.1**: Maintain accurate asset inventory
2. **Control 4.1**: Establish secure configuration process
3. **Control 5.1**: Establish centralized account management
4. **Control 6.1**: Establish access granting process

### Next Priority
5. **Control 7.1**: Establish vulnerability management process
6. **Control 8.1**: Establish audit logging
7. **Control 11.1**: Establish data recovery practices
8. **Control 14.1**: Establish security awareness program

### Then
9. **Control 3.1**: Establish data management process
10. **Control 10.1**: Deploy anti-malware
```

## Cross-Framework Mapping

### Control Mapping Matrix

| Capability | ISO 27001 | SOC 2 TSC | NIST CSF 2.0 | CIS v8 |
|------------|-----------|-----------|--------------|--------|
| Access Control | A.5.15, A.8.2-8.5 | CC6.1-6.3 | PR.AA | 5, 6 |
| Asset Management | A.5.9-5.11 | CC6.1 | ID.AM | 1, 2 |
| Encryption | A.8.24 | CC6.1, CC6.7 | PR.DS | 3.6, 3.9 |
| Logging | A.8.15 | CC7.2 | DE.AE | 8 |
| Vulnerability Mgmt | A.8.8 | CC7.1 | ID.RA | 7 |
| Incident Response | A.5.24-5.28 | CC7.4, CC7.5 | RS | 17 |
| Change Management | A.8.32 | CC8.1 | PR.IP | 4.2 |
| Secure Development | A.8.25-8.31 | CC8.1 | PR.IP | 16 |

### .NET Control Implementation Examples

```csharp
// Access Control implementation (multiple frameworks)
// ISO 27001 A.5.15 / SOC 2 CC6.1 / NIST PR.AA / CIS 5,6

public class AccessControlService
{
    private readonly IAuthorizationService _authService;
    private readonly IAuditLogger _auditLogger;

    public async Task<AuthorizationResult> Authorize(
        ClaimsPrincipal user,
        string resource,
        string action,
        CancellationToken ct)
    {
        // Log access attempt (CIS 8 / NIST DE.AE)
        var accessAttempt = new AccessAttempt
        {
            UserId = user.GetUserId(),
            Resource = resource,
            Action = action,
            Timestamp = DateTimeOffset.UtcNow
        };

        var result = await _authService.AuthorizeAsync(user, resource, action);

        accessAttempt.Success = result.Succeeded;
        accessAttempt.Reason = result.Failure?.FailureReasons
            .FirstOrDefault()?.Message;

        await _auditLogger.Log(accessAttempt, ct);

        return result;
    }
}

// Secure configuration (ISO A.8.9 / NIST PR.IP / CIS 4)
public class SecureConfigurationValidator
{
    public ValidationResult ValidateConfiguration(IConfiguration config)
    {
        var issues = new List<ConfigurationIssue>();

        // Check for secure defaults
        if (config["AllowHttp"] == "true")
        {
            issues.Add(new ConfigurationIssue
            {
                Setting = "AllowHttp",
                Issue = "HTTP should be disabled in production",
                Severity = Severity.High,
                Remediation = "Set AllowHttp=false"
            });
        }

        // Check TLS configuration
        var tlsVersion = config["MinTlsVersion"];
        if (tlsVersion != "1.2" && tlsVersion != "1.3")
        {
            issues.Add(new ConfigurationIssue
            {
                Setting = "MinTlsVersion",
                Issue = "TLS 1.2 or higher required",
                Severity = Severity.Critical,
                Remediation = "Set MinTlsVersion=1.2"
            });
        }

        return new ValidationResult { Issues = issues };
    }
}
```

## Framework Selection Guide

### Decision Tree

```text
What is your primary driver?

├─ Customer requirement for audit report?
│   ├─ US customers → SOC 2
│   └─ International customers → ISO 27001
│
├─ Regulatory requirement?
│   ├─ US Federal → NIST CSF + FedRAMP
│   └─ Healthcare → HIPAA (use NIST CSF)
│
├─ Starting security program?
│   └─ CIS Controls IG1 (practical starting point)
│
└─ Enterprise-wide ISMS?
    └─ ISO 27001 (comprehensive management system)
```

## Security Framework Checklist

### Pre-Assessment

- [ ] Identify applicable frameworks
- [ ] Determine scope boundaries
- [ ] Inventory systems in scope
- [ ] Document current controls
- [ ] Conduct gap analysis

### Control Implementation

- [ ] Prioritize gaps by risk
- [ ] Create remediation roadmap
- [ ] Implement missing controls
- [ ] Document evidence
- [ ] Test control effectiveness

### Audit Preparation

- [ ] Collect evidence artifacts
- [ ] Prepare control narratives
- [ ] Test samples (Type II)
- [ ] Address known gaps
- [ ] Brief stakeholders

## Cross-References

- **Data Privacy**: `gdpr-compliance`, `hipaa-compliance` for data protection
- **PCI**: `pci-dss-compliance` for payment security
- **AI**: `ai-governance` for AI-specific controls

## Resources

- [ISO 27001:2022](https://www.iso.org/standard/27001)
- [AICPA SOC 2](https://www.aicpa.org/soc2)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
- [CIS Controls v8](https://www.cisecurity.org/controls)
