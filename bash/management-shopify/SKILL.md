---
name: management-shopify
description: 覆盖Shopify店铺全流程管理，精通产品/订单/客户/库存/折扣/主题的GraphQL查询与变更操作
metadata:
  requires:
    bins:
    - shopify
  cliHelp: shopify --help
title: Shopify店铺管理
example: |-
  怎么使用？
  告诉我店铺域名，查询产品列表、订单状态和客户数据
  给出GraphQL查询语句，执行产品/订单/库存/折扣等任意数据检索
  确认后执行mutation操作，创建商品、调整库存、更新订单
version: 1.0.0
---
# Shopify CLI

`shopify` 是 Shopify 官方 CLI。本技能的目标是让 AI 知道如何使用用户本机已经安装并完成授权的 Shopify CLI。

使用本技能时，所有 Shopify 店铺数据操作都必须优先通过本地 `shopify` 命令完成：

- `shopify auth login`：登录 Shopify 账号。
- `shopify store auth`：为指定店铺授权 Admin API scopes。
- `shopify store execute`：使用已保存的店铺授权执行 Admin GraphQL 查询或 mutation。

不要要求用户提供 Admin API access token，也不要默认改用 curl/HTTP GraphQL。连接、授权和数据操作都应围绕本地 Shopify CLI 展开。

---

## 一、CLI 安装判断

AI 使用 Shopify CLI 前，先判断本机是否已安装 `shopify` 命令。

```bash
shopify --version
```

判断规则：

| 场景 | 判断 | AI 行为 |
|---|---|---|
| 返回版本号 | 已安装 | 继续执行连接状态判断 |
| 提示 command not found / 不是内部或外部命令 | 未安装 | 停止 Shopify 操作，说明 Shopify CLI 未安装 |
| 命令存在但返回异常 | 安装异常 | 停止 Shopify 操作，展示错误摘要 |

安装命令参考：

```bash
npm install -g @shopify/cli@latest
```

在 ManAI 内置环境中，通常由 ManAI 完成安装；AI 不应擅自更换全局 Node.js 或删除用户本机安装。

不要使用以下旧命令判断 CLI 安装或连接状态：

```bash
shopify auth status
shopify whoami
shopify store list
```

这些命令在 Shopify CLI v4.1.0 中不可依赖，可能不存在或不能准确表达当前账号和店铺授权状态。

---

## 二、连接状态判断

连接状态包含两层：

1. Shopify 账号登录状态。
2. Shopify 店铺授权状态。

AI 应自行判断连接状态：读取 Shopify CLI 本地配置，先发现已授权店铺域名，再用 `shopify store execute` 做真实连接验证。

### 2.1 安全规则

允许读取和展示：

- `store`
- `*.myshopify.com` 店铺域名
- 诊断时的缺失 scope 名称

禁止展示：

- `accessToken`
- `refreshToken`
- `sessionStore`
- `currentSessionId`
- 完整 `config.json`
- 完整 `sessionsByUserId`
- 完整授权对象

读取配置文件的目的只限于发现店铺域名和诊断连接状态。最终连接状态必须以 `shopify store execute` 查询结果为准。

### 2.2 账号登录状态诊断

账号登录配置位置：

Windows：

```text
%APPDATA%\shopify-cli-kit-nodejs\Config\config.json
```

macOS：

```text
~/Library/Preferences/shopify-cli-kit-nodejs/config.json
```

诊断命令只输出是否存在账号会话摘要，不输出原始配置：

Windows：

```bash
node -e "const fs=require('fs'),path=require('path'); const p=path.join(process.env.APPDATA,'shopify-cli-kit-nodejs','Config','config.json'); if(!fs.existsSync(p)){console.log(JSON.stringify({loggedIn:false,reason:'missing_account_config'}));process.exit(0)} const j=JSON.parse(fs.readFileSync(p,'utf8')); console.log(JSON.stringify({loggedIn:Boolean(j.currentSessionId&&j.sessionStore),hasAccountSession:Boolean(j.currentSessionId&&j.sessionStore)}))"
```

macOS：

```bash
node -e "const fs=require('fs'),path=require('path'),os=require('os'); const p=path.join(os.homedir(),'Library','Preferences','shopify-cli-kit-nodejs','config.json'); if(!fs.existsSync(p)){console.log(JSON.stringify({loggedIn:false,reason:'missing_account_config'}));process.exit(0)} const j=JSON.parse(fs.readFileSync(p,'utf8')); console.log(JSON.stringify({loggedIn:Boolean(j.currentSessionId&&j.sessionStore),hasAccountSession:Boolean(j.currentSessionId&&j.sessionStore)}))"
```

判断规则：

| 场景 | 判断 | AI 行为 |
|---|---|---|
| `loggedIn=true` | Shopify 账号已登录 | 继续判断店铺授权状态 |
| `missing_account_config` | Shopify 账号未登录 | 停止店铺数据操作，说明需要先完成账号登录 |
| `loggedIn=false` | Shopify 账号会话无效 | 停止店铺数据操作，说明需要重新登录 |

账号登录命令：

```bash
shopify auth login
```

Windows 非交互管道可用于跳过 “Press any key” 提示：

```cmd
echo. | shopify auth login
```

登录命令会打开浏览器或输出授权链接。AI 不能替用户完成网页登录、人机验证或账号密码输入。

### 2.3 店铺授权域名发现

店铺授权配置位置：

Windows：

```text
%APPDATA%\shopify-cli-store-nodejs\Config\config.json
```

macOS：

```text
~/Library/Preferences/shopify-cli-store-nodejs/config.json
```

Shopify CLI 店铺授权配置保存方式比较特殊：

- 顶层 key 通常形如 `7e9cb568cfd431c538f36d1ad3f2b4f6::cli-test001`。
- 域名后缀会被拆成嵌套对象，例如 `myshopify.com` 会保存为 `myshopify -> com`。
- 完整店铺域名可能出现在 session 的 `store` 字段中，例如 `cli-test001.myshopify.com`。
- 如果 session 里没有 `store` 字段，也可以从顶层 key 的 `::` 后半段加上嵌套路径推导，例如 `cli-test001` + `myshopify.com` = `cli-test001.myshopify.com`。

AI 发现店铺域名时必须同时支持两种来源：

1. 优先读取任意嵌套 session 对象中的 `store` 字段。
2. 兜底从配置 key 和嵌套路径推导 `*.myshopify.com` 域名。

Windows：

```bash
node -e "const fs=require('fs'),path=require('path'); const p=path.join(process.env.APPDATA,'shopify-cli-store-nodejs','Config','config.json'); if(!fs.existsSync(p)){console.log(JSON.stringify({stores:[]}));process.exit(0)} const j=JSON.parse(fs.readFileSync(p,'utf8')); const stores=new Set(); const valid=s=>/^[a-z0-9][a-z0-9-]*\.myshopify\.com$/i.test(s); function add(s){ if(typeof s==='string'&&valid(s)) stores.add(s.toLowerCase()); } function walk(v){ if(!v||typeof v!=='object') return; add(v.store); for(const child of Object.values(v)) walk(child); } walk(j); for(const [key,value] of Object.entries(j)){ const i=key.indexOf('::'); if(i<0) continue; const prefix=key.slice(i+2); if(!/^[a-z0-9][a-z0-9-]*$/i.test(prefix)||!value||typeof value!=='object') continue; if(value.myshopify&&typeof value.myshopify==='object'&&value.myshopify.com) add(prefix+'.myshopify.com'); } console.log(JSON.stringify({stores:[...stores]}))"
```

macOS：

```bash
node -e "const fs=require('fs'),path=require('path'),os=require('os'); const p=path.join(os.homedir(),'Library','Preferences','shopify-cli-store-nodejs','config.json'); if(!fs.existsSync(p)){console.log(JSON.stringify({stores:[]}));process.exit(0)} const j=JSON.parse(fs.readFileSync(p,'utf8')); const stores=new Set(); const valid=s=>/^[a-z0-9][a-z0-9-]*\.myshopify\.com$/i.test(s); function add(s){ if(typeof s==='string'&&valid(s)) stores.add(s.toLowerCase()); } function walk(v){ if(!v||typeof v!=='object') return; add(v.store); for(const child of Object.values(v)) walk(child); } walk(j); for(const [key,value] of Object.entries(j)){ const i=key.indexOf('::'); if(i<0) continue; const prefix=key.slice(i+2); if(!/^[a-z0-9][a-z0-9-]*$/i.test(prefix)||!value||typeof value!=='object') continue; if(value.myshopify&&typeof value.myshopify==='object'&&value.myshopify.com) add(prefix+'.myshopify.com'); } console.log(JSON.stringify({stores:[...stores]}))"
```

发现规则：

| 场景 | 判断 | AI 行为 |
|---|---|---|
| `stores` 为空 | 未发现已授权店铺 | 判断为店铺未连接，停止店铺数据操作 |
| `stores` 只有 1 个域名 | 发现唯一店铺 | 使用该域名执行连接验证，并在后续 `--store` 中复用 |
| `stores` 有多个域名 | 存在多个授权店铺 | 不猜测目标店铺；报告候选店铺域名，停止当前店铺数据操作 |

### 2.4 店铺连接验证

发现唯一店铺域名后，执行最小只读查询验证真实连接状态：

```bash
shopify store execute --store <store>.myshopify.com --query "query { shop { name myshopifyDomain } }" --json
```

判断规则：

| 场景 | 判断 | AI 行为 |
|---|---|---|
| 返回 `shop` 数据 | 店铺已授权且连接可用 | 后续命令复用该店铺域名 |
| 提示需要登录 | 账号未登录或会话失效 | 停止店铺数据操作，说明需要重新登录 |
| 提示需要先执行 `shopify store auth` | 店铺未授权 | 停止店铺数据操作，说明需要先完成店铺授权 |
| GraphQL `Access denied` | 缺少 scope | 说明缺少权限，并在需要时重新授权更多 scopes |
| 网络、验证码或超时错误 | 当前不可用 | 展示错误摘要，停止当前操作 |

### 2.5 店铺授权命令

当需要发起店铺授权时，使用 `shopify store auth`。`--store` 必须是连接流程或上下文中已经确定的 `*.myshopify.com` 店铺域名。

基础只读授权：

```bash
shopify store auth --store <store>.myshopify.com --scopes read_products,read_orders,read_customers,read_inventory,read_discounts --json
```

较完整的读写授权：

```bash
shopify store auth --store <store>.myshopify.com --scopes read_products,write_products,read_product_listings,read_orders,write_orders,read_all_orders,read_customers,write_customers,read_inventory,write_inventory,read_locations,read_discounts,write_discounts,read_price_rules,write_price_rules,read_fulfillments,write_fulfillments,read_assigned_fulfillment_orders,write_assigned_fulfillment_orders,read_merchant_managed_fulfillment_orders,write_merchant_managed_fulfillment_orders,read_third_party_fulfillment_orders,write_third_party_fulfillment_orders,read_content,write_content,read_files,write_files,read_themes,write_themes,read_script_tags,write_script_tags,read_marketing_events,write_marketing_events,read_analytics,read_reports,read_checkouts,write_checkouts,read_draft_orders,write_draft_orders,read_gift_cards,write_gift_cards,read_shipping,write_shipping,read_locales,write_locales,read_markets,write_markets,read_publications,write_publications,read_online_store_navigation,write_online_store_navigation,read_metaobjects,write_metaobjects,read_metaobject_definitions,write_metaobject_definitions,read_shopify_payments_payouts,read_shopify_payments_disputes --json
```

授权会打开浏览器并显示 Shopify 店铺安装/授权页面。AI 不能替用户完成网页登录、人机验证、店铺安装确认或账号密码输入。

### 2.6 scope 判断规则

Shopify CLI 落盘时，若同时申请 `read_xxx` 和 `write_xxx`，最终配置文件里可能只保存 `write_xxx`。

判断权限时必须使用以下规则：

| 需要的权限 | 可接受的已授权权限 |
|---|---|
| `write_xxx` | 必须存在 `write_xxx` |
| `read_xxx` | 存在 `read_xxx` 或对应 `write_xxx` 均可 |
| 没有对应 `write_xxx` 的特殊只读权限 | 必须存在该 `read_xxx` |

例如：

- 需要 `read_products` 时，已授权 `write_products` 也算满足。
- 需要 `read_orders` 时，已授权 `write_orders` 也算满足。
- 需要 `read_analytics` 时，必须已授权 `read_analytics`，不能用 `write_analytics` 代替。

---

## 三、CLI 功能使用介绍

### 3.1 通用执行规则

店铺数据操作优先使用：

```bash
shopify store execute --store <store>.myshopify.com --query "query { shop { name myshopifyDomain } }" --json
```

`shopify store execute` 会自动使用 Shopify CLI 保存的店铺授权。不要把问题转向 Admin API token、REST API token 或 curl。

复杂查询建议写入 `.graphql` 文件后使用 `--query-file`：

```bash
shopify store execute --store <store>.myshopify.com --query-file ./operation.graphql --json
```

带变量：

```bash
shopify store execute --store <store>.myshopify.com --query-file ./operation.graphql --variables "{\"id\":\"gid://shopify/Product/1\"}" --json
```

### 3.2 写操作安全规则

默认只执行查询 `query`。

当任务涉及创建、更新、删除、发布、关闭、取消、调整库存等会改变店铺数据的操作时：

1. 先说明将要修改的对象和字段。
2. 等待明确确认后再执行 mutation。
3. 执行 mutation 必须加 `--allow-mutations`。

示例：

```bash
shopify store execute --store <store>.myshopify.com --query "mutation { tagsAdd(id: \"gid://shopify/Product/123\", tags: [\"new\"]) { userErrors { field message } } }" --allow-mutations --json
```

### 3.3 查询店铺信息

```bash
shopify store execute --store <store>.myshopify.com --query "query { shop { name email myshopifyDomain currencyCode plan { displayName } } }" --json
```

### 3.4 查询产品列表

```bash
shopify store execute --store <store>.myshopify.com --query "query { products(first: 10) { edges { node { id title status vendor productType createdAt updatedAt } } } }" --json
```

分页查询：

```bash
shopify store execute --store <store>.myshopify.com --query "query { products(first: 10, after: \"CURSOR\") { edges { cursor node { id title status } } pageInfo { hasNextPage endCursor } } }" --json
```

### 3.5 查询单个产品

```bash
shopify store execute --store <store>.myshopify.com --query "query { product(id: \"gid://shopify/Product/PRODUCT_ID\") { id title descriptionHtml status vendor productType variants(first: 10) { edges { node { id title price sku inventoryQuantity } } } } }" --json
```

### 3.6 查询订单列表

```bash
shopify store execute --store <store>.myshopify.com --query "query { orders(first: 10, sortKey: CREATED_AT, reverse: true) { edges { node { id name createdAt displayFinancialStatus displayFulfillmentStatus totalPriceSet { shopMoney { amount currencyCode } } customer { id email displayName } } } } }" --json
```

注意：查询更早历史订单可能需要 `read_all_orders` 权限。

### 3.7 查询客户列表

```bash
shopify store execute --store <store>.myshopify.com --query "query { customers(first: 10) { edges { node { id displayName email phone createdAt numberOfOrders amountSpent { amount currencyCode } } } } }" --json
```

### 3.8 查询库存和地点

查询地点：

```bash
shopify store execute --store <store>.myshopify.com --query "query { locations(first: 20) { edges { node { id name address { city country } } } } }" --json
```

查询产品变体库存：

```bash
shopify store execute --store <store>.myshopify.com --query "query { products(first: 10) { edges { node { id title variants(first: 10) { edges { node { id title sku inventoryQuantity } } } } } } }" --json
```

### 3.9 查询折扣

```bash
shopify store execute --store <store>.myshopify.com --query "query { discountNodes(first: 10) { edges { node { id discount { __typename ... on DiscountCodeBasic { title status startsAt endsAt } ... on DiscountAutomaticBasic { title status startsAt endsAt } } } } } }" --json
```

### 3.10 查询 metaobjects

```bash
shopify store execute --store <store>.myshopify.com --query "query { metaobjectDefinitions(first: 10) { edges { node { id type name fieldDefinitions { key name type { name } } } } } }" --json
```

### 3.11 查询主题

```bash
shopify store execute --store <store>.myshopify.com --query "query { themes(first: 10) { edges { node { id name role createdAt updatedAt } } } }" --json
```

### 3.12 断开连接

```bash
shopify auth logout
```

该命令会退出 Shopify CLI 保存的账号会话。

除非任务明确要求断开连接，否则不要删除 Shopify CLI 本地配置文件。

### 3.13 错误处理

| 错误现象 | 常见原因 | 处理 |
|---|---|---|
| `To run this command, log in to Shopify` | 账号未登录 | 执行 `shopify auth login` |
| `Run shopify store auth first` | 店铺未授权 | 执行 `shopify store auth --store ... --scopes ... --json` |
| `invalid_scope` | scope 名称无效或当前店铺不支持 | 移除无效 scope 后重新授权 |
| `Token expired` | 浏览器授权超时 | 重新执行登录或店铺授权 |
| GraphQL `Access denied` | 缺少对应 scope | 重新执行店铺授权申请所需 scope |
| GraphQL `Field ... doesn't exist` | API 版本或字段错误 | 查询 Shopify Admin GraphQL 文档并修正 query |
| mutation 被拒绝 | 缺少 `--allow-mutations` 或权限不足 | 确认后加 `--allow-mutations`，必要时重新授权 |
