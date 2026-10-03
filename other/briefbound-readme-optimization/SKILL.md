---
name: briefbound-readme-optimization
description: Use when the user asks to create, rewrite, or improve a repository README（优化 README、补仓库文档、开源准备、仓库简介）, or a repo lacks a usable README before handoff or release; analyzes manifests and source facts first, then produces an audience-appropriate Chinese-first README where every command and claim is traceable.
license: MIT
---

# Briefbound Readme Optimization

## 目标

以仓库事实为据，产出或改进"读者不读源码即可上手"的中文优先 README。按项目类型裁剪章节，绝不编造命令、依赖或功能。

## Briefbound task contract

- Context Boundary: 目标仓库的清单文件（package.json、pyproject.toml、go.mod、Cargo.toml、installer 脚本等）、目录结构、现有 README 与文档、LICENSE、git 远程与语言统计；不改代码逻辑。
- Output Contract: README.md（多语仓含 README.en.md）+ 逐节变更说明 + 事实溯源表（每条命令/功能 ↔ 来源文件）。
- Allowed Action: 读写 README 与文档文件；读取仓库任意文件取证；不执行安装、不改源码语义。
- Success Evidence: 安装与用法逐条可溯源且与清单一致；章节按类型模板完整；新读者不读源码可完成安装与首次运行。
- Stop Condition: 仓库无可用事实源、要求与事实冲突、或需要虚构功能才能满足。
- Route Out: 原任务 owner、`briefbound-diagram-design`（架构配图）、`briefbound-plain-talk`（行文风格）、`briefbound-development-cleanup`（验证后的真实残留）、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 README/文档面；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文、保留技术字面量；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 章节骨架（按类型裁剪）

通用顺序：标题+一行描述 → 徽章（可选、不超过 4 枚）→ 简介（是什么/为什么，3 行内）→ 安装 → 使用（可复制命令+最小示例）→ 目录结构（仅复杂仓）→ 贡献（仅开源协作仓）→ 许可证。

- **agent 技能包**：加技能目录（名称+一句话）、安装命令、路由/链动入口说明（参照本仓库 README 模式）。
- **脚本/工具合集**：每个入口脚本一段用法（命令、输入输出、一个示例）；清单中不存在的脚本不写。
- **网页/应用项目**：加截图位、技术栈表、本地开发步骤。
- **研究仓库**：加环境、数据、复现命令、结果引用。
- **多语仓库**：README.md 与 README.en.md 语义一致，中文为主版本。

## 证据驱动规则

1. 安装命令、依赖版本、入口脚本、功能描述必须来自清单文件、installer、docstring 或源码，逐条可溯源；**清单里没有的不得出现**。
2. 不确定的事实标注 `TODO(待核实)` 而不是编造；徽章只用可验证项（license、语言、star）。
3. 改进现有 README 先逐节对照事实：删除过时或虚构内容，保留仍然真实的用户内容与语气。

## 工作流

1. 读清单与目录结构，判定项目类型与受众。
2. 现有 README 基本可用 → 增强模式（保骨架、逐节修订）；缺失或严重失真 → 重写模式。按证据自行判断，不为此询问用户，汇报时说明所用模式与理由。
3. 按骨架生成内容，逐条建立溯源。
4. 自查验收判据：新读者不读源码能否完成安装与首次运行；答案必须是"能"。
5. 汇报遵循 plain-talk：改了什么、为什么、怎么验。

## 致谢

章节骨架改编自 [standard-readme](https://github.com/richardlitt/standard-readme)（MIT）；工作流改编自 NASA-AMMOS/slim 的 slim-readme（Apache-2.0）；证据驱动原则参考 Agensi readme-generator 的公开描述（无代码借用）。详见 [references/upstream.md](references/upstream.md)。
