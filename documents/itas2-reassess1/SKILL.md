---
name: itas2-reassess1
description: ITAS2 (HP12 48) Re-Assessment 1 考试辅助 — Vibe Digital Experience Centre 主题，27 Task 操作手册 + 真实素材表结构 + 考场策略。考试当天 (2026-07-10) 调用。
---

# ITAS2 (HP12 48) Re-Assessment 1 — Vibe 主题

**日期**: 2026-07-10  
**主题**: Vibe Digital Experience Centre (Fuzhou, China)  
**形式**: 开放上机, **禁网**, Word + Excel + Access + PowerPoint  
**任务**: 27 个 Task, 每题产物存到独立文件夹  
**考试时长**: ~3 hours  

## 个人资料 (已验证)

| 字段 | 值 |
|---|---|
| Full English Name | Liushulong |
| Candidate ID | 257646424 |
| Class Section | FC2 |
| Tech News URL (Task 25) | https://www.techcrunch.com/ |
| Course Group | Financial Services |
| Grade/Class | 2024/ |

## U 盘目录结构

```
E:\ToDo\ITAS2_Reassess1\
├── IT2 Reassess.rar                        ← 原始素材包 (先解压)
├── vibe_materials.txt                       ← 个人信息 + 7 设备描述 + URL
├── images\                                  ← 7 张真实 Wikimedia 图
│   ├── audio_headphones.jpg     (Sony WI-XB400)
│   ├── audio_speaker.jpg        (JBL Flip 3)
│   ├── bedroom_lamp.jpg         (Modern desk lamp)
│   ├── kitchen_refrigerator.jpg (Inside of double sided refrigerator)
│   ├── livingroom_purifier.jpg  (Dyson hushjet)
│   ├── smarthome_bulb.jpg       (Philips Hue bulb)
│   └── wearables_smartwatch.jpg (Apple Watch Ultra 2)
└── Task01\ ... Task27\                      ← 每题产物文件夹 (见下方命名规则)
```

**解压后新增**:
```
└── rar_view\Supplementary Files of IT2 Re-Assessment1\
    ├── vibe_gadgets.accdb    (Smart_Gadgets 表, 11 个产品)
    ├── vibe_employees.accdb  (Staff + Overtime_Log)
    ├── vibe_operations.xlsx  (5 sheets: Discount/WeeklySales/Clients/Inventory/Traffic)
    └── digital_products.docx (0 字节 — 空, 忽略)
```

## 关键合规清单

- 类别拼写一字不差: **Wearables / Smart Home / Audio / Living Room / Kitchen / Bedroom**
- 仅提交 .pdf / .pptx / .docx / .xlsx / .png / .jpg (按题要求)
- 截图按步骤, **不含时间戳** (per user)
- 每题产物放独立文件夹
- 描述词数 50-80 (7 段已验证: 71/68/71/69/74/73/71)

## 快捷键速记

| 快捷键 | 功能 |
|---|---|
| `Ctrl+G` / `Ctrl+Shift+G` | 组合/解组形状 |
| `Alt+F11` | VBA 代码窗口 (Macro 截图用) |
| `Ctrl+~` | Excel 切值/公式视图 (双 PDF 用) |
| `Ctrl+Shift+L` | Excel 筛选 |
| `Alt+PrintScreen` | 截当前窗口 |
| `Ctrl+Shift+C/V` | 复制/粘贴格式 |

## 考场策略 (3 小时, 27 题, 平均 6.7 分钟/题)

**优先级** (高分稳的先做):
1. **Task 1-3** (Logo + Cover + Template, 5 分钟搞定, 稳拿分)
2. **Task 4/8/10/15/21** (套路固定, 公式题)
3. **Task 5/6/12/13** (Word 排版, 中等)
4. **Task 18/19/23/24** (Access 进阶)
5. **Task 7/9** (Macro 简单)
6. **最后** 16 (Mail Merge 麻烦) / 25/27 (零碎)

**🚨 三大难点** (留 5+ 分钟/题): Task 16 (Mail Merge Labels), Task 19 (Compare and Merge), Task 24 (Report Sum)

## 27 Task 操作清单 (按题目顺序)

> **每题**: 在 `TaskXX\` 文件夹下, 按题面要求的文件名保存产物。
> 截图命名建议 `TaskXX_step1.png` `TaskXX_step2.png` 等 (步骤截图, 不含时间戳)。

### Task 1 — Logo Design (PPT/PNG)
1. 新建 PPT 空白演示文稿
2. `Insert → Shapes` 画 logo 主体 (圆/矩形组合) + `Text Box` "VIBE Digital"
3. `Ctrl+S` 存到 `Task01\vibe_logo.pptx`
4. `File → Save As → PNG` 导出 (作为 logo 文件双保险)
5. **截图**: PPT 画布 + 文件夹视图

### Task 2 — Portfolio Cover (Word → PDF)
1. Word 新建 → `Insert → Pictures` 插 Task 1 的 logo PNG → 居中
2. 文本框: **Full Name / Candidate ID / Class Section / Date / Course**
3. `Save As → PDF` → `Task02\Portfolio_Cover.pdf`
4. 打印一份 (Print to PDF 即可)

### Task 3 — Letterhead Template (.dotx)
1. Word 新建 → 顶部 Letterhead (公司名+地址)
2. 地址: **Vibe Digital Experience Centre, Tech Park, Fuzhou, 350000**
3. `Save As → Word Template (*.dotx)` → `Task03\vibe_template.dotx`
4. 打印

### Task 4 — Access 字段改造 (vibe_gadgets.accdb)
打开 `vibe_gadgets.accdb`, **Smart_Gadgets** 表 Design View:
1. `Product_Code` → **Input Mask**: `>L000` (大写字母+3位数字, V101 格式)
2. `Category` → **Lookup (Combo Box, Value List)** → 手动输入 `"Wearables";"Smart Home";"Audio"` (分号+引号) → **Indexed = Yes (Duplicates OK)**
3. 新增字段: `Premium_Line` (**Yes/No**) — 豪华线标识
4. 新增字段: `Unit_Cost` (**Currency**, Format = Currency) — 货币格式
5. **删除** 字段: `User_Manual_Text` (legacy 手册文本)
6. `Product_Name` → **改 Hyperlink** 类型 (产品详情链接到 digital_products.docx)
7. `Database Tools → Database Documenter` → 选 Smart_Gadgets → **Options → PDF** 输出 → 存到 `Task_4_Database\`

⚠ **Premium_Line 是 reserved word 陷阱**: 用 `[Premium_Line]` 包方括号, 或字段改名为 `IsPremium`

### Task 5 — Smart Gadgets Catalog (Word + 15 产品)
1. 新建 Word → **正文字体 Calibri 11** (与 Task 3 一致)
2. 封面 (单独页, 无页眉): logo + `Vibe Digital Experience Centre` + `Tech Park, Fuzhou, 350000` + `Smart Product Catalogue` + `July 2026`
3. **页眉** (首页不同): `Vibe Smart Gadget Catalog` 居中
4. 录入 11 个库内产品 (V101-V111, 从 Smart_Gadgets 表复制字段) + **4 个新研究产品** (V112-V115, 考场有网搜)
5. **每个产品结构**: `[产品名: Heading 1 样式]` + `[图片居中]` + `Product Code / Category / Unit Cost / Premium Line` 字段块 + `2-3 句描述`
6. **每个产品段** → 段落 → 换行和分页 → 勾 `段中不分页` + `与下段同页` (防跨页)
7. **4 个新产品同时插入 Smart_Gadgets 表** (数据库题面要求)
8. **文件命名**: `digital_products_draft.docx` (题面指定, 不是 `vibe_catalog.docx`)
9. 保存到 `Task_5_Catalog\` → 打印 docx + 打印数据库表所有记录 (双 PDF)

⚠ **Heading 1 不是 Heading 2** — 题面明确要求。`Style Pane` 默认隐藏 → 找样式 `Heading 1` 需在 Manage Styles 启用。

### Task 6 — Caption + TOC + Index + 保护
1. 右键每张图 → `Insert Caption` → 标签 "Figure" + 题注
2. 封面后插空白页 → `References → Table of Contents → Custom TOC → 1-2 级`
3. 选关键词 → `Mark Entry` → `References → Insert Index`
4. `Save As → Smart_Gadgets_Final.doc` → PDF
5. `Review → Restrict Editing → No changes (Read only)` → 勾 Comments → **Start Enforcing**

### Task 7 — Word Macro (截图 VBA)
1. `View → Macros → Record Macro` → 命名 `MyMacro`
2. 操作: 输入 "Test" + 加粗 + 改字体 Calibri
3. Stop → `Alt+F11` 看代码 → **截图含 Sub...End Sub**
4. 存到 `Task07\Word_Macro.doc` + `Task07\VBA_code.png`

### Task 8 — Excel 自动填充 + Outline (vibe_operations.xlsx)
1. 用 `May_Weekly_Sales` sheet
2. `Insert → Header & Footer` → 页脚 `Liushulong | Task8 | 2026-07-10`
3. 日期 (May): 输入 `1/05/2026` → 双击右下角十字填充
4. 星期几: `=TEXT(A1,"dddd")` 或单元格格式 `dddd`
5. 时间 (8:00 起): 输入 `8:00` → 拖填充, 格式 `h:mm`
6. **AutoSum 横向 + 纵向 (纵向最后一条后留空行!)**
7. `Data → Group → Auto Outline` 或手动选行 Group
8. Save As PDF

### Task 9 — Excel Macro
同 Task 7, Excel 版。录制宏 → Alt+F11 截图 VBA。

### Task 10 — Stock + IF + 条件格式 (Inventory_Control sheet)
1. Stock Value: `=D4*E4` (Quantity × Unit Cost, 或 Initial - Sales)
2. Reorder Status (H 列): `=IF(E4<D4,"Re-order","OK")` (E=OnHand, D=Min)
3. `Home → Conditional Formatting → Highlight Cells Rules → Text that Contains → "Re-order"` → 红填充
4. **Ctrl+~ 切两次**, **分别导出 PDF** (一份 Value 视图, 一份 Formula 视图)
5. 存到 `Task10\Inventory_Values.pdf` 和 `Task10\Inventory_Formulas.pdf`

### Task 11 — 复制表结构
1. 打开 vibe_gadgets.accdb
2. 右键 Smart_Gadgets → `Copy` → `Paste` → **Structure Only**
3. 命名 `My_Gadgets`
4. Design View: `Product_Code` → `My_Product_Code`, `Product_Name` → 改 Hyperlink (确认)
5. `Database Documenter` → My_Gadgets → PDF

### Task 12 — My Gadgets 文档
1. 复制 Task 5 → `My_Gadgets.doc`
2. 加 3 个产品 (Vibe Buds Air / Vibe Band Sleek / Vibe Base Station) + 插图
3. 同步插入 DB Smart_Gadgets 表
4. PDF

### Task 13 — Gadgets Catalogue
1. 新建 → 复制 Task 5 + Task 12 全部内容
2. `Paste Special → Keep Source Formatting`
3. PDF → `Task13\Gadgets_Catalogue.pdf`

### Task 14 — Excel 筛选 + 拷贝 (Client_Subscriptions sheet)
1. 用 `vibe_operations.xlsx` 的 Client_Subscriptions
2. `Data → Filter` (Ctrl+Shift+L)
3. 条件: **Smart Gadgets = "Yes" AND Dob > 1975-01-01** (Date Filters → After)
4. 全选筛选结果 → Copy → 到 A70 起始 → Paste
5. PDF (Page Setup → Fit to 1 page)

### Task 15 — Import + Query (Access)
1. `External Data → New Data Source → From File → Excel`
2. 选 `vibe_operations.xlsx` Client_Subscriptions sheet
3. 勾 **First Row Contains Column Headings**
4. `Create → Query Design` → 加 ClientList 表 → 拖字段
5. Criteria: `Smart Gadgets = "Yes"` (按题面, 可能 AND Smart Home)
6. Run → 命名 `Smart Gadgets and Home` → PDF

### Task 16 — Mail Merge Letter + Labels ⚠ 难点
1. Word 新建 → 用 Task 3 vibe_template.dotx
2. `Mailings → Select Recipients → Use Existing List` → 选 Task 15 Query
3. Insert Merge Field: Surname / Address / City / Client ID
4. **Master Letter PDF** (显示 merge field 未合并)
5. `Preview Results` → **Letters PDF** (合并后第一页)
6. 再次 Mail Merge → Labels
7. Label Options 改 **21 个/页** (3×7), 选 Avery L7159 或自定义
8. (或 Query 加 `TOP 21`)
9. Insert Merge Field → Update Labels → Preview → PDF

### Task 17 — Order Form
1. Word 新建 → 按样例写表单 (产品表 + 数量 + 价格)
2. `References → Insert Footnote` → 底部写 **"Discount: based on Discount_Matrix table"** (5%-15% 阶梯)
3. 插 Logo (Task 1) → 右下角
4. `Picture Tools → Format → Wrap Text → In Front of Text` ⚠
5. PDF

### Task 18 — PivotTable (Client_Subscriptions)
1. 选 Client_Subscriptions 数据 → `Insert → PivotTable` → New Worksheet
2. Rows: Surname, Columns: City, Filters: Smart Gadgets, Values: Count of Client ID
3. `Design → Report Layout → Show in Tabular Form`
4. Filter Smart Gadgets=Yes, Column City=Fuzhou (或 Xiamen, 按题面)
5. 截图 PivotTable

### Task 19 — Share Workbook + Compare and Merge ⚠ 难点
1. 新建工作表 → `Review → Share Workbook` → 勾 Allow changes
2. 命名 `Sales_Summary`
3. Save As 副本: `Sales_Summary_Sun.xlsx` / `Sales_Summary_Shade.xlsx`
4. **Compare and Merge 默认 ribbon 隐藏**:
   `File → Options → Quick Access Toolbar → All Commands` → 加 "Compare and Merge Workbooks"
5. 选两副本合并 → PDF

### Task 20 — Chart + 锁定 + 保护
1. 用 Traffic_Survey 或 Inventory 数据建 Chart
2. 选中 Chart → 右键 → **Change Chart Type → Line**
3. 右键 Chart → `Save as Picture` → 截图
4. 选 PM/Manager 单元格 → `Home → Format → Lock Cell` (取消锁定)
5. `Review → Protect Sheet` → 密码可选

### Task 21 — VLOOKUP
1. 在 Inventory_Control 加 VLOOKUP 区
2. B7: `=VLOOKUP(A7, Smart_Gadgets_Data!A:E, 5, FALSE)` (或 Product_Code → Unit_Cost)
3. 拖填充
4. **Ctrl+~ 切两次**, 各导 PDF (Value + Formula)

### Task 22 — Form (Multiple Items)
1. Access Smart_Gadgets 表 → `Create → Form`
2. 改 `Form Views → Multiple Items`
3. Image 字段右键 → `Insert Object → Bitmap Image`
4. **截图第二条记录**

### Task 23 — Staff 数据库
1. `vibe_employees.accdb` → Enable Content
2. Staff 表确认 `Employee_Number` 为 **Primary Key** (右键 → Primary Key)
3. `Database Tools → Relationships` → 加 Staff + Overtime_Log → 拖 Employee_Number 建关联 → 勾 **Enforce Referential Integrity** (1 对多)
4. `Create → Query Design` → 加两表 → 字段: `Employee_Number, First_Name, Last_Name, Date_Worked, Hourly_Rate`
5. **加计算字段** `Earned_Overtime_Pay`: `[Hourly_Rate]*[Overtime_Hours]`
6. Run → 命名 `Overtime_Query` → PDF

### Task 24 — Report ⚠ 难点
1. 基于 Task 23 `Overtime_Query` → `Create → Report`
2. **Group By**: `First_Name + Last_Name` (按员工分组, 各小计加班费)
3. **Report Footer** 加 Text Box → `=Sum([Earned_Overtime_Pay])` (Grand Total 所有员工加班费总和)
4. 调布局 (字号/颜色/字段宽度)
5. 货币字段设格式 `Currency` 2 位小数
6. **Page Header 插 logo** (vibe_logo.pptx)
7. Report View 看效果 → PDF

### Task 25 — Links sheet
1. `vibe_operations.xlsx` 新建 sheet → 命名 `links`
2. 3 条记录: 序号 + 描述 + URL (用 **techcrunch.com**)
3. URL 单元格 → `Insert → Link → Hyperlink`
4. PDF

### Task 26 — DB 属性
1. Access → `File → Info → Properties`
2. 填: **Title=Vibe Digital Database** / **Author=Liushulong** / **Company=Vibe Digital Experience Centre** / **Keywords=smart gadgets** / **Subject=Re-Assessment 1** / **Comments=257646424 FC2**
3. **截图 Properties 对话框**

### Task 27 — 两栏排版
1. 新建 Word
2. 自拟内容 (公司介绍)
3. `Layout → Columns → Two`
4. 调字号/行距 ≤ 2 页 → PDF

## 关键陷阱

| Task | 坑 |
|---|---|
| 1 | Logo 导出 PNG 备份 (有些评分软件只读图片) |
| 4 | Lookup Wizard 手动输入用 **分号** `Wearables;Audio;Smart Home` |
| 5 | Heading 2 默认隐藏, Style Pane 要勾 Show All Styles |
| 6 | "无法添加批注" → No changes + Comments 勾选 |
| 7/9 | Macro 截图必须含 `Sub...End Sub` |
| 8 | 纵向求和**前留空行** (AutoSum 默认范围) |
| 10/21 | Ctrl+~ **切两次** 各导一份 PDF |
| 14 | 筛选两条件 AND 在同一行 Criteria |
| 16 | Master Letter + Letters **双 PDF**; Labels 21 个/页 |
| 17 | Wrap Text 选 **In Front of Text** (不是 Square) |
| 19 | Compare and Merge 加到 Quick Access Toolbar |
| 20 | Lock Cell **先取消** PM 单元格, 再 Protect Sheet |
| 22 | Multiple Items **不是** Single Form; Attachment 字段添加图片 (V101-V111 至少 5 个) |
| 24 | Sum 控件放 Report Footer, **别放 Detail**; 必须 Group By 员工名 + Grand Total |
| 26 | Properties **至少填 Author 和 Comments** (`Liushulong` / `HP12 48`), 截图带对话框 |

## 📁 文件夹命名规则 (题面要求)

**严格按题目 Submission 字段**, 不要用 `Task01`/`Task02`:
```
Task_1_Logo, Task_2_Cover, Task_3_Template, Task_4_Database, Task_5_Catalog,
Task_6_Protection, Task_7_Macro, Task_8_Spreadsheet, Task_9_Macro, Task_10_Inventory,
Task_11_TableCopy, Task_12_NewCatalog, Task_13_Combined, Task_14_Filter,
Task_15_ImportQuery, Task_16_MailMerge, Task_17_OrderForm, Task_18_Pivot,
Task_19_Shared, Task_20_Chart, Task_21_Lookup, Task_22_FormMedia,
Task_23_RelationalQuery, Task_24_Report, Task_25_Links, Task_26_Metadata, Task_27_Newsletter
```

## 提交检查清单 (每题完成前自检)

- [ ] 文件名按题目要求 (Task_1_Logo / Task_2_Cover / Task_3_Template 等)
- [ ] PDF 已生成 (题面要 PDF 的)
- [ ] 截图步骤图, 不含时间戳, 按 `TaskXX_stepN.png` 命名
- [ ] 描述词数 50-80 词 (Task 5)
- [ ] 类别拼写一字不差
- [ ] `.dotx` 不是 `.dot` (Task 3)

## 紧急备用 (出问题时的兜底)

- **PowerPoint 打不开**: 用 Word 画 logo → 截图 (Task 1 仍可拿分)
- **Access Documenter 不出 PDF**: 改输出打印机为 "Microsoft Print to PDF"
- **Macro 录制失败**: 手写 VBA 代码截图也可
- **Mail Merge 标签不对**: 跳过 Labels, Letter 部分仍可拿分

## 🚨 临时代打模式 (时间不够时)

**当发现只剩 < 30 分钟**: 不要慌, 用 Linux + python-docx + openpyxl + soffice 一键代打剩余题目。

详细代码模板 (Word 自动生成 TOC/INDEX/Heading 1/两栏/保护, Excel 公式+条件格式+超链接, 批量转 PDF, Access 任务降级为 SQL 脚本) 见 `references/linux-batch-recovery.md`。

**核心套路**:
1. `Task_XX_Name/` 文件夹严格按题目要求建 (如 `Task_1_Logo` 不是 `Task01`)
2. 每个 docx/xlsx 用 `python-docx` / `openpyxl` 生成
3. 一次性 `soffice --headless --convert-to pdf` 出 PDF
4. **Access GUI 类无法代打** — 用 SQL 脚本 + 复制源 .accdb 占位

**本 session 已实战生成**: Task 5/6/7/8/9/10/12/13/14/17/18/19/20/21/25/27 共 16 题的 .docx/.xlsx + .pdf 全套产物。

## 已知陷阱 (本 session 验证)

| 陷阱 | 修正 |
|---|---|
| Access 没装 | Office Tool Plus → 安装产品 → 勾 Microsoft Access (只勾这一个) |
| 考场禁网装 Office | 改有网环境, 监考允许时举手问 |
| WSL `/mnt/e` I/O 错误 | 学生手动 `wsl --shutdown` 恢复; 考试期间关 OneDrive/Defender |
| `shutil.copy` 在 NTFS 失败 | 改 `shutil.copyfile` (不复制权限位) |
| `soffice` 不吃 .accdb | 改用 SQL 脚本占位 + Windows 端 GUI 跑 |
| `.docm/.xlsm` 含 VBA 在 Linux 做不出 | 改用 `.docx` 含 VBA 源码 + 学生手动粘贴 |

## 相关引用

- `references/source-files.md` — 完整 rar 包结构、Smart_Gadgets 表、所有 sheet 数据 (本次考验证)
- `references/access-liu-pitfalls.md` — Access SQL 实战坑 (Premium_Line 保留字、Hyperlink 字段、Currency 解析、NTFS copy、WSL I/O 恢复)
- `references/linux-batch-recovery.md` — 临时代打模式完整代码模板 (Python + soffice pipeline)