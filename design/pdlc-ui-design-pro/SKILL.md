---
name: pdlc-ui-design-pro
description: UI/UX 专业设计（PDLC 集成层，依赖 ui-ux-pro-max）
argument-hint: <功能描述 | 设计目标>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: design
produces:
  - docs/02_design/ui-ux/**
requires: []
next_step: null
terminal_state: null
---

# UI/UX 专业设计（PDLC 集成层）

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

本命令是 PDLC 的 UI 设计集成点，负责 PRD 守卫、PDLC 文档结构管理、以及调用设计智能引擎。
优先调用 `ui-ux-pro-max` 开源 skill（67 种风格 / 161 款配色 / 57 组字体搭配 / 161 行业推理规则），skill 未安装时自动启用内置流程。

---

## PDLC 前置检查（必须执行，不可跳过）

1. 从用户输入中提取功能名称关键词
2. 在 `docs/01_requirements/prd/` 目录下搜索对应 PRD 文档
3. **未找到** → 立即停止并输出：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的 PRD 文档。
   UI 设计必须基于已有的 PRD。请先运行：
   👉 /pdlc-prd <需求描述>
   ```
4. **找到** → 提取功能ID，读取 PRD 内容；同时读取（若存在）：
   - `docs/02_design/api/` 下相关 API 设计文档
   - `docs/02_design/ui-ux/` 下已有 UI 设计文档
   - `docs/02_design/ui-ux/design-system/tokens.md`（项目 Token 规范）

---

## 设计引擎选择

按如下优先级检测 ui-ux-pro-max skill 是否可用：

| 安装范围 | 检测路径 |
|------|------|
| 项目级 | `.claude/skills/ui-ux-pro-max/scripts/search.py` |
| 全局   | `~/.claude/skills/ui-ux-pro-max/scripts/search.py` |

按顺序检测上述路径，将第一个找到的路径记为 `$UIPM_SCRIPT`。

### ✅ 路径 A：ui-ux-pro-max skill 可用（推荐）

> 此路径适用于已通过 `uipro-cli` 安装了 ui-ux-pro-max 的用户。
> 安装方法：`npm install -g uipro-cli && uipro init --ai claude`

**第一步：生成设计系统**

从 PRD 中提取：产品类型、行业、关键词、技术栈，然后运行：

```bash
python3 $UIPM_SCRIPT "<产品类型> <行业> <关键词>" \
  --design-system --persist -p "<项目名称>"
```

- 输出保存到 `design-system/MASTER.md`（全局设计规范）
- 如有具体页面，追加 `--page "<页面名>"` 生成页面级覆盖文件

**第二步：补充领域搜索（按需）**

```bash
# 获取动效 / 无障碍最佳实践
python3 $UIPM_SCRIPT "animation accessibility" --domain ux

# 获取技术栈特定最佳实践（可选値见下表）
python3 $UIPM_SCRIPT "<关键词>" --stack <栈名>
```

| 栈名 | 适用场景 |
|------|---------|
| `html-tailwind` | Tailwind CSS（默认） |
| `react` | React / Vite |
| `nextjs` | Next.js |
| `vue` | Vue 3 |
| `shadcn` | shadcn/ui |
| `react-native` | React Native |
| `flutter` | Flutter |
| `swiftui` | iOS SwiftUI |

**第三步：整合为 PDLC 设计文档**

基于 skill 输出，结构化写入以下文件：

| 文档 | 路径 |
|------|------|
| UI 主文档（线框图 + 交互规范） | `docs/02_design/ui-ux/<功能ID>-<功能名>-ui.md` |
| 设计 Token | `docs/02_design/ui-ux/design-system/tokens.md` |
| 组件目录 | `docs/02_design/ui-ux/design-system/components.md` |

所有文档顶部必须包含 PDLC 追溯头：
```markdown
<!-- PDLC-TRACE -->
<!-- 功能ID: <功能ID> -->
<!-- 功能名称: <功能名> -->
<!-- 阶段: 设计 -->
<!-- 前置文档: docs/01_requirements/prd/<功能ID>-<功能名>-prd.md -->
```

---

### 🔄 路径 B：内置流程（skill 未安装时自动降级）

> 自动降级路径，功能完整但不包含 67 种风格智能推荐。

**未检测到 skill** 时输出提示后继续：

```
ℹ️  ui-ux-pro-max skill 未安装，使用内置设计流程。
   安装后可获得 67 种风格 / 161 款配色 / 57 组字体搭配的智能推荐：
   npm install -g uipro-cli
   uipro init --ai claude
```

**技术栈探测**

扫描 `frontend/` 目录，读取 `package.json`，检测：
- 框架：Next.js / React / Vue 3 / Nuxt / 微信小程序 / 通用
- 样式：Tailwind / CSS-in-JS / CSS Modules / 预处理器
- 组件库：Ant Design / Element Plus / MUI / shadcn/ui / Vant / 自建

输出探测结果后继续。

**产出三类文档**（路径与路径 A 相同）：

**1. UI 主文档**（`docs/02_design/ui-ux/<功能ID>-<功能名>-ui.md`）

- 用户旅程图（文本箭头格式）
- 每个页面的 ASCII 线框图（含正常态 / 加载态 / 错误态 / 空状态）
- 交互行为规范表（触发条件 → 行为 → 反馈）
- 响应式断点说明（Web：mobile < 768px / tablet 768-1023px / desktop ≥ 1024px）

**2. 设计 Token**（`docs/02_design/ui-ux/design-system/tokens.md`）

提取并标准化：颜色 Token（品牌色 / 语义色 / 中性色）、字体 Token（字号 / 行高 / 字重）、间距 Token（4px 基准）、圆角 / 阴影 / 动效 Token。

**3. 组件目录**（`docs/02_design/ui-ux/design-system/components.md`）

每个组件含：变体矩阵（variant × size × state）、Props 定义、无障碍规范、动效说明。

**技术栈自适应代码骨架**

基于探测结果，在 `frontend/.../src/` 下生成：
- 页面组件骨架（仅含类型和结构，业务逻辑填 `// TODO`）
- CSS Token 变量文件（`tokens.css`）
- TypeScript 类型定义（`types/<功能名>.ts`）
- API 服务层骨架（`services/<功能名>Api.ts`）

支持代码格式：React/Next.js + Tailwind → TSX；Vue 3 → `.vue` SFC；小程序 → wxml/wxss/ts；未识别 → 通用伪代码骨架。

---

## 完成报告

所有内容完成后，输出：

```
✅ UI/UX 设计完成

设计引擎: ui-ux-pro-max skill / 内置流程
产出文件:
  📄 docs/02_design/ui-ux/<功能ID>-<功能名>-ui.md
  🎨 docs/02_design/ui-ux/design-system/tokens.md
  🧩 docs/02_design/ui-ux/design-system/components.md
  💻 frontend/.../src/<相关文件列表>

下一步:
  /pdlc-tdd <功能名>        ← 编写测试（可引用类型文件）
  /pdlc-implement <功能名>  ← 实现业务逻辑（填充 TODO）
```

---

设计目标: $ARGUMENTS

<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->

**本命令的 handoff 输出：**

```
✅ UI/UX 专业设计文档 完成
📦 产出：docs/02_design/ui-ux/<功能ID>-<功能名>-ui.md
👉 下一步：（本次流程结束，无后续）
```
