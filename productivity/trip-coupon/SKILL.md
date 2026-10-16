---
name: trip-coupon
display_name: 出行优惠券-支持滴滴出行、酒店优惠礼包（住宿打车天天领）
display_name_en: Trip Coupon
description: 获取出行优惠券，支持滴滴出行大礼包、酒店优惠大礼包（美团/同程/飞猪酒店券+打车券）。返回领取链接和二维码图片，用户可点击链接或扫描二维码在微信中领取优惠。
description_zh: 获取出行优惠券，支持滴滴出行大礼包、酒店优惠大礼包（美团/同程/飞猪酒店券+打车券）。返回领取链接和二维码图片，用户可点击链接或扫描二维码在微信中领取优惠。
description_en: Call trip/travel coupon API to fetch travel coupons including DiDi ride-hailing gift packages and hotel coupon bundles. Returns coupon links and QR code images for users to redeem via WeChat.
english_description: Call trip/travel coupon API to fetch travel coupons including DiDi ride-hailing gift packages and hotel coupon bundles. Returns coupon links and QR code images for users to redeem via WeChat.
version: 2.0.2
author: moooai
permissions: 网络访问权限（调用出行优惠券API）
homepage: https://github.com/moooai/trip-coupon
---

# 出行优惠券

## Overview

此skill通过调用出行优惠券API接口，获取滴滴出行大礼包和酒店优惠大礼包（住宿出行天天领）的优惠券信息。返回优惠券链接（coupon_url）和二维码图片（coupon_qrcode_img_url），供用户点击链接或扫描二维码领取优惠。

## Quick Start

1. 调用API: `GET https://agskills.moontai.top/coupon/trip`
2. 解析返回的JSON数组（滴滴出行、酒店优惠礼包及「更多优惠券」入口项）
3. 按平台分类展示优惠券信息
4. **重要**: coupon_url建议在微信中打开，或使用微信扫描二维码图片

## API配置

### 基础信息

| 配置项 | 值 |
|--------|-----|
| API地址 | `https://agskills.moontai.top/coupon/trip` |
| 认证方式 | 无需认证 |
| 请求方法 | GET |
| 返回格式 | JSON |

### 响应数据结构

```json
[
  {
    "title": "滴滴出行大礼包，打车券天天领",
    "coupon_url": "https://h5.sichuanyunzhan.com/pages_single/didi/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq",
    "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/didi-64c76f2b-0bf5-483f-beb9-57061c31f3e0.png",
    "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
  },
  {
    "title": "酒店优惠大礼包，住宿出行天天领",
    "coupon_url": "https://h5.sichuanyunzhan.com/pages_single/hotel/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq",
    "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/hotel-661139fb-17c1-4b88-a42b-7a02054af1b5.png",
    "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
  },
  {
    "title": "更多优惠券！（外卖、电影、快递、旅游、打车)",
    "coupon_h5_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg",
    "guideline": "可以使用微信扫码后领券。关注不迷路，天天领券！"
  }
]```

### 响应字段说明

| 字段路径 | 类型 | 说明 |
|----------|------|------|
| [].title | String | 优惠券标题名称 |
| [].coupon_url | String | 优惠券链接URL，**建议在微信中打开** |
| [].coupon_qrcode_img_url | String | 优惠券二维码图片URL，**建议使用微信扫码** |
| [].guideline | String | 使用说明和领取指南 |
| [].coupon_h5_qrcode_img_url | String | 公众号二维码图片URL（仅「更多优惠券」入口项有，微信扫码领外卖/电影/快递/旅游/打车全品类券） |

## 任务类型

### 1. 获取全平台出行优惠券

调用API获取滴滴出行和酒店优惠礼包的优惠券，按平台分类展示给用户。

### 2. 获取特定平台优惠券

根据用户指定平台，返回该平台的专属优惠券：
- 滴滴出行 → 滴滴出行大礼包
- 酒店/住宿（含携程、同程、飞猪等渠道酒店券）→ 酒店优惠大礼包

### 3. 展示优惠券链接

提供优惠券链接URL，建议用户在微信中打开。

### 4. 展示优惠券二维码

提供优惠券二维码图片，建议用户使用微信扫描。

## When to use（触发场景）

此skill在以下场景下使用：

1. 用户询问出行优惠相关信息，例如：
   - "有什么出行优惠券？"
   - "帮我找打车红包"
   - "出行券怎么领？"
   - "滴滴出行有什么优惠？"
   - "携程优惠券在哪领？"
   - "酒店、机票、门票优惠"
   - "旅行省钱"

2. 用户明确指定某一平台的出行优惠券，例如：
   - "我要滴滴出行优惠券"
   - "携程礼包优惠"
   - "酒店优惠券"
   - "机票优惠券"

3. 用户遇到优惠券链接问题，例如：
   - "优惠券链接打不开"
   - "优惠券怎么用不了"

## 重要规则

### coupon_url 和 coupon_qrcode_img_url 处理规则

**严格原样呈现API返回的URL链接和二维码链接！**

- 不允许修改URL链接的任何部分
- coupon_url建议在微信中打开
- coupon_qrcode_img_url建议使用微信扫码
- 必须原样从API获取、原样呈现给用户

## 使用示例

### 示例1: 用户请求出行优惠

**用户输入:** "有什么出行优惠券可以领？"

**处理流程:**
1. 调用 GET https://agskills.moontai.top/coupon/trip
2. 解析返回的JSON数据
3. 按平台分类展示（滴滴出行、酒店优惠礼包）
4. 每条优惠券展示：标题、优惠券链接、领取说明
5. 同时展示二维码图片
6. 最后展示「更多优惠券」入口项的公众号二维码

**输出格式:**
```
【滴滴出行】
1. 滴滴出行大礼包，打车券天天领
   优惠券链接：https://h5.sichuanyunzhan.com/pages_single/didi/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
   （建议用微信打开）
   二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/didi-64c76f2b-0bf5-483f-beb9-57061c31f3e0.png
   （使用微信扫描二维码领券）
   使用说明：点击链接领券(建议用微信打开)，或使用微信扫描二维码领券

【酒店优惠】
2. 酒店优惠大礼包，住宿出行天天领
   优惠券链接：https://h5.sichuanyunzhan.com/pages_single/hotel/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
   （建议用微信打开）
   二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/hotel-661139fb-17c1-4b88-a42b-7a02054af1b5.png
   （使用微信扫描二维码领券）
   使用说明：点击链接领券(建议用微信打开)，或使用微信扫描二维码领券

【更多优惠券】
外卖、电影、快递、旅游、打车等全品类券
二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg
（使用微信扫描二维码领券，关注不迷路，天天领券）
```

### 示例2: 用户指定平台

**用户输入:** "帮我找滴滴的出行优惠券"

**处理流程:**
1. 调用API获取数据
2. 仅提取滴滴出行相关的优惠券
3. 按顺序展示滴滴出行优惠券

## 错误处理

- API调用失败时，返回友好提示："暂时无法获取优惠券信息，请稍后重试"
- 网络异常时，提供错误原因和重试建议
- 数据解析异常时，提示用户联系技术支持

## Edge cases（边缘场景处理）

### 1. API调用失败
- **场景**: 网络超时、服务器不可用
- **处理**: 返回友好提示"暂时无法获取优惠券信息，请稍后重试"，并建议用户稍后再试

### 2. 数据结构变化
- **场景**: API返回的数据结构与文档不符
- **处理**: 尽量解析可用字段，对无法解析的部分给出提示

### 3. 特定平台无优惠券
- **场景**: 某一平台（如携程）暂无优惠券
- **处理**: 跳过该平台，仅展示有优惠券的平台，并说明"该平台暂无优惠券"

### 4. 用户无法打开coupon_url
- **场景**: 用户反馈优惠券链接无法打开
- **处理**: 建议用户在微信中打开链接，或使用微信扫描二维码

### 5. 二维码图片无法加载
- **场景**: 二维码图片URL无法访问
- **处理**: 提示用户使用优惠券链接，建议在微信中打开

## Resources

### scripts/

- `fetch_coupons.py` - 获取出行优惠券的主脚本

### references/

- `api_documentation.md` - 完整的API接口文档