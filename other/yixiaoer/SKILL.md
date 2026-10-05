---
name: yixiaoer
version: 1.6.4
description: "蚁小二 (YiXiaoEr) 核心技能：支持多账号矩阵管理、账号查询 (accounts)、图文视频分发发布 (publish)、一键发布、保存草稿 (draft)、资源上传 (upload)、素材库 (material/library)、发布记录查询 (records) 及运营数据统计 (overviews)。适配 50+ 平台，助力高效运营新媒体矩阵。"
author: wangzhengjiao
---

> ## PilotDeck 执行速查（必读）
>
> **优先使用内置工具 `yixiaoer_api`**（无需 bash、无需找 api.ts）。查正常抖音/小红书账号示例：
> `{"action":"accounts","platforms":["抖音","小红书"],"loginStatus":1,"page":1,"size":100}`
>
> **禁止**：在 `Documents/yixiaoer-docs` 等目录搜索 `api.ts`；**禁止** `dir /s` / `find` / `head`。
>
> 备选（仅当 `yixiaoer_api` 不可用时）：
> ```bash
> node "%PILOTDECK_YIXIAOER_API%" --payload-file payload.json
> ```
>
> Windows PowerShell：先把 JSON 写入文件，再执行上面命令（不要用单引号 JSON 在 cmd 里硬拼）。
>
> **查账号**（如「有哪些抖音/小红书号、只要正常的」）：
> 1. `read_file` → `{PILOTDECK_YIXIAOER_SKILL_DIR}/docs/query-accounts.md`（或 `skills/yixiaoer/docs/query-accounts.md`）
> 2. 写入 payload 文件，例如：`{"action":"accounts","platforms":["抖音","小红书"],"loginStatus":1,"page":1,"size":100}`
> 3. 执行 `node "%PILOTDECK_YIXIAOER_API%" --payload-file 该文件`
> 4. 解析 JSON：`status===1` 为登录正常；**无需**蚁小二桌面客户端（默认云发布）
>
> 详细约定：`references/pilotdeck-setup.md`

# OpenClaw 龙虾技能 (OpenClaw Skill)

本项目采用 **DTO 驱动 (Interface-Driven)** 的架构模式。所有的功能均可通过 `api.ts` 配合标准化的 DTO Payload 进行调用。

## 核心原则 (Core Principles)

1.  **接口即标准**: 所有的功能调用严格基于后端 API 的 Request DTO 设计。
2.  **文档即指引**: `docs/` 下的 Markdown 文档用于解释对应接口的参数规则、必填项与约束。
3.  **分级阅读原则**: 所有的发布任务文档采用“内容类型首页 (Index) + 平台详情页 (Platform)”的二级结构。
4.  **零映射透传**: 鼓励调用者使用 `api.ts` 透明地提交符合 DTO 要求的 JSON Payload。
5.  **AI 场景化驱动**: 所有的文档均包含 `Trigger` (触发场景) 和 `Logic Flow` (执行逻辑) 模块，旨在通过自然语言语义引导 Agent 进行精确的意图识别与参数构造。

> [!IMPORTANT]
> **严格合规性与执行标准 (Strict Compliance & Standard)**:
> 1. **执行标准**: 所有 Agent 的调用行为、版本校验、错误处理**必须**遵循 [yixiaoer-skill 严格执行标准](./docs/execution-standard.md)。
> 2. **首选排错指南**: 在遇到任何脚本报错、发布失败或逻辑异常时，**必须优先查阅** [蚁小二 Skill 避坑与故障排查手册](./docs/troubleshooting-guide.md)。该手册汇总了 90% 以上常见失败场景的解决方案。
> 3. **文档检索顺序**: 针对 `publish` 行为，查询文档时**必须**首先查阅对应内容类型的 `index.md`（如 `docs/publish/article/index.md`），以获取基础 JSON 结构。**严禁**跳过 Index 直接访问平台级文档（如 `douyin.md`），否则可能导致 Payload根结构缺失。
> 4. 所有接口调用**必须**严格遵守各文档中定义的**必填字段 (`必填: 是`)** 以及对应的**数据格式要求**。
> 5. **资源引用规范**: 所有的**封面图 (cover)**、**图文图片 (images)** 以及 **视频文件 (video)** 必须先通过[资源上传接口](./docs/upload-resource.md)上传至系统并获得唯一的 `key`。禁止填入非系统内的网络 URL 或随意留空，否则会导致发布任务执行失败。
> 6. **素材库入库流程**: 涉及“上传到素材库”时，**必须执行两步逻辑**：先 `upload` (资源入存储) -> 后 `material` (登记入库)。严禁省略第二步。



## 平台支持 (Platform Support)

API 调用时涉及的平台名称必须使用蚁小二定义的中文枚举或 Code。

*   **平台枚举列表**: [docs/platform.md](./docs/platform.md)

## 统一执行指令 (Unified Execution)

所有的 API 功能统一通过 [api.ts](./scripts/api.ts) 脚本执行。调用时需通过 `--payload` 参数传入 JSON，且 **`action` 字段为必填项**，用于指定具体功能。

| action 值 | 对应的能力描述 | 相关文档 |
| :--- | :--- | :--- |
| `publish` | 图文、视频、文章分发发布。支持**发布到平台**或**保存为平台草稿**。 | [文章](./docs/publish/article/index.md), [图文](./docs/publish/image-text/index.md), [视频](./docs/publish/video/index.md), [草稿指南](./docs/save-draft.md) |
| `save-draft` | 保存内容到**蚁小二草稿箱**。仅云端存储，不触发推送。 | [草稿指南](./docs/save-draft.md) |
| `accounts` | 查询已绑定的账号列表 | [query-accounts.md](./docs/query-accounts.md) |
| `upload` | 上传本地或 URL 图片/视频 | [upload-resource.md](./docs/upload-resource.md) |
| `material` | 将已上传资源登记到**蚁小二素材库** | [material-resource.md](./docs/material-resource.md) |
| `records` | 查询发布任务概览列表 | [get-publish-records.md](./docs/get-publish-records.md) |
| `details` | 查询特定任务的执行详情 | [get-publish-records.md](./docs/get-publish-records.md) |
| `categories`| 获取账号分类/话题列表 | [get-publish-categories.md](./docs/get-publish-categories.md) |
| `activities`| 获取征文活动列表 | [get-publish-activities.md](./docs/get-publish-activities.md) |
| `locations` | 获取 POI 物理位置列表 | [get-locations.md](./docs/get-locations.md) |
| `music` | 获取抖音/快手可选背景音乐 | [get-music.md](./docs/get-music.md) |
| `music-category` | 获取音乐分类列表 | [get-music-categories.md](./docs/get-music-categories.md) |
| `collections`| 获取账号已创建的合集列表 | [get-collections.md](./docs/get-collections.md) |
| `groups` | 获取账号可绑定的群聊列表 | [get-groups.md](./docs/get-groups.md) |
| `goods` | 获取账号可绑定的商品列表 | [get-goods.md](./docs/get-goods.md) |
| `hot-events`| 获取平台实时热点列表 | [get-hot-events.md](./docs/get-hot-events.md) |
| `challenges`| 获取平台话题/挑战列表 | [get-challenges.md](./docs/get-challenges.md) |
| `miniapps` | 获取可挂载的小程序列表 | [get-miniapps.md](./docs/get-miniapps.md) |
| `syncapps` | 获取可同步发布的关联账号 | [get-sync-apps.md](./docs/get-sync-apps.md) |
| `games` | 获取可挂载的游戏列表 | [get-games.md](./docs/get-games.md) |
| `proxies` | 获取团队可用代理列表 | [proxy-management.md](./docs/proxy-management.md) |
| `proxy-areas`| 获取默认代理地区编码列表 | [proxy-management.md](./docs/proxy-management.md) |
| `account-overviews` | 账号表现汇总 (V2) | [get-account-overviews.md](./docs/get-account-overviews.md) |
| `content-overviews` | 查看发布作品数据统计 | [get-content-overviews.md](./docs/get-content-overviews.md) |
| `update-account` | 更新账号信息 (如设置代理) | [proxy-management.md](./docs/proxy-management.md) |
| `drafts` | (Read-only) 草稿列表管理指南 | [save-draft.md](./docs/save-draft.md) |

## 草稿识别标准 (Draft Recognition Standard)

当用户意图涉及“保存”、“草稿”或“以后再发”时，Agent **必须**进行次级研判：

1.  **蚁小二草稿 (YXE Draft)**:
    - **逻辑**：内容仅存储在蚁小二云端，不触发任何平台推送。
    - **Trigger**: “存为蚁小二草稿”、“暂存到草稿箱”、“存为 YXE 草稿”。
    - **Action**: `save-draft`
2.  **平台草稿 (Platform Draft)**:
    - **逻辑**：内容会被推送到对应平台（如抖音、小红书）的草稿箱，用户可在 App 端二次编辑。
    - **Trigger**: “存为抖音草稿”、“推送到平台草稿箱”、“存为小红书草稿”。
    - **Action**: `publish` (并在 `accountForms` 内每项设置 `"contentPublishForm": { "pubType": 0 }`)

### ⚠️ 歧义处理：若用户仅提及“存草稿”而未明确指出是“蚁小二草稿”还是“平台草稿”，Agent **必须立刻询问用户**以明确意图，严禁自行默认或猜测。

### 调用示例 (Example)

```bash
# 查询账号列表 (action: accounts)
node scripts/api.ts --payload='{"action": "accounts", "platform": "抖音"}'
```

## 开发指南 (Development Guide)

为了简化 API 的调用与脚本开发，我们提供了通用的 **API 助手模块**：

*   **API 助手模块**: `scripts/api.ts`
*   **开发指引文档**: [API 助手使用指南](./docs/scripts/api-guide.md)

在开发新功能或修改现有脚本时，请务必参考此指引。

---
> [!NOTE]
> 所有的敏感信息应通过环境变量 `YIXIAOER_API_KEY` 注入。
> 如果用户没有发送clientId，则默认使用云发布，publishChannel: cloud
> 
> **故障诊断与常见问题 (Troubleshooting FAQ)**:
> 
> 请**立即参阅**最权威的避坑指南：[🛡️ 蚁小二 Skill 避坑与故障排查手册](./docs/troubleshooting-guide.md)
> 
> 更多详情请参阅：[YiXiaoEr Skill 严格执行标准](./docs/execution-standard.md)
