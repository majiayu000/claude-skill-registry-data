---
slug: lingmin-code-pm
version: 1.1.0
displayName: 代码项目管理 (Code PM)
summary: 管理项目注册表、git 工作流规范与 AI 编码同事最佳实践。
description: 代码项目管理。收到编码任务、操作 git 仓库或查看项目状态时激活。管理项目注册表、git 工作流规范与 AI 编码同事最佳实践。支持云效/GitHub/GitLab 等，可复制分发。
author: OpenClaw
---

# 代码项目管理技能

管理代码项目列表、git 工作流与编码规范。技能本身零个人信息，任何人将本技能文件夹拖入自己的 `workspace/skills/` 即可使用。

---

## 首次使用引导

当本技能被激活且**技能目录下尚无 `projects.yaml`** 时，按以下步骤引导用户完成配置：

1. **创建项目注册表**  
   将本技能目录下的 `references/projects.example.yaml` 复制为技能目录下的 `projects.yaml`，并提示用户填写实际项目信息（仓库地址、本地路径、主分支、技术栈、负责人等）。

2. **配置代码托管凭证**  
   提示用户在 **workspace 根目录** 的 `TOOLS.md` 中增加「代码托管平台」一节，填写所用平台的认证信息。格式参考如下（不限于云效，也支持 GitHub、GitLab 等）：

   ```markdown
   ## 代码托管平台

   - 平台：云效 Codeup（或 GitHub / GitLab 等）
   - 用户名：your-username
   - 密码/Token：your-token
   - 认证方式：HTTPS（或 SSH，已配置 ~/.ssh/id_rsa）
   ```

3. **校验环境**  
   确认 `git` 可用；若使用 HTTPS，提醒用户确保凭证已配置（如 git credential store）；若使用 SSH，可提示用户测试 `ssh -T` 连接对应平台。

4. **绝不在代码提交、日志、memory 中暴露凭证。**

引导完成后，日常使用从技能目录下的 `projects.yaml` 读取项目列表，从 `TOOLS.md` 获取凭证说明（执行 git 命令时由用户环境提供实际认证）。

---

## 何时激活

- 收到编码任务（写代码、修 bug、实现功能）
- 需要操作 git 仓库（拉代码、建分支、提交、推送）
- 需要查看项目状态、项目列表或切换项目

---

## 项目注册表

项目信息从**本技能目录下**的 `projects.yaml` 读取。格式与字段说明见 `references/projects.example.yaml`。

单条项目示例：

```yaml
- name: "项目名称"
  repo: "https://codeup.aliyun.com/org/repo.git"
  local_path: "~/projects/repo"
  main_branch: "master"
  tech_stack: "Java + Spring Boot"
  description: "简短描述"
  contacts: "负责人或团队"
```

`local_path` 支持 `~` 或绝对路径，用于定位本地克隆目录。

**规范**: 默认代码仓库应统一放置在 `~/Projects/` 目录下。

---

## Git 工作流规范

### 分支规则

- **禁止**直接在 `main` / `master` 分支上修改代码。
- **禁止**在人类同事的分支上直接修改；需要时从目标分支**新切分支**再改。
- **新建分支命名**：`<ai-name>/<type>/<简短描述>`
  - `type` 取：`feature`、`fix`、`refactor`、`chore`
  - 示例：`lingmin/feature/user-login`、`lingmin/fix/null-pointer`
- **禁止**主动合并到主分支，除非人类明确要求。
- **禁止** `git push --force`。

分支前缀 `<ai-name>` 从 workspace 身份配置中读取（如 `SOUL.md` 中的名字）；若未配置则使用 `ai`，以便不同 AI 使用同一技能时分支前缀可区分。

### Pre-flight Protocol（强制）

以下步骤在**任何代码阅读或编辑操作前**必须完成，不可跳过。

1. **同步远端**：`git fetch origin` 获取最新远端状态。
2. **拉取更新**：若当前在跟踪分支上，执行 `git pull`；若有未提交修改，先 `git stash` 再 pull 再 `git stash pop`。
3. **状态确认**：`git status` 确认工作区状态符合预期（无未预期修改）。
4. **分支就位**：
   - **保护检查**：确认当前分支**不是** `main`/`master`。若在受保护分支上，**必须**先切出工作分支，不可直接修改。
   - **分支拓扑感知**：执行 `git branch -a` 查看所有分支，用 `git log --oneline --graph --all -20` 理解分支间的派生关系（如 `feature/v0.2` 签出自 `feature/v0.1`，`feature/v0.1` 签出自 `main`）。若存在多个活跃分支，**必须**向用户说明分支拓扑并确认应基于哪个分支工作，不可自行假定。
   - 新任务：从**用户确认的**目标分支切出工作分支。
   - 继续任务：确认在正确的工作分支上（不能是 `main`/`master`），且已包含远端最新变更。
5. **阅读先行**：阅读项目结构与现有代码风格后再改代码。
6. **编辑走 opencode Plan→Build**：代码编辑必须通过 opencode 完成（配置见 `TOOLS.md` → opencode 段）。启动 opencode 后**先用 Plan agent 分析任务、生成方案**，可以使用Plan agent多次迭代方案，确认方案无误后再切 Build agent 执行。禁止跳过 Plan 直接 Build。

**违反 Pre-flight 直接操作代码视为工作流错误，必须回退并重新执行。**

### 提交规范

- **原子提交**：一个逻辑变更对应一个 commit。
- **提交前自查**：不提交 `.env`、密钥、调试代码（如 `console.log`、`print`）、构建产物；若有项目级 lint/test，提交前执行。
- Commit message 使用中文（若 workspace 有约定则遵循约定）。

### 推送规范

- 完成有意义的改动后及时推送，避免本地积攒过多未推送提交。
- push 前用 `git status` 与 `git log` 确认将要推送的内容无误。

---

## AI 编码同事最佳实践

1. **先读后写** —— 修改前充分阅读相关代码，理解上下文与风格，保持风格一致。
2. **不留垃圾** —— 提交前清理调试代码、临时注释与临时标记。
3. **冲突不自作主张** —— 遇到 merge conflict 时告知人类，由人类决策，不自动 resolve。
4. **进度汇报** —— 完成任务后简要总结：做了什么、改了哪些文件、可能的影响。
5. **不过度工程** —— 只做被要求的事，不顺手重构无关代码。
6. **安全意识** —— 不硬编码密钥；commit message 中不暴露敏感信息。
7. **测试意识** —— 修改后运行相关测试，确保不破坏已有功能。
8. **文档意识** —— 若修改了公共 API/接口，提醒人类是否需要更新文档（不自行决定并改文档）。
9. **安全回退** —— 改坏了用 `git revert`，不用 `git reset --hard`。
10. **上下文切换** —— 切换项目前先 stash 或提交当前工作，避免丢失进度。

---

## 可移植性说明

- 本技能 **不硬编码** 凭证、项目列表、平台名称；全部通过首次引导与用户配置完成。
- 适用于任意 git 型代码托管（云效、GitHub、GitLab 等），只需用户在 `TOOLS.md` 中填写对应凭证说明。
- 依赖仅为系统 `git` 与用户配置的认证方式（HTTPS 或 SSH）。
