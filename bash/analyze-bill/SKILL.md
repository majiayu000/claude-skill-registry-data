---
name: analyze-bill
description: "账单分析工具。通过 /analyze-bill 手动调用，解析微信/支付宝账单文件（CSV/Excel），支持按时间、商户、分类、支付方式等多维度交互式分析和消费报告生成。仅在用户明确输入 /analyze-bill 时触发。"
user-invocable: true
---

# 账单分析

分析支付宝和微信导出的账单文件。引导用户导入账单 → 自动解析 → 进入交互式查询模式。

## 工作流概览

```
用户触发 /analyze-bill
    ↓
Step 1: 引导用户导出账单并告知目录
    ↓
Step 2: 运行 parse.py 解析账单，汇报结果
    ↓
Step 2.5: 生成分析配置并请用户校对
    ↓
Step 3: 进入交互模式，响应用户的各类分析问题
```

---

## Step 1: 引导用户准备账单

首先向用户说明如何导出账单，并确认他们把账单放在了哪个目录中。

### 导出指引

**支付宝账单导出：**
支付宝 App → 我的 → 账单 → 右上角「...」→ 开具交易流水证明 → 选择时间段（建议选最大范围）→ 填写邮箱接收 CSV 文件 → 下载后放到一个目录中

**微信账单导出：**
微信 App → 我 → 服务 → 钱包 → 账单 → 右上角「...」→ 下载账单 → 用于个人对账 → 选择时间段（建议选最大范围）→ 填写邮箱 → 收到后解压得到 xlsx 文件，放到一个目录中

### 确认目录

用可点击的选项按钮让用户确认账单目录。常用位置包括 `~/Downloads/` 或用户手动指定的路径。不要假设目录——等用户明确告知后再继续。

用户只需提供一个目录路径，脚本会自动扫描其中所有可识别的账单文件（不递归子目录）。

---

## Step 2: 解析账单

用户确认目录后，运行 parse.py。

### 数据清理

每次执行解析前，先删除上次的临时数据，确保不被旧数据干扰：

```bash
rm -f /tmp/analyze_bill_data.json
rm -f /tmp/analyze_bill_config.json
```

### 执行解析

```bash
python3 skills/analyze-bill/scripts/parse.py <用户提供的目录> -o /tmp/analyze_bill_data.json
```

parse.py 自动完成：
- 扫描目录下所有文件，自动跳过无法识别的文件
- 识别支付宝账单（CSV，GBK 编码）和微信账单（XLSX）
- 统一字段结构：time、type、target、target_account、description、income_expense、amount、payment_method、status、order_id、merchant_order_id、remark、source
- 按交易时间排序
- 删除旧的输出文件（如果是同名路径）

### 汇报解析结果

解析完成后，向用户汇报：
- 识别到几个账单文件，分别是什么来源（支付宝/微信）
- 总共多少条交易记录
- 账单的时间范围（最早 → 最晚）
- 哪些文件被跳过了（如有）

如果解析结果为 0 条，提示用户检查目录和文件格式是否正确。

---

## Step 2.5: 生成并校对分析配置

解析完成后，需要生成分析配置文件。这个配置文件决定了哪些交易状态算"成功"、哪些算"收支"、如何归并商户名。

### 自动生成配置

```bash
python3 skills/analyze-bill/scripts/discover.py /tmp/analyze_bill_data.json -o /tmp/analyze_bill_config.json
```

`discover.py` 会自动：
- 扫描数据中出现的所有交易状态，用启发式规则分类（success / failure / unknown）
- 扫描所有收支方向，自动分类（income / expense / neutral）
- 列出所有出现的商户名称作为参考（`_reference.all_targets`）
- 生成空的 `target_aliases` 供后续填充

### 请用户校对配置

运行 discover.py 后，它会打印摘要信息。你需要在此基础上完成校对流程。

#### 第一步：汇报自动检测结果并处理 unknown 状态

向用户汇报：
- 交易状态：成功 X 种、失败 Y 种、未知 Z 种
- 列出每种状态及其具体分类
- 收支方向：income X 种、expense Y 种、neutral Z 种

**⚠️ unknown 状态必须逐项让用户确认：**

对于每个标记为 `unknown` 的状态，向用户展示该状态下的交易数量，**要求用户明确指定**该状态应归类为 `success` 还是 `failure`。不能跳过——因为只有 `success` 状态的交易才会被纳入分析，分类错误会直接影响统计结果的准确性。用户确认后，编辑 `/tmp/analyze_bill_config.json` 中 `status_mapping` 的对应项。

同样，如果有 `unknown` 的收支方向，也需要用户确认后更新 `direction_mapping`。

#### 第二步：AI 分析商户名并建议归并

读取配置文件中的 `_reference.all_targets`（包含所有商户名及其交易次数），**由你（AI）分析哪些商户名可能指向同一个实体**，然后向用户提出归并建议。

分析思路：
- 有些关系可以通过文本判断：如「美团」和「美团外卖」、「星巴克(中山公园店)」和「星巴克(南京路店)」
- 有些关系需要常识判断：如「网易云音乐」的实际运营主体是「杭州乐读科技有限公司」、某些连锁品牌在不同城市注册了不同的公司名
- 优先关注交易次数多的商户，对用户影响更大
- 不确定的关系，标注为"存疑"并让用户判断

向用户展示你的归并建议后，请用户确认。用户确认后，编辑 `/tmp/analyze_bill_config.json` 的 `target_aliases` 写入确认的归并关系。

**请用户确认配置是否正确。** 尤其关注：
- 是否有状态被错误分类？（如"退款成功"应该算成功还是排除？）
- AI 的商户归并建议是否合理？有没有需要调整的？
- 是否有 AI 漏掉的需要手动补充的归并关系？

### 配置文件格式

```json
{
  "status_mapping": {
    "交易成功": "success",
    "交易关闭": "failure",
    "付款失败": "failure"
  },
  "direction_mapping": {
    "支出": "expense",
    "收入": "income",
    "不计收支": "neutral"
  },
  "target_aliases": {
    "携程": ["携程旅行网", "上海赫程国际旅行社有限公司"],
    "哈啰": ["哈啰出行", "杭州青奇"]
  }
}
```

- `status_mapping`：每项分类为 `success` / `failure`。只有 `success` 状态的交易会被纳入分析
- `direction_mapping`：每项分类为 `income` / `expense` / `neutral`
- `target_aliases`：键为归一化名，值为原始商户名列表。analyze.py 会自动用 `re.fullmatch` 做匹配

**快速跳过：** 如果用户不想校对配置，可以直接跳过此步骤。`analyze.py` 在无配置文件时会自动从数据中检测（与 `discover.py` 相同的逻辑），只是无法使用商户别名。

---

## Step 3: 进入交互模式

解析完成后，数据已就绪。告诉用户现在可以自由提问，例如：

- 「生成一份上个月的消费报告」
- 「我在餐饮上总共花了多少钱」
- 「蜜雪冰城去了几次，花了多少」
- 「对比一下支付宝和微信的支出」
- 「看看每个月花了多少钱的趋势」
- 「消费最多的 10 个商户是哪些」
- 「交通出行方面，哪个月花得最多」
- 「看看我周末 vs 工作日的消费习惯」

**重要：** 不要主动生成完整报告。等待用户提出问题后，再针对性地查询和回答。

---

## Step 4: 响应用户查询

**所有数据查询统一通过 `analyze.py` CLI 完成，绝不修改 analyze.py 源码。**

基础调用格式（使用校对后的配置文件）：

```bash
python3 skills/analyze-bill/scripts/analyze.py --config /tmp/analyze_bill_config.json [查询模式] [筛选条件]
```

如果用户跳过了配置校对，省略 `--config` 参数即可（analyze.py 会自动检测）。

CLI 输出 JSON 格式的统计结果，你解读后将关键信息以易读的方式呈现给用户。

### 公共筛选参数

以下参数可用于所有查询模式：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--start` | 起始日期（含） | `--start 2025-01-01` |
| `--end` | 结束日期（含） | `--end 2025-06-30` |
| `--direction` | 收支方向 | `expense`（默认）/ `income` / `all` |
| `--group-by` | 时间分组 | `month` / `year` / `day` / `none`（默认） |

注意：`--group-by` 对排行类查询（`--top-*`、`--sources`）无效；默认查询（无任何模式参数）会自动按月分组。

### 查询模式速查

根据用户意图选择对应的命令行参数：

| 用户想问的 | 使用参数 |
|-----------|---------|
| 总览 / 每月趋势 | （默认，无参数） 或 `--summary --group-by month` |
| 某商户花了多少 | `--by-target 蜜雪冰城 --group-by month` |
| 某类消费花了多少 | `--by-type 餐饮美食 --group-by month` |
| 支付宝 vs 微信 | `--sources` |
| 周末 vs 工作日消费 | `--by-weekday` |
| 搜索关键词（如"美团"） | `--search 美团 --group-by month` |
| 消费最多的商户 | `--top-targets 10` |
| 消费最多的类别 | `--top-types 10` |
| 哪种支付方式用最多 | `--top-payment-methods 10` |
| 所有消费类别一览 | `--all-types` |
| 所有商户一览 | `--all-targets` |
| 只用支付宝的消费 | `--by-source alipay --group-by month` |

### 实际命令示例

以下示例省略了 `--config` 参数以保持简洁。如果已生成配置文件，每个命令都应加上 `--config /tmp/analyze_bill_config.json`。

**用户要某月消费报告：** 一次运行多条命令获取不同维度数据：
```bash
python3 skills/analyze-bill/scripts/analyze.py --config /tmp/analyze_bill_config.json --start 2025-06-01 --end 2025-06-30
python3 skills/analyze-bill/scripts/analyze.py --config /tmp/analyze_bill_config.json --start 2025-06-01 --end 2025-06-30 --top-targets 10
python3 skills/analyze-bill/scripts/analyze.py --config /tmp/analyze_bill_config.json --start 2025-06-01 --end 2025-06-30 --top-types 10
```

**用户问「蜜雪冰城去了几次」：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --by-target 蜜雪冰城 --group-by month
```

**用户问「餐饮花了多少」：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --by-type 餐饮美食 --group-by month
```

**用户想看收支总览（含收入）：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --direction all --group-by month
```

**用户想按年度看趋势：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --group-by year
```

**用户问「周末花得多还是工作日花得多」：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --by-weekday
```

**用户问「搜一下和余额宝相关的交易」：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --search 余额宝 --group-by month --direction all
```

**用户问「看看房租相关的支出」：**
```bash
python3 skills/analyze-bill/scripts/analyze.py --search 房租
```

### CLI 输出格式

每个统计结果项的标准字段：

```json
{
  "label": "2025-06",
  "count": 45,
  "total_amount": -3245.80,
  "income": {"count": 2, "amount": 120.00},
  "expense": {"count": 43, "amount": 3365.80},
  "avg_per_transaction": -72.13,
  "max_single": {"amount": 2000.00, "target": "携程", "time": "2025-06-15 14:30:00"},
  "min_single": {"amount": 1.50, "target": "哈啰", "time": "2025-06-03 08:20:00"}
}
```

- `label`：统计维度标签（月份、商户名、分类名、星期等）
- `count`：交易笔数
- `total_amount`：净额（收入 − 支出），负数表示净支出
- `expense.amount`：支出总额（始终为正数）
- `income.amount`：收入总额（始终为正数）
- `avg_per_transaction`：笔均净额
- `max_single`：该维度下金额最大的单笔交易（含金额、归一化商户名、时间）
- `min_single`：该维度下金额最小的单笔交易

### 结果呈现

拿到 JSON 结果后：
1. 用易读的表格或列表呈现关键数据
2. 附上简要文字总结：总金额、值得注意的变化趋势或异常值
3. 金额统一用 ¥ 符号，保留两位小数
4. 超过 20 行的数据，展示排名靠前的部分，其余概述

### 完整参数参考

```
usage: analyze.py [-h] [--file FILE] [--config CONFIG]
                  [--start START] [--end END]
                  [--direction {expense,income,all}] [--group-by {month,year,day,none}]
                  [--summary] [--by-target NAME] [--by-type TYPE] [--by-source SOURCE]
                  [--by-weekday] [--search KEYWORD]
                  [--top-targets [N]] [--top-types [N]] [--top-payment-methods [N]]
                  [--all-types] [--all-targets] [--sources]
                  [--min-amount MIN_AMOUNT] [--format {json,table}]
```

如果 `analyze.py` 报错找不到 `openpyxl`，执行 `pip3 install openpyxl`。

---

## 依赖

- Python 3.7+
- openpyxl：`pip3 install openpyxl`

## 支持的文件格式

- 支付宝：CSV（GBK 编码，自动检测表头）
- 微信：XLSX（通过 openpyxl 读取）
- 一个目录中可以同时有多个账单文件（例如不同时间段的导出），脚本会合并所有记录

## 数据说明

- 账单数据临时存储在 `/tmp/analyze_bill_data.json`
- 每次执行 `/analyze-bill` 时会先清理旧数据
- 系统重启后 `/tmp/` 中的数据会自动清除
- 原始账单文件始终保留在用户指定的目录中，不受影响
