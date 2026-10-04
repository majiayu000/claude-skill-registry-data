---
name: kelly-family-fund
description: Busabase-backed household pooled-pension / elder-care fund App-in-Skill (家庭统筹基金) that keeps one read-only bookkeeping dashboard where transparency equals fairness. Use when the user invokes $kelly-family-fund or /kelly-family-fund, wants to pool two elders' pensions (退休金) managed by one steward (统筹人), pay a fixed care cost (养老院 / nursing home), and share the surplus across sibling families (交通/聚餐/生日礼物/人情/social gifts), track a household fund balance and monthly income/expense/net, see per-family cumulative benefit, share %, and fairness deviation (公平), a per-category spend split, CSV import or manual ledger entry (记账). It reads Busabase only and NEVER moves money.
metadata:
  category: invest
  tags:
    - risk:read-only
    - industry:family
    - surface:busabase
  busabase:
    template: true
    folderSlug: kelly-family-fund
    resources:
      - beneficiaries
      - families
      - income
      - expenses
      - settings
    risk: read-only

---

# Kelly Family Fund

## Overview

Kelly Family Fund is a Busabase Cloud App-in-Skill. Its canonical product surface is the AirApp in Busabase, not a separate local-data product. The same Hono source supports an explicitly requested local preview with OAuth connection bootstrap. Use this skill as a family's pooled-pension / elder-care fund ledger (家庭统筹基金). Two elders' pensions are pooled and managed by one steward (e.g. the eldest sibling). The fund pays a fixed care cost (nursing home) and shares the remaining surplus across the sibling families — transport, meals, birthday gifts, and 人情 (social gifts). The whole point is transparency = fairness: everyone can see the balance, where the money went, and whether any family is benefiting more than the average. Data comes from CSV import (through a trusted skill-root script) and manual entry via that same script; there is no bank or payment API.

Default behavior is AirApp-first. Unless the user explicitly asks only for explanation, give the user the clickable AirApp URL. Start localhost only when local preview/debugging is explicitly requested; it uses the same Busabase resources and never offers another data provider. Use chat-only mode only when the user says "纯聊天", "chat only", "不要打开 UI", or similar.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-family-fund-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and report
the exact missing dependency. Do not invent a second data backend.

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly Family Fund overview"></td>
    <td width="50%"><img src="assets/screenshots/ledger.webp" alt="Kelly Family Fund ledger"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Fund balance, this-month income / expense / net, care and family totals, an expense-by-category donut, running-balance trend, and read-only insights.</td>
    <td><strong>Ledger</strong><br>Unified income and expense timeline by month, each entry tagged with its category and the sibling family it benefits.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/category.webp" alt="Kelly Family Fund by category"></td>
    <td width="50%"><img src="assets/screenshots/family.webp" alt="Kelly Family Fund fairness by family"></td>
  </tr>
  <tr>
    <td><strong>By category</strong><br>Spending across care, transport, meals, gifts, and gifts of obligation, with the care-versus-family split.</td>
    <td><strong>By family (fairness)</strong><br>Each sibling family's cumulative benefit, share, and deviation from the average — care excluded, shared costs split equally — so anyone can confirm it is balanced.</td>
  </tr>
</table>

## Boundary

- The skill may read a ledger CSV, normalize it, and write beneficiary/family/income/expense rows into Busabase through the trusted `scripts/import_csv.mjs` process.
- The AirApp reads Busabase records only; it is entirely read-only and must NEVER move money, pay a care home, transfer funds, settle between families, or mutate any remote system. It is a read-only bookkeeping and fairness dashboard (`readOnly: true`, no `writeProcedures`).
- Treat ledger data as sensitive. Never commit raw ledger exports, Busabase credentials, or env files.
- There is no approval lifecycle and no decisions workflow — this is bookkeeping only.

## Busabase Resources

Five Bases under one application Folder (`kelly-family-fund`), declared in
`content/kelly-family-fund-app/app/js/config.js` and the generated template sidecars under `content/`:

- `beneficiaries`: the elders whose pensions are pooled (`id`, `name`, `relation`, `pension_monthly`).
- `families`: the sibling families that share the surplus (`id`, `name`, `head`, `members_count`, `note`).
- `income`: monthly pension inflow per beneficiary.
- `expenses`: care cost and family-benefiting expenses. `care` rows are always the parents' cost (`family_id` empty, `shared` `"false"`).
- `settings`: one row per `kind` — `fund-meta` (fund name/steward/note/base_currency/deviation_threshold_pct, non-secret) and `onboarding`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/fund-schema.md` for exact
field shapes. The AirApp never writes to any Base — only the trusted CSV
importer does.

## First Run And Onboarding

On invocation, check the `fund-meta` and `onboarding` settings rows for
readiness. If absent, guide setup before importing real ledger data.

Set up in this order, asking only for non-secret setup details:

1. Define the fund: `name`, `steward`, optional `note`, and `base_currency` (default CNY, ¥).
2. Define beneficiaries — the elders whose pensions are pooled.
3. Define the sibling families that share the surplus.
4. Set `deviation_threshold_pct` (default 20).
5. Import a ledger CSV or enter income/expenses manually via `scripts/import_csv.mjs`.

Write the `fund-meta` and `onboarding` settings rows through the trusted
process; never ask the user to paste secrets into chat.

## CSV Import

Kelly Family Fund's AirApp is read-only; `scripts/import_csv.mjs` is the only
process that writes ledger rows. The documented template is
`references/ledger-csv-template.csv`. Columns:

- `type` (income|expense)
- `month` (YYYY-MM), `date` (YYYY-MM-DD, optional)
- `category` (care|transport|meal|gift|renqing|medical|misc — blank for income)
- `amount`
- `family` (family id or name; blank for income, shared, or care)
- `beneficiary` (beneficiary id, for income rows)
- `payee`, `occasion`, `shared` (true|false), `note`

Run:

```bash
BUSABASE_BASE_URL=... BUSABASE_API_KEY=... BUSABASE_SPACE_ID=... \
  node scripts/import_csv.mjs path/to/ledger.csv --apply
```

Without `--apply` it is a dry run that only prints the planned writes. It
resolves beneficiary/family references against Busabase, creating a new
family record on the fly if the CSV names one that doesn't exist yet, then
writes `income`/`expenses` rows via Busabase ChangeRequests. `care` rows are
always treated as the parents' cost (`family_id` empty, not shared).

## Demo Mode

- `?demo=1` (or `?demo=overview`) opens a deterministic offline fund: fund "家庭统筹基金", steward "老大 · 张伟", 2 beneficiaries (祖父 张国强 ¥16000, 祖母 李秀英 ¥14000), 4 sibling families, and 6 months (2026-01 … 2026-06) of pooled pension income and expenses in CNY.
- `?demo=ledger`, `?demo=family`, `?demo=detail`, and `?demo=category` select named scenes.
- `lang=en` or `lang=zh` forces UI chrome language for screenshots.
- Demo mode never reads or writes Busabase.

## Local App

Default behavior is AirApp-first — give the user the clickable AirApp URL.
Start `pnpm --dir content/kelly-family-fund-app dev` only when local preview/debugging is explicitly
requested. UI language supports Chinese (primary) and English chrome with an
`Auto` default.

## Views

- `#/overview`: fund balance, this-month income / expense / net, care and family totals, the max fairness deviation, an expense-allocation donut, and a running-balance trend. A month selector scopes the this-month figures.
- `#/ledger`: unified income + expense timeline, filterable by month, each row showing a category badge, amount, payee/occasion, and family tag (or 养老院/共享).
- `#/family`: the sibling families with cumulative benefit, share %, and a fairness bar showing deviation from average; select a family to drill into its directed and shared-share expenses.
- `#/category`: expense donut + care-vs-family split + a per-category totals table with percentages.
- `#/settings`: sanitized setup summary (fund, steward, base currency, beneficiaries, families, fairness threshold, data provider, onboarding). Never expose secrets.

## Insights

Read-only, deterministic observations rendered from `{ code, severity, params }` by localized templates (zh + en). Codes: `monthly_surplus` / `monthly_deficit`, `care_coverage`, `care_share`, `balance_runway`, `fairness_deviation`. They are neutral facts, never advice, and never actions.

## File Contract

Read `references/fund-schema.md` before editing the app, `content/kelly-family-fund-app/app/js/config.js`,
or `scripts/import_csv.mjs`.

## Safety Defaults

- Never move money, pay a care home, transfer, or settle between families. The AirApp only reads Busabase and renders it; only the trusted importer writes.
- Keep raw ledger exports outside git; write only normalized safe fields to Busabase.
- Fairness is computed deterministically and shown transparently; it never prescribes who should pay what.
- If a month is missing income or expenses, surface it as an empty/attention state rather than inventing values.
