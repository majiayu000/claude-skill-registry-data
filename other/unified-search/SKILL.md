---
name: unified-search
description: OpenMOSS 统一搜索 — Grok 深度搜索 + OpenCLI 多源补充（含故障降级逻辑）
version: 1.2
evolved_from: unified-search
evolution_type: FIX
---

# 统一搜索工具 (moss-search)

Grok (grok-4.20-0309-reasoning) 做主搜索，OpenCLI 多平台做细节补充。具备环境预检与登录拦截自动降级机制，确保在插件未连接时任务不中断。

## 适用场景
- 需要深度推理与实时数据结合的复杂查询。
- 需要跨平台（小红书、知乎、arXiv 等）汇总信息。
- 在 OpenCLI 环境不稳定（如 Browser Bridge 未连接）或目标平台有登录限制时需要自动切换方案。

## 步骤

1. **环境预检**：在执行任何 `opencli` 相关操作前，必须检查连接状态。
   ```bash
   opencli status
   ```
   - **正常**：继续执行带 `--detail` 的搜索。
   - **异常**（报错 `Browser Extension is not connected`）：**严禁**使用 `--detail` 模式或 `opencli` 抓取命令。

2. **执行搜索与自动降级**：
   - **首选方案**（环境正常）：
     ```bash
     python3 skills/unified-search/moss-search.py "关键词" --mode auto --detail
     ```
   - **次选方案**（环境异常/插件未连接）：
     - 仅使用 Grok 基础搜索（不带 `--detail`）：
       ```bash
       python3 skills/unified-search/moss-search.py "关键词" --mode auto
       ```
     - 使用原生 `browser` 工具直接访问：
       若需获取特定页面内容，改用 `browser.open_url("URL")` 并配合 `browser.get_content()`。

3. **异常处理逻辑**：
   - **登录拦截**：若特定平台（小红书/知乎）出现登录墙，立即切换为搜索引擎绕过模式：
     ```bash
     # 降级方案：使用 Google 搜索特定站点内容
     opencli google "site:xiaohongshu.com 关键词"
     ```

## 工具和命令

### 核心命令
```bash
python3 skills/unified-search/moss-search.py "关键词" [--mode MODE] [--detail] [--output path]
```

### 降级路径表
| 故障现象 | 根本原因 | 降级动作 |
|----------|----------|-----------|
| `Browser Extension is not connected` | Chrome 插件未连接 | 去掉 `--detail` 参数；改用 `browser` 工具 |
| `Login required` / 验证码 | 平台反爬/登录墙 | 使用 `google "site:domain.com ..."` 搜索索引 |
| `XAI_API_KEY` 错误 | Grok 认证失败 | 直接使用 `opencli google` 或 `browser` 搜索 |

## 注意事项
- **环境强依赖**：`opencli` 的深度抓取功能极度依赖 Browser Bridge。在自动化脚本中，必须先捕获 `opencli status` 的输出，若包含 `Error` 字样，必须分支到降级逻辑。
- **不要重试死循环**：一旦检测到插件未连接，不要尝试重启 daemon，应直接切换到 `browser` 工具完成任务。
- **Browser 工具优势**：当 `opencli` 无法连接插件时，原生 `browser` 工具通常仍可工作，因为它直接控制浏览器实例。

## 示例

### 1. 环境异常时的自动降级处理
```bash
# 1. 检查状态
opencli status 
# 输出: Error: Daemon is running but the Browser Extension is not connected.

# 2. 发现异常，执行不带 --detail 的搜索以保证结果产出
python3 skills/unified-search/moss-search.py "最新 AI 视频生成技术" --mode auto

# 3. 若需特定网页细节，手动调用 browser 工具
# 使用 browser.open_url("https://example.com/detail")
```

### 2. 绕过社交平台登录限制
```bash
# 如果 moss-search 在抓取小红书时因登录拦截失败
opencli google "site:xiaohongshu.com 2025年上海车展攻略"
```

### 3. 学术搜索降级
```bash
# arXiv 接口超时或受限时
opencli google "site:arxiv.org DeepSeek-V3 technical report"
```