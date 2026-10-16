---
name: takeout-coupon
display_name: Takeout Coupon 外卖优惠券-美团饿了么京东
display_name_en: Takeout Coupon
description: 调用外卖优惠券API，一键获取美团、饿了么/淘宝闪购、京东外卖红包与隐藏优惠券口令，附带聚合领券页面。返回优惠券代码和领取说明，用户复制口令到对应APP即可领券，天天领外卖红包。
description_zh: 调用外卖优惠券API，一键获取美团、饿了么/淘宝闪购、京东外卖红包与隐藏优惠券口令，附带聚合领券页面。返回优惠券代码和领取说明，用户复制口令到对应APP即可领券，天天领外卖红包。
description_en: Call takeout coupon API to fetch hidden coupon lists, red packets and aggregated redemption pages for platforms (Meituan, Taobao Flash/Ele.me, JD.com). Returns coupon codes and redemption instructions for users to copy and redeem in corresponding apps.
english_description: Call takeout coupon API to fetch hidden coupon lists, red packets and aggregated redemption pages for platforms (Meituan, Taobao Flash/Ele.me, JD.com). Returns coupon codes and redemption instructions for users to copy and redeem in corresponding apps.
version: 2.0.2
author: moooai
permissions: 网络访问权限（调用外卖优惠券API）
homepage: https://github.com/moooai/takeout-coupon
---

# 外卖优惠券

## Overview

此skill通过调用外卖优惠券API接口，获取美团、淘宝闪购/饿了么、京东三大外卖平台的隐藏优惠券，以及各平台扫码/H5领券页直达入口。返回优惠券代码（coupon_code）和领取指南，供用户复制到对应APP领取优惠。

## Quick Start

1. 调用API: `GET https://agskills.moontai.top/coupon/takeout`
2. 解析返回的JSON数据，包含4个主要部分
3. 按平台分类展示优惠券信息
4. **重要**: coupon_code字段必须原样呈现给用户，不可修改任何内容

## API配置

### 基础信息

| 配置项 | 值 |
|--------|-----|
| API地址 | `https://agskills.moontai.top/coupon/takeout` |
| 认证方式 | 无需认证 |
| 请求方法 | GET |
| 归因参数 | `ch=<渠道>&u=<安装uuid>`（fetch_coupons.py 自动附加，用于匿名安装统计与订单归因） |
| 返回格式 | JSON |

### 响应数据结构

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

### 响应字段说明

| 字段路径 | 类型 | 说明 |
|----------|------|------|
| 美团隐藏外卖券列表 | Array | 美团外卖平台优惠券数组 |
| 饿了么/淘宝闪购隐藏外卖券列表 | Array | 淘宝闪购/饿了么优惠券数组 |
| 京东隐藏外卖券列表 | Array | 京东外卖优惠券数组 |
| 扫码领取/H5网页跳转领取 | Array | 各平台领券页直达入口数组（H5 链接 + 二维码图片） |
| 查找更多优惠券 | Object | 更多优惠券入口（外卖、电影、快递、旅游、打车，公众号二维码） |
| [].title | String | 优惠券标题名称 |
| [].coupon_code | String | **优惠券代码，必须原样呈现，不可修改任何字符** |
| [].guideline | String | 领取说明 |
| [].coupon_url | String | H5 领取页链接（仅「扫码领取/H5网页跳转领取」数组内的项） |
| [].coupon_qrcode_img_url | String | 领取页二维码图片URL（仅「扫码领取/H5网页跳转领取」数组内的项） |
| 查找更多优惠券.coupon_h5_qrcode_img_url | String | 公众号二维码图片URL，微信扫码领更多券 |
| 查找更多优惠券.guideline | String | 使用说明 |

## 任务类型

### 1. 获取全平台外卖优惠券

调用API获取所有平台的外卖优惠券，按平台分类展示给用户。

### 2. 获取特定平台优惠券

根据用户指定平台，返回该平台的专属优惠券：
- 美团外卖 → 美团隐藏外卖券列表
- 饿了么/淘宝闪购 → 饿了么/淘宝闪购隐藏外卖券列表
- 京东外卖 → 京东隐藏外卖券列表

### 3. 展示「查找更多优惠券」入口

返回公众号二维码图片（qrcode_for_gh.jpg），供用户微信扫码关注后天天领更多类型的券。

### 4. 提供扫码/H5 直达领取页

返回「扫码领取/H5网页跳转领取」数组中各平台的领取页链接（coupon_url）和二维码图片（coupon_qrcode_img_url），供用户无法复制口令时直接扫码或点击领取。

### 5. 搜索口令型优惠券

接口可能返回搜索口令型优惠券（纯数字口令或短语口令），guideline 会说明在对应 APP 的搜索框中输入口令领取。此类口令同样必须原样呈现。

### 6. 主推优惠券优先

在展示时，主推标记的优惠券（如带🔥🔥或标注"主推"）应优先展示。

## When to use（触发场景）

此skill在以下场景下使用：

1. 用户询问外卖优惠相关信息，例如：
   - "有什么外卖优惠券？"
   - "帮我找外卖红包"
   - "外卖券怎么领？"
   - "美团外卖有什么优惠？"
   - "饿了么优惠券在哪领？"
   - "京东外卖红包"
   - "外卖平台哪个优惠最大？"

2. 用户明确指定某一平台的外卖优惠券，例如：
   - "我要美团外卖优惠券"
   - "淘宝闪购红包"
   - "帮我找京东外卖优惠"

3. 用户遇到优惠券复制问题，例如：
   - "优惠码复制不了"
   - "优惠券怎么用不了"

## 重要规则

### coupon_code 处理规则

**严格禁止修改coupon_code字段的任何内容！**

- 不允许添加、删除、修改任何字符
- 不允许格式化、美化或重新排列
- 不允许翻译或解释代码含义
- 必须原样从API获取、原样呈现给用户

coupon_code可能包含特殊字符（如%、¥、✔、！、£等），这些是平台特定的格式，必须保持原样。

## 使用示例

### 示例1: 用户请求外卖优惠

**用户输入:** "有什么外卖优惠券可以领？"

**处理流程:**
1. 调用 GET https://agskills.moontai.top/coupon/takeout
2. 解析返回的JSON数据
3. 按平台分类展示（美团、淘宝闪购、京东）
4. 每条优惠券展示：标题、优惠券代码、领取说明
5. 同时展示「扫码领取/H5网页跳转领取」的领券页链接与二维码，以及「查找更多优惠券」的公众号二维码图片

**输出格式:**
```
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


【扫码领取/H5直达】
- 美团优惠券领取页
  链接：https://h5.sichuanyunzhan.com/pages_single/meiTuan/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
  二维码：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/meituan-614d8c70-26c5-43bc-9e91-4468651709e8.png
  说明：点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）
- 饿了么/淘宝闪购优惠券领取页
  链接：https://h5.sichuanyunzhan.com/pages_single/hungry/index?platform=singlePage&pid=e467cdcafe2b1791cdfc&accountsId=nEjX0zy4Zmyq
  二维码：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/taobao-9dd25c45-2e2c-451d-af71-a502f815de16.png
  说明：点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）

【查找更多优惠券】
二维码图片：https://moontai-static.oss-cn-shenzhen.aliyuncs.com/qrcode_for_gh.jpg
领取说明：可以使用微信扫码后领券。关注不迷路，天天领券！
```

### 示例2: 用户指定平台

**用户输入:** "帮我找美团的外卖优惠券"

**处理流程:**
1. 调用API获取数据
2. 仅提取"美团隐藏外卖券列表"部分
3. 按顺序展示美团优惠券

### 示例3: 用户无法复制优惠码

**用户输入:** "优惠券代码复制不了怎么办"

**处理流程:**
1. 展示「扫码领取/H5网页跳转领取」中对应平台的领取页链接与二维码图片
2. 提示用户使用微信扫码或点击链接直接领取

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
- **场景**: 某一平台（如京东）暂无优惠券
- **处理**: 跳过该平台，仅展示有优惠券的平台，并说明"该平台暂无优惠券"

### 4. 用户无法复制coupon_code
- **场景**: 用户反馈优惠券代码复制失败
- **处理**: 提供「查找更多优惠券」的公众号二维码图片URL，提示用户使用微信扫码领取

### 5. coupon_code包含特殊字符
- **场景**: coupon_code可能包含%、¥、✔、！等特殊字符
- **处理**: 严格原样呈现，不进行任何转义或格式化处理

## Resources

### scripts/

- `fetch_coupons.py` - 获取外卖优惠券的主脚本

### references/

- `api_documentation.md` - 完整的API接口文档
