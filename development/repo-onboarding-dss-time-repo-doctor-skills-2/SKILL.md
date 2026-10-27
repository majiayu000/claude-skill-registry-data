---
name: repo-onboarding
description: "Understand an unfamiliar software repository before making changes. 在修改代码前理解一个陌生软件仓库。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Repo Onboarding

Use this skill to understand an unfamiliar repository before editing code.

## Safety Boundary

- Read-only by default.
- Do not modify files.
- Do not run commands unless the environment and user request allow it.
- Separate facts from assumptions.

## Workflow

1. Inspect repository metadata and top-level structure.
2. Identify the language, framework, package manager, and build tools.
3. Read the relevant README, manifest, config, CI, test, and plugin files; reuse current evidence and follow only links needed to establish the map, rather than exhaustively reading every directory.
4. Identify entry points, core modules, scripts, and validation commands.
5. Identify risky areas such as public interfaces, shared utilities, authentication, data migrations, generated files, release scripts, or build config.
6. Produce the practical onboarding map using the output contract.

# Output Format

Default `fast` map:

1. Project summary and stack with evidence.
2. Entry points, core flow, relevant directories/files and reading order.
3. Run/validation commands with sources; separate documented commands, executed results and unknowns. State once if nothing ran; a script definition is not a passed check.
4. Risks, material unknowns and one next step.

Omit exhaustive inventories and empty sections. Without repository evidence, give the limitation and minimum needed input, not a guessed map. Requested detail or `standard`/`audit` expands directory/module roles, flow, reading order and validation evidence within scope; permissions stay unchanged.

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 仓库理解

用于在修改代码前理解一个陌生仓库。

## 安全边界

- 默认只读。
- 不修改文件。
- 除非环境和用户明确允许，否则不运行命令。
- 区分事实和推断。

## 工作流程

1. 检查仓库元数据和顶层目录结构。
2. 识别语言、框架、包管理器和构建工具。
3. 阅读相关 README、manifest、配置、CI、测试和插件文件；复用当前证据，只沿建立地图所需的关联继续阅读，不遍历读取全部目录。
4. 识别入口文件、核心模块、脚本和验证命令。
5. 识别风险区域，例如公共接口、共享工具、认证、数据迁移、生成文件、发布脚本或构建配置。
6. 按输出契约给出实用的仓库地图。

# 输出格式

默认 `fast` 地图：

1. 项目总结、技术栈及证据。
2. 入口、核心流程、相关目录/文件和阅读顺序。
3. 运行/验证命令及来源，区分文档命令、实际结果和未知项。未运行时统一说明一次，脚本定义不等于检查通过。
4. 风险、重大未知项和一个下一步。

省略完整目录清单及空章节。没有仓库证据时说明限制和最小所需输入，不猜测地图。用户要求详细信息或选择 `standard`/`audit` 时，在范围内展开目录/模块职责、流程、阅读顺序和验证证据，权限不变。
