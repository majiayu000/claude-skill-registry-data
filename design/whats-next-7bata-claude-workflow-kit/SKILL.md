---
name: whats-next
description: 判断并汇报 /scaffold 项目下一步该干什么。用户说"下一步干什么 / 接下来做什么 / whats next / 我到哪了"，且项目根目录有 docs/PLAN.md 时触发。
allowed-tools: Read, Glob, Grep
---

# /whats-next

读 /scaffold 铺设的计划与进度文档，告诉用户下一步干什么。**全程默认中文输出**（技术标识符保持英文）。

**文档是唯一依据。** 不要为回答这个问题遍历代码库；只在文档之间出现矛盾需要核对时才抽查代码。

## 步骤 1：读进度文件

1. `docs/PLAN.md` — 总体路线、各 Phase 状态（标题带 ✅ = 已完成）、Spec 索引
2. `docs/Progress.md` — 上半部「进度总览」模块状态表（pending/doing/done）+ 下半部变更日志（**最新在上**，读最近 2~3 条）；更早月份在 `docs/archive/Progress-YYYY-MM.md`，需要追溯历史时才读
3. 最新 design spec — Spec 索引指向的最新一条 `docs/superpowers/specs/<日期>-<主题>-design.md`（索引没有就 Glob 该目录取日期最新）— 对照 Progress.md 判断是否已实现
4. `docs/DECISIONS.md` — **最新在上**，读最近 2~3 条：与下一步同域的决策必须进「随行注意」
5. `docs/MEETINGS.md` — 只看**最新一节**的「待办」：未勾选、且没出现在任何计划里的条目，进输出第 4 部分
6. `docs/REQUIREMENTS.md` 「目标台账」— 状态为 open 的未销账项，逐条进输出第 5 部分

ARCHITECTURE.md / DEPLOYMENT.md 是设计与部署文档，不含进度，不读；REQUIREMENTS.md 的「分期路线图」只在步骤 2 第三行命中时读，「目标台账」按上面第 6 项每次都读。

## 步骤 2：定位下一步（按序判断，命中即停）

| 状态 | 下一步 |
|---|---|
| 最新 spec 尚未实现（Progress 无对应实现记录） | 用 ultracode（Workflow 多代理编排）直接从该 spec 实现；Progress 或 spec 里记着被用户喊停的除外，那种先问一句 |
| spec 全部已实现（或还没有 spec），PLAN.md 还有未 ✅ 的 Phase | 对下一个 Phase 用 superpowers:brainstorming 出 design spec（落 `docs/superpowers/specs/`），写入后直接 ultracode 实现——不走 writing-plans；spec 登记进 Spec 索引 |
| PLAN.md 总体路线还是 `<!-- 待补 -->` | 先读 REQUIREMENTS.md「分期路线图」作输入，再用 superpowers:brainstorming 定分阶段路线图 |
| 所有 Phase 都 ✅ | 项目按计划已完成；建议复盘或开新 Phase |

## 步骤 3：输出契约（按序五部分）

1. **当前位置** — 一两句：最近完成了什么，引用 Progress 最新条目的日期
2. **下一步** — 任务名 + 第一步具体动作（到文件/命令级别）+ 出处（哪个文件哪一节）
3. **随行注意** — 与下一步相关的已定决策 / 踩坑，来源：DECISIONS.md 最近条目 + Progress 变更日志，注明出处；若最近一批改动动过 UI 且 Progress 里没有 ui-sweep 走查记录，在此提示一句：建议补跑一次交互回归扫描（没有则省略，不强推）；没有则省略此节
4. **未落计划的会议待办** — MEETINGS.md 最新一节里未勾选、且没进任何计划的待办，提醒用户决定去向；已登记进目标台账的条目不在此重复列；没有则省略此节
5. **未销账目标** — REQUIREMENTS.md 目标台账里状态为 open 的条目逐条列出，挂账超 7 天的置顶标注；只列台账条目；没有则省略此节

结尾问用户：现在开始吗？

## 边界情况

- `docs/PLAN.md` 或 `docs/Progress.md` 不存在 → 这不是 /scaffold 项目。说明缺哪个文件，建议先跑 `/scaffold`，不要猜下一步
- Progress（总览表或日志）与 spec 实现状态矛盾（说完成但无实现记录，或反之）→ 明确指出矛盾及双方出处，建议先核对再动工，不要默默择一
- DECISIONS.md 或 MEETINGS.md 不存在 → 不报错，跳过对应步骤即可（老项目可能没有）
- REQUIREMENTS.md 不存在或没有目标台账节 → 跳过第⑤部分，不报错（存量项目常态）
