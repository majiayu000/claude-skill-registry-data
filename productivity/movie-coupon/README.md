# movie-coupon 电影票优惠券

获取淘票票、猫眼等主流电影平台的优惠券，返回领取链接和二维码，微信扫码或点击链接即可领取。

## 安装

```bash
npx skills add moooai/movie-coupon
```

[![skills.sh installs](https://skills.sh/badge/moooai/movie-coupon)](https://skills.sh)

## 使用

对 AI 助手说："有电影票优惠券吗"、"淘票票/猫眼怎么领券"。

或直接运行脚本：

```bash
python scripts/fetch_coupons.py
python scripts/fetch_coupons.py --json
```

## 领取页面示例

扫码或点击领取链接后进入的购票页面：

**淘票票**（正在热映/即将上映，选座购票）：

![淘票票购票页](assets/movie-sample1.png)

## 重要说明

- API 请求自动附加 `ch` / `u` 归因参数（匿名安装标识，用于渠道统计）

## 许可

MIT
