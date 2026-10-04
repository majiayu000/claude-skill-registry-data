---
description: Track employee wages, deductions, and payroll obligations
---

# Payroll

Track employee wages, deductions, and payroll obligations for "$ARGUMENTS". Calculate gross and net pay, withholdings, and employer contributions.

## Prerequisites

None — utility skill, run anytime.

## Process

1. **Gather employee information:**
   - List all employees and contractors
   - Record: name, role, pay type (salary, hourly), rate, pay frequency
   - Note tax filing status and allowances
   - Identify any special deductions (benefits, garnishments, retirement)

2. **Calculate gross pay:**
   - Salaried employees: annual salary / pay periods
   - Hourly employees: hours worked x rate
   - Include overtime, bonuses, commissions as applicable
   - Track paid time off and sick leave balances

3. **Calculate deductions:**
   - **Employee withholdings:** income tax, social security, medicare
   - **Employee contributions:** health insurance, retirement (401k/pension), union dues
   - **Employer obligations:** employer share of payroll taxes, insurance, workers' comp
   - **Other:** garnishments, loan repayments

4. **Determine net pay:**
   - Gross pay minus all employee deductions
   - Verify against minimum wage requirements
   - Calculate employer total cost per employee

5. **Write the artifact** to `.metapowers/bookkeeping/$ARGUMENTS/payroll.md` with sections:
   - **Payroll Summary** — table with gross, deductions, and net per employee
   - **Withholdings Detail** — breakdown of each deduction type
   - **Employer Costs** — taxes and contributions paid by employer
   - **Totals** — aggregate payroll cost for the period
   - **Upcoming Obligations** — tax deposits and filing deadlines

## Output

The payroll report written to `.metapowers/bookkeeping/$ARGUMENTS/payroll.md`. Present a summary highlighting:
- Total payroll cost (employee + employer)
- Net pay distributed
- Upcoming tax deposit deadlines
