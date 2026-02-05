---
name: web-build
description: 通用 Web 项目构建工具，自动检测项目类型（Vue、React、Ant Design Pro 等），执行依赖安装和生产构建，生成可部署的静态文件并返回预览链接。
---

# 通用 Web 项目构建工具

## 功能说明

自动执行 Web 项目的完整构建流程：
1. 检查项目配置文件（package.json）
2. 自动检测项目类型（Vue、React、Ant Design Pro 等）
3. 安装项目依赖（npm install，如果 node_modules 不存在）
4. 执行生产构建（npm run build）
5. 生成可访问的预览链接

## 模板参考

本 skill 目录下的 `templates/` 包含纯 HTML/CSS/JS 参考模板，供 frontend-html agent 使用：

| 模板 | 类型 | 特点 |
|-----|------|------|
| `templates/mes-dashboard/` | 单文件 | 科技感大屏看板、深色主题、动画效果 |
| `templates/report-h5/` | 单文件 | 移动端响应式、简洁表单 |
| `templates/report-app/` | 多文件 | Tailwind CSS、模块化 JS、完整 API 调用 |

**使用方式**：可用 Read 工具读取上述模板文件，参考其风格和结构。

## 执行流程

### 步骤1：检查项目配置
```bash
ls -la package.json
```

如果不存在，提示用户：
```
❌ 未找到 package.json 文件
请先创建 Web 项目或使用相应的 Agent 创建项目
```

### 步骤2：检测项目类型

通过分析 `package.json` 中的依赖自动检测项目类型：

| 项目类型 | 检测依赖 | 构建工具 | 输出目录 |
|---------|---------|---------|---------|
| Vue 3 + Vite | `vue` + `vite` | Vite | `dist/` |
| React + Vite | `react` + `vite` | Vite | `dist/` |
| Ant Design Pro | `@umijs/max` 或 `umi` | UmiJS | `dist/` |
| Create React App | `react-scripts` | Webpack | `build/` |
| Next.js | `next` | Next.js | `.next/` 或 `out/` |

### 步骤3：检查并安装依赖
```bash
# 检查 node_modules 是否存在
if [ ! -d "node_modules" ]; then
  echo "📦 安装项目依赖..."
  npm install
else
  echo "✓ 依赖已存在，跳过安装"
fi
```

**说明**：
- 首次安装可能需要 1-3 分钟
- 会下载并安装所有依赖到 `node_modules/` 目录
- 失败时检查网络连接和 npm 配置

### 步骤4：执行构建
```bash
npm run build
```

**说明**：
- 构建时间通常为 10-60 秒（取决于项目大小）
- 构建工具会自动生成输出目录
- 失败时检查代码错误和依赖问题

### 步骤5：验证构建结果
```bash
# 检查输出目录是否存在
if [ -d "dist" ]; then
  echo "✓ dist/ 目录已生成"
elif [ -d "build" ]; then
  echo "✓ build/ 目录已生成"
else
  echo "❌ 构建产物目录未找到"
fi
```

### 步骤6：生成预览链接

构建成功后，生成可访问的预览链接。

**链接格式**：
```
{WEB_BASE_URL}/ai-coder/code/{project_type}/o_{org_id}/w_{coder_id}/{output_dir}/
```

**示例**：
```
http://localhost:8080/ai-coder/code/web_ant/o_20251114/w_102/dist/
http://localhost:8080/ai-coder/code/web/o_20251114/w_102/dist/
```

**路径提取**：
- 从当前工作目录路径中提取 org_id 和 coder_id
- 工作目录格式：`/workspace/code/{project_type}/o_{org_id}/w_{coder_id}/`
- WEB_BASE_URL 默认为：`http://localhost:8080`
- 输出目录根据项目类型确定（dist/、build/ 等）

## 输出格式

构建成功后，以 Markdown 格式输出：

```markdown
✅ Web 应用构建完成！

📦 构建信息：
- 项目类型：Ant Design Pro (UmiJS)
- 构建工具：UmiJS 4.x
- 输出目录：dist/
- 入口文件：index.html

🌐 预览地址：
[点击访问应用](http://localhost:8080/ai-coder/code/web_ant/o_20251114/w_102/dist/)

💡 使用提示：
- 点击上方链接即可在浏览器中预览应用
- 应用已部署到工作区，可随时访问
- 如需修改，请重新编辑代码并再次构建
```

## 关键错误处理

### 错误1：package.json 不存在
```markdown
❌ 构建失败：未找到 package.json

请先创建 Web 项目：
1. 使用 frontend-vue Agent 创建 Vue 项目
2. 使用 frontend-ant Agent 创建 Ant Design Pro 项目
3. 或手动创建 package.json 配置文件
```

### 错误2：npm install 失败
```markdown
❌ 依赖安装失败

可能原因：
- 网络连接问题
- npm 配置错误
- package.json 配置错误

建议操作：
1. 检查网络连接
2. 检查 package.json 中的依赖版本
3. 尝试使用国内镜像源：npm config set registry https://registry.npmmirror.com
4. 尝试清理缓存：npm cache clean --force
```

### 错误3：npm run build 失败
```markdown
❌ 构建失败

可能原因：
- 代码存在语法错误
- 依赖缺失或版本不兼容
- 构建工具配置错误

建议操作：
1. 仔细检查错误信息中的具体错误
2. 修复代码中的语法错误
3. 确保所有依赖已正确安装
4. 检查构建工具配置文件（vite.config.js、config/config.ts 等）
```

## 注意事项

1. **环境要求**：
   - Docker 容器中已安装 Node.js 和 npm
   - 确保网络连接正常（用于下载依赖）

2. **路径配置**：
   - Vue/Vite 项目：确保 `vite.config.js` 中 `base` 设置为 `'./'`（相对路径）
   - Ant Design Pro：确保 `config/config.ts` 中 `publicPath` 设置为 `'./'`
   - 这样可以适配任意部署路径

3. **构建时间**：
   - 首次构建较慢（需要下载依赖，1-3 分钟）
   - 后续构建会利用缓存加速（10-60 秒）

4. **预览链接**：
   - 链接格式由环境变量 `WEB_BASE_URL` 决定
   - 默认为 `http://localhost:8080`
   - 可在 `.env` 文件中修改

5. **路径映射**：
   - URL路径：`/ai-coder/code/{path}`
   - 文件系统路径：`/workspace/code/{path}`
   - 后端路由：`/ai-coder/code/{path:path}` → 映射到 `/workspace/code/{path}`
