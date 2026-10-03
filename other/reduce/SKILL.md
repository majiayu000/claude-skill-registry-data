---
name: reduce
description: Clean the thinking-tree fragment pool — filter by preferences, deduplicate, and remove outdated entries. Uses AskUserQuestion for option-based interaction so user can review without typing.
---

# 碎片池瘦身

对 thinking-tree 碎片池进行清理：偏好过滤、去重、过时删除。
纯减法操作——不读不写思路文件，只在碎片池内部操作。
使用 AskUserQuestion 提供选项式交互，用户无需打字即可审核。

> 推荐顺序：先 `/reduce`（清垃圾），再 `/distill`（建结构）

---

## 工具准备

本 skill 依赖 `AskUserQuestion` 提供选项式确认。进入交互前：

1. 若工具列表已含 `AskUserQuestion` → 直接使用
2. 未加载 → 先执行 `ToolSearch("select:AskUserQuestion")` 加载 schema
3. 加载失败（session 不支持该工具）→ 降级为纯文本确认：
   - 清晰列出编号选项（例如 `1) 全部删除 2) 逐条选择 3) 全部保留`）
   - 明确告知回复格式（例如「回复编号」）
   - 不要跳过确认步骤

降级只影响呈现方式，不影响功能。

---

## 执行步骤

### 1. 读取数据

读取以下文件（`~` = 用户 home 目录）：
- `~/.thinking-tree/fragments.md` — 碎片池（主要处理对象）
- `~/.thinking-tree/.preferences.md` — 用户偏好（判断碎片是否符合记录范围）

### 2. 分析碎片

对每个碎片（以 `## ` 开头、由 `---` 分隔的段落）逐条评估，分为四组：

| 组 | 判断标准 | 动作 |
|----|---------|------|
| **偏好外组** | 不符合 .preferences.md 中的记录范围（如工程细节） | 删除 |
| **重复组** | 核心论点与另一条碎片相同（仅措辞/例子不同） | 合并为一条 |
| **过时组** | 已被后续思考覆盖、推翻、或已无参考价值 | 删除 |
| **保留组** | 独立有效，不重复不过时 | 保留原位 |

### 3. 输出总览

先输出一行统计，让用户了解整体情况：

```
整理分析完成：73 条碎片 → 偏好外 6 条，重复 12 条，疑似过时 5 条，保留 50 条
```

### 4. 逐组确认（AskUserQuestion 交互）

**重要：使用 AskUserQuestion 工具让用户通过选项确认，不要让用户打字。**
**交互原则：推荐操作放第一位，让用户一键确认即可进入下一步。**

#### 4a. 偏好外组 — 单选批量确认

读取 .preferences.md 的记录范围，标记不符合的碎片。使用 AskUserQuestion：
- question: "发现 N 条碎片不符合当前记录偏好（如：工程细节），如何处理？"
- header: "偏好过滤"
- multiSelect: false
- options:
  - label: "全部删除 (Recommended)", description: "删除全部 N 条偏好外碎片：[列出标题摘要]"
  - label: "逐条选择", description: "展开每条碎片，逐一确认是否删除"
  - label: "全部保留", description: "不做改动"

如果用户选"逐条选择"，再用 multiSelect 展开每条碎片供选择（最多 4 条一批）。

#### 4b. 重复组 — 每组重复碎片一起确认

对每组重复碎片（2-3 条一组），使用 AskUserQuestion：
- question: "这 N 条碎片表达了相似观点，如何处理？"
- header: "去重"
- options:
  - label: "合并 (Recommended)", description: "保留最精炼的表述，删除冗余"
  - label: "全部保留", description: "不做改动"
- preview: 展示这几条碎片的标题和关键内容对比
- multiSelect: false

#### 4c. 过时组 — 单选批量确认

使用 AskUserQuestion：
- question: "发现 N 条碎片可能已过时，如何处理？"
- header: "过时清理"
- multiSelect: false
- options:
  - label: "全部删除 (Recommended)", description: "删除全部 N 条过时碎片：[列出标题摘要+过时原因]"
  - label: "逐条选择", description: "展开每条碎片，逐一确认是否删除"
  - label: "全部保留", description: "不做改动"

如果用户选"逐条选择"，再用 multiSelect 展开每条碎片供选择（最多 4 条一批）。

#### 4d. 保留组 — 不需要确认

保留组直接跳过，不打扰用户。

### 5. 执行改动

按用户在每一步选择的结果修改文件：
- 偏好外删除：直接从碎片池移除
- 合并：保留精炼版，删除冗余版
- 过时删除：直接从碎片池移除
- 保留：不动

### 6. 输出统计

```
整理完成：偏好过滤 X 条，合并 Y 条，删除 W 条，保留 M 条
碎片池：73 → 50 条
```

---

## 注意事项

- 所有文件路径使用绝对路径
- 不要创造新内容，只做整理和搬运
- 碎片合并时保留最完整的表述
- AskUserQuestion 每次最多 4 个选项、4 个问题，碎片多时分批
- 如果碎片数量很多（50+），优先处理偏好外和重复（确定性高）
- 不读不写思路文件——碎片归入思路体系由 /distill 负责
