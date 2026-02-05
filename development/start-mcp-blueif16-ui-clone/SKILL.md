---
name: start-mcp
description: 启动Chrome DevTools mcp服务器并加载到Claude Code
allowed-tools: Read, Bash
---

# 启动Chrome DevTools MCP服务器

当用户调用此skill时，自动执行以下操作：

1. 检测当前项目目录
2. 运行 `npm run setup-mcp` 自动设置环境变量和构建项目
3. 验证MCP服务器是否成功添加

## 执行步骤

首先检查MCP服务器是否已经可用：

```bash
claude mcp list
```

如果chrome-devtools已经连接并可用，则直接结束，不执行任何操作。

如果chrome-devtools不可用或未安装，尝试直接添加MCP服务器：

```bash
claude mcp remove chrome-devtools 2>/dev/null || true
claude mcp add chrome-devtools node "$CHROME_DEVTOOLS_MCP_PATH/build/src/index.js"
```

然后验证是否成功：

```bash
claude mcp list
```

如果添加成功并且chrome-devtools已连接，则结束。

如果添加失败（例如build目录不存在），则运行完整的setup脚本：

```bash
npm run setup-mcp
```

## 如果setup失败，手动执行

如果自动设置失败，执行以下命令：

```bash
# 1. 构建项目
npm run build

# 2. 移除旧的MCP服务器（如果存在）
claude mcp remove chrome-devtools 2>/dev/null || true

# 3. 添加新的MCP服务器
claude mcp add chrome-devtools node "$CHROME_DEVTOOLS_MCP_PATH/build/src/index.js"

# 4. 验证
claude mcp list
```

## 测试MCP服务器

使用MCP Inspector进行测试：
```bashsta
npx @modelcontextprotocol/inspector node build/src/index.js
```

## 可用功能

加载后，你可以使用26个浏览器自动化工具，包括：
- 页面导航和管理
- 表单填写和点击操作
- 网络请求监控
- 性能分析
- 页面截图和快照
- JavaScript执行

## 常见问题

**Q: 如何知道MCP服务器是否正常运行？**
A: 在Claude Code中，MCP工具会自动出现在可用工具列表中。

**Q: 修改代码后需要重启吗？**
A: 是的，需要重新构建并重新添加MCP服务器。

**Q: 如何查看MCP服务器日志？**
A: 使用 `npm run start-debug` 启动服务器查看详细日志。
