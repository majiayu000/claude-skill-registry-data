---
name: windows-app-workflow
description: Windows 桌面软件端到端开发工作流（主题无关、参数化）。适用场景：从零开始做一个新的 Windows 程序（.exe / 安装包 / 绿色版），具体主题每次不同、启动时注入。覆盖需求定义 → 技术选型与架构 → UI/UX 设计 → 工程地基 → 迭代实现 → 测试加固 → 打包签名发布 → 文档运维全流程。提炼自 agency-agents 仓库的 NEXUS 阶段流水线与 20+ 专家 agent。
---

# Windows 桌面软件开发工作流（主入口）

> 本工作流完全参数化：软件主题未定没关系，启动时注入「项目变量」，按 8 个阶段顺序执行，每阶段对应一个子 skill，可整体跑也可单独调用。

## 一、项目变量（每次启动新项目时填写）

| 变量 | 说明 | 示例 |
|---|---|---|
| `{{软件名称}}` | 产品名 | NoteVault |
| `{{一句话描述}}` | 为谁解决什么问题 | 本地加密的笔记管理工具 |
| `{{目标用户}}` | 主要使用者 | 需要保管敏感信息的 Windows 用户 |
| `{{核心功能}}` | 3–5 个核心功能 | 笔记编辑、全文搜索、加密、导出 |
| `{{时间线}}` | 时间预算 | 4 周 MVP |
| `{{团队规模}}` | 人力（1 人 = 你自己 + AI 兼任所有角色） | 1 |
| `{{发布渠道}}` | GitHub Releases / 官网直链 / MSIX / 微软商店 | GitHub Releases |
| `{{联网需求}}` | 纯本地 / 需要联网 / 需要账号同步 | 纯本地优先 |

## 二、流程总览（8 阶段 × 子 skill）

| # | 阶段 | 子 skill | 核心动作 | 质量门（不过不放行） |
|---|------|---------|---------|---------------------|
| 1 | 需求发现 | `01-requirements/` | 竞品速查、用户痛点、PRD、GO/NO-GO | PRD 完成且有 GO 决定 |
| 2 | 架构与选型 | `02-architecture/` | 运行时选型（Electron/Tauri/原生）、特权边界与 IPC 契约、ADR | 架构文档签核，选型有书面理由 |
| 3 | UI/UX 设计 | `03-ui-ux-design/` | 设计令牌、组件清单、亮暗主题、无障碍基线 | 设计系统落为代码可用的 tokens |
| 4 | 工程地基 | `04-foundation/` | Git 规范、CI 流水线、**签名基础设施先行** | CI 全绿 + 签名走通一次空壳发布 |
| 5 | 迭代实现 | `05-implementation/` | Sprint 循环、安全 IPC、足迹预算、代码审查 | 每个任务带证据过 QA |
| 6 | 测试加固 | `06-testing/` | 自动化测试、性能基准、无障碍审计、Reality Check | 证据化 READY 裁决（默认 NEEDS WORK） |
| 6+ | 安全加固 | `07-security/` | STRIDE 威胁建模、安全代码审查、密钥管理 | 威胁模型清零高危项 |
| 7 | 打包发布 | `08-packaging-release/` | 安装包、代码签名、自动更新、灰度发布 | 已签名构建 + 回滚演练通过 |
| 8 | 文档运维 | `09-docs-operations/` | README/用户文档、崩溃分诊、更新运营 | 文档覆盖核心场景 |

## 三、一键启动模板（复制后填变量即可）

```
启动 Windows App Workflow。

软件名称：{{软件名称}}
一句话描述：{{一句话描述}}
目标用户：{{目标用户}}
核心功能：{{核心功能}}
时间线：{{时间线}}
团队规模：{{团队规模}}
发布渠道：{{发布渠道}}
联网需求：{{联网需求}}

执行要求：
1. 按阶段 1→8 顺序执行，每个阶段开始前读取对应子 skill。
2. 每阶段结束必须通过质量门并给出证据；证据不足 = NEEDS WORK，不放行。
3. 签名与自动更新基础设施在第一个功能开发之前建好。
4. 所有跨阶段产出原样传递（不要摘要），后一阶段以前一阶段产出为输入。
```

## 四、全局铁律（来自各专家 agent 的硬性规则）

1. **证据优先**：任何"已完成 / 生产就绪"的结论必须附证据（截图、日志、测试输出）。默认立场是 NEEDS WORK，直到证据压倒性充分。首版实现通常需要 2–3 轮返工，一次通过是危险信号。
2. **签名先于功能**：代码签名证书 + 更新管道是发布阻塞项，第一天就建，不是上线前补。不签名的构建绝不发布。
3. **渲染进程是"有妄想症的浏览器标签页"**：一切 webview 内容视为不可信；IPC 是公共 API 面——窄动词、特权侧校验输入、绝不提供通用 `writeFile(path, data)` 式通道。
4. **离线是一等公民**：桌面用户期望在飞机上也能打开应用。本地优先数据 + 显式同步状态，优于转圈的白屏。
5. **足迹即功能**：冷启动、空闲内存、安装包体积是功能，写进 CI 预算，超标即失败。
6. **更新器是你拥有的最关键代码**：崩溃的应用只烦一个用户一次，坏掉的更新器会把所有用户永远困住。更新清单必须签名，灰度 1%→10%→100%，回滚路径必须演练过。
7. **尊重 Windows 平台约定**：任务栏/托盘行为、窗口控制按钮、快捷键（Ctrl 系）、文件关联、安装预期，按 Windows 标准来，"和我们的 Web 版一致"不是借口。
8. **原子提交 + 约定式提交**：`feat:` `fix:` `chore:` `docs:` `refactor:` `test:`，每个提交只做一件事、可独立回滚。

## 五、单人开发时的角色兼任表

1 人 + AI 的场景下，按此表轮流"戴帽子"（源 agent → 由谁执行）：

| 源 agent | 阶段 | 单人模式下 |
|---|---|---|
| Product Manager / Trend Researcher | 1 | AI 出初稿，你做最终取舍 |
| Software Architect / Desktop App Engineer | 2 | AI 出方案 + 权衡表，你拍板并记 ADR |
| UX Architect / UI Designer | 3 | AI 出 tokens 与组件规范 |
| DevOps Automator / Git Workflow Master | 4 | AI 直接生成配置 |
| Desktop App Engineer / Code Reviewer | 5 | AI 写 + 自审，你抽查 |
| Test Automation Engineer / Reality Checker | 6 | AI 跑测试，Reality Check 必须附证据 |
| AppSec Engineer | 6+ | AI 按 STRIDE 清单审 |
| Desktop App Engineer（分发方向） | 7 | AI 生成签名/打包脚本，你保管证书 |
| Technical Writer | 8 | AI 起草，你校对 |

## 六、来源映射（本 skill 包提炼自哪些 agent）

- `engineering/engineering-desktop-app-engineer.md` — 选型表、IPC 安全、签名/更新/灰度、足迹预算（核心来源）
- `engineering/engineering-software-architect.md` — ADR、架构模式选择、权衡思维
- `strategy/playbooks/phase-0 ~ phase-6` — 阶段划分、质量门、交接包机制（NEXUS 流水线）
- `product/product-manager.md` — PRD、RICE、North Star、路线图
- `design/design-ux-architect.md` / `design-ui-designer.md` — 设计系统、组件库、主题
- `engineering/engineering-devops-automator.md` / `engineering-git-workflow-master.md` — CI/CD、Git 规范
- `testing/testing-test-automation-engineer.md` / `testing-performance-benchmarker.md` / `testing-accessibility-auditor.md` / `testing-reality-checker.md` — 测试、性能、无障碍、证据化验收
- `security/security-appsec-engineer.md` / `security-secrets-credential-engineer.md` — 威胁建模、安全规则、密钥管理
- `engineering/engineering-i18n-engineer.md` / `engineering-technical-writer.md` — 多语言、文档
