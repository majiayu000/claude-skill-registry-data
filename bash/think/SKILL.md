---
name: think
description: Toggle thinking-tree recording mode on/off. When enabled, a background recorder evaluates each conversation turn and writes insights to ~/.thinking-tree/.
---

# 切换思考模式

脚本位于本 skill 的 `../../scripts/think-toggle.js`（相对于本文件目录）。

用系统给出的 **Base directory for this skill** 构造绝对路径，运行一次 bash 即可：

```
node "$(echo '<base-directory>/../../scripts/think-toggle.js' | tr '\\' '/')"
```

**原样输出脚本的 stdout**，不要额外解释。
