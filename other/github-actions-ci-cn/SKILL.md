---
name: github-actions-ci-cn
description: Use when diagnosing, summarizing, or fixing GitHub Actions CI failures in Chinese, including failed checks, logs, workflow files, flaky tests, and safe maintainer next steps.
---

# GitHub Actions CI CN

用在开源维护者需要排查 GitHub Actions 失败、解释失败原因、决定是否重跑或修复 PR 时。目标是把红色 CI 变成清楚的维护动作。

## 适用场景

- 用户说“CI 挂了”“GitHub Actions 为什么失败”“帮我看这个 check”。
- PR 合并前需要判断失败是否由代码变更、环境问题、依赖问题或 flaky test 引起。
- 需要用中文给贡献者说明失败原因和下一步。
- 需要修改 workflow、测试或项目配置来恢复 CI。

## 不适用场景

- 用户只需要解释本地测试失败，且没有 GitHub Actions 上下文。
- 失败涉及生产密钥、私有日志或安全漏洞，且日志未脱敏。
- 用户要求跳过失败检查强行合并。

## 工作流

1. 收集失败上下文。
   - 查看失败的 workflow、job、step、exit code、日志尾部和相关 PR diff。
   - 如果有 `gh` CLI 或 GitHub connector，优先读取 check run 和 failed logs。
   - 如果没有远程权限，要求用户提供失败日志摘要或链接。

2. 分类失败原因。
   - 代码回归：测试断言、类型检查、lint、构建失败。
   - 环境问题：依赖下载、缓存、runner、权限、路径差异。
   - 配置问题：workflow 触发条件、matrix、secrets、权限、工作目录。
   - flaky：超时、竞态、网络依赖、顺序依赖。

3. 建立最小复现路径。
   - 找到本地可运行的等价命令。
   - 优先跑失败 job 对应的最小命令，而不是全量 CI。
   - 记录无法本地复现的原因。

4. 提出修复。
   - 如果是代码问题，修代码并补测试。
   - 如果是 workflow 问题，最小修改 workflow。
   - 如果是 flaky，先收集证据，再建议重跑、加等待、隔离状态或去除网络依赖。

5. 输出维护者回复。
   - 中文说明失败原因、影响范围、建议动作。
   - 如果需要贡献者补充信息，列出具体信息，不要泛泛说“请检查”。

## 输出格式

```text
结论：

失败位置：
- workflow / job / step：
- 关键日志：

判断：
- 类型：代码回归 / 环境问题 / 配置问题 / flaky / 待确认
- 依据：

建议动作：
1. ...
2. ...

本地验证：
- 已运行：
- 未运行：

给贡献者的回复：
...
```

## 验证方式

- 修复后至少运行失败 job 对应的本地最小命令。
- 如果改了 workflow，检查 YAML 语法、工作目录、权限和触发条件。
- 如果无法运行 GitHub Actions，本地说明剩余风险，并建议远端重跑。

## 安全边界

- 不要复述日志中的 token、cookie、私有 URL、邮箱或其他敏感信息。
- 不要建议关闭必需检查或降低安全权限来“让 CI 绿”。
- 不要把一次偶发网络失败直接当成 flaky 结论；至少说明证据不足。
