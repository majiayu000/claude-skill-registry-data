---
name: hipaa-compliance
description: HIPAA compliance planning for healthcare applications including PHI handling, safeguards, BAAs, and risk assessments
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# HIPAA Compliance Planning

Comprehensive guidance for Health Insurance Portability and Accountability Act compliance before development begins.

## When to Use This Skill

- Building systems that handle Protected Health Information (PHI)
- Designing healthcare applications, patient portals, or medical devices
- Integrating with healthcare providers, payers, or clearinghouses
- Establishing Business Associate relationships
- Conducting HIPAA security risk assessments

## HIPAA Fundamentals

### Key Entities

| Entity Type | Definition | Requirements |
|-------------|------------|--------------|
| **Covered Entity** | Healthcare providers, health plans, clearinghouses | Full HIPAA compliance |
| **Business Associate** | Entities handling PHI on behalf of covered entities | BAA + compliance |
| **Subcontractor** | Business associates of business associates | BAA chain |

### The Three Rules

```text
1. Privacy Rule - Who can access PHI and how it can be used/disclosed
2. Security Rule - How to protect electronic PHI (ePHI)
3. Breach Notification Rule - How to respond to unauthorized disclosures
```

## Protected Health Information (PHI)

### 18 HIPAA Identifiers

When combined with health information, these become PHI:

```text
1.  Names
2.  Geographic data smaller than state
3.  Dates (except year) related to individual
4.  Phone numbers
5.  Fax numbers
6.  Email addresses
7.  Social Security numbers
8.  Medical record numbers
9.  Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photographs
18. Any other unique identifying number/code
```

### De-identification Methods

**Safe Harbor Method:**
Remove all 18 identifiers + no actual knowledge data can identify individual

**Expert Determination:**
Qualified statistician certifies re-identification risk is very small

```csharp
// De-identification validation
public class PhiDeidentifier
{
    private static readonly HashSet<string> HipaaIdentifiers = new()
    {
        "Name", "Address", "City", "State", "Zip", "DateOfBirth",
        "Phone", "Fax", "Email", "SSN", "MRN", "HealthPlanId",
        "AccountNumber", "LicenseNumber", "VIN", "DeviceSerial",
        "URL", "IPAddress", "Biometric", "Photo", "UniqueId"
    };

    public DeidentificationResult Validate(DataSet dataset)
    {
        var violations = new List<string>();

        foreach (var column in dataset.Columns)
        {
            if (HipaaIdentifiers.Contains(column.Name, StringComparer.OrdinalIgnoreCase))
            {
                violations.Add($"Column '{column.Name}' is a HIPAA identifier");
            }

            // Check for date patterns (except year-only)
            if (column.DataType == typeof(DateTime) &&
                !column.Name.EndsWith("Year", StringComparison.OrdinalIgnoreCase))
            {
                violations.Add($"Column '{column.Name}' contains full dates");
            }

            // Check for zip codes more specific than first 3 digits
            if (column.Name.Contains("Zip", StringComparison.OrdinalIgnoreCase))
            {
                var hasFullZips = dataset.Rows
                    .Any(r => r[column.Name]?.ToString()?.Length > 3);
                if (hasFullZips)
                {
                    violations.Add($"Column '{column.Name}' contains full zip codes");
                }
            }
        }

        return new DeidentificationResult
        {
            IsDeidentified = violations.Count == 0,
            Violations = violations
        };
    }
}
```

## Security Rule Safeguards

### Administrative Safeguards

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| Security Officer | Designated responsible person | Role assignment |
| Risk Analysis | Identify vulnerabilities | Annual assessment |
| Risk Management | Mitigate identified risks | Remediation plan |
| Workforce Training | Security awareness | Training program |
| Access Authorization | Role-based access | IAM policies |
| Incident Response | Breach procedures | IR playbook |
| Contingency Plan | Disaster recovery | DR/BC plan |
| BAA Management | Third-party compliance | Contract tracking |

### Physical Safeguards

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| Facility Access | Limit physical access | Badge systems, cameras |
| Workstation Use | Policies for use | Clean desk, screen locks |
| Workstation Security | Physical protection | Cable locks, privacy screens |
| Device Controls | Media handling | Encryption, disposal procedures |

### Technical Safeguards

| Requirement | Description | Implementation |
|-------------|-------------|----------------|
| Access Control | Unique user ID | SSO, MFA |
| Audit Controls | Activity logging | SIEM, log retention |
| Integrity Controls | Prevent unauthorized alteration | Checksums, versioning |
| Transmission Security | Protect ePHI in transit | TLS 1.2+, VPN |
| Encryption | Render ePHI unusable | AES-256 |
| Auto-Logoff | Session management | Idle timeout |
| Authentication | Verify user identity | MFA, strong passwords |

### .NET Implementation Patterns

```csharp
// HIPAA-compliant audit logging
public class HipaaAuditLogger : IAuditLogger
{
    private readonly IHipaaAuditRepository _repository;
    private readonly TimeProvider _timeProvider;

    public async Task LogPhiAccess(PhiAccessEvent accessEvent, CancellationToken ct)
    {
        var auditRecord = new HipaaAuditRecord
        {
            EventId = Guid.NewGuid(),
            Timestamp = _timeProvider.GetUtcNow(),
            UserId = accessEvent.UserId,
            UserRole = accessEvent.UserRole,
            PatientId = accessEvent.PatientId,
            ResourceType = accessEvent.ResourceType,
            ResourceId = accessEvent.ResourceId,
            Action = accessEvent.Action, // Read, Create, Update, Delete
            Reason = accessEvent.Reason, // Treatment, Payment, Operations
            SourceIp = accessEvent.SourceIp,
            UserAgent = accessEvent.UserAgent,
            Success = accessEvent.Success
        };

        await _repository.WriteAuditRecord(auditRecord, ct);
    }
}

public record PhiAccessEvent
{
    public required string UserId { get; init; }
    public required string UserRole { get; init; }
    public required string PatientId { get; init; }
    public required string ResourceType { get; init; }
    public required string ResourceId { get; init; }
    public required string Action { get; init; }
    public required string Reason { get; init; }
    public required string SourceIp { get; init; }
    public required string UserAgent { get; init; }
    public required bool Success { get; init; }
}
```

```csharp
// Minimum Necessary access control
public class MinimumNecessaryFilter
{
    private readonly IRolePermissionProvider _permissions;

    public T ApplyFilter<T>(T phiRecord, string userRole, string purpose) where T : class
    {
        var allowedFields = _permissions.GetAllowedFields(
            typeof(T).Name,
            userRole,
            purpose);

        // Create filtered view with only allowed fields
        var filtered = Activator.CreateInstance<T>();
        foreach (var field in allowedFields)
        {
            var prop = typeof(T).GetProperty(field);
            if (prop != null)
            {
                prop.SetValue(filtered, prop.GetValue(phiRecord));
            }
        }

        return filtered;
    }
}

// Role-based field access configuration
public class RoleFieldPermissions
{
    public Dictionary<string, RoleAccess> Roles { get; set; } = new();
}

public class RoleAccess
{
    public List<string> Treatment { get; set; } = new(); // Fields accessible for treatment
    public List<string> Payment { get; set; } = new();   // Fields accessible for payment
    public List<string> Operations { get; set; } = new(); // Fields for healthcare operations
}
```

## Business Associate Agreements

### BAA Requirements

Every BAA must include:

```markdown
## Required BAA Provisions

1. Permitted Uses and Disclosures
   - Specify exactly what BA can do with PHI
   - Limit to contract performance or as required by law

2. Safeguard Requirements
   - Implement appropriate safeguards
   - Prevent unauthorized use/disclosure

3. Reporting Obligations
   - Report any security incidents
   - Report breaches of unsecured PHI

4. Subcontractor Requirements
   - Flow-down provisions to subcontractors
   - Obtain BAAs from subcontractors

5. Individual Rights
   - Make PHI available for access requests
   - Make amendments when required
   - Provide accounting of disclosures

6. Compliance Verification
   - Make practices available for audit
   - Books and records accessible

7. Termination Provisions
   - Return or destroy PHI on termination
   - Extend protections if return impossible

8. Breach Liability
   - Responsibility for breach costs
   - Notification obligations
```

### BAA Tracking System

```csharp
public class BaaManagement
{
    public record BusinessAssociate
    {
        public required Guid Id { get; init; }
        public required string Name { get; init; }
        public required string ServiceDescription { get; init; }
        public required BaaStatus Status { get; init; }
        public required DateTimeOffset EffectiveDate { get; init; }
        public DateTimeOffset? ExpirationDate { get; init; }
        public required string[] PhiCategories { get; init; }
        public required string[] PermittedUses { get; init; }
        public required ContactInfo SecurityContact { get; init; }
        public required DateTimeOffset LastSecurityAssessment { get; init; }
        public DateTimeOffset? NextAssessmentDue { get; init; }
    }

    public enum BaaStatus
    {
        Pending,
        Active,
        UnderReview,
        Expired,
        Terminated
    }
}
```

## HIPAA Risk Assessment

### Assessment Framework

```markdown
## Risk Assessment Process

### 1. Scope Definition
- Systems that create, receive, maintain, or transmit ePHI
- All locations and devices
- Include cloud services and vendors

### 2. Data Flow Mapping
- Where is ePHI created?
- How does it move through systems?
- Where is it stored?
- Who has access?
- How is it transmitted externally?

### 3. Threat Identification
- Natural threats (fire, flood, earthquake)
- Human threats (hackers, insiders, social engineering)
- Environmental threats (power failure, HVAC)
- Technical threats (malware, system failure)

### 4. Vulnerability Assessment
- Technical vulnerabilities (unpatched systems)
- Administrative gaps (training, policies)
- Physical weaknesses (access control)

### 5. Risk Calculation
Risk = Likelihood × Impact

| Likelihood | Value | Description |
|------------|-------|-------------|
| Very Low | 1 | Highly unlikely |
| Low | 2 | Possible but unlikely |
| Medium | 3 | Could happen |
| High | 4 | Likely to occur |
| Very High | 5 | Almost certain |

| Impact | Value | Description |
|--------|-------|-------------|
| Minimal | 1 | Little to no effect |
| Low | 2 | Minor inconvenience |
| Medium | 3 | Significant disruption |
| High | 4 | Major breach/harm |
| Critical | 5 | Catastrophic impact |

### 6. Risk Mitigation
For each high/critical risk:
- Control options (avoid, mitigate, transfer, accept)
- Implementation timeline
- Responsible party
- Verification method
```

### Risk Register Template

```yaml
Risk ID: R-001
Title: Unencrypted ePHI on mobile devices
Threat: Device theft/loss
Vulnerability: Lack of device encryption
Asset: Mobile devices with EHR access
Likelihood: High (4)
Impact: Critical (5)
Risk Score: 20 (Critical)
Current Controls:
  - Password policy
  - Remote wipe capability
Proposed Controls:
  - Mandatory device encryption
  - MDM solution
  - No local PHI storage
Residual Risk: Low (4)
Owner: IT Security
Target Date: 2025-03-01
Status: In Progress
```

## Breach Notification Requirements

### Breach Definition

An impermissible use or disclosure that compromises the security or privacy of PHI.

**Exceptions (Not Breaches):**

1. Unintentional access by workforce member in good faith
2. Inadvertent disclosure between authorized persons
3. Good faith belief recipient couldn't retain information

### Breach Risk Assessment

```text
Factors to consider:
1. Nature and extent of PHI involved
2. Unauthorized person who used/received PHI
3. Whether PHI was actually acquired or viewed
4. Extent to which risk has been mitigated
```

### Notification Requirements

| Notification Type | Deadline | Method |
|-------------------|----------|--------|
| **Individuals** | 60 days from discovery | Written mail (or email if consented) |
| **HHS** | 60 days (500+) or annually (<500) | HHS breach portal |
| **Media** | 60 days (500+ in state) | Prominent media outlets |

### Breach Response Workflow

```csharp
public class BreachResponseWorkflow
{
    public async Task HandlePotentialBreach(BreachReport report, CancellationToken ct)
    {
        // Step 1: Contain and document
        var incident = await CreateIncident(report, ct);
        await ContainBreach(incident, ct);

        // Step 2: Conduct risk assessment
        var assessment = await ConductRiskAssessment(incident, ct);

        if (assessment.IsReportableBreach)
        {
            // Step 3: Prepare notifications
            var notifications = await PrepareNotifications(incident, assessment, ct);

            // Step 4: Submit to HHS if 500+ individuals
            if (assessment.AffectedCount >= 500)
            {
                await SubmitToHhs(incident, notifications, ct);
                await NotifyMedia(incident, ct);
            }
            else
            {
                await QueueForAnnualReport(incident, ct);
            }

            // Step 5: Notify individuals within 60 days
            await ScheduleIndividualNotifications(notifications, ct);
        }

        // Step 6: Document everything
        await CompleteIncidentDocumentation(incident, assessment, ct);
    }
}
```

## HIPAA Compliance Checklist

### Before Development

- [ ] HIPAA training completed for all team members
- [ ] BAAs in place with all vendors handling PHI
- [ ] Risk assessment conducted
- [ ] Security policies documented
- [ ] Incident response plan created
- [ ] Data flow diagrams with PHI marked

### Architecture & Design

- [ ] Encryption at rest (AES-256)
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Access control architecture defined
- [ ] Audit logging requirements specified
- [ ] Minimum necessary principle applied
- [ ] Session management (auto-logoff)
- [ ] Authentication requirements (MFA for ePHI access)

### Development

- [ ] PHI never in logs or error messages
- [ ] Secure coding practices followed
- [ ] Audit trails implemented
- [ ] Access controls enforced at all layers
- [ ] Input validation prevents injection
- [ ] No hardcoded credentials

### Testing & Deployment

- [ ] Penetration testing completed
- [ ] Vulnerability assessment performed
- [ ] Access control testing
- [ ] Audit log review
- [ ] Backup/restore testing
- [ ] DR testing

## Cross-References

- **GDPR**: Additional requirements for EU patients
- **Security Frameworks**: `security-frameworks` for control mappings
- **Data Classification**: `data-classification` for PHI vs non-PHI
- **AI Governance**: `ai-governance` for AI in healthcare

## Resources

- [HHS HIPAA Home](https://www.hhs.gov/hipaa/index.html)
- [NIST HIPAA Security Rule Guidance](https://csrc.nist.gov/publications/detail/sp/800-66/rev-2/final)
- [HHS Breach Portal](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf)
