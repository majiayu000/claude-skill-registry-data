---
name: predeploy
description: 배포 전 종합 검증 - 테스트/린트/빌드/환경 설정을 자동 확인하여 배포 가능 여부 판단. 배포 전 또는 사용자가 "배포 가능한지 확인", "테스트 실행" 요청 시 사용.
---

# 배포 전 종합 검증 Skill

배포하기 전에 모든 필수 검증을 자동으로 수행하여 배포 가능 여부를 판단합니다.

## 사용 시점

다음과 같은 요청을 받았을 때 이 Skill을 사용하세요:
- "배포해도 될까?", "배포 가능한지 확인해줘"
- "테스트 실행", "검증해줘"
- "코드 품질 체크", "배포 준비 상태 확인"
- `deploy` Skill 실행 전 자동 호출

## 실행 단계

### Phase 1: Git 상태 확인

```bash
bash /home/donghee/bodam/.claude/skills/predeploy/scripts/check-git-status.sh
```

**검증 항목**:
- 현재 브랜치 확인 (wonuk/donghee)
- 커밋되지 않은 변경사항 확인
- 원격 브랜치와 동기화 상태 확인

**경고 조건**:
- ⚠️ Untracked files 존재
- ⚠️ Modified but not staged
- ❌ 원격보다 로컬이 뒤처짐 (배포 차단)

### Phase 2: Backend 검증

#### 2.1 코드 품질 검사
```bash
cd /home/donghee/bodam/backend

# Ruff 린트 검사
echo "🔍 Ruff 린트 검사..."
ruff check . --output-format=concise 2>&1 | head -50

# MyPy 타입 검사
echo "🔍 MyPy 타입 검사..."
mypy src --ignore-missing-imports --no-error-summary 2>&1 | head -50
```

**통과 조건**: 오류 없음 (경고는 허용)

#### 2.2 단위 테스트
```bash
echo "🧪 Backend 단위 테스트..."
pytest tests/unit/ -v --tb=line --no-header -q 2>&1
```

**통과 조건**: 모든 테스트 PASSED

#### 2.3 통합 테스트 (선택)
```bash
echo "🧪 Backend 통합 테스트..."
# Docker Compose로 테스트 환경 구성
docker compose -f docker-compose.dev.yml up -d postgres redis
sleep 5
pytest tests/integration/ -v --tb=line --no-header -q 2>&1
docker compose -f docker-compose.dev.yml down
```

**통과 조건**: 모든 테스트 PASSED (실패 시 경고)

### Phase 3: Frontend 검증

#### 3.1 코드 품질 검사
```bash
cd /home/donghee/bodam/frontend

# ESLint 검사
echo "🔍 ESLint 검사..."
npm run lint 2>&1 | head -50

# TypeScript 타입 검사
echo "🔍 TypeScript 타입 검사..."
npm run type-check 2>&1 | head -50
```

**통과 조건**: 오류 없음

#### 3.2 단위 테스트
```bash
echo "🧪 Frontend 단위 테스트..."
npm run test:unit -- --passWithNoTests --silent 2>&1 | tail -20
```

**통과 조건**: 모든 테스트 PASSED

#### 3.3 빌드 테스트
```bash
echo "🏗️ Production 빌드 테스트..."
NODE_ENV=production npm run build 2>&1 | tail -30
```

**검증 사항**:
- `.next` 디렉토리 생성 확인
- 빌드 에러 없음
- 빌드 크기 확인

### Phase 4: Infrastructure 검증

#### 4.1 K8s 매니페스트 검증
```bash
echo "☸️ Kubernetes 매니페스트 검증..."
bash /home/donghee/bodam/.claude/skills/predeploy/scripts/validate-k8s.sh
```

**통과 조건**: 모든 YAML 파일 문법 유효

#### 4.2 환경 변수 체크리스트

사용자에게 다음 Secrets이 GitHub에 설정되어 있는지 확인하도록 안내:

**Backend 필수**:
- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`
- `TOGETHER_AI_API_KEY`
- `ADMIN_SECRET_KEY`

**Frontend 필수**:
- `NEXT_PUBLIC_API_URL`
- `VERCEL_TOKEN`

**Infrastructure 필수**:
- `DIGITALOCEAN_TOKEN`
- `DIGITALOCEAN_CLUSTER_ID_PROD`
- `DIGITALOCEAN_CLUSTER_ID_PREVIEW`

### Phase 5: 데이터베이스 마이그레이션 확인

```bash
cd /home/donghee/bodam/backend
echo "🗄️ 데이터베이스 마이그레이션 확인..."
alembic current 2>&1 || echo "No alembic migrations"
alembic check 2>&1 || echo "No pending migrations"
```

사용자에게 질문:
- 새로운 마이그레이션이 있습니까?
- Breaking changes가 있습니까?
- 데이터 백업이 필요합니까?

## 검증 결과 리포트

검증 완료 후 다음 형식으로 결과를 사용자에게 보고하세요:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 배포 전 검증 결과
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 통과 항목 ({통과수}/전체수):
- Git 상태 확인
- Backend 코드 품질 (Ruff, MyPy)
- Backend 단위 테스트 (12개 통과)
- Frontend 코드 품질 (ESLint, TypeScript)
- Frontend 단위 테스트 (25개 통과)
- Frontend 빌드
- K8s 매니페스트 검증

⚠️ 경고 항목:
- 커밋되지 않은 변경사항 3개 (선택적 커밋 권장)
- Backend 통합 테스트 1개 실패 (배포 가능하지만 확인 필요)

❌ 실패 항목:
- (없음)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 배포 권고:
{권고 사항 - 아래 3가지 중 하나}

1. ✅ 배포 가능: 모든 검증 통과, 즉시 배포 가능합니다.
   → 다음 명령어로 배포하세요: (deploy 요청)

2. ⚠️ 주의 배포: 경고 사항을 검토한 후 배포하세요.
   → 경고 내용을 확인하고 필요시 수정 후 배포하세요.

3. ❌ 배포 불가: 실패 항목을 수정한 후 다시 검증하세요.
   → 오류를 수정한 후 다시 predeploy를 실행하세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 오류 수정 가이드

검증 실패 시 다음 자동 수정 방법을 제안하세요:

### Ruff 오류
```bash
cd backend
ruff check . --fix
```

### ESLint 오류
```bash
cd frontend
npm run lint --fix
```

### 타입 오류
- 사용자에게 오류 위치와 내용을 알려주고 수동 수정 필요

### 테스트 실패
- 실패한 테스트 로그를 출력하고 디버깅 지원

### 빌드 실패
- 빌드 로그에서 에러 부분 추출하여 출력
- 의존성 또는 설정 파일 확인 필요

## 검증 실행 옵션

사용자가 특정 검증만 실행하고 싶을 경우:

- **Git만**: Git 상태 확인 스크립트만 실행
- **Backend만**: Backend 검증 단계만 실행
- **Frontend만**: Frontend 검증 단계만 실행
- **빠른 검증**: 테스트 제외, 린트/타입 검사만
- **전체 검증**: 모든 단계 포함 (기본값)

## 참고 스크립트

- Git 상태 확인: `scripts/check-git-status.sh`
- K8s 매니페스트 검증: `scripts/validate-k8s.sh`

## 관련 Skills

- `deploy`: 검증 통과 후 실제 배포 실행
- `rollback`: 배포 실패 시 롤백
