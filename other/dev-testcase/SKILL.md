---
name: dev-testcase
description: >
  기능 개발을 위한 테스트 케이스 및 시나리오 문서를 작성한다.
  AI가 스펙의 인수 조건에서 테스트 케이스를 자동 도출하고, 사용자가 누락 여부와 AC 매핑을 검증한다.
  사용 시점: "테스트 케이스 만들어줘", "TC 작성해줘", "테스트 시나리오 정리해줘",
  "/dev-testcase {기능명}" 등 테스트 케이스 단계 요청 시 트리거.
  SPEC(docs/dev-process/SPEC.md)이 있으면 인수 조건에서 TC를 자동 도출한다.
---

# dev-testcase

기능 개발의 네 번째 단계로, 테스트 케이스와 검증 시나리오를 작성한다.
AI가 스펙의 인수 조건에서 TC를 자동 도출하고, 사용자가 누락 확인과 AC 매핑을 검증한다.

## Workflow

### 1. 선행 문서 분석

다음을 순서대로 확인한다:

1. `docs/dev-process/SPEC.md` — 구현 단위, 인수 조건, 비즈니스 규칙 파악
2. `docs/dev-process/PRD.md` — 사용자 시나리오, 요구사항 파악
3. `docs/dev-process/ARCHITECTURE.md` — 기술 스택(테스트 도구 결정에 활용)
4. 프로젝트의 기존 테스트 파일 탐색 — 테스트 패턴과 프레임워크 파악

선행 문서가 없으면 사용자에게 기능 설명, 주요 시나리오, 인수 조건을 직접 물어본다.

### 2. TC 자동 도출

스펙 문서의 인수 조건(AC)에서 테스트 케이스를 자동으로 도출한다:

- 각 AC마다 최소 1개의 정상 케이스(positive)
- 각 비즈니스 규칙마다 위반 케이스(negative)
- 유효성 검증 규칙에서 경계값 케이스(boundary)
- 에러 응답마다 에러 케이스

도출 결과를 AC-TC 매핑 테이블로 정리하여 사용자에게 보여준다.

### 3. 정보 수집 — 1차 질문 (갭 분석)

자동 도출 결과를 보여준 뒤:

- 누락된 테스트 시나리오가 있는가?
- 특별히 중점적으로 테스트해야 할 영역은?
- 수동 테스트가 필요한 항목은? (자동화가 어려운 것)

### 4. 정보 수집 — 2차 질문 (테스트 환경)

- 테스트 데이터 준비 방식은? (fixture, seed, mock 등)
- 외부 의존성 처리 방식은? (mock, stub, test container 등)
- E2E 테스트 범위는 어디까지인가?

### 5. 테스트 문서 작성

[references/testcase-template.md](references/testcase-template.md) 형식에 맞춰 테스트 문서를 작성한다.

작성 원칙:
- 모든 AC가 최소 1개 TC에 매핑되어야 한다 (AC-TC 추적 매트릭스)
- 각 TC는 전제조건, 입력, 기대결과가 명확해야 한다
- 자동화 가능 여부를 명시한다
- 우선순위를 표기한다 (P0: 필수, P1: 중요, P2: 권장)
- 수동 확인 항목을 별도 섹션으로 분리한다

### 6. 리뷰 및 확정

초안을 사용자에게 보여주고:
- AC-TC 매핑의 완전성 확인
- 테스트 데이터의 현실성 확인
- 수동 체크 항목의 적절성 확인

피드백을 반영하여 확정한다.

### 7. Output

`docs/dev-process/TESTCASE.md`에 저장한다.
파일 저장 후 한 줄 요약과 함께 전체 프로세스 완료를 안내한다.
4개 문서의 요약 목록을 보여준다:
- docs/dev-process/PRD.md
- docs/dev-process/ARCHITECTURE.md
- docs/dev-process/SPEC.md
- docs/dev-process/TESTCASE.md
