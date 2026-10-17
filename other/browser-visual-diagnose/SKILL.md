---
name: browser-visual-diagnose
description: 浏览器自动化失败时的视觉诊断与进程恢复流程，用于识别弹窗、验证码及处理进程挂起/SIGTERM。
version: 1.1
evolved_from: browser-visual-diagnose
evolution_type: FIX
---

# Browser Visual Diagnose

## 适用场景
在使用 `browser` 或 `opencli` 工具进行网页自动化操作时，如果遇到以下情况，应立即触发此 Skill：
- **元素异常**：定位超时（Timeout）或报错 `element not found`。
- **流程阻塞**：预期操作已执行但页面未跳转，怀疑存在验证码（CAPTCHA）或遮罩弹窗。
- **系统级故障**：收到 `SIGTERM`、`Aborted` 信号，或浏览器进程长时间无响应（Hanging）。
- **重复失败**：同一操作在不同页面连续触发超时。

## 步骤
1. **进程状态检查**：
   - 若错误信息包含 `SIGTERM`、`Aborted` 或 `Protocol error`，判定为浏览器进程崩溃或挂起。
   - **执行清理**：调用 `opencli` 执行 `pkill -f chromium` 或 `pkill -f chrome` 清理僵尸进程。
   - **冷启动**：重新初始化浏览器环境，而非在当前 Session 盲目重试。

2. **捕获现场**：
   - 在进程恢复后或遇到逻辑阻塞时，立即执行 `browser({action: "screenshot"})` 获取当前视口截图。

3. **多模态视觉分析**：
   - 将截图输入给具备视觉能力的模型，诊断以下内容：
     - **阻碍元素**：验证码、Cookie 确认框、全屏广告、登录墙。
     - **渲染状态**：页面是否白屏、是否加载了错误的 404/风控页面。
     - **坐标识别**：获取阻碍元素关闭按钮或目标操作点的具体像素坐标。

4. **策略执行**：
   - **弹窗/遮罩**：根据视觉坐标执行 `browser({action: "click", x, y})`。
   - **验证码/风控**：若识别为高强度风控，停止自动化，向用户报告并建议人工介入或更换代理。
   - **视觉恢复模式**：若 DOM 定位失效，切换为基于坐标的视觉导航模式。

## 工具和命令
- `opencli({cmd: "pkill -9 -f chromium"})`: 强制清理挂起的浏览器进程。
- `browser({action: "screenshot"})`: 获取当前页面图像。
- `browser({action: "click", x: number, y: number})`: 绕过 DOM，直接根据视觉坐标点击。
- `browser({action: "evaluate", script: "window.devicePixelRatio"})`: 获取缩放比例以修正坐标偏移。

## 注意事项
- **拒绝盲目重试**：检测到 `SIGTERM` 后，直接重试原命令通常会再次失败，必须先执行进程清理。
- **坐标对齐**：截图的尺寸可能与浏览器视口尺寸不一致，点击前需确认 `viewport` 设置。
- **资源占用**：频繁的 `screenshot` 会消耗大量 Token 和带宽，仅在关键节点或报错时触发。
- **环境隔离**：在清理进程时，注意不要误杀其他必要的系统进程。

## 示例
**场景**：爬取小红书笔记时，连续三个 URL 均反馈 `Timeout` 且出现 `SIGTERM`。
1. **诊断**：判定为浏览器进程挂起。
2. **清理**：执行 `opencli({cmd: "pkill -f chromium"})`。
3. **恢复**：重新调用 `browser({action: "goto", url: "..."})`。
4. **视觉确认**：执行 `screenshot`，发现页面出现了“滑动验证码”。
5. **决策**：记录“触发验证码风控”，跳过当前 ID，调整爬取频率。