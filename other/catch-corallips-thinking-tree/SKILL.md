---
name: catch
description: Manually capture missed insights from recent conversation. Use when thinking-tree's auto-recording missed something valuable. Accepts a natural language hint about what to capture.
---

# 补录捕获

当自动记录遗漏了有价值的对话认知时，用户可以用这个命令手动补录。

## 用法

```
/catch 我们刚才关于碎片转化速度的讨论
/catch 上面 AI 分析的那个架构边界的判断
/catch 最近几轮关于捕获和思考关系的讨论
```

`$ARGUMENTS` 是自然语言提示，描述想要捕获的内容方向。

## 执行步骤

### 1. 回溯对话

回顾最近 10-15 轮对话内容（当前会话内），重点关注：
- 用户提示方向（`$ARGUMENTS`）相关的讨论
- AI 回复中的分析结论、架构判断、独立洞察
- 对话碰撞中产生的新认知

### 2. 提取认知

从回溯的对话中提取值得记录的独立认知点。每个点必须：
- 脱离对话上下文后仍然可理解
- 不与 `~/.thinking-tree/fragments.md` 中已有碎片重复
- 有明确的一个点（不是模糊的"讨论了 XXX"）

### 3. 路由判断

对每个提取出的认知点：
- 独立观点 → 碎片（fragment）
- 明确的疑问 → 问题（question）
- 具体可执行 → 行动项（todo）

### 4. 写入

通过原子写入脚本逐条写入：

```bash
echo '{"type":"fragment","title":"#标签 标题（日期）","body":"内容描述。"}' | node ~/.thinking-tree/bin/write-item.js
```

### 5. 输出确认

列出所有补录的条目：

```
补录完成：
📝 #标签1 标题1
📝 #标签2 标题2
❓ 问题标题
共 N 条
```

## 注意事项

- 先读 `~/.thinking-tree/fragments.md` 确认不重复
- 碎片标题加 `#标签` 前缀和日期后缀，与现有碎片风格一致
- 如果 `$ARGUMENTS` 为空，扫描最近 5 轮对话，自动识别遗漏
- 每次补录不超过 5 条，避免噪音
- 写入使用 `write-item.js`，不要直接 Edit/Write 文件
