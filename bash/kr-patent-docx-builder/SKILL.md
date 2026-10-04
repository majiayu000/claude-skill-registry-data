---
name: kr-patent-docx-builder
description: 한국 특허청 양식의 명세서 docx 빌드 인프라. 명세서 본문 텍스트를 JSON/JS 객체 형태의 콘텐츠로 받아 나눔고딕·청구항 들여쓰기·표준 섹션 헤더(【발명의 명칭】 등)·부호의 설명표 등 한국 특허청 별지 양식을 따르는 docx 파일을 자동 생성. 매번 docx 생성 코드를 처음부터 짜는 대신 본 스킬의 재사용 가능한 빌드 스크립트를 호출. "docx 빌드", "명세서 docx", "한국 특허 양식 docx", "워드 출력", "최종 docx", "출원용 docx", "build patent docx" 같은 표현이 보이면 사용. 다른 한국 특허 명세서 스킬(kr-patent-spec-drafting 등)에서 본문이 준비된 뒤 최종 산출물 단계에서 호출되는 인프라성 스킬.
---

# 한국 특허 docx 빌더

## 무엇을 하는가

명세서 본문 콘텐츠(텍스트, 청구항, 부호의 설명 등)를 표준화된 JS 객체 형태로 받아, **한국 특허청 별지 양식을 따르는 docx 파일을 자동 생성**한다.

**핵심 가치**: 매번 명세서 docx를 만들 때마다 폰트/들여쓰기/섹션 헤더 코드를 다시 짜지 않아도 된다. 본 스킬의 빌드 스크립트가 이미 검증된 양식을 적용한다.

## 핵심 파일

- `scripts/build_kr_patent.js` — 메인 빌드 스크립트. content 객체를 받아 docx 생성
- `references/content-schema.md` — content 객체의 스키마 (어떤 필드를 채워야 하는지)
- `references/example-content.js` — 샘플 content 파일

## 사용 방법

### Step 1. 필요 패키지 설치 (최초 1회)

```bash
# 본 스킬 디렉토리에서 1회만 실행. docx 패키지가 로컬 설치됨.
cd kr-patent-docx-builder
npm install
```

(package.json의 dependencies — `docx`)

### Step 2. content 객체 작성

명세서의 각 섹션을 채우는 JS 객체를 작성한다. 스키마는 `references/content-schema.md` 참조.

작업 디렉토리에 `content.js` (필요 시 `content_part1.js`, `content_part2.js`, … 분할) 파일을 생성한다.

```javascript
// content.js (최소 골격)
module.exports = {
  metadata: {
    file_label: "_법인명__관리번호_명세서초안01_담당자__YYYYMMDD_발명명",
    invention_title: "예시 발명의 명칭",
    representative_drawing: "도 1"
  },
  technical_field: "본 발명은 입자 가속기의 빔 진단 기술에 관한 것이다.",
  background: [
    "<배경 1단락>",
    "<배경 2단락>",
    "<배경 3단락>",
    "<배경 4단락 - 해결과제로의 브릿지>"
  ],
  problem_to_solve: [
    "본 발명의 첫 번째 목적은, ~ 위한 것이다.",
    "본 발명의 두 번째 목적은, ~ 위한 것이다."
  ],
  solution: [
    "<해결수단 단락 1>",
    "<해결수단 단락 2>"
  ],
  effects: [
    "<효과 1 (3단 인과 구조)>",
    "<효과 2>"
  ],
  drawings_brief: [
    { fig: "도 1", desc: "본 발명의 일 실시예에 따른 X를 보인 블록도이다." }
  ],
  detailed_description: [
    "<실시예 도입부 표준 문구>",
    "<도 1 실시예 단락>",
    "<도 2 실시예 단락>"
  ],
  // symbols: [ ... ]   // ⚠ default: 생략. 한국 변리사 실무상 【부호의 설명】
                          // 섹션은 의도적으로 두지 않는 게 권리범위 보호·검토 부담
                          // 양면에서 유리. symbols 키 자체를 누락 또는 [] 빈 배열로 두면
                          // 빌더가 해당 섹션을 건너뜀. 사용자가 명시적으로 두기로
                          // 결정한 경우에만 다음 형태로 채움:
                          //   symbols: [
                          //     { num: "10", name: "슬릿 스캐너" },
                          //     { num: "100", name: "빔 진단 시스템" },
                          //   ],
  claims: [
    "[청구항 1] ~를 포함하는 X 시스템.",
    "[청구항 2] 제1항에 있어서, ~인 것을 특징으로 하는 X 시스템."
  ],
  abstract: "본 발명은 ~에 관한 것이다. ~를 통해 ~한 효과를 얻을 수 있다."
};
```

### Step 3. 빌드 실행

```bash
cd <작업 디렉토리>
node /path/to/skill/scripts/build_kr_patent.js \
    --content ./content.js \
    --output /mnt/user-data/outputs/<filename>.docx
```

또는 더 간단하게 (작업 디렉토리에서):

```bash
cp /path/to/skill/scripts/build_kr_patent.js ./build.js
node build.js
```

이때 `build.js`는 동일 디렉토리의 `content.js`를 자동 로드.

### Step 4. 검증

```bash
python3 /mnt/skills/public/docx/scripts/office/validate.py <output.docx>
extract-text <output.docx> | head -50
```

## 표준 양식 사양 (자동 적용)

빌드 스크립트가 자동으로 적용하는 사양은 아래와 같다. 사용자가 별도로 신경 쓸 필요 없음.

| 항목 | 값 |
|---|---|
| 폰트 (한글) | 나눔고딕 |
| 폰트 (영문·숫자) | 나눔고딕 (eastAsia + hAnsi + hAnt 모두 지정 — 폰트 일관성) |
| 본문 폰트 크기 | 11pt (Half-point 22) |
| 섹션 타이틀 폰트 크기 | 12pt (24) |
| 줄 간격 | 360 (1.5배 정도) |
| 본문 단락 들여쓰기 | firstLine 280 DXA (약 2글자) |
| 청구항 들여쓰기 | firstLineChars 300 또는 firstLine 677 DXA |
| 정렬 | 본문 양쪽 정렬, 섹션 타이틀 좌측 정렬 또는 중앙 |
| 페이지 크기 | A4 |
| 여백 | 한국 특허법 시행규칙 별지 양식 기준 |
| 섹션 헤더 표기 | 【발명의 명칭】, 【기술분야】 등 한국 표준 |

## content 객체 분할 전략 (대규모 명세서)

명세서가 길어지면 content.js를 부분 파일로 분할.

```
content.js              # 전체 모음 (require로 부분 import)
content_part1.js        # 발명 명칭, 기술분야, 배경, 해결과제
content_part2.js        # 해결수단
content_part3.js        # 효과, 도면 설명
content_part4.js        # 실시예 (가장 큼)
content_part5.js        # 부호 설명, 청구항, 요약, 대표도
```

`content.js`:
```javascript
module.exports = {
  ...require("./content_part1.js"),
  ...require("./content_part2.js"),
  ...require("./content_part3.js"),
  ...require("./content_part4.js"),
  ...require("./content_part5.js")
};
```

## 파일 명명 규칙 ★ (2026-07-14 확정, 이전 패턴 폐기)

```
[<사무소관리번호>][<고객REF>]<발명의명칭_공백제거>.docx
```

예:
```
[사건 C][P26014KR]공정진척도산출방법및시스템.docx
[사건 E][사건 E]자연어기반EPICS제어프로그램자동생성방법및시스템.docx
```

규칙:
- 대괄호 2개를 앞에 붙이고 그 뒤에 발명의 명칭을 **공백 없이** 이어 붙인다.
- 첫 번째 대괄호 = 사무소 내부 관리번호, 두 번째 = 고객/출원 REF. 두 번호는 케이스 폴더명 또는 원본 청구항 docx 파일명에서 확인 가능(예 `[대학·공공 고객]IPYYYY-NNNN[사건 E]`, `사건 E_사건 E_청구항_….docx`).
- 발명의 명칭은 【발명의 명칭】 국문 그대로에서 공백만 제거(영문 병기 `{...}` 부분은 제외). 명칭은 "…방법 및 시스템" → `…방법및시스템`.
- 법인명·담당자·날짜·버전은 파일명에 넣지 않는다(구 패턴 `_법인명__관리번호_명세서초안NN_담당자__YYYYMMDD_발명명` 폐기).

`metadata.file_label` 필드를 위 형식으로 채우면 빌드 스크립트가 그대로 파일명에 사용한다.

## 도면 처리

본 스킬은 명세서 본문만 다룬다. 도면은 별도 처리:
- 도면 placeholder (도 1 ~ 도 N)만 본문에 포함
- 실제 도면 파일은 사용자가 별도로 첨부하여 출원

도면 placeholder는 빌드 스크립트가 자동으로 도면설명 섹션 끝에 또는 별도 페이지에 둔다.

## 컴파운딩 루프 (개선 메모)

빌드 스크립트의 양식이 특허청·법인 검토 과정에서 지적받은 패턴은 scripts/build_kr_patent.js를 직접 수정하여 누적. 다음 사용 시 자동으로 개선된 양식이 적용됨.

### 누적 양식 개선
- (예시) 청구항 단락 간 후방 간격을 추가로 0.5줄 띄우는 것이 검토자에게 가독성 좋다는 피드백 → 스크립트에 반영
- (2026-05-28) 외부에서 받은 도면 또는 docx 인계 시점에 docx 안 word/media/ 추출 + 외부 도면 폴더와 sha256 비교 → 도면 버전 차이 즉시 검출. 빌더 또는 정합성 점검 인프라성 스크립트로 추가. 옛 도면 폴더 기준으로 정합성 진단 시 잘못된 결함 보고 발생 사례 있음.
- (2026-05-28) OneDrive 한글 경로(OneDrive\문서\...) 안 docx 작업 시 파일 잠금·인코딩 충돌이 잦음 → C:\Users\<user>\_v<N>.docx 식 ASCII 경로 작업 사본 생성 → 작업 → OneDrive 복귀 패턴이 default. python-docx 스크립트 첫 줄에 os.environ['PYTHONIOENCODING']='utf-8'; sys.stdout.reconfigure(encoding='utf-8') 보일러플레이트 자동 삽입. 사례: v9/v10/v11 라운드 모두 동일 패턴 적용.
- (2026-05-28) 사용자 빌드 default 확정: 폰트 '맑은 고딕', 본문 12pt (size half-points 24), 줄간격 2.0 (spacing.line 480), 섹션 헤더 outline level 자동 부여 (Level 1: 【발명의 설명】·【청구범위】·【요약서】·【대표도】 / Level 2: 【발명의 명칭】·【기술분야】·【발명의 배경이 되는 기술】·【발명의 내용】·【도면의 간단한 설명】·【발명을 실시하기 위한 구체적인 내용】·【부호의 설명】·【요약】 / Level 3: 【해결하고자 하는 과제】·【과제의 해결 수단】·【발명의 효과】). buildDocument 첫 줄에 【발명의 설명】 컨테이너 헤더 출력 강제. sectionTitle(text, {level: N})·buildSection(title, paras, {level: N}) 시그니처로 호출.
- (2026-05-28 교정) outline level 정본 구조는 사용자 사건 A v11 정본 기준으로 재정렬. **Level 1 (4개 컨테이너)**: 【발명의 설명】·【청구범위】·【요약서】·【도면】. **Level 2**: 【발명의 명칭】·【기술분야】·【발명의 배경이 되는 기술】·【발명의 내용】·【도면의 간단한 설명】·【발명을 실시하기 위한 구체적인 내용】·【청구항 N】(각 청구항마다)·【요약】·【대표도】·【도면 N】(각 도면마다). **Level 3**: 【해결하고자 하는 과제】·【과제의 해결 수단】·【발명의 효과】·【본 발명 시작】·실시예 본문 1단 소제목 ('1. 시스템 구성', '2. 디지털 트윈 모델 생성' 등). **Level 4**: 실시예 본문 2단 소제목 ('2-1.', '2-2.', '6-1.' 등). buildClaims는 청구항마다 【청구항 N】 헤더 자동 출력, buildDrawingsSection으로 【도면】 컨테이너 + 【도면 N】 페이지 출력, buildDetailedDescription으로 실시예 본문 sub-heading 객체({heading, level, paragraphs}) 지원. 【대표도】는 L1 아닌 L2.
- (2026-05-28) python-docx의 insert_paragraph_before(ref_para, txt) 다중 신설 시 순서 동작 — ref_para가 고정된 채 정순으로 [a, b, c, d] 삽입 시 결과는 [..., a, b, c, d, ref_para] 순서로 누적 (각 삽입이 ref_para 바로 앞에 추가되므로 직전 삽입분은 한 칸 앞으로 밀림). reversed(list) 호출 시 결과는 역순으로 출력됨. 신설 단락 순서가 의도와 일치하는지 항상 검증 단계 필요 — d.paragraphs 재로딩 후 인덱스 출력으로 verify. 보일러플레이트: for txt in new_paras: ref_para.insert_paragraph_before(txt) — 정순 사용이 default. 사례: v12 첫 시도에서 reversed로 삽입하여 결과 순서가 역순으로 나옴(정의 단락이 변형 단락 뒤에 위치) → 정순으로 재실행.

## 자주 발생하는 빌드 오류

| 증상 | 원인 | 해결 |
|---|---|---|
| `Cannot find module 'docx'` | docx 패키지 미설치 | `cd kr-patent-docx-builder && npm install` |
| docx 파일이 열리지 않음 | 빌더 코드 오류로 invalid xml 생성 | validate.py 실행하여 오류 메시지 확인 |
| 한글이 깨져 보임 | 폰트 hint 누락 | TextRun 생성 시 `font: { name: "나눔고딕", eastAsia: "나눔고딕", hAnsi: "나눔고딕" }` 명시 |
| 청구항 들여쓰기 불일치 | firstLineChars vs firstLine 혼용 | 한 가지로 통일 |
- (2026-07-14, 사건 E) **본문·청구항 들여쓰기 firstLine=800 (사용자 선호)** — 빌더 기본 body_first_line=280은 사용자가 원하는 탭 간격과 다름. 대학 고객 사건 최종본([최종][사건 A] 명세서초안_담당 변리사.docx) 실측 기준: 본문 firstLine=800/jc=both, 청구항도 firstLine=800(claim_hanging=0, 매달림 미사용), 섹션 헤더 before=320/after=200/line=480. 전역 기본값은 280 유지 중이므로 건별 로컬 복사본(build_local.js)에서 INDENT.body_first_line=800·claim_first_line=800·claim_hanging=0·SPACING.section_before=320·section_after=200으로 수정 후 NODE_PATH=<skill>/node_modules 지정하여 실행.
- (2026-07-14, 사건 E) **Level 1 컨테이너 헤더 가운데 정렬 + 도면 간단한 설명 들여쓰기 (사용자 선호)** — (1) sectionTitle에서 level===1(【발명의 설명】·【청구범위】·【요약서】·【도면】, 탐색창 최상위 4요소)은 AlignmentType.CENTER. (2) buildDrawingsBrief의 각 도면 설명 줄에 indent { firstLine: INDENT.body_first_line } 추가(본문과 동일 들여쓰기). 사용자가 수정본에서 직접 반영한 서식. [[feedback_kr_patent_docx_indent]]
- (2026-07-14, 사건 E) **실시예 소목차(Level 3) 빌드 패턴** — detailed_description을 [도입부 문자열들, {heading, level:3, paragraphs} 소목차 객체들, 맺음말 문자열]로 구성하면 buildDetailedDescription이 【N. 제목】을 outlineLvl 2(탐색창 하위)로 출력. spec_draft.md에 【N. 제목】 마커를 넣고 파서가 이를 top-section이 아닌 소목차로 인식하도록 분기(정규식: 숫자.으로 시작하는 【…】는 소목차, 그 외는 top-section). 맺음말("한편, 상기의 상세한 설명은…")은 마지막 소목차에서 pop하여 무번호 trailing 문단으로 배치. ⚠️마커 삽입 앵커 주의: 【도면의 간단한 설명】의 '도 N은 …순서도이다' 문장과 실시예 본문의 도N 도입 문장이 동일하면 replace 1회가 간단한 설명에 잘못 삽입됨 → 실시예 쪽은 다음 문장(예 '도 N을 참조하면,')을 포함한 2줄 앵커로 유일화. 재사용 스크립트: scratchpad gen_content.py.
- (2026-07-14, 사건 E) **【도면】 섹션에 이미지 실제 삽입** — figures를 [{num, path}] 로 주면 buildDrawingsSection이 【도면 N】 헤더 + 중앙정렬 ImageRun + PageBreak(도면당 1페이지)를 출력하도록 확장. docx 라이브러리의 ImageRun 사용, PNG 크기는 IHDR(width@16, height@20 big-endian uint32) 직접 파싱하여 종횡비 유지 스케일. **표시 크기 상수: FIG_MAX_W=620px, FIG_MAX_H=780px (@96dpi)** — A4 본문영역(약 650x930px)에서 헤더와 여백을 뺀 값. MAX_H를 850으로 두면 세로형 도면(예 1178x1995)이 2페이지로 넘침 → 780이어야 1페이지에 들어감(실측). 도면 파일명은 공백 유무가 제각각인 경우가 많으므로(도면1.png vs "도면 5.png") 번호-파일명 명시 매핑 권장. 검증: word/media/ 이미지 수, <w:drawing> 수, PageBreak 수, PDF 변환(soffice --headless --convert-to pdf) 후 도면별 페이지 확인.
- (2026-07-14, 사건 E 보정) **도면 1페이지 1도면 보장 = PageBreak 문단이 아니라 pageBreakBefore** — 이미지 뒤에 PageBreak 문단을 넣는 방식은 렌더러(Word vs LibreOffice)에 따라 도면이 2페이지로 넘치거나 밀린다. sectionTitle에 opts.pageBreakBefore를 추가하여 【도면 N】 헤더 자체에 pageBreakBefore:true를 걸 것(첫 도면은 【도면】 컨테이너와 같은 페이지이므로 idx>0에만). 【도면】 컨테이너 헤더에도 pageBreakBefore:true. 표시 크기는 **FIG_MAX_W=600, FIG_MAX_H=720 (@96dpi)** 로 여유를 둘 것 (780은 Word에서 넘칠 여지 있음). 검증: PDF 변환 후 도면 번호별 페이지가 연속 1씩 증가하는지 확인.
- (2026-07-14, 사건 E) **Level 1 대목차는 새 페이지에서 시작** — 【청구범위】·【요약서】·【도면】 sectionTitle에 pageBreakBefore:true 부여(buildClaims / 요약서 buildSection / buildDrawingsSection). ⚠️【발명의 설명】은 문서의 첫 요소이므로 pageBreakBefore를 걸지 말 것(LibreOffice에서 선행 빈 페이지가 생길 수 있음). 검증: PDF 변환 후 대목차별 시작 페이지가 서로 다른 페이지인지, 1페이지가 【발명의 설명】인지 확인.
- (2026-07-14, 사건 E) **⚠️ 사용자가 손댄 산출물 docx를 절대 무단 덮어쓰지 말 것** — 같은 경로에 반복 빌드·복사하다가 사용자가 Word로 직접 넣은 편집(청구항·발명의 명칭 탭 삽입)을 통째로 날린 사고 발생. 규칙: (1) 케이스 폴더의 기존 산출물을 덮어쓰기 전에 반드시 **내 마지막 빌드와 diff**하여 사용자 편집 유무를 확인한다 (python-docx로 문단 텍스트 + <w:tab/> 개수 + w:ind 비교). (2) 차이가 있으면 덮어쓰지 말고 사용자에게 알린다. (3) 복구는 OneDrive 버전 기록 안내. - 참고: 이 사무소 청구항 서식에는 **firstLine 들여쓰기 대신 문단 첫머리 실제 탭 문자** 방식이 쓰이기도 함 — `<w:pPr><w:tabs><w:tab w:val="left" w:pos="1021"/></w:tabs></w:pPr>` + 런 시작에 `<w:r><w:tab/></w:r>` (w:ind 없음). 독립항.docx 사례. 사용자 확인 후 빌더에 반영할 것.
- (2026-07-14, 사건 E) **★ 발명의 명칭 + 청구항은 탭 문자 들여쓰기 (firstLine 아님)** — 사무소 서식 확정. `docx` 라이브러리에서 `const { Tab, TabStopType } = require("docx")` 후, 문단에 `tabStops: [{ type: TabStopType.LEFT, position: 1021 }]` 를 주고 런을 `new TextRun({ children: [new Tab(), text], font, size })` 로 만들어 **문단 첫머리에 실제 `<w:tab/>`** 를 넣는다. 해당 문단에는 **`indent`(firstLine)를 주지 않는다**(탭이 들여쓰기를 담당). 적용 대상: 【발명의 명칭】 본문 1문단 + 【청구항 N】 각 청구항의 모든 본문 문단. 본문(기술분야·배경·해결수단·효과·실시예)은 종전대로 firstLine=800 유지(탭 없음). 검증: `<w:tab/>` 개수 == 1 + 청구항 문단 수, `w:pos="1021"` 동수, 해당 문단에 `<w:ind>` 부재. 원본 근거: 사무소 독립항.docx.
- (2026-08-11, 사건 G) **★ 청구항 줄 분할 = 빌더 기본 동작으로 승격** — 사용자가 산출물을 열어 직접 청구항을 여러 문단으로 쪼갠 것을 확인하고 규칙화. `LAYOUT.claim_tab`(기본 true, 청구항·발명의 명칭을 실제 탭 문자로 들여쓰기)와 `LAYOUT.claim_linebreak`(기본 true, 구성요소 경계마다 문단 분할)를 신설하고 `splitClaimLines()`·`tabPara()`·`claimParas()`를 빌더에 추가. 분할 규칙: ①종속항 전제부 `제N항에 있어서,` 1행 분리 ②방법항 `단계;` / `단계; 및` 뒤 분할 ③시스템·장치항 `~부; 및` 뒤 분할 ④시스템·장치·프로그램항의 `~하고,` / `~하며,` 뒤 분할. **⚠️ ④를 방법항에 적용하면 안 된다** — 단계 내부의 `~검출하고,`에서 잘못 끊긴다. 청구항 말미가 시스템·장치·서버·단말·프로그램으로 끝나는지로 판정하여 차단하도록 구현됨. content의 `claims[i]`를 `{num, text:[...]}` 배열로 주면 사용자가 이미 나눈 것으로 보고 자동 분할을 건너뛴다. 검증: `<w:tab/>` 개수 == 명칭 1 + 전체 청구항 줄 수, `<w:ind>` 0건.
- (2026-08-11, 사건 G) **⚠️ OneDrive 케이스 폴더 산출물은 Word가 열려 있으면 PermissionError** — 사용자가 검토하려고 열어 둔 상태가 흔하다. `shutil.copy` 가 `[Errno 13] Permission denied`로 실패하면 파일 손상이 아니라 잠금이다. 대처: 같은 폴더에 `_v2` 접미 파일로 저장하고 사용자에게 Word를 닫아 달라고 요청한 뒤 백업 → 덮어쓰기. 잠긴 파일은 읽기도 실패하므로 diff 대조도 그 시점엔 불가.
- (2026-08-11, 사건 G) **청구범위 단독 docx** — 명세서 본문 없이 청구항만 산출할 때는 `content` 에 `invention_title` + `claims` 만 채우면 된다. buildDocument가 【발명의 설명】 컨테이너와 【발명의 명칭】, 【청구범위】만 출력한다. 파일명은 명명 규칙에 `_청구범위` 접미를 붙여 명세서 전문과 구분.
- (2026-07-14, 사건 E) **코드 블록 붙여쓰기 = 시도했다가 사용자가 되돌림 (기본 적용 금지)** — 워킹 이그잼플의 식별자 목록/.db/.proto 줄을 codePara(spacing {before:0, after:0, line:240}, indent {left:800})로 붙여서 출력해 보았으나, 사용자가 **"그전 버전으로 가자"며 본문과 동일한 서식(firstLine=800, line=480, after=120)으로 되돌림**. → **코드 줄도 산문과 같은 본문 서식이 기본**. codePara / {code:"..."} 렌더 경로는 빌더에 남아 있으나 사용자가 명시적으로 요청할 때만 사용할 것.
