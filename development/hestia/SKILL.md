---
name: hestia
description: >
  코드베이스 청소 + 위생 점검 (헤스티아 — 화로의 여신). Dead Code 탐지,
  미사용 export/의존성/파일 제거, LOC 측정, 의도적 단순화 마커(// minimal:)
  부채 장부, 코드 건강도 보고.
  "정리해줘", "dead code", "코드 위생", "쓸모없는 코드", "단순화 부채" 요청에 실행.
  /hestia로 실행.
---

# Hestia (헤스티아) — 화로의 여신, 코드 위생 관리자

> **헤스티아(Hestia)**: 올림포스 12신 중 하나, 화로와 가정의 여신.
> 화로를 깨끗이 유지하듯, 코드베이스에서 쓸모없는 것을 찾아 치운다.
> 조용하지만 빠지면 집이 무너진다.
>
> **argos가 "빠진 걸 찾고", hestia는 "남은 걸 치운다."**

## Quick Start

```
/hestia                         # 전체 스캔 (기본 = 보고만, 삭제 안 함)
/hestia scan                    # 스캔만 (보고만, 삭제 안 함)
/hestia clean                   # 스캔 + 자동 삭제
/hestia src/                    # 특정 디렉토리만
/hestia --dry-run               # 삭제 대상 미리보기 (실행 안 함)
```

**공식 호출명:** `/hestia` (별칭: `헤스티아`, `코드 정리`, `dead code`)

## 파이프라인 위치

```
/agent-team → /argos → /minos → /hestia → /clio
  구현          감리      QA      정리       기록
                                  ↑
                          "argos/minos 통과 후, clio 기록 전"
```

**또는 독립 실행** — 언제든 `/hestia`로 현재 코드베이스 점검 가능.

---

## Phase 1: 측정 (Before)

변경 전 현재 상태를 측정합니다. 측정 없는 정리는 감이지 사실이 아닙니다.

```bash
# 스캔 범위 — 인수로 경로를 주면 그 경로만, 없으면 프로젝트 전체.
# src/ app/ lib/로 고정하지 않는다: services/, packages/, apps/, 언어별 레이아웃에도 코드가 있다.
# rg는 .gitignore를 존중하므로 node_modules와 빌드 산출물은 대부분 자동 제외된다.
SCAN_ROOT="${1:-.}"
SRC_TYPES="-t ts -t js -t py -t java -t csharp -t go -t rust -t kotlin -t swift -t php -t ruby"
SKIP_BUILD="-g !**/node_modules/** -g !**/dist/** -g !**/build/** -g !**/out/** -g !**/vendor/** -g !**/.venv/** -g !**/*.min.*"
SKIP_TEST="-g !**/*.test.* -g !**/*.spec.* -g !**/*_test.* -g !**/test_*.* -g !**/__tests__/** -g !**/tests/**"

# 총 LOC (프로덕션 코드만, 테스트 제외)
rg --files -0 "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD $SKIP_TEST | xargs -0 wc -l 2>/dev/null | tail -1

# 파일 수
rg --files "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD $SKIP_TEST | wc -l

# 책임 분리 검토용 대형 파일 (wc 합계 줄은 제거)
rg --files -0 "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD $SKIP_TEST | xargs -0 wc -l 2>/dev/null \
  | sort -nr | sed '1d' | head -20
```

```
📏 현재 상태:
  LOC: {N}줄
  파일: {M}개
  책임 분리 검토 대상 파일: {K}개
```

---

## Phase 2: 스캔 (Dead Code 탐지)

### 2-1. 미사용 Export

```bash
# TypeScript/JavaScript — knip 권장 (미사용 export·파일·의존성을 한 번에, --fix로 자동 제거)
# ts-prune/depcheck/unimported는 2025년 archive/maintenance → knip이 통합 후속
npx knip 2>/dev/null | head -40

# 레거시 단일 목적 대안 (export만): npx ts-prune | grep -v "used in module"
# 결과 예시:
# src/utils/format.ts:15 - formatCurrency (unused)
```

### 2-2. 미사용 의존성

```bash
# JS/TS는 knip(2-1)이 의존성도 함께 탐지. depcheck는 레거시 대안 (2025 archive)
npx depcheck 2>/dev/null | head -20

# Python
pip-extra-reqs --ignore-requirement=dev "$SCAN_ROOT" 2>/dev/null

# 결과 예시:
# Unused dependencies: lodash, moment, classnames
# Missing dependencies: (none)
```

### 2-3. 미사용 파일

```bash
# JS/TS는 knip(2-1)이 미사용 파일도 함께 탐지. unimported는 레거시 대안 (knip으로 대체)
npx unimported 2>/dev/null | head -20

# 결과 예시:
# src/components/OldButton.tsx - not imported anywhere
# src/utils/deprecated.ts - not imported anywhere
```

### 2-4. Dead Code 마커

```bash
# 삭제 예고된 코드
rg -n --no-heading "@deprecated|TODO.*remove|TODO.*delete|HACK|FIXME|XXX" \
  "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD | head -20

# 호환성 코드
rg -n --no-heading -i "backwards.*compat|legacy.*shim|// old|// deprecated" \
  "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD | head -20
```

### 2-5. 빈 파일/폴더

```bash
# rg는 빈 파일을 나열하지 않으므로 find를 쓰되 스캔 루트와 제외 디렉터리를 맞춘다
find "$SCAN_ROOT" \( -name node_modules -o -name .git -o -name dist -o -name build \) -prune -o -empty -type f -print 2>/dev/null
find "$SCAN_ROOT" \( -name node_modules -o -name .git \) -prune -o -empty -type d -print 2>/dev/null
```

### 2-6. 사전 미등재 도메인 식별자 (도메인사전 있을 때만)

`docs/domain-dictionary.md`가 있으면 코드의 클래스/함수/타입명 중 사전에 없는 도메인 식별자를 보고합니다. 삭제 대상 ❌ — 사전 갱신 트리거일 뿐.

```bash
# 대문자로 시작하는 식별자 추출 (도메인 명사 후보)
rg -n --no-heading "^(export\s+)?(class|interface|type|enum)\s+[A-Z]\w+" \
  "$SCAN_ROOT" -t ts $SKIP_BUILD \
  | grep -oE "(class|interface|type|enum)\s+[A-Z]\w+" | sort -u
```

각 식별자에 대해:
- 사전 영문 식별자 목록과 대조
- 사전에 없으면 → 보고 (도메인 신규 용어인지 / 기술 인프라 용어인지 사용자 판단)

**출력 분류:**
- 도메인 신규 용어 (예: `class Voucher`) → 사전 갱신 권장
- 기술 인프라 용어 (예: `class CacheManager`) → 사전 외 정상

기술 인프라 용어 휴리스틱: `Manager`, `Handler`, `Factory`, `Builder`, `Cache`, `Queue`, `Worker`, `Pool`, `Adapter` 같은 GoF/구조 패턴 접미사가 붙으면 인프라로 분류.

### 2-7. 의도적 단순화 마커 (minimal 부채 장부)

Hestia가 소유하는 `// minimal: <상한> — <업그레이드 시점>` 규약을 사용합니다.
`상한`은 현재 구현이 의도적으로 감수하는 제약이고, `업그레이드 시점`은 교체를 검토할 수치·상태 조건입니다.
마커를 수확해 부채 장부로 보고합니다. **삭제 대상 ❌** — 의도된 지름길의 추적 장부일 뿐,
"later means never"로 썩는 것을 막는 게 목적입니다.

```bash
# 주석 스타일별 minimal 마커 수확 (// # -- <!--)
# 마커는 소스 루트 밖(scripts/, services/, packages/, 언어별 레이아웃)에도 달리므로
# 데드코드 스캔과 달리 프로젝트 전체를 훑는다. rg는 .gitignore를 존중한다.
rg -n --no-heading "(?://|#|--|<!--)\s*minimal:" \
  "$SCAN_ROOT" $SRC_TYPES -t sql -t html $SKIP_BUILD \
  | head -30
```

장부 형식으로 보고:

```
📒 단순화 부채 장부 ({N}건)
  1. src/api/orders.ts:42 — 전역 락 | 업그레이드: 처리량 문제 시 계좌별 락
  2. app/report.py:88 — O(n²) 스캔 | 업그레이드: 1만 행 초과 시 인덱스 조인
```

판단 기준:
- 상한 조건이 이미 도달한 것으로 보이는 마커 (예: "1만 행 초과 시" — 현재 데이터가 초과) → ⚠️ **업그레이드 권장** 표시
- 마커에 상한/업그레이드 시점이 없는 것 → 형식 보완 권장 (`<상한> — <시점>`)
- 업그레이드 실행 여부는 사용자 결정 — hestia는 장부만 만든다

### 스캔 결과 보고

```
🔍 Hestia 스캔 결과
━━━━━━━━━━━━━━━━━━━
  미사용 export:     {N}개
  미사용 의존성:     {N}개
  미사용 파일:       {N}개
  @deprecated 마커:  {N}개
  빈 파일/폴더:      {N}개
  사전 미등재 도메인: {N}개  (사전 있을 때만)
  minimal 부채 장부:  {N}건  (보고 전용, 삭제 안 함)
  ──────────────────
  총 정리 대상:      {N}건
```

**`scan` 모드면 여기서 종료.** `clean` 모드면 Phase 3으로 진행.

---

## Phase 3: 정리 (Clean)

### 삭제 전 안전 체크

| 확인 | 방법 | 불합격 시 |
|------|------|----------|
| git 상태 깨끗한가? | `git status --porcelain` | 커밋 먼저 |
| 테스트 통과하나? | 프로젝트 테스트 명령 실행 | 테스트 먼저 수정 |
| 브랜치 분리? | 현재 브랜치 확인 | 정리용 브랜치 생성 권장 |

### 삭제 순서 (안전한 것부터)

```
1단계: 빈 파일/폴더 삭제           (위험도: 없음)
2단계: 미사용 의존성 제거           (위험도: 낮음, package.json만)
3단계: 미사용 파일 삭제             (위험도: 낮음, import 체인에 없음)
4단계: 미사용 export 삭제           (위험도: 중간, 동적 import 가능성)
5단계: @deprecated 코드 제거        (위험도: 중간, 외부 사용자 확인 필요)
```

### 각 삭제 후 검증

```bash
# 삭제할 때마다
# 1. 타입 체크
npx tsc --noEmit 2>&1 || echo "타입 에러 발생 — revert"

# 2. 테스트
npm test 2>&1 || echo "테스트 실패 — revert"

# 실패 시 즉시 revert
git checkout -- {삭제한 파일}
```

**원칙: 삭제 → 검증 → 실패 시 되돌리기.** 한꺼번에 삭제하지 않고, 단계별로 검증합니다.

---

## Phase 4: 측정 (After) + 보고

```bash
# 동일 명령 재실행
rg --files -0 "$SCAN_ROOT" $SRC_TYPES $SKIP_BUILD $SKIP_TEST | xargs -0 wc -l 2>/dev/null | tail -1
```

### 최종 보고

```
🏠 Hestia 정리 완료
━━━━━━━━━━━━━━━━━━━━━
  Before: {N} LOC, {M} files
  After:  {N'} LOC, {M'} files
  Delta:  -{차이} LOC (-{퍼센트}%), -{파일} files

  삭제 내역:
    🗑️ 미사용 export {N}개 제거
    🗑️ 미사용 의존성 {N}개 제거
    🗑️ 미사용 파일 {N}개 삭제
    🗑️ @deprecated 코드 {N}건 제거
    ⏭️ 건너뜀 {N}건 (동적 참조 가능성)

  테스트: {PASS / 삭제 전으로 revert된 항목 N건}

다음 단계:
  /commit     → 정리 결과 커밋
  /clio       → 최종 기록
```

---

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `scan` | 스캔만 (삭제 안 함) | 기본 모드 |
| `clean` | 스캔 + 자동 삭제 | - |
| `--dry-run` | 삭제 대상 미리보기 | false |
| `--skip-deps` | 의존성 검사 건너뜀 | false |
| `--skip-tests` | 삭제 후 테스트 검증 건너뜀 (비권장) | false |

---

## 하지 않는 것

- **리팩토링 안 함** — 로직 변경, 함수 분리, 구조 개선은 범위 밖
- **마이그레이션 안 함** — 라이브러리 교체는 `/deprecate`
- **기능 추가 안 함** — 누락된 기능 구현은 `/argos` Healer
- **설계 판단 안 함** — "이 기능이 필요한가?"는 사용자 결정

**헤스티아는 오직 "아무도 안 쓰는 것을 치우는 것"만 합니다.**

---

## Related Files

| 파일 | 역할 |
|------|------|
| `skills/deprecation-and-migration/SKILL.md` | 라이브러리 교체/마이그레이션 (별도 스킬) |
| `skills/argos/SKILL.md` | 감리 — 누락 탐지 + Healer (채우기) |
| `skills/clio/SKILL.md` | 최종 기록 (정리 후 기록) |
| `skills/code-reviewer/SKILL.md` | 코드 품질 리뷰 |
