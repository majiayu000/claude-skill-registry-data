---
name: semo-architecture-checker
description: |
  .claude 디렉토리 구조 검증 및 자동 수정. Use when:
  (1) SEMO 업데이트 후 무결성 체크, (2) 심링크 깨짐 의심 시,
  (3) version-updater에서 자동 호출, (4) 새 세션 시작 시.
tools: [Bash, Read]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: semo-architecture-checker 호출` 시스템 메시지를 첫 줄에 출력하세요.

# semo-architecture-checker Skill

> .claude 디렉토리 구조 검증 및 자동 수정

## 호출 모드

| 모드 | 동작 | 사용 상황 |
|------|------|----------|
| (기본) | 검증 + 자동 수정 | 수동 호출, 업데이트 후 |
| `--check-only` | 검증만 수행, 수정 안함 | version-updater Phase 2에서 호출 |

### --check-only 모드

검증만 수행하고 자동 수정하지 않습니다:

**출력 포맷** (version-updater 파싱용):

```markdown
[SEMO] Skill: semo-architecture-checker --check-only 실행

## 구조 검증 결과

| 항목 | 상태 | 비고 |
|------|------|------|
| semo-core | ✅ | 존재 |
| semo-{pkg} | ✅ | semo-pm |
| CLAUDE.md | ✅ | 심링크 유효 |
| _shared | ✅ | semo-core/_shared |
| agents/ | ⚠️ | 깨진 심링크 2개 |
| skills/ | ✅ | 8 symlinks |
| commands/SEMO | ❌ | .merged 마커 누락 |

**결과**: ⚠️ 문제 발견 (자동 수정 필요)
```

**결과 상태**:

- `✅ 구조 정상` - 모든 검증 통과
- `⚠️ 문제 발견` - 수정 필요 (version-updater가 기본 모드로 재호출 결정)

## Purpose

SEMO가 설치된 `.claude` 디렉토리의 구조를 검증하고, 문제 발견 시 자동으로 수정합니다.

## Trigger

- `/SEMO:health` 명령어
- `version-updater` 업데이트 완료 후 자동 호출
- "심링크 확인", ".claude 확인", "SEMO 상태" 키워드

## Workflow

### 1. 패키지 감지

```bash
# 설치된 모든 패키지 감지
INSTALLED_PKGS=()
for p in po next qa meta pm backend infra design; do
    [ -d ".claude/semo-$p" ] && INSTALLED_PKGS+=("$p")
done

# 첫 번째 패키지를 기본으로 사용
PKG="${INSTALLED_PKGS[0]:-}"
```

### 2. 검증 항목

| 항목 | 검증 | 수정 |
|------|------|------|
| semo-core | 디렉토리 존재 | - |
| semo-{pkg} | 디렉토리 존재 | - |
| CLAUDE.md | 심링크 유효성 | 재생성 |
| _shared | 심링크 유효성 (semo-core/_shared) | 재생성 |
| agents/ | .merged 마커 + 심링크 + **누락 감지** | 재생성 + 추가 |
| skills/ | .merged 마커 + 심링크 + **누락 감지** | 재생성 + 추가 |
| commands/SEMO/ | .merged 마커 + 심링크 + **누락 감지** | 재생성 + 추가 |

### 3. 검증 실행

```bash
# 깨진 심링크 탐지
find .claude -type l ! -exec test -e {} \; -print 2>/dev/null

# .merged 마커 확인
[ -f ".claude/agents/.merged" ] && echo "agents: OK" || echo "agents: MISSING"
[ -f ".claude/skills/.merged" ] && echo "skills: OK" || echo "skills: MISSING"
[ -f ".claude/commands/SEMO/.merged" ] && echo "commands/SEMO: OK" || echo "commands/SEMO: MISSING"

# _shared 심링크 확인 (semo-core/_shared 참조용)
if [ -L ".claude/_shared" ]; then
  target=$(readlink ".claude/_shared")
  [ "$target" = "semo-core/_shared" ] && echo "_shared: OK" || echo "_shared: WRONG_TARGET ($target)"
elif [ -d ".claude/_shared" ]; then
  echo "_shared: DIRECTORY (should be symlink)"
else
  echo "_shared: MISSING"
fi

# 🔴 누락 심링크 감지 (NEW - Issue #7)
# semo-core와 semo-{pkg}의 컴포넌트가 .claude/{dir}에 모두 심링크되어 있는지 확인
for skill in .claude/semo-core/skills/*/; do
  name=$(basename "$skill")
  [ ! -e ".claude/skills/$name" ] && echo "skills: MISSING $name"
done
```

### 4. 자동 수정

문제 발견 시 `install-sax.sh`와 동일한 로직으로 수정:

```bash
# CLAUDE.md 수정
rm -f ".claude/CLAUDE.md"
ln -s "semo-$PKG/CLAUDE.md" ".claude/CLAUDE.md"

# _shared 심링크 수정
rm -rf ".claude/_shared"
ln -s "semo-core/_shared" ".claude/_shared"

# 병합 디렉토리 수정
# → references/fix-logic.md 참조
```

### 5. 결과 보고

```markdown
## .claude 디렉토리 검증 결과

| 항목 | 상태 | 비고 |
|------|------|------|
| 패키지 | ✅ | semo-pm |
| CLAUDE.md | ✅ | semo-pm/CLAUDE.md |
| _shared | ✅ | semo-core/_shared |
| agents/ | ⚠️ → ✅ | 심링크 2개 재생성 |
| skills/ | ✅ | 8 symlinks |
| commands/SEMO | ❌ → ✅ | 디렉토리 생성 + 4 symlinks |

**결과**: 2개 항목 자동 수정됨
```

## 🔴 세션 재시작 권장

> **심링크 재설정 후에는 세션 재시작을 권장합니다.**

### 재시작이 필요한 경우

| 상황 | 재시작 필요 | 이유 |
|------|-------------|------|
| 심링크 디렉토리 → 실제 디렉토리 변환 | ✅ 권장 | Claude Code가 캐시한 경로 무효화 |
| 새 skill/agent 심링크 추가 | ✅ 권장 | 새 컴포넌트 인식 필요 |
| 깨진 심링크 수정 | ⚠️ 선택 | 기존 캐시에 따라 다름 |
| .merged 마커만 추가 | ❌ 불필요 | 경로 변경 없음 |

### 결과 메시지에 안내 포함

심링크가 재설정된 경우 아래 안내를 출력:

```markdown
⚠️ **세션 재시작 권장**

심링크 구조가 변경되었습니다. Claude Code가 변경된 경로를 인식하도록
**새 세션을 시작**하는 것을 권장합니다.

재시작 방법: Claude Code 창을 닫고 다시 열기
```

### 판단 기준

```bash
# 심링크 재설정 여부 감지
SYMLINK_CHANGED=false

# 심링크 디렉토리가 실제 디렉토리로 변환된 경우
if [ "$dir_was_symlink" = true ]; then
  SYMLINK_CHANGED=true
fi

# 새 심링크가 생성된 경우
if [ $new_symlinks_count -gt 0 ]; then
  SYMLINK_CHANGED=true
fi
```

## 🔴 다중 패키지 감지

> **하나의 프로젝트에는 하나의 SEMO 패키지만 지원됩니다.**

### 검증 로직

```bash
INSTALLED_PKGS=()
for p in po next qa meta pm backend infra design; do
    [ -d ".claude/semo-$p" ] && INSTALLED_PKGS+=("$p")
done

if [ ${#INSTALLED_PKGS[@]} -gt 1 ]; then
    # 다중 패키지 경고 출력
fi
```

### 출력 형식

다중 패키지가 감지된 경우:

```markdown
🔴 **다중 패키지 설치 감지**

설치된 패키지: semo-next, semo-design

⚠️ 하나의 프로젝트에는 하나의 SEMO 패키지만 권장됩니다.
충돌로 인해 일부 기능이 정상 동작하지 않을 수 있습니다.

**해결 방법**: `./install-sax.sh {원하는패키지} --force`
```

### 결과 테이블에 포함

다중 패키지 감지 시 검증 결과 테이블 상단에 경고 추가:

| 항목 | 상태 | 비고 |
|------|------|------|
| 다중 패키지 | 🔴 | semo-next, semo-design 동시 설치 |
| semo-core | ✅ | 존재 |
| ... | ... | ... |

## 🔴 Windows 환경 지원

> **Windows에서는 심링크 생성에 제약이 있습니다.**

### 자동 폴백 동작

| 상황 | 동작 |
|------|------|
| 심링크 생성 성공 | 정상 심링크 사용 |
| 심링크 생성 실패 | 파일/디렉토리 복사로 대체 |

### 결과 메시지

심링크 실패 시 아래와 같이 표시됩니다:

```markdown
| 항목 | 상태 | 비고 |
|------|------|------|
| CLAUDE.md | ⚠️ | 복사됨 (Windows) |
| agents/ | ⚠️ | 3개 복사됨 |

⚠️ **Windows 환경 알림**

일부 심링크가 파일 복사로 대체되었습니다.
원본 파일 수정 시 수동으로 다시 설치해야 합니다.
```

### 심링크 사용을 원할 경우

1. **개발자 모드 활성화**: Windows 설정 → 개발자용 → 개발자 모드 ON
2. **또는 관리자 권한 실행**: 터미널을 관리자 권한으로 실행
3. **재설치**: `./install-sax.sh {패키지} --force`

### 복사 모드의 제약

| 항목 | 심링크 | 복사 |
|------|--------|------|
| 원본 수정 시 자동 반영 | ✅ | ❌ |
| 디스크 공간 | 절약 | 추가 사용 |
| SEMO 업데이트 후 | 자동 반영 | 재설치 필요 |

## References

- [Fix Logic](references/fix-logic.md) - 자동 수정 로직 상세
