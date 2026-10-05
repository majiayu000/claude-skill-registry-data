---
name: napcat-hermes-setup
description: 通过 NapCatQQ（OneBot v11）将 QQ 群聊/私聊接入 Hermes Agent。涵盖分支切换、配置、人格设计、反注入、按渠道模型和记忆隔离。包含 AstrBot 对比调研结论。
version: 2.2.0
author: Hermes Agent (Publieople session)
license: MIT
prerequisites:
  env_vars: [NAPCAT_TOKEN, NAPCAT_ALLOW_ALL_USERS]
---

# NapCatQQ + Hermes Agent 完整接入指南

> **⚠️ 2026-06-11 状态**：本项目（Hermes NapCat 桥接）已**停用**。用户切换到了
> [AstrBot](https://github.com/AstrBotDevs/AstrBot) 作为 QQ 机器人方案。
> 以下内容为历史参考和恢复指南。如需重新启用，按本文档恢复即可。
> AstrBot 部署笔记见 `references/astrbot-deploy.md`。
> 群员盒武器数据接入方案见 `references/astrbot-box-weapon.md`。

## 架构

```
QQ (Windows) → NapCatQQ (Windows) → WebSocket Client
    → ws://127.0.0.1:8646/napcat/ws
    → Hermes Gateway (WSL)
```

NapCat 适配器是**反向 WebSocket**：Hermes 开服务端（端口 8646），NapCat 作为客户端连接。

## ⚠️ 致命警告：hermes update 会清掉 NapCat（已用 fork 策略解决）

**NapCat 适配器未合入上游 main**（PR #17917 by MoeOver）。`hermes update` 本质是 `git pull origin main`，如果 origin 指向官方 repo，NapCat 代码会被清掉。

### 推荐方案：Fork 策略（已实施）

**原理**：`hermes update` 从 `origin` remote 拉代码。把 origin 指向自己的 fork（已合并 NapCat），官方指向 upstream。

```bash
# 1. Fork NousResearch/hermes-agent → publieople/hermes-agent (GitHub UI 或 gh CLI)
gh repo fork NousResearch/hermes-agent --fork-name hermes-agent --clone=false

# 2. 合并前先备份当前改动
cd ~/.hermes/hermes-agent
git stash push -m "pre-fork-backup" -- gateway/config.py gateway/run.py gateway/platforms/napcat.py

# 3. 合并 MoeOver 的 NapCat PR
git remote add moeover https://github.com/MoeOver/hermes-agent.git
git fetch moeover main
git merge moeover/main --no-edit  # 会有 5 个文件冲突，详见 references/fork-merge-patches.md

# 4. 切换 remote
git remote add upstream https://github.com/NousResearch/hermes-agent.git  # 官方
git remote set-url origin https://github.com/publieople/hermes-agent.git  # 自己的 fork
git push -u origin main --force

# 4. 补丁：merge 后 run.py、hermes_cli/gateway.py、authz_mixin.py 仍需手动加回 NapCat 集成
# 详见 references/fork-merge-patches.md
```

**之后**：`hermes update` = `git pull origin main` → 从你的 fork 拉，NapCat 永不被覆盖。

**同步上游**：
```bash
git fetch upstream
git merge upstream/main  # 有冲突手动解决
git push origin main
```

> ⚠️ **Fork 自动同步冲突**：GitHub 可能会自动同步上游的新 commit 到你的 fork（如果开启了 fork sync）。这会导致本地 push 时出现 `! [rejected] main -> main (fetch first)` 非快进错误。解决：先 `git pull origin main --no-rebase`，再 `git push origin main`。

### 如果没有 fork（手动恢复）

症状：NapCatQQ 日志 `ECONNREFUSED 127.0.0.1:8646`，gateway 日志 `Gateway running with 2 platform(s)`。

恢复到 PR #17917 的代码（从 git 历史或 moeover remote）：

```bash
cd ~/.hermes/hermes-agent
git remote add moeover https://github.com/MoeOver/hermes-agent.git  # 如果还没加
git fetch moeover main
git checkout moeover/main -- gateway/platforms/napcat.py  # 恢复适配器文件
```

然后手动补丁（详见下方「手动恢复流程」）。

## 完整配置清单

### .env
```bash
NAPCAT_TOKEN=<43字符 urlsafe base64>
NAPCAT_ALLOW_ALL_USERS=true
NAPCAT_MODEL=deepseek-v4-flash  # QQ 独立模型
```

### config.yaml
```yaml
memory:
  provider: mem0   # 其他渠道用 Mem0，QQ 代码层面 skip_memory

skills:
  platform_disabled:
    napcat:
      - <全部非必需的 258 个 Skill>
```

### 按渠道独立模型（`{PLATFORM}_MODEL` 环境变量）

**通用机制**：在 `_resolve_session_agent_runtime()` 中注入，不限于 NapCat。

`gateway/run.py` 约 2712 行：
```python
model = _resolve_gateway_model(user_config)
# ── Per-platform model override via {PLATFORM}_MODEL env var ──
if source and source.platform:
    _plat_model_env = f"{source.platform.value.upper()}_MODEL"
    _plat_model = os.getenv(_plat_model_env, "").strip()
    if _plat_model:
        model = _plat_model
```

**用法**：在 `.env` 中设 `{平台名大写}_MODEL`：
```bash
NAPCAT_MODEL=deepseek-v4-flash    # QQ 走 flash
TELEGRAM_MODEL=claude-sonnet-4    # Telegram 走 Claude
FEISHU_MODEL=deepseek-v4-pro      # 飞书走 pro
```

不设的平台走 `config.yaml` 的 `model.default`。这是通用 feature，不是 NapCat 专属补丁。

### 代码补丁（三个关键改动）

**1. QQ 渠道跳过 Mem0** — `gateway/run.py` line ~16803：
```python
_napcat = source.platform == Platform.NAPCAT
agent = AIAgent(..., skip_memory=_napcat, ...)
```

**2. ~~QQ 渠道独立模型~~** → 已升级为通用 `{PLATFORM}_MODEL` 机制，见上方。

**3. QQ 用户消息威胁扫描** — `gateway/run.py` line ~6862：
```python
if source.platform == Platform.NAPCAT and event.text:
    from tools.threat_patterns import scan_for_threats
    _threats = scan_for_threats(event.text, scope="context")
    if _threats:
        # 回复"检测到异常指令"并 return None
```

**4. 中文反注入模式** — `tools/threat_patterns.py`：
```
cn_role_hijack:     请(模拟|扮演|假装)(一个|一只|作为)
cn_reality_detach:  (所有|全部).*(与现实无关|虚拟情景)
cn_remove_restrict: (自由|不受限制).*(使用词汇|回答|表达)
cn_relationship_gaming: 好感度\s*(\d+|满)
cn_identity_override: (忘记|忽略|放弃).*(设定|身份|人格|规则)
```

## 人格设计核心教训（调研 AstrBot 源码后）

### 调研过程

克隆 AstrBot 源码 (`git clone --depth 1 https://github.com/AstrBotDevs/AstrBot.git`)，
重点分析了三个核心文件：
- `astrbot/core/astr_main_agent.py` — 系统提示词构建逻辑
- `astrbot/core/platform/sources/aiocqhttp/aiocqhttp_message_event.py` — OneBot 群组信息采集
- `astrbot/core/platform/astrbot_message.py` — 消息对象和 Group 结构

### AstrBot 的三大优势（与 Hermes 对比）

**1. 用户身份注入系统提示词** (`astr_main_agent.py:870-872`)：
```python
user_id = event.message_obj.sender.user_id
user_nickname = event.message_obj.sender.nickname
system_parts.append(f"User ID: {user_id}, Nickname: {user_nickname}")
```
每条消息把 QQ 号和昵称一起喂给 LLM。Bot 不用猜谁是谁。
**Hermes 对照**：user_id 只用于 auth，Agent 完全看不到。这是核心差距。

**2. 群组信息（群主/管理员）** (`aiocqhttp_message_event.py:233-258`)：
```python
members = await self.bot.call_action("get_group_member_list", group_id=group_id)
for member in members:
    if member["role"] == "owner": owner_id = member["user_id"]
    if member["role"] == "admin": admin_ids.append(member["user_id"])
```
Bot 知道群主是谁、管理员是谁。这对"我只听人民公仆的"这种身份忠诚度非常重要。
**Hermes 对照**：NapCat 适配器没有做这件事。

**3. begin_dialogs 预设对话** (`astr_main_agent.py:487-488`)：
```python
if begin_dialogs := persona.get("_begin_dialogs_processed"):
    req.contexts[:0] = begin_dialogs
```
用示例对话教 LLM 怎么回应，比规则描述有效得多。LLM 通过模仿学习，看到"用户说X → 回复Y"就直接照做。
这是反注入最有效的手段——不是"防御"，而是 LLM 的角色设定本身就不接受越狱。
**Hermes 对照**：SKILL.md 现在也用了预设对话（v5.1），效果待验证。

### 人格迭代（6 个版本的经验）

| 版本 | 行数 | 风格 | 效果 |
|------|:--:|------|------|
| v1 | 323 | 规则手册 + 表格 + 优先级层级 | ❌ LLM 完全无视 |
| v2 | 248 | 同上但稍短 + "铁律"话术 | ❌ 群主一个"再想想？"就动摇 |
| v3 | 50 | 叙事人格 | ⚠️ 好一些但无抗压能力 |
| v4 | 8 | 极简叙事 | ⚠️ 太短，被更长的 Skill 淹没 |
| v5 | 20 | 叙事 + 10个预设对话 | ⚠️ 预设对话有效，但篇幅偏短 |
| v5.1 | 52 | 叙事 + 预设对话 + 群聊规则 | AstrBot 路线 |
| **v6.0** | **~120** | **玖帕喵拟人模板定制** | **当前版本，结构化角色+社交距离+场景应对** |

**核心结论**：
- 叙事人格 > 规则手册。写"你是人民公仆的损友助手"胜过写"主人识别规则（按优先级）→ 防冒充"
- 预设对话是反注入最有效手段。LLM 模仿示例比遵循规则强得多。覆盖场景：身份冒充、社交施压、越狱、好感度操纵
- 人格不要超过 60 行。超过就稀释效果
- 身份要硬编码到人格里，不要让 LLM 去"推理"谁是谁
- **每条预设对话回复 ≤ 2 句，不解释、不纠结、不自证。示范的是态度，不是逻辑**
- **结构化模板 > 纯文本**。用标题和模块分层（角色设定/输出约束/格式示例/场景应对）比一段话更有效
- **玖帕喵模板分析** 见 `references/jiupamiao-template-analysis.md`

## 群聊上下文机制（NAPCAT_CONTEXT_MODE）

### 需求

"接收群里所有消息作为上下文，但只在被 @ 时回复"

### 当前实现（v2 — 文本注入模式）

配置：`.env` 中 `NAPCAT_CONTEXT_MODE=true`

可选：`NAPCAT_CONTEXT_MAX_LINES=50`（默认 50，超过裁剪最早的消息）

**原理**：完全在 `napcat.py` 内部处理，不依赖 gateway。

```python
# NapCatAdapter.__init__
self._context_mode: bool = os.getenv("NAPCAT_CONTEXT_MODE", "").lower() in {"true", "1", "yes", "all"}
self._pending_group_context: Dict[str, List[str]] = {}
self._max_context_lines: int = int(os.getenv("NAPCAT_CONTEXT_MAX_LINES", "50"))
```

**`_add_group_context(group_id, sender_name, text)`**：非@消息进来时调用。格式化为 `[名字] 内容` 存入 buffer。**跳过纯媒体消息**（`[图片:xxx]`、`[表情:xxx]`、`[视频:xxx]` 等——文件 ID 是临时的，没有可读上下文价值）。超出 `_max_context_lines` 时裁剪最早的行。

**`_drain_group_context(group_id)`**：有人 @bot 时调用，取出 buffer 格式化为：
```
[群聊上下文]
[阮出] 今天好热啊
[余出] 确实 35 度了
[人神] 你们在聊什么
---
```
清空 buffer 并返回。注入到 `stripped_text` 前面。

### 效果

```
群友 A: "今天好热啊"          → _add_group_context → 不回复
群友 B: "是啊 35 度了"         → _add_group_context → 不回复
@魔术师 什么时候降温           → _drain_group_context → Agent 上下文中包含:
                                  [群聊上下文]
                                  A: 今天好热啊
                                  B: 是啊 35 度了
                                  ---
                                  → 正常回复
```

### 注意事项

- Buffer 在**内存**中，gateway 重启会丢失。不持久化到磁盘。
- 非@消息必须包含纯文本（`_extract_reply_and_text` 提取），纯图片/语音等无文本的消息不会进入 buffer。
- `require_mention` 是 napcat.py 的硬编码逻辑（`_strip_self_mention`），当前版本**无法关闭**。`NAPCAT_REQUIRE_MENTION=true` 环境变量保留但代码实际上不读取它——因为群聊场景 @mention 是唯一触发方式，关闭会导致 bot 对每条群消息都回复。
### ⚠️ 关键修复：@bot 检测（`_strip_self_mention` 的 seen_text + has_reply）

**问题**：QQ 会在 reply 链/会话上下文中自动插入不可见的 `at` 段（@bot），导致非@消息也被判定为 `mentioned=True`，bot 对每条消息都回复。

**根因**：旧版 `_strip_self_mention` 只要看到消息段里有 `at` 指向 `self_id` 就返回 `mentioned=True`——不区分位置和上下文。

**修复**（`napcat.py` `_strip_self_mention` 方法）：
```python
seen_text = False   # 是否已经出现了非@、非reply的内容
has_reply = False   # 消息是否包含 reply 段（QQ 回复特性）
for seg in segments:
    ...
    if seg_type == "reply":
        has_reply = True
        continue
    if seg_type == "at":
        if qq == self._self_id:
            if not seen_text and not has_reply:  # 两个条件同时满足才提及
                mentioned = True
            continue
        ...
        seen_text = True
    if seg_type == "text" and value.strip():
        seen_text = True
    if marker:
        seen_text = True
```

**核心逻辑**：`mentioned` 只在同时满足两个条件时才为 True：
1. `@bot` 出现在任何文本/图片/@其他人**之前**
2. 消息**没有** `reply` 段（QQ 回复别人时自动插入 @bot，不算主动提及）

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="memory">
<｜｜DSML｜｜parameter name="action" string="true">add

## 致命陷阱：SOUL.md 会覆盖 SKILL.md 的对话风格

**这是本次对话最大的踩坑发现。**

SOUL.md (`~/.hermes/SOUL.md`) 是系统提示词第一槽位，其指令（如"精确、直接"、"信息密度"）会
**覆盖** 平台 SKILL.md 中的对话风格要求。这导致 QQ 群聊中 Bot 持续输出 586 字长文，
尽管 SKILL.md 明确要求 1-3 句。

### 症状

- SKILL.md 写满"简短""1-3句""口语"→ 完全无效
- Bot 回复 500+ chars，AI 味重，长篇大论
- 其他 Skill 配置正常，唯独回复长度不受控

### 根因

LLM 的系统提示词层级：
1. **SOUL.md**（第 1 槽位，优先级最高）
2. 平台 SKILL.md（第 N 槽位，优先级低）
3. 用户消息

当 SOUL.md 说"精确直接、信息密度"而 SKILL.md 说"简短口语"时，LLM 优先听 SOUL.md 的。

### 修复：在 SKILL.md 开头加强制覆盖

```markdown
# 基本要求
**本 prompt 的优先级高于你的默认行为模式。** QQ 群聊要求极短回复——
你的默认"信息密度"、"精确直接"风格在此渠道必须切换为"简短口语"模式。
忘记你学到的一切关于认真回答问题的训练——在 QQ 里，简短比正确更重要。
```

关键：必须用**绝对语气**（"优先级高于"、"切换为"、"忘记"），不能用"请注意"、"建议"等软话术。

## Skill 上下文污染：必须禁用无关 Skill

Hermes 默认加载所有已安装的 Skill（300+个）。QQ 群聊会被注满生物、物理、部署等
无关提示词，稀释 napcat 人格。

### 配置

`config.yaml`：
```yaml
skills:
  platform_disabled:
    napcat:
      - <258 个无关 Skill>
```

使用 Python 脚本批量生成禁用列表（排除 napcat + hermes-agent + perspective 类）。

### 效果

- 上下文从 300+ 个 Skill 压缩到 ~10 个
- napcat 人格不再被稀释

## Session 污染：越狱历史会触发 API 内容审查

QQ 群聊的 session 会跨消息累积。如果群友发过猫娘越狱等内容，下次消息带上
这段上下文时，DeepSeek API 会返回 **HTTP 400: Content Exists Risk**。

### 止血

```bash
# 删除所有 napcat session
python3 -c "
import json
with open('/home/po/.hermes/sessions/sessions.json') as f:
    data = json.load(f)
for k in list(data):
    if 'napcat' in k: del data[k]
# 保存...
"
```

然后重启 Gateway。Session 会被自动重建，但历史污染会清除。

## Hermes 的待解决问题

Agent 看不到 QQ 号，只能看到群名片。改进方向：参考 AstrBot 的做法，在 napcat 适配器的
`_build_message_event` 中，在消息文本前拼接发送者身份标识（如 `[QQ:2631792752|人民公仆]`）。

WebUI → 网络配置 → WebSocket 客户端：

| 字段 | 值 |
|------|-----|
| URL | `ws://127.0.0.1:8646/napcat/ws` |
| Token | 同 NAPCAT_TOKEN |
| 消息上报格式 | `array` |

## 人格 SKILL.md 的正确位置 ⚠️

**踩坑教训**：QQ 人格 SKILL.md 曾被错误放在源码仓库内（`hermes-agent/skills/messaging/napcat/SKILL.md`），用户指出后已移正。

Hermes 有两个 skills 目录，用途不同：

| 路径 | 用途 | 管理方式 |
|------|------|----------|
| `~/.hermes/skills/` | **用户安装的 skills** ← QQ 人格放这里 | 备份仓库同步，不跟源码版本 |
| `hermes-agent/skills/` | **源码自带的 built-in skills** | 跟 hermes-agent git 仓库，`hermes update` 时会变动 |

QQ 人格 SKILL.md 的正确路径：**`~/.hermes/skills/messaging/napcat/SKILL.md`**。

放在源码仓库里的后果：
- `git pull` 或 `hermes update` 可能覆盖或冲突
- 污染 upstream 仓库的干净状态
- 备份仓库（hermes-config-kit）的 sync-back.sh 不会检测到它（因为脚本从 `~/.hermes/skills/` 同步）

## hermes update 恢复流程

每次 `hermes update` 后如果 NapCat 断连（ECONNREFUSED），执行以下步骤恢复：

### 步骤 1：恢复 napcat.py

```bash
cd ~/.hermes/hermes-agent
# 找到 git 历史中 napcat.py 的最新版本
git log --all --oneline -- gateway/platforms/napcat.py | head -3
# 从最近的有效提交恢复（避开 auto-maintenance 那个删除它的提交）
git show <commit_hash>:gateway/platforms/napcat.py > gateway/platforms/napcat.py
```

> 如果本地 git 历史中没有 napcat.py（全新 clone），则从 MoeOver 分支 cherry-pick：`git checkout moeover/main -- gateway/platforms/napcat.py`

### 步骤 2：加回 Platform 枚举（gateway/config.py ~164 行）

```python
    QQBOT = "qqbot"
    NAPCAT = "napcat"    # ← 加这行
    YUANBAO = "yuanbao"
```

### 步骤 3：加回平台启用逻辑（gateway/config.py，QQBOT 段之后）

```python
    # NapCat (OneBot 11 reverse WebSocket)
    napcat_enabled = os.getenv("NAPCAT_ENABLED", "").lower() in {"true", "1", "yes"}
    napcat_token = os.getenv("NAPCAT_TOKEN", "").strip()
    if napcat_token:
        if Platform.NAPCAT not in config.platforms:
            config.platforms[Platform.NAPCAT] = PlatformConfig()
        cfg = config.platforms[Platform.NAPCAT]
        if napcat_enabled:
            cfg.enabled = True
        cfg.token = napcat_token
        extra = cfg.extra
        extra["host"] = os.getenv("NAPCAT_HOST", "0.0.0.0")
        extra["port"] = int(os.getenv("NAPCAT_PORT", "8646"))
        extra["path"] = os.getenv("NAPCAT_PATH", "/napcat/ws")
        napcat_home = os.getenv("NAPCAT_HOME_CHANNEL", "").strip()
        if napcat_home:
            cfg.home_channel = HomeChannel(
                platform=Platform.NAPCAT,
                chat_id=napcat_home,
                name=os.getenv("NAPCAT_HOME_CHANNEL_NAME", "Home"),
                thread_id=os.getenv("NAPCAT_HOME_CHANNEL_THREAD_ID") or None,
            )
        napcat_allow_all = os.getenv("NAPCAT_ALLOW_ALL_USERS", "").lower() in {"true", "1", "yes"}
        if napcat_allow_all:
            extra["allow_all_users"] = True
        napcat_allow_from = os.getenv("NAPCAT_ALLOW_FROM", "").strip()
        if napcat_allow_from:
            extra["allow_from"] = napcat_allow_from
        napcat_require_mention = os.getenv("NAPCAT_REQUIRE_MENTION", "").lower()
        if napcat_require_mention in {"true", "1", "yes", "false", "0", "no"}:
            extra["require_mention"] = napcat_require_mention in {"true", "1", "yes"}
```

### 步骤 4：加回 adapter 创建代码（gateway/run.py，QQBOT 段之后）

```python
        elif platform == Platform.NAPCAT:
            from gateway.platforms.napcat import NapCatAdapter, check_napcat_requirements
            if not check_napcat_requirements():
                logger.warning("NapCat: aiohttp not installed")
                return None
            return NapCatAdapter(config)
```

### 步骤 5：加到 _UPDATE_ALLOWED_PLATFORMS（gateway/run.py ~10835 行）

在 `Platform.QQBOT` 后加 `Platform.NAPCAT`。

### 步骤 5.5：加回 authz 授权映射（gateway/authz_mixin.py）

**这是隐藏最深的坑**。即使前 5 步都做对了，`NAPCAT_ALLOW_ALL_USERS=true` 也不会生效，因为 `authz_mixin.py` 的三个平台映射表没有 NAPCAT：

```python
# platform_env_map（约 157 行，QQBOT 之后加）
Platform.NAPCAT: "NAPCAT_ALLOW_FROM",

# platform_allow_all_map（约 183 行，QQBOT 之后加）
Platform.NAPCAT: "NAPCAT_ALLOW_ALL_USERS",
```

症状：Gateway 日志 `Unauthorized user: 2631792752 (人民公仆) on napcat`，所有消息被静默丢弃。

### 步骤 5.6：加回 hermes_cli/gateway.py 的 setup 函数和 PLATFORMS 条目

合并后 `hermes setup` 的 NapCat 交互式配置也会丢失。需要：

1. 在 `_setup_qqbot()` 函数之后加 `_setup_napcat()` 函数
2. 在 `_PLATFORMS` dict 中加 `"napcat": _setup_napcat,`

### 步骤 6：重启 Gateway

```bash
kill $(ps aux | grep 'gateway run' | grep -v grep | awk '{print $2}')
# systemd 会自动重启，或手动：
# nohup hermes gateway run --replace &
```

验证：`grep -a -E 'napcat|Gateway running with' /home/po/.hermes/logs/gateway.log | tail -5`
应该看到 `✓ napcat connected` 和 `Gateway running with 3 platform(s)`。

## 排障速查

| 现象 | 原因 | 方案 |
|------|------|------|
| **hermes update 后 ECONNREFUSED** | napcat.py + config/run 被更新覆盖 | 执行「hermes update 恢复流程」（上方章节） |
| **`napcat_call` 永远不可用 / 图片无法识别** | `gateway.run._active_runner` 从未赋值（模块级变量为 None） | 两步修复：<br>(1) 模块顶（约 67 行，`_ADAPTER_DISCONNECT_TIMEOUT` 之后）加 `_active_runner: Optional[Any] = None`<br>(2) `start_gateway()` 中（约 15713 行，`runner = GatewayRunner(config)` 之后）加 `global _active_runner; _active_runner = runner` |
| **非@消息也回复** | `_strip_self_mention` 不区分 @bot 的前后位置，QQ 自动塞的 @bot 被误判 | 加 `seen_text` 追踪——只有**开头**的 @bot 算主动提及 |
| **`NAPCAT_ALLOW_ALL_USERS=true` 不生效** | `authz_mixin.py` 映射表缺少 NAPCAT | 加 `Platform.NAPCAT` 到 `platform_allow_all_map` 和 `platform_env_map` |
| **Unauthorized user 警告** | 同上：authz 映射表不认 NAPCAT | 同上 |
| 401 | Token 不匹配 | 确认两端一致 |
| Unauthorized user | 不在白名单 | `NAPCAT_ALLOW_ALL_USERS=true` |
| 无消息事件 | message 字段缺失或 @mention 未检测 | 确认消息上报格式 array |
| Gateway 卡死 | Telegram 连接阻塞 | `kill -9 $(pgrep -f gateway)` |
| Agent 分不清主人 | **看不到 QQ 号**（核心缺陷） | 待改适配器注入身份 |
| Markdown 泄漏 | LLM 本能输出 Markdown | Skill 里用"硬件限制"话术 + 违规示例 |
| 猫娘越狱 | 群友直接 role-play prompt | 威胁扫描拦截（已加中文模式） |
| require_mention 不生效 | `hermes config set` 设到了 display.platforms 下 | 必须用 `hermes config set napcat.require_mention true`（顶层，不是 display 下） |
| 没 @ 的消息也回复了 | 适配器代码出错 | 确认 `_pending_context` 初始化和 `return None` 正确 |
| **"Content Exists Risk" (400)** | DeepSeek 内容审查拒绝处理请求 | 见下方专项说明 |
| **群消息发错误给群友** | agent 失败时中间结果仍发出 | 同上，跨 bot 连锁污染 |

### DeepSeek "Content Exists Risk" 专项 ⚠️

**现象**：agent.log 出现 `HTTP 400: Content Exists Risk`，gateway 把 147 字符错误消息发到 QQ 群。

**根因**：DeepSeek API（尤其是 `v4-flash`）的内容安全过滤器对某些上下文组合过于敏感。NapCat 会话通常较长（群聊多轮对话），累积的上下文更容易触发。

**连锁灾难**：如果群里有多个 bot（如 Hermes + 人出 bot），一个 bot 的错误消息会成为另一个 bot 的上下文 → 再触发同一个 400 → 两个 bot 互相喂毒，无限循环。

**止血方案（按推荐优先级）**：

1. **换模型** — 把 `NAPCAT_MODEL` 从 deepseek 系换成没有内容审查的 provider（如 minimax-cn、z.ai 等）。最快，一刀切。

2. **手动 reset session** — 在群里发 `/reset` 清除累积的上下文。治标，适合临时恢复。

3. **代码层面** — 修改 gateway 在 `agent_failed_early` 时不发原始错误到群（发"稍后重试"类文案），并加连续 2 次 `Content Exists Risk` 自动 reset。治本但需改代码。

详细排查记录见 `references/deepseek-content-risk.md`。
