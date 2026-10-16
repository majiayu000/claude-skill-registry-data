# parcel-coupon 快递优惠券

获取顺丰、中通、圆通、韵达、申通、菜鸟等快递优惠券及同城配送优惠，返回领取链接和二维码，微信扫码或点击链接即可领取。

## 安装

```bash
npx skills add moooai/parcel-coupon
```

[![skills.sh installs](https://skills.sh/badge/moooai/parcel-coupon)](https://skills.sh)

## 使用

对 AI 助手说："有快递优惠券吗"、"寄顺丰有优惠吗"。

或直接运行脚本：

```bash
python scripts/fetch_coupons.py
python scripts/fetch_coupons.py --json
```

## 重要说明

- API 请求自动附加 `ch` / `u` 归因参数（匿名安装标识，用于渠道统计）

## 许可

MIT
