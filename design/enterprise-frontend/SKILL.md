---
name: enterprise-frontend
description: >-
  约束驱动的企业级中后台前端规范执行器。凡企业级前端 / 中后台 / 管理端 / 控制台 /
  dashboard / admin console / workbench / enterprise frontend 的新建、扩展、迁移、审查——
  CRUD 页面、列表页、表单页、详情页、权限、菜单、路由、布局、页面设计、数据流、主题与
  设计 token、前端初始化、技术栈迁移、UI 迁移、一致性审查、前端代码审查——
  默认执行本规范硬约束清单，而非自由发挥；含 Ant Design Pro / ProComponents /
  ProTable / ProForm / Umi / Umi Max / React Query / map / GIS 前端场景。
  Use for any enterprise admin frontend work: admin dashboards, CRUD pages,
  forms, detail views, routing, menus, permissions, data layer, theming,
  migration, and consistency review. The spec is a hard-constraint checklist,
  not advisory reference material.
---

# 企业级前端约束规范（enterprise-frontend）

## Identity / Mission

本 skill 是**约束型规范执行器**：一切企业级中后台前端工作（新建 / 扩展 / 迁移 / 审查）
默认执行本规范的标准约束清单。规范是硬约束清单，不是参考建议——禁令一律硬执行，
约定跟随目标仓库真源；目标仓库的现实不构成放宽禁令的理由。

- **适用面**：通用企业中后台。地图 / GIS 为条件加载章节（见 References 路由表），
  非地图任务不读地图文档。
- **标准栈**（模式级，版本无关）：Umi Max 类元框架 + React + TypeScript strict；
  Ant Design + ProComponents；Tailwind CSS 类原子样式 + CSS-in-JS 主题 + CSS Modules 分层；
  框架路由与请求层；React Query 服务端状态；Biome + `tsc --noEmit` + Jest 质量门；
  ArcGIS SDK（仅地图场景，经唯一入口模块封装）。
- **表述纪律**：条文自洽，只讲模式不讲版本号、不讲来源仓库；token 默认值见
  `references/design-tokens.md`，随目标仓库真源裁决。

## Success Definition

任务完成 = 以下全部成立，缺一即未完成：

1. **禁令零违反**（B1–B7，全局硬执行）。ID 契约表见本文 References 层；
   完整禁令表（检查级 / 黑名单字面量 / 证据路径）唯一真源是 `references/engineering.md`。
2. **真源接线完整**：路由真源、导航真源、权限真源、query keys 真源、样式 token 真源
   五处同步，无平行体系（改真源，不复制默认值）。
3. **四态承载齐备**：每个数据驱动区块有加载 / 空 / 错误 / 禁用态的一致承载方案，
   禁「只有成功态」。
4. **质量命令通过**：lint（Biome）+ 类型检查（`tsc --noEmit`）+ 测试全绿。
5. **无越界断言**：完成判定以静态约束检查与质量命令为准；不以文档检查声称
   UI 视觉、交互或运行时效果实测通过。

## Workflow

1. **接收任务 → 判场景**（按序判定，命中即止）：
   1. 非地图 CRUD（列表 / 表单 / 详情 / 布局 / 接线）——默认场景；
   2. 地图 / GIS 场景（空间数据、图层、地图交互、地图资产）；
   3. 存量页面修改（目标仓库已有页面，小步改）；
   4. 规范审查（对既有前端做一致性审查）。
2. **按条件加载路由表读对应 references/ 文档**（见 References 层）；地图场景额外读
   两篇地图文档，非地图场景不读。
3. **设计推理（新页面 / 新功能必经）**：按 `references/design-reasoning.md` 的四步
   程序产出设计产物——页面形态、布局模式、卡片-内容组件组成（含四态方案）与真源
   接线增量；实现与 Review Loop 以此为对照基准。
4. **执行约束**：禁令（B1–B7）硬执行；token 与结构约定按 Decision Rules 分层裁决；
   每条新写代码可追溯到对应规范条文。
5. **Review Loop 自查**（见下）后交付；验收证据 = 命令输出，不是口头声明。

## Decision Rules

分层裁决（先定层级，再动手）：

| 层级 | 内容 | 裁决 |
| --- | --- | --- |
| 禁令与质量规则 | B1–B7、四态承载、质量命令、真源同步纪律 | **全局硬执行**，不因目标仓库现状让步 |
| token 与结构约定 | 色彩 / 圆角 / 高度 / 字号 / 间距、布局参数、目录组织 | **跟随目标仓库真源**：已有主题 / 路由 / 请求层 → 读其真源并沿用（改真源，不开平行体系）；新建项目无真源 → 用规范默认值（`references/design-tokens.md`） |
| 目标仓库自身规则 | 其 AGENTS / README / 约定文档 | 架构 / 主题 / 数据 / 权限约定优先于本规范的「跟随类」条款；**永不豁免禁令类条款** |

规则细目：

- 新建项目：全量按规范标准栈与默认 token 落地，不留「渐进适配」口子。
- 存量修改：最小完整变更；禁令面内的存量违规代码在触碰时顺手修正，不扩大战线。
- 冲突时序：目标仓库真源 > 规范默认值 > 通用直觉；禁令 > 一切仓库现实。
- 表述纪律：规范只讲模式不讲版本号；条文自洽，不引用外部仓库路径。

## Boundaries

- 只管**前端工程约束**：页面 / 组件 / 状态 / 样式 / 路由 / 质量。不做后端规范、
  不做 CI/CD 平台规范、不做移动端规范。
- 不替代目标仓库自身的 AGENTS / README 规则（优先级见 Decision Rules）。
- 不做生成页面的 with/without 对照评测、不做 UI 效果或 skill 效能实测；
  验证 = 静态约束检查 + 质量命令。

## Anti-Patterns

每条为规范明令禁止的反面模式（机制后果即判定依据）：

1. **独立 query key 前缀不共享 root** → invalidate 前缀匹配失联、联动失效。
2. **未声明例外的页面级滚动** → 内容壳滚动失控、高度链断裂。
3. **弹层放行清单漏配新路由** → 打开路由弹层静默失败；放行清单与路由表必须同步维护。
4. **独立 /login 路由页** → 登录入口发散、401 收敛断裂。登录入口收敛为首页弹层，
   401 恒处理跳转首页并带回跳参数。
5. **页面直连 axios** → 请求通道分裂、错误处理失控（B1）。
6. **双主题体系并行** → token 失真、样式漂移。主题偏离必须改真源并写 why 注释，
   不做局部覆盖体系。

## Review Loop

任务收尾自查清单（全部通过才交付）：

1. **禁令自扫**：B1–B6 逐条静态检查（扫描工具落地前按 engineering.md B 表手工 grep）；
   B7 按文档纪律人工复查（结构推断不自动化）。
2. **真源接线复查**：路由 / 导航 / 权限 / query keys / token 五真源 diff，无平行体系。
3. **四态承载复查**：新写数据驱动区块逐个确认加载 / 空 / 错误 / 禁用态承载。
4. **产物净度**：构建或生成后 `git status --short` 无意外产物、无生成物混入。
5. **文档引用完整性**：本次改动文档中出现的 `references/<路径>` 与章节锚点逐条存在。
6. 未通过项回改后重跑；不带未解释的红项交付。

## References

**条件加载路由表**（路径钉死；对应文档由后续规范篇目落地，任务按表读取）：

| 触发场景 | 读取文档 |
| --- | --- |
| 新页面 / 新功能：从需求推理页面形态、布局与卡片-内容组件组成（实现前必读） | `references/design-reasoning.md` |
| 任何页面 / 组件 / 布局工作（默认先读） | `references/general-pages.md` |
| 请求、数据获取、缓存、登录态、SSE | `references/data-layer.md` |
| 颜色、间距、字号、主题、样式方案选择 | `references/design-tokens.md` |
| 质量门、禁令、新页面接线、构建环境 | `references/engineering.md` |
| 测试编写与用例设计（四步接线第 4 步 / 回归锁定 / 测试评审） | `references/testing-guide.md` |
| 任务涉及地图 / GIS / 空间数据 / 图层（仅此时读） | `references/map-layers.md` |
| 地图交互、标注、高亮、资产同源约束（仅此时读） | `references/map-interaction.md` |

**B1–B7 禁令 ID 契约**（ID 固定不增删改义；一句话语义如下，完整表——检查级、
黑名单字面量——唯一真源是 `references/engineering.md`，扫描规则表
`scripts/ban_rules.json` 与其同源）：

| ID | 一句话语义 |
| --- | --- |
| B1 | 页面 / 组件代码不直接 import axios；HTTP 走框架 request 或统一 apiClient |
| B2 | 不用 react-router-dom 做页面路由 / 导航；组件内嵌渲染场景（如路由弹层）允许 MemoryRouter |
| B3 | 不用 import.meta.env；环境配置走框架 config / 代理通道 |
| B4 | 不安装 ESLint / Prettier；质量工具唯一 Biome |
| B5 | 不引入第二地图引擎；地图能力唯一入口封装模块 |
| B6 | 地图 SDK 静态资产构建期同源同步，禁运行时 CDN 引用 |
| B7 | 不硬编码地图 overlay 颜色 / 透明度 / 线宽；overlay 样式走唯一真源（文档纪律项，不自动扫描） |
