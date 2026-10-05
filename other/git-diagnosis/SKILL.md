---
name: git-diagnosis
description: >
  Git 이력으로 코드베이스 건강 상태를 진단하는 런북.
  변경 빈도(Churn)와 버그 집중도(Bug Clusters)를 교차 분석해
  고위험 핫스팟과 소유권 공백을 식별하고 탐색 우선순위를 제시한다.
  "프로젝트 분석해줘", "코드베이스 진단", "git 분석해줘",
  "이 레포 상태 어때?", "어디부터 읽어야 해?",
  "핫스팟 분석", "기술 부채 분석", "어디가 위험해?",
  "새로 합류했는데 뭐부터 읽어?", "레포 진단",
  "codebase audit", "diagnose this project",
  "analyze this repo", "where should I start reading?"
  등에서 트리거. 경로 지정 시 해당 레포를, 없으면 현재 디렉토리를 진단.
---

# Git Diagnosis

코드를 열기 전 Git 이력만으로 코드베이스의 건강 상태를 진단한다.
개별 지표가 아닌 교차 분석(핫스팟)으로 고위험 코드를 식별하고 탐색 우선순위를 제시한다.

## 읽기 전용 제약

이 스킬 활성 중 Edit, Write 사용 금지 (파일 저장 요청 시 Write만 예외).
진단 결과만 보고하고, 코드 수정은 사용자가 별도 요청할 때 수행한다.

## 진단 절차

### 1. 사전 점검

진단 시작 전 대상과 레포 상태를 확인한다.

- **대상 디렉토리 결정**: 사용자가 경로를 지정하면 해당 디렉토리로 이동. 미지정이면 현재 디렉토리 사용.
- **monorepo 감지**: 루트에 `packages/`, `apps/`, `services/` 등이 있거나 워크스페이스 설정(`workspaces`, `pnpm-workspace.yaml`)이 있으면 사용자에게 분석 대상 경로를 확인. 이후 모든 `git log` 명령에 `-- <path>` 필터 적용.
- **shallow clone 감지**: `git rev-parse --is-shallow-repository` — `true`이면 이력이 불완전하다고 경고하고 `git fetch --unshallow` 제안. 그래도 진행하려면 결과의 한계를 소견에 명시.
- **최소 이력 확인**: 커밋 수가 극단적으로 적으면(~50개 미만) 통계적 의미가 낮다. 소견에 한계를 명시하고 간략 진단으로 전환.

### 2. 데이터 수집

아래 세 가지를 수집한다. 명령어는 OS·프로젝트 크기에 맞게 자유롭게 구성.

#### Churn — 변경 빈도

최근 1년간 가장 많이 수정된 파일 상위 20개를 추출한다.

```bash
git log --since='1 year ago' --format= --name-only | sort | uniq -c | sort -nr | head -20
```

자동생성 파일(`package-lock.json`, `yarn.lock`, `*.generated.*` 등)이 상위를 점령하면 필터 후 재분석.

#### Contributors — 기여자 분포

전체 기여자 순위와 최근 6개월 활동 기여자를 비교한다.
squash-merge 워크플로우에서는 병합자가 커밋 작성자로 기록되므로, merge commit 비율을 먼저 확인하고 해석에 반영.

#### Bug Clusters — 버그 집중도

버그 관련 커밋에서 파일별 빈도를 추출한다. **단어 경계 필수** — `grep "bug"`는 "debugger"도 잡는다.

```bash
git log -i --grep='fix\|bug\|broken' --name-only --format='' | grep -vw 'debugger\|fixture' | sort | uniq -c | sort -nr | head -20
```

`-P`(Perl regex)는 macOS git에서 미지원일 수 있으므로 파이프라인에서 `grep -w` 후처리로 노이즈를 제거한다.

### 3. 교차 분석

개별 지표를 교차해서 고위험 코드를 식별한다.

```
Churn ──┐
        ├──→ 고위험 파일 ──→ × Complexity ──→ 심각도 순위
Bug  ───┘                 ──→ × Contributors ──→ 소유권 공백
```

#### Churn × Bug → 고위험 파일 (핫스팟)

Churn 상위 20과 Bug 상위 20에 **동시 등장**하는 파일을 추출한다.
자주 바뀌고 자주 고장나는 파일 — 코드베이스의 최대 부담.

양쪽 목록을 정렬 후 `comm -12`로 교집합을 구하거나, 육안 대조가 빠르면 그렇게 한다.
교집합이 비어 있으면 Churn 상위에서 Bug에도 등장하는 파일을 넓혀서 탐색.

#### 고위험 × Complexity → 심각도

고위험 파일들의 커밋당 평균 변경량을 계산한다.

```bash
git log --format= --numstat -- <파일경로>
```

additions + deletions per commit으로 복잡도를 근사.
변경량이 큰 파일은 복잡하고 다루기 어려운 코드. 변경량이 작은 파일은 구조적으로 자주 건드리는 파일(설정, 라우팅 등)일 수 있다.

#### 고위험 × Contributors → 소유권 공백

고위험 파일을 가장 많이 수정한 기여자가 최근에 활동 중인지 확인한다.

```bash
git log --format='%an' -- <파일경로> | sort | uniq -c | sort -nr | head -3
```

주요 수정자가 비활동이면 해당 파일의 지식 소유자가 부재.

### 4. 보조 지표 (선택)

교차 분석의 해석을 보강하는 보조 지표. 프로젝트 상황에 따라 취사선택.

- **Velocity** — 월별 커밋 수 추세. 프로젝트의 활동 추세를 파악해야 할 때 유용 (활발한지 방치 중인지).
- **Crisis** — Revert, Hotfix, Emergency 등 긴급 대응 커밋 빈도. 운영 안정성이 관심사일 때 유용. 단, 프로젝트가 "rollback" 기능을 제공하면 오탐이 발생하므로 맥락을 확인.

### 5. 종합 소견 출력

아래 형식으로 출력한다. 빈 섹션은 생략.

```
## Git Diagnosis: {project_name}

### 진단 요약
(교차 분석 결과를 프로젝트 맥락에 맞게 서술)

### 고위험 파일
(핫스팟 목록 + 왜 위험한지 + 소유권 공백 포함)

### 권장 탐색 순서
(어디부터 읽을지)
```

해석에 구체적 임계값을 쓰지 않는다. 데이터와 프로젝트 맥락을 보고 판단.

### 6. 파일 저장 (요청 시)

사용자가 "저장해줘", "파일로 남겨줘" 등 요청할 때만 저장한다.
경로: `{project_root}/docs/git-diagnosis-{YYYY-MM-DD}.md`

## Gotchas

- **자동생성 파일 오염**: `package-lock.json`, `yarn.lock`, `*.generated.*`, `*.min.*`, `*.snap` 등이 Churn/Bug 상위를 점령하면 진단이 무의미해진다. 필터 후 재분석.
- **단어 경계 미적용**: `grep "bug"`는 "debugger"도 잡는다. Bug Clusters에서 파이프라인 후처리(`grep -w`, `grep -v`)로 노이즈를 제거. macOS git은 `-P`(Perl regex)를 지원하지 않으므로 `git log --grep`에서는 기본 패턴을 사용하고 후처리로 정밀 필터링.
- **squash-merge 왜곡**: squash 워크플로우에서는 PR 작성자가 아닌 병합자가 커밋 작성자로 기록된다. merge commit 비율로 워크플로우를 먼저 판단하고 Contributors 해석에 반영.
- **커밋 메시지 품질**: 대부분 "fix stuff", "update" 수준이면 Bug Clusters와 Crisis 분석 신뢰도가 낮다. 해당 분석의 한계를 소견에 명시.
- **자동화 봇 커밋**: dependabot, renovate 등 봇 커밋이 많으면 Churn과 Contributors가 왜곡된다. `--author` 필터로 봇을 제외하거나, 봇 영향을 소견에 명시.
- **monorepo**: 분석 대상이 레포 전체가 아닌 특정 패키지/서비스일 수 있다. 경로 필터(`-- <path>`)를 적용해야 의미 있는 결과가 나온다.
- **shallow clone**: `--depth`로 clone한 레포는 `git log`가 불완전하다. 에러 없이 잘린 결과가 나오므로 조용한 실패. 사전 점검에서 반드시 확인.
- **초기 레포**: 커밋이 극소수인 레포에서는 통계적 의미가 없다. 간략 진단으로 전환하고 한계를 명시.
- **파일 리네임 왜곡**: `git log --name-only`는 리네임을 이전/이후 두 경로로 각각 카운트한다. Churn 상위에 현재 존재하지 않는 경로가 있으면 리네임 여부를 확인.
- **대규모 레포 성능**: 커밋 10만+ 레포에서 `git log` 전체 스캔은 수십 초가 걸릴 수 있다. `--since`로 범위를 제한하거나, 사전에 `git rev-list --count HEAD`로 규모를 확인.
