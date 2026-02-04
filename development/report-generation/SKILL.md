---
name: "report-generation"
description: "Generate Slovak VAT Act 2025 compliant reports for business trip tax deductions with automatic validation"
---

# Skill 5: Report Generation

## Purpose
Generate Slovak VAT Act 2025 compliant reports for business trip tax deductions. Automatically validate compliance before generating CSV exports.

## Activation Triggers
- "generate report"
- "export CSV"
- "November report"
- "business trips this month"
- "create tax report"

## Workflow

1. **Filter trips** by date range, vehicle, and purpose (Business/Personal/All)
2. **Run compliance check** against Slovak VAT Act 2025 requirements
3. **Generate CSV** with mandatory tax deduction fields
4. **Show summary** with statistics and compliance status
5. **Save to** ~/Documents/MileageLog/reports/

## Slovak VAT Act 2025 Compliance Verification

Before generating any report, ALWAYS display compliance checklist:

```
🇸🇰 Slovak VAT Act 2025 Compliance Check:
✅ VIN included (17 chars, no I/O/Q)
✅ Driver names present (all 15 trips)
✅ L/100km format (not km/L)
✅ Business descriptions complete (15/15)
✅ Trip timing separated from refuel

Report READY for tax deduction.
```

**If compliance issues detected:**
```
🇸🇰 Slovak VAT Act 2025 Compliance Check:
✅ VIN included
⚠️  Driver names missing (3 trips)
✅ L/100km format
❌ Business descriptions incomplete (2/15)

Report INCOMPLETE for tax deduction.
Fix issues before generating report? [Y/n]
```

## Mandatory CSV Fields (Slovak Tax Law)

Every business trip MUST include:
- **VIN**: 17-character vehicle identification number
- **Driver Name**: Full name of driver
- **Trip Start/End Datetime**: ISO 8601 format
- **Trip Start/End Location**: Separate from refuel location
- **Business Description**: Required for all business trips
- **Fuel Efficiency**: L/100km format (European standard)

## File Naming Convention

Format: `{license_plate}-{month}-{year}.csv`

Examples:
- BA-789XY-11-2025.csv (November 2025)
- BA-789XY-2025-Q4.csv (Quarter 4)
- BA-789XY-2025-full.csv (Full year)

## Summary Statistics Display

After generation, show:
```
Report Generated: BA-789XY-11-2025.csv
📊 Summary:
   • Total Distance: 4,920 km
   • Total Fuel: 418.2 L
   • Total Cost: €627.50
   • Avg Efficiency: 8.5 L/100km
   • Trip Count: 15 business trips

💾 Saved to: ~/Documents/MileageLog/reports/BA-789XY-11-2025.csv
```

## Handling Compliance Issues

**Missing VIN:**
→ Skill 1 (Vehicle Setup) to add VIN

**Missing Driver Names:**
→ Update trips manually or set default driver

**Business Description Missing:**
→ Prompt user to add descriptions before generating

**Wrong Format (km/L instead of L/100km):**
→ Auto-convert and warn user

## Related Skills

- **Skill 1**: Vehicle Setup (VIN requirement)
- **Skill 6**: Data Validation (pre-generation check)

## MCP Tools Used

- `car-log-core.list_trips` (filter by date/vehicle/purpose)
- `report-generator.generate_csv` (create compliant CSV)
