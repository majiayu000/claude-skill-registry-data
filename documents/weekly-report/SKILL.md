---
name: weekly-report
description: 端到端自动生成兴银理财多资产投资部产品运作周报。完整流程包括：(1)更新config日期配置，(2)运行Python数据处理管线(移动文件、AI产品分类、生成结果表、计算基准、收益预测)，(3)用openpyxl更新Excel链接工作簿中的外部文件路径和公式引用，(4)将Excel表格截图并按书签顺序插入Word模版生成最终docx/pdf周报。当用户说"生成XX日期的周报"、"生成本周周报"、"周报自动化"、"run weekly report for YYYYMMDD"时触发。
---

# 多资产投资部产品运作周报 - 端到端自动化

## 前置条件

1. **Wind终端已登录** (业绩基准计算需要)
2. **Python环境** - pandas, numpy, openpyxl, openai, pyarrow, WindPy, playwright, lxml
3. **LibreOffice已安装** - `brew install --cask libreoffice` (PDF生成需要)
4. **数据文件已就位** - 本周的产品净值、业绩指标、运作概览等原始文件已下载到 `~/Downloads` 或对应目录

## 执行流程概览

```
步骤1: 更新config日期 → 步骤2: Python数据处理管线(5个脚本)
→ 步骤3: 更新Excel链接工作簿 → 步骤4: Excel表格截图(含VLOOKUP解析)
→ 步骤5: 组装Word文档 + 生成PDF
```

## 步骤 1: 解析日期并更新配置

从用户输入中提取报告日期 (格式: `YYYYMMDD`)。

**更新 config.py:**
```python
# /Users/fanshengxia/Desktop/周报V2/config.py 中第46行左右
YUNZUOGAILAN_DATE = 'YYYYMMDD'  # 改为用户指定的日期
```

其他日期 (LASTW, LASTM, LASTY, WEEK_MON 等) 由 Config 类从此日期自动计算，无需手动改。

**验证:** 改完后用 Python 快速验证日期计算:
```bash
cd /Users/fanshengxia/Desktop/周报V2 && python -c "from config import Config; print(f'报告日期:{Config.YUNZUOGAILAN_DATE}, 上周:{Config.LASTW}, 上月:{Config.LASTM}')"
```

## 步骤 2: 运行 Python 数据处理管线

按顺序执行5个脚本。可使用主控脚本一键运行，也可逐个执行:

### 方式 A: 一键执行 (推荐)
```bash
cd /Users/fanshengxia/Desktop/周报V2
echo "y" | python run_weekly_report.py
```

### 方式 B: 逐步执行
```bash
cd /Users/fanshengxia/Desktop/周报V2

# 2.1 移动数据源文件到正确目录
python move_files.py

# 2.2 AI产品分类 (新产品自动归类)
python update_new_product_catgoery.py

# 2.3 生成主结果表 + AI文字总结 (最核心的步骤，约5-15分钟)
python generate_report.py

# 2.4 计算业绩基准表现 (需要Wind API)
python calculate_all_benchmarks.py --date {ZHOUBAO_DATE}

# 2.5 收益预测 (合享/悦动稳享系列)
python yield_forecast.py
```

**输出文件:** `输出结果/输出结果{DATE}.xlsx` (含40+个sheet)

**验证:** 确认输出文件存在且包含关键sheet:
```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('/Users/fanshengxia/Desktop/周报V2/输出结果/输出结果{DATE}.xlsx', read_only=True)
print(f'Sheet数量: {len(wb.sheetnames)}')
print('关键Sheet:', [s for s in wb.sheetnames if '总结文字' in s or '资产大表' in s or '分渠道' in s])
wb.close()
"
```

## 步骤 3: 更新 Excel 链接工作簿

**目标:** 替代原来的VBA宏操作。用openpyxl直接更新 `周报生成工具_加权_调整兴动合兴系列.xlsm` 中所有外部文件引用路径。

**核心原理:** 工作簿中68个sheet通过VLOOKUP公式引用外部Excel文件。需要把公式中的旧日期替换为新日期。

### 3.1 读取链接数据表获取新旧文件路径

```python
import openpyxl

WORKBOOK_PATH = '/Users/fanshengxia/Desktop/周报V2/周报生成工具_加权_调整兴动合兴系列.xlsm'
wb = openpyxl.load_workbook(WORKBOOK_PATH, keep_vba=True)

# 从 链接数据表 sheet 读取旧路径(B列)和新路径(C列)
link_sheet = wb['链接数据表']
for row in link_sheet.iter_rows(min_row=2, max_col=3, values_only=False):
    old_path = row[1].value  # B列：旧文件路径
    new_path = row[2].value  # C列：新文件路径
    if old_path and new_path:
        # 更新B列为C列的值
        row[1].value = new_path
```

### 3.2 批量替换公式中的日期引用

遍历所有数据sheet，将公式中的旧日期替换为新日期:

```python
OLD_DATE = '20260129'  # 上一期日期 (从链接数据表旧路径中提取)
NEW_DATE = '20260205'  # 本期日期

for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and OLD_DATE in cell.value:
                cell.value = cell.value.replace(OLD_DATE, NEW_DATE)
```

### 3.3 更新周报生成流程 sheet 中的日期

```python
ws_flow = wb['周报生成流程']
# 更新B2 (当前日期) 和 B3 (上期日期)
ws_flow['B2'] = NEW_DATE
ws_flow['B3'] = OLD_DATE
```

**保存时必须 `keep_vba=True`** 以保留.xlsm中的VBA代码:
```python
wb.save(WORKBOOK_PATH)
```

## 步骤 4: Excel 表格截图 (已验证可用)

**核心脚本:** `/tmp/generate_excel_screenshots_v2.py` (~800行)

该脚本从VBA工作簿读取59个数据sheet，生成高保真HTML（保留Excel原始格式、合并单元格、颜色样式），解析VLOOKUP/IF/SUM等公式从外部文件获取数据，最后通过Playwright截图为PNG。

### 运行方式
```bash
python /tmp/generate_excel_screenshots_v2.py
```

### 关键技术实现

#### 4.1 外部文件映射 (externalLink顺序)

**重要:** `[1]`, `[2]`等编号对应xlsm zip中 `xl/externalLinks/` 的顺序，不是链接数据表行号:

```python
EXTERNAL_FILES = {
    1: '数据/合享承诺收益率.xlsx',                    # [1] = 合享承诺收益率 (静态文件)
    2: f'输出结果/输出结果{DATE}.xlsx',               # [2] = Python输出结果
    3: f'数据/产品运作概览数据-母子产品/产品运作概览信息表增加指标变化_{DATE}.xlsx',  # [3] = 运作概览
    4: f'数据/产品业绩指标数据/内部产品业绩_{DATE}.xlsx',  # [4] = 产品业绩
    5: f'数据/收益测算数据/丰利合享底表-{DATE}.xlsx',   # [5] = 合享底表
    6: f'数据/收益测算数据/悦动稳享底表-{DATE}.xlsx',   # [6] = 悦动稳享底表
}
```

#### 4.2 openpyxl 关键注意事项

**绝对不要用 `read_only=True`!** 它会创建 `EmptyCell` 对象，没有 `.row`/`.column` 属性，导致所有外部数据加载静默失败:
```python
# 错误 - EmptyCell没有row/column属性会导致崩溃
wb = openpyxl.load_workbook(path, read_only=True, data_only=True)

# 正确
wb = openpyxl.load_workbook(path, data_only=True)
```

#### 4.3 公式解析 (覆盖 ~30K/33K 公式)

支持的公式模式（按频率排序）:
- `IF($A2="","",VLOOKUP(...))` — 14,536个
- `VLOOKUP(lookup, '[2]Sheet'!$A:$Z, col, 0)` — 8,040个 (含全列引用)
- `IF([2]Sheet!$A4="","",[2]Sheet!$A4)` — 3,744个 (外部单元格引用)
- `SUM(B3:B10)` — 1,507个
- `IFERROR(VALUE(VLOOKUP(...)),fallback)` — 534个
- 简单算术 `+,-,*,/` — 212个

**多轮解析:** 公式之间有依赖关系（SUM依赖VLOOKUP结果），需要5轮迭代解析。

#### 4.4 HTML生成与截图

- 从openpyxl读取单元格格式（字体、颜色、对齐、合并）
- 生成精确匹配Excel样式的HTML table
- Playwright异步截图59个HTML文件 → 59个PNG (~30秒)

**输出:**
- HTML文件: `/tmp/weekly_report_html/` (59个)
- PNG截图: `/tmp/weekly_report_screenshots/` (59个)

### 截图填充率说明

部分sheet因公式复杂度限制，数据填充不完整（属正常现象）:
- 高填充率 (>90%): 产品规模、系列产品业绩、指数收益、投资经理维度等核心表格
- 中等填充率 (50-90%): 分渠道余额、最短持有期、狭义客户周期等
- 低填充率 (<50%): 到期情况表、中收监控、持仓明细等（含SUMPRODUCT等未解析公式）

## 步骤 5: 组装 Word 文档并生成 PDF (已验证可用)

**核心脚本:** `/tmp/assemble_word_report.py` (~500行)

### 关键技术要点

#### 5.1 python-docx 无法打开 .docm 文件

`python-docx` 打开 `.docm` 会报 `ValueError: content type is 'application/vnd.ms-word.document.macroEnabled.main+xml'`。

**解决方案:** 用 zipfile 方式将 `.docm` 转换为 `.docx`:
```python
import zipfile, re

def convert_docm_to_docx(docm_path, docx_path):
    """Strip VBA from .docm to create valid .docx"""
    vba_files = {'word/vbaProject.bin', 'word/vbaData.xml', 'word/_rels/vbaProject.bin.rels'}
    with zipfile.ZipFile(docm_path, 'r') as zin:
        with zipfile.ZipFile(docx_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.namelist():
                if item in vba_files:
                    continue
                data = zin.read(item)
                if item == '[Content_Types].xml':
                    content = data.decode('utf-8')
                    content = content.replace(
                        'application/vnd.ms-word.document.macroEnabled.main+xml',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml')
                    content = re.sub(r'<Override[^>]*vbaData[^>]*/>', '', content)
                    content = re.sub(r'<Default[^>]*Extension="bin"[^>]*/>', '', content)
                    data = content.encode('utf-8')
                elif item == 'word/_rels/document.xml.rels':
                    content = data.decode('utf-8')
                    content = re.sub(r'<Relationship[^>]*vbaProject[^>]*/>', '', content)
                    data = content.encode('utf-8')
                zout.writestr(item, data)
```

#### 5.2 书签操作 - 用 lxml 直接操作 OOXML

所有66个书签都是空书签（bookmarkStart和bookmarkEnd相邻），需要在两者之间插入内容。

**文字书签插入:**
```python
from lxml import etree
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# 构建 <w:r><w:t>text</w:t></w:r> 元素
run_xml = f'<w:r xmlns:w="..."><w:rPr><w:rFonts w:hint="eastAsia"/><w:sz w:val="21"/></w:rPr><w:t xml:space="preserve">{text}</w:t></w:r>'
run_elem = etree.fromstring(run_xml.encode())
bm_start.addnext(run_elem)
```

**图片书签插入:**
```python
# 1. 将PNG文件添加到docx zip的 word/media/ 目录
# 2. 在 word/_rels/document.xml.rels 添加 Relationship
# 3. 构建 <w:r><w:drawing><wp:inline>...</wp:inline></w:drawing></w:r> XML
# 4. 插入到 bookmarkStart 后面

# 图片尺寸: 按96 DPI计算EMU (1 EMU = 1/914400 inch)
emu_per_px = 914400 / 96  # = 9525
cx = int(px_width * emu_per_px)
cy = int(px_height * emu_per_px)

# 缩放到页面宽度 (A4: 11906 twips - 720*2 margins = 10466 twips content)
MAX_WIDTH_EMU = 10466 * 635  # ~6,645,910 EMU
if cx > MAX_WIDTH_EMU:
    scale = MAX_WIDTH_EMU / cx
    cx = MAX_WIDTH_EMU
    cy = int(cy * scale)
```

**多行文字处理:** 规模文字、中收文字、到期文字含换行符。第一行插入当前段落，后续行创建新段落（复制原段落样式但排除sectPr）。

#### 5.3 文字书签内容来源

| 书签名 | 内容来源 | 说明 |
|--------|----------|------|
| 首页日期 | 固定格式 | `2026年02月05日` |
| 到期日期 | 固定格式 | `2026年02月05日` |
| 规模文字 | 输出结果.xlsx → 总结文字 sheet B4 | AI生成的规模总结 |
| 中收文字 | 输出结果.xlsx → 总结文字 sheet B3 | AI生成的中收总结 |
| 到期文字 | 输出结果.xlsx → 总结文字 sheet B2 | AI生成的到期总结 |
| 市场文字 | 留空 | 通常需手动填写 |
| 目标盈 | 留空 | 通常需手动填写 |

#### 5.4 PNG content type

必须在 `[Content_Types].xml` 中添加PNG的Default:
```xml
<Default Extension="png" ContentType="image/png"/>
```

#### 5.5 生成 PDF

```bash
# LibreOffice headless (推荐，最可靠)
soffice --headless --convert-to pdf --outdir "输出结果/" "输出结果/多资产投资部产品周报-{DATE}.docx"
```

**注意:** Word for Mac 的 AppleScript `save as` 不工作（返回 -1708 错误）。JXA `exportAs` 可以执行但不一定生成文件。LibreOffice headless 是最可靠的方案。

### 运行方式
```bash
python /tmp/assemble_word_report.py
```

**输出:**
- DOCX: `输出结果/多资产投资部产品周报-{DATE}.docx` (~13MB)
- PDF: `输出结果/多资产投资部产品周报-{DATE}.pdf` (~12MB, ~57页)

## 项目路径

| 路径 | 说明 |
|------|------|
| `/Users/fanshengxia/Desktop/周报V2/` | 项目根目录 |
| `config.py` | 配置文件 (日期、参数) |
| `run_weekly_report.py` | Python主控脚本 |
| `周报生成工具_加权_调整兴动合兴系列.xlsm` | Excel VBA工作簿 (68 sheets) |
| `多资产投资部产品周报-模版.docm` | Word模版 (66个书签) |
| `输出结果/` | 所有输出文件目录 |
| `数据/` | 所有源数据目录 |
| `/tmp/generate_excel_screenshots_v2.py` | 步骤4截图脚本 (~800行) |
| `/tmp/assemble_word_report.py` | 步骤5组装脚本 (~500行) |

## 关键数据文件

| 文件 | 说明 |
|------|------|
| `输出结果/输出结果{DATE}.xlsx` | Python输出 (40+ sheets) |
| `数据/产品运作概览数据-母子产品/产品运作概览信息表增加指标变化_{DATE}.xlsx` | 产品运作概览 |
| `数据/产品业绩指标数据/内部产品业绩_{DATE}.xlsx` | 业绩指标 |
| `数据/收益测算数据/丰利合享底表-{DATE}.xlsx` | 合享收益预测 |
| `数据/收益测算数据/悦动稳享底表-{DATE}.xlsx` | 悦动稳享收益预测 |
| `数据/合享承诺收益率.xlsx` | 合享承诺收益率 (静态文件) |

## 最终输出 (成功标志)

| 文件 | 格式 | 大小 |
|------|------|------|
| `输出结果/多资产投资部产品周报-{DATE}.docx` | Word文档 | ~13MB |
| `输出结果/多资产投资部产品周报-{DATE}.pdf` | PDF文档 (~57页) | ~12MB |

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| Wind未连接 | 跳过步骤2.4(业绩基准)，后续手动补充 |
| config日期格式错误 | 必须为YYYYMMDD格式，如20260205 |
| 数据文件缺失 | 检查Downloads中文件是否已下载，运行move_files.py |
| NAV缓存异常 | `python manage_nav_cache.py clear` 清除缓存后重试 |
| AI摘要生成失败 | 检查DeepSeek API key和网络连接 |
| openpyxl公式替换失效 | 确认旧日期字符串正确匹配 |
| openpyxl read_only=True崩溃 | **绝对不要用read_only=True**，EmptyCell没有row/column属性 |
| python-docx打不开.docm | 用zipfile方式剥离VBA后转为.docx再处理 |
| Word AppleScript save as失败 | 用LibreOffice headless: `soffice --headless --convert-to pdf` |
| LibreOffice未安装 | `brew install --cask libreoffice` |
| 截图公式数据缺失 | 部分复杂公式(SUMPRODUCT等)无法解析，属正常现象 |

## 参考文件

- **Excel Sheet→Word书签完整映射:** `references/bookmark_mapping.md`
- **PDF报告结构 (目录/章节/表格):** 参考最近的PDF `输出结果/多资产投资部产品周报-{LAST_DATE}.pdf`

## 示例

**用户:** "生成20260205的周报"

**执行:**
1. 更新 config.py: `YUNZUOGAILAN_DATE = '20260205'`
2. 运行 `run_weekly_report.py` (5个步骤)
3. 用 openpyxl 更新 Excel 链接工作簿日期引用
4. 运行 `/tmp/generate_excel_screenshots_v2.py` 截图59个表格
5. 运行 `/tmp/assemble_word_report.py` 组装Word (文字+图片→书签)
6. `soffice --headless --convert-to pdf` 导出PDF

**报告:**
```
已生成 20260205 周报

输出文件:
- DOCX: 输出结果/多资产投资部产品周报-20260205.docx (13MB)
- PDF:  输出结果/多资产投资部产品周报-20260205.pdf (12MB, 57页)

执行摘要:
- Python管线: 5/5 步骤成功
- Excel链接更新: 68 sheets, 6个外部文件引用已更新
- 表格截图: 59/59 完成 (含VLOOKUP公式解析)
- Word书签: 64/66 已填充 (市场文字和目标盈留空)
- AI文字总结: 规模/中收/到期 3段已生成
```
