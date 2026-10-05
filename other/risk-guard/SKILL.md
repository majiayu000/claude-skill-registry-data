---
name: risk-guard
version: 1.0.0
description: |
  Account ban risk monitor for Claude Code. Detects dangerous usage patterns
  that could trigger rate limiting, account suspension, or banning.
  Auto-triggers on session start. Manual trigger: /risk-guard.
  Checks: concurrent sessions, tool call velocity, automation loops,
  session frequency, config risks, secret exposure, telemetry leaks,
  file permissions. Triggers on: 'risk', '风险检查', '封号检查',
  'ban check', 'account safety', '账号安全'.
allowed-tools:
  - Bash
  - Read
hooks:
  SessionStart:
    - matcher: ""
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-risk.sh"
          statusMessage: "🛡️ Running account risk check..."
---

# /risk-guard — 账号封禁风险监控

自动检测可能导致 Claude Code 账号被封禁的使用模式和配置风险。

## 检查项目

| 检查项 | 风险等级 | 触发条件 |
|--------|----------|----------|
| 并发进程数 | 🔴 CRITICAL | >5 个 Claude 进程同时运行 |
| 工具调用速率 | 🔴 CRITICAL | >500 次/小时 |
| 子 Agent 数量 | 🟠 HIGH | 单会话 >30 个 Agent |
| 会话创建频率 | 🟠 HIGH | 1 小时内 >10 个新会话 |
| 密钥 git 暴露 | 🟠 HIGH | 含密钥文件未被 gitignore |
| 遥测数据残留 | 🟡 MEDIUM | telemetry 目录有 JSON 文件 |
| 文件权限过宽 | 🟡 MEDIUM | 敏感文件权限非 600 |
| 危险模式配置 | 🔵 INFO | bypassPermissions 开启 |

## 风险等级

- 🟢 **SAFE** — 无异常，正常使用
- 🟡 **MEDIUM** — 存在潜在风险，建议关注
- 🟠 **HIGH** — 需要及时处理
- 🔴 **CRITICAL** — 立即处理，可能触发封号

## 使用方式

**自动模式**: 每次启动新会话时自动运行检查

**手动模式**: 输入 `/risk-guard` 执行即时检查

## 手动执行检查

当此 skill 被手动触发时，执行以下命令并将结果展示给用户：

```bash
bash ~/.claude/skills/risk-guard/bin/check-risk.sh
```

根据输出结果：
- 如果全部通过（✅），告知用户当前状态安全
- 如果有警告，逐条解释风险来源和处理方法
- 如果是 CRITICAL，强烈建议用户立即采取行动

## 常见封号原因参考

1. **自动化滥用** — 脚本循环创建大量会话刷用量
2. **账号共享** — 多人/多设备同时使用同一账号
3. **绕过认证** — 使用非官方 API 或篡改认证
4. **违反 ToS** — 生成违禁内容
5. **速率限制** — 短时间内发送过多请求

**不会导致封号的**:
- 使用 bypassPermissions（官方功能）
- 安装第三方插件（官方机制）
- 关闭遥测（用户权利）
- 使用 MCP servers（官方功能）
