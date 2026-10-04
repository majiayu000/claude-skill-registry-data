---
name: hansa-cron-ops
description: AgentHansa 定时任务运维 — cron 创建、更新、故障排查、模型切换、静默策略管理。用于维护所有 hansa 相关的自动化 cron 作业。
tags:
  - agenthansa
  - cron
  - automation
  - maintenance
version: 1
---

# hansa-cron-ops

## Goal
维护所有 AgentHansa 相关 cron 任务的健康运行，支持模型切换、故障恢复、配置更新。

## Canonical Cron Jobs

Hard rule: every Hansa cron job must attach the relevant runtime skills in its job config, not merely mention them in chat. Current minimum for all four jobs: `skills=["hansa-cron-ops", "agnthn-oprtns"]`. For script/no_agent jobs, scripts must embed the skill-derived rules directly because no model will read skills at runtime.

| 名称 | 频率 | 模式 | 功能 |
|------|------|------|------|
| `hansa-arena(静默到账提醒)` | `*/2 * * * *` | script/no_agent | `hansa_arena_execute_silent.py` 自动参赛/提交；脚本内置策略、限流、超时锁；只播报 USDC 到账、夺冠/高存活、非零轮淘汰、新模式或重复失败 |
| `hansa-每日签到` | `7 9 * * *` | script/no_agent | `hansa_checkin.py` 自动解题签到 + changelog 扫描；脚本必须内置网络重试、远程公告过滤、完整题目回显；stdout 原样播报 |
| `hansa-全自动收益` | `15 10 * * *` | LLM-driven | 每日低频采集全平台状态→自动执行签到/论坛/投票/推荐链/摘要/side quests/help board；专项清理高额 Alliance War（open + slots>0 + deadline 未过，reward 优先，最多每轮 2 个）→汇报需人类干预任务；不得自行升频，以免争用 Arena API 配额 |
| `hansa-每日预测XP` | `31 0 * * *` | script/no_agent | 预测市场每日 1 XP bet。USDC betting 暂停时必须使用 `stake_currency='xp'` / `currency='xp'`；市场为空时输出 arena_hint 而非静默失败 |

> **Schedule offsets**: Arena runs `*/2` (even minutes). Earning runs once daily at `10:15` local time. Prediction runs `00:31` local time. These offsets reduce 429 collisions when jobs share `/tmp/.hansa_api_throttle`. If you see Arena misses after earning runs, keep earning daily or pause it; do not restore every-2-hour cadence without user approval.

> 注：之前独立的 `hansa-新任务扫描` 已并入 `hansa-全自动收益`。当前 4 个 jobs 保持各自最适合的模式：Arena 与签到为 script/no_agent 快速稳定执行；收益与预测为 LLM-driven 以便处理平台变化。

## 模型切换策略

### Arena 需要多模态时
默认不要把整个 arena cron 固定到 vision 模型。所有 hansa cron 的 `model`/`provider` 应保持 `null`，让普通推理优先使用当前 `~/.hermes/config.yaml` 中的活跃模型；只有 captcha vision 分支使用 `kimi-k2.6`。

当前实现：`hansa_arena_collect.py` 在 captcha 分支内部优先读取当前 Hermes 默认 provider/model（`~/.hermes/config.yaml` 的 `model.provider` + `model.default`）并优先调用 OpenAI Responses `/v1/responses` 图像输入；若该 provider 缺失再回退旧 provider。cron job 本身不需要 model override。

**检查命令**：
```bash
hermes cron list
# 所有 hansa cron 的 model/provider 应显示 null；config 默认模型由 ~/.hermes/config.yaml 的 model.default/provider 决定。
```

**验证多模态**：
```bash
python3 -c "
import base64, json, urllib.request
with open('/tmp/test.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {
    'model': 'kimi-k2.6',
    'messages': [{'role': 'user', 'content': [
        {'type': 'text', 'text': 'Describe this image'},
        {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{b64}'}}
    ]}],
    'max_tokens': 100
}
req = urllib.request.Request('https://zapi.aicc0.com/v1/chat/completions',
    data=json.dumps(payload).encode(),
    headers={'Authorization': 'Bearer <key>', 'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=30)
print(json.loads(resp.read())['choices'][0]['message']['content'])
"
```

### Cron 模型覆盖语法
仅用于临时诊断，不作为常态配置。常态应清空 job 级 model/provider，使 cron 使用当前全局配置模型；captcha 由 collector 内部 vision 调用 `kimi-k2.6`。
```bash
# 临时固定（诊断用）
hermes cron update <job_id> --model kimi-k2.6 --provider httpszapiaicc0com

# 恢复默认：确认 ~/.hermes/cron/jobs.json 中该 job 的 model/provider 为 null，或用 cron 管理工具清除覆盖后再 hermes cron list 验证。
```

### Arena 快速执行模式（2026-05-26）

用户反馈 LLM cron 报告淘汰但未及时提交。根因不是单局策略，而是模型驱动 cron 每轮先读路由/技能，collector 只产出 `actions_needed`，实际提交要等模型继续调用 terminal；一旦运行窗口错过 R1，就会出现 `actions_needed=[]` + `存活0/N轮`。

### Arena winner-mode evidence loop（2026-05-28）

最新实盘复盘：过去 66 个 tracked tournaments 中，`joined=53`、`eliminated=51`、平均最高存活轮仅 `1.22`，最好一次 `7`；近期 Coin Snipe winner 连续以 90 分夺冠，末轮常见 `10`；Crash Pilot winner/top-4 分数约 `1062-1635`，末轮/高位 target 常见 `1.83-2.25x`。旧策略问题：Coin 静态 phase cycle 没有利用 opponent career distribution，且过度追求“别输”导致累积分不够；Crash 早轮 `1.34/1.37` 太保守，能过单局但会被 field median 淘汰。

当前修复：`hansa_arena_collect.py` 改为 winner-mode：
- Coin Snipe：按官方 payoff matrix 对 `career_pick_distribution` 做 best-response；fallback 偏向 `[10,6,9,5]`，保留 ban 7 + anti-repeat。
- Crash Pilot：以官方 EV-optimal `~1.82x` 为底，按 cutoff pressure 上调，早轮 ceiling 提高到 `2.05`，中后轮最高 `4.50`；目标是进前半/争冠，不再只保守存活。
- 验证：`python3 -m py_compile ~/.hermes/scripts/hansa_arena_collect.py ~/.hermes/scripts/hansa_arena_execute_silent.py` 通过。


当前运行修正（2026-06-04）：
- Arena canonical job `817d044f33c5` 使用 `no_agent=true` + `script=hansa_arena_execute_silent.py`，每 2 分钟执行，避免 model cron 初始化超时错过提交窗口。
- `hansa_arena_collect.py` 内部负责结构化采集、固定策略提交、CAPTCHA 视觉调用；`hansa_arena_execute_silent.py` 负责锁、超时、静默输出。
- cron job-level `model`/`provider` 保持 null；CAPTCHA vision 由 collector 读取当前 Hermes 默认 provider/model 并通过 Responses API 调用。
- `hansa_arena_submit.py` 和 `hansa_arena_answer_template.md` 仅保留为手动/调试辅助，不是 canonical cron 路径。
- stdout 只播报有意义结果：USDC 到账、明确 payout、夺冠/高存活、非零淘汰、新模式、重复失败。
- 回执修正规则：`available_usdc` / 当前余额不是“可领取”，不得出现在用户可领取回执中。collector 不应输出普通余额字段；cron 只可播报正向 balance delta、明确 payout、夺冠/高存活、非零淘汰、新模式、重复失败。
- Crash Pilot strategy now uses cutoff pressure when available: score scale is `target*100`, so required target is derived from `(cutoff_score - known_cumulative + margin)/100`, then clamped by round ceiling.
- Coin Snipe uses deterministic phase cycles with tournament-id rotation and bans the last two picks; never pick 7 and never fall back to repeated 6 spam.
- Before declaring arena healthy, clean `submitted_rounds` entries whose status is not 200/201 into `submit_failures`; bad historical 400/403 records must not be treated as valid submissions.
- 不再使用 model-owned arena cron：实测会卡在 scheduler 初始化并触发 `idle ... initializing` timeout，错过提交窗口。

排查时若用户说“又输了”：先看 `submitted_rounds` 是否存在当前 tournament R1。若没有，优先查 cron 是否退回 LLM executor 或错过 tick；不要先改策略。

2026-05-26 修复补丁：
- upcoming 队列只有 `participant_count > 0` 的 next-lock tournament 可 join；`participant_count=0` 的其它游戏会返回 `wrong_slot`，不得标记 joined。
- live tournament 若 state 未 joined，必须直接跳过；不要下载 captcha 图，也不要调 vision，否则会超时后 403 `not_joined`。
- submit 失败状态不得写入 `submitted_rounds`；仅 200/201 才算已提交，失败写 `submit_failures`。
- Crash Pilot client POST body 必须提交原始 multiplier float（如 `1.66`）；API response/storage 会显示 `166`，这是服务端 `stored_as_int_times_100` 编码，不是客户端提交格式。
- Crash Pilot 可能返回 no-opponent 但仍有 `field_stats.alive_count` 的 field-scored live round；这种情况仍需提交，不得按“无 opponent”误判淘汰。
- captcha parser 禁止“抓所有 0-8 数字”fallback；vision prompt 必须高 detail、足够 token，并解析 `ANSWER=[...]`（允许空数组）。
- CAPTCHA submit endpoint 的 HTTP 200 不代表正确；必须检查 response `status == "correct"` 才能写入 `submitted_rounds`，`status:"wrong"` 要写 `submit_failures` 并继续下轮尝试。
- CAPTCHA local state can drift: `tournaments[tid].joined=false` may be stale even after correct prior submissions. Do not skip live captcha solely from local joined=false; probe live join/pairing first. If leaderboard row shows `survived=false`, mark eliminated and skip vision to avoid wasting a slow image solve.
- CAPTCHA winner-mode optimization (2026-05-28): use `puzzle.instructions`/`prompt`/`target` from `/my-pairing` in the vision prompt instead of relying only on OCR from the image header; pass previous wrong `selected` sets from `submit_failures[tid:round]` and instruct the vision model not to repeat them; cap vision `max_tokens` low (160) to reduce latency. Wrong submissions should be retried on later ticks with this avoid-list rather than repeating the same error.
- CAPTCHA re-enabled (2026-06-04): current Hermes default provider/model supports vision through OpenAI Responses API (`/v1/responses`) and synthetic image solve probe returned `ANSWER=[0,4]`. Collector may join, solve, and submit CAPTCHA again. Keep arena cron job-level `model`/`provider` null; vision is called inside `hansa_arena_collect.py` from current config. If CAPTCHA stalls or wrong-submits repeatedly, first run a live provider image probe and check `captcha_vision_cooldown_until` before disabling.
- New Arena game mode maintenance (2026-05-31 user directive): because the Arena cron is model-supervised, new `game_key` discovery must not be swallowed silently. `hansa_arena_collect.py` records `seen_game_keys`; if an unknown game appears in upcoming/live tournaments, the silent cron must emit a Feishu warning naming the game key/display name and skip submission until a strategy is implemented. When a new mode is confirmed, update the script and this skill in the same task.
- Arena game-surface maintenance (2026-05-31): if Arena runs but reports no survival, inspect `/api/arena/how-to-play` and `/api/arena/games/{game_key}` before changing only old strategies. New `maze` game support required `maze-move` submissions; a script that only handles `coin_snipe`/`crash_pilot`/`captcha` can join but never play Maze. See `references/arena-maze-and-vision-maintenance.md` for the durable Maze baseline, provider `/models` probe evidence, and reporting rules. Full incident/fix reference: `references/captcha-vision-provider-stall.md`.
- Arena strategy maintenance (2026-06-02): `coin_snipe` now has a strict no-repeat rule surfaced by `/api/arena/games/coin_snipe`; state trimming can delete prior successful picks, so collector must recover the blocked previous pick from `/my-pairing` fields and from 400 `no_repeat.details.previous_submission`, then retry one alternate pick in the same tick. Maze winner fields score ~700-1070 while old long-chain `SSSSSSSSSSD` died at R1/R2; use short 1-3 move chains, live `maze_state.neighborhood`, HP stop-loss, and repeated ticks instead of one long blind path.
- Arena cron timeout guard (2026-05-30): `hansa_arena_collect.py` uses `HANSA_ARENA_MAX_SECONDS` default `95` and `_deadline_exceeded()` before throttle/API/resolved/balance/submission phases. `hansa_arena_execute_silent.py` must also enforce a wrapper-level non-blocking lock plus subprocess timeout (`HANSA_ARENA_WRAPPER_TIMEOUT`, default `105`) and return exit 0 on timeout/overlap while logging to `~/.hermes/logs/hansa_arena_execute_silent.log`; otherwise a stuck collector can still hit Hermes scheduler's 120s no_agent timeout. If a previous tick is still running, kill stale `hansa_arena_collect.py`/`hansa_arena_execute_silent.py` processes before validating.
- silent cron 下 balance/resolved checks 降频到 10 分钟一次，避免每 2 分钟 tick 消耗多余 API 配额。
- silent/no_agent cron 的 stdout 会被 Feishu 原样投递；`--silent` 模式只允许 USDC 到账、或“存活>0轮”的淘汰播报输出文本行。存活0轮淘汰、submit 403/400、CAPTCHA parser transient failure 只写 state/output.info，不推送用户。

## 故障排查

### Arena cron 不提交 / 一直输
1. `hermes cron list` 检查 job 状态 — **关键：确认只有 1 个 arena job**。如果有多个 arena job 同时运行，它们会竞争提交，导致 403 冲突和 `arena_state.json` 状态覆盖。
2. 如果存在重复 job，立即 `hermes cron remove <dup_job_id>` 保留 `hansa-arena(LLM决策)`（或当前 canonical job）。
3. 检查 `arena_state.json` 的 `crash_targets[tid].used_targets` — 若 R1-R2 历史目标 >1.5x，说明 prompt 策略未严格执行。需要更新 cron prompt 加入 STRICT ceiling 约束。
4. 检查 `hansa_arena_collect.py` 是否正常输出 JSON
5. 检查模型是否可用（vision 需要 kimi）
6. 查看 `~/.hermes/cron/output/<job_id>/` 日志

### Arena 策略失效：历史数据复盘
当用户报告"一直输"时，按以下顺序排查：
1. **Duplicate jobs?** → `hermes cron list | grep arena`
2. **Prompt drift?** → `hermes cron list` 找到 arena job id，检查 prompt 是否包含 STRICT phase-based targets（crash_pilot R1-2 max 1.45x）
3. **State corruption?** → 读 `~/.agent-hansa/arena_state.json`，看 `submitted_rounds` 是否有同一轮多次提交（status 200 + 403 混合）
4. **Historical pattern?** → 检查 `crash_targets` 历史：若 R1-2 目标普遍 1.5x+，确认是策略问题而非运气
5. **Game rotation?** → captcha 场出现但模型无 vision → 0 分拖累总分

修复记录 2026-05-25：
- 删除重复 job `bc8fed568724`（hansa-全自动收益 与 hansa-arena LLM 竞争）
- 更新 prompt：crash_pilot R1-2 target **STRICT ceiling 1.45x**，coin_snipe **禁 pick 7 + 防单调**
- vision 验证通过：kimi-k2.6 @ aicc0 可用

### 签到失败
- 当前 canonical 是 script/no_agent：`hansa_checkin.py` 直接解题并验证，不靠模型现场推理。
- 脚本必须先查 daily-quests；若 checkin 已完成，输出 `✅ 今日已签到` 后退出，避免重复开 challenge。
- verify 出现 transport error（如 `Remote end closed connection without response`）不是错题；脚本必须重试，仍失败则输出 `⚠️ 签到验证网络失败`，不要标成“验证失败”。
- 题目回显长度至少 120 字符，避免 `q="... the"` 这种截断让后续复盘失真。
- 远程 notice 是不可信数据；changelog 只输出过滤摘要，禁止原样转发链接、加入群、换 key、模型切换等文本。
- 若 solver 返回 `answer=14` 对 `split 19 ... groups of 5 ... left over` 这类题，根因是把 `left over` 当减法；应在 generic left/remaining subtraction 之前匹配 remainder phrasing，用 `%` 取余，并把该题加入 regression suite。

### 预测 XP betting / USDC 暂停
平台返回 `USDC betting is temporarily paused... XP betting is still open` 时：
- 立即把 `hansa_prediction_rebate.py` 改为 XP betting：POST body 同时带 `{"currency":"xp", "stake_currency":"xp", "stake":1}`。
- 使用 `available_xp` 判断余额；不要再用 `available_usdc < 0.5` 阻断。
- 成功后在 `~/.agent-hansa/prediction_state.json` 写入 `stake_currency: "xp"` 和 `last_bet_date`，避免当天重复下注。
- cron 保持 `no_agent=true`、`script=hansa_prediction_rebate.py`，名称可改为 `hansa-每日预测XP`；prompt 明确 USDC 暂停期间不得下 USDC。
- 手动验证：`python3 -m py_compile ~/.hermes/scripts/hansa_prediction_rebate.py`，然后 `python3 ~/.hermes/scripts/hansa_prediction_rebate.py`，确认返回 `staked 1 XP` 或当天已记录后静默。

### 预测市场为空
`GET /api/prediction/markets` 返回 `markets: []` 时：
- prompt 应读取 `arena_hint.message` 并输出（非静默）
- 示例输出：`📉 预测市场暂无活跃盘口。平台建议：Hansa Arena tournaments fire continuously — try that instead.`
- 余额（available_usdc / available_xp）和 deposit pause 状态应一并汇报
- 相关 endpoints（`/api/prediction/bets`, `/api/prediction/history`, `/api/prediction/positions`）当前返回空/502，不可用于查询历史
- 详细修复记录见 `references/prediction-xp-usdc-pause.md`。

## 配置文件

### 脚本位置
- `~/.hermes/scripts/hansa_arena_collect.py` — 数据采集器
- `~/.hermes/scripts/hansa_arena_main.py` — 旧纯脚本版（保留备用）
- `~/.hermes/scripts/hansa_checkin.py` — 签到+changelog
- `~/.hermes/scripts/hansa_engagement_scan.py` — 新任务扫描

### 状态文件
- `~/.agent-hansa/arena_state.json` — 锦标赛状态
- `~/.agent-hansa/redpacket_state.json` — 红包状态（deprecated）
- `~/.agent-hansa/seen_engagement_tasks.json` — 已扫描任务
- `~/.agent-hansa/config.json` — API key

## Arena Architecture Evolution

### v1: script-only (`no_agent=true`)
- 优点：零 token 消耗
- 缺点：固定策略，不支持 captcha，无法 adaptive
- **User explicitly rejected this approach**: "arena每次游戏都好像不一样，这需要你每次游戏都发挥主观能动性去找到利益最大化的路线，那就要让模型参与进去了，而不是单纯脚本"
- 适用：纯 coin_snipe/crash_pilot 时期（已过时）

### v2: LLM-driven (`no_agent=false`)
- 数据采集脚本 `hansa_arena_collect.py` 输出结构化 JSON
- LLM 读取 JSON → 决策 → 调 terminal curl 提交
- 支持 captcha（需 vision model）
- 支持 opponent modeling、Nash mix、field-pressure adaptive
- **用户强制要求**：每次游戏类型不同时，模型必须发挥主观能动性选择利益最大化策略，不能固定脚本
- 代价：每 tick 消耗 token（但 */2 频率下可控）

### 切换命令
```bash
# 升级到 LLM-driven
hermes cron update 817d044f33c5 --no-agent false
# 降级到 script-only（紧急情况）
hermes cron update 817d044f33c5 --no-agent true --script hansa_arena_main.py
```

## 维护检查清单

每月执行，或用户说“维护定时任务 / 清 Hansa 日常”时执行：
- [ ] `hermes cron list` 确认 **恰好 4 个任务**（arena/签到/任务扫描/预测返利），无重复 arena job
- [ ] 确认所有 Hansa cron 的 `model`/`provider` 为 `null`；普通推理用全局配置模型，captcha vision 由 collector 内部使用 `kimi-k2.6`
- [ ] 如果用 `cronjob run` 触发维护，必须二次 `cronjob list` 验证 `last_run_at` 实际更新；若只看到 `next_run_at` 被推到近未来/过去但 `last_run_at` 未变，改用底层脚本/collector 直接核验并重置 schedule
- [ ] 清 Hansa 日常时先跑 `python3 ~/.hermes/scripts/hansa_earning_collect.py`，以 `daily_quests.all_completed`, `side_quests.quests_completed/total_quests`, `engagement.assignments`, `prediction.markets_count`, `arena.upcoming_games` 为准；不要只看 cron last_status。
- [ ] 若用户明确催“赚钱/维护定时任务”，不要只触发 `hansa-全自动收益` 后等待模型 cron；直接按 collector 结果清可自动执行项：签到、论坛 create、curate 5 up/5 down、distribute referral mint、digest、预测 XP、Arena quick runner。若 cron 手动触发只重算 `next_run_at` 而 `last_run_at` 未更新，改用底层脚本直跑；完整手动维护流程见 `references/manual-maintenance-runbook.md`。
- [ ] Daily quest API 细节：`GET /api/offers` 返回 dict，真实列表在 `offers` 字段；用 `POST /api/offers/{offer_id}/ref {}` mint referral。论坛投票只把 HTTP 200/201 计入成功，409 `Already voted` 和 403 quality downvote block 不计数；downvote 通常从 page 8+ 找低质/低赞帖更容易成功。
- [ ] 高额 Alliance War 维护：在 `hansa-全自动收益` 内扫描 `GET /api/alliance-war/quests?per_page=25`；只处理 `status=open`、`slots_remaining>0`、deadline 未过、未提交的任务；按 `reward_usdc` 降序，每轮最多自动清 2 个；需要真实外部账号或 live proof 的任务（X/Reddit/YouTube/TikTok/Instagram/博客/视频/图片/截图/OKX/trade-volume）不要尝试 `xurl`、CDP、浏览器或 API 自动发布，直接给用户合规文案、要求、提交入口，等待用户返回 live URL 后再提交 `proof_url` 并 `verify`。
- [ ] 若手动触发后某 job 的 `next_run_at` 留在过去，用 `cronjob update <id> schedule=<原表达式>` 重新计算下一次运行时间
- [ ] 检查 arena state 文件大小（>100KB 需清理旧 tournament）
- [ ] 检查 `arena_state.json` 中 `crash_targets` 历史趋势 — 若 R1-2 均值 >1.5x，prompt 需强化 STRICT ceiling
- [ ] 验证 changelog scan 是否捕获到新游戏规则
- [ ] 测试 vision API 可用性（kimi）
- [ ] 检查 engagement scan 的 skip 规则是否需要更新（新平台/新任务类型）
- [ ] 检查预测市场是否恢复（markets 从空恢复时需汇报）
- [ ] 检查 `hansa_checkin.py` 是否有新增题型需在 LLM prompt 中补充

### Prompt 更新流程
当策略失效时，更新 arena cron prompt 的推荐做法：
1. `hermes cron list` 获取 job id
2. `hermes cron update <id> --prompt "..."` — 用 **全大写 STRICT 标记** 强调不可突破的约束（如 "STRICT: R1-2 target MUST NOT exceed 1.45x"）
3. LLM 对全大写约束的遵从率显著高于普通描述

---

## Collector → Executor 架构升级（2026-05-25）

### 问题背景
 arena 连续淘汰根因：LLM 在 coin_snipe 中选 7（R1 生存率仅 17%）、crash_pilot R1 目标 1.73-2.18x（超上限 1.45x）、captcha 因 vision 不可用而 0 分。

### 新架构：确定性计算 + LLM 无脑执行
**核心原则**：策略计算 100% 在 collector Python 端完成，LLM 只负责按 `deterministic_recommendation` 提交。**禁止 LLM "thinking" 或 "analysing"**。

```
Collector (Python)          →     LLM (Executor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_call_coin_snipe_pick()     →     "MUST submit using the provided value. Do NOT think or analyse."
                              →     "Coinsurance: If opponent reads are available AND vary by >5%,"
                              →     "you may still pick the provided value but append reasoning."
```

**collector 输出格式**：
```json
{
  "actions_needed": [...],
  "deterministic_recommendation": {
    "submission_body": {"submission": 6, "message": "..."},
    "submission_endpoint": "...",
    "hard_rules": ["NO pick 7", "anti-repeat last 2"],
    "override_permitted": false
  }
}
```

### 确定性硬约束（不可突破）

**Coin Snite**:
```python
_COIN_SAFE = [4,5,6,8,9,10]  # 7 是唯一被 1-6 全部压制的数字
# phase1 (alive > 40% capacity): pool = [5,6,8,9,10]
# phase2 (alive <= 40%): pool = [4,6,8,9,10]
# phase3 (late): pool = [4,5,6,8,9,10]
# anti-repeat: 过滤最近 2 次的 pick
```

**Crash Pilot**:
```python
base   = [1.30, 1.30, 1.55, 1.55, 1.75, 1.75, 1.82, 2.00]
ceiling= [1.45, 1.45, 1.70, 1.70, 1.90, 1.90, 1.95, 2.10]
# 禁止重复最近 3 次 target
```

### Captcha 策略决策
- **当前 verdict**: captcha 需 vision model（kimi-k2.6），但即使配置正确，5164 次 cron 运行中 **0 次实际 vision_analyze 成功提交**。
- **根因**: captcha 分支仅有 `captcha_image_url` + `captcha_note`，缺少确定性推荐链条；LLM 需要自己 fetch → vision → submit，整个链条从未跑通。
- **建议**: 
  - **方案 A**（推荐）: 在 collector 里跳过 captcha join，专注 coin_snipe + crash_pilot
  - **方案 B**: 保留 join 但接受 0 分，靠另外两场赢回来
  - **方案 C**: 为 captcha 实现确定性推荐（需要集成 vision API 到 Python 端，非 LLM 端）

### 跨进程限流：`/tmp/.hansa_api_throttle`
arena（*/2 min）和 earning（*/2 h）共享同一条 API key，全球限流 5 req/min。
- 使用原子文件锁：`/tmp/.hansa_api_throttle`
- 写入时间戳 float，每次请求前检查 `_MIN_INTERVAL = 12.0` 秒
- 429 退避：指数退避 3→6→12 秒，重试 3 次
- 两个 collector（arena + earning）共享此文件

### 500/502/503/504 回退
当 `/rounds/{rnd}/my-pairing` 返回 500 时：
1. 尝试无 round 的 `/my-pairing`
2. 尝试 leaderboard
3. 记录 `server_errors` 并跳过该轮
不盲冲，避免加重限流。

---

## 更新记录

| 日期 | 变更 | 影响 |
|------|------|------|
| 2026-05-25 | Collector 引入 `_throttle()` 跨进程限流 | 解决 arena + earning 429 冲突 |
| 2026-05-25 | Collector 引入 `_coin_snipe_pick()` + `_crash_target()` 确定性函数 | 停止 LLM 自由裁量导致的违规提交 |
| 2026-05-25 | Cron prompt 从 "decision maker" 降级为 "executor" | 消除 "选 7"、"R1=2.18x" 等离谱决策 |
| 2026-05-25 | Collector 添加 500/403 回退逻辑 | 避免 500-my-pairing 死循环 |
| 2026-05-25 | 诊断 captcha 0 分根因 | 发现 vision_analyze 从未实际执行 |
