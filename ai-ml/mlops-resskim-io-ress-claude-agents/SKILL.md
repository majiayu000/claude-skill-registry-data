---
name: mlops
description: "MLOps — Kubeflow 로 ML 파이프라인을 구성하고 KServe 로 서빙, MLOps 와 LLMOps 비교. Use when 학습부터 배포까지 ML 파이프라인을 설계할 때, 실험 추적은 mlops-tracking 을 쓴다."
---

# MLOps 가이드

Kubeflow, KServe를 활용한 ML 파이프라인과 모델 서빙

## Quick Reference (결정 트리)

```
ML 플랫폼 선택?
    |
    +-- Kubernetes 네이티브 ---------> Kubeflow
    |       |
    |       +-- 파이프라인 중심 -----> Kubeflow Pipelines
    |       +-- 모델 서빙 -----------> KServe
    |
    +-- 경량/실험 추적 --------------> MLflow
    |       |
    |       +-- 로컬 + 클라우드 -----> MLflow + S3/GCS
    |       +-- 모델 레지스트리 -----> MLflow Model Registry
    |
    +-- LLM 특화 -------------------> LLMOps 도구
            |
            +-- RAG 운영 ------------> LangChain + 벡터 스토어
            +-- 프롬프트 관리 -------> LangSmith / PromptLayer
            +-- 평가 ----------------> LangSmith / Ragas

MLOps vs LLMOps?
    |
    +-- 전통 ML (분류, 회귀) --------> MLOps
    +-- LLM (생성형 AI) ------------> LLMOps
    +-- 하이브리드 -----------------> 둘 다 필요
```

---

## CRITICAL: MLOps vs LLMOps 비교

| 항목 | MLOps | LLMOps |
|------|-------|--------|
| **모델 훈련** | 직접 훈련 | 파인튜닝 또는 프롬프트 엔지니어링 |
| **데이터** | 구조화된 데이터 | 비정형 텍스트, 문서 |
| **평가 지표** | 정확도, F1, AUC | 유창성, 관련성, 안전성 |
| **버전 관리** | 모델 가중치 | 프롬프트 + 모델 버전 |
| **추론 비용** | 상대적 저렴 | 토큰당 비용 (고가) |
| **레이턴시** | ms 단위 | 초 단위 가능 |
| **컨텍스트** | 고정 입력 | RAG, 대화 기록 |

### 성숙도 모델

```
Level 0: Manual
    +-- 주피터 노트북 실험
    +-- 수동 모델 배포
    +-- 로그 없음

Level 1: Pipeline
    +-- 자동화된 학습 파이프라인
    +-- 모델 레지스트리
    +-- 기본 모니터링

Level 2: CI/CD for ML
    +-- 자동 재학습 트리거
    +-- A/B 테스트 배포
    +-- 데이터 품질 검증

Level 3: Full Automation
    +-- 자동 피처 엔지니어링
    +-- 자동 모델 선택
    +-- 자동 롤백
```

---

## Kubeflow

### 아키텍처

```
+------------------------------------------------------------------+
|                        Kubeflow Platform                           |
+------------------------------------------------------------------+
|                                                                    |
|  +-------------+  +-------------+  +-------------+  +-------------+|
|  | Notebooks   |  | Pipelines   |  | KServe      |  | Katib       ||
|  | (Jupyter)   |  | (Argo)      |  | (Serving)   |  | (AutoML)    ||
|  +-------------+  +-------------+  +-------------+  +-------------+|
|                                                                    |
|  +-------------+  +-------------+  +-------------+                 |
|  | Training    |  | Feature     |  | Model       |                 |
|  | Operators   |  | Store       |  | Registry    |                 |
|  +-------------+  +-------------+  +-------------+                 |
|                                                                    |
+------------------------------------------------------------------+
|                     Kubernetes Cluster                             |
+------------------------------------------------------------------+
```

### 설치

```bash
# Kubeflow 설치 (kustomize)
git clone https://github.com/kubeflow/manifests.git
cd manifests

# 전체 설치
while ! kustomize build example | kubectl apply -f -; do
  echo "Retrying..."
  sleep 10
done

# 또는 개별 컴포넌트
kustomize build apps/pipeline/upstream/env/platform-agnostic-multi-user | kubectl apply -f -
```

### Kubeflow Pipeline 정의

```python
# pipeline.py
from kfp import dsl
from kfp import compiler
from kfp.dsl import component, Input, Output, Dataset, Model, Metrics

@component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn"]
)
def preprocess_data(
    input_data: Input[Dataset],
    output_data: Output[Dataset],
    test_size: float = 0.2
):
    import pandas as pd
    from sklearn.model_selection import train_test_split

    df = pd.read_csv(input_data.path)
    train, test = train_test_split(df, test_size=test_size)
    train.to_csv(output_data.path, index=False)

@component(
    base_image="python:3.11-slim",
    packages_to_install=["pandas", "scikit-learn", "joblib"]
)
def train_model(
    train_data: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics],
    n_estimators: int = 100
):
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib

    df = pd.read_csv(train_data.path)
    X = df.drop('target', axis=1)
    y = df['target']

    clf = RandomForestClassifier(n_estimators=n_estimators)
    clf.fit(X, y)

    # 모델 저장
    joblib.dump(clf, model.path)

    # 메트릭 기록
    metrics.log_metric("accuracy", clf.score(X, y))

@dsl.pipeline(
    name="ML Training Pipeline",
    description="Train and deploy ML model"
)
def ml_pipeline(
    input_data_path: str,
    n_estimators: int = 100
):
    preprocess_task = preprocess_data(
        input_data=dsl.importer(
            artifact_uri=input_data_path,
            artifact_class=Dataset
        )
    )

    train_task = train_model(
        train_data=preprocess_task.outputs["output_data"],
        n_estimators=n_estimators
    )

# 파이프라인 컴파일
compiler.Compiler().compile(ml_pipeline, "pipeline.yaml")
```

### KServe 모델 배포

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-model
  namespace: kubeflow
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "s3://my-bucket/models/sklearn-model"
      resources:
        requests:
          cpu: 100m
          memory: 256Mi
        limits:
          cpu: 500m
          memory: 512Mi

    # 오토스케일링
    minReplicas: 1
    maxReplicas: 10
    scaleTarget: 10  # 동시 요청
    scaleMetric: concurrency
---
# Transformer (전처리/후처리)
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: model-with-transformer
spec:
  transformer:
    containers:
      - name: transformer
        image: myorg/transformer:latest
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "s3://my-bucket/models/model"
```

---

## 참조 스킬

- `/ai:mlops-tracking` - MLflow 실험 추적, 모델 레지스트리
- `/ai:llmops` - RAG 운영, 프롬프트 관리, LLM 평가 & 가드레일
- `/ai:ml-serving` - ML 서빙 심화
