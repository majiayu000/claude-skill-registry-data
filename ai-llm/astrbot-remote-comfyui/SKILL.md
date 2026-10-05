---
name: astrbot-remote-comfyui
description: 将 AstrBot 连接到远程 ComfyUI 服务器 — SSH 隧道、systemd 自启、插件选型、工作流配置
---

# AstrBot → 远程 ComfyUI 集成

## 适用场景

AstrBot 装在 WSL/本地，ComfyUI 在远程服务器（无公网 IP，通过 FRP/SSH 访问）。

**访问路径可换**：FRP / SSH 可换成网易 UU 远程端口映射（TCP-only，经跳板机进内网，省 FRP 流量）。整条迁移 + WSL sshd 换端口 + UU 掉线坑见 `references/uu-remote-tunnel.md`。

## 方案

### 1. SSH 隧道（核心）

```bash
# 测试连通性
ssh -p <port> -o BatchMode=yes -o ConnectTimeout=5 user@host "echo OK"

# 手动启动隧道（-N 不执行命令，-L 端口转发）
ssh -p <port> -N -L 8188:127.0.0.1:8188 user@host
```

### 2. systemd 服务

参照 AstrBot 已有服务的格式：

```ini
[Unit]
Description=SSH Tunnel to ComfyUI Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=po
ExecStart=/usr/bin/ssh -p <port> -N -L 8188:127.0.0.1:8188 \
  -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes user@host
ExecStop=/usr/bin/pkill -f "ssh.*<port>.*8188"
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now comfyui-tunnel
```

前提：SSH 密钥无密码（`BatchMode=yes` 验证）

### 3. AstrBot 插件配置

`server_ip = 127.0.0.1:8188`（指向本地转发端口）

### 4. 插件选型对比

| 插件 | LLM 触发 | 工作流方式 | 评价 |
|------|----------|-----------|------|
| cjxzdzh/astrbot_plugin_comfyui | LLM Tool 调用 | 文件名约定 `工作流名+文本N+图片M+视频K.json` + Simple String 节点 | 架构干净，但需改 ComfyUI 节点 |
| lumingya/astrbot_plugin_comfyui_pro | 正则提取 `<draw>` 标签 | 填 Input/Output 节点 ID | 社区最火，兼容性好 |
| tjc/astrbot_plugin_ComfyUI_promax | 指令前缀 | 预置 SD 工作流 | 功能最全但最重 |

### 5. 坑

- **cg-use-everywhere v7 移除了 Simple String**：需要 pin 到 v6。`git checkout f2a0c34...`（最后一个有 Simple String 的提交）
- **promax 插件只读 `models/checkpoints/`，不认 `diffusion_models/`**：Flux 等新架构模型需要自定义 workflow，插件内置工作流用不了
- **SSH 隧道需要 `ServerAliveInterval`**：否则长时间不用会断开
- **AstrBot 需要重载插件两次 + 刷新浏览器**（插件缓存机制）

### 6. 运维

- 检查隧道状态：`systemctl status comfyui-tunnel`
- 检查 ComfyUI 可达：`curl http://127.0.0.1:8188/system_stats`

### 7. 三个集成路径（plugin vs skill vs 直调）

AstrBot 调 ComfyUI 有三条互不重叠的路径，**先问用户走哪条**：

| 路径 | 落地形式 | 谁执行 curl | LLM 介入方式 | 何时选 |
|---|---|---|---|---|
| **A. AstrBot 插件**（plugin marketplace） | `data/plugins/astrbot_plugin_*/main.py` 注册 LLM tool | 插件 Python | tool 装饰器 + schema（强制） | 用户要现成的、生图成产品功能、跨工作流统一 |
| **B. AstrBot skill**（`data/skills/<slug>/`） | SKILL.md 文档 + 可选 `_meta.json` + 可选 Python | **LLM 自己**照文档 curl | 纯文档型无需 schema | 用户要"LLM 学会去调"，schema 写起来累，工作流少（1-3 个） |
| **C. 直调**：AstrBot 不参与 | 用户手动 `curl /prompt` + 取图 | 人 | 不适用 | 调试用、接口验证 |

**B 是最少配置的路线**：用户已经在 `data/skills/comfyui-anima-t2i/` 维护了一个本地 skill（`_meta.json` + SKILL.md），LLM 读 SKILL.md 直接 curl，**不写 Python、不注册 tool、不写 schema**。LTM tool 的 LLM "skill 模式" 由 AstrBot v4 的 `simple_subplugin` / skill loader 启用，前提是 skill 目录存在合法 `SKILL.md`。

**`_meta.json` schema**（AstrBot 识别 skill 的强依赖）：

```json
{"ownerId": "local", "slug": "comfyui-anima-t2i", "version": "1.0.0", "publishedAt": 1751972400000}
```

四字段缺一不可：缺 `slug` → 加载失败；缺 `version` → WebUI 标红；缺 `publishedAt` → 当成本地暂存（不显示在市场）。

**决策树** — 用户说"加 ComfyUI 能力"或"给 AstrBot 接 ComfyUI"：
1. 先查 `data/skills/` 看有没有现成 skill（`ls data/skills/comfy*`）
2. 有 → 直接复用，**不要**绕去 plugin marketplace
3. 没 → 若工作流固定 1-3 个，写 skill（B 路径）比装插件快 10 倍
4. 工作流多、要产品化功能 → A 路径，挑 `cjxzdzh/astrbot_plugin_comfyui`（架构最干净）或 `WalkerZJH/astrbot_plugin_easy_comfyui`（最简单）

**易错**：
- 用户说"找一下 skill"时不主动跳到 plugin marketplace——"skill"在 AstrBot 生态里特指 `data/skills/` 下的东西，跟 AstrBot Plugin Marketplace（`plugins.astrbot.app`）是两回事
- 跟"Hermes skill 市场"（`~/.hermes/skills/`、`skills.sh`）也**完全不同**——Hermes skill 是给 Hermes Agent 自己用的；AstrBot skill 是给 AstrBot 的 LLM 用的。混淆就闹笑话

### 7.1 复杂 + 演化型工具表面：选 self-evolving skill，绕过插件

**触发条件**（同时满足）：
1. 工具 API/model 频繁变（ComfyUI 加新模型架构、SVN 增新云 API...）
2. 用户嫌"每次有新东西都得重写插件"或"这插件太死板了"
3. 工作流数量有限（1-N 个，每个用户能维护 json 文件），不需要产品级功能

**走法 — 让 skill 自我演化**（not 框架，是约定）：
- 一个主 `SKILL.md`（< 200 行），教 LLM 怎么调用这个工具的**通用范式**（不绑死任何具体工作流/模型）
- 旁边三个数据目录（不在 skill 内，在 AstrBot 数据根）：

```
data/<slug>_workflows/<name>/       # 用户维护:workflow_api.json + README.md
data/<slug>_eval/<workflow>.md      # 回归 prompt 集,每个工作流 3-5 条
data/<slug>_journal/YYYY-MM-DD-N.md # LLM 每次跑完追加:prompt + 选择 + 结果 + 学到的
```

- 演化触发写入 SKILL.md：journal ≥ 5 条 / 同类失败 ≥ 2 次 / 用户显式吐槽
- 演化流程：LLM 自反思 → 提 patch（add/delete/replace 三种，少于 SKILL.md 20%）→ 在 eval 上回归 → 涨分落地，不涨拒绝
- 受 SkillOpt 启发，但**不装 SkillOpt 框架**：没有 trainer、没有 schema、没有 optimizer backend 抽象——LLM 自己就是 optimizer

**为什么不是 plugin**：
- plugin 写完就冻结；新模型要 fork、重写、发布
- plugin 的 `@llm_tool` 装饰器每个 tool 写一次 schema，工具多起来成本爆炸
- plugin 路径把 LLM 决策权偷走（每条 tool 是固定签名），skill 路径让 LLM 自己挑工作流、自己决定参数

**详细 recipe**：`references/skill-self-evolve-pattern.md`（ComfyUI 是第一个案例，模式可迁移到任何"AI 调外部工具"的场景——AstrBot 学 Git CLI、ffmpeg pipeline、SQL、任意外部 SaaS API）

**写 SKILL.md 时的 5 个坑**(jq 不在 PATH、SaveImage 节点别硬编码、polling history 500 兜底、object_info 常空、`POST /prompt` 的 number 队列位): `references/comfyui-skill-md-pitfalls.md`,端到端第一次跑通时撞到,下次写同类 SKILL.md 先看。

**反例**：用户说"我要一个能让我朋友也装的生图插件、跨 QQ 群都用"——这种要走 A 路径 plugin + 发布到 marketplace，self-evolve skill 是私人的，不能给别人用

### 8. 故障排查：图生成成功但效果不对 / "不接提示词"

用户报错"插件不接提示词"时，**90% 的排查时间应花在"到底是哪一截挂了"**。三个怀疑对象，按从服务端 → 客户端顺序排除：

**A. ComfyUI 服务端（先排除）**

```bash
# 1. 服务活没活
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8188/

# 2. 模型/工作流节点实际跑过没
ssh -i ~/.ssh/id_ed25519 -p <port> user@host \
  "sudo -n journalctl -u comfyui -n 100 --no-pager"

# 看到 "got prompt" + "Prompt executed in N seconds" = 服务端正常。
# 看到 "ValueError" / "KeyError" = 工作流/节点配置问题。
```

**关键诊断接口：`/history/{prompt_id}`** — 返回**完整** prompt JSON（包括用户输入的 text 节点值），不像 `/history` 列表那样被 truncation。

```bash
# 取最新一条 prompt_id
PID=$(curl -s "http://127.0.0.1:8188/history?max_items=1" | \
      python3 -c "import sys,json; print(list(json.load(sys.stdin).keys())[0])")
curl -s "http://127.0.0.1:8188/history/$PID" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); pj=d[list(d.keys())[0]]['prompt'][2]; print(json.dumps(pj, indent=2, ensure_ascii=False))"
```

看到 node `11` (CLIPTextEncode) 的 `inputs.text` 字段是**用户实际输入的中文**（或翻译后的英文），**就证明 promax 端正确传过去了**。这步把"提示词没到 ComfyUI"的可能性直接排除。

**B. AstrBot 端：plugin 配置位置（v4）**

AstrBot v4 的 plugin 配置文件**不在** `data/plugins/<plugin>/config.json`，在：

```
/home/po/astrbot/data/config/astrbot_plugin_<plugin>_config.json
```

**常见 promax 配置坑**：

| 配置项 | 默认 | 坑 |
|--------|------|-----|
| `enable_translation` | `false` | **关闭时中文 prompt 直接喂给 Qwen3 0.6B**，会出图但内容不达预期（Anima 等日漫风格必须用英文 Danbooru 标签） |
| `enable_fake_forward` | `true` | 配 `fake_forward_qq=""` 时转发失效，图可能没发到群 |
| `enable_auto_recall` | `false` | 配 true 的话图发出去 N 秒后撤回，用户没看到 |
| `daily_download_limit` | `1` | 用户一天超限后任务静默丢弃 |
| `group_whitelist` | `[]` | 空数组 = 全部拒绝，插件不会响应 |

**修法**：先用 `enable_translation: true` 让 promax 调 LLM 翻中文 → Danbooru 标签；或让用户**直接发英文 Danbooru 标签**（Anima 出图质量最高）。

**C. 客户端：日志死路**

AstrBot v4 默认 `log_file_enable: false`。systemd 拉起时 stdout 进 socket / journalctl，**`data/astrbot.log` 不会更新**——里面是几个月前的尸体日志。

```bash
# 即时查日志（推荐）
journalctl --user -u astrbot -f

# 或开文件日志
# /home/po/.config/systemd/user/astrbot.service 加上:
# StandardOutput=append:/home/po/astrbot/data/astrbot.log
# StandardError=append:/home/po/astrbot/data/astrbot.log
# 然后 daemon-reload + restart
```

**D. 提示词注入路径（promax workflow 模式）**

读懂 `_inject_user_params` / `build_workflow`（`workflow_engine.py:1202-1243`）：

- 节点参数按 `node_id:param_name` 格式（如 `11:text`）查表
- 用户消息中没有 `xxx:yyy` 模式的部分 → 走 LLM 翻译 → 注入到 `text` 节点
- 所以 `anima 抽烟的白毛猫娘` → 翻译成 Danbooru → 注入 node 11 的 text 字段

**参考**：`references/comfyui-diagnostics.md` 收录了完整的"问题在 ComfyUI 还是 AstrBot"诊断 recipe 和具体错误样例。`references/skill-vs-plugin-discovery.md` 收录三条集成路径的识别口诀、AstrBot skill 合规最小公约数、以及从废插件迁 skill 的最小步骤。
