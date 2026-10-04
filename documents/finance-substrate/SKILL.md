---
name: finance-substrate
category: finance
description: Personal finance and tax management substrate for Colombian residents. Imports bank transactions, tax certificates, and DIAN data. Projects annual tax liability (Form 210) with certificate-level accuracy. Handles password-protected PDFs from Colombian banks. Zero external paid services — all data stays local.
---

# Finance Substrate

Self-hosted personal finance and Colombian tax management. No paid aggregators — imports from bank exports, parses tax certificates, and uses free open data APIs.

## Data Sources

### Automated (no manual export needed)

| Source | Method | Data | Cost |
|--------|--------|------|------|
| **Gmail** (9 institutions) | GWS CLI (`gws gmail`) | Salary payments, bank notifications, certificates, PILA confirmations | Free |
| **DIAN MUISCA** | `agent-browser` automation | Exogena XLSX, e-invoices XLSX, RUT PDF | Free |
| **TRM (USD/COP)** | `datos.gov.co` REST API | Daily exchange rates | Free |

### Semi-automated (PDF parsing from user-provided files)

| Source | Method | Data | Cost |
|--------|--------|------|------|
| Davivienda | PDF certificate + CSV export | Cuentas, AFC, rendimientos, GMF | Free |
| Nubank Colombia | PDF certificate + CSV export | Rendimientos, retención, GMF | Free |
| Nequi | PDF certificate | Saldo, rendimientos | Free |
| RappiPay / RappiCard | PDF certificate | Saldo, deuda TC, cashback | Free |
| Skandia | PDF certificate (multi-page) | Pensión oblig/vol, cesantías, retiros | Free |
| Colmedica | PDF certificate | Medicina prepagada (Art. 387) | Free |
| Banco de Bogotá | PDF certificate | Intereses crédito | Free |
| Acciones & Valores | PDF certificate | Acciones, dividendos, FIC | Free |
| DolarApp/ARQ | Manual entry | USD balance (patrimonio exterior) | Free |
| PILA planillas | PDF from Compensar | SS contributions (salud, pensión, ARL, FSP) | Free |

### Gmail institution coverage

| Institution | Email sender | Messages/year | Key data |
|-------------|-------------|---------------|----------|
| Thera (salary) | `thera` | ~24 | USD payment amounts, dates |
| Davivienda | `davivienda` | ~16 | Monthly extractos (PDF), certs |
| Skandia | `skandia` | ~20 | Pension fund notifications |
| Nu Colombia | `nu.com.co` | ~20 | Account & rendimientos |
| Nequi | `nequi` | ~20 | Transaction confirmations |
| Compensar | `compensar` | ~18 | PILA payment confirmations |
| RappiPay | `rappipay` | ~11 | Payment notifications |
| Banco Falabella | `falabella` | ~15 | TC consumos, certs |
| DIAN | `dian.gov.co` | ~9 | Firma electrónica, RUT, códigos |

See `references/gmail-data-sources.md` for GWS CLI patterns, query syntax, and integration strategies.

## PDF Password Convention

Colombian financial institution PDFs are typically password-protected with the account holder's **cédula de ciudadanía (CC) number**. When parsing certificates:

1. First attempt: open without password (some PDFs like Davivienda are unprotected)
2. Second attempt: use CC number as password
3. The password is **never stored** in the skill repo or data files — prompted at runtime or passed via `--password` flag

Institutions known to use CC-based PDF passwords:
- Skandia (pension obligatoria, voluntaria, cesantías)
- Colmedica (medicina prepagada)
- Nu Colombia (certificado tributario, reporte anual de costos)
- Nequi (certificado tributario)
- RappiCard / RappiCuenta (certificados tributarios)
- Banco de Bogotá (certificado tributario)
- Acciones & Valores (bursátil + fondos)

Institutions with unprotected PDFs:
- Davivienda (certificado tributario, extractos)
- DIAN (borrador, comprobantes)
- Finanseguro

## Tax Declaration Strategy (Form 210)

### Income Structure — Foreign Salary

For Colombian residents earning USD salary from a foreign employer:

1. **Ingresos brutos (R32)**: Gross COP value of all salary payments, converted at the official TRM rate on each payment date
2. **INCR (R33)**: Social security contributions as independent:
   - Pension obligatoria (16% of IBC = 40% of gross)
   - Salud obligatoria (12.5% of IBC)
   - ARL (~0.522% of IBC, risk level I)
   - Fondo Solidaridad Pensional (1% of IBC if income > 4 SMLMV)
   - Source: pension fund certificate + monthly planillas
3. **FX losses**: Deductible as cost of earning foreign income (difference between TRM and actual received amount)

### Deduction Strategy — Maximizing R35 + R37

The primary tax optimization levers for persona natural:

1. **AFC contributions (R35)**: Cuenta AFC (Ahorro Fomento a la Construcción)
   - Aportes directos and aportes con contingente are both deductible
   - Withdrawals for housing (destino vivienda) are tax-free under Art. 126-4 ET
   - This is typically the single largest deduction available
   - Source: bank AFC certificate (page showing aportes and retiros)

2. **Voluntary pension (R35)**: Fondo de pensiones voluntarias
   - Aportes with retención contingente are deductible
   - Combined AFC + voluntary pension cap: 30% of gross income or 3,800 UVT (Art. 126-1 ET)
   - Withdrawals before 10 years (or without meeting pension requirements) trigger retención contingente (7%)
   - Source: pension fund voluntary certificate

3. **25% renta exenta (R36)**: Art. 206.10 ET
   - Automatic deduction of 25% on rentas de trabajo
   - Capped at 790 UVT/month

4. **Medicina prepagada (R39)**: Art. 387 ET
   - Deductible up to 16 UVT/month
   - Source: prepaid health provider certificate

5. **E-invoice 1% deduction (R39)**: Art. 336 numeral 5 ET
   - 1% of purchases paid electronically (tarjeta débito/crédito)
   - Source: DIAN facturas electrónicas recibidas report

6. **GMF deduction (R39)**: Art. 115 ET
   - 50% of GMF (4x1000) paid is deductible
   - Source: all bank certificates report GMF separately

7. **Limitation (R41)**: Total exentas + deducciones capped at 40% of R34 or 5,040 UVT
   - Strategy: maximize R35 (AFC + pension voluntaria) first since it's the most impactful before the cap binds

### Patrimonio Strategy

Track all assets for R29 (patrimonio bruto):
- Bank accounts: all savings/checking account saldos at Dec 31
- Investment funds: pension voluntaria saldo, FICs
- Stocks: valor nominal of holdings
- Pension: cesantías saldo
- Vehicle: avalúo catastral from municipality
- Real estate: escritura value or avalúo

Deudas (R30): credit card balances, outstanding loans at Dec 31

### Retenciones (R132)

Sum all retenciones from certificates:
- Pension fund: retención contingente + retención sobre rendimientos
- Banks: retención en la fuente on rendimientos financieros
- Other: any retención reported by third parties in exogena

Tip: the exogena report from DIAN aggregates retenciones reported by all third parties — use it to validate against individual certificates.

### Anticipo Strategy

- R130: Anticipo paid in prior year (reduces current year saldo a pagar)
- R133: New anticipo = max(0, 75% of R126 - R132)
- First declaration year: 25%. Second year: 50%. Third year onwards: 75%
- Higher retenciones in current year reduce the anticipo for next year

### Rendimientos Financieros (Rentas de Capital)

- Componente inflacionario: 50.88% of rendimientos (2024) are non-taxable (INCR)
- Banks report both total rendimientos and the non-taxable portion
- Source: each bank's certificate has a rendimientos + "no gravados" breakdown
- Don't forget: pension fund valorización counts as capital income

## Skill Modes

### 1. `import` — Ingest bank transactions

Import CSV/OFX/XLSX from any supported bank into the unified ledger.

**Scripts:**
- `scripts/import_csv.py` — Generic CSV/OFX parser with bank profiles in `importers/*.json`
- `scripts/import_declaracion.py` — Bulk import from `~/Dropbox/Declaracion/` directory:
  - Bank consolidated XLSX (from bank PDF extraction scripts)
  - Salary XLSX with USD→COP conversion details
  - DIAN exogena XLSX (third-party reported data)
  - DIAN e-invoices XLSX
  - Transfer CSVs (international + national email notifications)

### 2. `certificates` — Parse tax certificates

Import certificados tributarios from financial institutions.

**Script:** `scripts/import_certificates.py --year 2024 --password <CC>`

Extracts data from all certificates in `~/Dropbox/Declaracion/<year>/` using regex patterns. Handles password-protected PDFs. Outputs aggregated tax inputs mapped to Form 210 rows.

### 3. `trm` — Fetch exchange rates

**Script:** `scripts/fetch_trm.py`

Fetches TRM from datos.gov.co free API. Supports single date, range, or last N days.

### 4. `tax` — Tax projection (Form 210)

**Script:** `scripts/tax_projection.py --year 2024 --anticipo <amount>`

Projects full Form 210 using salary data, certificates, and exogena:
- Maps output to actual DIAN row numbers (R29-R136)
- Models INCR from social security contributions
- Applies AFC + voluntary pension + 25% exempt income + medicina prepagada
- Calculates anticipo renta for following year
- Compares against DIAN borrador when available

### 5. `categorize` — Classify transactions

Apply or update categorization rules on uncategorized transactions.

### 6. `summary` — Financial reports

Aggregate transactions by category, account, currency with multi-period comparison.

### 7. `dian-scrape` — MUISCA data download

Browser automation for DIAN portal data extraction (requires `agent-browser` skill).

**Capabilities** (post-login):
- Download exogena XLSX (third-party reported income, patrimony, withholdings)
- Download e-invoices received report
- Download withholding certificates
- Retrieve RUT PDF
- Query filed declarations and payment history

**Login flow**: Uses `agent-browser` to navigate the WebIdentidadLogin SPA → OAuth callback → JSF portal. Document type dropdown must be clicked (not `select`-ed) to avoid form reset. Sessions can be persisted with `agent-browser state save`.

See `references/dian-muisca-automation.md` for the complete technical reference including URL patterns, error codes, security measures, and legal considerations.

### 8. `dian-fill` — Form 210 Declaration Filing

Automate filling and submitting the declaración de renta (Form 210) on DIAN MUISCA using `agent-browser`.

**Script:** `scripts/fill_form210.py --year 2024 --anticipo 19287000`

**How it works:**
1. Runs `tax_projection.py` to compute all casilla values
2. Maps each casilla to the correct wizard step via `templates/form-210-schema.json`
3. Generates step-by-step `agent-browser` commands:
   - Navigates to each step via JS click on step counter elements
   - Snapshots to discover field refs (refs change between sessions)
   - Fills editable casillas with projected values (DIAN-rounded to thousands)
   - Skips auto-computed casillas (DIAN calculates them)

**Output modes:**
- `--dry-run` — Human-readable table of casilla → value mappings
- Default — Shell script with `agent-browser` commands (pipe to `bash`)
- `--json` — Machine-readable mapping for programmatic use

**Form 210 wizard structure (15 steps):**

| Step | Section | Key casillas |
|------|---------|-------------|
| 1 | Datos Declarante | 5-12, 24 (actividad económica), 286 (género) |
| 2 | Deducciones sin limitantes | 28, 297 (e-invoice), 245, 247, 249, 251, 299 |
| 3 | Patrimonio | 29, 30, 31 |
| 4 | Rentas de trabajo | 32-42 |
| 5 | Rentas de trabajo (no relación laboral) | 43-57 |
| 6 | Rentas de capital | 58-73 |
| 7 | Rentas no laborales | 74-90 |
| 8 | Cédula general | 91-97 |
| 9 | Pensiones | 99-103 |
| 10 | Dividendos | 104-120 |
| 11 | Liquidación privada | 121-133 |
| 12 | Ganancias ocasionales | 112-115 |
| 13 | Anticipo | 130, 133 |
| 14 | Saldo a pagar / favor | 134-141 |
| 15 | Firma y presentación | Electronic signature + submit |

**Typical workflow:**
```bash
# 1. Open headed browser (manual login required for now)
agent-browser --headed --session dian open "https://muisca.dian.gov.co/"
# Log in manually in the browser window

# 2. Navigate to Form 210 creation
# Dashboard → "Presentar Declaración de Renta" → Select year → Crear

# 3. Generate fill commands from tax projection
python3 scripts/fill_form210.py --year 2024 --dry-run  # Preview values
python3 scripts/fill_form210.py --year 2024 > /tmp/fill-210.sh  # Generate script

# 4. Execute step by step (review each step before advancing)
# Each step: snapshot → fill casillas → verify → next step
# The script uses placeholder refs (<REF_casilla_NNN>) that must be
# replaced with actual @eN refs after each snapshot

# 5. After all steps: Firmar → Presentar → Pagar
```

**Important notes:**
- DIAN rounds all values to thousands (no decimals) — the script does this automatically
- Field refs (`@eN`) change between sessions — always snapshot before filling
- For already-filed years (like 2024), DIAN only allows "Corrección" — not new "Inicial"
- The Firmar step requires electronic signature (manual intervention)
- **Always review values before submitting** — the script fills a draft, it does not auto-submit

See `templates/form-210-schema.json` for the complete casilla-to-ET-article mapping.

### 9. `optimize` — Deduction Optimizer

**Script:** `scripts/optimize_deductions.py --gross-income <COP> --year 2024`

Finds the optimal AFC + voluntary pension contribution split to minimize tax.

**What it computes:**
- Maximum useful contribution before the 1,340 UVT cap binds (Art. 336 Num. 3, Ley 2277/2022)
- Tax savings vs. zero contributions
- Marginal benefit analysis (tax saved per additional $1M COP)
- Warning when the global cap is the binding constraint

**Key constraint hierarchy:**
1. AFC + voluntary pension ≤ 30% of gross income or 3,800 UVT (Art. 126-1 + 126-4)
2. Total exentas + deducciones ≤ 40% of renta líquida or **1,340 UVT** (Art. 336)
3. 25% renta exenta ≤ 790 UVT/year (Art. 206 Num. 10)
4. The 1,340 UVT global cap is typically the binding constraint for incomes above ~$150M COP

### 10. `self-heal` — Validation and Anomaly Detection

**Script:** `scripts/self_heal.py --year 2024`

Detects data quality issues and signals improvements for agents to act on.

**Checks performed:**
- **Parser health**: validates all `parsers/*.json` definitions (schema, methods, no duplicates)
- **Extraction confidence**: flags parsers that extracted mostly zeros (PDF format likely changed)
- **Expected non-zero fields**: catches silent failures (e.g., rendimientos = $0 for a bank that should have them)
- **Cross-source validation**: compares retenciones and pension amounts across certificates, exogena, and planillas — flags >5% discrepancies
- **XLSX schema validation**: checks that DIAN export column structure matches expectations before import
- **Projection sanity**: verifies arithmetic (R34 = R32 - R33), cap compliance (R41 ≤ 1,340 UVT), no negatives

**Self-healing loop:**
1. Run `self_heal.py` after every import cycle
2. Issues logged to `.control/improvement-log.jsonl` with severity and suggestions
3. Agents (Claude or any LLM) read the log and take corrective action:
   - `unknown_institution` → create new `parsers/<name>.json`
   - `low_extraction_confidence` → update parser regex patterns for changed PDF format
   - `expected_nonzero_field` → investigate specific field in parser definition
   - `retenciones_mismatch` → check for missing certificate or exogena update
   - `exogena_schema_drift` → update column mappings in import script
4. After fix, re-run `self_heal.py` to verify the issue is resolved

**For agents reading this skill:**
When invoked, always run `python3 scripts/self_heal.py --year <year>` after importing data. If issues are found, read `.control/improvement-log.jsonl` for the latest signals and fix the root cause before proceeding with tax projection or form filling. The control metalayer in `.control/commands.yaml` defines the actuators (create-parser, update-parser, fix-xlsx-schema) that map to each signal type.

### 11. `budget` — Monthly Budget Planner

**Script:** `scripts/budget_planner.py --monthly-usd 8000 --year 2025`

Computes monthly budget allocation for a Colombian resident earning USD salary.

**Allocates:**
- Parafiscales PILA (fixed monthly obligation)
- AFC contribution (monthly portion of annual optimal amount)
- Voluntary pension (monthly portion)
- Tax savings fund (saldo a pagar / months to deadline)
- Available for living expenses (remainder)

Outputs a formatted table with COP, USD, and percentage of income for each category.

### 12. `patrimonio` — Net Worth Calculator

**Script:** `scripts/patrimonio_calc.py --year 2024 --detail`

Aggregates patrimonio from all data sources for Form 210 R29/R30/R31.

**Sources:**
- Certificates: bank account saldos, investment funds, pension funds
- Exogena: real estate (Marval), vehicle (Bogotá avalúo), stocks (Ecopetrol), third-party reported saldos
- Manual entries: `--add-asset "Cash" 5000000 --add-debt "Loan" 3000000`

**Deduplication:** When the same asset appears in both certificates and exogena, uses the higher value and flags the overlap.

### 13. `report` — Accounting Report Generator

Generates comprehensive accounting and tax report in Markdown format, covering:
- Executive summary (year-over-year comparison)
- Monthly salary detail with TRM conversion
- Social security (parafiscales) breakdown
- Patrimonio (assets and liabilities)
- Form 210 comparative table with ET article references
- Deduction strategy analysis
- Monthly budget plan with tax savings fund
- Filing calendar and data source inventory

### 14. `gmail` — Email Document Collector

**Script:** `scripts/gmail_collector.py --year 2025`

Searches Gmail for tax-relevant documents from all financial institutions using GWS CLI (`gws`).

**Sources searched:**
- **Thera** — salary payment confirmations (extracts USD amount and employer)
- **Davivienda** — extractos, certificados, transaction notifications
- **Nu Colombia** — account notifications
- **Nequi** — transaction notifications
- **RappiPay/RappiCard** — payment notifications
- **Skandia** — pension fund notifications
- **Compensar** — PILA/parafiscales confirmations
- **DIAN** — official notifications (firma electrónica, RUT, códigos)
- **Banco Falabella** — certificates and statements

**Capabilities:**
- Search by year with automatic date filtering
- Extract salary amounts from Thera payment emails ($USD parsed from body)
- Download PDF/XLSX attachments to `~/Dropbox/Declaracion/<year>/Gmail/`
- Filter by single source: `--source thera`

**Requires:** GWS CLI installed and authenticated (`npx skills add googleworkspace/cli`, `gws auth login`)

### 15. `invoice` — DIAN e-invoicing

Issue UBL 2.1 invoices via DIAN SOAP (requires `facho` + digital certificate).

## File Structure

```
finance-substrate/
├── SKILL.md                      # This file
├── skill.json                    # Schema definition
├── scripts/
│   ├── import_csv.py             # Bank CSV/OFX parser
│   ├── import_declaracion.py     # Bulk import from Declaracion/
│   ├── import_certificates.py    # Tax certificate PDF parser
│   ├── import_planillas.py       # PILA social security planilla parser
│   ├── parse_engine.py           # Declarative parser interpreter
│   ├── fetch_trm.py              # TRM API client
│   ├── tax_projection.py         # Form 210 tax engine (95% accuracy)
│   ├── fill_form210.py           # Agent-browser commands for DIAN wizard
│   ├── optimize_deductions.py    # AFC + vol. pension optimizer
│   ├── budget_planner.py         # Monthly budget allocation with tax savings
│   ├── patrimonio_calc.py        # Net worth calculator (R29/R30/R31)
│   ├── gmail_collector.py        # Gmail search for tax docs & salary payments
│   └── self_heal.py              # Validation, anomaly detection, self-healing
├── importers/
│   ├── davivienda.json           # Column mappings & date format
│   ├── nubank.json               # Column mappings & date format
│   ├── nequi.json                # Column mappings & date format
│   └── arq.json                  # Column mappings & date format
├── templates/
│   ├── tax-tables-2024.json      # DIAN tax brackets (UVT $47,065)
│   ├── tax-tables-2025.json      # DIAN tax brackets (UVT $49,799)
│   ├── tax-tables-2026.json      # DIAN tax brackets (projected)
│   └── categories.json           # Default category taxonomy (40+ rules)
├── references/
│   ├── dian-calendar.md          # Filing deadlines by NIT suffix
│   ├── dian-muisca-automation.md # MUISCA browser automation reference
│   ├── estatuto-tributario.md    # ET article citations for all Form 210 rows
│   ├── gmail-data-sources.md     # Gmail/GWS CLI patterns for all institutions
│   └── data-architecture.md      # Document flow and storage governance
├── reports/
│   └── financial-report-2025.md  # Comprehensive annual report with projections
└── README.md                     # Setup & usage
```

## Data Directory (user-local, not in skill repo)

```
~/.finance-substrate/
├── ledger/
│   ├── transactions.jsonl        # Append-only unified transaction log
│   ├── accounts.json             # Account registry
│   └── rules.json                # Categorization rules
├── tax/
│   ├── salary-history.jsonl      # Monthly salary payments with FX details
│   ├── certificates.jsonl        # Parsed institution certificates
│   ├── exogena.jsonl             # DIAN third-party reports
│   ├── withholdings.jsonl        # Retenciones tracking
│   └── projections/              # Saved tax projections
├── fx/
│   └── trm-history.jsonl         # TRM rate history
└── invoices/
    ├── issued/                   # Outgoing e-invoices
    └── received/
        └── e-invoices.jsonl      # DIAN e-invoices received
```

## Related Skills

- **[wealth-management](https://github.com/broomva/wealth-management)** — Compounds on this skill for long-term wealth building. Reads certificates, patrimonio, and salary data to run compound growth projections, Monte Carlo simulations, goal-based planning, and asset allocation optimization.
- **[investment-management](https://github.com/broomva/investment-management)** — Full-stack investment analysis and execution. Security screening, philosophy-based scoring, market data, backtesting, portfolio optimization, and trade execution across stocks, crypto, and prediction markets.

## Dependencies

- Python 3.10+
- `openpyxl` — Excel parsing (required for declaracion import)
- `pymupdf` — PDF text extraction (required for certificate parsing)
- `facho` — DIAN SOAP client (optional, only for e-invoicing)
- `agent-browser` skill (optional, only for DIAN scraping)
- No paid services. No API keys. All data stays local.
