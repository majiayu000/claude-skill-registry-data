---
name: stata
description: "Comprehensive Stata reference for writing correct .do files. Covers syntax, options, gotchas, and idiomatic patterns. Use this skill whenever the user asks you to  write, debug, or explain Stata code. Generates ready-to-run .do files for the user to execute manually."
---

# Stata Skill

You have access to comprehensive Stata reference files. **Do not load all files.**
Read only the 1-3 files relevant to the user's current task using the routing table below.

> **Execution model:** This skill generates Stata code and saves it as `.do` files for the user to run manually in Stata. Claude does **not** execute Stata code directly — there is no MCP server or CLI integration. After generating a `.do` file, always tell the user exactly which file to open or run and what output to expect.

---

## Critical Gotchas

These are Stata-specific pitfalls that lead to silent bugs. Internalize these before writing any code.

### Missing Values Sort to +Infinity
Stata's `.` (and `.a`-`.z`) are **greater than all numbers**.
```stata
* WRONG — includes observations where income is missing!
gen high_income = (income > 50000)

* RIGHT
gen high_income = (income > 50000) if !missing(income)

* WRONG — missing ages appear in this list
list if age > 60

* RIGHT
list if age > 60 & !missing(age)
```

### `=` vs `==`
`=` is assignment; `==` is comparison. Mixing them up is a syntax error or silent bug.
```stata
* WRONG — syntax error
gen employed = 1 if status = 1

* RIGHT
gen employed = 1 if status == 1
```

### Local Macro Syntax
Locals use `` `name' `` (backtick + single-quote). Globals use `$name` or `${name}`.
Forgetting the closing quote is the #1 macro bug.
```stata
local controls "age education income"
regress wage `controls'        // correct
regress wage `controls         // WRONG — missing closing quote
regress wage 'controls'        // WRONG — wrong quote characters
```

### `by` Requires Prior Sort (Use `bysort`)
```stata
* WRONG — error if data not sorted by id
by id: gen first = (_n == 1)

* RIGHT — bysort sorts automatically
bysort id: gen first = (_n == 1)

* Also RIGHT — explicit sort
sort id
by id: gen first = (_n == 1)
```

### Factor Variable Notation (`i.` and `c.`)
Use `i.` for categorical, `c.` for continuous. Omitting `i.` treats categories as continuous.
```stata
* WRONG — treats race as continuous (e.g., race=3 has 3x effect of race=1)
regress wage race education

* RIGHT — creates dummies automatically
regress wage i.race education

* Interactions
regress wage i.race##c.education    // full interaction
regress wage i.race#c.education     // interaction only (no main effects)
```

### `generate` vs `replace`
`generate` creates new variables; `replace` modifies existing ones. Using `generate` on an existing variable name is an error.
```stata
gen x = 1
gen x = 2          // ERROR: x already defined
replace x = 2      // correct
```

### String Comparison Is Case-Sensitive
```stata
* May miss "Male", "MALE", etc.
keep if gender == "male"

* Safer
keep if lower(gender) == "male"
```

### `merge` Always Check `_merge`
Never skip `tab _merge` — it costs nothing and is the only diagnostic you get when `assert` fails.
```stata
merge 1:1 id using other.dta
tab _merge                      // ALWAYS tab before assert
assert _merge == 3              // fails silently without tab output
drop _merge
```

### `preserve` / `restore` + `tempfile` for Collapse-Merge-Back
The standard pattern for computing group stats and merging them onto the original data:
```stata
tempfile stats
preserve
collapse (mean) avg_x=x, by(group)
save `stats'
restore
merge m:1 group using `stats'
tab _merge
assert _merge == 3
drop _merge
```
For simple group means, `bysort group: egen avg_x = mean(x)` avoids the round-trip entirely.

### Weights Are Not Interchangeable
- `fweight` — frequency weights (replication)
- `aweight` — analytic/regression weights (inverse variance)
- `pweight` — probability/sampling weights (survey data, implies robust SE)
- `iweight` — importance weights (rarely used)

### `capture` Swallows Errors
```stata
capture some_command
if _rc != 0 {
    di as error "Failed with code: " _rc
    exit _rc
}
```

### Line Continuation Uses `///`
```stata
regress y x1 x2 x3 ///
    x4 x5 x6, ///
    vce(robust)
```

### Stored Results: `r()` vs `e()` vs `s()`
- `r()` — r-class commands (summarize, tabulate, etc.)
- `e()` — e-class commands (estimation: regress, logit, etc.)
- `s()` — s-class commands (parsing)

A new estimation command **overwrites** previous `e()` results. Store them first:
```stata
regress y x1 x2
estimates store model1
```

---

## Delivering .do Files to the User

Claude's role is to **write correct, well-commented Stata code** and save it as a `.do` file. The user runs it manually in Stata.

### Workflow

```
1. Understand the research task and identify the relevant reference files (see routing table)
2. Write the complete .do file with inline comments explaining each step
3. Save the file to the workspace folder so the user can open it directly
4. Tell the user:
   - The file name and location
   - Any required packages to install first (see packages.md)
   - What the script produces (log, tables, graphs, .dta files, etc.)
   - Any paths or variable names they may need to adjust
```

### .do File Template

Every generated .do file should follow this structure:

```stata
/*==============================================================
  Project : [Project name]
  Task    : [What this script does]
  Author  : Generated by Claude
  Date    : [Date]
  Stata   : 16+ recommended
==============================================================*/

* ---------- Preamble ----------
clear all
set more off
version 16

* Set working directory — user should adjust this path
* cd "/path/to/your/data"

* ---------- Required packages ----------
* Install if not already installed:
* ssc install reghdfe, replace
* ssc install estout, replace

* ---------- [Step 1: ...] ----------
// ... code with comments ...

* ---------- [Step 2: ...] ----------
// ...

* ---------- Output ----------
// Tables saved to: results/
// Figures saved to: figures/
// Log: results/analysis.log

log using "results/analysis.log", replace text
// ... estimation code ...
log close
```

### After Delivering the File

Once the `.do` file is saved, tell the user:

> "Open `[filename].do` in Stata (or run `do [filename].do` from the Stata command line). The script will produce [describe outputs]. If you encounter any errors, paste the error message here and I'll fix the code."

Do **not** attempt to execute the `.do` file yourself or simulate output. Wait for the user to run it and share results if they want further analysis.

---

## Routing Table

Read only the guide(s) relevant to the user's task. All paths are relative to this SKILL.md file.

| Guide | Topics |
|-------|--------|
| `references/basics.md` | Syntax, variables, operators, macros, loops, programming, data import/export, Mata, workflow best practices, external tools integration |
| `references/methods.md` | OLS, panel data, DiD, IV/GMM, RDD, treatment effects, matching, time series, MLE, bootstrap, survey methods, sample selection, nonparametric |
| `references/data-mgmt.md` | Data management (generate, merge, reshape), string/date/math functions, descriptive statistics, missing data, Mata data access & matrix operations, specialized models (LDV, survival, SEM, spatial, ML) |
| `references/output.md` | Graphics (twoway, schemes, coefplot), regression tables (esttab, outreg2, asdoc), summary tables (tabout), export to LaTeX/Word/Excel, graph export best practices |
| `packages.md` | Community packages: reghdfe, ivreg2, xtabond2, csdid, rdrobust, synth, psmatch2, binsreg, gtools, winsor2, diagnostics, and package management |

---

## Common Patterns

### Regression Table Workflow
```stata
* Estimate models
eststo clear
eststo: regress y x1 x2, vce(robust)
eststo: regress y x1 x2 x3, vce(robust)
eststo: regress y x1 x2 x3 x4, vce(cluster id)

* Export table
esttab using "results.tex", replace ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label booktabs ///
    title("Main Results") ///
    mtitles("(1)" "(2)" "(3)")
```

### Panel Data Setup
```stata
xtset panelid timevar          // declare panel structure
xtdescribe                      // check balance
xtsum outcome                   // within/between variation

* Fixed effects
xtreg y x1 x2, fe vce(cluster panelid)
* Or with reghdfe (preferred for multiple FE)
reghdfe y x1 x2, absorb(panelid timevar) vce(cluster panelid)
```

### Difference-in-Differences
```stata
* Classic 2x2 DiD
gen post = (year >= treatment_year)
gen treat_post = treated * post
regress y treated post treat_post, vce(cluster id)

* Event study (uniform timing — must interact with treatment group)
reghdfe y ib(-1).rel_time#1.treated, absorb(id year) vce(cluster id)
testparm *.rel_time#1.treated   // pre-trend test

* Modern staggered DiD (Callaway & Sant'Anna)
csdid y x1 x2, ivar(id) time(year) gvar(first_treat) agg(event)
csdid_plot
```

### Graph Export
```stata
* Publication-quality scatter with fit line
twoway (scatter y x, mcolor(navy%50) msize(small)) ///
       (lfit y x, lcolor(cranberry) lwidth(medthick)), ///
    title("Title Here") ///
    xtitle("X Label") ytitle("Y Label") ///
    legend(off) scheme(s2color)
graph export "figure1.pdf", replace as(pdf)
graph export "figure1.png", replace as(png) width(2400)
```

### Data Cleaning Pipeline
```stata
* Load and inspect
import delimited "raw_data.csv", clear varnames(1)
describe
codebook, compact

* Clean
rename *, lower                 // lowercase all varnames
destring income, replace force  // convert string to numeric
replace income = . if income < 0

* Label
label variable income "Annual household income (USD)"
label define yesno 0 "No" 1 "Yes"
label values employed yesno

* Save
compress
save "clean_data.dta", replace
```

### Multiple Imputation
```stata
mi set mlong
mi register imputed income education
mi impute chained (regress) income (ologit) education = age i.gender, add(20) rseed(12345)
mi estimate: regress wage income education age i.gender
```

---

## Help Improve This Skill

If you produce Stata code with a significant error — wrong syntax, incorrect command usage, or a gotcha you failed to catch — and the issue seems to stem from a gap in these reference files rather than a one-off mistake, consider suggesting to the user that they report it so the documentation can be improved.

**When to raise this:** Only after you've already corrected the error and the user has working code. Frame it as optional: *"I made an error with [X] that I think comes from a gap in the Stata skill documentation. Would you like me to note this for future improvement?"*

If the user agrees, help them draft a clear description of the gap and the correct behavior.
