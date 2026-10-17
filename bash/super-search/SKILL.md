---
name: super-search
description: "搜索您的编码记忆。当用户询问过去的工作、以前的会话、某些内容是如何实现的、他们之前做过什么，或者想要召回以前会话中的信息时使用。"
allowed-tools: "bash (node: *)"
---

# 超级搜索 (Super Search)

在超级记忆库中搜索过去的编码会话、决策和保存的信息。

## 如何搜索

运行搜索脚本，使用用户的查询语句和可选的范围标志：

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" [--user|--repo|--both] "此处输入用户查询内容"
```

### 范围标志 (Scope Flags)

- `--both`（默认）：并行搜索团队成员之间的个人会话记忆和项目记忆。
- `--user`：跨会话搜索个人/用户记忆。
- `--repo`：在团队成员之间搜索项目/存储库 (Repository) 记忆。

## 使用示例

- 用户问“我昨天做了什么”：

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" "昨天的工作内容 最近活动"
  ```

- 用户询问“我们是如何实现身份验证的”（针对特定项目）：

  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" --repo "身份验证实现"
  ```

- 用户询问“我的编码偏好是什么”：
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/search-memory.cjs" --user "编码偏好 风格"
  ```

## 结果处理

该脚本将输出带有时间戳和相关性分数的格式化记忆结果。请将这些结果清晰地呈现给用户，并在需要时尝试使用不同的关键词再次搜索。
