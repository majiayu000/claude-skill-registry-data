---
name: study-note
description: 학습 중 떠오른 아이디어와 메모를 아카이브 파일에 시간순으로 기록합니다. `scripts/study-note-helper.sh`를 사용하여 현재 KATA 프로젝트의 docs/study/아카이브.md에 노트를 추가합니다.
allowed-tools: Bash
---

# Study Note - 학습 노트 기록 스킬

이 스킬은 `scripts/study-note-helper.sh` 스크립트를 사용하여 학습 과정에서 떠오른 아이디어, 메모, 질문을 체계적으로 아카이브에 기록합니다.

모든 노트는 **스택 형식**(LIFO - Last In First Out)으로 파일 끝에 추가되어, 최신 노트가 아래쪽에 위치합니다. 각 노트에는 타임스탬프가 자동으로 추가됩니다.

## 주요 기능

- **자동 경로 해결**: `.katarc`에서 `CURRENT_KATA`를 읽어 대상 프로젝트 자동 결정
- **타임스탬프 자동 생성**: KST(한국 표준시) 기준으로 기록 시점 추가
- **키워드 태깅**: 나중에 검색 가능하도록 키워드 지정
- **UTF-8 인코딩**: 한글 학습 내용 완벽 지원
- **자동 파일 초기화**: 아카이브 파일이 없으면 자동 생성

## 파일 위치

```
${CURRENT_KATA}/docs/study/아카이브.md
```

예시: `mini-shell/docs/study/아카이브.md`

## 명령어

모든 기능은 `./scripts/study-note-helper.sh`를 통해 접근합니다.

| 작업 | 명령어 | 설명 |
|---|---|---|
| **노트 추가** | `./scripts/study-note-helper.sh add --keyword "<키워드>" --content "<내용>"` | 아카이브에 새 학습 노트를 추가합니다. |
| **키워드 검색** | `./scripts/study-note-helper.sh search --keyword "<키워드>"` | 특정 키워드를 포함하는 모든 노트를 검색합니다. |
| **키워드 통계** | `./scripts/study-note-helper.sh stats` | 모든 키워드의 사용 빈도를 확인합니다. |
| **도움말** | `./scripts/study-note-helper.sh help` | 사용법을 확인합니다. |

### 인자 설명

**add 명령어:**
- `--keyword`: 노트를 분류할 키워드 (쉼표로 구분하여 여러 개 가능)
  - 예: `"fork, 프로세스"`, `"메모리 누수, Valgrind"`, `"리팩토링"`
- `--content`: 학습 내용, 아이디어, 질문 등 (자유 형식)
  - 여러 줄도 가능 (따옴표로 감싸기)

**search 명령어:**
- `--keyword`: 검색할 키워드 (대소문자 구분 안 함)
  - 부분 일치로 검색됩니다 (예: "메모리"로 "메모리 누수" 검색 가능)

---

## 아카이브 파일 형식

```markdown
# 학습 아카이브

이 파일은 학습 중 떠오른 아이디어, 메모, 질문을 시간순으로 기록합니다.

---

# [2025-12-13 14:30:00 KST]

**키워드**: fork, exec

**내용**: fork()는 현재 프로세스를 복제하고, exec()는 복제된 프로세스를 새 프로그램으로 교체한다. 이 조합으로 새 프로그램 실행이 가능하다.

---

# [2025-12-13 15:45:22 KST]

**키워드**: 메모리 누수, Valgrind

**내용**: wait_example.c에서 Valgrind 실행 결과 free() 호출 누락 발견. 동적 할당 후 반드시 해제해야 함.

---
```

---

## 사용 예시

### 예시 1: 개념 학습 중 메모

**사용자 요청:**
> "fork와 exec의 차이점을 공부했는데 이걸 노트에 기록해줘. fork는 프로세스 복제, exec는 프로그램 교체야."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh add --keyword "fork, exec, 프로세스" --content "fork()는 현재 프로세스를 복제하여 자식 프로세스를 생성한다. exec()는 현재 프로세스를 새로운 프로그램으로 교체한다. 둘을 조합하면 새 프로그램을 별도 프로세스로 실행할 수 있다."
```

### 예시 2: 버그 발견 및 해결 기록

**사용자 요청:**
> "메모리 누수 발견했어. Valgrind로 확인했는데 free() 안 불러서 생긴 문제야. 이거 아카이브에 남겨줘."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh add --keyword "메모리 누수, Valgrind, 디버깅" --content "wait_example.c 실행 시 Valgrind에서 메모리 누수 경고 발생. malloc() 후 free() 호출을 누락한 것이 원인. 모든 동적 할당 메모리는 반드시 해제해야 한다."
```

### 예시 3: 코드 리뷰 중 발견한 패턴

**사용자 요청:**
> "smallsh.c 코드 보다가 패턴 하나 발견했어. 입력 파싱 전에 항상 버퍼 초기화하더라. 이거 기록해."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh add --keyword "코드 패턴, 버퍼 초기화" --content "smallsh.c에서 발견한 패턴: 사용자 입력을 파싱하기 전에 memset()으로 버퍼를 0으로 초기화한다. 이전 데이터 잔류를 방지하는 좋은 습관."
```

### 예시 4: 질문이나 TODO 항목

**사용자 요청:**
> "waitpid의 옵션 중에 WNOHANG이 정확히 뭐하는 건지 나중에 더 알아봐야겠어. 이거 TODO로 남겨줘."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh add --keyword "TODO, waitpid, WNOHANG" --content "질문: waitpid()의 WNOHANG 옵션이 정확히 어떤 상황에서 필요한지 더 공부 필요. 논블로킹 대기와 관련이 있는 것 같음. 다음 학습 세션에서 man page 정독하기."
```

### 예시 5: 성능 최적화 아이디어

**사용자 요청:**
> "파이프 여러 개 쓸 때 성능 이슈 있을 수 있다는 생각이 드는데 이거 메모해줘."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh add --keyword "성능, 파이프, 최적화" --content "아이디어: 파이프를 많이 사용하는 명령어(예: ls | grep | sort | uniq)는 프로세스 간 컨텍스트 스위칭 오버헤드가 있을 수 있음. 벤치마크 필요. 대안으로 버퍼링 전략 검토."
```

### 예시 6: 키워드로 노트 검색

**사용자 요청:**
> "fork 관련 노트들 다시 보고 싶어. 검색해줘."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh search --keyword "fork"
```

**출력 예시:**
```
ℹ  현재 KATA: mini-shell
ℹ  키워드 'fork' 검색 중...

# [2025-12-13 13:59:58 KST]
**키워드**: fork, exec, 프로세스
**내용**: fork()는 현재 프로세스를 복제하여 자식 프로세스를 생성한다...
---

✅ 총 1개의 노트를 찾았습니다.
```

### 예시 7: 키워드 사용 통계 확인

**사용자 요청:**
> "어떤 주제를 많이 공부했는지 통계 보여줘."

**스킬 동작:**
```bash
./scripts/study-note-helper.sh stats
```

**출력 예시:**
```
ℹ  현재 KATA: mini-shell
ℹ  키워드 통계 분석 중...

키워드 사용 빈도:

    3회 | fork
    2회 | 메모리 관리
    2회 | 프로세스
    1회 | exec
    1회 | Valgrind
    1회 | 디버깅

✅ 총 6개의 고유 키워드
```

---

## 참고사항

### 인코딩

- 모든 파일은 UTF-8로 저장됩니다.
- 한글 키워드와 내용을 완벽하게 지원합니다.
- 쉘에서 입력 시 따옴표로 감싸야 합니다.

### 타임스탬프

- KST(한국 표준시, UTC+9) 기준으로 자동 생성됩니다.
- 형식: `YYYY-MM-DD HH:MM:SS KST`

### 파일 위치 확인

아카이브 파일 위치를 확인하려면:

```bash
cat .katarc  # CURRENT_KATA 확인
# 아카이브 위치: ${CURRENT_KATA}/docs/study/아카이브.md
```

### 멀티라인 콘텐츠

여러 줄의 내용을 입력하려면:

```bash
./scripts/study-note-helper.sh add \
  --keyword "시스템 콜" \
  --content "학습 내용:
1. fork()로 프로세스 복제
2. exec()로 프로그램 교체
3. wait()로 자식 프로세스 대기"
```

### 키워드 검색

나중에 특정 키워드가 포함된 노트를 찾으려면:

```bash
# 스킬의 search 명령어 사용 (권장)
./scripts/study-note-helper.sh search --keyword "fork"

# 또는 직접 grep 사용
grep -A 5 "키워드.*fork" mini-shell/docs/study/아카이브.md
```
