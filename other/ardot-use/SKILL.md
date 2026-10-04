---
name: ardot-use
description: |
  **强制性前置条件** — 每次调用 `batch_edit` 工具之前，必须先调用此技能。
  未经加载此技能，绝不能直接调用 `batch_edit`。

  当用户想要在 Ardot 设计文件中创建、更新、移动或删除节点时触发 —
  例如插入框架、文本、形状、组件；将变量绑定到填充/描边；
  构建屏幕、组件或设计库。当涉及 batch_edit DSL 操作时也加载
  （I/U/M/D/C/G 操作符）。
disable-model-invocation: false
---

# ardot-use — Ardot batch_edit DSL 技能

通过 `batch_edit` DSL 进行所有 Ardot 写操作的核心技能。提供关键规则、操作符参考、变量绑定模式、验证策略和错误恢复。

## 1. 关键规则

**1. 每个 `batch_edit` 调用最多 25 个操作。** 将较大的工作拆分为多个调用。建议保持在 20 个或更少以留出余量。

**2. 绑定名称在每次 `batch_edit` 调用后过期。** 在一次调用中分配的绑定名称（例如 `btn1 = I(...)`）仅在同一调用内有效。在下一个 `batch_edit` 中，你必须使用真实节点 ID（例如 `"3:544"`）— 绝不使用先前调用的绑定名称。

**3. I() 中的 TEXT 节点仅支持 `fill: "#HEX"` 字符串格式。** 在 I() 中创建 TEXT 节点时不能使用 `fills: [{..., boundVariables: {...}}]`。
**解决方法**：在 I() 中使用 `fill: "#HEX"` 创建 TEXT 节点，然后在后续的 `batch_edit` 调用中使用 U() 应用带有 `boundVariables` 的 `fills`。

**4. `updated: {}` 不代表失败。** U() 操作通常返回 `updated: {}` 而不是 `updated: {"nodeId": {...}}`。操作可能已成功 — 通过立即运行 `batch_read` 验证节点，而不是信任返回值。

**5. I() 必须指定父节点。** 第一个参数可以是 page、frame 的真实 ID，或同一次调用中已创建的 binding；跨页面插入时使用目标 pageId。

**6. M() 可以移动节点到新的父容器。** 第二个参数应是有效的父节点 ID（page 或 frame），可选第三个参数用于指定 sibling index。移动后必须读取目标父节点验证层级。**页面重排**：MCP 无专用工具，用 `M("pageId", "0:0", index)` 把 PAGE 移回文件根 `0:0`（DOCUMENT）即可重排页面列表，index 实测为 **1-based**（详见 [dsl-reference.md](references/dsl-reference.md) 的 Reordering pages）。

**7. 不支持 cornerRadius 变量绑定。** Ardot 目前不支持 `cornerRadius` 的 `boundVariables`。使用硬编码数值代替（例如 `cornerRadius: 6`）。

**8. 框架上的 variableModes 不可靠。** 设置 `variableModes: {"3:2": "3:3"}` 来切换颜色模式可能不会生效。使用专门的页面来表示浅色/深色模式。

**9. 始终 `return` 所有创建/修改的节点 ID。** 每个 `batch_edit` 响应都包含绑定名称和节点 ID。记录这些 — 在后续调用中需要它们。

**10. 增量构建。** 先用占位符构建骨架，然后逐个区块填充细节。每个 `batch_edit` 调用失败都是原子性的 — 文件不会被修改。

**11. 截图与编辑分离。** 不要在 `batch_edit` 操作中混合 `capture_screenshot` 调用。截图作为单独的验证步骤。

## 2. DSL 操作符参考

| 操作符 | 语法 | 用途 | 关键说明 |
|--------|------|------|----------|
| `I` | `I("parentId", {type, name, ...})` | 插入新节点 | parent 可以是 page、frame 或同批次 binding；`reusable: true` 用于组件 |
| `U` | `U("nodeId", {props...})` | 更新现有节点 | 必须使用真实节点 ID，不能使用先前调用的绑定名称 |
| `M` | `M("nodeId", "parentId", index?)` | 移动节点 | 目标是新的父节点 ID，可选 index |
| `D` | `D("nodeId")` | 删除节点 | 删除父节点会级联到所有子节点 |
| `C` | `C("componentId", "parentId", {props...})` | 创建组件实例 | 在指定父节点下创建组件实例，可在 copyNodeData 中设置尺寸、位置或 descendants |
| `G` | `G("nodeId", "ai"\|"stock", "prompt")` | 为已有 frame/shape 应用图片填充 | 先创建承载节点，再调用 G() |

### I() — 插入节点

```js
// 在 Components 页面上创建可复用按钮组件
btn = I("3:1672", {
  "type": "FRAME",
  "name": "Button/Primary/sm",
  "reusable": true,
  "width": "hug_contents",
  "height": 24,
  "paddingLeft": 12,
  "paddingRight": 12,
  "paddingTop": 4,
  "paddingBottom": 4,
  "layout": "horizontal",
  "cornerRadius": 6,
  "primaryAxisAlignItems": "CENTER",
  "fills": [{"type": "SOLID", "color": {"r": 0.91, "g": 0.44, "b": 0.29},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "label", "characters": "Button",
      "fontSize": 12, "fill": "#FFFFFF"}
  ]
})
```

**关键点：**
- `width: "hug_contents"` — 收缩以适应内容（需要自动布局）
- `width: "fill_container"` — 扩展以填充父元素
- `layout: "horizontal"` — 启用水平自动布局（需要 padding）
- TEXT 的 `fill` 在 I() 中必须是 `"#HEX"` 字符串格式
- SOLID 填充的颜色值使用 0–1 范围（{r, g, b}）
- `primaryAxisAlignItems`: `"MIN"` / `"CENTER"` / `"MAX"`
- `counterAxisAlignItems`: `"MIN"` / `"CENTER"` / `"MAX"`

### U() — 更新节点

```js
// 将颜色变量绑定到 TEXT 节点的填充
U("3:1676", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.61, "g": 0.59, "b": 0.56},
    "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}
  }]
})
```

### M() — 移动节点

```js
M("3:544", "3:1672")     // 将节点 3:544 移动到 Components 页面
M("3:544", "3:200", 0)   // 将节点 3:544 移动到 frame 3:200 的第一个位置
```

- 节点在移动后保留其原始 ID
- 移动源组件不会破坏组件实例
- 移动后用 `batch_read({parentId: "<parentId>"})` 或读取父节点 children 验证

### C() — 创建组件实例

```js
btn = C("3:544", "3:200", {x: 24, y: 200})  // 在父节点 3:200 下创建组件 3:544 的实例
```

- 在 copyNodeData 中可设置 x/y、width/height，或用 descendants 覆盖实例内部文本/属性

## 3. 变量绑定模式

### 颜色变量绑定格式（通用）

```json
"boundVariables": {
  "color": {"id": "VariableID:<variable-id>", "type": "VARIABLE_ALIAS"}
}
```

- 在 `fills[]` 中：每个填充对象上的 `boundVariables.color`
- 在 `strokes[]` 中：相同格式，在每个描边对象上
- `cornerRadius` 绑定：不支持（见关键规则 7）

### TEXT 节点：两步绑定

第一步 — 在 I() 中使用 `fill: "#HEX"` 创建：
```js
I("0:1", {
  "type": "TEXT", "characters": "Hello",
  "fontSize": 14, "fill": "#333333"
})
```

第二步 — 在单独的 batch_edit U() 调用中绑定变量：
```js
U("<textNodeId>", {
  "fills": [{
    "type": "SOLID",
    "color": {"r": 0.2, "g": 0.2, "b": 0.2},
    "boundVariables": {"color": {"id": "VariableID:3:12", "type": "VARIABLE_ALIAS"}}
  }]
})
```

### 变量 ID 格式

```
"VariableID:3:14"  — 前缀 "VariableID:" + 变量节点 ID
```

从 `apply_variables` 返回值或 `fetch_variables` 获取变量 ID。

## 4. 验证与恢复

### 验证工作流程

在每批 U() 操作之后：
1. 对关键节点运行 `batch_read` 以验证属性更改
2. 不要依赖 `updated: {}` — 它可能具有误导性
3. 对于视觉验证，对受影响的节点使用 `capture_screenshot`
4. 如果有问题，在下一个 `batch_edit` 调用中修复

### 错误恢复

- 每个 `batch_edit` 调用都是**原子性的** — 如果脚本失败，文件不会被更改
- 出错时：读取错误消息 → 修复操作字符串 → 重试
- 最常见原因：无效的节点 ID、错误的 pageId、DSL 字符串中的语法错误

## 5. 预检清单

在提交任何 `batch_edit` 调用之前，验证：

- [ ] 总操作数 ≤ 25（建议 ≤ 20）
- [ ] 所有父引用使用此调用中的绑定名称，而非先前调用的
- [ ] I() 使用有效父节点（跨页面时明确指定目标 pageId）
- [ ] TEXT 节点使用 `fill: "#HEX"`（不是带有 boundVariables 的 fills 数组）
- [ ] U() 和 M() 使用真实节点 ID（不是先前调用的绑定名称）
- [ ] M() 目标是有效父节点 ID；如指定 index，确认 index 在目标父节点 children 范围内
- [ ] 颜色值在 {r, g, b} 0–1 范围内，不是 0–255
- [ ] cornerRadius 使用硬编码数值，不是 boundVariables
- [ ] 所有创建的节点 ID 已捕获以供后续参考
- [ ] 自动布局框架设置了 `layout` + `padding*` 属性
- [ ] 已至少调用过一次 `fetch_editor_state(includeSchema: true)`

## 6. 错误矩阵

| 错误/症状 | 可能原因 | 修复方法 |
|-----------|----------|----------|
| U() 返回 `updated: {}` | 正常 — 操作可能已成功 | 使用 batch_read 验证，不要信任返回值 |
| 节点创建在错误的位置 | I() 的父节点错误 | 使用目标 pageId、frameId 或同批次 binding 作为第一个参数 |
| TEXT 变量绑定不工作 | 在 I() 中使用了 fills+boundVariables | 两步法：I() 使用 fill:"#HEX"，然后 U() 使用 fills+boundVariables |
| 绑定名称未识别 | 使用了先前 batch_edit 的绑定名称 | 在下一个调用中使用真实节点 ID（例如 "3:544"） |
| cornerRadius 变量未绑定 | Ardot 不支持此功能 | 使用硬编码值（例如 cornerRadius: 6） |
| M() 将节点移到错误位置 | 目标父节点 ID 或 index 错误 | 读取目标父节点 children，确认层级和顺序 |
| 无法可靠枚举页面 ID | 不带 nodeIds 的 batch_read 只返回当前上下文 | 从 create_new_page 返回值记录页面 ID，并在交接记录中保存 |
| variableModes 未生效 | 功能可能不稳定 | 使用单独的页面表示浅色/深色模式变体 |

## 7. 参考文档

| 参考 | 内容 |
|------|------|
| [注意事项](references/gotchas.md) | 已知陷阱与错误/正确示例 |
| [DSL 参考](references/dsl-reference.md) | 完整的 I/U/M/D/C/G 操作符参考 |
| [常用模式](references/common-patterns.md) | 常用操作模式 |
| [变量模式](references/variable-patterns.md) | apply_variables + batch_edit 绑定模式 |
| [验证与恢复](references/validation-and-recovery.md) | 验证工作流程和错误恢复策略 |
