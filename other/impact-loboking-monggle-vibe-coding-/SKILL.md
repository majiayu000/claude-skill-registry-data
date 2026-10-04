---
name: monggle-impact
version: 1.0.0
description: |
  Impact analysis - Find side effects and cascading issues before modifying code (monggle)
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - /impact
  - /side-effect
  - monggle impact
---

# impact (monggle)

## 목적

수정 전에 **사이드 이펙트**와 **연쇄 이슈**를 미리 파악하여, 수정 후 다른 곳에서 문제가 발생하는 상황을 방지합니다.

## 실행 프로세스

```
1. 타겟 식별 (함수/파일/diff)
2. 직접 의존성 스캔 (imports, function calls)
3. 간접 의존성 추적 (shared state, API contracts)
4. 리스크 등급 평가
5. 연쇄 이슈 예측
6. 수정 체크리스트 생성
```

## 단계별 가이드

### 1단계: 타겟 식별

사용자 입력에서 분석 대상을 파악:

| 입력 | 타겟 |
|-----|------|
| `/impact UserService.login` | `UserService.login` 함수/메서드 |
| `/impact src/api/auth.ts` | `src/api/auth.ts` 파일 |
| `/impact` | 현재 작업 디렉토리 |
| `/impact --diff HEAD~1` | Git diff |

### 2단계: 직접 의존성 스캔

**Grep으로 찾을 것:**
1. **Import/Require**: 타겟을 import하는 파일
2. **Function Calls**: 타겟을 호출하는 곳
3. **Type References**: 타겟을 타입으로 사용하는 곳

```bash
# 예: UserService.login 분석 시
grep -r "UserService" --include="*.ts" --include="*.js" .
grep -r "login" --include="*.ts" --include="*.js" . | grep -i "user"
```

### 3단계: 간접 의존성 추적

**찾을 간접 의존성:**
1. **Shared State**: 같은 state/store를 사용하는 곳
2. **Database Schema**: 같은 테이블을 조회하는 곳
3. **API Endpoints**: 같은 API를 호출하는 곳
4. **Environment Variables**: 같은 env var를 사용하는 곳

```bash
# 예: shared state 찾기
grep -r "useAuth\|authStore\|AuthContext" --include="*.ts" --include="*.tsx" .
```

### 4단계: 리스크 등급 평가

| 등급 | 조건 | 색상 |
|-----|------|------|
| 🔴 高危 | - DB 스키마 변경<br>- 공유 상태 변경<br>- API 계약 변경<br>- 인증/권한 관련 | RED |
| 🟡 中 | - UI 변경<br>- 로직 변경<br>- 함수 시그니처 변경 | YELLOW |
| 🟢 低 | - 내부 리팩토링<br>- 주석 변경<br>- 포맷 변경 | GREEN |

### 5단계: 연쇄 이슈 예측

**분석 흐름:**
```
A 변경 → B 영향 → C 영향 → D 문제 발생?
```

**예시:**
```
UserService.login 반환 타입 변경
  ↓
AuthContext.ts 타입 불일치
  ↓
LoginPage.ts 컴파일 에러
  ↓
Dashboard.ts (AuthContext 사용) 런타임 에러
```

### 6단계: 수정 체크리스트

출력 형식:

```markdown
## 📊 영향도 분석 보고

### 📍 직접 의존성 (N건)
- `src/components/LoginForm.ts` (line 15)
- `src/pages/AuthPage.tsx` (line 42)

### 🔗 간접 의존성 (N건)
- `src/context/AuthContext.ts` (동일 state 사용)

### ⚠️ 리스크 등급: 🟡 中

### 📊 연쇄 이슈 예측
1. `login()` 반환 타입 변경 → `AuthContext` 타입 불일치
2. → `LoginForm` 컴포넌트 props 불일치
3. → **런타임 에러 가능성**

### 📋 수정 체크리스트
- [ ] `src/context/AuthContext.ts` 타입 업데이트
- [ ] `src/components/LoginForm.ts` props 업데이트
- [ ] `src/pages/AuthPage.tsx` 사용 코드 확인
- [ ] 테스트: 로그인 흐름 확인
- [ ] 테스트: 인증 후 페이지 이동 확인
```

## --deep 모드 (Agent)

`--deep` 플래그가 있으면 Agent를 사용하여 심층 분석:

1. 전체 코드베이스 스캔
2. 호출 그래프 생성
3. 데이터 흐름 추적
4. 테스트 커버리지 확인

```bash
# Agent 사용 시
/impact --deep UserService.login
```

## 예시 시나리오

### 시나리오 1: 함수 수정

```
입력: /impact UserService.login

분석:
1. UserService.login 정의 확인
2. login 함수 호출하는 곳 모두 찾기
3. login 함수가 사용하는 의존성 확인
4. login 반환값을 사용하는 곳 확인
5. 연쇄 영향도 평가

출력: 위 체크리스트 형식
```

### 시나리오 2: 파일 수정

```
입력: /impact src/api/auth.ts

분석:
1. auth.ts에서 export하는 것 확인
2. auth.ts를 import하는 파일 모두 찾기
3. 각 import 사용처 분석
4. 연쇄 영향도 평가

출력: 파일별 영향도 리스트
```

### 시나리오 3: Diff 분석

```
입력: /impact --diff HEAD~1

분석:
1. git diff로 변경된 파일/함수 추출
2. 각 변경별 영향도 분석
3. 종합 리스크 평가

출력: 변경별 영향도 + 종합 리포트
```

## 주의사항

1. **의존성 누락 방지**: 직접/간접 모두 확인
2. **보수적 예측**: "가능성 있음"을 "위험"으로 분류
3. **구체적 파일명**: "어떤 파일"을 명확히 제시
4. **라인 번호 포함**: 정확한 위치 안내

## 출력 템플릿

```markdown
# 📊 영향도 분석

**타겟**: `{target}`
**분석 시간**: `{timestamp}`

---

## 📍 직접 의존성 ({count}건)

| 파일 | 라인 | 용도 |
|-----|------|------|
| `path/to/file.ts` | 15 | import |
| `path/to/another.ts` | 42 | function call |

---

## 🔗 간접 의존성 ({count}건)

| 파일 | 라인 | 연결 유형 |
|-----|------|----------|
| `path/to/context.ts` | - | shared state |
| `path/to/config.ts` | 10 | same env var |

---

## ⚠️ 리스크 등급: {badge} {level}

**사유**: {reason}

---

## 📊 연쇄 이슈 예측

```
{ascii graph}
```

**경로**: {path_description}

---

## 📋 수정 체크리스트

### 우선순위 순서

1. [ ] `{file}` - {task}
2. [ ] `{file}` - {task}
...

### 검증 항목

- [ ] {test_case}
- [ ] {test_case}
```
