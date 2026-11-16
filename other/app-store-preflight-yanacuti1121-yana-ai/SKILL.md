---
name: app-store-preflight
description: "Use when asked to check an iOS/macOS app before App Store submission, scan for App Store rejection patterns, validate app metadata/privacy manifest/subscription compliance, or run pre-submission Apple Review guidelines checks. Triggers on: 'app store preflight', 'app store rejection check', 'ios submission check', 'apple review guidelines scan', 'preflight ios', 'kiểm tra trước khi nộp app store', 'scan lỗi app store', 'app store compliance', 'privacy manifest check', 'xcode preflight', 'truongduy2611 preflight'."
---

# App Store Preflight Skill
# Source: truongduy2611/app-store-preflight-skills (1.2k★) — AI agent pre-submission scanner
# Tier: TIER 3 — PRODUCTIVITY

AI agent scan lỗi App Store rejection trước khi submit. 100+ Apple Review Guidelines.
Tích hợp `asc` CLI để pull metadata và kiểm tra tự động.

**Do NOT use for:** `terminal--app-store-optimization` (ASO keywords/ratings), `qa-expert` (general QA testing).

---

## Khi nào dùng

- Trước khi submit app lên App Store / TestFlight
- Muốn tự động phát hiện vi phạm Review Guidelines
- Kiểm tra privacy manifest, subscription ToS, metadata
- Scan competitor trademarks (Android, Google Play...) trong metadata
- App AI/GenAI cần check thêm ai_apps.md checklist

---

## Cài đặt

```bash
npx skills add truongduy2611/app-store-preflight-skills

# Cần asc CLI
brew install asc
```

---

## Workflow

```
1. Xác định loại app → load checklist phù hợp
2. Pull metadata:
   asc metadata pull --app "<APP_ID>" --version "<VERSION>" --dir ./metadata
3. Scan theo rules trong references/rules/
4. Report: severity + file bị ảnh hưởng + cách fix
5. Autofix + validate lại
```

---

## Checklist theo loại app

| App Type | File |
|----------|------|
| Tất cả app | `all_apps.md` |
| Subscription / IAP | `subscription_iap.md` |
| Social / UGC | `social_ugc.md` |
| App cho trẻ em | `kids.md` |
| Health & Fitness | `health_fitness.md` |
| Games | `games.md` |
| macOS | `macos.md` |
| AI / GenAI | `ai_apps.md` |
| Crypto / Finance | `crypto_finance.md` |
| VPN | `vpn.md` |

---

## Rules hay bị vi phạm

```
metadata/competitor_terms     — đề cập Android/Google Play trong mô tả
metadata/apple_trademark       — dùng ảnh thiết bị Apple trong icon
metadata/china_storefront      — nhắc OpenAI/ChatGPT ở storefront China
subscription/missing_tos_pp    — thiếu link ToS / Privacy Policy
privacy/privacy_manifest       — thiếu file PrivacyInfo.xcprivacy
design/ipad_support            — app iPhone không tương thích iPad
```

---

## Ví dụ sử dụng

```
"Scan app subscription iOS của tôi trước khi submit"
→ Load subscription_iap.md + all_apps.md
→ Pull metadata bằng asc
→ Kiểm tra ToS, pricing display, review notes
→ Report findings với severity
```

---

## Liên quan

- `terminal--app-store-optimization` — ASO: keywords, ratings, screenshots
- `compliance-auditor` — SOC2/GDPR compliance
- `qa-expert` — comprehensive QA testing strategy
