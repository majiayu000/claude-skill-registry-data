---
name: shopify-setup-prep
description: 引导用户完成 Shopify 店铺注册、创建并安装私密应用，自动换取和验证 Admin API Access Token，最终将店铺域名与
  Token 写入配置。
title: Shopify建站准备
example: 引导我在 BrowserWorker 插件浏览器中注册并授权安装指定的 Shopify 店铺应用，获取建站所需的访问凭证。
version: 1.0.1
---
# Shopify 建站前准备 Skill

## 用途
引导用户注册 Shopify 店铺 + 获取 Admin API Access Token。不涉及品牌设计、选品、上架。

## ⚡ 凭证获取优先级（读我，再执行）

**用户已提供 域名 + Client ID + Client Secret → 跳过注册/创建App，直接调用 `shopify_exchange_token` 换取/验证 Token**：
- 直接通过 BrowserWorker `/execute` 执行 `shopify_exchange_token` 动作：
  ```json
  {
    "action": "shopify_exchange_token",
    "action_search_path": "<skill_path>/scripts/actions",
    "args": {
      "shop": "店铺域名",
      "client_id": "Client_ID",
      "client_secret": "Client_Secret"
    }
  }
  ```
- ✅ 成功 → 完成并自动更新凭证配置。
- ❌ 失败（提示 400）→ 此时才告知用户"App 可能未安装或凭证错误"，走下方流程的第 2-3 步（创建 App + 安装）。

**用户未提供凭证** → 走下方完整 4 步流程。

## 触发条件
- "帮我开店"、"开个站"、"注册 Shopify"
- "准备建站"、"获取 API Token"、"取 API Key"
- "还没开店呢"、"没有 Shopify 账号"

## 不适用场景
- 品牌定位、选品策略 → 用对应 skill
- 已有 Token 要上架商品 → 用 shopify-builder

---

## 全流程 (BrowserWorker Plugin Flow)

本技能使用项目内置 `BrowserWorker` 插件浏览器，不要求用户机器安装 ChromeDriver、Playwright、Selenium 或 requests。遇到 Shopify 登录、邮箱验证、安装授权或验证码时，通过插件浏览器人工协助完成。

- 打开 Shopify 后必须调用框架级 `detect_page_state(domain_hint="<shop>.myshopify.com")`，按 `state/confidence/reason/suggested_action` 判断页面是否可继续。
- 人工登录、邮箱验证、授权安装或验证码使用 `request_help(validate_after=True)`；继续换 token 前必须二次校验不再处于 `login/captcha/blocked/wrong_domain/page_error`。
- 可能等待人工处理的 action 已声明 `max_runtime_ms`，CLI 外层 `/execute` timeout 需要覆盖人工协助等待时间。
- 不要通过本机默认浏览器、Playwright、Selenium、ChromeDriver、直接 CDP 或 `requests` 实现登录/验证流程。

---

### 第 1 步：引导用户注册 Shopify 店铺

**Agent 通过 BrowserWorker 插件浏览器打开注册页面**：

```json
{
  "action": "flexible_access",
  "action_search_path": "<BrowserWorker>/browser_service/actions",
  "args": {
    "steps": [
      {"op": "goto", "args": ["https://www.shopify.com/free-trial"]}
    ],
    "keep_open": true
  }
}
```

**用户操作**：
- 填自己的邮箱
- 设密码
- **起一个店铺名** — 英文，简短好记。提示用户：系统自动生成 `店铺名.myshopify.com`，选定不可改。如果名字被占用会加后缀（如 `-3`）。

**Agent 确认**：拿到域名后记下来（注意后缀，如 `daxiong-3.myshopify.com`）。

---

### 第 2 步：引导创建 Custom App（店铺后台 Dev Dashboard）

**Dev Dashboard 入口**：店铺注册完成后，直接通过以下 URL 进入：
```
https://admin.shopify.com/store/{店铺slug}/settings/apps/development
```
其中 `{店铺slug}` 是 myshopify.com 域名的前缀部分。
例如：店铺域名 `w1nkff-aw.myshopify.com` → slug 为 `w1nkff-aw`。

**Agent 通过 BrowserWorker 插件浏览器打开 Dev Dashboard**：

```json
{
  "action": "flexible_access",
  "action_search_path": "<BrowserWorker>/browser_service/actions",
  "args": {
    "steps": [
      {"op": "goto", "args": ["https://admin.shopify.com/store/{店铺slug}/settings/apps/development"]}
    ],
    "keep_open": true
  }
}
```

**引导与提示**：
1. 如需邮箱验证 → 让用户去邮箱点验证链接，验证后刷新继续。
2. 提示用户点击「Create an app」→ 名称填 `ManAI`。
3. 进入 App 配置页 → 点击「Configure Admin API scopes」。
4. 勾选全部 read + write 权限：
   - products / orders / inventory / themes / content
5. 点击「Save」→ 回到 App 概览页 → 点击「Release」发布版本。
6. 进入「API credentials」标签页，复制并获取 Client ID + Client Secret（shpss_xxx 格式）。

---

### 第 3 步：引导安装 App 到店铺 ⚠️

> **Dev Dashboard 发布版本 ≠ App 已安装。不安装的话换 Token 会报 400。**

**Agent 提示用户进行安装**：
1. 指引打开：`https://admin.shopify.com/store/{店铺slug}/settings/apps/development`
2. 找到 ManAI 并点击「Install app」，确认安装。

---

### 第 4 步：调用 Action 自动换取与验证 Access Token

不再需要用户手动在本地执行任何 PowerShell 或 Bash 脚本，Agent 直接通过 BrowserWorker `/execute` 执行自定义 Action `shopify_exchange_token`：

```json
{
  "action": "shopify_exchange_token",
  "action_search_path": "<skill_path>/scripts/actions",
  "args": {
    "shop": "店铺名.myshopify.com",
    "client_id": "Client_ID",
    "client_secret": "Client_Secret"
  }
}
```

**执行逻辑说明**：
- 底层使用 Python 标准库自动发起 Token 交换请求。
- 会直接访问 `shop.json` 进行有效性校验。
- 校验成功后会自动搜索并更新本地所有可用的 `USER.md` 凭证记录，免除手动写入。

**异常状态与重试判定**：
- 如果动作返回失败（例如 400），且确认参数正确，可能是安装有延迟，提示用户稍等 1-2 分钟后再告知重试。
- 若仍失败，提示用户去店铺后台确认 App 是否已正确安装且处于“已安装（Installed）”状态。
- 若返回登录、验证码、页面状态异常或人工处理超时，先让用户在插件浏览器中完成处理；不要自动反复请求 Shopify。

---

## 校验规则

| 参数 | 必填 | 类型 | 校验规则 | 不满足时的反馈话术 |
|------|------|------|----------|-------------------|
| `shop` | ✅ | `string` | 不能为空字符串，需包含店铺名或完整 myshopify.com 域名 | "店铺域名不能为空，请输入正确的 Shopify 店铺域名或名称。" |
| `client_id` | ✅ | `string` | 不能为空字符串 | "Client ID 不能为空，请在 App API 凭证页面复制并提供。" |
| `client_secret` | ✅ | `string` | 不能为空 | "Client Secret 不能为空，请在 App API 凭证页面复制并提供。" |
