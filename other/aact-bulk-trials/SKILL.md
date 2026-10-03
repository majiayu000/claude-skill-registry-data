---
name: aact-bulk-trials
description: 使用 AACT (Aggregate Analysis of ClinicalTrials.gov) PostgreSQL 数据仓库进行批量、历史、聚合性临床试验数据挖掘。Use this skill when the user requests bulk SQL analysis over the full clinical trials data warehouse — historical trial trends, disease landscapes, similar-design matching, or multi-year aggregations across hundreds of thousands of NCT records. 触发场景包括：AACT 查询、临床试验批量分析、PostgreSQL 试验数据、全量 NCT 检索、试验数据挖掘、历史试验分析、clinical trials data warehouse、SQL trials、bulk trial analysis、disease landscape、试验设计相似性匹配、跨年度聚合、sponsor/phase/country 多维统计。**与 clinical-trials-v2 差异**：本 skill 走批量 SQL · 离线大数据（PostgreSQL）；v2 走实时 API · 单查询。两者互补：单条 NCT 实时状态用 v2，百万级历史挖掘用本 skill。支持云端公共 PostgreSQL（aact-db.ctti-clinicaltrials.org · 零部署）和每日 dump 本地还原（高性能 · 离线）两种连接方式，自动检测优先用本地。跨平台（macOS/Linux/Windows）参数化 SQL 防注入，read-only 强制保护。
---

# AACT Bulk Trials · 批量临床试验数据仓库

## 1. 何时调用本 skill

**调用本 skill** 当用户请求：
- 疾病领域全景分析（"过去 10 年血液病所有 NCT 试验按 phase/sponsor 聚合"）
- 跨年度趋势聚合（"AML 领域 III 期试验赞助商分布"）
- 设计相似试验匹配（"找与 NCT12345678 设计相似的其他试验"）
- 整库扫描 / 百万级 JOIN（条件 + 干预 + 结果跨表）

**不要调用本 skill**（应转其他）：
- 单条 NCT 最新状态查询 → `clinical-trials-v2`（实时 API · 互补）
- 文献检索 → `pubmed-search` / `europepmc-search`
- 临床报告撰写 → `clinical-reports`

**与 clinical-trials-v2 的差异**：

| 维度 | clinical-trials-v2 | aact-bulk-trials（本 skill） |
|------|-------------------|----------------------------|
| 数据源 | ClinicalTrials.gov v2 REST API | AACT PostgreSQL 镜像（每日同步） |
| 单次容量 | ≤ 1000 条 | 单 SQL 可处理百万级 |
| 网络 | 强依赖 | 本地模式离线可用 |
| 延迟 | 低（实时） | T+1（每日 dump） |
| 适用场景 | 单试验细节、最新状态 | 批量聚合、历史趋势、跨表 JOIN |

---

## 2. 上下游 skill 协作

```
clinical-trials-v2  ────┐
   (实时单查 · 互补)      │
                         ▼
   aact-bulk-trials  →  medical-evidence-grading  →  evidence-appendix-sync
   (本 skill · 批量SQL)    (上层 · 批量 grade)         (终下游 · 报告附录)
```

- **上游**：用户原始批量挖掘需求（市场调研、疾病全景、设计相似性）
- **平级互补**：`clinical-trials-v2`（单条实时） / `pubmed-search`（文献）
- **下游**：`medical-evidence-grading`（用本 skill 输出的 NCT 列表批量评级） →  `evidence-appendix-sync`（终态报告附录 C）

---

## 3. 核心能力速查（5 个 SQL 模板）

所有签名见 `references/sql-templates.md`，参数化 SQL 防注入，默认 `LIMIT 1000`。

| 函数 | 签名（参数） | 用途 |
|------|------------|------|
| `query_trials_by_condition` | `(condition_term, year_from, year_to, phase, limit)` | 按适应症 + 年份 + phase 检索 |
| `query_trials_by_intervention` | `(intervention_name, intervention_type, limit)` | 按干预名 + 类型检索 |
| `query_trials_results_summary` | `(nct_id_list)` | 已上传 results 的试验统计摘要 |
| `bulk_disease_landscape` | `(disease_term, year_from, year_to)` | 疾病四维聚合（phase/status/sponsor/国家） |
| `find_similar_design_trials` | `(reference_nct_id, limit)` | 设计相似试验匹配 |

完整 SQL 见 → `references/sql-templates.md`

---

## 4. 双连接快速决策

skill 启动时自动检测：**本地 dump (B) → 云端 (A) → 报错指引**。

| 模式 | 何时用 | 性能 |
|------|--------|------|
| 本地 dump（B） | 批量挖掘 / 整库扫描 / 跨年度聚合 | 典型 < 5s |
| 云端公共（A） | 偶发查询 / 无本地 PostgreSQL | 200ms - 2s |

部署细节、yaml 配置、密钥管理、read-only 强制 → `references/connection-setup.md`

Schema 关系图、关键表速查、字段陷阱、推荐 GIN 索引 → `references/aact-schema.md`

---

## 5. 工作流（Decision Tree）

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
        ├─ 3. 参数校验（phase 枚举 / 日期合法 / LIMIT 上限 / NCT 格式 ^NCT\d{8}$）
        ├─ 4. 大查询先 EXPLAIN (ANALYZE, BUFFERS) 评估
        ├─ 5. 执行 + 流式取数（>50K 行用 server-side cursor）
        ├─ 6. 后处理（去重、聚合、JSON 序列化）
        └─ 7. 返回结构化结果 + meta（耗时、命中行数、来源 mode、snapshot 日期）
```

---

## 6. 失败模式与处置

| 现象 | 根因 | 处置 |
|------|------|------|
| 云连接超时 / SSL 错误 | 网络限制或 AACT 服务波动 | 切换 `mode: local`；或加 `sslmode=require` 重试 |
| `psql: connection refused`（本地） | 本地 PostgreSQL 未启动 | macOS: `brew services start postgresql@16` / Linux: `sudo systemctl start postgresql` / Windows: `Start-Service postgresql-x64-16` |
| `password authentication failed` | 凭据错误或环境变量缺失 | 检查 `$AACT_*` 环境变量；引导访问 https://aact.ctti-clinicaltrials.org/users/sign_up |
| `relation "xxx" does not exist` | AACT schema 年度变更（每年 1-2 次） | 对照 https://aact.ctti-clinicaltrials.org/release_notes 校准列名 |
| 查询无返回但 ClinicalTrials.gov 有 | T+1 数据延迟（当日新建试验未入 dump） | 转 `clinical-trials-v2` 实时 API |
| OOM / 客户端被 kill | 一次性拉百万行到内存 | 改用 server-side cursor `cursor(name='aact_stream')` 或加 LIMIT 分页 |
| `statement timeout`（120s） | 查询无索引或选择性差 | 检查 EXPLAIN；建 GIN trigram 索引；或临时 `SET LOCAL statement_timeout = 0` |
| `cannot execute DROP/DELETE in read-only transaction` | 用户/prompt 注入了破坏性 SQL | **正确行为**：read-only 模式拦截了误操作；不要绕过，检查输入来源 |

---

## 7. 输出契约

```json
{
  "meta": {
    "mode": "local",
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

## 8. 安全与合规

- AACT 数据为公开数据集，**不含 PHI**也不可重识别患者；勿与内部患者数据 JOIN
- 云端凭据通过环境变量 + `~/.config/aact.local.yaml`（`.gitignore`），**永不入 git**
- 所有 SQL 模板**参数化查询**（`:param`），禁止字符串拼接
- 会话级 `SET default_transaction_read_only = ON` 强制只读，防 DROP/DELETE 误操作
- 引用 AACT 数据时附署：`Data source: AACT (Clinical Trials Transformation Initiative), snapshot {date}`

---

## 9. References（按需深读）

| 文件 | 内容 |
|------|------|
| `references/connection-setup.md` | 云端 vs 本地 dump 部署、yaml 完整模板、跨平台服务管理、密钥铁律 |
| `references/aact-schema.md` | Schema 关系图、关键表速查、JOIN 路径、字段陷阱、推荐 GIN 索引 |
| `references/sql-templates.md` | 5 个 SQL 模板完整版、参数说明、性能优化、测试清单 |

---

## 10. 参考资料

- AACT 主页：https://aact.ctti-clinicaltrials.org
- 每日 dump：https://aact.ctti-clinicaltrials.org/downloads
- Schema 文档：https://aact.ctti-clinicaltrials.org/schema
- Release notes（schema 变更）：https://aact.ctti-clinicaltrials.org/release_notes
- ClinicalTrials.gov v2 API（实时备查）：https://clinicaltrials.gov/data-api/api

---

**版本**：v2.0 · 2026-04-25 · 适配 AACT schema 2026-Q1
