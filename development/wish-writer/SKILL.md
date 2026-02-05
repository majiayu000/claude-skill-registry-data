---
name: wish-writer
description: 7일간 매일 아침/저녁 발송할 응원 메시지 14개 생성
version: 1.0.0
trigger: "응원 메시지 생성"
---

# Wish Writer 스킬

## 🎯 역할

소원이 맞춤형 7일 응원 메시지 생성:
1. **아침 메시지** (7개): 하루 시작 동기부여
2. **저녁 메시지** (7개): 하루 마무리 격려
3. 총 14개 메시지

## 📥 입력

```json
{
  "name": "소원이 이름",
  "wish": "소원 내용",
  "miracleIndex": 78,
  "personality": "분석된 성향"
}
```

## 📤 출력

```json
{
  "messages": [
    {
      "day": 1,
      "morning": "좋은 아침이에요, {name}님! ...",
      "evening": "오늘 하루도 수고했어요..."
    },
    // ... Day 2-7
  ],
  "totalCount": 14
}
```

## 💬 메시지 스타일

- 따뜻하고 친근한 어조
- 소원이 이름 호명
- 소원 내용 연결
- 구체적 행동 제안
- 이모지 적절히 활용

## ⚡ 속도 기준

- 목표: 5초
- 최대: 10초

## 🔗 연동

← miracle-analyzer (분석 결과)
→ message-dispatcher (메시지 발송)
