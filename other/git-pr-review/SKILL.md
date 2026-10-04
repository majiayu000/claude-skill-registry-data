---
name: git-pr-review
description: 当用户明确要求审查 GitHub PR、评估是否合并或判断 PR 应如何处理时使用。对 PR 做只读、证据驱动的方案与风险评估，并给出合并建议。⚠️ 不适用：直接修改、合并 PR，或在本地执行不可信 PR 代码。
metadata:
  author: Bensz Conan
  short-description: 只读审查 GitHub Pull Request，并产出可决策的 Markdown 报告
  keywords:
    - git-pr-review
    - GitHub PR review
    - pull request review
    - PR 安全审查
    - merge decision
---

# Git PR Review

## 目标

当用户明确要求“review 某个 GitHub PR”“评估某个 pull request 是否值得 merge”“帮我判断这个 PR 怎么处理”时使用。基于用户提供的 GitHub 仓库地址、PR 编号/链接和补充说明，进行只读、证据驱动的 PR 审查：理解 PR 解决的问题、评估方案优劣与局限、默认优先使用内置“好 PR”标准并在必要时联网补充、识别恶意或高风险改动，并输出是否建议 merge 的 Markdown 决策报告。⚠️ 不适用：用户要你直接修改 PR 代码、直接 merge PR、或在本地执行 PR 分支中的不可信代码。

## 流程

### 输入

#### 你需要确认的输入

1. `github_repo`（必需）
   - GitHub 仓库根地址或 `owner/repo`，例如 `https://github.com/owner/repo`
   - 不接受 `issues/`、`pull/`、`tree/` 这类子页面 URL
2. `github_pr`（必需）
   - PR URL、`#123`、`123` 或 `pr-123`
3. `extra_instructions`（可选）
   - 用户已有判断、关注点、禁区、参考材料、团队背景
4. `review_count`（可选）
   - 独立评审次数，默认 5；用户明确指定时以用户要求为准
   - 当你调用 `build_parallel_review_plan.py` 时，把它映射为 `--n <review_count>`
5. `workspace_dir`（可选）
   - 默认 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/`
6. `report_dir`（可选）
   - 默认当前工作目录（项目根）

### 执行步骤

#### 核心原则

- **只读优先**：默认只能读取 GitHub 页面、API 返回、diff、评论、CI 状态、相关 issue/文档；不要修改源代码。
- **绝不主动 merge**：除非用户明确要求，否则不要执行 merge、rebase、squash、approve、request review 等操作。
- **绝不执行不可信 PR 代码**：不要 `gh pr checkout`、不要运行 PR 分支脚本、不要安装 PR 引入的依赖、不要触发可疑 CI/CD。
- **中间文件隔离**：所有中间文件必须保存在工作目录下的隐藏目录 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/`；若用户另有指定，才使用用户指定目录。
- **证据驱动**：所有结论都要回到证据，明确引用 diff、评论、CI、issue、社区资料或官方文档。
- **合规不忽略**：如果 PR 触及依赖、vendored 代码、复制粘贴第三方内容、资源资产或许可证文件，必须显式审查 license 风险与兼容性。

#### 标准工作流

##### 1. 初始化隔离工作区

优先使用确定性脚本创建本次评审目录与建议输出文件名：

```bash
python3 git-pr-review/scripts/prepare_review_job.py \
  --repo "https://github.com/owner/repo" \
  --pr "https://github.com/owner/repo/pull/123"
```

脚本会：
- 校验仓库地址与 PR URL 是否属于同一 GitHub 仓库
- 创建本次运行目录（默认 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/`）
- 生成 `manifest.json`
- 预创建最小占位文件：
  - `raw/README.md`
  - `notes/user_context.md`
  - `notes/community_good_pr.md`
  - `evidence/key_findings.md`
  - `evidence/missing_items.md`
- 输出建议的最终报告路径（默认项目根）

从这一步开始，所有抓取到的原始材料、分析笔记、临时摘要、命令输出都写入该工作区。

##### 2. 只读获取 PR 证据

优先选择**不会修改仓库状态**的方式读取 PR：

- GitHub 网页 / API / `.patch` / `.diff`
- `gh pr view`、`gh pr diff`、`gh api` 这类只读命令
- 仓库内公开 issue、discussion、相关文档、CI 状态页

建议至少保存下列材料到工作区：

- `raw/pr_meta.*`：标题、作者、状态、标签、基线分支、merge 状态、CI 状态
- `raw/pr_diff.*`：完整 diff 或 patch
- `raw/pr_comments.*`：review comments / discussion（如有）
- `raw/linked_issues.*`：关联 issue / discussion / docs（如有）
- `notes/user_context.md`：用户给的补充信息
- `notes/community_good_pr.md`：关于“好 PR”的社区标准摘记与链接
- `notes/license_review.md`：license / 合规审查笔记（如本次 PR 相关）
- `evidence/missing_items.md`：缺失材料、原因与影响

如果某项拿不到，要在工作区里记录“未获取原因”以及它对结论的影响，而不是静默跳过。

##### 3. 基于 parallel-vibe 做 N 次独立评审（默认 5 次）

目标：
- 使用 `parallel-vibe` 在多个独立 workspace 中做 **N 次彼此独立的 PR 审查**
- 默认 `N=5`
- 每个 thread 必须独立产出 `RESULT.md`
- 最后把多份 `RESULT.md` 聚合为一份统一摘要，再用于最终报告

推荐顺序：

```bash
python3 git-pr-review/scripts/build_parallel_review_plan.py \
  --manifest .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/manifest.json \
  --n 5
```

这里的 `--n` 是 helper script 参数；如果用户说“做 7 次独立评审”，等价于 `review_count=7`，最终在脚本层落成 `--n 7`。

该脚本会在本次 run 目录下生成：
- `parallel_review/input_snapshot/`：供每个 thread 复制的审查输入快照
- `parallel_review/parallel_plan.json`：`parallel-vibe` 的计划文件
- `parallel_review/parallel_review_job.json`：后续运行与聚合所需路径、已解析好的 `parallel-vibe` 脚本路径、固定的 `project_id` 与 `recommended_command`

重要说明：
- 优先直接执行 `parallel_review/parallel_review_job.json` 里的 `recommended_command`，避免手动拼路径或 `project_id`
- 如果 `raw/`、`notes/`、`evidence/` 有变化，必须重新运行 `build_parallel_review_plan.py`，让输入快照和 `project_id` 一起刷新

然后运行：

```bash
# 更推荐直接复制 `parallel_review_job.json` 里的 `recommended_command`
python3 ../parallel-vibe/scripts/parallel_vibe.py \
  --plan-file .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/parallel_review/parallel_plan.json \
  --src-dir .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/parallel_review/input_snapshot \
  --out-dir .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/parallel_review/parallel_runs \
  --project-id <parallel_review_job.json.project_id>
```

并行独立评审完成后，聚合结果：

```bash
python3 git-pr-review/scripts/aggregate_parallel_reviews.py \
  --job-file .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/parallel_review/parallel_review_job.json
```

如果 `parallel-vibe` 还没跑完、某个 thread 缺少 `RESULT.md`，或聚合输入不完整，聚合脚本应明确报错并停止，而不是静默生成误导性摘要。

聚合脚本会生成：
- `parallel_review/independent_review_summary.md`
- `parallel_review/independent_review_summary.json`

要求：
- 每个 thread 都要基于当前 workspace 中的材料独立审查，不看其他 thread 结果
- 每个 thread 的 `RESULT.md` 必须至少包含 recommendation / risk / evidence gaps
- 最终主报告必须明确综合独立评审的共识与分歧

##### 4. 理解这个 PR 在解决什么

至少回答清楚：

- PR 试图解决的核心问题是什么
- 这个问题是否真实存在，证据来自哪里
- PR 采用了什么方案
- 方案的主要优点、局限和潜在替代方案
- PR 是否与标题、描述、commit、测试、文档保持一致

如果 PR 描述模糊，必须从 diff、关联 issue、评论线程中补足上下文。

##### 5. 恶意 / 高风险 PR 审查

必须显式判断该 PR 是否存在恶意或高风险特征，并给出风险等级：
`Low` / `Medium` / `High` / `Critical`

重点检查：

- 是否存在数据窃取、凭证泄露、遥测偷报、后门逻辑
- 是否引入可疑下载、远程执行、shell 注入、SQL 注入、权限提升、破坏性删除
- 是否修改 CI/CD、部署脚本、权限配置、密钥读取路径、发布流程
- 是否引入难以解释的混淆代码、base64/hex 载荷、动态执行链
- 是否借“重构/清理”名义绕开测试、放宽校验、关闭安全保护
- 是否故意减少日志、删除告警、掩盖审计痕迹
- 是否存在明显不符合项目目标的改动范围漂移

只要怀疑恶意，就要把建议提升为：
- `不要 merge`
- `建议人工安全复核 / 维护者升级处理`

##### 6. License / 合规审查

这是强制步骤之一。即使用户没有主动提到 license，只要 PR 涉及下列内容，就必须显式检查：

- 新依赖、依赖升级、包管理器锁文件
- vendored 代码、复制的第三方脚本/模板/字体/图标/数据
- `LICENSE` / `NOTICE` / copyright header
- 模型权重、数据集、示例代码、前端资源

至少回答清楚：

- PR 是否引入了新的 license 风险或兼容性风险
- 是否存在互相冲突的 license / header / 声明
- 是否需要更新 `LICENSE`、`NOTICE`、README、第三方声明文档
- 该风险是否需要法务/维护者额外确认

对于 license 不明确、明显冲突、或可能触发 GPL/AGPL/SSPL 等传播义务的情况：
- 不能直接给出乐观 merge 建议
- 应提升为 `Request changes`、`Do not merge` 或至少 `Escalate security review` / 合规复核

参考：`references/license-checklist.md`

##### 7. 使用内置“好 PR”标准（默认不实时联网）

这里的默认做法**不是每次执行都实时联网**。

本 skill 已经把“什么是好 PR”的基础标准沉淀到：
- `references/good-pr-standards.md`

并且在初始化工作区时，会自动把该参考摘要写入：
- `notes/community_good_pr.md`

默认执行时：
- 优先使用 `notes/community_good_pr.md` 里的内置标准
- 结合当前 PR 做对照分析
- 在最终报告中明确写出“哪些维度符合 / 不符合”

只有在以下情况才需要再联网补充：
- 用户**明确要求**查看最新社区口径
- 用户指定某个特定社区 / 组织 / 仓库的 PR 规范
- 当前内置标准不足以覆盖该 PR 的特殊场景

即使需要补充联网，也应把新增来源继续沉淀到本次 run 的 `notes/community_good_pr.md`，而不是只在脑中使用。

不是机械照抄“最佳实践”，而是要回答：
- 这个 PR 在哪些维度上符合好 PR 的定义
- 哪些维度不符合
- 不符合之处是“小瑕疵”还是“阻断 merge 的问题”

##### 8. 输出决策报告

将最终结论写成 Markdown，默认放在项目根目录，文件名格式：

`Git-PR-Review_{repo_slug}_{pr_slug}_{timestamp}.md`

例如：

`Git-PR-Review_openai_openai-python_pr-2451_20260324153022.md`

报告必须包含以下章节：

- `## 结论摘要`
- `## 独立评审综合结果`
- `## PR 在解决什么问题`
- `## 方案分析`
- `## 恶意/安全风险审查`
- `## License / 合规审查`
- `## 与“好 PR”社区标准的对照`
- `## 关键证据`
- `## 证据不足与待确认点`
- `## 建议的处理方式`

完整模板不要直接内嵌在 `SKILL.md`，而是统一引用：
- `references/report-template.md`

写最终报告时，必须综合：
- 原始证据（`raw/`、`notes/`、`evidence/`）
- `parallel_review/independent_review_summary.md`
- 如有必要，`parallel_review/parallel_runs/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/parallel-vibe/<project_id>/@main/summary.md`

##### 9. 完成前自检

在交付前运行校验脚本，确认：
- 工作区结构完整
- 默认模式下工作区仍位于隐藏目录
- 最终报告文件名合规
- 最终报告包含配置要求的所有必需章节
- 没有把中间产物散落到工作区外

```bash
python3 git-pr-review/scripts/validate_review_artifacts.py \
  --manifest .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/{yyyy-mm-dd-hh-mm}/manifest.json \
  --report /abs/path/to/Git-PR-Review_<...>.md
```

#### 可读参考

- `references/report-template.md`：最终报告模板
- `references/security-checklist.md`：恶意/高风险 PR 审查清单
- `references/license-checklist.md`：license / 合规审查清单
- `references/community-research-playbook.md`：如何搜索“好 PR”社区标准
- `references/parallel-review-result-template.md`：独立评审 thread 的 `RESULT.md` 结构
- `references/parallel-vibe-integration.md`：`parallel-vibe` 集成方式与关键产物

### 输出

#### 输出要求

- 最终交付物：1 份 Markdown 报告
- 报告用语要明确，不要模棱两可
- 结论必须给出处理建议，不要只给“分析但不表态”
- 如果证据不足，要明确说明不足项，以及这如何影响你的建议

### 输出管理

#### BenszAPI 任务工作区


### 校验

交付前运行 `validate_review_artifacts.py`，确认 manifest、原始证据、独立评审汇总和最终报告齐全，报告包含配置要求的全部章节、建议明确且所有结论可回到证据；核对工作区仍在 `.bensz-api` 隐藏目录且未执行 PR 代码或远程写操作。

### 失败与恢复

仓库/PR 证据获取失败、并行 thread 缺少 `RESULT.md`、聚合输入不完整或报告校验失败时，保留已获取材料与错误摘要，停止生成乐观结论并明确证据缺口；不得通过 checkout、运行不可信代码或修改远程状态来绕过阻塞。


## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->

### Skill 专属约束

#### 明确禁止事项

- 不要修改目标仓库代码
- 不要 merge PR
- 不要 approve PR
- 不要 checkout PR 分支并执行代码
- 不要把 API token、cookie、认证信息写入工作区
- 不要把中间文件写到 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/git-pr-review/` 之外（除最终 Markdown 报告）
