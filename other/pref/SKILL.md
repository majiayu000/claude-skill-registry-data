---
name: pref
description: Adjust thinking-tree recording preferences via natural language. Updates ~/.thinking-tree/.preferences.md which guides how the clarifier captures and routes insights.
---

# 调整记录偏好

用户通过自然语言描述偏好，系统更新 `~/.thinking-tree/.preferences.md`。

## 用法

```
/pref 不要记录 debug 过程
/pref 碎片标题用问句形式
/pref 更关注产品认知，技术细节不用记
/pref 显示当前偏好
```

`$ARGUMENTS` 是自然语言描述的偏好调整。

## 工具准备

本 skill 依赖 `AskUserQuestion` 提供选项式确认。进入交互前：

1. 若工具列表已含 `AskUserQuestion` → 直接使用
2. 未加载 → 先执行 `ToolSearch("select:AskUserQuestion")` 加载 schema
3. 加载失败（session 不支持该工具）→ 降级为纯文本确认：
   - 清晰列出编号选项（例如 `1) 确认 2) 不改 3) 调整`）
   - 明确告知回复格式（例如「回复编号」）
   - 不要跳过确认步骤

降级只影响呈现方式，不影响功能。

## 执行步骤

### 1. 读取当前偏好

读取 `~/.thinking-tree/.preferences.md`（如果存在）。

### 2. 理解意图

判断用户想要：
- **新增偏好** — 之前没有类似规则
- **修改偏好** — 调整已有规则的方向或程度
- **删除偏好** — 用户说"取消"、"恢复默认"等
- **查看偏好** — 用户说"显示"、"当前"、"有哪些"

### 3. 展示方案并确认

**不要直接修改文件**，先展示你打算怎么改，让用户确认：

```
我理解你想：不记录纯 debug 讨论

打算这样调整 .preferences.md：
  + 新增「记录范围」：不记录纯 debug 过程中的排查细节
  
确认？(y/n)
```

如果涉及修改或删除已有偏好，要明确展示前后对比：

```
打算这样调整：
  ~ 修改「记录范围」：
    原：只关注产品认知
    改：只关注产品认知和架构决策

确认？(y/n)
```

用 AskUserQuestion 工具获取确认，提供选项按钮（用户点击即可，不用打字）：
- 选项 1：「确认，就这样改」
- 选项 2：「不改了」  
- 选项 3：「调整一下」（用户补充说明后重新展示方案）

### 4. 用户确认后写入

确认后修改 `~/.thinking-tree/.preferences.md`，保持格式：

```markdown
# 记录偏好

> 通过 /pref 命令管理。clarifier 每轮读取此文件作为额外判断依据。

## 记录范围
- {什么要记、什么不记}

## 记录风格
- {标题风格、内容详略、结构偏好}

## 整理偏好
- {/reduce 时的分组偏好、保留倾向}
```

只写用户明确表达的偏好，不要自作主张填充默认值。空分区不写。

### 5. 反馈

```
偏好已更新：
  + 新增：不记录纯 debug 讨论

当前偏好共 N 条。
```

## 注意事项

- .preferences.md 是纯人类可读的 markdown，不是 JSON
- 每条偏好一行，用 `- ` 开头
- 偏好之间不能矛盾——如果新偏好和旧偏好冲突，替换旧的
- 用户说"重置"或"清空"时，删除所有条目但保留文件框架
- 这个文件只影响 clarifier 的判断，不改变 clarifier 的核心规则
