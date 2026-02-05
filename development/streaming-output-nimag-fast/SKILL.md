---
name: streaming-output
description: Output format markers for the real-time stream formatter. Use when building prompts for streaming analysis to ensure proper progress display. Documents the patterns that StreamFormatter detects and displays.
allowed-tools:
  - Read
  - Grep
---

# Streaming Output Format

## Purpose
Define output markers that the `StreamFormatter` (`internal/agent/stream.go`) detects and displays as real-time progress.

## How It Works

The formatter buffers streaming text and uses regex patterns to detect phases and findings. When markers are found:
- **Status updates**: Overwrite a single line (using `\r`)
- **Findings**: Print on new lines (persist on screen)

## Required Output Markers

### Phase 0: Document Inventory (Immediate Feedback)
```
**📄 DOCUMENTS RECEIVED**
1. W2_2024.pdf - W-2 for John Smith, Employer: Acme Corp
2. paystub_jan.pdf - Pay period ending 01/15/2025
[etc...]
```

This should be output FIRST to provide immediate feedback while the model processes documents.

### Phase 1: Guideline Checks
```
**📋 GUIDELINE: B3-3.1-01 - Employment Documentation**
Requirement: [from guideline]
Finding: [what was found]
Status: ✅ COMPLIANT
```

Status options:
- `Status: ✅ COMPLIANT` → Shows green checkmark
- `Status: ⚠️ ISSUE` → Shows warning
- `Status: ❌ NON-COMPLIANT` → Shows error

### Phase 2: Cross-Validation
```
**🔍 CROSS-CHECK: W2 vs Paystubs**
Result: MATCH
```

Result options:
- `MATCH` (without MISMATCH nearby) → Shows "Match confirmed"
- `MISMATCH` → Shows warning "Mismatch detected"

### Phase 3: Income Calculation
```
**🧮 INCOME CALCULATION**
Base annual salary: $85,000.00
Total qualifying monthly income: $7,083.33
```

Extracted amounts (regex patterns):
- `base annual` or `base salary` followed by `$X,XXX.XX`
- `total qualifying monthly income` followed by `$X,XXX.XX`

### Phase 4: Issue Detection

These are detected automatically from natural language:

| Pattern | Display |
|---------|---------|
| "identical" + "ytd" | 🚨 FRAUD INDICATOR: Identical YTD |
| "Lorem Ipsum" or "placeholder text" | 🚨 FRAUD INDICATOR: Placeholder text |
| "conflicting" or "two different" | ⚠️ Conflicting document versions |
| "missing" + "document" | 📋 Missing required documentation |

### Phase 5: Final Determination
```
**✅ FINAL DETERMINATION**
Status: APPROVED
```

Status options:
- `Status: APPROVED` or `Status: ✅` → Shows ✅ APPROVED
- `Status: DENIED` or `Status: ❌` → Shows ❌ DENIED
- `Status: NEEDS REVIEW` or `Status: CONDITIONAL` → Shows ⚠️ NEEDS REVIEW

### Phase 6: Structured Extraction
```
Extracting structured results...
```

## Example Prompt Output

```
**📋 GUIDELINE: B3-3.1-01 - General Income Information**
Requirement: Verify stable income history for past 2 years
Finding: W2s provided for 2022 and 2023 showing consistent employment
Status: ✅ COMPLIANT

**📋 GUIDELINE: B3-3.1-03 - Base Pay Verification**
Requirement: Document current base salary with recent paystubs
Finding: Paystub dated 2024-01-15 shows base salary $85,000/year
Status: ✅ COMPLIANT

**🔍 CROSS-CHECK: W2 vs Paystubs**
W2 2023: $85,000 annual
Paystub YTD annualized: $85,000
Result: MATCH

**🧮 INCOME CALCULATION**
Base annual salary: $85,000.00
No additional income sources documented
Total qualifying monthly income: $7,083.33

**✅ FINAL DETERMINATION**
Status: APPROVED
Confidence: 0.92
```

## Display Output

The above produces this real-time display:
```
  ⏳ Checking B3-3.1-01 - General Income Information
  ✅ B3-3.1-01 - General Income Information: Compliant
  ⏳ Checking B3-3.1-03 - Base Pay Verification
  ✅ B3-3.1-03 - Base Pay Verification: Compliant
  ⏳ Cross-checking W2 vs Paystubs
  ✓ Document cross-check: Match confirmed
  ⏳ Calculating qualifying income...
  💰 Base salary: $85,000/year
  📈 Qualifying monthly income: $7,083.33
  ⏳ Making final determination...

  ✅ APPROVED
```

## Adding New Markers

To add new detected patterns, edit `internal/agent/stream.go`:

1. Add regex pattern in `parseAndDisplay()`
2. Add `sf.shown["key"]` check to prevent duplicates
3. Call `sf.updateStatus()` for transient status or `sf.printFinding()` for persistent findings

## Related Files
- `internal/agent/stream.go` - StreamFormatter implementation
- `internal/agent/income/income.go` - Example prompt using these markers
