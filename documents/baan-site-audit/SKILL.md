---
name: baan-site-audit
description: Audit the baan-site docs (https://baan.press) against the actual Baan codebase and READMEs to find drift — claims that do not match code, claims that do not match README, and gaps where the site silently omits facts the README considers essential. Use when asked to "audit baan-site", "check site docs against system", "verify docs match implementation", "find outdated docs", "sync baan-site with baan", or equivalent. Read-only by default — propose edits, wait for approval before applying.
---

# Baan-site ↔ Baan System Sync Audit

`baan-site` (the docs site at `baan.press`, source in the
`baan-press/baan-site` GitHub repository, typically cloned as a
sibling of this repo) makes thousands of concrete claims about
how Baan works. The audit verifies every
claim against the two sources of truth — **the code in `baan/`**
and **`README.md`**.

## Source-of-truth hierarchy

When statements disagree, the priority is:

1. **Code** — `baan/lib/**`, `baan/app/**`, `baan/.env.example`,
   `baan/themes/`, etc. The code is what runs. If the doc
   contradicts code, the doc is wrong.
2. **README** (`baan/README.md`) — the curated summary of code.
   The README is the canonical structure / vocabulary / framing
   reference. Where README and code disagree, code wins, but the
   README's *structure* (the 8-pillar framing, the term canon, the
   comparison axes) is itself the contract baan-site must mirror.
3. **baan-site** — the surface being audited. Always the last
   word, never the source of truth.

The audit's output is always a list of **doc edits to baan-site**
(or, occasionally, README edits if the README has gone stale
relative to code). Never code edits.

## What "match" means — three checks per claim

For every concrete claim in baan-site, verify all three:

### Check 1 — Literal match against code

The names, values, paths, counts, and behaviors stated in the
doc must appear in the code with the same spelling, casing, and
meaning.

- Env var: in `.env.example` and read by `process.env.X` somewhere
  in `lib/` or `app/`?
- Settings key: in `VALID_SETTINGS_KEYS` (`lib/settings/storage.ts`)?
- Route / URL: a matching `page.tsx` or `route.ts` exists?
- Theme name: directory exists under `themes/`?
- Model name: present in `lib/ai/config/ai-models.ts`?
- File / directory path: exists in the repo?
- Numeric default (rate limit, TTL, step count): matches a constant
  in code?

If literal match fails → drift.

### Check 2 — Literal match against README

The statement must be consistent with how the README describes
the same topic. The README is the negotiated truth — when README
lists 4 storage providers, baan-site must not list 3. When README
calls something `Baan Admin`, baan-site must not call it
`Admin panel`. When README structures the differentiators as 8
sections, baan-site's pitch should not silently drop one.

This is the check that catches **omission drift** — when the
words baan-site uses are individually correct but the *set* of
facts is shorter than the README's, the reader ends up with a
different model of Baan than the README intends.

If README mentions facts X, Y, Z and baan-site mentions only X, Y
→ drift (Z missing).

### Check 3 — Implication consistency (only after 1 and 2 pass)

If the literal claim matches code and matches README, ask:
does the natural takeaway from the prose still match the README's
framing? This is a defensive last pass for cases where wording
choices (e.g. "cloud storage" instead of "storage you choose")
might leave a reader with a different model than intended, even
when nothing is technically wrong.

This check is **secondary** — do not invoke it before completing
1 and 2, and do not let it dominate the audit. Most drift is
caught by 1 and 2.

## Audit procedure

### Step 1 — pick the scope

A page, an area (e.g. "all storage docs"), or "everything".

### Step 2 — collect baan-site claims

For the scope, list every concrete claim:
- Names (env vars, settings keys, themes, models, routes, files)
- Counts (number of themes, locales, wizard steps, providers)
- Default values
- "X is supported / not supported" statements
- Architecture / pitch statements (storage destinations, DB role,
  publishing flow, etc.) — including hero copy, pillars, and
  comparison-table rows

### Step 3 — collect the truth

Read the corresponding code and README sections:

| Claim about | Code source | README section |
|-------------|-------------|----------------|
| Storage providers | `lib/storage/` (one file per provider) | Architecture, "Markdown + 軽量DB" / Compare table |
| Database type & requirement | `lib/db/`, `.env.example`, `lib/settings/storage.ts` | "メタデータ" / Database section |
| Env vars | `.env.example` + `grep "process\.env\." lib/ app/` | "環境変数ファイル" |
| Settings keys | `lib/settings/storage.ts` `VALID_SETTINGS_KEYS` | `settings` テーブルの有効キー一覧 |
| Routes / admin sections | `app/(public)/`, `app/(admin)/baan-admin/[secretPath]/(authenticated)/` | Admin sections in differentiators |
| API endpoints | `app/api/cms/v1/`, `app/(admin)/baan-admin/api/` | CMS API mentions |
| Roles & permissions | `lib/security/admin-permissions.ts` | Security section |
| Themes | `themes/` (directory listing) | Theme system / 8. テーマシステム |
| AI models | `lib/ai/config/ai-models.ts` | AI最適化 / AI関連 |
| Setup wizard step count / order | `app/(admin)/baan-admin/setup/page.tsx` | Setup quickstart |
| Middleware / proxy | `proxy.ts` (Next.js 16; not `middleware.ts`) | Architecture |
| Locales | `locales/` + `app/(admin)/baan-admin/_lib/locales/` | 多言語対応 |

### Step 4 — verify each claim against the truth

For each claim, run the three checks in order. Cite the source
(file:line) for the verification result.

- Check 1 fail → "site says X, code shows Y at file:line" (literal drift)
- Check 1 pass, Check 2 fail → "site says X, README says X+Y" (omission drift)
- Checks 1 and 2 pass, Check 3 fail → "claim is technically correct
  but the framing implies Y, which contradicts README's framing"
  (implication drift, secondary)

A claim that nobody can locate evidence for is suspect. **Trust
verified evidence; do not trust memory.**

### Step 5 — classify findings

| Severity | Trigger |
|----------|---------|
| **Blocking** | Reader will act on the claim and break something (e.g. set a no-op env var, point at a removed route) |
| **High** | Names / counts / values do not match code or README — load-bearing literal drift |
| **Medium** | Wording is imprecise or framing differs from README, but the literal facts are recoverable |
| **Low** | Cosmetic / minor casing / cross-locale wording |

### Step 6 — single findings table

Per `.claude/rules/reporting.md`: lead with one table.

```
| # | Severity | Where | Site says | Code/README says (cite) | Proposed fix |
```

Cite a specific file:line for every "Code/README says" entry.
Without citation the finding is unverified.

### Step 7 — wait for approval before editing

Per `feedback_no_implement_without_approval.md`: do not start
editing baan-site after presenting findings. Wait for the user
to greenlight specific items.

When applying fixes, group commits by area; one commit per page
when scope is broad.

## Audit scope — what blocks of prose to read

The audit must read **every** claim in scope, including:

- Hero copy / page titles / meta descriptions
- "What makes Baan different" pillar grids
- Comparison tables (vs WordPress / vs static SGs / etc.)
- Architecture diagrams and the captions around them
- Setup / quickstart steps
- Reference pages (env vars, API endpoints, settings keys)
- Long-form explainers
- Sidebar labels (the IA itself is a claim)

Do not skip pillar copy or hero copy. They make the largest
factual claims and are easy to miss because they read like
marketing.

## Cross-locale check

`baan-site` is currently English-only at the doc level. If
locale-specific docs are added (e.g. `docs/ja/...`), audit each
locale separately. Translations re-frame literal claims and
need their own pass.

## Maintaining the skill itself

Update this skill when an audit reveals something the procedure
fails to catch. Two questions to ask before adding text:

1. Is this a new **fact** (a renamed field, a new model)? → No
   skill update; just fix the doc and update the README/code
   reference table if needed.
2. Is this a new **failure mode** (a class of claim the skill's
   procedure routinely misses)? → Update the procedure or scope
   so future audits catch it.

Do not turn this skill into an enumerated list of past mistakes.
The procedure (Checks 1–3, the source-of-truth table, the audit
scope) is what scales; line-item add-ons do not.

## What NOT to do

- Do not edit `baan/` source code to match a doc — code is the truth
- Do not skip the README check — the README is the negotiated
  structure baan-site must mirror, and omission drift hides there
- Do not invoke Check 3 (implication) before Checks 1 and 2 pass
  — most drift is literal, not philosophical
- Do not run `npm run build` on either repo as part of the audit
  (read-only by default)
- Do not commit changes unless the user explicitly asks
- Do not bundle audit fixes with unrelated copy edits or restyling
  — keep the diff reviewable
