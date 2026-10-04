---
name: china-price-compare
description: 实时对比淘宝/天猫、京东、拼多多、抖音、快手等主流电商平台的商品价格与优惠券，为用户找到全网最优购买方案。
homepage: https://github.com/aahl/skills/blob/main/skills/maishou/SKILL.md
metadata:
  manai:
    emoji: 🛍️
    requires:
      bins:
      - uv
    install:
    - id: uv-brew
      kind: brew
      formula: uv
      bins:
      - uv
      label: Install uv (brew)
    - id: uv-pip
      kind: pip
      formula: uv
      bins:
      - uv
      label: Install uv (pip)
    - id: pip-aiohttp
      kind: pip
      formula: aiohttp
      label: Install aiohttp (pip)
    - id: pip-argparse
      kind: pip
      formula: argparse
      label: Install argparse (pip)
    - id: pip-PyYAML
      kind: pip
      formula: PyYAML
      label: Install PyYAML (pip)
title: 国内全网比价
example: 在淘宝上搜索“手机壳”的最低售价，并给出商品的详情和购买链接。
version: 1.0.0
---
# 买手技能
全网比价，获取中国在线购物平台商品价格、优惠券

```yaml
# 参数解释
source:
  0: 全部
  1: 淘宝/天猫
  2: 京东
  3: 拼多多
  4: 苏宁
  5: 唯品会
  6: 考拉
  7: 抖音
  8: 快手
  10: 1688
```

## 搜索商品
```shell
uv run scripts/main.py search --source=0 --keyword='{keyword}'
uv run scripts/main.py search --source=0 --keyword='{keyword}' --page=2
```

## 商品详情及购买链接
```shell
uv run scripts/main.py detail --source={source} --id={goodsId}
```

## 关于脚本
本技能提供的脚本不会读写本地文件，可放心使用。 脚本仅作为客户端请求三方网站`maishou88.com`的商品和价格数据。