---
name: cnb-code-review
description: PR 代码评审，检查安全漏洞、Bug 和代码质量。
---

# PR 代码评审

对 PR 的代码变更进行专业评审，发现安全漏洞、Bug、代码质量和性能问题，并通过 PR Review API 发送行级评论。

## 评审步骤

### 1. 获取 PR 变更

使用 cnb-pr-diff Skill 获取 PR 的代码变更。

**需过滤的非代码文件**（不评审）：
- 依赖锁文件：`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `go.sum`, `Cargo.lock` 等
- 图片文件：`*.png`, `*.jpg`, `*.gif`, `*.svg`, `*.ico` 等
- 字体文件：`*.woff`, `*.ttf`, `*.eot` 等
- 二进制文件：`*.exe`, `*.dll`, `*.so`, `*.jar`, `*.pyc` 等
- 压缩文件：`*.zip`, `*.tar.gz`, `*.rar` 等
- 压缩的代码：`*.min.js`, `*.min.css`, `*.map`
- 构建产物目录：`dist/`, `build/`, `out/`, `target/`, `.next/`
- 依赖目录：`node_modules/`, `vendor/`, `.venv/`

**文件限制**：
- 最多评审 30 个文件
- diff 最大 100000 字符（超出则截断）

### 2. 分析代码

**评审重点**（按优先级）：

1. **安全漏洞**：SQL 注入、XSS、CSRF、硬编码凭证、敏感信息泄露、不安全加密
2. **潜在 Bug**：空指针、数组越界、并发问题、资源泄漏、异常处理不当
3. **代码质量**：可读性、命名规范、代码重复
4. **性能问题**：N+1 查询、低效算法、不必要的 I/O

**评审原则**：
- 只评审新增代码（diff 中 `+` 开头的行，不含 `+++` 文件头）
- **禁止评审**：删除的代码（`-` 开头）、上下文代码、未修改的代码
- **忽略**：EOF 换行符、行尾空格、缩进风格（应由 linter 处理）

**理解上下文**：
当 diff 上下文不足以理解代码时（如需要看函数定义、类型、依赖关系），使用 Read 工具读取相关源文件理解上下文，并确认准确行号。

### 3. 输出评审结果

**必须严格输出以下 JSON 格式**：

```json
{
  "status": "passed | needs_modification | critical",
  "issues": [
    {
      "severity": "critical | warning | info",
      "file": "文件路径",
      "start_line": 起始行号,
      "end_line": 结束行号,
      "problem": "问题：描述问题",
      "suggestion": "建议：修复建议"
    }
  ]
}
```

**字段说明**：
- `status`: 评审状态
  - `passed`: 通过，无问题
  - `needs_modification`: 需要修改
  - `critical`: 存在严重问题
- `severity`: 问题严重程度
  - `critical`: 严重（安全漏洞、崩溃 Bug）
  - `warning`: 警告（潜在问题）
  - `info`: 建议（代码质量改进）
- `start_line` / `end_line`: 问题代码的行号范围（对应新文件行号）
- `problem` / `suggestion`: 使用 Markdown 格式，提高可读性
  - 使用 \`代码\` 标记变量名、函数名
  - 使用代码块展示修复示例

**无问题时**：`issues` 为空数组 `[]`

### 4. 发送评审评论

**重要**：API 基础地址从环境变量 `CNB_API_ENDPOINT` 获取（默认 `https://api.cnb.cool`），仓库名从环境变量 `CNB_REPO_SLUG` 获取，PR 编号从环境变量 `CNB_PULL_REQUEST_IID` 获取。

**有问题时**：调用 PostPullReview 接口发送行级评审评论：

```bash
curl -X POST \
  "${CNB_API_ENDPOINT:-https://api.cnb.cool}/${CNB_REPO_SLUG}/-/pulls/${CNB_PULL_REQUEST_IID}/reviews" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "body": "**评审结果**: 需要修改",
  "event": "comment",
  "comments": [
    {
      "body": "问题: ...\n建议: ...",
      "path": "文件路径",
      "start_line": 起始行号,
      "start_side": "right",
      "end_line": 结束行号,
      "end_side": "right",
      "subject_type": "line"
    }
  ]
}'
```

**无问题时**：调用 PostPullComment 接口发送总结评论：

```bash
curl -X POST \
  "${CNB_API_ENDPOINT:-https://api.cnb.cool}/${CNB_REPO_SLUG}/-/pulls/${CNB_PULL_REQUEST_IID}/comments" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "body": "**评审结果**: 通过\n\n代码质量良好，未发现明显问题。"
}'
```

## 注意事项

1. **最多发送 10 条评论**，优先发送严重程度高的问题（critical > warning > info）
2. 行号必须对应 diff 中的**新文件行号**（右侧行号），务必通过读取源文件确认
3. 每条评论需说明问题原因和修复建议
4. 评审结果必须是有效 JSON
