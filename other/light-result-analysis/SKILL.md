---
name: light-result-analysis
description: 对执行出来的结果、实验数据、模型输出、图表结果进行详细专业深入的分析。当用户实验跑完、需要解读数据、问"这些结果说明什么"时使用。不只描述好坏，而是解释为什么、哪些结果证明方法有效、哪些暴露问题、哪些异常需排查、哪些规律可成为论文亮点、哪些需补充实验。
---

# 结果与数据深度分析

## 分析层次（逐层深入）
1. **描述**：指标汇总、分布、与 baseline 的差距，配误差棒/置信区间。
2. **解释**：为什么是这个结果？归因到方法的哪个组件（结合消融）。
3. **诊断**：哪些结果证明创新点有效，哪些反而暴露问题或矛盾。
4. **洞察**：能成为论文亮点的规律；意外发现；可解释性证据(SHAP/特征重要性/注意力)。
5. **行动**：哪些异常需排查，哪些结论需补实验验证，哪些不能过度声称。

## 必查清单
- 显著性：**≥5 随机种子；算力受限 ≥3 且须在报告显式标注**（与 m05 实验设计同口径），报均值±标准差；两组用 Welch t（不假设等方差）、非正态用 Mann-Whitney U、多组用 ANOVA+Tukey、比例用 two-proportion z-test。p 值 + 效应量(Cohen's d) + 置信区间三件套，别只报 p。多比较用 BH-FDR 校正（`multipletests(method="fdr_bh")`）。
- **配对设计识别（先判再选检验）**：方法是否在**同一组单元**（同一批种子/CV 折/测试样本）上评测？是 → 用**配对 t / Wilcoxon 符号秩**（功效更高，扣除单元间方差），不是独立 Welch/Mann-Whitney；误当独立会低估显著性。`analyze_results.py --paired-by seed` 自动按共享列对齐配对，配对效应量用 d_z、差值 CI 用 bootstrap（详见 references「配对设计识别」节）。
- **切片分析（防聚合指标盲区）**：整体指标会掩盖子群失败（整体 85% 但某类别只 50%）。按类别/域/难度/敏感属性/时间段切片，逐切片复算指标**并带样本量 n**，对照整体找异常切片；多切片比较过 BH-FDR；小 n 切片禁下强结论。**已脚本化**：`analyze_results.py --slice-by <col>` 对每个切片值复算同套 EDA+检验+效应量+FDR，自动标注小 n 切片为"待核查"（公平性维度的敏感属性可作 slice_by，关联 a10；详见 references「切片分析协议」节）。
- 一致性：跨数据集/跨设置是否稳定？哪里反常？
- 消融自洽：移除组件性能确实下降？方向对不对？用 anova_lm 或回归系数看组件贡献是否显著。
- 失败案例：错例分析找系统性偏差；用 SHAP(beeswarm/bar) 看模型实际依赖哪些特征是否合理。
- 公平性：对比是否同设置、同算力、同数据，避免不公平比较。
- 过拟合/泄漏：train/val/test 差距是否异常；特征-标签相关过高或时间穿越要查（deepchecks data_integrity / 漂移用 Evidently DataDriftPreset）。

## 工具与具体用法
- **快速体检**：`ProfileReport(df, minimal=True).to_file(...)` 一键出分布/缺失/相关/告警；deepchecks `data_integrity().run(Dataset(df,label=...))` 查泄漏/重复/单值列。
- **统计推断**：statsmodels。回归 `smf.ols("y~x1+x2",data).fit().summary()` 给系数/p/R²/AIC（OLS 用 sm.add_constant 加截距，公式接口自动加）；方差分析 `anova_lm(model, typ=2)`；检验在 `statsmodels.stats`（ttest_ind / proportions_ztest / multipletests / het_breuschpagan）。
- **可解释性**：SHAP，见即用脚本 `scripts/explain_shap.py`（一键产 beeswarm/bar/waterfall 三图）。树模型用 `shap.TreeExplainer`（快），通用兜底 `KernelExplainer`（慢，背景集要采样）；`shap.plots.beeswarm` 看全局方向、`bar` 看重要性排序、`waterfall` 拆单样本。SHAP 反映模型非因果。
- **静态出版图**：matplotlib 面向对象接口 `fig,ax=plt.subplots(layout="constrained")`，`savefig(dpi=300,bbox_inches="tight")` 存 PDF/SVG 矢量；seaborn 轴级函数(boxplot/heatmap/barplot, barplot 默认带 95%CI 误差棒)可嵌 ax，图形级(relplot/catplot)自带分面。配色用 viridis 等色盲友好 colormap，避免 jet。**出图语言三选（Python 为主，R/MATLAB 备选）**：以本技能 `make_figs.py`（Python/matplotlib）为默认；**R 用户**可用 ggplot2（`+ theme_classic() + scale_color_viridis_d()`，拼图 patchwork，`ggsave(units="mm")` 按期刊栏宽出图）；**MATLAB 生态**（信号/控制类）用 `exportgraphics(...,ContentType="vector")` 出矢量、`tiledlayout` 组图。三者出版级矢量质量相当，按项目栈选；具体用法与栏宽规范统一见 m11(light-figure-drawing)，本技能只做"分析→出图"不重复绘图细节。
- **交互/探索图**：plotly express(`px.scatter(...,color=,facet_col=)` → `write_html`) 或 altair(`alt.Chart(df).mark_point().encode(x="a:Q",...)`)，做附录/补充材料。
- **漂移监控**：Evidently `Report(metrics=[DataDriftPreset()]).run(reference_data=ref,current_data=cur)`（API 版本敏感，先确认版本）。
- **关系分析**：networkx 算 betweenness/pagerank 中心性、louvain 社区，用于引用网/特征关系/消融依赖。
- **留痕与汇编**：Jupyter Notebook 交付前 Restart&Run All 保证可复现、`nbconvert` 出报告；多组实验汇编成站点用 Jupyter Book(`_config.yml`+`_toc.yml` → `jupyter-book build`)。

## 产出
1. 结果分析报告：每个发现配"现象→原因→证据→对论文的意义"。**标准工件：claim↔证据对应表落盘为 `claim_evidence_table.md`**（交 m07/m09 的交接工件，命名见 CONVENTIONS §6.1）——**由 `analyze_results.py --emit-claim-table` 自动生成**：每个比较(claim)连到检验/p/q(FDR)/Cohen's d/CI/n，显著性以 BH-FDR 后 q 为准，并标"不显著的不得声称更好"。
2. 亮点清单（可写进 contribution）。
3. 问题/异常清单（含排查建议）。
4. 待补实验清单（回 m05 补设计）。
5. 推荐图表清单（交 m09 规划、m11 绘制）：方法对比柱状图(带 95%CI)、按种子分布的箱线+散点、学习/scaling 曲线(带 CI 带)、混淆/相关热图，以及**可解释性三图——SHAP beeswarm(全局方向)+ bar(重要性排序)+ waterfall(单样本分解)**，由 `scripts/explain_shap.py` 直接产出 dpi300 的 PDF/SVG/PNG。

## 即用脚本（scripts/，全部 python 自测跑通，复用 code_assets 已验证统计）
- `scripts/analyze_results.py`：结果表 csv 一键分析。EDA 摘要（n/均值±std/中位/95%CI/正态性）+ 按正态性与组数**自动选检验**（2 组正态→Welch t / 非正态→Mann-Whitney；≥3 组正态→**先 Levene 方差齐性：齐用 ANOVA+Tukey、不齐自动切 Welch-ANOVA** / 非正态→Kruskal-Wallis）+ 每对 Cohen's d(Hedges 校正)+ BH-FDR 跨比较校正，输出 `summary.json` + `summary.md`。**小样本（最小组 n<10）自动加 Shapiro 功效不足警告**（n 小时"判正态"不可靠，提示改非参/预设检验）。用法 `python scripts/analyze_results.py results.csv --group method --metric acc f1`；**共享种子/折加 `--paired-by seed` 配对检验**；**`--slice-by <col>` 切片分析**（逐切片复算+标小 n）；**`--emit-claim-table` 产 claim_evidence_table.md**（§6.1 工件）；无参跑合成 demo。
- `scripts/significance_test.py`："p + Cohen's d + CI + FDR"函数库（`welch_t`/`cohens_d`/`mean_diff_ci`/`bootstrap_ci`/`benjamini_hochberg`/`compare_two`/**`delong_two_auroc`**）。`__main__` 逐函数对齐 scipy/statsmodels 打印 ALL PASS。复用 `../../../code_assets/stats_tests.py`。**`delong_two_auroc(y,score_a,score_b)`**（借医疗评估常用 DeLong）：比较同一测试集上两模型 AUROC 差异是否显著（相关样本扣协方差，普通独立检验会错），与 sklearn `roc_auc_score` 数值对齐。
- `scripts/make_figs.py`：出版级 matplotlib 模板（OO 接口、constrained_layout、viridis 色盲友好、误差棒、dpi300 矢量 PDF/SVG/PNG）。builder：`grouped_bar_ci`/`box_strip`/`line_with_band`/`heatmap` + `save_all`。`python scripts/make_figs.py` 产 demo 四联图。
- `scripts/leakage_overfit_check.py`：纯 numpy/pandas 的 train/val/test gap（过拟合/漂移）+ 特征-标签高相关泄漏 + train/test 重复行 + 近常量列告警；deepchecks 缺失时自动降级（不强依赖）。**阈值可 CLI 覆盖**（`--gap-overfit`/`--gap-shift`/`--leak-corr`/`--near-const`，默认值仅启发式、强依赖任务，报告里如实标用的哪套阈值）。`python scripts/leakage_overfit_check.py` 跑带"植入泄漏"的合成 demo。
- `scripts/explain_shap.py`：SHAP 模型可解释性出图。派发 `TreeExplainer`(树模型快路径)→ `shap.Explainer`(统一入口自动挑 Tree/Linear)→ `KernelExplainer`(模型无关兜底，背景集用 shap.kmeans/sample 采样约 100 行控成本)；封装 SHAP 存图坑（每图 `show=False` → `plt.gcf()` → 复用 make_figs `save_all` 存 dpi300 PDF/SVG/PNG），产 beeswarm(全局方向)+ bar(重要性排序)+ waterfall(单样本分解) 三图。shap 未装时优雅降级跳过、exit 0（仿 deepchecks 处理，不强依赖）。`python scripts/explain_shap.py` 跑 make_classification+RandomForest 合成自测。坑：强相关稀释贡献、SHAP 非因果、KernelExplainer 昂贵。
- `examples/worked_example.py`：端到端 EDA→显著性→图→泄漏体检→填好的 `example_report.md`，全部写入 `examples/example_out/`。
- `assets/result_analysis_report_template.md`：四段式（现象→原因→证据→对论文的意义）报告模板，含亮点/异常/待补实验清单。

## 衔接
亮点 → m07 写作支撑；异常/不足 → 回 m05 补实验 或 回 m03 提新 idea；结论写入 db09。诚实标注已验证/未验证（CONVENTIONS §4）。

---
工具真实端点/API/参数与已知坑的逐工具笔记见 `references.md`。
