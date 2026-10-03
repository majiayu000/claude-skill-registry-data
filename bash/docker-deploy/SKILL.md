---
name: docker-deploy
description: Docker 이미지 기반 배포 환경을 자동으로 구성합니다. /docker-deploy 명령으로 Dockerfile, docker-compose, install.bat 등 배포에 필요한 모든 파일을 생성합니다.
license: MIT
metadata:
  author: user
  version: "2.8.0"
---

# Docker Deploy Skill

Docker 이미지 기반 배포 파일을 자동 생성하는 스킬입니다.

## Skill Description

프로젝트의 Docker 배포 환경을 자동으로 구성합니다.

**Triggers:**
- `/docker-deploy` - 전체 Docker 배포 파일 생성
- `/docker-deploy build` - 이미지 빌드 스크립트만 생성
- `/docker-deploy install` - install.bat만 생성

**생성되는 파일:**
- `backend/Dockerfile` - Backend 멀티스테이지 빌드
- `frontend/Dockerfile` - Frontend 멀티스테이지 빌드
- `docker-build-images.bat` - 이미지 빌드 + tar 저장 스크립트
- `docker-images/docker-compose.yml` - 배포용 (pre-built 이미지)
- `docker-images/backup-entrypoint.sh` - DB 백업 스케줄/보관 스크립트 (선택)
- `docker-images/install.bat` - 처음 설치
- `docker-images/update.bat` - 이미지만 업데이트 (DB 유지)
- `docker-images/reset.bat` - 완전 초기화 (데이터 삭제)
- `docker-images/.env` - 환경변수 (기본값 포함)
- `.gitattributes` - 줄바꿈 정책 (`*.sh text eol=lf`)
- `docker-images/logs.bat` - 로그 보기
- `docker-images/seed-data.sql` - 초기 데이터 (선택)
- `deploy.bat` - Git Deploy Monitor 연동용 자동 배포 스크립트

---

## Instructions

### 1. 프로젝트 분석

먼저 프로젝트 구조를 분석합니다:
- backend/ 폴더 확인 - Python/FastAPI, Node.js 등
- frontend/ 폴더 확인 - React, Vue 등
- 기존 Dockerfile 확인
- 기존 docker-compose.yml 확인
- 데이터베이스 종류 확인 (MySQL, PostgreSQL 등)

### 2. 사용자에게 설정 질문

현재 CLI의 질문 방식으로 다음을 확인:

#### 2.1 포트 설정
- Frontend 포트 (기본: 8001) - 웹 브라우저 접속용
- Backend 포트 (기본: 9201) - Swagger, API 테스트용
- DB 포트 (기본: 3307) - DB 클라이언트 접속용

#### 2.2 데이터베이스
- MySQL (기본) / PostgreSQL / MariaDB

#### 2.3 테스트 계정
- 초기 테스트 계정 생성 여부

#### 2.4 DB 덤프 자동 추출
- 빌드 시 실행 중인 DB 컨테이너에서 full-dump.sql을 자동 추출할지 여부

---

### 3~4. Dockerfile 생성

> 상세 템플릿: [references/dockerfile-templates.md](references/dockerfile-templates.md)

- Backend: Python 멀티스테이지 (builder → production), non-root user
- Frontend: Node 빌드 → nginx 서빙, 정적 파일만 복사

### 5. docker-compose.yml 생성

> 상세 템플릿: [references/docker-compose-templates.md](references/docker-compose-templates.md)

- MySQL/PostgreSQL 선택에 따른 DB 서비스 설정
- healthcheck + depends_on condition으로 시작 순서 보장
- named volume 사용 (bind mount 금지)
- 운영 백업이 필요하면 `db-backup` 서비스 추가 (`postgres:alpine` + cron + `pg_dump|gzip`)

### 6~8. 배치 스크립트 생성

> 상세 템플릿: [references/batch-scripts.md](references/batch-scripts.md)

- install.bat: 이미지 로드 → 서비스 시작 → DB 초기화
- update.bat: DB 유지하며 이미지만 교체 + 마이그레이션
- reset.bat: 볼륨까지 삭제 후 재설치

### 9. .env 생성

```env
PROJECT_NAME=myapp
FRONTEND_PORT=8001
API_PORT=9201
DB_PORT=3307
DB_USER=root
DB_PASSWORD=password123
DB_NAME=app_db
SECRET_KEY=change-this-secret-key-in-production
```

---

## 핵심 포인트 (안정성)

### 1. Healthcheck는 단순하게
- MySQL: `mysqladmin ping` (테이블 쿼리 X)
- PostgreSQL: `pg_isready`
- **절대 SELECT 쿼리 사용 금지** (초기화 중 실패함)

### 2. depends_on + condition: service_healthy
- DB가 완전히 준비된 후 API 시작

### 3. start_period 설정
- MySQL은 초기화 시간이 길므로 `start_period: 30s` 권장

### 4. 통합/개별 tar 모두 지원
- 단일: `${PROJECT_NAME}-all.tar` (권장)
- 개별: `${PROJECT_NAME}-api.tar` + `${PROJECT_NAME}-frontend.tar`

### 5. 한국어 출력
- `chcp 65001` 로 UTF-8 설정 (배치 파일 첫 줄)

### 6. install/update/reset 분리
- `install.bat`: 처음 설치 (더블클릭)
- `update.bat`: DB 유지하며 이미지만 교체
- `reset.bat`: 볼륨까지 완전 삭제 후 재설치

### 7. Git Bash 경로 변환 주의 (Windows)
- Git Bash에서 `/api`가 `C:/Program Files/Git/api`로 변환됨
- 해결책: 환경변수를 따옴표로 감싸기 (`"VITE_API_URL="`)

### 8. SQL bind mount 사용 금지
- bind mount 삭제 시 컨테이너 재시작 실패
- 해결: `docker exec -i <컨테이너> mysql ... < seed-data.sql`

### 9. install.bat DB 대기 루프는 goto 사용
- `for /L` 안의 `!errorlevel!`은 불안정 → goto 기반 루프 필수

### 10. deploy.bat Self-Reload 패턴 (v3.0) 필수
- git pull 후 `call "%~f0" %1 --reloaded`로 자기 자신 재실행
- `--reloaded` 플래그로 무한 루프 방지

### 11. DB 상태 판단은 USER_COUNT 사용
- TABLE_COUNT 대신 USER_COUNT로 판단 (빈 테이블 오판 방지)

### 12. .deploy-mode는 .gitignore에 추가 필수

### 13. DB backup shell 스크립트는 LF 고정 (CRLF 금지)
- `docker-images/backup-entrypoint.sh` 같은 `.sh` 파일은 Linux 컨테이너에서 실행되므로 LF 필수
- CRLF가 섞이면 `/entrypoint.sh: line N: \r: not found`, `set: illegal option -`로 재시작 루프 발생
- 반드시 `.gitattributes`에 `*.sh text eol=lf` 추가
- 생성/수정 직후 `git ls-files --eol docker-images/backup-entrypoint.sh`로 `w/lf` 확인

---

## 16. deploy.bat (Git Deploy Monitor 연동)

> 상세 템플릿 + 전략 테이블: [references/deploy-bat-template.md](references/deploy-bat-template.md)

---

## 다음 단계 안내

배포 환경 생성이 완료되면 사용자에게 다음 단계를 안내합니다:

```
배포 환경 생성 완료!

산출물: Dockerfile, docker-compose.yml, install.bat/sh

다음 단계 (선택):
  ./install.bat        → 로컬에서 Docker 빌드 & 실행
  /write-api-docs      → API 문서 생성
  /commit              → 변경사항 커밋
  /wrap-up             → 세션 요약 + MEMORY.md 업데이트

참고: docs/workflow-guide.md
```
