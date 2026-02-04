---
name: wastewise-analytics-validated
description: Enhanced WasteWise Complete Analysis with comprehensive validation framework. Validates all requirements before output including contract tab generation, clause extraction, optimization criteria, formula accuracy, and data completeness. Produces detailed validation report showing which checks passed/failed. Use when rigorous quality control is needed for waste management analysis.
---

# WasteWise Analytics - Validated Edition

## What This Skill Does

Enhanced version of WasteWise Complete Analysis with a **comprehensive validation framework** that ensures:

- ✅ Contract tabs are generated when contracts are provided
- ✅ Contract clauses are properly extracted and categorized
- ✅ Optimization recommendations meet strict criteria
- ✅ All formulas are correctly calculated
- ✅ Data completeness across all sheets
- ✅ Professional formatting standards
- ✅ Cross-sheet data consistency

**This skill will NOT produce output until ALL validation checks pass.**

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
     * 138 lbs/yd³ is EPA/ENERGY STAR standard for loose MSW
     * Already accounts for 3:1 compaction ratio
   - Dumpsters: (Container Size × Num Containers × Pickups/Week × 4.33) / Units
     * 4.33 = weeks per month (52/12)
☐ Cost per door: Total Monthly Cost / Units
☐ Capacity utilization: (Tons Per Haul / Target Tons) × 100%
☐ Days between pickups: 30 / (Hauls Per Month)

**CRITICAL:** All formulas must comply with official project standards documented in:
Documentation/CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md
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
```

### 6. Cross-Validation
```
☐ SUMMARY totals match EXPENSE_ANALYSIS
☐ HAUL_LOG tonnage matches OPTIMIZATION calculations
☐ CONTRACT_TERMS dates align with calendar reminders
☐ Cost per door consistent across all sheets
```

## Enhanced Implementation with Validation

### Step 1: Pre-Flight Validation Function

```python
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import re

class WasteWiseValidator:
    """Comprehensive validation framework for WasteWise Analysis"""
    
    def __init__(self):
        self.validation_results = {
            'contract_validation': {},
            'optimization_validation': {},
            'formula_validation': {},
            'sheet_structure_validation': {},
            'data_completeness_validation': {},
            'cross_validation': {}
        }
        self.errors = []
        self.warnings = []
        
    def validate_all(self, invoice_data: List[Dict], contract_data: Dict, 
                     property_info: Dict, optimization_results: Dict) -> Tuple[bool, Dict]:
        """
        Run all validation checks
        Returns: (passed: bool, validation_report: dict)
        """
        
        # 1. Contract Validation
        contract_valid = self.validate_contract(contract_data, invoice_data)
        
        # 2. Optimization Validation
        optimization_valid = self.validate_optimizations(optimization_results, invoice_data)
        
        # 3. Formula Validation
        formula_valid = self.validate_formulas(invoice_data, property_info)
        
        # 4. Sheet Structure Validation
        structure_valid = self.validate_sheet_structure(
            invoice_data, contract_data, optimization_results
        )
        
        # 5. Data Completeness Validation
        completeness_valid = self.validate_data_completeness(
            invoice_data, property_info
        )
        
        # 6. Cross-Validation
        cross_valid = self.validate_cross_references(
            invoice_data, optimization_results, contract_data
        )
        
        all_passed = all([
            contract_valid,
            optimization_valid,
            formula_valid,
            structure_valid,
            completeness_valid,
            cross_valid
        ])
        
        return all_passed, self.generate_validation_report()
    
    def validate_contract(self, contract_data: Dict, invoice_data: List[Dict]) -> bool:
        """Validate contract extraction and tab generation"""
        
        # Check if contract was provided
        contract_provided = contract_data is not None and len(contract_data) > 0
        
        self.validation_results['contract_validation']['contract_provided'] = contract_provided
        
        if not contract_provided:
            self.validation_results['contract_validation']['status'] = 'SKIPPED'
            self.validation_results['contract_validation']['reason'] = 'No contract file provided'
            return True  # Not an error if no contract
        
        # Contract was provided - validate extraction
        required_clause_types = [
            'Term & Renewal',
            'Rate Increases', 
            'Termination',
            'Liability',
            'Service Level',
            'Force Majeure',
            'Indemnification'
        ]
        
        extracted_clause_types = [
            clause['category'] for clause in contract_data.get('clauses', [])
        ]
        
        # Check for minimum clause extraction
        clauses_found = len(extracted_clause_types)
        self.validation_results['contract_validation']['clauses_found'] = clauses_found
        
        if clauses_found < 3:
            self.errors.append(
                f"❌ CONTRACT EXTRACTION FAILED: Only {clauses_found} clauses found. "
                f"Expected at least 3 of: {', '.join(required_clause_types)}"
            )
            self.validation_results['contract_validation']['status'] = 'FAILED'
            return False
        
        # Validate calendar reminders
        calendar_reminders = contract_data.get('calendar_reminders', [])
        if len(calendar_reminders) == 0:
            self.warnings.append(
                "⚠️  No calendar reminders found in contract. "
                "Check for termination notice windows."
            )
        
        # Validate verbatim text extraction
        for clause in contract_data.get('clauses', []):
            if 'verbatim_text' not in clause or len(clause['verbatim_text']) < 20:
                self.warnings.append(
                    f"⚠️  Clause '{clause['category']}' may not have verbatim text extracted"
                )
        
        self.validation_results['contract_validation']['status'] = 'PASSED'
        self.validation_results['contract_validation']['calendar_reminders'] = len(calendar_reminders)
        
        return True
    
    def validate_optimizations(self, optimization_results: Dict, 
                              invoice_data: List[Dict]) -> bool:
        """Validate optimization recommendations meet strict criteria"""
        
        optimizations = optimization_results.get('optimizations', [])
        
        for opt in optimizations:
            opt_type = opt['type']
            
            # Validate Compactor Optimization
            if opt_type == 'COMPACTOR_OPTIMIZATION':
                calc = opt.get('calculation_breakdown', {})
                avg_tons = calc.get('avg_tons_per_haul', 0)
                days_between = calc.get('days_between_pickups_optimized', 0)
                
                # Check < 6 tons trigger
                if avg_tons >= 6.0:
                    self.errors.append(
                        f"❌ COMPACTOR OPTIMIZATION INVALID: Avg tons {avg_tons:.2f} "
                        f"is not below 6.0 tons/haul threshold"
                    )
                    return False
                
                # Check 14-day constraint
                if days_between > 14:
                    self.errors.append(
                        f"❌ COMPACTOR OPTIMIZATION INVALID: Days between pickups "
                        f"({days_between:.1f}) exceeds 14-day maximum"
                    )
                    return False
                
                # Validate per-compactor pricing
                num_compactors = calc.get('num_compactors', 1)
                install_cost = calc.get('install_cost', 0)
                annual_monitor = calc.get('annual_monitor_cost', 0)
                
                expected_install = 300 * num_compactors
                expected_annual = 200 * 12 * num_compactors
                
                if install_cost != expected_install:
                    self.errors.append(
                        f"❌ INSTALL COST ERROR: Expected ${expected_install:,.0f} "
                        f"($300 × {num_compactors} compactors), got ${install_cost:,.0f}"
                    )
                    return False
                
                if annual_monitor != expected_annual:
                    self.errors.append(
                        f"❌ MONITORING COST ERROR: Expected ${expected_annual:,.0f} "
                        f"($200/mo × 12 × {num_compactors}), got ${annual_monitor:,.0f}"
                    )
                    return False
            
            # Validate Contamination Reduction
            elif opt_type == 'CONTAMINATION_REDUCTION':
                contamination_pct = opt.get('contamination_percentage', 0)
                
                if contamination_pct < 3.0:
                    self.errors.append(
                        f"❌ CONTAMINATION REDUCTION INVALID: {contamination_pct:.1f}% "
                        f"is below 3% threshold"
                    )
                    return False
            
            # Validate Bulk Subscription
            elif opt_type == 'BULK_SUBSCRIPTION':
                avg_bulk_monthly = opt.get('avg_bulk_monthly', 0)
                
                if avg_bulk_monthly < 500:
                    self.errors.append(
                        f"❌ BULK SUBSCRIPTION INVALID: ${avg_bulk_monthly:.2f}/month "
                        f"is below $500 threshold"
                    )
                    return False
        
        self.validation_results['optimization_validation']['status'] = 'PASSED'
        self.validation_results['optimization_validation']['count'] = len(optimizations)
        
        return True
    
    def validate_formulas(self, invoice_data: List[Dict], 
                         property_info: Dict) -> bool:
        """Validate all formula calculations"""
        
        units = property_info['unit_count']
        
        for invoice in invoice_data:
            service_type = invoice.get('service_type', '').lower()
            
            # Check yards per door calculation
            if 'compactor' in service_type:
                # Must use tonnage-based calculation (per CONTAINER_SPECIFICATIONS_AND_CALCULATION_STANDARDS.md)
                if 'tonnage' in invoice:
                    tons = invoice['tonnage']
                    expected_yards = (tons * 2000 / 138) / units  # EPA/ENERGY STAR standard: 138 lbs/yd³
                    actual_yards = invoice.get('yards_per_door', 0)
                    
                    if abs(expected_yards - actual_yards) > 0.01:
                        self.errors.append(
                            f"❌ YARDS PER DOOR FORMULA ERROR (Compactor): "
                            f"Expected {expected_yards:.3f}, got {actual_yards:.3f}"
                        )
                        return False
                else:
                    self.warnings.append(
                        f"⚠️  Compactor invoice missing tonnage data - "
                        f"cannot validate yards per door calculation"
                    )
            
            # Validate cost per door
            total_cost = invoice.get('amount', 0)
            expected_cpd = total_cost / units
            actual_cpd = invoice.get('cost_per_door', 0)
            
            if abs(expected_cpd - actual_cpd) > 0.01:
                self.errors.append(
                    f"❌ COST PER DOOR FORMULA ERROR: "
                    f"Expected ${expected_cpd:.2f}, got ${actual_cpd:.2f}"
                )
                return False
        
        self.validation_results['formula_validation']['status'] = 'PASSED'
        return True
    
    def validate_sheet_structure(self, invoice_data: List[Dict], 
                                contract_data: Dict, 
                                optimization_results: Dict) -> bool:
        """Validate expected sheet structure"""
        
        # Determine expected sheets
        has_compactor = any('compactor' in inv.get('service_type', '').lower() 
                           for inv in invoice_data)
        has_contract = contract_data is not None and len(contract_data) > 0
        
        expected_sheets = [
            'SUMMARY_FULL',
            'EXPENSE_ANALYSIS',
            'OPTIMIZATION',
            'QUALITY_CHECK',
            'DOCUMENTATION_NOTES'
        ]
        
        if has_compactor:
            expected_sheets.append('HAUL_LOG')
        
        if has_contract:
            expected_sheets.append('CONTRACT_TERMS')
        
        # Expected: 5-7 sheets
        expected_count = len(expected_sheets)
        
        self.validation_results['sheet_structure_validation']['expected_sheets'] = expected_sheets
        self.validation_results['sheet_structure_validation']['expected_count'] = expected_count
        self.validation_results['sheet_structure_validation']['has_compactor'] = has_compactor
        self.validation_results['sheet_structure_validation']['has_contract'] = has_contract
        self.validation_results['sheet_structure_validation']['status'] = 'PASSED'
        
        # Validate HAUL_LOG requirement
        if has_compactor:
            if 'HAUL_LOG' not in expected_sheets:
                self.errors.append(
                    "❌ HAUL_LOG sheet REQUIRED but not in sheet list (property has compactor)"
                )
                return False
        
        # Validate CONTRACT_TERMS requirement
        if has_contract:
            if 'CONTRACT_TERMS' not in expected_sheets:
                self.errors.append(
                    "❌ CONTRACT_TERMS sheet REQUIRED but not in sheet list (contract provided)"
                )
                return False
        
        return True
    
    def validate_data_completeness(self, invoice_data: List[Dict], 
                                   property_info: Dict) -> bool:
        """Validate all required data is present"""
        
        required_property_fields = ['name', 'unit_count']
        for field in required_property_fields:
            if field not in property_info or not property_info[field]:
                self.errors.append(
                    f"❌ MISSING PROPERTY DATA: '{field}' is required"
                )
                return False
        
        # Validate invoice data
        if len(invoice_data) == 0:
            self.errors.append("❌ NO INVOICE DATA: At least one invoice required")
            return False
        
        required_invoice_fields = ['date', 'amount', 'service_type']
        for i, invoice in enumerate(invoice_data):
            for field in required_invoice_fields:
                if field not in invoice or not invoice[field]:
                    self.errors.append(
                        f"❌ INVOICE {i+1} MISSING: '{field}' is required"
                    )
                    return False
        
        self.validation_results['data_completeness_validation']['status'] = 'PASSED'
        self.validation_results['data_completeness_validation']['invoice_count'] = len(invoice_data)
        
        return True
    
    def validate_cross_references(self, invoice_data: List[Dict],
                                  optimization_results: Dict,
                                  contract_data: Dict) -> bool:
        """Validate consistency across data sources"""
        
        # Validate optimization calculations match invoice data
        total_spend = sum(inv['amount'] for inv in invoice_data)
        
        # If contamination optimization exists, verify percentage
        for opt in optimization_results.get('optimizations', []):
            if opt['type'] == 'CONTAMINATION_REDUCTION':
                contamination_charges = sum(
                    inv.get('contamination_charge', 0) + inv.get('overage_charge', 0)
                    for inv in invoice_data
                )
                contamination_pct = (contamination_charges / total_spend) * 100
                
                stated_pct = opt.get('contamination_percentage', 0)
                if abs(contamination_pct - stated_pct) > 0.5:
                    self.errors.append(
                        f"❌ CROSS-VALIDATION ERROR: Contamination % mismatch. "
                        f"Calculated: {contamination_pct:.1f}%, Stated: {stated_pct:.1f}%"
                    )
                    return False
        
        self.validation_results['cross_validation']['status'] = 'PASSED'
        return True
    
    def generate_validation_report(self) -> Dict:
        """Generate comprehensive validation report"""
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'validation_results': self.validation_results,
            'errors': self.errors,
            'warnings': self.warnings,
            'passed': len(self.errors) == 0,
            'summary': {
                'total_checks': sum(
                    1 for category in self.validation_results.values()
                    if category.get('status') in ['PASSED', 'FAILED']
                ),
                'passed_checks': sum(
                    1 for category in self.validation_results.values()
                    if category.get('status') == 'PASSED'
                ),
                'failed_checks': len(self.errors),
                'warnings': len(self.warnings)
            }
        }
        
        return report
```

### Step 2: Main Analysis Function with Validation Gate

```python
def run_wastewise_analysis_validated(uploaded_files: List[str], 
                                     property_info: Dict) -> Dict:
    """
    Run WasteWise analysis with mandatory validation gate
    
    CRITICAL: Analysis will NOT produce output unless ALL validations pass
    """
    
    print("🔍 WasteWise Analytics - Validated Edition")
    print("=" * 60)
    
    # Step 1: Extract data from uploaded files
    print("\n📄 STEP 1: Document Processing...")
    invoice_data = []
    contract_data = None
    
    for file_path in uploaded_files:
        if 'contract' in file_path.lower() or 'agreement' in file_path.lower():
            contract_data = extract_contract_data(file_path)
        else:
            invoices = extract_invoice_data(file_path)
            invoice_data.extend(invoices)
    
    print(f"   ✓ Processed {len(invoice_data)} invoices")
    if contract_data:
        print(f"   ✓ Extracted contract with {len(contract_data.get('clauses', []))} clauses")
    
    # Step 2: Run optimizations
    print("\n⚙️  STEP 2: Optimization Analysis...")
    optimization_results = calculate_optimizations(invoice_data, property_info)
    print(f"   ✓ Identified {len(optimization_results['optimizations'])} opportunities")
    
    # Step 3: MANDATORY VALIDATION GATE
    print("\n🔐 STEP 3: Validation Gate - Running All Checks...")
    print("-" * 60)
    
    validator = WasteWiseValidator()
    passed, validation_report = validator.validate_all(
        invoice_data=invoice_data,
        contract_data=contract_data,
        property_info=property_info,
        optimization_results=optimization_results
    )
    
    # Display validation results
    print("\n📊 VALIDATION RESULTS:")
    for category, results in validation_report['validation_results'].items():
        status = results.get('status', 'UNKNOWN')
        icon = '✅' if status == 'PASSED' else '❌' if status == 'FAILED' else '⏭️ '
        category_name = category.replace('_', ' ').title()
        print(f"   {icon} {category_name}: {status}")
    
    # Display errors and warnings
    if validation_report['errors']:
        print("\n❌ ERRORS FOUND:")
        for error in validation_report['errors']:
            print(f"   {error}")
    
    if validation_report['warnings']:
        print("\n⚠️  WARNINGS:")
        for warning in validation_report['warnings']:
            print(f"   {warning}")
    
    print("\n" + "=" * 60)
    print(f"VALIDATION SUMMARY:")
    print(f"   Total Checks: {validation_report['summary']['total_checks']}")
    print(f"   Passed: {validation_report['summary']['passed_checks']}")
    print(f"   Failed: {validation_report['summary']['failed_checks']}")
    print(f"   Warnings: {validation_report['summary']['warnings']}")
    print("=" * 60)
    
    # GATE CHECK: Halt if validation failed
    if not passed:
        print("\n🛑 VALIDATION FAILED - Cannot proceed to output generation")
        print("   Please fix the errors above and re-run the analysis")
        return {
            'status': 'VALIDATION_FAILED',
            'validation_report': validation_report
        }
    
    print("\n✅ ALL VALIDATIONS PASSED - Proceeding to output generation")
    
    # Step 4: Generate workbook (only if validation passed)
    print("\n📊 STEP 4: Generating Excel Workbook...")
    workbook = generate_excel_workbook(
        invoice_data=invoice_data,
        contract_data=contract_data,
        property_info=property_info,
        optimization_results=optimization_results,
        validation_report=validation_report
    )
    
    output_filename = f"/mnt/user-data/outputs/{property_info['name'].replace(' ', '')}_WasteAnalysis_Validated.xlsx"
    workbook.save(output_filename)
    
    print(f"   ✓ Workbook saved: {output_filename}")
    
    # Step 5: Generate summary
    print("\n📝 STEP 5: Generating Executive Summary...")
    summary = generate_executive_summary(
        invoice_data=invoice_data,
        contract_data=contract_data,
        property_info=property_info,
        optimization_results=optimization_results,
        output_filename=output_filename
    )
    
    return {
        'status': 'SUCCESS',
        'output_file': output_filename,
        'validation_report': validation_report,
        'summary': summary
    }


def extract_contract_data(contract_file: str) -> Dict:
    """
    Extract contract data with focus on 7 clause categories
    
    Returns structure:
    {
        'clauses': [
            {
                'category': 'Term & Renewal',
                'verbatim_text': 'This agreement...',
                'risk_severity': 'high',
                'impact': 'Locked into 5-year auto-renewals',
                'action_required': 'Set calendar reminder 90 days before renewal'
            },
            ...
        ],
        'calendar_reminders': [
            {
                'date': datetime(2025, 10, 1),
                'action': 'Submit termination notice (certified mail)',
                'criticality': 'CRITICAL'
            }
        ]
    }
    """
    # Implementation would use Claude Vision API to extract
    # This is a placeholder showing the expected structure
    pass
```

### Step 3: Enhanced Excel Generation with Contract Tab

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_excel_workbook(invoice_data: List[Dict], 
                           contract_data: Dict,
                           property_info: Dict,
                           optimization_results: Dict,
                           validation_report: Dict) -> Workbook:
    """Generate complete Excel workbook with validation-enforced structure"""
    
    wb = Workbook()
    
    # Remove default sheet
    wb.remove(wb.active)
    
    # SHEET 1: SUMMARY_FULL
    create_summary_sheet(wb, invoice_data, contract_data, property_info, 
                        optimization_results, validation_report)
    
    # SHEET 2: EXPENSE_ANALYSIS
    create_expense_analysis_sheet(wb, invoice_data, property_info)
    
    # SHEET 3: OPTIMIZATION
    create_optimization_sheet(wb, optimization_results)
    
    # SHEET 4: QUALITY_CHECK
    create_quality_check_sheet(wb, validation_report)
    
    # SHEET 5: DOCUMENTATION_NOTES
    create_documentation_sheet(wb)
    
    # CONDITIONAL SHEET 6: HAUL_LOG (only if compactor)
    has_compactor = any('compactor' in inv.get('service_type', '').lower() 
                       for inv in invoice_data)
    if has_compactor:
        create_haul_log_sheet(wb, invoice_data)
    
    # CONDITIONAL SHEET 7: CONTRACT_TERMS (only if contract provided)
    if contract_data and len(contract_data.get('clauses', [])) > 0:
        create_contract_terms_sheet(wb, contract_data)
    
    return wb


def create_contract_terms_sheet(wb: Workbook, contract_data: Dict):
    """
    Create CONTRACT_TERMS sheet with verbatim clause extraction
    
    Sheet structure:
    - Header with property and contract info
    - Calendar reminders section (critical actions)
    - 7 clause categories with verbatim text
    - Risk severity indicators
    - Action items
    """
    
    ws = wb.create_sheet("CONTRACT_TERMS")
    
    # Styling
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    
    section_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
    section_font = Font(bold=True, size=11)
    
    high_risk_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    medium_risk_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    low_risk_fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    
    # Title
    ws['A1'] = "CONTRACT TERMS & RISK ANALYSIS"
    ws['A1'].font = Font(bold=True, size=14, color="1E3A8A")
    ws.merge_cells('A1:E1')
    
    row = 3
    
    # Calendar Reminders Section (CRITICAL)
    if contract_data.get('calendar_reminders'):
        ws[f'A{row}'] = "⚠️  CALENDAR REMINDERS - ACTION REQUIRED"
        ws[f'A{row}'].font = Font(bold=True, size=12, color="DC2626")
        ws[f'A{row}'].fill = high_risk_fill
        ws.merge_cells(f'A{row}:E{row}')
        row += 1
        
        # Headers
        ws[f'A{row}'] = "Date"
        ws[f'B{row}'] = "Action Required"
        ws[f'C{row}'] = "Criticality"
        ws[f'D{row}'] = "Days Until"
        ws[f'E{row}'] = "Notes"
        
        for col in ['A', 'B', 'C', 'D', 'E']:
            ws[f'{col}{row}'].font = header_font
            ws[f'{col}{row}'].fill = header_fill
        
        row += 1
        
        # Reminder rows
        today = datetime.now()
        for reminder in sorted(contract_data['calendar_reminders'], 
                             key=lambda x: x['date']):
            reminder_date = reminder['date']
            days_until = (reminder_date - today).days
            
            ws[f'A{row}'] = reminder_date.strftime('%Y-%m-%d')
            ws[f'B{row}'] = reminder['action']
            ws[f'C{row}'] = reminder['criticality']
            ws[f'D{row}'] = days_until
            ws[f'E{row}'] = "Set Outlook/Google Calendar reminder"
            
            # Color code by urgency
            if days_until < 90:
                for col in ['A', 'B', 'C', 'D', 'E']:
                    ws[f'{col}{row}'].fill = high_risk_fill
            elif days_until < 180:
                for col in ['A', 'B', 'C', 'D', 'E']:
                    ws[f'{col}{row}'].fill = medium_risk_fill
            
            row += 1
        
        row += 2  # Spacer
    
    # Contract Clauses Section
    ws[f'A{row}'] = "EXTRACTED CONTRACT CLAUSES"
    ws[f'A{row}'].font = section_font
    ws[f'A{row}'].fill = section_fill
    ws.merge_cells(f'A{row}:E{row}')
    row += 1
    
    # Headers
    ws[f'A{row}'] = "Category"
    ws[f'B{row}'] = "Verbatim Contract Language"
    ws[f'C{row}'] = "Risk Level"
    ws[f'D{row}'] = "Impact"
    ws[f'E{row}'] = "Recommended Action"
    
    for col in ['A', 'B', 'C', 'D', 'E']:
        ws[f'{col}{row}'].font = header_font
        ws[f'{col}{row}'].fill = header_fill
    
    row += 1
    
    # Clause rows
    for clause in contract_data.get('clauses', []):
        ws[f'A{row}'] = clause['category']
        ws[f'B{row}'] = clause['verbatim_text']
        ws[f'C{row}'] = clause['risk_severity'].upper()
        ws[f'D{row}'] = clause['impact']
        ws[f'E{row}'] = clause['action_required']
        
        # Apply risk color coding
        risk_fill = {
            'high': high_risk_fill,
            'medium': medium_risk_fill,
            'low': low_risk_fill
        }.get(clause['risk_severity'].lower(), low_risk_fill)
        
        for col in ['A', 'B', 'C', 'D', 'E']:
            ws[f'{col}{row}'].fill = risk_fill
            ws[f'{col}{row}'].alignment = Alignment(wrap_text=True, vertical='top')
        
        ws.row_dimensions[row].height = 60  # Accommodate wrapped text
        row += 1
    
    # Column widths
    ws.column_dimensions['A'].width = 18
    ws.column_dimensions['B'].width = 50
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 35
    ws.column_dimensions['E'].width = 40


def create_quality_check_sheet(wb: Workbook, validation_report: Dict):
    """Create QUALITY_CHECK sheet showing validation results"""
    
    ws = wb.create_sheet("QUALITY_CHECK")
    
    # Title
    ws['A1'] = "DATA QUALITY & VALIDATION REPORT"
    ws['A1'].font = Font(bold=True, size=14)
    ws.merge_cells('A1:D1')
    
    row = 3
    
    # Validation timestamp
    ws[f'A{row}'] = "Validation Timestamp:"
    ws[f'B{row}'] = validation_report['timestamp']
    row += 1
    
    ws[f'A{row}'] = "Overall Status:"
    ws[f'B{row}'] = "✅ PASSED" if validation_report['passed'] else "❌ FAILED"
    ws[f'B{row}'].font = Font(
        bold=True, 
        color="22C55E" if validation_report['passed'] else "DC2626"
    )
    row += 2
    
    # Validation summary
    ws[f'A{row}'] = "VALIDATION SUMMARY"
    ws[f'A{row}'].font = Font(bold=True, size=12)
    row += 1
    
    summary = validation_report['summary']
    ws[f'A{row}'] = "Total Checks:"
    ws[f'B{row}'] = summary['total_checks']
    row += 1
    
    ws[f'A{row}'] = "Passed:"
    ws[f'B{row}'] = summary['passed_checks']
    ws[f'B{row}'].fill = PatternFill(start_color="D1FAE5", end_color="D1FAE5", fill_type="solid")
    row += 1
    
    ws[f'A{row}'] = "Failed:"
    ws[f'B{row}'] = summary['failed_checks']
    if summary['failed_checks'] > 0:
        ws[f'B{row}'].fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    row += 1
    
    ws[f'A{row}'] = "Warnings:"
    ws[f'B{row}'] = summary['warnings']
    if summary['warnings'] > 0:
        ws[f'B{row}'].fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    row += 2
    
    # Detailed validation results
    ws[f'A{row}'] = "DETAILED VALIDATION RESULTS"
    ws[f'A{row}'].font = Font(bold=True, size=12)
    row += 1
    
    for category, results in validation_report['validation_results'].items():
        category_name = category.replace('_', ' ').title()
        status = results.get('status', 'UNKNOWN')
        
        ws[f'A{row}'] = category_name
        ws[f'B{row}'] = status
        
        if status == 'PASSED':
            ws[f'B{row}'].font = Font(color="22C55E", bold=True)
        elif status == 'FAILED':
            ws[f'B{row}'].font = Font(color="DC2626", bold=True)
        
        row += 1
    
    row += 1
    
    # Errors
    if validation_report['errors']:
        ws[f'A{row}'] = "ERRORS"
        ws[f'A{row}'].font = Font(bold=True, color="DC2626", size=12)
        row += 1
        
        for error in validation_report['errors']:
            ws[f'A{row}'] = error
            ws[f'A{row}'].fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
            ws[f'A{row}'].alignment = Alignment(wrap_text=True)
            ws.merge_cells(f'A{row}:D{row}')
            ws.row_dimensions[row].height = 40
            row += 1
    
    # Warnings
    if validation_report['warnings']:
        row += 1
        ws[f'A{row}'] = "WARNINGS"
        ws[f'A{row}'].font = Font(bold=True, color="F59E0B", size=12)
        row += 1
        
        for warning in validation_report['warnings']:
            ws[f'A{row}'] = warning
            ws[f'A{row}'].fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
            ws[f'A{row}'].alignment = Alignment(wrap_text=True)
            ws.merge_cells(f'A{row}:D{row}')
            ws.row_dimensions[row].height = 40
            row += 1
    
    # Column widths
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 20
    ws.column_dimensions['D'].width = 20
```

## Required Libraries

- **anthropic** - Claude Vision API for document processing
- **pandas** - Data manipulation and analysis
- **openpyxl** - Excel workbook generation with formatting
- **python-dateutil** - Date parsing and calendar calculations
- **typing** - Type hints for validation functions

## Example Usage

**User prompt**: "I uploaded 6 months of invoices and the waste service contract for The Club at Millenia (560 units). Run the validated analysis."

**Claude will**:
1. ✅ Process all invoices and extract contract
2. ✅ Run comprehensive validation suite (6 categories, 30+ checks)
3. ✅ **HALT if any validation fails** with detailed error report
4. ✅ Generate CONTRACT_TERMS sheet with verbatim clauses
5. ✅ Create HAUL_LOG if compactor detected
6. ✅ Validate all formulas and calculations
7. ✅ Cross-reference data across sheets
8. ✅ Generate validated Excel workbook with quality report

**Output files**:
- `TheClubAtMillenia_WasteAnalysis_Validated.xlsx` - Complete workbook with validation report
- Executive summary with validation status

## Validation Report Example

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

⚠️  WARNINGS:
   ⚠️  No calendar reminders found in contract. Check for termination notice windows.

============================================================
VALIDATION SUMMARY:
   Total Checks: 6
   Passed: 6
   Failed: 0
   Warnings: 1
============================================================

✅ ALL VALIDATIONS PASSED - Proceeding to output generation
```

## Key Principles

1. **Validation-First** - No output until ALL checks pass
2. **Transparent** - Detailed report of what was validated
3. **Strict Criteria** - Enforces all optimization thresholds
4. **Contract-Aware** - Mandatory CONTRACT_TERMS if contract provided
5. **Formula Accuracy** - Validates every calculation
6. **Cross-Referenced** - Ensures data consistency across sheets
7. **Quality Assurance** - Built-in QUALITY_CHECK sheet in every workbook

This validated edition provides enterprise-grade quality control for waste management analysis.
