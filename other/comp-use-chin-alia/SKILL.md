---
name: comp-use-chin-alia
description: 中文关键词触发 open-computer-use MCP 工具。提供截屏、点击、输入等操作的中文别名。
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [mcp, computer-use, chinese, aliases]
    related_skills: [native-mcp]
---

# Computer Use 中文别名

当用户使用以下中文关键词时，优先调用对应的 MCP 工具，而不是进行通用推理。

## 关键词映射

### 截屏 / 查看
- `截屏` / `截图` / `屏幕` / `看看` / `当前界面` → `get_app_state`
  - 需要指定应用，例如：`截屏 Chrome`、`看看访达`
  - 如果未指定应用，默认使用当前活动应用

### 点击
- `点击` / `点一下` / `按一下` / `选择` → `click`
  - 支持指定元素索引或坐标
  - 例如：`点击第3个元素`、`点击坐标(100,200)`

### 输入
- `输入` / `打字` / `键入` / `填写` → `type_text`
  - 例如：`输入你好`、`在搜索框输入关键词`

### 按键
- `按` / `按下` / `敲` → `press_key`
  - 例如：`按回车`、`按Tab`、`按Command+C`

### 滚动
- `滚动` / `翻页` / `下滑` / `上滑` → `scroll`
  - 例如：`向下滚动`、`滚动3页`

### 拖拽
- `拖拽` / `拖动` / `拉` → `drag`
  - 例如：`从A拖到B`

### 列出应用
- `列出应用` / `看看有什么应用` / `运行中的应用` → `list_apps`

### 设置值
- `设置` / `修改` / `填入` → `set_value`
  - 例如：`设置用户名为admin`

### 辅助操作
- `右键菜单` / `更多操作` → `perform_secondary_action`

## 使用规则

1. **优先匹配**：当用户输入包含上述关键词时，优先考虑调用 MCP 工具。
2. **参数推断**：从用户输入中推断应用名称、元素索引、坐标等参数。
3. **确认模糊指令**：如果指令模糊（例如“点击”没有目标），询问具体目标。
4. **错误处理**：如果权限不足，提示用户运行 `open-computer-use doctor` 授权。

## 示例

用户：`截屏 Chrome`
→ 调用 `get_app_state(app="com.google.Chrome")`

用户：`点击第2个按钮`
→ 调用 `click(element_index="2", app=当前应用)`

用户：`输入你好世界`
→ 调用 `type_text(text="你好世界", app=当前应用)`

用户：`按回车`
→ 调用 `press_key(key="Return", app=当前应用)`

## 注意事项

- 需要 macOS 辅助功能和屏幕录制权限。
- 如果操作失败，检查权限状态。
- 坐标使用截图像素坐标系。
- 元素索引来自 `get_app_state` 返回的无障碍树。