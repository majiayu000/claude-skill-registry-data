---
name: ecc-agentshield
description: "Security scanner cho Claude Code config — quét CLAUDE.md, settings.json, hooks, MCP servers, agents tìm lỗ hổng bảo mật. 1282 tests, 102 static analysis rules."
origin: ECC
user-invocable: true
---

# AgentShield — Security Scanner cho Agent Config

Audit Claude Code configuration cho vulnerabilities, misconfigurations, và injection risks.

## Khi nào dùng

- Setup project mới với Claude Code
- Sau khi sửa `.claude/settings.json`, `CLAUDE.md`, hoặc MCP configs
- Trước khi commit config changes
- Security hygiene định kỳ

## Cài đặt

```bash
npm install -g ecc-agentshield
# hoặc dùng npx không cần install
npx ecc-agentshield --version
```

## Scan cơ bản

```bash
# Scan project hiện tại
npx ecc-agentshield scan

# Scan path cụ thể
npx ecc-agentshield scan --path /path/to/.claude

# Chỉ hiện từ severity nhất định
npx ecc-agentshield scan --min-severity medium
```

## Output formats

```bash
npx ecc-agentshield scan                    # Terminal (màu + grade A-F)
npx ecc-agentshield scan --format json      # CI/CD integration
npx ecc-agentshield scan --format markdown  # Documentation
npx ecc-agentshield scan --format html > report.html
```

## Auto-fix

```bash
npx ecc-agentshield scan --fix
# Tự động sửa những gì có thể: replace hardcoded secrets với env vars,
# tighten wildcard permissions, v.v.
```

## Deep analysis (Opus 4.6)

```bash
export ANTHROPIC_API_KEY=your-key
npx ecc-agentshield scan --opus --stream
# Chạy 3 agents: Attacker (Red) → Defender (Blue) → Auditor (Final)
```

## Những gì được scan

| File | Checks |
|------|--------|
| `CLAUDE.md` | Hardcoded secrets, auto-run, prompt injection |
| `settings.json` | Overly permissive allow lists, missing deny lists |
| `mcp.json` | Risky MCP servers, hardcoded env secrets, npx supply chain |
| `hooks/` | Command injection via interpolation, data exfiltration |
| `agents/*.md` | Unrestricted tool access, missing model specs |

## Grade scale

| Grade | Score | Ý nghĩa |
|-------|-------|---------|
| A | 90-100 | Secure |
| B | 75-89 | Minor issues |
| C | 60-74 | Needs attention |
| D | 40-59 | Significant risks |
| F | 0-39 | Critical vulnerabilities |

## GitHub Action

```yaml
- uses: affaan-m/agentshield@v1
  with:
    path: '.'
    min-severity: 'medium'
    fail-on-findings: true
```

## Lỗi nghiêm trọng (fix ngay)

- Hardcoded API keys trong config files
- `Bash(*)` trong allow list (unrestricted shell)
- Command injection trong hooks qua `${file}` interpolation
- Shell-running MCP servers

## Source

https://github.com/affaan-m/agentshield · npm: `ecc-agentshield`
