---
name: gui-learn
user-invocable: false
description: >-
  Atom Game GUI pipeline 第 7 阶段（每次修 bug / 做需求完成后自动跑），不面向用户手动调用。
  从本次开发提取经验回写**私有知识库** ${CLAUDE_PLUGIN_DATA}/gui-knowledge/：建实例层 bug/fix、
  泛化出通用层 component/pattern/lesson、写 edges、独立 reviewer 晋升 proposed→confirmed、
  重建 query_pack；promote/demote 时对公共库语义去重（公共库为准）。
  两遍式：默认捕获遍；`enrich` 参数触发充实遍填 _TODO_ 段。
  用户手动沉淀私有库请用 `/dev-gui-plugin:gui-learn-private` command；
  沉淀进**项目公共库**用 `/dev-gui-plugin:gui-learn-public` command。
---

# Phase 7: gui-learn — 知识沉淀

**职责**：从本次开发中提取经验回写知识库。**核心是「泛化」**——不只记「这个 panel 发生了什么」，
更要抽出**可跨 panel 复用**的通用教训/组件用法/性能经验。**不限于 GUI**：语法习惯、工具使用技巧、
编辑器配置、调试方法、Shell 脚本模式等通用开发经验同样准入。

## 写入目标

本 skill **只写私有知识库**：`$KB_ROOT = ${CLAUDE_PLUGIN_DATA}/gui-knowledge`（个人、跨版本存活、不进 git）。
下文所有 `gui_knowledge.py` 命令的 root 一律用 `"$KB_ROOT"`；首次写入前若目录不存在，先
`gui_knowledge.py init "$KB_ROOT"`（gui-plan 通常已建）。

> 沉淀进**项目公共库**（团队共享、走 p4）请改用 **`gui-learn-public`** command。
> Schema 见 `${CLAUDE_PLUGIN_ROOT}/shared-references/knowledge-schema.md`。
> 机制总纲见 plan §十 与 `acceptance-gate.md`。
> **私有库去重**：promote / demote 时对公共库查重（见第 7 步与 D 段），重复/矛盾以公共库为准。

**触发条件**：① pipeline 中每次修 bug 或做需求完成（PASS 或 2 轮 improve 结束）自动跑；
② 本 skill 是 pipeline 内部阶段，**不面向用户手动调用**——用户手动沉淀私有库请用
`/dev-gui-plugin:gui-learn-private` command。
即使本次无 panel 级产物（纯逻辑/性能修复），只要学到可复用的东西也必须沉淀到通用层。

---

## 模式 A：捕获遍（默认，每次必跑，便宜）

### 0. 写入前机械筛（capture_filter）

任何条目持久化前先过滤（PreToolUse hook 也会兜底拦截写 gui-knowledge 的内容）：
```bash
echo "<条目正文>" | python3 "${CLAUDE_PLUGIN_ROOT}/tools/capture_filter.py" -
```
命中 `env_failure` / `transient_error` / `negative_tool_claim` / `single_instance_narrative` →
**不存原文**，改存「怎么修 / 缺什么配置 / 它隐含的类级规则」或丢弃。

### A. 实例层（本次发生的事，带 panelId）

1. **记录 Bug** → `bugs/<bug_id>.md`：现象 + 根因(file:line) + 修复 + 验证。
2. **归档修复** → `fixes/<fix_id>.md`：成功/失败、变更、影响。失败也记，且原因必须是**类级**
   （如「每帧重建子节点」），不是操作噪音。

### B. 通用层（泛化后可跨 panel 复用 —— 每次必做，先查重）

> **实例→类级规则**：「B003 在 XXPanel 因未判空 SerializeField 崩」是实例；存进通用层的是它隐含的
> 类级规则「SerializeField 引用在 OnXxx 使用前必须判空」。**只存后者。**

写每条通用层条目前先查重（§十.7，三态：新增 / 补充 / 冲突）：
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" find-existing \
    "$KB_ROOT" --type lesson --slug <slug>
```
- 空输出 → 新建条目（`status: proposed`，通用层段落留 `_TODO._`）。
- 已存在且互补 → 追加段。
- 已存在且**冲突** → 不静默覆盖；在条目标注 `conflict`，入队人工 / reviewer 裁决。

3. **组件用法** → `components/<slug>.md`（用法/坑点/性能特征）
4. **模式** → `patterns/<slug>.md`（反模式建条目 / 已知追加案例 / 最佳实践亦收录）
5. **通用教训·性能经验** → `lessons/<slug>.md`（H1 一句话教训 + 类级规则填实；其余段可留 `_TODO._`）

### C. 索引、晋升与摘要（确定性脚本，零 LLM）

6. **写关系图 + 渲染关联**：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" add-edge "$KB_ROOT" \
       --from bug:B001 --to component:styles-module --type caused_by
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" render-connections "$KB_ROOT"
   ```
   （⑤ 图是真相源，各页「## 关联」段由脚本重渲染，禁手编。）

7. **晋升 load-bearing + 对公共库去重（⑥ 拒/纳不对称）**：通用层条目默认 `proposed`，要进
   query_pack 必须经 **独立 reviewer 背书**。

   **7a. 机械初筛公共库候选**：对每条待晋升私有条目跑：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" find-dedup-candidates lesson:L004 \
       --root "$KB_ROOT" --public-root "${CLAUDE_PROJECT_DIR}/.claude/dev-gui-knowledge"
   ```
   输出公共库同主题候选（node_id/title/excerpt）；`[]` 表示公共库无覆盖。

   **7b. spawn `gui-reviewer` subagent（全新上下文）批量裁决**，对每条私有条目同时判：
   ① 「确为类级、正确、可复用」（背书）；② 与 7a 候选的语义关系，三态之一：
   - `confirm`：公共库无语义覆盖 → 晋升：
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" promote "$KB_ROOT" \
         lesson:L004 --reviewer gui-reviewer --verdict-id <背书产物>
     ```
   - `duplicate`（语义相似/相近）**或** `conflict`（语义矛盾）→ **以公共库为准，删私有条目**（不晋升）：
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" remove "$KB_ROOT" \
         lesson:L004 --reason duplicate-of-public --superseded-by <公共 node_id>
     ```
   机械筛只能「拒」，「纳」（promote）必须 reviewer 背书；7a 只是缩小候选，删/留由 reviewer 语义裁决。

8. **重建 query_pack + 索引**（确定性、只收 confirmed）：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" rebuild-index "$KB_ROOT"
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" rebuild-query-pack "$KB_ROOT"
   ```

9. **追加 log**：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" log "$KB_ROOT" \
       "panelId=XXX verdict=PASS | lesson L004(confirmed): 列表优先 ListModule 复用"
   ```

10. **收尾**：
    ```bash
    python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_run_state.py" set "${CLAUDE_PROJECT_DIR}" <panelId> gui-learn done
    ```

### D. 降级（demote）—— confirmed 条目不再成立时

当某私有库 confirmed 通用层条目被推翻（reviewer 复审否定 / 被新证据取代 / 用户显式要求降级）：

1. **降级**（撤销 load-bearing，属「拒」，**无需 reviewer 背书**）：
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/tools/gui_knowledge.py" demote "$KB_ROOT" \
       lesson:L004 --reason "<为何不再成立>"
   ```
2. **降级时同样对公共库去重**：跑第 7a 的 `find-dedup-candidates` + reviewer 语义判；
   若公共库现已覆盖（`duplicate`/`conflict`）→ 改用 `remove`（公共库为准）而非停留在 proposed。
3. 之后重跑第 8 步 `rebuild-index` / `rebuild-query-pack`（query_pack 只收 confirmed，降级/删除即生效）。

---

## 模式 B：充实遍（pipeline 内部调用，`enrich [--max N]`）

把通用层骨架里 `_TODO._` 段填成 1–3 句结论（②）：
- 默认只填**含 `_TODO._`** 的条目（可复用成分 / 适用场景 / 失败模式）。
- `--max N` 封顶批量（token 预算真实存在）。
- **「## 关联」段受保护**，永远由 edges 渲染，enrich 不碰。
- 填完不动 frontmatter 的 `status`（晋升仍走第 7 步的 reviewer 背书）。

填充后可再跑 `rebuild-query-pack`（confirmed 条目的新内容会被重新抽句）。
