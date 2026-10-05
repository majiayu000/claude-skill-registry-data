---
name: issue-triage-cn
description: Use when triaging GitHub issues or bug reports in Chinese, classifying priority, reproducing evidence, labels, and actionable maintainer replies.
---

# Issue Triage CN

用在维护开源仓库、整理 GitHub issue、处理 bug report 和 feature request 时。目标是把模糊反馈变成可执行维护动作。

## 适用场景

- 用户要你“整理这些 issues”“判断优先级”“帮我回复这个 issue”。
- issue 描述不完整，需要提炼复现步骤和缺失信息。
- 需要决定 label、assignee、下一步维护动作。

## 不适用场景

- 用户已经要求直接修复某个明确 bug。
- issue 包含账号、token、隐私日志，且没有脱敏。
- 需要法律、医疗、金融等高风险判断。

## 工作流

1. 读取 issue 内容和相关上下文。
   - 标题、正文、评论、截图、日志、版本、环境、复现步骤。
   - 如有代码仓库，搜索相关模块和已有 issue。

2. 分类。
   - 类型：bug、feature、docs、question、duplicate、needs-repro、security。
   - 优先级：P0/P1/P2/P3，依据影响范围和是否阻塞。
   - 状态：ready、needs-info、needs-design、blocked、wontfix 候选。

3. 判断可执行性。
   - 是否有复现步骤。
   - 是否有期望行为和实际行为。
   - 是否能定位到模块或最近变更。

4. 输出维护动作。
   - 建议 labels。
   - 建议回复。
   - 建议下一步：复现、补测试、修复、关闭、拆分。

## 输出格式

```text
分类：bug / feature / docs / question / ...
优先级：P1，因为 ...
状态：needs-info / ready / duplicate / ...
建议 labels：...

判断依据：
- ...

建议回复：
...

下一步：
1. ...
2. ...
```

## 安全边界

- 遇到疑似安全漏洞时，不要要求用户公开更多敏感细节；建议转到私密渠道。
- 不要把用户日志里的 token、cookie、邮箱、手机号原样复述。
- 不要在缺乏复现依据时武断关闭 issue。

## 验证方式

- triage 结论必须能追溯到 issue 内容、日志、截图、代码或已有讨论。
- 如果缺少复现步骤，状态应标为 `needs-info`，不要假装已确认。
- 如果建议关闭 issue，说明关闭依据：重复、无法复现、超出范围或已有修复。
