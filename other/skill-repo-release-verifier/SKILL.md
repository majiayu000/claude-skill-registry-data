---
name: skill-repo-release-verifier
description: Use when a Codex Skill repository needs a deterministic release gate, scoped commit evidence, GitHub synchronization, or verified remote publication status.
---

# Skill Repo Release Verifier

## 中文简介

**Skill 仓库发布验证器**把多 Skill 仓库的本地结构、导航、Git 提交和远端发布拆成可复核的门禁。它先给出机器可读的本地问题清单，再以实际命令证据区分“已验证同步”和“尚未验证/失败”。

## 使用背景

Skill 仓库容易在批量修改后留下目录与 frontmatter 不一致、V2 文件缺失、README 分类重复、中文索引遗漏或失效链接。更危险的是把本地提交或一次 push 尝试误写成远端已发布。本 Skill 用确定性脚本固定本地结构检查，并要求远端 SHA、默认分支和文件树都实际返回后才能报告成功。

## 核心原则

- 先检查工作区、目标仓库、默认分支、权限和网络，再执行会改变远端的操作。
- 本地结构由 `scripts/validate_skill_repo.py` 判定；CLI 默认要求本仓库的 20 个 Skill，也可用 `--expected-count` 验证通用 fixture 或其他仓库。脚本只使用标准库、稳定排序问题，并以非零退出阻断失败。
- 每个 Skill 独立运行 `quick_validate.py`；仓库脚本不替代该结构校验。
- 只暂存本次发布范围。发现无关改动时保留它们并停止请求确认，不能回退或顺手提交。
- 普通 `git push` 是首选；只有其失败且 GitHub CLI/API 身份可用时才使用 Contents API 回退。
- 远端成功必须有实际查询证据。没有默认分支、远端 SHA 或文件树结果时，状态只能是未验证、受阻或失败。

## 适用场景

- 多个 Skill 完成升级后，需要统一检查 V2 结构、六类 README 清单、中文索引和链接。
- 准备提交并发布到 GitHub，需要记录精确提交范围、push/API 回退和远端完整性。
- 网络、权限或分支信息不确定，需要把失败原因和下一步写准确，而不是猜测同步结果。

## 不适用场景

- 只需创建或重写单个 Skill 内容时；先使用对应领域 Skill 和 `quick_validate.py`。
- 没有 Git 仓库、远端或发布授权而要求“发布成功”时；本 Skill 只能完成本地检查并报告缺口。
- 需要修改 GitHub 仓库设置、权限策略或分支保护规则时；这些需要具备权限的仓库 owner 决策。

## 输入要求

至少收集仓库根目录、预期 GitHub `OWNER/REPO`、目标默认分支、允许发布的提交/文件范围，以及中文导航是否为发布要求。远端操作还需要可用认证、网络和对该分支写入权限。若用户指定 SHA、可见性或必需路径，也把它们列为验收条件。

## 信息不足时的处理

缺少仓库路径时只请求或确认当前目录；缺少 `OWNER/REPO`、默认分支、凭据或发布授权时，仍可运行本地验证，但远端状态写为“未执行，缺少 X”。push/API 报认证、403、404、超时或网络错误时，逐字记录命令、退出状态和可观察错误，不把它解释为仓库不存在、权限足够或发布完成。

## 工作流

1. **预检**：确认根目录、`git status --short --branch`、远端 URL、目标分支、预期发布文件和 `gh auth status`（仅在需要 API 时）。
2. **逐 Skill 与仓库校验**：对每个 `*/SKILL.md` 运行 `quick_validate.py`，再运行确定性验证器；保存人读摘要或 `--json` 问题对象。
3. **审计发布范围**：比较 base 与候选提交的 `git diff --name-only`、`git diff --check` 和暂存区；无关改动不暂存，范围不清楚就停下。
4. **提交**：只 `git add` 已批准路径，提交后记录完整 SHA 和 `git show --stat --oneline` 证据。
5. **普通同步**：向明确的远端和分支执行普通 push；成功后仍查询远端分支 SHA，确认它等于或包含本地候选提交。
6. **Contents API 回退**：仅在普通 push 已失败、目标分支和权限已确认时，先把 base 到候选提交的完整 A/M/D 清单保存为 NUL 文件；上传内容和候选 blob SHA 都从固定候选提交读取，删除项调用 Contents DELETE。A/M 只允许 Contents API 能准确表示的 `100644 blob`，其他 Git mode/type 停止并改用普通 push。
7. **远端核验**：查询仓库可见性、默认分支、分支 SHA 与未截断递归文件树；按同一份完整变更清单确认 A/M 的远端条目为 `100644 blob` 且 SHA 等于候选 blob、D 已不存在，再确认必需发布路径。无法读取或逐项匹配时不报告远端成功。
8. **报告**：分别给出本地、提交、同步和远端状态，附命令证据、路径/SHA、失败原因与剩余风险。

## 专业判断规则

- `validate_skill_repo.py` 的任何问题均为本地发布阻断项，除非 owner 明确接受例外并记录原因；不要用手工浏览替代。
- README 六类中每个实际 Skill 必须恰好出现一次；README/中文索引只提及但未正确分类仍不通过。相对链接不得逃出仓库，必需文件和 Markdown 目标的 symlink 也不得解析到仓库外；percent 编码路径必须解码后检查，Markdown 文件 fragment 必须匹配实际 heading anchor。
- `git push` 返回零只证明 transport 命令成功，不能证明默认分支、文件树或目标文件正确；必须随后读取远端状态。
- Contents API 的一次文件更新可能产生多个提交；因此按 API 返回值和最终分支 SHA/树验证，不能假设它等于本地 commit SHA。工作区可能在候选提交后继续变化，所以 fallback 的内容必须来自 `git show candidate:path`，候选 blob 必须来自 `git rev-parse candidate:path`；diff 必须先独立成功并保存完整清单，不能放进吞掉退出状态的 pipeline/process substitution。
- Contents API 不保留可执行位、symlink 或 submodule 语义。候选 `git ls-tree` 只有 `100644 blob` 可进入 fallback；`100755 blob`、`120000 blob`、`160000 commit` 及未知 mode/type 都必须在上传前 fail closed，并建议普通 `git push`。
- 读取远端文件时只有明确 `404` 才进入 create，`401`、`403` 和网络失败必须停止；递归树的 `.truncated` 为 `true` 时不能作完整性结论。上传后必须逐项验证完整 A/M/D 清单，不得只检查几个代表路径。
- `401` 表示认证缺失或失效，`403` 表示无权或策略拒绝，`404` 可能是路径不存在或私有仓库不可见，网络/超时是未验证；不得互相替换含义。
- 若远端默认分支不是预期分支，停止同步并报告分支差异；不要静默改写到 `main` 或当前分支。

## 输出契约

输出必须包含：

- 本地验证命令、Skill 数量、通过/失败状态，以及每个 `{path, code, message}` 问题。
- 逐 Skill `quick_validate.py` 结果、Git 工作区/暂存范围、base 与候选完整 SHA。
- 提交 SHA、同步方法、实际 push/API 输出和失败时的原始类别。
- 远端 `OWNER/REPO`、可见性、默认分支、远端分支 SHA、文件树数量和必需路径核验。
- 明确状态：`已验证同步`、`本地通过但远端未验证`、`同步失败` 或 `本地验证失败`，以及剩余风险和下一步。

## 质量门槛

- 确定性验证器和所有 fixture 测试通过，且真实仓库脚本输出 `PASS`。
- 每个 Skill 的 `quick_validate.py` 通过，`git diff --check` 为零。
- 发布提交只含批准路径；无关用户改动未被改写或暂存。
- 远端状态只有在默认分支、SHA 和文件树均由成功命令返回且满足预期时才可标为成功。

## 常见失败与修正

- **脚本只在真实仓库通过**：补充临时 fixture 覆盖缺文件、遗漏、重复、章节、链接、残留和 frontmatter，不允许测试读取真实仓库。
- **分类看起来完整但跨类重复**：依据 README 六个正式分类的首列条目修正，而不是搜索全文的偶然提及。
- **把命令示例当模板残留**：残留扫描跳过 fenced code，仅识别高置信未填写语句；仍人工复核新的命中。
- **push 失败后直接说已同步**：改为记录失败类别；只有可用凭据、目标分支确认后才能尝试 API 回退。
- **API 上传后没有远端核验**：查询 Contents SHA、默认分支与递归树；任何查询失败都保留未验证状态。

## 参考资料

- [中文使用指南](references/usage-guide.zh.md)：调用前准备、输入不足和结果解读。
- [命令与远端回退](references/commands.md)：本地验证、范围审计、push、Contents API 和远端核验命令。
- [发布检查清单](references/checklists.md)：本地、Git、同步和远端门禁。
- [场景示例](references/examples.md)：典型发布、信息不足和失败边界的准确报告。
