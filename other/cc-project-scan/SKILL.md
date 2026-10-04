---
name: project-scan
description: 扫描当前仓库并生成或更新项目级 AGENTS.md / README.md / 全套脚手架文件（restart.sh、ignore、Dockerfile、docker-compose），适用于显式 project-scan、项目认知初始化或刷新项目级 Codex 上下文的场景。
---

# Project Scan

当用户明确要求 `project-scan`、扫描项目、生成项目级 `AGENTS.md`、生成或刷新 `README.md`，或刷新项目级 Codex 上下文时，使用本技能。

不要用于：

- feature 开发或 bug 修复
- 无确认地覆盖已有 `AGENTS.md`、`README.md`、`Dockerfile` 或脚本

## 必须生成的文件清单

扫描结束后，默认按以下清单一次性补齐项目脚手架（已存在的逐个询问"覆盖 / 跳过 / 增量更新"）：

| 序号 | 文件 | 用途 |
|------|------|------|
| 1 | `AGENTS.md` | 项目级 Codex 上下文 |
| 2 | `README.md` | 项目说明 |
| 3 | `restart.sh` | 前后端打包 + 启动脚本 |
| 4 | `.claudeignore` | Claude Code 忽略 |
| 5 | `.geminiignore` | Gemini CLI 忽略（内容复制自 `.claudeignore`） |
| 6 | `.gitignore` | Git 忽略 |
| 7 | `.dockerignore` | Docker 忽略 |
| 8 | `Dockerfile` | 容器构建 |
| 9 | `docker-compose.yml` | 容器编排 |

清单不可缩减；与 Claude `/project-scan`、Cursor 同名命令的产出对齐。

## 核心方式

1. 先扫描仓库中的关键信号文件和目录，区分"明确识别"的事实与"基于结构的推断"。
2. 默认确保项目级 `.codex/tasks/`、`.codex/tasks/archived/`、`.codex/templates/` 存在；若项目根目录写入触发权限边界，先走平台审批，不静默跳过。
3. 读取根目录现有 `AGENTS.md`、`README.md`、`.claude/CLAUDE.md`，并复用 `cc-project-init/assets/AGENTS.project.md` 作为 `AGENTS.md` 模板来源。
4. 先输出扫描摘要（含技术栈识别表 + 文件存在情况表），再追问 3-5 个关键问题：项目一句话描述、是否生成全套脚手架、已存在文件的处理策略（覆盖 / 增量 / 跳过）、Docker 暴露端口、API 契约确认。
5. **AGENTS.md / README.md 写入策略**：
   - 不存在 → 基于模板生成
   - 已存在且包含 `<!-- AUTO:* -->` 区块 → 优先增量更新自动区块，保留手写内容
   - 已存在但无自动区块 → 必须先让用户选择"首次全量重建 / 追加自动区块 / 跳过"
6. **脚手架文件写入策略**（restart.sh / ignore / Dockerfile / docker-compose）：
   - 不存在 → 从 `cc-project-init/assets/` 选模板按技术栈渲染后落盘
   - 已存在 → 询问"覆盖 / 跳过"，不静默覆盖
   - `.geminiignore` 内容必须与 `.claudeignore` 保持一致
7. `restart.sh` 落盘后必须 `chmod +x`。
8. 模板选择规则参见 `cc-project-init/references/template-selection.md`；忽略文件内容规范参见 `references/scaffold-files.md`。
9. 完成后输出摘要：已生成文件、已跳过文件、已补齐的 `.codex` 骨架，以及仍需用户补充的项目事实。

## 协作约束

- 项目级 `AGENTS.md` 模板资产复用 `cc-project-init/assets/AGENTS.project.md`
- 脚手架模板复用 `cc-project-init/assets/`（`restart-go.sh.tmpl`、`Dockerfile-go.tmpl`、`docker-compose-*.yml.tmpl`、`gitignore-go.tmpl`、`dockerignore.tmpl` 等）
- `README.md` 生成和更新遵循 `references/readme-update.md`
- 后续 feature 任务持久化依赖 `new-feature`
- 若涉及接口契约总结或列表/分页/筛选结构判断，遵循 `cc-api-contract-safety` 的方式，不臆测响应结构

## 输出要求

- 明确区分"扫描识别"与"待确认项"
- 明确说明每个文件采用"新建 / 增量更新 / 首次全量重建 / 追加自动区块 / 覆盖 / 跳过"中的哪一种
- 若补齐了 `.codex/tasks/`、`.codex/tasks/archived/`、`.codex/templates/`，必须明确说明
- 若已有文件用户选择跳过，要说明后续风险
- 若接口契约无法从代码或文档确定，在 `AGENTS.md` 中标注"待用户确认"，不要伪造规范
- 若无法可靠确认启动方式、端口、部署方式或许可证，`README.md` 中必须标注"待确认"，不要编造命令
- 若仓库无 `Cargo.toml`、`go.mod`、`pom.xml`、`package.json` 之一可推断技术栈，必须先和用户确认目标技术栈，再选模板，避免按错栈生成脚手架

## 按需展开

- 扫描项：`references/scan-checks.md`
- 自动区块：`references/agents-blocks.md`
- 重建策略：`references/rebuild-strategy.md`
- README 更新：`references/readme-update.md`
- 脚手架文件清单与忽略文件规范：`references/scaffold-files.md`
- 模板选择：`cc-project-init/references/template-selection.md`
