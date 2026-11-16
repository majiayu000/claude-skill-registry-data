---
name: nexu-io--open-design
description: "Alternative mã nguồn mở cho Claude Design — filesystem of design skills, 150 brand-grade DESIGN.md systems, 261 plugins. Chạy trên 21+ agent CLI qua MCP server."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Open Design là platform thiết kế agent-native: agent đọc DESIGN.md files như một design system và tạo ra prototype HTML, pitch deck, motion graphic, dashboard — tất cả từ 1 brief.

## Install

```bash
# Desktop app (recommended) — auto-detect agent CLIs
# macOS / Windows: download từ https://open-design.ai

# CLI
curl -fsSL https://open-design.ai/install.sh -o /tmp/open-design-install.sh
# Inspect first: head -40 /tmp/open-design-install.sh — then run if safe:
sh /tmp/open-design-install.sh claude-code
# Hoặc: cursor, copilot, hermes, opencode, kimi...
```

## Slash Commands

```
od skill list              # xem 100+ skills
od skill search dashboard  # tìm skill theo keyword
od skill apply landing-page --design minimal-saas

od plugin list             # 261 plugins
od plugin install figma-to-react

od design-system list      # 150 brand systems
```

## Artifact Types (từ 1 brief)

```
/design landing-page brief="SaaS product for developers"
→ HTML prototype (web/mobile/desktop)
→ Live dashboard với editable params
→ Pitch deck (PPTX/PDF export)
→ Motion graphic (HTML→MP4 via HyperFrames)
→ Generated images/video
```

## DESIGN.md Format

```markdown
# Brand: YamTam Engine

## Colors
primary: #6366f1
background: #0f0f0f
text: #e2e8f0

## Typography
heading: "ui-sans-serif", weight 700
body: "ui-sans-serif", size 16px, line-height 1.5

## Components
button: rounded-lg, px-4 py-2, bg-primary
card: bg-zinc-900, border border-zinc-800, rounded-xl p-6
```

## REST API (local daemon)

```
GET  /api/skills            — skill registry
GET  /api/plugins           — marketplace
GET  /api/design-systems    — brand catalog
POST /api/chat (SSE)        — streaming artifact generation
GET  /api/artifacts/lint    — validate artifact
```

## Stack

- Frontend: Next.js 16 + React 18
- Backend: Node 24, Express, SSE, SQLite
- Desktop: Electron
- Storage: `.od/` directory
- MCP server: tools for any MCP-compatible agent

## Khi Nào Dùng

- Tạo prototype nhanh từ brief
- Generate pitch deck từ mô tả sản phẩm
- Cần design system portable (DESIGN.md) cho team
- Thay thế Figma cho AI-first workflow

## Source

https://github.com/nexu-io/open-design · Apache-2.0
