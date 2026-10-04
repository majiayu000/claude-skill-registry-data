---
name: git-publish-release
description: 当用户明确要求发布项目到 GitHub、创建 GitHub Release 或生成 Release Notes 时使用。根据版本历史整理发布说明；仅要求预览时不执行发布。

metadata:
  author: Bensz Conan
  short-description: GitHub Release 发布与 Release Notes 生成（按请求区分预览/发布）
  keywords:
    - git-publish-release
    - GitHub Release
    - release notes
    - version publish
---

# GitHub Release

## 目标

当用户明确要求"发布项目到 GitHub"、"创建 GitHub Release"或"生成 Release Notes"时使用。智能分析 tag 间历史变化并生成专业的 Release Notes；明确发布/创建请求时自动创建 GitHub Release，单独的 notes/历史总结请求仅生成预览，除非用户随后确认发布。支持首次发布、常规版本、预发布版本（alpha/beta/rc），自动识别 prerelease 标记。

## 流程

### 输入

#### 触发条件

用户需要：
- 发布项目的新版本到 GitHub
- 创建 GitHub Release 并自动生成 Release Notes
- 推送某个 tag 到 GitHub 并创建 release
- 总结版本间的历史变化

#### 你需要确认的输入

1. **目标 tag**（如 `v3.0.0`）
   - 如未指定，列出最近 tags 供选择
2. **项目路径**（可选，默认当前工作目录）

3. **任务输出目录**（宿主可设置 `TASK_OUTPUT_DIR`，指向本轮已声明的
   `./.bensz-api/task-.../git-publish-release/output/`；未设置时临时 notes 使用 OS 临时目录并立即清理）

> 认证通过 `gh auth login` 管理，无需手动配置 token。

明确要求“发布项目到 GitHub”或“创建 GitHub Release”时，按配置执行远程发布；仅要求“生成 Release Notes”或“总结版本间的历史变化”时只生成文案/预览，不调用 `gh release create`，除非用户随后明确确认发布。`release.require_confirmation` 的含义是：明确发布/创建请求可作为本次授权，覆盖已有 Release 仍按下方错误处理规则询问；不得把文案生成请求视为远程发布授权。

### 执行步骤

#### 工作流程

##### 确认项目信息

```bash
# 获取 owner/repo
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

##### 获取最新 Release 信息

```bash
# 获取最近一次 release 的 tag
PREVIOUS_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')
```

- 如果存在历史 release，比较范围为：`PREVIOUS_TAG..TARGET_TAG`
- 如果是首个 release，比较范围为：从初始 commit 到 `TARGET_TAG`

##### 分析历史变化

获取两个版本之间的 commit 历史：

```bash
# 如果有历史 release
git log ${PREVIOUS_TAG}..${TARGET_TAG} --pretty=format:"%h|%s|%an|%ad" --date=short

# 如果是首个 release
git log ${TARGET_TAG} --pretty=format:"%h|%s|%an|%ad" --date=short
```

##### 生成 Release Notes

根据 commit 历史和项目特点，智能生成 Release Notes。

###### Release Notes 结构

```
🎉 [版本号] - [吸引人的标题]
[一句话总结本次发布的核心价值/意义]

🚀 核心亮点：
• [亮点1]
• [亮点2]
• [亮点3]

✨ 主要更新：
[类别1]
• 更新内容1
• 更新内容2

[类别2]
• 更新内容3
• 更新内容4

🔧 技术改进：
• 技术改进1
• 技术改进2

📋 完整变更日志：
[简略说明获取方式或列出主要 commits]
```

###### 标题撰写原则

- **情感化表达**：使用"革命性"、"突破性"、"里程碑"等词汇
- **场景化描述**：说明这个版本解决什么问题、带来什么价值
- **时效性关联**：如"为 2026 年就绪"、"拥抱新范式"

###### 内容分类原则

根据 commit 信息自动分类：

| 类别图标 | 类别名称 | Commit 关键词示例 |
|---------|---------|-----------------|
| 🚀 | 核心亮点 | breakthrough, major, feature |
| ✨ | 新功能 | add, new, feature |
| 🐛 | Bug 修复 | fix, bugfix, resolve |
| 🔧 | 技术改进 | refactor, optimize, improve |
| 📝 | 文档更新 | docs, readme, guide |
| 🔐 | 安全更新 | security, fix vulnerability |
| 💥 | 破坏性变更 | breaking, deprecate |

###### 语言风格

- **简洁有力**：每个要点不超过一行
- **价值导向**：强调"为什么"而非仅仅"是什么"
- **用户视角**：用用户能理解的语言，避免技术术语堆砌
- **适当煽动**：使用感叹号、emoji 营造氛围，但不过度

##### 判断是否为 Prerelease

根据 tag 名称自动判断：
- 包含 `alpha`, `beta`, `rc`, `pre` 等标识 → `prerelease: true`
- 否则 → `prerelease: false`

##### 按授权创建 GitHub Release

仅在用户明确要求发布/创建 Release，或在预览后明确确认发布时执行以下命令；单独的 Release Notes/历史总结请求不得执行此步骤。

```bash
# 将 Release Notes 写入临时文件（避免 shell 转义问题）
# TASK_OUTPUT_DIR 可由宿主设置为本次任务已声明的
# ./.bensz-api/task-.../git-publish-release/output/ 目录；未注入时仅使用
# 一次性的 OS 临时目录，并在流程结束后清理，不把它当作任务产物。
NOTES_DIR="${TASK_OUTPUT_DIR:-${TMPDIR:-/tmp}}"
mkdir -p "$NOTES_DIR"
NOTES_FILE=$(mktemp "$NOTES_DIR/release-notes-XXXXXX.md")
cat > "$NOTES_FILE" << 'NOTES_EOF'
[生成的 Release Notes 内容]
NOTES_EOF

# 正式版
gh release create "$TARGET_TAG" \
  --title "$TARGET_TAG" \
  --notes-file "$NOTES_FILE"

# 预发布版（tag 含 alpha/beta/rc/pre 时）
gh release create "$TARGET_TAG" \
  --title "$TARGET_TAG" \
  --notes-file "$NOTES_FILE" \
  --prerelease

# 清理临时文件
rm -f "$NOTES_FILE"
```

#### 参考资源

- Release Notes 生成策略：[references/release-notes-strategy.md](references/release-notes-strategy.md)
- Release Notes 示例模板：[references/release-templates.md](references/release-templates.md)
- GitHub CLI 文档：https://cli.github.com/manual/gh_release_create

### 输出

#### 输出格式

完成发布后，向用户输出：

```
✅ Release 发布成功！

📍 Release URL: [release 链接]
🏷️ Tag: [tag 名称]
📅 发布时间: [时间]

📝 Release Notes 预览：
[生成的前 10 行 notes]
```

如果用户只要求 Release Notes 或历史总结，输出文案预览及对应的历史范围，不报告 Release URL，也不宣称已发布。

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 前置检查

确认 `gh` CLI 已安装并已认证：

```bash
gh auth status
```

如未认证，提示用户运行：

```bash
gh auth login
```

### 失败与恢复

#### 错误处理

| 场景 | 处理方式 |
|------|---------|
| `gh` 未安装 | 提示安装：`brew install gh` 或访问 https://cli.github.com |
| `gh` 未认证 | 提示运行 `gh auth login` |
| Tag 不存在 | 提示用户可用的 tags 列表 |
| 网络请求失败 | 重试 3 次，仍失败则报错并给出手动创建指南 |
| 权限不足 | 提示检查 `gh auth status` 及仓库权限 |
| Release 已存在 | 询问用户是否覆盖（使用 `gh release edit`） |

#### 实现注意事项

1. **跨平台兼容**：始终使用正斜杠 `/` 处理路径
2. **Notes 转义**：使用 `--notes-file` 传递临时文件，避免 shell 特殊字符转义问题
3. **Git 远程解析**：`gh repo view` 自动处理 HTTPS 和 SSH 两种 remote URL 格式
4. **认证管理**：`gh` CLI 使用系统 keychain 或 `~/.config/gh/hosts.yml` 存储凭证，无需手动管理 token


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
