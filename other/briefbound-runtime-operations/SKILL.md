---
name: briefbound-runtime-operations
description: "Use when a deployed or local service fails to start, misbehaves at runtime, or needs deployment verification: environment-vs-code triage, the port/health/business evidence ladder, service lifecycle, or safe restart and rollback; do not use for source-code bugs, PR checks, or post-merge cleanup."
license: MIT
---

# Briefbound Runtime Operations

## 目标

让“服务起不来、跑不对、要不要重启”有可复现的证据链。它负责部署与运行故障的分流、验证与恢复，不负责源码 bug、CI/PR 检查或合并后的资源清理。

## Briefbound task contract

- Context Boundary: 服务清单与端口、启动方式与入口、配置与数据目录、日志位置、预期行为与最近变更。
- Output Contract: 故障分流结论、验证阶梯证据、已执行动作、恢复或回滚结果、剩余风险。
- Allowed Action: 读取状态与日志、启动/停止有归属证明的服务、按授权改配置或回滚；不修改业务实现逻辑。
- Success Evidence: 每级验证的命令与输出（监听、健康、真实业务）、分流依据、变更前后对照。
- Stop Condition: 归属不明的进程或数据目录、需要改源码才能恢复、生产或远程环境未授权、故障无法复现。
- Route Out: 源码缺陷 `briefbound-bug-review`；合并后残留 `briefbound-development-cleanup`；多会话进程归属冲突 `briefbound-thread-coordination`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，先说分流结论和证据，再给动作；不整屏贴日志，引用关键行并注明来源；Route Out 仅以 Briefbound task contract 为准，有自然闸门时末行 `下一步建议: <一个具体动作>`，否则继续已授权工作。

## 激活闸门

请求涉及部署、启动、端口、进程、日志、健康检查、环境配置或运行故障恢复时进入。症状指向源码逻辑错误（可定位到代码行为的确定性错误）时交 `briefbound-bug-review`；两边都可能时先在这里分流。

## 验证阶梯

三级证据逐级取证，不可互换：

1. 端口监听：进程在指定端口 listen。
2. 健康接口：health/readiness 接口返回预期状态。
3. 真实业务：一个真实请求走通关键路径。

端口监听不等于健康接口通过，健康接口通过不等于真实业务成功。上报时写清验证到了哪一级；只到第一级就声称服务可用是未验证。

## 故障分流

先分流环境还是代码，再动手：

- 环境征象：端口占用、依赖缺失、权限、路径/编码、配置不匹配、数据目录锁、磁盘或内存耗尽。
- 代码征象：确定性堆栈、特定输入必现、最近提交可关联。

环境故障就地修复（配置、依赖、目录、进程）；代码故障带证据交 `briefbound-bug-review`，不在运维流程里顺手改实现。同一现象两次修复后复发，升级为根因排查而不是再次重启。

## 服务生命周期

- 启动：前台验证通过后再转后台；后台服务隐藏窗口并重定向日志，启动器记录 worktree、端口、数据目录和最终 listener。
- 停止：按端口与命令行确认归属后才停止；不得广泛结束进程族，更不得按名字批量杀 Node/Python/模型进程。
- 证据：停止后确认端口释放、子进程退出，再声称关闭完成。

停止或重启会影响他人正在运行的任务时，先协商（`briefbound-thread-coordination`），不先斩后奏。

## 重启与回滚

先取证后重启：保留现场证据（日志尾、进程表、配置快照）再执行变更。回滚遵循“最后已知良好”原则：恢复到上一个可验证状态并重新走验证阶梯；回滚本身也要留下证据。破坏性动作（清数据目录、重置状态）单独请求授权。

## 日志与敏感信息

读日志定位问题，但不把密钥、Token、真实用户数据或完整响应正文复制进汇报或新文件；引用时脱敏。发现疑似泄漏凭证时只报告位置和处置建议，不扩散内容。

## 输出

```text
结论: <分流判断 + 当前验证到哪一级>
证据: <关键命令输出与日志行>
已执行: <启动/停止/配置/回滚动作>
剩余风险: <未验证层级或需代码修复的项>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```
