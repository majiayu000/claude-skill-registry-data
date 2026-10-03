---
name: setup-analysis-delivery
description: 首次为新项目接 analysis-to-delivery 工作流 — 生成 4 个项目级 paths/*.md 配置(legacy 仅兼容)。启动新项目或为既有项目接入此工作流时调用。
disable-model-invocation: true
version: 4.0.0
requires: [context-pointer]
---

# Setup Analysis-Delivery — 项目配置初始化

## Contract

- 输入: 项目根目录,已检测到的项目文件,可选的既有项目配置
- 输出: `paths/knowledge-path.md`、`paths/compliance-path.md`、`paths/tech-stack-path.md`、`paths/doc-naming-path.md`;可选 `decisions.md` ADR
- 门控: 4 个 `paths/*.md` 文件存在且非空(legacy 项目根 `*-path.md` 可接受但产生 warning);`knowledge-path.md` 至少含 1 个真实路径后才进入下游字段工作
- Required rules: `context-pointer`
- Required paths: `knowledge-path`, `compliance-path`, `tech-stack-path`, `doc-naming-path`
- 下一步: `/grill-task`

## 适用场景

- 拿到一个新项目,需要接 analysis-to-delivery 工作流
- 给现有项目补这套工作流的配置

## 流程步骤

### 1. 检测项目根

- 必须在 git 仓库根执行(`git rev-parse --show-toplevel`)
- 项目根不存在 `.git` → 提示用户先 `git init`

### 2. 检测项目类型

读项目根文件,推断技术栈:
- `pom.xml` / `build.gradle` → Java/Maven/Gradle
- `package.json` → Node/前端
- `pyproject.toml` / `requirements.txt` → Python
- `go.mod` → Go

### 3. 生成 4 个项目级配置(canonical)

**默认**:在项目根的 `paths/` 目录下生成 4 个空模板(用户填写后提交到 git)。
这 4 个文件是**唯一**项目级配置加载输入:

| Canonical 文件 | 作用 | 模板来源 |
|---|---|---|
| `paths/knowledge-path.md` | 列项目涉及的外部知识库(领域表结构、合规法规等)路径 | `paths/knowledge-path.md` |
| `paths/compliance-path.md` | 列项目适用的合规规则文件路径 + 启用开关 | `paths/compliance-path.md` |
| `paths/tech-stack-path.md` | 列后端/前端/数据库/中间件 + 团队规范路径 | `paths/tech-stack-path.md` |
| `paths/doc-naming-path.md` | 文档编号、命名前缀、存放目录 | `paths/doc-naming-path.md` |

**Legacy 兼容**:既有 v1.1 项目可能用项目根 `*.md`(`knowledge-path.md` 等)。`setup-check.py`
会把它们识别为 warning 并继续通过。生成时加 `--legacy` 切换到兼容输出位置(仅 v1.1 旧项目)。

### 4. 可选记录配置使用 ADR

- `config-used.md` 不是配置文件,不参与配置加载,不属于 4 个项目级配置
- 如需记录"本项目用了哪些配置、为什么这么选",从 `templates/CONFIG_USED.md` 复制生成
- `config-used.md` 应作为阶段 1 交付产物提交,用于审计和交接

### 5. 验证

- 4 个文件存在且非空(允许只有注释)
- 跑 `python3 scripts/setup-check.py --strict <project>` 确认通过(legacy 项目根文件会产生 warning 但仍通过)
- 跑 `python3 scripts/field-alignment-check.py --help` 确认脚本可用

## 调用的 rule

- `rules/context-pointer` — 三层配置加载规则

## 结束条件

- [ ] 4 个 `paths/*.md` 全部生成在项目根(或兼容的 legacy 项目根 `*.md`)
- [ ] 用户已填写真实内容(`paths/knowledge-path.md` 必须至少 1 个真实路径)
- [ ] 如生成 `config-used.md`,已明确标注为配置使用记录 / ADR,而非配置输入
- [ ] `setup-check.py --strict <project>` 通过(warning 可接受)
- [ ] 已提交到 git(可选,但建议)

## 反模式

- ❌ 4 个 paths/*.md 留 TBD / placeholder — 必须填真实路径,`setup-check.py --strict` 必过
- ❌ knowledge-path 写"待补充" — 必须至少 1 个真实可访问路径,否则字段对齐时无据可查
- ❌ compliance-path 不标 `mode` — 必须 `mode=gsp` / `mode=hipaa` / `mode=none` 选一
- ❌ tech-stack-path 不标 Target_DB — 必须标 `oracle` / `postgresql` / `mysql` / `firestore` 等,否则 SQL 方言检查失据
- ❌ `config-used.md` 写成配置文件 — 实际是 ADR / 配置使用记录,不参与加载,严禁误用
- ❌ 把项目级 `paths/*.md` 复制到 skill 内 — skill 级是 fallback,项目级才是真实配置,优先级不同
- ❌ 混用 legacy 项目根 + canonical paths/ — 选一种;legacy 项目可逐步迁移到 paths/ 并删除根目录旧文件
