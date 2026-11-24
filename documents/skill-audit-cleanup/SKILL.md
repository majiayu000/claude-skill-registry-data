---
name: skill-audit-cleanup
description: |
  WorkBuddy 技能库全量审计与清理。扫描所有已注册技能，用真实使用记录判定
  「高频必留 / 低频暂存 / 无用归档」，产出分类报告 + 归档制清理脚本 + 冷库挂载开关。
  触发词：技能清理、技能盘点、技能太多、技能审计、skill cleanup、skill audit、
  技能列表太长、上下文技能清单臃肿、技能调用不准确。
agent_created: true
version: 1.0.0
---

# 技能库审计与清理

对 WorkBuddy 已注册技能做全量盘点、分类、清理。核心原则：**归档制，永不 `rm`**。

## 1. 数据源（关键：usage-log 才是使用证据）

| 路径 | 内容 | 说明 |
|---|---|---|
| `~/.workbuddy/usage-log.json` | `skills` / `mcps` / `activeDays` | **唯一可靠的使用记录**（lastUsedDate、recentDates、firstSeenDate）。30 天窗口 |
| `~/.workbuddy/skills/` | 用户级技能 | 可自由移动，清理主战场 |
| `~/.workbuddy/plugins/cache/` | 插件级技能 | 不可删，只能整插件开关 |
| `~/.workbuddy/connectors/skills/` | 连接器技能 | **disconnected 仍会被注册**，需 UI 断开 |
| `~/.claude/skills/` | Claude Code 技能 | 单独维护 |
| `~/.workbuddy/settings.json` | `enabledPlugins` | 唯一的插件开关 |
| `~/.workbuddy/plugins/marketplaces/` | 市场索引（数百个 SKILL.md） | **不注入上下文**，不用管 |

> 坑：文件 mtime 只是安装/更新时间，不能当「最近使用时间」用。
> 只有 usage-log 里出现过的技能才算真的用过。

## 2. 执行流程

### Step 1 — 扫描

```bash
PY="C:/Users/USER/.workbuddy/binaries/python/versions/3.13.12/python.exe"
"$PY" scripts/scan_skills.py > skills.json 2> err.txt
```

解析每个 SKILL.md 的 frontmatter（name / description / version）+ mtime + 体积 + 文件数。
注意：多值 description 有 `|` 和 `>-` 两种写法，简单正则只取首行会截断，
被截断的几个要单独 `head -30` 读全文。

### Step 2 — 计算真实注册条目数

磁盘上的 SKILL.md 数量 ≠ 注册进上下文的条目数。以 system prompt 的 `<available_skills>`
列表为准核对。市场索引（marketplaces 下）不计入。

### Step 3 — 分类判定

| 分类 | 标准 |
|---|---|
| 高频必留（常驻） | usage-log 有记录，或场景强相关且不可替代 |
| 低频暂存（冷库） | 场景相关但近期未触发，或季节性/项目性需求 |
| 无用归档 | 功能重复、场景无关、平台错配 |

**必须查的三类冲突**：
1. **功能重复组** —— 挑出「描述重叠」的技能组，每组只留一个（留更完整 / 有使用记录的那个）。
2. **同名重复** —— 用户级与插件级同名（如 `humanizer-zh`），会在列表里出现两次。
3. **description 规则冲突** —— 某个技能写了「所有 X 操作必须通过此 skill」，会劫持同类技能的路由，必须改写。

### Step 4 — 分层处置

按性价比排序执行（收益最大优先）：

| Tier | 动作 | 手段 |
|---|---|---|
| T1 | 归档重复/无关技能 | `mv` 到 `~/.workbuddy/skills_archive_<date>/` |
| T2 | 冷库迁移低频技能 | `mv` 到 `~/.workbuddy/skills_cold/`（不在 `skills/` 下即不注册） |
| T3 | 禁用插件 | `settings.json` 的 `enabledPlugins` 设 false（先备份 .bak） |
| T4 | 断开僵尸连接器 | **UI 操作，交给用户**（disconnected 的技能仍被注册） |
| T5 | 改写冲突 description | 编辑 SKILL.md，先备份 |

### Step 5 — 产出

- 审计报告（清单 + 分类 + 场景矩阵 + 启用规则 + 执行指令）
- `execute_cleanup.sh`（分 tier 执行，默认 dry-run，支持 `--rollback`）
- `skill_toggle.sh`（冷库 on/off/status）
- inventory CSV

## 3. 冷库机制

```
~/.workbuddy/skills_cold/<name>    # 不注册
~/.workbuddy/skills/<name>          # 注册
bash scripts/skill_toggle.sh on  <name>   # 挂载
bash scripts/skill_toggle.sh off <name>   # 卸载
bash scripts/skill_toggle.sh status
```

## 4. 硬约束

1. **永不 `rm`** —— 全部用 `mv` 归档，回滚就是把目录 `mv` 回来。
2. **改 settings.json / SKILL.md 前先备份** `.bak-<YYYYMMDD>`。
3. **默认 dry-run** —— 脚本无参数时只打印预览，必须显式传 tier 参数才动手。
4. **内置 seed 技能不可禁** —— `wb-finance-skill` / `cloudstudio-deploy` /
   `geo-map-compliance-guard` 等在 `plugins/cache` 下且不在 `enabledPlugins` 管控内，
   移动会破坏插件缓存，只能接受。
5. **禁用插件前先确认替代路径** —— 例如禁 `tencent-docx` 前要确认
   `tencent-docs-routing` + `tencent-local-office-edit` 能覆盖 Word 需求。

## 5. 复核节奏

每 30 天读一次 `usage-log.json`：
- 常驻技能连续 30 天 0 次 → 降入冷库
- 冷库技能连续两季度 0 次 → 归档删除

## 6. 2026-08-30 基线

78 条 → 约 36 条（磁盘上界 43，-54%）。

已执行：归档 `agent-browser-core` / `browser-skill` / `memory-setup__skillhub` / `dist`；
冷库 `expert-behavior-calibration` / `hongzhua-ruanzhu__skillhub`；
禁用 `tencent-docx`(13) / `weixinpay`(3) / `tabbit`(1)；改写 `web-access` 冲突描述。
待用户：断开飞书连接器（-27）。

### 用户决策偏好（重要）

**不要为了去重而精简数学建模相关技能。** 用户明确要求保留：

- 科研画图双件套（`scipilot-figure-skill` + `figure-generation`）
- 自我改进双件套（`darwin-skill` + `self-improving-agent__skillhub`）
- 全部数学技能常驻（`data-science-stack` / `heuristic-algorithms` / `pyomo` / `mathmodel-latex-skill`），
  包括零使用的，也不进冷库

理由推断：数模竞赛场景下，宁可多几个同类技能做交叉验证，也不愿在关键题上缺工具。
下次审计默认沿用这条约束，除非用户改口。
