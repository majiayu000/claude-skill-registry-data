---
name: domain-dictionary
description: 도메인 용어 사전(Ubiquitous Language) 생성 및 일관성 검증. 코드/스펙/대화에서 용어 추출, 동의어/모호어/과부하 탐지, 영-한 매핑, 규범 용어 제안. /domain-dictionary 또는 "도메인사전", "용어사전", "도메인 용어" 트리거. zephermine에서 자동 호출됨.
---

# Domain Dictionary (도메인사전)

> Eric Evans의 *Domain-Driven Design* — Ubiquitous Language 개념을 한국 SI/현장의 영-한 혼용 환경에 맞게 적용.
> 한 프로젝트 안에서 **개발자, 도메인 전문가, 사업 담당자**가 같은 단어를 같은 뜻으로 쓰도록 강제하는 사전.

## 적용 시점

| 시점 | 진입점 |
|------|--------|
| 신규 기능 계획 시 | `zephermine`이 Spec Synthesis 직후 자동 호출 |
| 기존 코드베이스 분석 시 | `/domain-dictionary` 직접 호출 |
| 코드 리뷰 시 | `code-reviewer`가 `domain-dictionary.md` 위반을 검출 |
| 신규 멤버 온보딩 시 | `domain-dictionary.md` 한 장이 첫 자료 |

## 첫 실행 시 동작

스킬 첫 실행 시 글로벌 폴더를 자동 생성하고 `references/global-readme-template.md`를 README.md로 복사합니다. 기본 위치는 `~/.agent-memory/domain-dictionaries/`이며, `AGENT_DOMAIN_DICTIONARY_HOME` 환경 변수가 있으면 그 값을 우선합니다. 사용자가 `install.bat`/`install.sh`를 다시 실행하지 않아도 됩니다.

처음에는 글로벌 도메인 파일들이 비어있습니다(`ecommerce.md`, `healthcare.md` 등). 시간이 흐르면서 zephermine 컨텍스트 모드의 명확한 범용 용어 또는 사용자의 직접 선택으로 누적됩니다 — 의도된 설계.

## 질문 도구 호환성

CLI마다 질문 도구 스키마가 다릅니다. `Invalid tool parameters`를 피하기 위해 기본은 일반 텍스트 번호 목록입니다.

- zephermine 컨텍스트 모드에서는 질문하지 않는 것이 기본입니다. 충돌 용어가 DB/API/타입/UI/보안/정책을 바꿀 때만 한 질문씩 묻습니다.
- 직접 호출 모드(`/domain-dictionary`)에서는 사용자가 사전 점검을 요청한 것이므로 핵심 충돌이나 수정 후보를 물을 수 있습니다.
- 구조화 질문 도구는 짧은 단일/소수 선택에만 사용합니다.
- 한 번에 최대 3개 질문, 질문당 2-3개 짧은 선택지만 보냅니다.
- 다중 선택은 기본적으로 "1, 3, 5처럼 번호로 답해주세요" 방식으로 받습니다. 구조화 다중 선택 필드는 현재 CLI가 명시 지원할 때만 사용합니다.
- 도구 오류가 한 번 나면 같은 payload를 재시도하지 말고 일반 텍스트 질문으로 전환합니다.

## 사전의 두 종류 (글로벌 + 프로젝트)

| 종류 | 위치 | 역할 |
|------|------|------|
| **글로벌** | `~/.agent-memory/domain-dictionaries/{도메인}.md` | 사용자 자산 — 자주 다루는 도메인의 누적 용어 (참고용 씨앗) |
| **프로젝트** (마스터) | `<project>/docs/domain-dictionary.md` | **진실의 원천** — 이 프로젝트만의 확정 사전 |
| **프로젝트** (델타) | `<project>/docs/plan/{feature}/domain-dictionary-delta.md` | 이번 feature에서 추가/변경된 이력 (zephermine 산출물) |

### 글로벌 사전 폴더 구조

```
~/.agent-memory/domain-dictionaries/
├── README.md          ← 사용 안내 + 도메인 분류 가이드
├── ecommerce.md       ← Cart, Order, SKU, Fulfillment...
├── healthcare.md      ← Patient, Encounter, Diagnosis...
├── finance.md         ← Position, Settlement, Counterparty...
└── general.md         ← 도메인 무관 (User, Session, Audit...)
```

### 관계: 참고형 + 보수적 자동 채택

- 글로벌은 **씨앗만 제공**. zephermine 컨텍스트 모드에서는 명확히 맞는 후보만 자동 시드하고, 애매하면 가져오지 않습니다.
- 프로젝트 사전이 **최종 결정권자**. 글로벌과 다르게 정의해도 프로젝트가 우선.
- 프로젝트 변경의 글로벌 반영은 보수적으로 처리합니다. 명확히 범용인 용어만 출처 메타데이터와 함께 반영하고, 애매하면 `[inferred-skip]`로 기록합니다. 직접 호출 모드에서는 사용자 선택을 우선합니다.
- 자세한 동기화 절차: [global-sync.md](references/global-sync.md)

## 모드 결정

### 1. 컨텍스트 모드 (zephermine에서 자동 호출, Phase 2~3에서 진화)

| Phase | 사전 버전 | 동작 |
|-------|----------|------|
| Phase 2 (Step 8 끝) | v1 초안 | spec.md, interview.md + 글로벌 사전 후보에서 추출. 사용자 개입 없음 |
| Phase 3 (Step 10 끝) | v2 자동 병합 | 6개 전문가의 `## Dictionary Updates`를 자동 병합. CONFLICT는 미룸 |
| Phase 3 (Step 11 끝) | v3 확정 | 충돌만 확인 + 명확한 글로벌 반영 자동 처리, 애매하면 스킵 |

**산출 위치:**
- 마스터: `<project>/docs/domain-dictionary.md` (없으면 생성, 있으면 갱신)
- 델타: `<planning_dir>/domain-dictionary-delta.md` (이번 feature 변경 이력)

### 2. 코드베이스 모드 (직접 호출)
- 입력: 현재 작업 디렉토리의 코드, 기존 문서
- 출력: `<project>/docs/domain-dictionary.md` (마스터 직접 갱신)

### 3. 갱신 모드 (이미 마스터 사전이 있는 경우)
- 입력: 기존 마스터 + 새 변경사항
- 동작: 신규 용어 병합 (기존 항목 덮어쓰지 않음), 변경 이력에 행 추가
- 충돌 시 zephermine 컨텍스트 모드는 핵심 충돌만 질문하고, 직접 호출 모드는 사용자 확인

## 워크플로우

### Step 1: 후보 용어 수집

추출 알고리즘과 패턴은 [extraction-guide.md](references/extraction-guide.md) 참조.

**컨텍스트 모드:**
- spec.md, interview.md의 명사/동사 추출
- team-reviews/domain-* 의 도메인 용어 추출

**코드베이스 모드:**
- Glob/Grep으로 클래스/함수/타입/변수 식별자 추출
- 주석, UI 문자열 리터럴(메뉴/라벨)에서 한국어 용어 추출
- 기존 README, docs/*.md에서 용어 추출

### Step 2: 문제 패턴 탐지

| 문제 | 예시 | 처리 |
|------|------|------|
| **동의어** (같은 개념, 다른 단어) | `cart` / `basket` / `bag` | 하나로 통일 제안 |
| **이의어** (같은 단어, 다른 개념) | `Order` = "주문" or "정렬"? | 분리 (`Order` vs `SortOrder`) |
| **과부하** (한 단어가 너무 많은 의미) | `User` = 고객/관리자/판매자 | 분리 (`Customer` / `Admin` / `Seller`) |
| **영-한 불일치** | DB는 `user`, UI는 "고객" | 매핑 명시 또는 통일 |
| **약어 남용** | `usrCfg` (=userConfig?) | 풀어쓰기 권장 |
| **외래어 표기 흔들림** | "어카운트" / "계정" / "account" | 한 표기로 통일 |

### Step 3: 규범 용어 제안

각 핵심 개념마다 다음 형식으로 정리:

```markdown
## Cart (장바구니)
- **정의**: 사용자가 결제 전 임시로 모은 상품 목록
- **영문 식별자**: `cart` (변수, 클래스 prefix)
- **한글 표기**: 장바구니 (UI, 문서)
- **관련 개념**: CartItem (장바구니 항목), Wishlist (찜 — 구매 의도 없음, 다른 개념)
- **금지 표현**: ~~basket~~, ~~bag~~, ~~shopping_list~~
- **예시**:
  - ✅ `cart.addItem(item)`, "장바구니에 담기"
  - ❌ `basket.push(item)`, "쇼핑백 추가"
- **위치**: `src/cart/` 모듈 전체
```

### Step 4: 충돌 점검

**zephermine 컨텍스트 모드:** 핵심 용어(상위 5~10개)를 자동 확정하고, 충돌만 점검합니다. 사용자 질문은 DB/API/타입/UI/보안/정책을 바꿀 수 있는 충돌에 한정합니다. 나머지는 `accepted-by-default`, `inferred`, `inferred-skip`으로 델타에 기록하고 진행합니다.

**직접 호출 모드:** 사용자가 사전 점검을 요청한 것이므로 핵심 용어(상위 5~10개)를 일반 텍스트 번호 목록으로 확인할 수 있습니다. 구조화 다중 선택 UI는 현재 CLI가 명시 지원할 때만 사용하며, 이때 한 호출당 `options`는 2~4개만 사용합니다. 5개 이상이면 일반 텍스트 번호 목록으로 받거나 4개씩 분할하고, vendor-specific 질문 UI를 쓸 때는 그 런타임의 `header` 제한도 지킵니다.

```
"아래 용어 정의를 확인해주세요. 수정이 필요한 항목을 선택하세요."
header: "도메인사전"
selection: "multiple numbers by default; structured multiple-selection only if supported"
options:
  - label: "✅ Cart = 장바구니"
    description: "결제 전 임시 상품 목록. basket/bag 금지"
  - label: "✅ Wishlist = 찜"
    description: "구매 의도 없는 관심 상품. cart와 분리"
  ...
```

수정 요청 항목은 추가 질문으로 구체화. zephermine 컨텍스트 모드에서 사용자가 "알아서"라고 답하면 추천 기본값으로 진행합니다.

### Step 5: 출력 (마스터 + 델타 + 글로벌 반영)

**컨텍스트 모드 (zephermine 흐름)**:

1. **마스터 갱신**: `<project>/docs/domain-dictionary.md`
2. **델타 작성**: `<planning_dir>/domain-dictionary-delta.md` (이번 feature 변경 이력)
3. **글로벌 반영**: 명확히 범용인 항목만 `~/.agent-memory/domain-dictionaries/{도메인}.md`에 출처 메타데이터와 함께 추가. 애매하면 스킵 기록

**코드베이스 모드 (직접 호출)**: 마스터 직접 갱신만.

마스터 사전 형식:

```markdown
# Domain Dictionary

> 생성일: YYYY-MM-DD
> 도메인: {프로젝트명/기능명}
> 버전: v1.0
> 대상 청중: 개발자 + 도메인 전문가 + 사업 담당자

## 핵심 용어 (Core Terms)

{각 용어의 정의 + 영-한 매핑 + 예시}

## 관계도 (Optional — 5개 이상의 핵심 용어가 있을 때)

​```mermaid
graph TD
  Customer -->|places| Order
  Order -->|contains| OrderItem
  OrderItem -->|references| Product
​```

## 외부 표준 매핑 (해당 시)

| 용어 | 외부 표준 | 매핑 |
|------|-----------|------|
| Patient | HL7 FHIR `Patient` | 1:1 |
| Diagnosis | ICD-10 코드 | 다대일 |

## 금지 표현 모음

| 금지 | 대신 사용 | 이유 |
|------|-----------|------|
| basket, bag | cart | Cart로 통일 |
| user (고객 의미로) | customer | User는 시스템 사용자 일반 |

## 변경 이력

| 날짜 | 변경 | 이유 |
|------|------|------|
| YYYY-MM-DD | 초안 | 첫 작성 |
```

델타 파일 형식 (`<planning_dir>/domain-dictionary-delta.md`):

```markdown
# Domain Dictionary Delta — {feature-name}

> 생성일: YYYY-MM-DD
> 마스터 사전: docs/domain-dictionary.md
> 이 feature에서 추가/변경된 항목만 기록

## v1 → v2 (Step 10 자동 병합)
- ADD Wishlist (출처: Domain Researcher) — 찜 정의
- REFINE Order (출처: Process Expert) — 결제 시점 명확화

## v2 → v3 (Step 11 최종 확정)
- accepted-by-default: Wishlist 추가
- inferred: Order 다듬음 확정
- user-confirmed: Cart 채택, Basket 거부 (CONFLICT 해소)

## Global Dictionary Sync
- added: Wishlist → ~/.agent-memory/domain-dictionaries/ecommerce.md
- inferred-skip: FlashSale → 프로젝트 특수성으로 보류
```

### Step 6: 후속 안내

```
✅ 도메인사전 갱신 완료
   - 마스터: docs/domain-dictionary.md (v3, 핵심 용어 N개)
   - 델타: <planning_dir>/domain-dictionary-delta.md
   - 글로벌: ~/.agent-memory/domain-dictionaries/{도메인}.md (M개 추가)

다음 단계 (선택):
  zephermine 진행      → Step 12 Plan부터 사전 v3 따라 작성
  /argos               → 구현 후 사전 준수 감리
  코드 리뷰 시         → code-reviewer가 자동으로 위반 검출
```

## 갱신 모드 동작

기존 `domain-dictionary.md`가 있으면:

1. 기존 용어와 신규 용어를 비교
2. 신규 용어만 추가 (기존 항목 덮어쓰지 않음)
3. 충돌 시(같은 영문, 다른 정의) zephermine 컨텍스트 모드는 핵심 충돌만 질문하고, 직접 호출 모드는 사용자 확인
4. 변경 이력 표에 행 추가:
   ```markdown
   | 2026-04-28 | + Wishlist 추가 | 신규 기능 도입 |
   | 2026-04-28 | Cart 정의 정밀화 | 인터뷰에서 모호성 발견 |
   ```

## 제약

- **영-한 매핑이 핵심**: 한국 현장의 영-한 혼용을 명시적으로 처리
- **외부 표준 우선 검토**: 의료(FHIR/ICD-10), 금융(ISO 20022) 등 표준이 있으면 출발점으로 활용
- 용어 분쟁이 있으면 **사용자 결정 우선**. 단, zephermine 컨텍스트 모드는 비차단 분쟁을 `[inferred]`로 기록하고 계속 진행
- 한 번 결정된 규범 용어는 변경 시 반드시 변경 이력 기록 (이력 보존)
- 사전은 **살아있는 문서** — 기능이 추가되면 갱신, 새 멤버 온보딩 시 첫 자료
- **분량 제한**: 핵심 용어 30개 이내. 더 많아지면 BoundedContext별로 분할 (`domain-dictionary-{context}.md`)

## 다른 스킬과의 관계

| 스킬 | 관계 |
|------|------|
| `zephermine` | Spec Synthesis 직후 이 스킬을 자동 호출 |
| `code-reviewer` | maintainability specialist가 사전 위반을 검출 |
| `argos` | 감리 시 코드/문서가 사전을 따르는지 검증 |
| `database-schema-designer` | 테이블/컬럼명이 사전의 영문 식별자를 따름 |
| `clio` | 최종 문서 생성 시 사전을 참조하여 용어 일관성 확보 |

## Related Files

| 파일 | 용도 |
|------|------|
| `references/extraction-guide.md` | 용어 추출 알고리즘과 패턴 상세 |
| `references/global-sync.md` | 글로벌 사전 폴더 구조, 도메인 자동 추정, 동기화 절차 |
| `<project>/docs/domain-dictionary.md` | **마스터** 사전 (프로젝트 단일, 진실의 원천) |
| `<planning_dir>/domain-dictionary-delta.md` | 델타 — 이번 feature에서 추가/변경된 이력 |
| `~/.agent-memory/domain-dictionaries/{도메인}.md` | 글로벌 사전 — 사용자 자산, 명확한 범용 용어 또는 명시 선택으로만 추가됨 |
