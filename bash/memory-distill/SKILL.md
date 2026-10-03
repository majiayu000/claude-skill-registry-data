---
name: memory-distill
description: >
  memory/{gotchas,learned}/observations.jsonl raw 관찰을 정제 .md로 변환하는
  사용자 트리거 스킬. 핸드오프 의존이 약할 때 의지로 호출. Dreaming-like
  rebuild 모드 지원 (기존 정제 .md + 새 관찰 통합 + 중복/모순 제거).
  /memory-distill로 실행. 또한 핸드오프 자동 정제와 동일 로직을 공유.
  대상은 프로젝트 루트 memory/ 전용 — 호스트 네이티브 메모리나 Antigravity /learn과 무관.
---

# Memory Distill — observations.jsonl → 정제 .md

> 핸드오프가 충분히 자주 발동되지 않을 때, 사용자 의지로 raw 관찰을 정제 .md로 굳힙니다.
> append-only 누적의 부풀음을 막기 위해 **rebuild 모드**로 기존 정제 .md를 통합합니다.

## Antigravity `/learn` 경계

Antigravity 네이티브 `/learn`은 현재 대화의 교정·선호를 Rules 또는 Skill로 정리하는 빠른 학습 경로입니다.
최근 세션의 한두 교정을 런타임 규칙으로 남기는 요청은 `/learn`이 우선입니다. 이 모듈은 여러 세션에 걸쳐
프로젝트 루트에 쌓인 `observations.jsonl`을 클러스터링하고, 중복·모순을 제거하며, 기존 정제 파일까지
재구성하는 저장소 수준 유지보수를 소유합니다. `/learn`을 프로그램적으로 호출하거나 그 결과를 이 모듈의
rebuild 증거로 간주하지 않습니다.

## 사용법

```bash
# 스캔 (기본) — 후보만 출력, 파일 미생성
/memory-distill

# 적용 — 새 정제 .md 생성
/memory-distill --apply

# 통째 재구성 — 기존 정제 .md + 새 관찰 통합 + 중복/모순 제거
/memory-distill --rebuild

# 대상 선택
/memory-distill --type gotchas
/memory-distill --type learned

# 시점 필터
/memory-distill --since 2026-04-01
```

### 인자

| 인자 | 기본값 | 설명 |
|------|--------|------|
| `--apply` | off | 후보를 실제 .md 파일로 생성 |
| `--rebuild` | off | 기존 정제 .md까지 함께 재구성 |
| `--type` | `both` | `gotchas`, `learned`, `both` |
| `--since` | (전체) | 해당 ISO 날짜 이후 관찰만 |
| `--min-cluster` | 2 | 그룹핑 최소 관찰 수 |

`--rebuild`는 `--apply`를 암시합니다.

## 워크플로우

### Phase 1: 입력 수집

```
1. raw 관찰 로드
   ├─ memory/gotchas/observations.jsonl  (event: tool_error | turn_error)
   └─ memory/learned/observations.jsonl  (event: tool_success | turn_success)

2. 기존 정제 로드 (있을 때만)
   ├─ memory/gotchas.md  (단일 카테고리 파일, 22개 정제 항목)
   ├─ memory/gotchas/*.md  (개별 정제 파일, 0~N개)
   ├─ memory/learned.md  (있으면)
   └─ memory/learned/*.md
```

### Phase 2: 그룹핑 (CLI가 직접 수행)

같은 패턴의 관찰을 묶어 클러스터로 만듭니다. 노이즈 줄이기 위해 다음 기준을 활용:

| 신호 | 사용 |
|------|------|
| 같은 `tool` + 유사 `output` 에러 메시지 | 함정 클러스터 |
| 같은 도구 시퀀스 (예: Grep→Read→Edit) | 패턴 클러스터 |
| 같은 `file_path` 영역 반복 실패 | 영역별 함정 |
| 같은 키워드(에러 코드, 함수명) 반복 | 키워드 클러스터 |

`--min-cluster` 미만인 단발 관찰은 무시 (노이즈).

입력이 커서 격리 분석이 유리할 때만 **읽기 전용 클러스터 후보 추출**을 네이티브 역할에 위임합니다: Claude `Explore`, Codex `explorer`, Antigravity `research`, Grok `explore`. 작업자는 스크럽된 관찰만 읽고 후보를 반환하며 파일을 쓰지 않습니다. 별도 `gotcha-analyzer` 이름은 필요하지 않습니다. 모드 판정, archive, 재번호, 파일 쓰기, index/MEMORY 동기화는 이 스킬을 실행한 메인 하네스가 소유합니다. 위임이 없거나 병렬 이득이 없으면 메인 컨텍스트에서 같은 클러스터링을 순차 실행합니다.

### Phase 3: 출력 형식

#### `--scan` (기본): 후보 미리보기

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Memory Distill — 정제 후보 스캔
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  대상         관찰  기존정제  신규클러스터  통합대상
  gotchas      326    22         8           3
  learned      662     0        14           0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /memory-distill --apply 로 적용
  /memory-distill --rebuild 로 통째 재구성
```

#### `--apply`: 신규 정제 .md 생성

```
memory/gotchas/
├── index.md                       (생성 또는 갱신)
├── 001-{slug}.md                  (신규 클러스터)
├── 002-{slug}.md
└── ...

memory/learned/
├── index.md                       (신규 생성)
├── 001-{slug}.md
└── ...
```

#### `--rebuild`: 통째 재구성

기존 정제 .md를 **재배치**합니다. 절대 삭제 X — 다음 절차:

```
1. 기존 .md 백업: memory/{type}/.archive/YYYY-MM-DD-NNN-{slug}.md
2. 기존 + 신규 클러스터를 하나의 후보 풀로 합침
3. 중복/모순 분석:
   - 동일 키워드 + 동일 메시지 → 병합 (날짜 합산, 신뢰도 갱신)
   - 모순 (예: A→B 했더니 됨 vs 안 됨) → 최신 timestamp 우선 + SUPERSEDED 표시
4. 새 NNN 부여하여 .md 재작성
5. index.md 통째 갱신
6. memory/{type}.md 카테고리 파일도 동기화
```

### Phase 4: 정제 .md 형식

```markdown
# {제목 — 키워드 조합}

`tags: keyword1, keyword2, keyword3`        ← 최소 3개
`type: CLI 오답 | 환경 함정 | 워크플로우 패턴 | 검증된 성공`
`date: YYYY-MM-DD`
`source: memory-distill`
`observations: 5`                           ← 클러스터 크기
`confidence: 0.7`                           ← 0.0~1.0
`first_seen: YYYY-MM-DD`
`last_seen: YYYY-MM-DD`

**함정** (gotcha) | **패턴** (learned): 무엇이 잘못되었는지 / 무엇이 효과적이었는지
**해결/적용**: 어떻게 고쳤는지 / 어떻게 재현하는지
**교훈**: 다음에 어떻게 해야 하는지

**관련 관찰** (선택):
- {timestamp1} {tool} — 1줄 요약
- {timestamp2} {tool} — 1줄 요약
```

`confidence`는 통계적 확률이 아니라 관찰량 기반 정제 우선순위입니다.

| 관찰 수 | confidence |
|---------|------------|
| 2 | 0.3 |
| 3-5 | 0.5 |
| 6-10 | 0.7 |
| 11+ | 0.85 |

### Phase 5: 승격 판단 (정제 후)

정제된 각 항목에 대해 상위 계층 승격 후보 여부를 판단해 `--apply`/`--rebuild` 보고서에 표기합니다.
계층: 정제 .md(기본) → 상시 가시(CLAUDE.md 가드레일) → 작업 현장(관련 SKILL.md 내장).
상위 계층은 컨텍스트 예산을 상시 소모하므로 아래 기준으로 선별합니다.

| 유형 | 판단 | 근거 |
|------|------|------|
| 유명/공개 함정 (BOM, cp949, 웹폰트 폴백 등 공개 문서화된 것) | **승격 금지** — 정제 .md 보관만 | T0 스크리닝 실측(2026-07-31): 프런티어 모델이 실행 수준에서 이미 회피(후보 8건 중 7건 발동률 0~20%). 상시 노출은 예산 낭비 |
| 습관 재정의형 (모델이 알면서도 기본 습관·최신 문법이 함정 쪽으로 미는 것) | **상시 가시 후보** | 유일한 스크리닝 생존 유형(Join-Path 3-인수: 리플렉션 지목 3/3인데 실행 발동 3/5). 지식이 아니라 행동 교정이 필요한 함정 |
| 레포 고유형 (공개 문서가 없는 이 시스템 특유의 규약·경로·마커) | **상시 가시 후보** | 모델이 알 수 없는 정보 (예: observations.jsonl delta 판정 — gotcha 058) |
| 경합 제약형 (다른 정당한 규칙이 함정 쪽으로 미는 구조) | **작업 현장 내장 우선** | 발동 지점이 특정 작업에 결박됨 (예: 디자인 정본이 라틴 페어링을 강제하는 맥락의 한글 폰트 함정 — gotcha 041) |
| 판단 애매 | **승격 금지** | 보수적 기본값 — 상시 가시 예산(100줄) 보호 |

승격 실행(가드레일/스킬 편집)은 이 스킬의 범위 밖 — 후보 목록만 보고하고 사용자 확인 후 별도 진행.
근거 데이터: `docs/research/2026-07-31-q1-t0-screening-results.md`

## 보안 / 시크릿 스크럽핑

저장 전 다음 패턴을 `[REDACTED]`로 마스킹:

| 패턴 | 예시 |
|------|------|
| API 키 | `sk-...`, `xoxb-...`, `ghp_...` |
| 토큰 | `Bearer xxx`, `token=xxx` |
| 패스워드 | `password=xxx`, `pwd=xxx` |
| PEM 키 | `-----BEGIN ... PRIVATE KEY-----` |
| AWS | `AKIA...`, `ASIA...` |

`skills/mnemo/scripts/validate_handoff.py`의 SECRET_PATTERNS와 동일 로직을 재사용.

## 기존 시스템과의 관계

| 트리거 | 빈도 | 깊이 | LLM 비용 | 역할 |
|--------|------|------|---------|------|
| Stop 훅 (jsonl append) | 매 응답 | 0 | 0 | 관찰 수집 |
| Stop 훅 (mnemo-status notify) | 임계값 도달 시 | 0 (텍스트 안내) | 0 | 사용자 인지 (`memory/.mnemo-status.md`) |
| **`/memory-distill`** | **사용자 의지** | **풀 정제 + rebuild** | **1회** | **주 정제** |
| 핸드오프 자동 추출 | 컨텍스트 위기 시 | 풀 정제 + 통합 | 1회 | 세션 경계 정제 |

설계 원칙:
- **자동 분석기는 의도적으로 두지 않음** — LLM 호출 비용을 명시적 트리거에만 묶기 위함
- 정제 발동은 사용자 의지(`/memory-distill`) 또는 세션 경계(핸드오프)에서만
- 분석 모델은 frontmatter에 `model:` 미지정 → 호출자(메인 세션) 모델 상속 → Anthropic Dreaming 동등 품질
- Stop 훅의 안내는 LLM 호출 X — 단순 텍스트 출력으로 사용자에게 정제 시기 알림

`/memory-distill --rebuild`와 핸드오프 자동 추출은 **동일 로직**을 공유합니다.

## 제약 사항

| # | 규칙 |
|---|------|
| 1 | **입력 jsonl은 절대 수정 X.** raw는 보존, 정제만 별도 파일로 |
| 2 | **기존 정제 .md 삭제 금지.** rebuild 시 `.archive/`로 이동 |
| 3 | **시크릿 스크럽핑 필수.** 마스킹 안 된 채 저장 금지 |
| 4 | **클러스터 ≥ `--min-cluster`만 정제.** 단발 노이즈 무시 |
| 5 | **`--scan` 기본.** `--apply` 또는 `--rebuild` 명시 시에만 파일 생성 |

## 산출물

```
memory/
├── gotchas/
│   ├── observations.jsonl           ← 입력 (수정 안 함)
│   ├── index.md                     ← 갱신
│   ├── NNN-{slug}.md                ← 신규/재구성
│   └── .archive/                    ← rebuild 시 기존 .md 백업
│       └── YYYY-MM-DD-NNN-{slug}.md
├── gotchas.md                       ← 카테고리 파일도 동기화 갱신
├── learned/
│   └── (위와 동일 구조)
└── learned.md                       ← 신규 생성될 수 있음

MEMORY.md                            ← 키워드 인덱스 갱신 (raw/정제 건수 동기화)
```

## 관련 스킬

| 스킬 | 관계 |
|------|------|
| `project-gotchas` | 관찰 수집 (jsonl 생성) — 이 스킬의 입력 |
| `mnemo` | 핸드오프 시 동일 로직 호출 |
| `skill-evolve` | 정제된 .md를 입력으로 받아 SKILL.md 진화 |

## 트리거 후 권장 흐름

```
/memory-distill --scan          ← 1. 후보 확인
/memory-distill --apply         ← 2. 정제 적용 (또는 --rebuild)
/skill-evolve                   ← 3. 정제된 .md로 스킬 진화 후보 스캔
```
