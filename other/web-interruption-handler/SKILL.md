---
name: web-interruption-handler
description: 处理网页自动化中的弹窗、登录墙及 Cookie 授权等中断干扰。
version: 1.0
evolution_type: CAPTURED
---

# Web Interruption Handler

## 适用场景
在执行自动化网页浏览、数据抓取或 UI 测试时，页面突然弹出非预期的遮罩层（Modal）、登录强制跳转、Cookie 同意对话框或订阅弹窗，导致后续操作无法定位目标元素。

## 步骤
1. **状态诊断**：当操作超时或定位失败时，调用 `browser.screenshot` 获取当前页面截图。
2. **元素扫描**：
    - 检查是否存在常见的干扰项选择器：`[aria-label*="close" i]`, `button:has-text("Accept")`, `.modal-close`, `[class*="overlay"]`。
    - 检查是否存在 `iframe`，弹窗可能嵌套在独立文档中。
3. **尝试自动消除**：
    - **模拟点击**：优先尝试点击“关闭”、“接受”或“跳过”按钮。
    - **键盘操作**：发送 `Escape` 键尝试关闭模态框。
    - **DOM 清理**：若点击无效，使用 `browser.evaluate` 直接从 DOM 中移除遮罩元素或修改其 `display: none`。
4. **验证恢复**：再次检查目标元素是否变为 `is_visible`。
5. **人工同步**：若自动化处理失败，输出当前页面状态描述，并请求用户提供登录凭据或手动操作建议。

## 工具和命令
- **定位与点击**：
  `browser.click('text="Accept All"')`
  `browser.click('button[aria-label="Close"]')`
- **强力移除**：
  `browser.evaluate("document.querySelectorAll('[class*=\"popup\"], [class*=\"modal\"]').forEach(el => el.remove())")`
- **状态检查**：
  `browser.is_visible(selector)`
- **键盘干预**：
  `browser.press("Escape")`

## 注意事项
- **死循环预防**：设置最大重试次数（建议不超过 2 次），防止弹窗关闭后立即重新弹出的死循环。
- **动态 ID 陷阱**：避免使用类似 `button-12345` 的动态 ID，应使用 `has-text` 或 `aria-label` 等语义化选择器。
- **等待延迟**：部分弹窗有淡入动画，点击前应确保元素已处于 `stable` 状态。
- **Cookie 策略**：拒绝 Cookie 可能导致某些功能不可用，优先选择“接受必要 Cookie”。

## 示例
### 场景：处理 Google 搜索时的 Cookie 同意弹窗
```javascript
// 1. 识别弹窗
const isCookiePopup = await browser.is_visible('text="Before you continue to Google"');
if (isCookiePopup) {
  // 2. 点击“接受全部”
  await browser.click('button:has-text("Accept all")');
  // 3. 等待消失
  await browser.wait_for_selector('text="Before you continue"', { state: 'hidden' });
}
```

### 场景：移除无法点击的透明遮罩
```javascript
await browser.evaluate(() => {
  const overlays = document.querySelectorAll('[style*="z-index"], [class*="overlay"]');
  overlays.forEach(el => {
    if (window.getComputedStyle(el).position === 'fixed') el.remove();
  });
  document.body.style.overflow = 'auto'; // 恢复滚动条
});
```