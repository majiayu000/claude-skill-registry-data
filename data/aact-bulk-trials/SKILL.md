---
name: aact-bulk-trials
description: 使用 AACT (Aggregate Analysis of ClinicalTrials.gov) PostgreSQL 数据库进行大批量临床试验历史分析与数据挖掘。触发场景包括：AACT 查询、临床试验批量分析、PostgreSQL 试验数据、全量 NCT 检索、试验数据挖掘、clinical trials data warehouse、疾病领域全景分析、设计相似试验匹配、跨年度试验趋势聚合。本 skill 通过 SQL 接口处理百万级试验记录，支持云端公共 PostgreSQL 服务（aact-db.ctti-clinicaltrials.org）和每日 dump 本地还原两种连接方式，自动检测并优先使用本地高性能模式。
---

# AACT Bulk Trials · 批量临床试验数据仓库

## 1. 职责边界

**只做**：基于 AACT PostgreSQL 数据库的批量、历史、聚合性临床试验数据分析。
**不做**：
- 实时单条 NCT 查询（→ 使用 `clinical-trials-v2` skill）
- 文献检索（→ 使用 `pubmed-search` / `europepmc-search`）
- 临床数据撰写报告（→ 使用 `clinical-reports`）

**典型用例**：
- "分析血液科所有 IFI（侵袭性真菌感染）相关历史试验的设计趋势"
- "找出过去 10 年 AML 领域全部 III 期试验的赞助商分布"
- "匹配某个 NCT 的设计相似试验（同 condition + intervention + phase）"
- "按国家维度聚合 CAR-T 试验的 status 分布"

---

## 2. 与 clinical-trials-v2 的差异

| 维度 | clinical-trials-v2 | aact-bulk-trials（本 skill） |
|------|-------------------|----------------------------|
| 数据源 | ClinicalTrials.gov v2 REST API | AACT PostgreSQL 镜像（每日同步） |
| 单次容量 | ≤ 1000 条 | 单 SQL 可处理百万级 |
| 网络 | 强依赖 | 本地模式离线可用 |
| 延迟 | 低（实时） | T+1（每日 dump） |
| 适用场景 | 单试验细节、最新状态 | 批量聚合、历史趋势、跨表 JOIN |

---

## 3. 两种连接方式

skill 启动时自动检测优先级：**本地 dump (B) → 云端 (A) → 报错指引**。

### 方式 A · 云端公共 PostgreSQL（推荐零部署）

- Host: `aact-db.ctti-clinicaltrials.org`
- Port: `5432`
- Database: `aact`
- 注册免费账号: https://aact.ctti-clinicaltrials.org/users/sign_up
- 适合：偶发查询、无本地 PostgreSQL、可接受网络延迟

### 方式 B · 本地 dump 还原（高性能 · 离线分析）

- 下载每日 dump（约 2.27 GB pg_dump custom format）：https://aact.ctti-clinicaltrials.org/downloads
- 要求：本地 PostgreSQL 16+
- 还原命令：
  ```bash
  createdb aact
  pg_restore -d aact -j 4 --no-owner --no-privileges /path/to/postgres_data.dmp
  ```
- 适合：批量挖掘、跨年度聚合、设计相似性匹配、整库扫描

### 配置文件 `~/.config/aact.local.yaml`

```yaml
# 优先模式：local 或 cloud；auto 表示自动检测（默认）
mode: auto

local:
  host: localhost
  port: 5432
  database: aact
  user: postgres
  password: ${AACT_LOCAL_PASSWORD}  # 从环境变量读取

cloud:
  host: aact-db.ctti-clinicaltrials.org
  port: 5432
  database: aact
  user: ${AACT_CLOUD_USER}
  password: ${AACT_CLOUD_PASSWORD}

defaults:
  query_limit: 1000          # 防爆默认 LIMIT
  cursor_threshold: 50000    # 超过该行数自动切 server-side cursor
  statement_timeout: 120000  # 毫秒
```

**密钥管理铁律**：永远不要把 password 明文写进 yaml；用 `${VAR}` 占位符 + 环境变量。

---

## 4. AACT Schema 关系图（精简版）

```
                        ┌──────────────┐
                        │   studies    │  主表 nct_id 主键
                        │  (~500K 行)   │
                        └──────┬───────┘
                               │ nct_id (1-N)
        ┌─────────────┬────────┼────────┬──────────────┬───────────────┐
        │             │        │        │              │               │
   ┌────▼─────┐ ┌─────▼────┐ ┌─▼──────┐ ┌─▼───────┐ ┌──▼──────┐ ┌──────▼──────┐
   │conditions│ │interv-   │ │outcomes│ │sponsors │ │facilities│ │eligibilities│
   │(MeSH)    │ │entions   │ │        │ │         │ │(国家/址) │ │(入排标准)   │
   └──────────┘ └──────────┘ └────┬───┘ └─────────┘ └─────────┘ └─────────────┘
                                  │
                            ┌─────▼──────────┐
                            │outcome_analyses│  统计学结果
                            └────────────────┘

  Results-only 子树（仅有结果上传的试验）：
  studies → result_groups → results_baseline / outcome_measurements
```

**关键表**：
- `studies` — 总览（phase, study_type, overall_status, start_date, completion_date, enrollment）
- `conditions` — MeSH 适应症（downcase_name 用于不区分大小写匹配）
- `interventions` — 干预（intervention_type: Drug/Biological/Device/Procedure）
- `outcomes` — 结局指标定义
- `outcome_analyses` — 统计分析（p_value, ci_lower_limit, method）
- `sponsors` — 赞助商（lead_or_collaborator, agency_class: NIH/INDUSTRY/OTHER）
- `eligibilities` — 入排（gender, minimum_age, maximum_age, criteria 全文）
- `facilities` — 站点（country, city, status）
- `result_groups` — 结果分组（arm/group 标识）
- `results_baseline` — baseline 人口学

完整 schema：https://aact.ctti-clinicaltrials.org/schema

---

## 5. 核心检索能力（5 个 SQL 模板）

所有模板默认 `LIMIT 1000`，可通过参数覆盖。生产环境调用前**必须**评估 EXPLAIN。

### 5.1 `query_trials_by_condition(condition_term, year_from, year_to, phase, limit)`

```sql
-- 按适应症（支持 MeSH term 或自由文本，不区分大小写）检索试验
SELECT s.nct_id, s.brief_title, s.phase, s.overall_status,
       s.start_date, s.completion_date, s.enrollment,
       array_agg(DISTINCT c.downcase_name) AS conditions
FROM studies s
JOIN conditions c ON c.nct_id = s.nct_id
WHERE c.downcase_name ILIKE '%' || :condition_term || '%'
  AND (:year_from IS NULL OR s.start_date >= make_date(:year_from, 1, 1))
  AND (:year_to   IS NULL OR s.start_date <  make_date(:year_to + 1, 1, 1))
  AND (:phase     IS NULL OR s.phase = :phase)
GROUP BY s.nct_id
ORDER BY s.start_date DESC NULLS LAST
LIMIT :limit;
```

### 5.2 `query_trials_by_intervention(intervention_name, intervention_type, limit)`

```sql
-- 按干预名称（如 "voriconazole"）+ 类型（Drug/Biological/Device）检索
SELECT s.nct_id, s.brief_title, s.phase, s.overall_status,
       i.name AS intervention_name, i.intervention_type
FROM studies s
JOIN interventions i ON i.nct_id = s.nct_id
WHERE LOWER(i.name) LIKE LOWER('%' || :intervention_name || '%')
  AND (:intervention_type IS NULL OR i.intervention_type = :intervention_type)
ORDER BY s.start_date DESC NULLS LAST
LIMIT :limit;
```

### 5.3 `query_trials_results_summary(nct_id_list)`

```sql
-- 仅查询已上传 results 的试验，返回 baseline + 主要终点统计
WITH have_results AS (
  SELECT nct_id FROM studies
  WHERE nct_id = ANY(:nct_id_list) AND has_results = true
)
SELECT s.nct_id, s.brief_title,
       rb.title AS baseline_title, rb.param_value, rb.param_type,
       oa.p_value, oa.ci_lower_limit, oa.ci_upper_limit, oa.method
FROM have_results h
JOIN studies s ON s.nct_id = h.nct_id
LEFT JOIN results_baseline rb ON rb.nct_id = s.nct_id
LEFT JOIN outcome_analyses oa ON oa.nct_id = s.nct_id
ORDER BY s.nct_id;
```

### 5.4 `bulk_disease_landscape(disease_term, year_from, year_to)` — 疾病全景

```sql
-- 按 phase / sponsor_class / status / 国家 四维聚合
WITH cohort AS (
  SELECT DISTINCT s.nct_id, s.phase, s.overall_status, s.start_date
  FROM studies s
  JOIN conditions c ON c.nct_id = s.nct_id
  WHERE c.downcase_name ILIKE '%' || :disease_term || '%'
    AND s.start_date BETWEEN make_date(:year_from, 1, 1)
                         AND make_date(:year_to, 12, 31)
)
SELECT 'phase' AS dim, COALESCE(phase, 'Unknown') AS bucket, COUNT(*) AS n
FROM cohort GROUP BY phase
UNION ALL
SELECT 'status', overall_status, COUNT(*) FROM cohort GROUP BY overall_status
UNION ALL
SELECT 'sponsor_class', sp.agency_class, COUNT(DISTINCT c.nct_id)
FROM cohort c
JOIN sponsors sp ON sp.nct_id = c.nct_id AND sp.lead_or_collaborator = 'lead'
GROUP BY sp.agency_class
UNION ALL
SELECT 'country', f.country, COUNT(DISTINCT c.nct_id)
FROM cohort c
JOIN facilities f ON f.nct_id = c.nct_id
GROUP BY f.country
ORDER BY dim, n DESC;
```

### 5.5 `find_similar_design_trials(reference_nct_id, limit)`

```sql
-- 找设计相似试验：相同 condition + intervention_type + phase
WITH ref AS (
  SELECT s.phase,
         array_agg(DISTINCT c.downcase_name) AS conds,
         array_agg(DISTINCT i.intervention_type) AS itypes
  FROM studies s
  LEFT JOIN conditions c ON c.nct_id = s.nct_id
  LEFT JOIN interventions i ON i.nct_id = s.nct_id
  WHERE s.nct_id = :reference_nct_id
  GROUP BY s.phase
)
SELECT s.nct_id, s.brief_title, s.phase, s.overall_status,
       COUNT(DISTINCT c.downcase_name) FILTER (
         WHERE c.downcase_name = ANY((SELECT conds FROM ref))
       ) AS shared_conditions
FROM studies s
JOIN conditions c ON c.nct_id = s.nct_id
JOIN interventions i ON i.nct_id = s.nct_id
WHERE s.nct_id <> :reference_nct_id
  AND s.phase = (SELECT phase FROM ref)
  AND i.intervention_type = ANY((SELECT itypes FROM ref))
  AND c.downcase_name = ANY((SELECT conds FROM ref))
GROUP BY s.nct_id
HAVING COUNT(DISTINCT c.downcase_name) >= 1
ORDER BY shared_conditions DESC
LIMIT :limit;
```

---

## 6. 性能优化

### 6.1 默认安全网

- 所有模板内置 `LIMIT 1000`，调用方必须显式传更大值才能突破
- `statement_timeout = 120s`（在 yaml 配置）防止慢查询挂死
- 大于 50K 行的扫描自动切 server-side cursor（Python 用 `psycopg2.connection.cursor(name='aact_stream')`）

### 6.2 推荐 GIN 索引（仅本地 dump 模式）

dump 默认无以下索引，建议建立加速文本检索：

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS idx_conditions_downcase_trgm
  ON conditions USING gin (downcase_name gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_interventions_name_trgm
  ON interventions USING gin (LOWER(name) gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_studies_start_date
  ON studies (start_date) WHERE start_date IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_eligibilities_criteria_trgm
  ON eligibilities USING gin (criteria gin_trgm_ops);
```

### 6.3 查询习惯

- 始终先 `EXPLAIN (ANALYZE, BUFFERS)` 验证大查询
- JOIN 多表时按选择性最高的表先过滤（通常 `conditions`）
- 聚合大于 100K 行时用 `WITH cohort AS (...)` CTE 物化中间结果
- 不要 `SELECT *`，AACT 表通常 30+ 列

---

## 7. 失败模式与处置

| 现象 | 根因 | 处置 |
|------|------|------|
| 云连接超时 / SSL 错误 | 网络限制或 AACT 服务波动 | 切换 `mode: local`；或加 `sslmode=require` 重试 |
| `psql: connection refused` (本地) | 本地 PostgreSQL 未启动 | `pg_ctl start` 或 `brew services start postgresql@16`（Mac）/ `Start-Service postgresql-x64-16`（Win） |
| `password authentication failed` | 凭据错误或缺失 | 检查环境变量；引导用户访问 https://aact.ctti-clinicaltrials.org/users/sign_up 重置 |
| `relation "xxx" does not exist` | AACT 年度 schema 变更（每年 1-2 次） | 对照官方 https://aact.ctti-clinicaltrials.org/schema 校准；常见变更：列重命名、新增 results 子表 |
| 查询无返回但 ClinicalTrials.gov 网站有 | 该试验尚未进入当日 dump（T+1 延迟） | 切 `clinical-trials-v2` 实时 API |
| `OOM` 或客户端被 kill | 一次性拉百万行到内存 | 改用 server-side cursor 或加 `LIMIT` + 分页 |
| `statement timeout` | 查询超过 120s | 检查索引；或临时 `SET LOCAL statement_timeout = 0`；或加 GIN 索引 |

---

## 8. 工作流（Decision Tree）

```
用户请求
  │
  ├─ 单条 NCT 实时？ → 转 clinical-trials-v2
  ├─ 文献需求？ → 转 pubmed-search
  │
  └─ 批量 / 历史 / 聚合？ → 本 skill
        │
        ├─ 1. 检测连接（local → cloud → 报错）
        ├─ 2. 解析意图，匹配 5 个 SQL 模板之一
        ├─ 3. 参数校验（phase 枚举 / 日期合法 / LIMIT 上限）
        ├─ 4. EXPLAIN 评估（大查询）
        ├─ 5. 执行 + 流式取数（>50K 行用 cursor）
        ├─ 6. 后处理（去重、聚合、JSON 序列化）
        └─ 7. 返回结构化结果 + meta（耗时、命中行数、来源 mode）
```

---

## 9. 输出契约

每次返回包含 `meta` + `data`：

```json
{
  "meta": {
    "mode": "local",                  // local | cloud
    "query_template": "bulk_disease_landscape",
    "elapsed_ms": 1842,
    "row_count": 273,
    "limit_applied": 1000,
    "aact_snapshot_date": "2026-04-24",
    "warnings": []
  },
  "data": [ /* 结构因模板而异 */ ]
}
```

---

## 10. 安全与合规

- AACT 数据为公开数据集，但**不含 PHI**也不可重识别患者；勿与内部患者数据 JOIN
- 云端凭据按 `~/.config/aact.local.yaml` 管理，**永不入 git**（加 `.gitignore`）
- 所有 SQL 模板使用**参数化查询**（`:param`），禁止字符串拼接（防注入）
- 引用 AACT 数据时附署：`Data source: AACT (Clinical Trials Transformation Initiative), snapshot {date}`

---

## 11. 测试清单

新模板上线前验证：
- [ ] 在云端和本地两种模式下均可执行
- [ ] 参数化查询无 SQL 注入向量
- [ ] LIMIT 默认生效
- [ ] EXPLAIN 显示使用了预期索引
- [ ] 极端输入（空字符串、超长 NCT 列表、未来年份）不崩溃
- [ ] 无结果时返回空数组而非异常
- [ ] meta.elapsed_ms 在 95th percentile < 5s（本地）/ < 30s（云端）

---

## 12. 参考资料

- AACT 项目主页：https://aact.ctti-clinicaltrials.org
- 每日 dump 下载：https://aact.ctti-clinicaltrials.org/downloads
- Schema 文档：https://aact.ctti-clinicaltrials.org/schema
- 快照公告（schema 变更）：https://aact.ctti-clinicaltrials.org/release_notes
- 注册免费账号：https://aact.ctti-clinicaltrials.org/users/sign_up
- ClinicalTrials.gov v2 API（实时备查）：https://clinicaltrials.gov/data-api/api
- PostgreSQL 16 文档（cursor / GIN）：https://www.postgresql.org/docs/16/

---

**版本**：v1.0 · 2026-04-25
**适配 AACT schema**：2026-Q1（如年度变更请对照 release_notes 校准）
