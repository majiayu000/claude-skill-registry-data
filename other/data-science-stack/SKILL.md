---
name: data-science-stack
description: 数学建模竞赛数据科学技能（C 类数据题、预测题及 MathorCup 大数据题）：EDA、预处理与特征工程、统计推断、机器学习、时间序列、模型评估与调参。触发词：数据题、C题、MathorCup、EDA、数据预处理、特征工程、机器学习、回归、分类、聚类、时间序列、预测、ARIMA、XGBoost、统计检验。与 contest-orchestrator executor 阶段、math-modeling、scipilot-figure-skill 协作。
metadata:
  version: "1.0"
---

# 数学建模竞赛 · 数据科学全链路（C 题/预测题）

> 定位：解决"拿到 Excel/CSV 附件后怎么办"的问题。目标是一场数据题从 EDA 到论文结果的全部代码与文字素材一次到位，结果只从代码生成。

## Contest-Orchestrator Adapter

本技能是 `contest-orchestrator` 中 C 类/预测类小问的执行器，不是独立主控。只接收当前任务卡、数据审计、`model_blueprint.yaml`/`model_contract.yaml` 和已批准数据源；输出写入项目工作区，并进入 `run_manifest`、`result_registry` 和 `numeric_source_map`。

- 每个数据处理决定记录来源、处理原因、影响范围和可复算命令；不得静默删除样本、改动原始数据或捏造缺失结果。
- 训练、验证、预测和敏感性结果必须绑定随机种子、数据版本、代码路径、指标定义和结果文件；模型选择遵循 baseline → 验证 → 必要复杂化。
- 返回 `status`、`active_mode`、`task_card`、`artifacts`、`evidence`、`checks`、`blockers`、`next_node` 节点包。缺数据、缺标签、指标不适用或证据断裂时返回 `BLOCKED_INPUT`/`FAIL`。
- 数据结果图只走 `scipilot-figure-skill` → `modelviz` → `scipilot-figure-skill`；本技能不替代绘图技能执行视觉检查，进入绘图路由后按图表契约默认完成视觉检查。
- 节点包和论文可见内容不得出现元话语、内部交流、调试信息、失败过程或其他负回响。

`active_mode: full-contest-mathorcup` 时，M2 的 data 实例依据 `problem_statement.md`、`data_overview.yaml`、`task_kpi.yaml` 和题面附件输出 `eda_report.md`、`features.yaml` 与分割/预处理协议；verifier 独立签署 `leakage_audit.yaml` 后才能冻结特征。M3 仅由唯一 solver 使用冻结数据管线完成各小问 baseline、同切分/同指标候选比较、参数选择和 `run_manifest.yaml`；本技能不能另起解题主线或绕过独立 `independent_validation.yaml`。填补、编码、缩放、特征选择、目标编码和调参仅在训练折拟合；时间数据按时间分割，实体相关样本按组隔离，测试集不参与拟合或路线选择。M2 不写最终模型结果，M3 的每个量化结论必须绑定数据/代码/参数/种子/结果文件与跨问接口。下文时长、阈值、图型和算法是按需参考，不是 MathorCup 的固定门禁。

## 0. 何时触发

MathorCup 的评估、模型能力核对和资源恢复先读取 `references/mathorcup_experiment_protocol.md`。该协议补充现有模型卡与 run manifest，不新增固定算法、数字门槛或审批阶段。

题目出现以下任一信号即进入本技能流程（典型：国赛 C 题、美赛 C/E/F 题的数据部分）：

- 题目附带了数据文件（.xlsx/.csv/.txt），且问题围绕这些数据
- 问题动词是"预测 / 分类 / 识别 / 评价 / 关联 / 画像 / 排序"
- 问题要求"建立……与……之间的关系模型"

不触发：纯机理建模（微分方程）、纯优化调度（无数据依赖）——那走 `pyomo` / `heuristic-algorithms`。

## 1. 总览：五步流水线

```
Step1 EDA（1-2h）→ Step2 预处理+特征工程（1-2h）→ Step3 统计推断（按需）
→ Step4 ML 建模+评估（4-8h，核心）→ Step5 时间序列（若为预测题）
全程产出：数据报告.md + 图（scipilot）+ 结果表（.csv）+ 代码落盘
```

每一步都必须产出**论文可直接使用的素材**（表格/图/一段话），不允许"只探索不记录"。

## 2. Step 1：EDA（探索性分析）

### 10 步清单（顺序执行，输出一份《数据报告.md》）

1. **形状与类型**：`df.shape`、`df.dtypes`、列名规范
2. **缺失值**：逐列缺失率；缺失 >20% 的列标记"慎用或剔除"
3. **重复行**：`df.duplicated().sum()`
4. **描述统计**：`df.describe()`；核对量纲差异 >3 个数量级的列（需标准化或换单位）
5. **异常值**：每列 IQR 法 + 3σ 法交叉标记；异常比例 >5% 的列写进数据报告（保留还是剔除要论证）
6. **分布形状**：直方图/箱线图（scipilot 出图），偏度、峰度数值
7. **相关性**：数值列 Pearson 相关矩阵热力图 + 与目标变量的相关系数排序
8. **分组结构**：类别列分组后目标变量的差异（分组箱线图）；**判断是否该用混合效应/分层**
9. **时间结构**：若有时间列——趋势、季节、缺失时间段；画时序图
10. **结论表**：一列一个结论（类型/缺失/异常/分布/相关性/处理建议），这就是数据报告正文

```python
import pandas as pd, numpy as np
df = pd.read_excel('附件.xlsx')  # 单表示例；多 sheet 时逐表选择并审计
# 或 df = pd.read_csv('data.csv', encoding='gbk')  # 中文数据常见 gbk

report = []
for col in df.columns:
    s = df[col]
    miss = s.isnull().mean()
    if pd.api.types.is_numeric_dtype(s):
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        n_out = ((s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)).sum()
        report.append({'列': col, '类型': '数值', '缺失率': f'{miss:.1%}',
                       '均值': round(s.mean(), 4), '异常数': int(n_out)})
    else:
        report.append({'列': col, '类型': '类别', '缺失率': f'{miss:.1%}',
                       '唯一值数': s.nunique()})
print(pd.DataFrame(report).to_string(index=False))
```

**EDA 雷区**：不做 EDA 直接建模（评委问"为什么用这个模型"时答不上）｜ 只数缺失率不处理 ｜ 不看量纲 ｜ 不记录发现（赛后无法写论文）。

## 3. Step 2：预处理与特征工程

按 EDA 结论执行，**每项处理都要在数据报告里留一行记录**（论文"数据预处理"节就靠它）。

以下算子只表示处理方式。凡需从样本估计均值、众数、分位数、编码词表或尺度参数的操作，必须放入训练折内拟合的管线，再对验证/测试折调用同一变换；时间插值不得跨越预测时点或分割边界。

| 问题 | 处理 | 代码 |
|---|---|---|
| 缺失（数值） | 均值/中位数/线性插值/模型预测填充（按缺失率选择） | `df[col].interpolate(method='linear')` |
| 缺失（类别） | 众数填充或"未知"类 | `df[col].fillna(df[col].mode()[0])` |
| 异常值 | 3σ 截尾 / IQR 缩尾 / 保留并标注（竞赛中**优先缩尾或保留**，直接删行会被质疑） | `s.clip(s.quantile(0.01), s.quantile(0.99))` |
| 量纲差异 | 标准化（Z-score）/ 归一化（MinMax），注意**先划分训练测试再fit** | `from sklearn.preprocessing import StandardScaler` |
| 类别编码 | LabelEncoder（有序）/ OneHot（无序）/ 频数编码（高基数） | `pd.get_dummies()` |
| 长尾分布 | log1p 变换（目标变量偏斜时常用） | `np.log1p(y)`，预测完 `np.expm1()` 还原 |
| 时间列 | 拆成年/月/日/星期/小时；构造滞后特征 | `df['month'] = df['date'].dt.month` |

**特征工程（拿奖关键）**，按重要性排序：
1. **领域特征**：读题找隐含变量（例：销量题 → 节假日/促销/天气；定价题 → 利润率/竞争价差）
2. **统计特征**：历史均值/中位数/极差/标准差/趋势斜率（滚动窗口）
3. **交互特征**：两变量乘积/比值（例：单价×销量=销售额）
4. **降维**：相关性 >0.9 的列只留一个；PCA 用于可视化或消除多重共线性（要解释主成分含义）

**铁律**：特征构造只能使用**已知信息**（比赛时刻之前的数据），严禁用未来数据构造特征（数据泄漏，评委会质疑、重算会翻车）。

## 4. Step 3：统计推断（按需，不要为用而用）

| 问题 | 方法 | 代码 |
|---|---|---|
| 两组目标变量有无显著差异 | 独立样本 t 检验 / Mann-Whitney U | `scipy.stats.ttest_ind` / `mannwhitneyu` |
| 多组差异 | 单因素方差分析 + Tukey HSD | `scipy.stats.f_oneway` + `statsmodels.stats.multicomp.pairwise_tukeyhsd` |
| 类别×类别独立性 | 卡方检验 | `scipy.stats.chi2_contingency` |
| 两变量线性相关 | Pearson（正态） | `scipy.stats.pearsonr` |
| 两变量单调相关 | Spearman（非正态/序数） | `scipy.stats.spearmanr` |
| 数据是否正态 | Shapiro-Wilk（n<5000）/ 偏度峰度 | `scipy.stats.shapiro` |
| 多因素对目标的关联强度 | 灰色关联度（国赛常用，手写 15 行） | 见下方模板 |

```python
# 灰色关联度分析（评价/相关性题高频使用）
def grey_relational_degree(X, y):
    """X: (n, m) 特征矩阵, y: (n,) 目标列。返回每个特征的关联度"""
    Xn = (X - X.min(0)) / (X.max(0) - X.min(0) + 1e-9)
    yn = (y - y.min()) / (y.max() - y.min() + 1e-9)
    diff = np.abs(Xn - yn[:, None])
    rho = 0.5
    rel = (diff.min(0) + rho * diff.max(0)) / (diff + rho * diff.max(0))
    return rel.mean(0)  # 每列一个关联度，可排序
```

## 4.5 详细 ML 手册（按需加载）

- ML 类算法完整手册（XGBoost/LightGBM/RF/SVM/BP 系统展开，含问题适配框架与参数建议）：`references/cookbook-ml.md`。本文档选择树是首选入口，手册提供更细的算法适配细节。

## 5. Step 4：机器学习模型库（选择树）

按问题类型直接选，**首选简单可解释模型，复杂模型只做提升**（评委喜欢"baseline 对比"叙事）：

```
回归（预测连续值）
├─ 线性/岭回归 → 快、可解释、适合关系建模题（"建立X与Y的关系"）
├─ 随机森林 / XGBoost / LightGBM → 特征多、非线性强时主用
└─ 对比叙事：线性做 baseline，树模型做提升，报告两者 R²

分类（判别/识别/分类）
├─ 逻辑回归 → baseline + 可解释（系数=影响）
├─ 随机森林/XGBoost → 主用；SVM → 小样本高维
└─ 指标：准确率 + F1 + 混淆矩阵（别只报准确率）

聚类（画像/分区/划分）
├─ K-Means → 首选，肘部法则定 K + 轮廓系数验证
├─ DBSCAN → 密度不均/有离群点
└─ 输出：每类中心 + 画像表（论文"用户画像"节直接抄）

评价/排序（无监督打分）
├─ 熵权法（客观权重）+ TOPSIS（综合排序）→ 数据驱动评价题首选
└─ AHP（主观权重，需专家判断，评委接受度高但要有理由）
```

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib, os

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler(); X_tr = scaler.fit_transform(X_train); X_te = scaler.transform(X_test)

# 回归主模型 + 可解释性
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_tr, y_train)
r2 = model.score(X_te, y_test)
imp = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)
print(f'R²={r2:.4f}  前5重要特征:\n{imp.head(5)}')

# 落盘（orchestrator 要求：结果只从代码生成，可复现）
os.makedirs('results', exist_ok=True)
joblib.dump({'model': model, 'scaler': scaler, 'r2': r2}, 'results/model.pkl')
```

**多模型对比表（论文必备）**：

| 模型 | 训练R² | 测试R² | RMSE | 结论 |
|---|---|---|---|---|
| 线性回归 | 0.85 | 0.81 | 12.3 | baseline |
| 随机森林 | 0.97 | 0.89 | 8.1 | 主模型 |
| XGBoost | 0.98 | 0.88 | 8.4 | 与RF持平 |

## 6. Step 5：时间序列（预测类题目）

流程：**画图看趋势/季节 → ADF 平稳性检验 → 差分/分解 → 选模型 → 评估 → 外推预测**。

```python
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

# 1. 平稳性检验：p<0.05 视为平稳
p_val = adfuller(series.dropna())[1]

# 2. 差分到平稳（通常 d=1）
# 3. ARIMA 定阶：AIC 网格搜索
best_aic, best_order = np.inf, None
for p in range(0, 4):
    for q in range(0, 4):
        try:
            aic = ARIMA(series, order=(p, 1, q)).fit().aic
            if aic < best_aic: best_aic, best_order = aic, (p, 1, q)
        except Exception: pass
model = ARIMA(series, order=best_order).fit()
print(model.summary())

# 4. 外推预测 + 置信区间
fc = model.get_forecast(steps=12)
pred = fc.predicted_mean; ci = fc.conf_int()
```

**时间序列雷区**：
- 不做平稳性检验直接套 ARIMA
- 用整段数据训练再"预测"历史段（要先划分：前 80% 训练、后 20% 验证）
- 有季节性的数据用普通 ARIMA（该用 SARIMA/Prophet）
- 外推步数超过数据长度的 1/3 硬预测（结果不可信，评委一眼看穿）
- 多序列互相关时忽略（可用 VAR，但竞赛 ARIMA/SARIMA/Prophet 足够）

## 7. 模型评估与调参（论文"模型检验"节）

1. **交叉验证**：小样本用 5 折 CV 报均值±std；大样本固定划分 + 报告方差
2. **回归指标**：R²、RMSE、MAE（论文报全，评委看 R² 和 RMSE）
3. **分类指标**：准确率 + F1 + 混淆矩阵热力图；不平衡数据报 F1 和召回不报准确率
4. **调参**：`GridSearchCV`（小网格）或手工 2-3 轮；**不要盲目大网格**（时间成本）
5. **泛化验证**：随机划分 3 次取平均，报告波动区间（证明模型稳定，不是运气）
6. **与 baseline 对比**：任何 ML 模型都必须配一个简单模型（均值预测/线性回归）对比，差距就是你的"建模贡献"

## 8. 论文输出规范（每步都产出，最后直接组装）

| 论文章节 | 素材来源 |
|---|---|
| 数据预处理 | Step2 的处理记录表（转成论文表格） |
| 探索性分析 | Step1 数据报告 + scipilot 出的分布图/相关热力图 |
| 模型建立 | Step4 模型公式/流程（写清目标函数与评估指标） |
| 结果分析 | 对比表 + 预测结果表 + 误差分析 |
| 模型检验 | Step7 交叉验证 + 灵敏度/鲁棒性 |
| 结论 | 每个子问题的数字结果 + 特征重要性前3 |

**图表规范**：图标题在下方、表标题在上方；坐标轴带单位；图内直接标注关键结论（评委 30 秒扫图）；热力图用 scipilot 默认色盲安全配色，禁用 rainbow。

## 9. 竞赛雷区（红线，违反直接丢分）

- ❌ 数据泄漏：用未来数据/全局统计量（如全量 mean）填充训练集——必须 train 内部 fit
- ❌ 测试集参与特征工程或标准化
- ❌ 过拟合汇报：测试 R² 与训练差 >0.15 还宣称"模型很好"
- ❌ 不报告模型参数与随机种子（结果不可复现 = 评委不信任）
- ❌ 论文里的数字与代码输出不一致（评审核对必抓）
- ❌ 小样本（<100 行）硬上深度学习/XGBoost 大调参——过拟合且无必要
- ❌ 只报一个指标（准确率）掩盖类别不平衡

## 10. 与现有体系对接

- 在 `contest-orchestrator` 中：本技能在 **H5 解题阶段**调用，输入为当前任务卡、`unified_problem_package.yaml`（H1 题意理解产物，含数据字典和约束）、`model_contract.yaml` 和已批准数据源；输出《数据报告.md》+ 结果表必须落盘到项目工作区并进入 result_registry 和 numeric_source_map
- 数据结果图统一交给 `modelviz` → `scipilot-figure-skill`（数据剖析/模板适配 → 科研规范质检）；本技能不替代绘图技能执行视觉检查，绘图路由默认完成视觉检查
- 若题目同时含优化部分（如"预测后做排产"），预测结果直接作为 `pyomo`/`heuristic-algorithms` 的输入参数
- 时间序列预测结果写回 `math-modeling` 的"预测"速查流程

## 代码注释规范（B 题优化加固协同变更）

进行数据处理、特征工程、统计分析、机器学习建模时，代码必须有必要的注释，像人写的而不是 AI 生成的。不用大量注释，但关键位置必须有。

**必须有注释的位置**：
- 文件头：1-3 行说明这个文件做什么
- 数据加载和清洗：每个关键步骤注释说明做什么、为什么
- 特征工程：每个特征注释说明含义、计算方式、业务意义
- 模型配置：每个参数注释说明含义、取值依据、对结果的影响
- 模型评估：每个指标注释说明含义、结果解读
- 特征重要性：注释说明用途

**注释内容红线**：注释中禁止出现内部讨论话语（经讨论、agent建议）、AI 思考过程（首先、其次、让我）、元话语（本文将、以下代码）、负向回响（之前用、v2修正、尝试了）、AI 协作痕迹（agent、prompt、审查）。注释必须是纯粹的技术说明。

**详细规范和示例**：`references/code_comment_guide.md`

## 数值合理性检查规范（B 题优化加固协同变更）

进行数据处理、统计分析、机器学习建模后，必须对结果进行数值合理性检查，禁止异常结果进入结果登记。

**必查项**：
- inf/nan 检测：数据和结果中不得出现无穷大或非数
- 目标值/指标量级异常：预测值、评估指标 >1e15 或 <1e-15（非零）需要说明原因
- 数据范围检查：特征值是否在合理范围内（如概率[0,1]、年龄>0等）
- 缺失值检查：关键特征是否有缺失值，缺失率是否在可接受范围内
- 异常值检查：是否存在明显的离群点，是否需要处理
- 模型评估指标合理性：准确率、AUC、RMSE等指标是否在合理范围内
- 结果文件完整性：JSON 可解析、CSV 列数一致、非空

**检查时机**：每次数据处理和模型训练完成后立即检查，不通过的结果不得登记到 result_registry。

**异常处理**：发现异常必须排查原因（数据质量问题、特征工程错误、模型参数不当等），修复后重新处理，不得带着异常结果进入下一环节。

**详细规范和领域特定检查**：`references/numerical_sanity_guide.md`
