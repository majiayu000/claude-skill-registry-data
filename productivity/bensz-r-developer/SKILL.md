---
name: bensz-r-developer
description: 当主要交付物是可复用的 R 函数、稳定 API、S3/S4/R6 类或 R Package，需要设计、开发、重构或审查其接口、测试、文档、并行与性能边界时使用。分析项目中只有需要跨分析复用或形成公共 API 的组件才进入本 Skill。⚠️ 不适用：主要交付物是数据分析流程、科学结果、R Markdown 报告或仅服务当前分析的辅助函数；这些任务使用 bensz-rmd-rules。
metadata:
  author: Bensz Conan
  keywords:
    - bensz-r-developer
    - R development
    - R package
    - S3
    - S4
    - R6
    - devtools
    - roxygen2
    - parallel computing
    - Rcpp
---

# bensz-r-developer

## 目标

开发优雅、可维护且可复用的 R 软件组件：以明确的输入、返回、错误和副作用契约设计函数与公共 API，用领域对象承载真实不变量和生命周期，并以成熟工具管理文档、测试、并行和性能。

本 Skill 关注的是“R 代码怎样稳定地被调用”，而不是“某次分析怎样可靠地跑完”。触发依据是主要交付物和复用边界，不是任务里是否出现 `.R` 文件或函数：

| 场景 | 主导 Skill |
| --- | --- |
| 主要交付物是可独立测试、文档化、版本化或跨项目复用的函数、类、API、Package | `bensz-r-developer` |
| 主要交付物是数据流、统计结果、Rmd/HTML 报告、论文图表，函数只服务当前分析 | `bensz-rmd-rules` |
| 同时交付分析流水线与可复用组件 | 由主要交付物决定主 Skill；分析主导时先由 `bensz-rmd-rules` 定义组件契约，再由本 Skill 实现组件，最后回到分析流程集成验证 |

不负责单纯运行既有代码，也不把分析项目中的每个 `_functions.R` 或 helper 都泛化成 Package。若主要验收标准是科学结果正确、缓存可恢复或报告可交付，应交给 `bensz-rmd-rules`；仅在其中出现具有独立复用价值的组件时参与协作。

## 流程

### 输入

确认主要交付物、复用范围（当前分析/当前项目/跨项目/公开 Package）、任务类型（函数/脚本/Package、新建/兼容修改）、数据与公开 API、对象生命周期、返回/错误、`output.dir`/`cache.dir` 职责、R/平台/依赖/硬件/复现约束，并读取现有 `DESCRIPTION`、`NAMESPACE`、`R/`、`tests/`、`src/`、`renv.lock` 与项目指令。不得读取凭据、环境文件或无关数据。保守默认不得改变公共 API；会改变类系统、覆盖、依赖或性能语义时先声明假设。

### 执行步骤

#### 1. 盘点现状与定义契约

先判定主要验收对象：是“函数/API/Package 自身的可复用契约”，还是“分析结果、数据流与报告”。再确认目标代码是否需要独立版本、稳定公共接口、跨项目复用或独立测试；仅服务当前分析单元的 helper 即使写在 `.R` 文件中，也仍由 `bensz-rmd-rules` 管理。

确认本 Skill 应主导后，读取调用链和测试，列出不变量、I/O、错误、副作用、并行及兼容边界。已有项目保持命名、类系统和公开 API，除非用户授权迁移。混合任务记录主 Skill、组件边界与交接点，避免两个 Skill 同时改写同一层职责。

#### 2. 选择类系统并建立最小对象模型

对象确有身份、不变量、状态或多步生命周期时才建类；无状态工具保持普通函数：

- S3：轻量值对象、单分派和多数分析型 API。
- S4：需要正式 slot、严格验证、多分派或 Bioconductor 互操作。
- R6：需要引用语义、可变资源或服务式生命周期。

类 API 至少有构造器、验证器、摘要打印和泛型/方法；不要让调用方拼内部结构。详见 [references/class-api-design.md](references/class-api-design.md)。

#### 3. 实现输出与缓存契约

自动落盘显式提供 `output.dir`；重要中间产物另设 `cache.dir`，二者不得同路：

- `output.dir`：稳定、面向用户、可解释的结果和 manifest。
- `cache.dir`：按输入、参数、代码/格式版本生成身份，可删除并重建。
- `NULL`：默认不持久化；不得暗中写入工作目录。
- 覆盖：默认拒绝覆盖，只有显式 `overwrite = TRUE` 才替换已知目标。

创建父目录、原子写入、返回产物路径；缓存损坏应可重算。详见 [references/io-cache-contract.md](references/io-cache-contract.md)。

#### 4. 保留可执行手测块

在函数文档与函数定义之后、核心逻辑之前放置：

```r
# Test
if (FALSE) {
  x <- datasets::iris
  output.dir <- tempfile("r-output-")
  cache.dir <- tempfile("r-cache-")
  # 在这里构造对象、参数并逐行运行当前函数。
}
```

使用内置/最小合成数据或项目 fixture，不写私人绝对路径、凭据或大数据。手测块不能替代 `testthat`。

#### 5. 写出清晰、惯用且可维护的 R

- 明确命名、小函数、早失败、稳定返回；公开函数写完整 roxygen2。
- 避免无意义封装、深层嵌套、隐式全局状态、部分匹配和 `1:length(x)`。
- 只在 I/O、用户输入、外部系统边界防御；构造器/验证器保证内部不变量。
- 随机过程显式接收 seed；库函数不静默改变 RNG、options、工作目录或并行计划。
- `styler`/`lintr` 辅助一致性，既有风格和可读性优先。

#### 6. 设计并行与性能路径

先用基准/profiler 找热点，再依次改算法、向量化/成熟包、复制与 I/O、分块、并行，最后考虑原生代码。并行优先 `future` 或领域主流后端；Package 尊重调用方 plan，顶层用 `parallelly::availableCores()` 配 workers。管理 RNG、错误、清理、嵌套并行与内存放大；默认留一个逻辑核，aggressive 模式需用户显式要求和资源评估。详见 [references/parallel-performance.md](references/parallel-performance.md)。

#### 7. 判断是否采用 C++/原生扩展

仅当 profiler 证明热点位于紧循环、递归、数值 kernel/转换边界且现有包无解时，才引入 `Rcpp`/`cpp11`。先冻结 R 参考实现和等价测试；检查 NA/NaN、溢出、内存、线程、中断和跨平台构建。文件编排、业务判断与易变逻辑留在 R。

#### 8. 按现代 R Package 工具链工作

Package 任务读取 [references/package-workflow.md](references/package-workflow.md)：`usethis` 建结构，roxygen2 管文档/NAMESPACE，`testthat` 测试，`devtools` 执行 document/load_all/test/check。依赖写入 `DESCRIPTION`；API 变化同步示例、测试、README、CHANGELOG。

#### 9. 使用 demo 起步

`templates/demo-package/` 提供可运行 Package：S3 对象与方法、输出/缓存、手测块、future 并行和 testthat。复制后更换包名与领域语义，并运行：

```r
devtools::document("path/to/package")
devtools::test("path/to/package")
devtools::check("path/to/package", cran = FALSE)
```

#### 10. 审查并交付

检查类不变量、文件副作用、缓存失效、串/并行等价、RNG、恢复和跨平台路径；说明设计取舍、验证命令及风险。

### 输出

按规模交付可复用的 R 源码、类/泛型/方法、roxygen2、`testthat`、手测块与 demo；Package 同步 `DESCRIPTION`/`NAMESPACE`/README/CHANGELOG；性能任务附基准、等价证据与回退；摘要公开 API、副作用、依赖、验证和风险。若由分析流程发起协作，还要返回可供 `bensz-rmd-rules` 集成的调用契约和最小示例，但不接管分析编排、科学解释或报告交付。

### 输出管理

过程材料放入唯一 `.bensz-api/task-*/bensz-r-developer/{input,output,log}/`；正式源码与文档进目标项目。profile、临时编译物、R CMD check 和包归档进任务工作区或项目 `tmp/`。不得默认覆盖、删除或迁移用户文件。

### 校验

按风险选择并记录：

```r
parse(file = "R/example.R")
devtools::document()
devtools::test()
devtools::check(cran = FALSE)
lintr::lint_package()
```

确认手测块可解析且不自动执行；输出/缓存分离且缓存可重建；串/并行结果在容差内一致；seed 可复现；backend 已恢复或未修改；公开函数有文档和测试。原生扩展还需 R 等价测试与目标平台构建证据。

### 失败与恢复

- 输入/契约不清：停在设计层，列出会改变 API 的待确认项。
- 依赖缺失：报告包名、版本和复现命令；未经授权不全局安装。
- 缓存损坏：隔离单个缓存并重算，不删除最终输出或整个缓存树。
- 并行失败：保留错误和 seed，以 sequential 后端复现；不得把静默降级冒充并行成功。
- 原生构建失败：回退到已验证的 R 参考实现，保留编译日志与平台信息。
- `R CMD check` 失败：按 error/warning/note 分类修复；证据不足时不宣称 Package 可发布。

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

- 不把 `if (FALSE)` 手测块当自动测试，也不在其中保留私人绝对路径或真实敏感数据。
- 不以“榨干设备”为由默认占满 CPU/GPU；激进资源策略必须显式、可测量、可恢复。
- 不在未 profile、无参考实现或无等价测试时引入 C++。
- 不静默改变用户的工作目录、future plan、RNG、options 或包库。
