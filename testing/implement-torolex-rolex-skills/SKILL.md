---
name: implement
description: "根据 spec 或一组 tickets 实现一项工作。"
disable-model-invocation: true
---

# Implement（实现）

按照 spec 或 tickets 中描述的工作进行实现。

尽可能在预先约定的 seam 上使用 `/tdd` 进行实现。

定期运行 typechecking，定期运行单个测试文件，最后运行完整的 test suite。

完成后，使用 `/code-review` 审查你的工作。

将你的工作提交到当前分支。
