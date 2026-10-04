---
name: paper2code
description: |
  연구 논문(PDF/arXiv URL)을 분석하여 실행 가능한 코드로 변환합니다.
  논문 복제, 알고리즘 구현, 연구 재현 요청 시 자동으로 활성화됩니다.
  "이 논문 구현해줘", "paper2code", "논문 코드로 변환" 등의 요청에 반응합니다.
---

# Paper2Code: 연구 논문을 코드로 변환하는 AI 에이전트

## 개요

이 Skill은 연구 논문을 체계적으로 분석하고, 실행 가능한 코드로 변환하는 **4+2단계 파이프라인**을 실행합니다.

**핵심 원칙**: 단순히 논문을 읽고 코드를 생성하는 것이 아니라, **구조화된 중간 표현(YAML)**을 먼저 생성한 후 코드를 작성합니다.

---

## ⚠️ 핵심 행동 제어 규칙 (CRITICAL)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ MANDATORY BEHAVIORAL RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 한 번에 하나의 파일만 구현
2. 파일 구현 후 확인/허락 없이 다음 파일로 진행
3. 논문 원본 사양이 항상 참조 코드보다 우선
4. 완료 전 각 Phase의 Self-Check 필수 수행
5. 모든 중간 결과는 YAML 파일로 저장

DO:
✓ 논문에 명시된 것을 정확히 구현
✓ 간단하고 직접적인 코드 작성
✓ 작동하는 것 우선, 우아한 것은 나중
✓ 각 컴포넌트 즉시 테스트
✓ 구현 완료 후 바로 다음 파일로 이동

DON'T:
✗ 파일 사이에 "다음 파일을 구현할까요?" 묻지 말 것
✗ 핵심 기능에 필요하지 않은 광범위한 문서화
✗ 재현에 필요하지 않은 최적화
✗ 과도한 추상화나 디자인 패턴
✗ 지시만 제공하고 실제 코드를 작성하지 않는 것
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 입력 처리

### 지원 형식
1. **arXiv URL**: `https://arxiv.org/abs/xxxx.xxxxx` 또는 `https://arxiv.org/pdf/xxxx.xxxxx.pdf`
2. **PDF 파일 경로**: `/path/to/paper.pdf`
3. **이미 변환된 텍스트/마크다운**: 논문 내용이 텍스트로 제공된 경우

### 입력 처리 방법

**arXiv URL인 경우:**
```bash
# PDF URL로 변환하여 다운로드
curl -L "https://arxiv.org/pdf/xxxx.xxxxx.pdf" -o paper.pdf

# PDF를 텍스트로 변환 (pdftotext 사용)
pdftotext -layout paper.pdf paper.txt
```

**PDF 파일인 경우:**
```bash
pdftotext -layout "/path/to/paper.pdf" paper.txt
```

---

## 파이프라인 개요

```
[사용자 입력: 논문 URL/파일]
        │
        ▼
┌─────────────────────────────────────────────┐
│ Step 0: 논문 텍스트 확보                     │
│ - arXiv URL → PDF 다운로드                  │
│ - PDF → 텍스트 변환                         │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 0: 참조 코드 검색 (선택적)             │
│ @[05_reference_search.md]                   │
│ 출력: reference_search.yaml                 │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 1: 알고리즘 추출                       │
│ @[01_algorithm_extraction.md]               │
│ 출력: 01_algorithm_extraction.yaml          │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 2: 개념 분석                           │
│ @[02_concept_analysis.md]                   │
│ 출력: 02_concept_analysis.yaml              │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 3: 구현 계획                           │
│ @[03_code_planning.md]                      │
│ 출력: 03_implementation_plan.yaml           │
└─────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────┐
│ Phase 4: 코드 구현                           │
│ @[04_implementation_guide.md]               │
│ 출력: 완전한 프로젝트 디렉토리               │
└─────────────────────────────────────────────┘
```

---

## 단계 간 데이터 전달 형식

### Phase 1 → Phase 2 전달
```yaml
phase1_to_phase2:
  algorithms_found: "[발견된 알고리즘 수]"
  key_algorithms:
    - name: "[알고리즘 이름]"
      section: "[논문 섹션]"
      complexity: "[Simple/Medium/Complex]"
  hyperparameters_count: "[수집된 하이퍼파라미터 수]"
  critical_equations: "[핵심 수식 번호 목록]"
  missing_info: "[누락된 정보 목록]"
```

### Phase 2 → Phase 3 전달
```yaml
phase2_to_phase3:
  components_count: "[식별된 컴포넌트 수]"
  implementation_complexity: "[Low/Medium/High]"
  key_dependencies:
    - "[컴포넌트 A] → [컴포넌트 B]"
  experiments_to_reproduce:
    - "[실험 이름]: [예상 결과]"
  success_criteria:
    - "[구체적인 성공 기준]"
```

### Phase 3 → Phase 4 전달
```yaml
phase3_to_phase4:
  file_order: "[구현 순서대로 파일 목록]"
  current_file: "[현재 구현 중인 파일]"
  completed_files: "[완료된 파일 목록]"
  blocking_dependencies: "[해결해야 할 의존성]"
```

---

## 각 Phase 상세

### Phase 0: 참조 코드 검색 (선택적)
@[05_reference_search.md](05_reference_search.md) 프롬프트를 사용하여:
- 유사 구현체 5개 검색 및 평가
- 구현 품질 향상을 위한 참조 확보
- **출력**: YAML 형식의 참조 목록

### Phase 1: 알고리즘 추출
@[01_algorithm_extraction.md](01_algorithm_extraction.md) 프롬프트를 사용하여:
- 모든 알고리즘, 수식, 의사코드 추출
- 하이퍼파라미터와 설정값 수집
- 학습 절차 및 최적화 방법 정리
- **출력**: YAML 형식의 완전한 알고리즘 명세

### Phase 2: 개념 분석
@[02_concept_analysis.md](02_concept_analysis.md) 프롬프트를 사용하여:
- 논문 구조 및 섹션 매핑
- 시스템 아키텍처 분석
- 컴포넌트 간 관계 및 데이터 흐름 파악
- 실험 및 검증 요구사항 정리
- **출력**: YAML 형식의 구현 요구사항 명세

### Phase 3: 구현 계획 수립
@[03_code_planning.md](03_code_planning.md) 프롬프트를 사용하여:
- Phase 1, 2 결과를 통합
- 5개 필수 섹션의 상세 구현 계획 생성:
  1. `file_structure`: 프로젝트 파일 구조
  2. `implementation_components`: 구현할 컴포넌트 상세
  3. `validation_approach`: 검증 및 테스트 방법
  4. `environment_setup`: 환경 및 의존성
  5. `implementation_strategy`: 단계별 구현 전략
- **출력**: 완전한 YAML 구현 계획 (8000-10000자)

### Phase 4: 코드 구현
@[04_implementation_guide.md](04_implementation_guide.md) 가이드를 따라:
- 계획에 따라 파일별로 코드 생성
- 의존성 순서대로 구현
- 각 파일은 완전하고 실행 가능해야 함
- **출력**: 실행 가능한 코드베이스

---

## 메모리 관리
@[06_memory_management.md](06_memory_management.md) 가이드를 참조:
- 긴 논문 처리 시 컨텍스트 관리
- 단계별 출력 저장
- 중단 시 복구 프로토콜

---

## 품질 기준

### 반드시 지켜야 할 원칙
- **완전성**: 플레이스홀더나 TODO 없이 완전한 구현
- **정확성**: 논문에 명시된 수식, 파라미터 정확히 반영
- **실행 가능성**: 바로 실행할 수 있는 코드
- **재현 가능성**: 논문의 결과를 재현할 수 있어야 함

### 파일 구현 순서
1. 설정 및 환경 파일 (config, requirements.txt 초기화)
2. 핵심 유틸리티 및 베이스 클래스
3. 메인 알고리즘/모델 구현
4. 학습 및 평가 스크립트
5. 문서화 (README.md, requirements.txt 최종화)

---

## ✅ 최종 완료 체크리스트 (MANDATORY)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ BEFORE DECLARING COMPLETE - ALL MUST BE YES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ 논문의 모든 알고리즘이 구현됨?                 → YES / NO
□ 정확한 버전의 모든 환경/데이터셋 설정됨?       → YES / NO
□ 실험에서 참조된 모든 비교 방법 구현됨?         → YES / NO
□ 논문의 실험을 실행할 수 있는 작동하는 통합?    → YES / NO
□ 모든 metrics, figures, tables 재현 가능?      → YES / NO
□ 결과 재현 방법을 설명하는 기본 문서?           → YES / NO
□ 코드가 에러 없이 실행됨?                       → YES / NO

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 하나라도 NO라면 완료가 아님!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 사용 예시

### 예시 1: arXiv 논문
```
사용자: https://arxiv.org/abs/2301.12345 이 논문 구현해줘

Claude: 논문을 분석하고 코드로 변환하겠습니다.

[Phase 0: 참조 코드 검색 (선택적)...]
[Phase 1: 알고리즘 추출...]
[Phase 2: 개념 분석...]
[Phase 3: 구현 계획 수립...]
[Phase 4: 코드 생성...]
```

### 예시 2: PDF 파일
```
사용자: /home/user/papers/attention.pdf 이 논문의 알고리즘을 구현해줘
```

### 예시 3: 특정 부분만 요청
```
사용자: 이 논문에서 Section 3의 알고리즘만 구현해줘
```

---

## 관련 파일

- [01_algorithm_extraction.md](01_algorithm_extraction.md) - Phase 1: 알고리즘 추출
- [02_concept_analysis.md](02_concept_analysis.md) - Phase 2: 개념 분석
- [03_code_planning.md](03_code_planning.md) - Phase 3: 구현 계획
- [04_implementation_guide.md](04_implementation_guide.md) - Phase 4: 구현 가이드
- [05_reference_search.md](05_reference_search.md) - Phase 0: 참조 검색 (선택)
- [06_memory_management.md](06_memory_management.md) - 메모리 관리 가이드

---

## 주의사항

```
⚠️ REMEMBER:

1. 논문을 충분히 읽기: 전체 내용을 파악한 후 구현 시작
2. 중간 결과물 저장: 각 Phase의 YAML 출력을 파일로 저장
3. 점진적 구현: 한 번에 모든 코드를 생성하지 말고 파일별로 진행
4. 검증 포함: 가능하면 간단한 테스트 코드 포함
5. 참조는 영감: 참조 코드는 복사가 아닌 이해와 적용
```
