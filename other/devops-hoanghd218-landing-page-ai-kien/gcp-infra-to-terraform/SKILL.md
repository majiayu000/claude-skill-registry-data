---
name: gcp-infra-to-terraform
description: 기존 GCP 리소스(BigQuery, GCS, IAM 등)를 gcloud/bq 명령어로 추출하여 문서화하고, 이를 Terraform(IaC) 코드로 변환하는 워크플로우 스킬입니다. Reverse Engineering Infrastructure.
---

# GCP Infrastructure to Terraform

## Purpose

현재 수동으로 구축되어 있는 GCP 인프라(특히 BigQuery Object Table, Connection, GCS 등)를 `gcloud` 및 `bq` 명령어를 통해 상태를 추출(Export)하고, 이를 문서화한 뒤 유지보수 가능한 Terraform 코드로 변환하는 과정을 가이드합니다.

## When to Use

다음과 같은 상황에서 자동 활성화됩니다:
- "현재 인프라를 Terraform으로 바꿔줘"
- "gcloud로 설정 내보내기"
- "기존 리소스 문서화 및 IaC 변환"
- "Terraform 마이그레이션"

**Manual activation**: 기존에 구축된 BigQuery Object Table이나 Connection을 코드로 관리하고 싶을 때 사용하세요.

---

## Workflow

### Phase 1: Export & Audit (상태 추출)

기존 리소스의 상세 설정을 JSON 포맷으로 추출하여 정확한 스펙을 파악합니다.

#### 1. BigQuery Connection 추출
```bash
# Connection 상세 정보 (Service Account 등 확인)
bq show --format=json --connection PROJECT_ID.REGION.CONNECTION_ID > connection_config.json
```

#### 2. BigQuery Object Table 추출
```bash
# 테이블 스키마 및 옵션 (DDL 옵션 확인)
bq show --format=json PROJECT_ID:DATASET.TABLE_ID > table_config.json
```

#### 3. IAM 정책 추출
```bash
# GCS 버킷 IAM 정책 (Service Account 권한 확인)
gsutil iam get gs://BUCKET_NAME > bucket_iam.json
```

---

## Phase 2: Documentation (문서화)

추출된 JSON 데이터를 바탕으로 현재 인프라 상태를 사람이 읽을 수 있는 문서(`INFRA_AUDIT.md`)로 정리합니다.

**문서화 포함 항목:**
- **Resource ID**: 프로젝트 ID, 리전, 데이터셋 명, 테이블 명
- **Configuration**:
  - Object Table: `uris`, `metadata_cache_mode`, `max_staleness`
  - Connection: `serviceAccountId`
- **Dependencies**: 어떤 Service Account가 어떤 버킷에 권한을 가지고 있는지

---

## Phase 3: Terraform Conversion (코드 변환)

문서화된 내용을 바탕으로 Terraform 리소스로 매핑합니다.

### 1. Provider & Variables
```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}
```

### 2. BigQuery Connection
`google_bigquery_connection` 리소스를 사용합니다.
```hcl
resource "google_bigquery_connection" "connection" {
  connection_id = "gcs_audio_connection"
  location      = "asia-northeast3"
  cloud_resource {}
}
```

### 3. IAM Binding (GCS)
Connection 생성 시 만들어진 SA에 권한을 부여합니다.
```hcl
resource "google_storage_bucket_iam_member" "connection_permission" {
  bucket = "pio-test-36cf5_cloudbuild"
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_bigquery_connection.connection.cloud_resource[0].service_account_id}"
}
```

### 4. BigQuery Object Table
`google_bigquery_table` 리소스와 `external_data_configuration` 블록을 사용합니다.
```hcl
resource "google_bigquery_table" "object_table" {
  dataset_id = "audio_analytics"
  table_id   = "audio_object_table"

  external_data_configuration {
    autodetect    = false
    source_uris   = ["gs://pio-test-36cf5_cloudbuild/sounds/*.mp3"]
    source_format = "GOOGLE_SHEETS" # Terraform 버그로 인해 비정형 데이터도 포맷 지정 필요할 수 있음 (확인 필요)
    # 실제로는 object_metadata 옵션 사용
    metadata_cache_mode = "AUTOMATIC"
    object_metadata     = "SIMPLE"
  }
  
  # 주의: Terraform Provider 버전에 따라 Object Table 지원 구문이 다를 수 있음
  # 최신 google-beta 프로바이더 사용 권장
}
```

---


## Reference Documents

Detailed guides are available in the `reference/` directory:

- **[Export Guide](reference/export_guide.md)**: Detailed `gcloud` and `bq` commands for extracting configurations.
- **[Terraform Mapping](reference/terraform_mapping.md)**: JSON to HCL mapping reference.

## Tools & Scripts

### Dry Run Script
A helper script to validate and plan your Terraform configuration.

```bash
# Run the dry run script
./.claude/skills/gcp-infra-to-terraform/scripts/dry_run.sh
```

This script will:
1. Check for Terraform installation.
2. Create a sample `main.tf` if none exists.
3. Run `terraform init`, `validate`, and `plan`.

---

## Best Practices

1.  **Import**: 기존 리소스를 Terraform State로 가져올 때는 `terraform import`를 사용합니다.
    ```bash
    terraform import google_bigquery_connection.connection projects/pio-test-36cf5/locations/asia-northeast3/connections/gcs_audio_connection
    ```
2.  **Verification**: `terraform plan`을 실행하여 기존 리소스와 코드 간의 차이(Drift)가 없는지 확인합니다.
3.  **Sensitive Data**: Service Account Key 등 민감 정보는 코드에 하드코딩하지 않습니다.


---

## Example Scenario: Audio Analytics Migration

**User Request**: "현재 `audio_object_table` 설정을 Terraform으로 옮겨줘."

**Agent Action**:
1.  `bq show`로 테이블 옵션(`max_staleness` 등) 확인.
2.  `google_bigquery_table` 리소스 작성.
3.  `terraform import` 명령어 제공.
