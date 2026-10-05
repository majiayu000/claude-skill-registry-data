---
name: knowledge
description: |
  "/knowledge", "knowledge scan", "knowledge update", "knowledge delete",
  "knowledge list", "knowledge status",
  "지식 DB", "KB 스캔", "KB 업데이트", "KB 삭제", "KB 목록"
  Syscon Robotics Knowledge DB CRUD.
  Manage module-specific knowledge files for specify pipeline.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /knowledge — Knowledge DB Manager

시스콘 로보틱스 모듈별 지식 DB를 관리한다.
Knowledge DB는 `/specify` Phase 0.5 (Context Research) 단계에서 풀 코드베이스 스캔을 보완하거나 대체하는 사전 구축 지식으로 활용된다.
brownfield 작업 시 `/specify`가 `qa-log.md`의 `where.sr_modules` 정보를 참고하여 해당 모듈 파일을 직접 Read할 수 있다.

---

## Knowledge DB 구조

```
.sr-harness/knowledge/
├── index.yaml                              ← 전체 인덱스 (필수)
├── sarics-nx/
│   ├── backend.md                          ← {product}/{module}.md
│   └── frontend.md
├── spx/
│   ├── core-driver.md                      ← 공통 지식
│   ├── core-driver.ros1.md                 ← ROS1 전용 (선택)
│   ├── core-driver.ros2.md                 ← ROS2 전용 (선택)
│   ├── core-localization.md
│   ├── core-navigation.md
│   ├── core-task.md
│   └── core-docking.md
└── cross/
    └── sarics-spx.md                       ← cross-product 연동
```

### 네이밍 규약

| 규칙 | 패턴 | 예시 |
|------|------|------|
| 제품 폴더 | `{product}/` (kebab-case) | `sarics-nx/`, `spx/` |
| 모듈 파일 | `{module}.md` | `core-driver.md` |
| ROS 분기 | `{module}.{ros-version}.md` | `core-driver.ros1.md` |
| Cross-product | `cross/{product-a}-{product-b}.md` | `cross/sarics-spx.md` |

---

## Commands

인자에 따라 동작이 분기된다.

### `/knowledge scan {module}`

현재 워크스페이스를 풀 스캔하여 모듈의 지식 파일을 생성/갱신한다.

`/specify` Phase 0.5 may call this command when a stale KB entry is found and the user selects "Re-scan now". In that handoff:
- Return normally only after the module KB file and `index.yaml` are updated.
- If the scan cannot complete, report a concise failure reason and stop without partially marking the module fresh.
- `/specify` will catch the failure, record `KB re-scan failed: {module} — {reason}` in `qa-log.md ## Research`, and fall back to agent scan for that module.

**동작:**

1. 워크스페이스에서 프로젝트 구조 스캔 (Glob/Grep/Read)
2. 표준 포맷으로 지식 파일 생성
3. index.yaml 업데이트

**스캔 항목 (표준 포맷):**

```markdown
# {모듈명} Knowledge Base

## 1. Overview
- 목적: (1-2문장)
- GitHub: (레포 URL — .git/config에서 추출)
- 기술 스택: (언어, 프레임워크, 빌드 시스템)
- ROS 버전: ROS1 / ROS2

## 2. Architecture
- 패키지/디렉토리 구조 (트리)
- 핵심 클래스/노드 목록 (이름 + 역할 1줄)
- 의존 패키지 (package.xml 또는 requirements.txt 요약)

## 3. Interfaces (외부 연동)
- 입력: | 이름 | 타입 | 소스 | 주기 |
- 출력: | 이름 | 타입 | 수신자 | 주기 |
- 설정: (파라미터 파일, launch 인자)

## 4. Patterns & Conventions
- 네이밍 규칙, 에러 처리 패턴, 테스트 구조

## 5. Known Constraints
- HW 제약, 성능 요구, 호환성

## 6. Common Changes
- 새 드라이버/노드 추가 시 절차
- 파라미터 변경 시 영향 범위

## 7. Accumulated Learnings
(초기에는 비어 있음 — /execute, /bugfix, /specify가 패턴 발견 시 자동 추가)
```

**driver 모듈 추가 섹션** (§7-8을 끼워 넣고 Accumulated Learnings는 §9로 이동):
```markdown
## 7. Hardware Interfaces
| 장치 | 프로토콜 | 포트/버스 | 데이터 레이트 | 드라이버 노드 |

## 8. Error Handling
| 에러 유형 | 감지 방법 | 복구 동작 | 안전 영향 |

## 9. Accumulated Learnings
(초기에는 비어 있음 — /execute, /bugfix, /specify가 패턴 발견 시 자동 추가)
```

> **섹션 번호 정책:** Accumulated Learnings 섹션의 번호는 프로파일에 따라 가변(§7 또는 §9). **다른 스킬에서 이 섹션을 참조할 때는 반드시 헤딩 텍스트(`Accumulated Learnings`)로 찾아야 하며, 번호로 참조하면 안 됨.** 권장 검색: `grep -n '^## .*Accumulated Learnings' {file}` 로 라인 번호를 얻어 그 다음 빈 줄 이후에 append.

> **⚠ regex 함정 주의:** 헤딩 매칭은 **라인 단위**로 처리해야 한다. `^## .*Accumulated Learnings.*?` 같은 패턴을 `re.DOTALL` 플래그와 함께 쓰면 첫 `^## ` (예: `## 1. Overview`)에서 시작해 `Accumulated Learnings` 까지 전체 본문을 매치하여 §1~§N 섹션을 통째로 삭제하는 사고가 발생한다. **올바른 방법:** 라인을 split한 뒤 `re.match(r'^## .*Accumulated Learnings.*$', line)` 로 헤딩 라인을 찾고, 그 다음 라인부터 다음 `## ` 또는 EOF 직전까지를 본문으로 추출한다.

> **de-dup 정책 (Accumulated Learnings 추가 시):** 신규 학습 항목을 추가하기 전에 기존 항목과 중복 여부를 검사한다.
> 1. **bullet 본문(`- ` 이후)** 의 정규화된 텍스트로 비교: 날짜 prefix(`YYYY-MM-DD`), 출처 태그(`[specify]/[execute T-XXX]/[bugfix]`), 양옆 공백 제거 후 lower-case 비교.
> 2. **완전 동일** → skip하고 기존 항목의 날짜만 오늘로 갱신 (in-place).
> 3. **부분 일치** (Jaccard 유사도 ≥ 0.7 또는 substring 포함) → 기존 항목 유지하고 신규는 skip. 단 bugfix처럼 회피 패턴이 추가되는 경우 신규를 별도 항목으로 추가.
> 4. **불일치** → 정상 추가.
>
> **압축 정책 (선택):** Accumulated Learnings가 50개를 초과하면 가장 오래된 절반을 `## Archived Learnings` 섹션으로 이동. 같은 헤딩 anchor 정책 적용. 자동 트리거되지 않으며 `/knowledge update {module} --compact` 옵션이 명시될 때만 수행. 구현은 `scripts/kb-compact.py` 헬퍼 스크립트에 위임:
> ```bash
> python3 scripts/kb-compact.py {kb_file.md} [--threshold 50] [--keep-ratio 0.5] [--dry-run]
> ```
> 압축 결과: 가장 최근 절반(날짜 기준)을 Accumulated Learnings에 유지, 나머지를 Archived Learnings로 이동. 다른 섹션은 영향 없음.

**ROS 분기 파일 생성 규칙:**
- `package.xml`에서 ROS 버전 감지
- ROS1: catkin, rospy, roscpp → `.ros1.md` 생성
- ROS2: rclpy, rclcpp, ament → `.ros2.md` 생성
- ROS 분기 파일에는 topic/service/action 목록, 빌드 시스템, QoS 등 ROS 버전별 정보

**스캔 실행:**

```
1. 프로젝트 루트 감지 (package.xml, CMakeLists.txt, package.json 등)
2. 기존 KB 파일이 존재하면: ## Accumulated Learnings 섹션 내용을 메모리에 백업
3. ROS 버전 감지 (있으면)
4. 디렉토리 구조 트리 생성
5. 소스 파일 스캔 (클래스, 노드, 인터페이스)
6. 설정 파일 스캔 (yaml, launch, config)
7. 결과를 표준 포맷으로 .sr-harness/knowledge/{product}/{module}.md에 저장
8. 백업해둔 Accumulated Learnings 항목을 ## Accumulated Learnings 섹션에 복원
9. ROS 분기 파일 생성 (해당 시)
10. index.yaml 업데이트 (source.path, commit_sha, scanned_at)
```

> **재스캔 시 학습 보존 (필수):** 기존 KB 파일이 있으면 `## Accumulated Learnings` 섹션의 모든 항목(빈 자리표시자 줄 제외)을 우선 백업한다. 새 KB 파일을 표준 포맷으로 작성한 후, 백업된 항목들을 `## Accumulated Learnings` 섹션에 그대로 복원한다. **재스캔이 누적 학습을 절대 잃어버려서는 안 된다.** 백업 대상 식별: `## Accumulated Learnings` 헤딩 다음 줄부터 다음 `## ` 헤딩 또는 EOF 직전까지. 자리표시자(`(초기에는 비어 있음 …)`)만 있으면 백업 불필요.

**index.yaml 항목 형식:**

```yaml
modules:
  {module-name}:
    product: {product}
    files:
      common: {product}/{module}.md
      ros1: {product}/{module}.ros1.md    # 있으면
      ros2: {product}/{module}.ros2.md    # 있으면
    source:
      path: {워크스페이스 절대 경로}
      github: {git remote URL}
    ros: {ros1|ros2|null}
    scanned_at: "{ISO 8601}"
    commit_sha: "{git HEAD SHA}"
```

**스키마 검증 (모든 명령 진입 시 실행):**

`/knowledge` 명령 (list/status/scan/update/delete/Phase 0.5 KB-first 등)이 index.yaml을 읽을 때 다음 검증을 수행한다.

| 필드 | 필수 | 타입 | 검증 규칙 |
|------|------|------|---------|
| `modules` | 필수 | dict | 비어있어도 dict이어야 함 |
| `modules.<name>.product` | 필수 | string | non-empty |
| `modules.<name>.files.common` | 필수 | string | 실제 파일 존재 여부 검증 |
| `modules.<name>.files.ros1` | 선택 | string | 있으면 파일 존재 검증 |
| `modules.<name>.files.ros2` | 선택 | string | 있으면 파일 존재 검증 |
| `modules.<name>.source.path` | 필수 | string | 절대 경로, 존재 디렉토리 |
| `modules.<name>.source.github` | 선택 | string | URL 형식 (검증 안 해도 됨) |
| `modules.<name>.ros` | 필수 | `ros1\|ros2\|null` | 셋 중 하나 |
| `modules.<name>.scanned_at` | 필수 | string | ISO 8601 |
| `modules.<name>.commit_sha` | 필수 | string | 40자 hex (full SHA) |

검증 실패 시:
- 손상된 모듈 이름과 누락/오류 필드를 명시한 에러 메시지 출력
- 해당 모듈만 스킵하고 나머지 모듈로 명령 계속 (graceful degradation)
- list/status에서는 해당 행에 `⚠ schema error` 표시

**`commit_sha` / `source.path` 시맨틱:**

- `source.path`는 **모듈 자체의 레포 루트**여야 한다. mono-repo 서브디렉토리는 허용되지만, 그 경우 `commit_sha`는 mono-repo 루트의 HEAD SHA를 의미한다.
- sr-harness 자체는 KB **호스트** 역할이므로 `source.path`로 등록할 수 없다. 픽스처 디렉토리(`.playground/`)도 운영 환경에서는 등록하지 않는다.
- `commit_sha`는 `git -C {source.path} rev-parse HEAD` 의 출력값이다. `.git` 디렉토리가 없으면 staleness 비교 불가 → `/knowledge status`에서 `⚠ no-git` 표시.

**Cross-product 항목 스키마 (예외):**

`cross/{a}-{b}.md` 형태의 cross-product KB는 단일 모듈에 속하지 않으므로 다음 변형 스키마를 사용한다.

```yaml
modules:
  {bridge-name}:                    # 예: sarics-spx-bridge
    product: cross                  # 고정값
    files:
      common: cross/{a}-{b}.md
    source:
      path: {KB 호스트 레포 루트}    # cross는 모듈 레포 없음 → KB 호스트 참조 (예외)
      github: {KB 호스트 git remote URL}
    ros: null                       # cross는 ROS 버전 무관
    scanned_at: "{ISO 8601}"
    commit_sha: "{KB 호스트 HEAD SHA}"
    cross_modules: [{module-a}, {module-b}]   # 필수: 연결된 모듈 이름
```

cross-product `commit_sha`는 KB 호스트의 SHA로 staleness 추적. 연결된 모듈 중 하나라도 변경되면 사용자가 수동으로 cross KB를 갱신한다 (자동 추적 미지원).

---

### `/knowledge update {module} [--compact]`

기존 지식 파일을 갱신한다. 변경이 있을 때만 재스캔.

**동작:**

1. index.yaml에서 해당 모듈의 `commit_sha` 조회
2. 현재 워크스페이스의 `git rev-parse HEAD`와 비교
3. 동일하면: "변경 없음. 스킵합니다." (단, `--compact` 옵션이 있으면 압축은 진행)
4. 다르면: 재스캔 (= `/knowledge scan` 동작) → commit_sha 갱신
5. `--compact` 옵션이 있으면 마지막에 `scripts/kb-compact.py` 호출하여 압축 (위 압축 정책 참조)

---

### `/knowledge delete {module}`

모듈의 지식 파일을 삭제한다.

**동작:**

1. index.yaml에서 해당 모듈 항목 조회
2. 연결된 파일 삭제 (common + ros1/ros2)
3. index.yaml에서 항목 제거
4. 빈 디렉토리 정리

---

### `/knowledge list`

등록된 모듈 목록을 표시한다.

**출력 형식:**

```
Knowledge DB — .sr-harness/knowledge/

| Module | Product | ROS | Scanned | Commit |
|--------|---------|-----|---------|--------|
| core-driver | spx | ros2 | 2026-04-15 | a1b2c3d |
| backend | sarics-nx | — | 2026-04-15 | e5f6g7h |

Total: 2 modules
```

---

### `/knowledge status`

각 모듈의 변경 여부를 확인한다.

**동작:**

1. index.yaml의 각 모듈에 대해:
2. `source.path`에서 현재 `git rev-parse HEAD` 조회
3. `commit_sha`와 비교

**출력 형식:**

```
Knowledge DB Status

| Module | Scanned Commit | Current Commit | Status |
|--------|---------------|----------------|--------|
| core-driver | a1b2c3d | a1b2c3d | ✅ up-to-date |
| backend | e5f6g7h | x9y0z1w | ⚠ outdated |

Outdated: 1 module(s). Run `/knowledge update {module}` to refresh.
```

---

## 인자 없이 호출 시

`/knowledge` 만 입력하면 `/knowledge list`와 동일하게 동작한다.

## 인자 파싱

| 입력 | 동작 |
|------|------|
| `/knowledge` | list |
| `/knowledge list` | list |
| `/knowledge status` | status |
| `/knowledge scan core-driver` | scan core-driver |
| `/knowledge update core-driver` | update core-driver |
| `/knowledge delete core-driver` | delete core-driver |
| `/knowledge scan` (모듈 없이) | 현재 워크스페이스를 자동 감지하여 모듈명 추론 |
