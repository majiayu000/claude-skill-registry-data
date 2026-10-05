---
name: cumcm-code-writer
description: 数学建模竞赛代码编写（CUMCM/研赛/美赛/校赛/自定义均可）：用户给出“数学模型＋采用算法＋模型框架（可选赛题原文与论文提纲）”后，技能先做硬门禁——确认数据是否齐全、本机 Python/MATLAB 与依赖是否可用，缺料缺工具就出《待补清单》并停下；门禁通过才按赛题小问编写竞赛可读风格的代码，固定随机种子，跑三轮自测（跑通／数值与算法正确性／多种子稳定性与论文口径一致），最后生成两份交付物：①符合国赛附录要求的《附录》（支撑材料文件列表＋全部完整源码，逐文件哈希校对）②《结果文档》（逐问结果表＋严谨而具创意的可视化＋运行说明与环境快照）。用于“帮我写这道题的代码／按这个模型和算法实现／生成附录和结果文档”等场景。不写论文正文，不给奖项位次。
---

# 数模代码编写 Skill

> 定位：这是**写作向**技能——输入是模型与算法约定，输出是可运行代码与两份提交级文档。查代码用 `代码编写评价/`（cumcm-code-reviewer），两者不要混用。
> 依据：`references/`（风格与规范）＋ `references/algorithm_library/`（精选参考实现）＋ `references/official/`（国赛 2026 格式规范的附录与支撑材料条款）。
> 边界：只写代码与两份文档，不写论文正文，不给奖项位次、不给分数。

## 何时使用

- 用户给出模型、算法或框架，要求“按这个思路写代码”“把这题实现出来”“出附录和结果”。
- 用户提供了赛题并用代码求解，需要交付可运行程序与结果材料。

不适用：只想评价已有代码（转 `代码编写评价`）；只想评论文（转 `数学模型评价`）。

## 输入要求

必给：

1. **模型与算法**：这一问要建什么模型、用什么算法或求解器。
2. **模型框架**：变量与符号、目标函数、约束、参数含义与单位；有公式就给公式。
3. **数据**：需要数据的题目必须提供文件（CSV/XLSX/JSON/txt/mat），并说明每列含义与单位；确实不需要数据的要明说“无需数据”。

可选：赛题原文或年份题号（用于对齐小问与红线）、论文提纲或已有草稿（用于对齐符号与结果口径）、指定语言（默认 Python，备选 MATLAB）。

## 硬门禁（未通过不写代码）

按序检查 G0→G3，任一未过即输出《待补清单》并停止，清单里写清缺什么、怎么补、补齐后能继续到哪一步。

| 编号 | 门禁 | 通过标准 | 检查手段 |
|---|---|---|---|
| G0 | 题意与算法自洽 | 模型/算法/框架三项齐全；所选算法满足成立条件（如 GM(1,1) 需小样本单调趋势、AHP 需一致性检验可行） | 对照 `references/算法-模型对照表.md` |
| G1 | 数据齐全可用 | 文件可读、编码与分隔符可解析、列名与单位明确、缺失与异常已说明 | `scripts/check_data.py`，产出 `数据说明.md` |
| G2 | 工具齐全 | **Python（含 numpy、matplotlib）为强制项**——交付图件必须由 Python 生成；有 MATLAB 时其工具箱也要齐；中文字体可用；磁盘余量足够 | `scripts/check_env.py`；缺失时 `scripts/bootstrap_env.py` |
| G3 | 参考实现命中 | 命中对应算法且状态可用，并产出 `work/<项目名>/参考依据.md`：写出引用的模板 id、参考了哪部分、偏离与理由 | 查 manifest 与 `index.md`；由 `scripts/check_gates.py` 校验 id 真实性 |

工具缺失的处理：Python 依赖可在**工作区虚拟环境** `工具/code_env/` 内自动安装（需联网）；**Python 本身缺失时不降级、不出图，直接请用户安装**；MATLAB 或工具箱缺失只报告并给出替代方案，不静默降级。

## 五阶段流程

1. **拆题冻结**：把赛题或用户描述切成小问，逐问写清“建什么模型、用什么算法、输出什么数值/表/图”。冻结后不在中途增删小问。
2. **数据与环境**：跑 G1/G2，产出 `work/<项目名>/数据说明.md` 与 `work/<项目名>/环境快照.md`；缺失即停。
3. **参考命中与写码**：按 G3 命中算法模板，读懂接口约定与常见坑，再按 `references/代码风格规范_竞赛可读版.md` 写代码：小问分脚本＋公共模块＋总运行入口，公式编号写进注释，固定随机种子。同时写 `work/<项目名>/参考依据.md`（模板见 `templates/参考依据模板.md`），记录每个小问引用了哪个模板、沿用了什么、按题目改了什么、为什么改。
4. **三轮自测**：`scripts/selftest.py` 依次跑三轮并把输出写进 `work/<项目名>/自测记录.md`：
   - 第一轮：语法与依赖、端到端跑通、输入输出形状与量纲。
   - 第二轮：数值与算法正确性对照（小规模暴力解、解析解或成熟库实现三者互证），边界与极端输入。
   - 第三轮：多种子稳定性、关键参数敏感性、结果与论文口径（若给了提纲/草稿）一致性。
   任一轮失败就回到写码阶段修，修完重跑该轮，不允许带着失败结论进入交付。第二轮不得空转：校验脚本必须打印 `CHECK-SUMMARY total=.. passed=.. baselines=..`，且 total≥3、baselines≥1（baselines 指由另一条代码路径算出的基准值）；缺校验机制或校验强度不足一律判未通过并阻塞交付，只有用户明示豁免（`--allow-missing-verify`）才放行，且必须在结果文档的限制说明里写明。
5. **交付**：写码时同步登记 `work/<项目名>/论文口径.md`（模板见 `templates/论文口径模板.md`），把论文里写下的关键数值逐条列出；随后跑 `scripts/check_gates.py --project <项目名>`，七项门禁（数据说明／环境快照／参考依据／三轮自测／代码体检／图件合规／论文口径）全绿才允许生成文档；然后 `scripts/build_appendix.py` 生成附录（支撑材料文件列表＋运行说明＋全部完整源码＋数据说明＋参考依据与偏离说明，逐文件哈希校对），`scripts/build_results_doc.py` 生成结果文档（逐问结果表＋图＋运行说明＋环境快照）。缺 `参考依据.md` 时附录脚本直接报错不出文档。默认同时给 Markdown 源与 DOCX 成品。

## 代码风格要点

- 竞赛可读优先：一个问一个脚本，公共函数抽到 `common/`，根目录一个 `run_all.py` 或 `main.m` 顺序调用；附录里能直接读懂。
- 注释与 docstring 只写两块：公式/符号与代码的对应、非显然的算法步骤。不写“初始化变量”“开始循环”这类废话。
- **禁止在注释/docstring 里留流程与修订痕迹**（`S3R`/`S4B`/`P1-x`/`work/...`/`_s3r*`/`方案 §x`/`假设 Ax`/“等价性对照”“开箱复现”“性能改造”等）——附录要像正常竞赛代码，不能暴露流水线与修订过程；改完代码若注释提到旧文件名或旧路径，一并清掉。
- 随机算法固定种子并记录；迭代类算法输出收敛过程；结果文件带表头与单位。
- 数据校验与异常处理保留最小必要部分，不写整屏 `try/except` 包装。
- 不为了“显得专业”引入用不到的抽象层、设计模式或第三方库。

完整规则见 `references/代码风格规范_竞赛可读版.md` 与 `references/低AI味代码规范.md`。

## 性能与效率（硬规则：能快必须快，且不许改口径）

1. **时间预算**：全流程（含校验与出图）默认目标 **≤120 s**；超过就在结果文档《运行说明》里写清每阶段耗时与优化方案。交付前记录一次基准运行时间。
2. **线性代数不许手写循环**：时间步里的隐式求解一律用 `scipy.linalg.solve_banded` / `scipy.sparse.linalg` / `numpy.linalg.solve`；**禁止**在 Python `for` 里手写追赶法（网格数 ≥10 时）。实测：20 格追赶法每步 ~2.4 ms，换 banded 求解可快 2–4 倍。
3. **每步只做一次向量化**：物性、界面系数、装配用 numpy 数组一次算完；不在不动点迭代里重复构造常量数组或重复 `np.exp` 全场。
4. **大结果文件用 xlsxwriter**：行数 >1 万的表用 `xlsxwriter`（`constant_memory=True` + `write_row`）或 `pandas.ExcelWriter(engine="xlsxwriter")`，禁止逐格写；**写出的数值必须是数字类型**，工作表名/表头/A 列/列序/末列名一律不变（实测 59370×22×2：openpyxl 13.0 s → xlsxwriter 9.7 s）。
5. **积分步长 ≠ 输出步长**：模板要求"每 1 s 输出"不等于必须 1 s 积分。允许内部用较粗步长积分、再插值到输出网格，但**必须先做 ≥3 档步长的收敛验证**（关键量偏差 ≤0.1%，必要时更严），并在结果文档写明口径；不通过就退回 1 s 积分。
6. **独立小问并行**：各问互不依赖时用进程级并行（`ProcessPoolExecutor` 或并行脚本），保留 `--jobs` 开关；并行不得改变随机种子与数值结果。
7. **增量重跑**：入口脚本支持 `--only q3` 之类的子集开关与结果缓存（按输入哈希跳过未变体），改一处不重跑全部。
8. **性能日志**：每个小问、每轮校验打印耗时（`[time] q3 solver 12.3 s`），汇总进《运行说明》。
9. **性能回归**：任何改动若使整轮运行时间上升 >30%，必须在修订记录里说明原因与取舍。

## 可视化要求

**所有交付图件必须由 Python + matplotlib 生成**，MATLAB 只负责计算，不允许用 MATLAB 出交付图；本机没有可用 Python 时停止并请用户安装（Python 3.10+，<https://www.python.org/downloads/>），再跑 `scripts/bootstrap_env.py --install-optional`。
统一 300dpi、色盲友好配色、中文字体显式设置、坐标轴带单位、图号与题号对应；每问除规范图外再给一张信息量更高的组合主图（多子图、带注释或不确定性区间）。绘图脚本与数据分离，保证重跑可复现。细则见 `references/可视化规范.md`，检查由 `scripts/check_figures.py` 执行。

## 输出与命名

默认写 `代码编写/output/<项目名>/`，绝不在 `数据集/` 下产生任何文件。
技能被安装到全局（`~/.codex/skills/`）后，可用环境变量 `CUMCM_CODE_PROJECT` 指定项目根目录，产物会写到 `<该目录>/output/` 与 `<该目录>/work/`，避免把结果堆在技能目录里。

```text
output/<项目名>/
├── code/                     # 可运行代码（含数据接口说明）
├── figures/                  # 每图 PNG(300dpi) + PDF(矢量)
├── tables/                   # 逐问结果表（CSV + Markdown）
├── <项目名>_附录.md / .docx    # 附录：支撑材料列表 + 全部源码
├── <项目名>_结果文档.md / .docx  # 结果：逐问结论、图表、运行说明
└── 运行说明.md                # 环境、命令、产物清单
```

支撑材料只生成**文件列表**（写在附录），不打包压缩包。

## 阅读预算

- 算法库有 90 个算法、180 个模板：**只读命中的 1–3 个 `meta.yaml` 与对应 `python/main.py`／`matlab/main.m`**，不要通读 `algorithm_library/`。
- 需要按题型找算法时读 `references/算法-模型对照表.md` 或 `index.md` 的目录表，再定位到具体模板。
- 方法公式口径以 `references/来源与方法依据.md` 登记的权威来源为准，摘要片段在 `references/_methods/<id>.md`。
- 参考库依赖与许可看 `manifest.csv`，外部下载记录看 `manifest_sources.csv`。

## 边界与规则

- 只写代码与两份文档；论文正文、摘要、奖项位次不在职责内。
- 结果必须来自真实运行；没跑通就写“未跑通”并说明卡在哪，不虚构数值。
- 参考库只复制宽松许可实现并登记来源；生成用户代码时按公式自行重写，不整段搬运。
- 数据与产物不写入 `数据集/`；用户数据只做只读使用，不改变原始文件。
- 涉密或未授权数据不复制进参考库与附录样例。

## references 索引

- `references/算法-模型对照表.md`：题型 ↔ 算法 ↔ 成立条件 ↔ 必需库 ↔ 常见误用（拆题与选型时必读）。
- `references/代码风格规范_竞赛可读版.md`：文件组织、命名、注释、随机性、结果输出规范（写码前必读）。
- `references/低AI味代码规范.md`：反 AI 味的正反例与自检清单。
- `references/数据交接规范.md`：数据提交清单、数据说明模板、缺失与异常处理口径。
- `references/环境与工具检查规范.md`：工具探测项、虚拟环境策略、缺失时的报告口径。
- `references/可视化规范.md`：字体、配色、图种选择、创意主图与自检清单。
- `references/附录与结果文档规范.md`：两份文档的结构、合规要求与命名。
- `references/official/`：国赛 2026 格式规范中附录与支撑材料条款原文。
- `references/algorithm_library/`：精选参考实现，`manifest.csv` 为索引，`index.md` 为可读目录。

## scripts 索引

| 脚本 | 作用 | 典型调用 |
|---|---|---|
| `check_env.py` | 探测 Python/包/MATLAB/工具箱/字体/磁盘 | `python check_env.py --need numpy,scipy,matplotlib` |
| `bootstrap_env.py` | 在工作区建 `工具/code_env` 并安装缺失包 | `python bootstrap_env.py --install` |
| `check_data.py` | 数据可读性、列名、缺失、异常、单位表生成 | `python check_data.py <数据路径> --out 数据说明.md` |
| `build_library.py` | 由注册表生成算法库的 meta/index/manifest 并烟测 | `python build_library.py --smoke` |
| `fetch_reference_library.py` | 按清单下载宽松许可参考实现并登记来源 | `python fetch_reference_library.py --plan` |
| `selftest.py` | 三轮自测驱动与留痕；第二轮强制 CHECK-SUMMARY 与独立基准 | `python selftest.py --project <项目名>` |
| `check_gates.py` | 交付门禁：数据说明/环境快照/参考依据/三轮自测/代码体检/图件合规/论文口径 七项全绿才放行 | `python check_gates.py --project <项目名>` |
| `build_appendix.py` | 生成附录并逐文件哈希校对；缺参考依据直接报错 | `python build_appendix.py --project <项目名>` |
| `build_results_doc.py` | 由结果表与图生成结果文档 | `python build_results_doc.py --project <项目名>` |
| `lint_code.py` | 机械检查：吞异常、绝对路径、未固定种子、空话输出、占位命名、重复注释 | `python lint_code.py --project <项目名>` |
| `check_figures.py` | 图件合规：300dpi、PNG/PDF 成对、宽度、轴标签与命名 | `python check_figures.py --project <项目名>` |
| `check_paper_consistency.py` | 论文口径核对：论文声明数值 vs 结果表 | `python check_paper_consistency.py --project <项目名>` |
| `collect_method_references.py` | 抓取并登记算法方法的权威依据 | `python collect_method_references.py --fetch` |
| `matlab_smoke.m` | 单会话批量烟测全部 MATLAB 模板 | `matlab -batch "matlab_smoke"` |
| `install_skill.ps1` | 把本技能安装到 `~/.codex/skills`（需你手动运行） | `powershell -File install_skill.ps1` |
