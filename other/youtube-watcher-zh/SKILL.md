---
name: youtube-watcher-zh
description: 通过 yt-dlp 提取 YouTube 视频字幕，支持视频摘要、问答和内容提取，仅适用于有字幕的视频
tags: [youtube, subtitle, transcription, video]
permissions: [network, shell]
metadata:
  clawdbot:
    requires:
      bins: [yt-dlp, ffmpeg]
      env: []
    files: []
  capabilities:
    allow:
      - execute: [yt-dlp, ffmpeg]
      - network: ["*.youtube.com", "youtube.com"]
      - read: [workspace/**]
      - write: [workspace/**]
    deny:
      - execute: ["!*"]
      - network: ["!*.youtube.com", "!youtube.com"]
---

# YouTube 字幕提取器

> 通过 yt-dlp 提取 YouTube 视频字幕并进行内容分析

## 🎯 功能特性

- 📝 字幕提取 - 从 YouTube 视频中提取带时间戳的字幕
- 🎬 内容分析 - 基于字幕进行视频内容摘要
- ❓ 问答支持 - 根据字幕内容回答问题
- 🔍 内容搜索 - 在字幕内容中搜索特定信息
- 📊 统计分析 - 分析字幕的词汇、主题等统计信息

## 🚀 快速开始

### 1. 安装依赖

确保安装了 yt-dlp：

```bash
# Ubuntu/Debian
sudo apt install yt-dlp

# macOS (使用 Homebrew)
brew install yt-dlp

# 或通过 pip 安装
pip install yt-dlp
```

### 2. 基本使用

提取视频字幕：

```bash
# 提取单个视频字幕
yt-dlp --write-subs --sub-format "srt" "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 📝 使用方法

### 提取字幕

```bash
# 提取字幕并保存为 SRT 格式
yt-dlp --write-subs --sub-format "srt" --sub-lang "en,zh" "YOUTUBE_URL"

# 提取字幕并包含自动生成的字幕
yt-dlp --write-subs --sub-format "srt" --sub-lang "en,zh,en-auto" "YOUTUBE_URL"
```

### 字幕格式支持

- **SRT** - 标准字幕格式
- **VTT** - WebVTT 字幕格式  
- **ASS/SSA** - 高级字幕格式
- **JSON** - 原始 JSON 数据

## 🔍 内容分析

### 视频摘要

基于字幕内容生成视频摘要：

```bash
# 提取关键字和主题
# 通过文本分析工具处理字幕内容
```

### 内容问答

根据字幕内容回答问题：

```bash
# 示例问题
"这个视频主要讲了什么？"
"视频中提到了哪些关键概念？"
"视频的主要内容分为哪几个部分？"
```

### 内容搜索

在字幕中搜索特定内容：

```bash
# 搜索关键词
grep "关键词" video.srt

# 使用文本搜索工具
find "搜索词" in video.srt
```

## ⚙️ 配置选项

### yt-dlp 参数

| 参数 | 描述 |
|------|------|
| `--write-subs` | 写入字幕文件 |
| `--sub-format "srt"` | 字幕格式 |
| `--sub-lang "en,zh"` | 字幕语言 |
| `--sub-lang "en-auto"` | 自动生成的英文字幕 |
| `--no-playlist` | 不提取播放列表 |
| `--no-mtime` | 不修改文件时间戳 |

### 输出格式

```bash
# 输出文件命名规则
视频标题.语言.srt
视频标题.语言.vtt
视频标题.语言.json
```

## 📊 字幕处理

### 字幕清理

- 去除重复条目
- 时间戳标准化
- 文本格式化
- 语言检测

### 内容分析

- **词汇统计** - 计算词频、关键词
- **主题提取** - 识别主要讨论话题
- **情感分析** - 分析内容的情感倾向
- **结构分析** - 识别内容结构和逻辑

## 🎬 实际应用

### 1. 视频研究

```bash
# 提取教育视频的主要观点
# 分析演讲者的主要论点
# 识别技术视频的关键步骤
```

### 2. 内容创作

```bash
# 基于字幕创建文章摘要
# 生成视频内容的文字版本
# 创建视频内容的索引目录
```

### 3. 学习辅助

```bash
# 将视频内容转换为文字笔记
# 创建视频内容的问答集
# 生成视频内容的思维导图
```

## 📁 文件管理

### 存储结构

```
workspace/
├── videos/
│   ├── [视频ID]/
│   │   ├── video.srt          # 字幕文件
│   │   ├── video.vtt          # WebVTT 格式
│   │   ├── video.json        # 原始数据
│   │   └── summary.txt       # 内容摘要
└── processed/
    ├── transcripts/           # 处理后的字幕
    ├── summaries/            # 视频摘要
    └── analysis/             # 内容分析
```

### 文件命名约定

- 使用视频 ID 作为主目录名
- 保留原始文件扩展名
- 添加处理时间戳避免覆盖

## 🔧 高级功能

### 批量处理

```bash
# 批量提取多个视频字幕
for video_id in "ID1" "ID2" "ID3"; do
    yt-dlp --write-subs --sub-format "srt" "https://www.youtube.com/watch?v=$video_id"
done
```

### 自动化工作流

结合其他工具实现自动化：

```bash
# 字幕提取 + 内容分析 + 摘要生成
extract_and_analyze() {
    local url="$1"
    yt-dlp --write-subs --sub-format "srt" "$url"
    # 后续处理脚本
}
```

## ⚠️ 注意事项

### 限制条件

- **字幕可用性** - 仅适用于有字幕的视频
- **语言支持** - 取决于视频的字幕语言
- **版权限制** - 请遵守版权法和 YouTube 服务条款

### 性能考虑

- 大文件处理需要较多内存
- 网络连接质量影响下载速度
- 视频长度影响处理时间

## 🚨 使用限制

### 法律合规

- 仅用于个人学习和研究
- 不得用于商业目的
- 尊重内容创作者的版权
- 遵守 YouTube 的服务条款

### 技术限制

- 需要稳定的网络连接
- 需要足够的存储空间
- 处理大量视频时需要考虑性能

## 📞 故障排除

### 常见问题

1. **字幕提取失败**
   - 检查视频是否有字幕
   - 尝试不同的字幕格式
   - 确认网络连接正常

2. **格式不支持**
   - 更新 yt-dlp 到最新版本
   - 尝试使用备用提取器
   - 检查视频地区的字幕可用性

3. **处理错误**
   - 检查文件权限
   - 确保有足够的磁盘空间
   - 重试失败的提取

---

**提示**: 此技能仅适用于有字幕的 YouTube 视频。无字幕的视频将无法提取内容。