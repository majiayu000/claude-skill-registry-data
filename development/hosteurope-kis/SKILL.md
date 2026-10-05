---
name: hosteurope-kis
description: Help administer HostEurope / KIS hosting accounts and contracts. Use for inventories, contract/domain/DNS/mail/SSL reviews, costs, renewal dates, cancellation windows, local inventory files, and explicitly confirmed preparation of cancellations, transfers, DNS, mailbox, SSL, or product changes.
---

# HostEurope KIS

Unofficial skill. Not affiliated with, endorsed by, or maintained by HostEurope.

## Purpose

Support HostEurope/KIS administration in a cautious, evidence-first way. Default to reading, inventorying, summarizing, and flagging risks. Treat live changes to contracts, domains, DNS, mail, SSL, billing, or cancellations as sensitive.

Reply to the user in German by default unless they clearly use another language.

## Hard Rules

- Never ask for, store, copy, summarize, or expose passwords, cookies, session tokens, 2FA codes, TANs, recovery codes, API keys, or other credentials.
- The user must log in to HostEurope/KIS themselves in the Codex in-app browser.
- Do not inspect login fields, credential stores, cookies, local storage, or session tokens.
- Default to read-only. Reading, extracting, reconciling, and summarizing account state is allowed.
- Before any irreversible or externally visible action, get explicit confirmation for the exact action, target, and timing.
- Broad approval does not authorize a different action. A confirmed DNS review is not approval to change DNS; a cancellation draft is not approval to submit it.
- Without confirmation, prepare only a checklist, draft, or step plan.
- Do not save screenshots, raw exports, invoices, or personal data locally unless the user asks for a local artifact and confirms what it should contain.

## Working Modes

### 1. Browser Inventory

Use when the user has opened KIS in the in-app browser and logged in themselves.

1. Read only visible post-login pages, tables, labels, links, statuses, dates, costs, DNS, mail, SSL, and contract details.
2. Navigation on read-only pages and exports is allowed when the user wants the inspection.
3. Stop before using any button or form that saves, deletes, cancels, transfers, activates, deactivates, resets, orders, or changes anything. Switch to Change Preparation.
4. Create sanitized local inventory files in the workspace when useful.

Additional details: `references/browser-workflow.md` and `references/support-resources.md`.

### 2. Inventory

Use first unless the user asks for a specific confirmed change.

1. Collect evidence: visible KIS pages, CSV/PDF exports, screenshots, emails, invoices, contracts, DNS zones, and local notes.
2. Extract only operational facts needed for the request.
3. Reconcile duplicates by contract number, domain, product, billing period, or date.
4. Mark uncertain values as `unknown` or `needs verification`; do not guess contract dates or costs.
5. Return a concise table plus open verification points.

Field schema when needed: `references/inventory-schema.md`.

### 3. Review

Use when the user asks what can be cleaned up, cancelled, consolidated, transferred, renewed, or made safer.

1. Start from the inventory.
2. Separate facts from recommendations.
3. Highlight renewals, cancellation windows, domain dependencies, DNS/mail coupling, SSL expiry, and recurring cost drivers.
4. Require explicit confirmation before any external action.

### 4. Change Preparation

Use only for preparing actions such as cancellation, domain transfer, DNS migration, mailbox migration, SSL changes, or product downgrades.

1. Restate the exact action and affected objects.
2. Build a preflight checklist and, where useful, a rollback or fallback plan.
3. Check dependencies: MX, SPF, DKIM, DMARC, A, AAAA, CNAME, forwarding, SSL, mailboxes, aliases, and TTL.
4. Show before/after with current value, target value, impact, and rollback/fallback.
5. Prepare drafts, forms, or steps, but do not submit them.
6. Before any live submission, get confirmation containing the action, target, and timing.

Checklists when needed: `references/change-checklists.md`.

## Evidence And Local Files

- Prefer structured sources: CSV, XLSX, JSON, zone files, PDF invoices, and KIS exports.
- For KIS pages, capture only needed fields.
- Redact unnecessary personal data such as addresses, bank details, customer numbers in chat, and irrelevant invoice lines.
- Local artifacts should be sanitized summaries, not raw sensitive dumps.
- Useful default structure:
  - `inventory/contracts.csv`
  - `inventory/domains.csv`
  - `inventory/mailboxes.csv`
  - `inventory/dns-zones/`
  - `inventory/ssl-certificates.csv`
  - `inventory/contract-mapping.csv`
  - `inventory/requirements-high-level.csv`
  - `notes/inventory-summary.md`
  - `notes/migration-plan.md`
  - `notes/cancellation-checklist.md`
  - `notes/audit-log.md`

## KIS Term Mapping

Keep KIS UI terms exactly as shown. Do not merge distinct KIS fields into one generic lifecycle date.

- `Vertrags- Übersicht`: Vertrag/Produkt, Abrechnung, Betrag, Laufzeitoptionen, `Änderbar Bis`.
- `Domainservices` -> `Bestehende Domains bearbeiten`: Domains und Produktzuordnung. Spalte `Produkt` ist nicht automatisch Domainstatus.
- `Domainservices` -> `Nameserver / DNS-Einträge bearbeiten`: AutoDNS und Records. Nur lesen, nicht speichern/löschen.
- `Domain & Mail`, `Webhosting`, `cPanel WebHosting`, `Email`: produktspezifische Verwaltung.
- Mail-Statistiken können gecacht sein. Wenn Quota/Nutzung wichtig ist, sichtbare Aktualisierung nutzen und Quelle/Zeitpunkt notieren.
- `E-Mail-Konto` ist das Postfach mit Speicher/Quota/Passwort. `E-Mail-Adresse` ist die routbare Adresse, die in ein Postfach, an externe Ziele oder beides zustellen kann.
- `-- Kein E-Mail-Konto --` bedeutet nur: kein internes HostEurope-Postfach ausgewählt. Es kann trotzdem Weiterleitungen geben.
- Externe Weiterleitungsziele können mehrzeilig in Textfeldern stehen. Alle Zeilen vollständig erfassen.
- `cPanel WebHosting`: `VERTRAGS-ID` erfassen. Sichtbare `he-*.dummy`-Domains als `visible_kis_domain` notieren und nicht als Kundendomain interpretieren.
- SSL-Ansichten können Domainlisten widersprechen, z. B. `Website absichern` vs. aktive SSL-Bindung. Beides erhalten und als Prüfsignal markieren.

## Date And Status Rules

- Treat `Änderbar Bis` as `kis_changeable_until`, not as a cancellation deadline.
- Record `Abgerechnet bis` or domain-list dates as `accounted_until` or `renewal_date` with the original label.
- Record `Kündigungsfrist` as the visible period, for example `1 Monat`. Do not calculate an absolute date unless KIS shows it.
- Treat `Produkt: Unbekannt` as unknown product assignment, not unknown domain status.
- If KIS pages conflict, keep both facts and add a verification note.

## Owner And Target State

Keep factual inventory separate from user-provided ownership and target requirements.

- `inventory/contract-mapping.csv`: owner/customer group, family hints, object-to-contract mapping.
- `inventory/requirements-high-level.csv`: target needs such as domain + mail + storage, forwarding only, or optional website.
- Clearly mark user input as user input.
- Before recommending cancellation, downgrade, DNS migration, or mailbox deletion, reconcile facts against the target state and list open points.

## Overview Standard

When the user asks for an overview, short overview, full inventory, broad summary, or similar:

- choose medium detail;
- make contracts, domains, mail, DNS, SSL, costs, and cleanup risk comparable;
- separate facts from recommendations;
- show missing or conflicting evidence.

Preferred columns:

| Bereich | Objekt | Zuordnung | Status | Laufzeit / Datum | Kosten | Abhängigkeiten | Risiko / Hinweis | Quelle | Offene Prüfpunkte |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Optional columns when useful: owner, target state, KIS contract ID, product assignment, nameservers, MX/mail routing, storage/usage, SSL binding, cancellation period, recommended action, priority.

## Output Patterns

For inventories:

- contract/product
- domain(s)
- status
- runtime / accounted until / changeable until
- cancellation period
- costs
- dependencies
- owner/requirement, when available
- source
- open verification points

For risky changes:

- exact target
- evidence used
- impact / blast radius
- before state
- after state
- preflight checks
- proposed steps
- required confirmation sentence

Example:

`Bitte bestätige explizit: "DNS-Änderung für example.de auf die genannten Zielwerte vorbereiten."`

Do not proceed beyond preparation without this confirmation.
