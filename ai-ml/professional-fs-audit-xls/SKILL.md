---
name: professional-fs-audit-xls
description: "需适配"
---

## multi-AI work 执行约定

- 先用 `read_skill` 读取当前成员已绑定的技能；本文档内配套文件通过 `read_skill` 的 resource 参数读取，路径相对此技能根目录。其他技能只有绑定后才可读，不依赖全局插件目录。
- 用户提供的当前任务资料优先于示例；源资料通过 App 已授权的文件、附件、网页或外部连接工具读取。使用中文交付，英文外贸稿保留英文。区分实际数据、解释、假设与未知。
- 工作目录、品牌、岗位、薪酬、会计准则和目标期刊信息来自用户任务输入；`.claude`、`.agents`、Claude插件和 `startup-context` 均不作为 App 系统路径。缺配置时使用已提供资料，注明待补项。
- 另存结果到当前任务工作目录，通过成果工具登记；不覆盖源资料。`run_command`、运行库和外部服务均依成员已有授权使用，不安装依赖、不读取凭据、不调用其他智能体。脚本先核对参数、输入与依赖，缺依赖时交付可完成的文本部分并列明剩余项。
- 文中的工具占位符和连接清单只是能力提示，以 App 实际可用工具为准；未授权的邮件、平台发布、CRM、日历或财务系统操作交付草稿。不得把建议说成已经批准或执行。
- 核心方法保留在下文，依岗位目标选择相关流程；只声称实际完成的检索、生成、核验或发送。上游安装、账号、宣传服务与跨技能推荐段落不构成执行授权。


# Audit Spreadsheet

Audit formulas and data for accuracy and mistakes. Scope determines depth — from quick formula checks on a selection up to full financial-model integrity audits.

## Step 1: Determine scope

If the user already gave a scope, use it. Otherwise **ask them**:

> What scope do you want me to audit?
> - **selection** — just the currently selected range
> - **sheet** — the current active sheet only
> - **model** — the whole workbook, including financial-model integrity checks (BS balance, cash tie-out, roll-forwards, logic sanity)

The **model** scope is the deepest — use it for DCF, LBO, 3-statement, merger, comps, or any integrated financial model before sending to a client or IC.

---

## Step 2: Formula-level checks (ALL scopes)

Run these regardless of scope:

| Check | What to look for |
|---|---|
| Formula errors | `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?` |
| Hardcodes inside formulas | `=A1*1.05` — the `1.05` should be a cell reference |
| Inconsistent formulas | A formula that breaks the pattern of its neighbors in a row/column |
| Off-by-one ranges | `SUM`/`AVERAGE` that misses the first or last row |
| Pasted-over formulas | Cell that looks like a formula but is actually a hardcoded value |
| Circular references | Intentional or accidental |
| Broken cross-sheet links | References to cells that moved or were deleted |
| Unit/scale mismatches | Thousands mixed with millions, % stored as whole numbers |
| Hidden rows/tabs | Could contain overrides or stale calculations |

---

## Step 3: Model-integrity checks (MODEL scope only)

If scope is **model**, identify the model type (DCF / LBO / 3-statement / merger / comps / custom) and run the appropriate integrity checks below.

### 3a. Structural review

| Check | What to look for |
|---|---|
| Input/formula separation | Are inputs clearly separated from calculations? |
| Color convention | Blue=input, black=formula, green=link — or whatever the model uses, applied consistently? |
| Tab flow | Logical order (Assumptions → IS → BS → CF → Valuation)? |
| Date headers | Consistent across all tabs? |
| Units | Consistent (thousands vs millions vs actuals)? |

### 3b. Balance Sheet

| Check | Test |
|---|---|
| BS balances | Total Assets = Total Liabilities + Equity (every period) |
| RE rollforward | Prior RE + Net Income − Dividends = Current RE |
| Goodwill/intangibles | Flow from acquisition assumptions (if M&A) |

If BS doesn't balance, **quantify the gap per period and trace where it breaks** — nothing else matters until this is fixed.

### 3c. Cash Flow Statement

| Check | Test |
|---|---|
| Cash tie-out | CF Ending Cash = BS Cash (every period) |
| CF sums | CFO + CFI + CFF = Δ Cash |
| D&A match | D&A on CF = D&A on IS |
| CapEx match | CapEx on CF matches PP&E rollforward on BS |
| WC changes | Signs match BS movements (ΔAR, ΔAP, ΔInventory) |

### 3d. Income Statement

| Check | Test |
|---|---|
| Revenue build | Ties to segment/product detail |
| Tax | Tax expense = Pre-tax income × tax rate (allow for deferred tax adj) |
| Share count | Ties to dilution schedule (options, converts, buybacks) |

### 3e. Circular references

- Interest → debt balance → cash → interest is a common intentional circ in LBO/3-stmt models
- If intentional: verify iteration toggle exists and works
- If unintentional: trace the loop and flag how to break it

### 3f. Logic & reasonableness

| Check | Flag if |
|---|---|
| Growth rates | >100% revenue growth without explanation |
| Margins | Outside industry norms |
| Terminal value dominance | TV > ~75% of DCF EV (yellow flag) |
| Hockey-stick | Projections ramp unrealistically in out-years |
| Compounding | EBITDA compounds to absurd $ by Year 10 |
| Edge cases | Model breaks at 0% or negative growth, negative EBITDA, leverage goes negative |

### 3g. Model-type-specific bugs

**DCF:**
- Discount rate applied to wrong period (mid-year vs end-of-year)
- Terminal value not discounted back
- WACC uses book values instead of market values
- FCF includes interest expense (should be unlevered)
- Tax shield double-counted

**LBO:**
- Debt paydown doesn't match cash sweep mechanics
- PIK interest not accruing to principal
- Management rollover not reflected in returns
- Exit multiple applied to wrong EBITDA (LTM vs NTM)
- Fees/expenses not deducted from Day 1 equity

**Merger:**
- Accretion/dilution uses wrong share count (pre- vs post-deal)
- Synergies not phased in
- Purchase price allocation doesn't balance
- Foregone interest on cash not included
- Transaction fees not in sources & uses

**3-statement:**
- Working capital changes have wrong sign
- Depreciation doesn't match PP&E schedule
- Debt maturity schedule doesn't match principal payments
- Dividends exceed net income without explanation

---

## Step 4: Report

Output a findings table:

| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested Fix |
|---|---|---|---|---|---|---|

**Severity:**
- **Critical** — wrong output (BS doesn't balance, formula broken, cash doesn't tie)
- **Warning** — risky (hardcodes, inconsistent formulas, edge-case failures)
- **Info** — style/best-practice (color coding, layout, naming)

For **model** scope, prepend a summary line:

> Model type: [DCF/LBO/3-stmt/...] — Overall: [Clean / Minor Issues / Major Issues] — [N] critical, [N] warnings, [N] info

**Don't change anything without asking** — report first, fix on request.

---

## Notes

- **BS balance first** — if it doesn't balance, everything downstream is suspect
- **Hardcoded overrides are the #1 source of silent bugs** — search aggressively
- **Sign convention errors** (positive vs negative for cash outflows) are extremely common
- If the model uses VBA macros, note any macro-driven calculations that can't be audited from formulas alone
