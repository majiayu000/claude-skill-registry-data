---
name: claude-guide
description: Guides Claude Code setup and configuration. Use when setting up CLAUDE.md, rules, hooks, or skills structure for projects.
invocable: true
invocable_description: Reviews and refactors existing CLAUDE.md. Run to analyze memory structure and extract reusable patterns to skills.
---

# Claude Guide

Claude Code 설정 구조를 안내하고, 프로젝트별 CLAUDE.md를 리뷰합니다.

## 설정 유형 선택 가이드

Claude Code는 다양한 설정 방식을 제공합니다. **컨텍스트 소비 최소화**를 위해 적절한 유형을 선택하세요.

| 유형 | 로드 시점 | 용도 |
|------|----------|------|
| CLAUDE.md | 항상 | 핵심 규칙, 필수 설정 |
| rules/ | 자동 로드 (paths 지정 시 해당 경로만) | 상세 규칙 분리 (20줄+ 시) |
| hooks/ | 이벤트 시 | 도구 호출 전후 자동 실행 |
| commands/ | 호출 시만 | 반복 작업 템플릿 (/auto-dev) |
| skills/ | 필요 시만 | 전문 지식 패키지 (drawio) |
| agents/ | 위임 시만 | 독립 컨텍스트 작업 (code-review) |

### 어디에 넣을까?

**CLAUDE.md**: 커밋 규칙, 테스트 정책, 금지 사항 (항상 적용되어야 할 것)
**rules/**: 상세 규칙 (20줄+), 영역별 분리 (frontend/, backend/)
**hooks/**: 도구 호출 전후 자동화 (pre-Bash, post-Edit 등)
**commands/**: 반복 워크플로우 (/review, /deploy, /docs)
**skills/**: 특정 주제 전문 지식 (항상 필요하지 않은 것)
**agents/**: 독립 컨텍스트 필요한 작업 (코드 리뷰, 탐색)

---

## Memory 계층 구조

Claude Code는 여러 위치에서 메모리를 로드합니다. **위에서 아래로 우선순위**가 높습니다.

| 우선순위 | 유형 | 위치 | 공유 범위 |
|:---:|------|------|----------|
| 1 | Enterprise policy | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br>Linux: `/etc/claude-code/CLAUDE.md`<br>Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | 조직 전체 |
| 2 | User memory | `~/.claude/CLAUDE.md` | 개인 (모든 프로젝트) |
| 3 | Project memory | `./CLAUDE.md` 또는 `./.claude/CLAUDE.md` | 팀 (소스 컨트롤) |
| 4 | Project rules | `./.claude/rules/*.md` | 팀 (소스 컨트롤) |
| 5 | Project local | `./CLAUDE.local.md` | 개인 (현재 프로젝트만) |

**동작 방식**: cwd에서 루트까지 재귀적으로 탐색하며 모든 `CLAUDE.md`, `CLAUDE.local.md` 로드

> `CLAUDE.local.md`는 자동으로 `.gitignore`에 추가됨

### @ Import 문법

다른 파일을 import할 수 있습니다:

```markdown
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
- 개인 설정 @~/.claude/my-project-instructions.md
```

- 상대/절대 경로 모두 지원
- 최대 5단계 재귀 import
- 코드 블록 내에서는 평가되지 않음

### Path-Specific Rules

`.claude/rules/` 내 파일에 YAML frontmatter로 특정 경로에만 적용:

```markdown
---
paths: src/api/**/*.ts
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
```

**Glob 패턴 예시**:
- `**/*.ts`: 모든 TypeScript 파일
- `src/**/*`: src/ 하위 모든 파일
- `src/components/*.tsx`: 특정 디렉토리만
- `{src,lib}/**/*.ts`: 여러 디렉토리

### Memory 명령어

```bash
/init    # CLAUDE.md 생성
/memory  # 로드된 memory 파일 확인
```

> 공식 문서: https://code.claude.com/docs/en/memory

---

## CLAUDE.md 리뷰

프로젝트별 CLAUDE.md를 리뷰하고 정리합니다.

**핵심 목표**:
- 프로젝트 고유 정보만 간결하게 유지 (토큰 효율성 우선)
- 범용 패턴은 Skills로 분리
- 필수 항목 누락 방지
- 정해진 형식 없음, 간결하고 읽기 쉽게
- 실제 문제 해결 중심

## Instructions

### 워크플로우: 기존 claude.md 리뷰

#### 1. 파일 확인

```bash
# 현재 디렉토리 확인
pwd

# claude.md 찾기
ls claude.md 2>/dev/null || ls CLAUDE.md 2>/dev/null
```

**있으면**: 리뷰 시작
**없으면**: 생성 제안 (templates/ 참조)

#### 2. Read 및 분석

```
Read claude.md (또는 CLAUDE.md)
```

**분석 항목**:

1. **컨텍스트 효율성 체크**
   - 간결하고 핵심만: ✅ 적절
   - 다소 장황함: ⚠️ 약간 김
   - 범용 내용 많음: ❌ Skills 분리 필요

2. **Skills로 분리할 내용 감지**

   키워드 패턴으로 감지:
   - "TypeScript", "타입", "컨벤션", "린팅" → patterns-typescript
   - "React", "컴포넌트", "hooks", "상태 관리" → patterns-react
   - "API 설계", "엔드포인트", "RESTful" → patterns-api
   - "테스트", "유닛", "E2E", "mocking" → test-guidelines
   - "에러 핸들링", "try-catch", "로깅" → patterns-error-handling

   **판단 기준**:
   - 해당 섹션이 20줄 이상
   - 프로젝트 독립적인 범용 내용
   - 다른 프로젝트에도 적용 가능

3. **필수 항목 체크**

   - [ ] 프로젝트 개요 (1-2줄 설명)
   - [ ] 퀵 커맨드 (build, test, dev, deploy 등)
   - [ ] 서비스 엔드포인트/포트
   - [ ] 환경변수 필수 항목
   - [ ] 프로젝트 특이사항/주의사항

#### 3. 리포트 생성

사용자에게 분석 결과 요약:

```markdown
## 📊 claude.md 리뷰 결과

### 전체 현황
- 총 라인: XXX줄
- 상태: ✅ 간결하고 적절 / ⚠️ 약간 김 / ❌ 분리 필요

### Skills로 분리 권장 (총 YYY줄)
1. TypeScript 컨벤션 (50줄) → patterns-typescript
2. React 패턴 (80줄) → patterns-react
3. 테스트 가이드 (40줄) → test-guidelines

### 필수 항목 누락
- [ ] 퀵 커맨드
- [ ] 서비스 엔드포인트

### 적절한 내용
- [x] 프로젝트별 quirks
- [x] 특정 서비스 설정
```

#### 4. 사용자 확인

개선 방향 선택지 제시:

**[1] Skills 분리 + 정리**
- 범용 내용을 skills로 분리
- 프로젝트 고유 정보만 남김
- 누락된 필수 항목 추가

**[2] 정리만 (분리 없이)**
- 현재 구조 유지
- 포맷만 정리

**[3] 새로 작성**
- 기존 내용 참고하여 템플릿 기반 재작성

#### 5. 개선 실행

**[1] Skills 분리 선택 시**:

1. 각 분리 대상마다 확인:
   ```
   "TypeScript 컨벤션(50줄)을 patterns-typescript skill로 분리하시겠습니까?"
   → Yes: 새 skill 생성
   → No: claude.md에 유지
   ```

2. 새 skill 생성:
   ```bash
   mkdir -p skills/patterns-{name}/
   Write skills/patterns-{name}/SKILL.md
   ```

3. claude.md에서 해당 섹션 제거

4. claude.md에 skill 참조 추가:
   ```markdown
   ## 코딩 가이드
   - TypeScript: `patterns-typescript` skill 참조
   - React: `patterns-react` skill 참조
   ```

**[2] 정리만 선택 시**:

- 포맷 정리
- 섹션 재배치
- 필수 항목 추가

**[3] 새로 작성 선택 시**:

1. 프로젝트 유형 확인:
   - Web App (Next.js, React 등)
   - API Server (Express, Fastify 등)
   - Monorepo (Turborepo, Nx 등)
   - Minimal (기본)

2. 적절한 템플릿 선택 (`templates/{유형}.md`)

3. 사용자와 대화하며 커스터마이징:
   - "프로젝트명은?"
   - "빌드 명령어는?"
   - "개발 서버 포트는?"
   - "특별한 주의사항은?"

4. claude.md 생성

#### 6. 검증

정리 후 재확인:

- 간결한가?
- 필수 항목 모두 포함?
- Skills 참조 명확?

## 포함/제외 기준

### ✅ claude.md에 포함할 것

**프로젝트 고유 정보:**
- 프로젝트 개요 및 목적
- 빌드/테스트/배포 명령어
- 서비스 엔드포인트 및 포트
- 환경변수 필수 항목
- 인증/테스팅 워크플로우 (프로젝트 특화)
- 프로젝트별 quirks 및 주의사항
- 특정 서비스 설정 (Redis, DB 등)
- 프로젝트 특화 트러블슈팅

**예시:**
```markdown
# MyApp

웹 기반 사용자 관리 시스템

## 퀵 커맨드
- Build: `npm run build`
- Dev: `npm run dev` (http://localhost:3000)
- Test: `npm test`
- Deploy: `./scripts/deploy.sh`

## 서비스
- API: http://localhost:3000/api
- Admin: http://localhost:3001
- Redis: localhost:6379

## 환경변수 필수
- DATABASE_URL
- REDIS_URL
- JWT_SECRET

## 주의사항
- DB 마이그레이션은 항상 백업 후 실행
- Redis는 개발 시 docker compose로 자동 실행
```

### ❌ Skills로 분리할 것

**범용 패턴 및 가이드:**
- 언어별 컨벤션 (TypeScript, Python 등)
- 프레임워크 패턴 (React, Vue, Express 등)
- API 설계 원칙 (RESTful, GraphQL)
- 테스트 작성 가이드
- 에러 핸들링 패턴
- 데이터베이스 설계 원칙
- 성능 최적화 기법

**분리 대상 skill 매핑:**
- TypeScript 컨벤션 → `patterns-typescript`
- React 패턴 → `patterns-react`
- Backend 아키텍처 → `patterns-backend`
- API 설계 → `patterns-api`
- 테스트 가이드 → `test-guidelines`
- 에러 핸들링 → `patterns-error-handling`
- 보안 → `review-security`

---

## 대규모 프로젝트 CLAUDE.md

대규모 엔터프라이즈 프로젝트는 일반 권장 범위를 초과할 수 있습니다.

### 언제 200줄+ CLAUDE.md가 필요한가?

- 프로젝트 고유 규칙이 많은 경우 (REST API 표준, 로깅 표준, i18n 등)
- DDD 같은 복잡한 아키텍처를 사용하는 경우
- 규제 준수 요구사항이 있는 경우 (금융, 의료 등)
- 체크리스트가 필요한 경우 (새 Controller, 새 Service 등)

### 대규모 프로젝트 권장 섹션

```markdown
1. Project Overview        # 프로젝트 개요
2. Quick Commands          # 개발 명령어
3. Services                # 서비스 엔드포인트
4. Environment Variables   # 환경변수
5. Architecture            # 아키텍처 가이드라인 (패키지 구조, 계층 의존성)
6. REST API Standards      # API 응답 패턴, 로깅 표준
7. Internationalization    # i18n 메시지 사용법
8. Swagger Documentation   # API 문서화 규칙
9. Checklists              # 체크리스트 (새 컨트롤러, 새 서비스, PR)
10. Testing Strategy       # 테스트 전략, 디렉토리 구조
11. Troubleshooting        # 자주 발생하는 문제 해결
12. References             # 상세 문서 링크
```

### 코드 예시 패턴 (✅/❌)

올바른 방법과 잘못된 방법을 대비하여 명확하게 가이드:

```java
// ✅ 올바른 패턴: ApiResult 래퍼 사용
@PostMapping
public ResponseEntity<ApiResult<UserResponse>> createUser(...) {
    return ResponseEntity.status(HttpStatus.CREATED)
        .body(ApiResult.success(response, message));
}

// ❌ 잘못된 패턴: ApiResult 없이 직접 반환
@GetMapping
public ResponseEntity<List<UserResponse>> getUsers() {
    return ResponseEntity.ok(service.getAll());  // 이렇게 하지 마세요
}
```

**효과**: AI가 명확한 패턴을 학습하여 일관된 코드 생성

### 체크리스트 패턴

새 기능 구현 시 빠뜨리기 쉬운 사항을 명시적으로 나열:

```markdown
### New Controller Checklist

- [ ] **ApiResult 패턴 적용**: 모든 엔드포인트가 `ResponseEntity<ApiResult<T>>` 반환
- [ ] **MessageSourceService 주입**: 다국어 메시지 처리를 위해 필수
- [ ] **Swagger 문서화**: `@Tag`, `@Operation`, `@ApiResponses` 어노테이션 추가
- [ ] **로깅 표준 준수**: GET은 `debug`, POST/PUT/DELETE는 `info` 레벨
- [ ] **메시지 파일 업데이트**: messages_ko.properties에 메시지 키 추가
```

**효과**: AI가 코드 생성 후 자체 검증 가능

### 템플릿

대규모 프로젝트용 템플릿: `templates/enterprise.md`

## 체크리스트

### 필수 항목
- [ ] 프로젝트 개요 (1-2줄)
- [ ] 퀵 커맨드 (build, test, dev)
- [ ] 서비스 엔드포인트/포트
- [ ] 환경변수 필수 항목

### 품질
- [ ] 간결하게 유지
- [ ] Skills 참조 명확
- [ ] 프로젝트 고유 정보만
- [ ] 섹션 구조 명확

### Skills 분리
- [ ] 코딩 컨벤션 (> 20줄) 분리
- [ ] 프레임워크 패턴 분리
- [ ] 범용 가이드 분리

## 예시

### 예시 1: 리뷰 후 Skills 분리

User: "claude.md 리뷰해줘"
Assistant:
1. Read claude.md (250줄)
2. 분석:
   - TypeScript 컨벤션 (60줄) → patterns-typescript
   - React 패턴 (70줄) → patterns-react
   - 퀵 커맨드 누락
3. 리포트 제시
4. 사용자 승인
5. 실행:
   - skills/patterns-typescript/ 생성
   - skills/patterns-react/ 생성
   - claude.md에서 해당 섹션 제거
   - 퀵 커맨드 추가
6. 결과: 80줄의 깔끔한 claude.md

### 예시 2: 새로 작성

User: "claude.md 만들어줘"
Assistant:
1. 프로젝트 유형 확인
2. templates/web-app.md 선택
3. 커스터마이징
4. claude.md 생성

## Technical Details

템플릿은 `templates/` 디렉토리 참조:
- minimal.md: 최소 구성
- web-app.md: 웹앱 프로젝트
- api-server.md: API 서버
- monorepo.md: 모노레포
- enterprise.md: 엔터프라이즈 프로젝트 (DDD, 규제 준수)
