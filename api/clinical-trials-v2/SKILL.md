---
name: clinical-trials-v2
description: 通过 ClinicalTrials.gov API v2 实时检索官方临床试验注册数据。触发词包括 ClinicalTrials.gov、临床试验、NCT、试验注册、招募状态、phase 1/2/3、RCT lookup、interventional trial、observational study。专注实时单次查询(≤1000 条/请求),适合"某试验最新状态/招募信息/主次要终点"场景。批量历史分析请用 aact-bulk-trials,文献检索用 pubmed-search/europepmc。
keywords:
  - clinical-trials
  - clinicaltrials-gov
  - nct
  - trial-registry
  - recruitment-status
  - phase-1-2-3
  - rct-lookup
  - interventional
  - observational
  - real-time-api
license: MIT
---

# ClinicalTrials.gov API v2 实时检索

封装 ClinicalTrials.gov 官方 API v2,为医学证据检索体系提供"实时官方源"原子能力。

## 1. 定位与边界

### 只做
- 通过 `https://clinicaltrials.gov/api/v2/studies` 实时检索单个/批量试验
- 单次请求 ≤ 1000 条记录
- 返回完整 protocol + results 模块结构化数据

### 不做
- **大批量历史分析**(>10k 试验 / 全量 NCT 镜像) → 用 `aact-bulk-trials` (本地 PostgreSQL)
- **文献检索** → 用 `pubmed-search` / `europepmc`
- **全文 XML 解析** → 用 `bioc-fulltext`
- **Meta 分析编排** → 用 `systematic-review`

### 与 aact-bulk-trials 关系
| 维度 | clinical-trials-v2 (本 skill) | aact-bulk-trials |
|---|---|---|
| 数据源 | 实时 API | 每日同步的 PostgreSQL 镜像 |
| 单次规模 | ≤1000 条 | 无限 |
| 延迟 | 实时 (T+0) | T-1 |
| 适用场景 | 用户问某试验最新状态 | 批量分析所有 NCT |
| 速率限制 | 建议 ≤5 RPS | 仅本地 IO |

## 2. 认证与速率

### 无需 API key
ClinicalTrials.gov API v2 是开放 API,无需注册或 API key。

### 建议 User-Agent
```python
HEADERS = {
    "User-Agent": "ClinicalTrialsV2-Skill/1.0 (medical-evidence-retrieval; contact@example.com)",
    "Accept": "application/json",
}
```

### 速率限制
- 官方未强制 RPS 限制,但建议自约束 ≤5 RPS
- 实现指数退避: 429/503 → 退避 2^n * 0.5s, 最多 5 次重试

## 3. 安装与依赖

```bash
pip install httpx tenacity pydantic
```

仅依赖标准 HTTP 客户端,无需特殊 SDK。

## 4. 核心 API 设计

### 统一返回 dataclass

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TrialRecord:
    nct_id: str
    title: dict                      # {"brief": str, "official": str}
    status: str                      # RECRUITING / ACTIVE_NOT_RECRUITING / COMPLETED / ...
    phase: list[str]                 # ["PHASE2", "PHASE3"]
    study_type: str                  # INTERVENTIONAL / OBSERVATIONAL / EXPANDED_ACCESS
    condition: list[str]
    intervention: list[dict]         # [{"type": "DRUG", "name": "Pembrolizumab"}]
    sponsor: dict                    # {"lead": str, "class": "INDUSTRY"|"NIH"|...}
    enrollment: Optional[int]
    enrollment_type: Optional[str]   # ACTUAL / ESTIMATED
    start_date: Optional[str]
    completion_date: Optional[str]
    primary_outcomes: list[dict]     # [{"measure": str, "time_frame": str}]
    locations: list[dict]            # [{"facility": str, "city": str, "country": str, "status": str}]
    has_results: bool
    last_update_posted: Optional[str]
    source_url: str = field(init=False)

    def __post_init__(self):
        self.source_url = f"https://clinicaltrials.gov/study/{self.nct_id}"
```

### 5 个核心检索函数

#### 4.1 `search_studies(query, filters)`
综合检索入口,支持自由文本 + 结构化过滤器组合。

```python
def search_studies(
    query: str,
    *,
    recruitment_status: list[str] | None = None,    # ["RECRUITING", "ACTIVE_NOT_RECRUITING"]
    phase: list[str] | None = None,                  # ["PHASE2", "PHASE3"]
    study_type: str | None = None,                   # "INTERVENTIONAL"
    country: str | None = None,
    sponsor: str | None = None,
    date_from: str | None = None,                    # "2023-01-01"
    date_to: str | None = None,
    page_size: int = 100,                            # ≤1000
    max_results: int = 500,
) -> list[TrialRecord]:
    """组合查询。query 走 query.term,过滤器映射到 filter.* 参数。"""
```

#### 4.2 `get_study_details(nct_id)`
按 NCT ID 获取完整 protocol + results。

```python
def get_study_details(nct_id: str) -> TrialRecord:
    """GET /api/v2/studies/{nct_id}?format=json"""
```

#### 4.3 `search_by_condition(condition_term, ...)`
疾病专项检索,内部映射到 `query.cond`。

```python
def search_by_condition(
    condition_term: str,                  # "Multiple Myeloma" / "AML"
    *,
    status: list[str] | None = None,
    phase: list[str] | None = None,
    country: str | None = None,
    max_results: int = 200,
) -> list[TrialRecord]:
```

#### 4.4 `search_by_intervention(intervention_term, intervention_type)`
干预专项检索,映射到 `query.intr`。

```python
def search_by_intervention(
    intervention_term: str,                          # "Pembrolizumab" / "CAR-T"
    intervention_type: str | None = None,            # "DRUG"|"DEVICE"|"BEHAVIORAL"|"BIOLOGICAL"
    *,
    status: list[str] | None = None,
    max_results: int = 200,
) -> list[TrialRecord]:
```

#### 4.5 `get_study_outcomes(nct_id)`
专取主/次要终点 + 已发布结果(若 hasResults=True)。

```python
def get_study_outcomes(nct_id: str) -> dict:
    """
    返回:
    {
      "primary_outcomes": [...],
      "secondary_outcomes": [...],
      "has_results": bool,
      "results": {...} | None,         # outcomeMeasuresModule + adverseEventsModule
    }
    """
```

## 5. 参数化过滤器枚举

### recruitment_status (有效值)
`NOT_YET_RECRUITING` · `RECRUITING` · `ENROLLING_BY_INVITATION` · `ACTIVE_NOT_RECRUITING` · `COMPLETED` · `SUSPENDED` · `TERMINATED` · `WITHDRAWN` · `UNKNOWN`

### phase
`EARLY_PHASE1` · `PHASE1` · `PHASE2` · `PHASE3` · `PHASE4` · `NA`

### study_type
`INTERVENTIONAL` · `OBSERVATIONAL` · `EXPANDED_ACCESS`

### intervention_type
`DRUG` · `DEVICE` · `BIOLOGICAL` · `PROCEDURE` · `RADIATION` · `BEHAVIORAL` · `GENETIC` · `DIETARY_SUPPLEMENT` · `COMBINATION_PRODUCT` · `DIAGNOSTIC_TEST` · `OTHER`

### date 字段
- `study_first_posted`: 首次注册时间
- `last_update_posted`: 最近更新
- `results_first_posted`: 结果首次发布
- `start_date` / `completion_date` / `primary_completion_date`

## 6. API v2 端点映射

| 函数 | HTTP | 关键参数 |
|---|---|---|
| search_studies | GET /api/v2/studies | query.term, filter.overallStatus, filter.phase |
| get_study_details | GET /api/v2/studies/{nct_id} | format=json |
| search_by_condition | GET /api/v2/studies | query.cond |
| search_by_intervention | GET /api/v2/studies | query.intr |
| get_study_outcomes | GET /api/v2/studies/{nct_id} | fields=protocolSection.outcomesModule,resultsSection |

### 分页
API v2 使用 `pageToken` 游标分页,响应中 `nextPageToken` 用于下一页。

```python
params = {"pageSize": 100, "pageToken": next_token}
```

## 7. 标准请求示例

```python
import httpx

BASE = "https://clinicaltrials.gov/api/v2/studies"

def _fetch(params: dict) -> dict:
    with httpx.Client(headers=HEADERS, timeout=30.0) as client:
        r = client.get(BASE, params=params)
        r.raise_for_status()
        return r.json()

# 示例: 检索"多发性骨髓瘤 + PHASE3 + RECRUITING"
data = _fetch({
    "query.cond": "Multiple Myeloma",
    "filter.overallStatus": "RECRUITING",
    "filter.phase": "PHASE3",
    "pageSize": 100,
    "format": "json",
})
```

## 8. 错误与重试

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=8),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
    reraise=True,
)
def _fetch_with_retry(params: dict) -> dict:
    ...
```

错误处理优先级:
- `404` (NCT 不存在) → 直接抛 `TrialNotFoundError`,不重试
- `429`/`503` → 指数退避
- `400` (参数错误) → 抛 `InvalidQueryError`,记录原参数

## 9. 输出规范

- **永远返回结构化 dataclass**,不返回 raw JSON
- `source_url` 字段供下游引文用
- list 字段空值用 `[]` 而非 `None`
- 日期统一 `YYYY-MM-DD` 字符串(原始 API 可能返回 `YYYY-MM`,前端补 `-01`)

## 10. 集成下游

```python
# 与 evidence-appendix-sync 协作
for trial in search_studies("CAR-T", recruitment_status=["RECRUITING"]):
    appendix.add_reference({
        "type": "clinical_trial",
        "id": trial.nct_id,
        "title": trial.title["official"] or trial.title["brief"],
        "url": trial.source_url,
        "accessed": today_iso(),
    })
```

## 11. 测试清单

- [ ] `get_study_details("NCT04368728")` 返回 BNT162b2 完整 protocol
- [ ] `search_by_condition("Acute Myeloid Leukemia", status=["RECRUITING"])` ≥10 条
- [ ] `search_by_intervention("Pembrolizumab", "DRUG")` 返回 KEYNOTE 系列
- [ ] `get_study_outcomes("NCT00000000")` 对未发布结果试验返回 `has_results=False`
- [ ] 不存在的 NCT 触发 `TrialNotFoundError`
- [ ] 5 次连续 429 后正确退避并最终返回结果
- [ ] 分页超过 1000 条时使用 pageToken 自动续取

## 12. 限制与注意

- API v2 已替代 v1(2024-06 起 v1 deprecated),本 skill 仅使用 v2
- `hasResults=True` 不代表所有 endpoint 已发布;需检查 `resultsSection` 各子模块
- `locations` 数组可能极大(国际多中心试验 >500 站点),按需用 `fields` 参数裁剪
- 单次 ≥1000 条请用 `aact-bulk-trials` 改走本地镜像
- 试验 status 字段可能滞后真实招募情况(由 sponsor 自报),严肃决策需交叉验证
- 不要把本 skill 用于"导出全库做统计"——会被识别为滥用模式
