---
name: prompt
description: >
  프롬프트를 다듬거나 생성하는 스킬. 진단 기반으로 구조, 기법, 표현을 필요한 만큼 개선한다.
  Claude Code 안팎 모두 대상 (SKILL.md, system prompt, API prompt, 웹 프롬프트 등).
  "프롬프트 다듬어줘", "프롬프트 만들어줘", "prompt 정리",
  "이거 프롬프트로", "프롬프트 리파인", "프롬프트 개선",
  "refine prompt", "polish prompt", "improve this prompt",
  "prompt engineering", "system prompt 작성", "system prompt 개선",
  "이런 프롬프트 필요해", "프롬프트 작성해줘",
  "/prompt"
  등에서 트리거.
---

# Prompt

프롬프트를 다듬거나 생성한다. 입력을 진단하고, 부족한 부분만 개선하고, 체크리스트로 검증한다.

## 흐름

1. **진단** — 입력을 보고 무엇이 부족한지 판단
2. **처방** — 부족한 부분만 해당 reference를 참조하여 개선
3. **검증** — `references/checklist.md`로 최종 점검
4. **출력** — 프롬프트 + 뭘 왜 바꿨는지(또는 왜 이렇게 만들었는지) 해설

입력이 초안이면 부족한 부분만 손본다. 목적 설명이면 구조화부터 시작한다.

## 진단 기준

입력을 보고 세 가지를 판단한다:

**구조가 약한가?**
4요소(Instruction, Context, Input Data, Output Indicator) 중 빠진 것이 있거나, delimiter로 영역이 분리되어 있지 않거나, 출력 형식이 지정되어 있지 않다면 → `references/structure.md` 참조.

**기법이 필요한가?**
복잡한 reasoning, 분류, 다단계 처리, 사실 기반 답변 등 단순 지시로 부족한 태스크라면 → `references/techniques.md` 참조.

**표현이 약한가?**
부정형 지시, 모호한 수량, 불필요한 중복, 핵심 지시 미강조 등이 보이면 구조/기법 처방 과정에서 함께 교정한다.

세 가지 모두 괜찮으면 체크리스트 검증만 돌리고 "이미 잘 짜여 있다"고 답한다. 과도하게 손대지 않는다.

## Strategy Escalation

기법은 단순한 것부터. 과도한 기법은 오히려 해롭다.

```
zero-shot → few-shot → CoT → self-consistency → prompt chaining
```

zero-shot으로 충분하면 zero-shot으로 둔다. 모든 프롬프트에 기법을 쑤셔넣지 않는다.

## Reasoning 모델 분기

대상이 reasoning 모델(o1, o3 등)이면:
- 수동 CoT("step by step" 등)를 **제거** — 모델 자체 reasoning을 방해
- Instruction은 simple & direct하게, high-level 지시와 제약만
- 출력 구조는 XML 기본 권장

사용자가 대상 모델을 명시하거나 문맥에서 명확할 때만 적용한다.

## 출력

- 프롬프트 + 해설 (뭘 왜 바꿨는지)
- 형식은 유연하게 — 짧은 프롬프트는 짧은 해설, prompt chaining이면 여러 프롬프트 제시
- 생성 모드에서 목적이 모호하면 프롬프트 작성 전에 확인 질문

## Gotchas

- **과잉 교정**: 이미 잘 짜인 프롬프트를 불필요하게 뜯어고치지 말 것. 진단에서 문제가 없으면 "잘 짜여 있다"고 답하는 게 맞다.
- **생성 시 모호한 목적**: "프롬프트 만들어줘"만 있고 구체적 목적이 없으면, 프롬프트를 만들기 전에 용도/대상/제약을 확인한다.
- **환경 차이**: Claude Code용 프롬프트(tool 사용 가능)와 웹 프롬프트(텍스트만)는 제약이 다르다. 대상 환경을 고려한다.
- **기법 과적용**: "CoT를 넣으면 항상 좋다"는 착각. 단순 분류에 CoT를 넣으면 오히려 느리고 불안정해진다.
