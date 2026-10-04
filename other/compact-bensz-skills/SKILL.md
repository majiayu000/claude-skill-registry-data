---
name: compact-bensz-skills
description: 当用户明确要求压缩、瘦身或精简 Agent Skill 文档、降低上下文开销且不改变功能时使用。⚠️ 不适用：新增功能、修复脚本逻辑、批量改代码或压缩普通文档。

metadata:
  author: Bensz Conan
  short-description: 在不改变功能的前提下压缩 Agent Skill 的 Markdown 上下文
  keywords:
    - compact-bensz-skills
    - skill compaction
    - markdown compression
    - context reduction
    - Agent Skills
---

# compact-bensz-skills

## 目标

当用户明确要求“压缩/瘦身/精简某个 Agent Skill 的 Markdown 文档”“在不改变功能前提下降低 skill 上下文开销”时使用。先理解目标 skill 的真实能力与安全边界，再在忽略 `tests/`、`plans/` 以及目标 skill 的 `README.md`、`CHANGELOG.md` 的前提下，压缩 `SKILL.md`、`references/*.md` 等工作型 Markdown，并把中间产物隔离到 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/`。⚠️ 不适用：用户主要想新增功能、修复脚本逻辑、批量改代码、或只想压缩非 skill 文档。

## 流程

### 输入

#### 输入

1. `skill_root`（必需）
   - 目标 Agent Skill 根目录
2. `workspace_dir`（可选）
   - 默认把本轮工作区建在 `<skill_root>/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/`
   - 如果用户显式指定其它目录，则把它视为“run 容器根目录”，本轮仍落到其中的 `{yyyy-mm-dd-hh-mm}/`
3. `run_id`（可选）
   - 用于在 `init -> measure -> validate` 间显式复用同一轮工作区
4. `test_dir`（可选）
   - 默认 `<skill_root>/tests/compact-bensz-skills/`

### 执行步骤

#### 核心原则

- **先理解，再压缩**：先读 `SKILL.md`、`config.yaml`、`scripts/` 和必要的 `references/`，再判断哪些 Markdown 可以缩短。
- **不改行为，只改表达**：压缩的是文档体积，不是功能边界；不得擅自新增、删除或扭曲目标 skill 的能力。
- **保护触发语义**：`SKILL.md` frontmatter 的 `name` 必须保持不变；`description` 只能等价压缩，不能丢失关键触发条件。
- **保护硬约束**：输入、输出、默认路径、安全限制、必跑脚本、失败条件、与其它 skill 的协作约定都必须保留。
- **只动源工作文件**：忽略目标 skill 的 `tests/`、`plans/` 及其内容，不把它们视为待压缩源文件。
- **默认不动说明文档**：目标 skill 根目录下的 `README.md`、`CHANGELOG.md` 一般属于面向人类的说明或发布记录，不视为默认压缩目标。
- **中间文件隔离**：分析、快照、统计、验证结果都写到隐藏目录 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/`；除非用户另有指定，不向外泄露中间文件。
- **按轮次隔离**：每次运行都应在 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/` 内工作，避免多次压缩会话互相覆盖。
- **链接不能越界**：压缩后保留的本地 Markdown 链接必须仍位于目标 skill 根目录内，不能借相对路径跳到 skill 外部。

#### 标准工作流

##### 1. 初始化隐藏工作区

优先使用确定性脚本创建工作区、快照和 Markdown 清单：

```bash
python3 compact-bensz-skills/scripts/init_workspace.py --skill-root /path/to/target-skill
```

脚本会：
- 创建 `<skill_root>/.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/`
- 在隐藏根目录写入 `latest-run.txt`
- 扫描待压缩 Markdown（忽略 `tests/`、`plans/`、`README.md`、`CHANGELOG.md`）
- 生成 `analysis/file-inventory.json`
- 备份原文到 `snapshots/before/`
- 生成 `analysis/compaction-plan.md`
- 记录压缩前统计到 `reports/size-before.json`

##### 2. 理解目标 skill 的真实功能

最低阅读范围：
- `SKILL.md`
- `config.yaml`（如存在）
- `scripts/`（如存在）
- `references/` 中与核心流程直接相关的文档
- 仅当 `README.md`、`CHANGELOG.md` 与核心行为边界强相关时才辅助阅读；默认不把它们纳入压缩目标

理解时重点确认：
- 技能触发条件与不适用范围
- 输入输出契约
- 默认工作区 / 测试区 / 中间文件路径
- 安全边界与只读/只写限制
- 任何“必须执行”“不得省略”的步骤

##### 3. 执行 Markdown 压缩

优先顺序：
1. 删重复：移除跨文件、跨章节重复解释
2. 缩长句：把啰嗦描述改成短句、表格或清单
3. 主从分离：`SKILL.md` 只保留触发逻辑、主流程、硬约束；细节下沉到 `references/`
4. 压示例：保留最小可用命令和最关键示例，删除低价值变体

默认优先处理：
- `SKILL.md`
- `references/` 中真正承载执行细则的 Markdown

默认不处理：
- 目标 skill 根目录下的 `README.md`
- 目标 skill 根目录下的 `CHANGELOG.md`

压缩时必须保留：
- `SKILL.md` frontmatter 与关键词可发现性
- 关键命令、路径、文件名、配置键
- 输入/输出、默认目录、安全限制
- 会改变行为的条件分支
- 与 `bensz-collect-bugs` 等跨 skill 约定

压缩时禁止：
- 把“必需”改成“可选”
- 删除失败条件、边界条件、路径约束
- 删除唯一的命令示例或唯一的输出说明
- 只为了省字而制造歧义

##### 4. 复测压缩收益

完成文档修改后重新统计：

```bash
python3 compact-bensz-skills/scripts/measure_markdown.py --skill-root /path/to/target-skill --phase after
```

如需显式复用某一轮：

```bash
python3 compact-bensz-skills/scripts/measure_markdown.py \
  --skill-root /path/to/target-skill \
  --run-id 2026-03-28-15-52 \
  --phase after
```

该脚本会输出：
- `reports/size-after.json`
- `reports/size-delta.md`

##### 5. 校验压缩后仍可用

```bash
python3 compact-bensz-skills/scripts/validate_compaction.py --skill-root /path/to/target-skill
```

默认会复用 `latest-run.txt` 指向的最近一轮；如果你在多个 run 之间切换，显式传 `--run-id` 更稳妥。

至少检查：
- `SKILL.md` frontmatter 是否完整
- `metadata.author` 是否保留
- `metadata.keywords` 是否仍包含 skill 名
- 本地 Markdown 相对链接是否仍有效且没有越出目标 skill 根目录
- 压缩后的总字数是否低于压缩前
- 若 `description` 有改动，确认只是等价压缩而非改坏触发语义

#### 何时读取参考文档

- 需要决定“哪些内容必须保留”时，读 `references/preservation-checklist.md`
- 需要具体压缩手法时，读 `references/compaction-playbook.md`
- 做收尾校验时，读 `references/validation-checklist.md`

### 输出

#### 输出

对用户的主要交付：
- 更新后的目标 skill 工作型 Markdown 源文件

隐藏工作区产物：
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/latest-run.txt`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/analysis/file-inventory.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/analysis/compaction-plan.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/reports/size-before.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/reports/size-after.json`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/reports/size-delta.md`
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/compact-bensz-skills/{yyyy-mm-dd-hh-mm}/reports/validation.json`

### 输出管理

#### BenszAPI 任务工作区


### 校验

至少检查 frontmatter、`metadata.author`、技能关键词、相对链接、关键命令/路径/失败条件和触发语义均保留；压缩后的 Markdown 总量应低于压缩前，且 `validate_compaction.py` 与引用检查通过。不能证明语义等价时不得交付压缩版本。

### 失败与恢复

快照、统计、链接或语义校验失败时保留 `snapshots/before/`、报告和错误日志，停止写回正式 Skill；可在同一 run 目录修正后重试，若收益或保真无法满足阈值则恢复基线并报告原因。


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
