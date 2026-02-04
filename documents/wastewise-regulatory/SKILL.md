---
name: wastewise-regulatory
description: WasteWise Complete Analysis with automated regulatory compliance research and LLM Judge validation. Includes all standard analysis features PLUS automated ordinance research, compliance checklists, and quality-scored evaluation. Use when you need both waste analysis AND regulatory compliance documentation.
---

# WasteWise Regulatory - Complete Analysis with Compliance Research

## What This Skill Does

Enhanced version of WasteWise Complete Analysis with:

### Core Validation Framework
- ✅ Contract tabs are generated when contracts are provided
- ✅ Contract clauses are properly extracted and categorized
- ✅ Optimization recommendations meet strict criteria
- ✅ All formulas are correctly calculated
- ✅ Data completeness across all sheets
- ✅ Professional formatting standards
- ✅ Cross-sheet data consistency

### NEW: Regulatory Compliance Research
- ✅ Automated research of local waste/recycling/organics ordinances
- ✅ Extraction of mandatory requirements and thresholds
- ✅ Documentation of penalties and enforcement
- ✅ Licensed hauler identification
- ✅ Compliance checklist generation
- ✅ Confidence scoring for research quality

**This skill will NOT produce output until ALL validation checks pass, including regulatory compliance research validation.**

## Pre-Flight Validation Checklist

Before generating the final workbook, this skill runs a **mandatory validation suite**:

### 1. Contract Validation
```
☐ If contract file detected → CONTRACT_TERMS sheet MUST be created
☐ Extract 7 clause types: Term & Renewal, Rate Increases, Termination, Liability,
   Service Level, Force Majeure, Indemnification
☐ Calendar reminders calculated for critical dates
☐ Verbatim clause text extracted (not paraphrased)
☐ Risk severity assigned (high/medium/low)
```

### 2. Optimization Validation
```
☐ Compactor optimization: Only if avg < 6 tons/haul AND 14-day max interval
☐ Contamination reduction: Only if charges > 3-5% of spend
☐ Bulk subscription: Only if avg > $500/month
☐ Per-compactor pricing validated (not per-property)
☐ ROI calculations include all costs (install + monitoring)
☐ 14-day constraint enforced in recommendations
```

### 3. Formula Validation
```
☐ Yards per door: Correct formula for equipment type (per CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md)
   - Compactors: (Total Tons × 2000 / 138) / Units
   - Dumpsters: (Qty × Size × Freq × 4.33) / Units
☐ Cost per door: Total Monthly Cost / Units
☐ Capacity utilization: (Tons Per Haul / Target Tons) × 100%
☐ Days between pickups: 30 / (Hauls Per Month)
```

### 4. Sheet Structure Validation
```
☐ SUMMARY_FULL: 2026 savings one-liner at top
☐ EXPENSE_ANALYSIS: Month-by-month COLUMN format
☐ OPTIMIZATION: All 3 opportunities with calculation breakdowns
☐ QUALITY_CHECK: Confidence scores and validation metrics
☐ DOCUMENTATION_NOTES: Vendor contacts, formulas, glossary
☐ HAUL_LOG: Created only if compactor present
☐ CONTRACT_TERMS: Created only if contract provided
☐ REGULATORY_COMPLIANCE: Created with location-based research
```

### 5. Data Completeness Validation
```
☐ Property name extracted
☐ Unit count specified
☐ All invoice dates parsed
☐ Tonnage data present (if compactor)
☐ Service types identified
☐ Account numbers captured
☐ Vendor name extracted
☐ Location data extracted (city, county, state, zip)
```

### 6. Cross-Validation
```
☐ SUMMARY totals match EXPENSE_ANALYSIS
☐ HAUL_LOG tonnage matches OPTIMIZATION calculations
☐ CONTRACT_TERMS dates align with calendar reminders
☐ Cost per door consistent across all sheets
☐ REGULATORY_COMPLIANCE location matches property data
```

### 7. NEW: Regulatory Compliance Validation
```
☐ Location data successfully extracted from property documents
☐ Minimum 3 official government sources (.gov) consulted
☐ Waste, recycling, AND organics requirements researched
☐ Mandatory vs voluntary status explicitly documented
☐ Capacity requirements are numerical (not "adequate" or "sufficient")
☐ Service frequencies are specific (not "regular" or "as needed")
☐ Penalty amounts documented with $ figures
☐ At least 3-5 licensed haulers identified with full contact info
☐ Ordinance citations include chapter/section numbers
☐ Property size thresholds verified (4+, 5+, 8+, 10+ units)
☐ Recent regulatory changes (2023-2025) checked
☐ Confidence score assigned (HIGH/MEDIUM/LOW)
```

## Regulatory Compliance Research Protocol

### Phase 1: Extract Location Data

From uploaded documentation, identify:
- City name
- County (if available)
- State
- Zip code
- Property type and size (unit count)
- Building stories/height (for threshold determination)

### Phase 2: Conduct Regulatory Research

**Search Pattern Sequence:**
1. `"[City Name] [State]" waste recycling ordinance`
2. `"[City Name]" universal recycling ordinance`
3. `"[City Name]" mandatory composting multifamily`
4. `"[City Name]" solid waste code`
5. `"[County Name] County" waste management requirements`
6. `"[State]" recycling law commercial properties`

**Priority Sources:**
- Municipal solid waste/sanitation department websites (.gov)
- City/county ordinance databases (Municode, American Legal)
- State environmental agency waste division pages
- Regional waste authority sites

### Phase 3: Extract Regulatory Requirements

For each waste stream (Trash, Recycling, Composting/Organics), document:

#### TRASH/WASTE COLLECTION
- Municipal service availability for property size
- Private licensed hauler requirement (mandatory/optional)
- Minimum service frequency requirements
- Container size/type specifications
- Placement restrictions
- Licensed hauler directory URL

#### RECYCLING REQUIREMENTS
- Mandatory vs voluntary status
- Property size threshold for mandate
- Minimum capacity requirement (% of waste, gallons per unit, or total volume)
- Accepted materials list
- Service frequency minimum
- Container specifications (size, type, color)
- Placement requirements
- Signage requirements (language, symbols, content)
- Co-location rules

#### COMPOSTING/ORGANICS REQUIREMENTS
- Mandatory vs voluntary status
- Effective date (especially 2023-2025 mandates)
- Property size threshold
- Minimum capacity requirement
- Service frequency minimum
- Accepted materials (food scraps, food-soiled paper, yard waste, BPI-certified)
- Container specifications
- Resident education requirements

### Phase 4: Document Penalties & Enforcement

Extract:
- Violation classification (misdemeanor, civil, criminal)
- Fine structure (per offense, per day, maximum)
- Enforcement agency name and contact
- Warning vs citation procedures
- Repeat violation escalation

### Phase 5: Identify Licensed Haulers

Compile minimum 3-5 haulers with:
- Company name
- Phone number
- Website URL
- Service capabilities (waste, recycling, composting, compactor hauls)
- Official hauler directory URL

### Phase 6: Generate Compliance Checklist

Create property-specific checklist showing:
- ✅ Requirements currently met
- ⚠️ Requirements needing attention
- ❌ Requirements not met
- 📅 Upcoming compliance deadlines

## Confidence Scoring System

After completing regulatory research, assign confidence level:

### HIGH CONFIDENCE
- All waste streams documented with official ordinance citations
- Penalty amounts and enforcement agency confirmed
- Licensed hauler directory found and verified
- Reporting requirements fully documented
- All sources from official .gov domains
- Capacity requirements are specific numerical values
- Recent regulatory changes confirmed

### MEDIUM CONFIDENCE
- Core requirements found but some details missing
- Ordinance cited but specific sections unclear
- Hauler list incomplete (fewer than 3 haulers)
- Some sources from non-official websites
- Mixed specificity in requirements

### LOW CONFIDENCE - FLAG FOR HUMAN REVIEW
- Limited official information available
- Conflicting sources found
- Recent changes not confirmed
- No licensed hauler directory located
- Key requirements vague or missing
- Property size threshold unclear
- **REQUIRES MANUAL VERIFICATION**

## Enhanced Validation Implementation

### Regulatory Compliance Validator Class

```python
class RegulatoryComplianceValidator:
    """Validates regulatory compliance research quality"""

    def __init__(self):
        self.validation_results = {
            'location_extraction': {},
            'source_quality': {},
            'requirement_specificity': {},
            'completeness': {},
            'confidence_assessment': {}
        }
        self.errors = []
        self.warnings = []
        self.confidence_score = None

    def validate_regulatory_research(self, regulatory_data: Dict,
                                    property_info: Dict) -> Tuple[bool, str]:
        """
        Validate regulatory compliance research quality
        Returns: (passed: bool, confidence_level: str)
        """

        # 1. Validate location extraction
        location_valid = self.validate_location_data(
            regulatory_data.get('location', {}),
            property_info
        )

        # 2. Validate source quality
        sources_valid = self.validate_sources(
            regulatory_data.get('sources', [])
        )

        # 3. Validate requirement specificity
        specificity_valid = self.validate_requirement_specificity(
            regulatory_data.get('requirements', {})
        )

        # 4. Validate completeness
        completeness_valid = self.validate_completeness(
            regulatory_data
        )

        # 5. Assess confidence level
        confidence_level = self.assess_confidence(
            location_valid, sources_valid, specificity_valid, completeness_valid
        )

        # Determine if research passed minimum standards
        passed = confidence_level in ['HIGH', 'MEDIUM']

        if confidence_level == 'LOW':
            self.errors.append(
                "❌ REGULATORY RESEARCH CONFIDENCE TOO LOW: "
                "Research quality insufficient for automated compliance assessment. "
                "HUMAN REVIEW REQUIRED."
            )

        return passed, confidence_level

    def validate_location_data(self, location: Dict, property_info: Dict) -> bool:
        """Validate location extraction quality"""

        required_fields = ['city', 'state']
        optional_fields = ['county', 'zip_code']

        missing_required = [f for f in required_fields if not location.get(f)]

        if missing_required:
            self.errors.append(
                f"❌ LOCATION DATA INCOMPLETE: Missing required fields: "
                f"{', '.join(missing_required)}"
            )
            return False

        # Check for property size data
        if not property_info.get('unit_count'):
            self.warnings.append(
                "⚠️  Unit count not specified - may affect threshold applicability"
            )

        self.validation_results['location_extraction'] = {
            'status': 'PASSED',
            'city': location.get('city'),
            'state': location.get('state'),
            'county': location.get('county'),
            'unit_count': property_info.get('unit_count')
        }

        return True

    def validate_sources(self, sources: List[Dict]) -> bool:
        """Validate research source quality"""

        if len(sources) < 3:
            self.errors.append(
                f"❌ INSUFFICIENT SOURCES: Only {len(sources)} sources consulted. "
                f"Minimum 3 required."
            )
            return False

        # Check for .gov sources
        gov_sources = [s for s in sources if '.gov' in s.get('url', '')]

        if len(gov_sources) == 0:
            self.warnings.append(
                "⚠️  No official .gov sources found - relying on secondary sources"
            )

        self.validation_results['source_quality'] = {
            'status': 'PASSED' if len(gov_sources) >= 1 else 'WARNING',
            'total_sources': len(sources),
            'gov_sources': len(gov_sources),
            'source_list': [s.get('name', 'Unknown') for s in sources]
        }

        return True

    def validate_requirement_specificity(self, requirements: Dict) -> bool:
        """Validate that requirements are specific and measurable"""

        vague_terms = ['adequate', 'sufficient', 'appropriate', 'regular', 'as needed']
        specificity_issues = []

        # Check recycling requirements
        recycling = requirements.get('recycling', {})
        capacity = recycling.get('capacity_requirement', '')

        if any(term in str(capacity).lower() for term in vague_terms):
            specificity_issues.append("Recycling capacity uses vague terms")

        if recycling.get('service_frequency', '') in ['regular', 'as needed', '']:
            specificity_issues.append("Recycling frequency not specific")

        # Check composting requirements
        composting = requirements.get('composting', {})
        if composting.get('mandatory'):
            comp_capacity = composting.get('capacity_requirement', '')
            if any(term in str(comp_capacity).lower() for term in vague_terms):
                specificity_issues.append("Composting capacity uses vague terms")

        # Check penalties
        penalties = requirements.get('penalties', {})
        if not penalties.get('fine_per_offense') or '$' not in str(penalties.get('fine_per_offense')):
            specificity_issues.append("Penalty amounts not specified with $ values")

        if specificity_issues:
            for issue in specificity_issues:
                self.warnings.append(f"⚠️  SPECIFICITY: {issue}")

        self.validation_results['requirement_specificity'] = {
            'status': 'PASSED' if len(specificity_issues) == 0 else 'WARNING',
            'issues_found': len(specificity_issues),
            'issues': specificity_issues
        }

        return len(specificity_issues) == 0

    def validate_completeness(self, regulatory_data: Dict) -> bool:
        """Validate completeness of regulatory research"""

        requirements = regulatory_data.get('requirements', {})

        # Check all three waste streams are addressed
        waste_streams = ['waste', 'recycling', 'composting']
        missing_streams = []

        for stream in waste_streams:
            if stream not in requirements or not requirements[stream]:
                missing_streams.append(stream)

        if missing_streams:
            self.warnings.append(
                f"⚠️  INCOMPLETE RESEARCH: Missing waste streams: {', '.join(missing_streams)}"
            )

        # Check for licensed haulers
        haulers = regulatory_data.get('licensed_haulers', [])
        if len(haulers) < 3:
            self.warnings.append(
                f"⚠️  INSUFFICIENT HAULERS: Only {len(haulers)} licensed haulers found. "
                f"Minimum 3 recommended."
            )

        # Check for ordinance citations
        ordinances = regulatory_data.get('ordinances', [])
        if len(ordinances) == 0:
            self.errors.append(
                "❌ NO ORDINANCE CITATIONS: No ordinances referenced in research"
            )
            return False

        self.validation_results['completeness'] = {
            'status': 'PASSED' if len(missing_streams) == 0 else 'WARNING',
            'waste_streams_covered': len(waste_streams) - len(missing_streams),
            'haulers_found': len(haulers),
            'ordinances_cited': len(ordinances)
        }

        return len(missing_streams) <= 1  # Allow 1 missing stream

    def assess_confidence(self, location_valid: bool, sources_valid: bool,
                         specificity_valid: bool, completeness_valid: bool) -> str:
        """
        Assess overall confidence level for regulatory research
        Returns: 'HIGH', 'MEDIUM', or 'LOW'
        """

        # Count validations passed
        validations_passed = sum([
            location_valid,
            sources_valid,
            specificity_valid,
            completeness_valid
        ])

        # Get detailed metrics
        source_quality = self.validation_results.get('source_quality', {})
        requirement_specificity = self.validation_results.get('requirement_specificity', {})
        completeness = self.validation_results.get('completeness', {})

        gov_sources = source_quality.get('gov_sources', 0)
        specificity_issues = requirement_specificity.get('issues_found', 0)
        haulers_found = completeness.get('haulers_found', 0)

        # HIGH CONFIDENCE criteria
        if (validations_passed == 4 and
            gov_sources >= 2 and
            specificity_issues == 0 and
            haulers_found >= 3):
            confidence = 'HIGH'

        # MEDIUM CONFIDENCE criteria
        elif (validations_passed >= 3 and
              gov_sources >= 1 and
              specificity_issues <= 2):
            confidence = 'MEDIUM'

        # LOW CONFIDENCE
        else:
            confidence = 'LOW'

        self.confidence_score = confidence

        self.validation_results['confidence_assessment'] = {
            'level': confidence,
            'validations_passed': f"{validations_passed}/4",
            'gov_sources': gov_sources,
            'specificity_issues': specificity_issues,
            'haulers_found': haulers_found
        }

        return confidence
```

### Integration with Main Validator

```python
class WasteWiseValidator:
    """Comprehensive validation framework for WasteWise Analysis"""

    def __init__(self):
        self.validation_results = {
            'contract_validation': {},
            'optimization_validation': {},
            'formula_validation': {},
            'sheet_structure_validation': {},
            'data_completeness_validation': {},
            'cross_validation': {},
            'regulatory_compliance_validation': {}  # NEW
        }
        self.errors = []
        self.warnings = []
        self.regulatory_validator = RegulatoryComplianceValidator()  # NEW

    def validate_all(self, invoice_data: List[Dict], contract_data: Dict,
                     property_info: Dict, optimization_results: Dict,
                     regulatory_data: Dict) -> Tuple[bool, Dict]:  # NEW parameter
        """
        Run all validation checks including regulatory compliance
        Returns: (passed: bool, validation_report: dict)
        """

        # 1-6. Original validations (contract, optimization, formula, etc.)
        contract_valid = self.validate_contract(contract_data, invoice_data)
        optimization_valid = self.validate_optimizations(optimization_results, invoice_data)
        formula_valid = self.validate_formulas(invoice_data, property_info)
        structure_valid = self.validate_sheet_structure(
            invoice_data, contract_data, optimization_results, regulatory_data  # NEW
        )
        completeness_valid = self.validate_data_completeness(
            invoice_data, property_info
        )
        cross_valid = self.validate_cross_references(
            invoice_data, optimization_results, contract_data
        )

        # 7. NEW: Regulatory compliance validation
        regulatory_valid, confidence_level = self.regulatory_validator.validate_regulatory_research(
            regulatory_data, property_info
        )

        # Store regulatory validation results
        self.validation_results['regulatory_compliance_validation'] = {
            'status': 'PASSED' if regulatory_valid else 'FAILED',
            'confidence_level': confidence_level,
            'details': self.regulatory_validator.validation_results
        }

        # Merge errors and warnings from regulatory validator
        self.errors.extend(self.regulatory_validator.errors)
        self.warnings.extend(self.regulatory_validator.warnings)

        all_passed = all([
            contract_valid,
            optimization_valid,
            formula_valid,
            structure_valid,
            completeness_valid,
            cross_valid,
            regulatory_valid  # NEW
        ])

        return all_passed, self.generate_validation_report()
```

## EXPENSE_ANALYSIS Sheet Structure

**CRITICAL FORMAT REQUIREMENT:** Expense analysis must be displayed in detailed monthly groupings with line-item breakdowns and subtotals for each month.

### Required Column Headers
```
Month | Vendor | Service Type | Invoice Number | Amount | Cost/Door | Notes
```

### Format Rules

1. **Month Grouping:**
   - Group all line items by month (e.g., "October 2024")
   - Each month section contains multiple rows (one per line item)
   - Month name appears in first column of first row only

2. **Line Item Rows:**
   - Each service/invoice gets its own row
   - Format: `Month | Vendor | Service Type | Invoice Number | $Amount | $CPD | Description`
   - Example: `October 2024 | Ally Waste | Bulk Trash Removal | 41953 | $909.33 | $5.05 | Monthly bulk trash removal service`

3. **Monthly Subtotal Row:**
   - Immediately follows last line item for that month
   - Format: `[MONTH YEAR] TOTAL: | [blank] | [blank] | [blank] | $X,XXX.XX | $XX.XX | Monthly budget: $XX.XX/door`
   - Example: `October 2024 TOTAL: | | | | $909.33 | $5.05 | Monthly budget: $5.05/door`
   - Leave vendor, service type, and invoice columns blank
   - Include descriptive text: "Monthly budget: $X.XX/door"

4. **Grand Total Row:**
   - Appears at end of all months
   - Format: `GRAND TOTAL: | [blank] | [blank] | [blank] | $XXX,XXX.XX | $XX.XX | Avg monthly budget: $XX.XX/door`
   - Summarizes entire analysis period
   - Shows average cost per door across all months

5. **Amount Formatting:**
   - All dollar amounts with comma separators: `$1,234.56`
   - Cost per door rounded to 2 decimals: `$12.34`

6. **Notes Column:**
   - Line items: Descriptive service information
   - Subtotals: "Monthly budget: $XX.XX/door"
   - Grand total: "Avg monthly budget: $XX.XX/door"

### Example Output Structure

```
DETAILED MONTHLY EXPENSE ANALYSIS

Month              Vendor              Service Type           Invoice Number    Amount        Cost/Door    Notes
October 2024       Ally Waste          Bulk Trash Removal     41953            $909.33       $5.05        Monthly bulk trash removal service
                   October 2024 TOTAL:                                         $909.33       $5.05        Monthly budget: $5.05/door

November 2024      Waste Management    Dumpster Hauling       5998169-1571-5   $1,388.51     $7.71        Regular waste hauling service
November 2024      Waste Management    Compactor Service      RI1370230        $500.44       $2.78        Compactor maintenance and service fees
November 2024      Ally Waste          Bulk Trash Removal     43819            $368.55       $2.05        Monthly bulk trash removal service
                   November 2024 TOTAL:                                        $2,257.50     $12.54       Monthly budget: $12.54/door

December 2024      Waste Management    Compactor Service      RI1376420        $506.87       $2.82        Compactor maintenance and service fees
December 2024      Ally Waste          Bulk Trash Removal     46450            $563.55       $3.13        Monthly bulk trash removal service
December 2024      Waste Management    Dumpster Hauling       N/A              $506.87       $2.82        Regular waste hauling service
December 2024      Waste Management    Dumpster Hauling       N/A              $1,825.12     $10.14       Regular waste hauling service
                   December 2024 TOTAL:                                        $3,402.41     $18.90       Monthly budget: $18.90/door

                   GRAND TOTAL:                                                $34,460.72    $14.73       Avg monthly budget: $14.73/door
```

### Visual Presentation Requirements

1. **Clear Month Boundaries:**
   - Blank row between months (optional but recommended)
   - Month subtotal row visually distinct (can use bold or borders)

2. **Alignment:**
   - Month/Vendor/Service Type: Left-aligned
   - Amounts: Right-aligned with consistent decimal places
   - Invoice numbers: Left-aligned

3. **Data Source:**
   - Use ACTUAL invoice data from CSV files
   - Each row represents a real invoice line item
   - Month totals are SUM of line items for that month
   - Grand total is SUM of all monthly totals

4. **Sorting:**
   - Primary: Chronological by month
   - Secondary: By vendor within each month (alphabetical)
   - Tertiary: By service type within vendor

### Validation Checks for EXPENSE_ANALYSIS

```
☐ Each month has at least one line item
☐ Monthly subtotal equals sum of line items for that month
☐ Grand total equals sum of all monthly subtotals
☐ Cost per door = Amount / Unit count (consistent across all rows)
☐ All amounts formatted with $ and commas
☐ No missing months in date range
☐ Invoice numbers present (or "N/A" if not available)
☐ Service types are descriptive and consistent
☐ Notes column provides context for each line item
☐ Monthly budget notation included in subtotal rows
```

**IMPORTANT:** This format shows ACTUAL monthly expenses with real cost fluctuations. Do NOT use averages or repeat the same amount across months. Users need to see seasonal surcharges, rate changes, partial months, and holiday fees to identify billing anomalies and cost trends.

## REGULATORY_COMPLIANCE Sheet Structure

**CRITICAL FORMAT REQUIREMENT:** Regulatory compliance section must be presented in a structured, table-based format with clear sections and actionable checklists.

### Section 1: Header and Ordinance Status

```
[CITY/JURISDICTION] RECYCLING/WASTE ORDINANCE COMPLIANCE

Property: [Property Name] ([X] units)

Ordinance Status: ✅ APPLICABLE / ⚠️ NOT APPLICABLE / 📋 UNDER REVIEW
    - [Brief explanation of applicability based on unit threshold]

Compliance Deadline: [Date] ([property size threshold])
```

### Section 2: Ordinance Overview

```
ORDINANCE OVERVIEW

[2-3 sentence summary of the ordinance, including jurisdiction's waste reduction goals]

Key Dates:
• [Date 1]: [Milestone or threshold requirement]
• [Date 2]: [Milestone or threshold requirement]
• [Date 3]: [Milestone or threshold requirement]
```

### Section 3: Mandatory Requirements Table

**Table Format:**

| Requirement | Description | Verification Status |
|-------------|-------------|-------------------|
| [Requirement 1] | [Detailed description] | VERIFY ON-SITE / VERIFY WITH VENDOR / VERIFY SUBMISSION |
| [Requirement 2] | [Detailed description] | VERIFY ON-SITE / VERIFY WITH VENDOR / VERIFY SUBMISSION |
| [Requirement 3] | [Detailed description] | VERIFY ON-SITE / VERIFY WITH VENDOR / VERIFY SUBMISSION |

**Example:**
| Requirement | Description | Verification Status |
|-------------|-------------|-------------------|
| Recycling Container | Must provide dedicated recycling container(s) accessible to all residents | VERIFY ON-SITE |
| Collection Service | Must arrange for regular collection of recyclable materials | VERIFY WITH VENDOR |
| Verification Records | Must maintain and submit verification records to the city annually | VERIFY SUBMISSION |
| Container Signage | Containers must have clear signage indicating recyclable materials | VERIFY ON-SITE |
| Resident Access | Recycling must be as convenient as trash disposal | VERIFY ON-SITE |

### Section 4: Compliance Checklist Table

**Table Format:**

| Item | Status | Priority | Action Required |
|------|--------|----------|----------------|
| [Compliance item 1] | ✅ COMPLIANT / ⚠️ VERIFY / ❌ NON-COMPLIANT / 📋 RECOMMENDED | HIGH / MEDIUM / LOW | [Specific action needed] |
| [Compliance item 2] | ✅ COMPLIANT / ⚠️ VERIFY / ❌ NON-COMPLIANT / 📋 RECOMMENDED | HIGH / MEDIUM / LOW | [Specific action needed] |

**Status Icons:**
- ✅ COMPLIANT: Verified as meeting requirement
- ⚠️ VERIFY: Requires site inspection or documentation review
- ❌ NON-COMPLIANT: Confirmed violation requiring immediate action
- 📋 RECOMMENDED: Best practice, not mandatory

**Priority Levels:**
- HIGH: Mandatory requirement with enforcement
- MEDIUM: Required but with grace period or lower enforcement priority
- LOW: Recommended best practice

**Example:**
| Item | Status | Priority | Action Required |
|------|--------|----------|----------------|
| Recycling container provided | ⚠️ VERIFY | HIGH | Schedule site inspection and verify compliance |
| Collection service arranged | ⚠️ VERIFY | HIGH | Confirm active recycling service with vendor |
| Verification records submitted | ⚠️ VERIFY | MEDIUM | Review city submission requirements and deadlines |
| Container locations comply | ⚠️ VERIFY | MEDIUM | Verify placement meets accessibility requirements |
| Resident education program | 📋 RECOMMENDED | LOW | Consider implementing resident education materials |

### Section 5: Licensed Haulers Table

**Table Format:**

| Company | Phone | Services | Website |
|---------|-------|----------|---------|
| [Company Name 1] | [Phone] | [Service types] | [URL] |
| [Company Name 2] | [Phone] | [Service types] | [URL] |
| [Company Name 3] | [Phone] | [Service types] | [URL] |

**Service Types:** Waste & Recycling, Commercial Waste & Recycling, Compactor Service, Composting/Organics

**Example:**
| Company | Phone | Services | Website |
|---------|-------|----------|---------|
| Waste Connections of Florida | 407-261-5000 | Waste & Recycling | www.wasteconnections.com/orlando |
| Waste Management | 407-857-5500 | Commercial Waste & Recycling | www.wm.com |
| Haulla Waste Services | (contact via website) | Commercial Waste & Recycling | www.haulla.com |
| City of Orlando Solid Waste | 407-246-2314 | Residential & Commercial Options | www.orlando.gov/trash-recycling |

### Section 6: Penalties & Enforcement

```
PENALTIES & ENFORCEMENT

Classification: [Municipal code violation / Civil infraction / Misdemeanor]

Enforcement Agency: [Full agency name]
Contact: [Name, Title] | [Phone] | [Email]

Fine Structure:
    [Description of fine structure - per offense, per day, maximum amounts]
    [If not publicly specified, note that enforcement is through compliance verification]
```

**Example:**
```
PENALTIES & ENFORCEMENT

Classification: Municipal code violation

Enforcement Agency: City of Orlando Solid Waste Management Division
Contact: Joseph England, Sustainability Project Manager | 407-246-2314 | joseph.england@orlando.gov

Fine Structure:
    Not publicly specified - enforcement through compliance verification
```

### Section 7: Sources Consulted

**Numbered List Format:**

```
SOURCES CONSULTED

1. [Official source 1 title and link]
2. [Official source 2 title and link]
3. [Official source 3 title and link]
4. [Additional source 4 title and link]
```

**Source Priority:**
1. Official government ordinances and codes (.gov)
2. Municipal department policy pages
3. State environmental agency guidance
4. Industry publications covering ordinance implementation

**Example:**
```
SOURCES CONSULTED

1. City of Orlando Commercial & Multifamily Recycling Policy
2. Orlando Ordinance 2019-08
3. Waste Dive: Orlando mandating commercial and multi-unit residential recycling
4. The Recycling Partnership: Expanding Equitable Recycling Access in Orlando
```

### Visual Formatting Requirements

1. **Use Clear Section Headers:** All-caps for main sections
2. **Table Formatting:** Clean borders, header row with bold text
3. **Status Icons:** Use emoji indicators (✅ ⚠️ ❌ 📋) consistently
4. **Contact Information:** Name | Phone | Email format with pipe separators
5. **Bullet Points:** Use bullet points (•) for lists within sections
6. **Hyperlinks:** Include full URLs for all web references

### Validation Checks for REGULATORY_COMPLIANCE

```
☐ Property name and unit count displayed in header
☐ Ordinance applicability clearly stated with reasoning
☐ Compliance deadline specified (if applicable)
☐ Ordinance overview includes jurisdiction's waste goals
☐ Key dates listed chronologically
☐ Mandatory requirements table includes 3-5 key items
☐ All requirements have verification status assigned
☐ Compliance checklist includes 5-8 actionable items
☐ Each checklist item has status, priority, and action
☐ Licensed haulers table includes minimum 3-4 providers
☐ All hauler entries have phone and services listed
☐ Enforcement agency and contact person identified
☐ Fine structure or enforcement approach documented
☐ Minimum 3-4 sources consulted and cited
☐ At least 1 official .gov source included
```

### Research Quality Requirements

**HIGH Confidence:**
- Official ordinance text cited with chapter/section numbers
- All requirements verified against primary sources (.gov)
- 4+ licensed haulers identified with complete contact info
- Enforcement penalties documented with specific amounts
- Recent regulatory changes (2023-2025) confirmed

**MEDIUM Confidence:**
- Core requirements found but some details incomplete
- 2-3 official sources consulted
- 3+ licensed haulers identified
- Enforcement approach described (even if fines not specified)

**LOW Confidence - FLAG FOR MANUAL REVIEW:**
- Limited official information available
- Conflicting sources found
- Fewer than 3 licensed haulers identified
- Key requirements vague or missing
- Recent changes unconfirmed

**IMPORTANT:** If research confidence is LOW, include a warning box at the top of the regulatory section:

```
⚠️ MANUAL VERIFICATION REQUIRED
This regulatory research requires human review due to [list specific issues].
Recommend contacting [Agency Name] at [phone] for verification.
```

## Complete Workflow with Regulatory Compliance

### Step 1: Initial Data Processing
1. Process uploaded invoices
2. Extract contract (if provided)
3. **NEW:** Extract location data from property documents
4. Identify property characteristics (units, type, building height)

### Step 2: Regulatory Research Phase
1. Execute search pattern sequence
2. Consult minimum 3 official sources
3. Extract waste, recycling, and organics requirements
4. Document penalties and licensed haulers
5. Generate compliance checklists
6. Assign confidence score

### Step 3: Comprehensive Validation
1. Run contract validation
2. Run optimization validation
3. Run formula validation
4. Run sheet structure validation
5. Run data completeness validation
6. Run cross-validation
7. **NEW:** Run regulatory compliance validation
8. Assess overall confidence level

### Step 4: Validation Gate
- **HIGH/MEDIUM Confidence:** Proceed to output
- **LOW Confidence:** HALT and flag for human review

### Step 5: Generate Output
1. Create all standard sheets (SUMMARY, EXPENSE_ANALYSIS, OPTIMIZATION, etc.)
2. **NEW:** Create REGULATORY_COMPLIANCE sheet
3. Create QUALITY_CHECK sheet with regulatory confidence score
4. Generate executive summary with compliance status

## Enhanced Validation Report Example

```
🔐 STEP 3: Validation Gate - Running All Checks...
------------------------------------------------------------

📊 VALIDATION RESULTS:
   ✅ Contract Validation: PASSED
   ✅ Optimization Validation: PASSED
   ✅ Formula Validation: PASSED
   ✅ Sheet Structure Validation: PASSED
   ✅ Data Completeness Validation: PASSED
   ✅ Cross Validation: PASSED
   ✅ Regulatory Compliance Validation: PASSED (CONFIDENCE: HIGH)

🏛️ REGULATORY RESEARCH SUMMARY:
   Location: Austin, Texas
   Sources Consulted: 5 (.gov: 3, Other: 2)
   Ordinances Cited: 3
   Licensed Haulers Found: 6
   Confidence Level: HIGH

   Key Findings:
   ✅ Universal Recycling Ordinance applies (8+ units)
   ✅ Mandatory composting effective January 2024
   ✅ Minimum 1:1 recycling:waste capacity ratio required
   ⚠️  Annual reporting required by February 1, 2026

⚠️  WARNINGS:
   ⚠️  Property may need additional compost capacity
   ⚠️  Annual reporting deadline in 85 days

============================================================
VALIDATION SUMMARY:
   Total Checks: 7
   Passed: 7
   Failed: 0
   Warnings: 2
   Regulatory Confidence: HIGH
============================================================

✅ ALL VALIDATIONS PASSED - Proceeding to output generation
```

## Low Confidence Example - Human Review Required

```
🔐 STEP 3: Validation Gate - Running All Checks...
------------------------------------------------------------

📊 VALIDATION RESULTS:
   ✅ Contract Validation: PASSED
   ✅ Optimization Validation: PASSED
   ✅ Formula Validation: PASSED
   ✅ Sheet Structure Validation: PASSED
   ✅ Data Completeness Validation: PASSED
   ✅ Cross Validation: PASSED
   ❌ Regulatory Compliance Validation: FAILED (CONFIDENCE: LOW)

🏛️ REGULATORY RESEARCH SUMMARY:
   Location: [City], [State]
   Sources Consulted: 2 (.gov: 0, Other: 2)
   Ordinances Cited: 0
   Licensed Haulers Found: 1
   Confidence Level: LOW

   Issues Identified:
   ❌ No official .gov sources found
   ❌ No ordinance citations located
   ❌ Insufficient hauler information
   ⚠️  Conflicting information on composting mandate
   ⚠️  Recent ordinance changes (2024) not confirmed

🚨 HUMAN REVIEW REQUIRED 🚨

The regulatory compliance research did not meet minimum quality
standards for automated assessment. Manual verification needed for:

1. Composting mandate status (conflicting sources)
2. Property size threshold applicability
3. Enforcement penalties (not documented)
4. Licensed hauler requirements

Recommend: Contact [City] Solid Waste Department directly
Phone: [If available]
Website: [If available]

============================================================
VALIDATION SUMMARY:
   Total Checks: 7
   Passed: 6
   Failed: 1
   Warnings: 4
   Regulatory Confidence: LOW - MANUAL REVIEW REQUIRED
============================================================

❌ VALIDATION FAILED - Output generation halted
Please complete manual regulatory verification before proceeding.
```

## Required Libraries

- **anthropic** - Claude API for document processing and web research
- **pandas** - Data manipulation and analysis
- **openpyxl** - Excel workbook generation with formatting
- **python-dateutil** - Date parsing and calendar calculations
- **typing** - Type hints for validation functions
- **requests** - Web research for regulatory compliance
- **beautifulsoup4** - HTML parsing for ordinance extraction

## Example Usage

**User prompt**: "I uploaded 6 months of invoices, the waste service contract, and property documents for The Club at Millenia (560 units, Austin TX). Run the validated analysis with regulatory compliance research."

**Claude will**:
1. ✅ Process all invoices and extract contract
2. ✅ Extract location data (Austin, Travis County, Texas)
3. ✅ Research Austin waste/recycling/composting ordinances
4. ✅ Consult official sources (austintexas.gov, Travis County)
5. ✅ Extract Universal Recycling Ordinance requirements
6. ✅ Document composting mandate (effective 2024)
7. ✅ Identify 5+ licensed haulers
8. ✅ Run comprehensive validation suite (7 categories, 40+ checks)
9. ✅ Assign confidence level (HIGH/MEDIUM/LOW)
10. ✅ **HALT if LOW confidence or any validation fails**
11. ✅ Generate REGULATORY_COMPLIANCE sheet
12. ✅ Generate CONTRACT_TERMS sheet
13. ✅ Create HAUL_LOG if compactor detected
14. ✅ Validate all formulas and calculations
15. ✅ Cross-reference data across sheets
16. ✅ Generate validated Excel workbook with quality report

**Output files**:
- `TheClubAtMillenia_WasteAnalysis_Validated.xlsx` - Complete workbook with all sheets including regulatory compliance
- Executive summary with validation status and regulatory confidence level

## Key Principles

1. **Validation-First** - No output until ALL checks pass (including regulatory)
2. **Research Quality** - Minimum 3 sources, preference for .gov domains
3. **Specificity Required** - Vague terms trigger warnings or failures
4. **Confidence Transparency** - Clear scoring of research quality
5. **Human-in-the-Loop** - LOW confidence requires manual review
6. **Contract-Aware** - Mandatory CONTRACT_TERMS if contract provided
7. **Compliance-Focused** - Property-specific regulatory checklists
8. **Formula Accuracy** - Validates every calculation
9. **Cross-Referenced** - Ensures data consistency across sheets
10. **Quality Assurance** - Built-in QUALITY_CHECK sheet with regulatory confidence

This enhanced validated edition provides enterprise-grade quality control for waste management analysis with comprehensive regulatory compliance research.
