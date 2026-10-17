---
name: cli-anything-skill
description: CLI-Anything 桌面软件 CLI 化工具 — 让 Agent 通过命令行操控桌面应用
---

# CLI-Anything Skill

CLI-Anything 将桌面软件转为 Agent 可用的 CLI 工具。已安装在 /root/CLI-Anything/。

## 已支持的软件

| 软件 | CLI 命令 | 用途 |
|------|---------|------|
| Blender | `cli-anything-blender` | 3D 建模、渲染 |
| GIMP | `cli-anything-gimp` | 图像编辑 |
| Inkscape | `cli-anything-inkscape` | 矢量图形 |
| LibreOffice | `cli-anything-libreoffice` | 文档处理 |
| Audacity | `cli-anything-audacity` | 音频编辑 |
| OBS Studio | `cli-anything-obs` | 录屏/直播 |
| KDenlive | `cli-anything-kdenlive` | 视频编辑 |
| Shotcut | `cli-anything-shotcut` | 视频编辑 |
| Draw.io | `cli-anything-drawio` | 图表绘制 |
| Mermaid | `cli-anything-mermaid` | 图表生成 |
| ComfyUI | `cli-anything-comfyui` | AI 图像生成 |
| Ollama | `cli-anything-ollama` | 本地 LLM |
| Zoom | `cli-anything-zoom` | 视频会议 |
| Browser | `cli-anything-browser` | 浏览器自动化 |

## 安装特定软件的 CLI

```bash
cd /root/CLI-Anything/<software>/agent-harness
pip install -e .
```

## 使用方式

```bash
# 查看帮助
cli-anything-<software> --help

# 进入交互模式 (REPL)
cli-anything-<software>

# JSON 输出（适合 Agent 解析）
cli-anything-<software> --json <command>
```

## 示例

### Blender
```bash
cli-anything-blender --json render --scene scene.blend --output ./render/
cli-anything-blender --json list-objects --scene scene.blend
```

### GIMP
```bash
cli-anything-gimp --json apply-filter --input photo.png --filter gaussian-blur --radius 5
cli-anything-gimp --json resize --input photo.png --width 800 --height 600
```

### LibreOffice
```bash
cli-anything-libreoffice --json convert --input doc.docx --format pdf
cli-anything-libreoffice --json export --input sheet.xlsx --format csv
```

### Browser (DOMShell)
```bash
cli-anything-browser navigate "https://example.com"
cli-anything-browser screenshot --output page.png
cli-anything-browser extract --selector "h1"
```

## 为新软件生成 CLI

如果目标软件有源码，可用 CLI-Anything 插件自动生成：
```bash
# 需要 Claude Code 环境
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything
/cli-anything <software-name>
```

## 注意事项

- 需要目标桌面软件已安装在系统上
- 部分软件需要图形环境（GNOME 桌面已安装）
- 安装软件：`apt-get install blender gimp inkscape libreoffice`
