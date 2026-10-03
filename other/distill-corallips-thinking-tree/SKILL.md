---
name: distill
description: Distill fragments into structured thought files — classify into existing files or synthesize new ones. Scans fragment pool for related insights, proposes actions, and executes. Accepts optional topic hint.
---

# 碎片→体系

将碎片池中的碎片转化为结构化的思路体系。两种动作：
- **归入已有思路文件**：碎片主题与已有文件高度匹配 → 整合进去
- **新建思路文件**：多条碎片可聚合为新主线 → 合成新文档

```
/distill                    → AI 扫描碎片池，建议可归类和提炼的内容
/distill 产品定位的核心思路   → 按用户方向找碎片，直接进入提炼
```

`$ARGUMENTS` 是可选的主题方向提示。

> 推荐顺序：先 `/reduce`（清垃圾），再 `/distill`（建结构）

---

## 工具准备

本 skill 依赖 `AskUserQuestion` 提供选项式确认。进入交互前：

1. 若工具列表已含 `AskUserQuestion` → 直接使用
2. 未加载 → 先执行 `ToolSearch("select:AskUserQuestion")` 加载 schema
3. 加载失败（session 不支持该工具）→ 降级为纯文本确认：
   - 清晰列出编号选项（例如 `1) 全部归入 2) 逐条选择 3) 跳过`）
   - 明确告知回复格式（例如「回复编号」）
   - 不要跳过确认步骤

降级只影响呈现方式，不影响功能。

---

## 执行步骤

### 1. 读取数据

读取以下文件（`~` = 用户 home 目录）：
- `~/.thinking-tree/fragments.md` — 碎片池（提炼素材）
- `~/.thinking-tree/` 目录下所有 *.md 思路文件 — 读取标题和大纲（判断归入目标、避免主题重复）

### 2. 识别动作

扫描碎片池，对每条碎片判断：
- **可归入**：主题与某个已有思路文件的主线高度匹配
- **可聚合**：多条碎片围绕同一主题，可合成新思路文件
- **暂留**：独立观点，暂不适合归入或聚合

#### 有参数时：
按用户给的方向，从碎片池中找出语义相关的碎片，进入提炼流程。

#### 无参数时：
输出两部分建议，按顺序处理：

**A. 可归入已有思路文件的碎片**（如果有）：

使用 AskUserQuestion：
- question: "发现 N 条碎片可归入已有思路文件，如何处理？"
- header: "归类"
- multiSelect: false
- options:
  - label: "全部归入 (Recommended)", description: "将碎片整合进对应思路文件：[列出 碎片标题 → 目标文件]"
  - label: "逐条选择", description: "展开每条碎片，逐一确认"
  - label: "跳过", description: "不归类，继续看可提炼的主题"

如果用户选"逐条选择"，对每条碎片用单选确认：
- options: "归入 XXX.md (Recommended)" / "保留在碎片池"

**B. 可提炼为新思路文件的主题**（如果有）：

使用 AskUserQuestion：
- question: "发现 N 个主题方向可以提炼为思路文件，如何处理？"
- header: "提炼"
- multiSelect: false
- options:
  - label: "全部提炼 (Recommended)", description: "依次生成 N 个思路文件：[列出 主题→文件名（涉及碎片数）]"
  - label: "逐个选择", description: "展开每个主题，逐一确认是否提炼"
  - label: "跳过", description: "不提炼，保持现状"

如果用户选"逐个选择"，对每个主题用单选确认：
- options: "提炼为 XXX.md (Recommended)" / "跳过"

### 3. 归类执行（如果有）

用户确认归类后：
1. 将碎片内容追加到对应思路文件末尾（加 `---` 分隔）
2. 从 `fragments.md` 移除已归类的碎片
3. 保持目标文件的既有风格和结构

### 4. 展示素材与大纲（提炼新文件时）

展示：
- 涉及的碎片标题列表
- 一句话主线概述
- 建议的文件名（如 `positioning.md`）
- 三级大纲草案

使用 AskUserQuestion：
- question: "以上是提炼方案，如何处理？"
- header: "大纲确认"
- options:
  - label: "确认，开始提炼", description: "按此大纲生成思路文件"
  - label: "调整方向", description: "补充说明后重新生成大纲"
  - label: "取消", description: "不提炼，返回"
- multiSelect: false

如果用户选「调整方向」，根据补充重新生成大纲，再次确认。

### 5. 生成思路文件

按确认的大纲，将碎片内容**提炼重写**为有主线的结构化文档。

**关键要求：**
- 不是碎片的拼接或复制粘贴
- 是理解碎片群的集体含义后，写出一篇有主线的文档
- 每节在主线上有位置，读完能一句话概括
- 适当使用 ASCII 图、对比表、层级关系来表达结构
- 保留碎片中的锐利表述和关键判断，不要稀释

### 6. 预览成品

将生成的完整文档内容展示给用户。

使用 AskUserQuestion：
- question: "以上是生成的思路文件，如何处理？"
- header: "成品确认"
- options:
  - label: "写入", description: "保存为思路文件，从碎片池移除已提炼的碎片"
  - label: "再改改", description: "补充反馈后重新生成"
  - label: "放弃", description: "不保存，碎片保持原样"
- multiSelect: false

如果用户选「再改改」，根据反馈调整内容，再次预览确认。

### 7. 写入与清理

用户确认后：
1. 在 `~/.thinking-tree/` 创建新 .md 思路文件（提炼时）或追加到已有文件（归类时）
2. 从 `fragments.md` 移除已提炼/归类的碎片（按 `<!-- frag:ID -->` 或标题定位）

输出：
```
提炼完成：7 条碎片 → xxx.md（新建） / 3 条碎片 → yyy.md（归入）
碎片池：120 → 110 条
```

---

## 注意事项

- 所有文件路径使用绝对路径
- 至少 3 条相关碎片才值得提炼为新文件，少于 3 条时建议归入已有文件或继续积累
- 归入已有思路文件时保持该文件的既有风格和结构
- 思路文件的质量标准：主线清晰，每节有位置，能一句话概括全文
- 碎片移除时保持 fragments.md 的格式完整性
- 归类和提炼可以在同一次 /distill 中完成
