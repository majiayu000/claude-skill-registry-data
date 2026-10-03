---
name: audit-remote-secret-leaks
description: "Use when a git project may have leaked private information, credentials, tokens, keys, passwords, PII, internal URLs, or secrets into pushed remote branch or tag history, or when local staged, unstaged, untracked, ignored, stashed, or local-only commits need leak risk review before push. Do not use for: actually pushing commits (use push-remote), producing release readiness or rollback plans (use release-readiness), or general code quality review (use code-review-deep-zh)."
---

# 远程敏感信息泄露审计 (audit-remote-secret-leaks)

面向**项目/仓库级**敏感信息泄露排查。核心目标是判断已经推送到远程仓库的 git 历史中是否包含隐私或敏感信息，同时统计尚未推送到远程的风险内容，并产出带证据、影响范围和通用修复方案的报告。

## 核心原则

- **远程优先**：先审计 `refs/remotes/*` 指向的已推送历史，再看本地未推送内容。
- **只读审计**：审计阶段只收集证据和统计，不删除文件、不改写历史、不强推。
- **证据脱敏**：报告中不得完整展示密钥、密码、Token、私钥、Cookie、个人身份信息等敏感值。
- **范围透明**：清楚标注审计了哪些远程、分支、提交范围、工作区状态和扫描方法。
- **修复先轮换**：一旦敏感值已推送远程，删除提交不等于安全；先建议撤销/轮换凭据，再考虑历史清理。
- **Do not validate live secrets**：不要主动调用外部服务验证真实凭据是否有效，除非用户明确要求并确认风险。
- **sanitized scanner output**：扫描器原始输出可能包含完整敏感值；报告只能引用脱敏后的摘要和证据。

## 使用边界

使用本 skill：

- 用户要求检查项目是否把隐私、密钥、Token、密码、私钥、证书、个人身份信息或内部地址提交到远程仓库。
- 用户要求审计 git history、remote repository、pushed commits、远程历史、已推送提交中的敏感信息泄露。
- 用户还希望同时查看未提交、已暂存、未暂存、未跟踪、本地领先远程的内容是否存在泄露风险。

不要使用本 skill：

- 只做普通代码质量审查或安全代码审查，改用 `code-review-deep-zh`。
- 只读懂项目结构，改用 `code-read-deep-project`。
- 用户要求立即删除提交、改写历史或强推；本 skill 可给方案，但执行前必须单独确认。

## 前置确认

1. 确认当前目录是 git 仓库根或能定位到仓库根。
2. 确认是否存在远程仓库：`git remote -v`。
3. 说明默认审计范围：
   - 远程历史：所有 `refs/remotes/*`，以及已获取的 `refs/tags/*`。
   - 未推送内容：工作区、暂存区、未跟踪文件、ignored 文件、stash、本地领先上游的提交。
4. 如果用户指定远程、分支、路径、时间段或提交范围，以用户指定为准并在报告中记录。
5. 如果需要联网刷新远程引用，运行 `git fetch --all --prune` 前按当前环境权限处理；无法刷新时继续审计本地已有远程跟踪引用，并在报告中标注。

## 审计流程

按顺序执行，不要跳阶段。

### 阶段 1：仓库和远程范围确认

收集基础信息：

- `git rev-parse --show-toplevel`
- `git status --short --branch`
- `git remote -v`
- `git branch -vv`
- `git for-each-ref refs/remotes refs/tags --format="%(refname:short) %(objectname:short) %(committerdate:iso8601)"`
- `git tag -l`
- `git lfs ls-files`（如果安装了 Git LFS）
- `git submodule status --recursive`（如果存在 `.gitmodules`）

报告中记录：

- 仓库根目录。
- 远程名称和 URL（可对私有 URL 做脱敏）。
- 当前分支、上游分支、默认远程 HEAD。
- Remote tag scope：本次纳入审计的 tag 范围，以及是否能确认它们来自远程。
- Git LFS / submodule 覆盖情况：若未扫描，作为限制说明。
- 最近一次 `fetch` 是否成功。

### 阶段 2：敏感信息类型准备

加载 `references/sensitive-patterns.md`，按类型建立检查清单。优先关注：

- API Key、Access Key、Secret Key、Token、Cookie、Session。
- Password、数据库连接串、服务账号凭据。
- Private key、SSH key、证书、keystore。
- 云厂商凭据、CI/CD 凭据、Webhook secret。
- PII、身份证件、手机号、邮箱、客户数据。
- Internal address、内网域名、VPN、堡垒机、管理后台地址。

如果项目有特定技术栈或云厂商，补充对应模式；例如 AWS、Azure、GCP、阿里云、腾讯云、GitHub、GitLab、npm、PyPI、Docker Registry。

### 阶段 3：Remote history audit

目标是审计**已经推送到远程的历史**，不要只看当前工作区。

推荐顺序：

1. 刷新并列出远程引用：
   - `git fetch --all --prune --tags`
   - `git for-each-ref refs/remotes refs/tags --format="%(refname:short) %(objectname)"`
2. 枚举远程提交范围：
   - `git rev-list --remotes --tags`
   - 如用户指定范围，使用指定的 remote ref、commit range 或 pathspec。
   - 如果本地 tag 可能包含未推送 tag，在报告中标注 tag 来源限制，不要把无法确认来源的 tag 直接说成已推送。
3. 使用可用的专用扫描器：
   - 如果仓库已有 `gitleaks`、`trufflehog`、`detect-secrets` 等工具配置，优先使用现有配置。
   - 运行前先查看工具 `--help`，确认当前版本支持的历史扫描参数。
   - 记录工具名称、版本、命令、配置文件和退出结果。
4. 手工 git 证据交叉检查：
   - 用 `git log --remotes --tags -G <regex> --pickaxe-regex -- <paths>` 查找远程分支和 tag 历史 diff 中出现过的敏感模式。
   - 用 `git grep -I -n -E <regex> <remote-or-tag-commit> -- <paths>` 对可疑提交树做 blob 内容检查。
   - 用 `git log --remotes --tags --name-only --pretty=format:` 查找敏感文件名，如 `.env`、`.npmrc`、`.pypirc`、`id_rsa`、`*.pem`、`*.p12`、`kubeconfig`。
5. 检查 Git LFS 和 submodule 边界：
   - 如果存在 Git LFS，检查 `.gitattributes` 与 `git lfs ls-files`。Git 历史中的 LFS pointer 不等于真实对象内容；实际 LFS 对象若未下载或无权限扫描，必须写成覆盖限制。
   - 如果存在 submodule，使用 `git submodule status --recursive` 列出子仓库。子模块是独立 git 历史；除非用户要求纳入，否则不要假装已覆盖。
6. 对命中项做置信度判断：
   - High：真实凭据格式、私钥块、带有效上下文的 secret 变量、连接串含账号密码。
   - Medium：疑似 Token/key 但无法确认有效性。
   - Low：测试 fixture、示例值、明显占位符或已脱敏文本。

每条远程历史命中至少记录：

- 类型、置信度、是否已推送远程。
- 首次出现提交、最近仍存在提交、涉及远程引用。
- 文件路径、行号或 blob 位置。
- 脱敏证据片段。
- 影响判断和建议动作。

### 阶段 4：Unpushed content statistics

统计尚未推送到远程的内容，区分不同来源：

- 工作区状态：`git status --porcelain=v1 --branch`
- 已暂存差异：`git diff --cached`
- 未暂存差异：`git diff`
- 未跟踪文件：`git ls-files --others --exclude-standard`
- ignored 文件：`git ls-files --others --ignored --exclude-standard`
- stash：`git stash list`，必要时用 `git stash show -p stash@{n}` 只读检查并脱敏记录。
- 本地领先上游的提交：`git log @{u}..HEAD --oneline --decorate`；如果没有上游，说明无法直接判断并改用远程默认分支作参考。

对这些内容执行与远程历史一致的敏感模式检查，但报告中标记为**未推送**或**本地待推送风险**。统计至少包括：

- 命中总数，按来源分组：staged、unstaged、untracked、ignored、stash、local-only commits。
- 命中文件数和高风险命中数。
- 是否存在即将随下一次 push 进入远程的内容。
- 建议在提交/推送前如何清理。

### 阶段 5：证据脱敏和去重

不得在报告中输出完整敏感值。使用以下方式表达证据：

- 保留变量名、文件路径、行号、提交号。
- 值只显示短前缀和长度，例如 `ghp_****(len=40)`。
- 私钥只说明块类型，例如 `BEGIN OPENSSH PRIVATE KEY`，不粘贴正文。
- PII 只展示字段名、数量和类别，不展示完整个人数据。
- 对同一敏感值跨多个提交重复出现的情况合并为一个发现项，并记录传播范围。
- 扫描器日志、JSON 或 SARIF 结果只保留 sanitized scanner output；如果工具输出含完整 secret，先脱敏再汇总，不把原始输出贴进报告。
- 不主动验证真实 Token、密码或 key 是否可用；验证动作可能扩大审计范围并触发外部系统日志。

## 报告输出

使用 `references/report-template.md` 的结构。报告必须包含：

- Audit summary：整体风险等级、是否发现已推送远程泄露、是否发现未推送风险。
- Scope：审计范围、远程引用、提交范围、工作区范围、工具和限制。
- Remote tag scope：tag 是否纳入、来源是否可确认。
- Remote history findings：已推送远程历史命中记录。
- Unpushed content statistics：未推送内容统计和命中记录。
- Local stash and ignored files：stash 与 ignored 文件覆盖情况。
- General remediation：通用修复方案。

如果没有发现命中，也要输出审计范围、方法、限制和预防建议，不能只说“没问题”。

## 通用修复方案 (General remediation)

按风险分层给建议，不在未确认前执行破坏性操作。

### 已推送到远程

1. **立即撤销或轮换凭据**：API key、Token、密码、证书、Webhook secret、数据库密码等先在来源系统失效化。
2. **评估暴露面**：确认远程仓库可见性、分支、tag、fork、release、CI 日志、缓存和包制品是否也含敏感值。
3. **清理当前代码**：移除敏感值，改用环境变量、secret manager、加密配置或运行时注入。
4. **改写历史**：需要时使用 `git filter-repo` 或 BFG 清理历史；执行前要求用户确认范围和备份策略。
5. **安全推送**：清理后使用 `git push --force-with-lease`，并明确提示会影响协作者历史。
6. **协作者同步**：通知团队重新 clone 或按指定步骤重置本地分支，避免旧提交再次推回远程。
7. **远程平台处理**：必要时联系 GitHub/GitLab/托管平台清理缓存、PR diff、release、artifact 或搜索索引。

### 未推送到远程

1. 从工作区或暂存区移除敏感值。
2. 如果在本地提交中，使用 amend、interactive rebase 或 reset 清理；执行前确认不会丢失用户未保存工作。
3. 更新 `.gitignore`，例如忽略 `.env`、本地证书、密钥文件、临时导出文件。
4. 在推送前重新运行扫描，确认命中消失。

### 长期预防

- 增加 pre-commit secret scanning。
- 在 CI 中加入 secret scanning，并阻止高风险命中合并。
- 为示例配置使用 `.example` 文件和占位符。
- 使用最小权限、短期凭据和自动轮换。
- 为敏感配置建立团队约定和安全清单。

## 常见错误

- 只扫描当前工作区，漏掉已经推送到远程的历史提交。
- 只扫描远程分支，漏掉已经推送的 tag、release 指向或 tag-only 提交。
- 把 Git LFS pointer 当成真实 LFS 对象内容，或者默认子模块已被主仓库审计覆盖。
- 漏掉 stash 和 ignored 文件中尚未推送但高风险的本地敏感信息。
- 报告中粘贴完整密钥，造成二次泄露。
- 拿真实 Token 调外部接口做“有效性验证”，扩大泄露面。
- 发现远程泄露后只删除文件，不撤销或轮换凭据。
- 没有区分“已推送远程”和“未推送本地风险”。
- 在未确认范围和影响前执行 `git filter-repo`、BFG、`git reset --hard` 或强推。
- 把测试用例、示例值和真实凭据混为一谈，没有做置信度判断。

## 交付前自检

- [ ] 已说明远程引用是否刷新成功。
- [ ] 已审计 `refs/remotes/*`、`refs/tags/*` 或用户指定的远程范围。
- [ ] 已说明 Git LFS 和 submodule 是否覆盖。
- [ ] 已统计 staged、unstaged、untracked、ignored、stash、local-only commits。
- [ ] 已避免验证真实凭据有效性。
- [ ] 所有证据均已脱敏。
- [ ] 已区分 High/Medium/Low 置信度。
- [ ] 已给出已推送远程和未推送内容的不同修复路径。
- [ ] 未执行删除、历史改写、强推等破坏性操作，除非用户另行明确确认。
