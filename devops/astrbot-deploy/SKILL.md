---
name: astrbot-deploy
description: 在 WSL/Linux 上通过 uv 部署 AstrBot QQ 机器人，对接已有 NapCatQQ
version: 1.3.0
author: Hermes Agent
tags: [astrbot, qq, napcat, onebot, deploy, uv]
prerequisites:
  commands: [uv, python3]
---

# AstrBot 部署（uv 方式）

在 WSL/Linux 上用 uv 一键部署 AstrBot，对接 Windows 上已运行的 NapCatQQ。

## 架构

```
QQ 群聊 ←→ NapCatQQ (Windows, 寄生 NTQQ)
                │
    WebSocket Client → ws://127.0.0.1:6199/ws
                │
                ↓
         AstrBot (WSL, uv 安装)
         WebUI: :7833（旧版 :6185）, WS: :6199
```

NapCat 是 WS 客户端，AstrBot 是 WS 服务端。

## 1. 安装

```bash
# Python 3.12+ 必需
uv tool install astrbot --python 3.12

# 初始化（在目标目录）
mkdir -p ~/astrbot && cd ~/astrbot
yes Y | astrbot init
```

## 2. 启动

```bash
cd ~/astrbot
astrbot run
```

首次启动会自动下载 WebUI（~10MB）。成功时显示：
```
AstrBot vX.XX WebUI is ready
➜  Local: http://localhost:6185
➜  Initial username: astrbot
➜  Initial password: xxxxxxxxxx
```

## 3. 后台持久化

WSL 无 systemd user bus 时用 Python subprocess。

### 方法 A：execute_code 启动（推荐，Hermes 内最稳定）

Hermes 的 `terminal(background=true)` 在 WSL 下存在 bash 终端组问题（`无法设定终端进程组`），输出会丢失且进程可能快速退出。最可靠的方式是从 `execute_code` 中用 `subprocess.Popen` 启动：

```python
import subprocess, os

os.chdir("/home/po/astrbot")
log = open("data/astrbot.log", "w")

proc = subprocess.Popen(
    ["/home/po/.local/bin/astrbot", "run"],
    stdout=log, stderr=subprocess.STDOUT,
    start_new_session=True,
    env={**os.environ, "PYTHONUNBUFFERED": "1"},
)
print(f"AstrBot PID: {proc.pid}")
```

验证：`ss -tlnp | grep -E "6185|6199"` 应看到两个端口监听，`ps aux | grep astrbot` 确认进程存活。

### 方法 B：systemd 服务（已在使用）

实际部署使用系统级 systemd 服务 `/etc/systemd/system/astrbot.service`：

```bash
sudo systemctl start astrbot    # 启动
sudo systemctl status astrbot   # 查看状态
sudo systemctl restart astrbot  # 重启（配置修改后需要）
sudo systemctl stop astrbot     # 停止
```

⚠️ 启动需要 sudo。Hermes 不应自动执行 systemctl 命令（用户已明确禁止自动 sudo）。

## 4. 密码管理

### CLI 方式（推荐）

```bash
cd ~/astrbot
printf 'NewPass123!\nNewPass123!\n' | /home/po/.local/bin/astrbot password
```

⚠️ **密码修改后必须重启 AstrBot**（杀进程 → 重新启动）。密码要求至少一个大写字母。

### 直接写入配置（绕过 CLI 限制）

当 `astrbot password` CLI 因密码策略拒绝时（如缺少大写字母），可直接写入 MD5 + 标记升级：

```python
import hashlib, json

password = "your_password"
md5_hash = hashlib.md5(password.encode()).hexdigest()

with open("data/cmd_config.json", "r", encoding="utf-8-sig") as f:
    config = json.load(f)

config["dashboard"]["password"] = md5_hash
config["dashboard"]["password_storage_upgraded"] = False  # 触发下次登录时升级到 PBKDF2
config["dashboard"]["password_change_required"] = False

with open("data/cmd_config.json", "w", encoding="utf-8-sig") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
```

改完后重启 AstrBot 生效。

## 5. 对接 NapCatQQ

### AstrBot 端（WebUI: :7833 或 :6185）
左边栏 → **机器人** → **+ 创建机器人** → **OneBot v11**：
- ID: 随意（如 `QQ`）
- 启用 ✅
- 反向 WS 主机地址: `0.0.0.0`
- 反向 WS 端口: `6199`
- Token: 留空

### NapCat 端（WebUI: :6099）
「网络配置」→ 修改/新建 WebSocket 客户端：
```
ws://127.0.0.1:6199/ws
```
⚠️ **必须带 `/ws` 后缀**。消息格式 Array，不需要 token。

验证：AstrBot WebUI → 控制台，看到蓝色 `aiocqhttp(OneBot v11) 适配器已连接` 即成功。

## 6. 配置 LLM

左边栏 → 配置 → 服务提供商 → 添加 → **OpenAI 兼容接口**：
- Base URL: `https://api.deepseek.com/v1`
- API Key: DeepSeek key
- 默认模型: `deepseek-chat`

## 7. 人格配置（Persona）

WebUI：左边栏 → 配置 → **人格情境** → 新建/切换。社区最佳实践见 `references/persona-magician.md`。

### QQ 内切换人格（最快）

在群聊/私聊发指令即可切换，无需开 WebUI：

```
/persona list              → 列出所有可用人格
/persona <人格名>          → 切换到指定人格
/persona unset             → 取消人格（恢复默认）
/persona view <人格名>     → 查看某个人格的详细信息
/reset                     → 切人格后清空上下文（建议切完就发）
```

### 人格模板来源

- **jiupamiao.asia**（玖帕喵）：提示词模板市场，有成熟的"拟人模板"（如第二版拟人模板 `market?id=509`），可直接参考结构（社会关系、社交距离、对话安全等模块）
- AstrBot 插件市场搜 `portrayal`、`Private Companion` 等辅助人格连续性

### 核心要点

- **身份用"你"**："你是损友"比"角色是损友"有效
- **预设对话是关键**：给出 5-8 组"用户说→你回"的理想示例，比长篇描述更有效
- **开启识别群员**：配置 → 大语言模型 → 勾选「识别群员」
- **开启日期时间提示**：让 bot 有时间感

## 与 Hermes NapCat 的对比

WebUI → 插件市场，搜以下关键字安装：

| 插件 | 作用 |
|------|------|
| `Self-Learning` | 自动学习群聊风格、黑话、社交关系（越聊越像人） |
| `Private Companion` | 人格连续性、关系识别、长期记忆 |
| `Multimodal Router` | 图片自动路由到有视觉能力的模型（DeepSeek 不支持图片） |
| `Meme Manager` | 表情包管理 |

## 与 Hermes NapCat 的对比

| | Hermes NapCat | AstrBot |

## 8. 知识库管理

AstrBot v4.5.0+ 原生支持 RAG 知识库。完整 API 工作流（创建、上传、检索、更新）见 `astrbot-knowledge-base` skill。

关键配置：服务提供商 → Embedding → SiliconFlow `BAAI/bge-m3`（免费），`embedding_dimensions` 必须设为 `0`（`bge-m3` 不支持此参数）。
|---|---|---|
| WS 方向 | Hermes 是服务端 | AstrBot 是服务端 |
| 端口 | 8646 | 6185(UI) + 6199(WS) |
| 部署方式 | 代码级 hack | `uv tool install` |
| 更新风险 | 每次 update 需修复 | 无 |
| Web 面板 | 无 | ✅ |

## 踩坑

- **Hermes `terminal(background=true)` 在 WSL 下有终端组问题**：输出仅显示 `bash: 无法设定终端进程组`，AstrBot 的输出完全丢失，进程可能在数秒内退出（exit_code 0 但无输出）。**不要**用后台模式启动 AstrBot。替代方案：(1) `execute_code` + `subprocess.Popen(start_new_session=True)` — 最可靠；(2) `terminal(pty=true)` 前台运行 — 可行但 fish shell 配置可能干扰。
- **`uv tool install` 输出被抑制**：Hermes 后台 bash 不显示 uv 进度条。用 `HOME=/home/po /home/po/.local/bin/uv ...` 绝对路径 + 前台运行。
- **Docker 国内拉镜像超时**：直接用 uv，不走 Docker。DaoCloud 等镜像代理也可能超时。
- **Docker 国内拉镜像超时**：直接用 uv，不走 Docker。
- **密码修改后不生效**：必须重启 AstrBot 进程才能加载新密码。密码要求至少一个大写字母。
- **NapCat WS URL 必须带 `/ws`**：`ws://127.0.0.1:6199/ws`，少写后缀就 400。
- **端口默认 6199 不是 6186**：AstrBot 官方文档默认的 aiocqhttp 端口是 6199。
- **embedding_dimensions 非零致 bge-m3 警告泛滥**：硅基流动不接受 `dimensions` 参数（仅 Qwen 系列支持），设为 1024 导致日志被 WARN 刷屏。改 `cmd_config.json` 中对应 provider 的 `embedding_dimensions` 为 `0`。
- **UI 路径变更**：新版本中「消息平台」在「机器人」菜单下，选「OneBot v11」而非单独 aiocqhttp。

### 配置文件相关（高频陷阱）
- **Hermes `read_file`+`write_file` 会破坏 JSON**：`read_file` 返回带行号前缀（`123|content`）的文本，`write_file` 会原样写入。**绝对不要**用于编辑 JSON 配置文件——读用 `execute_code` 中的 `open`，写用 `execute_code` 中的 `json.dump`。此链导致 `cmd_config.json` 被写入行号前缀，AstrBot 启动崩溃。详见 `hermes-file-pitfalls` skill。
- **AstrBot 会静默重建损坏的 config**：如果 `cmd_config.json` 无法解析，AstrBot 启动时**不会报错而是直接生成默认配置**，导致你手动写的所有设置丢失。写完配置后务必用 `python3 -c "import json; json.load(open('data/cmd_config.json','rb'))"` 验证合法性。
- **JSON 文件的 BOM 头**：AstrBot 的 `cmd_config.json` 自带 UTF-8 BOM。`execute_code` 沙箱可能因 Python 版本差异报 BOM 错误——这不代表文件损坏，AstrBot 自己能正常读取。

### Self-Learning 插件：DB 启动警告（"数据库尚未启动"）

**症状**：AstrBot 控制台看到三条 WARN 在同一毫秒：

```
[DomainRouter] 数据库尚未启动，暂跳过数据库操作 (get_pending_style_reviews)
[DomainRouter] 数据库尚未启动，暂跳过数据库操作 (get_reviewed_persona_update_records)
[DomainRouter] 数据库尚未启动，暂跳过数据库操作 (get_reviewed_persona_learning_updates)
```

**根因**：`astrbot_plugin_self_learning/config.py` 中 `DEFAULT_DB_TYPE = "postgresql"`（默认 PostgreSQL），而 WSL 环境无 `asyncpg` 驱动。每次启动先尝试 PostgreSQL（15s 超时）→ 失败 → 回退 SQLite，此窗口内 `_started=False`，WebUI dashboard 自动加载触发的 DB 查询全部被跳过。

**修复**（一行改）：

```python
# astrbot_plugin_self_learning/config.py 第19行
DEFAULT_DB_TYPE = "sqlite"  # 原来是 "postgresql"
```

改后重启 AstrBot 生效。警告无害（DB 最终会回退到 SQLite 成功），但去掉 PostgreSQL 重试可消除时序窗口。

### 插件渲染相关

- **Pillow 渲染插件需要 CJK 字体**：如 `astrbot_plugin_bangumi_enhance` 等生成图片的插件，依赖 NotoSansCJK 字体。插件初始化时会后台下载，但国内网络直连 GitHub 必失败 → 字体目录为空 → Pillow 降级到 `load_default()` → 渲染白板。解决：手动装字体或软链系统已有中文字体到插件 fonts 目录。详见 `references/bangumi-plugin-rendering.md`。

### 数据库相关

#### personas 表列类型速查

SQLAlchemy ORM 对 `personas` 表的列类型定义与实际 SQLite schema 不完全一致。以下列被 ORM 定义为 **JSON 类型**（必须存储合法 JSON 字符串）：

| 列名 | 正确格式 | 错误示例 |
|------|---------|---------|
| `system_prompt` | `"系统提示词文本..."` (JSON 包裹的字符串) | `系统提示词文本...` (纯文本,无引号) |
| `begin_dialogs` | `"[{\"role\":\"user\",...}]"` 或 `"[]"` | `""` (空字符串) |
| `tools` | `"null"` 或 `"[]"` 或 `"{}"` | `""` (空字符串) |
| `skills` | `"null"` 或 `"[]"` 或 `"{}"` | `""` (空字符串) |
| `custom_error_message` | `"报错信息..."` (JSON 包裹的字符串) 或 `null` | `报错信息...` (纯文本,无引号) |

以下列是**非 JSON 类型**（datetime/string/integer），不应被 JSON 引号包裹：

| 列名 | 正确格式 | 错误示例 |
|------|---------|---------|
| `created_at` | `2026-06-10 17:25:13.380503` | `"2026-06-10..."` (被 JSON 引号包裹) |
| `updated_at` | `2026-06-10 17:25:13.380503` | `"2026-06-10..."` |
| `persona_id` | `魔术师` | `"魔术师"` (被 JSON 引号包裹) |
| `folder_id` | `null` 或整数 | — |
| `sort_order` | `0` 或整数 | — |

⚠️ **最常见崩溃原因**：从 WebUI 创建 persona 后再拿到别处数据库操作时，`custom_error_message` 填了纯中文字符串（如 `报错了, 呼叫人神📢`），但 ORM 期望它是 `"报错了, 呼叫人神📢"`（JSON 字符串）。同理 `system_prompt` 填裸文本也会触发 JSON 解析崩溃。崩溃堆栈：`get_personas() → json.loads("")` → `JSONDecodeError: Expecting value`。

- **INSERT 时必须对所有 JSON 列用 `json.dumps()`**：`system_prompt`、`begin_dialogs`、`custom_error_message` 全部要 `json.dumps(val, ensure_ascii=False)`。`tools` 和 `skills` 用 `json.dumps({})` 或 `"null"`。
- **崩溃诊断**：AstrBot 启动崩溃且堆栈指向 `get_personas()` → `json.loads` 时，逐列检查所有 persona 记录的 JSON 合法性。详见 `references/personas-json-columns.md`。
- **`begin_dialogs` 格式兼容问题**：某些 AstrBot 版本对预设对话格式敏感——存入 `[{role, content}]` JSON 后 LLM 调用时可能报 `validation error for Message`。报此错时**直接清空字段**（`UPDATE personas SET begin_dialogs='[]'`），让用户通过 WebUI 手动填预设对话。不要再反复尝试不同格式。
- **MiniMax M3**（2026-06-01 发布）是原生多模态模型，可作为 AstrBot 的聊天+看图统一方案，避免多模态路由插件。详见 `references/minimax-multimodal.md`。
- **写数据库后必须重启**：直接 SQLite 写入不会热加载，需要重启 AstrBot。
- **插件支持热重载**：新插件放到 `data/plugins/` 后 AstrBot 启动时会自动检测加载，**不要 kill 进程**。如果插件加载失败（如 import 错误），修复文件后调用 API 重试：`POST /api/plugin/reload-failed` body `{"dir_name":"<plugin_dir>"}`。**注意**：这是首次加载场景，不是改代码后自动热重载——运行时改源码默认不加载，需重启或开 watcher（见下一条）。
- **插件 import 错误常见模式**：类名/函数名不匹配（如 `VideoCardRenderer` → `CardRenderer`），保留原名做 alias：`from .module import CardRenderer as VideoCardRenderer`。
- **ASTRBOT_RELOAD=1` 才能热重载插件**：仅把改过的文件放到 `data/plugins/<plugin>/` **不会**自动加载到运行中的进程。`star_manager._watch_plugins_changes` 由 `os.getenv("ASTRBOT_RELOAD", "0") == "1"` 控制（CLI `astrbot run --reload` / systemd 单元 `Environment="ASTRBOT_RELOAD=1"`）。**默认不监听文件**，改了代码必须 `sudo systemctl restart astrbot`（或 `pkill -f 'astrbot run'` + 重启）。官方文档也不推荐热重载，dev workflow 是 WebUI 点 `...` → 重载插件。验证：修改文件后 `journalctl -u astrbot --since '30s' | grep '文件变化'`——没出现就是没开 watcher。

### 调试排查（运行时异常）

- **查 AstrBot 日志优先用 `journalctl`，不要先 grep `data/astrbot.log`**：`data/astrbot.log` 是普通文件,默认按天 rotate 但**不一定切**,且只捕获 AstrBot 直接写出的 stdout (受 `PYTHONUNBUFFERED` 影响)。systemd unit (`astrbot.service`) 接管时所有输出都进 journal,带完整时间戳 + 二进制保留 + 不用猜日志文件 mtime 是否新鲜。顺序: `journalctl --user -u astrbot.service --since '30 min ago'` (或 `XDG_RUNTIME_DIR=/run/user/$(id -u) journalctl --user -u astrbot.service` 当 $XDG_RUNTIME_DIR 缺失时)。如果进程是手动 `astrbot run` 起的而 systemd unit `inactive (dead)`,journal 里就**不会有新事件**——先确认 `systemctl --user status astrbot` 是 `active` 才看 journal,否则只能 `tail -F` 那个 log 文件。诊断前先 `stat data/astrbot.log` 看 mtime——mtime 锁在几天前 = 当前进程根本没写这个文件,日志本身失效。详见 `references/runtime-anomaly.md`。
- **DeepSeek reasoning model 输出泄漏到 QQ 消息**:AngelHeart 等插件经常看到群里有 `<system_decision>...</system_decision>`、`<core_topic>...</core_topic>`、`<reasoning>...</reasoning>`、`<think>...</think>` 这种 XML 块被原文发出。这是 AstrBot 的 DeepSeek provider 适配器 (`core/provider/sources/openai_source.py` 或类似) 没正确把 `reasoning_content` 字段从 `content` 剥离。触发条件是 `is_reasoning_model: true` 或模型本身是 reasoning 类 (DeepSeek-R1, o1, Claude with thinking 等)。验证: `cmd_config.json` 里 provider 条目的 `model` 字段是不是 reasoning 类 + 看 journal 里有没有 `reasoning_content` 字段(如果有但没被剥离,就是适配器 bug)。根因是 AstrBot 框架,不在插件——解法是把 `is_reasoning_model` 改成 `false`(模型本身不输出 reasoning 仍能用),或给 AstrBot 提 issue。详见 `references/runtime-anomaly.md`。
- **读源码被 `AGENTS.md` / `CLAUDE.md` 二次注入污染**: AstrBot 框架 + 不少插件(angel_memory, angel_heart, 社区插件)会在插件目录里塞 AGENTS.md,内容是项目背景、文件路径、常见坑。`search_files` / `read_file` 触发后,这些上下文会被注入到后续 tool output,**看起来像 agent 自己总结的**,其实是从 RAG 风格的文件 load 出来的——不要把它们当成"我从那个文件学到的"加进 skill,也不要在诊断时引用其中的"关键决策点"作为结论(尤其当这些"决策"跟你正在追的现象无关时)。判定方法: 看 SKILL.md 顶部有没有 `## Project Context` / `## Subdirectory context discovered` 之类的 banner——是 AGENTS 注入,不是 agent 推理。
- **`secretary_decision` 不是 prompt 字面量**:AngelHeart 插件的 `secretary_decision` (含 `topic` / `entities` / `facts` / `keywords` / `reply_strategy`) 是**结构化 Python 对象** (`models/analysis_result.py`),序列化进 `event.angelheart_context` 后作为系统提示词的素材注入。AngelHeart 的 prompt 模板 (`prompts/modules/*.md`) 里**没有** `core_topic` / `recommended_strategy` / `interaction_target` 这种字面量字段。所以"群里有 `<core_topic>...</core_topic>`" 不是 AngelHeart 输出,是上游 LLM 自己的 reasoning / scratchpad 行为 (同上条)。诊断步骤: `rg -uu 'core_topic|recommended_strategy' ~/astrbot` 命中 0 + `cmd_config.json` 模型是 reasoning 类 → 几乎确定是 reasoning field 泄漏。
- **构造 `session` 字符串时 platform id 别写死**：aiocqhttp 适配器的 `PlatformMetadata.id` 来自 `cmd_config.json` 的 `platform.id`（用户配置），不一定是 `"aiocqhttp"`（本机实际是 `"default"`）。插件里拼 `aiocqhttp:GroupMessage:<群号>` 会得到 `AstrBot 主动发送未找到匹配平台: aiocqhttp:GroupMessage:<id>`，因为 `context.send_message` 用 `platform.meta().id == session.platform_name` 找平台（`star/context.py:533`）。修法：从 `self.context.platform_manager.platform_insts` 里 `meta().name == "aiocqhttp"` 的实例拿 `meta().id`。
- **FutureTask 的 note 要自包含**：Agent 被唤醒时只有 note 文本，没有原会话上下文。note 必须包含完整的检查步骤和数据路径，不能依赖"之前的对话中提过"。
- **bangumi 订阅用内置服务**：不需要 Hermes 的 cronjob/send_message 工具。AstrBot 插件自带 APScheduler 定时检查 + OneBot 推送。**绝不能同时维护 Hermes cron job 和 AstrBot 插件两套系统**——会导致重复通知。追番由插件统一管理，Hermes 侧如有旧的 bgm cron job/skill 立即清理。推送链路（`session` 字符串拼接、平台 id 查找、调试命令、fork 同步）详见 `references/bangumi-plugin-database.md` 和 `references/bangumi-push-notification.md`。

### 用户偏好
- **用户说"我来手动配置"时立即停手**：当用户明确表示要自己通过 WebUI 操作时，不要再碰数据库/配置文件。只确保服务在运行就行。
- **`begin_dialogs` 的预设对话格式报错时停止深入**：AstrBot 对不同版本对 `begin_dialogs` 格式要求不一致（某些版本期望纯文本而非 JSON），一旦报 `validation error` 直接清空该字段让用户手动配，不要反复尝试修复。

## 直接配置人格（写数据库，绕过 WebUI）

WebUI 的「人格情境」最终存储在 SQLite 数据库 `/home/po/astrbot/data/data_v4.db` 的 `personas` 表中。可直接写入：

```python
import sqlite3, json, datetime

conn = sqlite3.connect("/home/po/astrbot/data/data_v4.db")
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

system_prompt = "完整的系统提示词..."
begin_dialogs = [
    {"role": "user", "content": "用户说的示例"},
    {"role": "assistant", "content": "bot 应该回的示例"},
]
custom_error = "报错了, 呼叫人神📢"

conn.execute("""
    INSERT INTO personas (created_at, updated_at, persona_id, system_prompt,
                          begin_dialogs, tools, skills, custom_error_message,
                          folder_id, sort_order)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    now,  # created_at: 纯文本 datetime，不要 JSON 包裹
    now,  # updated_at: 同上
    "persona-id",  # persona_id: 纯文本，不要 JSON 包裹
    json.dumps(system_prompt, ensure_ascii=False),  # ⚠️ 必须 JSON 包裹
    json.dumps(begin_dialogs, ensure_ascii=False),  # ⚠️ 必须 JSON 包裹
    json.dumps({}),  # tools: JSON，空对象用 {}
    json.dumps({}),  # skills: 同上
    json.dumps(custom_error, ensure_ascii=False),  # ⚠️ 必须 JSON 包裹（或 null）
    None,  # folder_id
    0,     # sort_order
))
conn.commit()
conn.close()
```

⚠️ **关键**：`system_prompt`、`begin_dialogs`、`custom_error_message` 三个字段在 ORM 中被定义为 JSON 类型，**必须用 `json.dumps()` 包裹**。`created_at`、`updated_at`、`persona_id` 是纯文本/日期类型，**不应 JSON 包裹**。错误地 JSON 包裹日期会导致 `ValueError: Invalid isoformat string`。

然后修改 `cmd_config.json` 中的 `provider_settings.default_personality` 为对应的 `persona_id`，重启 AstrBot。

## AstrBot Skills 管理

AstrBot v4.13+ 支持 Anthropic Skills 格式。Skills 存放在 `~/astrbot/data/skills/`，两种路径格式均支持：

```
~/astrbot/data/skills/
├── <skill名>-<version>/        ← 市场安装（带版本号 + _meta.json）
│   ├── SKILL.md
│   ├── _meta.json
│   └── skill-card.md
├── <skill名>/                   ← 本地手动安装（不带版本号）
│   ├── SKILL.md
│   ├── scripts/                 ← 可选：可执行脚本
│   ├── .venv/                   ← 可选：Python 虚拟环境
│   └── references/              ← 可选
└── skills.json                  ← 注册表：{"skills":{"<name>":{"active":bool}}}
```

### ⚠️ `npx skills add` 不适用于 AstrBot

`npx skills add <repo>` 命令输出会宣称 "symlinked: AstrBot"，但**实际上不会更新 `skills.json`**，skill 在 AstrBot 中不可用。该 CLI 主要面向 OpenClaw、Claude Code 等 agent。

**正确做法**：手动复制 SKILL.md + 更新 skills.json，见下方"直接安装"。

### Python 依赖：始终用 venv

PEP 668 阻止系统级 pip install。AstrBot skill 需要 Python 库时，在 skill 目录下创建 venv：

```bash
SKILL_DIR="$HOME/astrbot/data/skills/<skill名>"
python3 -m venv "$SKILL_DIR/.venv"
"$SKILL_DIR/.venv/bin/pip" install <包名>
```

脚本中通过 `SKILL_DIR/../.venv/bin/<command>` 引用 venv 内的工具。**不要尝试 `uv pip install --system` 或 `pip install` 到全局**，都会失败。

### 直接安装 Skill（无需 WebUI）

```bash
VERSION="1.0.0"
SKILL_NAME="<skill名>"
SKILL_DIR="$HOME/astrbot/data/skills/${SKILL_NAME}-${VERSION}"

mkdir -p "$SKILL_DIR"

# 下载 SKILL.md（从 GitHub raw、skills.sh、SkillHub 等市场）
curl -sL "https://raw.githubusercontent.com/<作者>/<仓库>/main/SKILL.md" \
  -o "$SKILL_DIR/SKILL.md"

# 写 _meta.json
cat > "$SKILL_DIR/_meta.json" << EOF
{"ownerId":"local","slug":"${SKILL_NAME}","version":"${VERSION}","publishedAt":$(date +%s)000}
EOF

# 注册
python3 -c "
import json
with open('$HOME/astrbot/data/skills.json') as f:
    c = json.load(f)
c['skills']['${SKILL_NAME}-${VERSION}'] = {'active': True}
with open('$HOME/astrbot/data/skills.json', 'w') as f:
    json.dump(c, f, indent=4, ensure_ascii=False)
"
```

### 重启 AstrBot（安全方法）

⚠️ **AstrBot 不能直接 `pkill astrbot` 重启自己**——agent 进程跑在 AstrBot 内部，直接 kill 会把自己也杀了。用延时脚本分离进程：

```bash
cat > /tmp/astrbot_restart.sh << 'SCRIPT'
#!/bin/bash
sleep 2
pkill -f 'astrbot run' 2>/dev/null
sleep 3
cd ~/astrbot && nohup astrbot run > data/astrbot.log 2>&1 &
SCRIPT
chmod +x /tmp/astrbot_restart.sh
nohup /tmp/astrbot_restart.sh > /dev/null 2>&1 &
```

### 从 OpenClaw/Claude Code 适配 Skill 到 AstrBot

外部 skill（来自 ClawHub、skills.sh、GitHub 等）通常面向 OpenClaw 或 Claude Code 环境，需要以下适配：

**路径映射：**

| 原始路径 | AstrBot 路径 |
|----------|-------------|
| `~/workspace/` | `~/astrbot/data/` |
| `~/.openclaw/workspace/` | `~/astrbot/data/` |
| `$HOME/workspace/knowledge/` | `~/astrbot/data/transcripts/` 或自定义 |
| `scripts/`（skill 内） | `$(dirname "$0")/..` 推导 SKILL_DIR |

**功能替换：**

| OpenClaw 功能 | AstrBot 替代 |
|---------------|-------------|
| `openclaw cron add` | AstrBot FutureTask（自然语言创建） |
| Discord 发文件 | QQ 群发消息（无文件附件时发摘要） |
| `knowledge-rag` 索引 | 手动 `cat` 读取 + Agent 总结 |
| `clawhub install` | 手动复制 + skills.json 注册 |

**SKILL.md 重写要点：**
- 触发条件改为 QQ 群场景（"发送 B站链接"而非 Discord 命令）
- 输出格式适配 QQ（纯文本，避免复杂表格和超长内容）
- 去掉对 OpenClaw 专用工具（`openclaw cron`、Discord webhook、`knowledge-rag`）的引用
- 脚本中的输出目录改为 `~/astrbot/data/` 子目录

**示例：** 从 ClawHub 获取 `bilibili-auto-transcript`，适配为 AstrBot skill：
```bash
# 1. 获取源 skill
clawhub install bilibili-auto-transcript  # → ~/.openclaw/workspace/skills/...

# 2. 复制核心脚本
cp -r scripts/ ~/astrbot/data/skills/bilibili-transcript/scripts/

# 3. 修改脚本中的路径 (OUTPUT_DIR, SKILL_DIR)
# 4. 写 AstrBot 版 SKILL.md（QQ 群触发 + 简洁回复格式）
# 5. 创建 venv 装依赖
python3 -m venv ~/astrbot/data/skills/bilibili-transcript/.venv
# 6. 注册并重启
```

### Skill 市场来源

`find-skills` skill 内置了 6 个搜索来源，按速度和质量排序：

| 来源 | 规模 | 特点 |
|------|------|------|
| skills.sh | 350K+ | 全球最大，`npx skills` CLI，Vercel 背书 |
| ClaudeSkills.info | 658+ | 人工精选，质量高 |
| SkillHub (`skillhub.cn`) | — | 国内加速（腾讯云广州 COS），`skillhub search/install` CLI |
| vercel-labs/anthropics/obra | — | 官方 Awesome 合集，免搜索直接翻目录 |
| ClawHub | 13.7K+ | VirusTotal + Socket 安全审计 |
| GitHub 代码搜索 | 全网 | 兜底方案 |

### 现有参考 Skill

| Skill | 用途 |
|-------|------|
| `find-skills` | 自动搜索 6 个 skill 市场并安装到 AstrBot |
| `skill-vetter` | 安装前安全检查 |
| `writing-skills` | 怎么写好 Skill（TDD 方法论） |
| `clash-proxy` | Clash 代理管理（`http://127.0.0.1:7890`） |
| `hermes-file-pitfalls` | Hermes 文件操作避坑（read_file 行号污染等） |
| `markdown-to-image-plugin` | Markdown 转图片插件（正则问题 + 自定义样式） |
| `astrbot_plugin_bangumi_enhance` | 番剧查询+追番插件（united-pooh）。Pillow 渲染需 CJK 字体（`references/bangumi-plugin-rendering.md`），数据库诊断（`references/bangumi-plugin-database.md`），推送链路诊断（`references/bangumi-push-notification.md`） |
| `bgmlist` API | `https://bgmlist.com/api/v1/bangumi/onair` — 获取所有在播番剧的放送时间（CST），用于填充 `broadcast_time` 字段 |
| 运行时异常诊断 | LLM 输出泄漏 / reasoning 字段 / 日志入口选择 / AGENTS.md 注入污染 → `references/runtime-anomaly.md` |

---

## AstrBot 插件开发工作流（fork → 改 → ship → 部署）

> **铁律**：动手写 `main.py` 之前**必须先读完官方文档**：
> - https://docs.astrbot.app/dev/star/plugin-new.html（骨架/装饰器/注册）
> - https://docs.astrbot.app/dev/star/guides/plugin-config.html（`_conf_schema.json` 字段）
> - https://docs.astrbot.app/dev/star/guides/llm-tool.html（LLM 工具注册；如路径 404 试 `/dev/star/guides/llm-tool.html`）
>
> 官方框架源码在 `/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/astrbot/`（**唯一可靠事实源**）。装饰器、API、参数都不要凭印象写，从源码 `grep` 出来。
>
> **不要 grep `astrbot/dashboard/dist/`** 找渲染逻辑 — 那是 webpack 打包后的巨型 JS（单文件 50KB+），找不到任何可读代码，反而烧 tool call 预算。

当要改进一个已安装的 AstrBot 插件、或从零开发新插件时：

### 0. 选型：先搜现成再决定

AstrBot 官方收录的插件在 https://github.com/AstrBotDevs/AstrBot_Plugins_Collection。`web_search "astrbot 插件 <关键词>"` / GitHub code search 都行。
- 有现成且功能覆盖 → **直接 fork + 改**（比从零写省 80% 工作量）
- 有现成但缺小功能 → fork 后加 1-2 个 commit
- 没有 → 走下面 1-5 步从零写

**装饰器 / schema 实测 cheat sheet**（v4.x，单文件即可的最小插件）：

| 用途 | 装饰器 | import | 关键点 |
|------|--------|--------|--------|
| 插件注册 | `@register("name", "author", "desc", "v1.0.0", "repo_url")` | `from astrbot.api.star import register, Context, Star` | 第一个 arg 是**插件 id**（不是目录名） |
| 命令 | `@filter.command("看图")` | `from astrbot.api.event.filter import command` | 函数签名 `async def f(self, event: AstrMessageEvent, arg1: str = "")` — **空格分隔参数**自动绑定（**注意：第 3 个 token 起会被丢弃**，见下方 pitfall） |
| LLM 工具 | `@filter.llm_tool(name="my_tool")` | `from astrbot.api.event.filter import llm_tool` | 函数 docstring 写 `Args: xxx(type): desc`，参数自动解析为 JSON Schema |
| 消息事件 | `@filter.event_message_type(EventMessageType.ALL)` | `from astrbot.api.event.filter import event_message_type, EventMessageType` | 拦截所有消息 |
| 工具调用响应 | `@filter.on_llm_tool_respond()` | `from astrbot.api.event.filter import on_llm_tool_respond` | 监听 LLM 工具结果 |

**`_conf_schema.json` 字段类型**（v4.x 实测可用）：

```json
{
  "my_string":   {"type": "string", "default": ""},
  "my_text":     {"type": "text",   "default": ""},   // 大文本框
  "my_int":      {"type": "int",    "default": 0, "slider": {"min": 0, "max": 10}},
  "my_bool":     {"type": "bool",   "default": false},
  "my_select":   {"type": "string", "options": ["a","b"], "labels": ["A","B"]},  // 单选
  "my_list":     {"type": "list", "items": {"type": "string"}, "default": []},  // 字符串列表
  "my_multichoice": {                                                  // 多选（实测可用）
    "type": "list",
    "items": {"type": "string", "options": ["k1","k2"], "labels": ["L1","L2"]},
    "default": []
  },
  "select_provider": {"type": "string", "_special": "select_provider", "default": ""}
}
```

**`event` 助手**（`AstrMessageEvent` 的方法）：

| 方法 | 用途 | 返回 |
|------|------|------|
| `event.plain_result("text")` | 纯文本回复 | `MessageEventResult` |
| `event.image_result(url_or_path)` | 单图 | `MessageEventResult` |
| `event.chain_result([components])` | 多 component | `MessageEventResult` |
| `event.send(result)` | 主动发送（不等生成器） | awaitable |
| `event.make_result().file_image(path)` | 构造本地图消息 | `MessageChain` |
| `event.message_str` | 纯文本消息字符串 | str |
| `event.get_sender_name()` | 发送者昵称 | str |

**装饰器快速验证法**（写完 main.py 不用启动 AstrBot 就能检查）：

```python
import ast
tree = ast.parse(open("main.py").read())
# 找 @llm_tool / @command 的方法名
for n in tree.body:
    if isinstance(n, ast.ClassDef):
        for stmt in n.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for d in stmt.decorator_list:
                    if isinstance(d, ast.Call) and isinstance(d.func, ast.Name):
                        if d.func.id in ("command", "llm_tool", "register"):
                            # d.args[0] 是 name, d.keywords 里也可能用 name=...
                            name = d.args[0].value if d.args and isinstance(d.args[0], ast.Constant) else None
                            for kw in d.keywords:
                                if kw.arg == "name" and isinstance(kw.value, ast.Constant):
                                    name = kw.value.value
                            print(f"  {d.func.id}: {stmt.name} (name={name})")
```

**插件加载成功的日志标志**（`sudo journalctl -u astrbot --since '30 seconds ago'`）：

```
[Core] [INFO] [star.star_manager:1078]: Loading plugin astrbot_plugin_xxx ...
[Core] [INFO] [provider.func_tool_manager:388]: Added llm tool: <tool_name>
[Core] [INFO] [star.star_manager:1162]: Plugin astrbot_plugin_xxx (vX.Y.Z) by <author>: <desc>
```

**无 `Added llm tool:` 行 = LLM 工具没注册成功**（装饰器名字写错 / import 路径错 / 函数 docstring 缺 `Args:` 段）。

**fork 上游后注册 upstream 同步**（`gh repo fork` 自动加）：

```bash
gh repo fork <upstream-owner>/<repo-name> --clone=false  # 在 GitHub 端 fork
cd ~/astrbot/data/plugins/<repo-name>
gh repo clone <your-username>/<repo-name> .  # 拉 fork 到本地
git remote add upstream https://github.com/<upstream-owner>/<repo-name>.git  # gh fork 不一定自动加
git fetch upstream
```

**ad-hoc 验证脚本模式**（不是单元测试，但能 30 秒内覆盖 80% 错误）：

写 `/tmp/hermes-verify-<plugin>-v<X>.py`，里面用 AST walk 检查：
- 装饰器存在 + 参数（name kwarg 还是 positional）
- `_conf_schema.json` 合法 JSON + 字段形状（type、items、options 长度匹配 labels 长度）
- 类内部常量字典（如 `CATEGORIES`）的 keys ⊂ 业务边界
- 别名映射、fallback 行为用 plain Python 模拟函数执行

跑一次，删脚本。这是 spec-first 实践的延伸：把"我心里想这样对"翻译成"代码说它是这样"。

**详细 API 参考**（装饰器签名 / event 助手 / Image component / config 字段类型 / fork 工作流 / 实战验证脚本模板）见 `references/astrbot-plugin-dev.md`。

### 0.5 命令参数解析的三大陷阱

AstrBot `@filter.command` 在底层把消息按 `message_str.split(" ")` 切 token,再按位置绑定到函数参数。**第 3 个 token 起的全丢**——番剧名/路径含空格时这条坑得能让你 debug 一晚上:

```python
# 看起来无害:
@filter.command("放送时间")
async def show(self, event, name_or_id: str = "", time: str = ""):
    pass

# 用户发: /放送时间 无职转生 第三季 ～ 到了异世界 周日 23:00
# 期望: name_or_id="无职转生 第三季 ～ 到了异世界", time="周日 23:00"
# 实际: name_or_id="无职转生", time="周日"   # 23:00 被丢了
```

**解法 (按推荐度):**

1. **只取 1 个 `GreedyStr` 参数 + 自己 split** (`@command("放送时间")` 路由还是命中,只是参数全在自己手里):

   ```python
   from astrbot.core.star.filter.command import GreedyStr

   @filter.command("放送时间")
   async def show(self, event, args: GreedyStr):  # 不要默认值!
       raw = event.get_message_str().strip()
       for prefix in ("/放送时间", "放送时间"):
           if raw.startswith(prefix):
               raw = raw[len(prefix):].lstrip()
               break
       tokens = raw.split()  # 现在拿到完整 args
   ```

   **关键: `args: GreedyStr` 不要给默认值**。`args: GreedyStr = GreedyStr("")` 会被 AstrBot 识别成"普通字符串 + 默认值",`is GreedyStr` 比较失败,args 当普通字符串处理(反而取第 1 个 token)。Bilibili 插件写法(`raw_args: GreedyStr` 无默认值)是有意为之。

2. **改用 `@filter.regex(r"^/xx(?:\s+(.*))?$")`** — 完全脱离 command 路由。⚠️ 注意: regex filter 的 message_str 会**绕过 wake_prefix**——可能与平台的"必须 @bot 才回复"规则冲突,部分用户发现 regex 命令被 LLM 自然语言回复抢答。验证方式: 发命令后看 AstrBot 日志是否有 `[regex]` 处理记录,如果有 LLM 也回了就说明路由冲突。

3. **保持命令装饰器 + 单 token 限制**——要求用户用下划线/ID 而非自然语言命名番剧。最稳但 UX 差。

**事件方法备查**:

| 方法 | 来源 | 用途 |
|------|------|------|
| `event.message_str` | 属性 | 完整消息纯文本(含命令前缀) |
| `event.get_message_str()` | 方法 | 同上,某些版本才支持 |

**症状速查**:

- 命令解析后 token 数对不上 → 看 `event.message_str` 原文,确认没被前置插件(ForwardReader/AstrNa)改写
- 命令不触发只走 LLM → 大概率被前置插件拦了,看 journal `analysis_type` 日志
- 解析成功但参数错位 → 函数签名参数顺序 vs AstrBot 切分顺序不匹配
- `GreedyStr` 写了默认值,期望贪婪但拿到的仍是单 token → 删默认值

详见 `references/astrbot-command-parsing.md`。

### 1. 找到 Agent 的 workspace

AstrBot agent 的代码改动在 `~/astrbot/data/workspaces/{platform}_{chat_type}_{chat_id}/` 下。如果有未提交的改动，先保存：

```bash
find ~/astrbot/data/workspaces/ -name ".git" -type d
cd <workspace>/<repo>
git status
```

### 2. 确认 fork 和解耦双系统

- 确认 remote origin 是用户的 fork（如 `publieople/astrbot_plugin_bangumi`）
- 如果 Hermes 侧有同名功能的 cron job/skill，**立即清理**——追番/通知类功能由 AstrBot 插件统一管理，不维护两套
- 删除 Hermes cron：`cronjob action='remove'`；删除 skill：`skill_manage action='delete'`

### 3. 改代码 → 跑测试 → commit

用 AstrBot 自带的 Python 3.12 venv 跑测试（所有依赖已就绪）：

```bash
cd <workspace>/<repo>
/home/po/.local/share/uv/tools/astrbot/bin/python -m pytest -q
```

提交时拆成语义清晰的 commit（新增 → 模型/数据层 → 集成/命令层）。

### 4. Push + 提 PR

```bash
git push origin feat/<branch-name>
gh pr create \
  --repo <upstream-owner>/<repo> \
  --head <fork-owner>:feat/<branch-name> \
  --base main \
  --title "..." --body "..."
```

### 5. 同步到运行中的 AstrBot

替换源码（不动 plugin_data 数据库）→ 重启：

```python
# execute_code
workspace = "/home/po/astrbot/data/workspaces/.../<repo>"
plugin_dir = "/home/po/astrbot/data/plugins/<plugin_name>"

subprocess.run(['pkill', '-f', 'astrbot run'])
time.sleep(3)

# 替换 src/ 和 .py 文件
shutil.rmtree(os.path.join(plugin_dir, "src"))
shutil.copytree(os.path.join(workspace, "src"), os.path.join(plugin_dir, "src"))
for f in ["main.py", "__init__.py", "metadata.yaml"]:
    shutil.copy2(os.path.join(workspace, f), os.path.join(plugin_dir, f))

# 重启
os.chdir("/home/po/astrbot")
proc = subprocess.Popen(
    ["/home/po/.local/bin/astrbot", "run"],
    stdout=open("data/astrbot.log", "a"), stderr=subprocess.STDOUT,
    start_new_session=True,
    env={**os.environ, "PYTHONUNBUFFERED": "1"},
)
```

验证加载成功：
```bash
grep -E "plugin.*loaded|bgmlist|broadcast|定时更新|自动填充" ~/astrbot/data/astrbot.log | tail -10
```

AstrBot 插件的测试依赖（pytest、pytest-asyncio、pydantic、aiohttp、SQLAlchemy 等）已安装在 AstrBot 自己的 venv 里。**直接用 AstrBot 的 Python 跑测试**，不用另外装：

```bash
cd ~/astrbot/data/plugins/<plugin_dir>
/home/po/.local/share/uv/tools/astrbot/bin/python -m pytest -q
```

⚠️ 不用 `pip install -r requirements.txt` 到系统 Python（3.14 缺 pip）或单独建 venv——AstrBot 的 Python 3.12 venv 已有全部依赖。

## 插件升级（替换源码，不动数据）

当改了 fork 版插件代码，要更新到运行中的 AstrBot 时：

1. **停 AstrBot**（用 `execute_code` 的 `subprocess.run(['pkill', '-f', 'astrbot run'])`——不能用 `terminal` 的 nohup/disown）
2. **替换源码**：删除插件目录下的 `src/`、`main.py` 等源文件（保留 `plugin_data/` 不动），从 workspace 或 fork 仓库 `shutil.copytree/copy2` 过来
3. **重启**：用 execute_code + `subprocess.Popen(start_new_session=True)`

```python
import subprocess, shutil, os, time

# 1. 停
subprocess.run(['pkill', '-f', 'astrbot run'])
time.sleep(3)

# 2. 换源码
workspace = "/home/po/astrbot/data/workspaces/default_GroupMessage_707942526/<repo>"
plugin_dir = "/home/po/astrbot/data/plugins/<plugin_name>"
for d in ["src"]:
    target = os.path.join(plugin_dir, d)
    if os.path.exists(target): shutil.rmtree(target)
    shutil.copytree(os.path.join(workspace, d), target)
for f in ["main.py", "__init__.py", "metadata.yaml"]:
    shutil.copy2(os.path.join(workspace, f), os.path.join(plugin_dir, f))
# 清 pycache
for pc in [os.path.join(plugin_dir, d) for d in ["__pycache__", "src/__pycache__"]]:
    if os.path.exists(pc): shutil.rmtree(pc)

# 3. 重启
os.chdir("/home/po/astrbot")
log = open("data/astrbot.log", "a")
proc = subprocess.Popen(
    ["/home/po/.local/bin/astrbot", "run"],
    stdout=log, stderr=subprocess.STDOUT,
    start_new_session=True,
    env={**os.environ, "PYTHONUNBUFFERED": "1"},
)
print(f"AstrBot PID: {proc.pid}")
```

重启后观察日志确认插件加载成功：
```bash
grep -i "bangumi\|plugin.*loaded\|定时更新" ~/astrbot/data/astrbot.log | tail -10
```

⚠️ **AstrBot 不能在 `terminal` 中用 nohup/disown 重启**——Hermes 会拒绝。始终走 `execute_code` + `subprocess`。

## 调试 AstrBot Agent 的工作

当 AstrBot 的 LLM agent 在群聊中被要求写代码/改插件时，它的工作会留在两个地方：

### 1. 会话记录

Agent 的完整对话历史（含 tool calls）存在 `data_v4.db` 的 `conversations` 表：

```python
import sqlite3, json
conn = sqlite3.connect('/home/po/astrbot/data/data_v4.db')
rows = conn.execute('''
    SELECT conversation_id, user_id, updated_at, content
    FROM conversations ORDER BY updated_at DESC LIMIT 10
''').fetchall()
for r in rows:
    msgs = json.loads(r[3])
    # msgs 是 [{role: "user"|"assistant"|"tool", content: ...}, ...]
```

- `user_id` 格式：`default:GroupMessage:<群号>` 或 `default:FriendMessage:<QQ号>`
- `platform_message_history` 表**只存 webchat 消息**，QQ 群聊消息全在 conversations 里

### 2. 工作区（代码改动）

Agent 的代码改动在 `~/astrbot/data/workspaces/{platform}_{chat_type}_{chat_id}/`：

```bash
# 找 agent 的 git 仓库
find ~/astrbot/data/workspaces/ -name ".git" -type d
# 例：~/astrbot/data/workspaces/default_GroupMessage_707942526/astrbot_plugin_bangumi/
```

Agent 可能在 feature branch 上有未提交的改动——检查 `git status`、`git diff`、`git log`。

⚠️ **Agent 调用次数用尽时，代码改动可能留在 workspace 未 commit**。这时候接手前先 `git stash` 保存现场，别丢工作。

### 3. 远端仓库与 fork

Agent 配置的 git remote 通常是用户的 GitHub fork（如 `publieople/astrbot_plugin_bangumi`），但它可能改的是 workspace 里的本地副本。检查：

```bash
cd <workspace>/<repo>
git remote -v            # 看 fork 地址
git branch -a            # 看是否有 feature branch
git diff origin/main     # 和远端 main 对比
```

---

## Whisper (Local) 语音转文字 + GPU 加速

AstrBot 内置 `openai_whisper_selfhost` 提供商会自动加载 openai-whisper 模型。**源码只认 `cpu` 和 `mps`，不认 `cuda`**，需手动 patch。

### 1. 装 CUDA 版 torch + whisper

```bash
ASTRBOT_PY=$(/home/po/.local/bin/uv python find 3.12)
uv pip install --python /home/po/.local/share/uv/tools/astrbot/bin/python \
  --index-url https://download.pytorch.org/whl/cu128 torch
uv pip install --python /home/po/.local/share/uv/tools/astrbot/bin/python \
  -i https://pypi.tuna.tsinghua.edu.cn/simple openai-whisper
```

### 2. 源码加 CUDA 支持

编辑 `/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/astrbot/core/provider/sources/whisper_selfhosted_source.py`，在 `_resolve_device()` 最前面加：

```python
if self.device == \"cuda\":
    import torch
    if getattr(torch.cuda, \"is_available\", None) and torch.cuda.is_available():
        return \"cuda\"
    logger.warning(\"Whisper 已配置为使用 CUDA，但当前环境不可用，将回退到 CPU。\")
    return \"cpu\"
```

### 3. 配置 cmd_config.json

⚠️ **该文件有 UTF-8 BOM**，Python 读时必须用 `encoding='utf-8-sig'`。

```python
import json
with open('data/cmd_config.json', encoding='utf-8-sig') as f:
    conf = json.load(f)

# 改 provider 内嵌列表中的 whisper_selfhost 条目
for p in conf['provider']:
    if p.get('id') == 'whisper_selfhost':
        p['model'] = 'small'           # RTX 4070 8GB → small
        p['whisper_device'] = 'cuda'   # 不是 cpu 不是 mps

# 启用 STT
conf['provider_stt_settings'] = {'enable': True, 'provider_id': 'whisper_selfhost'}

with open('data/cmd_config.json', 'w', encoding='utf-8-sig') as f:
    json.dump(conf, f, indent=2, ensure_ascii=False)
```

### GPU 模型选择

| GPU 显存 | 模型 | 速度 |
|----------|------|------|
| ≥12GB | medium | ~0.45x 实时 |
| 6-12GB | **small** | ~0.21x 实时 |
| <6GB | base | — |

> WSL CUDA 下 medium 反而比 small 慢（开销大），4070 8GB 选 small。

### 验证

```bash
/home/po/.local/share/uv/tools/astrbot/bin/python -c "
import torch; print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0))
import whisper; print('whisper OK')
"
```

### 注意

- **WebUI 下拉框可能仍只显示 CPU**（前端硬编码），但配置文件写 `cuda` 后端能认。别在 WebUI 里改这个 provider。
- **`uv tool update` 会覆盖源码 patch**，更新后需重新 patch。
- **stt_health_check.wav 缺失**：PyPI wheel 中不包含 `samples/stt_health_check.wav`，测试会报"文件不存在"。用 ffmpeg 生成一个 16kHz 单声道 WAV 放到 `/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/samples/`。
- **systemctl 重启**：`sudo systemctl restart astrbot`（如已配 systemd service）。

### 速度优化

- **清华 PyPI 镜像**：国内网络 pip 下载极慢，加 `-i https://pypi.tuna.tsinghua.edu.cn/simple` 秒装。
- **PyTorch CUDA 索引**：`--index-url https://download.pytorch.org/whl/cu128`，不能和 `-i` 混用。`uv pip install` 报 `cannot be used multiple times` → 分两次调用。
- **Python 3.14 避坑**：Arch 系统 Python 3.14 下很多包（openai-whisper 等）因 `pkg_resources` 移除而无法安装。**始终用 `uv venv --python 3.12`**。
- **Python 3.14 避坑**：Arch 系统 Python 是 3.14，但很多包（openai-whisper、setuptools 等）在 3.14 下因 `pkg_resources` 移除而无法安装。**始终用 `uv venv --python 3.12` 或 `uv tool install --python 3.12`**，别和系统 3.14 死磕。

### B站视频转录（bilibili-transcript）

详见 `references/bilibili-transcript.md`。核心要点：B站 412 反爬 → 加 `Origin` 头；Whisper 不要强设 `--language zh`；必须 Python 3.12 venv。

## FutureTask 定时任务

AstrBot v4.14+ 支持主 Agent 管理定时任务。用户说自然语言即可触发：

> "帮我创建定时任务：每周五 23:00 检查番剧更新"
> "每天早上 8 点提醒我开会"

Agent 会调用内置的 `create_future_task` 等工具。任务到时间后 AstrBot 自动唤醒 Agent，执行 `note` 中的 prompt，结果通过 `send_message_to_user` 推送到原会话。

**支持的推送平台**：OneBot v11（QQ）、Telegram、Slack、飞书、Discord、Misskey、Satori。

**⚠️ 所有 FutureTask 都是 LLM 推理模式**——Agent 收到 note 文本后自主决策。没有"直接发固定消息"的硬执行模式。适合需要智能判断的场景（如检查 API 是否有更新），不适合纯确定性操作。

---

## 从 Hermes 迁出 NapCat（完全清理）

当你决定不再用 Hermes 接 QQ，而是换 AstrBot 时：

```bash
# 1. 禁用 NapCat
sed -i 's/NAPCAT_ENABLED=true/NAPCAT_ENABLED=false/' ~/.hermes/.env
sed -i '/^NAPCAT/d' ~/.hermes/.env  # 或直接清掉所有 NapCat 行

# 2. 停止 gateway
pkill -f 'gateway run'

# 3. 重置到官方 main（如果之前用了 fork）
cd ~/.hermes/hermes-agent
git fetch origin
git reset --hard origin/main
git remote remove upstream 2>/dev/null
git remote remove moeover 2>/dev/null
git remote remove fork 2>/dev/null
git remote set-url origin https://github.com/NousResearch/hermes-agent.git

# 4. 同步个人 fork（如果 fork 存在）
git remote add fork https://github.com/<username>/hermes-agent.git
git push fork main --force
git remote remove fork

# 5. 重启 gateway（systemd 自动重启，或手动）
```

清除后 gateway 会以 2 个平台运行（api_server + feishu），**端口 8646 释放**，NapCat 不再连接。

---

## cmd_config.json 关键字段

| 字段 | 路径 | 说明 |
|------|------|------|
| `default_personality` | `provider_settings` | 设为 persona_id（如 `"magician"`） |
| `identifier` | `provider_settings` | 识别群员，设为 `true` |
| `datetime_system_prompt` | `provider_settings` | 日期时间提示，设为 `true` |
| `reply_with_mention` | `platform_settings` | 只看@才回复，设为 `true` |
| `default_provider_id` | `provider_settings` | 默认模型 ID |
