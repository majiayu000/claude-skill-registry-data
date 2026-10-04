---
name: mr
description: Opens the merge request for the current branch, assembling the six-section description from repo artifacts and refusing to invent the Why. Use when a branch is ready for review, when the user says /mr, or when asked to create, open or update a merge request.
---

# /mr —— 开 MR

`/rv` 之后、`/fb` 之前的那一步。**只开 MR，永不合并。**

## 前置（不满足就停下来说，不要绕过）

- `/rv local` 跑过且已处理完 findings
- `AGENTS.md`「合并前本地验证」表里的三条命令本地全绿 —— 没跑就先跑
- 工作区干净，已 `git fetch origin && git pull --rebase origin <主干>`
- 分支名带工作项号（`feat/PROJ-1234-order-state`）；不带 → 先 `git branch -m`

## Step 1 · 从仓库产物汇总，不要从 diff 编

| 段 | 原料 |
|---|---|
| What | `SPEC.md` 的目标一句话 + Meegle 工作项号与链接 |
| Why | **只能来自 `docs/intent/<主题>.md` / `tasks/plan.md#方案选型`** |
| How | `tasks/plan.md` 的阶段 + `git log --oneline <base>..HEAD` |
| Scope | `git diff --stat <base>..HEAD`，逐条回答 Scope 段的三个勾选 |
| Tests | `/t` 的结论：新增用例覆盖哪几条验收、回归跑了多少、手工验证做了什么 |

```bash
BASE=$(git merge-base origin/${TARGET:-main} HEAD)
git log --oneline "$BASE"..HEAD; git diff --stat "$BASE"..HEAD
```

**Why 找不到出处 → 报缺口并停下。** 让用户补 `docs/intent/`，补完重跑。没有例外。
从 diff 反推的理由看起来像结论，实际没有任何决策发生过 —— 这是这个 skill 唯一会拒绝执行的地方。

## Step 2 · 按模板写，别新造格式

用仓库里的 `docs/templates/merge-request.md` 六段：What / Why / How / Scope / Tests / 注意点。
写进临时文件（`/tmp/mr-body.md`），**不要**把描述塞进命令行字符串。

## Step 3 · 自检

```bash
CI_MERGE_REQUEST_TITLE="<标题>" CI_MERGE_REQUEST_DESCRIPTION="$(cat /tmp/mr-body.md)" \
  sh .gitlab/mr-contract-check.sh   # 仓库里有才跑；没有就人工对一遍六段
```

不过就改描述，不是改脚本。

## Step 4 · 开

```bash
git push -u origin HEAD
glab mr create --title "feat(order): 对账逻辑 [PROJ-1234]" \
  --description "$(cat /tmp/mr-body.md)" \
  --target-branch main --assignee @me \
  --squash-before-merge --remove-source-branch --yes
```

- 分支上已有 open MR（`glab mr list --source-branch $(git branch --show-current)`）→
  改用 `glab mr update <id> --title "<标题>" --description "$(cat /tmp/mr-body.md)"` ——
  标题一并同步，自检校的就是它。不要开第二个 MR。
- 还没写完想先要反馈 → 加 `--draft`。
- 属于「必须人审」类别（schema 迁移、认证/权限、公开接口、删代码、不可逆操作）→
  在描述「注意点」里点名，并 `--reviewer <人>`。

## Step 5 · 挂回工作项

把 MR 链接贴到 Meegle 工作项（装了 CLI 就自己贴，没装就把链接给用户）。
**状态回写在合入后做，不在这里。**

## 输出

MR 链接 + 标题 + `glab ci status` 的结果 + 还缺什么（比如 Why 出处、待人审的类别）。
CI 绿了就报「ready to merge」并停 —— 合并是人的显式决定。

## Red Flags

- Why 段写「因为需求要求」「为了提升体验」—— 等于没写
- 六段里有一段是 `TBD` / `待补` 就推上去
- 本地没跑验证，指望 CI 告诉你能不能过（同一分支第三次 push「看看线上行不行」= 停）
- 一个分支开了两个 MR，或一个 MR 塞了两个工作项
- 开完顺手 `glab mr merge`
