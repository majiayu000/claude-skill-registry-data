---
name: browser-tools
description: 浏览器与网页任务的路由器：按任务把工作交给 ego-browser / OpenCLI / firecrawl / anysearch / CloakBrowser 之一。当需要打开或操作网页（点击/填表/截图/登录态操作）、网页搜索或深度调研、读取 URL / 批量抓取 / 整站抓取 / 监控页面变化、访问反爬站点（验证码/挑战页/被拦截）、页面性能/网络/控制台/内存诊断，web scraping / browser automation / deep research 等英文表达，或抓取/搜索工具报错需要回退时使用。
---

# 浏览器与网页任务路由

本 skill 只做三件事：**选工具、交接、失败回退**。各工具的具体用法住在各自的 skill 和 references/，本文件只裁决选型。

| 工具 | 定位 |
| ------ | ------ |
| **OpenCLI** | 站点 adapter —— 固定命令行，反爬已被 adapter 消化 |
| **anysearch** | 网页搜索 —— 返回结果条目，垂直域强 |
| **firecrawl** | 深度抓取 —— 全文 markdown、整站批量、监控（托管服务） |
| **ego-browser** | 本地登录态操作 + CDP 直连诊断 |
| **CloakBrowser** | 反爬穿透（指纹消除） |

## 第一步：硬约束前置

以下约束在分类之前裁决，命中即落定，分类树无权覆盖：

1. **用户指定了工具** → 用指定工具。
2. **需本地登录态或涉及隐私内容** → 在 ego-browser 与 OpenCLI 本地桥中选择，托管服务（firecrawl / anysearch）退出候选。
3. **敏感操作**（购买 / 发布 / 删除 / 权限修改 / 私密数据外发）→ 先向用户确认再执行。用户已明确授权的，直接执行。

完成条件：三条约束逐一核对过，命中的那条已落定，未命中的进入第二步。

## 第二步：adapter gate（条件式）

仅当**目标站点明确**且需求是**查询或固定操作**时执行；其余请求直接进第三步。

```text
1. 查 adapter 目录：本会话已有 `opencli list` 结果 → 用缓存；没有 → 跑一次并缓存
2. 有目标站 adapter 且子命令覆盖需求 → OpenCLI
   覆盖 ≠ 最合适：仍按任务形态核对第三步分类树，与任务不匹配的覆盖不算命中
3. 子命令不覆盖需求（截图 / 自由交互 / 诊断等）→ 视为无命中，进第三步
4. opencli 不可用或报错 ≠ 无命中：如实标注，继续第三步
```

完成条件：已有 adapter 目录缓存；命中判定同时核对了「子命令覆盖需求」和「任务形态匹配」；「无命中」与「opencli 不可用」已区分开。

命中 OpenCLI 的**桥接型命令**需先 bind（拉起 Chrome + 绑定标签页，操作序列见 [references/tool-reference.md](references/tool-reference.md) 的 OpenCLI 节）；`[api]` adapter 直接调 HTTP，无需此步。

## 第三步：按任务形态分类

先判**深浅**，再落叶子。深浅按需求形态判断，不等用户说出"深度研究"：

- **快速拿结果**（"查查""确认一下"）→ 取到可用结果即回复。
- **深入调研**（要跨页探索 / 多源比对 / 完整脉络）→ 按分类树的深入调研叶子执行。

工具选择本身不甩给用户：一般歧义自行判断、先执行、凭结果升级；只有授权、私密数据外发、付费、交付范围存在实质歧义时才问。

### 分类树

每片叶子标注 skill；各工具的 reference 见文末「参考文档表」。落到叶子即按「交接」节处理。首个命中即停。

```text
网页搜索
├─ 快速拿结果 → Skill("anysearch") search，结果够用即回复
├─ 独立多条搜索并行 → Skill("anysearch") batch_search
├─ 深入调研（多页面并行 / 跨页探索 / 追踪链接 / 上下文比对）
│  → Skill("ego-browser") 多开 task space（默认主场），细节见 references/ego-browser.md
├─ 主要要大量公开全文 / 批量抓取 / 结构化数据
│  → Skill("firecrawl") search --scrape / crawl
└─ 混合 → ego-browser 主导探索 + firecrawl 补批量

URL 读取
├─ 静态文章轻读 → Skill("anysearch") extract —— 先轻后重：从最轻的工具试起，
│   技术细节（是否 JS 渲染等）先试再说，不拿问题挡在用户前面
├─ JS 渲染 / PDF / 结构化提取 / 整站 / 监控 → Skill("firecrawl")
└─ 需交互 / 截图 / 可视验证 / 登录态 → Skill("ego-browser")

页面交互
├─ 交互为了拿数据 → Skill("firecrawl") interact
├─ 交互本身是任务 / 需可视验证 / 用户接管 → Skill("ego-browser")
└─ 固定操作且 adapter gate 已命中 → OpenCLI（沿用 gate 结果）

诊断（性能 / 网络 / 控制台 / 内存）→ Skill("ego-browser") cdp()，无替代；
   CDP domain 用法见 references/ego-browser.md
```

完成条件：已按需求形态命中唯一叶子，该叶子的 skill 与 reference 已按「交接」节处理。

## 反爬

反爬是**能力约束**，不是站点名的一票裁决：

- 有 adapter 的站点仍可优先 OpenCLI（命中判定见第二步）。
- 需用户现有登录态 → 保留本地路径（ego-browser / OpenCLI 桥），不为反爬放弃登录态。
- 确认出现挑战页，或该工具对此站已知过不了（穿透矩阵见 [references/anti-bot-field-guide.md](references/anti-bot-field-guide.md)）→ CloakBrowser，用法见 [references/cloakbrowser.md](references/cloakbrowser.md)（无独立 skill）。

执行后取回的内容像验证码 / 挑战页（"请稍候…"、challenges.cloudflare.com）或异常空 DOM：先排除网络故障 / 页面未加载 / 权限问题，再按 anti-bot-field-guide.md 判型，转移到对应叶子。

## 交接

每片叶子标注 skill，reference 按工具从「参考文档表」取。执行交接：

1. **skill 已注册** → 加载：`Skill("opencli")` / `Skill("ego-browser")` / `Skill("firecrawl")` / `Skill("anysearch")`。
2. **未注册但其 SKILL.md 文件可读** → 直接读该文件。
3. **两者皆不可用** → 按 reference 中的可执行说明操作，或按分类树重新路由到别的叶子。

CloakBrowser 无独立 skill，唯一入口是 references/cloakbrowser.md。

交接完成的标志：对应 skill 内容已实际加载，或 reference 已读。在此之前按未激活处理，引用的工具命令以已加载内容为准。

## 失败回退

**失败** = 同一任务里工具执行出错。多个工具正常协作、研究多查几步，都不算失败回退。

- 同一失败条件（**工具 × 操作 × 目标**）在条件不变时不重试。
- 最多 **3 条**回退路径，按叶子的自然替代关系换；耗尽即交付部分结果 + 已试工具链 + 阻塞原因。
- 按错误类型先处理再换叶：
  - 额度耗尽（402 / quota）→ 直接换下表回退叶，任务继续
  - 429 → 尊重 Retry-After，限次重试，重试耗尽才换叶
  - 认证失败 → 先配 key / 走登录，这是配置问题不是工具问题
  - 网络故障 → 先健康检查，再决定是否换叶
- 写操作回退前先确认是否已生效；发帖 / 下单类操作禁止盲重放。
- 用户接管（"user is controlling" / 人工介入）是正常交接：交还控制权，等待用户。

额度耗尽时的换叶方向：

| 失败叶 | 回退 |
| -------- | ------ |
| firecrawl `crawl` / `map` / `batch` 需 key 或超额 | URL 发现 → 去重队列 → 限深度/页数逐页抓：静态页 anysearch extract；需 JS 渲染或登录态 ego-browser task space |
| firecrawl `search --scrape` 失败 | anysearch search 拿条目 → 目标 URL 交 ego-browser 读全文 |
| firecrawl `scrape` 失败 | 静态页 anysearch extract；JS 渲染 / 登录态 ego-browser |
| firecrawl `monitor` 不可用 | ego-browser task space 打开比对（仅本次）；持续监控与用户确认调度方式后另建 |
| anysearch 额度尽 | firecrawl `search --scrape`；或 opencli 搜索 adapter（bind 后） |
| ego-browser 连接故障 | 按 ego-browser skill 自身的恢复文档恢复，不换工具 |

## 参考文档

| 文件 | 内容 |
| ------ | ------ |
| [references/tool-reference.md](references/tool-reference.md) | 五工具的完整 API、命令表、环境入口、OpenCLI bind 操作、独占能力对照 |
| [references/ego-browser.md](references/ego-browser.md) | ego-browser 能力画像、诊断 cdp 示例、task space 速记、与 CloakBrowser 互补、委派语法 |
| [references/anti-bot-field-guide.md](references/anti-bot-field-guide.md) | 反爬类型分类、检测方法、穿透矩阵、实战案例、可执行脚本 |
| [references/cloakbrowser.md](references/cloakbrowser.md) | CloakBrowser 安装、配置、API、macOS 注意、部署方案 |
| [references/combo-patterns.md](references/combo-patterns.md) | 多工具组合使用模式（实战场景） |
