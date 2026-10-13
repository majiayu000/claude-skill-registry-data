---
name: summarize-zh
version: 1.0.0
description: 使用 summarize CLI 对 URL 或文件进行摘要（网页、PDF、图片、音频、YouTube）的中文版本
---

# 摘要工具 🔍

使用 `summarize` CLI 对各种内容进行智能摘要。

## 使用场景

- 对网页内容进行快速摘要
- 处理 PDF 文档的摘要
- 图片内容的视觉摘要
- 音频/视频的文字转录和摘要
- YouTube 视频的摘要分析

## 核心功能

### 1. 网页摘要
```bash
summarize https://example.com
summarize https://example.com --max 500
```

### 2. 文档摘要
```bash
summarize document.pdf
summarize document.docx
summarize presentation.pptx
```

### 3. 多媒体内容
```bash
# 图片摘要
summarize image.jpg
summarize image.png

# 音频转录和摘要
summarize audio.mp3
summarize audio.wav

# YouTube 视频摘要
summarize https://youtube.com/watch?v=VIDEO_ID
```

### 4. 批量处理
```bash
summarize file1.pdf file2.pdf file3.docx
summarize *.txt
```

## 参数选项

| 参数 | 说明 | 示例 |
|------|------|------|
| `--max` | 最大摘要长度 | `--max 1000` |
| `--min` | 最小摘要长度 | `--min 100` |
| `--focus` | 重点主题 | `--focus "技术分析"` |
| `--format` | 输出格式 | `--format json` |
| `--lang` | 输出语言 | `--lang zh` |

## 实际应用

### 学术研究
```bash
summarize https://arxiv.org/abs/XXXX.XXXX --max 800
summarize research-paper.pdf --focus "方法论"
```

### 商业分析
```bash
summarize https://company.com/annual-report --min 200
summarize market-research.pdf --focus "市场趋势"
```

### 媒体内容
```bash
summarize https://youtube.com/watch?v=abc123 --max 500
summarize podcast.mp3 --format json
```

## 支持的格式

**文档格式：**
- PDF (.pdf)
- Word (.docx)
- PowerPoint (.pptx)
- Text (.txt, .md)
- HTML (.html)

**媒体格式：**
- 图片 (.jpg, .png, .gif)
- 音频 (.mp3, .wav, .m4a)
- 视频 (通过 YouTube 链接)

**网络资源：**
- 网页 URL
- GitHub 仓库
- 在线文档

## 高级用法

### 自定义模板
```bash
summarize document.pdf --template custom-template.md
```

### API 集成
```bash
summarize https://api.example.com/data --format json --lang zh
```

### 定批处理
```bash
# 批量处理多个文件
for file in *.pdf; do
    summarize "$file" --max 300
done
```

## 质量控制

### 摘要质量检查
```bash
# 检查摘要完整性
summarize document.pdf --verify

# 生成质量评分
summarize document.pdf --score
```

### 交互式摘要
```bash
summarize https://example.com --interactive
```

## 故障排除

### 常见问题
1. **文件格式不支持** - 检查文件格式是否在支持列表中
2. **网络连接问题** - 确保 URL 可访问
3. **内存不足** - 使用 `--max` 参数限制输出长度
4. **语言识别错误** - 使用 `--lang zh` 明确指定中文

### 性能优化
- 大文件建议使用 `--max` 参数
- 批量处理时避免同时处理过多文件
- 网络资源使用稳定的连接

## 最佳实践

1. **明确需求** - 使用 `--focus` 参数指定摘要重点
2. **控制长度** - 根据用途调整 `--max` 参数
3. **格式选择** - JSON 格式适合程序处理，Markdown 格式适合阅读
4. **验证结果** - 重要文档建议使用 `--verify` 验证摘要质量

---

*为中文用户优化的智能摘要工具*