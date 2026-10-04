---
name: cj-dropshipping-api
description: 打通CJ Dropshipping全链路，搜品、下单、跟踪一键调用
tool_triggers:
- tool: bash
  args:
    command: /accio-mcp-cli\s+call\s+(?:start_cj_auth|get_cj_access_token)\b/i
title: CJ代发货源
example: |-
  怎么使用？
  Use when integrating CJ Dropshipping API V2.0 — products, orders (Shopping API), logistics, webhooks, Shopify delivery profiles. Business calls are REST against `developers.cjdropshipping.com`; use `accio-mcp-cli` only to obtain OAuth tokens (`start_cj_auth`, `get_cj_access_token`), not for produ...
version: 1.0.0
---
# CJ Dropshipping API V2.0

**accio-mcp-cli** 仅用于 **CJ OAuth 认证和读取存储的令牌**（`start_cj_auth`、`get_cj_access_token`）。其余所有功能——商品搜索、订单、物流、Webhook、伙伴刊登——均遵循第 2 节起的 **REST API**：使用 `get_cj_access_token` 获取的 **`CJ-Access-Token`** 请求头调用 `https://developers.cjdropshipping.com/api2.0/v1/...`。

两个认证调用的 CLI 参数（如 `--port`、`--raw`、`--refresh`），请参阅 **accio-mcp-cli** 技能。

## 1. 认证（仅限 accio-mcp-cli）

执行一次 OAuth，然后在每次 REST 请求前读取令牌。

```bash
accio-mcp-cli call start_cj_auth
accio-mcp-cli call get_cj_access_token
```

| 步骤 | 命令 |
|------|---------|
| 启动 OAuth（用户在浏览器中完成授权链接） | `accio-mcp-cli call start_cj_auth` |
| 读取存储的令牌对 | `accio-mcp-cli call get_cj_access_token` |

将返回的 `accessToken` 作为 **`CJ-Access-Token`** 用于下方所有 REST 调用。如需完整的网关 JSON，请在 `get_cj_access_token` 后附加 `--raw`。

**返回数据示例**（字段可能有所差异；使用 `--raw` 可获取精确的 MCP 结果）：

```json
{
  "provider": "cj",
  "accessToken": "...",
  "accessTokenExpiryDate": "...",
  "refreshToken": "...",
  "refreshTokenExpiryDate": "..."
}
```

## 2. 商品管理与刊登

所有商品接口均需要：
- `CJ-Access-Token: YOUR_ACCESS_TOKEN`

### 2.1 获取分类列表
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/getCategory`

返回 CJ 分类树。

### 2.2 获取商品列表（V2）
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/listV2`

新集成的主要商品搜索/列表接口。

**查询参数：**
- `page`：页码，默认 `1`，最小 `1`，最大 `1000`
- `size`：每页数量，默认 `20`，最小 `1`，最大 `100`
- `keyWord`：搜索关键词，匹配商品名称或 SKU
- `categoryId`：分类 ID 过滤
- `countryCode`：仅返回指定国家有库存的商品
- `minPrice`：最低价格
- `maxPrice`：最高价格
- `features`：可选扩展参数，用于展开商品/分类详情

### 2.3 获取商品详情
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/query`

获取单个商品及其规格信息。

**查询参数：**
- `pid`：商品 ID。从 `pid`、`productSku`、`variantSku` 中选一个
- `productSku`：商品 SKU。从 `pid`、`productSku`、`variantSku` 中选一个
- `variantSku`：规格 SKU。从 `pid`、`productSku`、`variantSku` 中选一个
- `countryCode`：可选，库存国家过滤
- `features`：可选，已记录的支持值：
  - `enable_combine`
  - `enable_video`
  - `enable_inventory`

**重要说明：** 本接口请勿使用未记录的查询参数，如 `productId` 或 `variantId`。

### 2.4 获取所有规格
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/variant/query`

**查询参数：**
- `pid`：从 `pid`、`productSku`、`variantSku` 中选一个
- `productSku`：从 `pid`、`productSku`、`variantSku` 中选一个
- `variantSku`：从 `pid`、`productSku`、`variantSku` 中选一个
- `countryCode`：可选，库存国家过滤

### 2.5 获取规格详情
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/variant/queryByVid`

**查询参数：**
- `vid`：规格 ID
- `features`：可选。使用 `enable_inventory` 可包含库存详情

### 2.6 按规格 ID 获取库存
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryByVid`

**查询参数：**
- `vid`：规格 ID

### 2.7 按 SKU 获取库存
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/queryBySku`

**查询参数：**
- `sku`：SKU 或 SPU

### 2.8 按商品 ID 获取库存
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/stock/getInventoryByPid`

**查询参数：**
- `pid`：商品 ID

### 2.9 添加到我的商品
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/addToMyProduct`

**请求体：**
```json
{
  "productId": "CJ_PRODUCT_ID"
}
```

### 2.10 查询我的商品
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/myProduct/query`

**查询参数：**
- `keyword`：SKU/SPU/商品名称
- `categoryId`：分类过滤
- `startAt`：开始时间
- `endAt`：结束时间
- `isListed`：刊登状态过滤
- `visiable`：可见性过滤
- `hasPacked`：打包状态过滤
- `hasVirPacked`：虚拟打包状态过滤

### 2.11 商品评价
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/product/productComments`

**查询参数：**
- `pid`：商品 ID
- `score`：可选评分过滤
- `pageNum`：页码，默认 `1`
- `pageSize`：每页数量，默认 `20`

### 2.12 批量刊登
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/listedByPids`

将 CJ 商品刊登到第三方店铺（如 Shopify）。

**请求头：**
- `CJ-Access-Token: USER_TOKEN`

**请求体：**
```json
{
  "shopIds": ["..."],
  "productIds": ["..."],
  "formula": {
    "formulaType": 1,
    "formulaNumber": 15,
    "shippingFrom": "CN",
    "shippingTo": "US",
    "isLogistics": 1
  },
  "templateShopCategoryVOList": [
    {
      "shopId": "...",
      "deliveryProfileId": "..."
    }
  ]
}
```
*注意：Shopify 平台通常必须提供 `deliveryProfileId`，否则会触发 7001001 错误。*

### 2.13 查询平台分类树
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getPlatformCategoryTree`

获取目标平台的分类/集合（如 Shopify Collections）。

### 2.14 查询供应商列表
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/queryVendors`

获取指定店铺的可用供应商列表。

### 2.15 获取 CJ 默认配送模板
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getCjDefaultDeliveryProfile`

返回默认配送模板，可用作 `createDeliveryProfile` 的基础。

### 2.16 创建配送模板
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/createDeliveryProfile`

在目标 Shopify 店铺中创建新的配送模板。需要提供 `locationIds` 列表和 `zones`（含国家和省份）。

### 2.17 更新配送模板
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/updateDeliveryProfile`

更新现有配送模板。

### 2.18 删除配送模板
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/removeDeliveryProfile`

删除配送模板。

### 2.19 查询店铺仓库位置
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/shop/location/queryList`

列出店铺的所有履约仓库位置。用于识别"CJ Dropshipping"位置 ID（`fromCj: true` 的位置）。

### 2.20 查询国家与省份
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/shop/property/queryCountries`

返回支持的国家及其省份/州列表，构建配送模板的 `zones` 对象时必须调用。

## 3. 订单处理（购物）

### 3.1 创建订单 V2
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/shopping/order/createOrderV2`

**请求头：**
- `CJ-Access-Token: YOUR_ACCESS_TOKEN`

**请求体：**
```json
{
  "orderNumber": "YOUR_ORDER_ID_123",
  "shippingZip": "10001",
  "shippingCountryCode": "US",
  "shippingCountry": "United States",
  "shippingProvince": "New York",
  "shippingCity": "New York",
  "shippingAddress": "123 Main St",
  "shippingCustomerName": "John Doe",
  "shippingPhone": "1234567890",
  "remark": "Dropshipping order",
  "fromCountryCode": "CN",
  "logisticName": "CJPacket Sensitive",
  "payType": "1",
  "products": [
    {
      "vid": "CJ_VARIANT_ID",
      "quantity": 1
    }
  ]
}
```
*`payType`：1（URL 支付）、2（余额支付）、3（仅创建）*

### 3.2 获取订单详情/列表
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list`
*（注：搜索用 `list`，获取单条详情用 `queryById`；若 `list` 不是标准路径，请查阅文档确认确切路径）*

**列表接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/shopping/order/list`（标准 V2 模式，支持按 `orderNumber`、`cjOrderCode`、`status` 等过滤）

**查询参数：**
- `page`: 1
- `size`: 20
- `orderNumber`：您的订单 ID
- `cjOrderCode`：CJ 订单 ID
- `status`：订单状态（如 '10' 表示已支付）

### 3.3 确认订单（支付）
若使用了 `payType=3`，通过以下接口确认/支付：
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/shopping/pay/payBalance`

**请求体：**
```json
{
  "orderIdList": ["CJ_ORDER_ID_1", "CJ_ORDER_ID_2"]
}
```

## 4. 物流

### 4.1 运费计算
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate`

**请求体：**
```json
{
  "startCountryCode": "CN",
  "countryCode": "US",
  "products": [
    {
      "vid": "CJ_VARIANT_ID",
      "quantity": 1
    }
  ]
}
```

### 4.2 物流跟踪
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo`

**查询参数：**
- `trackNumber`：追踪号（批量查询可重复：`?trackNumber=A&trackNumber=B`）

### 4.3 查询配送模板（伙伴）
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/queryDeliveryProfiles`

获取刊登时需绑定的 Shopify 配送模板。

### 4.4 查询收件国家信息
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/product/listed/getReceiverCountryInfo`

## 5. Webhook

配置 Webhook 以接收实时更新。

**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/webhook/set`

**请求体：**
```json
{
  "product": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/product"] },
  "stock": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/stock"] },
  "order": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/order"] },
  "logistics": { "type": "ENABLE", "callbackUrls": ["https://your-domain.com/webhook/logistics"] }
}
```

**事件类型：**
- `product`：价格/库存变更（请查阅文档确认具体 payload 类型）
- `stock`：库存更新
- `order`：状态变更（已支付、已发货、已完成）
- `logistics`：物流跟踪更新

## 6. 账号设置

### 6.1 获取账号设置
**接口：** `GET https://developers.cjdropshipping.com/api2.0/v1/setting/get`

返回账号信息、API 配额及当前 Webhook 配置。

### 6.2 设置 Webhook 回调
**接口：** `POST https://developers.cjdropshipping.com/api2.0/v1/setting/setCallback`

**请求体：**
```json
{
  "product": {"type": "ENABLE", "urls": ["..."]},
  "stock": {"type": "ENABLE", "urls": ["..."]},
  "order": {"type": "ENABLE", "urls": ["..."]},
  "logistic": {"type": "ENABLE", "urls": ["..."]}
}
```

## 7. 店铺 API（伙伴模式）

这些接口用于管理店铺连接和设置。

### 7.1 查询店铺列表
**接口：** `GET /shop/getShops`

**说明：** 返回用户已授权的店铺列表。成功状态码为 `0`。
**注意：** 相对路径，基础 URL 需通过伙伴系统确认。

---

## 8. API 参考（详细）

伙伴/ERP 集成的详细文档：
- [伙伴集成指南（ERP/平台）](references/partner_integration.md)

本节提供伙伴/刊登 API 接口摘要。

### 8.1 批量刊登商品（listedByPids）
**接口：** `POST /product/listed/listedByPids`

**请求体（JSON）：**
| 字段 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `shopIds` | Set<String> | 是 | 目标店铺 ID（如 `["shop_id"]`）。 |
| `productIds` | List<String> | 是 | 要刊登的 CJ 商品 ID。 |
| `formula` | Object | 是 | 刊登定价公式。 |
| `formula.formulaType` | Integer | 是 | 0-固定，1-加价，2-百分比，3-推荐。 |
| `formula.formulaNumber` | BigDecimal | 是 | 公式数值/倍数（类型非 3 时必填）。 |
| `formula.shippingFrom` | String | 是 | 发货国代码（如 `"CN"`）。 |
| `formula.shippingFromName` | String | 是 | 发货国名称（如 `"China"`）。 |
| `formula.shippingTo` | String | 是 | 目的国代码（如 `"US"`）。 |
| `formula.shippingToName` | String | 是 | 目的国名称（如 `"United States"`）。 |
| `formula.logisticsMaxDay` | Integer | 是 | 最长送达天数（如 `30`）。 |
| `formula.logisticsMaxPrice` | BigDecimal | 是 | 最高物流费用（如 `100.00`）。 |
| `formula.logisticsType` | Integer | 是 | 物流类型（如 `0`）。 |
| `formula.isLogistics` | Integer | 是 | 1：含物流费，0：不含。 |
| `templateShopCategoryVOList` | List<Object> | 否 | Shopify 店铺必填。 |
| `templateShopCategoryVOList[].shopId` | String | 是 | 店铺 ID。 |
| `templateShopCategoryVOList[].deliveryProfileId` | String | 是 | Shopify 配送模板 ID。 |

**请求示例：**
```json
{
  "shopIds": ["2603221653513529700"],
  "productIds": ["1772614144538193920"],
  "formula": {
    "formulaType": 3,
    "shippingFrom": "CN",
    "shippingFromName": "China",
    "shippingTo": "US",
    "shippingToName": "United States",
    "logisticsMaxDay": 30,
    "logisticsMaxPrice": 100.00,
    "logisticsType": 0,
    "isLogistics": 1
  },
  "templateShopCategoryVOList": [
    {
      "shopId": "2603221653513529700",
      "deliveryProfileId": "112235774194"
    }
  ]
}
```

### 8.2 查询平台分类树
**接口：** `POST /product/listed/getPlatformCategoryTree`

**请求体（JSON）：**
| 字段 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `shopId` | String | 是 | 目标店铺 ID。 |
| `countryCode` | String | 否 | 按国家站点过滤。 |
| `pageNum` | Integer | 否 | 默认 1。 |

**响应数据（`data` 字段）：**
包含 `categoryVOS` 列表。对于 Shopify：
- `categoryLevel 0`：自定义集合（Custom Collections）。
- `categoryLevel 1`：智能集合（Smart Collections）。

### 8.3 查询店铺配送模板
**接口：** `POST /product/listed/queryDeliveryProfiles`

**请求体（JSON）：**
| 字段 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `shopId` | String | 否 | 目标店铺 ID。 |
| `forceRefresh` | Boolean | 否 | 强制刷新缓存。 |

### 8.4 获取访问令牌（伙伴模式）
**接口：** `POST /authentication/getAccessToken`

**成功响应（`data` 字段）：**
- `accessToken`：用于 `CJ-Access-Token` 请求头的令牌。
- `accessTokenExpiryDate`：令牌过期时间戳。
- `refreshToken`：用于刷新会话的令牌。
- `openId`：用户在平台中的唯一标识。

### 8.5 店铺 API - 获取店铺列表
**接口：** `GET /shop/getShops`

**响应示例：**
```json
{
  "success": true,
  "code": 0,
  "data": [
    {
      "shopId": "...",
      "shopName": "...",
      "platformName": "Shopify",
      "currencyCode": "USD"
    }
  ]
}
```

---

## 常见错误码
- `200`：成功
- `1600100`：参数错误
- `1601000`：用户不存在
- `500`：系统错误（请稍后重试）

## 9. 故障排查与常见错误

### 9.1 错误码 400：请求参数错误
- **原因**：`formula` 中缺少必填字段（如 `shippingFrom`、`shippingTo`），或 Shopify 店铺缺少 `templateShopCategoryVOList`。
- **解决**：确保所有必填字段均已填写。Shopify 平台需提供有效的 `deliveryProfileId`。

### 9.2 错误码 7001001：模板缺少配送模板
- **原因**：Shopify 店铺要求为商品分配配送模板，但未传入 `deliveryProfileId`。
- **解决**：通过 `/product/listed/queryDeliveryProfiles` 查询可用模板，并将 ID 传入 `templateShopCategoryVOList`。

### 9.3 错误码 7001003：配送模板不包含应用创建的仓库位置
- **原因**：Shopify 配送模板未启用"CJ Dropshipping"仓库位置。
- **API 自动修复**：
    1. 通过 `/api/shop/location/queryList` 查询所有位置，找到 `fromCj: true` 的位置。
    2. 通过 `/api/product/listed/createDeliveryProfile` 创建新配送模板，或更新现有模板，将该位置 ID 加入 `locationIds`。
    3. 对于有省份的国家（如美国），需在 `zones.countries` 数组中明确提供所有省份。
- **手动修复**：引导用户进入 **Shopify 后台 > 设置 > 配送与交付**，编辑配送模板，将"CJ Dropshipping"位置添加进去。

## 10. 最佳实践
1. **检查 `deliveryProfileOpen`**：通过 `getShops` 查询店铺时，若 `deliveryProfileOpen=1`，刊登时必须提供 `deliveryProfileId`。
2. **缓存访问令牌**：不要每次调用都重新获取令牌，将其存储至接近过期时再刷新。
3. **遵守速率限制**：遵循 `setting/get` 接口返回的 QPS 限制。
4. **使用 Webhook**：优先使用 Webhook 而非轮询获取订单状态更新。
5. **记录请求 ID**：在响应中记录 `requestId`，方便与 CJ 客服协作排查问题。

## 11. Shopify 配送模板自动化工作流

在 Shopify 上刊登商品时，按以下自动化流程处理配送模板：

1. **检查要求**：通过 `/shop/getShops` 获取店铺列表。若目标店铺的 `deliveryProfileOpen: 1`，则需继续处理配送模板。
2. **识别 CJ 仓库位置**：调用 `/shop/location/queryList`，找到 `fromCj: true` 的位置，保存该 `id`（即 CJ 应用仓库位置 ID）。
3. **查询省份（如需）**：若发货目的地为美国等需要强制填写省份的国家，调用 `/shop/property/queryCountries` 获取省份代码列表。
4. **配置配送模板**：
   - 调用 `/product/listed/queryDeliveryProfiles` 查看现有模板。
   - 若有效模板已包含 CJ 位置，直接使用其 ID。
   - 否则，使用 CJ 位置 ID 和所需的国家/省份 zones 调用 `/product/listed/createDeliveryProfile` 创建新模板。
5. **执行刊登**：调用 `/product/listed/listedByPids` 时，将配送模板 ID 通过 `templateShopCategoryVOList` 传入。
