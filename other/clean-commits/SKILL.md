---
name: clean-commits
description: 生成干净、符合仓库既有风格的 git commit message。当用户要提交代码、让你写/改 commit message、拆分提交，或要求提交历史保持干净时使用。只写改动本身——不加 AI 共同作者署名，不加任何生成工具水印。
---

# Clean Commits

帮用户写出只描述改动本身的 commit message：主题行准确、正文讲清动机、零噪音。

## 输入

- 已暂存或未暂存的代码改动（自己用 git 命令读取，不需要用户描述）
- 用户可能附带的上下文（关联 issue、改动动机）；没有就从 diff 推断

## 工作流

1. `git diff --staged` 读实际改动（无暂存内容则看 `git diff`）
2. `git log --oneline -15` 观察仓库既有风格：是否用 Conventional Commits
   前缀（`feat:`/`fix:`…）、中文还是英文——**跟随既有风格，不要另起一套**
3. 从改动的*效果*（而非代码机制）提炼主题行
4. 动机不明显时补正文，说明*为什么*改，而不是复述 diff
5. 若暂存区混入多个不相关改动，先建议拆分再提交

## 输出格式

- 主题行：祈使语气，≤ 72 字符，无句号
- 正文（可选）：与主题行空一行，每行 ≤ 72 字符，只写动机与取舍
- **禁止出现**：
  - `Co-Authored-By:` 等 AI 共同作者署名
  - `🤖 Generated with ...` 等任何工具水印
  - 仓库没在用的 issue 标签、emoji 前缀等额外噪音

示例：

```
fix: 配置缺 timeout 字段时回退默认值

v0.3 写出的配置文件完全没有 timeout 键，加载时直接崩溃。
改为缺键时应用默认值，而不是假设键一定存在。
```

```
add retry with backoff to webhook delivery
```
