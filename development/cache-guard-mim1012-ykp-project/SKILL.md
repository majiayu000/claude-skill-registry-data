---
name: cache-guard
description: Monitor Laravel configuration file changes and automatically manage caches. Use immediately after .env modifications, config file edits, or when user reports "settings not reflecting" or "changes not applied". Prevents stale configuration issues.
allowed-tools: [Bash, Read]
---

# Laravel Cache Guardian

Laravel 설정 파일 변경을 감지하고 자동으로 캐시를 관리하는 Skill입니다.

## 🎯 자동 실행 트리거

다음 상황에서 **자동으로 실행**:
- `.env` 파일 수정 직후
- `config/*.php` 파일 수정 직후
- "설정이 반영 안돼" / "Changes not applied"
- "왜 변경 사항이 안 보이지?"
- "캐시 때문인가?"

## 🔍 캐시 상태 진단

### 1. 캐시 파일 존재 여부 확인

```bash
# Laravel 캐시 파일 목록
ls -la bootstrap/cache/ 2>/dev/null | grep -E "\\.php$"
```

**캐시 파일 종류**:
- `config.php` - 설정 캐시 (`.env` 무시됨!)
- `routes-v7.php` - 라우트 캐시
- `services.php` - 서비스 프로바이더 캐시
- `packages.php` - 패키지 발견 캐시
- `events.php` - 이벤트 리스너 캐시

### 2. 캐시 타임스탬프 확인

```bash
# 캐시 파일 생성 시간 확인
stat -c "%y %n" bootstrap/cache/*.php 2>/dev/null
```

**위험 신호**:
- `.env` 수정 시간 < `config.php` 생성 시간
  → ❌ 오래된 캐시 사용 중!

### 3. 현재 사용 중인 설정 확인

```bash
# 실제 적용된 설정 확인
php artisan tinker --execute="
echo 'Config Source: ' . (file_exists(base_path('bootstrap/cache/config.php')) ? 'CACHED' : 'FRESH') . PHP_EOL;
echo 'Config Age: ' . (file_exists(base_path('bootstrap/cache/config.php')) ? human_readable_time(filemtime(base_path('bootstrap/cache/config.php'))) : 'N/A') . PHP_EOL;
"
```

## 🛠️ 자동 캐시 관리

### 시나리오 1: .env 파일 수정 감지

**.env 파일 수정 직후 자동 실행**:

1. **캐시 상태 체크**:
   ```bash
   if [ -f bootstrap/cache/config.php ]; then
       echo "⚠️ 캐시 파일 발견: .env 변경 사항이 무시될 수 있습니다"
   fi
   ```

2. **자동 캐시 클리어**:
   ```bash
   php artisan config:clear
   echo "✅ Config 캐시 클리어 완료"
   ```

3. **검증**:
   ```bash
   # 현재 설정 재확인
   php artisan tinker --execute="echo config('app.env') . ' / ' . config('database.default');"
   ```

4. **사용자 안내**:
   > ✅ **.env 변경 감지 및 캐시 클리어 완료**
   >
   > 수정된 파일: `.env`
   > 실행한 명령: `php artisan config:clear`
   >
   > 📋 다음 단계:
   > 1. 서버 재시작 권장:
   >    ```bash
   >    # 현재 서버 종료 (Ctrl+C)
   >    # 새로 시작
   >    php artisan serve
   >    ```
   >
   > 2. 변경 사항 확인:
   >    - http://127.0.0.1:8000
   >    - 로그인하여 정상 작동 확인

### 시나리오 2: config/*.php 파일 수정 감지

**config 디렉토리 파일 수정 시**:

1. **영향 받는 캐시 확인**:
   ```bash
   # 수정된 파일에 따라 다른 캐시 클리어
   # - config/database.php → config + cache 클리어
   # - config/session.php → config + session 클리어
   # - config/cache.php → config + cache 클리어
   ```

2. **선택적 캐시 클리어**:
   ```bash
   # 설정 파일에 따라 적절한 캐시만 클리어
   php artisan config:clear
   php artisan cache:clear  # cache.php 수정 시
   ```

3. **사용자 안내**:
   > ✅ **Config 파일 변경 감지**
   >
   > 수정된 파일: `config/database.php`
   > 영향 받는 캐시: config, cache
   >
   > 실행한 명령:
   > ```bash
   > php artisan config:clear
   > php artisan cache:clear
   > ```
   >
   > ⚠️ 서버 재시작 필요: 메모리에 로드된 설정 갱신

### 시나리오 3: 전체 캐시 클리어 필요

**모든 캐시 문제 해결**:

```bash
# 올인원 솔루션
php artisan optimize:clear
```

**포함된 명령**:
- `config:clear` - 설정 캐시 삭제
- `cache:clear` - 애플리케이션 캐시 삭제
- `route:clear` - 라우트 캐시 삭제
- `view:clear` - 블레이드 뷰 캐시 삭제
- `event:clear` - 이벤트 캐시 삭제

**사용자 안내**:
> 🧹 **전체 캐시 클리어 완료**
>
> 실행한 명령: `php artisan optimize:clear`
>
> 삭제된 캐시:
> - ✅ Config cache
> - ✅ Route cache
> - ✅ View cache
> - ✅ Event cache
> - ✅ Application cache
>
> 🔄 서버 재시작:
> ```bash
> # 기존 서버 종료
> # 새로 시작
> php artisan serve
> ```

## ⚡ 서버 재시작 가이드

### 왜 서버 재시작이 필요한가?

캐시 파일을 삭제해도, **실행 중인 PHP 프로세스**는:
- 이전 설정을 메모리에 보관
- 싱글톤 인스턴스에 오래된 값 유지
- 재시작해야만 새 설정 로드

### 서버 재시작 방법

**방법 1: 정상 종료 (권장)**
```bash
# 터미널에서 Ctrl+C
# 그 후 재시작
php artisan serve
```

**방법 2: 강제 종료 (Windows)**
```bash
# 모든 PHP 프로세스 종료
taskkill /F /IM php.exe

# 재시작
php artisan serve
```

**방법 3: 프로세스 ID로 종료**
```bash
# PID 확인
netstat -ano | findstr :8000

# 특정 PID 종료
taskkill /F /PID <PID>

# 재시작
php artisan serve
```

### 재시작 필요 여부 판단

**즉시 재시작 필요**:
- ✅ `.env` 파일 수정
- ✅ `config/*.php` 파일 수정
- ✅ 서비스 프로바이더 변경
- ✅ 미들웨어 추가/삭제

**재시작 불필요**:
- ❌ Blade 뷰 파일 수정 (HMR 지원)
- ❌ React 컴포넌트 수정 (Vite HMR)
- ❌ CSS/JS 파일 수정 (Vite HMR)
- ❌ 마이그레이션 파일 생성

## 📊 캐시 모니터링 보고서

캐시 관리 완료 후 보고:

```
🛡️ Laravel 캐시 상태 보고

📁 캐시 파일 현황:
- config.php: 삭제됨 ✅
- routes-v7.php: 존재 (정상)
- services.php: 삭제됨 ✅

⚙️ 현재 설정:
- APP_ENV: local
- DB_CONNECTION: pgsql_local
- CACHE_STORE: file

🔄 실행한 작업:
1. php artisan config:clear ✅
2. php artisan cache:clear ✅
3. 캐시 상태 검증 ✅

📋 다음 조치:
1. 서버 재시작 (Ctrl+C → php artisan serve)
2. 브라우저에서 기능 테스트
3. 문제 재발 시 env-health Skill 실행

💡 팁:
- 개발 중에는 `php artisan serve`만 사용 (캐시 비활성화)
- `php artisan config:cache`는 프로덕션 배포 시에만 사용
```

## 🚨 프로덕션 환경 주의사항

### 프로덕션에서 캐시 관리

**절대 금지**:
- ❌ `php artisan optimize:clear` (성능 저하!)
- ❌ 캐시 없이 운영 (매우 느림)

**올바른 방법**:
```bash
# 설정 변경 후
php artisan config:cache   # 새 캐시 생성
php artisan route:cache     # 라우트 캐시 재생성
php artisan view:cache      # 뷰 캐시 재생성

# 프로세스 재시작 (Railway/서버)
# Railway는 자동 재시작됨
```

## 🎓 캐시 메커니즘 이해

### Laravel 캐시 우선순위

1. **Cached Config 존재 시**:
   ```
   bootstrap/cache/config.php 사용
   → .env 파일 무시!
   → config/*.php도 무시!
   ```

2. **Cached Config 없으면**:
   ```
   .env 로드 → config/*.php 로드 → 런타임 설정 생성
   ```

### 캐시 생성 명령어

**개발 환경**: 사용 금지!
```bash
php artisan config:cache    # ❌ .env 무시됨
php artisan route:cache     # ❌ 라우트 고정됨
php artisan view:cache      # ❌ 뷰 변경 무시됨
```

**프로덕션**: 성능 향상
```bash
php artisan optimize        # ✅ 모든 캐시 생성
# = config:cache + route:cache + view:cache
```

### 캐시 삭제 vs 재생성

**개발 중**:
```bash
php artisan optimize:clear  # 캐시 삭제만 (재생성 X)
```

**배포 시**:
```bash
php artisan optimize:clear  # 1. 기존 캐시 삭제
php artisan optimize        # 2. 새 캐시 생성
```

## 📚 트러블슈팅 가이드

### 문제: 캐시 클리어했는데도 변화 없음

**체크리스트**:
1. ✅ 서버 재시작 했나요?
2. ✅ 브라우저 캐시 클리어 했나요? (Ctrl+Shift+R)
3. ✅ `.env` 파일이 올바른 위치에 있나요?
4. ✅ Vite 개발 서버도 재시작 했나요? (`npm run dev`)

**최종 해결책**:
```bash
# 1. 모든 서버 종료
taskkill /F /IM php.exe
taskkill /F /IM node.exe

# 2. 캐시 완전 삭제
php artisan optimize:clear
rm -rf bootstrap/cache/*.php
rm -rf storage/framework/cache/*
rm -rf storage/framework/views/*

# 3. 재시작
php artisan serve
npm run dev
```

### 문제: "Class config does not exist" 오류

**원인**: 캐시 파일이 손상됨

**해결**:
```bash
# 1. 캐시 파일 완전 삭제
rm -f bootstrap/cache/config.php

# 2. Composer autoload 재생성
composer dump-autoload

# 3. 캐시 재생성 (프로덕션만)
php artisan config:cache
```

## 🎯 학습 포인트

이 Skill을 통해 배운 핵심:

1. **Laravel 캐시는 양날의 검**:
   - 프로덕션: 성능 ⬆️ (필수)
   - 개발: 디버깅 ⬇️ (사용 금지)

2. **설정 변경 후 3단계**:
   1. 캐시 클리어
   2. 서버 재시작
   3. 검증

3. **언제 캐시 의심?**:
   - ".env 바꿨는데 변화 없음"
   - "예전 DB로 연결 시도"
   - "설정 수정이 반영 안됨"

**다음에 비슷한 문제 발생 시**:
1. `php artisan optimize:clear` 실행
2. 서버 재시작 (Ctrl+C → php artisan serve)
3. 그래도 안되면 `env-health` Skill 호출
