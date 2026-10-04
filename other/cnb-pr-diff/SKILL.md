---
name: cnb-pr-diff
description: 获取 PR 的 diff 变更信息。
---

# 获取 PR Diff

获取 PR 的代码变更差异信息，用于代码评审、变更总结等场景。

## 1. 判断场景并获取 SHA

### 场景 A：PR 评论触发（`CNB_PULL_REQUEST_IID` 存在）

直接从环境变量获取：
- head SHA：`CNB_PULL_REQUEST_SHA`
- target SHA：`CNB_PULL_REQUEST_TARGET_SHA`

若环境变量不存在，通过 API 查询当前 PR 详情。

### 场景 B：Issue 或其他场景引用 PR

用户输入中提及了 PR 编号（如 `!45`），需要：
1. 从用户输入中解析 PR 编号
2. 通过 API 查询该 PR 详情获取 SHA
3. fetch 对应的 commit（本地可能没有）

### API 查询 PR 详情

```bash
# 将 ${pr_iid} 替换为实际 PR 编号
pr_info=$(curl -s \
  "${CNB_API_ENDPOINT:-https://api.cnb.cool}/${CNB_REPO_SLUG}/-/pulls/${pr_iid}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN")

head_sha=$(echo "$pr_info" | jq -r '.head.sha')
target_sha=$(echo "$pr_info" | jq -r '.base.sha')

# 场景 B 需要确保本地有这些 commit
git fetch origin "$head_sha" "$target_sha" 2>/dev/null || git fetch origin
```

## 2. 获取 Diff

### 获取变更文件列表

```bash
git diff --name-only "${target_sha}...${head_sha}"
```

### 获取变更统计

```bash
git diff --stat "${target_sha}...${head_sha}"
```

### 获取完整 Diff

```bash
git diff -U5 "${target_sha}...${head_sha}"
```

### 获取特定文件的 Diff

```bash
git diff -U5 "${target_sha}...${head_sha}" -- path/to/file.ts
```

## 3. 过滤文件

根据使用场景，可排除无需关注的文件：

```bash
# 常见排除模式
git diff -U5 "${target_sha}...${head_sha}" -- . \
  ':!package-lock.json' ':!yarn.lock' ':!pnpm-lock.yaml' ':!go.sum' ':!*.lock' \
  ':!*.png' ':!*.jpg' ':!*.gif' ':!*.svg' ':!*.ico' \
  ':!*.min.js' ':!*.min.css' ':!*.map' \
  ':!dist/*' ':!build/*' ':!node_modules/*'
```

**可排除的文件类型**：
- 锁文件：`package-lock.json`、`yarn.lock`、`pnpm-lock.yaml`、`go.sum`、`Cargo.lock`
- 图片/字体：`*.png`、`*.jpg`、`*.gif`、`*.svg`、`*.woff`、`*.ttf`
- 二进制：`*.exe`、`*.dll`、`*.so`、`*.jar`、`*.pyc`
- 压缩包：`*.zip`、`*.tar.gz`、`*.rar`
- 构建产物：`dist/`、`build/`、`out/`、`target/`、`.next/`
- 依赖目录：`node_modules/`、`vendor/`、`.venv/`
- 压缩文件：`*.min.js`、`*.min.css`、`*.map`

## 4. 使用建议

1. **diff 过大时**：先用 `--name-only` 查看文件列表，再按需获取具体文件
2. **代码评审**：建议排除锁文件、图片、构建产物
3. **变更总结**：可保留更多文件，但排除二进制和依赖目录
4. **上下文行数**：`-U5` 提供 5 行上下文，可按需调整
