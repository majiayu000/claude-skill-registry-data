---
name: ppt-grid-deck
description: 그리드 기반 PPT 생성 하네스(공유본) — 12×8 모듈러 그리드+24 아키타입으로 1920×1080 PPTX를 빌드, 32 완성본 룩 통째 선택. 트리거 — 'ppt-grid-deck', '그리드 덱', '그리드 기반 ppt', '24 아키타입'. 일반 'ppt 만들어줘'는 ppt-deck 우선 — 이 스킬은 명시적 호출 시.
---

## 트리거 상세

- 트리거 전체 — 'ppt-grid-deck', '그리드 덱', '그리드 기반 ppt', '24 아키타입', '그리드 PPT 하네스'를 사용자가 명시할 때.
- 캐논 출처 — 공개 디자인 캐논(Müller-Brockmann 그리드 · Zelazny 차트)에서 도출. 이미지 카드·미디어 슬롯·차트 20종 지원(본문 해당 절 참조).

# ppt-grid-deck — 그리드 기반 PPT 하네스 (공유본)

**그리드(좌표계)는 자작·불변** — 공개 디자인 캐논(Müller-Brockmann)에서 1차 원리로 도출한 12×8 모듈러 그리드(`grid.json`). 모든 레이아웃이 이 그리드 위에 앉는다. 그 위 **두 카탈로그**: ① **레이아웃 아키타입** 24종(7 family) — 슬라이드 내용에서 추론. ② **룩(look)** 32종 — 색·폰트·카드·구성 문법을 한 번에 채우는 자기완결 번들(사용자/지정에서만 선택, 내용 추론 금지).

> 이 스킬은 **완성본 공유 빌드**다. 32 룩 = 정체성(구성 문법)까지 흡수된 20룩 + 절제된 클린 격자가 곧 정체성인 12룩. 모두 빌드·시각 QA를 통과한 "다 끝난" 룩만 담았다. (룩 카탈로그를 키우는 흡수 R&D는 별도 연구 하네스 `ppt-lab-rebuild`.) 출처·자작 범위는 [`CANON.md`](CANON.md), 외부 라이선스 자산은 [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).

## 직교 4축 + 룩 번들

```
레이아웃(layout) × 스타일(style) × 팔레트(palette) × 크기(size)   + (옵션) 룩(look = style+palette+문법 번들)
```
- **레이아웃** = 24 아키타입(7 family). **슬라이드마다** spec `variant`로 선택. 내용 보고 판단(허용).
- **스타일** = 폰트(latin/ea) + 카드(radius/border/shadow/accent). `--style`. (house·myeongmungo·consulting·velis)
  - 폰트 블록은 선택적 `display: {latin, ea}` 티어 지원 — 있으면 표지/페이지헤딩(display·h1·h2)만 이 페이스로, 본문·소제목은 `latin/ea`로 렌더(없으면 본문 폰트로 폴백 = 무회귀). 세리프 룩이 표지=송명(Song Myung)으로 이 티어를 쓴다.
- **팔레트** = 색 역할 램프. `--palette`. (7종 — 유효 id: 1,2,3,4,5,6,8 / 7번은 없음)
- **크기** = 글자 크기 티어 **소/중/대**. `--size`(또는 spec `size`). 룩과 직교 — 어떤 룩에든 얹힌다. **본문 위주**로 키우고 제목은 소폭(방이 커도 제목만 비대해지지 않게). 룩의 line/tracking은 보존하고 size scale만 교체. **소=룩 본연 크기**(무회귀 기본). 본문 환산: 소≈18pt(룩 따라) · **중≈22.5pt** · **대≈25pt**. 표(matrix)는 큰 크기에서 셀이 2줄로 줄바꿈되고 행 높이가 자동 확장됨.
- **룩(look)** = 32종, style+palette(+구성 문법)를 한 번에 채우는 자기완결 번들. `--look <slug>`. 레이아웃은 항상 직교.

> 원칙: 레이아웃은 LLM이 내용에서 추론 OK. **스타일·색은 내용에서 추론 금지**(슬롭) — 룩/사용자 지정에서만.

## 실행 워크플로 (필수 — 순서 준수, 건너뛰기 금지)

> 🚩 **룩·스타일·팔레트는 LLM이 임의로 고르지 않는다.** 아래 2단계(룩 선택 게이트)를 반드시 거친 뒤에만 빌드한다. 이 확인 없이 빌드하면 규칙 위반.

1. **콘텐츠 파악** — 자료·목적·톤 확인. 레이아웃(아키타입)은 슬라이드 내용에서 추론 OK.
2. **룩 선택 게이트 (STOP — 사용자 확인 필수)**
   - **🖼 비주얼 갤러리 자동 오픈 (먼저)** — 이름만으로 32 룩을 고르기 어려우므로, 추천 전에 **룩 갤러리 HTML을 새로고침 후 브라우저로 띄운다**(색·폰트·라이트/다크를 눈으로 보고 고르게). best-effort, 실패 시 경로만 안내:
     ```bash
     cd references && python3 tools/render-look-gallery.py        # 토큰에서 즉석 생성(항상 최신)
     # WSL→Windows: Start-Process가 UNC 경로를 처리(cmd start는 UNC CWD라 거부됨)
     powershell.exe -NoProfile -Command "Start-Process '$(wslpath -w look-gallery.html)'" 2>/dev/null \
       || echo "갤러리: references/look-gallery.html 를 브라우저로 직접 여세요"
     ```
     (비-WSL/헤드리스 환경이면 자동 오픈 생략하고 경로만 안내한다.)
     갤러리는 톤(라이트/다크) 필터 + 이름·폰트 검색을 지원. (PPTX COM 렌더가 아닌 토큰 목업 — 색·폰트·톤 미리보기용. 픽셀 정확 X.)
   - 그 위에서 덱의 목적·톤에 맞는 **룩 2~3개를 근거와 함께 추천**한다(예: IR/투자 → `ppt-samsung-ir-restrained`·`ppt-goldman-ir-deck` / 컨설팅 → `ppt-mckinsey-ghost-deck`·`ppt-bcg-exhibit-deck` / 다크 키노트 → `ppt-dark-tech`·`ppt-dark-luxury-keynote` / 에디토리얼 세리프 → `ppt-luxury-editorial-serif` / 강한 포스터 → `ppt-neo-brutalism`·`ppt-swiss-editorial-bold`). 전체 목록·토큰은 [`design-tokens.json`](references/design-tokens.json)의 `looks`. (레이아웃 슬롯 와이어프레임은 별도 [`catalog.html`](references/catalog.html).)
   - 사용자가 **룩 슬러그를 직접 지정**하거나, 룩 대신 `--style`+`--palette` 조합을 고를 수도 있다 — 어느 쪽이든 **사용자 확인을 받는다.**
   - **다크 덱**을 원하면 다크 룩(`ppt-dark-tech`)을 고르거나, 아무 룩 + spec 최상위 `"canvas":"#0C1A17"`(어두운 hex)로 그 배경 색조의 다크 덱을 만들 수 있다(역할 팔레트 자동 도출). 상세: [`spec-schema.md`](references/spec-schema.md) §1.
   - 사용자가 **"아무거나/알아서 골라"라고 명시하기 전에는 빌드하지 않는다.**
3. **글자 크기 게이트 (강의·발표용일 때 필수로 물음)** — 글자 크기를 **소 / 중 / 대**로 묻는다. 매핑은 엔진이 관리:
   - **소** = 룩 본연 크기 (배포·인쇄·미감 우선)
   - **중** ≈ 본문 22.5pt (일반 교실)
   - **대** ≈ 본문 25pt (대형 교실·원거리 — 교실 프로젝터 기본 권장)
   - → `build-template.py ... --size 소|중|대` 로 전달. 슬라이드당 정보량이 많거나 표/불릿이 빽빽하면 큰 크기에서 줄바꿈이 늘므로, 큰 크기를 고르면 카드 불릿 수를 줄이도록 안내한다.
   - **인쇄/배포·웹 미감용**이 명백하면 이 게이트를 생략하고 소(룩 기본)로 가도 된다. 거리 가독성이 중요한 강의/발표 자료에서만 필수.
4. **가독성↔일관성 트레이드오프 게이트 (조건부 STOP — 사용자 확인)** — 선택 룩이 **번잡한 배경**(메시 그라디언트 등)이고 덱에 **fragile 차트(추이=line·산점도·분포)**가 있을 때만 발동. 차트 뒤 가독성 패널의 불투명도가 **룩 일관성 ↔ 차트 가독성**의 균형점인데, 이건 결정론으로 못 박는 *아트디렉팅 판단*이라 **LLM이 임의로 정하지 말고 사용자에게 묻는다**:
   - ① **가독 우선**(기본) = 엔진이 도출한 대비 바닥선(가장 약한 마크가 대비 ~3:1 넘는 최소 불투명도).
   - ② **일관 우선** = 카드와 동일(≈16%). 화면 완전 일관, 단 얇은 선이 배경에 묻혀 흐려짐.
   - ③ **절충**(≈30%).
   - 고르면 `--chart-backdrop-opacity N`(0~100) 또는 룩 토큰 `grammar.chart_backdrop_opacity`로 반영. busy 배경 아니거나 fragile 차트 없으면 미발동.
   > 💡 **일반 원칙(HITL)**: 중요한 미감 트레이드오프(특히 일관성↔가독성)는 침묵으로 해결하지 않는다 — 옵션+기본값으로 사용자에게 제시. **객관적 바닥선은 엔진이, 그 위 균형은 사람이.**
5. **확정 후 빌드** — 선택된 `--look`(또는 `--style`+`--palette`) + `--size` (+ 게이트 발동 시 `--chart-backdrop-opacity`)로 `build-template.py` 실행.
6. **시각 QA → 보고** — `qa-runner.sh` 렌더 → PNG 직접 확인 → 사용자 보고.

> 자율 실행(/goal 등)에서도 룩은 **합리적 기본값을 1개 골라 "○○ 룩으로 진행합니다" 한 줄 고지**하고 즉시 되돌릴 여지를 준다. 룩은 덱의 디자인 정체성이라 묵시적으로 넘어가지 않는다. 크기도 마찬가지 — 강의 덱이면 **대(25pt)를 기본**으로 한 줄 고지하고 진행한다.

## 24 아키타입 (7 family) — 권위: [`archetypes.md`](references/archetypes.md)

```
덱 뼈대?       → Frame    cover · section · agenda · closing
한 메시지?     → Focus    statement · feature · showcase
병렬 나열?     → Set      duo · trio · grid · list
명시적 비교?   → Contrast versus · matrix · rank
2축 배치?      → Field    quadrant · map
순서·구조?     → Structure flow · system
데이터?        → Data     share · bars · trend · spread · correlate · kpi
```
좌표는 전부 `grid.json`의 `grid_box(c0,cspan,r0,rspan)`에서 파생(매직넘버 없음). 분류 도출 근거는 archetypes.md.

## 이미지·미디어 슬롯 (수업·자료용 핵심)

이미지는 아키타입이 아니라 **슬롯 fill 종류**. `feature`의 큰 미디어(우측 반쪽), `showcase`의 **좌측정렬 무크롭 미디어 + 불릿**(가이드/UI 캡처·도표), `duo`/`trio`/`grid` 카드별 `image`(이미지 카드 = 사진+설명 2컬럼).
- spec `image: {src:"경로", fit:"cover|contain", caption:"…"}` → 실제 이미지 삽입(cover 크롭/contain 레터박스).
- **와이드 스크린샷·UI 캡처는 `showcase` 권장** — 헤더와 좌측정렬·무크롭으로 크게, 불릿은 **이미지 종횡비가 자동 배치**(세로 여유=우측 / 가로 여유=하단). `feature`(우측·cover)에 넣으면 잘리거나 작아짐.
- `src` 없거나 `{}` → **플레이스홀더 박스**("이미지 자리" + 권장 비율 + 도형 픽토, 이모지 없음). 자리만 잡고 나중에 교체.
- 경로는 `/mnt/c/...`.

### 🎯 이미지 조달 우선순위 (슬롯 만나면 이 순서로)
1. **사용자 콘텐츠에 쓸 이미지 있나?** → `tools/extract-images.py`로 추출해 재활용(생성보다 우선).
2. **없고 코드로 그릴 수 있는 추상/질감인가?** → `tools/gen-texture.py`로 절차적 생성(결정론·무비용).
3. **실사(사람·제품·장소)가 꼭 필요한가?** → 웹 검색·다운로드.
4. 그 외 → 빈 `{}` 플레이스홀더로 자리만.
→ 어느 경로든 **크롭/맞춤은 엔진 `media()`**: `fit:cover`(크롭)·`contain`(레터박스) + `focal`.

### 사용자 콘텐츠 이미지 추출 (`tools/extract-images.py`)
PDF·PPTX·DOCX·폴더·이미지·URL 에서 이미지를 떼어내 `assets/extracted/`에 저장 + 매니페스트(크기·비율·형태) 출력 → 슬롯에 맞는 걸 고른다(아이콘/불릿류 자동 제외, 중복 제거).
```bash
cd references
python3 tools/extract-images.py --src /mnt/c/dev/원본.pdf --slides-dir /mnt/c/dev/decks/<deck>
#  → <deck>/assets/extracted/img-NN.* + manifest.json. 와이드=feature/배경, 정사각·세로=카드.
```
- 떼어낸 경로를 spec `media`/`image`/`background` 의 `src` 에 넣고 `fit:cover`(+`focal`)로 슬롯에 맞춤.

### 절차적 배경/텍스처 (`tools/gen-texture.py` — 모델 없음·결정론)
추상 배경·질감(그라디언트·메시·글로우·도트·그레인)은 **AI 없이 코드로 그린다** — 키·비용·네트워크 0, 같은 입력=같은 출력(재현). 덱 배경/플레이스홀더 채우기의 1순위. (사람·제품 실사는 이걸로 안 됨.)
```bash
cd references
python3 tools/gen-texture.py --kind glow --look ppt-dark-luxury-keynote \
    --slides-dir /mnt/c/dev/decks/<deck> --name cover-glow
#  → <deck>/assets/cover-glow.png 저장 + 경로 출력 → spec 의 background/media/image.src 에 꽂기
```
- `--kind` : `mesh`(4코너 메시) · `linear`(각도 다중스톱) · `glow`(다크+가산 라디얼 발광) · `dots`(미세 도트그리드) · `grain`(필름 그레인) · `solid`.
- 채색: `--look <slug>`(룩 팔레트 canvas/accents 자동) 또는 `--colors "#a,#b,.."` / `--canvas` / `--accent`. → **덱 룩과 결 맞춤이 핵심**.
- `--size`(기본 1920x1080) · `--angle`(linear) · `--seed`(grain 결정론) · `--blur`. 출력은 항상 PNG.

## 차트 20종 — `chart()` 헬퍼

- **네이티브(python-pptx)**: column(clustered/stacked/stacked_100) · bar · line · line_markers · area · pie · doughnut · radar · xy_scatter · bubble
- **합성(도형)**: waterfall · funnel · gauge · gantt · tam_sam_som · bullet · slope · kpi_cards
- Data 아키타입 spec에서 `chart.type`으로 선택. 활성 팔레트 색 적용.
- `kpi` 카드 배열 키: **`items`(권장)** · `kpis` · `stats` (셋 다 허용, Set·List와 키 일관). 항목 `{value, label, note?}`.

## 빌드 / QA

```bash
cd references
# 그리드 → layouts.json 재생성 (좌표 SSOT 변경 시에만)
python3 tools/gen-layouts.py
# 빌드 (스타일/팔레트 또는 룩 선택)
python3 tools/build-template.py /tmp/out.pptx --spec demo/all-archetypes.spec.json --style house --palette 1
python3 tools/build-template.py /tmp/out.pptx --spec spec.json --look ppt-samsung-ir-restrained   # 룩 통째
python3 tools/build-template.py /tmp/out.pptx --spec spec.json --look ppt-neo-brutalism --size 대  # 크기 축(강의용 25pt)
# 시각 QA (Windows PowerPoint COM 렌더 → PNG)
bash tools/qa-runner.sh /tmp/out.pptx ppt-neo-brutalism   # 2번째 인자=룩 → 렌더 직전 폰트 자동 보장
# → /tmp/out_qa/images/slide_N.png
```
spec: `{ "style":"house", "palette":1, "slides":[ {"archetype":"duo","data":{...}} ] }` (`variant`는 `archetype`의 alias). **`data` 입력 키 권위는 [`spec-schema.md`](references/spec-schema.md)** — 아키타입별 필수/선택/alias·최소 예시.

## 파일 맵 (SSOT)

- `references/grid.json` — 그리드 SSOT(12×8 모듈러, 좌표 파생식)
- `references/archetypes.md` — 24 아키타입 분류·슬롯·도출 근거
- `references/spec-schema.md` — 아키타입별 spec `data` 입력 키(필수/선택/alias·최소 예시). `build_*` 함수 추출 권위본
- `references/layouts.json` — gen-layouts.py 생성물(좌표). **직접 수정 금지** → grid.json/gen-layouts.py 수정 후 재생성
- `references/design-tokens.json` — palettes(7) · styles(4) · looks(32 완성본: grammar 흡수 20 + 스킨완성 12)
- `references/catalog.html` — 24 아키타입 레이아웃 슬롯 와이어프레임
- `references/look-gallery.html` — 32 룩 색·폰트·톤 미리보기(`render-look-gallery.py` 생성물, 항상 재생성 후 사용)
- `references/tools/` — build-template.py(엔진) · gen-layouts.py · gen-texture.py · extract-images.py · render-look-gallery.py · render-catalog.py · qa-runner.sh · ensure-fonts.ps1(폰트 자동 프로비저닝)
- `CANON.md` · `THIRD-PARTY-NOTICES.md` — 출처/라이선스

## 환경 메모

- 빌드: WSL python3 + python-pptx. 렌더 QA: Windows PowerPoint COM(soffice 아님).
- **폰트 자동 보장(없으면 다운로드)**: 룩은 폰트 *이름*만 배포하고 파일은 품지 않는다. 폰트가 PC에
  없으면 PowerPoint가 대체 → 룩 타이포 손실. `tools/ensure-fonts.ps1` 이 설치확인→로컬캐시
  (`C:\dev\ppt-fonts`)→다운로드(Google=gwfh API / Pretendard=릴리스 zip) 순으로 **per-user 설치**
  (관리자 불필요, WM_FONTCHANGE 브로드캐스트로 COM 인식). MaruBuri·Clash는 자동 미지원→링크 안내. 멱등.
  - **렌더 시 자동**: `bash tools/qa-runner.sh deck.pptx <look-slug>` — 2번째 인자로 룩을 주면
    렌더 직전에 그 룩 폰트를 자동 보장(best-effort). 빌드→QA 흐름에서 룩 슬러그를 그대로 넘기면 된다.
  - **수동/새 PC 1회**: 스킬이 WSL 네이티브 위치라 powershell.exe 엔 wslpath -w(UNC)로 넘긴다 —
    `powershell.exe -ExecutionPolicy Bypass -File "$(wslpath -w tools/ensure-fonts.ps1)" -All`
    (전체) 또는 `-Look <slug>`(그 룩만) / `-WhatIf`(미리보기).
- 산출물 `/tmp/` 또는 `/mnt/c/...`.
