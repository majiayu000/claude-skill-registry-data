---
name: coze-file-send
description: '在 Coze 聊天里需要把文件、图片、截图、图表、PDF、报告或任何可视化/二进制产物送达用户时使用——本地文件 (你刚生成的) 和群文件 (你从 `coze agent` 拿到群文件路径的) 两种来源都走这个技能。聊天默认纯文本, 生成的文件不会自动送达用户。触发: 用户明说要看 ("把图发我"、"send me the chart"); 隐式产出 (你刚生成 plot.png 用户在等结果); 主动展示 (做完该让用户看到的文件); 群文件转发 (你通过 `coze agent` 命令上传/获取到群文件路径后)。不适用于: 纯文本回答、短代码块、大于 50MB 的本地文件。'
---

# coze-file-send: 把文件 / 图片发给用户

你跟用户在 coze 平台聊天, 对话默认纯文本。生成的**图片 / PDF / 报告 / 图表**等文件用户**不会自动看到** — 必须用 `coze-bridge send` 主动发, 用户才能在聊天界面看到。

## 先决条件: 从 `<coze-context>` 提取身份 ID

**每条用户消息开头**云端会注入一段身份上下文块。Coze 有两种聊天形态, 上下文块格式不同:

**单聊消息**:
```
<coze-context>
单聊消息
account_id: 7639...001
agent_id: 7639...571
session_id: 7639...999
</coze-context>
```

**群聊消息** (多了 `group_id`):
```
<coze-context>
群聊消息
account_id: 7639...001
agent_id: 7639...571
session_id: 7639...999
group_id: 7639...888
</coze-context>
```

调 `coze-bridge send` 时**必须**用 `--agent-id` 和 `--session-id` flag 把对应 ID 带上。命令无状态, 每次调用都要带, 不带会 exit 4。

## 两种模式: 决策树

```
你要发的文件在哪里?
├─ 本地 (你刚生成 / cp 来的) → 模式 A (本地文件)
└─ 已在群文件里 (你从 coze agent 拿到 path) → 模式 B (群文件)
                                                 需要群聊上下文, 单聊场景没有这种 path
```

**关键差异**:

| 维度 | 模式 A: 本地文件 | 模式 B: 群文件 |
|---|---|---|
| 适用场景 | 单聊 / 群聊均可 | **仅群聊** (需要 group_id 来源) |
| `<path>` 含义 | 本地文件路径 | 群文件路径 (原样透传) |
| 是否上传 | 是 (走 HTTP API) | 否 (直接 WS 通知 IM) |
| `--mime` | 自动探测 (忽略) | **必填** |
| 大小限制 | ≤ 50MB | 无 (云端管) |

## 命令调用规范

**永远用固定路径** `~/.coze/bridge/bin/coze-bridge` 调用 CLI, 不要用裸 `coze-bridge` — 不同 framework 的 bash tool 继承 PATH 不一致, 裸命令可能 exit 127。固定路径是 daemon 启动时一定写好的 shim, 跨 framework / 跨平台都解析得到。

(注: 这里指 CLI 二进制本身的路径; 传给 CLI 的文件 `<path>` 参数另说, 见各模式。)

---

## 模式 A: 本地文件 (单聊 / 群聊都可用)

```bash
# 图片
~/.coze/bridge/bin/coze-bridge send image <localPath> \
  --agent-id <agent_id> --session-id <session_id> \
  [--caption "说明文字"]

# 通用文件
~/.coze/bridge/bin/coze-bridge send file <localPath> \
  --agent-id <agent_id> --session-id <session_id> \
  [--caption "..."] [--name "report.pdf"]
```

参数:
- `image`: 图片 (png / jpeg / webp / gif), 聊天界面直接渲染
- `file`: 通用文件 (pdf / text / markdown 等), 显示为附件
- `<localPath>`: 本地文件路径 (相对当前目录或绝对路径)
- `--agent-id` / `--session-id`: 从 `<coze-context>` 抄过来 (**必填**)
- `--caption`: 一行说明 (可选, 但**强烈推荐** — 用户体验好十倍)
- `--name`: 用户看到的文件名 (默认从 path 取 basename)

**典型用法**:

生成 + 发 (必须 `&&` 串行 — 文件没写完时 send 会读到残缺):
```bash
python3 plot.py && ~/.coze/bridge/bin/coze-bridge send image plot.png \
  --agent-id <agent_id> --session-id <session_id> \
  --caption "训练曲线 (epoch 1-100)"
```

批量发 (同一 turn 内 ID 不变):
```bash
A=<agent_id>; S=<session_id>
for f in chart1.png chart2.png chart3.png; do
  ~/.coze/bridge/bin/coze-bridge send image "$f" --agent-id "$A" --session-id "$S" --caption "$f"
done
```

生成 PDF + 发:
```bash
pandoc report.md -o report.pdf && ~/.coze/bridge/bin/coze-bridge send file report.pdf \
  --agent-id <agent_id> --session-id <session_id> \
  --caption "本周报告"
```

---

## 模式 B: 群文件 (仅群聊可用)

**触发**: 你用 `coze agent` 命令把文件**上传**到群里 (拿到群文件 path), 或从群里**获取**到一个已有的群文件 path, 现在要把它发给当前用户看。文件已在云端, 你**不需要重新上传**, 直接透传即可。

**前提**: `<coze-context>` 是**群聊消息** (有 `group_id`)。单聊场景下你不会有群文件 path, 用不到本模式。

```bash
~/.coze/bridge/bin/coze-bridge send file <groupFilePath> \
  --agent-id <agent_id> --session-id <session_id> \
  --group-file --mime <mimeType> \
  [--name "..."] [--caption "..."]
```

参数:
- `<groupFilePath>`: 群文件**绝对路径** (`/` 开头; 从 `coze agent file write/upload` 或 `coze agent file list/read` 输出拿来, **原样填**——返回的路径已经是 `/` 开头的)
- `--group-file`: 群文件模式开关 (**必填**)
- `--mime`: mime 类型 (**必填** — 云端没有本地文件可探, 必须显式)
  - 常见: `application/pdf`, `image/png`, `image/jpeg`, `text/markdown`, `text/plain`
- `--name`: 用户看到的文件名 (默认取 path basename; 群文件场景**强烈建议**显式给个可读名字)

> **path 来源限制**: 群文件 path **只**能来自 `coze agent ...` 命令输出。**不要**自己编, 也不要把网上找的 URL 当群文件 path — 云端找不到对应资源会失败。

**典型用法**:

```bash
# 你刚 coze agent file write 改了群文件, 转发给用户
~/.coze/bridge/bin/coze-bridge send file "/本周周报.md" \
  --agent-id <agent_id> --session-id <session_id> \
  --group-file --mime text/markdown \
  --name "本周周报.md" --caption "已按你的要求更新"
```

> 群文件协作产出 → 让用户看到的完整衔接 pattern 见 coze-project 技能的"协作产出"一节。

**何时不该用 `--group-file`**:
- 你自己刚生成的本地文件 → 用**模式 A**, 让 Bridge 上传
- 你只有本地路径, 不知道云端 path → 用**模式 A**
- 网上随手下载的链接 → 先下到本地, 再用**模式 A** 走上传

---

## 何时该触发 (适用于两种模式)

| 场景 | 例子 | 模式 |
|---|---|---|
| 用户明说要看 | "show me", "send me", "把图发我", "可以给我看吗" | A 或 B |
| 用户问结果, 你刚生成了文件 | 用户问"训练效果怎么样", 你跑了 matplotlib 出了 plot.png | A |
| PDF / 报告 / 导出任务 | 用户说"出个周报", 你 pandoc 出了 report.pdf | A |
| 截图 / OCR / 图像处理 | 你截了图 / 做了图像处理 | A |
| 数据分析可视化 | 你画了 chart | A |
| 群文件协作产出 | 你 `coze agent` 改了群文件, 用户在等结果 | B |
| 任何"做完应该展示给用户"的文件 | 用户的隐式期望 — 不要等 ta 问 | A 或 B |

⚠️ **生成文件 ≠ 送达用户** — 必须显式 `coze-bridge send`, 否则用户看不到。

## 何时不该触发

- 纯文本回答 (直接说就行)
- 短代码块 / 命令输出 (markdown 代码块够了)
- 大于 50MB 的本地文件 (模式 A 会被拒; 模式 B 不受此限)
- 你只有想象出来的"path 字符串", 没真上传/改过 (模式 B 会失败)

## 退出码

| 退出码 | 含义 | 你的动作 |
|---|---|---|
| 0 | 成功送达用户 | 简短报告"已发送 `<name>`"给用户即可 |
| 3 | 文件 / 路径 / 格式问题, 或 `--group-file` 缺 `--mime` | 看 stderr, 换路径 / 转格式 / 补 `--mime` 后重试 |
| 4 | 环境问题 (缺 flag / daemon 没起 / 鉴权失败) | 看 stderr; 如果是缺 flag 自查 `<coze-context>` 重新抄 ID 再发 |
| 5 | 网络 / 上传失败 | 重试 1 次; 仍失败告诉用户"上传失败, 稍后再试" |

stderr 的错误信息可以直接转给用户, 不要硬翻译。

## 常见错误 + 修法

**`missing --agent-id and/or --session-id`** (exit 4): 没从 `<coze-context>` 抄 ID。重新看本 turn 用户消息开头的 `<coze-context>` 块, 把 agent_id / session_id 原样填到 flag 里。

**`coze-bridge daemon not running`** (exit 4): daemon 挂了, 你重试也修不了, 告诉用户"暂时无法发送文件"。

**文件路径不对** (模式 A): 把文件先 `cp` 到当前目录, 用相对路径 `./foo.png`。

**文件 > 50MB** (模式 A):
- 图片压缩: `magick convert input.png -resize 50% output.png`
- PDF 压缩: `gs -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -sDEVICE=pdfwrite -o out.pdf in.pdf`
- 拆分多次发
- 真发不了告诉用户"文件太大, 当前支持 50MB 以内"

**格式不支持**:
- 转格式: `.svg` → `.png` (用 ImageMagick); `.docx` → `.pdf` (`libreoffice --headless --convert-to pdf`)
- 如果是 PDF 但用了 `send image`, 改成 `send file`

**上传失败** (模式 A): 重试 1 次 (网络瞬断常见); 仍失败告诉用户稍后再试

**`--group-file requires --mime`** (exit 3): 模式 B 下 mime 必须显式给, 加 `--mime application/pdf` / `--mime image/png` 等。

**`path is not a regular file`** (exit 3, 模式 A 误用): 你拿了群文件 path 但走了模式 A → daemon 把字符串当本地路径 stat 失败。修法: 改用模式 B, 加 `--group-file --mime <m>`。

**模式 B 找不到云端资源**: 把本地真实文件当群文件发 → 云端按"群文件引用"路由, 查不到不存在的资源失败。修法: 本地文件走**模式 A**, 让 Bridge 帮你上传。

## 不要做的事

- ❌ **不要忘记带 `--agent-id` / `--session-id`** — 命令无状态, 每次都要从 `<coze-context>` 抄
- ❌ **不要自己编 agent_id / session_id** — 只能用 `<coze-context>` 里云端下发的值
- ❌ **不要把 acpSessionId / 本地 session ID 当 `--session-id`** — 必须用 `<coze-context>` 里那个云端下发的 session_id
- ❌ **不要 inline base64 长图到对话里** — 用户聊天界面看不到 base64, 全是乱码
- ❌ **不要把绝对路径贴给用户** — 用户没办法访问你的文件
- ❌ **不要后台 spawn (`&`) 跟 send 串** — 文件还没写完时 send 会读到残缺
- ❌ **不要在生成命令报错时还发文件** — 检查 `&&` 是否能跑到 send
- ❌ **不要把群文件 path 当本地路径走模式 A** — 必须用模式 B + `--group-file --mime`
- ❌ **不要把本地文件走模式 B** — 群文件模式跳过上传, 云端找不到
- ❌ **不要在单聊场景下走模式 B** — 单聊没有 group_id 来源, 你也不会有群文件 path

## 总结

**核心信号**: 你脑里冒出"用户会想看到这个文件" → 从 `<coze-context>` 抄 agent_id/session_id → 立刻 `coze-bridge send`, 不要等用户主动问。

**两种模式速选**:
- 文件**在你本地** (你刚生成 / cp 进来) → **模式 A**, Bridge 帮你上传
- 文件**在云端群文件里** (你用 `coze agent` 拿到 path) → **模式 B**, `--group-file --mime <m>`, 不上传
