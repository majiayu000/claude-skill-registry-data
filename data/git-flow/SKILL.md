---
name: git-flow
description: 当用户用自然语言请求提交代码时触发（如「帮我提交」「commit 一下」「提交代码」）。自动应用 Git 提交规范，从分支名提取任务 ID，生成符合规范的提交信息。
---

# Git 提交辅助

当用户用自然语言请求提交代码时，自动应用此 skill。

## 触发场景

用户消息包含以下关键词时触发：
- 「帮我提交」「提交一下」「提交代码」
- 「commit」「commit 一下」
- 「推送」「push」
- 「创建 MR」「创建合并请求」

## 执行流程

### 1. 检查分支

**检测仓库默认分支（三级检测 + 用户确认）：**

详细步骤参见：[reference.md](./reference.md#检测默认分支三级检测--用户确认)

**简要说明：**
1. 首先尝试：`git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`
2. 如失败，依次检查 main/master/develop 分支是否存在
3. 如仍失败，使用 `AskUserQuestion` 询问用户选择基准分支

**获取当前分支：**
```bash
git branch --show-current
```

**如果当前在默认分支（main/master/develop 等）：**
- 检查用户消息是否包含任务 ID（TAP-xxx）或飞书链接
- 如果有：询问分支描述，创建工作分支
  ```bash
  # 获取远程最新代码
  git fetch origin
  
  # 基于远程默认分支创建新分支
  new_branch="feat/TAP-xxxxx-description"
  if ! git checkout -b "$new_branch" "origin/$default_branch"; then
    echo "❌ 创建分支失败"
    echo "💡 请先处理本地修改：git stash 或 git commit"
    exit 1
  fi
  ```
- 如果没有：提示用户需要提供任务工单链接或 ID

### 2. 分析变更

```bash
git status
git diff HEAD --stat
git diff --cached
```

### 3. 提取任务 ID

详细步骤参见：[reference.md](./reference.md#任务ID提取)

**概要：** 按优先级从分支名、用户输入、用户询问中获取任务 ID
（若需使用 `no-ticket`，必须先与用户确认是否为纯文档/配置等非功能性变更；否则要求用户提供/创建工单 ID）

### 4. 生成提交信息

详细规范参见：[reference.md](./reference.md#commit信息生成规范)

**格式：** `type(scope): 中文描述 #TASK-ID`

**Type 和 Description 规范：** 详细参见 [reference.md](./reference.md#提交信息规范)

### 5. 执行提交

```bash
git add <files>  # 排除 .env、credentials 等敏感文件
git commit -m "type(scope): 中文描述 #TASK-ID"
```

### 6. 可选：推送并创建 MR

如果用户请求推送或创建 MR：

**策略（与 `/git:commit-push-pr` 保持一致）：glab 优先，失败则 fallback 到 push options**

1. **检测 glab 是否可用**：
```bash
which glab && glab auth status
```

**安全限制（严格禁止）：**
- `glab mr approve` - 禁止自动审批
- `glab mr merge` - 禁止自动合并

2. **准备 MR 标题和描述（模板优先）**：
- **MR Title**：优先使用最新 commit 标题（`git log -1 --pretty=%s`）
- **MR Description**：从 commit message 汇总生成（与 command 一致），并按以下规则填充 MR 模板：
  - 优先模板：`.gitlab/merge_request_templates/default.md`
  - 兼容模板：`.gitlab/merge_request_templates/Default.md`
  - 填充规则：替换模板中 `## Description` 与下一个 `## ` 标题之间的内容；若模板没有 `## Description`，则在顶部插入

3. **推送并创建 MR**：

**如果 glab 可用：**
```bash
# 推送分支
git push -u origin $(git branch --show-current)

# 生成 MR_DESC（模板优先；无模板则直接用汇总正文），然后创建 MR
TEMPLATE_FILE=""
if [ -f ".gitlab/merge_request_templates/default.md" ]; then
  TEMPLATE_FILE=".gitlab/merge_request_templates/default.md"
elif [ -f ".gitlab/merge_request_templates/Default.md" ]; then
  TEMPLATE_FILE=".gitlab/merge_request_templates/Default.md"
fi

COMMIT_SUMMARY="$(cat <<'EOF'
## 改动内容
- [汇总所有 commit 的改动点]

## 影响面
- [汇总所有 commit 的影响面]
EOF
)"

if [ -n "$TEMPLATE_FILE" ]; then
  MR_DESC="$(TEMPLATE_FILE="$TEMPLATE_FILE" COMMIT_SUMMARY="$COMMIT_SUMMARY" python3 - <<'PY'
import os
import re

template_path = os.environ["TEMPLATE_FILE"]
summary = os.environ["COMMIT_SUMMARY"].rstrip("\n")

with open(template_path, "r", encoding="utf-8") as f:
  template = f.read()

header_re = re.compile(r"(?m)^## Description\\s*$")
m = header_re.search(template)

block = f"\\n\\n{summary}\\n\\n"

if not m:
  out = f"## Description{block}" + template.lstrip(\"\\n\")
else:
  start = m.end()
  rest = template[start:]
  m2 = re.search(r"(?m)^##\\s+.+$", rest)
  end = start + (m2.start() if m2 else len(rest))
  out = template[:start] + block + template[end:]

print(out, end=\"\")
PY
  )"
else
  MR_DESC="$COMMIT_SUMMARY"
fi

glab mr create \
  --title "$(git log -1 --pretty=%s)" \
  --description "$MR_DESC" \
  --yes --remove-source-branch
```

**如果 glab 不可用（fallback）：**
- 先确保你已经通过步骤 1 的默认分支检测拿到了 `default_branch`
```bash
git push -u origin $(git branch --show-current) -o merge_request.create -o merge_request.target=$default_branch
```

4. **输出结果**：显示 MR 链接，并使用系统默认浏览器打开（如果可获取到链接）。

## 与 Commands 的关系

- `/git:commit`：用户显式调用命令（仅提交）
- `/git:commit-push`：用户显式调用命令（提交并推送）
- `/git:commit-push-pr`：用户显式调用命令（提交、推送并创建 MR）
- **此 Skill**：用户用自然语言描述，Claude 自动应用规范

详细规范参见：[reference.md](reference.md)
