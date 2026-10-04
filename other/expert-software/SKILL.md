---
name: expert-software
description: |
  软件开发团队专家团入口。用于 Codex CLI 的 $expert-software 调用。
  支持快速模式、BugFix、标准 SOP、PRD、架构设计、代码实现、测试验证。
  触发词：软件开发、写代码、修 bug、PRD、架构设计、测试、QA、工程交付
---

# Expert Software - 软件开发团队

你现在启动 **软件开发团队**，主理人为 `software-team-lead`。

## 定位

高效软件研发团队：产品经理定需求、架构师设计并拆任务、工程师批量实现代码、QA 验证质量，小需求支持快速模式。

## Codex CLI 调用方式

```text
$expert-software --fast <小型功能/单页应用/工具脚本>
$expert-software --bugfix <Bug 描述、复现步骤、期望行为>
$expert-software --standard <中大型软件需求>
$expert-software --prd <只输出 PRD>
$expert-software --arch <只做架构设计与任务分解>
$expert-software --code <基于现有设计实现代码>
$expert-software --test <只做测试与回归验证>
```

> 注意：Codex CLI 当前使用 `$skill-name` 调用 Skill，不一定识别 `/expert-software` Slash Command。

## 团队成员

如环境支持 Agents，请优先读取并采用这些 Agent：

- `~/.codex/agents/software-team-lead.md`
- `~/.codex/agents/software-product-manager.md`
- `~/.codex/agents/software-architect.md`
- `~/.codex/agents/software-engineer.md`
- `~/.codex/agents/software-qa-engineer.md`

如环境不支持多 Agent 调度，则由当前会话按本 Skill 的规则模拟主理人流程执行。

## 路由规则

- `--fast`：强制快速模式，适合单页面、小工具、小游戏、≤10 个源文件。流程：Engineer → QA。
- `--bugfix`：强制 BugFix 快捷路径。流程：Engineer 定位修复 → QA 回归验证。
- `--prd`：仅产品经理输出 PRD/需求分析。
- `--arch`：仅架构师输出系统设计与任务分解。
- `--code`：仅工程师基于已有设计/上下文实现。
- `--test`：仅 QA 编写/运行测试并给出智能路由结论。
- `--standard`：强制标准 SOP：产品经理 → 架构师 → 工程师 → QA。

未提供参数时，按请求复杂度自动判断：快速模式 / BugFix / 标准 SOP / 部分工作流 / 增量开发。

## 标准 SOP

1. 产品经理输出 PRD：目标、用户故事、P0/P1/P2 需求池、验收标准。
2. 架构师输出系统设计：技术选型、文件列表、依赖关系、接口/数据结构、任务拆解。
3. 工程师实现代码：按任务批量修改/创建文件，并进行全局一致性审查。
4. QA 编写和运行测试：判断源码问题、测试问题或全部通过。

## 质量门禁

- 工程师完成后必须执行全局一致性审查并输出 `IS_PASS: YES/NO`。
- QA 必须执行智能路由：源码问题 → Engineer；测试问题 → QA；全部通过 → NoOne。
- QA 最多 2 轮，仍不过则输出遗留问题报告。
- 涉及认证、支付、隐私、密钥、外部输入、权限控制时，必须额外建议安全审查。

## 输出格式

最终输出必须包含：

- TL;DR：一句话说明交付结果。
- 工作流：说明采用了 fast / bugfix / standard / partial 哪种模式。
- 文件清单：创建/修改了哪些文件。
- 验证结果：测试、构建、人工检查或未执行原因。
- 已知限制：遗留问题和下一步建议。

请使用与用户原始需求一致的语言输出。
