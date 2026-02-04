---
name: stofo-optimize
description: StoFo 알고리즘 최적화 - 낙찰 예측 정확도 향상
model: opus
trigger: /stofo, /optimize
---

# StoFo 최적화 스킬

> **용도**: 낙찰 예측 알고리즘 파라미터 튜닝 및 검증
> **모델**: Opus 4.5 (분석/추론 특화)

---

## 트리거

```bash
/stofo tune         # 파라미터 최적화
/stofo validate     # 예측 검증
/stofo backtest     # 과거 데이터 백테스트
```

---

## 파라미터 튜닝

### 최적화 대상

```yaml
사정률 분포:
  mean: 100.0 → 튜닝 대상
  std: 0.15 → 튜닝 대상

경쟁률 추정:
  base_competitors: 15 → 튜닝 대상
  competition_factor: 1.0 → 튜닝 대상

투찰가 분포:
  mu_offset: 0.0 → 튜닝 대상
  sigma: 0.02 → 튜닝 대상
```

### 최적화 방법

```python
def optimize_parameters(historical_data):
    """
    과거 낙찰 데이터를 기반으로 파라미터 최적화

    목적함수:
    - 예측 오차 최소화 (MAE)
    - 순위 예측 정확도 최대화

    제약:
    - 물리적 의미 유지
    - 오버피팅 방지
    """
    from scipy.optimize import minimize

    def loss_function(params):
        predictions = predict_all(historical_data, params)
        actual = historical_data['actual_results']
        return mean_absolute_error(predictions, actual)

    result = minimize(loss_function, initial_params, method='L-BFGS-B')
    return result.x
```

---

## 예측 검증

### 검증 메트릭

```yaml
정확도 지표:
  - MAE (Mean Absolute Error): 예측가 vs 실제 낙찰가
  - MAPE: 백분율 오차
  - Hit Rate: 낙찰 예측 적중률

순위 지표:
  - Top-3 Accuracy: 상위 3개 예측 정확도
  - Kendall Tau: 순위 상관계수
  - NDCG: 순위 품질 지표

분류 지표:
  - Precision: BID 권장 중 실제 낙찰 비율
  - Recall: 실제 낙찰 중 BID 권장 비율
  - F1 Score: 조화 평균
```

### 검증 리포트

```markdown
## StoFo 예측 검증 리포트

### 테스트 데이터셋
- 기간: 2024-Q4
- 공고 수: 127건
- 낙찰 건수: 23건

### 정확도 지표

| 지표 | 값 | 목표 | 상태 |
|------|-----|------|------|
| MAE | 0.8% | <1.0% | ✅ |
| Hit Rate | 72% | >70% | ✅ |
| Top-3 Acc | 85% | >80% | ✅ |

### 분류 성능

| 권장 | 실제 낙찰 | Precision |
|------|----------|-----------|
| BID | 18/25 | 72% |
| REVIEW | 4/32 | 12.5% |
| SKIP | 1/70 | 1.4% |

### 개선 필요 영역
- 5억 이상 공고 예측 정확도 낮음
- 특수 조건 공고 처리 개선 필요
```

---

## 백테스트

### 백테스트 시나리오

```yaml
시나리오 1: 과거 6개월 전체
  - 기간: 2024-07 ~ 2024-12
  - 대상: 전체 매칭 공고

시나리오 2: 고금액 공고
  - 기간: 2024-07 ~ 2024-12
  - 대상: 5억 이상

시나리오 3: 전략별 성능
  - aggressive vs balanced vs conservative
  - 각 전략 수익률 비교
```

### 백테스트 리포트

```markdown
## StoFo 백테스트 리포트

### 시뮬레이션 결과

| 전략 | 입찰 | 낙찰 | 수익률 | ROI |
|------|------|------|--------|-----|
| aggressive | 45 | 12 | 26.7% | 15% |
| balanced | 45 | 8 | 17.8% | 22% |
| conservative | 45 | 5 | 11.1% | 28% |

### 최적 전략 권장
- 1~3억 공고: balanced
- 3~5억 공고: conservative
- 5억+ 공고: aggressive (높은 마진)

### 월별 성과

| 월 | 입찰 | 낙찰 | 수주액 |
|----|------|------|--------|
| 2024-07 | 8 | 2 | 3.2억 |
| 2024-08 | 7 | 1 | 1.8억 |
| ... | ... | ... | ... |
```

---

## MCP 도구 활용

```yaml
qetta-core:
  - get_stofo_prediction: 예측 실행
  - get_stats: 과거 데이터 조회

sequential-thinking:
  - 파라미터 최적화 과정 구조화
  - 복잡한 분석 단계별 진행

supabase:
  - 과거 낙찰 데이터 조회
  - 예측 결과 저장
```

---

## 사용 예시

```bash
# 파라미터 튜닝
/stofo tune --data=2024-Q4

# 예측 검증
/stofo validate --recent=100

# 백테스트
/stofo backtest --from=2024-07 --to=2024-12 --strategy=all
```

---

*StoFo 최적화 스킬 v1.0*
