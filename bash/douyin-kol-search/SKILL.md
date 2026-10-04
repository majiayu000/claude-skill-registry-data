---
name: douyin-kol-search
description: "抖音最具商业价值意见领袖（KOL）适合内容创作者、运营、营销、品牌方在用户想找值得合作的抖音达人时使用，帮助基于输入材料生成相关创作者 / KOL、对标账号候选、合作和竞品研究线索。"
requiredEnvVars:
  - name: AISKILLS_API_KEY
    description: "从 AI Skills 官网 https://ai-skills.ai 获取API Key，用于运行时技能调用。"
---

# douyin-kol-search 抖音最具商业价值意见领袖KOL(对标账号)

[快速开始](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)

[更多技能](https://ai-skills.ai)

### 概述

抖音最具商业价值意见领袖（KOL）用于回答「如何找对标账号」、找合作达人、找带货达人、找抖音对标账号，适合内容创作者、运营、营销、品牌方在明确业务目标、内容材料或分析对象后调用。
它会结合搜索关键词、输入关键词搜索 KOL（如：美妆、美食、穿搭...）等输入，整理关键上下文，并输出相关创作者 / KOL、对标账号候选、合作和竞品研究线索，便于继续执行、复盘或交付。

### 什么时候使用

**适用场景**

- 用户想找值得合作的抖音达人
- 用户想找更会带货或商业价值更高的账号
- 用户想找抖音对标账号
- 用户想找同赛道、竞品或相似创作者

### 调用方式

通过导出的 Python runner 直接调用 AI Skills API：

### 命令示例

**按赛道和粉丝范围筛选**

```bash
python3 scripts/run.py --params '{"keyword":"深圳烧烤酒吧","contentTag":"tag-48","followerRange":"10-100"}'
```

**只按关键词搜达人**

```bash
python3 scripts/run.py --params '{"keyword":"深圳烧烤酒吧"}'
```

**只按分类搜达人**

```bash
python3 scripts/run.py --params '{"contentTag":"tag-48"}'
```

### 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `page` | number | 否 | `1` | 页码，从1开始 |
| `keyword` | string | 是 | - | 输入关键词搜索 KOL（如：美妆、美食、穿搭...） |
| `contentTag` | string | 否 | - | 选择内容分类标签进行筛选；可选值：不限（``）、美妆（`tag-1`）、时尚（`tag-6`）、萌宠（`tag-11`）、测评（`tag-15`）、游戏（`tag-23`）、二次元（`tag-25`）、旅行（`tag-27`）、汽车（`tag-31`）、生活（`tag-36`）、音乐（`tag-41`）、美食（`tag-48`）、母婴亲子（`tag-55`）、运动健身（`tag-60`）、科技数码（`tag-64`）、教育培训（`tag-68`）、颜值达人（`tag-72`）、才艺技能（`tag-79`）、影视娱乐（`tag-85`）、艺术文化（`tag-87`）、财经投资（`tag-91`）、剧情搞笑（`tag-97`）、房产（`tag-139`）、生活家居（`tag-1001`） |

完整机器可读参数结构见 `references/form-schema.json`。

### 参数取值参考

当前技能没有需要额外查表的分类参数。

### 支持的输入格式

当前技能直接接收 JSON 参数，不涉及分享链接解析。

### 示例请求

下面的示例参数可直接传给 `scripts/run.py`，runner 会把它们发送给 AI Skills API。

```bash
python3 scripts/run.py --params '{"keyword":"深圳烧烤酒吧","contentTag":"tag-48","followerRange":"10-100"}'
```

等价的 `--params` JSON：

```json
{
  "keyword": "深圳烧烤酒吧",
  "contentTag": "tag-48",
  "followerRange": "10-100"
}
```

### 返回结果示例

```json
{
  "success": true,
  "data": {
    "keyword": "深圳烧烤酒吧",
    "platformSource": "_1",
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 1
    },
    "items": [
      {
        "uid": "kol-1",
        "nickname": "深圳烧烤王",
        "region": "广东 深圳",
        "followerCount": 560000,
        "interactionRate30d": 0.082,
        "convertIndex": 82,
        "spreadIndex": 76,
        "starIndex": 91,
        "expectedPlayCount": 320000,
        "price20_60": 180000,
        "contentTags": [
          "美食"
        ]
      }
    ],
    "searchStrategy": {
      "usedFallback": true,
      "droppedFilters": [
        "contentTag"
      ],
      "localContentTagFilterApplied": true
    }
  },
  "meta": {
    "executionTime": 842,
    "cached": false
  }
}
```

### 交付内容

- 达人候选列表：包含账号定位、粉丝规模和内容标签等合作筛选信息。
- 商业价值线索：重点辅助判断传播能力、转化潜力和综合合作优先级。
- 对标账号参考：用于找同赛道创作者、竞品账号和可学习的内容样本。

### 结果使用建议

- 先按赛道和关键词圈定候选，再用商业价值、传播能力和转化潜力做优先级排序。
- 找合作达人时重点看账号定位是否匹配品牌；找对标账号时重点看内容标签和受众相似度。
- 如果筛选条件过窄导致结果少，可以放宽粉丝量或关键词后再比较。

### 运行前准备

- `AISKILLS_BASE_URL`：默认 `https://ai-skills.ai`
- `AISKILLS_API_KEY`：必填，用于认证调用
- `AISKILLS_TENANT_ID`：默认 `default`
