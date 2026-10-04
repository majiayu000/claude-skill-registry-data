---
name: generate-word-clouds
description: Generate one or multiple weighted keyword word-cloud PNG images with confirmed brand colors, Top N selection, transparent or colored backgrounds, compact margins, horizontal text, and selectable shapes. Use when the user asks to create 词云、关键词云、品牌词云 or batch word clouds from Excel, CSV, JSON, tables, or pasted keyword lists; supports up to 10 lists per run.
---

# 品牌词云生成

将关键词及权重生成紧凑、可复用的 PNG 词云。默认输出横排文字、透明背景、椭圆形和四周 20px 边距。

## 工作流

1. 读取关键词数据并识别每个列表的名称、关键词列和权重列。Excel 优先运行 `scripts/extract_xlsx.py`，不要临时编写转换脚本或用重量级工作簿渲染工具读取。
2. 最多接受 10 个列表；超过时请用户拆分批次。
3. 查询尚未缓存的品牌配色后，一次性确认最终配置：

```text
请确认词云配置：
- 配色：品牌名、候选官方色值及来源 / 用户指定色值
- 关键词数量：Top 50
- 底色：透明
- 形状：椭圆
- 输出列表：列表名称（共 N 个）
```

若用户已明确其中部分配置，只确认尚未明确的项目并展示最终汇总。每个任务最多请求一次配置确认；用户明确说“按默认”“直接生成”或“无需确认”时可直接执行。

4. 配色为品牌名时，先查 `references/brand_palettes.json`。存在已核验记录时直接复用并展示来源；没有记录时才联网查询品牌官网、官方品牌手册或官方媒体资料，只采用官方来源。将新结果写入缓存，记录来源、提取依据、日期和 3–6 个十六进制色值。若官方色值无法可靠取得，说明情况并请用户提供颜色；不得把第三方取色结果声称为官方配色。
5. 按权重降序取 Top N。默认值：
   - Top N：50
   - 底色：透明
   - 形状：椭圆
   - 边距：20px
   - 文字方向：全部从左到右水平排列
6. Excel 输入先运行快速提取器，再运行生成器：

```bash
python scripts/extract_xlsx.py input.xlsx config.json --top-n 50 \
  --palette-file references/brand_palettes.json
node scripts/generate_word_clouds.mjs config.json output-directory
```

提取器同时接受 `{列表名: [色值...]}` 映射或 `brand_palettes.json` 的缓存格式。作为 `html-report` 插件内置 skill 使用时，若依赖缺失，先在插件根目录运行 `node scripts/bootstrap_html_report_deps.mjs`，让 `sharp` 和 `openpyxl` 可用。CSV、JSON 或粘贴数据可直接整理成生成器配置。

7. 用一个批次检查所有输出，不为每张图重复启动检查流程：
   - 文件为 PNG，透明底时必须含 Alpha 通道。
   - 所有词均为水平文字。
   - 实际内容与画布四边均为 20px；非透明底以背景画布边界为准。
   - 输出词数等于 `min(Top N, 有效关键词数)`。
   - 中文无乱码、文字无重叠、主要关键词层级清楚。
8. 向用户展示预览、下载链接、实际输出词数和品牌配色来源。

## 输入整理

脚本配置格式：

```json
{
  "margin": 20,
  "lists": [
    {
      "name": "品牌A",
      "topN": 50,
      "background": "transparent",
      "shape": "ellipse",
      "palette": ["#7A1F2B", "#C68A1D", "#E1B84B"],
      "words": [
        {"text": "关键词", "weight": 100}
      ]
    }
  ]
}
```

支持的 `shape`：`ellipse`、`circle`、`rectangle`、`diamond`。支持的 `background`：`transparent` 或 `#RRGGBB`。同一关键词重复出现时先合并权重；删除空关键词和非正数权重。

## 排版原则

- 保持全部文字水平，不允许旋转。
- 字号采用对数缩放，避免头部词过度挤压尾部词。
- 优先保证 Top N 全部出现；必要时缩小整体字号后重排。
- 颜色按调色板循环使用，同时避免最大关键词全部使用同一颜色。
- 透明背景只包含词云，不添加标题、来源、边框或装饰。
- 文件名使用安全化后的列表名称加 `_TOP{N}_词云.png`。

## 资源

- `scripts/generate_word_clouds.mjs`：确定性批量词云生成器。
- `scripts/extract_xlsx.py`：快速识别 Excel 工作表、关键词列和权重列并生成配置。
- `references/confirmation.md`：确认话术和品牌配色来源规则。
- `references/brand_palettes.json`：已核验的官方素材配色缓存；命中时避免重复联网取色。
