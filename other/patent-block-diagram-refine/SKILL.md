---
name: patent-block-diagram-refine
description: >
  이미 존재하는 특허 도면 편집파일(.pbd)을 입력으로 받아 수정·정제하는 스킬. 새로 그리는
  patent-block-diagram과 달리, 입력 .pbd에서 현재 스타일(fs·shape·부호 태그·레이아웃)을
  먼저 자동 추출해 "하우스 스타일 스냅샷"을 만들고, 그 규약을 깨지 않는 선에서 박스 추가/삭제/
  문구변경, 단계 삽입, 분기 경로 변경, 카드 증설, 화살표 계단꺾임·관통 교정, 부호 재배치 같은
  수정을 가한 뒤, 특허 블록도 에디터 앱에 주입해 렌더링·육안 검증하고 출원용 PNG까지 내보낸다.
  부호를 바꾸는 수정이면 명세서 본문·부호의 설명과의 정합 위험을 함께 보고한다.
  "도면 수정해줘", "이 pbd 고쳐", "블록도 단계 추가", "흐름도 분기 바꿔", "도면 부호 정리",
  "화살표 정렬 교정", "도면 카드 늘려", "pbd refine", "도면 정제", "기존 도면 손봐",
  "도면_스타일가이드대로 수정" 같은 표현이 보이거나, 완성된 .pbd 세트를 부분 수정하려는
  맥락에서 사용. (백지에서 새 도면 작도=patent-block-diagram, 기존 PNG에 부호만 얹기=
  kr-patent-drawing-tagging 은 별개.)
---

# 특허 도면 정제 (.pbd 수정)

## 무엇을 하는가

완성된 `.pbd`(에디터 네이티브 JSON)를 입력으로 받아, **기존 스타일을 유지한 채** 부분 수정한다.
새로 그리는 게 아니라 고치는 작업이므로, 착수 전에 입력 파일의 현재 규약을 먼저 읽어
"이 도면이 지금 어떤 fs·shape·부호·간격을 쓰는지"를 스냅샷으로 확정하고, 수정은 그 스냅샷을
복제하는 방향으로만 한다. 임의로 새 값을 도입하지 않는다.

**철칙: 렌더 없이 좌표만 믿지 않는다.** 수정 → CDP 포트로 렌더 → PNG를 Read로 육안 확인 →
보정. 최소 1회전, 실전에서 3회전까지 돈다.

## 입력

- 단일 `.pbd` 또는 도면 세트 폴더(`도면1.pbd` … `도면N.pbd`).
- (있으면) 사건 폴더의 `도면_스타일가이드.md` — 부호 체계 SINGLE SOURCE. 없으면 pbd에서 추출.
- (권장) 명세서 최신 `.docx` 경로 — 부호·단계명 정합 대조용.

## 앱·렌더 (patent-block-diagram과 공유)

- 앱: `$APP_DIR` (Electron, 레포 동봉 소스 = `patent-block-diagram-app/`)
- 렌더 스크립트: `~/.claude/skills/patent-block-diagram/scripts/render_pbd.mjs`
- 작업용 실행(CDP):

```bash
cd "$APP_DIR" && \
  ./node_modules/.bin/electron.cmd . --remote-debugging-port=9222 \
    --user-data-dir="$TMP/pbd-agent" > /dev/null 2>&1 &
# 9초쯤 기다린 뒤
node "~/.claude/skills/patent-block-diagram/scripts/render_pbd.mjs" <입력.pbd> <출력.png> [scale]
```

⚠️ `--user-data-dir` 없이 띄우거나 `taskkill` 로 electron 을 싹 죽이면 사용자가 편집 중인
창을 빼앗는다(단일 인스턴스 락이 userData 폴더 단위). 절대 하지 않는다.

scale 2 = 검토용, 3 = 출원용. `.pbd` 스키마·화살표 라우팅 규칙은 patent-block-diagram
`SKILL.md`가 단일 진실(중복 서술 안 함). 여기서는 **수정 워크플로우**만 규정한다.

## 작업 순서

### 1. 스타일 스냅샷 추출 (수정 전 필수)
입력 `.pbd`(들)를 파싱해 아래를 표로 뽑는다. 이게 이번 수정의 준수 기준이 된다.

```bash
python3 - <<'PY'
import json,glob,os
for f in sorted(glob.glob('*.pbd')):
    d=json.load(open(f,encoding='utf-8'))
    b=d.get('boxes',[]); a=d.get('arrows',[]); t=d.get('tags',[])
    fss=sorted({x.get('fs') for x in b})
    sh={}
    for x in b: sh[x['shape']]=sh.get(x['shape'],0)+1
    cont=[x['id'] for x in b if x.get('textTop') or x['w']>1000]
    print(f"{f}: box={len(b)} arr={len(a)} tag={len(t)} fs={fss} shapes={sh} nextId={d.get('nextId')} containers={cont}")
    print("  tags:", [x['label'] for x in t])
PY
```

여기서 확정: 이 도면의 표준 fs, 도형 용법, 부호 부여 규칙(S계열/장치/개념), `nextId`(새 id는 이보다 커야 함).

### 2. 하우스 스타일 대조
스냅샷을 `references/도면_스타일가이드_템플릿.md` §1과 대조. 벗어난 값이 있으면
"기존 도면이 이미 비표준"인 것이므로, **기존 도면 값을 우선**한다(정합이 표준 준수보다 위).
새로 추가하는 요소만 §1 규약을 따른다.

### 3. 수정 계획 → 사용자 확인
무엇을 바꾸는지 표로: 대상 id, 변경 종류(추가/삭제/문구/좌표/부호), 새 값, 부호 영향.
**부호를 신설·변경·재배열하면** 명세서 본문·【부호의 설명】 동시 수정 필요 여부를 표시하고
사용자에게 먼저 알린다. 이 확인 없이 부호를 건드리지 않는다.

### 4. .pbd 편집
- id는 boxes/arrows/tags 통틀어 유일. 새 id는 `nextId`부터, 끝나면 `nextId` 갱신.
- 세로 흐름도에 단계 삽입 시: 이후 박스 y를 일정 간격(기존 간격 그대로, 보통 118~130)씩 밀어 겹침 방지.
- 박스 이동 시 딸린 태그 `dx`/`dy`는 박스 상대좌표라 함께 안 옮겨도 따라온다. 이중 이동 주의.
- 화살표 정렬: 상하 연결=중심 x, 좌우 연결=중심 y. 양방향=화살표 2개 중심축 정렬.

### 5. 렌더 & 육안 검증
scale 2 PNG → **Read로 이미지 확인**. 점검: 글자 잘림, 태그가 선에 물림, 화살표 계단 꺾임,
스파인이 박스 관통, 컨테이너 밖 삐져나옴, 삽입으로 인한 겹침.

### 6. 보정 → 재렌더
문제 없을 때까지 반복.

### 7. 출원용 내보내기 + 마무리
scale 3 PNG를 `PNG_out\`에 `[도면0N]_설명_유형.png` 규약으로 저장.
수정 전 원본은 `pbd_bak\`에 백업(덮어쓰기 전에). 필요 시 `topatent`로 TIFF.
끝나면 `.pbd`를 `Start-Process`로 열어 사용자가 GUI로 이어 편집하게 둔다.

## 수정 유형별 프롬프트 템플릿

`references/도면_스타일가이드_템플릿.md` §4에 5종(블록도 기능부 추가, 흐름도 단계삽입·분기변경,
개념도 카드 증설, UI 요소 추가, 화살표 정렬 교정)이 있다. 사용자 지시를 이 유형에 매핑해 실행.

## 하우스 스타일 요약 (전문은 references/ 템플릿)

- 도형: rect=기능/단계/카드/UI, round=시작종료·개념노드, diamond=판단, cylinder=저장/입력. 4형뿐.
- fs: 시스템블록도 24, 표준흐름도 22, 촘촘흐름도 19~20, 초촘촘 16, UI 23~24, 상세카드 16. 한 도면 내 통일.
- 화살표: ortho 기본, 양방향=2개 중심축 정렬, 분기 Yes/No=noFrame 소형 rect.
- z: 컨테이너 1, 화살표 2~9, 박스 10~, 태그 60~.
- 태그: 우측 dx=w+40 / 흐름도 단계부호 왼쪽 dx≈-62 / 컨테이너 위쪽 dx=60,dy=-45.

## 체크리스트 (렌더 후)

1. 글자 잘림 없음(fs16 주의). 3줄+ 이면 h 키움.
2. 태그가 화살표·테두리에 안 물림.
3. ortho 계단 꺾임 없음(상하=중심 x, 좌우=중심 y).
4. 팬아웃 스파인이 다른 박스 관통 안 함.
5. 컨테이너가 내부 박스 다 감쌈(여백 40px+).
6. **부호·단계명이 명세서 본문·【부호의 설명】과 일치.** 바꿨으면 명세서 수정 대상 보고.
7. 양방향 화살촉 양쪽 보임.

## 누적 학습 항목

- (초기) 이 스킬은 patent-block-diagram의 자매 스킬. 작도 규칙·스키마는 그쪽 SKILL.md가 단일 진실,
  본 스킬은 "기존 pbd를 스냅샷 추출 후 스타일 보존 수정"이라는 워크플로우만 추가한다.
