---
name: ecc-guide
description: "Navigation guide cho ECC — onboarding, tìm skills/agents/commands phù hợp, setup, troubleshooting. Dùng khi cần hỏi 'làm X với ECC như thế nào?'"
origin: ECC
user-invocable: true
---

# ECC Guide — Navigation & Onboarding

Hỗ trợ navigation trong Everything Claude Code (ECC): tìm skill đúng, setup, troubleshoot.

## Khi nào dùng

- Hỏi "làm X với ECC như thế nào?"
- Cần tìm skill/agent/command phù hợp
- Setup ECC cho project mới
- Troubleshoot khi ECC không hoạt động đúng

## Install

```bash
# Plugin path (recommended)
npm install -g ecc-universal
plugin install ecc@ecc

# Hoặc manual
bash install.sh   # Linux/macOS
.\install.ps1     # Windows
```

## Tìm skill phù hợp

```bash
# List tất cả skills
ls ~/.claude/skills/

# Tìm theo keyword
grep -r "your-topic" ~/.claude/skills/*/SKILL.md -l

# Kiểm tra skill có tồn tại không
ls ~/.claude/skills/skill-name/
```

## Skills vs Commands

| | Skills | Commands |
|-|--------|---------|
| Gọi bằng | `/skill-name` | `/cmd-name` |
| Loại | Primary interface | Legacy shims |
| Nên dùng | Ưu tiên skills | Fallback |

## Harnesses được hỗ trợ

| Platform | Config dir |
|---------|-----------|
| Claude Code | `.claude/` |
| Cursor | `.cursor/` |
| OpenCode | `.opencode/` |
| Codex | `.codex/` |
| Zed | `.zed/` |
| Gemini CLI | `.gemini/` |

## Project setup

```bash
# Detect stack + generate install plan
/project-init

# Review plan
cat install-plan.json

# Apply
node install-apply.js
```

## Troubleshoot

```bash
# Check plugin metadata
ecc doctor

# List installed components
ecc list-installed

# Repair broken install
ecc repair

# Inspect hook config
cat ~/.claude/settings.json | grep hooks
```

## Nguyên tắc quan trọng

> "Answer from current files, not memory. ECC changes quickly — hard-coded feature lists go stale."

Luôn verify component tồn tại trước khi recommend.

## Source

https://github.com/affaan-m/ECC · 215K⭐
