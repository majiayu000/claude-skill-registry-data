---
name: oscal-control-mapper
description: Create and analyze OSCAL Control Mapping documents to establish formal relationships between controls across different frameworks (NIST 800-53, ISO 27001, CIS, PCI-DSS, etc.). Use this skill to document control equivalencies, gaps, and harmonization for multi-framework compliance.
---

# OSCAL Control Mapper Skill

Create and analyze OSCAL 1.2.0 Control Mapping documents to establish formal, machine-readable relationships between security controls across different frameworks.

## When to Use This Skill

Use this skill when you need to:
- Map controls between different frameworks (NIST 800-53 ↔ ISO 27001)
- Document control equivalencies and relationships
- Identify gaps when transitioning between frameworks
- Create harmonized control sets for multi-framework compliance
- Generate mapping documentation for auditors
- Analyze existing control mapping documents

---

## ⛔ Authoritative Data Requirement

Control mapping requires **authoritative catalogs** for both source and target frameworks.

### What This Skill Does (Safe)
- Creates OSCAL Control Mapping document structure
- Defines relationship types (equal, subset, superset, intersects, not-equal)
- Documents mapping rationale and notes
- Validates mapping document structure

### What Requires Authoritative Sources
| Element | Source Needed |
|---------|---------------|
| Source control IDs | Source catalog (e.g., NIST 800-53) |
| Target control IDs | Target catalog (e.g., ISO 27001) |
| Control text/requirements | Both catalogs |

### When Creating Mappings
```
To create a control mapping, I need:
• Source framework catalog (e.g., NIST 800-53 Rev 5)
• Target framework catalog (e.g., ISO 27001:2022)
• Your mapping analysis or documented equivalencies

I will NOT generate mappings from training data — only from authoritative sources.
```

---

## What is the Control Mapping Model?

**New in OSCAL 1.2.0** (December 2025), the Control Mapping model provides a standardized way to express relationships between controls in different frameworks.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Control Mapping** | Document defining relationships between controls |
| **Mapping Entry** | Single relationship between source and target control(s) |
| **Relationship Type** | Nature of the mapping (equal, subset, superset, etc.) |
| **Mapping Collection** | Grouped set of related mappings |

### Relationship Types

| Type | Description | Example |
|------|-------------|---------|
| `equal` | Controls are functionally equivalent | NIST AC-2 = ISO 27001 A.9.2.1 |
| `subset` | Source is narrower than target | NIST AC-2(1) ⊂ ISO 27001 A.9.2.1 |
| `superset` | Source is broader than target | NIST AC-2 ⊃ ISO 27001 A.9.2.1 |
| `intersects` | Partial overlap between controls | NIST SC-7 ∩ ISO 27001 A.13.1.1 |
| `not-equal` | Controls address different requirements | NIST AC-1 ≠ ISO 27001 A.5.1.1 |

---

## Control Mapping Structure

```yaml
control-mappings:
  uuid: [unique-id]
  metadata:
    title: "NIST 800-53 to ISO 27001 Mapping"
    version: "1.0"
    oscal-version: "1.2.0"
    last-modified: "2026-01-20T00:00:00Z"
  
  # Define the frameworks being mapped
  import-control-schemes:
    - href: "#nist-800-53-rev5"
      scheme: "nist-800-53-rev5"
    - href: "#iso-27001-2022"
      scheme: "iso-27001-2022"
  
  # Mapping entries
  control-mapping-set:
    - uuid: [set-uuid]
      title: "Access Control Mappings"
      description: "Mappings for access control requirements"
      
      control-mappings:
        - uuid: [mapping-uuid]
          source:
            control-id: "ac-2"
            scheme: "nist-800-53-rev5"
          
          target:
            - control-id: "a.9.2.1"
              scheme: "iso-27001-2022"
          
          relationship: "equal"
          
          remarks: |
            Both controls require account management procedures
            including creation, modification, and removal.
```

## How to Create Control Mappings

### Step 1: Obtain Required Catalogs

You need OSCAL catalogs for both frameworks:
- Use the `oscal-catalog-provider` skill for NIST 800-53, FedRAMP
- Request ISO, CIS, or other framework catalogs from the user

### Step 2: Define Mapping Document Metadata

```json
{
  "control-mappings": {
    "uuid": "[generate-uuid]",
    "metadata": {
      "title": "Framework A to Framework B Control Mapping",
      "version": "1.0",
      "oscal-version": "1.2.0",
      "last-modified": "[current-date]",
      "roles": [
        {
          "id": "mapper",
          "title": "Control Mapping Analyst"
        }
      ],
      "parties": [
        {
          "uuid": "[party-uuid]",
          "type": "organization",
          "name": "Your Organization"
        }
      ]
    }
  }
}
```

### Step 3: Import Control Schemes

Define the frameworks being mapped:

```json
"import-control-schemes": [
  {
    "href": "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json",
    "scheme": "nist-800-53-rev5"
  },
  {
    "href": "#iso-27001-catalog",
    "scheme": "iso-27001-2022"
  }
]
```

### Step 4: Create Mapping Sets

Group related mappings logically:

```json
"control-mapping-set": [
  {
    "uuid": "[set-uuid]",
    "title": "Access Control Mappings",
    "description": "Mappings for access control domain",
    "control-mappings": [
      // Individual mappings here
    ]
  }
]
```

### Step 5: Define Individual Mappings

For each control relationship:

```json
{
  "uuid": "[mapping-uuid]",
  "source": {
    "control-id": "ac-2",
    "scheme": "nist-800-53-rev5"
  },
  "target": [
    {
      "control-id": "a.9.2.1",
      "scheme": "iso-27001-2022"
    }
  ],
  "relationship": "equal",
  "remarks": "Both require account management lifecycle procedures"
}
```

### Step 6: Handle Complex Mappings

#### One-to-Many Mapping
```json
{
  "source": {
    "control-id": "ac-2",
    "scheme": "nist-800-53-rev5"
  },
  "target": [
    {
      "control-id": "a.9.2.1",
      "scheme": "iso-27001-2022"
    },
    {
      "control-id": "a.9.2.2",
      "scheme": "iso-27001-2022"
    }
  ],
  "relationship": "superset"
}
```

#### Many-to-One Mapping
Create separate mapping entries for each source control pointing to the same target.

#### Partial Coverage
```json
{
  "source": {
    "control-id": "sc-7",
    "scheme": "nist-800-53-rev5"
  },
  "target": [
    {
      "control-id": "a.13.1.1",
      "scheme": "iso-27001-2022"
    }
  ],
  "relationship": "intersects",
  "remarks": "NIST SC-7 covers boundary protection broadly; ISO A.13.1.1 focuses on network controls. Partial overlap."
}
```

---

## Analyzing Existing Mappings

When analyzing a control mapping document:

### Step 1: Parse the Document
Use the `oscal-parser` skill to read the mapping document.

### Step 2: Validate Structure
- Confirm all source and target control IDs exist in referenced catalogs
- Check relationship types are valid
- Verify UUIDs are unique

### Step 3: Generate Analysis Report

```markdown
# Control Mapping Analysis

**Source:** NIST 800-53 Rev 5
**Target:** ISO 27001:2022
**Total Mappings:** 145

## Relationship Distribution

- Equal: 78 (53.8%)
- Subset: 23 (15.9%)
- Superset: 31 (21.4%)
- Intersects: 13 (9.0%)
- Not-equal: 0 (0%)

## Coverage Analysis

### NIST 800-53 Coverage
- Total controls: 323
- Mapped controls: 245 (75.9%)
- Unmapped controls: 78 (24.1%)

### ISO 27001 Coverage
- Total controls: 93
- Mapped controls: 89 (95.7%)
- Unmapped controls: 4 (4.3%)

## Gaps Identified

### Unmapped NIST Controls
- AC-25: Reference Monitor
- SC-47: Alternate Communications Paths
- [...]

### Unmapped ISO Controls
- A.6.1.1: Information Security Roles
- [...]
```

### Step 4: Identify Mapping Quality Issues

| Issue | Description |
|-------|-------------|
| Orphaned mappings | References to non-existent control IDs |
| Bidirectional conflicts | A→B (equal) but B→A (subset) |
| Coverage gaps | Large numbers of unmapped controls |
| Relationship mismatches | Questionable relationship types |

---

## Common Use Cases

### 1. Multi-Framework Compliance

**Scenario:** Organization must comply with both FedRAMP and ISO 27001.

**Approach:**
1. Create mapping: FedRAMP Moderate → ISO 27001
2. Identify overlapping controls (implement once)
3. Identify ISO-only controls (additional requirements)
4. Generate combined control set

### 2. Framework Migration

**Scenario:** Moving from NIST 800-53 Rev 4 → Rev 5.

**Approach:**
1. Create mapping: Rev 4 → Rev 5
2. Identify deprecated controls
3. Identify new requirements
4. Plan implementation updates

### 3. Vendor Control Correlation

**Scenario:** Map cloud provider controls to your baseline.

**Approach:**
1. Import vendor component definition
2. Create mapping: Vendor controls → NIST 800-53
3. Identify responsibility model (inherited vs. hybrid vs. customer)
4. Document coverage and gaps

### 4. Regulatory Harmonization

**Scenario:** Create unified control set for HIPAA, PCI-DSS, SOC 2.

**Approach:**
1. Create mappings for each framework pair
2. Identify common control core
3. Document framework-specific additions
4. Generate harmonized control catalog

---

## Output Format

### Mapping Summary Report

```
CONTROL MAPPING SUMMARY
=======================
Document: nist-to-iso-mapping.json
Source: NIST 800-53 Rev 5 (323 controls)
Target: ISO 27001:2022 (93 controls)
Version: 1.0
Last Updated: 2026-01-20

MAPPING STATISTICS
------------------
Total Mappings: 145
• Equal: 78 (53.8%)
• Subset: 23 (15.9%)
• Superset: 31 (21.4%)
• Intersects: 13 (9.0%)

COVERAGE
--------
Source Coverage: 245/323 (75.9%)
Target Coverage: 89/93 (95.7%)

TOP GAPS
--------
Unmapped Source Controls: 78
• Access Control: 12
• System Communications: 15
• Supply Chain: 8
[...]

Unmapped Target Controls: 4
• A.6.1.1, A.7.1.1, A.8.2.1, A.15.1.1

QUALITY
-------
✓ No orphaned references
✓ All UUIDs unique
⚠ 3 potential bidirectional conflicts detected
```

---

## Example Mapping Entry

```json
{
  "uuid": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "source": {
    "control-id": "ac-2",
    "scheme": "nist-800-53-rev5"
  },
  "target": [
    {
      "control-id": "a.9.2.1",
      "scheme": "iso-27001-2022"
    },
    {
      "control-id": "a.9.2.5",
      "scheme": "iso-27001-2022"
    }
  ],
  "relationship": "superset",
  "props": [
    {
      "name": "mapping-confidence",
      "value": "high"
    }
  ],
  "remarks": "NIST AC-2 comprehensively covers account management including provisioning (ISO A.9.2.1) and privileged access (ISO A.9.2.5). The NIST control is broader in scope."
}
```

---

## Best Practices

1. **Document Rationale**: Always include remarks explaining mapping decisions
2. **Use Authoritative Sources**: Never map from memory or training data
3. **Validate Bidirectionally**: Check mappings make sense from both perspectives
4. **Review Coverage**: Identify and document gaps explicitly
5. **Version Control**: Track mapping versions as frameworks evolve
6. **Expert Review**: Have subject matter experts validate critical mappings
7. **Maintain Consistency**: Use consistent relationship type definitions
8. **Update Regularly**: Review when frameworks release new versions

---

## Integration with Other Skills

| Skill | Use With Control Mapper |
|-------|-------------------------|
| `oscal-catalog-provider` | Fetch source/target catalogs |
| `oscal-parser` | Read existing mapping documents |
| `oscal-validator` | Validate mapping document structure |
| `control-implementation-generator` | Generate unified implementation guidance |
| `compliance-report-generator` | Report on multi-framework compliance |
| `gap-analyzer` | Identify coverage gaps |

---

## Limitations

- **Semantic Understanding**: Mappings require human judgment; AI cannot definitively declare controls "equal"
- **Framework Updates**: Mappings become stale when frameworks are revised
- **Context Dependency**: Mapping appropriateness may vary by organizational context
- **Tool Support**: OSCAL 1.2.0 Control Mapping model is new; tool support is emerging

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid control-id | Control doesn't exist in catalog | Verify against authoritative catalog |
| Unknown scheme | Framework not recognized | Use standard scheme identifiers |
| Relationship conflict | Bidirectional mappings inconsistent | Review and reconcile relationships |
| Missing catalog | import-control-schemes href broken | Provide valid catalog references |

---

## Additional Resources

- [OSCAL Control Mapping Model Specification](https://pages.nist.gov/OSCAL/reference/latest/control-mappings/)
- NIST SP 800-53B - Control Baselines
- ISO/IEC 27001:2022 - Information Security Management
- NIST-to-ISO Official Mapping (if available)

---

## Version History

- **v1.0** (2026-01-20) - Initial skill for OSCAL 1.2.0 Control Mapping model
