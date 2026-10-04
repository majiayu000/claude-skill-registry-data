---
name: amazon-product-image
description: 按关键词批量下载 Amazon 搜索结果页产品图，多关键词自动分文件夹存储
title: 亚马逊产品图下载
example: 在亚马逊上搜索“wireless earbuds”（无线耳机），下载前5个商品的全部主图并保存到我的桌面文件夹。
version: 1.0.1
---
# Amazon产品图片采集 Skill

## 1. 适用范围

本 skill 适合以下任务：

- 电商选品：批量下载 Amazon 搜索结果中的产品主图进行视觉分析。
- 竞品监控：按品牌/品类关键词采集竞品产品图片。
- 数据集构建：为机器学习/图像分类任务收集电商产品图片。
- 市场调研：快速获取某品类的产品图片样本。

不要用本 skill 处理其他电商平台的图片下载。如果用户需求落在上述范围外，直接向用户说明本 skill 不覆盖该场景。

## 2. 核心工作机制 (BrowserWorker Plugin)

- **插件浏览器操控**：本技能通过项目内置 `BrowserWorker` 插件 daemon 执行浏览器动作，不直接依赖用户机器上的 Chrome、ChromeDriver、Playwright、Selenium、requests 等环境。
- **跨平台端口发现**：`run.py` 会优先读取 `BrowserWorker_PORT` / `MANAI_BROWSER_CONTROL_PORT`，其次读取工作区 `storage/browser_daemon.lock`，最后使用默认端口 `12321`；daemon 未响应时会尝试从项目内 `BrowserWorker` 目录自动启动。
- **Action 执行方式**：通过 BrowserWorker `/execute` 调用本技能的 `scripts/actions/collect_images.py`，action 使用 `browser.goto`、`browser.evaluate`、`browser.scroll`、`browser.wait_ms` 和 `browser.request_help` 完成页面交互。
- **页面状态检测**：action 使用 BrowserWorker 框架级 `detect_page_state(domain_hint=...)` 判断 `login/captcha/region_prompt/blocked/empty_result` 等通用状态，不维护商品页专用检测逻辑。
- **人工协助**：遇到 Amazon 登录、验证码、地区确认等必须人工处理的页面时，action 会调用 `request_help(validate_after=True)`，用户继续后由框架二次校验页面状态。

## 3. 调用参数格式

### 动作：`collect_images` (批量下载亚马逊产品图)
- **Action**: `"collect_images"`
- **Args**:
  - `keywords`: 搜索关键词，多个关键词用换行 `\n` 分隔（`string`，必填）
  - `image_save_path`: 图片存放的本地文件夹路径（`string`，必填）
  - `max_images_per_keyword`: 每个关键词最多下载图片数（`integer`，可选；默认 `0` 表示不限制，测试时建议传较小值）

**调用示例：**
```json
{
  "action": "collect_images",
  "action_search_path": "<skill_path>/scripts/actions",
  "args": {
    "keywords": "iphone case\nusb cable",
    "image_save_path": "C:\\Users\\Desktop\\amazon_images",
    "max_images_per_keyword": 20
  }
}
```

---

## 4. 不可违反的原则

1. **先确认，后执行**：收集完需求后，必须用自然语言复述已识别的筛选和下载条件并等待用户确认；用户确认前不要执行。
2. **严格的参数校验**：LLM 在执行 `collect_images` 之前，必须先对传入参数进行合法性检查，不满足时反馈错误并不执行。
3. **合规低频执行**：如果页面跳转或出现验证码/登录过期，通过插件浏览器的人工协助窗口提示用户处理。

## 5. 标准工作流

### Step 1：收集需求
问清这些信息（用户没有要求的使用默认值，不要强行追问）：
- `keywords`：搜索关键词（必填，多个用 `\n` 分隔）
- `image_save_path`：本地图片存放路径（必填）

### Step 2：复述并确认
复述用户启用的业务条件，不暴露内部字段名。待用户确认后再继续。

### Step 3：执行下载
调用 BrowserWorker 插件接口，传入 `action: "collect_images"`、`action_search_path` 及相应参数执行；或直接通过本目录 `run.py collect_images` 间接调用。
- **登录与异常状态判定**：如果接口提示需要登录或验证码，直接让用户在插件浏览器中完成，不要求用户安装或打开本机 Chrome。

### Step 4：汇报结果
向用户汇报每个关键词的下载数量与详细统计信息。

---

## 6. 参数校验规则

| 参数 | 必填 | 类型 | 校验规则 | 不满足时的反馈话术 |
|------|------|------|----------|-------------------|
| `keywords` | ✅ | `string` | 不能为空字符串 | "参数 `keywords` 为必填项，请提供搜索关键词。" |
| `image_save_path` | ✅ | `string` | 不能为空字符串 | "参数 `image_save_path` 为必填项，请提供图片存放路径。" |
| `max_images_per_keyword` | ❌ | `integer` | 非负整数；测试或演示时建议不超过 3 | "参数 `max_images_per_keyword` 必须是非负整数。" |
