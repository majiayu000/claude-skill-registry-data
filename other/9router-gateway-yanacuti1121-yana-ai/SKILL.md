---
name: 9router-gateway
description: "Set up 9Router as a local AI gateway so coding agents never stop when a provider quota runs out — one OpenAI-compatible endpoint (localhost:20128) fanning out to 40+ providers with automatic fallback. Use when asked to 'set up 9router', 'cài 9router', 'hết quota Claude thì làm sao', 'fallback provider tự động', 'never hit rate limits', 'free AI router', or 'nối Claude Code vào nhiều provider'. Do NOT use for: cloud gateway architecture comparisons (LiteLLM/Portkey/Kong) — see ai-gateway-patterns. Do NOT use for: YAMTAM's internal task routing — see yana-router docs."
tier: TIER 3 — CONSISTENCY
source: github.com/decolua/9router (MIT) + yana-ai integration
---

# 9Router Gateway — Quota Armor cho mọi AI coding tool

Một endpoint local duy nhất, đằng sau là 40+ providers với fallback tự động.
Hết quota Claude giữa chừng → request tự chảy sang provider kế tiếp,
phiên làm việc không đứt.

```
Claude Code / Cursor / Codex / yana-web
        │  OpenAI-compatible request
        ▼
http://127.0.0.1:20128/v1   ← 9Router (local, MIT)
        │  3-tier fallback + token saver (RTK −20..65%)
        ├─ Anthropic (subscription)
        ├─ Gemini / OpenAI / Groq / DeepSeek …
        └─ Free pools (OpenCode Zen, Kiro …)
```

## Cài đặt (1 phút)

```bash
npm install -g 9router        # passes L4 vetting: 29K+ stars (xác nhận 2026-09-17), MIT, active
9router                       # dashboard: http://localhost:20128
```

Dashboard → Add Provider (dán API key từng provider) → tạo Combo
(chuỗi fallback có thứ tự) → copy API key của 9Router.

## Nối vào từng tool

```bash
# Claude Code (~/.claude/settings.json hoặc env)
export ANTHROPIC_BASE_URL="http://localhost:20128"
export ANTHROPIC_API_KEY="<9router-key>"

# Bất kỳ tool OpenAI-compatible nào
export OPENAI_BASE_URL="http://localhost:20128/v1"
export OPENAI_API_KEY="<9router-key>"

# yana-web: Provider picker → 9Router → model "kr/claude-sonnet-4.5"
# (key tự đọc từ ~/.9router/db/data.sqlite khi khởi động, không cần dán tay:
# tools/yana-web/lib/providers.js dòng 17-26. Bảng provider gốc đã dời từ
# server.js sang file này, entry '9router' ở dòng 155)

# Yana Studio: Models & Runtime → chọn 9Router → dán NINE_ROUTER_API_KEY
# → bấm "Dò model" để lấy danh sách model thật từ 9router đang chạy
# (provider có sẵn: tools/yana-studio/host/model-catalog.cjs, id "9router",
# kind: "local", discoverable: true, baseUrl 127.0.0.1:20128/v1)
```

Model naming của 9Router: `<provider-prefix>/<model>` — ví dụ
`kr/claude-sonnet-4.5`. Combo dùng tên tự đặt: `my-coding-stack`.

## Combo mẫu — "không bao giờ đứt mạch"

```
Combo: maximize-claude
  1. Anthropic subscription   (chính)
  2. OpenCode Zen free        (khi hết quota)
  3. Groq Llama 3.3 70B       (khi cả hai chết)
Sticky round-robin + tự quay lại tier 1 khi quota reset.
```

## Luật an toàn khi dùng (YAMTAM rules vẫn áp)

```
□ 9Router chỉ bind loopback — KHÔNG expose 0.0.0.0 ra ngoài (rule 66)
□ API key các provider nằm trong 9Router dashboard (local) — không
  được dán vào file .env của project (rule 03-privilege-isolation)
□ Key 9Router trong yana-web đi qua YanaVault (AES-256-GCM at rest)
□ Outbound từ 9Router là của NGƯỜI DÙNG cấu hình — agent không được
  tự thêm provider/endpoint mới vào dashboard (rule 53 egress)
□ Telemetry cost trên dashboard là "savings tracker", không phải hóa đơn
```

## Khi nào KHÔNG dùng

- Cần guardrails/PII filtering tầng gateway → ai-gateway-patterns (Portkey)
- Production multi-tenant serving → ai-gateway-patterns (Kong, LiteLLM)
- Định tuyến task nội bộ YAMTAM (simple/complex/external) → yana-router

## Anti-Fake-Pass

```
❌ Claim "fallback hoạt động" mà chưa test: tắt provider 1, gửi request,
   xác nhận response đến từ provider 2 (xem dashboard logs)
❌ Claim "đã nối Claude Code" mà chưa chạy 1 prompt thật qua endpoint mới
❌ Để ANTHROPIC_BASE_URL trỏ 9router nhưng 9router không chạy
   → mọi request chết im lặng. Kiểm tra: curl -s http://127.0.0.1:20128/v1/models
❌ Đo "tiết kiệm token" bằng số trên dashboard mà không so baseline
   cùng workload trước khi bật RTK
```

## See also

- `ai-gateway-patterns` — so sánh LiteLLM / Portkey / Kong / Bifrost
- `llm-cost-optimizer` — chiến lược giảm cost tầng prompt
- `token-budget-policy` (rule) — cap token mỗi session
