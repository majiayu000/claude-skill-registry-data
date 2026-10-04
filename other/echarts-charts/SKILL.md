---
name: echarts-charts
description: Create interactive Apache ECharts charts and dashboard-ready HTML from Excel, CSV, JSON, tables, or pasted data. Use when Codex needs to make charts, visualizations, dashboards, ECharts options, interactive HTML charts, or convert analysis results into bar, line, pie, scatter, heatmap, radar, funnel, map, or combination charts.
---

# ECharts 图表生成

将结构化数据转换为可交互的 Apache ECharts 图表。默认交付单文件 HTML；用户在项目中开发时，按项目框架输出相应组件或 `option`。

## 工作流

1. 识别数据来源、字段含义、图表目标和交付形态。
2. 选择图表类型：
   - 趋势：折线图、面积图、双轴组合图。
   - 排名/对比：柱状图、条形图、堆叠柱图。
   - 构成：饼图、环形图、旭日图、矩形树图。
   - 相关性/分布：散点图、气泡图、箱线图、热力图。
   - 漏斗/流程/关系：漏斗图、桑基图、关系图。
3. 优先整理为 `dataset.source`，用 `encode` 映射字段。不要把同一份数据散落在多个 `series.data` 中，除非图表类型确实需要。
4. 生成 `option` 时包含：标题、图例、提示框、坐标轴、网格留白、数据缩放（长序列）、标签策略、颜色和导出工具箱。
5. 独立 HTML 交付时运行：

```bash
node scripts/render_echarts_html.mjs config.json output.html
```

6. 交付前用浏览器打开 HTML 验证：图表不空白、tooltip 可用、图例切换正常、中文不乱码、轴标签不严重重叠。
7. 若用户需要图片或报告嵌入，先生成 HTML，再用浏览器截图导出 PNG/PDF。作为 `html-report` 插件内置 skill 使用时，若浏览器或依赖缺失，先在插件根目录运行 `node scripts/bootstrap_html_report_deps.mjs`。

## 配置格式

`render_echarts_html.mjs` 接受：

```json
{
  "title": "图表标题",
  "subtitle": "可选副标题",
  "width": 1200,
  "height": 720,
  "theme": "default",
  "echartsUrl": "https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js",
  "option": {}
}
```

`option` 是标准 ECharts 配置对象。没有特殊要求时，使用 `references/option-patterns.md` 中的模板起步。

## 设计规则

- 默认使用浅色背景、清晰标题、紧凑网格和可读字号。
- 中文图表优先使用 `PingFang SC, Microsoft YaHei, sans-serif`。
- 类目超过 12 个时优先横向条形图或启用 `dataZoom`。
- 排名图默认按指标降序排序；时间序列默认按时间升序排序。
- 数值需格式化：百分比、金额、千分位和单位不要混淆。
- 不要用 3D 效果装饰普通业务数据。
- 对业务汇报类图表，颜色不超过 6 个主色；强调色只用于关键系列或异常值。

## 资源

- `scripts/render_echarts_html.mjs`：将 ECharts `option` 包装为可打开的单文件 HTML。
- `references/option-patterns.md`：常见图表类型的 ECharts 配置模板和选择建议。
- `references/official-links.md`：官方文档入口，遇到不熟悉的图表类型时优先查阅。
