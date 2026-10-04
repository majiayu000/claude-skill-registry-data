---
name: code-reviewer
description: >
  코드를 붙여넣으면 보안·성능·설계·가독성을 종합 리뷰하고 심각도별 분류와 Before/After 개선 코드를
  PR 코멘트 형식으로 제공하는 스킬입니다. 복잡도 수치·리팩토링 분석은 complexity-analyzer 참조.
  키워드: "코드 리뷰", "PR 리뷰", "보안 취약점", "성능 문제", "코드 품질", "N+1 쿼리", "XSS",
  "SQL Injection", "CORS", "SOLID", "Java", "TypeScript", "Python", "Node.js", "Dart", "Flutter"
---

# Code Reviewer 스킬

코드를 붙여넣으면 **보안 → 성능 → 설계 → 가독성** 순으로 검토 후
심각도 분류 + Before/After 개선 코드 + PR 코멘트 형식으로 제공합니다.

---

## 작동 흐름

```
1. 코드 입력 접수
         ↓
2. 기술 스택 감지 (Java / TypeScript / SQL / Python / Node.js / Dart)
         ↓
3. 체크리스트 기반 자동 분석
   ├─ 🔵 설계   → references/design-review.md     (항상 로드)
   ├─ ⚪ 가독성  → references/readability-review.md (항상 로드)
   ├─ 📝 PR형식  → references/pr-comment-format.md  (항상 로드)
   ├─ 🔴 보안   → references/security-review.md    (조건부)
   └─ 🟡 성능   → references/performance-review.md  (조건부)
         ↓
4. 심각도 분류 & 우선순위 정렬
         ↓
5. Before/After 개선 코드 제시
         ↓
6. PR 리뷰 코멘트 형식 출력
```

### 레퍼런스 로드 기준

| 레퍼런스 | 로드 조건 | 트리거 키워드/패턴 |
|---------|----------|-----------------|
| `references/design-review.md` | **항상 로드** | 모든 리뷰의 기본 체크리스트 |
| `references/readability-review.md` | **항상 로드** | 모든 리뷰의 기본 체크리스트 |
| `references/pr-comment-format.md` | **항상 로드** | PR 코멘트 출력 형식 |
| `references/security-review.md` | **조건부** — 아래 키워드 감지 시 Read 도구로 로드 | `password`, `secret`, `token`, `auth`, `login`, SQL 문자열 연결, `innerHTML`, `dangerouslySetInnerHTML`, `permitAll`, `BeanUtils.copyProperties`, 파일 경로 입력 처리 |
| `references/performance-review.md` | **조건부** — 아래 키워드 감지 시 Read 도구로 로드 | `findAll()` 루프 내 호출, `.get()` 반복, stream 다중 순회, `@Cacheable` 미사용, 페이지네이션 없는 전체 조회, `useMemo`/`useCallback` 미사용, N+1, 대량 데이터 처리 |

---

## 심각도 분류 기준

| 등급 | 기호 | 기준 | 머지 가능 여부 |
|------|------|------|-------------|
| **Critical** | 🔴 | 보안 취약점, 데이터 손실 위험, 운영 장애 | ❌ 즉시 수정 필요 |
| **Major** | 🟡 | 성능 저하, 설계 원칙 위반, 잠재적 버그 | ⚠️ 수정 권고 |
| **Minor** | 🟢 | 가독성, 네이밍, 스타일 | ✅ 선택적 수정 |
| **Nitpick** | 💬 | 취향 차이, 개인 선호 | ✅ 논의 가능 |

---

## 기술 스택별 분기

감지된 스택에 해당하는 레퍼런스를 Read 도구로 로드한다. 공통 체크리스트는 항상 함께 로드한다.

| 스택 | 레퍼런스 파일 |
|------|-------------|
| Java / Spring Boot | `references/stack-java.md` + `references/stack-common.md` |
| TypeScript / React | `references/stack-typescript.md` + `references/stack-common.md` |
| SQL / QueryDSL | `references/stack-sql.md` + `references/stack-common.md` |
| Python / FastAPI | `references/stack-python.md` + `references/stack-common.md` |
| Node.js / NestJS | `references/stack-nodejs.md` + `references/stack-common.md` |
| Dart / Flutter | `references/stack-dart.md` + `references/stack-common.md` |

---

## 리뷰 응답 형식

```
## 📊 리뷰 요약
[발견된 이슈 수: Critical N / Major N / Minor N]

## 🔴 Critical (즉시 수정)
### [이슈 제목]
**위치**: [파일명:라인]
**문제**: [문제 설명]
**Before / After**
[코드]

## 🟡 Major (수정 권고)
...

## 🟢 Minor (선택적)
...

## 💬 PR 코멘트 (복사용)
[GitHub PR 코멘트 형식으로 출력]

## ✅ 잘된 점
[긍정적 피드백]
```

---

## 리뷰 핵심 원칙

- **Critical 없으면 머지 가능** — 완벽함보다 배포 가능 기준 명확히
- **이유 설명 필수** — "이렇게 바꾸세요" 가 아닌 "왜" 포함
- **대안 제시** — 문제 지적만이 아닌 개선 코드 제공
- **긍정 피드백 포함** — 잘된 부분도 명시
- **질문 형식 허용** — 확신 없으면 "이 부분은 의도가 ~인가요?" 형식
- **영역 구분** — 복잡도 측정·SOLID 위반·리팩토링 중심 분석이 필요하면 → complexity-analyzer 스킬 참조
