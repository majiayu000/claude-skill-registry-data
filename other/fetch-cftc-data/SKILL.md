---
name: fetch-cftc-data
description: Download official CFTC Disaggregated Managed Money weekly positions for physical commodity futures, export CSV/JSON, and verify seasonal historical ranks. Use for CFTC数据下载、管理基金持仓、净多头历史序列、历史同期比较. Does not substitute Legacy noncommercial or TFF leveraged funds for Managed Money.
---

# CFTC 管理基金持仓数据

用 `scripts/fetch_cftc.py` 下载 CFTC 官方 Disaggregated 数据。默认仅期货、Managed Money、多头减空头。支持大豆、玉米别名和用户指定的 CFTC 合约市场代码；仅需 Python 3.10+ 标准库。

## 执行

1. 沿用用户指定的品种、日期和报告口径；未指定时下载大豆和玉米、自2006年起至当前可得日期的仅期货数据。市场代码保留前导零，不按模糊名称拼接序列。
2. 在用户工作区选择新的输出目录，将下面的 `<skill-dir>` 替换为本技能所在目录。脚本会分页、核对行数、验证字段并保留原始响应。
3. 检查 `manifest.json` 的实际覆盖日期、最新日期差异和周度缺口提示。下载时间、查询结束日、最新可用持仓日是不同概念。
4. 需要历史纪录判断时，读 [数据口径与比较规则](references/data-contract.md)，核对 `summary.json` 的样本范围、缺失年份、并列纪录与比较定义，再写结论。

```bash
python "<skill-dir>/scripts/fetch_cftc.py" --commodities soybeans,corn --out-dir "outputs/cftc"
python "<skill-dir>/scripts/fetch_cftc.py" --codes 005602,002602 --report combined --start 2020-01-01 --out-dir "outputs/cftc-combined"
python "<skill-dir>/scripts/fetch_cftc.py" --commodities soybeans,corn --end 2026-09-22 --compare-date 2026-09-22 --comparison iso-week --out-dir "outputs/cftc-asof"
```

日期示例仅为用法，不是默认截止日。`--end` 包含当日；未指定时用执行日 UTC 日期。`--compare-date` 必须是每个请求市场实际存在的持仓日期，否则报错；不提供时分别使用各市场最新日期。

## 输出和复用

- `positions.csv`：UTF-8 BOM，可用 Excel 打开；含多头、空头、净头寸、总未平仓量、净头寸/OI、日历年和 ISO 周年。数量单位为手。
- `raw.json`、`raw_pages/*.json`：官方字段和原始响应；`manifest.json` 保存请求 URL、SHA-256、下载时间、行数核对及质量提示。
- `summary.json`：最新值、截至比较日的全样本最大值、同期逐年样本、排名、此前纪录、是否严格创新高。同期第一不自动等于全样本新高。
- `--raw-input PATH`：离线重算原始 JSON（数组或本脚本的 `raw.json`），输出标记为离线数据，不能据此宣称已刷新到最新。
- `--comparison nearest-date`：各年以比较日月日为锚点，选择±3天内最近一期，可用于对 ISO 周比较做敏感性复核。

需要图表时，用导出数据制作时间序列或季节图，注明口径、单位、样本范围和持仓日。XLSX 或公众号图卡可接续可用的表格/图卡技能；本脚本不安装第三方依赖。

## 边界

- Managed Money 可比历史始于2006年6月13日，部分市场更晚。不能用 Legacy 非商业持仓补齐后仍称 Managed Money，或用20年数据宣称30年纪录。
- 历史查询只能验证下载范围；近三年最高不能写成历史最高。“同期”须注明比较方法和实际覆盖年份。
- 保留官方持仓日期，不强制改成周二；节假日可能改变日期。发布日与持仓日分开表述。
- 仅期货与期货加期权使用不同数据集，不能混用；Combined 将期权按期货等值合并。
- HTTP 429、5xx、连接中断最多重试两次；403 不自动换源。遇到沙箱网络限制，按当前环境要求申请网络权限；获准后仍失败则报告具体错误。
- 输出目录非空时停止，选择新目录保留已有成果。发布到网站、GitHub 或定时更新需要相应任务授权，本技能不增加这些操作。

修改计算逻辑时运行 `python -B "<skill-dir>/scripts/test_fetch_cftc.py"`，再对真实品种做小范围在线验证。
