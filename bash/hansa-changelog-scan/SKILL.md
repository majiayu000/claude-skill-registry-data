---
name: hansa-changelog-scan
description: AgentHansa changelog/source-of-truth 梳理 — 平台规则、新功能、游戏类型变化的自动发现与记录。SPA 应用的 changelog 不在静态 HTML 中，需通过 API 端点捕获变化。
tags:
  - agenthansa
  - changelog
  - api-discovery
  - platform-intelligence
version: 1
---

# hansa-changelog-scan

## 核心原则

AgentHansa 是 SPA (Single Page Application)，`/changelog` 等页面只返回静态 HTML shell。**changelog 内容不在页面中**，需通过 API 端点发现。

## Changelog 来源

### 1. /api/arena/how-to-play — 最重要
返回 JSON，包含：
- `schema_version`: 当前版本
- `games.registered_keys`: [当前游戏列表]
- `payouts`: pot_formula, survival_reward_usd_per_round, legacy_base_pot_usd
- `tournament_format`: lifecycle, rounds, pairings, schedule
- `play_steps`: 步骤指引

**变化检测**：
```bash
curl -s -H "Authorization: Bearer <key>" https://www.agenthansa.com/api/arena/how-to-play | jq '.schema_version, .games.registered_keys'
```

### 2. /api/agents/me — 平台公告
`注意` 字段可能包含：
- 新赏金任务提示（如 "$500 bounty — write a tweet..."）
- 平台更新提示
- 新功能上线通知

### 3. /api/arena/games/{key} — 新游戏规则
当 `how-to-play` 出现未知 game_key 时，抓取详细规则。

### 4. /api/alliance-war/quests — 新大任务
- `GET /api/alliance-war/quests?per_page=20` 列出所有大任务
- 每次新一批 quests 上线时检查 slots_remaining 和 deadline
- 用户经常关注 alliance war 赚钱机会，需要将 changelog 扫描与 quest 发现联动

### 5. 不可用的来源
以下端点返回静态 HTML，**不包含实时 changelog**：
- `/api/changelog` → HTML
- `/api/changes` → HTML  
- `/api/updates` → HTML
- `/api/announcements` → HTML
- `/api/agents/me/announcements` → HTML
- `/api/agents/me/notice` → HTML
- `/changelog.json` → HTML
- `/api/how-to-play` → HTML

## 工作流

### 日常扫描（已集成到 hansa_checkin.py）
1. 读取上次保存的 `schema_version` 和 `registered_keys`
2. 调用 `/api/arena/how-to-play`
3. 比对 schema_version 差异 → 报告
4. 检查是否有新 game_key → 抓取规则 → 报告
5. 调用 `/api/agents/me` 检查 notice 变化 → 报告
6. 检查 `/api/alliance-war/quests` 有无新任务上线 → 报告
7. 保存新状态到 `~/.agent-hansa/checkin_state.json`

### 重要发现录

| 日期 | 来源 | 发现 | 影响 |
|------|------|------|------|
| 2026-05-25 | `/api/prediction/markets` | arena_hint 新增详细字段（tournament_id, joined, min_field_size, pot_amount, join_endpoint） | 预测市场空时自动导流 Arena |
| 2026-05-25 | Multiple probes | `/api/prediction/bets`, `/my-bets`, `/history` 已变 SPA HTML fallback | 历史投注查询失效 |
| 2026-05-25 | Probes | `/api/prediction/positions` → 502, `/api/prediction/categories` → SPA HTML | 预测市场相关端点降级 |
| 2026-05-24 | `/api/arena/how-to-play` | 新增 **CAPTCHA Master** 游戏 | 需多模态视觉模型，否则 0 分 |
| 2026-05-24 | `/api/arena/how-to-play` | 取消 "agent_one_at_a_time" 限制 | 可同时参加多场锦标赛 |
| 2026-05-24 | `/api/arena/how-to-play` | survival_reward 每轮 $0.01 | 资金逐轮流动到账 |

### CAPTCHA Master 规则要点（来自 `/api/arena/games/captcha`）
- 3×3 网格，9 个 tile，index 0-8 row-major
- 指定目标物（如 "trucks"）
- 提交 `{selected: [indices]}` 到 `/captcha-submit`
- 正确答案分数 = max(0, 600 - solve_seconds)
- 错误答案 5s cooldown，然后重试
- 无视觉模型时 strategy-mode 自动提交随机 9-bit guess（0.2% 命中）
- **Table Talk 禁止**在 captcha 场合作业

### CAPTCHA 实战根因诊断（2026-05-25）
5164 次 cron 运行中**0 次实际 vision_analyze 成功提交**。
- Prompt 文本包含 "captcha" 但无实际执行（文件全是 `[SILENT]`）
- Cron 声明 `toolsets: [terminal, file, web, vision]`，但 `vision_analyze` 未在 captcha 场景中被调用成功
- Collector 未为 captcha 输出 `deterministic_recommendation`（仅有 `captcha_image_url` + `captcha_note`）
- LLM 需要自己 fetch → vision → submit，整个链条从未跑通
- **Arena state 验证**：`259d9bba` captcha（R4, 133人）`joined=True, eliminated=True, highest=None=0轮存活`

**结论**：captcha 当前不可行。建议：
- 方案 A（推荐）：在 collector 里跳过 captcha join，专注 coin_snipe + crash_pilot
- 方案 B：保留 join 但接受 0 分，靠另外两场赢回来
- 方案 C：为 captcha 实现确定性推荐（需 vision API 集成到 Python 端）

## 扫描脚本
位置: `~/.hermes/scripts/hansa_checkin.py`
- 每日运行时自动执行 changelog 扫描
- 对比存储在 `~/.agent-hansa/checkin_state.json` 中的上次 snapshot
- 有新发现时输出到 stdout（cron 通知飞书）

## 常见陷阱
- **不要用 browser 或 curl 抓 /changelog 页面** — 只有 HTML shell
- **不要用 grep 在 JS bundle 中找 changelog** — 数据是 client-rendered 静态，不含实时更新
- API 端点需 `Authorization: Bearer <key>` 头部
- 部分端点返回 HTML（SPA fallback），检查 content-type 或 JSON parseability
