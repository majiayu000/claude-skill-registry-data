---
name: env-health
description: Diagnose and fix Laravel environment configuration issues, cache problems, and database connection errors. Use when user reports "configuration not applied", "database connection error", "SQLite connection attempt", "hosts array is empty", or any environment-related issues. Also use after .env file modifications.
allowed-tools: [Bash, Read, Grep]
---

# Environment Health Checker

당신이 Laravel 환경 설정, 캐시, 또는 데이터베이스 연결 문제를 진단해야 할 때 이 Skill을 사용하세요.

## 🎯 자동 실행 트리거

다음 상황에서 **자동으로 실행**:
- 사용자가 "설정이 반영 안돼" 또는 "configuration not applied" 언급
- "Database connection error" 또는 "SQLite connection attempt" 오류
- "Database hosts array is empty" 오류
- ".env 파일 수정했는데 변화 없음"
- "왜 Laravel이 [잘못된 DB]로 연결하려고 해?"

## 📋 진단 체크리스트

### 1. 현재 환경 상태 확인

```bash
# 현재 환경 정보 수집
php artisan tinker --execute="
echo 'APP_ENV: ' . config('app.env') . PHP_EOL;
echo 'APP_DEBUG: ' . (config('app.debug') ? 'true' : 'false') . PHP_EOL;
echo 'DB_CONNECTION: ' . config('database.default') . PHP_EOL;
echo 'DB_DATABASE: ' . DB::connection()->getDatabaseName() . PHP_EOL;
echo 'SESSION_DRIVER: ' . config('session.driver') . PHP_EOL;
echo 'CACHE_STORE: ' . config('cache.default') . PHP_EOL;
echo 'QUEUE_CONNECTION: ' . config('queue.default') . PHP_EOL;
"
```

**기대값 (로컬 개발 환경)**:
- `APP_ENV: local`
- `DB_CONNECTION: pgsql_local`
- `DB_DATABASE: ykp_dashboard_local`
- `SESSION_DRIVER: file`
- `CACHE_STORE: file`
- `QUEUE_CONNECTION: sync`

### 2. .env 파일 검증

```bash
# .env 파일 읽기 (중요 변수만)
grep -E "^(APP_ENV|DB_CONNECTION|DB_HOST_LOCAL|DB_DATABASE_LOCAL|SESSION_DRIVER|CACHE_STORE|QUEUE_CONNECTION)=" .env
```

**검증 항목**:
- ✅ `APP_ENV=local` (프로덕션 아님)
- ✅ `DB_CONNECTION=pgsql_local` (로컬 PostgreSQL)
- ✅ `SESSION_DRIVER=file` (database 아님)
- ✅ `CACHE_STORE=file` (database 아님)
- ✅ `QUEUE_CONNECTION=sync` (database 아님)

### 3. 캐시 상태 진단

```bash
# 캐시된 설정 파일 존재 여부 확인
ls -la bootstrap/cache/*.php 2>/dev/null | grep -E "(config|routes|services)"
```

**문제 감지**:
- `config.php` 존재 → **캐시된 설정 사용 중** → `.env` 변경 무시됨!
- `routes.php` 존재 → 라우트 캐시 사용 중
- `services.php` 존재 → 서비스 캐시 사용 중

### 4. 데이터베이스 연결 테스트

```bash
# 실제 DB 연결 테스트
php artisan tinker --execute="
try {
    \$count = DB::table('users')->count();
    echo 'DB 연결 성공! Users: ' . \$count . PHP_EOL;
} catch (Exception \$e) {
    echo 'DB 연결 실패: ' . \$e->getMessage() . PHP_EOL;
}
"
```

## 🔧 자동 해결 절차

### 문제 1: 캐시 문제 (가장 흔함!)

**증상**: `.env` 변경했는데 반영 안됨, 구 설정 사용 중

**해결**:
```bash
# 모든 캐시 클리어
php artisan optimize:clear

# 개별 캐시 클리어 (필요 시)
php artisan config:clear
php artisan cache:clear
php artisan route:clear
php artisan view:clear
```

**사용자에게 안내**:
> ✅ **캐시 클리어 완료!**
>
> Laravel이 캐시된 설정을 사용하고 있었습니다. 다음 명령어로 모든 캐시를 삭제했습니다:
> ```bash
> php artisan optimize:clear
> ```
>
> **다음 단계**: 서버를 재시작하세요:
> ```bash
> # 기존 서버 종료 (Ctrl+C)
> # 새로 시작
> php artisan serve
> ```

### 문제 2: 잘못된 DB 연결

**증상**: "SQLite connection attempt", "pgsql 대신 sqlite 사용", "Supabase 대신 로컬 DB 사용"

**해결**:
1. `.env` 파일에서 `DB_CONNECTION` 확인
2. 올바른 값으로 수정 제안:
   - 로컬: `DB_CONNECTION=pgsql_local`
   - 프로덕션: `DB_CONNECTION=pgsql`

**사용자에게 안내**:
> ⚠️ **잘못된 DB 연결 감지!**
>
> 현재 설정: `DB_CONNECTION=sqlite` (또는 잘못된 값)
> 로컬 개발용 권장 설정:
> ```env
> DB_CONNECTION=pgsql_local
> DB_HOST_LOCAL=localhost
> DB_DATABASE_LOCAL=ykp_dashboard_local
> ```
>
> `.env` 파일을 수정한 후 캐시를 클리어하세요:
> ```bash
> php artisan optimize:clear
> ```

### 문제 3: Session/Cache 드라이버 문제

**증상**: "Database hosts array is empty" (session/cache가 DB 사용하려 함)

**해결**:
`.env` 파일에서 다음 값 확인:
```env
SESSION_DRIVER=file  # database 아님!
CACHE_STORE=file     # database 아님!
QUEUE_CONNECTION=sync # database 아님!
```

**사용자에게 안내**:
> ⚠️ **Session/Cache 드라이버 문제!**
>
> 로컬 개발 환경에서는 파일 기반 드라이버를 사용하세요:
> ```env
> SESSION_DRIVER=file
> CACHE_STORE=file
> QUEUE_CONNECTION=sync
> ```
>
> **왜?** 더 빠르고, DB 연결 문제 없고, 디버깅 쉬움!
>
> `.env` 수정 후:
> ```bash
> php artisan optimize:clear
> ```

### 문제 4: 서버 재시작 필요

**증상**: 캐시 클리어했는데도 변화 없음

**해결**:
```bash
# Windows에서 PHP 서버 프로세스 종료
taskkill /F /IM php.exe

# 또는 Ctrl+C로 종료 후 재시작
php artisan serve
```

**사용자에게 안내**:
> 🔄 **서버 재시작 필요!**
>
> 캐시를 클리어했지만, 실행 중인 PHP 서버가 이전 설정을 메모리에 유지하고 있을 수 있습니다.
>
> **해결**: 서버 재시작
> ```bash
> # 현재 서버 종료 (Ctrl+C)
> # 새로 시작
> php artisan serve
> ```

## 📊 최종 보고서 형식

진단 완료 후 다음 형식으로 보고:

```
🏥 환경 건강 진단 완료

✅ 정상 항목:
- APP_ENV: local
- DB_DATABASE: ykp_dashboard_local

⚠️ 문제 발견:
1. 캐시 문제: config.php 파일 존재 (캐시된 설정 사용 중)
   → 해결: php artisan optimize:clear 실행 완료

2. Session 드라이버 문제: SESSION_DRIVER=database
   → 권장: SESSION_DRIVER=file (로컬 개발용)

📋 권장 조치:
1. .env 파일에서 SESSION_DRIVER=file 설정
2. 서버 재시작: Ctrl+C 후 php artisan serve

💡 참고: CLAUDE.md "Environment Configuration" 섹션 참조
```

## 🚨 프로덕션 환경 감지 시

만약 `APP_ENV=production` 감지 시:

```
🚨 경고: 프로덕션 환경 감지!

현재 설정:
- APP_ENV: production
- DB_CONNECTION: pgsql (Supabase로 추정)

⚠️ 로컬 개발 중이라면 즉시 수정 필요:

.env 파일:
APP_ENV=local
DB_CONNECTION=pgsql_local

⚠️ 실제 프로덕션(Railway)이라면:
- Railway 환경변수에서 관리 (파일 수정 금지)
- DB 백업 확인 후 작업 진행
```

## 🎓 학습 포인트

이 Skill이 발견한 문제는 다음과 같이 요약:

1. **Laravel 캐시 메커니즘**: `php artisan config:cache` 실행 시 `.env` 무시됨
2. **환경 파일 로딩 순서**: `.env.local`은 production 모드에서 로드 안됨
3. **파일 vs DB 드라이버**: 로컬 개발은 파일 드라이버가 빠르고 안정적

**다음에 비슷한 문제 발생 시**:
1. 먼저 캐시 클리어: `php artisan optimize:clear`
2. 서버 재시작
3. 그래도 안되면 `.env` 파일 확인
