---
name: docker-db-backup
description: Docker 환경에서 DB 자동 백업이 필요할 때 사용. PostgreSQL, MySQL, MariaDB 지원. /docker-db-backup으로 실행.
license: MIT
metadata:
  author: user
  version: "1.0.0"
---

# Docker DB Backup Skill

Docker Compose 프로젝트에 cron 기반 자동 DB 백업 컨테이너를 추가하는 스킬입니다.

## Skill Description

**Triggers:**
- `/docker-db-backup` — 대화형으로 DB 종류를 확인 후 백업 서비스 추가
- `/docker-db-backup pg` — PostgreSQL 백업 서비스 추가
- `/docker-db-backup mysql` — MySQL/MariaDB 백업 서비스 추가

**생성/수정되는 파일:**
- `{compose-dir}/backup-entrypoint.sh` — 백업 실행 엔트리포인트
- `{compose-dir}/docker-compose.yml` — db-backup 서비스 추가
- `{compose-dir}/.env` — 백업 설정 변수 추가

## Execution Steps

### Step 1: 프로젝트 분석

1. `docker-compose.yml` 위치를 찾는다 (프로젝트 루트 또는 `docker-images/` 등)
2. 기존 DB 서비스를 파악한다:
   - `postgres` / `pg` 이미지 → PostgreSQL
   - `mysql` / `mariadb` 이미지 → MySQL/MariaDB
3. DB 서비스명, 환경변수명, 포트, 헬스체크 조건을 추출한다
4. 인자가 없으면 사용자에게 DB 종류를 확인한다

### Step 2: backup-entrypoint.sh 생성

**반드시 LF 줄바꿈으로 생성해야 한다.** Windows에서 CRLF로 생성하면 컨테이너에서 깨진다.

생성 후 아래 명령을 실행:
```bash
sed -i 's/\r$//' {compose-dir}/backup-entrypoint.sh
```

#### PostgreSQL 템플릿

```sh
#!/bin/sh
set -e

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
CRON_SCHEDULE="${CRON_SCHEDULE:-0 2 * * *}"

mkdir -p "$BACKUP_DIR"

cat > /usr/local/bin/run-backup.sh << 'SCRIPT'
#!/bin/sh
set -e

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${POSTGRES_DB}_${TIMESTAMP}.sql.gz"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 백업 시작: ${POSTGRES_DB}"

PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
    -h "$POSTGRES_HOST" \
    -p "${POSTGRES_PORT:-5432}" \
    -U "$POSTGRES_USER" \
    "$POSTGRES_DB" \
    --no-owner --no-acl \
    | gzip > "$BACKUP_FILE"

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 백업 완료: $BACKUP_FILE ($SIZE)"

DELETED=$(find "$BACKUP_DIR" -name "${POSTGRES_DB}_*.sql.gz" -mtime +"$RETENTION_DAYS" -print -delete | wc -l)
if [ "$DELETED" -gt 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 오래된 백업 ${DELETED}개 삭제 (보관: ${RETENTION_DAYS}일)"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 현재 백업 목록:"
ls -lh "$BACKUP_DIR"/${POSTGRES_DB}_*.sql.gz 2>/dev/null || echo "  (없음)"
SCRIPT

chmod +x /usr/local/bin/run-backup.sh
env | grep -E '^(POSTGRES_|BACKUP_|RETENTION_)' > /etc/backup.env
echo "${CRON_SCHEDULE} . /etc/backup.env; /usr/local/bin/run-backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root

echo "============================================"
echo "  DB Backup Service Started (PostgreSQL)"
echo "  Schedule: ${CRON_SCHEDULE}"
echo "  Retention: ${RETENTION_DAYS} days"
echo "  Backup dir: ${BACKUP_DIR}"
echo "============================================"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 초기 백업 실행..."
/usr/local/bin/run-backup.sh

exec crond -f -l 2
```

#### MySQL/MariaDB 템플릿

```sh
#!/bin/sh
set -e

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
CRON_SCHEDULE="${CRON_SCHEDULE:-0 2 * * *}"

mkdir -p "$BACKUP_DIR"

# crond 설치 (mysql 이미지에는 없을 수 있음)
if ! command -v crond > /dev/null 2>&1 && ! command -v cron > /dev/null 2>&1; then
    if command -v apt-get > /dev/null 2>&1; then
        apt-get update -qq && apt-get install -y -qq cron > /dev/null 2>&1
        CRON_CMD="cron -f"
    elif command -v apk > /dev/null 2>&1; then
        CRON_CMD="crond -f -l 2"
    fi
else
    if command -v crond > /dev/null 2>&1; then
        CRON_CMD="crond -f -l 2"
    else
        CRON_CMD="cron -f"
    fi
fi

cat > /usr/local/bin/run-backup.sh << 'SCRIPT'
#!/bin/sh
set -e

BACKUP_DIR="${BACKUP_DIR:-/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${MYSQL_DATABASE}_${TIMESTAMP}.sql.gz"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 백업 시작: ${MYSQL_DATABASE}"

mysqldump \
    -h "$MYSQL_HOST" \
    -P "${MYSQL_PORT:-3306}" \
    -u "$MYSQL_USER" \
    -p"$MYSQL_PASSWORD" \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    "$MYSQL_DATABASE" \
    | gzip > "$BACKUP_FILE"

SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 백업 완료: $BACKUP_FILE ($SIZE)"

DELETED=$(find "$BACKUP_DIR" -name "${MYSQL_DATABASE}_*.sql.gz" -mtime +"$RETENTION_DAYS" -print -delete | wc -l)
if [ "$DELETED" -gt 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 오래된 백업 ${DELETED}개 삭제 (보관: ${RETENTION_DAYS}일)"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 현재 백업 목록:"
ls -lh "$BACKUP_DIR"/${MYSQL_DATABASE}_*.sql.gz 2>/dev/null || echo "  (없음)"
SCRIPT

chmod +x /usr/local/bin/run-backup.sh
env | grep -E '^(MYSQL_|BACKUP_|RETENTION_)' > /etc/backup.env

# crontab 설정 (Debian/Alpine 분기)
if [ -d /etc/crontabs ]; then
    echo "${CRON_SCHEDULE} . /etc/backup.env; /usr/local/bin/run-backup.sh >> /var/log/backup.log 2>&1" > /etc/crontabs/root
else
    echo "${CRON_SCHEDULE} root . /etc/backup.env; /usr/local/bin/run-backup.sh >> /var/log/backup.log 2>&1" > /etc/cron.d/db-backup
    chmod 0644 /etc/cron.d/db-backup
fi

echo "============================================"
echo "  DB Backup Service Started (MySQL)"
echo "  Schedule: ${CRON_SCHEDULE}"
echo "  Retention: ${RETENTION_DAYS} days"
echo "  Backup dir: ${BACKUP_DIR}"
echo "============================================"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 초기 백업 실행..."
/usr/local/bin/run-backup.sh

exec $CRON_CMD
```

### Step 3: docker-compose.yml에 서비스 추가

기존 `volumes:` 선언 바로 위에 서비스를 추가한다.

#### PostgreSQL용 서비스

```yaml
  db-backup:
    image: postgres:{DB와 동일 버전}-alpine
    container_name: ${PROJECT_NAME}-db-backup
    restart: unless-stopped
    environment:
      POSTGRES_HOST: {DB 서비스명}
      POSTGRES_PORT: "5432"
      POSTGRES_USER: ${DB_USER변수}
      POSTGRES_PASSWORD: ${DB_PASSWORD변수}
      POSTGRES_DB: ${DB_NAME변수}
      BACKUP_DIR: /backups
      RETENTION_DAYS: ${BACKUP_RETENTION_DAYS:-7}
      CRON_SCHEDULE: ${BACKUP_CRON_SCHEDULE:-0 2 * * *}
      TZ: ${TZ:-Asia/Seoul}
    volumes:
      - db_backups:/backups
      - ./backup-entrypoint.sh:/entrypoint.sh:ro
    entrypoint: ["/bin/sh", "/entrypoint.sh"]
    depends_on:
      {DB 서비스명}:
        condition: service_healthy
    networks:
      - {기존 네트워크명}
```

#### MySQL/MariaDB용 서비스

```yaml
  db-backup:
    image: mysql:{DB와 동일 버전}   # 또는 mariadb:{버전}
    container_name: ${PROJECT_NAME}-db-backup
    restart: unless-stopped
    environment:
      MYSQL_HOST: {DB 서비스명}
      MYSQL_PORT: "3306"
      MYSQL_USER: ${DB_USER변수}
      MYSQL_PASSWORD: ${DB_PASSWORD변수}
      MYSQL_DATABASE: ${DB_NAME변수}
      BACKUP_DIR: /backups
      RETENTION_DAYS: ${BACKUP_RETENTION_DAYS:-7}
      CRON_SCHEDULE: ${BACKUP_CRON_SCHEDULE:-0 2 * * *}
      TZ: ${TZ:-Asia/Seoul}
    volumes:
      - db_backups:/backups
      - ./backup-entrypoint.sh:/entrypoint.sh:ro
    entrypoint: ["/bin/sh", "/entrypoint.sh"]
    depends_on:
      {DB 서비스명}:
        condition: service_healthy
    networks:
      - {기존 네트워크명}
```

**volumes 섹션에 추가:**
```yaml
volumes:
  db_backups:     # ← 이 줄 추가
```

### Step 4: .env에 변수 추가

```bash
# DB 백업 설정
BACKUP_RETENTION_DAYS=7
BACKUP_CRON_SCHEDULE=0 2 * * *
```

### Step 5: LF 변환 + 테스트

```bash
# 1. LF 변환 (필수)
sed -i 's/\r$//' {compose-dir}/backup-entrypoint.sh

# 2. 백업 서비스 시작
cd {compose-dir} && docker compose up -d db-backup

# 3. 로그 확인 (초기 백업 성공 여부)
docker logs {프로젝트}-db-backup

# 4. 백업 파일 확인
MSYS_NO_PATHCONV=1 docker exec {프로젝트}-db-backup ls -lh /backups/
```

### Step 6: 결과 보고

실행 후 사용자에게 다음을 알려준다:

- 생성/수정된 파일 목록
- 백업 스케줄 (기본 매일 02:00)
- 보관 기간 (기본 7일)
- 운영 명령어 (수동 백업, 복원 방법)

## DB별 주요 차이점

| 항목 | PostgreSQL | MySQL/MariaDB |
|------|-----------|---------------|
| 이미지 | `postgres:{ver}-alpine` | `mysql:{ver}` 또는 `mariadb:{ver}` |
| 덤프 도구 | `pg_dump` (이미지 내장) | `mysqldump` (이미지 내장) |
| cron | Alpine `crond` 내장 | Debian이면 `cron` 설치 필요 |
| 환경변수 prefix | `POSTGRES_` | `MYSQL_` |
| 덤프 옵션 | `--no-owner --no-acl` | `--single-transaction --routines --triggers --events` |
| 복원 명령 | `gunzip -c file.sql.gz \| psql -U user -d db` | `gunzip -c file.sql.gz \| mysql -u user -p db` |

## 주의사항

- **backup-entrypoint.sh는 반드시 LF 줄바꿈**이어야 한다. Windows CRLF → 컨테이너에서 `/bin/sh: set: illegal option` 에러 발생
- **백업 도구 버전 ≥ DB 서버 버전.** pg_dump/mysqldump는 forward-compatible이 아니라, **구버전 도구로 newer 서버를 덤프하면 `server version mismatch`로 실패**한다. 백업 이미지를 DB 이미지와 **동일 태그**로 고정하라(DB를 올리면 백업 이미지도 같이 올림). MySQL은 버전이 같아야 `caching_sha2_password` 인증 핸드셰이크도 안전하다
- **Docker volume `db_backups`**에 저장되므로 컨테이너 삭제해도 백업은 유지된다
- 호스트로 백업을 꺼내려면: `docker cp {컨테이너}:/backups/{파일} ./`
- `.env`의 `BACKUP_CRON_SCHEDULE`은 cron 5-field 표현식 (초 없음)
