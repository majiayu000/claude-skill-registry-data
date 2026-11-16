---
name: ecc-tools-cost-audit
description: "Audit cost overrun cho ECC Tools GitHub App — investigate runaway PR creation, quota bypass, premium-model leakage, duplicate jobs, billing spikes."
origin: ECC
user-invocable: true
---

# ECC Tools Cost Audit

Evidence-first workflow để investigate cost overruns trong ECC Tools GitHub App.

## Khi nào dùng

- ECC Tools đang tạo quá nhiều PRs
- Chi phí API bất ngờ tăng cao
- Nghi ngờ quota bypass hoặc premium model leakage
- Duplicate jobs chạy nhiều lần
- GitHub App billing spikes

## Workflow

### Bước 1 — Freeze scope

```bash
# Switch sang ECC-Tools repo
# Identify entry points: webhook router, queue producer/consumer, PR creation, billing path
```

### Bước 2 — Trace ingress

```
Map tất cả enqueue paths TRƯỚC khi theorize.
Inspect: webhook handlers → queue producers → downstream consumers
```

### Bước 3 — Trace worker

```
Xác nhận mỗi queued analysis produce gì:
- PR creation?
- Branch creation?
- Token spending?
```

### Bước 4 — Audit burn paths

| Pattern | Check |
|---------|-------|
| PR multiplication | 1 webhook → N PRs? |
| Quota bypass | Post-enqueue usage reservation? |
| Premium leakage | Free-tier jobs đang route qua premium models? |
| Retry burn | Retry logic chạy vòng lặp? |
| Duplicate jobs | App-generated branches re-entering webhooks? |

### Bước 5 — Fix theo priority

1. PR multiplication (fix trước)
2. Quota bypass
3. Premium model leakage
4. Duplicate jobs
5. Rerun safety

### Bước 6 — Verify hẹp

```bash
# Chỉ rerun tests trên changed path
# Không test toàn bộ suite
```

## 5 failure modes cao nhất

1. Single queue type xử lý tất cả triggers
2. Post-enqueue usage reservation → quota bypass
3. Free-tier jobs route qua premium providers
4. App-generated branches re-enter webhooks (loop)
5. Expensive work complete trước khi persistence safety check

## Related skills

- `autonomous-loops` — loop detection
- `customer-billing-ops` — billing investigation
- `security-review` — security audit
- `verification-loop` — narrow verification

## Source

https://github.com/affaan-m/ECC · ECC Tools: https://github.com/marketplace/ecc-tools
