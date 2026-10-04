---
name: VaneworkerGW
title: VaneworkerGW 模型网关指南
description: 提供 VaneworkerGW 大模型网关的使用说明、配置方法和常见问题解答，帮助 Agent 和用户统一管理模型访问。
version: 1.0.0
example: |-
  > **如何配置网关**：请参考 `~/.vaneworker-gw/config/vaneworker-gw.yaml` 文件，设置服务商和模型偏好。
  > **故障切换**：当某个服务商不可用时，网关会自动尝试其他候选模型。
  > **本地模型安装**：如需启用本地模型，可运行安装脚本下载 Ollama 和 Qwen 模型。
---

# VaneworkerGW Agent 使用与问答指南

VaneworkerGW 是一个运行在本机的**大模型网关**，为 Codex、Claude Code、WorkBuddy、Hermes 以及其他 Agent 提供统一的模型访问入口。它把本地模型、云端模型、免费服务商和 DeepSeek Web 账号统一到一个地址，并负责协议转换、模型路由、故障切换、记忆管理和隐私保护。

本文件不仅描述技术接口，也提供 Agent 回答用户常见疑问时应采用的产品说明、优缺点和配置方法。

---

## 1. Agent 应先掌握的结论

### 1.1 VaneworkerGW 能解决什么问题

- **统一入口**：客户端只需要配置一个本地 URL、一个 API Key 和模型名 `auto`，不用分别维护多个供应商地址。
- **模型路由**：根据服务商是否启用、凭据是否可用、模型是否允许、健康状态、价格、能力和延迟选择候选模型。
- **协议兼容**：同时提供 OpenAI Chat Completions、OpenAI Responses、Anthropic Messages 三种格式，按客户端要求选择。
- **故障切换**：某个服务商超时、限流或返回 5xx 时，可按路由策略尝试其他候选。
- **本地能力**：可选安装 Ollama 和 Qwen 模型，用于本地对话、嵌入、记忆提取和记忆检索。
- **隐私保护**：敏感信息可在记忆处理前脱敏；本地模型模式下，适合不希望把内容发送到云端的场景。
- **跨平台安装**：设计目标是 macOS 和 Windows 一键安装、运行环境隔离；用户运行目录与开发目录应分开理解。
- **便于排查**：管理端可查看服务状态、供应商可用性、请求日志、记忆内容和当前配置。

### 1.2 应如何向用户解释优点

可以这样回答：

> VaneworkerGW 相当于本机的大模型总开关。Agent 不必为每个模型服务商单独改配置，统一连到 `127.0.0.1:12320` 即可。需要便宜或免费的模型时使用已配置的云端服务商，需要隐私、离线或稳定的记忆检索时可以安装本地模型；两者也可以按需混合使用。

### 1.3 应主动说明的限制

- 本地模型需要下载模型文件，并占用数 GB 磁盘空间以及数 GB 或更多运行内存；模型越大，回答质量通常越好，但响应速度和资源占用也会增加。
- 首次安装**不预装本地模型和记忆数据**，因此安装后不会自动占用大量模型空间；用户选择启用本地能力后再安装。
- 云端服务商的免费额度、价格、限流、可用模型和登录状态可能变化；不能承诺永久免费或固定速度。
- 本地模型不等于所有任务都比云端强。复杂推理、超长上下文、最新知识和高质量代码任务，可能更适合云端模型。
- 记忆功能不是完整聊天记录备份，也不是模型训练；它保存经过提取的偏好、事实、项目上下文等，用于后续相关对话检索。

---

## 2. 配置文件与运行环境

### 2.1 配置文件位置

- **开发环境**：`config/vaneworker-gw.yaml`
- **macOS 安装环境**：`~/.vaneworker-gw/config/vaneworker-gw.yaml`
- **Windows 安装环境**：`%USERPROFILE%\.vaneworker-gw\config\vaneworker-gw.yaml`
- **目录规范**：安装运行目录下，配置文件位于 `config/vaneworker-gw.yaml`，数据位于 `data/`，日志位于 `logs/`（均在 vaneworker-gw 根目录下）。

不要把开发环境路径硬编码到用户配置、发布包或 Agent 配置中。安装环境应以用户目录下的配置文件和安装目录为准。

### 2.2 当前本地网关 API 配置

配置文件中的以下字段是本地 API 的权威来源：

```yaml
server:
  router_host: 127.0.0.1
  router_port: 12320
router:
  api_key: vaneworker-gw-local-key
```

因此本地网关连接参数为：

- **Base URL**：`http://127.0.0.1:12320/v1`
- **API Key**：`vaneworker-gw-local-key`
- **Model**：`auto`
- **认证方式**：通常使用 `Authorization: Bearer vaneworker-gw-local-key`；兼容客户端也可使用 `x-api-key: vaneworker-gw-local-key`。

`auto` 是网关的虚拟模型名，不代表某一个固定上游模型。网关会根据当前启用的候选和路由策略选择实际模型。

### 2.3 语言站点

- 中文界面、中文用户说明或中文认证流程：指向 `https://manai.cc`。
- 英文界面、英文用户说明或英文认证流程：指向 `https://vaneworker.com`。

---

## 3. 对外的三个大模型接口

三个接口都使用同一个本地地址、API Key 和模型名 `auto`。**按客户端协议选择其中一个即可，不需要三个都配置。**

### 3.1 OpenAI Chat Completions

适合大多数 OpenAI-compatible 客户端、脚本和只支持传统聊天格式的工具。

```http
POST http://127.0.0.1:12320/v1/chat/completions
Authorization: Bearer vaneworker-gw-local-key
Content-Type: application/json
```

```json
{
  "model": "auto",
  "messages": [
    {"role": "user", "content": "请介绍 VaneworkerGW"}
  ],
  "stream": false
}
```

`curl` 示例：

```bash
curl http://127.0.0.1:12320/v1/chat/completions \
  -H 'Authorization: Bearer vaneworker-gw-local-key' \
  -H 'Content-Type: application/json' \
  -d '{"model":"auto","messages":[{"role":"user","content":"你好"}]}'
```

### 3.2 OpenAI Responses

适合支持 OpenAI Responses wire API 的客户端，例如 Codex 类客户端。请求主体使用 `input`，而不是 `messages`。

```http
POST http://127.0.0.1:12320/v1/responses
Authorization: Bearer vaneworker-gw-local-key
Content-Type: application/json
```

```json
{
  "model": "auto",
  "input": "请总结今天的工作",
  "stream": false
}
```

Codex 类配置示例：

```toml
[model_providers.VaneworkerGW]
name = "VaneworkerGW"
base_url = "http://127.0.0.1:12320/v1"
experimental_bearer_token = "vaneworker-gw-local-key"
wire_api = "responses"
```

VaneworkerGW 启动时只注册或更新上面的 Provider 配置，**不会修改 Codex 当前的默认 `model` 和 `model_provider`**。

当用户明确要求把 Codex 默认 Provider 切换到 VaneworkerGW 时，Agent 应编辑以下文件：

- macOS：`~/.codex/config.toml`
- Windows：`%USERPROFILE%\.codex\config.toml`

在文件顶层、所有 `[section]` 之前设置：

```toml
model = "auto"
model_provider = "VaneworkerGW"
```

并确保文件中存在前述 `[model_providers.VaneworkerGW]` 配置段。修改时必须遵守以下规则：

1. 先读取现有 `config.toml`，保留其他 Provider、项目设置、信任设置和用户自定义配置。
2. 只更新顶层 `model`、`model_provider` 和 `[model_providers.VaneworkerGW]`，不要重复添加同名键或同名配置段。
3. `model` 使用网关虚拟模型 `auto`，`model_provider` 的大小写必须与配置段名称 `VaneworkerGW` 完全一致。
4. 只有用户明确要求切换默认 Provider 时才修改这两个顶层键；仅启动 VaneworkerGW 不得修改它们。
5. 用户要求恢复原 Provider 时，恢复修改前的 `model` 和 `model_provider` 值，不要删除其他配置。

### 3.3 Anthropic Messages

适合 Claude Code 或其他使用 Anthropic Messages 格式的客户端。该接口的认证头可使用 `x-api-key`。

```http
POST http://127.0.0.1:12320/v1/messages
x-api-key: vaneworker-gw-local-key
Content-Type: application/json
```

```json
{
  "model": "auto",
  "max_tokens": 1024,
  "messages": [
    {"role": "user", "content": "请检查这个问题"}
  ]
}
```

Claude Code 类环境变量示例：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:12320",
    "ANTHROPIC_API_KEY": "vaneworker-gw-local-key"
  }
}
```

### 3.4 三种接口如何选择

| 使用场景 | 选择 |
| --- | --- |
| 普通 OpenAI SDK、简单脚本、WorkBuddy | `/v1/chat/completions` |
| Codex 或明确要求 Responses 的客户端 | `/v1/responses` |
| Claude Code、Anthropic SDK 或 Messages 客户端 | `/v1/messages` |

排查连接问题时，先确认网关已启动，再确认客户端使用了正确的协议路径；不要把 `/v1/responses` 的请求体直接发到 Chat Completions，也不要把 Anthropic Messages 的认证方式和响应格式当成 OpenAI 格式处理。

---

## 4. 本地模型：用途、价值和代价

### 4.1 本地模型有什么用

本地模型通过 Ollama 运行在用户电脑上。它主要有四类用途：

1. **快速响应**：模型在本机运行，不需要等待云端网络往返；实际速度取决于 CPU、GPU、内存和模型大小。
2. **隐私保护**：对话、项目内容、记忆提取和嵌入可以留在本机，适合源码、客户资料、内部文档等敏感内容。
3. **记忆提取**：从对话中识别用户偏好、长期事实、项目约定和重要上下文，形成可检索的记忆条目。
4. **记忆检索**：新问题到来时，先从本地语义数据库找到相关历史信息，再交给 Agent 参考，从而减少用户重复说明。

### 4.2 为什么需要几个 GB 内存

本地模型文件通常较大，运行时还需要加载模型权重、上下文窗口、KV cache 和嵌入模型。小模型可能只需要数 GB 资源，大模型可能需要更多。内存不足时会出现加载失败、系统变慢或响应变慢。

因此应向用户说明：

- 追求隐私、离线可用和低网络延迟：考虑本地模型。
- 电脑内存有限、希望立即使用或需要更强推理：优先云端模型。
- 可以混合使用：本地模型负责记忆/隐私敏感内容，云端模型负责复杂回答；具体路由取决于配置和可用性。

### 4.3 本地模型的默认状态与启用

首次安装不带本地模型和记忆数据。配置中的 `ollama.local_llm_enabled` 和 `ollama.embedding_enabled` 应在模型安装完成后再启用，避免新电脑首次安装就下载大型文件。

安装流程：

1. `GET http://127.0.0.1:12310/api/ollama/status` 查看状态。
2. 如未安装，调用 `POST http://127.0.0.1:12310/api/ollama/install`。
3. 轮询 `GET http://127.0.0.1:12310/api/ollama/install/status`，直到安装阶段为 `ready`。
4. 在管理端配置中启用本地 LLM 或嵌入模型，并重新加载配置。

默认模型配置位于 `ollama` 节：

```yaml
ollama:
  base_url: http://127.0.0.1:12330
  llm_model: qwen3.5-4b-int8
  embedding_model: qwen3-embedding-0.6b-int8
  local_llm_enabled: false
  embedding_enabled: false
```

---

## 5. 记忆功能：是什么、有什么用、如何管理

### 5.1 记忆不是聊天记录

记忆功能会从对话中提取对未来有帮助的长期信息，而不是无条件保存全部原文。典型内容包括：

- 用户偏好：语言、输出格式、代码风格、常用工具。
- 稳定事实：所在时区、项目名称、技术栈、团队约定。
- 工作上下文：当前项目目标、已做决定、待办事项和重要限制。
- 交互习惯：希望回答简洁、需要先给结论、特定文件必须记录工作日志等。

记忆的价值是让 Agent 在后续会话中**少问重复问题、延续上下文、提供更个性化的回答**。它不会凭空增加模型能力，也不保证召回每一条历史内容。

### 5.2 记忆的主要功能

- **自动提取**：从用户和 Agent 的对话中提取候选记忆。
- **语义检索**：按照问题含义检索相关记忆，不要求关键词完全相同。
- **预取**：在新一轮请求前提前查询相关记忆。
- **同步回合**：把一轮用户消息和 Agent 回复一起纳入记忆处理。
- **去重更新**：对相似记忆进行语义去重，避免数据库不断重复增长。
- **隐私清理**：按规则处理邮箱、IPv4、API Key 等敏感信息。
- **人工维护**：管理端可以列出、修改和删除记忆。

### 5.3 记忆存储和 API

默认存储目录是相对于运行配置目录的 `data/memory/`，向量数据库位于 `data/memory/qdrant/`。首次安装不会携带已有用户记忆。

网关管理端默认地址为 `http://127.0.0.1:12310`，记忆接口包括：

- `POST /api/memories/search`：按问题检索记忆。
- `POST /api/memories/add`：添加记忆。
- `POST /api/memories/update`：修改记忆。
- `POST /api/memories/delete`：删除记忆。
- `POST /api/memories/prefetch`：预取相关记忆。
- `POST /api/memories/sync-turn`：同步一轮对话。
- `GET /api/memories`：管理端列出记忆。
- `PUT /api/memories/{memory_id}`：管理端修改记忆。
- `DELETE /api/memories/{memory_id}`：管理端删除记忆。

用户问“记忆有什么用”时，应优先解释实际收益和隐私边界，不要把记忆描述成模型训练、永久保存或绝对准确的个人档案。

---

## 6. 预装服务商及设置方式

服务商配置位于配置文件的 `providers` 数组，也可以通过管理端 `GET /api/config` 查看、通过带当前 `revision` 的 `PUT /api/config` 更新。修改前先读取最新配置，不要覆盖其他进程刚写入的修改。

### 6.1 Kilo：免费，可直接使用

Kilo 已预装免费模型 `kilo-auto/free`，通常不需要用户填写 API Key。启用方式：

1. 在管理端打开 Kilo 服务商开关，确认 `enabled: true`。
2. 确认模型 `kilo-auto/free` 的 `enabled: true`。
3. 客户端使用本地网关地址和模型 `auto`，由路由器选择 Kilo。
4. 如遇限流或服务不可用，等待网关切换其他可用服务商。

Kilo 适合希望快速开始、无需单独注册 API Key 的用户。免费服务仍可能有额度、并发或可用性限制。

### 6.2 ManaiAPI：注册后使用，GPT5.6 价格约为官方的 50%

ManaiAPI 需要完成注册或授权后使用。配置步骤：

1. 中文用户访问 `https://manai.cc`，英文用户访问 `https://vaneworker.com`。
2. 完成注册/登录和 API 授权流程。
3. 在管理端启动 ManaiAPI 授权，或在 `providers.manai` 中填写授权后得到的 `api_key` 和 `base_url`。
4. 启用 ManaiAPI 及目标模型，例如 `gpt-5-6-luna`。
5. 用管理端测试模型，确认可用后再让 `auto` 路由到它。

当前配置预置了 GPT5.6 兼容模型条目。价格说明应表述为“当前产品说明约为官方价格的 50%，实际以 ManaiAPI 页面和账户结算为准”，不要承诺固定价格。

### 6.3 Nvidia：免费额度，需要 API Key

Nvidia 提供可使用的免费额度/模型，但需要用户创建或填写 API Key。设置方法：

1. 打开 `http://127.0.0.1:12310/nvidia-api-key-tutorial?lang=zh`。
2. 按页面说明申请 Nvidia API Key。
3. 在管理端 Nvidia 设置中填写 Key 并启用服务商。
4. 确认模型（例如 `nauto`）已启用。
5. 用“测试模型”验证连接，再使用 `model: auto`。

API Key 属于敏感凭据，不要写入聊天记录、日志、截图或提交到代码仓库。

### 6.4 DeepSeek Web：绑定 Web 账号，使用 Web 免费额度

DeepSeek 服务通过 Web 账号绑定，不是普通的独立 API Key 申请流程。设置方法：

1. 在管理端打开 DeepSeek Web 连接/绑定流程。
2. 按页面提示登录 DeepSeek Web 账号并完成授权。
3. 等待本地 DeepSeek2API 服务启动并通过健康检查。
4. 确认 `deepseek-chat` 模型可用。
5. 使用 `model: auto`，网关会在健康且允许的候选中进行路由。

DeepSeek Web 的免费额度、账号状态、登录会话和上游可用性由 DeepSeek Web 控制；出现 502、空流、登录过期或额度耗尽时，应先查看服务状态和绑定状态，不要直接断言是本地协议错误。

### 6.5 服务商选择建议

| 需求 | 优先选择 |
| --- | --- |
| 不想注册、希望免费开始 | Kilo |
| 希望使用 GPT5.6 且成本较低 | ManaiAPI |
| 有 Nvidia 账号并希望使用免费额度 | Nvidia |
| 已有 DeepSeek Web 账号和免费额度 | DeepSeek Web |
| 敏感内容、离线或本机记忆处理 | 本地 Ollama |

---

## 7. 路由、模型和故障排查

- `model: auto`：使用网关自动路由，是推荐的默认方式。
- 显式模型名：可请求某个公开模型；如果该模型当前没有可路由候选，网关会按统一规则回退到 `auto`，只有 `auto` 也没有候选时才失败。
- 路由会检查服务商启用状态、模型启用状态、认证、允许清单、熔断、容量和协议类型。
- `GET /v1/models`：查看当前实际可路由的公开模型；不要仅根据静态配置判断模型在线。
- `GET http://127.0.0.1:12310/healthz`：检查管理服务健康状态。
- `GET http://127.0.0.1:12310/api/providers/availability`：查看服务商可用性。
- `GET http://127.0.0.1:12310/api/request-logs`：查看请求元数据和失败线索；不要复制其中的 Token、Cookie、Authorization 或完整敏感 Prompt。

常见判断：

1. **连接失败**：先确认网关进程和 `12320` 端口是否监听。
2. **401**：检查 API Key 是否与当前配置的 `router.api_key` 一致，以及认证头是否正确。
3. **404/协议不匹配**：检查是否把 Chat、Responses、Messages 的 URL 和请求体混用了。
4. **没有可用模型**：检查供应商启用、凭据、模型启用、服务状态和额度。
5. **上游 502/空流**：区分本地网关协议错误和供应商/上游账号、网络、额度问题。

---

## 8. 配置更新规则

所有配置更新应遵循乐观锁流程：

1. `GET http://127.0.0.1:12310/api/config` 获取最新配置。
2. 读取返回的 `revision`。
3. 只修改需要变更的字段。
4. `PUT /api/config`，请求体使用：

```json
{
  "expected_revision": 108,
  "config": {}
}
```

其中 `config` 应是完整的修改后配置对象，而不是只提交一个局部字段。如果返回 `409 Conflict`，重新读取配置并重试。不要手工伪造未在后端 schema 中定义的配置字段。

---

## 9. Agent 回答用户的推荐话术

### 用户问“这是什么”

> VaneworkerGW 是本机大模型网关。你只需把 Agent 指向本机的一个地址，它就能统一使用本地模型、Kilo、ManaiAPI、Nvidia 或 DeepSeek Web，并自动处理模型路由、协议转换和故障切换。

### 用户问“为什么要装本地模型”

> 本地模型可以在电脑上完成快速响应、记忆提取和记忆检索，敏感内容不必发送到云端；代价是需要占用数 GB 或更多内存和磁盘。你也可以不安装本地模型，直接使用已配置的云端服务商。

### 用户问“记忆有什么用”

> 记忆会保存对未来有帮助的偏好、项目事实和工作上下文，并在新问题中检索相关内容，让 Agent 少问重复问题、延续上下文。它不是完整聊天记录，也不是模型训练；敏感信息会按规则脱敏，并且记忆可以查看、修改和删除。

### 用户问“我该用哪个接口”

> 普通 OpenAI SDK 用 `/v1/chat/completions`；Codex 或 Responses 客户端用 `/v1/responses`；Claude Code 或 Anthropic 客户端用 `/v1/messages`。三者都使用 API Key `vaneworker-gw-local-key` 和模型 `auto`。

### 用户问“哪个服务商最好”

> 想免费直接开始可选 Kilo；想使用 GPT5.6 且控制成本可注册 ManaiAPI；有 Nvidia 免费额度可配置 Nvidia；已有 DeepSeek Web 账号可绑定 DeepSeek。对隐私和本地记忆要求高时安装 Ollama。本地和云端可以混合使用，不必只选一个。
