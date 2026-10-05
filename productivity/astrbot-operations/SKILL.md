---
name: astrbot-operations
description: AstrBot 运营维护 — 进程管理、插件热重载、人格系统、知识库集成、常见故障排查
---

# AstrBot 运维指南

## 进程管理

**AstrBot 通过 systemd 管理（非用户手动启动）**：
```bash
sudo systemctl status astrbot      # 查看状态
sudo systemctl restart astrbot     # 重启
sudo systemctl stop astrbot        # 停止
```

日志输出到 systemd journal，非日志文件：
```bash
sudo journalctl -u astrbot --no-pager -n 100
sudo journalctl -u astrbot --no-pager --since "1:06"
```

#### ⚠️ 用户说"查日志"时,先验证日志在不在写

**常见坑：用户问"看一下 astrbot 日志"时,`data/astrbot.log` 经常是死文件。** 三个根因:

1. `cmd_config.json` 里 `log_file_enable: false`(默认)→ AstrBot 不写文件,只 stdout
2. systemd unit (`~/.config/systemd/user/astrbot.service`) 没设 `StandardOutput=append:<path>` → stdout 默认进 journal,而不是 `data/astrbot.log`
3. 用户以前手敲 `astrbot run >> data/astrbot.log 2>&1` 留下的旧文件,mtime 几个月前,跟当前进程完全无关

**验证日志是不是活的(不要直接 grep):**

```bash
# 1. 看文件 mtime
stat /home/po/astrbot/data/astrbot.log | grep Modify

# 2. 看当前 astrbot 进程的 stdout 实际指向哪
PID=$(pgrep -f 'astrbot run' | head -1)
ls -l /proc/$PID/fd/{1,2}
# 指向 socket 或 pipe → stdout 被 systemd 接管,data/astrbot.log 是死的
# 指向 /home/po/astrbot/data/astrbot.log → 真的在写

# 3. 进程是 systemd 直接拉起的还是手敲的?
ps -o pid,ppid,cmd -p $PID
# PPID=1 (systemd) → 父进程是 init
# PPID=bash 的 pid → 手敲启动
```

如果 `data/astrbot.log` mtime < 当前时间,直接看 journal:
```bash
journalctl --user -u astrbot -n 200 --no-pager
journalctl --user -u astrbot --since "30 min ago" --no-pager
```

**修复 systemd unit 持久记录日志(推荐):**

在 `~/.config/systemd/user/astrbot.service` 加:
```ini
[Service]
# ... existing ...
StandardOutput=append:/home/po/astrbot/data/astrbot.log
StandardError=append:/home/po/astrbot/data/astrbot.log
```
然后 `systemctl --user daemon-reload && systemctl --user restart astrbot`,日志立刻开始写。`append:` 而不是 `file:` —— 避免 systemd 启动前清空文件,重启不会丢历史日志。

WebUI: `http://localhost:6185`，用户名 `Publieople`，密码 `Fzj103415422`。

## 版本升级

AstrBot 通过 `uv` 部署，**不支持在 WebUI 里直接升级**。WebUI 升级只更新前端 dist 文件，Core 版本不变会导致版本错配。

```bash
# 通过代理升级时需加大超时（默认 30s 不够），大包走清华镜像
env UV_HTTP_TIMEOUT=300 UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple uv tool upgrade astrbot --python 3.12
```

升级后如果 WebUI 和 Core 版本不一致：删除 `data/dist` 目录后重启。
```bash
sudo systemctl stop astrbot
rm -rf /home/po/astrbot/data/dist
sudo systemctl start astrbot
```

**注意**：升级后首次启动可能弹出 `Install dashboard? [Y/n]:` 交互式提示。先手动跑一次 `echo "y" | astrbot run` 让 dashboard 装完，然后再用 systemd 启动。

## 插件管理

**AstrBot 热重载有两层含义，要分清**：

1. **新增插件** — 把新插件目录放到 `data/plugins/`，**重启 AstrBot 后生效**（启动时扫描一次）。不要手动 kill 进程。
2. **修改已有插件代码** — 默认**不会自动热重载**。`star_manager.py:210` 写明 `if os.getenv("ASTRBOT_RELOAD", "0") == "1": asyncio.create_task(self._watch_plugins_changes())`，watcher 默认不启。当前 systemd service 没设这个 env，所以**改了 main.py 或任何被 import 的子模块都要 `sudo systemctl restart astrbot`**。即使启了 watcher，热重载也只重建插件主 class 实例，被主模块 import 的二级 .py（如 `workflow_engine.py`）不会重新 import（Python 模块缓存机制），改完还是要 restart。

插件目录: `/home/po/astrbot/data/plugins/`

### 通过 CLI 安装（推荐）

```bash
cd /home/po/astrbot
# 搜索插件
astrbot plug search bangumi
# 用 marketplace 名称安装（注意：可能与 GitHub repo 名不同）
astrbot plug install astrbot-plugin-bangumi-enhance
# 从 GitHub URL 安装
astrbot plug install https://github.com/united-pooh/astrbot_plugin_bangumi
```

**注意**：命令是 `astrbot plug`（不是 `plugin`）。marketplace 上的插件名用连字符（`astrbot-plugin-bangumi-enhance`），可能不同于 GitHub repo 名（`astrbot_plugin_bangumi`）。

### 手动 git clone

```bash
cd /home/po/astrbot/data/plugins
git clone <repo-url>  # 需要代理: export https_proxy=http://127.0.0.1:7890
```

### 插件加载失败

如果插件加载失败，通过 API 重载:
```
POST /api/plugin/reload-failed  {"dir_name": "astrbot_plugin_xxx"}
```

**不要凭记忆说"X 插件已装"**：memory 里关于"哪些插件装了"的记录会过期（插件可能被禁用/卸载/重命名）。在断言某个插件存在之前**先 `ls ~/astrbot/data/plugins/` 确认目录在不在**，再决定后续操作。错误信息: "meme_manager 已装"→目录不存在→给用户错误指引。

## 插件开发（fork + 改造 vs 从零写）

**先调研后开工**（用户偏好：spec-first，先搜现成方案再集成）。完整开发流程、文档坑、装饰器陷阱、验证模式见 [references/plugin-dev.md](references/plugin-dev.md)。

### 核心规则

1. **先搜现成** — GitHub + AstrBot 官方 marketplace，能 fork 不要从零写。`gh repo fork <upstream>` 自动加 upstream remote
2. **写不熟悉的框架/工具代码前必须先查文档** — AstrBot 文档站 `docs.astrbot.app` 大量路径 404，真实路径是 `/dev/star/guides/xxx.html` 不是 `/dev/star/xxx.html`
3. **本地直写** — 放 `data/plugins/<name>/` 后 `sudo systemctl restart astrbot` 加载；不要走 WebUI 安装
4. **改完 metadata.yaml 的 name/author/version**，fork 仓时改 author 标注上游 `X / publieople`
5. **每次改动写 ad-hoc 验证** — 详见下方验证模式

### 关键装饰器（`from astrbot.api.event.filter import`）

```python
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import (
    event_message_type, EventMessageType,  # 全消息钩子
    command,                                # 命令: @command("xxx")
    llm_tool,                               # LLM 工具: @llm_tool(name="x")
)

@register("plugin_id", "Author", "description", "v1.0.0", "https://github.com/...")
class MyPlugin(Star):
    def __init__(self, context: Context, config=None): super().__init__(context)

    @command("看图")                                              # 命令
    async def cmd(self, event: AstrMessageEvent, arg: str = ""):  # 空格分隔参数
        yield event.plain_result("...")

    @llm_tool(name="my_tool")                                      # LLM 工具
    async def my_tool(self, event: AstrMessageEvent, query: str):
        '''工具描述。

        Args:
            query(string): 检索词
        '''
        return "结果"  # str 加入 LLM 上下文

    @event_message_type(EventMessageType.ALL)                       # 消息钩子
    async def on_msg(self, event: AstrMessageEvent):
        if "触发词" in event.message_str:
            ...
```

**常见坑**：
- `@llm_tool(name="x")` 的 `name=` 是 **keyword arg** 不是 positional（AST 检查时必须查 keywords 而不是 args）
- 命令带空格参数时 AstrBot 框架自动 split 给 `arg: str` 形参
- 命令函数 return 一次就行（`yield event.plain_result(...)` 或 `return event.plain_result(...)`）；`event.image_result(url)` 是图片助手

### `_conf_schema.json` 字段类型速查

- `string` + `options:[...]+labels:[...]` → 下拉单选
- `list` + `items.type=string` + `options+labels` → 复选多选（list 的 items 也支持 options/labels）
- `int`/`float` + `slider:{min,max,step}` → 滑块
- `_special: "select_provider" / "select_persona"` → WebUI 下拉选已注册的 provider/persona

### 验证模式（ad-hoc 脚本 + journal）

每次代码改动后**必须**做 3 件事：

```bash
# 1. 语法
python3 -c 'import ast; ast.parse(open("main.py").read()) && print("OK")'

# 2. 重启 + journal 确认（Loading plugin + Added llm tool 出现，无 error）
sudo systemctl restart astrbot
sleep 4
sudo journalctl -u astrbot --since "30 seconds ago" --no-pager | \
  grep -E "Loading plugin <name>|Added llm tool: <tool>|error|exception"
```

**journal 没看到 plugin 行**时等更久（AstrBot 顺序加载多插件，timing 不固定），再 grep 一次。

**ad-hoc 验证脚本**（推荐）：用 `ast` 模块走 AST 提取装饰器、参数、数据结构，写到 `/tmp/hermes-verify-<name>.py` 跑完删。验证项示例：
- 装饰器是否存在、参数 keyword 还是 positional
- 数据结构正确性（dict 长度、list 元素类型、keys ⊆ 某集合）
- 业务逻辑模拟（解析函数、过滤函数）
- 配置字段保留（schema 改后其他字段不变）

→ 完整开发流程、fork 工作流、`_conf_schema.json` 字段细节、LLM tool 文档路径、栗次元/figment 等外部 API 集成的具体配方见 [references/plugin-dev.md](references/plugin-dev.md)


## 人格系统（Persona）

**生效链路**：
1. 用户在 WebUI 保存人格 → 存入 AstrBot DB
2. 群消息到达 → `self_learning` 插件 `get_persona_id()` 选择人格
3. `MemoryProcessor` 加载人格提示词 → 注入 LLM system prompt
4. LLM 按人格生成回复

**关键坑**：`self_learning` 插件有自己的人格选择逻辑，可能会覆盖 WebUI 中手动切换的人格。日志中看到 `最终使用人格: XXX` 才是实际生效的人格。如果切换了人格但群里没变，检查 `self_learning` 覆盖。

### 限定 Skill/Tool 到指定群

Persona 的 `tools` 和 `skills` 字段控制哪些 Tool/Skill 对该人格可用：

- `null` / 不填 → 使用所有 Tool/Skill
- `[]`（空数组）→ 不使用任何 Tool/Skill（空白名单）
- `["name1", "name2"]` → 只使用列出的 Tool/Skill

结合**会话规则**（Session Rules）可以将一个绑定指定 Tool/Skill 白名单的人格绑定到某个群，实现「这个 Skill 只在 A 群可用」：

**WebUI 操作步骤：**

1. **创建专用人格**: WebUI → 侧边栏 **人格** → 新建人格 → 在高级设置中设置 `skills` / `tools` 白名单（只勾选你要限定的 Skill）
2. **确保默认人格不加这个 Skill**: 默认人格的 `skills` 保持 `null`（全开）或 `[]`（关闭），这样其他群看不到它
3. **绑定到目标群**: WebUI → **配置** → **会话管理**（Session Rules）→ 找到目标群的 UMO（格式如 `aiocqhttp:GroupMessage:群号`）→ 编辑 `session_service_config` → 设置 `persona_id` 为人格名

**查看当前群的 UMO：** 在群里发 `/sid`，返回的 UMO 字符串就是该群的唯一标识。也可以用 `/name <别名>` 给群设别名方便在 WebUI 里检索。

**生效链路：**

消息到达 → `persona_mgr.resolve_selected_persona()` 检查 UMO 的 `session_service_config.persona_id` → 强制使用该 Persona → 只加载 Persona 配置的 `skills` 列表 → LLM 只能调这些 Skill

**验证方法：**

```bash
sudo journalctl -u astrbot --since "1 minute ago" --no-pager | grep -i "persona.*最终使用"
```

日志显示 `最终使用人格: <你绑定的人格>` + LLM 的 tools/skills 列表被过滤到只含白名单项。

**源码确认（Persona 模型 `/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/astrbot/core/db/po.py`）：**
```python
class Persona(SQLModel, table=True):
    tools: list | None = Field(default=None, sa_type=JSON)
    """None means use ALL tools, empty list means no tools, otherwise a list of tool names."""
    skills: list | None = Field(default=None, sa_type=JSON)
    """None means use ALL skills, empty list means no skills, otherwise a list of skill names."""
```

通过 API 查看人格列表：
```
GET /api/persona/list  (Authorization: Bearer <token>)
```

**人格存储位置**：存在 SQLite DB（`data_v4.db`）里，**不是文件系统 yaml/json**。AstrBot 默认配置在 `cmd_config.json` 里只有两个相关字段：
- `provider_settings.default_personality: "..."` — 默认人格名
- `provider_settings.persona_pool: ["..."]` — 可用人格池

**编辑入口**：**WebUI 侧边栏 → 人格**（不是插件配置页）。要新建/编辑/切换默认人格都从这里进，不是写配置文件。Angel Heart 插件的 `personality.ai_self_identity` 是插件追加给 LLM 的补充系统提示，叠加在人格系统提示之上——两者都填才完整（人格 = 身份，插件 personality = 行为约束）。

## 知识库集成

配置在 `/home/po/astrbot/data/cmd_config.json`:
- `kb_names: ["盒武器"]` — 使用的知识库列表
- `kb_agentic_mode: true` — 让 LLM 可主动调用 KB 工具（推荐）
- `kb_fusion_top_k: 20` / `kb_final_top_k: 5` — 检索参数

**盒武器知识库**: `kb_id=c0ca81b9-f1f0-4479-9ce8-f6c3017958cf`，Embedding: SiliconFlow `BAAI/bge-m3`。

注意：`embedding_dimensions` 对 `bge-m3` 应设为 `0`（硅基流动不支持该参数）。

## 添加 OpenAI 兼容模型提供商

AstrBot 支持通过 OpenAI 兼容 API 接入自定义模型（如 OpenCode Zen 免费模型）。

### 配置方式

在 WebUI `设置 → 大语言模型 → 添加模型源`，或直接编辑 `data/config/abconf_*.json`：

#### provider_sources 添加源

```json
{
  "provider": "opencode",
  "type": "openai_chat_completion",
  "api_base": "https://opencode.ai/zen/v1",
  "key": [""],       // ⚠️ OPENCODE 免费模型特例：见下方 Auth 坑章节，正确配置是 key: []（空数组）
  "id": "opencode",
  "enable": true
}
```

#### provider 添加模型（可选，预览模型时自动创建）

```json
{
  "id": "opencode/deepseek-v4-flash-free",
  "enable": true,
  "provider_source_id": "opencode",
  "model": "deepseek-v4-flash-free",
  "modalities": ["text"],
  "custom_extra_body": {},
  "max_context_tokens": 20000,  // 免费模型通常20k
  "reasoning": false
}
```

### OpenCode Zen 免费模型

| 模型名 | 上下文 | 说明 |
|--------|--------|------|
| `deepseek-v4-flash-free` | ~20K | 通用编程 |
| `big-pickle` | ~20K | OpenCode 官方免费 |
| `minimax-m2.5-free` | ~32K | 科大讯飞 |
| `mimo-v2.5-free` | ~20K | 小米开源 |
| `nemotron-3-ultra-free` | ~20K | NVIDIA |
| `north-mini-code-free` | ~20K | 知乎开源 |

### Auth 关键行为

**OpenCode Zen 免费模型 `POST /v1/chat/completions` 的行为：**
- **不传 `Authorization` header → 200 OK**（返回 `cost":"0"`）
- 传了任何非空 `Authorization` header → 401 `Invalid API key.` 或 403 `error code: 1010`
- 免费的 `/v1/models` 列表不需要 auth（可以用来确认模型存在）

**AstrBot 的 `openai_source.py`（第 360 行，v4.26.2）：**
```python
self.chosen_api_key = self.api_keys[0] if len(self.api_keys) > 0 else None
```
- `key: []` → `chosen_api_key = None` → SDK 不发 `Authorization` header → ✅
- `key: ["***"]` → `chosen_api_key = "***"` → SDK 发 `Bearer ***` → ❌ 401
- `key: [""]` → `chosen_api_key = ""` → 新版 OpenAI SDK 不接受空字符串，抛错

**新版 OpenAI SDK 不允许 `api_key=None` 或 `api_key=""`**，会直接报 `Missing credentials` 错误。需要在 `~/.config/astrbot/` 或系统层面设 `OPENAI_API_KEY` 环境变量为任意值绕过去。详见 [references/opencode-auth-debug.md](references/opencode-auth-debug.md)。

### 注意事项

- **`api_base` 必须 `/v1` 结尾**：`https://opencode.ai/zen/v1`（不是 `zen`）
- **免费模型上下文窗口小**（20K-32K），日常对话够用但长文本会截断
- **无速率保证**：免费 tier 有隐式限速，超限等待即可
- **可用模型列表**：`curl https://opencode.ai/zen/v1/models`
- **不传敏感代码**：免费 tier 数据可能用于改进服务

## 常见故障

### WSL PYTHONPATH 污染

Hermes Agent 设置 `PYTHONPATH=/home/po/.hermes/hermes-agent` 全局环境变量，
WSL 中每个 Python 进程都继承此路径。症状：
- `pip install` 产生 `hermes-agent requires xxx` 版本冲突警告
- `uv pip install --python` 安装到错误位置
- Python 进程加载 hermes-agent 依赖导致版本冲突

**修复**：启动任何 Python 命令前 `unset PYTHONPATH`。
在 systemd service 或启动脚本中也应主动 unset。

详见 references: [配置文件陷阱](references/config-file-hazards.md) | [人格系统详解](references/persona-flow.md) | [Persona Skill 限域源码细节](references/persona-skill-scope-detail.md) | [音乐插件坑](references/music-plugin.md) | [Bangumi 番剧订阅](references/bangumi-plugin.md) | [Whisper STT 配置](references/stt-whisper-setup.md) | [IndexTTS/CosyVoice2 部署](references/indextts-setup.md) | [CosyVoice2 部署](references/cosyvoice2-setup.md) | [TTS 模型选型](references/tts-model-selection.md) | [GPT-SoVITS Docker 部署](references/gpt-sovits-setup.md) | [记忆/认知插件栈选型](references/memory-plugin-stack.md) | [NVIDIA Rerank Provider 配置](references/nvidia-rerank-provider.md) | [远程服务隧道](references/remote-tunnel.md) | [ComfyUI promax 插件](references/comfyui-promax-plugin.md) | [LLM Provider 故障排查](references/llm-provider-debugging.md)

- **调试 / 配置 / 查询命令的参数应该接受自然语言输入，不要强制技术 ID** — 用户在群里看到的是中文番剧名、用户别名，不是 `subject_id=622206`。第一版 `/放送测试 描绘` 报"未找到"是因为只接受 ID。修法：参数解析层先试 `get_<thing>_name(target_id)`，miss 时 fallback 到 `find_<thing>_candidates(group_id, target_id, limit=3)`：单候选自动取 ID，多候选列出来让用户选，零候选报"未找到"。复用已有的 fuzzy match 函数，0 行新逻辑。**适用范围**：任何 `/<plugin>X <Y>` 命令，凡是用户大概率输入中文/自由文本的，都该如此。

### LLM/Provider 端故障排查（"bot 不回我"、"bot 调了 tool 但没执行"）

排查路径：QQ 网关 → AngelHeart 决策 → LLM 调用 → promax → ComfyUI。每层都有具体的 journal 特征和修复方式，详见 [references/llm-provider-debugging.md](references/llm-provider-debugging.md)。最常见的五个根因（按频率排序）：

1. **`/provider` 是 session 级** — 在群 A 切到 M3 成功，群 B 仍走 free 档 5 次 429。修 `cmd_config.json:233 default_provider_id` 改全局默认
2. **antipromptinjector 静默封禁 admin** — bot 完全不回你（`antipromptinjector.main:1673 黑名单用户 ... 封禁已到期` 是解封信号）。等 1 小时 / `/unban` / 加白名单
4. **AngelHeart "被呼唤"路径二次压制 tool 调用** — AngelHeart 决策"参与"但 LLM 只回文字不调 tool,bot 回"行吧给你画任务丢进去了"但 ComfyUI 0 got prompt。修复:**promax 加 `@filter.custom_filter(DrawCommandFilter)` 装饰器,匹配 `text.startswith("画"/"/画"/"t2i"/"复刻"/...)` 直接走 submit_task,bypass LLM 整条决策链**。50 行内,不动 AngelHeart,不动 LLM provider。 完整 patch 在 [references/comfyui-promax-plugin.md](references/comfyui-promax-plugin.md) 末尾"Command 路由绕过 LLM"段(2026-07-08 实测生效)

5. **M3 模型 docstring 服从性弱** — `comfyui_txt2img` docstring 写"You MUST translate"+ 中英对照 + tags 列表,M3 仍多次幻觉回文不调 tool。Prose 指令对 M3 不够用,必须 code-level 强制路由(`@filter.command`)。M3 会在回包时诚实承认:"我没法直接调 curl,我能用的是 comfyui_txt2img",然后**还是不调** — 它嘴说"会调"和手发 `tool_use` 块是分开的两个决策

6. **SKILL.md 写"调 curl/terminal"没用** — AstrBot `skills_like` tool schema 模式下,LLM 只能看到 LLM-registered tools(`comfyui_txt2img` 这种),看不到 terminal/curl tool。M3 自描述:"我没法直接调用那个文件里的 curl 命令啊,我能用的是 comfyui_txt2img 这个 tool"。SKILL.md 的"调 curl POST /prompt"是写给自己看的提示词,不是工具。**真要走 SKILL 路径,skill 必须注册成 `@llm_tool` 才有 LLM 可见的 tool schema**

7. **SKILL.md 还需 `_meta.json` 才被 AstrBot sandbox 识别** — 只放 `SKILL.md` 在 `data/skills/<name>/`,AstrBot skills.json 不识别,LLM 看不到。`{"ownerId":"local","slug":"<name>","version":"1.0.0","publishedAt":<unix_ms>}` 最小 meta。少了 `slug` 字段就不出现 active=true

8. **ComfyUI Anima 不内嵌 CLIP/VAE** — `comfyui_txt2img` 走 `_build_comfyui_prompt` 标准路径,Anima ckpt 加载后 clip=null,立即报 `clip input is invalid: None`。修法:检测 `eng.workflow_prefixes["anima"]`,有就走 anima workflow(三节点 CLIPLoader+VAELoader+CheckpointLoaderSimple)。详见 comfyui-api skill 的 Anima 集成 pitfall 段

9. **promax `@llm_tool` + `@filter.command` 是两套路径** — `@llm_tool(name="comfyui_txt2img")` 走 LLM tool schema,被 LLM 调;`@filter.custom_filter(DrawCommandFilter)` 走 plugin filter,绕过 LLM。两条路径**互不冲突**,但 prompt 注入策略不同:tool path 需要 LLM 写 Danbooru 标签,command path 由用户直接写英文 prompt。同一 plugin 装两套后,`aimg 抽烟白毛猫娘` 走 tool path,"画 1girl, white_hair, cat_girl" 走 command path,后者成功率 100%(实测 0 幻觉)

排查路径(完整):QQ 网关 → AngelHeart 决策 → LLM 调用 → promax 内部 task_queue → submit_task → ComfyUI server `POST /prompt`。每层都有具体的 journal 特征:AngelHeart 决策日志在 `[Plug] [INFO] [roles.front_desk:566] 决策为'参与'` 行;LLM tool 调用见 `[Core] [INFO] [provider.func_tool_manager:388] Added llm tool: <name>` 启动行;promax submit_task 见 `[Plug] [INFO] [ModComfyUI.*]` 内部(注意 log_file_enable=false 时这些行不会进 journal);ComfyUI 端见 `ssh server 'sudo journalctl -u comfyui --since "5 min ago" --no-pager | grep "got prompt\|clip input\|Prompt executed"'`

M3 模型特性观察(2026-07-08 复刻白毛猫娘 session):
- M3 在 AngelHeart "被呼唤回复"路径下,3 次都口头承诺"调 tool 给你跑"但实际 0 tool call
- M3 在 `skills_like` 模式下会**自描述 tool schema 限制**("我没法直接调 curl"),不会硬编"调 curl 了"
- 翻译中文 prompt:M3 不像 deepseek-v4-flash 会写英文,M3 直接编"我按 Danbooru 风格写"但实际可能传中文

## 远程服务隧道（SSH + systemd）

AstrBot 需要访问内网/无公网 IP 的远程服务（如实验室 ComfyUI 服务器）时，**优先用 WSL systemd 管理 SSH 隧道**，不要用 Windows 任务计划程序或 WSL 登录脚本。

### 原则

- **WSL 里跑** — ssh 客户端在 WSL 内，systemd 管理生命周期
- **Type=simple** — 不加 `-f`（SSH fork 标志），让 systemd 直接控制进程
- **Restart=on-failure** — 网络闪断自动重建
- **After=network-online.target** — 确保网络就绪再连，避免开机时 SSH 隧道跑在网卡未就绪前

### service 模板

```ini
[Unit]
Description=SSH Tunnel to <服务名>
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=po
ExecStart=/usr/bin/ssh -p <端口> -N -L <本地端口>:127.0.0.1:<远程端口> -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes <user>@<host>
ExecStop=/usr/bin/pkill -f "ssh.*<host>.*<本地端口>"
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

关键参数：
- `-N`：不执行远程命令（纯隧道）
- `-L <A>:<B>:<C>` ：本地端口转发，`A:B:C` = 本地监听端口:目标主机:目标端口
- `ServerAliveInterval=30`：每 30s 发心跳保活 SSH 连接
- `ExitOnForwardFailure=yes`：转发失败时退出（让 systemd 重启），避免 SSH 进程挂起

### 安装

```bash
sudo tee /etc/systemd/system/<name>.service << 'EOF'
...service content...
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now <name>
```

**前提**：SSH 密钥已配置且无密码。验证方法：
```bash
ssh -o BatchMode=yes -p <port> <user>@<host> "echo OK"
```

### 验证

```bash
curl -s http://127.0.0.1:<本地端口>/system_stats | head -c 200
```

### cjxzdzh/astrbot_plugin_comfyui 配置

插件通过文件名约定将任意 ComfyUI 工作流封装为 LLM 可调用工具。详见 [references/remote-tunnel.md](references/remote-tunnel.md)。

## 记忆/认知插件选型

AstrBot 生态里有 `livingmemory` / `self_learning` / `angel_heart` + `angel_memory` / `portrayal` 等多套记忆/认知插件。**多套并存会互相污染上下文**（同条消息被记 N 次，召回时上下文打架）。当前推荐组合：**Angel Heart + Angel Memory**，把前两个禁用。

详细选型、provider 配置、rerank 选型、与人格系统的关系见 [references/memory-plugin-stack.md](references/memory-plugin-stack.md)。

**1. LLM API 挂死导致 bot 不回复**
症状：进程在跑但日志不再更新，10+ 分钟无新消息。
原因：LLM API 连接进入 CLOSE-WAIT 阻塞消息处理管线。
修复：`sudo systemctl restart astrbot`

**2. 插件热加载后不生效**
症状：插件目录有文件但未出现在已安装列表。
修复：调用 `POST /api/plugin/reload-failed {"dir_name":"xxx"}`

**3. systemd 下插件文件修改不生效**
症状：手动改了 plugins 目录下的 .py 文件，WebUI 也点了热重载但行为不变。
原因：systemd 管理的 AstrBot 进程跑的是内存中的代码。热重载通知运行中的进程重新加载模块，但 `@filter.command` generator 可能不会重新绑定。
修复：`sudo systemctl restart astrbot`。验证：看日志是否有对应代码路径的新日志行。

**特例——修改 workflow_engine.py 等二级模块**：AstrBot 热重载只重建插件实例（main.py 的 class），不会重新导入被主模块 import 的二级 .py 文件（Python 模块缓存机制）。修改任何 main.py 以外的插件文件后，必须 `sudo systemctl restart astrbot` 才能生效。

**推送失败 `'group' is not a valid MessageType` 或 `未找到匹配平台`**：这是 AstrBot v4 session 字符串构造错误。格式必须是 `{cmd_config.json platform.id}:{GroupMessage|FriendMessage|OtherMessage}:{群号或用户ID}` —— platform_id 是用户在配置里给 platform 起的名字（公仆这里是 `default`），不是 adapter 类名 `aiocqhttp`。枚举 `context.platform_manager.platform_insts` 找真 id 而不是猜。完整解剖 + 诊断流程见 `astrbot-plugin-development/references/session-string-format.md`。

### 3.5 验证代码改动是否真进了运行进程（不是改了文件就以为生效）

改完代码 → 怀疑没生效 → 不要凭印象走。先三步确诊：

```bash
# 1. 确认文件确实改过（避免编辑器没保存、buffer 同步错）
grep -n "aiocqhttp:GroupMessage" ~/astrbot/data/plugins/<plugin>/src/app/subscription_service.py

# 2. 确认 watcher 是否启动
PID=$(pgrep -f 'astrbot run' | head -1)
tr '\0' '\n' < /proc/$PID/cmdline | head
# 看不到 --reload → ASTRBOT_RELOAD 默认未启 → watcher 没启动
cat /proc/$PID/environ | tr '\0' '\n' | grep ASTRBOT_RELOAD
# 无输出 = env 没设，watcher 必然没起

# 3. 跑触发路径，journal 看新代码有没有出现
sudo journalctl -u astrbot --since "30 sec ago" --no-pager | \
  grep -E "<新代码路径的日志特征>"
```

**永久开启 watcher（dev-only 推荐，生产保持关闭）**：`sudo systemctl edit astrbot` 加：
```ini
[Service]
Environment="ASTRBOT_RELOAD=1"
```
`sudo systemctl daemon-reload && sudo systemctl restart astrbot`。之后改 main.py 会自动重建 class 实例，但**子模块仍要手动 restart**（Python `import` 缓存）。**生产前关掉** — 开发期 reload 频率高时撞 15min 轮询点会触发 session-closed traceback（详见 astrbot-plugin-development SKILL "Plugin reload 与 cron 触发撞点的 race" pitfall）。

**dashboard API 手动 reload 单个插件**（需要鉴权）：
```
POST http://localhost:6185/api/plugins/reload
Header: Authorization: Bearer <dashboard token>
Body: {"name": "astrbot_plugin_xxx"}  # 用 metadata.yaml 里的 name 字段
```
等价于 `sudo systemctl restart astrbot` 但只动一个插件，代价是 plugin scope 鉴权；token 在 `data_v4.db` 表 `api_keys` 里查 key_hash 不便，可改 system unit 加 `Environment="ASTRBOT_RELOAD=1"` 走 watcher 路线。

### 3.6 fork → 上游 PR 的 CI 必坑（plugin-dev 也讲，2026-07-10 实测）

适用：自己有 fork (`publieople/<repo>`)，改完 PR 回上游 (`<upstream-owner>/<repo>`)。

**push 前自检（一次性跑完避免多轮 force-push）**：
```bash
cd ~/astrbot_plugin_bangumi
uvx ruff check . && uvx ruff format --check .   # 失败 → uvx ruff format . + commit amend
uvx --with mypy --with types-PyYAML mypy src main.py
uvx --with pyyaml --with pytest python -m pytest tests/test_project_manifest.py -q
git status --short                                # M 必须 add+amend, ?? 允许
git push --force-with-lease origin feat/xxx
```

**CI 失败三件套**：
1. **`ruff format --check .` 报 Would reformat** — 本地 `uvx ruff format .` 后再 amend + force-push。坑：force-push 后**还要再 amend 一次**才能把 working tree 的格式化 diff add 进去（amend 经常漏掉 working tree 改动）
2. **pytest 红灯 + test 写死旧值** — 修复代码时同步改 dead test（`tests/app/test_subscription_service.py:176` 写死 `aiocqhttp:group:group` 这种）
3. **`tests/test_project_manifest.py` 报新命令未在 README 登记** — 用 AST 扫 main.py 的 `@command`，要求 README.md 指令表登记

**完整 PR 提交 + force-push amend + 等 CI 循环**详见 `references/bangumi-plugin.md` §5.3。

### 4. 人格切换不生效
症状：WebUI 切了人格但群内语气未变。
原因：`self_learning` 动态覆盖了选择。查看日志确认实际人格。

### 5. B站 API 412 — aiohttp TLS 指纹被拦截 / IP 风控

B站风控会检测 HTTP 客户端 TLS 指纹或封禁出口 IP。`aiohttp`（以及 Python `urllib`、`requests`）的 TLS 指纹与原生 `curl` 不同，导致搜索/用户信息等 API 返回 412 + HTML 风控页，即使 cookies 有效。

**症状**：
```
[Plug] [WARN] [BiliVideo/HTTP] HTTP GET https://api.bilibili.com/x/web-interface/search/type attempt 1 failed: bad JSON from ...
```
日志显示 `bad JSON`（API 返回 HTML 而非 JSON），但用 `curl` 带相同 cookies 能正常返回 JSON。

**诊断**：
```bash
curl -s --cookie "SESSDATA=xxx; bili_jct=xxx" \
  "https://api.bilibili.com/x/web-interface/search/type?page=1&search_type=bili_user&keyword=test" \
  | head -c 200
```
如果 curl 返回 JSON（`{"code":0,...}`）而插件报错，就是 TLS 指纹问题。

**解决方案（按优先级）**：

1. **切换 Clash 节点换 IP** — B站搜索 API `search/type` 经常被整个出口 IP 封禁。切节点可能绕过
2. **重新扫码登录** — 新 buvid3 能暂时绕过风控
3. **将搜索端点从 `search/type` 换到 `search/all/v2`** — 实测 `search/all/v2` 风控力度更低
   - 两个 endpoint 要一起换：`ENDPOINT_SEARCH_TYPE` 和 `ENDPOINT_SEARCH_TYPE_WBI`
   - 新端点返回格式不同：`data.result` 是分类的结果列表（`[{"result_type":"bili_user","data":[...]}]`），不是直接的用户列表
   - 需要改响应解析：遍历 `data.result` 找到 `result_type == "bili_user"` 的 sect，取 `sect.data`
   - 去掉 `search_type=bili_user` 参数（新端点不需要过滤参数）
   - 如果 aiohttp 仍被拦截，Python 插件中用 `subprocess.run(["curl", ...])` + `urllib.parse.quote()` 兜底（curl 的 TLS 指纹不被 B站拦截）。注意 `import urllib.parse` 不要只写 `import urllib`，否则 `urllib.parse.quote()` 会抛 `NameError`
   4. **curl_cffi 在 WSL 上不稳定**，不推荐
5. **终极方案** — 改用 RSS 轮询+OpenCC 订阅而非 B站 API 搜索

**5. openpyxl 兼容性**
Python 3.12+/3.14 上 `Fill()` 报错。用 zipfile + xml.etree 直接解析 xlsx。

**6. STT 语音转文字（Whisper 自托管）**

详见 [references/stt-whisper-setup.md](references/stt-whisper-setup.md)。

典型故障：WebUI 测试显示 "Provider xxx not found" → `openai-whisper` 未安装在 AstrBot 的
Python 环境。provider 源码顶部 `import whisper` 失败时静默跳过注册，日志无报错。

诊断：
```bash
~/.local/share/uv/tools/astrbot/bin/python3 -c "import whisper"
```

修复（**用 AstrBot 工具自身的 pip**，不要用 `uv pip install --python`）：
```bash
unset PYTHONPATH
~/.local/share/uv/tools/astrbot/bin/python3 -m pip install openai-whisper \
  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

⚠️ `uv pip install --python <path>` 会把包装到 uv 的内部 CPython base
（`~/.local/share/uv/python/`），不进入工具的 site-packages
（`~/.local/share/uv/tools/astrbot/`）。运行时 `import whisper` 仍会失败。

torch 约 532MB，网络慢时用清华镜像 + 600s 超时。安装后需 `sudo systemctl restart astrbot`。
日志应有 `下载或者加载 Whisper 模型中` + `Whisper 模型加载完成。device=...`。

**⚠️ `device=cpu` 陷阱：** `whisper_device: "cuda"` 配置后，日志可能出现
`device=cpu`。这是 `_resolve_device()` 源码只处理 `mps`/`cpu`，"cuda" 被归类为
未知值回退到 CPU。见 reference 中的 patch workaround。

**7. TTS 语音合成（本地 GPU 模式）**

详见 references/indextts-setup.md 和 references/cosyvoice2-setup.md。

**部署原则**：
- TTS 模型以**独立 FastAPI 服务**运行，AstrBot 插件只做 HTTP 客户端
- 模型依赖复杂时，优先用 Docker 或 conda，不要死磕 uv/pip 环境
- 遇到依赖卡住时，**先评估替代方案的总成本**（换模型、换部署方式），不要在一棵树上反复试

**8. 升级后 dashboard 交互提示**

v4.25→v4.26 升级后，首次 `astrbot run` 可能弹出 `Install dashboard? [Y/n]:` 交互式提示。
systemd 环境下无法交互，导致反复崩溃（`auto-restart` 死循环）。

修复：先手动跑一次 `echo "y" | astrbot run` 让 dashboard 装完，然后 `sudo systemctl restart astrbot`。

## TTS 语音合成提供商配置

AstrBot WebUI 内置多个 TTS 提供商。选型前**先查文档/源代码**，不凭记忆猜 API。

### 内置提供商速查

| 提供商 | 本地/API | 日语 | 声音克隆 | 费用 | 适用场景 |
|--------|---------|------|---------|------|---------|
| **GSV TTS(本地)** | 本地 | ✅ | ✅ | 免费 | 7z整合包一键部署，GPU~4GB |
| **FishAudio TTS(API)** | 云端 | ✅ | ✅ | 免费额度 | 零部署，注册就有额度 |
| **Edge TTS** | 免费 | ✅ | ❌ | 免费 | 不需要克隆时首选 |
| **阿里云百炼 TTS(API)** | 云端 | ✅ | ✅ | 免费额度 | CosyVoice/Qwen3-TTS |
| **MiniMax TTS(API)** | 云端 | ✅ | ✅ | 付费 | 商业级 |
| **火山引擎 TTS(API)** | 云端 | ✅ | ✅ | 付费 | 字节跳动模型 |
| **Azure TTS** | 云端 | ✅ | ❌ | 付费 | 微软标准 |
| **ElevenLabs TTS(API)** | 云端 | ✅ | ✅ | 💰贵 | 效果最好但最贵 |

### GSV TTS(本地) — GPT-SoVITS 部署

AstrBot 的 GSV TTS(本地) 连接到 GPT-SoVITS 标准 API（`GET /tts` 端点），默认 `http://127.0.0.1:9880`。

**部署前必须查官方文档**（README + api.py 参数），不凭记忆猜命令。

**Docker 部署（推荐）：** 镜像内置模型，免模型下载和依赖安装。详见 [GPT-SoVITS Docker 部署](references/gpt-sovits-setup.md)。

关键坑：
- 镜像预装模型在 `/workspace/models/pretrained_models/`，但 config 指向的 `GPT_SoVITS/pretrained_models/` 是空目录——需删目录后 `ln -s` 建立软链
- `ref_audio_path` 是容器内路径，用 `-v` 挂载宿主机目录到容器
- Docker compose 有多个 service 定义（含 Lite 版多了 ASR/UVR5 目录挂载），`docker compose up` 会校验全部 service 的 volume 是否存在——用 `docker run` 绕过

**AstrBot 源码路径**（排查参数时查阅）：
```
/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/astrbot/core/provider/sources/gsv_selfhosted_source.py
```

关键配置字段：`api_base`（默认 `http://127.0.0.1:9880`）、`gpt_weights_path`、`sovits_weights_path`、`gsv_default_parms`（传给 `/tts` 的额外参数，键名自动去掉 `gsv_` 前缀）。

### GSV TTS 配置参数详解

AstrBot 的 GSV TTS(本地) 提供商源码路径：
```
/home/po/.local/share/uv/tools/astrbot/lib/python3.12/site-packages/astrbot/core/provider/sources/gsv_selfhosted_source.py
```

**API 端点：** `GET /tts`（标准 GPT-SoVITS API）。

**已知坑：**

1. **`.lower()` 问题**：GSV 提供商会把 `default_params` 的所有值 `str(value).lower()`，所以 `ref_audio_path` 中的路径会被转小写。容器内的路径必须兼容小写，或建立小写软链。
   - 例如：Docker 内实际路径 `/workspace/GPT-SoVITS/reference_audio/xxx.wav`
   - 被 `.lower()` 变成 `/workspace/gpt-sovits/reference_audio/xxx.wav`
   - 解决：容器内 `ln -s /workspace/GPT-SoVITS /workspace/gpt-sovits`

2. **参考音频时长**：GPT-SoVITS API 要求参考音频 3~10 秒。超出会返回 `"Reference audio is outside the 3-10 second range"`。

3. **参考音频文本**：`prompt_text` 越准确，声音克隆效果越好。不确定内容时用 whisper 转写：
   ```bash
   python3 -c "
   import whisper
   m = whisper.load_model('small')
   r = m.transcribe('path/to/audio.wav', language='ja')
   print(r['text'].strip())
   "
   ```

4. **跨语言合成**：日语参考音频 + `text_lang=zh` 可输出中文，反之亦然。GPT-SoVITS 支持跨语言零样本克隆。

**GSV 默认参数（在 WebUI 中填写）：**

```json
{
  "ref_audio_path": "/workspace/gpt-sovits/reference_audio/千早爱音.wav",
  "prompt_text": "あのー、もう始まってる？んっ、じゃあ改めてこんにちは、アノンです",
  "prompt_lang": "ja",
  "text_lang": "zh",
  "text_split_method": "cut0",
  "media_type": "wav"
}
```

**注意：** 参数字段在 WebUI 中显示为带 `gsv_` 前缀（如 `gsv_ref_audio_path`），但源码中会自动去掉前缀。填不带前缀的键名。

### GSV TTS 上下文配置项说明

| WebUI 显示字段 | 实际 key | 说明 |
|--------------|---------|------|
| 参考音频文件路径 | `ref_audio_path` | 容器内绝对路径（会被 `.lower()`） |
| 参考音频文本 | `prompt_text` | 参考音频的台词内容 |
| 参考音频文本语言 | `prompt_lang` | `zh` / `ja` / `en` |
| 文本语言 | `text_lang` | 要合成的输出语言 |
| 切分文本的方法 | `text_split_method` | `cut0` 不切（短句用）|
| 输出媒体的类型 | `media_type` | `wav` / `ogg` / `aac` |
| 语音播放速度 | `speed_factor` | 1.0 = 原速 |
| 生成语音的多样性 | `top_k` | 默认 15 |
| 核采样的阈值 | `top_p` | 默认 1 |
| 生成语音的随机性 | `temperature` | 默认 1 |

### 部署前查文档铁律

**用户对此要求严格：任何不熟悉的工具/框架/部署流程，必须先查阅官方文档再给用户命令。**

这是用户在对话中多次纠正的行为（"你查一下文档再说"、"你看完完整文档再说"）。正确的流程：

1. 用户问「怎么配置X」→ 先找 X 的官方文档/README → 理解后再给出步骤
2. **不要凭记忆或猜测**写配置文件路径、API 参数、命令行参数
3. 不确定的直接查文档或 man page，不要"我觉得应该是这样"
4. 如果文档不完整，先读源码确认

### 本地 TTS 部署原则

- 模型以独立 FastAPI 服务运行，AstrBot 插件只做 HTTP 客户端
- 依赖复杂时优先 Docker 或 conda，不在 venv/pip 上死磕
- 遇依赖卡住先评估替代方案——换模型/换部署方式比修依赖更快
- 网络慢时用镜像（`pypi.tuna.tsinghua.edu.cn`）+ 设 `UV_HTTP_TIMEOUT=300`
- WSL 的 PYTHONPATH 污染全局，启动任何 Python 前 `unset PYTHONPATH`

## 插件页面（Plugin Pages）开发

AstrBot 支持在 WebUI 中内嵌自定义页面。HTML 文件放入 `pages/<page_name>/index.html`，WebUI 自动扫描。

**开发铁律：先读官方文档 https://docs.astrbot.app/dev/star/guides/plugin-pages.html，不猜 API。**

### API 存在的坑

以下 API 在 v4.x 中**不存在**，不要用：
- `filter.on_message()` — 用 `@filter.event_message_type(EventMessageType.ALL)` 代替
- `filter.on_llm_response()` — 不存在
- `EventMessageType` 的导入路径：`from astrbot.api.event.filter import EventMessageType`，不是 `astrbot.api.event`
- 语音消息没有独立事件类型，通过检查 `message_obj.message` 中的 `Record` component 识别
- 新增 `pages/` 目录后必须**重启 AstrBot**（热重载扫描不到新目录）
- 插件页面在 iframe 中运行，不支持文件上传

### 注册 Web API 的正确格式

`register_web_api` 的 route 参数格式是 `f"/{PLUGIN_NAME}/endpoint"`，**不是** `/plugin-page/{PLUGIN_NAME}/xxx`。

```python
from astrbot.api.web import json_response, error_response, request
PLUGIN_NAME = "astrbot_plugin_xxx"
context.register_web_api(f"/{PLUGIN_NAME}/voices", handler, ["GET"], "List")
# request.query.get("limit", 20, type=int)  — query 参数
# await request.json(default={})             — POST body
# json_response({"data": ...}) / error_response("message")
```

前端（`pages/xxx/index.html`）用 bridge SDK：
```javascript
const bridge = window.AstrBotPluginPage;  // 自动注入，no import needed
const data = await bridge.apiGet("endpoint", { limit: 20 });
const result = await bridge.apiPost("endpoint", { key: "val" });
```

**注意**：Bridge 侧的 endpoint **不带插件名前缀**——bridge 自动加。后端注册了 `/{PLUGIN_NAME}/voices`，前端调 `bridge.apiGet("voices")`。