---
name: project-init
description: 结构化新项目初始化工作流，适用于显式 project-init、仓库开荒、生成项目级 AGENTS.md 或按技术栈落基础脚手架文件的场景；不负责替用户无差别覆盖现有配置。
---

# Project Init

当用户明确要求 `project-init`、`cc-project-init`、初始化新仓库、生成项目级 `AGENTS.md`，或按技术栈补基础脚手架时，使用本技能。

不要用于：

- 已成熟项目上的大规模重写
- 代替 feature 开发或 bug 修复
- 无确认地覆盖已有 `AGENTS.md`、`Dockerfile` 或脚本
- 为 Claude/Gemini 生成专属配置文件
- 默认生成 `README.md` 这类扫描型项目文档；需要生成或刷新 README 时使用 `project-scan`

## 核心方式

1. 先读取仓库现状，判断是不是空仓库、样板仓库，还是已有部分脚手架。
2. 优先从现有文件推断技术栈，再只问缺失的关键信息：项目描述、启动方式、数据库迁移、额外约定、是否需要脚手架文件。
3. 需要项目级说明时，以 `assets/AGENTS.project.md` 为起点生成仓库根目录 `AGENTS.md`，内容聚焦项目特定约定，不重复用户级全局规则；模板中的 `AUTO:*` 区块可供后续 `project-scan` 增量刷新。若项目包含 Java 代码，需遵守项目署名约定：文档和代码署名统一使用 `wwj`，新增 Java 文件或补齐文件头注释时使用 `@author wwj`。
4. 默认同时初始化项目级 `.codex/` 最小骨架：`.codex/tasks/`、`.codex/tasks/archived/`、`.codex/templates/`，保证后续 `new-feature` 可直接持久化任务；若这些目录已存在，则只补缺失项，不整目录覆盖。若项目根目录本身没有写权限，必须先触发平台原生审批流程；只有审批后仍失败，才说明当前会话无法在该项目内初始化骨架。
5. 只有用户明确要创建或补齐额外脚手架时，才从 `assets/` 选择对应模板；不要默认把所有模板都写进仓库。
6. 如果目标文件已存在，先比较差异并说明保留/合并策略，避免整文件覆盖。
7. 若用户预期生成 `README.md`、技术栈摘要、目录结构或快速开始说明，明确说明这是 `project-scan` 的职责，并建议继续执行 `$project-scan`。
8. 完成后说明创建了哪些文件、哪些模板没有使用，以及后续建议。

## 资源选择

- 项目级说明模板：`assets/AGENTS.project.md`
- 项目级 `.codex` 骨架：`assets/codex-skeleton/`
- Go/Docker/compose/重启脚本模板：按需从 `assets/` 选择
- 具体选择规则：`references/template-selection.md`

## 输出要求

- 先说明识别到的项目形态和技术栈假设
- 只为用户确认过的文件落盘
- 新建文件默认可直接用，但保留最少必要占位符
- 明确指出哪些内容仍需用户补充或替换
- 若用户已执行 `tools/sync-config.sh`，必须明确说明项目级 `.codex` 骨架仍需在目标项目根目录内由 `project-init` 或 `new-feature` 实际落盘，不要把用户级 `~/.codex/project-template/.codex/` 当成已完成的项目初始化
