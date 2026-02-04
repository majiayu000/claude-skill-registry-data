---
name: component-definition-builder
description: Create and manage OSCAL component definitions for reusable security control implementations. Inspired by CivicActions components and community patterns. Use for building component libraries and shared control implementations.
---

# Component Definition Builder Skill

Create and manage OSCAL component definitions for reusable security control implementations, enabling consistent compliance across systems.

## When to Use This Skill

Use this skill when you need to:
- Create reusable component definitions
- Document how a product implements controls
- Build component libraries for common services
- Merge multiple components into SSPs
- Define capability-based control implementations

---

## ⛔ Authoritative Data Requirement

Component definitions require **control catalogs** to reference valid control IDs.

### What Requires Authoritative Sources
| Element | Source Needed |
|---------|---------------|
| Control IDs (e.g., AC-2) | OSCAL catalog |
| Control statements | OSCAL catalog |
| Parameter values | Profile or organizational settings |

### What You CAN Generate (Templates & Structure)
- Component definition structure
- Capability descriptions (user-stated)
- Implementation approach patterns
- Responsibility designations

### What You CANNOT Generate
- Valid control IDs without a catalog
- Control requirement text without a catalog
- Vendor-specific implementation claims without documentation

### When Building Components
```
To create a component definition, I need:
• The control catalog (to reference valid control IDs)
• Your description of how this component implements those controls
• Responsibility model (implemented, shared, inherited)

I will use valid control IDs from your catalog — not from training data.
```

---

## Component Types

| Type | Description | Examples |
|------|-------------|----------|
| Software | Applications | Web servers, databases |
| Hardware | Physical devices | Firewalls, HSMs |
| Service | Cloud/managed services | AWS S3, Azure AD |
| Policy | Governance documents | Security policies |
| Process | Procedures | Change management |
| Plan | Planning documents | Contingency plans |
| Guidance | Reference material | Standards, baselines |

## Component Definition Structure

```yaml
component-definition:
  uuid: [unique-id]
  metadata:
    title: AWS S3 Security Component
    version: 1.0.0
  
  components:
    - uuid: [component-uuid]
      type: service
      title: Amazon S3
      description: Object storage service
      
      control-implementations:
        - uuid: [impl-uuid]
          source: NIST 800-53 Moderate
          description: S3 security controls
          
          implemented-requirements:
            - control-id: SC-28
              description: S3 encrypts data at rest using AES-256
            - control-id: AC-3
              description: S3 bucket policies enforce access control
```

## How to Build Component Definitions

### Step 1: Define Component Metadata
```yaml
component:
  uuid: [generate-uuid]
  type: service
  title: [Product/Service Name]
  description: |
    Brief description of the component
    and its security relevance.
  
  properties:
    - name: vendor
      value: [Vendor Name]
    - name: version
      value: [Version]
```

### Step 2: Identify Applicable Controls
For the component, determine:
1. What security controls does it help implement?
2. Is implementation full or partial?
3. What specific features address each control?

### Step 3: Document Control Implementations

For each control:
```yaml
implemented-requirement:
  control-id: SC-28
  uuid: [generate-uuid]
  
  description: |
    [How the component implements this control]
    
  remarks: |
    [Additional context, limitations, configuration needed]
  
  props:
    - name: implementation-status
      value: implemented  # or partial, planned
    
  responsible-roles:
    - role-id: cloud-administrator
```

### Step 4: Add Responsible Roles
Define who manages the component:
```yaml
responsible-roles:
  - role-id: system-owner
    party-uuids: [party-uuid]
  - role-id: cloud-admin
    party-uuids: [party-uuid]
```

## Common Component Templates

### Cloud Service Component

```yaml
component:
  type: service
  title: [Cloud Service Name]
  
  control-implementations:
    # Access Control
    - control-id: AC-2
      description: |
        [Service] provides account management through IAM.
        User provisioning and deprovisioning is managed via...
      
    - control-id: AC-3
      description: |
        Access enforcement implemented through [mechanism].
        Policies define permitted actions...
    
    # Audit
    - control-id: AU-2
      description: |
        [Service] logs [event types] to [destination].
        Retention period: [duration]
    
    # Encryption
    - control-id: SC-28
      description: |
        Data at rest encrypted using [algorithm].
        Key management via [service/method].
```

### Software Component

```yaml
component:
  type: software
  title: [Application Name]
  
  properties:
    - name: vendor
      value: [Vendor]
    - name: version  
      value: [Version]
    - name: deployment-model
      value: [on-prem/cloud/hybrid]
  
  control-implementations:
    - control-id: IA-2
      description: |
        Application implements authentication through...
        MFA supported via...
```

### Policy Component

```yaml
component:
  type: policy
  title: Information Security Policy
  
  control-implementations:
    - control-id: AC-1
      description: |
        The organization's Access Control Policy establishes:
        - Purpose and scope
        - Roles and responsibilities
        - Compliance requirements
        
        Policy location: [document reference]
        Review frequency: Annual
```

## Component Library Patterns

### Organize by Service Category
```
components/
├── identity/
│   ├── azure-ad.json
│   ├── okta.json
│   └── aws-sso.json
├── storage/
│   ├── aws-s3.json
│   └── azure-blob.json
└── monitoring/
    ├── splunk.json
    └── datadog.json
```

### Version Components
```yaml
metadata:
  version: 2.1.0
  revision-history:
    - published: 2024-01-15
      version: 2.1.0
      remarks: Added SC-28(1) implementation
```

## Merging Components into SSP

When building an SSP from components:

1. **Select applicable components**
2. **Resolve overlapping implementations**
   - If multiple components implement same control, merge or select
3. **Add system-specific context**
4. **Fill gaps**
   - Controls not covered by components need custom implementation

## Component Inheritance

Components can indicate inheritance:
```yaml
implemented-requirement:
  control-id: PE-3
  description: |
    Physical access control inherited from 
    AWS data center security controls.
  
  props:
    - name: implementation-status
      value: inherited
    - name: inherited-from
      value: AWS Infrastructure
```

## Output Format

When creating a component definition:

```
COMPONENT DEFINITION
====================
Title: Amazon Web Services S3
Type: Service
Version: 1.0.0

Control Implementations:
- Baseline: NIST 800-53 Moderate
- Controls Addressed: 15

Coverage:
✅ SC-28: Data at Rest Encryption
✅ AC-3: Access Enforcement  
✅ AU-2: Audit Events
✅ SC-8: Transmission Confidentiality
...

Generated Files:
- aws-s3-component.json (OSCAL format)
```

## Example Usage

When asked "Create a component definition for Azure AD":

1. Set up component metadata (Azure AD, Microsoft, service type)
2. Identify relevant controls (AC, IA, AU families primarily)
3. For each control, document how Azure AD implements it
4. Note any partial implementations or prerequisites
5. Add responsible roles (IAM Admin, Security Admin)
6. Generate valid OSCAL component definition JSON
