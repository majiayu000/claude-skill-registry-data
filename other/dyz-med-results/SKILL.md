---
name: dyz-med-results
description: >-
  把已核实的统计输出、表格和图转写为医学论文结果部分，保持样本量、效应量、置信区间、P 值、模型及分析
  层级可追溯。当用户需要撰写或修订结果正文、图表引用或数值一致性时使用；不运行新分析、不补造缺失数字，
  也不承担讨论解释。
  Use to write results sections while preserving verified effect estimates and numerical provenance.
---

# 医学论文结果部分撰写

## 写作前提

优先读取：

- 研究方案或统计分析计划中的主要、次要和探索性分析定义；
- 可追溯的统计输出或结构化结果；
- 方法部分中的分析人群、模型和协变量；
- 表格、图及其数据来源；
- 目标期刊与适用报告规范。

若只有截图、转述或无法追溯的数字，先标出可用性限制。缺少主要结局结果时，不生成看似完整的结果正文。

## 核心原则

1. 每个数字逐项复制并核对，不重算统计结果或改原输出；展示舍入须逐值明确精度和规则，计数精确相等。
2. 结果说明“观察到什么”，不解释原因、不比较文献、不写临床建议。
3. 预设主要结局优先；预设次要、敏感性、亚组和事后探索性分析分层呈现。
4. 统计显著不等于临床重要，无统计显著也不等于无效；优先报告效应量及不确定性。
5. 基线 P 值不用于自动选择混杂因素；调整集以方法和实际模型为准。

## 工作流

### 1. 建立结果来源表

为每个拟写结果记录：分析名称、预设层级、分析人群、N、事件数、效应量、置信区间、P 值、模型、调整集、
来源文件及位置。发现正文、表格与输出冲突时，停止该项写作并列出冲突。

用稳定工件ID `analysis-results` 映射实际 `path/version/sha256`，兼容既有
`analysis-results.json`、`analysis-results.yaml`、`structured_results.yaml`等名称，不改名、不凭文件名猜身份。
接受有效可追溯的外部统计输出，不要求先运行 `dyz-med-analyze`。缺来源或未执行的结果保留为`unverified`。
最小结果字段及有定位的报告清单见[结构化对账输入合同](templates/results-section-skeleton.md#结构化对账输入合同)。

对关键结果概括使用[关键结论反查](templates/results-self-check-checklist.md#h-关键结论反查)，把拟写句
关联到上述来源表或已有论断证据矩阵中的同一条记录；按实际效应、区间、结局层级、设计及可信阈值复核，
不只复制上游分类标签。缺少信息保留待核，不新增事实库或执行分析。

### 2. 确定呈现顺序

通常按参与者流程与描述性信息、主要结局、次要结局、安全性或不良事件、敏感性分析、亚组分析和探索性分析
组织。顺序服从研究方案、研究类型和期刊要求。

### 3. 起草正文

- 报告各分析的实际分母、事件数或样本量；
- 给出适合该模型的效应量和置信区间，P 值作为补充；
- 区分未调整与调整结果，并准确写出模型或调整集；
- 亚组分析报告各组估计值与不确定性，并以交互检验评价组间差异；不要用“一组显著、另一组不显著”
  推断交互；
- 计划外分析明确标为事后或探索性；
- 临床阈值只有在预先定义且来源明确时才可作为描述性参照，不在结果段落扩展解释。

### 4. 处理图表

正文概括主要发现，不逐格重复表格。核对每个图表编号、标题、分母和正文引用均存在且一致。图题、表题位置
服从目标期刊要求，不假设所有期刊规则相同。

### 5. 解释防火墙

标出并移出原因推测、机制、与既往研究比较、价值判断和临床建议。不要静默删除作者内容；把拟移动文字放入
“讨论素材”或变更记录。

### 6. 可选只读数值对账

仅在用户请求核对时，使用自包含标准库[对账脚本](scripts/check_result_consistency.py)。输入为显式
工件清单、规范化结果JSON与有定位的报告值JSON；不通用提取Word/PDF、不运行统计模型、不改稿或源结果。
现有YAML可继续人工读取；需要机器核对时在获准输出区另建JSON派生工件，同时绑定原件并人工核实转换。

从已加载的本技能 `SKILL.md` 所在目录定位脚本，将 `<本技能目录>` 替换为该目录的绝对路径。在论文项目根目录运行；输入、输出及 `--root` 属于论文项目，技能目录仅提供脚本和模板：

```powershell
python -B "<本技能目录>/scripts/check_result_consistency.py" paper/data/stats/result-artifacts.json --root . --report paper/reports/result-consistency-run-001.json --record paper/reports/result-consistency-run-001.check.json --check-id result-consistency-run-001
```

开发者单元测试在下载的源码仓库内运行：`python -B -m unittest discover -s tests -p test_result_consistency.py -v`。安装副本不包含仓库测试目录。

所有引用/输出路径相对于显式`--root`，禁止绝对路径、反斜杠、空段、`.`、`..`及链接逃逸；manifest参数自身
相对于当前调用目录。输出必须为新文件，拒绝覆盖。输入运行前后按原字节核验。stdout为JSON摘要，领域报告
含`differences/unverified/matched_values/reported_items/coverage/inputs`，其中报告项保留实际定位。
独立`.check.json`含R2同形`artifacts/checks`记录及已落盘报告的SHA256；不自动写passport。

退出码：`0`=清单范围内consistent；`1`=discrepant（仍可并列未核实项）；`3`=无已检出差异但unverified；
`2`=参数、格式、路径、I/O或绑定错误（未生成可登记完成检查，检查stdout/stderr；后段写失败可能保留报告）。
正常发现差异仍是`execution_status=completed`而非执行failed。空清单、缺来源、未执行、缺口径、未知字段或
无法处理的值不能自动通过。整数严格相等；非整数默认精确比较，仅允许逐值显式十进制舍入，绝不以宽泛容差
掩盖236与235。分别核对组别、单位、时间点及P/CI口径，不从P与CI推导相互矛盾，不自动换算HR/OR/RR。

`consistent`不是全文、模型适用性、来源真实性或医学结论认证；未列入清单的结果会单列为未覆盖。
输入字节或版本改变后须新建检查，不能沿用旧结论。无passport也可独立使用这些记录；更新索引前由人审阅。

## 输出

默认写入 `paper/sections/03-results.md`，并附一份数值核对表或问题清单。只修改用户指定段落时，保留其余
结果内容和编号。

## 验收标准

- 正文中的每个数字可追溯到指定输出；
- 主要、次要、亚组与探索性分析身份清楚；
- 结果与方法中的人群、模型和调整集一致；
- 没有新增数字、因果解释或文献比较；
- 图表编号、正文引用和分母一致；单位、参考组、时间点及展示精度已核对；
- 机器对账的覆盖范围、差异、未核实项及输入版本明确，不把工具退出0或completed当作科学通过。

## 配套资源

- [结果部分骨架](templates/results-section-skeleton.md)
- [结果自查清单](templates/results-self-check-checklist.md)
- [虚构示例](examples/worked-example-xelox-dfs.md)
- [报告规范参考](references/citation-list.md)
