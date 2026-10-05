---
name: ai-agent-consulting-delivery
description: "企业/高校承接 AI 智能体项目时出方案、报价、demo 的全流程。"
version: 1.0.0
metadata:
  hermes:
    tags: [ai-agent, consulting, proposal, pricing, demo]
    category: business
---

# AI 智能体项目交付（方案→报价→Demo）

接到"帮我把 AI Agent 项目做成方案/报价/演示"这类需求时的完整流程。适用于商业公司、学校实验室、导师项目等多种承接主体。

## 流程总览

1. **需求解析** — 读需求文档（docx 用 read_file 自动提取；PDF 用 `uv run --with pdfplumber`，`extract_tables()` 取表格）
2. **方案 docx** — docx-js 生成（见下方坑），渲染验证
3. **报价调研** — web_search 市场行情 → 按承接主体套用报价模型
4. **Demo** — 模拟数据 + 脚本真实跑一遍，产出可交付物
5. **交付** — 产物放用户 Windows 可见目录（/mnt/e/...），附演示话术

## 方案 docx 生成（docx-js）

```bash
npm install docx   # 在 /tmp 或项目目录
node gen_plan.js   # 生成 .docx
# 验证渲染:
soffice --headless --convert-to pdf plan.docx --outdir /tmp/prev
pdftoppm -jpeg -r 100 /tmp/prev/plan.pdf /tmp/prev/page
# 然后用 vision_analyze 逐页检查表格/中文/跨页
```

**坑（docx 9.x）：**
- `TableRow` 跨页重复表头用 **`tableHeader: true`**，不是 `header`（9.x 改名，`header` 静默无效）。数据行加 `cantSplit: true` 防行内拆分
- 验证 tblHeader 是否写入：`unzip -p plan.docx word/document.xml | grep -o tblHeader | wc -l` 应等于表格数
- 表格：`columnWidths` 总和 = 表格宽（DXA），每格也要 `width`
- 中文：默认字体设 `Microsoft YaHei`，页脚页码用 `docx.PageNumber.CURRENT`
- 大量 TableRow 批量改写用脚本时容易误伤函数定义和 PageBreak 行——改完先 `node --check` 再跑
- PDF 预览（LibreOffice）表头重复可能不显示，但 Word 打开正常——以 document.xml 的 tblHeader 为准

## 报价模型（2026 国内行情，已调研）

| 层级 | 价格 |
|---|---|
| 基础型 Agent | 3–8 万（单任务，2-4 周） |
| 进阶型 | 15–40 万（多 Agent + 定制 UI，2-3 月） |
| 企业级 | 50–150 万+（私有化 + 微调 + 系统集成） |
| RPA 流程开发 | 7–35 万/流程 |
| 人天单价 | ~1500 元/人/天 |

**高校横向课题模式**（学校/导师承接时）：
- 合理区间 **10–18 万**，甜点 **12–15 万**（比市场低 30-50%）
- 管理费学校计提 4-6%（各校不同）；**软件类劳务费比例最高可到 80%**（学生团队主力）
- 技术开发合同经认定**免增值税**
- ≥10 万才立项为院级横向课题（低于此导师攒不到科研业绩）
- 定价逻辑：学生劳务 60% + 导师指导 15% + 设备/API 10% + 管理费 6% + 结余 9%
- 内部项目（集团→旗下学校）报太高显没诚意，报太低没价值

**给导师/甲方话术模板：** 报 12-15 万走横向课题，分期 50/50，注明比市场低 30-50%、成果沉淀软著/论文、二期（系统对接）另行立项。

## Demo 制作模式

用模拟数据真实跑一遍核心场景，产出三个东西：
1. **分析脚本**（pandas + matplotlib）：读 CSV → 算指标 → 识别风险 → 出图
2. **简报 docx**：python-docx 从 markdown 转（无 pandoc 时），嵌图表
3. **HTML 看板**：自包含单文件（KPI 卡片 + 漏斗 + 表格 + 预警横幅），浏览器截图存 output/看板截图/

**matplotlib 中文（WSL 无文泉驿时）：** `fc-list :lang=zh file` 找字体 → `font_manager.addfont(path)` → `plt.rcParams["font.family"] = 字体名`；`matplotlib.use("Agg")`

**模拟数据要点：** 贴合真实需求字段（学校/省份/专业/计划数/完成数/就业率），数值分布制造真实感（要有低于预警线的风险项，demo 才有说服力）。

## 交付检查

- 每个产物真实跑通（有 tool output 背书），不交"看起来做了"的东西
- 微信可直接发的：docx + 截图（HTML 需截图才能发）
- 附 README：怎么跑 + demo 对应方案哪个角色 + 与正式版差距
- 给用户的演示话术：3-4 句讲清"数据进→自动分析→出报告"和"逾期自动催办"这类核心卖点
