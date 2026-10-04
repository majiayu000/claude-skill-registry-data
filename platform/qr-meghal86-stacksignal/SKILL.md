---
name: QR
description: Generate, customize, and deploy QR codes with proper sizing, error correction, and use-case optimization.
---

## Before Generating

1. **Choose correct type** — URL is not the only option. See `types.md` for vCard, WiFi, email, SMS, geo, etc.
2. **Shorten dynamic URLs** — Long URLs = dense codes = harder to scan. Use short links for tracking too.
3. **Set error correction** — L (7%) for clean environments, M (15%) default, Q (25%) with logos, H (30%) for harsh conditions

## Sizing Rules

**Minimum sizes by scan distance:**
- Phone at arm's length (~30cm): 2x2 cm minimum
- Table tent (~50cm): 3x3 cm
- Poster (~1m): 5x5 cm
- Billboard (~5m): 25x25 cm

**Formula:** QR size = scan distance ÷ 10

## Color & Contrast

- **Minimum 70% contrast** between foreground and background
- Dark on light ONLY — scanners expect dark modules
- Never invert (white on black fails on many readers)
- Avoid gradients on modules — solid colors only
- Background can have subtle texture if contrast maintained

## Testing Checklist

Before printing/deploying:
- [ ] Scan with 3+ different phones (iOS, Android old/new)
- [ ] Test in target lighting conditions
- [ ] Verify destination loads correctly
- [ ] Check at actual print size, not screen preview
- [ ] Test after any logo/customization applied

## Common Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Won't scan | Too small / low contrast | Increase size, check colors |
| Scans but wrong content | URL changed after print | Use dynamic QR / redirect |
| Works on some phones | Over-customized, low error correction | Reduce customization, increase EC |
| Slow to recognize | Too dense | Shorten URL, reduce data |

## Use Case Guides

| Context | See |
|---------|-----|
| Data types (WiFi, vCard, etc.) | `types.md` |
| Business deployment patterns | `deployment.md` |
