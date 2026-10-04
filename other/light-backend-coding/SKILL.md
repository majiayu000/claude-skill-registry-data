---
name: light-backend-coding
description: 后端代码编写、逻辑强、安全性高、可读性好、版本控制、代码审查。当任务需要写实验代码、模型代码、数据处理代码、可视化代码、后端接口或系统逻辑时使用。要求逻辑清晰、安全、可读、可维护、便于复现/扩展/部署。支持 Git 版本管理、代码审查、注释规范、README、依赖管理、环境配置、运行说明与项目结构整理。
user-invocable: false
---

# 后端代码编写与审查

## 写代码前
读现有代码，匹配项目的风格、约定与依赖库，不擅自引入新框架(CONVENTIONS)。明确输入输出、边界条件、复现要求(种子/版本)。

## 代码质量标准
- **逻辑清晰**：单一职责、小函数、清楚的数据流。
- **安全**：参数化查询、输入校验、异常处理；不硬编码密钥(走环境变量/配置)；不回显敏感值(a10)。
- **可读**：命名达意、注释解释"为什么"而非"是什么"、与周围代码同密度。
- **可维护/可扩展**：低耦合、配置化(Hydra)、避免过度工程。
- **可复现**：固定随机种子、锁依赖版本、记录环境、确定性数据划分。

## 工程实践
- **版本控制**：Git；功能分支不直接推 main；有意义的提交信息；仅用户明确要求才提交/推送。
- **依赖/环境**：
  - uv（推荐，Rust 实现快 10-100x）：`uv init` → `uv add <pkg>` → `uv lock`/`uv sync`(按 `uv.lock` 精确复现) → `uv run`；`uv python pin 3.11` 锁 Python 版本。
  - Poetry：`poetry add` → `poetry install`(按 `poetry.lock`)；依赖放 PEP 621 `[project.dependencies]`，dev 依赖入 `[tool.poetry.group.dev]`；CI 固定 Poetry 版本。
  - 始终提交 lock 文件，CI 用 `uv sync`/`poetry install` 还原确定性环境。
- **测试**：pytest——文件 `test_*.py`、函数 `test_*` 自动发现，纯 `assert`；`@pytest.fixture`(scope function/module/session) 做依赖注入，`@pytest.mark.parametrize` 跑多组输入，共享 fixture 放 `conftest.py`。新功能/修 bug 先配测试，改完跑 `pytest -x` 验证。覆盖率 `pytest --cov=pkg --cov-report=term-missing`，CI 出 `--cov-report=xml`。
- **质量门**：
  - Ruff：`[tool.ruff.lint]` 用 `select`/`extend-select`(如加 `B`)/`ignore`(如 `E501`)；`[tool.ruff]` 设 `line-length`/`target-version`；CI 分别跑 `ruff check .` 与 `ruff format --check .`(linter 与 formatter 是两个命令)。
  - **静态类型检查（mypy / pyright）**：按项目性质选档——**新项目/科研代码用 pyright basic（或 mypy 基础档，仅检明显类型错、不强制全注解）起步**，**库代码/对外 API 用 `mypy --strict`（要求全量注解，最严）**。CI 加一步 `mypy src`；第三方无 stub 时 `ignore_missing_imports`（库代码按模块 override 收紧），测试代码可 `ignore_errors`。scaffold 的 `pyproject.toml` 已带 `[tool.mypy]` 基础配置 + strict 切换注释，与 uv 路线不冲突。
  - pre-commit：`.pre-commit-config.yaml` 的 `repos` 用 `rev` 锁版本(tag/SHA，勿用浮动分支)；接 `astral-sh/ruff-pre-commit` 的 `ruff`(`args:[--fix]`)+`ruff-format`；`pre-commit install` 启用，CI 跑 `pre-commit run --all-files`。
  - SonarQube(必要时)：`sonar-project.properties` 设 `sonar.sources`/`sonar.tests`/`sonar.python.coverage.reportPaths=coverage.xml`；Quality Gate 卡阈值；token 走 secrets。**仅团队/长期维护/有合规要求时才上**——单人脚本、一次性实验靠本地 ruff+mypy+pytest 即够，别为重型基建徒增维护面(YAGNI)；适用边界详见 `references.md` SonarQube 节。
- **CI**：GitHub Actions 放 `.github/workflows/*.yml`；`actions/checkout@v6` + `actions/setup-python@v6`(`cache:"pip"`，缓存默认关须显式开)；`strategy.matrix.python-version` 多版本并行；典型流水线 checkout → 装依赖 → `ruff check` → `pytest`；secrets 用 `${{ secrets.X }}` 注入。
- **维护元规则（仓库有清单/脚本时）**：资产清单防漂移（manifest 按精确键校验防漏登、AST 查脚本入口、warning 升 hard gate）与脚本自测入口治理（显式 `--selftest`、离线合成断言、可选依赖"可用则验证不可用则降级"）两套元规则细节见 `references/asset_manifest_governance.md` 与 `references/skill_selftest_ci.md`。
- **文档**：README(安装/运行/复现命令)、关键模块注释、运行说明。

## 调试与审查
四套方法（动手前先定位根因，不在症状处打补丁）——细节与展开见 `references/code_examples.md`「调试与审查四法」：
- **系统化调试**：逐字读错误→稳定复现→查最近改动→边界埋点定位坏在哪层→反向追数据流到源头修；一次只改一个变量；连修 3 次仍失败→停手质疑架构。
- **自我代码审查**：按 Critical/Important/Minor 分级；每条建议过五查（技术正确/会否破坏/为何这么写/跨平台/上下文全）+ YAGNI；回应技术化不表演性赞同。
- **改进架构**：用"删除测试"诊断浅模块 vs 深模块，把浅模块改造成"小接口藏大实现"。
- **拆子任务/收尾分支**：隔离上下文、规格审查先于质量审查；合并→重跑测试→移 worktree→删分支，丢弃工作需显式确认。

## 安全提示
创建网络暴露的接口/服务时，若无鉴权必须主动指出安全影响(security_awareness)，不静默上线无认证服务。

## 产出
可运行代码 + 测试 + 依赖/环境说明 + README + 运行命令。结构交 a06 规整。**作 a03 实验代码阶段时的标准交接工件：`run_manifest.md`**（记录运行命令/环境/产物路径/关键指标，交 m06；命名见 CONVENTIONS §6.1）。
起步可直接复制同目录 `assets/project-scaffold/`（含 `pyproject.toml`/`.pre-commit-config.yaml`/CI/示例模块+测试 + `CODE_REVIEW_CHECKLIST.md` + `scripts/`(边界调试埋点)，版本号已实测、`pytest` 实跑通过）。
推荐 TDD(test-driven-development)：先写最小失败测试并**亲眼看它失败**(确认是功能缺失而非拼写错)→ 写最简实现转绿 → 绿灯后才重构；无失败测试不写生产代码。**最小够用 vs 过度工程、源头校验 vs 症状补丁的代码对照例见 `references/code_examples.md`。**

## 衔接
实现 m05 方案与 m02 流水线；优先复用 db03 方法卡的 `implementation_repo`（已验证的官方实现/库，如 HuggingFace Transformers、scikit-learn、xgboost/lightgbm、diffusers）而非从零造轮子；产出供 m06 分析；代码版本登记 db09；系统级设计交 a04。
- **论文复现落地**：m05「复现已有论文协议」放行的复现任务由本技能实现——按其偏差预算与复现日志格式落代码，复现日志的"逐次只改一个变量"与本技能 systematic-debugging 的假设-验证同源；复现失败的三分归因（实现差异/数据差异/原文问题）中"实现差异"是本技能可继续逼近的部分，指向"原文问题"时移交 research-ethics，勿在代码里轻率断言原文有错。

---
工具硬信息(真实端点/参数/配置/工作流)见同目录 `references.md`。
深用专题：TDD 红旗与合理化反驳表见 `references/tdd_redflags.md`；系统化调试四阶段+边界埋点见 `references/debug_protocol.md`（配套可跑模板 `assets/project-scaffold/scripts/debug_instrument.sh` 与 `boundary_trace.py`）；自审清单 `assets/project-scaffold/CODE_REVIEW_CHECKLIST.md`。
资产清单/manifest 防漂移校验模式见 `references/asset_manifest_governance.md`；技能脚本 `--selftest` 与 CI 实际执行门模式见 `references/skill_selftest_ci.md`；维护 Light 技能包时的断点恢复、质量门、入口文档防漂移与提交纪律见 `references/light_skill_pack_maintenance.md`。
