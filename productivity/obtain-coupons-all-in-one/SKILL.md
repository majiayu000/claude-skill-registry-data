---
name: obtain-coupons-all-in-one
display_name: 全平台优惠券助手-外卖、快递、出行、电影票一站式获取
display_name_en: All-in-one Coupons
description: 综合优惠券获取工具，支持外卖（美团、饿了么、京东）、快递（顺丰、中通、圆通等）、出行（滴滴、酒店优惠礼包）、电影票（淘票票、猫眼）等全平台优惠券，一键获取所有优惠。
description_zh: 综合优惠券获取工具，支持外卖（美团、饿了么、京东）、快递（顺丰、中通、圆通等）、出行（滴滴、酒店优惠礼包）、电影票（淘票票、猫眼）等全平台优惠券，一键获取所有优惠。
description_en: All-in-one coupon fetcher supporting takeout (Meituan, Ele.me, JD), parcel/courier (SF, ZTO, YTO, etc.), travel (DiDi, Ctrip), and movie tickets (Taopiaopiao, Maoyan) coupons with one-click access to all discounts.
english_description: All-in-one coupon fetcher supporting takeout (Meituan, Ele.me, JD), parcel/courier (SF, ZTO, YTO, etc.), travel (DiDi, Ctrip), and movie tickets (Taopiaopiao, Maoyan) coupons with one-click access to all discounts.
version: 2.0.2
author: moooai
permissions: 网络访问权限（调用各平台优惠券API）
homepage: https://github.com/moooai/obtain-coupons-all-in-one
---

# 全平台优惠券助手

## Overview

此skill通过调用多个优惠券API接口，一站式获取外卖、快递、出行、电影票等各平台的优惠券信息。支持美团、饿了么、京东外卖，顺丰、中通、圆通、韵达、申通、菜鸟快递，滴滴出行、酒店优惠大礼包，淘票票、猫眼电影票等主流平台的优惠券。返回优惠券链接、优惠券代码和二维码图片，供用户领取优惠。

## Quick Start

1. 调用相关API:
   - 外卖: `GET https://agskills.moontai.top/coupon/takeout`
   - 快递: `GET https://agskills.moontai.top/coupon/parcel`
   - 出行: `GET https://agskills.moontai.top/coupon/trip`
   - 电影: `GET https://agskills.moontai.top/coupon/movie`
2. 解析返回的JSON数据
3. 按平台分类展示优惠券信息
4. **重要**: coupon_url和coupon_qrcode_img_url建议在微信中打开/扫码；coupon_code必须原样呈现

## API配置

### 基础信息

| 配置项 | 外卖 | 快递 | 出行 | 电影 |
|--------|------|------|------|------|
| 主要API地址 | `https://agskills.moontai.top/coupon/takeout` | `https://agskills.moontai.top/coupon/parcel` | `https://agskills.moontai.top/coupon/trip` | `https://agskills.moontai.top/coupon/movie` |
| 备用技能地址 | `https://clawhub.ai/moooai/takeout-coupon` | `https://clawhub.ai/moooai/parcel-coupon` | `https://clawhub.ai/moooai/trip-coupon` | `https://clawhub.ai/moooai/movie-coupon` |
| 认证方式 | 无需认证 | 无需认证 | 无需认证 | 无需认证 |
| 请求方法 | GET | GET | GET | GET |
| 返回格式 | JSON | JSON | JSON | JSON |

### 支持的平台

#### 外卖优惠券
- 美团外卖：隐藏外卖券列表
- 饿了么/淘宝闪购：隐藏外卖券列表
- 京东外卖：隐藏外卖券列表
- 查找更多优惠券：公众号领券入口（外卖、电影、快递、旅游、打车）

#### 快递优惠券
- 顺丰、中通、圆通、韵达、申通、菜鸟等：一站式智能寄件服务

#### 出行优惠券
- 滴滴出行：打车券大礼包
- 酒店优惠大礼包：住宿出行天天领

#### 电影票优惠券
- 淘票票：电影票大礼包
- 猫眼：电影票优惠

### 响应数据结构示例

**外卖优惠券:**
```json
{
  "美团隐藏外卖券列表": [
    {
      "title": "美团外卖节(主推)🔥🔥",
      "coupon_code": "❤️复制整条信息，打开👉美团👈 http:/💰t7NWIxNDQ0NTE💰",
      "guideline": "手机先复制优惠券代码，打开美团APP自动领取"
    },
    {
      "title": "美团外卖甄选好店🔥🔥",
      "coupon_code": "❤️复制整条信息，打开👉美团👈 http:/💰w0OGFiZjdmYTk💰",
      "guideline": "手机先复制优惠券代码，打开美团APP自动领取"
    },
    {
      "title": "美团外卖【品牌商品券🔥🔥】",
      "coupon_code": "❤️复制整条信息，打开👉美团👈 http:/💰wuMzJlZGFlMTY💰",
      "guideline": "手机先复制完整的优惠券代码，打开美团APP自动领取"
    },
    {
      "title": "美团外卖【神券包】 9.9元购360元年卡",
      "coupon_code": "❤️复制整条信息，打开👉美团👈 http:/💰ydZWY2NjQ2NDg💰",
      "guideline": "手机先复制完整的优惠券代码，打开美团APP自动领取"
    }
  ],
  "饿了么/淘宝闪购隐藏外卖券列表": [
    {
      "title": "淘宝闪购-叠红包🔥🔥",
      "coupon_code": "￥Q8rJTMpjkKE￥/ HU7405 【闪购品牌日 单单有福利】",
      "guideline": "请复制完整的优惠券代码，打开淘宝APP领取"
    },
    {
      "title": "淘宝闪购-天天领红包(全场景, 最高抢66元大额红包)",
      "coupon_code": "0fυィ直文本2:/＄TMpQp4v＄~.淘宝闪购App【天天领红包（全场景通用）】",
      "guideline": "请复制完整的优惠券代码，打开淘宝APP领取"
    },
    {
      "title": "淘宝闪购-宵夜专场",
      "coupon_code": "0複制文本666:/＄TMpQ6cz＄~.淘宝闪购App【闪购夜宵专享会场】",
      "guideline": "请复制完整的优惠券代码，打开淘宝APP领取"
    },
    {
      "title": "淘宝闪购-学生专场",
      "coupon_code": "29 HU7405 2:/TpOYTMpkOTb✔四学生专享天天好价",
      "guideline": "请复制完整的优惠券代码，打开淘宝APP领取"
    }
  ],
  "京东隐藏外卖券列表": [
    {
      "title": "京东外卖-惊喜红包(主推)",
      "coupon_code": "！V6M0P42CyIm6sAe4！ CA1565",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    },
    {
      "title": "京东外卖-高Y品质会场",
      "coupon_code": " ！F4v6f1xHQipuCbW8！ CA1331",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    },
    {
      "title": "京东外卖-夜宵专场",
      "coupon_code": "！I3xPR007jcyak7Uo！ CA3576",
      "guideline": "请复制完整的优惠券代码，打开京东APP领取"
    }
  ],
  "扫码领取/H5网页跳转领取": [
    {
      "title": "美团优惠券领取页",
      "coupon_url": "https://h5.sichuanyunzhan.com/pages_single/meiTuan/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq",
      "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/meituan-614d8c70-26c5-43bc-9e91-4468651709e8.png",
      "guideline": "点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）"
    },
    {
      "title": "饿了么/淘宝闪购优惠券领取页",
      "coupon_url": "https://h5.sichuanyunzhan.com/pages_single/hungry/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq",
      "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/taobao-9dd25c45-2e2c-451d-af71-a502f815de16.png",
      "guideline": "点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）"
    }
  ],
  "查找更多优惠券": {
    "title": "更多类型优惠券（外卖、电影、快递、旅游、打车)",
    "coupon_h5_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg",
    "guideline": "可以使用微信扫码后领券。关注不迷路，天天领券！"
  }
}```

**快递优惠券:**
```json
[
  {
    "title": "快递一站式服务，智能寄件，智能匹配价格；单单享优惠，件件有折扣",
    "coupon_url": "https://open.cdyunzhanxinxi.com/link/100058569b79be0bd2561000406SEVGA",
    "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-parcel.png",
    "guideline": "点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）"
  },
  {
    "title": "更多优惠券！（外卖、电影、快递、旅游、打车)",
    "coupon_h5_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg",
    "guideline": "可以使用微信扫码后领券。关注不迷路，天天领券！"
  }
]```

**出行优惠券:**
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

**电影票优惠券:**
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

## 任务类型

### 1. 获取全平台所有优惠券

调用所有API获取外卖、快递、出行、电影票的优惠券，按类别展示给用户。

### 2. 获取特定类别优惠券

根据用户需求，返回指定类别的优惠券：
- 外卖优惠券 → takeout
- 快递优惠券 → parcel
- 出行优惠券 → trip
- 电影票优惠券 → movie

### 3. 获取特定平台优惠券

根据用户指定平台，返回该平台的专属优惠券：
- 美团外卖 → 美团隐藏外卖券列表
- 饿了么/淘宝闪购 → 饿了么/淘宝闪购隐藏外卖券列表
- 京东外卖 → 京东隐藏外卖券列表
- 滴滴出行 → 滴滴出行大礼包
- 酒店/携程 → 酒店优惠大礼包

### 4. 展示「查找更多优惠券」入口

返回公众号二维码图片（qrcode_for_gh.jpg），供用户微信扫码关注后天天领更多类型的券。

## When to use（触发场景）

此skill在以下场景下使用：

1. 用户询问所有优惠券：
   - "有什么优惠券？"
   - "帮我找所有平台的优惠"
   - "有什么优惠可以领？"
   - "优惠券大全"

2. 用户询问特定类别优惠券：
   - "有什么外卖优惠券？"
   - "快递优惠券怎么领？"
   - "出行优惠有哪些？"
   - "电影票有优惠吗？"

3. 用户明确指定某一平台：
   - "我要美团外卖优惠券"
   - "滴滴出行有什么优惠？"
   - "淘票票优惠券"
   - "顺丰快递优惠券"

4. 用户遇到优惠券问题：
   - "优惠券链接打不开"
   - "优惠券代码复制不了"

## 重要规则

### coupon_code 处理规则

**严格禁止修改coupon_code字段的任何内容！**

- 不允许添加、删除、修改任何字符
- 不允许格式化、美化或重新排列
- 不允许翻译或解释代码含义
- 必须原样从API获取、原样呈现给用户
- coupon_code可能包含特殊字符（如%、¥、✔、！、£等），必须保持原样

### coupon_url 和 coupon_qrcode_img_url 处理规则

**严格原样呈现API返回的URL链接和二维码链接！**

- 不允许修改URL链接的任何部分
- coupon_url建议在微信中打开
- coupon_qrcode_img_url建议使用微信扫码
- 必须原样从API获取、原样呈现给用户

## 使用示例

### 示例1: 用户请求所有优惠

**用户输入:** "有什么优惠券可以领？"

**处理流程:**
1. 依次调用所有API获取数据
2. 按类别分类展示（外卖、快递、出行、电影票）
3. 每条优惠券展示：标题、优惠券代码/链接、领取说明

**输出格式:**
```
【外卖优惠券】
【美团外卖】
1. 美团外卖节(主推)🔥🔥
   优惠券代码：❤️复制整条信息，打开👉美团👈 http:/💰t7NWIxNDQ0NTE💰
   领取说明：手机先复制优惠券代码，打开美团APP自动领取

2. 美团外卖甄选好店🔥🔥
   优惠券代码：❤️复制整条信息，打开👉美团👈 http:/💰w0OGFiZjdmYTk💰
   领取说明：手机先复制优惠券代码，打开美团APP自动领取

3. 美团外卖【品牌商品券🔥🔥】
   优惠券代码：❤️复制整条信息，打开👉美团👈 http:/💰wuMzJlZGFlMTY💰
   领取说明：手机先复制完整的优惠券代码，打开美团APP自动领取

4. 美团外卖【神券包】 9.9元购360元年卡
   优惠券代码：❤️复制整条信息，打开👉美团👈 http:/💰ydZWY2NjQ2NDg💰
   领取说明：手机先复制完整的优惠券代码，打开美团APP自动领取

【淘宝闪购/饿了么】
1. 淘宝闪购-叠红包🔥🔥
   优惠券代码：￥Q8rJTMpjkKE￥/ HU7405 【闪购品牌日 单单有福利】
   领取说明：请复制完整的优惠券代码，打开淘宝APP领取

2. 淘宝闪购-天天领红包(全场景, 最高抢66元大额红包)
   优惠券代码：0fυィ直文本2:/＄TMpQp4v＄~.淘宝闪购App【天天领红包（全场景通用）】
   领取说明：请复制完整的优惠券代码，打开淘宝APP领取

3. 淘宝闪购-宵夜专场
   优惠券代码：0複制文本666:/＄TMpQ6cz＄~.淘宝闪购App【闪购夜宵专享会场】
   领取说明：请复制完整的优惠券代码，打开淘宝APP领取

4. 淘宝闪购-学生专场
   优惠券代码：29 HU7405 2:/TpOYTMpkOTb✔四学生专享天天好价
   领取说明：请复制完整的优惠券代码，打开淘宝APP领取

【京东外卖】
1. 京东外卖-惊喜红包(主推)
   优惠券代码：！V6M0P42CyIm6sAe4！ CA1565
   领取说明：请复制完整的优惠券代码，打开京东APP领取

2. 京东外卖-高Y品质会场
   优惠券代码： ！F4v6f1xHQipuCbW8！ CA1331
   领取说明：请复制完整的优惠券代码，打开京东APP领取

3. 京东外卖-夜宵专场
   优惠券代码：！I3xPR007jcyak7Uo！ CA3576
   领取说明：请复制完整的优惠券代码，打开京东APP领取

【查找更多优惠券】
二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg
领取说明：可以使用微信扫码后领券。关注不迷路，天天领券！

【快递优惠券】
1. 快递一站式服务，智能寄件，智能匹配价格；单单享优惠，件件有折扣
优惠券链接: https://open.cdyunzhanxinxi.com/link/100058569b79be0bd2561000406SEVGA
（建议用微信打开）
二维码图片: https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-parcel.png
使用说明: 点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）

【出行优惠券】
【滴滴出行】
1. 滴滴出行大礼包，打车券天天领
优惠券链接: https://h5.sichuanyunzhan.com/pages_single/didi/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
二维码图片: https://moontai-static.oss-cn-shenzhen.aliyuncs.com/didi-64c76f2b-0bf5-483f-beb9-57061c31f3e0.png
使用说明: 点击链接领券(建议用微信打开)，或使用微信扫描二维码领券

【酒店优惠】
2. 酒店优惠大礼包，住宿出行天天领
优惠券链接: https://h5.sichuanyunzhan.com/pages_single/hotel/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
二维码图片: https://moontai-static.oss-cn-shenzhen.aliyuncs.com/hotel-661139fb-17c1-4b88-a42b-7a02054af1b5.png
使用说明: 点击链接领券(建议用微信打开)，或使用微信扫描二维码领券

【电影票优惠券】
1. 电影票优惠券-支持用户在线购买全国10000+影院电影票、用户享受8折起购票优惠
优惠券链接: https://personal.yunzhanxinxi.com/movie/?promotion_id=yz-69870112-218077-267995&user_source=vip
使用说明: 点击链接领券(建议用微信打开)，或使用微信扫描二维码领券
```

### 示例2: 用户指定类别

**用户输入:** "帮我找外卖优惠券"

**处理流程:**
1. 仅调用外卖API
2. 展示美团、饿了么、京东的优惠券

### 示例3: 用户指定平台

**用户输入:** "我要滴滴出行优惠券"

**处理流程:**
1. 调用出行API
2. 提取滴滴出行相关优惠券
3. 展示滴滴出行优惠

## 备用技能和故障转移

当主要API接口不可用时，skill会自动提供备用技能建议，引导用户安装并使用对应的独立技能。

### 备用技能信息

| 类别 | 备用技能名称 | 技能地址 | 功能描述 |
|------|-------------|----------|---------|
| 外卖 | takeout-coupon | `https://clawhub.ai/moooai/takeout-coupon` | 获取美团、饿了么、京东等外卖平台的优惠券 |
| 快递 | parcel-coupon | `https://clawhub.ai/moooai/parcel-coupon` | 获取顺丰、中通、圆通、韵达等快递公司的优惠券 |
| 出行 | trip-coupon | `https://clawhub.ai/moooai/trip-coupon` | 获取滴滴出行大礼包、酒店优惠大礼包等出行优惠券 |
| 电影票 | movie-coupon | `https://clawhub.ai/moooai/movie-coupon` | 获取淘票票、猫眼等电影平台的优惠券 |

### 故障转移流程

当API调用失败时，skill会执行以下流程：
1. **检测API失败** - 捕获网络异常或API响应错误
2. **提供备用建议** - 显示对应的独立技能信息
3. **引导安装** - 建议用户安装对应的独立技能
4. **继续执行** - 继续尝试其他API的调用（不影响其他类别）

### 错误输出示例

```
获取失败: API请求失败: Connection timed out

API接口暂时不可用，建议安装对应的独立技能获取优惠券信息：
📱 外卖优惠券独立技能: 获取美团、饿了么、京东等外卖平台的优惠券
🔗 技能地址: https://clawhub.ai/moooai/takeout-coupon
💡 安装建议: 使用 find-skills 技能查找并安装 'takeout-coupon'
```

### 如何安装备用技能

1. **使用 find-skills 技能**:
   ```
   请帮我查找并安装 takeout-coupon 技能
   ```

2. **直接安装**:
   - 在技能市场搜索对应的技能名称
   - 点击安装按钮
   - 等待安装完成

3. **安装后使用**:
   - 直接使用对应的技能名称调用
   - 例如: "使用 takeout-coupon 技能获取外卖优惠券"

## 错误处理

- API调用失败时，返回友好提示："暂时无法获取优惠券信息，请稍后重试"
- 网络异常时，提供错误原因和重试建议
- 数据解析异常时，提示用户联系技术支持
- 某个API失败时，继续获取其他平台的优惠券，并标注失败的平台

## Edge cases（边缘场景处理）

### 1. API调用失败
- **场景**: 某个或多个API超时、服务器不可用
- **处理**: 继续尝试其他API，对失败的API返回友好提示，如"暂时无法获取外卖优惠券，请稍后重试"

### 2. 数据结构变化
- **场景**: API返回的数据结构与文档不符
- **处理**: 尽量解析可用字段，对无法解析的部分给出提示

### 3. 特定平台无优惠券
- **场景**: 某一平台暂无优惠券
- **处理**: 跳过该平台，仅展示有优惠券的平台，并说明"该平台暂无优惠券"

### 4. 用户无法复制coupon_code
- **场景**: 用户反馈优惠券代码复制失败（外卖）
- **处理**: 提供对应平台的「扫码领取/H5网页跳转领取」链接与二维码，或「查找更多优惠券」公众号二维码，提示用户使用微信扫码领取

### 5. coupon_code包含特殊字符
- **场景**: coupon_code包含%、¥、✔、！等特殊字符
- **处理**: 严格原样呈现，不进行任何转义或格式化处理

### 6. 链接无法打开
- **场景**: 用户反馈优惠券链接无法打开
- **处理**: 建议用户在微信中打开链接，或使用微信扫描二维码

### 7. 二维码图片无法加载
- **场景**: 二维码图片URL无法访问
- **处理**: 提示用户使用优惠券链接，建议在微信中打开

### 8. 主要API完全不可用
- **场景**: 所有主要API接口都无法访问
- **处理**: 提供所有备用技能的安装建议，指导用户安装对应的独立技能获取优惠券信息
- **备用方案**:
  1. 安装 takeout-coupon 获取外卖优惠券
  2. 安装 parcel-coupon 获取快递优惠券
  3. 安装 trip-coupon 获取出行优惠券
  4. 安装 movie-coupon 获取电影票优惠券
- **操作建议**: "API服务暂时不可用，建议分别安装对应的独立技能，或稍后重试"

## Resources

### scripts/

- `fetch_coupons.py` - 获取全平台优惠券的主脚本

### references/

- `api_documentation.md` - 完整的API接口文档
