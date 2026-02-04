---
name: data-classification
description: Data classification framework including sensitivity levels, handling requirements, labeling, and data lifecycle management
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Data Classification

Comprehensive guidance for data classification, handling requirements, and data lifecycle management.

## When to Use This Skill

- Establishing data classification policies
- Defining handling requirements for different data types
- Designing data protection controls by classification
- Implementing data labeling and tagging
- Creating data retention and disposal procedures

## Classification Framework

### Standard Sensitivity Levels

| Level | Description | Examples | Impact of Breach |
|-------|-------------|----------|------------------|
| **Public** | Intentionally public | Marketing, published docs | None |
| **Internal** | General business use | Policies, org charts | Minimal |
| **Confidential** | Business sensitive | Financial reports, contracts | Moderate |
| **Restricted** | Highly sensitive | PII, PHI, trade secrets | Severe |
| **Top Secret** | Critical/regulated | Encryption keys, M&A data | Catastrophic |

### Visual Labeling

```text
┌─────────────────────────────────────────┐
│ █ PUBLIC                                │  Green
├─────────────────────────────────────────┤
│ █ INTERNAL - For Internal Use Only     │  Blue
├─────────────────────────────────────────┤
│ █ CONFIDENTIAL - Authorized Only       │  Yellow
├─────────────────────────────────────────┤
│ █ RESTRICTED - Need-to-Know Only       │  Orange
├─────────────────────────────────────────┤
│ █ TOP SECRET - Strictly Controlled     │  Red
└─────────────────────────────────────────┘
```

## Handling Requirements Matrix

### By Classification Level

| Requirement | Public | Internal | Confidential | Restricted |
|-------------|--------|----------|--------------|------------|
| **Access Control** | None | Authentication | RBAC | Need-to-know + MFA |
| **Encryption at Rest** | Optional | Recommended | Required | Required + HSM |
| **Encryption in Transit** | HTTPS | TLS 1.2+ | TLS 1.2+ | TLS 1.3 + mTLS |
| **Backup** | Standard | Standard | Encrypted | Encrypted + geo-separate |
| **Sharing External** | Allowed | Approval | NDA required | Prohibited |
| **Cloud Storage** | Any | Approved cloud | Approved + encryption | On-premises or approved |
| **Print** | Allowed | Allowed | Watermarked | Prohibited/tracked |
| **Retention** | As needed | 3 years | 7 years | 7 years + legal hold |
| **Disposal** | Standard delete | Secure delete | Cryptographic erase | Physical destruction |

### Data Flow Controls

```text
Restricted Data Flow:
┌──────────────┐     Encrypted      ┌──────────────┐
│   Source     │ ───────────────▶  │ Destination  │
│   System     │                    │   System     │
└──────────────┘                    └──────────────┘
       │                                   │
       ▼                                   ▼
   Audit Log                           Audit Log
       │                                   │
       ▼                                   ▼
  ┌────────────────────────────────────────────┐
  │              SIEM / Monitoring              │
  └────────────────────────────────────────────┘
```

## Classification Implementation

### .NET Data Annotation Approach

```csharp
// Classification attributes
[AttributeUsage(AttributeTargets.Property | AttributeTargets.Class)]
public class DataClassificationAttribute : Attribute
{
    public DataClassification Level { get; }
    public string? DataCategory { get; set; }
    public string? RetentionPolicy { get; set; }
    public string[] RequiredRoles { get; set; } = Array.Empty<string>();

    public DataClassificationAttribute(DataClassification level)
    {
        Level = level;
    }
}

public enum DataClassification
{
    Public = 0,
    Internal = 1,
    Confidential = 2,
    Restricted = 3,
    TopSecret = 4
}

// Usage on domain models
public class Customer
{
    public Guid Id { get; set; }

    [DataClassification(DataClassification.Internal)]
    public string Name { get; set; } = string.Empty;

    [DataClassification(DataClassification.Restricted,
        DataCategory = "PII",
        RequiredRoles = new[] { "CustomerAdmin", "Support" })]
    public string Email { get; set; } = string.Empty;

    [DataClassification(DataClassification.Restricted,
        DataCategory = "PII",
        RetentionPolicy = "7years")]
    public string SocialSecurityNumber { get; set; } = string.Empty;

    [DataClassification(DataClassification.Confidential,
        DataCategory = "Financial")]
    public decimal CreditLimit { get; set; }
}
```

### Classification-Based Access Control

```csharp
public class ClassificationAuthorizationHandler
    : AuthorizationHandler<DataAccessRequirement, object>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        DataAccessRequirement requirement,
        object resource)
    {
        var classificationAttr = resource.GetType()
            .GetCustomAttribute<DataClassificationAttribute>();

        if (classificationAttr == null)
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        var userClearance = GetUserClearanceLevel(context.User);

        // User clearance must meet or exceed data classification
        if ((int)userClearance >= (int)classificationAttr.Level)
        {
            // Check role requirements if specified
            if (classificationAttr.RequiredRoles.Length > 0)
            {
                var hasRequiredRole = classificationAttr.RequiredRoles
                    .Any(r => context.User.IsInRole(r));

                if (hasRequiredRole)
                {
                    context.Succeed(requirement);
                }
            }
            else
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}
```

### Field-Level Encryption

```csharp
public class ClassificationBasedEncryption
{
    private readonly IEncryptionService _encryptionService;

    public async Task<T> ProtectData<T>(T data, CancellationToken ct) where T : class
    {
        var properties = typeof(T).GetProperties()
            .Where(p => p.GetCustomAttribute<DataClassificationAttribute>() != null);

        foreach (var prop in properties)
        {
            var attr = prop.GetCustomAttribute<DataClassificationAttribute>()!;

            if (attr.Level >= DataClassification.Confidential)
            {
                var value = prop.GetValue(data) as string;
                if (!string.IsNullOrEmpty(value))
                {
                    var encrypted = await _encryptionService.Encrypt(value, ct);
                    prop.SetValue(data, encrypted);
                }
            }
        }

        return data;
    }
}
```

## Data Discovery and Inventory

### Automated Classification

```csharp
public class DataDiscoveryService
{
    private readonly IRegexPatternMatcher _patternMatcher;

    public ClassificationSuggestion AnalyzeContent(string content)
    {
        var detections = new List<DataTypeDetection>();

        // Check for PII patterns
        if (_patternMatcher.ContainsPattern(content, PiiPatterns.SocialSecurityNumber))
            detections.Add(new DataTypeDetection("SSN", DataClassification.Restricted));

        if (_patternMatcher.ContainsPattern(content, PiiPatterns.CreditCard))
            detections.Add(new DataTypeDetection("Credit Card", DataClassification.Restricted));

        if (_patternMatcher.ContainsPattern(content, PiiPatterns.Email))
            detections.Add(new DataTypeDetection("Email", DataClassification.Confidential));

        if (_patternMatcher.ContainsPattern(content, PiiPatterns.PhoneNumber))
            detections.Add(new DataTypeDetection("Phone", DataClassification.Confidential));

        // Check for financial patterns
        if (_patternMatcher.ContainsPattern(content, FinancialPatterns.BankAccount))
            detections.Add(new DataTypeDetection("Bank Account", DataClassification.Restricted));

        // Determine highest classification
        var suggestedLevel = detections.Any()
            ? detections.Max(d => d.Classification)
            : DataClassification.Internal;

        return new ClassificationSuggestion
        {
            SuggestedLevel = suggestedLevel,
            Detections = detections,
            Confidence = CalculateConfidence(detections)
        };
    }
}

public static class PiiPatterns
{
    public static readonly string SocialSecurityNumber = @"\b\d{3}-\d{2}-\d{4}\b";
    public static readonly string CreditCard = @"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b";
    public static readonly string Email = @"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b";
    public static readonly string PhoneNumber = @"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b";
}
```

### Data Inventory Template

```yaml
Data Inventory Entry:
  asset_id: DATA-001
  name: Customer Database
  description: Master customer records
  owner: Customer Service Department
  custodian: IT Operations
  location:
    - Azure SQL Database (prod-sql-001)
    - Daily backup to Azure Blob Storage
  data_categories:
    - PII (names, emails, addresses)
    - Financial (payment history, credit limits)
    - Behavioral (purchase history)
  classification: Restricted
  volume: ~2M records
  sensitivity_reason: Contains PII and financial data
  regulatory_requirements:
    - GDPR (EU customers)
    - CCPA (California customers)
  retention:
    active: Duration of customer relationship
    archived: 7 years after relationship ends
  access:
    roles:
      - CustomerAdmin (full access)
      - Support (read-only)
      - Analytics (anonymized only)
    mfa_required: true
    vpn_required: true
  encryption:
    at_rest: AES-256 (Transparent Data Encryption)
    in_transit: TLS 1.3
  backup:
    frequency: Daily
    retention: 30 days
    tested: Monthly
  last_review: 2025-01-15
  next_review: 2025-07-15
```

## Data Lifecycle Management

### Lifecycle Stages

```text
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Create  │───▶│  Store  │───▶│   Use   │───▶│ Archive │───▶│ Destroy │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
 Classify      Encrypt       Monitor        Restrict       Certify
   Label       Access Ctrl   Audit Log      Read-only      Disposal
```

### Retention Policy Implementation

```csharp
public class DataRetentionService
{
    private readonly IRetentionPolicyProvider _policies;
    private readonly IAuditLogger _auditLogger;

    public async Task ApplyRetentionPolicies(CancellationToken ct)
    {
        var policies = await _policies.GetActivePolicies(ct);

        foreach (var policy in policies)
        {
            var expiredData = await FindExpiredData(policy, ct);

            foreach (var item in expiredData)
            {
                switch (policy.Action)
                {
                    case RetentionAction.Archive:
                        await ArchiveData(item, policy, ct);
                        break;

                    case RetentionAction.Anonymize:
                        await AnonymizeData(item, policy, ct);
                        break;

                    case RetentionAction.Delete:
                        await SecureDelete(item, policy, ct);
                        break;
                }

                await _auditLogger.LogRetentionAction(item, policy, ct);
            }
        }
    }

    private async Task SecureDelete(DataItem item, RetentionPolicy policy, CancellationToken ct)
    {
        var classification = item.Classification;

        switch (classification)
        {
            case DataClassification.Public:
            case DataClassification.Internal:
                // Standard deletion
                await _repository.Delete(item.Id, ct);
                break;

            case DataClassification.Confidential:
                // Secure deletion with verification
                await _repository.SecureDelete(item.Id, ct);
                await VerifyDeletion(item.Id, ct);
                break;

            case DataClassification.Restricted:
            case DataClassification.TopSecret:
                // Cryptographic erasure + verification
                await _encryptionService.DestroyKey(item.EncryptionKeyId, ct);
                await _repository.SecureDelete(item.Id, ct);
                await VerifyDeletion(item.Id, ct);
                await GenerateDeletionCertificate(item, ct);
                break;
        }
    }
}
```

### Disposal Certification

```csharp
public class DisposalCertificate
{
    public required Guid CertificateId { get; init; }
    public required DateTimeOffset DisposalDate { get; init; }
    public required string DataDescription { get; init; }
    public required DataClassification Classification { get; init; }
    public required string DisposalMethod { get; init; }
    public required string PerformedBy { get; init; }
    public required string WitnessedBy { get; init; }
    public required string VerificationMethod { get; init; }
    public required bool VerificationPassed { get; init; }
    public string? Notes { get; init; }
}
```

## Labeling and Tagging

### Document Labeling

```csharp
public class DocumentLabeler
{
    public async Task<LabeledDocument> ApplyLabel(
        Document document,
        DataClassification classification,
        CancellationToken ct)
    {
        var label = new ClassificationLabel
        {
            Level = classification,
            AppliedAt = DateTimeOffset.UtcNow,
            AppliedBy = _currentUser.Id,
            ExpiresAt = classification >= DataClassification.Confidential
                ? DateTimeOffset.UtcNow.AddYears(1)  // Require re-classification
                : null
        };

        // Add visual header/footer
        if (document.Type == DocumentType.Word || document.Type == DocumentType.PDF)
        {
            await AddVisualLabel(document, label, ct);
        }

        // Add metadata
        document.Metadata["classification"] = classification.ToString();
        document.Metadata["classification_date"] = label.AppliedAt.ToString("O");
        document.Metadata["classification_by"] = label.AppliedBy;

        // Apply protection
        if (classification >= DataClassification.Confidential)
        {
            await ApplyProtection(document, classification, ct);
        }

        return new LabeledDocument
        {
            Document = document,
            Label = label
        };
    }
}
```

## Classification Policy Template

```markdown
# Data Classification Policy

## 1. Purpose
Establish consistent data handling based on sensitivity.

## 2. Scope
All data created, collected, stored, or processed by [Organization].

## 3. Classification Levels

### 3.1 Public
Data intended for public disclosure.
- **Examples**: Marketing materials, press releases
- **Handling**: No special requirements

### 3.2 Internal
General business information.
- **Examples**: Policies, procedures, org charts
- **Handling**: Access limited to employees

### 3.3 Confidential
Business-sensitive information.
- **Examples**: Financial reports, contracts, strategies
- **Handling**: Need-to-know access, encryption required

### 3.4 Restricted
Highly sensitive, regulated data.
- **Examples**: PII, PHI, payment card data
- **Handling**: Strict access control, MFA, encryption, audit logging

## 4. Roles and Responsibilities

### Data Owner
- Assign classification level
- Approve access requests
- Review classification annually

### Data Custodian
- Implement technical controls
- Manage access permissions
- Monitor for violations

### All Employees
- Handle data per classification
- Report misclassification
- Protect sensitive data

## 5. Handling Requirements
[See matrix above]

## 6. Non-Compliance
Violations subject to disciplinary action.

## 7. Review
Policy reviewed annually.
```

## Classification Checklist

### Implementation

- [ ] Define classification levels
- [ ] Create handling requirements matrix
- [ ] Identify data owners
- [ ] Conduct data inventory
- [ ] Apply classifications to existing data
- [ ] Implement technical controls
- [ ] Train employees

### Ongoing

- [ ] Annual classification review
- [ ] New data assessment
- [ ] Access review
- [ ] Control effectiveness testing
- [ ] Policy updates

## Cross-References

- **GDPR**: `gdpr-compliance` for personal data
- **HIPAA**: `hipaa-compliance` for health data
- **Security**: `security-frameworks` for controls

## Resources

- [NIST SP 800-60](https://csrc.nist.gov/publications/detail/sp/800-60/vol-1-rev-1/final)
- [ISO 27001 Annex A.8.2](https://www.iso.org/standard/27001)
