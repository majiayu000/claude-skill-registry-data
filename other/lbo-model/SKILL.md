---
name: lbo-model
description: This skill should be used when completing LBO (Leveraged Buyout) model templates in Excel for private equity transactions, deal materials, or investment committee presentations. The skill fills in formulas, validates calculations, and ensures professional formatting standards that adapt to any template structure.
---

# LBO Model Builder

## Preflight: Dependency Check

Before starting, verify required libraries and tools are installed and install any that are missing.

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install openpyxl
python3 -c "import xlwings" 2>/dev/null && echo "xlwings: OK" || (
  ls "/Applications/Microsoft Excel.app" 2>/dev/null && echo "macOS Excel: OK" ||
  ls "/mnt/c/Program Files/Microsoft Office/root/Office16/EXCEL.EXE" 2>/dev/null && echo "Windows Excel (WSL): OK" ||
  echo "WARNING: MS Office not detected. Install MS Excel or run: pip install xlwings. Required for scripts/recalc.py."
)
```

**Important**: Do not skip this step — `scripts/recalc.py` is required to verify IRR/MOIC, cash sweep mechanics, and sensitivity base-case.

## Scripts

- `scripts/recalc.py` — Force formula recalculation via MS Office (xlwings/Windows COM/macOS AppleScript). Run after building: `python scripts/recalc.py <model.xlsx>`

## Reference Template

A starter LBO template is bundled at `lbo-model.xlsx` in this skill directory. If the user does not attach their own template, reuse the bundled file structure (do not copy cell values, only the layout/section conventions).

## TEMPLATE REQUIREMENT
- If template attached → use that template's structure exactly
- If no template → ask user, or use standard examples/LBO_Model.xlsx
- NEVER build from scratch when template is provided

## CRITICAL INSTRUCTIONS - READ FIRST

### Environment: Office JS vs Python
- Office JS: range.formulas = [["=B5*B6"]], no recalc needed
- Python/openpyxl: ws["D20"] = "=B5*B6", run recalc.py before delivery
- Merged cell pitfall: value to top-left first, then merge + format

### Core Principles
- Every calculation must be an Excel formula — NEVER compute in Python and hardcode
- Use the template structure — follow existing organization
- Work section by section, verify with user at each step

### Formula Color Conventions (4-color system)
- Blue (0000FF): Hardcoded inputs
- Black (000000): Formulas with calculations
- Purple (800080): Links to cells on SAME tab (direct references, no calculation)
- Green (008000): Links to cells on DIFFERENT tabs

### Fill Color Palette — Professional Blues & Greys
- Section headers: Dark blue #1F4E79 (white bold text)
- Column headers: Light blue #D9E1F2 (black bold text)
- Input cells: Light grey #F2F2F2
- Formula cells: White
- Key outputs (IRR, MOIC): Medium blue #BDD7EE (black bold)

### Number Formatting Standards
- Currency: $#,##0;($#,##0);"-"
- Percentages: 0.0%
- Multiples: 0.0"x"
- MOIC/Detailed Ratios: 0.00"x"

## TEMPLATE ANALYSIS PHASE
1. Map the structure — identify sections and relationships
2. Understand the timeline — columns = periods, pro forma column
3. Identify input vs formula cells — respect template conventions
4. Read existing labels — they specify expected calculations
5. Check for existing formulas — don't overwrite working formulas
6. Note template-specific conventions — sign conventions, subtotal structures

## FILLING FORMULAS - GENERAL APPROACH
### Step 1: Check the Template (existing formula? comment? label? pattern?)
### Step 2: Check the User's Instructions
### Step 3: Apply Standard Practice

## COMMON PROBLEM AREAS
- Balancing Sections: Sources = Uses, one item is "plug"
- Tax Calculations: reference income line + tax rate only
- Interest and Circular References: use Beginning Balance to break circularity
- Debt Paydown / Cash Sweeps: priority waterfall, MAX/MIN to prevent negative
- Returns Calculations (IRR/MOIC): correct signs, consecutive periods
- Sensitivity Tables: ODD dimensions, center cell = base case, #BDD7EE highlight

## VERIFICATION CHECKLIST
- [ ] Section balancing (Sources = Uses)
- [ ] Income projections (subtotals, margins, links)
- [ ] Balance Sheet (Assets = L+E, beginning = prior ending)
- [ ] Cash Flow (correct signs, ending cash ties)
- [ ] Supporting Schedules (roll-forwards balance)
- [ ] Debt Schedule (beginning balance, interest, paydown priority)
- [ ] Returns (IRR/MOIC correct signs and ranges)
- [ ] Sensitivity Tables (ODD grid, center = base, all cells have formulas)
- [ ] Formatting (blue/black/purple/green, number formats, no errors)
- [ ] Logical Sanity Checks (magnitude, trends, reasonableness)

## COMMON ERRORS TO AVOID
| Hardcoding | Wrong cell refs | Circular refs | Sections unbalanced |
| Negative balances | IRR/return errors | Sensitivity same value | Roll-forwards don't tie |
| Inconsistent signs |

## WORKING WITH THE USER — SECTION-BY-SECTION CHECKPOINTS
1. After Sources & Uses → confirm plug, get sign-off
2. After Operating Model → confirm growth rates, margins
3. After Debt Schedule → confirm waterfall logic
4. After Returns (IRR/MOIC) → confirm cash flow signs
5. After Sensitivity Tables → confirm base case lands correctly
