---
name: version-close
description: "版本收尾:门禁复核→生成审计对局→派 engine-auditor 无上下文审核→分诊→写 docs/changelog/vX.Y.md→打 tag 并 push。一个版本的所有 phase 实现完且 /validate 通过后触发。"
argument-hint: "[版本号,如 v1.0]"
disable-model-invocation: true
allowed-tools: Read, Write, Glob, Grep, Task, Bash
---

# 版本收尾

版本:$ARGUMENTS(留空则从最近 commit message 的 vX.Y 前缀推断,并向用户确认;
用户离线时直接采用推断值并记入 docs/DECISIONS.md)

> `allowed-tools` 给了完整 Bash,因为要跑测试和对局脚本;它是「本轮免批准范围」,
> 不构成硬限制。收尾纪律的定义端在 `.claude/rules/versioning.md`,本 skill 是执行壳。

## 第 0 步 前置检查(不满足就停,不要硬闭环)

- `/validate` 已跑过且「必须修」清零——没跑就先去跑,本 skill 不替代它。
- `git status --short` 干净(所有 phase 已按 `vX.Y <功能>` 规范 commit)。脏 → 先提交再回来。

## 第 1 步 门禁复核

跑 `pytest -x -q` 和 `ruff check src/ tests/`,**贴真实输出**。任一不绿 → 停,报告,不进下一步。
(Stop hook 的 verify.sh 也会拦,但收尾必须留下一份显式的全绿证据,不靠「没被拦=绿」。)

## 第 2 步 生成审计对局

用受版本控制的脚本跑一场(或多场)覆盖本版本功能的脚本化对局,产物落
`experiments/<YYYYMMDD>-vX.Y-audit/`,按 rules/experiments.md 落齐六项
(git hash / resolved config / seed / 启动命令 / 日志 / 机器可读 metrics)。
**必须是收尾时新跑的**——旧日志审不出新 commit 的问题。
对局脚本本身若还没有,这是本版本 plan 的遗漏:补一个最小脚本再继续。

## 第 3 步 派 engine-auditor(无上下文审核)

派 `engine-auditor` subagent,prompt **必须带三样**:
1. issue.md 中 vX.Y 规格段的行号范围
2. src/ 的审计范围(本版本动过的模块为主,可给 `git diff --stat <上个tag>..HEAD` 的文件清单)
3. 第 2 步的 run 目录路径

不要附加任何「实现时我们决定…」的背景——**无上下文是它的价值,不是缺陷**。

## 第 4 步 分诊(逐条处理,不要只转述)

- **P0**:必须修。小改直接修并按规范 commit;伤筋动骨走 /plan。修完**重跑第 1–3 步**
  (审核对象变了,旧审核作废)。
- **P1**:用户在线则列给用户裁决(改实现还是改 issue 规格);离线则按最合理解释处理
  并逐条记入 docs/DECISIONS.md 供醒后复核。
- **P2**:原样搬进 changelog 的「已知问题」。

## 第 5 步 写 changelog

写 `docs/changelog/vX.Y.md`,**格式逐字照抄 `.claude/rules/versioning.md` 的契约**,
不做等价改写。素材:`git log --oneline <上个tag>..HEAD` 的 vX.Y commit(新增/修复)、
本版本数值改动(平衡,带 [source: run_id])、第 4 步的 P2(已知问题)。

## 第 6 步 tag 与收尾输出

1. 五件套核对清单(versioning.md 的版本完成定义),逐项 ✅/❌;有 ❌ 不许进下一步。
2. 执行 `git tag -a vX.Y -m "<changelog 的一句话主题>"` 并 `git push --tags`
   (用户已授权;这偏离通用模板默认,依据记录在 docs/DECISIONS.md)。
3. 跑 /handoff,把版本收尾状态落盘并 commit。

## 硬约束

- 不跳过第 2 步直接派审核(没有新鲜对局日志的审核只剩静态读码,漏掉整个动态不变量层)。
- P0 未清零不写 changelog、不打 tag。
- 规格歧义的最终解释权在用户;本 skill 对 issue.md 的修改仅限「吃透后的通透化改写」
  纪律(见 versioning.md),不得夹带规格变更。
