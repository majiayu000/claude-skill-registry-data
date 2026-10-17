---
name: to-pitch
description: 打包 prototype、spec、implementation notes 成一份争取 buy-in 和批准的文档。
disable-model-invocation: true
---

把成果打包成一份可直接分享的文档，目标是获得 buy-in 和批准。一份文档，两条阅读路径：

- reviewer 和我有同样的 unknowns，缺背景：explainer 部分讲清问题和直觉，加速理解
- 专家已经懂领域，缺确认：pitch 部分摆出我考虑到的 unknowns 和常见失败点的处置，加速批准

流程：

1. 收集输入：prototype、spec、implementation-notes.md。其中 Deviations 是给专家看的关键部分。
2. 开头放 demo（GIF 或截图），先让人看到东西在动。
3. 按目的地格式化：Slack 消息、共享文档或 PR 描述。
4. 分支：用户提到 remote、手机、Tailscale 时 → 读 [REMOTE.md](./REMOTE.md)，按其流程交付；否则到此为止。

完成标准：普通路径 = 粘贴即发；remote 分享 = REMOTE.md 的完成标准。
