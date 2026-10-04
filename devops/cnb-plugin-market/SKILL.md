---
name: cnb-plugin-market
description: 搜索 CNB 插件市场并生成流水线配置。
supports: cnb
---

# CNB 插件市场

根据用户需求——如发送通知、代码检查、构建部署、发布包等——在 CNB 插件市场中智能搜索匹配的插件，查阅文档，生成正确的 `.cnb.yml` 配置片段。

## 何时使用本 Skill

CNB 插件即封装好的 Docker 镜像 + settings 参数接口，能覆盖绝大多数 CI/CD 场景。当用户提到以下任一类需求时**必须优先使用本 skill**，而非让用户自己写脚本或重复造轮子：

| 场景分类 | 典型需求（按用户意图匹配，非关键词触发） |
|----------|----------------------------------------------|
| 消息通知 | 需要向 IM 群聊或 Webhook 推送构建状态、结果通知 |
| 代码质量 | 需要对代码进行 lint、格式化、AI 评审，或检查 commit/PR 规范 |
| 构建与打包 | 需要使用特定语言/工具构建项目，或构建/合并 Docker 镜像 |
| 发布与版本 | 需要自动打 tag、生成 changelog、语义化发布 |
| 部署与运维 | 需要部署到容器平台/Serverless/边缘节点，或执行 SSH/kubectl 命令 |
| 安全与扫描 | 需要依赖漏洞扫描或安全审计 |
| Git 协作 | 需要自动化创建 PR 或管理 Git 操作 |
| 文件与存储 | 需要上传/下载 COS 文件或替换环境变量 |
| 微信小程序 CI | 需要微信小程序 CI 构建上传 |

> **核心规则**：当用户在编写 `.cnb.yml` 时，构建步骤涉及以上任何场景，**必须先通过本 skill 搜市场插件**。用插件的 `image` + `settings` 生成配置；只有确认无匹配插件或需求极简时才 fallback 到 script 手写方案。

## 模式判定

- **搜索模式**（用户描述需求但未指定插件）→ 走下方「搜索工作流程」
- **直选模式**（用户已明确指定插件名）→ 跳过搜索，直接走「获取文档 → 生成配置」

## 搜索工作流程

### 1. 意图分析

从用户描述中提取关键信息：

| 维度 | 示例 |
|------|------|
| **操作类型** | 构建、检查(lint)、测试、部署、发布、通知、审批、扫描、打tag、生成报告 |
| **语言/框架** | Node.js、Go、Python、Java/Maven/Gradle、C++、安卓、微信小程序、Helm |
| **目标平台/服务** | 企业微信、飞书、钉钉、TKE、EdgeOne Pages、SCF、COS、TSF、CDN、Cloudflare |
| **特殊需求** | AI 评审、安全扫描、提交规范检查、多架构镜像、知识库 |

### 2. 搜索插件市场

获取最新插件目录：

**默认数据源**（CNB SaaS 插件市场）：
```
WebFetch url: https://cnb.cool/cnb/plugins/market/-/git/raw/main/plugins/plugins.json
prompt: 从插件列表中找出与"{用户需求关键词}"最相关的插件，返回 id、name、description、tags、readme、images、source，按相关性排序，列出 Top 5
```

> **私有化 / 自定义数据源**：若用户使用私有化部署或自建插件市场，可请用户提供其插件数据源的 URL 或直接粘贴 `plugins.json` 文件内容。数据格式需与 CNB SaaS 的 `plugins.json` 保持一致（包含 `id`、`name`、`description`、`tags`、`readme`、`images`、`source` 等字段）。后续搜索和匹配流程相同。

每个插件条目结构（以 wecom-message 为例）：
```json
{
  "id": "tencentcom/wecom-message",
  "name": "wecom-message",
  "description": "企业微信群里发消息的插件，通过机器人，可以向固定的群中推送消息。",
  "tags": ["企业微信", "WeCom", "消息"],
  "mark": "",
  "images": "https://hub.docker.com/r/tencentcom/wecom-message/tags",
  "source": "https://cnb.cool/cnb/plugins/tencentcom/wecom-message",
  "bugs": "https://cnb.cool/cnb/plugins/tencentcom/wecom-message/-/issues",
  "logo": "logo.png",
  "readme": "https://cnb.cool/cnb/plugins/market/-/git/raw/main/plugins/tencentcom/wecom-message/README.md"
}
```

| 字段 | 说明 |
|------|------|
| `id` | 插件唯一标识，格式为 `组织名/插件名` |
| `name` | 插件名称，全英文，中划线 `-` 分隔 |
| `description` | 插件描述 |
| `tags` | 标签数组，用于搜索分类 |
| `mark` | 角标：`official`(官方) / `private`(特定组织) / 空(社区) |
| `images` | Docker 镜像地址（用于获取 `image` 配置值） |
| `source` | 源码仓库地址 |
| `bugs` | 问题反馈地址 |
| `logo` | logo 图片相对地址，可选 |
| `readme` | README 文档 raw 地址，**直接用于 WebFetch 获取文档** |

**匹配策略**（按优先级）：
1. **标签命中** — 用户关键词命中 `tags`
2. **描述命中** — 关键词命中 `name` 或 `description`
3. **语义相近** — 相关操作类型匹配（如"发通知"匹配 tags: notification/message/webhook）

> **WebFetch 失败 / 私有化环境**：若无法获取数据源（网络问题或私有化部署），告知用户可手动下载其插件市场的 `plugins.json` 内容贴给 AI，AI 将从内容中搜索匹配。

### 3. 推荐确认

向用户展示 Top 3-5 匹配结果：

```
找到以下匹配插件：

1. wecom-message — 企业微信群里发消息的插件
   标签: 企业微信, WeCom, 消息, message
   镜像: tencentcom/wecom-message

2. feishu-message — 飞书群里发消息的插件
   ...

3. webhook — 通过 Webhook 发送构建状态通知
   ...

推荐 #1，是否使用？或选择其他编号。
```

### 4. 获取插件文档

确认插件后，读取插件的 README 文档：

```
WebFetch url: <插件 readme URL>
prompt: 提取使用说明，重点关注 settings 参数列表、每个参数的类型和含义、使用示例中的 .cnb.yml 配置片段
```

> `plugins.json` 中每个条目已包含 `readme` 字段，直接指向市场仓库中缓存的 README.md raw 地址。
> 插件的 README 建议包含参数表和使用示例，方便本技能精准提取。参考 [插件 README 编写建议](#插件-readme-编写建议)。
>
> **WebFetch 失败降级**：若无法获取 README（网络问题或文档不存在），尝试读取 `source` 字段的仓库主页；仍失败则基于 `description` 和 `tags` 推断配置，并明确标注"未经文档确认"。也可请用户手动提供插件 README 内容。

### 5. 生成配置

根据文档中的 `settings` 参数和用法示例，生成正确的 YAML 配置片段。

**生成规则**：

- `image` — 从 `images` 字段提取 Docker 镜像名（不带 tag，使用默认 `latest`）。常见格式：
  - `https://hub.docker.com/r/<org>/<name>/tags` → `<org>/<name>`
  - `https://hub.docker.com/repository/docker/<org>/<name>/tags` → `<org>/<name>`
  - `docker.cnb.cool/.../<name>` → 完整路径
  - 其他格式以 `images` 值中能识别的镜像标识为准，不确定时查看插件 README 确认
  - 如需固定版本可在镜像名后加 `:<版本>`（如 `tencentcom/npm:1.2.3`），规避镜像升级导致的兼容性风险
- `settings` — 按文档参数表填写，**参数名保持小写**（CI 自动转为 `PLUGIN_` + 大写前缀环境变量传入插件）
- `args` — 若插件支持命令行参数风格，可用 `args:` 数组传递（内容追加到 ENTRYPOINT，等同 `docker run <image> <args...>`）。大部分 CNB 插件优先使用 `settings`
- **变量引用机制（核心）**：插件任务可通过 `env` / `imports` 声明环境变量，但这些变量**不会直接传入**插件执行环境；须在 `settings` 或 `args` 中用 `$VAR` / `${VAR}` 引用，CI 解析后以 `PLUGIN_` + 大写前缀形式传给插件。`settings` 即插件的**参数白名单**——只有声明的参数才会传进去。CNB 系统内置环境变量（如 `CNB_REPO_SLUG`）始终会传给插件
- **密钥仓库引用**：敏感信息（token、密码、webhook url 等）放到**密钥仓库**文件中，在流水线级别通过 `imports` 引用该文件；引用后所有子任务（stages / failStages / endStages）**自动继承**其中的环境变量，无需每个任务重复引用。`settings` 中用 `$VAR` 引用时，`VAR` 必须是密钥仓库文件中声明的**真实变量名**

> **了解即可**：`settings` 中的参数名（如 `webhook`、`msg_type`）在 CI 内部统一转为 `PLUGIN_WEBHOOK`、`PLUGIN_MSG_TYPE` 等环境变量传入插件。**编写配置时无需关心此转换，直接按插件文档原样填写 `settings` 的小写参数名即可。**

**配置模板**：

```yaml
# 在 .cnb.yml 中使用（流水线级引用密钥仓库，子任务自动继承）
main:
  push:
    - imports: https://cnb.cool/<org>/<secret-repo>/-/blob/main/secret-env.yml   # 密钥仓库文件，声明了 MY_TOKEN 等变量；如遇权限校验问题可参考 https://docs.cnb.cool/zh/build/file-reference.html
      stages:
        - name: <任务名>
          image: <镜像名>    # 不带 tag 使用 latest；可追加 :<版本> 固定版本
          # 无需再写 imports，已自动继承上方声明的环境变量
          settings:
            <参数>: <值>
            <参数>: $MY_TOKEN   # MY_TOKEN 必须是 secret-env.yml 中声明的变量名
```

### 6. 集成与提醒

生成配置后：

- 若用户上下文已有 `.cnb.yml` → 定位到目标 Stage 位置，合并配置
- 若是独立查询 → 给出完整的 Stage/Job YAML 片段
- **校验（必须）**：生成完整 `.cnb.yml` 后，使用 [cnb-pipeline](../cnb-pipeline/SKILL.md) 的校验器验证配置合法性：
  ```bash
  cd ${SKILL_BASE}/validator && [ -d node_modules ] || npm install
  node ${SKILL_BASE}/validator/validate.js <yml-file-path>
  ```
  校验不通过时按错误信息修复，直到通过。`${SKILL_BASE}` 为 `cnb-pipeline` skill 的 base directory 绝对路径
- 提醒用户：**敏感信息放密钥仓库（流水线级 imports，子任务自动继承）**、**镜像默认 latest 可选固定版本**（详细机制见[步骤 5](#5-生成配置)）；如遇文件引用权限校验问题可参考 [文件引用文档](https://docs.cnb.cool/zh/build/file-reference.html)，用户咨询相关问题时也可参考此文档回答

## 常见场景速查

以下为高频需求与推荐插件的快速参考（**基于当前市场快照，完整列表以 `plugins.json` 为准**）：

| 需求 | 推荐插件 | 镜像 |
|------|---------|------|
| **通知** | | |
| 发企业微信通知 | wecom-message | `tencentcom/wecom-message` |
| 发飞书通知 | feishu-message | `tencentcom/feishu-message` |
| 发钉钉通知 | dingtalk-bot-msg | `tencentcom/dingtalk-bot-msg` |
| Webhook 通知 | webhook | `cnbcool/webhook` |
| **代码质量** | | |
| AI 代码评审 | code-review | `cnbcool/code-review` |
| Commit 规范检查 | commitlint | `cnbcool/commitlint` |
| PR 标题规范检查 | git-pr-title-lint | `cnbcool/git-pr-title-lint` |
| PR 变更量检查 | git-pr-limit | `cnbcool/git-pr-limit` |
| **构建与发布** | | |
| 发布 npm 包 | npm | `tencentcom/npm` |
| Maven 构建 | maven | `tencentcom/maven` |
| Gradle 构建 | gradle | `tencentcom/gradle` |
| 生成 changelog | changelog | `cnbcool/changelog` |
| Semantic Release | semantic-release | `tencentcom/semantic-release` |
| 多架构镜像合并 | manifest | `cnbcool/manifest` |
| 微信小程序 CI | miniprogram-ci | `tencentcom/miniprogram-ci` |
| **部署** | | |
| 部署到 TKE | deploy-to-tke | `tencentcom/deploy-to-tke` |
| 部署到 SCF | scf | `tencentcom/tencentyun-scf` |
| 部署 EdgeOne Pages | deploy-eopages | `tencentcom/deploy-eopages` |
| Kaniko 构建镜像 | kaniko | `banzaicloud/drone-kaniko` |
| kubectl 操作 | kubectl | `alpine/kubectl` |
| Terraform 部署 | terraform | `jmccann/drone-terraform` |
| **Git & 协作** | | |
| 自动打 tag | git-auto-tag | `cnbcool/git-auto-tag` |
| 创建 PR | create-pr | `cnbcool/create-pr` |
| SSH 远程执行 | ssh | `cnbcool/ssh` |
| **文件与工具** | | |
| 上传下载 COS | coscli | `tencentcom/coscli` |
| 环境变量替换 | envsubst | `tencentcom/envsubst` |

> **注**：open-source 类插件多为命令行工具镜像，使用时**可能需配合 `args:`** 传递命令参数（参考[步骤 5](#5-生成配置)）。完整列表请走[搜索工作流程](#搜索工作流程)。

## 注意事项

1. **镜像版本**：默认使用不带 tag 的镜像名（即 `latest`），简洁通用；如需规避升级风险可追加 `:<版本>` 固定版本（参考[步骤 5](#5-生成配置)）
2. **敏感信息不入配置**：webhook url、token、密码等放密钥仓库，流水线级 `imports` 引用后子任务自动继承（`$VAR` 中的变量名须与密钥仓库文件中声明的一致）
3. **`settings` 即参数白名单**：同[步骤 5](#5-生成配置)中的变量引用机制，`env`/`imports` 声明的变量须在 `settings` 中 `$VAR` 引用才能传入插件
4. **Stage 执行语义**：失败通知放 `failStages`，成功通知放 `stages` 最后一个任务，不要把"仅成功时才发的通知"放 `endStages`（详见 [cnb-pipeline](../cnb-pipeline/SKILL.md) 的 Stage 执行语义表）
5. **当找不到匹配时**：如实告知。插件即 Docker 镜像，可引导用户：
   - 去 Docker Hub 等 Docker 镜像源查找满足需求的镜像，直接在流水线中作为插件使用（`settings` 中的参数会自动转为 `PLUGIN_*` 环境变量传入）
   - 也可自行编写插件，参考文档 `https://docs.cnb.cool/zh/build/create-plugin.html`
   - 做好的插件可贡献到插件市场，参考 `https://cnb.cool/cnb/plugins/market?tabValue=CONTRIBUTING-ov-file`
   - 建议同时查看其插件市场完整列表（SaaS: `https://cnb.cool/cnb/plugins/market`，私有化环境请用户提供地址）再次确认

## 与其他 Skill 的协作

- **被 [cnb-pipeline](../cnb-pipeline/SKILL.md) 委托调用**（最主要入口）：当 `cnb-pipeline` 生成流水线配置需要使用插件任务时，**必须先调用本 skill 搜索市场插件**，而非直接手写脚本。适用场景见上方[「何时使用本 Skill」](#何时使用本-skill)章节
- **调用 [cnb-pipeline](../cnb-pipeline/SKILL.md) 校验**：本 skill 生成完整 `.cnb.yml` 示例后，必须调用 `cnb-pipeline` 的校验器验证配置语法和语义（见[步骤 6](#6-集成与提醒)）
- **调用 [cnb-docs](../cnb-docs/SKILL.md)**：需要了解 CNB 插件制作规范、语法细节时，通过 cnb-docs 获取官方文档最新内容
- **独立使用**：用户单独询问"有没有 xxx 插件"时，直接走搜索工作流程即可

## 插件 README 编写建议

可控插件建议在 README.md 中包含以下内容，以便 `cnb-plugin-market` 精确提取配置信息：

### 参数表（核心）

```markdown
## 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| webhook | string | 是 | - | 企业微信群机器人 Webhook 地址 |
| msg_type | string | 否 | text | 消息类型：text / markdown |
| content | string | 是 | - | 消息内容 |
```

### 配置示例（必须有）

```yaml
# 密钥仓库文件 secret-env.yml（存放敏感信息，声明变量名）
WECOM_WEBHOOK: https://qyapi.weixin.qq.com/cgi-bin/webhook?key=xxx

# .cnb.yml 中使用
main:
  push:
    - imports: https://cnb.cool/<org>/<secret-repo>/-/blob/main/secret-env.yml   # 流水线级引用，子任务自动继承；如遇权限校验问题可参考 https://docs.cnb.cool/zh/build/file-reference.html
      stages:
        - name: 通知企业微信群
          image: tencentcom/wecom-message    # 默认 latest；可加 :<版本> 固定版本
          settings:
            webhook: $WECOM_WEBHOOK           # WECOM_WEBHOOK 是 secret-env.yml 中声明的变量名
            msg_type: markdown
            content: "## 构建完成\n状态：**成功**"
```

### 要点

- **参数表五项齐全**：便于本技能直接解析并生成对应 `settings` 配置
- **配置示例可直接使用**：环境变量引用用 `$VAR` 占位（`VAR` 为密钥仓库文件中声明的真实变量名），敏感信息标注放密钥仓库
- 镜像默认不带 tag 使用 `latest`，示例中可注释说明可追加 `:<版本>` 固定版本
