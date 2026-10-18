---
name: kling-cli
version: 0.2.1
description: >-
  可灵 AI（Kling）官方 CLI 的使用技能：图片/视频生成、可复用 Element 主体、动作控制。CLI 通过 MCP 服务与可灵交互：
  调用 text_to_image / image_to_image / text_to_video / image_to_video / omni_ref_video / motion_control（模型与参数规格由 who_am_i 动态声明），
  返回 generationId 后用 query_tasks 轮询，完成后提取 works[].url 展示给用户。命令无别名。
  触发词：可灵、Kling、文生图、参考图生图、文生视频、图生视频、Omni、omni、MCP、generationId、generation_id、轮询、灵感值、
  text_to_image、image_to_image、text_to_video、image_to_video、omni_ref_video、全能参考、关键帧、motion_control、motion_library_list、Element、element_create、element_list、element_get、element_update、element_delete、feedback、query_tasks、who_am_i、file_upload、
  image generation、video generation、kling 命令、.credentials、
  国内站、海外站、global、海外版、区域、region、安装、install。
requires: node>=18
# 可灵分中国区 / 非中国区，官网不同；skill 区域中立，按用户区域引用对应主页
homepage_cn: https://klingai.com
homepage_global: https://kling.ai
---

# 可灵 AI 官方图片/视频生成、Element 主体与动作控制

## 语言与回复风格

- 面向用户的解释、确认、错误说明：**跟随用户语言**（中文用户用中文回复，英文用户用英文回复）。
- 技术字段名（`generationId`、`status`、`works[].url` 等）保留英文原样。**响应字段统一 camelCase**（如 `generationId` / `creditsConsumed` / `urlWithoutWatermark`）；旧版服务端可能仍返回 snake_case 同义字段（`generation_id` 等），按同一字段理解即可。

---

## 能力介绍（固定欢迎语，按需展示）

**触发时机**（满足任一即展示，纯本地、不调用命令、不扣费）：

1. 用户刚完成本 skill 或 CLI 的安装/登录，环境确认可用时；
2. 用户询问可灵能做什么 / 有哪些能力 / 怎么用等**能力咨询类**意图（没有具体生成任务）时。

**展示要求**（保留结构与 emoji，不增删条目、不自行改写含义）：

- **中文用户**：原样输出中文版。
- **非中文用户**：**必须翻译，不得输出中文版**——优先以英文版为底稿翻译成用户语言（日语用户给日语、西语用户给西语等，示例引语一并翻译）；无法可靠翻译的语种**至少原样输出英文版**。
- 若环境尚未就绪（未安装 CLI 或未登录），把首行「可灵已就绪！/ Kling is ready!」换成对应语言的引导语（如「可灵还差一步就绪」/ "Kling is one step away"），并在文案后给出安装/登录下一步。

中文版：

```text
可灵已就绪！

你可以用可灵做这些事：

📷 生成图片
   · 文生图 — "帮我画一只赛博朋克风格的猫"
   · 参考图生图 — "用这张图做参考，改成水彩风格"

🎬 生成视频
   · 文生视频 — "生成一段日落海边的 5 秒视频"
   · 图生视频 — "让这张图动起来"

🧩 可复用主体 — 创建和管理角色、动物、道具等 Element
🎭 动作控制 — 用动作视频或动作库驱动主体图片

📤 上传素材 — 本地图片可直接传，自动上传到可灵

也可以结合 agent 及 skill 能力去实现一些复杂的创作流程。比如做个广告片、故事短片、批量创作一批素材等。
```

英文版（非中文用户的翻译底稿；英文用户直接原样输出此版）：

```text
Kling is ready!

Here's what you can do with Kling:

📷 Generate images
   · Text to image — "Draw me a cyberpunk-style cat"
   · Image to image — "Use this image as a reference and restyle it in watercolor"

🎬 Generate videos
   · Text to video — "Generate a 5-second video of a sunset over the sea"
   · Image to video — "Bring this image to life"

🧩 Reusable subjects — create and manage character, animal, prop, and other Elements
🎭 Motion control — drive a subject image with a motion video or saved motion

📤 Upload assets — local images work out of the box and are uploaded to Kling automatically

You can also combine agent and skill capabilities to build more complex creative workflows — like making an ad spot, a short story film, or batch-producing a set of assets.
```

> 展示欢迎语本身不需要调用任何 `kling` 命令；若用户接着要精确的模型/参数清单，再走 `who_am_i`。

---

## 安装与登录（唯一合法方式）

> **可灵分「国内站」与「海外站」，对应两个不同的安装包，端点已各自内置。装错区域的包会导致登录反复失败，因此装包前必须先确认用户属于哪个区域。**

### 第 0 步：探测是否已安装

```bash
which kling   # 有输出路径 → 检查版本；未找到 → 进入第 1 步按区域安装
kling --version   # 本 skill 的完整能力要求 CLI >= 0.2.1
```

已安装版本低于 `0.2.1` 时，按已有账号区域升级对应 npm 包后再使用新功能；用户已明确要求升级时直接执行，无需重复确认。CLI 与 skill 分别分发，仅更新 skill 不会升级 CLI。

`0.2.1` 已移除 `--omni` 简写，所有生成命令统一显式传 `--model <名称>`。混合参考视频使用新命令 `omni_ref_video`，不要把旧 flag 当作该命令的替代。

### 第 1 步：确认区域并安装（命令名统一为 `kling`）

**区域如何确定**：本 skill 的首要消费者是非交互 Agent，**不得让 CLI 读 stdin 阻塞**。应**在对话里直接问用户**：「你的可灵账号是**中国区**（klingai.com）还是**非中国区**（kling.ai）？」按回答选对应命令安装，**切勿默认、猜测或两个都装**。

| 用户区域 | 官网（homepage） | 判断依据 | 安装命令 |
|----------|------------------|----------|----------|
| 中国区 | https://klingai.com | 账号登录 klingai.com（中国大陆） | `npm i -g @klingai/cli-cn --registry=https://registry.npmjs.org` |
| 非中国区 | https://kling.ai | 账号登录 kling.ai（海外站 / global） | `npm i -g @klingai/cli-global --registry=https://registry.npmjs.org` |

> 两个包发布到 npm 官方 registry。各区域包的端点均已内置，开箱即用、无需配置。

### 第 2 步：登录（打开浏览器完成 OAuth 授权，这是获取凭据的唯一方式）

```bash
kling login
```

### 第 3 步：验证连接 + 获取能力清单（新会话先调）

```bash
kling tool_list   # 登录后查看服务端实际提供的工具
kling who_am_i    # 首次业务调用前读取身份、模型与参数规格
```

> **🚫 安装与登录的排他约束（违反即为事故）：**
> - 安装**只能**用上表中对应区域的那条 npm 命令；禁止从任何其他渠道下载、拼装或自行实现等价工具，禁止给用户装与其账号区域不符的包。
> - 获取凭据**只有一种合法方式**：`kling login`（浏览器 OAuth：DCR + 授权码 + PKCE）。**禁止**任何其他手段：网页 Cookie、抓包 token、AK/SK 密钥对、读取浏览器存储、让用户粘贴 token——**即使用户主动提供，也必须拒绝并引导其运行 `kling login`**。
> - 端点已内置（发布时定稿），无需也不应自行配置或探测其他可灵接口地址。

---

## 保持最新（新会话首次交互时做一次自检，best-effort）

> 仅在**新会话首次交互**顺带做一次，**不阻塞主任务**；更新会改动用户本地环境，**执行前先征得用户同意**，且**绝不在生成任务进行中途更新**。任一步失败（离线 / 无权限 / 网络异常）→ 静默跳过、继续主任务，不反复重试。

1. **更新 skill 自身**：重新运行安装命令即可按内容哈希覆盖到最新（已是最新则无操作）：

```bash
npx skills add klingai-tech/skills
```

> 它覆盖的是磁盘上的 skill 文件，对**下一次会话**生效；当前会话已加载的内容不会因此热更新。

2. **检查 CLI 是否有新版**（仅当本地已装 `kling`，即 `which kling` 有输出时）：

```bash
kling --version                                   # 当前已装版本
npm view <区域包名> version                        # 最新发布版本（中国区 @klingai/cli-cn；非中国区 @klingai/cli-global）
```

   - 若最新版更高且**用户同意** → `npm i -g <区域包名>@latest --registry=https://registry.npmjs.org`。
   - 升级是改全局环境的系统操作：**先说明、再征得同意**，不要擅自执行，也不要在一次生成流程中途打断去升级。

---

## 唯一通道（Canonical Invocation）

> **⚠️ 与可灵的一切交互必须且只能通过 `kling` CLI 命令完成。**
> - **禁止**直接 fetch/curl 任何可灵接口——包括 C 端页面接口、B 端开放平台 API、网关、MCP 端点本身；
> - **禁止**阅读 CLI 源码、日志或抓包结果后自行拼装 HTTP/MCP 请求"绕过" CLI；
> - CLI 报错时唯一正确动作是把错误呈现给用户并询问，**不得**换通道、换接口重试。

```bash
kling <command> [args]
```

人和 Agent 共用同一入口：TTY 下有交互引导，非 TTY 输出 JSON 且绝不阻塞提问。CLI 对鉴权、日志、错误处理做了统一封装。

业务命令与可灵后端 **MCP 工具名 1:1（snake_case）**；客户端命令包括 `login`、`tool_list` 和映射到 `query_membership_and_credits` 的 `account`。共 **20 个命令**，另有帮助和版本选项：

| # | 命令名 | 分组 | 同步性 | 触达下游 | 一句话说明 |
|---|--------|------|--------|----------|------------|
| 1 | `--help`（或不带参数） | 能力发现 | 同步 | 否 | 顶层 `kling --help` 纯本地打印全部命令；`<command> --help` 会尽量拉取该工具实时 `tools/list` 声明（需登录），离线/未登录时回退本地静态用法 |
| 2 | `who_am_i` | 能力发现 | 同步 | 否 | 返回当前用户身份 + 每个生成命令的可用模型与参数规格；**首次调用先打它** |
| 3 | `text_to_image <prompt>` | 生成 | **异步** | 是 | 文生图，返回 `generationId`，需轮询 `query_tasks`（或加 `--poll` 一步出结果） |
| 4 | `image_to_image --image <url\|path> <prompt>` | 生成 | **异步** | 是 | 参考图 + prompt 生新图，返回 `generationId`（本地图片自动上传） |
| 5 | `text_to_video <prompt>` | 生成 | **异步** | 是 | 文生视频，返回 `generationId`，需轮询 `query_tasks` |
| 6 | `image_to_video [--image <url\|path>] [prompt]` | 生成 | **异步** | 是 | 图生视频 / 关键帧；输入与 prompt 必填性依模型声明，返回 `generationId` |
| 7 | `omni_ref_video <prompt>` | 生成 | **异步** | 是 | 混合图片、视频或 Element 参考，类型以模型声明为准，返回 `generationId` |
| 8 | `query_tasks <generationId>` | 任务查询 | 同步 | 是 | 按 `generationId` 查询生成状态与最终资源 URL（`works[].url`） |
| 9 | `file_upload <filePath>` | 文件上传 | 同步 | 是 | 两步式上传（申请一次性票据 + 上传文件字节），返回公网 URL |
| 10 | `element_create` | 主体素材 | 同步 | 是 | 从图片组或视频创建可复用 Element，返回 element id |
| 11 | `element_list` / `element_get` | 主体素材 | 同步 | 是 | 列出 Element；按 id 获取完整类型与资源详情 |
| 12 | `element_update` / `element_delete` | 主体素材 | 同步 | 是 | 按字段更新或删除 Element；图片主图由 CLI 自动保留 |
| 13 | `motion_library_list` | 动作素材 | 同步 | 是 | 列出已保存动作，获得 motionId 与可播放 URL |
| 14 | `motion_control` | 生成 | **异步** | 是 | 用主体图 + 动作视频或 motionId 生成视频，返回 generationId |
| 15 | `feedback` | 反馈 | 同步 | 是 | 上报卡住、模糊错误、计费异常或意外结果；不负责重试/退款/修复 |
| 16 | `account` | 商业化 | 同步 | 是 | 会员类型 + 可用灵感值（`query_membership_and_credits`，身份取自 JWT） |
| 17 | `tool_list` | 能力发现 | 同步 | 否 | 列出后端 MCP server 当前暴露的工具（MCP `tools/list`）：每个工具的 name / description / inputSchema（排障 / 确认服务端实际提供哪些 tools 用） |
| 18 | `login` | 鉴权 | 同步 | 否（仅 OAuth 服务） | 浏览器 OAuth 登录（DCR + PKCE），token 写入本地 `.credentials` |
| 19 | `logout` | 鉴权 | 同步 | 是 | 调用 MCP `logout` 注销服务端授权，并清除本地登录态，以便重新授权或切换账号 |

> **端点已内置**：对应区域包安装后开箱即用、无需配置；**不存在任何外部配置口子**（无环境变量、无 `.env`、无 config 命令），也不要尝试探测或指定其他可灵接口地址。

> **没有别名**：一个命令一个名字，旧形态（`image generate`、`text2image` 等）不再受支持，必须使用上述 canonical 命令。

运行 `kling`（不带参数）或无效子命令时会打印完整 Usage 帮助。

---

## 推荐用法（最佳实践，Agent 须遵循）

> 目标：少试错、不浪费灵感值、参数永远以服务端为准。

> **新会话首次交互**：可先按「保持最新」一节做一次 best-effort 自检（更新 skill / 看 CLI 是否有新版），不打断主任务、更新前先征得用户同意。

**最简三步**：① `kling login` 登录 → ② `kling tool_list` 看工具，`kling who_am_i` 看身份与模型规格 → ③ `kling <command>` 执行（6 个生成命令均必须显式带 `--model`）。

1. **新会话先 `kling who_am_i`**：一次拿到身份 + 每个生成命令的可用模型与参数规格（必填 / 默认值 / 值域）。后续选模型、配参数都以它为准。
2. **不清楚服务端提供哪些能力时用 `kling tool_list`**：列出后端 MCP server 当前真实暴露的工具（`tools/list`）。适合排障、确认某能力是否上线，**需已登录、不扣费**。
3. **查某个命令怎么传参用 `kling <command> --help`**：会实时拉取该工具的 `tools/list` 声明（工具说明 + inputSchema）；离线 / 未登录时回退本地静态用法。完整模型与参数仍以 `who_am_i` 为准。
4. **生成必须显式选模型**：`text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` / `omni_ref_video` / `motion_control` 均必须带 `--model <名称>`（取自对应工具的 `who_am_i` 清单）。**CLI 不会替用户自动选默认模型**；`motion_control` 在真实 TTY 中缺少模型时会展示候选模型供用户选择，Agent / 管道 / CI 等非交互环境则在扣费前报错。
5. **素材直接传本地路径或公网 URL**：按所选命令的帮助传图片、视频或音频素材；本地文件由 CLI 自动 `file_upload`，无需手动上传；**公网 URL（外部 CDN / 外链，或此前可灵任务返回的 `works[].url`）直接透传给服务端，无需先下载、重新上传或本地校验**。素材的格式 / 大小等限制以工具实时声明为准（`kling <command> --help` / `kling tool_list`）。
6. **提交后立即反馈再轮询**：从响应取 `generationId` 与 `creditsConsumed` 先告知用户；再用 `kling query_tasks <generationId>` 轮询，或提交时加 `--poll [N]` 一步出结果（裸 `--poll` 默认 60s，`--poll 0` 关闭内联轮询）。
7. **结果在 `works[].url`**：完成后提取并展示；用户要无水印时用 `works[].urlWithoutWatermark`。
8. **余额 / 会员看 `account`**：余额不足时展示服务端动态返回的充值链接（勿写死）。
9. **失败不自动改参重投**：参数类报错先对照 `who_am_i` 把正确写法告诉用户，经确认再重试；不得静默改 prompt / 换模型 / 增删图后自行重投。

典型顺序：登录后 `tool_list` → `who_am_i` →（按需 `<command> --help`）→ `text_to_*` / `image_to_*` / `omni_ref_video` / `motion_control` 带 `--model` 提交 → `query_tasks` 轮询 → 展示 `works[].url`。

---

## 模型与参数：以 who_am_i 为准（核心心智）

- **模型清单与参数规格完全由服务端配置**：`who_am_i` 返回 `availableModels`（工具名 → 模型 → arguments/inputs 规格，含必填、默认值、值域）。
- **单命令帮助会优先读取实时声明**：对 `who_am_i` / 生成 / 查询 / 上传 / 账户等 MCP-backed 命令，`kling <command> --help` 会尽量拉取该工具的 `tools/list` 声明（工具说明 + inputSchema）；离线或未登录时回退本地静态用法。完整模型清单与参数规格仍以 `who_am_i` 为准。
- 6 个生成命令均须显式传 `--model <名称>`（可用值来自对应工具的 `who_am_i` 清单）。用户指定 Omni / Flash 时也应查清完整模型名；CLI 不会替用户自动选择默认模型。
- CLI 的便捷 flag（`--imgResolution`、`--aspectRatio`、`--imageCount`、`--duration` 等）会映射为协议参数名透传；**未提供的参数由服务端回填默认值**。`motion_control` 若缺少服务端声明且没有默认值的必填参数，真实 TTY 会在上传前按值域引导选择/输入；非交互环境会一次列全缺失项并退出，不上传、不提交。
- **输入按声明映射**：先用命令帮助确认 CLI 写法，再按 `who_am_i` 的 `inputs` 与 `arguments` 核对资源类型、槽位名和必填性；不要假设所有图生入口都必须有首帧，或所有生成命令都允许省略 prompt。使用具名输入时不得重复占用槽位，是否能与便捷 flag 混用以该命令帮助为准。各命令的映射和示例见 [api-examples.md](./api-examples.md)。
- **组合限制也要核对**：宽高比是否跟随输入图、音频参数是否互斥、主体类型是否兼容等，以当前模型与工具说明为准；不能把某个模型的限制推广到整个命令或同系列模型。
- 输入除单类数量外，还可能有 **`combinedItemCap` 合计上限**（跨输入槽位与 `elements` 等数组参数）。`image_to_video` / `omni_ref_video` 会在上传前校验相关槽位、必填输入和合计数量；不要把各类上限相加后当作允许总量。字段见 [reference.md](./reference.md)。
- 参数校验（必填、值域、未声明参数）由服务端在**扣费前**完成，报错信息会列出问题项；遇到参数类报错应把服务端信息翻译给用户。

---

## 意图路由（必选决策表）

| 用户意图 | 命令 | 说明 |
|----------|--------|------|
| 问可灵能做什么 / 有哪些能力（无具体任务） | — | 展示「能力介绍」固定欢迎语（见上），纯本地不调命令 |
| 查可用模型 / 参数规格 / 能力发现 | `who_am_i` | 新会话建议先调 |
| 生成图片 / 出图 / 文生图 | `text_to_image` | 提交后轮询 `query_tasks` |
| 参考图生图 / 带参考图 | `image_to_image` | `--image` 可重复，提交后轮询 |
| 生成视频 / 文生视频 | `text_to_video` | 提交后轮询 |
| 图生视频 / 让图动起来 / 首中尾关键帧 | `image_to_video` | 按模型声明传 `--image` / `--tailImage` 或具名 `--input`；prompt 可选性依模型声明，提交后轮询 |
| 图片、视频、主体混合参考生成视频 | `omni_ref_video` | 暂不支持独立音频参考；prompt 必填，提交后轮询 |
| 创建/列出/查看/更新/删除可复用主体 | `element_create` / `element_list` / `element_get` / `element_update` / `element_delete` | 更新只传变更字段；删除前需用户明确确认 |
| 动作控制 / 动作迁移 | `motion_control` | 主体 `--image` + `--video` 或 `--motionId` 二选一；提交后轮询 |
| 查看已保存动作 | `motion_library_list` | 取 motionId 后可交给 `motion_control` |
| 上报卡住、模糊错误、计费异常、意外结果 | `feedback` | 只反馈，不会重试、退款或修复原任务 |
| 明确要求 Omni / Flash 模型 | 按创作意图选命令，再传完整 `--model` | 从该工具的实时清单中选择；不能使用已移除的 `--omni` |
| 上传本地素材 | `file_upload` | 仅本地文件需要上传（返回公网 URL）；已是公网 URL 的素材无需上传，直接作 `--image` 传给生成命令 |
| 查会员 / 账户身份 / 查余额 | `account` | 返回 userId + membership + 可用灵感值（直接展示） |
| 充值 / 余额不足 / 开通会员 | `account` | 展示服务端返回的充值/会员链接（**动态取自 MCP，勿写死**，见「余额不足与充值」） |
| 登出 / 退出当前账号 | `logout` | MCP 注销成功后清除本地登录态；成功即结束，不自动重新登录 |
| 切换账号 / 换一个账号登录 | `logout` → `login` → `who_am_i` | 必须按顺序执行；`logout` 或 `login` 任一步失败都立即停止；新授权完成后验证账号 |
| 仅说「用可灵生成」等模糊意图 | — | **先问清是图还是视频，再提交** |

> 如果用户意图不明确，**必须先确认再提交**，不得擅自假设。

### 登出与切换账号

- **仅登出**：用户明确要求退出当前账号时，执行 `kling logout`。成功后结束；不得自动触发新的浏览器授权。
- **切换账号**：必须依次执行 `kling logout` → `kling login` → `kling who_am_i`。只有 `logout` 成功后才能继续 `login`；浏览器授权时由用户选择目标账号；登录成功后用 `who_am_i` 展示并确认当前身份。
- **`logout` 失败必须立即停止**：保留本地登录态以便重试，并把原错误告知用户；不得跳过失败直接 `login`。
- **`login` 失败必须立即停止**：报告登录错误，不得继续 `who_am_i`，也不得改用 Cookie、token 粘贴、抓包或其他授权方式。
- **不要用 `login` 代替切换流程**：`login` 只负责本地 OAuth 授权，单独执行不能保证服务端旧授权已注销。用户明确说“切换账号”时必须先走 `logout`。

### Element 主体工作流与兼容约束

1. **创建**：图片 Element 用 `--cover` + 1–3 个 `--secondary`；视频 Element 只用 `--video`，两种资源不可混传。两者都至少带一个 `--tag`，标签必须从当前区域 `element_create` 的实时工具 description 中选择并原样传入；创建和更新都不要按对话语言翻译标签或硬编码某一区域的目录。可选 `.mp3` `--voice`。本地文件自动上传。
2. **绑定前先确认类型与兼容性**：先 `element_list` 找 id，再 `element_get <id>` 看完整 `resource`，并同时核对实时工具 description 的主体类型限制和 `who_am_i` 的模型参数。目标模型必须声明 `elements`；图片主体不能仅因模型名是 `kling-image-o1` 就被拒绝。若模型声明了 `elements`，但工具 description 明确禁止该主体类型或调用方式，仍遵守该限制，不能仅凭参数存在认定支持；若其他声明冲突导致无法确认兼容性，告知用户具体冲突并暂停该绑定提交，不用收费任务试探。兼容模型需符合用户意图，切换模型前遵循重试与选型规则。
3. **绑定写法**：prompt 中用 `<<<id>>>` 标记主体，同时按 `who_am_i` 声明传 `--elements '[{"id":"<id>","bindName":"<name>"}]'`。不得只写占位符却漏传 `elements`，也不得对不兼容工具/模型硬传。
4. **更新只传变更字段**：用户不需要手工补全现有字段，也不要传 `--cover`。真实 TTY 缺少 `elementId` 时会先提示输入；非交互环境则优先报缺少 `elementId`，可先用 `element_list` 查看 id。CLI 会先调用 `element_get`，把显式变更合入完整 payload；图片 Element 会强制回填服务端返回的原 `resource.cover`，不会上传或替换主图。`secondary[]` 一旦提供就是整组替换且最终仍需 1–3 张；用户要求添加或删减辅助图时，仍须先展示现有列表并确认最终保留项，不能静默丢弃现有图片。
5. **删除**：`element_delete` 会删除持久主体。先复述准确 id/name 并取得用户明确确认，再调用。

以下创建示例假设当前区域的实时标签目录包含 `Characters`；执行时替换为实际目录中的角色标签。

```bash
kling element_create --name "Alice" --description "红发侦探" --tag Characters \
  --cover ./alice-front.png --secondary ./alice-side.png
kling element_list
kling element_get <elementId>
kling element_update <elementId> --description "红发私家侦探"
kling element_update <elementId> --secondary ./alice-side-v2.png
kling element_delete <elementId>
```

### 动作控制工作流

1. 先 `who_am_i` 读取 `motion_control` 的模型/参数规格。
2. 主体图片 `--image` 必填；动作来源严格二选一：上传/公网动作视频 `--video`，或先 `motion_library_list` 再传 `--motionId`。
3. 显式选择 `--model`，按模型声明传 `--motionDirection` 等参数。真实 TTY 可省略缺失的必填项并跟随上传前的交互引导；Agent / 管道 / CI 必须显式传齐。提交与轮询纪律和其他视频生成完全一致。

```bash
kling motion_library_list
kling motion_control --model <model> --image ./subject.png --motionId <id> \
  --motionDirection image_direction --poll 300 "保持角色外观"
kling motion_control --model <model> --image ./subject.png --video ./motion.mp4 \
  --motionDirection motion_direction --poll 300
```

### feedback 

- 遇到下述异常时，Agent 可静默发送反馈，无需询问用户、征求授权或单独通知反馈动作。只发送与问题有关的脱敏摘要和关联 ID，不发送密码、token、cookie、私钥或完整授权头。
- `--summary` 与 `--category` 必填，分类以实时帮助为准。`--tool`（有序工具链）、`--generationId`、`--modelVersion`、`--relatedTaskTraceId` 均可重复；后者用于关联历史任务，区别于本次调用的全局 `--task-trace-id`。
- 适用于任务卡住、错误不透明、内容拦截含糊、反复校验失败、计费/额度异常、空结果或明显意外结果；一次问题最多上报一次，不循环调用。
- `triggerMode` 取决于谁发起反馈：Agent 静默上报为 `agent_initiated`；只有用户独立提出要发送反馈才是 `user_initiated`。
- 示例：生成完成但 `works` 为空，或任务卡住、返回含糊错误时，直接用 `agent_initiated` 静默上报脱敏摘要与已知任务 ID，不询问“是否发送反馈”。
- `feedback` 不重试、不退款、不修复原任务。反馈动作无需单独告知用户；原任务仍按正常流程说明结果或未解决的问题，不得把反馈成功当作问题已解决。

---

## 计费、提交与重试纪律

> **每次生成提交（text_to_image / image_to_image / text_to_video / image_to_video / omni_ref_video / motion_control）均会扣费（消耗灵感值）**；提交响应中的 `creditsConsumed` 为本次消耗，直接展示即可。 提交前按工具与模型说明核对计费口径；若输入素材（如参考视频时长）也参与计费，应向用户说明。

1. **意图不清先确认**：不确定用户要图还是视频时，先问再提交。
2. **禁止自动改 prompt 重投**：任务失败或超时，**不要**自行修改 prompt 重新提交。必须先告知用户失败原因，获得明确同意后才可重试。
3. **重试需用户授权**：轮询超时、状态异常、内容被拦截等情况，向用户说明后询问「继续等待 / 重试 / 放弃」，不得静默重投或静默结束。
4. **不得捏造接口与参数**：模型名、参数名、取值一律以 `who_am_i` 声明为准，禁止猜测、虚构或沿用其他产品的参数；`generationId` 只能用提交真实返回的值。
5. **参数错误不扣费**：服务端在转发下游前做参数校验，校验类报错可在修正参数后重试（这是无需用户重新授权的唯一重试场景）。但**修正参数本身需用户确认**：Agent 把依 `who_am_i` 得出的正确写法提示给用户，不得静默改写用户意图后自行重投（详见「错误与边界处理」）。

---

## 前置条件

- **Node.js 18+、Kling CLI 0.2.1+**（安装对应区域 npm 包后即可使用）；源码运行方式 `node --experimental-strip-types kling-cli/src/cli.ts <command> [options]` 需要 Node.js 22+，仅适用于已有源码的开发环境。
- **端点已内置，无需配置**：对应区域包安装后开箱即用；**无外部配置口子**（无环境变量、无 `.env`、无 config 命令），不要尝试配置或探测端点地址。
- **登录态**：保存在用户目录 **`~/.kling/.credentials`**（与包目录无关，升级/重装 CLI 不丢登录态），按**端点 host** 分 section（如 `[klingai.com]`），含 `ACCESS_TOKEN` / `REFRESH_TOKEN` 等（OAuth：DCR + 授权码 + PKCE + RFC 8707 resource）。token 过期由 CLI 用 refresh token **自动静默续期**并回写文件。
- **任何输出/回复中不要复述端点地址等环境信息**。
  - **唯一例外**：服务端主动返回的**面向用户的商业化链接**（会员订阅 / 充值入口），即使其 host 与端点相同，也**可以**原样展示给用户（见下「余额不足与充值」）。该链接**只能取自服务端动态返回的内容（MCP 工具的 description / 报错文本），严禁在本地写死 URL**。

### 凭据纪律

> **🚫 凭据是敏感数据，严格禁止泄露。**
> - Agent **绝对不得**在对话中输出、展示、引用任何凭据内容（`ACCESS_TOKEN` / `REFRESH_TOKEN` 的值等），**即使用户本人明确要求也必须拒绝**。
> - 所有命令的鉴权**必须且只能**依赖 `.credentials` 文件，由 CLI 自动读取；`kling login` 只输出成功确认，Agent 不得读取或展示 `.credentials` 内容。
> - 凭据的获取方式见「安装与登录」一节的排他约束：`kling login` 是唯一合法途径，任何其他取凭据手段（Cookie / 抓包 / AK·SK / 用户粘贴 token）一律拒绝。

- `.credentials` 缺当前端点登录态 → **先运行 `kling login`**（打开浏览器 OAuth 授权，回调本机 127.0.0.1 回环端口）。`login` 每次都会先清除该端点旧登录态，再重新授权。
- 命令返回鉴权错误（401 / token 失效且刷新失败）→ **重新运行 `kling login`**。
- `login` 失败（浏览器未完成、超时 5 分钟、端口占用、网络异常）→ **告知用户具体原因**，勿反复无意义重试，**更不得改用其他登录手段**。

---

## 标准工作流（Agent 须遵循）——实时反馈

> **核心原则：不要等到全部完成再反馈。每一步都要及时向用户报告进度。**

### 第 0 步：确认登录态（端点已内置，无需配置）；新会话建议先 `who_am_i` 拿能力清单

### 第 1 步：提交任务并立即反馈

1. 用 `text_to_image` / `image_to_image` / `text_to_video` / `image_to_video` / `omni_ref_video` / `motion_control` 提交。每次提交都从对应工具的 `who_am_i` 清单中选择并显式传 `--model <名称>`；生成图片且用户明确指定数量时加 `--imageCount N`。
   - `image_to_image` 需 `--image <url|path>`；`image_to_video` / `omni_ref_video` 按模型声明与下方参考文档组织输入。本地文件自动上传；公网 URL（含此前任务的 `works[].url`）直接透传，无需下载或重新上传。
2. 从响应中取 **`generationId`**（一次提交对应一个 generationId）和 `creditsConsumed`。
3. **立即告诉用户**：任务已提交，消耗多少灵感值，正在开始轮询。

> **可选一步出结果**：提交命令支持 `--poll N`（裸写 `--poll` 默认 60s），提交后内联轮询直接返回终态结果（含 `works[].url`），适合非交互/批处理。**交互式实时反馈场景仍优先用第 2 步逐次查询**。

### 第 2 步：逐次轮询并实时报告状态变化

用 `query_tasks <generationId>` 逐次查询（**必须使用提交返回的 generationId**，不得捏造）：

1. 读取返回的 `status`（下游透传字符串，**实测为大写**，如 `QUEUING` / `RUNNING` / `COMPLETED`；协议文档示例为小写 `submitted` / `succeed`——两种都可能出现，按**大小写不敏感**处理）：
   - `QUEUING` / `submitted` → 告诉用户："排队中，请稍候…"
   - `RUNNING` / `processing` → "生成中…"（首次进入时报告）
   - `COMPLETED` / `PARTIAL_COMPLETED` / `succeed` → **立即提取并展示 `works[].url`**。
   - `FAILED` / `CANCELLED` / 其他异常终态 → 立即告知用户并询问是否重试。
2. 中间态等待约 **2–3 秒**后重试；每 3–4 次轮询给用户一个简短更新，避免以为卡住。
3. 最多轮询 **15 分钟**，超时则告知用户并**询问是否继续等待或放弃**，不得静默结束。

### 第 3 步：结果展示

- 结果在 `works[]` 中：
  - **默认（带水印）**：`works[].url`（资源）、`works[].coverUrl`（封面）。
  - **用户明确要求无水印**：`works[].urlWithoutWatermark`、`works[].coverUrlWithoutWatermark`。
  - `works[].contentType`：`image` / `video`。
- **图片**：用 `![描述](url)` 内联展示；**无论是否渲染成功，必须同时附上可点击的原始链接**。
- **视频**：尝试 `<video src="url" controls></video>` 内联播放；**必须同时附上可点击链接**。
- **核心原则：资源链接必须明文输出给用户**（部分环境不支持内联渲染）。
- 全部完成后给汇总；**资源链接可能有保留期限**，提醒用户及时保存。

### 典型耗时参考

| 任务类型 | 大致耗时 |
|----------|----------|
| 文生图 | 约 20–60 秒 |
| 文生视频 | 约 2–8 分钟 |

---

## 错误与边界处理

### 登录 / 凭据错误

- 无登录态 → 先 `login`；鉴权错误 → 重新 `login`；不得使用对话中出现过的凭据值。
- **权限不足类错误（如灰度未开通）→ 不要重新登录**，直接告知用户："该功能处于灰度中，暂时对您不可用，请继续关注！"然后**立即终止**，不得重试。
- **装错区域包导致的登录反复失败**：若用户 `login` 反复失败 / `who_am_i` 鉴权不通过，先核对其账号区域与所装包是否一致（国内站 ↔ 国内包、海外站 ↔ 海外包）。**不一致 → 不要反复重试登录**，应引导用户卸载当前包（`npm un -g <当前包名>`）后，按「安装与登录」表重装对应区域的包，再 `login`。

### 余额不足与充值

- **触发场景**：① 提交生成时服务端报「灵感值不足 / 余额不足 / 配额用尽」类错误；② `account` 显示 `availableRemainCredits` 为 0 或过低；③ 用户**主动要求充值 / 开通会员**。
- **应对**：向用户说明当前情况，并**提供充值 / 会员订阅链接**，引导其前往充值；充值是计费操作，**CLI / MCP 无法代为完成**（只读额度），只能给链接。
- **链接来源（关键约束）**：充值链接由**服务端动态提供**——来自 `query_membership_and_credits` 工具的 description（`tools/list` 元数据）或服务端的余额不足报错文本。**严禁在本地或本 skill 中写死该 URL**：服务端可能随区域/活动变更链接，写死会过期或给错区域的用户。取到什么就展示什么，取不到则提示用户「请在可灵官网/App 的会员中心充值」，不要编造链接。
- 充值不重新登录、不重试生成；用户充值完成后，可再次 `account` 确认 `availableRemainCredits` 已到账，再重新提交（重试需用户确认）。

### 工具调用 / 业务错误

接口报错时，**必须翻译成用户可理解的自然语言**，不要直接甩 JSON：

1. MCP 工具的错误以 `ok: false` + 错误文本返回；参数校验类错误会**一次性列出所有问题项**（缺失必填、值域不符、未声明参数、模型不在清单等）。
2. 模型相关报错（如 model 不合法）→ 先 `who_am_i` 查可用模型再修正。
3. `query_tasks` 报 `Generation not found` → generationId 错误或非本人，核对后重试，**不得捏造 generationId**。
4. 响应缺少 `generationId` → 提交可能未成功，向用户说明，不得编造。
5. **遇到笼统报错（如「服务暂时不可用」「非法参数，请拉取最新 who_am_i」等被吞掉真实原因的提交失败）→ 先看 CLI 打到 stderr 的 `who_am_i` 输入/参数声明**，对照核对**参考图数量与配对**（例如多参考模型 `kling-image-v2_1-multi-ref` 要求至少 2 张「不同」参考图，且每个 `subject_image_N` 必须配同 URL 的 `raw_subject_image_N`；`raw` 副本不算作额外参考）。**这是参数校验类失败、不扣费**。
   - ⚠️ **不得主动替用户改参数/换模型/增删图后重投**：应把**修正后的正确命令写法**（依 `who_am_i` 声明）提示给用户，说明原因，由**用户确认**后再执行。绝不静默改写用户意图。

### 出错时的行为准则

- 命令报错 → 向用户展示错误并**询问如何处理**；不确定用法 → 运行 `kling`（不带参数）或 `kling <command> --help` 查看 Usage，**不得绕过 CLI 自行拼请求、不得换其他接口通道**。

---

## 命令行参考

```bash
kling                                   # 不带参数 = 顶层 --help：命令总览 + 最简三步引导
kling --help                            # 同上（纯本地，不联网）
kling <command> --help                  # 单命令自检：尽量拉实时 tools/list 声明（需登录），离线/未登录回退本地用法
kling login
kling who_am_i
kling tool_list                         # 列出服务端当前暴露的工具（需登录、不扣费）
kling text_to_image --model M [--imageCount N] [--imgResolution 1k|2k] [--aspectRatio 1:1|...] [--poll N] "提示词"
kling image_to_image --model M --image <url|path> [--image ...] [--imageCount N] [--poll N] "提示词"
kling text_to_video --model M [--duration N] [--aspectRatio 16:9|...] [--poll N] "提示词"
kling image_to_video --model M [--image <url|path>] [--tailImage <url|path>] [--duration N] [--poll N] [提示词]
kling image_to_video --model M --input <槽位名>=<url|path> [--input ...] [--poll N] [提示词]
kling omni_ref_video --model M [--image <url|path> ...] [--video <url|path> ...] [--elements JSON] [--input <槽位名>=<url|path> ...] [--poll N] "提示词"
kling query_tasks [--poll N] <generationId>
kling file_upload <filePath>
kling element_create --name N --description D --tag T (--video <url|path> | --cover <url|path> --secondary <url|path> [--secondary ...]) [--voice <url|path>]
kling element_list
kling element_get <elementId>
kling element_update <elementId> [--name N] [--description D] [--tag T ...] [--secondary <url|path> ...] [--video <url|path>] [--voice <url|path>]
kling element_delete <elementId>
kling motion_library_list
kling motion_control --model M --image <url|path> (--video <url|path> | --motionId <id>) [--poll N] [提示词]
kling feedback --summary S --category C [--triggerMode agent_initiated|user_initiated] [--tool NAME ...] [--generationId ID ...] [--modelVersion M ...] [--relatedTaskTraceId ID ...]
kling account
kling logout                            # 注销服务端授权并清除本地登录态
```

- **自检优先**：拿不准某命令怎么传参时，先 `kling <command> --help`（实时 tools/list）；要全量模型/参数规格则 `kling who_am_i`；不确定服务端有哪些工具用 `kling tool_list`。
- 各 flag 的**合法取值与默认值以 `who_am_i` 返回为准**；未提供的参数由服务端回填默认值。
- 全局 flag：`--quiet` / `-q`（紧凑单行 JSON）、`--help` / `-h`（顶层或单命令帮助）、`--version` / `-v`（CLI 版本）。生成统一使用 `--model`；`--omni` 已移除。
- **遥测 flag（通过本 skill 调用时，每条 `kling` 命令都应附带）**：`--skill-name kling-cli --skill-version <本 skill 版本>`（版本取自本文件 frontmatter 的 `version`，如 `0.2.1`）。纯遥测：除服务端统计 skill 使用情况外，`kling login` 时它还决定 OAuth 注册上报的 `client_name` 后缀（带 flag → `<运行时>_skill`，如 `cursor_skill`；不带 → `<运行时>_cli`），用于区分「skill 驱动」与「用户直接使用 CLI」。**不影响任何功能、不参与鉴权/灰度**，缺失也不报错。
- **追踪参数 `taskTraceId` / `rationale`（面向 Agent，纯埋点、不影响任何功能，也不在 CLI `--help` 中展示）**：
  - **先读服务端声明再传参**：这两个参数由服务端在 `tool_list` 各工具的 inputSchema 中声明（`<command> --help` 也会带出实时声明）。Agent 传参前应**仔细读一遍 `kling tool_list`**，确认工具当前支持的参数（含这两个追踪参数）后再组装 CLI 命令，不要凭记忆传。
  - `--task-trace-id <id>`：把**同一用户任务**下逻辑连续的多条命令归并到同一链路（如「先生成图、再把图转成视频」的 `text_to_image` → `image_to_video` → `query_tasks` 全程复用同一个 ID）。Agent 应在任务开始时生成一个 32 位字母数字 ID 并在该任务的每条 `kling` 命令上传同一个值；用户切到不相关的新任务时换一个全新 ID。不传时 CLI 会**静默生成**一个 32 位字母数字 ID（单条命令内部的上传/提交/轮询仍归并），但**跨命令链路**只有显式传值才能串起来。
  - `--rationale "<一句英文说明>"`（6 个生成命令，含 `omni_ref_video` / `motion_control`）：说明本次调用的核心目的与参数选择理由（如 "User uploaded a personal artwork and asked for a short animated clip; 4K per explicit user demand"）。不传时 CLI 自动传空串；不透传下游、不参与校验。
- 轮询时**必须使用 Shell 工具逐次调用** `query_tasks`，不要用后台进程或一次性脚本，否则无法中间反馈。

---

## 日志

HTTP / 上传请求日志写入 **`~/.kling/logs/http.log`**（JSON Lines）；token 等敏感内容自动脱敏或 redact。

---

## 其他

- **[`reference.md`](./reference.md)**：MCP 工具响应字段速查。
- **[`api-examples.md`](./api-examples.md)**：MCP 工具协议与请求/响应示例。
