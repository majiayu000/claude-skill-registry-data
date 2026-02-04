---
name: db-validate
description: Validate Laravel database configuration and test actual connections. Use when user reports "database connection error", "hosts array is empty", "could not connect to database", or wants to verify database setup is correct.
allowed-tools: [Bash, Read, Grep]
---

# Database Connection Validator

Laravel 데이터베이스 설정을 검증하고 실제 연결을 테스트하는 Skill입니다.

## 🎯 자동 실행 트리거

다음 상황에서 **자동으로 실행**:
- "Database connection error" 오류
- "Database hosts array is empty" 오류
- "Could not connect to database" 오류
- "SQLSTATE[HY000]" 오류
- "DB 연결 확인해줘"
- "데이터베이스 설정 맞나?"

## 🔍 검증 체크리스트

### 1. .env 파일 DB 설정 확인

```bash
# DB 관련 환경변수 추출
grep -E "^(DB_CONNECTION|DB_HOST|DB_HOST_LOCAL|DB_PORT|DB_PORT_LOCAL|DB_DATABASE|DB_DATABASE_LOCAL|DB_USERNAME|DB_USERNAME_LOCAL|DB_PASSWORD|DB_PASSWORD_LOCAL)=" .env
```

**기대값 (로컬 개발)**:
```env
DB_CONNECTION=pgsql_local
DB_HOST_LOCAL=localhost
DB_PORT_LOCAL=5432
DB_DATABASE_LOCAL=ykp_dashboard_local
DB_USERNAME_LOCAL=postgres
DB_PASSWORD_LOCAL=1234
```

**검증 항목**:
- ✅ `DB_CONNECTION`이 정의되어 있나?
- ✅ 연결 이름과 일치하는 HOST/DATABASE 변수가 있나?
  - `pgsql_local` → `DB_HOST_LOCAL`, `DB_DATABASE_LOCAL` 필요
  - `pgsql` → `DB_HOST`, `DB_DATABASE` 필요
- ✅ 비밀번호가 설정되어 있나?

### 2. config/database.php 연결 설정 확인

```bash
# pgsql_local 연결 설정 확인
grep -A 15 "'pgsql_local'" config/database.php
```

**확인 사항**:
- 연결 정의 존재 여부
- `env()` 함수가 올바른 변수명 사용
- 올바른 드라이버 (`'driver' => 'pgsql'`)

### 3. 실제 DB 연결 테스트

```bash
# 현재 설정으로 연결 테스트
php artisan tinker --execute="
try {
    echo 'Testing Connection: ' . config('database.default') . PHP_EOL;
    echo 'Host: ' . config('database.connections.' . config('database.default') . '.host') . PHP_EOL;
    echo 'Database: ' . config('database.connections.' . config('database.default') . '.database') . PHP_EOL;

    \$count = DB::connection()->table('users')->count();
    echo 'SUCCESS: Connected! Users found: ' . \$count . PHP_EOL;
} catch (Exception \$e) {
    echo 'FAILED: ' . \$e->getMessage() . PHP_EOL;
}
"
```

### 4. PostgreSQL 서버 상태 확인 (로컬)

```bash
# PostgreSQL 프로세스 확인
tasklist /FI "IMAGENAME eq postgres.exe" 2>/dev/null || echo "PostgreSQL not running"

# 포트 5432 리스닝 확인
netstat -ano | findstr :5432
```

## 🛠️ 문제별 해결 방법

### 문제 1: "Database hosts array is empty"

**원인**: Session/Cache 드라이버가 database인데, 연결 설정이 없음

**진단**:
```bash
# Session/Cache 드라이버 확인
grep -E "^(SESSION_DRIVER|SESSION_CONNECTION|CACHE_STORE|CACHE_DATABASE_CONNECTION)=" .env
```

**해결**:
1. **로컬 개발**: 파일 드라이버 사용 (권장)
   ```env
   SESSION_DRIVER=file
   CACHE_STORE=file
   ```

2. **DB 드라이버 계속 사용**:
   ```env
   SESSION_DRIVER=database
   SESSION_CONNECTION=pgsql_local  # 명시적 연결
   CACHE_STORE=database
   CACHE_DATABASE_CONNECTION=pgsql_local
   ```

**사용자 안내**:
> ⚠️ **"Database hosts array is empty" 감지**
>
> **원인**: Session/Cache가 database 드라이버를 사용하려는데,
> 연결 설정(`SESSION_CONNECTION`)이 지정되지 않았습니다.
>
> **권장 해결 (로컬 개발)**:
> ```env
> SESSION_DRIVER=file
> CACHE_STORE=file
> QUEUE_CONNECTION=sync
> ```
>
> **또는 DB 연결 명시**:
> ```env
> SESSION_CONNECTION=pgsql_local
> CACHE_DATABASE_CONNECTION=pgsql_local
> ```
>
> 수정 후:
> ```bash
> php artisan optimize:clear
> ```

### 문제 2: "Could not connect to server"

**원인**: PostgreSQL 서버가 실행 중이지 않음 (로컬)

**진단**:
```bash
# PostgreSQL 실행 여부 확인
tasklist /FI "IMAGENAME eq postgres.exe"
```

**해결**:
```bash
# PostgreSQL 시작
postgresql-17.6-2-windows-x64-binaries/bin/pg_ctl.exe -D postgresql-data start

# 상태 확인
postgresql-17.6-2-windows-x64-binaries/bin/pg_ctl.exe -D postgresql-data status
```

**사용자 안내**:
> ⚠️ **PostgreSQL 서버 미실행**
>
> 로컬 PostgreSQL 서버가 실행되고 있지 않습니다.
>
> **해결**:
> ```bash
> # PostgreSQL 시작
> postgresql-17.6-2-windows-x64-binaries/bin/pg_ctl.exe -D postgresql-data start
>
> # 연결 테스트
> php artisan tinker --execute="DB::connection()->getPdo();"
> ```
>
> **자동 시작 설정** (선택사항):
> Windows Services에 PostgreSQL 등록하여 부팅 시 자동 시작

### 문제 3: "Access denied for user"

**원인**: 비밀번호 불일치 또는 사용자 권한 부족

**진단**:
```bash
# 직접 PostgreSQL 연결 테스트
postgresql-17.6-2-windows-x64-binaries/bin/psql.exe -U postgres -d ykp_dashboard_local -c "SELECT 1;"
```

**해결**:
1. **비밀번호 확인**:
   ```env
   DB_PASSWORD_LOCAL=1234  # 실제 PostgreSQL 비밀번호
   ```

2. **사용자 권한 확인**:
   ```sql
   -- PostgreSQL에 접속하여 실행
   \du  -- 사용자 목록 및 권한 확인
   ```

**사용자 안내**:
> ⚠️ **인증 실패**
>
> PostgreSQL 사용자 인증에 실패했습니다.
>
> **체크리스트**:
> 1. `.env` 파일의 `DB_PASSWORD_LOCAL` 확인
> 2. psql로 직접 연결 테스트:
>    ```bash
>    psql -U postgres -d ykp_dashboard_local
>    ```
> 3. 비밀번호가 다르면 PostgreSQL 재설정:
>    ```bash
>    psql -U postgres
>    ALTER USER postgres PASSWORD '새비밀번호';
>    ```

### 문제 4: "Database does not exist"

**원인**: 데이터베이스가 생성되지 않음

**진단**:
```bash
# 데이터베이스 목록 확인
postgresql-17.6-2-windows-x64-binaries/bin/psql.exe -U postgres -c "\l"
```

**해결**:
```bash
# 데이터베이스 생성
postgresql-17.6-2-windows-x64-binaries/bin/psql.exe -U postgres -c "CREATE DATABASE ykp_dashboard_local;"

# 마이그레이션 실행
php artisan migrate
php artisan db:seed
```

**사용자 안내**:
> ⚠️ **데이터베이스 미존재**
>
> `ykp_dashboard_local` 데이터베이스가 생성되지 않았습니다.
>
> **해결**:
> ```bash
> # 1. 데이터베이스 생성
> psql -U postgres -c "CREATE DATABASE ykp_dashboard_local;"
>
> # 2. 마이그레이션 실행
> php artisan migrate
>
> # 3. 테스트 데이터 시딩
> php artisan db:seed
> ```

### 문제 5: 로컬/프로덕션 DB 혼동

**증상**: 로컬 환경인데 Supabase 연결 시도

**진단**:
```bash
# 현재 연결 확인
php artisan tinker --execute="
echo 'Connection: ' . config('database.default') . PHP_EOL;
echo 'Host: ' . config('database.connections.' . config('database.default') . '.host') . PHP_EOL;
"
```

**위험 신호**:
- `APP_ENV=local`인데 `DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com`

**해결**:
`.env` 파일 수정:
```env
# 로컬 개발용
DB_CONNECTION=pgsql_local
DB_HOST_LOCAL=localhost
DB_DATABASE_LOCAL=ykp_dashboard_local
```

**사용자 안내**:
> 🚨 **위험: 프로덕션 DB 연결 시도 감지!**
>
> 로컬 환경(`APP_ENV=local`)인데 Supabase 프로덕션 DB에 연결하려고 합니다!
>
> **즉시 수정**:
> ```env
> DB_CONNECTION=pgsql_local
> DB_HOST_LOCAL=localhost
> DB_DATABASE_LOCAL=ykp_dashboard_local
> ```
>
> **캐시 클리어**:
> ```bash
> php artisan optimize:clear
> ```
>
> ⚠️ 프로덕션 데이터를 실수로 수정할 뻔했습니다!

## 📊 검증 보고서

모든 검증 완료 후 보고:

```
🗄️ 데이터베이스 연결 검증 완료

✅ 환경 설정:
- APP_ENV: local
- DB_CONNECTION: pgsql_local

✅ 연결 설정:
- Host: localhost:5432
- Database: ykp_dashboard_local
- Username: postgres

✅ PostgreSQL 서버:
- 상태: 실행 중 ✅
- 버전: PostgreSQL 17.6
- 포트: 5432 리스닝 중

✅ 연결 테스트:
- 연결 성공 ✅
- Users 테이블: 63 rows
- 응답 시간: < 50ms

🎯 추천 사항:
- ✅ 모든 설정이 올바릅니다
- ✅ 데이터베이스 정상 작동 중
- ℹ️  테스트 계정: admin@ykp.com / password
```

## 🔧 연결 설정 참조

### 로컬 개발 환경 (pgsql_local)

```env
DB_CONNECTION=pgsql_local
DB_HOST_LOCAL=localhost
DB_PORT_LOCAL=5432
DB_DATABASE_LOCAL=ykp_dashboard_local
DB_USERNAME_LOCAL=postgres
DB_PASSWORD_LOCAL=1234
```

### 프로덕션 환경 (pgsql - Supabase)

**Railway 환경변수에서 설정**:
```env
DB_CONNECTION=pgsql
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres.qwafwqxdcfpqqwpmphkm
DB_PASSWORD=<Supabase 비밀번호>
DB_SSLMODE=require
```

## 🚨 프로덕션 DB 안전 수칙

### 절대 금지

1. ❌ 로컬에서 프로덕션 DB 직접 연결
2. ❌ `.env` 파일에 Supabase 자격증명 저장
3. ❌ 프로덕션 DB에서 `migrate:fresh` 실행
4. ❌ 테스트 데이터를 프로덕션에 삽입

### 권장 사항

1. ✅ 로컬은 항상 `pgsql_local` 사용
2. ✅ Supabase는 Railway 환경변수에서만 관리
3. ✅ 프로덕션 작업 전 백업 필수
4. ✅ 읽기 전용 연결로 프로덕션 확인

## 🎓 트러블슈팅 플로우차트

```
DB 연결 오류 발생
     ↓
[1] PostgreSQL 실행 중?
     No → 서버 시작
     Yes ↓
[2] .env 파일 올바른 설정?
     No → pgsql_local 설정 확인
     Yes ↓
[3] 캐시 문제?
     Yes → optimize:clear
     No ↓
[4] 데이터베이스 존재?
     No → CREATE DATABASE
     Yes ↓
[5] 비밀번호 일치?
     No → .env 수정 또는 PG 재설정
     Yes ↓
[6] env-health Skill 실행
```

## 💡 학습 포인트

이 Skill을 통해 배운 핵심:

1. **연결 이름의 일관성**:
   - `DB_CONNECTION=pgsql_local`
   - → `DB_HOST_LOCAL`, `DB_DATABASE_LOCAL` 사용
   - 접미사 일치 중요!

2. **Session/Cache 드라이버 함정**:
   - `SESSION_DRIVER=database`
   - → `SESSION_CONNECTION` 필수!
   - 없으면 "hosts array is empty" 오류

3. **로컬/프로덕션 명확한 분리**:
   - 로컬: localhost PostgreSQL
   - 프로덕션: Supabase (Railway 환경변수)
   - 절대 혼용 금지!

**다음에 DB 문제 발생 시**:
1. PostgreSQL 실행 확인
2. `.env` 파일 검증
3. 캐시 클리어
4. 연결 테스트 (tinker)
