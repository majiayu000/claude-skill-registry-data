---
name: kr-patent-format-unify
description: 한국 특허 명세서 .docx 안에서 후속 작업으로 신설된 단락(insert_paragraph_before·정합성 수정·청구항 본문 매핑·도면 도입 문장 신설·S14 1파트 신설 등으로 추가된 단락)이 인접 본문 단락과 서식(글꼴·글자 크기·색상·줄간격·들여쓰기·첫 줄 들여쓰기·정렬 등)이 달라 시각적으로 튀는 문제를 자동 검출하여 인접 본문 단락의 pPr(paragraph properties) 및 첫 run의 rPr(character properties)를 deepcopy로 복사해 일괄 동기화. python-docx의 `insert_paragraph_before(text, style=...)`는 paragraph style 객체만 승계하고 character formatting(font·size·color·outlineLvl 제외) + paragraph format(들여쓰기·줄간격)을 default로 두기 때문에, 신설 단락이 본문 다른 단락과 서식 어긋남이 자주 발생. 본 스킬은 (1) 명세서 안 신설 추정 단락 자동 검출 — 한국 특허 흔한 신설 도입어 패턴(청구항 정형 "본 발명의 일 실시예에 있어서,", "본 발명에 따른 [발명의 명칭]은,", 도면 도입 "도 N은 ~ 이다.", S14 1파트 "이상에서 살펴본 바와 같이, 본 발명에 따르면,") + 사용자 지정 패턴 + 자동 폰트 불일치 감지 — 와 (2) 인접 본문 단락(직전 우선, 없으면 직후)의 pPr·rPr deepcopy 복사를 수행. outline level은 헤더가 아닌 본문 단락에는 부여하지 않음(자동 제거). 청구범위·요약서 섹션은 처리 대상에서 제외(불변). "서식 통일", "서식 동기화", "format unify", "서식이 다르다", "단락 서식 안 맞아", "쌩뚱맞은 서식", "폰트가 달라", "신설 단락 서식", "insert_paragraph_before 서식"이 언급되거나, 청구항 본문 매핑·도면 도입 문장 신설·정합성 수정 직후 명세서가 서식 어긋남으로 보이는 맥락이면 사용. kr-patent-navigation-pane(outline 부여)과 짝을 이루는 docx 후처리 인프라.
---

# kr-patent-format-unify — 한국 특허 명세서 신설 단락 서식 동기화

## 무엇을 하는가

한국 특허 명세서 docx 안에서 후속 작업으로 신설된 단락이 인접 본문 단락과 서식이 달라 시각적으로 튀는 문제를 자동 해소한다.

- `<w:pPr>`(paragraph properties: 들여쓰기·줄간격·정렬·첫 줄 들여쓰기) — 인접 본문 단락에서 deepcopy 복사
- `<w:rPr>`(character properties: 글꼴·크기·굵기·기울임·색상) — 인접 본문 단락의 첫 run rPr을 신설 단락의 모든 run에 deepcopy 복사
- `<w:outlineLvl>` — 본문 단락에는 부여하지 않음 (자동 제거)

명세서 외관을 통째로 바꾸는 게 아니라 **튀어나온 단락만** 인접 흐름에 맞춤. 외관 자체는 그대로 유지.

## 언제 사용하는가

- `kr-patent-spec-drafting` 수정 모드 / `kr-patent-consistency-check` 수정 적용 후 신설 단락 다수
- `kr-patent-ralph-loop`이 도면 도입 문장·S14 1파트 등 신설 단락을 자동 추가한 직후
- 청구항 본문 매핑(청구항 1~N 정형 문언을 S13 안 각 절에 1:1 삽입) 직후
- 외부 변리사 docx에서 일부 단락만 서식이 다를 때 (수동 편집 흔적)

## 언제 사용하지 않는가

- 명세서 전체 서식을 통째로 바꾸려 할 때 (이건 별도 docx-builder 재빌드)
- 본문이 아닌 표·도면 캡션의 서식 (표 셀 안 서식은 별도 처리 필요)

## 검출 대상 단락 (default 패턴)

다음 도입어로 시작하는 단락을 신설 추정 단락으로 자동 검출:

| 카테고리 | 도입어 패턴 |
|---|---|
| 청구항 종속항 풀어쓰기 | `본 발명의 일 실시예에 있어서,` |
| 청구항 독립항(방법) 풀어쓰기 | `본 발명에 따른 ~ 방법은,` |
| 청구항 독립항(시스템) 풀어쓰기 | `본 발명에 따른 ~ 시스템은,` |
| 도면 도입 정형 | `도 N은 ~ 이다.` (N = 1~99, 종결 "이다." 또는 "이고,") |
| S14 1파트 정형 | `이상에서 살펴본 바와 같이, 본 발명에 따르면,` |
| 변형 실시예 (선택) | `한편,`, `또 다른 실시예에 있어서,`, `또한, 일 실시예에 있어서,`, `나아가,` |

추가로 **자동 폰트 불일치 감지**: 단락의 첫 run rPr이 인접 본문 단락의 첫 run rPr과 다르면 신설 후보. (font name·size·color 비교)

## 처리 영역

- **포함**: 본문 전체 (앞표지 ~ 【부호의 설명】 직전)
- **제외**: 【청구범위】 ~ 끝 (청구범위·요약서·요약·대표도는 불변)
- **제외**: 표(table) 안 단락 — 표는 자체 서식 관리

## 참조 단락 선정 규칙

각 신설 단락에 대해 인접 본문 단락의 서식을 복사. 선정 우선순위:

1. **직전 본문 단락** (1~5 단락 이내) — 같은 절 안일 가능성 높음
2. **직후 본문 단락** (1~5 단락 이내) — 직전이 모두 신설 단락이거나 절 헤더일 때
3. 둘 다 없으면 스킵 (안전한 default)

"본문 단락"의 조건:
- 비어있지 않음
- 절 헤더(`【...】` 단독)가 아님
- 신설 추정 도입어로 시작하지 않음 (다른 신설 단락 회피)

## 사용 방법

### 일반 호출

```bash
python "~/.claude/skills\kr-patent-format-unify\scripts\apply_format_unify.py" "<docx 경로>"
```

추가 옵션:
- `--patterns "패턴1|패턴2|..."` — 추가 검출 도입어 패턴 (정규식, OR 결합)
- `--auto-detect` — 자동 폰트 불일치 감지 활성화 (default: off, 도입어 패턴 기반만)
- `--dry-run` — 실제 수정 안 하고 어느 단락이 동기화 대상인지만 출력
- `--no-backup` — 백업 생략 (비추천)

### 사전 점검

1. **파일이 Word에서 열려 있지 않은지 확인** — 잠금 시 PermissionError
2. **원본은 항상 백업** (`{원본명}_서식통일전.docx`)
3. **청구범위 무결성** — 시작·종료 시점 byte 단위 비교 (위반 시 즉시 중단)

### 출력 형식

```
Backup: <백업 경로>

서식 동기화 적용 — N개 단락:
  [85] (청구항 1) ref=[84]: 시뮬레이션 결과 데이터 생성부(170) 동의어 정리
  [119] (도 5 도입) ref=[118]: 손상 데이터 생성 절 진입 본문
  [231] (S14 1파트) ref=[230]: 다국어 UI 변형 실시예
  ...

청구범위 byte 일치: ✅
Wrote: <원본 경로>
```

## 동작 원리 (왜 deepcopy로 pPr·rPr를 복사하는가)

python-docx의 `insert_paragraph_before(text, style=parent_style)`는:
- paragraph style 객체(예: "Normal")만 승계
- pPr 안 ind·spacing·jc·outlineLvl 등 직접 속성은 default
- run 안 rPr의 font·size·color 등은 default (style에서 inherit 안 됨)

결과: 신설 단락의 글꼴이 시스템 default(맑은 고딕 11pt 등)로 보임. 명세서 다른 단락이 나눔고딕 10pt·줄간격 200% 등이면 시각적 차이 명확.

해결: 인접 본문 단락의 pPr·rPr 전체 XML element를 `copy.deepcopy`로 복제하여 신설 단락에 통째로 이식. style을 통한 inherit이 아닌 직접 속성 설정이라 안정적.

### 왜 outline level은 제거하는가

본 스킬의 대상은 **본문 단락**. 참조 단락이 우연히 헤더(`outlineLvl=0~3`)였다면 그 outline 값을 복사하면 안 됨(신설 단락이 잘못 탐색창에 노출). 따라서 deepcopy 후 outlineLvl element는 자동 제거.

탐색창 outline 부여는 `kr-patent-navigation-pane`이 별도로 담당.

## 헤더 매칭 규칙

paragraph의 전체 텍스트가 `【...】` 단독인 단락은 헤더로 인정, 처리 대상에서 제외. 본문 중간의 `【…】` 인용은 본문으로 인정.

## 의존성

- Python ≥ 3.8
- python-docx ≥ 0.8.11

## 다른 스킬과의 관계

| 스킬 | 짝 관계 |
|---|---|
| **kr-patent-navigation-pane** | docx 후처리 짝. navigation-pane은 outline level, format-unify는 본문 서식. 두 스킬은 책임이 직교(orthogonal)하여 둘 다 호출해도 충돌 없음. 일반적 순서: 본문 작업 종료 → format-unify → navigation-pane → 최종 검토. |
| **kr-patent-spec-drafting** | spec-drafting이 수정 모드로 본문 신설할 때마다 호출 직후 format-unify 권장. |
| **kr-patent-consistency-check** | consistency-check의 자동 수정 결과 신설 단락에 적용. |
| **kr-patent-ralph-loop** | ralph-loop 각 iteration 종료 직전에 format-unify를 자동 호출하면 매 iter 서식 어긋남 방지. |
| **kr-patent-docx-builder** | builder가 처음부터 만든 docx는 서식이 일관 — format-unify 불필요. 외부 명세서 수정 흐름에서만 의미. |

## 사용 예시

### 예시 1: 청구항 본문 매핑 직후

```
User: 청구항 14개 본문 매핑했더니 일부 단락 서식이 본문과 다른데?

Claude: [format-unify 호출]
→ 청구항 정형 도입어 검출 14건 + 도면 도입 신설 7건 + S14 1파트 1건
→ 인접 본문 단락의 pPr·rPr deepcopy 복사
→ 청구범위 byte 일치 ✅
→ Word에서 확인: 시각적 차이 사라짐
```

### 예시 2: ralph-loop 사이클 종료 직후

```
User: ralph-loop 엄격 수렴 끝났어. 서식 좀 보고 싶어.

Claude: [format-unify --auto-detect]
→ 도면 도입 신설 (B-1) + 청구항 본문 매핑 + S14 1파트 모두 검출
→ 일괄 서식 동기화
→ Word 탐색창 outline은 navigation-pane이 별도 담당
```

### 예시 3: dry-run으로 사전 확인

```
User: 어떤 단락이 바뀔지 먼저 보고 싶어.

Claude: [format-unify --dry-run]
→ 21개 단락 검출, 각각의 참조 단락 후보 출력
→ 실제 수정 없음
→ OK이면 --dry-run 빼고 재실행
```

## 누적 학습 항목

(이 섹션은 `kr-patent-skill-updater`가 작업 회고 후 자동으로 추가)

- (2026-05-27 신설, 사건 A 첫 사용) python-docx `insert_paragraph_before(text, style=parent.style)`는 paragraph style 객체만 승계하고 pPr·rPr의 직접 속성은 default로 두어, 신설 단락이 명세서 본문과 글꼴·줄간격이 다르게 보이는 결함이 빈발. **신설 작업 직후 format-unify 호출이 default**. 검출은 도입어 패턴(청구항 정형 + 도면 도입 정형 + S14 1파트) + 자동 폰트 불일치 감지 두 트랙 병행.
- (2026-05-27) outline level은 헤더가 아닌 본문 단락에 부여하면 탐색창에 잘못 노출 — deepcopy 후 outlineLvl element는 자동 제거 필수. format-unify와 navigation-pane은 책임 직교(orthogonal).
- (2026-05-27, 사건 A 첫 사용) python-docx의 `paragraph._element.find(qn('w:rPr')).xml`은 lxml `XmlString` 타입이라 set·dict 키로 직접 사용 불가(unhashable). 자동 폰트 불일치 감지 함수에서는 반드시 `str()` 변환을 거쳐 hashable 보장. 빈발하는 TypeError 버그.
