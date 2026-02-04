---
name: dokploy-skill
description: |
  Dokploy 셀프호스팅 PaaS 플랫폼의 전체 관리 스킬. SSH 및 API를 통한 서버 관리,
  애플리케이션 배포, Docker Compose/Swarm 관리, 데이터베이스(PostgreSQL, MySQL, MongoDB, Redis) 관리,
  Traefik 리버스 프록시 설정, SSL 인증서(Let's Encrypt, Cloudflare Origin CA), 도메인 설정,
  볼륨 백업/복원, 컨테이너 모니터링, 서버 문제 해결 및 디버깅을 지원합니다.

  이 스킬 사용 시점:
  (1) "Dokploy", "dokploy" 언급 시
  (2) 애플리케이션 배포/재배포 요청
  (3) Docker Compose 또는 Swarm 관련 작업
  (4) 도메인 설정, SSL 인증서, HTTPS 설정
  (5) Traefik 설정 확인/수정, 502 에러, 도메인 접속 문제
  (6) 데이터베이스 생성, 백업, 복원
  (7) 볼륨 백업/복원, S3 연동
  (8) 컨테이너 로그 확인, 서버 상태 점검
  (9) 서버 유지보수, Dokploy 업데이트
  (10) 빌드 타입 선택 (Nixpacks, Dockerfile, Buildpack)
---

# Dokploy 서버 관리 스킬

Dokploy는 셀프호스팅 PaaS(Platform as a Service) 도구로, Docker 기반 애플리케이션 배포를 간편하게 관리합니다.

## 센터 프로젝트 Dokploy 설정 정보

> **참고**: 아래 정보는 센터 프로젝트의 실제 Dokploy 설정입니다. 설정 파일 위치: `.claude/skills/center-skill/scripts/config.sh`

| 항목 | 값 |
|------|-----|
| **Dokploy 서버 URL** | `http://209.97.169.136:3000` |
| **프로덕션 사이트** | `https://sonub.com` |
| **SSH 접속** | `root@sonub.com` |
| **애플리케이션 ID** | `DYmNZmKYtRG0RdNrsGcfn` |
| **PostgreSQL 호스트** | `209.97.169.136:5433` |
| **데이터베이스 이름** | `center` |

### 배포 모니터링 스크립트

```bash
# 배포 상태 실시간 모니터링
./.claude/skills/center-skill/scripts/deploy-watch.sh

# 배포 상태 및 이력 조회
./.claude/skills/center-skill/scripts/deploy-monitor.sh

# 배포 실패 시 에러 로그 확인
./.claude/skills/center-skill/scripts/deploy-error-check.sh auto
```

---

## 일반 Dokploy 서버 접속 정보

새로운 Dokploy 서버 작업 시, **반드시** 사용자에게 아래 정보를 요청합니다:

| 변수 | 설명 | 예시 |
|------|------|------|
| `DOKPLOY_SERVER_IP` | Dokploy 서버 IP | `1.2.3.4` |
| `ROOT_SSH_CONNECTION` | Root SSH 접속 주소 | `root@1.2.3.4` |
| `DOKPLOY_API_KEY` | Dokploy API 키 | Settings → Profile → API/CLI에서 생성 |

**보안 원칙**: 접속 정보는 메모리에만 보관하고, 파일에 저장하지 않습니다.

### 사용자에게 요청할 질문

```
Dokploy 서버 작업을 진행하기 전에 다음 정보가 필요합니다:

1. Dokploy 서버 IP 주소 (예: 1.2.3.4)
2. Root SSH 접속 주소 (예: root@1.2.3.4)
3. Dokploy API 키 (Settings → Profile → API/CLI에서 생성)

※ SSH 키 인증이 설정되어 있어야 합니다 (ssh-copy-id 완료)
```

---

## 참조 문서

작업 유형에 따라 해당 문서를 참조합니다:

| 작업 | 문서 | 주요 내용 |
|------|------|----------|
| **API를 통한 원격 관리** | [api.md](references/api.md) | Dokploy REST API, 인증, 배포 자동화 |
| **애플리케이션 관리/설정** | [applications.md](references/applications.md) | 환경변수, 모니터링, 리소스 관리, Swarm 설정 |
| **빌드 타입 선택** | [build-types.md](references/build-types.md) | Nixpacks, Dockerfile, Buildpack 비교 |
| **Cloudflare 도메인/SSL** | [cloudflare.md](references/cloudflare.md) | Cloudflare DNS, Origin CA, 프록시 설정 |
| **traefik.me 무료 도메인** | [traefik-me-domain.md](references/traefik-me-domain.md) | 테스트용 무료 도메인 (HTTP only) |
| **볼륨 백업/복원** | [volume-backups.md](references/volume-backups.md) | S3 연동, Named Volume 백업/복원 |
| **데이터베이스 관리** | [database.md](references/database.md) | PostgreSQL, MySQL, MongoDB, Redis 관리 |
| **Docker Compose 관리** | [docker-compose.md](references/docker-compose.md) | 멀티 컨테이너 설정, 볼륨 마운트 규칙 |
| **문제 해결/디버깅** | [debugging.md](references/debugging.md) | 502 에러, 도메인 접속 문제, Traefik 로그 |
| **서버 유지보수/업데이트** | [maintenance.md](references/maintenance.md) | Dokploy 업데이트, 디스크 관리, 백업 |

---

## 빠른 참조

### 필수 포트 설정

| 프레임워크 | 기본 포트 |
|------------|----------|
| Next.js / Node.js | 3000 |
| Laravel / PHP | 8000 |
| Django / Python | 8000 |
| NGINX (정적) | 80 |

### 컨테이너 수신 주소

```bash
# 올바른 설정 (모든 인터페이스에서 수신)
0.0.0.0:3000

# 잘못된 설정 (외부 접근 불가)
127.0.0.1:3000
```

### Docker Compose 볼륨 마운트

```yaml
# 올바른 형식 (상대 경로)
volumes:
  - "../files/my-data:/var/lib/data"

# 잘못된 형식 (절대 경로 사용 금지)
volumes:
  - "/folder:/path/in/container"
```

---

## SSH 기반 작업 예시

### 서버 상태 확인

```bash
# Docker 컨테이너 상태 확인
ssh root@$SERVER_IP "docker ps"

# Dokploy 필수 컨테이너 확인 (4개: dokploy, postgres, redis, traefik)
ssh root@$SERVER_IP "docker ps | grep -E 'dokploy|postgres|redis|traefik'"

# 디스크 사용량 확인
ssh root@$SERVER_IP "df -h"
```

### 도메인 접속 문제 진단

```bash
# DNS 확인
dig +short example.com

# HTTP 응답 확인
curl -sI https://example.com | head -10

# Traefik 설정에서 도메인 검색
ssh root@$SERVER_IP "grep -r 'example.com' /etc/dokploy/traefik/dynamic/*.yml"

# SSL 인증서 확인
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates
```

### 컨테이너 로그 확인

```bash
# Traefik 로그
ssh root@$SERVER_IP "docker logs dokploy-traefik --tail 100"

# 특정 서비스 로그
ssh root@$SERVER_IP "docker service logs <service-name> --tail 100"
```

### Docker 재시작

```bash
# Traefik만 재시작
ssh root@$SERVER_IP "docker restart dokploy-traefik"

# Dokploy 전체 재시작
ssh root@$SERVER_IP "docker service update --force dokploy"
```

---

## API 기반 작업 예시

### 프로젝트/애플리케이션 조회

```bash
# 모든 프로젝트 조회
curl -X GET "http://$SERVER_IP:3000/api/project.all" \
  -H "x-api-key: $API_KEY"

# 특정 애플리케이션 조회
curl -X GET "http://$SERVER_IP:3000/api/application.one?applicationId=$APP_ID" \
  -H "x-api-key: $API_KEY"
```

### 애플리케이션 재배포

```bash
curl -X POST "http://$SERVER_IP:3000/api/application.redeploy" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"applicationId\": \"$APP_ID\"}"
```

상세한 API 사용법은 [api.md](references/api.md) 참조.

---

## 문제 해결 순서

1. **포트 확인**: 앱이 올바른 포트에서 실행 중인지
2. **수신 주소 확인**: `0.0.0.0`에서 수신 대기하는지
3. **DNS 확인**: 도메인이 서버 IP를 가리키는지
4. **컨테이너 로그 확인**: `docker service logs <service-name>`
5. **Traefik 설정 확인**: `/etc/dokploy/traefik/dynamic/*.yml`
6. **API로 배포 상태 확인**: `deployment.all` 엔드포인트

상세한 문제 해결 가이드는 [debugging.md](references/debugging.md) 참조.

---

## 주요 작업 워크플로우

### 새 애플리케이션 배포

1. 프로젝트 생성 (UI 또는 API)
2. 애플리케이션 생성 및 Git 소스 연결
3. 빌드 타입 선택 ([build-types.md](references/build-types.md) 참조)
4. 환경 변수 설정
5. 도메인 설정 및 SSL 인증서 발급
6. 배포 실행

### 도메인 설정

1. DNS 레코드 설정 (A 레코드 → 서버 IP)
2. Dokploy에서 도메인 추가
3. HTTPS 활성화 및 인증서 타입 선택
4. 접속 테스트

Cloudflare 사용 시 [cloudflare.md](references/cloudflare.md), 테스트용 도메인은 [traefik-me-domain.md](references/traefik-me-domain.md) 참조.

### 볼륨 백업 설정

1. S3 호환 스토리지 연결
2. 명명 볼륨(Named Volume) 사용 확인
3. 백업 스케줄 설정 (Cron 형식)
4. 테스트 백업 실행

상세 가이드는 [volume-backups.md](references/volume-backups.md) 참조.

---

## 센터 프로젝트 Docker 설정

### Dockerfile 구성 (`etc/docker/Dockerfile`)

```dockerfile
FROM php:8.4-fpm

# 설치 패키지:
# - nginx, libpq-dev (PostgreSQL)
# - libpng-dev, libjpeg-dev, libwebp-dev, libfreetype6-dev (GD 이미지 처리)
# - APCu (PHP 공유 메모리 캐시)

# PHP 확장:
# - pdo, pdo_pgsql (PostgreSQL PDO)
# - gd (이미지 썸네일 생성)
# - apcu (캐시)

WORKDIR /www
COPY . /www
EXPOSE 80
CMD php-fpm -D && nginx -g "daemon off;"
```

**주요 특징:**
- PHP 8.4 + FPM + Nginx 단일 컨테이너
- PostgreSQL PDO 드라이버
- GD 라이브러리 (썸네일 생성)
- APCu 캐시
- 업로드 디렉토리: `/uploads` (777 권한)

### docker-compose.yml (로컬 개발 전용)

```yaml
services:
  center:
    build:
      context: .
      dockerfile: etc/docker/Dockerfile
    ports:
      - "8080:80"
    volumes:
      - .:/www          # 소스 코드 실시간 반영
      - ./uploads:/uploads  # 업로드 파일 영구 저장
```

**중요:** Dokploy 배포 시에는 docker-compose.yml을 사용하지 않습니다. Dockerfile만 사용하여 소스 코드가 COPY됩니다.

### Nginx 설정 (`etc/nginx/conf.d/center.conf`)

| 설정 | 값 | 설명 |
|------|-----|------|
| **client_max_body_size** | 50M | 최대 업로드 크기 |
| **정적 파일 캐시** | 365일 | `/uploads/*` 경로 |
| **PHP 실행 방지** | 403 | uploads 폴더 내 PHP 차단 |
| **라우팅** | `layout.php` | 모든 요청을 Front Controller로 |

### 배포 워크플로우

```bash
# 1. 테스트 실행 (Deploy + Browser 테스트)
./deploy.sh

# 2. 빌드 날짜 업데이트
npm run patch:build-date

# 3. 커밋 및 푸시
git add .
git commit -m "커밋 메시지"
git push

# 4. 배포 모니터링
./.claude/skills/center-skill/scripts/deploy-watch.sh
```

**deploy.sh 테스트 항목:**
- `tests/Deploy/**/*Test.php` - 배포 환경 테스트
- `tests/Browser/**/*Test.php` - 브라우저 테스트
