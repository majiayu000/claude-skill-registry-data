---
name: apifox-cli
description: 通过 Apifox CLI 管理 Apifox 项目资源。触发场景：运行接口自动化测试/测试套件，查询/创建/更新/删除接口、环境、Schema、Mock、分支等项目资源，导入导出 API 文档，查看测试报告，管理 Runner、定时任务、通知等 CI/CD 配置。CLI 输出为结构化 JSON，常含 agentHints.nextSteps；所有命令支持 --help。
---

# Apifox CLI

用 Apifox CLI 完成用户请求；不要凭记忆拼 payload，优先让 CLI 的 `--help`、`cli-schema`、`cli-schema validate`、`agentHints.nextSteps` 驱动下一步。

## 新会话检查

- 首次处理 Apifox CLI 任务时，先轻量确认 CLI 可用：`apifox --version`、`apifox --help`。
- 如果 `apifox` 不存在或无法输出版本，先安装 CLI：`npm i -g apifox-cli@latest --registry=https://registry.npmmirror.com/`。
- 安装后执行 `apifox login --with-token <TOKEN>` 登录。API 访问令牌可在 Apifox 客户端或网页端「用户头像 → 账号设置 → API 访问令牌」创建。
- 不要每次默认升级；只有命令返回版本过低/unknown command/参数缺失疑似旧版导致，或用户任务依赖新能力时，才建议升级。

## 基础用法

```bash
apifox --help
apifox <command> --help
apifox <command> <subcommand> --help
```

常用全局参数：

```text
--project <projectId>     项目 ID
--branch <branchName>     分支名；纯数字值兼容旧 branchId
--access-token <token>    覆盖当前登录 token
--api-base-url <url>      私有部署地址
```

## 登录与项目

- 未登录时让用户提供 API 访问令牌，执行：`apifox login --with-token <TOKEN>`。
- Apifox CLI 的鉴权凭证存在 `~/.apifox/config.toml`；不要把 token 打印到日志、提交到仓库或写进普通聊天摘要。
- 如果用户未指定项目，先查看当前工作区是否存在 `.apifox/settings.json`；如其中有常用默认 `projectId`，优先使用该项目。
- 项目 ID 可推荐用户从「项目设置 - 基本设置 - 项目 ID」获取；或先执行 `apifox project list`，给用户确认需执行命令的目标项目。
- 写入任何本地配置文件前先询问用户。

## 写入标准流程

强制：执行 `create` 或 `update` 命令前必须先获取完整的资源定义和数据格式，并在正式执行前通过 `cli-schema validate` 校验写入准确，具体流程：

1. 查对应资源执行命令的 JSON schema：`apifox cli-schema get <schemaKey>`
2. 生成资源的 JSON 数据文件。
3. 校验：`apifox cli-schema validate <schemaKey> --file <path>`
4. 只有 `validate` 无误后，才执行真实  `create` 或 `update` 命令。

命令输出结果后，优先读取 JSON 输出里的 `agentHints.nextSteps` 继续执行或恢复。

## CLI 事实优先

- 具体命令、参数、schema key 以当前 CLI 输出为准：`apifox <command> --help`、`apifox cli-schema list`、`agentHints.nextSteps`。
- 如本 skill 与当前 CLI 输出不一致，以当前 CLI 输出执行，并同步修正本 skill 的事实性描述。

## CLI 写入权限声明

- 执行写入被 AI（CLI 来源）权限限制时，若用户未声明，不要替用户选择，优先询问写入方式：开启目标分支的直接编辑权限，或在 AI 分支上编辑目标分支数据。
- 如用户需直接编辑主分支、迭代分支或通用分支数据，请用户在 Apifox 客户端 2.8.32+ 版本在「项目设置 - 功能设置 - AI 功能设置 - 外部 AI 编辑权限」开启直接编辑权限的开关。
- 如用户选择 AI 分支，流程是：
  step1：创建 AI 分支并指定来源分支；
  step2：按实际需要导入（pick-to）来源分支资源；
  step3：按用户需求编辑 AI 分支；
  step4：完成后，提醒用户确认是否发起合并请求或合并。
- 从 CLI 直接执行合并/合并请求时，要求来源分支和目标分支的直接编辑权限开关均已开启；否则请提醒用户先打开对应分支类型的权限开关，或直接在客户端手动触发合并。

## AI 分支说明

- AI 分支是给 AI/自动化修改项目资源的隔离分支，避免直接污染源分支。
- AI 分支若在 24 小时内与来源分支无差异，将自动归档。
- AI 分支初始为空，不会自动 clone 源分支资源；编辑/删除来源分支已有资源前，先导入到 AI 分支。
- AI 分支中新建资源无需先导入。
- AI 分支修改不会自动写回源分支；完成后必须让用户确认是否立刻合并或发起合并请求。
- 目标主分支受保护时（isProtected），优先走 `merge-request`，不要直接 `merge`。

## 必须询问用户

- 登录 token、本地配置写入、私有部署地址。
- 创建/切换 AI 分支、导入源分支资源到 AI 分支。
- 删除、归档、覆盖导入、批量更新等破坏性操作。
- 将 AI 分支改动 merge / merge-request 回源分支。
- 是否升级 CLI。

## 故障恢复

| 现象 | 处理 |
|------|------|
| 未登录 | `apifox login --with-token <TOKEN>` |
| 不知道项目 | `apifox project list` |
| 不知道命令参数 | `apifox <command> --help` |
| 参数或 schema 错误 | 先跑 `cli-schema get` / `cli-schema validate` |
| AI 写入受限 | 解释 AI 分支/权限开关，让用户选择 |
| 私有部署 | 加 `--api-base-url <PRIVATE_APIFOX_BASE_URL>` |
