# obtain-coupons-all-in-one 全平台优惠券助手

一站式获取外卖（美团、饿了么、京东）、快递（顺丰、中通、圆通等）、出行（滴滴、携程）、电影票（淘票票、猫眼）全平台优惠券，一键领取。

## 安装

```bash
npx skills add moooai/obtain-coupons-all-in-one
```

[![skills.sh installs](https://skills.sh/badge/moooai/obtain-coupons-all-in-one)](https://skills.sh)

## 使用

对 AI 助手说："帮我领今天所有的优惠券"、"外卖和快递的优惠一起看看"。

或直接运行脚本：

```bash
python scripts/fetch_coupons.py                      # 全品类
python scripts/fetch_coupons.py -c takeout           # 仅外卖
python scripts/fetch_coupons.py --json               # 原始 JSON
```

## 重要说明

- 外卖口令 `coupon_code` 必须原样呈现，禁止修改任何字符
- API 请求自动附加 `ch` / `u` 归因参数（匿名安装标识，用于渠道统计）

## 许可

MIT
