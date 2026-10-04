---
name: wengz-domain-workflows
description: Implements or changes Wengz marketplace workflows across client, provider, PM, FM, and super admin. Use when building request lifecycle, approval SLA, contact leaks, role dashboards, or any feature that must match docs/ADVANCED_BUSINESS.md.
---

# Wengz domain workflows

## Prerequisites

1. Read **`docs/ADVANCED_BUSINESS.md`** (actors, client journey, request lifecycle, known gaps).
2. Skim **`docs/ADVANCED_TECHNICAL.md`** for paths/procedures.
3. Check role ACL: `src/lib/roles.ts` + `.cursor/rules/wengz-roles-access.mdc`.

## Role surfaces (golden paths)

| Role     | UI root           | Key routers / libs                                                       |
| -------- | ----------------- | ------------------------------------------------------------------------ |
| Client   | `/client`         | `request`, `subscription`, `payment`, `create-request.ts`                |
| Provider | `/provider`       | `provider` router, `provider-workload.ts`, `provider-wallet.ts`          |
| PM       | `/admin/requests` | `requestManagerProcedure`, contact-leaks, `approve-delivered-request.ts` |
| FM       | `/admin/finance`  | `financeManagerProcedure`, `payment` approve/reject                      |
| SA       | `/admin`          | `adminProcedure` + all of the above                                      |

## Request lifecycle checklist

Statuses: `PENDING` → `IN_PROGRESS` → `DELIVERED` ⇄ `REVISION_REQUESTED` → `COMPLETED`.

- [ ] Credits / scope validated on create (`create-request.ts`).
- [ ] Contact leak before free-text persist (`contact-leak-enforce.ts`).
- [ ] Provider concurrency (`provider-workload.ts`).
- [ ] Deliver sets `deliveredAt`; cron handles 1h / 12h SLA.
- [ ] Approve via `approveDeliveredRequest` (client or staff `onBehalfOfClient`).
- [ ] Settlement hold 7 days (`provider-wallet.ts`).
- [ ] `logRequestActivity` for mutations.
- [ ] Notify with **recipient** locale (see `wengz-notifications-locale` skill).

## Do not ship as if done

Unless explicitly implementing: RequestWatcher UI, priority pricing UI, card/Fawry rails, credit refunds, WhatsApp outbound. Listed under **Known gaps** in the business doc.

## After changes

Update `docs/ADVANCED_BUSINESS.md` if product behavior changed. Run `npm run type-check` (and lint) for server/UI edits.
