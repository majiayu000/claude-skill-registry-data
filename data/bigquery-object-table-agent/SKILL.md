---
name: bigquery-object-table-agent
description: BigQuery Object Tables를 활용한 비정형 데이터(오디오, 이미지 등) 분석 및 Audio Analytics Agent 구축 가이드. GCS 데이터 연동, 메타데이터 캐싱, AI 모델 통합, ADK 에이전트 구현 패턴을 다룹니다.
---

# BigQuery Object Table Agent

## Purpose

BigQuery Object Tables를 활용하여 GCS에 저장된 비정형 데이터(오디오, 이미지, 문서 등)를 SQL로 분석하고, 이를 전담하는 ADK 기반 Audio Analytics Agent를 구축하기 위한 가이드입니다. `docs/feature/bigquery-object-table-agent`의 내용을 바탕으로 작성되었습니다.

## When to Use

다음과 같은 상황에서 자동 활성화됩니다:
- BigQuery Object Table 또는 비정형 데이터 분석 언급
- GCS 데이터의 SQL 쿼리 또는 메타데이터 분석 필요 시
- Audio Analytics Agent 구현 또는 오디오 데이터 분석 시
- `metadata_cache_mode`, `max_staleness` 등 Object Table 최적화 설정 시

**Manual activation**: BigQuery Object Table 설정 방법이나 Audio Analytics Agent 구조에 대해 질문하세요.

---

## Core Concepts

### BigQuery Object Tables
GCS의 비정형 데이터를 BigQuery의 구조화된 테이블처럼 조회할 수 있게 해주는 기능입니다.
- **BigLake 기반**: 스토리지와 컴퓨팅의 분리, 통합 보안 관리.
- **SQL 인터페이스**: `uri`, `size`, `updated`, `metadata` 등의 가상 컬럼 제공.
- **AI 통합**: Cloud Vision, Speech-to-Text, Vertex AI 모델을 SQL 함수(`ML.PREDICT` 등)로 직접 호출 가능.

### Architecture
```mermaid
graph LR
    GCS[GCS Bucket\n(Unstructured Data)] -->|BigLake Metadata| BQ[BigQuery Object Table]
    BQ -->|SQL Query| User[User / Agent]
    BQ -->|Remote Function| AI[Vertex AI / Cloud APIs]
```

---

## Setup Workflow

### 1. 사전 요구사항
- **APIs**: `bigquery.googleapis.com`, `bigqueryconnection.googleapis.com`, `storage.googleapis.com`
- **IAM**: `roles/bigquery.admin`, `roles/bigquery.connectionAdmin`, `roles/storage.objectViewer`

### 2. Connection 생성
BigQuery가 GCS에 접근하기 위한 권한 위임 통로입니다.
```bash
bq mk --connection --location=asia-northeast3 --project_id=PROJECT_ID \
    --connection_type=CLOUD_RESOURCE gcs_audio_connection
```
*생성 후 `serviceAccountId`를 확인하여 GCS 버킷에 `Storage Object Viewer` 권한을 부여해야 합니다.*

### 3. Object Table 생성 (DDL)
```sql
CREATE EXTERNAL TABLE `project.dataset.audio_object_table`
WITH CONNECTION `project.region.gcs_audio_connection`
OPTIONS (
  object_metadata = 'SIMPLE',
  uris = ['gs://bucket/path/*.mp3'],
  metadata_cache_mode = 'AUTOMATIC',  -- 성능 핵심
  max_staleness = INTERVAL 1 HOUR
);
```

---

## Agent Implementation

### Audio Analytics Agent
`alyac_family_domain_expert.py` 패턴을 따르는 도메인 전문가 에이전트입니다.

**Specs:**
- **Role**: Audio Analytics Specialist
- **Tools**:
  - `analyze_audio_metadata`: GCS 메타데이터 통계 (크기, 분포 등)
  - `generate_transcription_report`: STT 품질 및 언어 분석
  - `analyze_user_behavior`: Firestore 로그 기반 청취 패턴 분석
  - BigQuery 표준 도구 (`list_templates`, `execute`, `dry_run` 등)

**Instruction Guidelines:**
- **시간 필터**: `TIMESTAMP_SUB` 사용 시 반드시 `DAY` 단위 사용 (MONTH 지원 안 함).
- **JOIN 전략**: `audio_object_table.uri`와 Firestore의 `audio_url`을 조인 키로 사용.
- **비정형 데이터**: 파일 크기(`size`), 스토리지 클래스(`storage_class`) 등을 활용한 비용/성능 최적화 제안.

### Custom Tools (`audio_analysis.py`)
```python
def analyze_audio_metadata(project_id, dataset_id, table_id):
    """
    Object Table을 쿼리하여 스토리지 클래스별 파일 수, 용량, 평균 크기 등을 분석.
    """
    # ... (BigQuery Client 활용)
```

---

## Performance & Optimization

### Metadata Caching
대량의 파일(수천 개 이상)이 있는 경우 필수입니다.
- **설정**: `metadata_cache_mode = 'AUTOMATIC'`
- **효과**: 쿼리 시 GCS 파일 목록을 매번 스캔하지 않고 캐시된 메타데이터 사용 (수 분 -> 수 초 단축).
- **갱신**: `max_staleness` 주기에 따라 자동 갱신되거나, 수동으로 테이블을 재생성하여 갱신.

### Query Optimization
- **Partitioning**: 날짜 기반 파티셔닝을 통해 스캔 비용 절감.
- **Pseudo-columns**: `size`, `updated` 등 메타데이터 컬럼만 조회 시 데이터 스캔 비용 무료(또는 매우 저렴).
- **Filter Early**: `WHERE` 절을 사용하여 불필요한 파일 처리를 사전에 차단.

---

## Reference Documents

상세 내용은 `docs/feature/bigquery-object-table-agent/` 디렉토리를 참조하세요.

- **[README.md](../../docs/feature/bigquery-object-table-agent/README.md)**: 프로젝트 개요 및 빠른 시작.
- **[setup_guide.md](../../docs/feature/bigquery-object-table-agent/setup_guide.md)**: 상세 구축 가이드 및 트러블슈팅.
- **[audio_analytics_agent_plan.md](../../docs/feature/bigquery-object-table-agent/audio_analytics_agent_plan.md)**: 에이전트 설계 및 구현 계획.
- **[bigquery_object_tables_analysis.md](../../docs/feature/bigquery-object-table-agent/bigquery_object_tables_analysis.md)**: 기술 심층 분석.
