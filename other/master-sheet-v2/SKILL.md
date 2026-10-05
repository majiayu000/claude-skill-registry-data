---
name: master-sheet-v2
description: "마스터 시트 V2 — 캐릭터·제품의 '클린 일관성 레퍼런스 시트'를 gpt_image_2로 만드는 스킬. 정면·3/4·측면·전신·표정만 큰 패널로 깔끔하게(헤더 텍스트만, hex·디테일·긴 설명 없음) 뽑아 얼굴/형태 일관성을 최우선으로 잡는다. 큰 정면 포트레이트가 Seedance Element 주입 시 일관성 유지력을 높인다. 사용자가 '마스터 시트, 레퍼런스 시트, 캐릭터 시트, 제품 시트, 콘셉트 시트, character sheet, reference sheet, turnaround, 360 뷰, Element 락용 시트, 깔끔한 일관성 시트'를 원하거나 Higgsfield/Seedance 일관성 레퍼런스 한 장이 필요할 때 사용. 첨부 이미지로 '이 인물/제품으로 시트 만들어줘'에도 트리거. 트리거: '마스터 시트/캐릭터 시트 만들어줘 · 시트로 빼줘 · V2로 · Element 락용으로 · 얼굴 일관성 중요'. ⚠️ 의상 멀티세트·소품·컬러 팔레트(HEX)·세계관까지 디테일을 다 담는 풀 바이블은 V2가 아니라 master-sheet-v1을 쓴다. 얼굴 일관성 최우선·클린 = V2(이 스킬), 디테일·오브제·컬러 = V1."
metadata:
  version: "2.1.0"
---

# Master Sheet v2 — 포토리얼 레퍼런스 시트 빌더

캐릭터 또는 제품의 **마스터 시트(여러 앵글·디테일이 한 장에 정리된 레퍼런스 시트)**를
`gpt_image_2`로 생성한다. 결과물은 Higgsfield/Seedance Element 락, 광고·드라마 캐릭터
일관성, 제품 패키지 콘티의 **단일 진실 소스**로 쓰인다.

검증된 예시: `assets/reference-character-sheet-v2.png` (들결 우먼 — 정면·3/4·측면·전신·표정),
`assets/reference-character-sheet.png` (지우). 이 레이아웃·톤·텍스트 밀도(헤더만)를 기준선으로 삼는다.

---

## V1 vs V2 — 무엇을 쓰나 (먼저 확인)

| | **V1 (`master-sheet-v1`)** | **V2 (이 스킬)** |
|---|---|---|
| 목적 | 오브제·디테일·컬러·세계관 풀 lock | **얼굴/형태 일관성**만 클린하게 |
| 담는 것 | IDENTITY·표정6·헤어메이크업·의상 멀티세트·**HEX 팔레트**·브랜드 컨셉·소품 | 정면·3/4·측면·전신·표정 |
| 이미지 내 텍스트 | 풍부함 = 기능 | **헤더만** (hex·긴 설명 금지) |
| 레이아웃 | 세로 2:3 매거진 | **가로 3:2 클린 그리드** |
| 쓸 때 | 룩북·세계관·소품·팔레트 중요 | **얼굴만 정확 / Seedance Element 주입** |

→ "디테일 다 넣은 마스터 시트/바이블" = **V1**. "얼굴 일관성·Element 락용 클린 시트" = **V2(이 스킬)**.

## V2의 절제 원칙 (반드시 지킬 것)

V2는 **일부러** 정보를 덜어낸다. 디테일·오브제·컬러까지 한 장에 담아야 하면 **`master-sheet-v1`**(풀 바이블)을
쓰고, 여기서는 **얼굴/형태 일관성**만 잡는다. hex·라벨 전개도·콜아웃 리더선·긴 설명을 욱여넣으면
gpt_image_2에서 **글자 깨짐 / 잡 실패**가 잦다(구 v1의 실패 모드). 그래서 V2의 철칙:

1. **포토리얼 우선.** 별도 지정 없으면 일러스트가 아니라 **포토리얼 스튜디오/에디토리얼**.
   (캐릭터=자연광 인물 사진 톤, 제품=클린 커머셜 product photography)
2. **패널 ≤ 6개.** 더 넣지 않는다. 욕심내면 깨진다.
3. **이미지 안 텍스트는 '패널 헤더'만.** 예: `정면(FRONT)`, `측면(SIDE)`, `표정(EXPRESSION)`.
   hex 코드·전개도·긴 콜아웃·문단 설명을 **이미지에 박지 않는다.**
   (컬러 팔레트/스펙/전개도가 필요하면 **이미지 대신 별도 문서**로 뺀다 — 아래 참조.)
4. **얼굴/의상/조명/제품형태 = 모든 패널에서 동일.** 일관성이 시트의 존재 이유.
5. **기본 비율 3:2 가로** (시트는 가로가 안정적). 세로 캐릭터 1컷만 필요하면 2:3/3:4.

---

## STEP 1 — 모드 판별

| 입력 | 모드 |
|---|---|
| 인물/캐릭터/배우/모델/페르소나 | **CHARACTER** |
| 제품/패키지/보틀/캔/박스/굿즈 | **PRODUCT** |

첨부 이미지가 있으면: "첨부 인물/제품과 **동일한 외모·복장·형태**"를 자연어로 명시
(참조 표기 @ 금지). 없으면 사용자 설명에서 외형 스펙을 확정한다.

부족한 핵심 변수만 1개씩, 최대 2개 질문(이름/역할, 핵심 의상 or 라벨 스펙). 비율은 묻지 않음.

---

## STEP 2 — 레이아웃 선택 (검증된 패널 세트)

### CHARACTER 시트 (기본) — 가로 3:2
좌측 대형 **정면(FRONT)** 포트레이트 + 우측·하단에:
- **3/4** (45° 반측면)
- **측면(SIDE)** 프로필
- **전신(FULL BODY)** (메인 의상, 발끝까지)
- **표정(EXPRESSION)** 2~3컷 (기본/미소/놀람 등) — 작은 헤드 클로즈업 행

> 동일 인물·동일 헤어·동일 메인 의상·동일 광질. 배경은 톤 통일(뉴트럴/거리).

### PRODUCT 시트 (기본) — 가로 3:2
좌측 대형 **히어로(HERO)** 1컷 + 우측·하단에:
- **정면(FRONT) / 측면(SIDE) / 후면(BACK)** 360 행 (동일 보틀)
- **디테일(DETAIL)** 2~3 인서트 (캡 / 배지·로고 / 핵심 마감) — 헤더만, 리더선 남발 금지

> 동일 보틀 실루엣·동일 라벨·동일 음료색. 라벨에 박히는 글자는 **워드마크+핵심 카피만**.

선택 헤더만 한/영 병기(`히어로(HERO)`), 그 외 이미지 내 텍스트 금지.

---

## STEP 3 — gpt_image_2 호출 스펙

```
model: gpt_image_2
aspect_ratio: "3:2"   # 시트 기본. 세로 단일컷만 "2:3"/"3:4"
resolution: "2k"
quality: "high"
```
첨부 레퍼런스가 있으면 medias[].role="image"로 업로드(자연어로 "첨부와 동일" 기술, @표기 X).

---

## STEP 4 — 프롬프트 템플릿 (복붙용, 빈칸만 채움)

### ▶ CHARACTER 템플릿
```
You are a professional photographer and character art director. Generate ONE photoreal CHARACTER MASTER SHEET, clean editorial multi-panel layout on a soft neutral background.

[SUBJECT — 캐릭터]
Name/role: [이름/역할]
Appearance: [성별·나이대·헤어(길이/색)·눈·피부·체형], identical across every panel
Main outfit (LOCKED): [상의·하의·신발·가방·액세서리 — 색/소재 고정]
Vibe/tone: [예: 한국 인디 거리 스냅, 자연광, 따뜻한 톤]

[PANELS — 한 장에 6개 이하, 헤더 텍스트만 표기]
1. 정면(FRONT) — large left portrait, calm slight smile
2. 3/4 — 45° three-quarter view
3. 측면(SIDE) — clean side profile
4. 전신(FULL BODY) — full-length in the locked main outfit, head to shoe
5. 표정(EXPRESSION) — row of 2~3 head close-ups: [기본/미소/놀람 등]

[STYLE RULES]
- Photoreal portrait photography, natural soft light, consistent face/hair/outfit/lighting in EVERY panel.
- Editorial grid, generous neutral negative space.
- ONLY panel header labels printed (Korean + English in parens). NO other in-image text, NO hex codes, NO long captions, NO leader-line callouts.
- NO illustration/anime, NO 3D render, NO over-saturation, NO watermark, NO Japanese text.
```

### ▶ PRODUCT 템플릿
```
You are a commercial product photographer and packaging art director. Generate ONE photoreal PRODUCT MASTER SHEET, clean studio layout on a cream/neutral background.

[PRODUCT — 제품]
Name/wordmark: [영문 워드마크]  (라벨에 박히는 유일한 텍스트군)
Format: [예: clear 500mL PET bottle]
Contents/color: [예: golden corn-silk tea]
Cap: [색/마감]
Label: [베이스색 + 핵심 요소 1~3개: 배지/밴드/세리프 로고 — 간결하게]
Motif: [예: cold condensation droplets]

[PANELS — 5개 이하, 헤더 텍스트만 표기]
1. 히어로(HERO) — large front bottle, soft warm key light, shallow DoF
2. 360: 정면(FRONT) / 측면(SIDE) / 후면(BACK) — identical bottle row
3. 디테일(DETAIL) — 2~3 macro insets: [캡 / 배지·로고 / 마감]

[STYLE RULES]
- Photoreal commercial product photography, premium clean look, accurate label, crisp droplets.
- Consistent bottle shape/label/liquid color in EVERY panel.
- ONLY panel header labels + the product wordmark printed. NO hex codes, NO dieline/flat unwrap crammed in, NO long callouts, NO clutter, NO watermark, NO real existing brand, NO Japanese text.
```

---

## 컬러·스펙·전개도가 필요할 때 (이미지에 넣지 말 것)

팔레트 hex, 사이즈 스펙, 라벨 전개도(dieline), 소재 표 등은 **이미지가 아니라 문서**로 뺀다:
- 짧으면 채팅 인라인 표, 길면 `마크다운(.md)` 또는 `시트(.xlsx)`로 산출.
- 시트 이미지는 "보이는 레퍼런스", 스펙 문서는 "읽는 레퍼런스" — 역할 분리가 깨짐을 막는다.

---

## STEP 5 — 산출 후

1. 결과 위젯 확인(자동 폴링 — 재폴링 금지).
2. 사용자가 OK하면, Element 락은 별도 단계: **깨끗한 단일 히어로/정면 1컷**을 락 소스로 권장
   (멀티패널 시트 통째보다 생성 전이가 안정적).
3. 수정 요청 시 해당 패널/요소만 좁혀서 재생성.

---

## 안티-페일 체크리스트 (핸드오프 전 묵시 점검)

```
✓ 포토리얼? (별도 지정 없으면 일러스트 아님)
✓ 패널 6개 이하?
✓ 이미지 내 텍스트가 '패널 헤더(+제품 워드마크)'로만 한정? hex/전개도/긴 콜아웃 없음?
✓ 얼굴/의상/조명(또는 보틀/라벨/음료색) 전 패널 동일?
✓ 비율 3:2(시트) / 단일컷만 2:3·3:4?
✓ @참조 표기 0개, 워터마크·일본어 0?
✓ 컬러/스펙 요청은 이미지가 아니라 문서로 분리?
```
하나라도 실패면 수정 후 산출.
