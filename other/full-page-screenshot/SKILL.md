---
name: full-page-screenshot
description: |
  在浏览器中对网页做完整长截图（full-page screenshot），生成一张包含页面所有内容的 PNG 长图。
  触发场景：用户要求对网页截长图、全页截图、完整截图、long screenshot、full page capture，
  或要求把网页/文章/报告截成一张完整的图片。支持用户已打开的 tab 或指定 URL。
  自动处理 SPA 内部滚动容器、懒加载图片、超长页面分片拼接。
  无外部依赖，直连 Chrome DevTools 协议完成所有操作。
---

# Full Page Screenshot

对浏览器中的网页生成一张完整的长截图 PNG，覆盖页面全部内容（包括需要滚动才能看到的部分）。直连 Chrome DevTools WebSocket，无需 CDP Proxy 或其他中间层。

## 前置条件

只需 Node.js 22+ 和 Chrome 开启远程调试：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/full-page-screenshot.mjs" --check
```

如果 chrome 检查失败，引导用户：打开 `chrome://inspect/#remote-debugging`，勾选 **"Allow remote debugging for this browser instance"**。

## 工作流程

### 用户描述了已打开的 tab（推荐，尤其是需要登录的页面）

先列出所有 tab，匹配用户描述找到 `targetId`：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/full-page-screenshot.mjs" --list
```

然后截图该 tab：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/full-page-screenshot.mjs" <targetId> <output> [--width N] [--dpr N]
```

### 用户给了 URL

一条命令完成全部流程（建 tab → 等加载 → 截图 → 关 tab）：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/full-page-screenshot.mjs" --url "<URL>" <output> [--width N] [--dpr N] [--wait N]
```

**注意**：`--url` 模式创建后台 tab。对于需要登录的内部系统（如 SAP、企业 SSO），后台 tab 可能无法完成认证。此时应引导用户先在 Chrome 中打开页面，然后使用 targetId 模式截图。

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `output` | 输出文件路径 | `/tmp/screenshot.png` |
| `--width` | 视口宽度（CSS 像素）。文章页 1200，宽表格/面板 1440-1920 | 1200 |
| `--dpr` | 设备像素比。2 可获 Retina 清晰度，但体积翻 4 倍 | 1 |
| `--wait` | 页面加载超时（毫秒），仅 `--url` 模式 | 15000 |

### 验证输出

```bash
sips -g pixelWidth -g pixelHeight <output>
```

裁剪局部验证（需要 Pillow）：

```python
from PIL import Image
img = Image.open("<output>")
w, h = img.size
img.crop((0, 0, w, 1500)).save("/tmp/check_top.png")
img.crop((0, h-1500, w, h)).save("/tmp/check_bottom.png")
```

## 核心能力

- **SPA 内部滚动容器**：自动检测 `overflow-y: auto/scroll` 的容器，用 `!important` 覆盖 CSS 高度约束（含 Tailwind `h-[calc(...)]` 等），展开全部内容后截图
- **DOM 稳定等待**：`readyState=complete` 后继续监测 DOM 元素数量变化，直到 SPA 数据渲染完成
- **懒加载处理**：逐步滚动触发 IntersectionObserver，等待所有 `img.complete`
- **超长页面分片**：>16000px 的页面自动分片截取（每片 8000px），用 Python PIL 拼接
- **Proxy 兼容**：当 web-access CDP Proxy 运行时，自动检测并通过 proxy API 完成截图（滚动容器分片拼接）

## 注意事项

- 超长页面（> 20000px）在高 DPR 下可能导致 Chrome 内存问题。遇到此情况降低 `--dpr` 到 1 或减小 `--width`。
- `--url` 模式会自动创建后台 tab 并在截图后关闭，不影响用户已有 tab。
- 截图期间会临时改变页面视口尺寸和滚动容器样式，完成后自动恢复。
- 脚本通过读取 `DevToolsActivePort` 文件发现 Chrome 调试端口，直连 WebSocket，无需任何代理或中间服务。
- 分片拼接需要 Python 3 + Pillow（macOS 通常已安装）。无 Pillow 时会保留分片文件。
- 当 web-access 的 CDP Proxy 在运行时，脚本先尝试直连，超时后降级到 proxy API（通过 /eval 和 /screenshot 端点操作）。
