---
name: work-report
description: 生成工作汇报PPT。使用python-pptx库创建演示文稿，用于生成工作周报、月报、项目汇报等。第一页标题用宋体48号，内容页标题36号，正文18号，总页数控制在10页以内，最后一页为"谢谢观看"。
---

# Work Report PPT Generator

使用 Python python-pptx 库生成工作汇报演示文稿。

## 输出文件

PPT 保存到：`~/Documents/工作汇报_<日期>.pptx`

## 使用方法

### 基本命令
```bash
python3 ~/Desktop/github/openclaw/skills/work-report/scripts/generate_ppt.py \
  --title "本周工作汇报" \
  --sections "项目进展:完成了用户登录功能开发|问题与挑战:后端接口响应慢|下周计划:优化接口性能" \
  --output ~/Documents/my_report.pptx
```

### 参数说明

- `--title`: 汇报标题（必填）
- `--sections`: 内容板块，格式为"板块名:内容|板块名:内容"
- `--output`: 输出文件路径（可选，默认 ~/Documents/工作汇报_日期.pptx）

### 内容格式

```
板块名1:板块内容的第一段|板块名1:板块内容的第二段
板块名2:板块内容
```

用 `|` 分隔同一板块的多段内容，用 `:` 分隔板块名和内容。

## 示例

### 生成周报
```bash
python3 ~/Desktop/github/openclaw/skills/work-report/scripts/generate_ppt.py \
  --title "第12周工作汇报" \
  --sections "本周完成:完成了用户管理模块的开发|本周完成:修复了5个已知bug|遇到问题:测试环境数据库连接不稳定|下周计划:完成订单管理模块开发|下周计划:准备UAT测试"
```

### 生成项目汇报
```bash
python3 ~/Desktop/github/openclaw/skills/work-report/scripts/generate_ppt.py \
  --title "XX项目进度汇报" \
  --sections "项目概况:项目总进度60%，团队5人|本周进展:完成核心功能开发，进入测试阶段|风险评估:人员紧张，可能影响进度|后续安排:增加资源，确保按期交付"
```

### 直接打开生成的PPT
```bash
open ~/Documents/工作汇报_2026-03-12.pptx
```

## PPT 格式规范

- **首页**: 标题居中，宋体48号，加粗
- **内容页**: 标题36号，正文18号
- **页数**: 最多10页（首页 + 内容页 + 谢谢观看页）
- **布局**: 标题+内容的简单布局

## 在 OpenClaw 中使用

直接告诉 OpenClaw：
- "帮我生成一份本周工作汇报PPT"
- "创建一个项目进度汇报"
- "生成月度工作总结演示文稿"

OpenClaw 会调用此 skill 生成 PPT。
