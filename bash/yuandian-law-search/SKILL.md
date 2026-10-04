---
name: yuandian-law-search
homepage: https://github.com/cat-xierluo/legal-skills
author: 杨卫薪律师（微信ywxlaw）
version: "1.1.1"
license: MIT
description: 元典法条与案例检索。本技能应在需要查询中国法律法规条文、检索相关案例、为法律分析提供数据支撑时使用。
---

# 元典法条与案例检索

通过元典开放平台 API 检索中国法律法规条文、案例、法规与企业信息。检索结果归档到：

`/mnt/user-data/workspace/yuandian-law-search/archive`

## 使用前检查

每次调用前先检查 `scripts/.env` 中是否已配置 `YD_API_KEY`。

```bash
if [ -f "scripts/.env" ]; then
  KEY=$(grep '^YD_API_KEY=' scripts/.env | cut -d'=' -f2)
  if [ -n "$KEY" ] && [ "$KEY" != "your-api-key-here" ]; then
    echo "API Key 已就绪"
  else
    echo "API Key 未配置"
  fi
else
  echo ".env 文件不存在"
fi
```

若未配置，则提示用户先在元典开放平台创建 API Key 并写入：

```bash
scripts/.env
YD_API_KEY=sk-你的密钥
```

## 何时使用

在以下场景使用本技能：

- 查询具体法律条文、法规内容或法条详情
- 检索相关案例或查看案例详情
- 查询法规清单或法规详情
- 查询企业基本信息或企业详情
- 为法律分析、合同审查、合规判断提供检索依据

## 接口选择规则

### 法条

- 用户提出自然语言法律问题、想找相关法条：`search`
- 用户给出明确关键词、需要精确筛选：`keyword`
- 用户直接指定法规名 + 条号：`detail`

### 案例

- 用户要找相关案例、已给出关键词或筛选条件：`case`
- 用户描述案情、想找相似案例：`case-semantic`
- 用户要查看某个案例完整文书：`case-detail`
- 仅在明确需要权威案例时使用：`case --authority-only`

### 法规

- 用户要检索法规列表：`regulation`
- 用户要查看某部法规详情：`regulation-detail`

### 企业

- 用户明确要求查询企业信息时：`enterprise`
- 用户明确要求查询企业详情时：`enterprise-detail`

## 调用原则

- 优先选择能直接满足问题的最少调用路径
- 法条语义检索 `search` 返回结果通常已包含条文内容，不要默认再调用 `detail`
- 案例检索先返回列表，只有在需要查看完整文书时才调用 `case-detail`
- 用户提到“之前查过”“历史记录”时，优先读取归档，不要重复请求 API

## 常用命令

### 1. 法条语义检索

```bash
python3 scripts/yd_search.py search "正当防卫的限度" --sxx 现行有效
```

### 2. 法条关键词检索

```bash
python3 scripts/yd_search.py keyword "人工智能 监管" \
  --effect1 法律 --sxx 现行有效 \
  --fbrq-start 2022-01-01 --fbrq-end 2026-03-01
```

### 3. 法条详情

```bash
python3 scripts/yd_search.py detail "民法典" --ft-name "第十五条"
```

### 4. 案例关键词检索

```bash
python3 scripts/yd_search.py case "买卖合同纠纷" --province 广西
```

### 5. 权威案例关键词检索

```bash
python3 scripts/yd_search.py case "买卖合同纠纷" --province 广西 --authority-only
```

### 6. 案例语义检索

```bash
python3 scripts/yd_search.py case-semantic "正当防卫的限度" --jarq-start 2020-01-01
```

### 7. 案例详情

```bash
python3 scripts/yd_search.py case-detail --type ptal --ah "（2025）桂09民终192号"
```

### 8. 法规关键词检索

```bash
python3 scripts/yd_search.py regulation "数据安全" --effect1 法律 --sxx 现行有效
```

### 9. 法规详情

```bash
python3 scripts/yd_search.py regulation-detail --name "中华人民共和国数据安全法"
```

### 10. 企业检索

```bash
python3 scripts/yd_search.py enterprise "华为" --num 5
```

### 11. 企业详情

```bash
python3 scripts/yd_search.py enterprise-detail --credit-code "9144030071526726XG"
```

## 常用筛选参数

### 法条相关

- `--effect1`：效力级别，可多次指定
- `--sxx`：时效性，可多次指定
- `--fbrq-start` / `--fbrq-end`：发布日期范围
- `--ssrq-start` / `--ssrq-end`：实施日期范围

### 案例相关

- `--province` / `--xzqh-p`：省份筛选
- `--jarq-start` / `--jarq-end`：结案日期范围
- `--cj`：法院层级
- `--wenshu-type`：案件类型
- `--authority-only`：仅检索权威案例

## 归档记录

归档目录：

`/mnt/user-data/workspace/yuandian-law-search/archive`

浏览历史记录：

```bash
python3 scripts/yd_search.py archive-list
python3 scripts/yd_search.py archive-list --keyword "正当防卫"
```

## 调试

```bash
python3 scripts/yd_search.py raw /open/law_vector_search "正当防卫" --extra '{"fatiao_filter":{"sxx":["现行有效"]}}'
```

## 更新

```bash
python3 scripts/yd_search.py check-update
python3 scripts/yd_search.py do-update
```

## Reference 文档索引

这些文档用于补充各接口的参数、返回结构和字段含义。  
当需要精确构造请求参数、理解响应字段或排查接口返回异常时，优先查阅对应 reference 文件。

### 法条相关
- `references/01-law-vector-search.md`  
  法条语义检索接口说明。包含 `search` 子命令对应的请求体结构、`fatiao_filter` 过滤条件、返回的 `extra.fatiao` 字段含义。适合在处理自然语言法律问题时查阅。

- `references/02-law-keyword-search.md`  
  法条关键词检索接口说明。包含 `keyword` 子命令的请求参数、AND/OR 检索逻辑、效力级别/时效性/日期过滤参数，以及返回字段说明。适合在用户给出明确关键词时查阅。

- `references/03-law-detail.md`  
  法条详情接口说明。说明如何通过法规名称 + 条号，或 ID 获取单条法条全文与元信息。适合精确引用具体条文时查阅。

### 案例相关
- `references/04-case-semantic-search.md`  
  案例语义检索接口说明。包含 `case-semantic` 子命令的过滤参数、案例类别、法院层级、结案日期等字段说明。适合处理“类似案件怎么判”的问题。

- `references/05-case-keyword-search.md`  
  普通案例关键词检索接口说明。包含全文关键词、案号、标题、案由、法院、援引法条等参数，及 `{total, lst}` 返回结构说明。适合精确筛选普通案例时查阅。

- `references/06-case-keyword-search-authority.md`  
  权威案例关键词检索接口说明。参数与普通案例关键词检索接近，但用于检索权威案例库。适合用户明确要求典型案例、指导性案例、权威案例时查阅。

- `references/07-case-detail.md`  
  案例详情接口说明。说明如何通过 `id` 或 `ah` 获取完整裁判文书正文，以及 `ptal/qwal` 两种案例类型的区别。适合用户要求展开查看某个具体案例时查阅。

### 法规相关
- `references/08-regulation-search.md`  
  法规关键词检索接口说明。用于检索法规级对象而非单条法条，适合查法规名称、法规列表和法规元信息时查阅。

- `references/09-regulation-detail.md`  
  法规详情接口说明。用于获取整部法规的完整信息及条文列表，适合用户要求查看某部法规全文时查阅。

### 企业相关
- `references/10-enterprise-search.md`  
  企业名称检索接口说明。用于按企业名称、曾用名或简称查找企业基本信息及候选结果列表。

- `references/11-enterprise-detail.md`  
  企业详情接口说明。用于按企业 ID 或统一社会信用代码获取企业详细信息。