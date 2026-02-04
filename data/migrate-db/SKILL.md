---
name: migrate-db
description: |
  Prisma/SQL 마이그레이션 관리. Use when:
  (1) 스키마 변경, (2) 마이그레이션 생성/적용, (3) DB 동기화,
  (4) 마이그레이션 상태 확인, (5) 롤백 필요 시.
tools: [Bash, Read, Grep]
model: inherit
triggers:
  - 마이그레이션
  - 스키마 변경
  - DB 동기화
  - prisma migrate
  - 테이블 추가
---

> **호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: migrate-db 호출 - {service_name}` 시스템 메시지를 첫 줄에 출력하세요.

# Migrate DB Skill

> Prisma/SQL 마이그레이션 안전 관리

## 지원 기술 스택

| 스택 | 도구 | 서비스 예시 |
|------|------|------------|
| **Prisma** | `prisma migrate` | ms-notifier, ms-scheduler, ms-ledger, ms-allocator |
| **SQL** | 수동 마이그레이션 | ms-gamer (Go) |
| **Supabase** | Supabase CLI | ms-collector |

## 워크플로우

### Phase 0: 환경 확인 (NON-NEGOTIABLE)

```bash
# 현재 브랜치 확인
git branch --show-current

# 미커밋 변경사항 확인
git status --porcelain

# 기술 스택 감지
if [ -f "prisma/schema.prisma" ]; then
  MIGRATION_TOOL="prisma"
elif [ -f "go.mod" ]; then
  MIGRATION_TOOL="sql"
else
  MIGRATION_TOOL="unknown"
fi
echo "마이그레이션 도구: $MIGRATION_TOOL"
```

> **경고**: 프로덕션 환경에서는 반드시 백업 후 진행하세요.

---

### Phase 1: 마이그레이션 상태 확인

#### Prisma

```bash
# 현재 마이그레이션 상태
npx prisma migrate status

# 스키마 유효성 검사
npx prisma validate

# 스키마 포맷 확인
npx prisma format --check
```

#### SQL (Go 서비스)

```bash
# 마이그레이션 파일 목록
ls -la db/migrations/ 2>/dev/null || ls -la migrations/

# 적용된 마이그레이션 확인 (schema_migrations 테이블)
psql -c "SELECT * FROM schema_migrations ORDER BY version DESC LIMIT 10"
```

---

### Phase 2: 마이그레이션 생성

#### Prisma - 개발 환경

```bash
# 스키마 변경 후 마이그레이션 생성
npx prisma migrate dev --name {migration_name}

# 예시: 새 필드 추가
npx prisma migrate dev --name add_user_email
```

#### Prisma - 프로덕션 환경

```bash
# 마이그레이션 파일만 생성 (적용하지 않음)
npx prisma migrate dev --create-only --name {migration_name}

# 생성된 SQL 검토 후 수동 적용
cat prisma/migrations/{timestamp}_{name}/migration.sql
```

#### SQL 수동 마이그레이션

```bash
# 마이그레이션 파일 생성
TIMESTAMP=$(date +%Y%m%d%H%M%S)
touch db/migrations/${TIMESTAMP}_{migration_name}.sql

# 예시 내용
cat << 'EOF' > db/migrations/${TIMESTAMP}_add_user_email.sql
-- Up
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Down
ALTER TABLE users DROP COLUMN email;
EOF
```

---

### Phase 3: 마이그레이션 적용

#### Prisma

```bash
# 개발 환경
npx prisma migrate dev

# 프로덕션 환경 (CI/CD에서 사용)
npx prisma migrate deploy
```

#### SQL (golang-migrate)

```bash
# 적용
migrate -path db/migrations -database "$DATABASE_URL" up

# 특정 버전까지만 적용
migrate -path db/migrations -database "$DATABASE_URL" up 1
```

---

### Phase 4: 롤백 (주의 필요)

> **경고**: 롤백은 데이터 손실을 유발할 수 있습니다. 반드시 백업 후 진행하세요.

#### Prisma

```bash
# Prisma는 직접적인 롤백을 지원하지 않음
# 대신 새 마이그레이션으로 변경 사항 되돌리기

# 1. 되돌릴 스키마 변경 작성
# 2. 새 마이그레이션 생성
npx prisma migrate dev --name revert_{previous_migration}
```

#### SQL (golang-migrate)

```bash
# 마지막 마이그레이션 롤백
migrate -path db/migrations -database "$DATABASE_URL" down 1

# 모든 마이그레이션 롤백 (위험!)
# migrate -path db/migrations -database "$DATABASE_URL" down
```

---

### Phase 5: Prisma 클라이언트 재생성

```bash
# 스키마 변경 후 클라이언트 재생성
npx prisma generate

# 타입 확인
npx tsc --noEmit
```

## 출력 포맷

### 마이그레이션 성공

```markdown
[SEMO] Skill: migrate-db 호출 - ms-{service}

=== 마이그레이션 결과 ===

## 환경
- 서비스: ms-{service}
- 도구: Prisma
- 환경: development

## 실행 내역
| 단계 | 상태 | 상세 |
|------|------|------|
| 상태 확인 | ✅ | 대기 중인 마이그레이션 1건 |
| 스키마 검증 | ✅ | 유효 |
| 마이그레이션 적용 | ✅ | 20250122_add_user_email |
| 클라이언트 생성 | ✅ | @prisma/client 재생성 |

## 적용된 마이그레이션
- `20250122143000_add_user_email`
  - ALTER TABLE `users` ADD COLUMN `email` VARCHAR(255)

## 다음 단계
1. `npx tsc --noEmit`로 타입 확인
2. 테스트 실행: `npm test`
3. 커밋: `git add prisma/ && git commit -m "db: add user email field"`
```

### 마이그레이션 실패

```markdown
[SEMO] Skill: migrate-db 호출 - ms-{service}

=== 마이그레이션 실패 ===

## 오류
```
Error: P3009
migrate found failed migrations in the target database.
```

## 원인
- 이전 마이그레이션이 실패한 상태로 남아있음

## 해결 방법
1. 실패한 마이그레이션 확인:
   ```bash
   npx prisma migrate status
   ```

2. 수동으로 실패한 마이그레이션 해결:
   ```bash
   npx prisma migrate resolve --rolled-back {migration_name}
   ```

3. 재시도:
   ```bash
   npx prisma migrate dev
   ```
```

## 안전 체크리스트

### 개발 환경

- [ ] 로컬 DB 백업 불필요 (재생성 가능)
- [ ] 스키마 변경 검토
- [ ] 테스트 통과 확인

### 스테이징/프로덕션 환경

- [ ] DB 백업 완료
- [ ] 마이그레이션 SQL 검토
- [ ] 롤백 계획 수립
- [ ] 다운타임 영향도 확인
- [ ] 팀 공유 및 승인

## 서비스별 스키마 정보

| 서비스 | 스키마명 | Prefix | 주요 테이블 |
|--------|---------|--------|------------|
| ms-notifier | notifier | nf_ | notifications, channels, jobs |
| ms-scheduler | scheduler | sc_ | schedules, executions, job_queue |
| ms-ledger | ledger | lg_ | accounts, transactions, subscriptions |
| ms-allocator | allocator | al_ | tracked_subjects, snapshots, aggregates |
| ms-gamer | public | ladder_ | round, bet, pattern |

## Related Skills

- [setup-prisma](../setup-prisma/SKILL.md) - Prisma 초기 설정
- [debug-service](../debug-service/SKILL.md) - DB 연결 디버깅

## References

- [Prisma Migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [golang-migrate](https://github.com/golang-migrate/migrate)
- [Microservices Context](/.claude/memory/microservices.md) - 서비스별 스키마 정보
