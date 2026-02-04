---
name: control-implementation-generator
description: Generate detailed control implementation guidance, technical steps, and implementation plans for OSCAL security controls. Use this skill to create implementation narratives, technical procedures, and deployment plans.
---

# Control Implementation Generator Skill

Generate comprehensive implementation guidance, technical procedures, and deployment plans for security controls based on system context.

## When to Use This Skill

Use this skill when you need to:
- Create control implementation narratives for SSPs
- Generate technical implementation steps
- Build implementation timelines
- Identify tools and resources needed
- Create system-specific guidance

---

## ⛔ Authoritative Data Requirement

### What Requires Authoritative Sources

| Requirement | Source Needed |
|-------------|---------------|
| Control text/definition | OSCAL catalog document |
| Control parameters | Profile with parameter settings |
| Baseline requirements | FedRAMP/NIST baseline profile |
| Vendor-specific implementation | Vendor documentation |

### What You CAN Generate (Templates & Methodology)
- Narrative structure and format
- Implementation approach patterns (based on user's stated technology)
- Timeline templates
- Effort estimation frameworks
- General best practices for stated platforms

### What You CANNOT Generate
- Specific control requirement text (must cite from catalog)
- Parameter values (must come from profile or organization)
- Vendor configuration details without documentation
- Compliance claims without evidence

### Safe vs Unsafe Examples

**✅ Safe:** "For AC-2 in your AWS environment, the typical approach involves AWS IAM for identity management combined with..."

**⛔ Unsafe:** "AC-2 requires organizations to define and document account types within 30 days..." (← This specific requirement must come from the catalog)

### If Control Definition Needed
```
To generate accurate implementation guidance for [control], I need:
• The control definition from your OSCAL catalog
• Your baseline profile (for parameter values)
• Your technology stack (you've stated: [tech])

I can provide implementation templates and patterns, but the specific
control requirements must come from your authoritative catalog.
```

---

## Implementation Status Options

| Status | Description | SSP Usage |
|--------|-------------|-----------|
| Implemented | Fully in place | Describe how |
| Partially Implemented | Some aspects complete | Describe what's done, what's remaining |
| Planned | Scheduled for implementation | Describe timeline |
| Alternative | Different approach meeting intent | Describe alternative |
| Not Applicable | Control doesn't apply | Provide justification |

## Implementation Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| Automated | Technology-enforced | Technical controls |
| Manual | Human-performed | Procedural controls |
| Hybrid | Combination | Complex controls |
| Inherited | Provided by another system | Shared services |

## System Types

| Type | Characteristics | Implementation Focus |
|------|-----------------|---------------------|
| Cloud Service | AWS, Azure, GCP | API, IAM, native tools |
| On-Premises | Traditional datacenter | Network, physical |
| Hybrid | Mixed environment | Integration, consistency |
| SaaS | Software service | Configuration, access |

## How to Generate Implementation Guidance

### Step 1: Understand the Control
Parse the control requirement:
1. Read the control statement
2. Identify key requirements
3. Note any parameters
4. Review guidance section

### Step 2: Assess System Context
Consider:
- System type (cloud, on-prem, hybrid)
- Technology stack
- Existing capabilities
- Organizational constraints

### Step 3: Determine Implementation Method
Based on control type and system:
- Technical controls → Automated
- Policy controls → Manual/Hybrid
- Shared services → Inherited

### Step 4: Generate Implementation Steps

For each control, provide:

```yaml
implementation:
  control_id: AC-2
  status: implemented
  method: hybrid
  
  description: |
    Account management is implemented through Azure Active Directory
    for identity management, combined with automated provisioning
    workflows and quarterly access reviews.
  
  technical_steps:
    - Configure Azure AD as identity provider
    - Implement automated user provisioning via SCIM
    - Configure access review campaigns (quarterly)
    - Enable Privileged Identity Management (PIM)
    - Set up termination automation via HR integration
  
  tools_required:
    - Azure Active Directory Premium P2
    - Azure AD Connect
    - ServiceNow (or HR system)
  
  responsible_roles:
    - IAM Administrator
    - HR Business Partner
    - Application Owners
  
  evidence:
    - Azure AD configuration export
    - Access review completion reports
    - Provisioning workflow documentation
```

## Implementation Narrative Templates

### For Policy Controls (e.g., AC-1)

```
[Organization] has developed, documented, and disseminated an 
access control policy that:
a. Addresses purpose, scope, roles, responsibilities, and compliance
b. Is consistent with applicable laws and regulations
c. Is reviewed and updated [frequency]

The policy is maintained in [location] and communicated to all 
personnel via [method]. The [role] is responsible for policy 
maintenance and updates.
```

### For Technical Controls (e.g., IA-2)

```
The system implements multi-factor authentication through 
[solution] for all user access. Authentication factors include:
- Something you know: Password meeting complexity requirements
- Something you have: [Authenticator app / Hardware token / SMS]

Configuration: [Specific settings]
Enforcement: [How it's enforced]
Exceptions: [Any approved exceptions]
```

### For Hybrid Controls (e.g., AC-2)

```
Account management is implemented through a combination of:

Technical Controls:
- [Identity system] manages user accounts
- Automated provisioning via [method]
- [Tool] enforces access policies

Procedural Controls:
- Access requests submitted via [process]
- Manager approval required for all access
- Quarterly access reviews conducted by [role]
```

## Implementation Effort Estimation

| Complexity | Hours | Description |
|------------|-------|-------------|
| Low | 1-8 | Configuration change |
| Medium | 8-40 | New tool/process |
| High | 40-160 | Major implementation |
| Very High | 160+ | Program-level effort |

## Implementation Plan Structure

```
CONTROL IMPLEMENTATION PLAN
===========================
Control: CM-6 (Configuration Settings)
System: Production Web Environment
Timeline: Q2 2024

Phase 1: Planning (Week 1-2)
- Define baseline configurations
- Identify configuration management tools
- Create change management process

Phase 2: Implementation (Week 3-6)
- Deploy configuration management tool
- Apply baseline configurations
- Test and validate settings

Phase 3: Monitoring (Week 7-8)
- Configure drift detection
- Set up alerting
- Document procedures

Resources Required:
- Security Engineer: 40 hours
- Systems Administrator: 60 hours
- Tool licensing: [Cost]

Dependencies:
- CM-2 (Baseline Configuration) must be complete
- Change management process approved
```

## Common Implementation Patterns

### Cloud (AWS Example)

| Control | AWS Implementation |
|---------|-------------------|
| AC-2 | IAM + AWS SSO + Organizations |
| AU-2 | CloudTrail + CloudWatch Logs |
| CM-2 | Config Rules + Systems Manager |
| SC-7 | VPC + Security Groups + WAF |

### Azure Example

| Control | Azure Implementation |
|---------|---------------------|
| AC-2 | Azure AD + PIM |
| AU-2 | Azure Monitor + Log Analytics |
| CM-2 | Azure Policy + Automation |
| SC-7 | NSG + Azure Firewall + Front Door |

## Example Usage

When asked "How should I implement IA-2 for a cloud system?":

1. Parse IA-2 requirements (identification and authentication)
2. Assess system type (cloud)
3. Identify cloud-native options:
   - AWS: Cognito, IAM Identity Center
   - Azure: Azure AD, Conditional Access
   - GCP: Cloud Identity, IAP
4. Generate implementation steps
5. Specify MFA requirements
6. Create implementation narrative
7. Estimate effort and timeline
