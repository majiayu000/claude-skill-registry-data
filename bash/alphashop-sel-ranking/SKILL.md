---
name: alphashop-sel-ranking
description: 查询Amazon和TikTok平台的关键词榜单、商品榜单和类目数据，支持热销榜、飙升榜、新品榜、蓝海词榜等多种类型，帮助快速发现跨境选品机会。
metadata:
  manai:
    primaryEnv: none
    requires:
      env: []
title: Alpha跨境选品
example: 查询亚马逊美国站服饰类目的热搜词排行榜，分析前五名关键词的趋势。
version: 1.0.0
---
> **⚠️ 重要提示**:
>
> 本 skill 使用 **AlphaShop API**，需要配置：
> - `ALPHASHOP_ACCESS_KEY`
> - `ALPHASHOP_SECRET_KEY`
>
> **不要与 `1688-ranking` 混淆！** 如果你看到要求 `ALI1688_APP_KEY`、`ALI1688_REFRESH_TOKEN` 等变量，说明你运行了错误的 skill。
>
> 两个 skill 的区别：
> - `1688-ranking`: 使用 1688 官方 Open API（OAuth 认证，需要 ALI1688_* 变量）
> - `alphashop-sel-ranking`: 使用 AlphaShop 平台 API（JWT 认证，需要 ALPHASHOP_* 变量）

## 配置

### 环境变量

需要配置 AlphaShop API 凭证（与 alphashop-sel-newproduct 共享）：

**重要提示**: `userId` 参数需要使用 **Java Long 类型范围的数字**（建议使用大于 10 位的整数），例如 `1234567890123`。小整数如 `123456` 会导致参数校验失败。

```json5
{
  skills: {
    entries: {
      "alphashop-sel-ranking": {
        env: {
          ALPHASHOP_ACCESS_KEY: "你的AccessKey",
          ALPHASHOP_SECRET_KEY: "你的SecretKey",
          ALPHASHOP_ENV: "pre"  // 可选: pre(预发) 或 prod(线上)，默认 pre
        }
      }
    }
  }
}
```

**环境说明**:
- `ALPHASHOP_ENV=pre` - 预发环境: `https://pre-api.alphashop.cn`
- `ALPHASHOP_ENV=prod` - 线上环境(默认): `https://api.alphashop.cn`

### 如何获取 API Key

#### 获取途径

本 skill 使用 AlphaShop/遨虾平台的 API 服务，需要申请以下凭证：
- `ALPHASHOP_ACCESS_KEY` - API 访问密钥（32位字符）
- `ALPHASHOP_SECRET_KEY` - API 密钥

#### 申请步骤

1. **联系平台方**
   - 如果您是 1688 或阿里内部用户，请联系 AlphaShop/遨虾 平台管理员

2. **获取凭证**
   - 平台审核通过后会提供 Access Key 和 Secret Key
   - 确认凭证格式：Access Key 为32位，Secret Key 为更长字符串
   - 确认凭证有效期和权限范围

3. **配置到环境**
   - 命令行方式：`export ALPHASHOP_ACCESS_KEY='...'`
   - 或使用 OpenClaw 配置（推荐）

#### 验证配置

```bash
# 检查环境变量
echo "Access Key: ${ALPHASHOP_ACCESS_KEY:0:10}..."
echo "Secret Key: ${ALPHASHOP_SECRET_KEY:0:10}..."

# 运行环境检查脚本
bash check-env.sh

# 测试 API 调用
python3 scripts/ranking.py overview --platform amazon --country US
```

# AlphaShop选品榜单查询SKILL

通过榜单服务API查询跨境电商市场的热门关键词、爆款商品和类目数据，快速发现选品机会。

## 功能说明

本 Skill 封装了 1688 选品系统的榜单服务 API，提供 5 大核心功能：

### 1. 获取总榜列表 (overview)
返回可用的榜单配置和元数据，包括：
- 机会赛道榜（关键词维度）
- 全网商品榜（商品维度）
- 平台国家映射
- 榜单更新时间

### 2. 查询关键词榜单 (keyword)
根据平台、国家、类目、榜单类型查询关键词榜单明细，包括：
- 关键词市场机会分
- 销量和销售额数据
- 市场竞争指数
- 商品图片预览
- **仅支持一级类目**

**使用模式**:
- **交互式模式** (推荐): 不提供参数或使用 `--interactive`,系统将引导您完成以下步骤:
  1. 选择关注的平台 (Amazon/TikTok)
  2. 选择国家 (默认US)
  3. 自动查询并展示该平台国家的所有类目
  4. 选择感兴趣的类目
  5. 选择榜单类型 (热销词榜/蓝海词榜)
  6. 展示查询结果

- **命令行模式**: 提供所有必需参数 (--platform, --country, --cate-id, --ranking-type) 直接查询

### 3. 查询商品榜单 (product)
根据平台、国家、类目层级、榜单类型查询商品榜单明细，包括：
- 商品基本信息
- 销量趋势
- 评分评论
- 上架时间
- **支持1-3级类目**
- **支持全站榜单查询**

**使用模式**:
- **交互式模式** (推荐): 不提供参数或使用 `--interactive`,系统将引导您完成以下步骤:
  1. 选择关注的平台 (Amazon/TikTok)
  2. 选择国家 (默认US)
  3. 选择查询全站榜单或指定类目
  4. 如选择指定类目,自动查询并展示商品类目树(支持1-3级)
  5. 选择感兴趣的类目
  6. 选择榜单类型 (热销榜/飙升榜/新品榜/微创新榜)
  7. 展示查询结果

- **命令行模式**: 提供所有必需参数 (--platform, --country, --ranking-type) 直接查询

### 4. 查询商品类目 (product-category)
获取指定平台和国家的商品类目树（最多3层），按商品数量降序排列

### 5. 查询关键词类目 (keyword-category)
获取指定平台和国家的关键词类目列表（仅一级类目），按关键词数量降序排列

---


## 支持的平台和国家

### Amazon 平台
支持国家：`US`, `GB`, `ES`, `FR`, `DE`, `IT`, `CA`, `JP`

### TikTok 平台
支持国家：`ID`, `VN`, `MY`, `TH`, `PH`, `US`, `SG`, `BR`, `MX`, `GB`, `ES`, `FR`, `DE`, `IT`, `JP`

---

## 榜单类型说明

### 商品维度榜单

| 榜单类型 | 代码 | 说明 | 适用场景 |
|---------|------|------|---------|
| 热销榜 | HOT_SELL_LIST | 验证过的成熟爆款 | 适合跟卖或寻找供应链 |
| 销量飙升榜 | SALE_GROW_LIST | 短期爆发型商品 | 适合捕捉季节性趋势或网红效应 |
| 趋势新品榜 | NEW_ITM_LIST | 处于上升期的新潜力股 | 适合早期切入 |
| 微创新机会榜 | IMPROVE_LIST | 存在痛点改进空间的高销商品 | 适合差异化开发 |

### 关键词维度榜单

| 榜单类型 | 代码 | 说明 | 适用场景 |
|---------|------|------|---------|
| 热销词榜 | sold_cnt | 高流量大词 | 适合投放广告或SEO布局 |
| 蓝海词榜 | new_itm | 高需求低竞争词 | 适合中小卖家突围 |

---

## 使用方法

### 功能1: 获取总榜列表

#### 基础用法

查询指定平台和国家的榜单配置：

```bash
python3 scripts/ranking.py overview \
  --platform amazon \
  --country US
```

#### 输出示例

```
→ 正在查询总榜列表: AMAZON US
→ 请求中... (响应时间约5秒内)

======================================================================
总榜列表
======================================================================

1. 全网商品榜
   描述: 基于销量、评分等多维度筛选的优质商品榜单
   子榜单 (4):
     - 热销榜 (HOT_SELL_LIST)
       更新时间: 2026-03-23 10:00:00
     - 销量飙升榜 (SALE_GROW_LIST)
       更新时间: 2026-03-23 10:00:00
     - 趋势新品榜 (NEW_ITM_LIST)
       更新时间: 2026-03-23 10:00:00
     - 微创新机会榜 (IMPROVE_LIST)
       更新时间: 2026-03-23 10:00:00

2. 机会赛道榜
   描述: 基于市场机会分析的关键词榜单
   子榜单 (2):
     - 热销词榜 (sold_cnt)
       更新时间: 2026-03-23 10:00:00
     - 蓝海词榜 (new_itm)
       更新时间: 2026-03-23 10:00:00
```

---

### 功能2: 查询关键词榜单

#### 交互式模式（推荐）

无需提供任何参数,系统会引导您完成查询流程:

```bash
python3 scripts/ranking.py keyword
```

交互式流程:
1. **选择平台**: 从 Amazon 和 TikTok 中选择
2. **选择国家**: 输入国家代码(默认US)或直接回车
3. **查看类目**: 系统自动查询并展示所有可用类目及关键词数量
4. **选择类目**: 从列表中选择感兴趣的类目
5. **选择榜单类型**: 热销词榜 或 蓝海词榜
6. **查看结果**: 展示关键词榜单数据

**示例输出**:
```
======================================================================
关键词榜单查询 (交互式)
======================================================================

请选择您关注的平台:
  1) AMAZON
  2) TIKTOK

请输入序号 [1-2]: 1

选择的平台: AMAZON

请选择国家 (支持: US, GB, ES, FR, DE, IT, CA, JP):
请输入国家代码 [默认: US]:

→ 正在查询 AMAZON US 的关键词类目...

找到 12 个类目:

   1) Clothing - 1580 个关键词
   2) Home & Kitchen - 1250 个关键词
   3) Sports & Outdoors - 980 个关键词
   ...

请选择类目序号 [1-12]: 1

选择的类目: Clothing (ID: 2001)

请选择榜单类型:
  1) 热销词榜 (sold_cnt)
  2) 蓝海词榜 (new_itm)

请输入序号 [1-2]: 1

→ 正在查询关键词榜单...
```

#### 命令行模式（高级用法）

如果您已知所有参数,可以直接查询:

```bash
python3 scripts/ranking.py keyword \
  --platform amazon \
  --country US \
  --cate-id 123456 \
  --ranking-type sold_cnt
```

#### 带类目名称

```bash
python3 scripts/ranking.py keyword \
  --platform amazon \
  --country US \
  --cate-id 123456 \
  --ranking-type new_itm \
  --cate-name "Clothing"
```

#### 强制交互式

即使提供了部分参数,也可以使用 `--interactive` 强制进入交互式模式:

```bash
python3 scripts/ranking.py keyword --interactive
```

#### 参数说明

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--platform` | String | ⚠️ | 平台（amazon/tiktok）,不提供则交互式询问 | `amazon` |
| `--country` | String | ⚠️ | 国家代码,不提供则使用默认US | `US` |
| `--cate-id` | String | ⚠️ | 类目ID（**仅支持一级类目**）,不提供则交互式选择 | `123456` |
| `--ranking-type` | String | ⚠️ | 榜单类型（sold_cnt/new_itm）,不提供则交互式选择 | `sold_cnt` |
| `--cate-name` | String | ❌ | 类目名称 | `"Clothing"` |
| `--interactive` | Flag | ❌ | 强制使用交互式模式 | - |
| `--output-json` | Flag | ❌ | 输出完整JSON | - |

**注意**: 如果缺少 `--platform`、`--cate-id` 或 `--ranking-type` 任一参数,将自动进入交互式模式

#### 输出示例

```
→ 正在查询关键词榜单: AMAZON US - 类目 123456 - sold_cnt
→ 请求中... (响应时间约5秒内)

======================================================================
关键词榜单 (100)
======================================================================

1. yoga pants (瑜伽裤)
   平台: AMAZON | 国家: US
   机会分: 42.5 - 击败同一级类目85.3%关键词
   排名: #1
   平均价格: US$25.99
   月销量: 113.7K
   在售商品: 15K

2. yoga mat (瑜伽垫)
   平台: AMAZON | 国家: US
   机会分: 38.2 - 击败同一级类目78.5%关键词
   排名: #2
   平均价格: US$22.50
   月销量: 85.3K
   在售商品: 12K

... 还有 90 个关键词（使用 --output-json 查看完整数据）
```

---

### 功能3: 查询商品榜单

#### 交互式模式（推荐）

无需提供任何参数,系统会引导您完成查询流程:

```bash
python3 scripts/ranking.py product
```

交互式流程:
1. **选择平台**: 从 Amazon 和 TikTok 中选择
2. **选择国家**: 输入国家代码(默认US)或直接回车
3. **选择范围**:
   - 全站榜单(不限定类目)
   - 或 指定类目榜单
4. **查看类目**(如选择指定类目): 系统自动查询并展示所有类目(支持1-3级树形结构)
5. **选择类目**(如选择指定类目): 从列表中选择感兴趣的类目
6. **选择榜单类型**: 热销榜/飙升榜/新品榜/微创新榜
7. **查看结果**: 展示商品榜单数据

**示例输出**:
```
======================================================================
商品榜单查询 (交互式)
======================================================================

请选择您关注的平台:
  1) AMAZON
  2) TIKTOK

请输入序号 [1-2]: 1

选择的平台: AMAZON

请选择国家 (支持: US, GB, ES, FR, DE, IT, CA, JP):
请输入国家代码 [默认: US]:

查询范围:
  1) 全站榜单 (不限定类目)
  2) 指定类目榜单

请选择 [1-2, 默认: 1]: 2

→ 正在查询 AMAZON US 的商品类目...

找到 15 个一级类目:

   1) Clothing [L1] - 125000 个商品
   2)   Women's Clothing [L2] - 85000 个商品
   3)     Activewear [L3] - 15000 个商品
   4)     Dresses [L3] - 20000 个商品
   5)   Men's Clothing [L2] - 40000 个商品
   ...

请选择类目序号 [1-35]: 3

选择的类目: Activewear (ID: 1001-01-01, L3)

请选择榜单类型:
  1) 热销榜 (HOT_SELL_LIST)
  2) 销量飙升榜 (SALE_GROW_LIST)
  3) 趋势新品榜 (NEW_ITM_LIST)
  4) 微创新机会榜 (IMPROVE_LIST)

请输入序号 [1-4]: 1

→ 正在查询商品榜单...
```

#### 命令行模式（高级用法）

**查询全站榜单**:

```bash
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type HOT_SELL_LIST
```

**指定类目（一级类目）**:

```bash
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type SALE_GROW_LIST \
  --cate-id 123456 \
  --cate-level 1
```

**指定类目（二级类目）**:

```bash
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type NEW_ITM_LIST \
  --cate-id 789012 \
  --cate-level 2 \
  --cate-name "Women's Clothing"
```

#### 强制交互式

即使提供了部分参数,也可以使用 `--interactive` 强制进入交互式模式:

```bash
python3 scripts/ranking.py product --interactive
```

#### 参数说明

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `--platform` | String | ⚠️ | 平台（amazon/tiktok）,不提供则交互式询问 | `amazon` |
| `--country` | String | ⚠️ | 国家代码,不提供则使用默认US | `US` |
| `--ranking-type` | String | ⚠️ | 榜单类型,不提供则交互式选择 | `HOT_SELL_LIST` |
| `--cate-id` | String | ❌ | 类目ID,不提供则交互式选择或查全站 | `123456` |
| `--cate-level` | String | ❌ | 类目层级（1/2/3） | `1` |
| `--cate-name` | String | ❌ | 类目名称 | `"Clothing"` |
| `--interactive` | Flag | ❌ | 强制使用交互式模式 | - |
| `--output-json` | Flag | ❌ | 输出完整JSON | - |

**注意**: 如果缺少 `--platform` 或 `--ranking-type` 任一参数,将自动进入交互式模式

**榜单类型**:
- `HOT_SELL_LIST` - 热销榜
- `SALE_GROW_LIST` - 销量飙升榜
- `NEW_ITM_LIST` - 趋势新品榜
- `IMPROVE_LIST` - 微创新机会榜

#### 输出示例

```
→ 正在查询商品榜单: AMAZON US - 类目 123456 (L1) - HOT_SELL_LIST
→ 请求中... (响应时间约5秒内)

======================================================================
商品榜单 (100)
======================================================================

1. Women's High Waist Yoga Pants - Tummy Control
   商品ID: B0ABC12345
   平台: AMAZON | 国家: US
   机会分: 78.5
   价格: US$29.99
   月销量: 5.2K
   评分: 4.5 ⭐ (1523条评论)
   上架时间: 2025/10/15
   链接: https://www.amazon.com/dp/B0ABC12345

2. Premium Yoga Mat with Carrying Strap
   商品ID: B0DEF67890
   平台: AMAZON | 国家: US
   机会分: 72.3
   价格: US$24.99
   月销量: 4.8K
   评分: 4.7 ⭐ (2891条评论)
   上架时间: 2025/09/20
   链接: https://www.amazon.com/dp/B0DEF67890

... 还有 98 个商品

> **字段说明**：
> - **必有字段**：商品ID、平台、国家、价格、商品链接
> - **可选字段**：机会分、月销量、评分、上架时间、商品图片等
> - 实际显示字段取决于API返回的数据，部分字段可能为空而不显示
> - 如需查看API返回的所有字段，使用 `--debug-fields` 参数
```

---

### 功能4: 查询商品类目

#### 基础用法

```bash
python3 scripts/ranking.py product-category \
  --platform amazon \
  --country US
```

#### 输出示例

```
→ 正在查询商品类目: AMAZON US
→ 请求中... (响应时间约5秒内)

======================================================================
类目树 (15 个一级类目)
======================================================================

服装鞋包 (ID: 1001, 商品数: 125000)
  └─ 女装 (ID: 1001-01, 商品数: 85000)
    └─ 运动装 (ID: 1001-01-01, 商品数: 15000)
    └─ 连衣裙 (ID: 1001-01-02, 商品数: 20000)
    ... 还有 8 个子类目
  └─ 男装 (ID: 1001-02, 商品数: 40000)
    └─ T恤 (ID: 1001-02-01, 商品数: 12000)
    ... 还有 6 个子类目

家居厨房 (ID: 1002, 商品数: 95000)
  └─ 厨房用品 (ID: 1002-01, 商品数: 50000)
    ... 还有 4 个子类目

... 还有 13 个一级类目（使用 --output-json 查看完整数据）
```

---

### 功能5: 查询关键词类目

#### 基础用法

```bash
python3 scripts/ranking.py keyword-category \
  --platform amazon \
  --country US
```

#### 输出示例

```
→ 正在查询关键词类目: AMAZON US
→ 请求中... (响应时间约5秒内)

======================================================================
类目树 (12 个一级类目)
======================================================================

Clothing (ID: 2001, 商品数: 1580)
Home & Kitchen (ID: 2002, 商品数: 1250)
Sports & Outdoors (ID: 2003, 商品数: 980)
Beauty & Personal Care (ID: 2004, 商品数: 850)
Electronics (ID: 2005, 商品数: 720)

... 还有 7 个一级类目（使用 --output-json 查看完整数据）
```

---

### 功能6: 查询1688类目信息

#### 基础用法

本地查询1688平台一级类目信息（不需要API调用）：

```bash
# 列出所有类目
python3 scripts/test_categories.py list

# 根据ID查询类目
python3 scripts/test_categories.py get --id 2

# 根据名称搜索类目
python3 scripts/test_categories.py search --name 服装
```

#### 输出示例

**查询类目**:
```
✅ 找到类目:
  类目ID: 2
  类目名称: 食品、饮料
  别名: 食品酒水
```

**搜索类目**:
```
✅ 找到 1 个匹配的类目:

  ID          3: 服装
```

---

## 特殊策略说明

### 1. 随机洗牌策略

**适用接口**: 关键词榜单、商品榜单

- **目的**: 避免榜单固化，给更多商品/关键词展示机会
- **实现**: 从候选池中随机抽取指定数量的结果
- **影响**: 每次查询相同参数，返回的榜单顺序可能不同

### 2. 类目轮播策略

**适用接口**: 商品类目、关键词类目

- **目的**: 根据时间段轮播展示不同类目，避免首位类目过度曝光
- **实现**: 基于当前时段计算轮播索引，将对应类目排在第一位
- **影响**: 不同时间段查询，类目排序可能不同

### 3. 候选池配置

**关键词榜单**:
- 候选池大小: 500
- 展示数量: 100
- 仅支持一级类目

**商品榜单**:
| 类目层级 | 候选池大小 | 展示数量 |
|---------|-----------|---------|
| 一级类目 | 500 | 100 |
| 二级类目 | 200 | 50 |
| 三级类目 | 100 | 30 |

---

## 使用技巧

### 1. 优先使用交互式模式（关键词和商品榜单）

对于关键词和商品榜单查询,**强烈推荐使用交互式模式**:

```bash
# 交互式查询关键词榜单 (推荐)
python3 scripts/ranking.py keyword

# 交互式查询商品榜单 (推荐)
python3 scripts/ranking.py product

# 优势:
# - 无需记忆类目ID
# - 自动查询并展示类目列表
# - 支持全站或指定类目查询
# - 友好的引导式体验
```

### 2. 商品榜单的两种查询方式

**方式A: 全站榜单**（快速查看整体市场）
```bash
# 交互式: 选择"全站榜单"
python3 scripts/ranking.py product
# 然后在步骤3选择: 1) 全站榜单

# 命令行:
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type HOT_SELL_LIST
```

**方式B: 类目榜单**（精准类目分析）
```bash
# 交互式: 选择"指定类目榜单"
python3 scripts/ranking.py product
# 然后在步骤3选择: 2) 指定类目榜单
# 系统会展示多级类目树供选择
```

### 3. 多次查询获取更多样本

由于采用随机洗牌策略，可以多次查询同一榜单，获取不同的商品/关键词样本：

```bash
# 第一次查询
python3 scripts/ranking.py keyword --platform amazon --country US --cate-id 123456 --ranking-type sold_cnt

# 等待几秒后第二次查询（会得到不同的结果顺序）
python3 scripts/ranking.py keyword --platform amazon --country US --cate-id 123456 --ranking-type sold_cnt
```

### 4. 使用 JSON 输出进行数据分析

```bash
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type NEW_ITM_LIST \
  --cate-id 123456 \
  --cate-level 1 \
  --output-json > analysis.json
```

数据会同时输出到终端和自动保存到 `output/alphashop-sel-ranking/` 目录。

### 5. 使用调试模式排查字段问题

如果发现某些字段（如商品链接、图片链接）没有显示，使用 `--debug-fields` 参数诊断：

```bash
# 调试商品榜单
python3 scripts/ranking.py product \
  --platform amazon \
  --country US \
  --ranking-type HOT_SELL_LIST \
  --debug-fields

# 调试关键词榜单
python3 scripts/ranking.py keyword \
  --platform amazon \
  --country US \
  --cate-id 123456 \
  --ranking-type sold_cnt \
  --debug-fields

# 交互式模式也支持调试
python3 scripts/ranking.py product --debug-fields
```

**调试输出说明**：
- 显示第一个条目的所有字段名和值
- 标记空字符串和null值
- 帮助诊断字段缺失或数据不完整问题

**查看详细的调试指南**：[DEBUG_FIELDS_GUIDE.md](DEBUG_FIELDS_GUIDE.md)

---

## 错误处理

### 常见错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `platform or country is empty!` | 平台或国家参数缺失 | 检查必填参数 |
| `cateId is empty!` | 类目ID缺失 | 添加 --cate-id 参数 |
| `Invalid ranking type` | 榜单类型不合法 | 检查榜单类型是否在支持列表中 |
| `Invalid country code` | 国家代码不合法 | 检查国家代码是否在支持列表中 |
| `FAIL_AUTH_ERROR` | API 凭证不正确 | 检查 ALPHASHOP_ACCESS_KEY 和 ALPHASHOP_SECRET_KEY |
| `FAIL_REQUEST_PARAMETER_ILLEGAL` | userId 参数非法 | userId 必须是 Java Long 类型（>10位整数） |
| `请求超时` | 网络问题或服务响应慢 | 稍后重试或切换环境 |

### 环境诊断

运行环境检查脚本诊断配置问题：

```bash
bash check-env.sh
```

检查项包括：
- ✅ 当前目录和 skill 名称
- ✅ 必需的环境变量（ALPHASHOP_ACCESS_KEY、ALPHASHOP_SECRET_KEY）
- ⚠️  错误的环境变量（ALI1688_* 相关变量）

---

## 注意事项

1. **响应时间**: 所有接口响应时间在5秒内
2. **数据更新**: 榜单数据每天更新
3. **类目限制**:
   - 关键词榜单仅支持一级类目
   - 商品榜单支持1-3级类目
4. **随机性**: 由于随机洗牌策略，相同查询参数多次请求可能返回不同的结果顺序
5. **平台差异**: Amazon 和 TikTok 的部分字段不同

---

## 安全声明

本 Skill 的安全策略：

### 数据处理
- ✅ 不处理个人身份信息（PII）
- ✅ 不访问生产数据库
- ✅ 仅查询公开的榜单数据

### 权限要求
- ✅ 需要 AlphaShop API 凭证（通过环境变量配置）
- ✅ 不需要 Root 或管理员权限
- ✅ 输出文件仅写入当前目录的 `output/` 子目录

### 网络访问
- ✅ 仅访问 AlphaShop API 端点
  - 预发环境：`https://pre-api.alphashop.cn`
  - 线上环境：`https://api.alphashop.cn`
- ✅ 所有请求使用 HTTPS 加密
- ✅ 设置 30 秒超时防止长时间阻塞

### 敏感信息保护
- ✅ API 密钥通过环境变量传递，不写入日志
- ✅ 错误信息仅包含 RequestId，不包含完整请求内容
- ✅ 输出文件权限仅限当前用户访问

---

## 能力边界与约束

### ✅ 本 Skill 可以做什么

- ✅ 查询 Amazon 和 TikTok 平台的多种榜单类型（热销榜/飙升榜/新品榜/蓝海词榜等）
- ✅ 支持关键词榜单和商品榜单两大查询模式
- ✅ 支持交互式模式：自动引导用户选择平台→查询范围→类目→榜单类型
- ✅ 商品榜单支持全站查询和 1-3 级类目树形展示
- ✅ 支持切换环境（预发/生产）
- ✅ 将榜单结果保存到本地文件
- ✅ 可以多次调用，查询不同关键词、类目或榜单类型

### ❌ 本 Skill 不能做什么

- ❌ **不能批量查询**：一次调用只能查询一个关键词或一个类目的榜单
- ❌ **不能跨平台对比**：一次只能查询一个平台（Amazon 或 TikTok）
- ❌ **不能深度分析**：只展示榜单原始数据，不做商品分析、市场趋势分析
- ❌ **不能历史对比**：只返回当前榜单数据，不包含历史排名变化
- ❌ **不能自定义榜单规则**：榜单类型和计算规则由 AlphaShop 平台预定义
- ❌ **不能访问其他 API**：只调用 AlphaShop 榜单相关端点

### 💡 合理的延伸问题示例

**✅ 推荐的延伸方向**（在能力范围内或可多次调用实现）：
- "换一个关键词查询看看"
- "切换到商品榜单模式"
- "查询 TikTok 平台的同一个关键词"
- "查看某个具体类目的热销榜"
- "切换到飙升榜查看新兴趋势"
- "将榜单保存到文件"
- "对比'瑜伽裤'在 Amazon 和 TikTok 的榜单"（提示：需要手动调用两次）

**❌ 不推荐的延伸方向**（超出 skill 范围）：
- "分析这 10 个关键词在两个平台的差异"（需要数据分析工具）
- "预测这个关键词下个月的排名"（无预测能力）
- "筛选出价格低于 50 美元的上榜商品"（API 可能不返回价格数据）
- "对比这个商品今天和上周的排名变化"（无历史对比能力）

**💡 后续处理建议**：
- 可以将同一关键词在不同平台的榜单保存后，手动对比差异
- 可以定期查询同一关键词/类目，手动记录排名变化趋势
- 可以结合榜单数据，在对应平台上进一步查看商品详情

## API 参考文档

完整的API接口和数据结构文档请参阅 [references/api-ranking-list.md](references/api-ranking-list.md)。
