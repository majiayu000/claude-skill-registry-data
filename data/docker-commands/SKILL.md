---
name: docker-commands
description: "ICJC Docker 서비스 관리 및 Make 명령어. Use when: (1) docker, make, 컨테이너, 서비스, 재시작, 로그 관련 요청, (2) 백엔드/프론트엔드/에이전트 재시작, (3) 빌드, 컨테이너 접속, 로그 확인, 서비스 상태 확인 필요시."
---

# Docker Commands Skill

ICJC 프로젝트의 Docker 서비스 관리를 위한 스킬입니다.

<trigger_conditions>
## 사용 시점

다음 키워드나 상황에서 이 스킬을 사용하세요:
- "docker", "make", "컨테이너", "서비스", "재시작", "로그"
- "백엔드 재시작", "프론트엔드 재시작", "빌드"
- "컨테이너 접속", "로그 확인", "서비스 상태"
</trigger_conditions>

<service_architecture>
## 서비스 아키텍처

**의존성 순서:** MongoDB (27017) → Redis (6379) → Backend (8000) → Agent Gateway (8100→8080) → Frontend (3000)

| 서비스 | 컨테이너명 | 외부포트 | 내부포트 | 설명 |
|--------|-----------|---------|---------|------|
| mongodb-primary | mongodb-primary-dev | 27017 | 27017 | MongoDB Atlas Local |
| redis | redis-dev | 6379 | 6379 | Redis 캐시 |
| backend | backend-dev | 8000 | 8000 | FastAPI 백엔드 |
| agent-multi-gateway | agent-multi-gateway-dev | 8100 | 8080 | AI Agent Gateway |
| frontend | frontend-dev | 3000 | 3000 | Next.js 프론트엔드 |
</service_architecture>

<commands>
## 명령어 레퍼런스

### 빠른 시작
| 명령어 | 설명 | 사용 시점 |
|--------|------|----------|
| `make build` | 전체 빌드 및 실행 | 첫 실행, 의존성 변경 |
| `make all` | 빌드 없이 실행 | 이미 빌드된 상태 |
| `make dev` | Docker Watch 개발 모드 | 개발 중 |

### 개별 서비스
| 명령어 | 설명 | 영향 범위 |
|--------|------|----------|
| `make backend` | 백엔드 + Agent 재시작 | DB/Frontend 유지 |
| `make frontend` | 프론트엔드 재시작 (dev) | Frontend만 |
| `make frontend-prod` | 프론트엔드 (prod) | Frontend만 |
| `make agent` | Agent Gateway만 실행 | Agent만 |
| `make agents` | 모든 Agent 재빌드 | Agent 전체 |
| `make agents-light` | 모든 Agent 재시작 (빌드X) | Agent 전체 |
| `make re-app` | 앱 컨테이너만 재시작 | DB 유지 |

### 로그
| 명령어 | 대상 |
|--------|------|
| `make logs` | 전체 |
| `make logs-backend` | 백엔드 |
| `make logs-frontend` | 프론트엔드 |
| `make logs-agent` | Agent Gateway |
| `make logs-mongo` | MongoDB 초기화 |
| `docker logs -f backend-dev` | 백엔드 (직접) |
| `docker logs -f --tail 100 frontend-dev` | 프론트엔드 최근 100줄 |

### 컨테이너 접근
| 명령어 | 대상 |
|--------|------|
| `docker exec -it backend-dev bash` | 백엔드 |
| `docker exec -it frontend-dev sh` | 프론트엔드 |
| `docker exec -it mongodb-primary-dev mongosh` | MongoDB |
| `docker exec -it agent-multi-gateway-dev bash` | Agent |

### 클린업
| 명령어 | 설명 | 주의 |
|--------|------|------|
| `make down` | 컨테이너 중지 + 볼륨 삭제 | 데이터 유지됨 |
| `make fclean` | down + 이미지/네트워크 정리 | |
| `make purge` | 모든 Docker 리소스 제거 | **매우 주의** |

### MongoDB 관리
| 명령어 | 설명 |
|--------|------|
| `make mongo` | MongoDB 레플리카셋 테스트 |
| `make mongo-reset` | MongoDB 완전 초기화 (데이터 삭제!) |
| `make mongo-backup-dev` | Dev DB 백업 |
| `make mongo-restore` | 백업 복원 |
| `make mongo-sync-dev` | 백업 → 복원 |
| `make mongo-rebuild` | 초기화 + 재시작 + 복원 |

### 문제 해결
| 명령어 | 설명 |
|--------|------|
| `make fix-permissions` | 파일 권한 문제 해결 |
| `make frontend-fix-next-perms` | .next 볼륨 권한 수정 |
| `make mem-watch` | 메모리 모니터링 |
</commands>

<environment_variables>
## 환경 변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| FRONTEND_MODE | development | 프론트엔드 모드 |
| USER_ID | $(id -u) | 컨테이너 사용자 ID |
| GROUP_ID | $(id -g) | 컨테이너 그룹 ID |

```bash
# 프로덕션 모드로 빌드
make build FRONTEND_MODE=production
```
</environment_variables>

<workflows>
## 일반적인 워크플로우

### 코드 변경 후 테스트
1. **백엔드 변경**: `make backend` (빠른 재시작)
2. **프론트엔드 변경**: Hot reload 자동 적용 (재시작 불필요)
3. **Agent 변경**: `make agents-light` (빌드 없이 재시작)
4. **의존성 변경**: `make build` (전체 재빌드)

### 문제 발생 시
1. 로그 확인: `make logs-backend` 또는 `make logs-frontend`
2. 컨테이너 상태: `docker ps`
3. 앱만 재시작: `make re-app`
4. 그래도 안되면: `make down && make build`

### 깨끗한 환경으로 시작
```bash
make fclean && make build
```
</workflows>

<instructions>
## 이 스킬 사용 시 지침

1. **명령어 실행 전 상황 파악**: 사용자가 원하는 작업을 정확히 이해하고, 최소한의 영향을 주는 명령어를 선택하세요.
2. **DB 보존 우선**: 가능하면 DB를 유지하는 명령어 (`make backend`, `make re-app`)를 먼저 시도하세요.
3. **로그 확인 습관화**: 서비스 재시작 후 반드시 로그를 확인하여 정상 동작을 검증하세요.
4. **purge 사용 주의**: `make purge`는 모든 Docker 리소스를 삭제합니다. 사용자에게 경고하세요.
</instructions>
