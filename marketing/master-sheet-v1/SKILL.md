---
name: master-sheet-v1
description: "마스터 시트 V1 — 캐릭터(또는 제품)의 '풀 에디토리얼 바이블'을 gpt_image_2로 만드는 스킬. 정체성·얼굴 레퍼런스·표정·헤어/메이크업·의상 멀티세트·컬러 팔레트(HEX 포함)·브랜드 컨셉·소품까지 한 장에 다 담아, 캐릭터의 다양한 오브제·디테일·색상·세계관을 통째로 lock한다. (포토리얼 기본, 일러스트 전환 가능 / 세로 매거진 레이아웃) Use this skill whenever the user wants a RICH, detail-packed master/reference sheet that preserves objects, outfits, colors, and worldbuilding — 마스터 시트, 캐릭터 바이블, 풀 캐릭터 시트, 디테일 시트, 콘셉트 시트, 룩북 시트, 의상/소품/컬러까지, IDENTITY 시트, character bible, full reference sheet, lookbook sheet, brand muse sheet. 트리거: '디테일 다 넣은 마스터 시트 · 의상·소품·컬러까지 · 풀 버전으로 · 바이블로 빼줘 · V1으로'. ⚠️ 디테일을 덜어내고 얼굴 일관성만 클린하게 뽑는 건 V1이 아니라 master-sheet-v2를 쓴다. 오브제·디테일·컬러 유지 = V1(이 스킬), 얼굴 일관성 최우선·Seedance 주입용 클린 = V2."
metadata:
  version: "1.0.0"
---

# Master Sheet V1 — 풀 디테일 에디토리얼 바이블

캐릭터 또는 제품의 **모든 디테일(정체성·얼굴·표정·헤어/메이크업·의상 멀티세트·컬러 팔레트·
브랜드 컨셉·소품)을 한 장에 담은 매거진형 레퍼런스 시트**를 `gpt_image_2`로 생성한다.
"캐릭터의 다양한 오브제·디테일·색상·세계관을 통째로 lock"이 존재 이유다.

검증 예시: `assets/reference-master-sheet.png` (PUREUM MUSE — IDENTITY / FACE REFERENCE /
EXPRESSIONS / HAIR & MAKEUP / WARDROBE / COLOR & TONE / BRAND CONCEPT, 세로 매거진).
이 섹션 구성·밀도·톤을 기준선으로 삼는다.

---

## V1 vs V2 — 무엇을 쓰나 (먼저 확인)

| | **V1 (이 스킬)** | **V2 (`master-sheet-v2`)** |
|---|---|---|
| 목적 | **오브제·디테일·컬러·세계관**까지 풀 lock | **얼굴 일관성**만 클린하게 |
| 담는 것 | IDENTITY·표정6·헤어/메이크업·의상 멀티세트·**HEX 팔레트**·브랜드 컨셉·소품 | 정면·3/4·측면·전신·표정 (헤더 텍스트만) |
| 이미지 내 텍스트 | **풍부함 = 기능** (라벨·스펙·HEX·설명) | **헤더만** (hex·긴 설명 금지) |
| 레이아웃 | **세로 2:3 매거진** | 가로 3:2 클린 그리드 |
| glitch 리스크 | 텍스트 많아 높음(감수) | 낮음(우선) |
| 쓸 때 | 룩북·세계관·소품·팔레트가 중요 | 얼굴만 정확하면 됨 / Seedance Element 주입 |

> 둘은 '좋고 나쁨'이 아니라 **역할이 다르다.** 디테일을 다 보여줘야 하면 V1, 얼굴 흔들림 없이
> 영상에 주입하는 게 핵심이면 V2. 실무 팁: **V1로 세계관·컬러를 잡고, 그 안의 정면 1컷을
> 별도로 깨끗이 뽑아(또는 V2로) Element 락**에 쓰면 둘의 장점을 다 가진다.

---

## STYLE — 기본 포토리얼 (전환 가능)

- **기본값: 포토리얼 에디토리얼** (PUREUM처럼 — 자연광 인물 사진 톤, 매거진 화보).
- 프로젝트가 애니/일러스트면 **일러스트 모드로 전환**(셀셰이딩/Pixiv 톤 등) — STYLE 블록만 교체.
- 어느 쪽이든 **얼굴·헤어·메인 의상·비율 = 전 패널 동일**이 절대 규칙.

## STEP 1 — 모드 판별
| 입력 | 모드 |
|---|---|
| 인물/캐릭터/배우/모델/페르소나/브랜드 뮤즈 | **CHARACTER** (기본) |
| 제품/패키지/보틀/캔/박스/굿즈 (풀 스펙 바이블) | **PRODUCT** |

첨부 이미지가 있으면 "첨부 인물/제품과 **동일한 외모·복장·형태**"를 자연어로 명시(@표기 금지).
없으면 설명에서 스펙 확정. 부족한 핵심 변수만 1~2개 질문(이름/컨셉, 핵심 의상/팔레트). 비율은 묻지 않음.

---

## STEP 2 — 섹션 구성 (CHARACTER 바이블 · PUREUM 기준)

세로 2:3 매거진. 좌측 대형 히어로 + 우측/하단 정보 패널. **필요한 섹션만 골라 채운다**
(전부 넣으면 풍부하지만 글자 밀도↑ — 핵심 6~8섹션 권장).

1. **히어로(HERO)** — 좌측 대형 인물 컷(환경 포함 가능) + 브랜드 워드마크 대형 세리프 + `VOL.00x`
2. **캐릭터 / IDENTITY** — 이름(Name)·나이(Age)·신장(Height)·국적(Nationality)·컨셉(Concept)·프로필(Profile, 한국어 2~3줄)
3. **얼굴 특징 / FACE REFERENCE** — 핵심 특징(얼굴형·눈·코·입술·피부 한국어 서술) + **얼굴 레퍼런스 4컷**: 정면(Front)·3/4(Three-quarter)·측면(Profile)·미소(Soft smile)
4. **표정 / EXPRESSIONS** — **얼굴 클로즈업 6컷** (예: 차분·미소·응시·사색·청춘·그리움), 전부 동일 인물·동일 스타일
5. **헤어 & 메이크업 / HAIR & MAKEUP** — 헤어(컬러·스타일·디테일) + 메이크업(베이스·아이·립·블러셔) 서술 + 디테일 2컷(헤어 측면·메이크업 글로즈업)
6. **의상 / WARDROBE** — **의상 멀티세트(보통 4)**: 메인(MAIN)·세트(예 Sailor Full Set)·일상(Casual)·여름(Summer), 각 전신/반신 + 아이템 한국어 설명
7. **컬러 & 톤 / COLOR & TONE** — **컬러 스와치 6 + 이름 + HEX**(예 스카이블루 #6FB6E8 …) + 톤 태그라인 1줄
8. **브랜드 컨셉 / BRAND CONCEPT** — 브랜드 설명 박스 + 추천 캠페인 톤(Recommended campaign tone) 불릿
* (선택) **소품 / PROPS**, **무드 / MOOD BOARD**, **포즈 / POSES**, **스타일링 분해 / STYLING** — 세계관·소품이 중요한 프로젝트에 추가.

> PRODUCT 바이블이면: 히어로 + 360(정면/측면/후면) + 디테일 인서트 + **라벨 전개도(dieline)** +
> 스펙(용량/소재) + **컬러 팔레트 HEX** + 브랜드 컨셉. (V2와 달리 스펙·전개도·hex를 **시트 안에 포함**)

---

## STEP 3 — gpt_image_2 호출 스펙
```
model: gpt_image_2
aspect_ratio: "2:3"     # 세로 매거진 (디테일 섹션 수용). 가로 한 줄 요약형만 "3:2"
resolution: "2k"
quality: "high"
count: 1
```
첨부 레퍼런스가 있으면 `medias[].role="image"` 업로드(자연어 "첨부와 동일", @표기 금지).

---

## STEP 4 — 프롬프트 템플릿 (복붙용, 빈칸만 채움 · CHARACTER)

```
You are an editorial photographer, art director, and character designer. Generate ONE rich CHARACTER MASTER BIBLE — a magazine-style multi-section reference sheet on a clean cream/ivory background, portrait orientation. Photoreal editorial unless otherwise noted.

[HERO]
Large left portrait of the character (environment allowed). Big serif brand wordmark "[브랜드]" + "[부제 / KOREAN ... LIFESTYLE BRAND]" + "VOL.00[x]".

[IDENTITY 캐릭터/IDENTITY]
이름(Name): […]  나이(Age): […]  신장(Height): […]  국적(Nationality): […]
컨셉(Concept): […]
프로필(Profile, KOR 2–3 lines): "[…]"

[FACE REFERENCE 얼굴 특징]
Key features (KOR): 얼굴형 […] / 눈 […] / 코 […] / 입술 […] / 피부 […]
4 reference photos: 정면(Front) · 3/4(Three-quarter) · 측면(Profile) · 미소(Soft smile) — same identity

[EXPRESSIONS 표정]
Row of 6 face close-ups: [차분 / 미소 / 응시 / 사색 / 청춘 / 그리움] — identical face & hairstyle

[HAIR & MAKEUP 헤어 & 메이크업]
Hair: 컬러 […] / 스타일 […] / 디테일 […]    Makeup: 베이스 […] / 아이 […] / 립 […] / 블러셔 […]
+ 2 detail shots: 헤어 측면(Hair detail) · 메이크업 글로즈업(Makeup close-up)

[WARDROBE 의상] — 4 outfits, each full/half body + KOR item list
메인(MAIN): […]   세트([세트명]): […]   일상(Casual): […]   여름(Summer): […]

[COLOR & TONE 컬러 & 톤]
6 swatches + names + HEX: [스카이블루 #______] [네이비 #______] [크림 #______] [베이지 #______] [선골드 #______] [피치 #______]
Tagline: "[…]"

[BRAND CONCEPT 브랜드 컨셉]
Box (KOR): "[브랜드] — [설명 2–3 lines]"
추천 캠페인 톤: • […] • […] • […]

[STYLE RULES]
- Photoreal editorial portrait photography (or specified illustration style), natural soft light, SAME face/hair/main-outfit/proportions across every section.
- Clean grid-based magazine layout, large hero left, info panels right, generous negative space.
- Korean labels prominent, English in parentheses. NO Japanese text, NO watermark, NO real existing brand/logo (use the fictional wordmark only).
- This is a DETAIL-RICH bible: printing section labels, specs, HEX swatches, and short descriptions IS intended — keep each text block short and legible to avoid glyph errors.
```

---

## 텍스트 밀도 주의 (V1 특유)
V1은 의도적으로 텍스트가 많다 → 글자 깨짐 리스크가 따라온다. 줄이는 게 아니라 **블록을 짧게·정렬되게**:
- 섹션당 라벨 + 짧은 키워드(문장 길게 쓰지 않기). HEX는 6개 이하.
- 한 번에 다 안 나오면 **핵심 6~8섹션만** 먼저, 나머지(소품/무드/포즈)는 2장째로 분리.
- 시트는 "보이는+읽는 통합 바이블", 그래도 **Element 락은 별도**: 시트 안 정면 1컷을 깨끗이 다시 뽑아
  락 소스로(또는 `master-sheet-v2`로). 멀티섹션 시트 통째 주입보다 영상 전이가 안정적.

## STEP 5 — 산출 후
1. 결과 위젯 확인(자동 폴링 — 재폴링 금지).
2. 세계관/디테일 OK → 콘티는 `storyboard-v1`(전체) → `storyboard-v2`(핵심 컷)로.
3. 수정은 해당 섹션만 좁혀 재생성.

## 안티-페일 체크리스트
```
✓ 세로 2:3 매거진, 밝은 크림 배경, 좌측 대형 히어로?
✓ 핵심 6~8섹션 채움(IDENTITY/FACE/표정/헤어메이크업/의상/컬러HEX/브랜드)?
✓ 얼굴·헤어·메인 의상·비율이 전 패널 동일?
✓ 의상 멀티세트 + 컬러 스와치 HEX 포함(V1의 핵심)?
✓ 한국어 라벨 + 영문 괄호, 일본어 0, 워터마크 0, 실제 브랜드 0?
✓ 텍스트 블록이 짧고 정렬됨(과밀로 안 깨짐)?
✓ Element 락은 별도 정면 1컷으로 분리 권장?
```
하나라도 실패면 수정 후 산출.
