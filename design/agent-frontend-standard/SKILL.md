---
name: agent-frontend-standard
version: 1.0.0
description: "agent 时代前端工程手册——写/评审前端代码(React/RN/Next/组件/样式/状态/前端测试)、建立或评审前端仓工程门禁、设计系统对接 AI 时加载。覆盖:设计系统即契约(token 语义/受限组件词表/lint 硬门)、类型端到端契约(生成客户端只读/typecheck 主反馈环/封 any 逃逸)、视觉验证环(a11y 树优先+截图双轨/迭代预算/回归重检)、前端测试分时门禁、gotcha 库(use client 幻觉/barrel file/任意值样式)。电在回路前端面:能下沉 lint/CI 的绝不写散文。Use when writing or reviewing frontend/UI code, wiring design systems for AI agents, or establishing frontend repo gates: components, styling, tokens, typed API clients, visual verification, frontend testing."
---

# Agent Frontend — 前端工程手册

> 姊妹篇：后端归 `agent-backend-standard`(hub)；Git 归 `git-workflow-standard`；护栏供给回路
> canonical = `cto-orchestration` 的 shock-in-the-loop 篇（电在回路/能电不文）。
> 本手册条目均有 2026 调研证据背书（Anthropic / Figma / Atlassian 等公开来源，二手数据已标注）。
> 铁律同 hub：**"In nearly 100% of cases the prompt will win over the guidelines"（Figma 实证）——
> 声明式规则是软的，只有编译器、lint=error 和 CI 是硬的。能电不文。**

## 1. 设计系统即 agent 契约

- **受限组件词表**：业务代码只准从少量 vetted DS primitives 组合，禁自由 CSS/裸 HTML 拼装。
  机制："LLM 不擅长一致发明，擅长查找"。
- **薄封装收窄 prop 面**：禁 app 直接 import 厂商组件库；wrapper 禁 `{...rest}` 透传——透传=把
  厂商全部 API 面暴露给 agent 猜。
- **token 语义标注是性价比最高的一招**：token 定义处写 role + **反用法**（"仅 destructive 操作；
  禁用于品牌强调"）。50 个设计系统审计只有 1 家写了 do-not-use——写了 agent 就稳定选对。
- **三条 lint 硬门（=error，warn 等于没有）**：
  1) tailwind `no-arbitrary-value`——agent 不知道你的 token 就会吐 hex/px，任意值=样式漂移主通道；
  2) `no-restricted-imports` 禁 legacy/厂商直连路径——agent 分不清 `ui/` 和 `legacy/`；
  3) 非法 prop 组合用 discriminated union 灭在类型层——"TS 编译器就是设计系统评审员"。
- **机器可查询 > 散文描述**：组件 API 给结构化形态（manifest/story/类型），使用规则才写 Markdown。
  格式即成本：JSON 组件元数据比散文省 ~80% token（Indeed 1056-prompt 实测，二手）。

## 2. 类型端到端契约

- **契约在 agent 编辑范围之外**：后端契约生成 client，生成物只读——"编不出不存在的 endpoint"。
  配对律：契约改动必须触发再生成（pairing 门），生成物手改必须被拦（starter hook ①②已落）。
- **typecheck 是 agent 主反馈环**：`tsc --noEmit` 的 file/line/col 五元组比测试堆栈更适合收敛；
  每轮都跑（tsgo 已把成本压到可每轮）。
- **封死逃逸口**：agent 会用 `any`/`as`/`@ts-expect-error` 把红变绿。type-coverage 阈值 +
  **抑制注释必须人类 override commit 才放行**。
- **认知边界**：类型错误是 agent 最会修的一类（也正因此 typecheck 绿≠正确）；逻辑错误修复率仅
  ~45% 且两轮后收益枯竭——正确性预算投给断言强度（mutation/oracle），别再收紧 tsconfig。

## 3. 视觉验证环

- **a11y 树优先、截图兜底（双轨不二选一）**：snapshot ~200-400 token/确定性/ref 精确；截图
  ~3000-5000 token/坐标脆——动画/图表/文案才用截图。axe 类 a11y 检查是少数客观可机验门
  （覆盖 ~57%，是门不是证明）。
- **迭代必须设预算上限**：视觉环 ≤5 轮、a11y ≤3 轮，超限熔断上报——无退出条件的 agent
  "要么跑死要么随机停"，迭代精化可能只烧成本零改善。
- **多轮视觉反馈会引发功能遗忘**（第 N 轮修好、第 N-3 轮坏了）——**视觉环必须配回归重检**：
  VRT 基线 diff / story interaction test 每轮全量复跑。这是 VRT 在 agent 环里的真正理由。
- **"没有 check 时 looks-done 是唯一停止条件"**：给 agent 的 UI 任务必须带可跑验证
  （story test / screenshot diff / typecheck+lint 组合），同北极星 doctrine。

## 4. 测试分时门禁

- PR 环内：typecheck + lint + 组件级测试（秒~分钟）；全量 E2E + VRT 夜间/pre-deploy。
- flaky："fix or quarantine, do not retry"——重试训练 agent 无视红灯。
- agent 写的测试 80.2% 无强断言（大样本）——前端同病：断言强度门（interaction test 必须有
  行为断言，不收快照即过的 change-detector）。
- 倒金字塔（E2E 优先）论证据链为空，不采。

## 5. Gotcha 库（hook 判不了，散文稍详）

- **RSC `use client` 幻觉**：agent 训练分布来自"一切在浏览器"的旧 React，会习惯性加
  `'use client'`——不报错、静默把子树拉过边界、膨胀 bundle、传染 imported children。
  review 时专项看新增的 `use client`。
- **barrel file（index.ts 桶）**：唯一有硬生产数据的架构负资产（Atlassian：去桶 build −75%/
  触发单测 −88%）；agent 顺手建桶要拦（lint no-barrel 或 review 项）。
- **agent 默认往训练先验的默认调色板靠**（`sky`/`blue`），对自定义 token 反而不稳——这正是
  no-arbitrary-value 必须 error 的原因。
- **凭空出现的循环/未要求的功能/被禁用删除的测试** = agent 作弊三红旗（Kent Beck），review
  checklist 常备。

## 6. 落地指针

- 全链已在某下游前端 starter 活体落地（生成 client 配对门 / 依赖边界 lint / token 漂移检查 /
  selfcheck pre-push+CI）——本章条目非纸上清单。
- 新前端仓建门顺序：typecheck → lint 三硬门 → 配对门（契约↔生成物）→ 组件测试 → VRT。
  每门带负探针（红一次再恢复），登记进仓 AGENTS.md 验证配方节。
