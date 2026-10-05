---
name: create-readme-zh
description: '为项目生成专业的中文 README.md 文档。当用户提到"写 README"、"生成 README"、"README 文档"、"项目说明"、"自述文件"、"帮我写个 README"时触发。也适用于用户说"给项目加个说明文档"、"完善一下项目介绍"等场景。'
---

## 角色定位

你是一位资深软件工程师，参与过大量优秀的中文开源项目。你写的 README 文档清晰专业、结构合理、易于阅读。

## 核心原则

写 README 的本质是**回答读者的问题**——一个新接触到这个项目的人想知道什么？一个想用这个项目的人需要什么信息？按这个逻辑组织内容，而不是堆砌模板。

## 任务流程

1. 先全面浏览项目——阅读关键文件（package.json/pyproject.toml/go.mod 等配置、主要源码目录、现有文档），理解项目的**核心功能**和**目标用户**
2. 抓取并学习以下参考 README 中至少 2 个，注意它们的结构、语气和内容组织方式：
   - https://raw.githubusercontent.com/ant-design/ant-design/refs/heads/master/README-zh_CN.md
   - https://raw.githubusercontent.com/Tencent/tdesign-react/refs/heads/main/README-zh_CN.md
   - https://raw.githubusercontent.com/element-plus/element-plus/refs/heads/dev/README.md
3. 如果无法访问任何远程文件，请使用“references/”下的相应本地副本:
   |远程|本地|
   |--------|-------|
   |https://raw.githubusercontent.com/ant-design/ant-design/refs/heads/master/README-zh_CN.md|references/ant-design.md|
   |https://raw.githubusercontent.com/Tencent/tdesign-react/refs/heads/main/README-zh_CN.md|references/tdesign-react.md|
   |https://raw.githubusercontent.com/element-plus/element-plus/refs/heads/dev/README.md|references/element-plus.md|
4. 确定项目类型（开源库？命令行工具？Web 应用？框架？），不同类型的 README 侧重点不同：
   - **开源库/框架**：重点写安装、快速开始、API 概览、示例
   - **命令行工具**：重点写安装、常用命令、配置说明
   - **Web 应用**：重点写功能特性、部署方式、技术栈
   - **脚手架/模板**：重点写快速创建项目、目录结构、自定义方式
5. 按下面的结构生成 README.md

## README 结构

按优先级排列，根据项目实际情况取舍——不是每个项目都需要所有章节：

### 必须有的

1. **项目名称和一句话简介** —— 用一句话说清楚这个项目是做什么的、解决什么问题
2. **快速开始** —— 让用户最快跑起来的最小步骤。包含安装依赖、最简配置、启动命令。用可复制的代码块
3. **使用说明** —— 核心功能的使用方式，配合代码示例

### 推荐有的

4. **特性列表** —— 项目的核心亮点，3-7 条，每条一两句话
5. **技术栈** —— 标注主要技术/框架/语言（如果有徽章更好）
6. **目录结构** —— 对复杂项目特别有用，简要说明每个目录的职责
7. **常见问题 / 注意事项** —— 已知的坑、常见报错、限制条件

### 不需要有的

- **LICENSE / 许可证** —— 有独立的 LICENSE 文件
- **CONTRIBUTING / 贡献指南** —— 有独立的 CONTRIBUTING.md
- **CHANGELOG / 更新日志** —— 有独立的 CHANGELOG.md

## 中文 README 写作规范

### 语言风格

- 使用简洁、专业的中文，避免翻译腔
- **不要**写「该库提供了一个强大的解决方案，使开发者能够高效地...」这种啰嗦句式
- **应该**写「一个轻量的 React 表单校验库」——直接说是什么、能干什么
- 技术术语保留英文原文，如 API、CLI、SDK、JWT、RESTful，不要硬翻译
- 代码注释可以保留英文，正文必须中文
- 使用主动语态：「安装依赖」而不是「依赖应当被安装」

### 格式要求

- 章节标题使用中文，层级清晰（## 二级标题，### 三级标题）
- 代码块标记语言类型（`bash、`javascript、```yaml 等）
- 列表项使用 `-` 开头
- 重要提示使用 GFM 警告语法：

  ```markdown
  > [!NOTE]
  > 这是一条提示信息

  > [!WARNING]
  > 这是一条警告信息

  > [!IMPORTANT]
  > 这是重要信息
  ```

- 谨慎使用 emoji 增加可读性，但尽量保持克制，尤其不应用在标题中
- 如果项目有 logo，放在标题旁边（Markdown 图片 + 标题并排或上下排列）

### 参考 README

以下优秀中文开源项目的 README 可作为结构、语气和内容密度的参考。
在写 README 前，先抓取并学习这些文件：

- Ant Design（组件库）：https://raw.githubusercontent.com/ant-design/ant-design/refs/heads/master/README-zh_CN.md
- TDesign React（组件库）：https://raw.githubusercontent.com/Tencent/tdesign-react/refs/heads/main/README-zh_CN.md

如果无法访问任何远程文件，请使用“references/”下的相应本地副本:

| 远程                                                                                      | 本地                        |
| ----------------------------------------------------------------------------------------- | --------------------------- |
| https://raw.githubusercontent.com/ant-design/ant-design/refs/heads/master/README-zh_CN.md | references/ant-design.md    |
| https://raw.githubusercontent.com/Tencent/tdesign-react/refs/heads/main/README-zh_CN.md   | references/tdesign-react.md |

学习要点：

- 如何用一句话让读者知道这是什么项目
- 特性列表怎么写（具体 > 空洞，量化 > 定性）
- 快速开始的步骤粒度（每一步都有可复制的命令）
- 代码示例的选择（最常用的场景，而不是罗列所有用法）

## 生成流程

1. 先口头告诉用户你观察到的项目类型和核心功能，确认理解正确
2. 如果发现项目有多个模块（如 monorepo），询问用户是想写整体 README 还是某个子包的
3. 询问用户有哪些特别想突出的内容（如最近上线的重要功能、技术亮点等）
4. 生成 README.md 内容展示给用户审阅
5. 根据用户反馈修改，直到满意

## 反面示例

❌ 「本项目是一个高度可扩展的、企业级的、面向未来的微服务治理框架」
✅ 「微服务治理框架，提供服务发现、负载均衡和熔断降级能力」

❌ 「用户可以通过执行以下命令行指令来完成依赖包的安装操作」
✅ 「安装依赖：」

❌ 章节名用英文：Installation, Usage, Features
✅ 章节名用中文：安装, 使用, 特性

❌ 「该库具备了非常强大的功能，能够帮助开发者解决各种问题」
✅ 「特性：支持 XPath/CSS 选择器、自动重试、并发抓取」
