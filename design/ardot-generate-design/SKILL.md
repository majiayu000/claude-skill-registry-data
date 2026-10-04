---
name: ardot-generate-design
description: |
  在 Ardot 中从头构建完整页面、屏幕或多区块 UI 布局时，将此技能与 ardot-use 配合使用。
  通过 6 步工作流程编排多个 MCP 工具：初始化 → 样式系统 → 变量 → 骨架 →
  逐区块构建 → 验证。

  触发条件："在 Ardot 中创建落地页"、"构建登录屏幕"、
  "在 Ardot 中设计仪表板"、"制作设置页面"、"创建个人资料屏幕"、
  "在 Ardot 中构建此页面"、"将此设计转换为 Ardot"。
disable-model-invocation: false
---

# ardot-generate-design — 构建页面和屏幕

在 Ardot 中使用设计系统组件、变量和样式构建完整的页面、视图和多区块 UI 容器。不使用硬编码的十六进制/像素值。

## 技能边界

- 当交付物是**组合页面或屏幕**时使用此技能（登录页面、仪表板、设置面板、落地页等）
- 如果用户想要创建**可复用组件**，切换到 [ardot-generate-library](../ardot-generate-library/SKILL.md)
- 如果用户只想**查询样式指南**，直接使用 [ardot-style-guide](../ardot-style-guide/SKILL.md)

## 前置条件

**开始前必须加载：**
- `ardot-use` — 用于 batch_edit DSL 规则、变量绑定、注意事项
- `ardot-create-new-file` — 用于 create_new_page 用法
- `ardot-style-guide` — 用于 search_style_guide → build_style_guide 工作流程

---

## 必需工作流程（6 步）

### 第一步：初始化

获取目标页面类型的编辑器状态和设计指南。

```
fetch_editor_state(includeSchema: true)
fetch_guidelines(topic)          // landing-page | web-app | mobile-app | slides | table
fetch_file_info                  // 检查写入权限
```

### 第二步：建立样式系统

如果尚不存在设计系统：

```
search_style_guide → build_style_guide  （完整协议见 ardot-style-guide）
get_available_fonts                    （验证字体可用性）
```

如果文件中已存在设计系统：

```
fetch_variables                        （获取现有变量 ID 和值）
batch_read({parentId: "<ComponentsPage>"})  （发现现有可复用组件）
```

### 第三步：创建变量

将样式指南的设计令牌转换为 Ardot 变量：

```
apply_variables({
  "Colors": {
    "modes": ["Dark"],
    "variables": {
      "bg-primary": { "type": "COLOR", "scopes": ["ALL_FILLS"],
        "valuesByMode": {"Dark": {r: ..., g: ..., b: ..., a: 1}} },
      "text-primary": { "type": "COLOR", "scopes": ["TEXT_FILL"],
        "valuesByMode": {"Dark": {r: ..., g: ..., b: ..., a: 1}} },
      ...build_style_guide 中的所有颜色...
    }
  },
  "Spacing": {
    "modes": ["Dark"],
    "variables": {
      "spacing-sm": { "type": "FLOAT", "scopes": ["GAP"],
        "valuesByMode": {"Dark": 8} },
      "spacing-md": { "type": "FLOAT", "scopes": ["GAP"],
        "valuesByMode": {"Dark": 16} },
      "radius-sm": { "type": "FLOAT", "scopes": ["CORNER_RADIUS"],
        "valuesByMode": {"Dark": 6} }
    }
  }
})
```

**记录所有返回的变量 ID** — 在第五步绑定时需要它们。

> **硬性关卡 — 禁止的快捷方式：**
> - **禁止：** 在变量创建之前开始 batch_edit
> - **禁止：** 使用硬编码十六进制值代替变量（cornerRadius 除外）

### 第四步：创建页面骨架

```
create_new_page({name: "<页面名称>", select: false})
  → 记录 pageId
```

然后创建包装框架和区块容器：

```js
// 骨架的单个 batch_edit 调用
wrapper = I("<pageId>", {
  "type": "FRAME", "name": "<屏幕名称>",
  "width": 375, "height": "hug_contents",
  "layout": "vertical",
  "fills": [{"type": "SOLID", "color": {r:..., g:..., b:...},
    "boundVariables": {"color": {"id": "VariableID:X:Y", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "FRAME", "name": "Header", "width": "fill_container", "height": 56,
      "layout": "horizontal", "paddingLeft": 16, "paddingRight": 16,
      "counterAxisAlignItems": "CENTER"},
    {"type": "FRAME", "name": "Content", "width": "fill_container",
      "height": "hug_contents", "layout": "vertical",
      "paddingLeft": 24, "paddingRight": 24, "paddingTop": 24, "paddingBottom": 24},
    {"type": "FRAME", "name": "Footer", "width": "fill_container", "height": 48}
  ]
})
```

记录每个区块框架的节点 ID（Header、Content、Footer 等）。

### 第五步：构建每个区块

一次构建一个区块。每个区块使用自己的 `batch_edit` 调用（≤25 个操作）。

```
对于每个区块：
  1. 准备该区块的操作字符串
  2. batch_edit → 创建区块内容
  3. batch_read → 验证结构
  4. batch_edit (U) → 绑定变量（特别是 TEXT 节点）
  5. batch_read → 验证绑定
```

**TEXT 节点需要两步绑定**（见 ardot-use 注意事项 #4）：
- I() → 使用 `fill: "#HEX"` 创建
- 单独的 batch_edit U() → 使用 fills+boundVariables 绑定变量

> **硬性关卡 — 禁止的快捷方式：**
> - **禁止：** 在 I() 中直接将变量绑定到 TEXT 节点
> - **禁止：** 使用来自先前 batch_edit 调用的绑定名称
> - **禁止：** 每个 batch_edit 调用超过 25 个操作

### 第六步：验证

```
capture_screenshot({
  "nodeIds": ["<screenNodeId>", ...所有屏幕节点 ID],
  "screenShotDir": "/tmp/ardot-verify"
})
```

**审查所有截图**检查：
- 视觉正确性（颜色、间距、对齐）
- 文本未被裁剪或溢出
- 所有区块存在且布局正确

如果发现问题 → `batch_edit` 修复 → 再次 `capture_screenshot`。

## 变量 ID 追踪

维护所有变量 ID 的持续记录：

| 变量名 | 变量 ID |
|--------|---------|
| bg-primary | VariableID:3:14 |
| text-primary | VariableID:3:15 |
| accent-warm | VariableID:3:16 |
| spacing-md | VariableID:3:17 |
| radius-sm | VariableID:3:18 |

从 `apply_variables` 返回值或 `fetch_variables` 获取。

## 批次管理 — 25 操作限制

当区块需要超过 25 个操作时：

1. **按逻辑子区块拆分** — 一个调用中的头部项目，另一个调用中的内容卡片
2. **将创建与绑定分离** — 一个调用中的 I()，下一个调用中的 U() 绑定
3. **合并小型独立更新** — 将多个单节点 U() 调用合并为一个批次

## 错误恢复

如果 batch_edit 失败：
1. 读取错误 — 它是原子性的，文件未更改
2. 修复问题（通常是：错误的节点 ID、错误的 pageId 或语法错误）
3. 重试 batch_edit 调用

详细恢复策略见 [ardot-use references/validation-and-recovery.md](../ardot-use/references/validation-and-recovery.md)。
