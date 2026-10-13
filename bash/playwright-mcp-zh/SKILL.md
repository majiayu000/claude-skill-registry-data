---
name: playwright-mcp-zh
description: 通过 Playwright MCP 服务器实现浏览器自动化。导航网站、点击元素、填写表单、提取数据、截图，执行完整的浏览器自动化工作流。
metadata: {"openclaw":{"emoji":"🎭","os":["linux","darwin","win32"],"requires":{"bins":["playwright-mcp","npx"]},"install":[{"id":"npm-playwright-mcp","kind":"npm","package":"@playwright/mcp","bins":["playwright-mcp"],"label":"安装 Playwright MCP"}]}}
---

# Playwright MCP 技能

通过 Playwright MCP 服务器实现浏览器自动化。支持编程控制 Chrome、Firefox 或 WebKit 浏览器。

## 安装

```bash
npm install -g @playwright/mcp
# 或者
npx @playwright/mcp
```

首次使用需要安装浏览器：
```bash
npx playwright install chromium
```

## 快速开始

### 启动 MCP 服务器（STDIO 模式）
```bash
npx @playwright/mcp
```

### 带参数启动
```bash
# 无头模式
npx @playwright/mcp --headless

# 指定浏览器
npx @playwright/mcp --browser firefox

# 设置视口大小
npx @playwright/mcp --viewport-size 1280x720

# 忽略 HTTPS 错误
npx @playwright/mcp --ignore-https-errors
```

## 常见用例

### 1. 导航并提取数据
```python
# 可用的 MCP 工具：
# - browser_navigate: 打开 URL
# - browser_click: 点击元素
# - browser_type: 输入文本
# - browser_select_option: 选择下拉选项
# - browser_get_text: 提取文本内容
# - browser_evaluate: 执行 JavaScript
# - browser_snapshot: 获取页面结构
# - browser_close: 关闭浏览器
```

### 2. 表单交互
```
1. browser_navigate 导航到表单 URL
2. browser_type 在输入框中输入内容
3. browser_click 提交表单
4. browser_get_text 验证结果
```

### 3. 数据提取
```
1. browser_navigate 导航到目标页面
2. browser_evaluate 执行数据提取脚本
3. 解析返回的 JSON 数据
```

## MCP 工具参考

| 工具 | 描述 |
|------|------|
| `browser_navigate` | 导航到 URL |
| `browser_click` | 通过选择器点击元素 |
| `browser_type` | 在输入框中输入文本 |
| `browser_select_option` | 选择下拉选项 |
| `browser_get_text` | 获取文本内容 |
| `browser_evaluate` | 执行 JavaScript |
| `browser_snapshot` | 获取无障碍页面快照 |
| `browser_close` | 关闭浏览器上下文 |
| `browser_choose_file` | 上传文件 |
| `browser_press` | 按下键盘按键 |

## 配置选项

```bash
# 安全设置
--allowed-hosts example.com,api.example.com
--blocked-origins malicious.com
--ignore-https-errors

# 浏览器设置
--browser chromium|firefox|webkit
--headless
--viewport-size 1920x1080
--user-agent "Custom Agent"

# 超时设置
--timeout-action 10000      # 操作超时（毫秒）
--timeout-navigation 30000  # 导航超时（毫秒）

# 输出设置
--output-dir ./playwright-output
--save-trace
--save-video 1280x720
```

## 示例

### 网站登录
```
browser_navigate: { url: "https://example.com/login" }
browser_type: { selector: "#username", text: "user" }
browser_type: { selector: "#password", text: "pass" }
browser_click: { selector: "#submit" }
browser_get_text: { selector: ".welcome-message" }
```

### 提取表格数据
```
browser_navigate: { url: "https://example.com/data" }
browser_evaluate: { 
  script: "() => { return Array.from(document.querySelectorAll('table tr')).map(r => r.textContent); }" 
}
```

### 截图
```
browser_navigate: { url: "https://example.com" }
browser_evaluate: { script: "() => { document.body.style.zoom = 1; return true; }" }
# 截图通过 --output-dir 保存或在响应中返回
```

## 安全注意事项

- 默认限制文件系统访问范围为工作区根目录
- 主机验证防止导航到不受信任的域名
- 默认启用沙箱（谨慎使用 `--no-sandbox`）
- 默认阻止 Service Workers

## 故障排除

```bash
# 更新浏览器
npx playwright install chromium

# 调试模式
npx @playwright/mcp --headless=false --output-mode=stdout

# 检查安装
playwright-mcp --version
```

## 链接

- [Playwright 文档](https://playwright.dev)
- [MCP 协议](https://modelcontextprotocol.io)
- [NPM 包](https://www.npmjs.com/package/@playwright/mcp)
