---
name: ai-collab-system-bootstrap
description: 把「AI 协作文档体系」（AGENTS.md 入口 + .agents 规则/工作流/技能/决策记忆 + doc 分层文档 + 机器校验闸门）落地的完整方法论与可复制模板。当用户要求为新项目搭建 AI 协作体系、初始化 AGENTS.md 与 .agents 规则工作流、生成 doc 文档骨架、或把某项目的协作规范沉淀复制到新项目时使用。不用于普通编码、单次文档撰写或纯代码审查。
---

# AI 协作体系搭建（Bootstrap）

把一套已验证的「人机共读」AI 协作文档体系落地到目标项目。适用三种场景：**新项目从零搭建** / **存量项目补齐** / **把 A 项目的规范移植到 B 项目**。

体系原型来自 `cleancode-sast-web`（SAST 前端 · Vue3 + TS）。与技术栈无关的部分已抽成可直接复制的模板，栈相关部分用占位符参数化。

> **`assets/` 的定位**：其中的文件是**供复制到目标项目**的模板，不是给本 skill 自己用的资料；**不要**把 `assets/` 整包拷进目标项目根目录，要按 Phase 2/3/4 逐项复制并改名、替换占位符。

## 一、体系模型（先建立整体认知）

七层结构，**入口只做导航，内容各归其位，闸门可机器校验**：

| 层 | 载体 | 定位 | 维护者 |
| --- | --- | --- | --- |
| L0 入口 | `AGENTS.md` | 跨工具通用入口；只放导航表 + 红线速查 + 流程索引 | 人工 |
| L1 规则 | `.agents/rules/*.md` | 行为约束与硬闸门；带 `alwaysApply` frontmatter | 人工 + LLM 提议 |
| L2 工作流 | `.agents/workflows/*.md` | 按意图路由的多步骤流程（怎么做） | 人工 |
| L3 技能 | `.agents/skills/` | 仅放**可跨项目复用**的通用能力（含第三方开源 skill） | 人工 |
| L4 记忆 | `.agents/memory/decisions.md` | 追加式决策日志 D1…Dn，LLM 自动沉淀 | LLM 自动追加 |
| L5 项目文档 | `doc/**` | 人机共读的项目资产：业务/接口/架构/设计/计划/模板/变更 | 人工 + LLM |
| L6 机器校验 | git hook + 自定义 lint 插件 | 把「可机械判定」的约定从提示硬化成拦截 | 人工 |

**放置三问**（决定任何一份内容放哪儿，这是体系最容易走形的点）：

1. 是**跨项目可复用的方法论/工具能力**吗？→ `.agents/skills/`（副本可直接拷到别的项目）
2. 是**本项目专属的约束、闸门、约定**吗？→ `.agents/rules/`
3. 是**项目事实**（业务、接口、架构、设计、计划、模板、变更记录）吗？→ `doc/`

> 反面案例：把「本项目设计 token 对照表」放进 skills（应为 rules）；把「业务域知识」放进 `.agents/skills/business/`（应为 `doc/business/`）；把代码骨架模板放进 `.agents/templates/`（应为 `doc/templates/`）。

### 单一事实来源（避免同一内容多处维护）

| 主题 | 唯一权威处 | 其它位置只允许 |
| --- | --- | --- |
| 七层模型 / 放置原则 | [references/architecture.md](references/architecture.md) | 本文件 §一 保留速览表 |
| 规则写法与分类 | [references/rule-catalog.md](references/rule-catalog.md) | 不重述 |
| 意图路由表 + 各工作流步骤 | `assets/workflows/` + `assets/rules/workflow-guide.md` | `AGENTS.md` 模板保留**索引表**（入口职责，允许列「请求类型→工作流」但不再抄步骤）；references 只讲原则 |
| 三层文档结构 | `assets/doc/templates/change/` + `assets/rules/spec-first.md` | 不重述 |

## 二、搭建流程

### Phase 0 · 侦察目标项目（必做，不要跳过）

先摸清事实，再决定生成什么。至少确认：

```bash
ls -a                                    # 是否已有 AGENTS.md / CLAUDE.md / .cursorrules / .agents / doc
cat package.json 2>/dev/null | head -40  # 技术栈、脚本命令（type-check / lint / test / build）
ls .husky .github/workflows 2>/dev/null  # 现有钩子与 CI
find . -maxdepth 2 -name "*.md" -not -path "./node_modules/*" | head -30
git log --oneline -20                    # 提交信息风格（是否有 Conventional Commits / issue 号约定）
```

产出：**技术栈清单 + 现有命令清单 + 已有规范文件清单 + 缺口清单**。

### Phase 0.5 · 冲突与幂等策略（存量/移植项目必做）

**默认不覆盖任何已存在文件。** 逐项按以下顺序处理：

| 情况 | 处理方式 |
| --- | --- |
| 目标文件不存在 | 直接复制 |
| 目标文件已存在且内容相同 | 跳过，不重复写 |
| 目标文件已存在且内容不同 | **停下**，向用户展示 diff 摘要与建议（保留现有 / 合并 / 覆盖），由用户决定 |
| `.agents/memory/decisions.md` 已存在 | **绝不覆盖**，只在其末尾追加一条注入记录（见下） |
| `AGENTS.md` 已存在 | 不覆盖，改为产出「待合并片段」并逐节说明插入位置 |

**注入记录**：首次注入后，在 `decisions.md` 末尾追加一条，天然留下版本与时间痕迹：

```markdown
## D1 · AI 协作体系由 ai-collab-system-bootstrap 注入

- **结论**：本项目的 `.agents/` 规则与工作流由 ai-collab-system-bootstrap v1.0 于 <YYYY-MM-DD> 生成，后续按需本地演进。
- **理由**：保留来源与初始版本，便于回溯体系来源与后续同步。
- **日期**：<YYYY-MM>
```

### Phase 1 · 访谈（1~2 轮问全，别挤牙膏）

单轮提问最多 4 项，因此拆成 **1~2 轮**（优先第 1 轮问 1~4 项，剩余第 2 轮补齐）。缺一不可：

| # | 要确认的 | 影响 |
| --- | --- | --- |
| 1 | 项目类型与一句话定位 | AGENTS.md 第一节 |
| 2 | 技术栈（框架/语言/UI 库/状态管理/测试） | AGENTS.md 第二节、rules 内容 |
| 3 | 包管理器与关键命令（type-check / lint / test / build） | 所有 workflow 的验证步骤、verification 规则 |
| 4 | 复杂需求是否需要**先出方案等确认** | 是否启用 spec-first 闸门（默认启用） |
| 5 | 是否需要多语言（i18n） | 是否生成 i18n 规则 |
| 6 | 提交信息规范（Conventional Commits？语言？change-id？） | git-commit 规则 + 机器校验 |
| 7 | 是否需要「机器校验硬化」 | Phase 5 是否执行 |

### Phase 2 · 生成 `.agents/`（规则 + 工作流 + 决策记忆）

按 Phase 0.5 的幂等规则复制，然后替换占位符（见第三节）。

**必选的 5 个闸门规则**（体系骨架，务必都装）：

| 模板 | 作用 | 不装的后果 |
| --- | --- | --- |
| `assets/rules/spec-first.md` | 复杂需求先出三层文档、停下等确认，未确认禁改源码 | AI 先动手再确认，漏改、返工 |
| `assets/rules/workflow-guide.md` | 意图→工作流决策表；一致性由表保证而非 AI 自觉 | 不同场景混着来 |
| `assets/rules/verification.md` | 完工前自检 + 测试豁免条款 + **输出留痕** | 凭「看起来对」宣布完成 |
| `assets/rules/memory.md` | 决策自动追加 `decisions.md` + 复盘三问 | 决策反复讨论、教训不落库 |
| `assets/rules/project_rules.md` | 指向代码规范总纲 skill 的强制引用 | 生成代码无统一规范来源 |

**按需选择**：`git-commit-message.md`（默认装）、`api-convention.md`（有独立 API 层的项目）、`i18n.md`（多语言项目）。

**决策记忆**：复制 `assets/memory-decisions.md` → `.agents/memory/decisions.md`（种子含 D1–D3）；若已存在则只追加 Phase 0.5 的注入记录，不覆盖。

> 规则写作红线：① 闸门规则必须写「何时触发 + 豁免条件 + 禁令」，缺豁免会导致简单改动也被卡；② 每条规则 frontmatter 必须有 `description`（唯一例外：`scene` 型规则如 git-commit-message，可只有 `alwaysApply` + `scene`，但**建议补齐 description**）；③ 规则之间不重复描述同一件事，用链接互引。
>
> **无模板的规则**：「事实型」规则（如 `design-system.md`，`alwaysApply: false`）随项目设计体系而定，本 skill 不提供模板，按需自建，写法要点见 [references/rule-catalog.md](references/rule-catalog.md) §三。

### Phase 3 · 生成 `doc/` 骨架

建目录 + 落索引，**不做空文档凑数**（细节见 [references/doc-layers.md](references/doc-layers.md)）：

```text
doc/
├── api/<version>/        # 接口/需求事实层（长期权威，按版本归档）—— 首次有接口文档时再建
├── business/<域>.md      # 业务域知识：组件地图 / 枚举速查 / API 落点 / 已知坑
├── architecture/         # 技术架构与开发指南
├── design/               # 设计思路文档（按版本）
├── plan/                 # 改造与升级计划（带状态跟踪 + 明确不做清单）
├── templates/            # change 三层 / code 骨架 / design 模板
└── changes/<change-id>/  # 当次变更层：proposal / design / tasks
```

**必须落地的文件**（逐一复制，不要漏）：

| 来源 | 目标 | 说明 |
| --- | --- | --- |
| `assets/doc/README-business.md` | `doc/business/README.md` | 业务域索引与目录约定 |
| `assets/doc/README-changes.md` | `doc/changes/README.md` | 变更层约定与 change-id 规范 |
| `assets/doc/README-plan.md` | `doc/plan/README.md` | 计划索引 + 状态图例 + 明确不做清单 |
| `assets/doc/templates/change/*.md` | `doc/templates/change/` | 三层变更文档模板（3 个文件） |
| `assets/doc/templates/business-domain.md` | `doc/templates/business-domain.md` | 业务域文档模板（`README-business` 会引用它） |
| `assets/doc/templates/code-README.md` | `doc/templates/code/README.md` | 代码骨架目录索引（**骨架本体由目标项目按自身技术栈补齐**，本 skill 不产出代码） |

> **关于 `doc/templates/code/`**：各工作流与 `AGENTS.md` 多处引用它，但代码骨架强依赖技术栈，bootstrap 只建目录与 README 索引，**并在 README 中列出「待补骨架清单」**（列表页 / API 层 / 状态管理 / i18n 等，按项目实际裁剪）。

### Phase 4 · 生成入口 `AGENTS.md`

1. 复制 `assets/AGENTS.template.md` → 项目根 `AGENTS.md`（**必须改名，去掉 `.template`**）；
2. 替换全部占位符，逐节填写标注 `<按项目填写>` 的位置；
3. **索引一致性**：入口里引用的每个文件必须真实存在；尚未创建的文档保留在索引中但标注 **（待创建）**，并在 Phase 6 核对标记数量符合预期；
4. **与既有工具的共存**：目标项目若已有 `CLAUDE.md` / `.cursorrules` / `.github/copilot-instructions.md`，**不要**复制内容过去——在其内写一行「本项目 AI 协作约定以 `AGENTS.md` 为唯一入口」，保持单向引用，避免多份规则漂移。

> `AGENTS.template.md` 之所以不叫 `AGENTS.md`，是因为仓库内任何 `AGENTS.md` 都会被 Trae / Claude Code / Cursor 一类的约定扫描并注入上下文，模板里的占位符会被当成真实指令。

### Phase 5 · 机器校验硬化（可选，但强烈建议）

体系最大的单点脆弱性：**软约束 AI 不遵守即归零**。可机械判定的部分必须下沉为机器校验。

**通用判据**（与技术栈无关）：

1. **能用正则/文件数判断的流程约束** → 提交钩子（如「改动 ≥3 个代码文件且提交信息无 change-id → 拦截」）；
2. **能用 AST/文本模式判定的代码约定** → lint 规则（如「禁止绕过统一请求封装」「禁止内联某样板代码」）；
3. **语义条件**（涉枚举状态机、需求含糊）→ **留在规则里**，不要试图用脚本判断。

**钩子的三种落地路径**（按目标项目栈选择，不要默认 Node）：

| 路径 | 适用 | 落地方式 |
| --- | --- | --- |
| husky | Node 生态 | `.husky/commit-msg` 调脚本 |
| `core.hooksPath` | 任意栈 | 仓库内 `.githooks/` + `git config core.hooksPath .githooks`（需在 README 注明一次性配置） |
| pre-commit 框架 | Python / 多语言 | `.pre-commit-config.yaml` 挂 local hook |

`assets/scripts/check-spec-first.mjs` 是**参考实现**（Node；改 `EXCLUDE` 列表即可适配）。非 Node 项目请按上表用等价脚本重写同一条判据。

> **不在本 skill 交付范围**：自定义 lint 插件（AST 规则）的骨架。需要时按目标项目 lint 工具的插件机制自行实现，并在 `AGENTS.md` 规则表中登记。

### Phase 6 · 自检（交付前逐条过）

- [ ] `.agents/rules/` 至少含 5 个闸门规则，且每条都有 `alwaysApply`；`description` 无缺失（`scene` 型例外需显式说明）
- [ ] `.agents/workflows/` 4 件套齐全，命令占位符已替换为项目真实命令
- [ ] `.agents/memory/decisions.md` 已就位（或已追加注入记录）
- [ ] `AGENTS.md` 的每个索引项**要么文件存在、要么显式标注（待创建）**——无死链
- [ ] `AGENTS.md` 中声明的技能，在 `.agents/skills/` 下都有对应文件
- [ ] `doc/` 六个索引/模板文件全部落地（见 Phase 3 表），`doc/templates/code/README.md` 已列出待补骨架清单
- [ ] **占位符零残留**：`grep -rn "{{" <目标项目>` 必须为空；尖括号标记按第四节判据逐处目视（`<X>` 在「实例文档」中须替换，在「命名模式说明」中应保留）
- [ ] 若启用机器校验：钩子已生效（用一次真实提交验证）
- [ ] 与既有 AI 工具文件（`CLAUDE.md` 等）为单向引用，**无内容复制**
- [ ] 向用户输出「生成了什么 / 放在哪 / 被跳过的冲突项 / 下一步建议」

## 三、占位符与标记约定

### 两种语法（语义不同，不要混用）

| 语法 | 含义 | 校验方式 |
| --- | --- | --- |
| `{{NAME}}` | **bootstrap 必须替换**的参数 | 机器可查：`grep "{{"` 必须为空 |
| `<文字>` | **人工标记**：实例文档中待填写的内容（如 `<覆盖内容>`）或命名模式说明（如 `doc/business/<域>.md`） | 人工判断：前者须替换，后者须保留 |

### 占位符清单（`{{...}}`，共 16 个）

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `{{PROJECT_NAME}}` | 项目名 | `cleancode-sast-web` |
| `{{PROJECT_DESC}}` | 一句话定位 | `SAST 平台的 Web 前端` |
| `{{STACK}}` | 技术栈关键项 | `TypeScript + Vue 3 + Vite + Pinia` |
| `{{PKG_MANAGER}}` | 包管理器 | `pnpm` / `npm` / `cargo` / `go` |
| `{{INSTALL_CMD}}` | 安装依赖 | `pnpm install` |
| `{{DEV_CMD}}` | 启动开发 | `pnpm dev` |
| `{{BUILD_CMD}}` | 构建 | `pnpm build` |
| `{{TYPE_CHECK_CMD}}` | 类型检查（无则删除该项） | `pnpm type-check` |
| `{{LINT_CMD}}` | Lint 命令 | `pnpm lint` |
| `{{TEST_CMD}}` | 测试命令 | `pnpm vitest run` |
| `{{SRC_DIR}}` | 业务源码目录（闸门保护对象） | `src/` / `apps/` / `internal/` |
| `{{API_DIR}}` | API 层目录 | `src/api/` |
| `{{FETCH_CLIENT}}` | 统一请求客户端名 | `fetchClient` |
| `{{LOCALE_DIR}}` | 多语言文案目录 | `src/locale/` |
| `{{DOMAIN_LIST}}` | 业务域清单 | `dashboard / project / rule / system` |
| `{{CHANGE_ID_FORMAT}}` | change-id 格式 | `YYYYMMDD-<kebab主题>` |

> **没有对应能力的项直接删除**，不要留空占位符（例如无类型检查的后端项目就把 type-check 从验证步骤去掉）。删掉后同步检查 `verification.md` 与各 workflow 的验证步骤，保持自洽。

## 四、红线

- **不要**把项目事实（业务知识/接口/设计 token）塞进 `.agents/skills/`；skills 只放跨项目可复用能力；
- **不要**在未确认的情况下直接改目标项目的 `{{SRC_DIR}}`——本流程只产出协作文档骨架，代码实现走目标项目自己的 workflow；
- **不要**覆盖目标项目已存在的同名文件与 `decisions.md`（Phase 0.5）；
- **不要**生成空目录与空文档凑数，没内容就不建（未建项在索引中标注「待创建」）；
- **不要**让 `AGENTS.md` 变成大杂烩：超过 ~250 行就该外链；
- **不要**复制原型项目的技术栈细节（antd/vxe-table/具体 token）到异栈项目，只取方法论。

## 五、来源、版本与同步

- **来源**：从原型项目 `cleancode-sast-web` 的 `.agents/` + `doc/` 体系抽取，抽取日期 2026-09-16；方法论部分对应其决策记录 D1–D15。
- **当前版本**：v1.1（v1.0 首发 → v1.1 修复死链/孤儿模板/占位符体系，补幂等策略与钩子泛化）。
- **与原型的关系**：模板中的命令、目录、i18n/API 细节均为**占位符化改写**，与原型文件存在有意差异（原型专属条目如 `ui/`、`.gitlab-ci.yml` 等已泛化为通用条目），**这不是漂移**。
- **同步**：原型项目新增可迁移决策（D-n）或流程变更时，评估是否回流到本 skill；回流时更新本节的版本号与日期。

## 六、参考

| 文件 | 内容 |
| --- | --- |
| [references/architecture.md](references/architecture.md) | 七层模型详解、放置原则、体系演进教训（含 D1–D15 决策精华） |
| [references/rule-catalog.md](references/rule-catalog.md) | 规则分类学、frontmatter 契约、9 条规则写法要点、规则写作红线 |
| [references/workflow-catalog.md](references/workflow-catalog.md) | 意图路由原则、4 条工作流的闸门要点、新增工作流的做法 |
| [references/doc-layers.md](references/doc-layers.md) | `doc/` 七层详解、命名与生命周期、文档流转规则、索引维护 |
| `assets/` | 可复制模板：`AGENTS.template.md` / `rules/` / `workflows/` / `doc/` 索引与模板 / `memory-decisions.md` / `scripts/check-spec-first.mjs`（参考实现） |
