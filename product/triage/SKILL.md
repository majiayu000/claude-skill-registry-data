---
name: github-issue-triage
description: 当用户要拉取并分析 GitHub 仓库的 open issues、给所有 issue 排优先级、产出 triage 报告,或要定期(配合 /schedule)巡检新 issue 时使用。按「数据正确性/崩溃 > 高价值&高呼声 > 体验 > 长尾」四级分流,结合社区呼声(👍/💬)与产品核心卖点相关度,可选结合代码库验证 bug 真实性,输出可维护的 `.docs/issue-triage.md`。触发关键词:"分析 github issue"、"issue 优先级 / triage"、"梳理 issues 排优先级"、"看下还有哪些有价值的需求或急需修的 bug"、"定期拉取 issue 分析"、"triage open issues"、"backlog 排序"。不适用于:单个 issue 的具体修复(直接修即可)、PR review、issue 的回复/关闭操作。
---

# GitHub Issue Triage 技能

## 做什么

把一个 GitHub repo 的**全部 open issue** 拉下来,按统一维度分级排序,产出一份可维护的优先级文档(`.docs/issue-triage.md`),并可配合 `/schedule` 定期增量更新。目标:把"几十个 issue 的噪声"压成"先做哪几个"的清晰判断。

**核心信念**:triage 是只读的决策支持,不是替用户做决定 —— 产出文档,排好序,讲清理由,把"做不做、先做谁"留给人。

## 何时触发

- 用户问"还有哪些有价值的需求 / 急需修的 bug"
- 要给 backlog 排优先级 / 出 roadmap
- 要定期(周/双周)自动巡检新 issue

## 流程

### 1. 拉取(注意网络兜底)

`gh` 已认证即可。**坑**:某些网络环境(如公司 Zscaler 代理)下 `gh` 走 HTTPS GraphQL API 会 TLS 握手超时;失败就 unset 代理重试(git push 走 SSH 不受影响,只有 gh API 需要):

```bash
env -u HTTPS_PROXY -u HTTP_PROXY -u https_proxy -u http_proxy -u ALL_PROXY -u all_proxy \
gh issue list --repo OWNER/REPO --state open --limit 100 \
  --json number,title,labels,body,comments,reactionGroups,createdAt
```

repo 从用户给的、或当前目录 `git remote` 推断。

### 2. 读呼声信号

- 👍 = `reactionGroups` 里 `THUMBS_UP` 的 `users.totalCount`
- 💬 = `comments` 数组长度
- **先扫一眼这个 repo 用哪个信号为主**:很多 repo 用户根本不点 👍(全 0),呼声只能看评论数。别只按 👍 排序得出"全都不重要"的错误结论。

用 jq 一把梭出按呼声排序的总览:
```bash
... gh issue list ... --json number,title,labels,comments,reactionGroups \
| jq -r 'map({n:.number, up:([.reactionGroups[]?|select(.content=="THUMBS_UP")|.users.totalCount]|add // 0), c:(.comments|length), l:(.labels|map(.name)|join(",")), t:.title}) | sort_by(-.up,-.c) | .[] | "#\(.n)\t👍\(.up)\t💬\(.c)\t[\(.l)]\t\(.t)"'
```

### 3. 四级分流(核心维度)

| 级 | 判据 |
|---|---|
| 🔴 **P0** | 数据正确性错误 / 崩溃卡死 / 核心功能首用即失效。**最优先:用户数据被悄悄记错那种**(总额对、方向/归类错,用户自己发现不了) |
| 🟡 **P1** | 高呼声需求、明显性能问题、与产品核心卖点强相关的体验缺陷 |
| 🟢 **P2** | 局部体验改善、有用但非紧急的功能 |
| ⚪ **P3** | 锦上添花、长尾、小众、含义模糊待澄清 |

排序权重:**数据正确性/崩溃 > 呼声 > 与核心卖点相关度**。一个安静(0💬)但会记错账的 bug,排在热闹(5💬)的外观需求前面。

### 4.(深入时)用代码验证 bug

对 P0/P1 的 bug,别只信描述 —— 在 codebase 里定位相关代码,确认 bug 真实存在、找到根因行号。把"疑似 bug"升级成"已定位、可修",triage 的含金量主要来自这一步。能顺手判断工作量(S <1天 / M 1–3天 / L >3天建议拆)。

### 5. 主题聚类(epic 视角)

把同主题的 issue 归成 epic(例:「自动记账可靠性」「平账/余额修正」「特殊交易类型(退款/报销/红包)」「CSV 导入」)。**很多 issue 一次设计能解决一串** —— 这个视角往往比逐条排序更有决策价值。

### 6. 产出文档

写 / 更新 `.docs/issue-triage.md`:

```
# <Repo> Issue 优先级 Triage
> 生成于 <日期> · 共 N 个 open issue
> 排序依据 + 呼声说明 + 工作量图例
## 🔴 P0 …  (表格:# / 标题 / 一句判断 / 呼声 / 工作量)
## 🟡 P1 …
## 🟢 P2 …
## ⚪ P3 …
## 🧩 主题聚类(epic)
## 🗺️ 推荐 Roadmap(分波次:先数据正确性+核心功能,再高呼声功能,再体验打磨)
```

仅凭标题初判的标「*待细看*」,提示动手前需读 body / 代码。

## 定期运行(配合 /schedule)

让用户用 `/schedule` 起一个 cron(如每周一 09:00),prompt 引用本技能。增量模式:

1. 读 `.docs/issue-triage.md` 顶部的上次生成日期
2. `gh issue list --search "created:>YYYY-MM-DD"` 只拉新增 issue,归入已有分级
3. 有新 P0 时在摘要里**显著提示**,别埋在文档里

## 红线

- **只读**:不自动关闭 / 不自动评论 / 不改 issue 状态或 label —— 一切供人决策
- **不臆断价值**:含义模糊的 issue 标「待澄清」,不强行归级、不编造重要性
- **诚实呼声**:👍/💬 如实呈现,不夸大;repo 没人互动就说明"呼声数据弱,主要靠内容判断"
