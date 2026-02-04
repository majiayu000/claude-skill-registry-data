---
name: dev-coding-debug
description: 체계적인 디버깅(Systematic Debugging) 절차를 통해 버그의 원인을 찾고 해결합니다. (Source: obra/superpowers)
---

# 🐞 체계적 디버깅 (Dev Coding Debug)

이 워크플로우는 `obra/superpowers`의 **"The Iron Law"**를 준수합니다. **근본 원인 규명 없이는 절대 코드를 수정하지 않습니다.**

## 1. 초기화 (Initialization)
1.  **원칙 확인**: `this document`를 읽고 **Iron Law**를 상기합니다.
2.  **증상 정의**: 사용자로부터 정확한 에러 메시지와 현상을 입력받습니다.

## 2. 조사 (Phase 1: Root Cause Investigation)
**"추측하지 말고 증거를 수집하세요."**

1.  **에러 분석**: 스택 트레이스와 에러 코드를 정밀 분석합니다.
2.  **재현 (Reproduction)**: 버그를 확실하게 발생시키는 최소 단위의 스크립트를 작성합니다. (필수)
3.  **기기/로그 추가 (Instrumentation)**: 데이터가 오염되는 지점을 찾기 위해 로그를 추가하고, 데이터 흐름을 역추적(Trace)합니다.

## 3. 분석 (Phase 2: Pattern Analysis)
**"정상적인 패턴과 무엇이 다른가요?"**

1.  **정상 사례 찾기**: 프로젝트 내에서 잘 동작하는 유사한 코드를 찾습니다.
2.  **비교 분석**: 정상 코드와 문제가 있는 코드의 차이점을 한 줄 한 줄 비교합니다.
3.  **차이점 목록**: 사소해 보이는 차이점이라도 모두 나열합니다.

## 4. 가설 (Phase 3: Hypothesis & Testing)
**"과학적 방법론을 적용하세요."**

1.  **가설 수립**: "X 때문에 Y가 발생한다"는 가설을 하나 세웁니다.
2.  **최소 검증**: 가설을 확인하기 위해 변수 하나만 변경하여 테스트합니다. (수정이 아님)
3.  **반복**: 가설이 틀렸다면 변경 사항을 되돌리고(Revert), 새로운 가설을 세웁니다. **기존 변경 위에 덧칠 금지.**

## 5. 해결 (Phase 4: Implementation)
**"증상이 아닌 원인을 고치세요."**

1.  **실패 테스트 (Red)**: 식별된 원인을 타겟으로 하는 실패 테스트 케이스를 확정합니다.
2.  **단일 수정 (Green)**: 근본 원인을 제거하는 최소한의 코드를 작성합니다.
3.  **검증 (Verification)**: 테스트 통과 및 회귀 테스트(Regression Test) 수행.
4.  **정리 (Cleanup)**: 디버깅용 로그와 임시 코드를 깨끗이 삭제합니다.

## 6. 종료 (Completion)
1.  **회고**: 어떤 부분이 근본 원인이었는지 사용자에게 설명하고 종료합니다.


---

## Standards & Rules

# Systematic Debugging (Dev Coding Debug)

## Core Principles (The Iron Law)

> **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

If you haven't completed Phase 1 (Root Cause) and Phase 2 (Pattern Analysis), you cannot propose fixes. Symptom fixes are failure.

## 🏗️ The Four Phases

### Phase 1: Root Cause Investigation
**Goal: Understand WHAT and WHY.**
1.  **Read Errors**: sticky to the error message. Don't skip stack traces.
2.  **Reproduce**: Can you trigger it reliably? If not, gather more data.
3.  **Instrumentation**: For multi-component systems, log data flow at boundaries.
4.  **Trace**: Follow the bad value backwards to its source (`root-cause-tracing`).

### Phase 2: Pattern Analysis
**Goal: Find the standard before fixing.**
1.  **Find Working Examples**: Locate similar code that works.
2.  **Compare**: Read reference implementations completely.
3.  **Identify Differences**: List every difference, however small.

### Phase 3: Hypothesis and Testing
**Goal: Scientific Method.**
1.  **Single Hypothesis**: "I think X is the root cause because Y".
2.  **Test Minimally**: Change ONE variable at a time to test the hypothesis.
3.  **Verify**: If it didn't work, revert and form a NEW hypothesis. NO layering fixes.

### Phase 4: Implementation
**Goal: Fix the root cause, not the symptom.**
1.  **Failing Test**: Create a minimal reproduction test case (Red).
2.  **Single Fix**: Address the identified root cause (Green).
3.  **Verify**: Ensure no regressions.

## �️ Supporting Techniques

### 1. Root Cause Tracing ("Why did this happen?")
**Don't just fix the bad value. Find where it came from.**
- **Technique**: Ask "What called this with a bad value?" repeatedly until you find the source.
- **Rule**: Fix at the source, not at the symptom.

### 2. Defense-in-Depth ("Make it impossible")
**Don't just validate at one place.**
- **Layer 1 (Entry)**: Reject invalid input at IDL/API boundary.
- **Layer 2 (Logic)**: Ensure data makes sense for the operation.
- **Layer 3 (Guard)**: Environment checks (e.g., test vs prod).
- **Layer 4 (Debug)**: Logging for forensics.

### 3. Condition-Based Waiting (No `sleep`)
**Never guess how long something takes.**
- **Bad**: `sleep(50)`
- **Good**: `waitFor(() => condition)`
- **Why**: Flaky tests often come from arbitrary timeouts.

## �🚩 Red Flags (STOP immediately)
- "Quick fix for now"
- "Just try changing X"
- "One more fix attempt" (Limit: 3 attempts. Then question Architecture.)
- Proposing solutions before tracing.

## ✅ Quality Standards
- **Reproduction Script**: Must exist before fixing.
- **Log Cleanup**: All temporary instrumentation removed.
- **Safe YAML**: Frontmatter descriptions quoted.

## Checklist
- [ ] **Phase 1**: Did you identify the *exact* line/reason for failure?
- [ ] **Phase 2**: Did you compare with a working example?
- [ ] **Phase 4**: Is there a test case that failed before and passes now?
- [ ] **Cleanup**: Are all `print`/`console.log` removed?
