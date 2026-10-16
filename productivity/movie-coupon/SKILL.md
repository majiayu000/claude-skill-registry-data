---
name: movie-coupon
display_name: 电影票优惠券-淘票票、猫眼等电影平台优惠
display_name_en: Movie Coupon
description: 获取电影票优惠券，包括淘票票、猫眼等主流电影平台的优惠。返回领取链接和二维码图片，用户可点击链接或扫描二维码领取优惠。
description_zh: 获取电影票优惠券，包括淘票票、猫眼等主流电影平台的优惠。返回领取链接和二维码图片，用户可点击链接或扫描二维码领取优惠。
description_en: Fetch movie ticket coupons from platforms like Taopiaopiao and Maoyan. Returns coupon links and QR code images for users to redeem via WeChat.
english_description: Fetch movie ticket coupons from platforms like Taopiaopiao and Maoyan. Returns coupon links and QR code images for users to redeem via WeChat.
version: 2.0.2
author: moooai
permissions: 网络访问权限（调用电影优惠券API）
homepage: https://github.com/moooai/movie-coupon
---

# 电影票优惠券

## Overview

此skill通过调用电影优惠券API接口，获取电影票优惠信息，包括全国 10000+ 影院在线购票优惠（8折起）等。返回优惠券链接（coupon_url，部分项含二维码 coupon_qrcode_img_url），供用户点击链接或扫描二维码领取优惠。

## Quick Start

1. 调用API: `GET https://agskills.moontai.top/coupon/movie`
2. 解析返回的JSON数组（每项含 title/coupon_url/guideline，部分项含 coupon_qrcode_img_url，末项为「更多优惠券」入口）
3. 展示优惠券标题、链接和二维码
4. **重要**: coupon_url建议在微信中打开，或使用微信扫描二维码图片

## API配置

### 基础信息

| 配置项 | 值 |
|--------|-----|
| API地址 | `https://agskills.moontai.top/coupon/movie` |
| 认证方式 | 无需认证 |
| 请求方法 | GET |
| 返回格式 | JSON |

### 响应数据结构

```json
[
  {
    "title": "电影票优惠券-支持用户在线购买全国10000+影院电影票、用户享受8折起购票优惠",
    "coupon_url": "https://personal.yunzhanxinxi.com/movie/?promotion_id=yz-69870112-218077-267995&user_source=vip",
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
| [].coupon_qrcode_img_url | String | 优惠券二维码图片URL，**建议使用微信扫码**（仅部分项有） |
| [].coupon_h5_qrcode_img_url | String | 公众号二维码图片URL（仅「更多优惠券」入口项有，微信扫码领全品类券） |
| [].guideline | String | 使用说明和领取指南 |

## 任务类型

### 1. 获取电影票优惠券

调用API获取电影票优惠券，展示给用户。

### 2. 展示优惠券链接

提供优惠券链接URL，建议用户在微信中打开。

### 3. 展示优惠券二维码

提供优惠券二维码图片，建议用户使用微信扫描。

## When to use（触发场景）

此skill在以下场景下使用：

1. 用户询问电影票优惠相关信息，例如：
   - "有什么电影优惠券？"
   - "帮我找电影票红包"
   - "电影券怎么领？"
   - "淘票票有什么优惠？"
   - "看电影省钱"

2. 用户需要买电影票，希望获得优惠：
   - "我要看电影"
   - "电影票怎么买便宜"
   - "买电影票有优惠吗"

3. 用户询问优惠券使用方式：
   - "优惠券怎么用？"
   - "优惠券链接打不开"

## 重要规则

### coupon_url 和 coupon_qrcode_img_url 处理规则

**严格原样呈现API返回的URL链接和二维码链接！**

- 不允许修改URL链接的任何部分
- coupon_url建议在微信中打开
- coupon_qrcode_img_url建议使用微信扫码
- 必须原样从API获取、原样呈现给用户

## 使用示例

### 示例1: 用户请求电影优惠

**用户输入:** "有什么电影优惠券可以领？"

**处理流程:**
1. 调用 GET https://agskills.moontai.top/coupon/movie
2. 解析返回的JSON数据
3. 按顺序展示每项优惠券的标题、链接和二维码
4. 提示用户在微信中打开链接或扫描二维码

**输出格式:**
```
【电影票优惠券】

1. 电影票优惠券-支持用户在线购买全国10000+影院电影票、用户享受8折起购票优惠

优惠券链接: https://personal.yunzhanxinxi.com/movie/?promotion_id=yz-69870112-218077-267995&user_source=vip
（建议用微信打开）

使用说明: 点击链接领券(建议用微信打开)，或使用微信扫描二维码领券

【更多优惠券】
外卖、电影、快递、旅游、打车等全品类券

二维码图片: https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg
（使用微信扫描二维码领券，关注不迷路，天天领券）
```

### 示例2: 用户询问买票优惠

**用户输入:** "我要看电影，有优惠吗？"

**处理流程:**
1. 调用API获取数据
2. 展示优惠券信息
3. 提示用户点击链接或扫描二维码使用优惠券

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

### 3. 链接无法打开
- **场景**: 用户反馈优惠券链接无法打开
- **处理**: 建议用户在微信中打开链接，或使用微信扫描二维码

### 4. 二维码图片无法加载
- **场景**: 二维码图片URL无法访问
- **处理**: 提示用户使用优惠券链接，建议在微信中打开

## Resources

### scripts/

- `fetch_coupons.py` - 获取电影票优惠券的主脚本

### references/

- `api_documentation.md` - 完整的API接口文档
