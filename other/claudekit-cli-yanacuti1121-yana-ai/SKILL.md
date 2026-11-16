---
name: claudekit-cli
description: "Use when asked to manage ClaudeKit projects via CLI, install/migrate skills to other coding agents (Cursor, Codex), run Claude hook diagnostics, set up a ClaudeKit web dashboard, or automate skill distribution across AI editors. Triggers on: 'claudekit', 'claudekit-cli', 'ck cli', 'install claudekit skills', 'migrate claudekit', 'claude hook diagnostics', 'skill manager cli', 'quản lý skill claude code', 'ck config', 'claudekit dashboard'."
---

# ClaudeKit CLI Skill
# Source: mrgoonie/claudekit-cli (TypeScript) — CLI + web dashboard for ClaudeKit projects
# Tier: TIER 3 — PRODUCTIVITY

CLI + web dashboard quản lý ClaudeKit: install skills, migrate cấu trúc, chẩn đoán hooks.

**Do NOT use for:** `write-a-skill` (tạo skill mới từ đầu), `update-config` (sửa settings.json trực tiếp).

---

## Khi nào dùng

- Install ClaudeKit skills sang Cursor, Codex, hoặc agent khác
- Xem và debug hook activity gần đây (`ck config`)
- Migrate skills structure khi có breaking change
- Quản lý nhiều project ClaudeKit từ một registry trung tâm
- Auto-generate content log từ git activity

---

## Cài đặt

```bash
npm install -g claudekit-cli
# hoặc
bun add -g claudekit-cli
```

> **Lưu ý:** Cần mua ClaudeKit Starter Kit tại claudekit.cc và có GitHub PAT với `repo` scope.

---

## Lệnh chính (16 commands)

```bash
ck new          # Tạo project ClaudeKit mới
ck init         # Init ClaudeKit trong project hiện tại
ck config       # Mở web dashboard (React UI)
ck config ui    # Dashboard đầy đủ với hook diagnostics
ck skills       # Liệt kê / cài skills
ck agents       # Quản lý agents
ck commands     # Quản lý commands
ck migrate      # Migrate skills structure (RECONCILE → EXECUTE → REPORT)
ck doctor       # Kiểm tra cấu hình, phát hiện lỗi
ck versions     # Xem version history
ck update       # Update ClaudeKit lên version mới
ck watch        # Daemon theo dõi GitHub issues
ck content      # Generate content từ git activity
```

---

## Hook Diagnostics

```bash
ck config   # Mở dashboard → tab "Hook Activity"
# Hiện toàn bộ hook events gần đây, errors, và timing
# Scope: global (~/.claudekit) và project-level
```

---

## Skill Installation sang agent khác

```bash
# Cài skill vào Cursor
ck skills install --target cursor

# Cài từ local archive (offline)
ck skills install --from ./claudekit-backup.zip
```

---

## Security

- Path traversal protection + symlink validation
- UNC path protection (Windows)
- Multi-tier auth: gh CLI → env vars → keychain → prompt

---

## Liên quan

- `write-a-skill` — tạo SKILL.md mới
- `agent-memory-security` — bảo mật agent memory
- `update-config` — sửa settings.json / hooks trực tiếp
