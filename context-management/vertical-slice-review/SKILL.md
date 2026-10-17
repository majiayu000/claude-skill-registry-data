---
name: vertical-slice-review
description: 审查 ticket 拆解方案是否符合 vertical slice 方法论：逐条判定是否贯穿 schema/API/UI/tests、能否独立 demo、大小能否放进一个 context window，读代码库验证、必要时重拆，并调用 strong-model-consultant 复核。
disable-model-invocation: true
---

# Vertical Slice Review（垂直切片审查）

一条窄但完整、贯穿每一层的路径，胜过三条各自只碰一层的宽切片。本 skill 判定拆解方案是否真 vertical，必要时重拆。

## 判定标准

一个 slice 是 vertical，当且仅当**同时**满足：

- **贯穿每一层** — 从 schema → API → UI → tests 切出一条窄路径。只碰一层就是 horizontal slice：只搭共享模块、只迁一列字段、只补集成测试，都是。
- **独立可验证** — 完成即可独立 demo 或独立验证，不依赖后续 slice。
- **context window 大小** — 能放进一个全新 context window 完成。

两条周边规则：

- **prefactor 先做** — 让后续 slice 变容易的机械重构（模块抽取、类型收窄）独立成票排在前，不混进实现 slice。它不贯穿各层，但合法。
- **共享管线整张落地** — 多条用户路径汇聚同一管线时，占位/降级/竞态是路径完整性，不是 gold-plating；之后沿用户路径切验证切片。

## 流程

1. **收集划分方案** — 抽取每张 ticket 的 title、deliverable（端到端行为）、blocking edges；来源缺口如实指出，不脑补。
   *完成标志*：每张票三要素齐全，或缺口已列出。
2. **读代码库建立层事实** — 读项目约定（CLAUDE.md / CONTEXT.md / docs/adr/）与技术栈，把 schema/API/UI/tests 落到代码落点。只建层事实，不做无关探索。
   *完成标志*：方案触碰的每层都有落点；无法确认的记为 gap。
3. **逐 slice 判定** — vertical ✓（贯穿证据）/ horizontal ✗（指出只碰哪层）/ 边界问题（过大、blocking edges 错、prefactor 混入）。不确定标 gap。
   *完成标志*：每张票有 verdict + 证据或 gap。
4. **重拆（若需要）** — 产出 tracer bullet 方案：每条窄但完整、可独立验证、含 blocking edges；只改不 vertical 的部分，保留已合理边界。覆盖全仓的机械变更按 expand–contract 编排，不硬塞 vertical。
   *完成标志*：修正方案覆盖原票且全部满足判定标准。
5. **强代理复核** — 把原方案 + 修正方案连同层事实交给 strong-model-consultant，聚焦垂直性/可验证性/大小/blocking edges；与自查不一致处并列呈现。
   *完成标志*：顾问意见已并入，或差异已列出待裁决。
6. **输出** — ① 审查结论（每票 verdict + 证据）② 修正方案（title / deliverable / blocked by / 独立验证）③ 顾问意见 ④ 三个确认点（粒度、blocking edges、合并拆分）。
   *完成标志*：用户点头或明确说出要改什么。
