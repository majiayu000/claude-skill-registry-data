---
name: bensz-collect-bugs
description: 当 Bensz Agent Skill 或基础设施本身因设计缺陷出现问题，或用户明确要求记录/上报此类 bug 时使用。⚠️ 不适用：用户数据错误、第三方服务故障、用户主动改源码或模型偶发波动。
metadata:
  author: Bensz Conan
  short-description: 收集并公开上报 Bensz 系列 skills 的设计缺陷类 bug
  keywords:
    - bensz-collect-bugs
    - bug collection
    - bug report
    - gh upload
    - skills bug
---

# Bensz Collect Bugs

## 目标

这是一个用于 Bensz Agent Skill 与基础设施设计缺陷留痕和按需上报的 Agent Skill。当 Bensz Agent Skill 在真实用户环境中因设计缺陷而出现 bug，或用户明确说“我想 report bensz skills bugs”“帮我公开上报 bensz skills 的 bug”时使用。该 Skill 负责把 bug 规范化记录到 `~/.bensz-skills/bugs/`，并在用户明确要求公开报告时通过本地 `gh` 轻量上传到 `huangwb8/bensz-bugs`，全程严禁修改用户本地 Claude Code/Codex 中已安装 Skills 的源代码。

用于“先本地留痕，再按需公开上报”的 bug 管理 skill。

## 流程

### 输入

#### 输入契约

##### 本地记录时必需信息

- `skill_name`
- `skill_author`
- `bug_summary`
- `expected_behavior`
- `actual_behavior`

##### 强烈建议补充

- `reproduction_steps`
- `evidence`
- `workaround`
- `agent_runtime`
- `skill_source_path`

### 执行步骤

#### 只处理哪类问题

只处理这类 bug：

- 由于 **Bensz Agent Skill 或 Bensz 基础设施的设计缺陷** 导致其无法按契约工作
- 典型表现包括：流程漏判、输入契约不完整、环境假设错误、脚本/模板设计不健壮、输出规范不一致

不要把下列情况记为本 skill 的 bug：

- 用户数据本身有误
- 第三方服务临时不可用
- 用户主动修改了 skill 源码引入的问题
- 纯粹属于模型偶发发挥波动、但 skill 设计本身没有明显缺陷的情况

#### 标准工作流

##### 阶段一：判断是否属于“skill 设计缺陷”

至少回答清楚：

1. 出问题的 skill 是哪个
2. 它原本应该怎样工作
3. 实际发生了什么
4. 为什么这是 skill 设计缺陷，而不是用户输入问题或外部服务抖动

如果判断不足以支持“设计缺陷”结论，不要强行记录。

##### 阶段二：本地记录 bug

优先运行确定性脚本：

```bash
python3 bensz-collect-bugs/scripts/collect_bug.py \
  --skill-name "<skill_name>" \
  --skill-author "Bensz Conan" \
  --bug-summary "<一句话概括 bug>" \
  --expected-behavior "<预期行为>" \
  --actual-behavior "<实际行为>" \
  --reproduction-step "<步骤1>" \
  --reproduction-step "<步骤2>" \
  --evidence "<关键报错或关键现象>"
```

可选补充：

- `--workaround`
- `--severity`
- `--device-type`
- `--agent-runtime`
- `--skill-source-path`
- `--skill-source-repo`
- `--additional-note`
- `--software key=value`

脚本会自动：

- 收集当前设备 / OS / shell / 常见软件版本
- 对 bug 摘要、预期/实际行为、复现步骤、证据、补充说明等自由文本执行敏感信息清洗
- 按 `config.yaml:hashing.stable_fields` 计算稳定的 `bug_hash`
- 在 `~/.bensz-skills/bugs/{skill_name}/{reporter}/{bug_hash}/` 写入标准化记录
- 若同一 bug 已存在，则只更新 `occurrence_count`、`last_seen_at` 等追踪字段

说明：

- `reporter` 优先使用当前 GitHub 用户名
- 若没有 GitHub 用户名，报告展示名默认使用匿名占位，不再回退到本地用户名
- 若当前机器尚未配置 `gh`，则本地目录先落到 `pending-github-identity/`，公开上报时再改用真实 GitHub 用户名作为远端路径

##### 阶段三：让当前任务继续

记录 bug 并不意味着当前任务必须中断。

如果 AI 仍可通过临时 workaround 完成用户任务：

- 把 workaround 写进 bug 记录
- 继续完成用户眼前的任务

##### 阶段四：公开上报到 `bensz-bugs`

只有当用户明确说出类似意图时才做：

- “我想 report bensz skills bugs”
- “帮我公开上报这些 bensz skill 的 bug”

先检查 `gh`：

```bash
gh auth status
```

若未登录，指导用户执行：

```bash
gh auth login
```

然后运行：

```bash
python3 bensz-collect-bugs/scripts/report_bugs.py
```

可选过滤：

```bash
python3 bensz-collect-bugs/scripts/report_bugs.py --skill-name "<skill_name>"
```

该脚本会：

- 扫描 `~/.bensz-skills/bugs/` 下全部本地 bug
- 用当前 `gh` 登录用户作为公开报告用户名
- 先校验远端仓库可访问，再开始上传
- 跳过已公开或远端已存在的 bug
- 对公开副本做脱敏，移除本地用户名、主机名、工作目录、绝对路径等仅应保留在本机的信息
- 直接通过 `gh api repos/{owner}/{repo}/contents/{path}` 创建文件
- 把本地 `bug-context.json` 的公开状态更新为已上报

若只想预演，可运行：

```bash
python3 bensz-collect-bugs/scripts/report_bugs.py --dry-run
```

`--dry-run` 只输出“预计会上传哪些 bug”，不会修改本地状态，也不会触碰远端仓库。

##### 阶段五：追加 resolution 闭环

修复、专项回归和版本核对全部通过后，先预演：

```bash
python3 bensz-collect-bugs/scripts/resolve_bug.py \
  --bug-dir "<bug目录>" \
  --status fixed \
  --canonical-root-cause "<canonical ID>" \
  --fixed-version-or-commit "<版本或 commit>" \
  --verification "<可复核的测试命令与结果>" \
  --dry-run
```

确认后移除 `--dry-run`。重复报告改用 `--status duplicate` 并提供 `--duplicate-of`。脚本只创建 `RESOLUTION.md`：相同 resolution 重复执行返回 unchanged，已有内容不同时拒绝覆盖；缺少验证证据或修复版本时拒绝标记 resolved。

#### 参考资源

- 规范模板：`templates/BUG_REPORT_TEMPLATE.md`
- resolution 模板：`templates/RESOLUTION_TEMPLATE.md`
- 数据模型说明：`references/DATA_MODEL.md`
- 公开上报约定：`references/REPORTING_PROTOCOL.md`

### 输出

#### 输出

##### 本地记录输出

- `~/.bensz-skills/bugs/{skill_name}/{reporter}/{bug_hash}/bug-context.json`
- `~/.bensz-skills/bugs/{skill_name}/{reporter}/{bug_hash}/BUG_REPORT.md`
- 完成闭环后追加 `~/.bensz-skills/bugs/{skill_name}/{reporter}/{bug_hash}/RESOLUTION.md`

##### 公开上报输出

- 远端仓库路径：`{skill_name}/{github_username}/{bug_hash}/`
- 本地 `bug-context.json` 中的：
  - `tracking.public_reported`
  - `tracking.public_repo`
  - `tracking.public_path`
  - `tracking.reported_at`

### 输出管理

正式交付物、临时产物和日志继续遵循原有路径及覆盖边界；任务级中间文件使用当前会话声明的 `.bensz-api` 工作区。

### 校验

提交本地记录或公开上报前，校验 `BUG_REPORT.md`/`bug-context.json` 的必需字段、最小复现与影响范围、路径模式和敏感信息脱敏；只有提供修复版本与可复核验证证据时才允许追加 `RESOLUTION.md` 或标记 resolved。网络/`gh` 失败时保留本地记录并报告阻塞。

### 失败与恢复

#### 执行注意事项

- 优先读 `config.yaml` 获取本地根目录、文件名、仓库名和版本采集命令
- 本地目录结构遵循 `config.yaml:storage.path_pattern`
- 若配置了非默认 GitHub 主机，公开上报阶段应遵循 `config.yaml:github.api_host`
- `BUG_REPORT.md` 必须保持标准章节，便于后续人工浏览
- 如果用户给出的文本里含有敏感信息，必须先做脱敏/替换，再允许落盘或公开
- `--reporter-display-name` 已废弃；为保护隐私，该参数当前不会写入记录
- 如果用户只想本地记录，不要擅自公开
- 如果用户要求公开，但 `gh` 不可用，要先把阻塞点说清楚，再帮助其配置，而不是跳过鉴权直接失败


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

#### 硬规则

- **严禁**直接修改用户本地 Claude Code / Codex 已安装 skills 的源代码来“顺手修 bug”
- 本地记录目录固定为 `~/.bensz-skills/bugs/`
- 本地每个 bug 目录固定结构为 `{skill_name}/{reporter}/{bug_hash}/`
- 每个 bug 目录必须包含：
  - `bug-context.json`
  - `BUG_REPORT.md`
- `RESOLUTION.md` 只能在源码修复、专项回归和版本核对完成后追加；不得覆盖原始证据
- 用户明确要求“report bensz skills bugs”之前，只做本地记录，不做公开上传
- 公开上传时必须走用户本机的 `gh` 能力；如果 `gh` 未登录，先协助用户完成 `gh auth login`
- 上传阶段**不要 pull / clone 整个 `bensz-bugs` 仓库**；直接用 `gh api` 按文件路径创建内容
- 写入 `BUG_REPORT.md` 与 `bug-context.json` 时，**严禁**保留用户隐私、财产或其他私密信息，尤其是密钥、密码、身份信息、电话、邮箱、银行卡号与私密路径
- 本地记录阶段也必须执行最小化采集：默认不收集本地用户名、主机名、当前工作目录等高风险个人标识
- 公开上传前必须对本地专属信息做脱敏；公开仓库中不得泄露本地用户名、主机名、工作目录、绝对路径等隐私字段
