---
name: miracle-analyzer
description: 소원이의 12질문 응답을 분석하여 기적지수(50-100점)와 5대 지표 점수를 산출
version: 1.0.0
trigger: "기적지수 분석"
---

# Miracle Analyzer 스킬

## 🎯 역할

소원이가 작성한 소원폼 12질문 응답을 분석하여:
1. **기적지수** (50-100점) 산출
2. **5대 지표** 점수 계산
3. 맞춤형 분석 결과 생성

## 📊 5대 지표

| 지표 | 설명 | 배점 |
|------|------|------|
| 구체성 | 소원의 명확도 | 20점 |
| 진정성 | 진심의 깊이 | 20점 |
| 실현가능성 | 현실적 달성 가능성 | 20점 |
| 행동의지 | 실천 준비 정도 | 20점 |
| 긍정에너지 | 믿음과 희망 | 20점 |

## 📥 입력

```json
{
  "name": "소원이 이름",
  "wish": "소원 내용",
  "answers": ["Q1답변", "Q2답변", ...]
}
```

## 📤 출력

```json
{
  "miracleIndex": 78,
  "indicators": {
    "specificity": 16,
    "authenticity": 18,
    "feasibility": 14,
    "willingness": 15,
    "positivity": 15
  },
  "summary": "분석 요약 텍스트",
  "recommendation": "맞춤 추천"
}
```

## ⚡ 속도 기준

- 목표: 10초
- 최대: 20초

## 🔗 연동

→ roadmap-generator (30일 로드맵)
→ wish-writer (7일 응원 메시지)
