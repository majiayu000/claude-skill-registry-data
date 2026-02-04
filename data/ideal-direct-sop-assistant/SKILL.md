---
name: ideal-direct-sop-assistant
description: Automate Ideal Direct finance and supply chain SOPs with browser-based workflow guidance. Handles payroll, working hours, purchase orders, and audits using Playwright MCP.
---

# Ideal Direct SOP Assistant

## Core Principle

**GUIDE, AUTOMATE, VALIDATE** - Walk users through Ideal Direct business processes with browser automation, data validation, and audit trail creation.

## When to Activate

Activate when user mentions:
- "payroll" + "joiners" or "leavers" or "A4G"
- "working hours" + "summary" or "payroll"
- "purchase order" or "PO" + "CU"
- "PDM audit" or "finance audit"
- "WorkSmarter" + any finance task
- "ideal direct" + any SOP reference

Also activate for:
- SOP numbers: F.4.B, F.4.E, F.18.A, SC.15.A
- Keywords: "new starter", "leaver", "A4G template", "fortnightly payroll"

## MCP Integration

This skill requires:
- **playwright**: Browser automation (WorkSmarter, SharePoint Excel, ClickUp)
- **filesystem**: Save reports, screenshots, audit files
- **mcp-response-optimization**: Token management (MUST be active)

**Critical:** MCP efficiency skill must be installed and active before using this skill to prevent token overflow from browser operations.

## Available SOPs

### SOP F.4.B: Add Joiners/Leavers to Payroll

**Purpose:** Update A4G payroll template with new starters and leavers from WorkSmarter

**When to use:** Fortnightly payroll processing, employee status changes

**Trigger phrases:**
- "Process payroll joiners and leavers"
- "Add new starter to payroll"
- "Update leaver in A4G template"
- "Run SOP F.4.B"

### SOP F.4.E: Summarise All Working Hours

**Purpose:** Collate hours and holidays from WorkSmarter into A4G template

**When to use:** Fortnightly payroll period, hours reconciliation

**Trigger phrases:**
- "Summarise working hours"
- "Collate hours and holidays"
- "Process payroll hours"
- "Run SOP F.4.E"

### SOP SC.15.A: Add Purchase Order to CU

**Purpose:** Add purchase orders to CU system (supply chain)

**When to use:** New purchase order processing

**Trigger phrases:**
- "Add purchase order"
- "Process PO in CU"
- "Run SOP SC.15.A"

### SOP F.18.A: PDM Audit

**Purpose:** Finance audit process for PDM

**When to use:** Regular audit cycles

**Trigger phrases:**
- "Run PDM audit"
- "Process finance audit"
- "Run SOP F.18.A"

## SOP F.4.B Workflow: Payroll Joiners/Leavers

### Step 1: Download WorkSmarter Report

**Action:** Retrieve joiners and leavers report

**Playwright Automation:**
```javascript
// Navigate to WorkSmarter
browser_navigate("https://worksmarter.com")
browser_click("Reports")
browser_click("Joiners and Leavers")
browser_click("Download")
```

**User Prompt:**
"I've automated opening WorkSmarter and downloading the joiners/leavers report. The file should now be in your Downloads folder. Let me know when you see it."

**Data to Extract:**
- New starters: Name, start date, salary, pay frequency
- Leavers: Name, leave date, length of service

**Validation:**
- Check if start date falls in current payroll period
- Verify leaver has termination date populated

### Step 2: Open SharePoint Payroll Template

**Action:** Navigate to Ideal Direct Finance folder and open A4G template

**Playwright Automation:**
```javascript
// Open SharePoint payroll template
browser_navigate("https://idealdirectuk.sharepoint.com/:x:/s/IdealDirectFinance/EUYMq4IOBGhEvkrT_4njTiwBVdMlgLbi0zaascp_Z0nKnw?e=KRWmZd")

// Wait for Excel Online to load
browser_wait_for({ text: "Ideal Direct Limited - Fortnightly Payroll Template" })
```

**User Instructions:**
1. Save as new copy
2. Rename for current fortnight (e.g., "Fortnight 8")
3. Confirm when template is open

**MCP Efficiency Rule:**
- DON'T extract full spreadsheet
- Only query specific cells when needed

### Step 3: Update Leaver Information

**Action:** Find leaver row and update status

**Playwright Automation:**
```javascript
// User provides leaver name (e.g., "Roy Keane")
// Search for employee in template
browser_click({ element: "Search box", ref: "employee_search" })
browser_type("Roy Keane")

// Navigate to Starter/Leaver field
browser_click({ element: "Starter/Leaver dropdown", ref: "status_dropdown" })
browser_select_option({ values: ["Leaver"] })

// Input leave date
browser_type("27/05/2025", { element: "Leave date field", ref: "leave_date" })
```

**Validation Checklist:**
- ✅ Leave date matches WorkSmarter report
- ✅ Status changed to "Leaver"
- ✅ Employee row found in template

**Screenshot Audit:**
```javascript
browser_take_screenshot({ path: "/outputs/leaver_updated.png" })
```

### Step 4: Add New Starter

**Action:** Insert new row and populate starter information

**Playwright Automation:**
```javascript
// Find last employee row
browser_click({ element: "Last employee row", ref: "last_row" })

// Insert new row
browser_click("Insert row below")

// Copy last employee format
browser_click("Copy row format")

// Input new starter details
browser_type("Juan Sebastien Veron", { element: "Employee name", ref: "name_field" })
browser_type("£12.50", { element: "Hourly rate", ref: "rate_field" })
browser_select_option({ element: "Pay type", values: ["Hourly"] })
browser_select_option({ element: "Status", values: ["Starter"] })
browser_type("27/05/2025", { element: "Start date", ref: "start_date" })
```

**Validation Checklist:**
- ✅ All fields populated from WorkSmarter report
- ✅ Pay type set correctly (Hourly/Salary)
- ✅ Start date matches payroll period

### Step 5: Verify Formula Ranges

**Action:** Ensure totals include new starter row

**Playwright Automation:**
```javascript
// Click total row at bottom
browser_click({ element: "Total hours cell", ref: "total_cell" })

// Verify formula includes new row
const formula = browser_evaluate("document.activeElement.value")
// Expected: =SUM(B2:B51) after adding Juan

// Check each total column
const columns_to_check = ["Hours", "Gross Pay", "Deductions"]
for (const col of columns_to_check) {
  browser_click({ element: `${col} total`, ref: `${col}_total` })
  // Verify formula range
}
```

**User Instructions:**
"Double-click each total cell to verify the formula includes the new row. The range should extend from B2 to B51 (or your last employee row)."

**Validation:**
- ✅ All total formulas updated
- ✅ New row included in calculations
- ✅ Gross total matches expected

**Screenshot Audit:**
```javascript
browser_take_screenshot({ path: "/outputs/formulas_verified.png" })
```

### Step 6: Save and Create ClickUp Task

**Action:** Save template and assign for manager review

**Playwright Automation:**
```javascript
// Save Excel template
browser_click("File → Save As")

// Open ClickUp
browser_navigate("https://app.clickup.com")
browser_click("New Task")

// Create review task
browser_type("Payroll Joiners/Leavers - Fortnight 8", { element: "Task name", ref: "task_name" })
browser_type("Ready for manager review. Template updated with:\n- Leaver: Roy Keane (27/05/25)\n- Starter: Juan Sebastien Veron (£12.50/hr)", { element: "Description", ref: "task_desc" })
browser_click("Attach link")
browser_type("sharepoint_template_url", { element: "Link URL", ref: "link_url" })
browser_click("Assign to: Line Manager")
browser_click("Create Task")
```

**Completion Message:**
```
✅ SOP F.4.B Complete

Updated:
- Leaver: Roy Keane (leave date: 27/05/25)
- New starter: Juan Sebastien Veron (£12.50/hr, start: 27/05/25)
- Formulas verified and updated
- ClickUp task created for manager review

Audit trail saved:
- /outputs/leaver_updated.png
- /outputs/formulas_verified.png

Next: Manager reviews and approves for A4G submission
```

## SOP F.4.E Workflow: Working Hours Summary

### Step 1: Download All Reports

**Action:** Retrieve hours, holidays, and absences from WorkSmarter

**Playwright Automation:**
```javascript
// Download approved hours
browser_navigate("https://worksmarter.com/reports/hours")
browser_click("Approved Hours")
browser_click("Download")

// Download holidays
browser_navigate("https://worksmarter.com/reports/holidays")
browser_click("Download")

// Download absences (if applicable)
browser_navigate("https://worksmarter.com/reports/absences")
browser_click("Download")
```

**User Prompt:**
"I've downloaded all three reports from WorkSmarter. Check your Downloads folder for:
- Approved hours report
- Holidays report
- Absences report (if any)

Open each file to verify data is for the correct payroll period."

### Step 2: Collate Data in Excel

**Action:** Combine reports into single summary sheet

**Playwright Automation:**
```javascript
// Open new Excel workbook in SharePoint
browser_navigate("sharepoint_working_hours_location")
browser_click("New → Excel Workbook")

// Create tabs
browser_click("Add Sheet")
browser_type("Hours", { element: "Sheet name", ref: "sheet_name" })
browser_click("Add Sheet")
browser_type("Holidays", { element: "Sheet name", ref: "sheet_name" })

// User pastes data from downloads into respective tabs
```

**User Instructions:**
1. Open downloaded Hours report
2. Copy data to "Hours" tab
3. Open downloaded Holidays report
4. Copy data to "Holidays" tab
5. Create "Total" column: =Hours + Holidays

**Validation:**
- ✅ All employee hours accounted for
- ✅ Holiday hours separated
- ✅ No absences to process (or processed if applicable)

### Step 3: Create Total Column

**Action:** Calculate combined hours + holidays

**Playwright Automation:**
```javascript
// Navigate to Summary tab
browser_click({ element: "Summary tab", ref: "summary_tab" })

// Create Total column header
browser_click("Cell C1")
browser_type("Total (Hours + Holidays)")

// Add formula for first employee
browser_click("Cell C2")
browser_type("=Hours!B2+Holidays!B2")

// Copy formula down for all employees
browser_click("C2")
browser_click("Copy")
browser_click("C2:C50")
browser_click("Paste")
```

**User Verification:**
"Check the Total column. It should show combined hours + holidays for each employee. Spot-check a few rows to ensure calculations are correct."

### Step 4: Update A4G Payroll Template

**Action:** Transfer totals to official payroll template

**Playwright Automation:**
```javascript
// Open previous week's A4G template
browser_navigate("sharepoint_a4g_template_location")

// Navigate to "Hours worked in pay period" column
browser_click({ element: "Column B header", ref: "hours_column" })

// User overwrites with new data from summary
```

**User Instructions:**
1. Copy Total column from summary sheet
2. Paste into "Hours worked in pay period" column (Column B) in A4G template
3. Verify totals match at bottom of template

**Validation:**
```javascript
// Compare summary total to template total
const summary_total = browser_locator(".summary-total").textContent()
const template_total = browser_locator(".template-total").textContent()

if (summary_total === template_total) {
  console.log("✅ Totals match - ready to save")
} else {
  console.log("❌ Totals don't match - check data entry")
}
```

### Step 5: Save and Send for Review

**Action:** Save template and notify line manager

**Playwright Automation:**
```javascript
// Save template
browser_click("File → Save")

// Take screenshot of totals for audit
browser_take_screenshot({ path: "/outputs/hours_summary_totals.png" })

// Create ClickUp task
browser_navigate("https://app.clickup.com")
browser_click("New Task")
browser_type("Working Hours Summary - Fortnight 8 - Ready for Review", { element: "Task name" })
browser_click("Assign to: Line Manager")
browser_click("Create Task")
```

**Completion Message:**
```
✅ SOP F.4.E Complete

Processed:
- Approved hours: [total hours]
- Holidays: [total holiday hours]
- Total combined: [total]

Verified:
- Summary totals match A4G template
- All employees accounted for
- Ready for manager review

Audit trail:
- /outputs/hours_summary_totals.png

Next: Manager reviews and approves for A4G submission
```

## Token Management Rules

**CRITICAL: This skill generates browser automation commands that can produce massive token responses. Follow these rules strictly.**

### Rule 1: Never Display Full Page Content

```javascript
// ❌ NEVER:
const page_html = browser_snapshot() // 50,000+ tokens

// ✅ ALWAYS:
browser_click({ element: "Employee name field", ref: "A45" })
// Returns: "Clicked cell A45" (10 tokens)
```

### Rule 2: Screenshots Save Only, Never Display

```javascript
// ❌ NEVER:
const screenshot = browser_take_screenshot()
// Returns base64 image = 125,000+ tokens

// ✅ ALWAYS:
browser_take_screenshot({ path: "/outputs/audit.png" })
// Returns: "Screenshot saved: /outputs/audit.png" (20 tokens)
```

### Rule 3: Target Specific Elements

```javascript
// ✅ Good - specific cell reference
browser_type("£12.50", { element: "Hourly rate", ref: "B45" })

// ❌ Bad - full table query
const table = browser_locator("table").innerHTML()
// 10,000+ tokens
```

### Rule 4: Limit Data Extraction

```javascript
// Only extract what you need to validate
const employee_count = browser_locator(".employee-row").count()
console.log(`Found ${employee_count} employees`)

// DON'T extract full employee list
```

### Rule 5: Save Large Responses to Files

```javascript
// If WorkSmarter returns large report
const report = browser_locator(".report-data").textContent()

// Save, don't display
filesystem.write_file({
  path: "/outputs/worksmarter_report.txt",
  content: report
})

return "Report saved: /outputs/worksmarter_report.txt"
```

## Token Budget per SOP

| SOP | Steps | Est. Tokens | Status |
|-----|-------|-------------|--------|
| F.4.B Payroll Joiners/Leavers | 6 | 1,500 | ✅ Safe |
| F.4.E Working Hours Summary | 5 | 1,800 | ✅ Safe |
| SC.15.A Purchase Order | TBD | <2,000 | Pending |
| F.18.A PDM Audit | TBD | <2,000 | Pending |

**Safe limit:** <2,000 tokens per complete SOP workflow

## Pre-Execution Checklist

Before starting any SOP:

1. ✅ MCP efficiency skill active?
2. ✅ User logged into WorkSmarter?
3. ✅ SharePoint access available?
4. ✅ ClickUp account accessible?
5. ✅ Downloads folder empty/organized?

**If all YES → Proceed with SOP**

## Error Handling

### If WorkSmarter Login Fails
```
"I couldn't access WorkSmarter. Please:
1. Open WorkSmarter manually
2. Log in
3. Tell me when you're logged in
Then I'll continue with the report download."
```

### If Excel Formula Doesn't Update
```
"The formula range didn't update automatically. Let's fix it manually:
1. Double-click the total cell
2. Update the range from B50 to B51 (or your last row)
3. Press Enter
4. Verify the new total includes all employees"
```

### If Totals Don't Match
```
"❌ Totals don't match:
- Summary: [X] hours
- Template: [Y] hours
- Difference: [Z] hours

Check:
1. All employees copied from summary?
2. Any duplicate entries?
3. Formula errors in Total column?

I can help investigate once you identify which employees are missing."
```

## Success Checklist

SOP completion is successful when:
- ✅ All data transferred from WorkSmarter
- ✅ Excel formulas updated correctly
- ✅ Totals verified and match
- ✅ Screenshots saved for audit
- ✅ ClickUp task created
- ✅ Manager notified
- ✅ Token usage stayed under 2,000

## Post-Execution

After SOP completion:
1. Review audit screenshots in /outputs/
2. Verify ClickUp task assigned correctly
3. Confirm manager received notification
4. Archive WorkSmarter downloads
5. Document any errors or edge cases

## Integration with Other Skills

Works best with:
- **mcp-response-optimization** (REQUIRED) - Token management
- **concise-execution-mode** - Minimal explanations for experienced users

## System Requirements

- Windows PC (tested environment)
- Chrome/Edge browser
- Active sessions:
  - WorkSmarter
  - SharePoint (Ideal Direct Finance folder)
  - ClickUp

## Definitions

**New Starter** - Person who has commenced employment with Ideal Direct
**Leaver** - Person who has ceased employment with Ideal Direct
**WorkSmarter** - Online HR system for hours, holidays, absences
**A4G Payroll Template** - Excel file sent to A4G for external payroll processing
**Fortnight** - Two-week payroll period

## Training Recommendations

For new users:
1. Run SOP F.4.B once with supervision
2. Verify understanding of formula validation
3. Practice ClickUp task creation
4. Review audit screenshots for completeness

For experienced users:
- Activate concise-execution-mode skill
- Reduce step-by-step explanations
- Focus on validation only

---

**Deployment:** Import .zip to Claude Desktop → Settings → Skills
**Prerequisites:** MCP efficiency skill must be active
**Impact:** Automates 4 critical finance/supply chain SOPs
**Result:** Consistent, auditable, error-free SOP execution
