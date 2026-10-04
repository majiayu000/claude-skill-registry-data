---
name: ardot-style-guide
description: |
  从头设计或为 Ardot 项目应用视觉主题时使用此技能。
  涵盖 `search_style_guide` → `build_style_guide` 工作流程，用于发现和应用完整的设计系统（颜色、排版、间距、布局模式）。

  触发条件："设计落地页"、"创建仪表板"、"应用深色主题"、
  "设置设计系统"、"选择调色板"、"为应用选择字体"、
  "样式指南"、"视觉风格"、"外观和感觉"。
disable-model-invocation: false
---

# ardot-style-guide — 样式指南搜索与构建

通过 `search_style_guide` → `build_style_guide` 工具链发现和应用完整的设计系统。Ardot 独有的能力，Figma 没有等效功能。

## 技能边界

- 当用户想要从头建立视觉风格时使用此技能
- 在任何创建带样式 UI（颜色、排版）的 `batch_edit` 之前使用此技能
- 如果用户已有已建立的设计系统和已知令牌，可跳过此技能
- `build_style_guide` 的输出是**权威性的** — 所有下游工具必须严格遵循其值

## 前置条件

- 必须已调用 `fetch_editor_state(includeSchema: true)`
- 应为目标设计类型加载 `fetch_guidelines(topic)`

---

## search_style_guide — 三轮回退协议

### 第一轮：关键词搜索

提供特定关键词以定位用户意图。

```
search_style_guide({
  "topic": "landing-page",        // 或 web-app、mobile-app、slides、table
  "designKeywords": "SaaS dashboard modern clean professional",
  "colorKeywords": "dark mode cool blue professional",
  "typographyKeywords": "modern sans-serif clean readable",
  "layoutKeywords": "dashboard analytics cards grid"
})
```

**收到结果后**，逐一审查每个领域：

- **style**：样式类别是否与请求的视觉风格匹配？
- **color**：检查背景、卡片和前景值。如果用户想要深色模式但所有背景值都是浅色（#F_xxxx 范围），则此领域没有合适匹配。
- **typography**：情绪是否匹配？字体是否可用（使用 `get_available_fonts` 检查）？
- **layout**：模式是否适合页面类型？

如果某个领域的所有候选都合适 → 继续到 `build_style_guide`。

### 第二轮：完整目录（如果任何领域没有合适匹配）

对于第一轮没有合适匹配的领域，再次调用 `search_style_guide`，对该领域的关键词使用 `true` 以获取完整目录：

```
search_style_guide({
  "topic": "landing-page",
  "designKeywords": "SaaS dashboard",
  "colorKeywords": true,           // 颜色的完整目录
  "typographyKeywords": true       // 排版的完整目录
})
```

### 第三轮：自身设计知识（仅在第二轮也失败时）

仅对第二轮后仍无合适匹配的领域，你可以使用自己的设计知识。这应该很少见。

---

## build_style_guide — 权威性约束

一旦你在所有领域做出选择，调用 `build_style_guide`：

```json
build_style_guide({
  "selections": {
    "style": 2,          // 搜索结果中的索引或名称
    "color": 1,
    "typography": 3,
    "layout": 0
  }
})
```

### 关键：返回的设计系统是权威性的

`build_style_guide` 响应提供必须使用的**精确值**：

- **颜色**：使用精确的 `#HEX` 或 `{r, g, b}` 值 — 不要调整
- **排版**：使用精确指定的字体系列、大小、粗细
- **边框半径**：使用精确的 px 值
- **间距**：使用精确的 px 值
- **效果**：使用精确的阴影/模糊参数

> **硬性关卡**：如果设计系统说背景是 `#FAF5FF`，使用 `#FAF5FF`
> （转换为 0–1 范围用于 batch_edit）。如果你意识到它与用户意图冲突
> （例如，用户想要深色但得到浅色），返回 `search_style_guide` 使用更正后的关键词
> — 不要静默覆盖值。

### 将样式指南值转换为 batch_edit

样式指南十六进制颜色 → batch_edit {r, g, b} 0–1 格式：
```
#FAF5FF → {r: 0.98, g: 0.96, b: 1.0}
#1A1A2E → {r: 0.10, g: 0.10, b: 0.18}
#E8714A → {r: 0.91, g: 0.44, b: 0.29}
```

---

## 每个领域的选择策略

### 样式
将样式类别名称与用户描述匹配。信任内容而非搜索分数 — 匹配意图的低分候选比不相关的高分候选更好。

### 颜色
具体检查背景（主表面颜色）、卡片（次表面）和前景（文本/图标）值。这三个值告诉你调色板是浅色还是深色。

### 排版
在选择之前使用 `get_available_fonts` 验证字体可用性。如果两种字体都不可用，字体配对就没有用。检查标题和正文字体。

### 布局
将模式名称与功能意图匹配。例如，"pricing" → 寻找比较/表格布局；"dashboard" → 寻找卡片网格布局。

---

## topic 参数指南

| topic | 用途 | 典型 designKeywords |
|-------|------|---------------------|
| `landing-page` | 营销页面、主页、促销网站 | "hero section"、"CTA"、"features" |
| `web-app` | SaaS 仪表板、管理面板、内部工具 | "dashboard"、"data table"、"sidebar" |
| `mobile-app` | iOS/Android 应用屏幕 | "bottom nav"、"cards"、"list" |
| `slides` | 演示文稿 | "title slide"、"content"、"chart" |
| `table` | 数据表和仪表板 | "data grid"、"filters"、"pagination" |

---

## 完整工作流程总结

```
1. fetch_editor_state(includeSchema: true)
2. fetch_guidelines(topic)                          → 页面类型的设计规则
3. get_available_fonts                              → 检查字体可用性
4. search_style_guide (第一轮)                      → 关键词搜索
5. [如需要] search_style_guide (第二轮)             → 完整目录回退
6. build_style_guide(selections)                    → 获取权威设计令牌
7. apply_variables                                  → 创建与令牌匹配的变量
8. batch_edit                                       → 使用精确的令牌值构建 UI
```
