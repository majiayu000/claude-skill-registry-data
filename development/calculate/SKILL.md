---
name: calculate
description: Perform basic arithmetic operations.
version: 1.0.0
author: Azure GPT-5.X Skillset Sample
parameters:
  type: object
  properties:
    expression:
      type: string
      description: "The math expression to evaluate, e.g. '2 + 2'"
  required:
    - expression
---

# Calculator Skill 🧮

기본적인 수학 연산을 수행하는 스킬입니다.

## 행동 지침 (Playbook)

계산 결과를 출력할 때는 다음 지침을 따르세요:

1. **수식 언급**: 단순 결과만 말하지 말고, 어떤 계산을 수행했는지 수식을 다시 한 번 언급하세요.
2. **천 단위 구분**: 결과값이 1,000이 넘을 경우 쉼표(,)를 사용해 천 단위 구분을 하세요.
3. **의미 설명**: 계산 결과의 의미를 짧게 덧붙이세요.

## 지원 연산

- 덧셈: `+`
- 뺄셈: `-`
- 곱셈: `*`
- 나눗셈: `/`
- 거듭제곱: `**`
- 괄호: `()`

## 예시 응답

```
2 + 2의 계산 결과는 4입니다.
간단한 덧셈 연산이네요!
```

```
1000 * 1000의 계산 결과는 1,000,000입니다.
백만이라는 큰 숫자가 나왔네요!
```

## 사용 예시

- "2 더하기 3은?"
- "100 곱하기 25 계산해줘"
- "(10 + 5) * 3 계산"

## 보안 주의사항

⚠️ 이 스킬은 안전한 수식만 평가합니다. 시스템 명령이나 악성 코드 실행은 차단됩니다.
