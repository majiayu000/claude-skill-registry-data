---
name: unfreeze
version: 0.1.0
description: |
  清除 /freeze 建立的目录边界，让所有目录重新可编辑。
  适用于想扩大编辑范围但不想重开会话的时候。 (gstack)
allowed-tools:
  - Bash
  - Read
---
<!-- 中文参考译文。 -->

# /unfreeze

移除 `/freeze` 写下的目录边界，让编辑权限回到“全目录可写”。

## 行为

- 如果找到 `freeze-dir.txt`，删除它，并告诉用户之前锁定的是哪个目录。
- 如果当前没有设置过边界，就明确告诉用户“没有 freeze boundary”。
- `/freeze` 的 hook 仍然会保留在会话里，只是状态文件不存在时会自动放行。
