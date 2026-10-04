---
name: ardot-create-new-file
description: |
  **强制性前置条件** — 每次调用 `create_new_page` 工具之前，必须先调用此技能。
  未经加载此技能，绝不能直接调用 `create_new_page`。

  当用户想要在 Ardot 设计文件中创建新页面时触发。
  关键词：在 Ardot 上下文中的"创建新页面"、"添加页面"、"新画布"。
disable-model-invocation: false
---

# ardot-create-new-file — 创建新 Ardot 页面

处理 Ardot 设计文件中的页面创建。轻量级前置技能，确保正确的页面 ID 追踪和编辑器状态管理。

## 工作流程

### 第一步：确定页面名称和位置

根据用户意图决定描述性页面名称：
- `"Components"` — 用于可复用组件库
- `"Light Mode"` / `"Dark Mode"` — 用于特定主题的页面
- `"Screens"` — 用于设计原型
- 如果新页面需要出现在特定现有页面之后，使用 `leftPageId`

### 第二步：调用 create_new_page

```json
create_new_page({
  "name": "Components",
  "select": false
})
```

**默认使用 `select: false`** — 这会创建页面但不切换编辑器焦点，允许你继续在当前页面工作。

仅当你需要立即切换到新页面进行后续操作时，才使用 `select: true`。

### 第三步：记录返回的 pageId

响应包含新页面的 ID。**立即保存** — 这是后续跨页面写入和交接时最可靠的 pageId 来源。

```
响应示例：pageId = "3:1672"
```

使用此 pageId 进行：
- 跨页面 `I("3:1672", {...})` 操作
- `M("nodeId", "3:1672")` 将节点移动到此页面
- `batch_read({parentId: "3:1672"})` 读取此页面内容

## 重要说明

- **pageId 发现受限**：不带 nodeIds 的 `batch_read({})` 只返回当前上下文的内容，不能作为全文件页面枚举依据。
- **在创建时记录页面 ID** — 这是最可靠的交接方式；必要时也可以读取已知 pageId 或已知节点 ID。
- **`select: true`**（默认值）会将编辑器切换到新页面。如果你正在跨多个页面构建，这可能会中断你的工作流程。
- **`leftPageId`** 允许在特定兄弟页面之后插入新页面，有助于维护页面顺序。

## 跨页面操作参考

一旦你记录了页面 ID：

| 操作 | 方法 | 示例 |
|------|------|------|
| 在特定页面创建 | `I("pageId", {...})` | `I("3:1672", {type: "FRAME", ...})` |
| 移动节点到页面 | `M("nodeId", "pageId")` | `M("3:544", "3:1672")` |
| 读取页面内容 | `batch_read({nodeIds: ["pageId"], properties: ["children"], readDepth: 1})` | `batch_read({nodeIds: ["3:1672"], properties: ["children"], readDepth: 1})` |
| 截图页面内容 | `capture_screenshot({nodeIds: [...]})` | 通过节点 ID 跨页面 |
