---
name: law-local-retrieval
description: 基于 Elasticsearch 的政策法规条文检索 Skill。适用于从已建立的政策法规 ES 索引中检索中国法律法规、政策文件、法律条文、政策依据、执法依据、效力状态、发布机关、发布日期、实施日期等信息，并为政策分析报告、合规审查、执法风险分析提供可回溯的法规依据。
---

# Policy Regulation ES Search Skill

## 1. 技能定位

本技能用于访问 Elasticsearch 中已经建立好的政策法规条文级索引，完成政策法规、法律条文、政策依据、执法依据和合规依据的检索。

本技能的核心能力是：

1. 根据用户问题检索相关政策法规条文；
2. 根据法规名称、条号、法规类别、效力状态、发布日期、实施日期、发布机关等元数据进行过滤；
3. 返回条文正文、法规名称、条号、发布机关、发布日期、实施日期、效力状态、来源路径等可回溯信息；
4. 为政策分析、法规依据引用、执法风险判断、合规审查、专题报告生成等任务提供法规检索支撑。

本技能不是通用知识问答技能，也不是普通网页搜索技能。它只检索当前 Elasticsearch 政策法规索引中已经存在的数据。

---

## 2. 使用边界

### 2.1 应该使用本技能的情况

当用户问题涉及以下任一场景时，应优先使用本技能：

- 查询某部法律、法规、规章、规范性文件或政策文件的具体条文；
- 查询某类治理问题、执法问题、监管问题、审批问题、处罚问题对应的法律法规依据；
- 查询“依据什么法规”“哪一条规定了”“是否有现行有效依据”“有什么执法依据”；
- 查询法规的效力状态、发布机关、发布日期、实施日期；
- 需要在政策分析报告、合规审查报告、执法风险分析报告中引用法规依据；
- 需要对用户上传的数据、台账、通知、报告中的问题匹配法律法规依据；
- 需要输出带有来源路径、法规名称、条号、发布日期等可回溯信息的结果。

典型用户问题包括：

- “电动自行车违规停放和飞线充电涉及哪些法律法规依据？”
- “请检索消防安全整治相关的现行有效法规条文。”
- “《中华人民共和国消防法》中关于占用疏散通道的规定是哪一条？”
- “行政执法过程中，如果未履行告知程序，可能违反哪些法律规定？”
- “请根据相关法规分析某区整治措施是否存在合规风险。”
- “请为市领导报告补充可引用的政策法规依据。”

### 2.2 不应该使用本技能的情况

以下情况不应优先使用本技能：

- 用户只是闲聊、解释概念，且不需要检索政策法规依据；
- 用户要求联网搜索最新新闻、网页内容、公告原文，但这些内容不在 ES 索引中；
- 用户要求处理 Excel、PDF、Word、图片、音视频等文件本身，应先由对应的数据处理或文件解析 skill 处理；
- 用户要求生成图表、统计分析或可视化，本技能只能提供法规依据，不能替代数据分析或图表生成 skill；
- 用户要求写正式公文、报告、通知、讲话稿，本技能只能提供法规依据，不能替代文书生成 skill；
- 用户要求进行纯向量数据库管理、索引创建、数据导入、ES 运维操作，本技能主要用于检索，不负责数据入库和索引维护；
- 用户要求查询国外法律、案例裁判文书、公司信息、新闻资讯，除非这些数据已经被导入当前政策法规 ES 索引。

### 2.3 与其他技能的区别

为避免和其他 skill 混淆，LLM 调用时应注意：

| 技能类型 | 是否使用本技能 | 说明 |
|---|---|---|
| 政策法规条文检索 | 使用 | 本技能专门用于检索 ES 中的政策法规条文 |
| 法律依据匹配 | 使用 | 可检索相关条文并提供依据 |
| 政策分析报告 | 配合使用 | 本技能只提供法规依据，报告撰写应由报告生成能力完成 |
| Excel / 台账分析 | 配合使用 | 先由表格处理 skill 分析数据，再用本技能补充法规依据 |
| PDF / Word 解析 | 配合使用 | 先由文件解析 skill 提取文本，再用本技能检索法规依据 |
| 图表生成 | 不直接使用 | 本技能不生成图表 |
| 网络搜索 | 不替代 | 本技能不联网，只查本地 ES 索引 |
| ES 运维 / 数据导入 | 不作为主要用途 | 本技能可健康检查和查看 mapping，但不负责生产级数据导入 |

---

## 3. 数据来源与索引结构

Elasticsearch 中已经建立政策法规条文级索引。每条文档通常对应一条法律法规条文。

### 3.1 常用字段

主要字段包括：

- `id`：文档唯一 ID；
- `title`：条文标题，通常为“法规名称 + 条号”；
- `content`：条文正文；
- `page_content`：用于检索的拼接文本，通常包含法规名称、章/节信息和条文正文；
- `law_name`：法规名称，例如“中华人民共和国消防法”；
- `article_no`：中文条号，例如“第三十二条”；
- `article_number`：数字条号，例如 `32`；
- `source_article_index`：原始条文序号；
- `category`：法规类别，例如“宪法”“法律”“行政法规”“地方性法规”等；
- `validity_status`：效力状态，例如“有效”；
- `publish_date`：发布日期；
- `effective_date`：实施日期；
- `office`：发布机关；
- `office_level`：发布机关层级；
- `office_category`：发布机关类别；
- `effective_period`：数据集中的年代分段字段，不应直接理解为法规已经失效；
- `source_path`：来源文件路径；
- `metadata`：扩展元数据，包括编、章、节、条、来源标题、来源类型、来源状态、来源发布日期、来源实施日期等；
- `vector-text-embedding-v4`：向量字段，通常不应直接输出给用户；
- `_embedding_model`：向量模型名称；
- `_embedding_dimensions`：向量维度；
- `_embedding_text_field`：生成向量所用文本字段。

### 3.2 默认返回字段原则

为了避免输出过长，检索结果默认应返回以下字段：

- `rank`
- `score`
- `id`
- `title`
- `law_name`
- `article_no`
- `article_number`
- `category`
- `validity_status`
- `publish_date`
- `effective_date`
- `office`
- `office_level`
- `content`
- `source_path`
- `part_title`
- `chapter_title`
- `section_title`

默认不应返回：

- 向量字段；
- 大段重复字段；
- 调试用 highlight 字段；
- 不必要的完整 metadata。

---

## 4. 脚本说明

本技能通过 Python 脚本访问 Elasticsearch，包含三个主要脚本：

```text
scripts/es_policy_search.py
scripts/es_get_mapping.py
scripts/es_health_check.py
```
---

## 5. 核心检索脚本：`scripts/es_policy_search.py`

### 5.1 脚本用途

`es_policy_search.py` 是本技能的核心脚本，用于执行政策法规条文检索。

它支持：

- 普通关键词检索；
- 按法规名称过滤；
- 按条号过滤；
- 按法规类别过滤；
- 按效力状态过滤；
- 按发布机关过滤；
- 按发布日期范围过滤；
- 按实施日期范围过滤；
- 控制返回条数；
- 控制分页起点；
- JSON 格式化输出。

### 5.2 基础调用格式

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py --query "<用户问题或关键词>" --top-k 5 --pretty
```

### 5.3 常用参数

| 参数 | 含义 | 示例 |
|---|---|---|
| `--query` | 用户问题或检索关键词 | `--query "电动自行车 飞线充电 消防安全"` |
| `--top-k` | 最多返回结果数量 | `--top-k 8` |
| `--from` | 分页起点 | `--from 10` |
| `--index` | 指定 ES 索引名 | `--index cn_law_articles_text_embedding_v4` |
| `--law-name` | 按法规名称过滤 | `--law-name "中华人民共和国消防法"` |
| `--title` | 按标题过滤 | `--title "消防法 第二十八条"` |
| `--article-no` | 按中文条号过滤 | `--article-no "第二十八条"` |
| `--article-number` | 按数字条号过滤 | `--article-number 28` |
| `--category` | 按法规类别过滤 | `--category "法律"` |
| `--validity-status` | 按效力状态过滤 | `--validity-status "有效"` |
| `--office` | 按发布机关过滤 | `--office "全国人民代表大会常务委员会"` |
| `--office-level` | 按机关层级过滤 | `--office-level "全国人民代表大会"` |
| `--office-category` | 按机关类别过滤 | `--office-category "人民代表大会"` |
| `--publish-date-from` | 发布日期起始 | `--publish-date-from "2020-01-01"` |
| `--publish-date-to` | 发布日期结束 | `--publish-date-to "2026-12-31"` |
| `--effective-date-from` | 实施日期起始 | `--effective-date-from "2020-01-01"` |
| `--effective-date-to` | 实施日期结束 | `--effective-date-to "2026-12-31"` |
| `--sort-by-date` | 优先按发布日期倒序 | `--sort-by-date` |
| `--pretty` | 格式化 JSON 输出 | `--pretty` |

---

## 6. 检索调用示例

### 6.1 普通关键词检索

适用于用户没有指定具体法律名称，只是询问某类问题对应的法规依据。

用户问题：

```text
电动自行车违规停放和飞线充电涉及哪些法律法规依据？
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "电动自行车 违规停放 飞线充电 消防安全 执法 处罚" \
  --validity-status "有效" \
  --top-k 8 \
  --pretty
```

### 6.2 查询某部法律中的具体条文

适用于用户明确给出法规名称和条号。

用户问题：

```text
查询《中华人民共和国宪法修正案（2018年）》第三十二条。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --law-name "中华人民共和国宪法修正案（2018年）" \
  --article-no "第三十二条" \
  --top-k 3 \
  --pretty
```

说明：

`--top-k 3` 表示最多返回 3 条。如果精确过滤后只有 1 条匹配结果，则只返回 1 条，这是正常情况。

### 6.3 查询某部法律的相关条文

适用于用户指定法律名称，但没有指定条号。

用户问题：

```text
《中华人民共和国消防法》中关于消防通道、疏散通道、安全出口的规定有哪些？
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --law-name "中华人民共和国消防法" \
  --query "消防通道 疏散通道 安全出口 占用 堵塞 封闭" \
  --validity-status "有效" \
  --top-k 10 \
  --pretty
```

### 6.4 只检索现行有效法规

适用于用户强调“现行有效依据”。

用户问题：

```text
请检索现行有效的安全生产事故隐患排查治理相关法律依据。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "安全生产 事故隐患 排查治理 监督管理" \
  --validity-status "有效" \
  --top-k 10 \
  --pretty
```

### 6.5 按法规类别检索

适用于用户只想查法律、行政法规、地方性法规等特定类别。

用户问题：

```text
只查询法律层级中关于城市管理行政执法的依据。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "城市管理 行政执法 处罚 监督检查" \
  --category "法律" \
  --validity-status "有效" \
  --top-k 10 \
  --pretty
```

### 6.6 按发布机关检索

适用于用户要求限定发布机关。

用户问题：

```text
查询全国人大常委会发布的消防安全相关法律条文。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "消防安全 火灾隐患 消防设施" \
  --office "全国人民代表大会常务委员会" \
  --validity-status "有效" \
  --top-k 10 \
  --pretty
```

### 6.7 按发布日期范围检索

适用于用户要求查询某个时间段发布的法规政策。

用户问题：

```text
查询 2020 年以后发布的城市治理相关政策法规依据。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "城市治理 城市管理 基层治理 综合执法" \
  --publish-date-from "2020-01-01" \
  --validity-status "有效" \
  --top-k 10 \
  --sort-by-date \
  --pretty
```

### 6.8 为政策分析报告补充依据

适用于报告类任务，需要将法规依据和业务问题对应起来。

用户问题：

```text
请基于电动自行车违规停放、飞线充电整治台账，补充相关法规依据，并分析执法合规风险。
```

推荐调用：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --query "电动自行车 违规停放 飞线充电 消防安全 疏散通道 安全出口 物业 管理责任 行政处罚" \
  --validity-status "有效" \
  --top-k 12 \
  --pretty
```

LLM 在使用返回结果时，应将法规条文与业务问题建立对应关系，例如：

- 违规停放对应消防通道、安全出口、疏散通道管理要求；
- 飞线充电对应消防安全、用电安全、火灾隐患排查治理要求；
- 物业或管理单位责任对应管理责任、隐患整改、监督检查要求；
- 行政执法风险对应程序合法、依据明确、处罚适当等要求。

### 6.9 精确查询后结果少的处理方式

如果精确查询只返回 1 条，不代表异常。

例如：

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_policy_search.py \
  --law-name "中华人民共和国宪法修正案（2018年）" \
  --article-no "第三十二条" \
  --top-k 3 \
  --pretty
```

如果 ES 中只有一条文档同时满足法规名称和条号条件，则只返回一条。

如果用户想查看更多相关条文，应去掉 `--article-no` 或改用关键词检索。

---

## 7. 健康检查脚本：`scripts/es_health_check.py`

### 7.1 脚本用途

`es_health_check.py` 用于检查 Elasticsearch 服务是否可访问，以及集群是否处于正常状态。

它通常用于：

- skill 调试前确认 ES 是否启动；
- 检索失败时排查是否是 ES 服务不可用；
- 检查账号密码、端口、网络访问是否正常；
- 判断问题是“检索逻辑问题”还是“ES 连接问题”。

### 7.2 调用方式

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_health_check.py
```

### 8.3 预期输出

正常情况下会返回类似 JSON：

```json
{
  "cluster_name": "docker-cluster",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 1
}
```

其中：

- `green`：状态正常；
- `yellow`：通常表示单节点副本未分配，单机环境中可能可以接受；
- `red`：状态异常，需要检查 ES 容器或索引状态；
- 连接失败：需要检查 ES 地址、端口、账号密码、容器状态。

### 8.4 什么时候调用

LLM 不需要在每次法规检索前都调用健康检查。

只有以下情况建议调用：

- 用户明确要求检查 ES 是否可用；
- `es_policy_search.py` 报连接错误；
- 检索脚本超时；
- 出现 HTTP 401、403、404、500 等错误；
- 初次部署或迁移环境后进行验证。

---

## 9. Mapping 查看脚本：`scripts/es_get_mapping.py`

### 9.1 脚本用途

`es_get_mapping.py` 用于查看当前政策法规索引的字段 mapping。

它通常用于：

- 确认索引是否存在；
- 确认字段名是否正确；
- 确认 `law_name`、`article_no`、`content`、`page_content`、`metadata` 等字段的类型；
- 检查向量字段是否存在；
- 排查 term 查询、match 查询、range 查询不生效的问题；
- 新增或调整检索脚本参数前确认字段结构。

### 9.2 调用方式

```bash
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_get_mapping.py
```

如果需要临时指定索引，可先设置环境变量：

```bash
export POLICY_ES_INDEX=cn_law_articles_text_embedding_v4
cd /mnt/skills/custom/policies-regulations/law-local-retrieval && python3 scripts/es_get_mapping.py
```

### 9.3 什么时候调用

LLM 不需要在普通用户检索问题中调用 mapping 脚本。

只有以下情况建议调用：

- 初次配置 skill；
- 检索结果为空，但确认索引中应该有数据；
- 字段过滤不生效；
- `article_no`、`law_name`、`category` 等字段类型不确定；
- 新增参数或修改查询 DSL；
- 用户明确要求查看 ES 索引结构。

---

## 10. LLM 调用决策规则

### 10.1 优先调用规则

当用户问题中出现以下关键词或语义时，应优先调用 `es_policy_search.py`：

- 法律依据；
- 法规依据；
- 政策依据；
- 执法依据；
- 现行有效；
- 条文；
- 第几条；
- 规定；
- 合规风险；
- 执法风险；
- 处罚依据；
- 监管依据；
- 消防安全；
- 安全生产；
- 城市治理；
- 行政执法；
- 审批；
- 管理责任。

### 10.2 参数选择规则

LLM 应根据用户问题自动选择参数：

1. 用户给出具体法规名称：使用 `--law-name`；
2. 用户给出具体条号：使用 `--article-no` 或 `--article-number`；
3. 用户要求“现行有效”：使用 `--validity-status "有效"`；
4. 用户要求某类法规：使用 `--category`；
5. 用户要求某发布机关：使用 `--office`；
6. 用户要求某时间段：使用 `--publish-date-from`、`--publish-date-to`、`--effective-date-from`、`--effective-date-to`；
7. 用户只描述业务问题：使用 `--query` 提取关键词检索；
8. 用户要求报告或分析：先检索法规依据，再基于条文做分析。

### 10.3 关键词构造规则

当用户问题较长时，不应直接把完整问题原样塞入 `--query`，应提取核心关键词。

例如用户问题：

```text
请分析各区电动自行车违规停放和飞线充电问题的执法依据和程序风险。
```

推荐 `--query`：

```text
电动自行车 违规停放 飞线充电 消防安全 疏散通道 安全出口 行政执法 处罚 程序
```

不要使用过于口语化、无关的词。

---

## 11. 重要约束

- 本技能只检索当前 ES 索引中已有的数据；
- 本技能不保证覆盖所有最新法律法规，除非索引已经同步更新；
- 本技能返回的是检索结果，不等同于最终法律意见；
- 回答法律、政策、执法风险问题时，必须基于检索到的条文进行分析；
- 检索不到结果时，不得编造条文；
- 对正式法律意见、重大执法决策、处罚决定等，应提示需要由专业人员复核；
- 默认不输出向量字段；
- 默认不输出无关调试字段；
- 默认优先返回现行有效、相关度高、可回溯的法规依据。
