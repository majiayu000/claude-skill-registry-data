---
name: ardot-generate-library
description: |
  在 Ardot 中构建可复用组件库或设计系统时使用此技能。
  涵盖从变量/设计令牌创建到使用正确变量绑定构建组件的完整工作流程，
  直至最终验证。

  触发条件："创建组件库"、"构建设计系统"、
  "制作可复用按钮"、"创建 UI 组件"、"构建组件集"、
  "设计系统"、"组件库"、"可复用组件"。
disable-model-invocation: false
---

# ardot-generate-library — 构建组件库

在 Ardot 中构建可复用组件库和设计系统。组件使用正确的变量绑定创建，以便响应主题/模式变化。

## 技能边界

- 构建**可复用组件**时使用此技能（按钮、卡片、输入框、导航栏等）
- 创建包含令牌和组件的**设计系统**时使用此技能
- 如果构建一次性页面/屏幕，请改用 [ardot-generate-design](../ardot-generate-design/SKILL.md)

## 前置条件

- `ardot-use` — 用于 batch_edit DSL 规则、变量绑定、注意事项
- `ardot-create-new-file` — 用于创建 Components 页面

---

## 阶段一：基础

### 1a：创建 Components 页面

```
create_new_page({name: "Components", select: false})
  → 记录 pageId（例如 "3:1672"）
```

### 1b：创建设计令牌（变量）

使用 `apply_variables` 创建变量基础。组件将绑定到这些变量。

```json
apply_variables({
  "variables": {
    "Colors": {
      "modes": ["Dark", "Light"],
      "variables": {
        "accent-primary": {
          "type": "COLOR", "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.91, "g": 0.44, "b": 0.29, "a": 1},
            "Light": {"r": 0.83, "g": 0.38, "b": 0.23, "a": 1}
          }
        },
        "accent-primary-text": {
          "type": "COLOR", "scopes": ["TEXT_FILL"],
          "valuesByMode": {
            "Dark": {"r": 1, "g": 1, "b": 1, "a": 1},
            "Light": {"r": 1, "g": 1, "b": 1, "a": 1}
          }
        },
        "bg-secondary": {
          "type": "COLOR", "scopes": ["ALL_FILLS"],
          "valuesByMode": {
            "Dark": {"r": 0.15, "g": 0.15, "b": 0.15, "a": 1},
            "Light": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1}
          }
        },
        "text-primary": {
          "type": "COLOR", "scopes": ["TEXT_FILL"],
          "valuesByMode": {
            "Dark": {"r": 0.95, "g": 0.95, "b": 0.95, "a": 1},
            "Light": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1}
          }
        },
        "border-default": {
          "type": "COLOR", "scopes": ["STROKE"],
          "valuesByMode": {
            "Dark": {"r": 0.25, "g": 0.25, "b": 0.25, "a": 1},
            "Light": {"r": 0.85, "g": 0.85, "b": 0.85, "a": 1}
          }
        }
      }
    },
    "Spacing": {
      "modes": ["Dark", "Light"],
      "variables": {
        "spacing-xs": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 4, "Light": 4}},
        "spacing-sm": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 8, "Light": 8}},
        "spacing-md": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 16, "Light": 16}},
        "spacing-lg": {"type": "FLOAT", "scopes": ["GAP"],
          "valuesByMode": {"Dark": 24, "Light": 24}},
        "radius-sm": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 6, "Light": 6}},
        "radius-md": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 8, "Light": 8}},
        "radius-lg": {"type": "FLOAT", "scopes": ["CORNER_RADIUS"],
          "valuesByMode": {"Dark": 12, "Light": 12}}
      }
    }
  }
})
```

**在追踪表中记录所有返回的变量 ID** 以供后续绑定使用。

> **硬性关卡：**
> - **禁止：** 在变量存在之前创建组件
> - **禁止：** 使用硬编码颜色创建组件（cornerRadius 除外）

---

## 阶段二：组件创建

按依赖顺序逐个构建组件：

```
原子组件（无依赖）：
  → Button、Input、Label、Icon、Badge、Avatar、Divider

分子组件（依赖原子组件）：
  → Card（使用 Button、Badge）、NavBar（使用 Button）、FormField（使用 Input、Label）
```

### 每个组件的工作流程

```
1. batch_edit (I) → 在 Components 页面上创建组件，设置 reusable:true
   - 对框架填充使用 boundVariables（暂不用于 TEXT 填充）
   - TEXT 子元素使用 fill: "#HEX" 占位符
   - 记录返回的组件节点 ID

2. batch_read → 验证组件结构

3. batch_edit (U) → 将变量绑定到 TEXT 子元素
   - 对每个 TEXT 节点应用 fills+boundVariables

4. batch_read → 验证变量绑定存在

5. capture_screenshot → 组件的视觉检查
```

### 示例：Button/Primary/md

```js
// 第一步：创建组件
btnPrimaryMd = I("3:1672", {
  "type": "FRAME",
  "name": "Button/Primary/md",
  "reusable": true,
  "width": "hug_contents", "height": 32,
  "layout": "horizontal",
  "paddingLeft": 16, "paddingRight": 16,
  "paddingTop": 6, "paddingBottom": 6,
  "cornerRadius": 8,
  "primaryAxisAlignItems": "CENTER",
  "counterAxisAlignItems": "CENTER",
  "fills": [{"type": "SOLID", "color": {"r": 0.91, "g": 0.44, "b": 0.29},
    "boundVariables": {"color": {"id": "VariableID:3:14", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "Label", "characters": "Button",
      "fontSize": 14, "fill": "#FFFFFF"}
  ]
})
// 返回：btnPrimaryMd → "3:544"，TEXT 子元素 → "3:545"

// 第三步（单独的 batch_edit）：绑定文本颜色变量
U("3:545", {
  "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1},
    "boundVariables": {"color": {"id": "VariableID:3:15", "type": "VARIABLE_ALIAS"}}}]
})
```

### 示例：带子元素的卡片

```js
card = I("3:1672", {
  "type": "FRAME",
  "name": "Card/Default",
  "reusable": true,
  "width": 320, "height": "hug_contents",
  "layout": "vertical",
  "paddingLeft": 20, "paddingRight": 20,
  "paddingTop": 20, "paddingBottom": 20,
  "cornerRadius": 12,
  "fills": [{"type": "SOLID", "color": {"r": 0.15, "g": 0.15, "b": 0.15},
    "boundVariables": {"color": {"id": "VariableID:3:16", "type": "VARIABLE_ALIAS"}}}],
  "strokes": [{"type": "SOLID", "color": {"r": 0.25, "g": 0.25, "b": 0.25},
    "boundVariables": {"color": {"id": "VariableID:3:18", "type": "VARIABLE_ALIAS"}}}],
  "children": [
    {"type": "TEXT", "name": "Title", "characters": "Card Title",
      "fontSize": 18, "fill": "#F2F2F2"},
    {"type": "TEXT", "name": "Body", "characters": "Card description text.",
      "fontSize": 14, "fill": "#AAAAAA"}
  ]
})
```

## 阶段三：验证

### 3a：结构验证

```json
batch_read({parentId: "<ComponentsPageId>"})
```

检查：
- 所有计划的组件存在且名称正确
- 所有组件都有 `reusable: true`
- 所有组件都有预期的子元素

### 3b：变量绑定验证

对于每个组件，验证变量绑定存在：

```json
batch_read({nodeIds: ["<componentId1>", "<componentId2>", ...]})
```

检查 `fills[].boundVariables` 和 `strokes[].boundVariables` 不为空。

### 3c：视觉验证

```json
capture_screenshot({
  "nodeIds": ["<所有组件 ID>"],
  "screenShotDir": "/tmp/ardot-components"
})
```

审查所有组件截图以确保视觉正确性。

## 硬性关卡 — 禁止的快捷方式

- **禁止：** 在变量存在之前创建组件
- **禁止：** 在组件填充中硬编码十六进制颜色（使用 boundVariables）
- **禁止：** 跳过 TEXT 两步变量绑定
- **禁止：** 使用与设计令牌不匹配的硬编码字体大小
- **禁止：** 在原子依赖之前创建依赖（分子）组件

## 推荐命名约定

```
<类别>/<变体>/<大小>

示例：
  Button/Primary/sm
  Button/Primary/md
  Button/Primary/lg
  Button/Secondary/md
  Button/Ghost/md
  Card/Default
  Card/Elevated
  Input/Default
  Input/Error
  Badge/Success
  Badge/Warning
```

使用 `/` 作为分隔符 — 这会创建与 Figma 兼容的组件分组。
