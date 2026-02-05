---
name: "Ultimate Beneficial Owner Lookup"
description: "Identify ultimate beneficial owners and control structures"
allowed-tools:
  - src.tools.ubo_lookup
---

# Ultimate Beneficial Owner Lookup

## Purpose

Identify ultimate beneficial owners (UBOs) and beneficial ownership structures of companies and trusts. Essential for AML compliance, sanctions screening, and regulatory due diligence requirements.

## When to Use

- KYC/AML compliance for corporate customers
- Beneficial ownership reporting requirements
- Sanctions screening of controlling parties
- PEP (Politically Exposed Persons) identification
- Complex ownership structure analysis
- Trust and foundation beneficial ownership
- Regulatory compliance for financial institutions
- Enhanced due diligence investigations

## How to Use

The UBO lookup tool traces ownership through multiple layers:

- **Direct Ownership**: Immediate shareholders and their percentages
- **Indirect Ownership**: Multi-layered ownership structures
- **Control Analysis**: Voting rights, management control, other influence
- **Natural Persons**: Individual ultimate beneficial owners
- **Ownership Thresholds**: 25%, 10%, or other regulatory thresholds
- **Trust Structures**: Settlors, trustees, beneficiaries

## Examples

**Corporate customer onboarding:**
```
Entity: Investment Fund ABC
UBO Analysis: Identify all individuals with >25% beneficial ownership
Compliance: Screen UBOs against sanctions and PEP lists
```

**Complex ownership investigation:**
```
Target: Multinational Corporation
Structure: Trace ownership through holding companies across jurisdictions
Analysis: Map complete beneficial ownership chain to natural persons
```

**Trust beneficial ownership:**
```
Entity: Private Family Trust
Investigation: Identify settlors, trustees, and current beneficiaries
Screening: Assess AML/sanctions risk for all beneficial owners
```

**Sanctions compliance:**
```
New Customer: Offshore Holdings Ltd
Due Diligence: Verify no sanctioned individuals in ownership chain
Documentation: Create UBO disclosure for regulatory filing
```

## Important Notes

- UBO definitions vary by jurisdiction (typically 10-25% ownership threshold)
- Complex structures may require multiple data sources and manual analysis
- Trust and foundation structures present unique identification challenges
- Ownership percentages may change - ensure information is current
- Some jurisdictions have UBO registries, others rely on company disclosure
- Privacy laws may limit access to beneficial ownership information
- Cross-reference findings with sanctions, PEP, and adverse media screening
- Document UBO analysis thoroughly for regulatory compliance