---
name: version-updater
description: |
  SEMO 패키지 버전 체크 및 업데이트 알림. Use when:
  (1) 새 세션 시작 시 자동 체크, (2) 수동 버전 확인 요청,
  (3) SEMO 업데이트 실행.
tools: [Bash, Read]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: version-updater 호출` 시스템 메시지를 첫 줄에 출력하세요.

# Version Updater Skill

> SEMO 패키지 버전 체크 및 업데이트 지원

## Purpose

모든 SEMO 패키지에서 공통으로 사용되는 버전 관리 및 무결성 검증:

1. **새 세션 시작 시** 자동 버전 체크 + 무결성 검증
2. **업데이트 가능 시** 사용자에게 알림
3. **업데이트 실행** 지원
4. **무결성 검증** 구조 및 동기화 상태 확인

## 무결성 검증 흐름 (4-Phase)

```text
[세션 시작] → version-updater 호출
    ↓
Phase 1: 버전 체크
    ↓
Phase 2: 구조 검증 (semo-architecture-checker --check-only)
    ↓
Phase 3: 동기화 검증 (package-sync --check-only) ※ semo-core 환경만
    ↓
Phase 4: 메모리 복원 (skill:memory sync) ※ .claude/memory/ 존재 시만
    ↓
[무결성 리포트 출력]
```

## 🔴 버전 비교 필수 규칙

**"최신 버전이야?" 질문에 대한 응답 프로세스**:

1. 로컬 VERSION 파일 읽기
2. 원격 저장소 VERSION 조회 (gh api)
3. 두 버전 비교
4. 결과 출력

❌ 로컬 버전만 읽고 "최신입니다" 응답 금지
✅ 반드시 로컬과 원격 버전을 비교한 후 결과 출력

## Output Format

### 업데이트 가능 시

```markdown
[SEMO] Skill: version-updater 호출

## 📦 SEMO 업데이트 알림

| 패키지 | 현재 버전 | 최신 버전 | 상태 |
|--------|----------|----------|------|
| semo-core | 1.2.0 | 1.3.0 | ⬆️ 업데이트 가능 |
| semo-meta | 0.22.2 | 0.22.2 | ✅ 최신 |

**업데이트하려면**: "SEMO 업데이트해줘"
```

## References

- [Update Process](references/update-process.md) - 상세 업데이트 절차
- [Integrity Check](references/integrity-check.md) - 4-Phase 무결성 검증 상세
