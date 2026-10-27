---
name: imagine-empty
description: UI 엠프티 스테이트·에러·로딩·온보딩 일러스트를 **라이트/다크 쌍**으로 생성한다. 같은 모티프를 두 모드에 걸쳐 자연스럽게 보이게 하되, **단순 색 반전이 아니라 라이트·다크를 각각 별도 프롬프트로 분리 생성**한다. 프리셋 카탈로그는 `data/empty-states.json` 에 분리되어 커뮤니티 PR로 확장 가능. 투명 배경 PNG가 기본이며 alpha 채널을 검증한다. 사용자가 "엠프티 스테이트", "empty state", "404 일러스트", "로딩 일러스트", "imagine-empty", "preset-pack" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<preset> [--mode light|dark|both] [--style flat-duotone|line-art|paper-cut|iso-geometric] [--colors #HEX,#HEX] [--brand <brand.json>] [--svg] | preset-pack <brand.json>"
---

# imagine-empty

"데이터 없음"·"404"·"오프라인"·"로딩" 같은 UI 빈 상태 일러스트를 **한 번의 호출로 라이트·다크 두 벌** 산출한다. 다크 모드 버전을 "라이트 버전을 invert"로 만들지 않는다 — 팔레트가 뭉개진다.

## 트리거

- `imagine-empty no-result --style flat-duotone --colors "#6B46C1,#F472B6"`
- `imagine-empty error-404 --style line-art --mode both`
- `imagine-empty preset-pack ./brand.json` (8종 기본 팩 일괄)
- "엠프티 스테이트", "empty state 일러스트", "404 페이지 비주얼", "오프라인 일러스트", "온보딩 단계 이미지"
- "imagine-empty"

## 라이트/다크 쌍 생성 방침 — **단순 색 반전 금지**

- **별도 호출로 분리 생성한다.** 같은 preset에 대해 라이트용 프롬프트와 다크용 프롬프트를 **각각 독립적으로** 모델에 보낸다.
- 프롬프트에는 공통 `prompt_base` + 공통 motif hints + **모드별 cue** (config 카탈로그의 `light_mode_cues` / `dark_mode_cues`)가 들어간다.
  - 라이트: `soft off-white strokes on transparent background, gentle duotone accent, subtle warm highlights, neutral mood`.
  - 다크: `bright light strokes on transparent background, vibrant duotone accent, gentle cool highlights, neutral mood`.
- **후처리 `invert()` / 채널 swap 사용 금지.** `color_invert_forbidden: true`. 픽셀 반전은 duotone 팔레트를 뭉개고, 어두운 배경에서 그림자 영역이 밝게 튀어나와 이상해진다.
- **모티프 일관성**: 두 모드 모두 같은 `motif_hints`를 받아 "같은 그림의 라이트·다크" 인상을 유지한다. 랜덤 seed·메타포까지 완전히 같을 필요는 없으며, 시각적 패밀리만 유지.
- `--mode both`(기본)이면 라이트·다크 둘 다 생성, `light` / `dark`만 지정 가능.

## 프리셋 카탈로그 (`data/empty-states.json`)

- **별도 파일로 분리** — 커뮤니티 PR 친화.
- 각 프리셋 스키마: `{ label, prompt_base, motif_hints: string[], aspect, negative_extra }`.
- 기본 팩 8종 (`preset_pack.default_slugs`): `no-result`, `error-404`, `error-500`, `offline`, `no-permission`, `success`, `loading-wait`, `onboarding-step`.
- 공통 전역 필드: `common_negative`, `light_mode_cues`, `dark_mode_cues`.

## 파이프라인

1. **프리셋 해석**: `<preset>` 키를 `data/empty-states.json`에서 조회. 없으면 거절(자동 매핑 금지).
2. **브랜드 토큰 주입 (선택)**: `--brand ./brand.json`이 있으면 Style Guardian scope(`per_brand`)로 palette / line_weight / corner_style / tone을 prefix로 주입. 같은 브랜드 안 8종이 한 패밀리로 보이게 한다.
3. **모드별 프롬프트 조립**:
   - 공통 negative: `cute mascot, cartoon character, kawaii, chibi, white background, photo of people, text, letters, typography, numbers, logo text, watermark, photorealistic` (+ preset의 `negative_extra`).
   - positive: `prompt_base` + `motif_hints` + `style_presets[<style>]` + 모드 cue.
4. **이미지 생성 (분리 호출)**: light/dark 각각 `size: 1024x1024` PNG 1장. `--aspect 3:2` 시 생성 후 중앙 배치로 투명 패드.
5. **Alpha 채널 검증**: `alpha_check.enabled_default: true`. 투명 픽셀 비율이 `min_transparent_ratio: 0.25` 미만이면 "투명 배경 실패" 경고 + 해당 모드만 1회 재생성 (`fail_action: warn_and_retry_once`). 지속 실패 시 사용자에게 노출.
6. **SVG 선택 출력**: `--svg` 플래그 시 `scripts/lib/vectorize.js`(potrace) 호출. **duotone은 single path로 flatten됨**을 경고하고 원본 PNG는 보존.

## 출력 규약

```
./images/empty-states/<brand>/
├── no-result_light.png
├── no-result_dark.png
├── error-404_light.png
├── error-404_dark.png
├── error-500_light.png
├── error-500_dark.png
├── offline_light.png
├── offline_dark.png
├── no-permission_light.png
├── no-permission_dark.png
├── success_light.png
├── success_dark.png
├── loading-wait_light.png
├── loading-wait_dark.png
├── onboarding-step_light.png
├── onboarding-step_dark.png
└── _tokens.json           ← palette / line_weight / corner_style / tone + per-preset metaphor / alpha check summary
```

- `<brand>`: `--brand`의 파일명 기반 또는 사용자 `--slug` 지정값. 명시 없으면 `default`.
- `--out-dir` 명시 시 그대로 사용. 루트 `./images/` 직하 쓰기 금지.

## preset-pack 서브명령

`imagine-empty preset-pack <brand.json>` — 기본 8종을 동일 브랜드 토큰으로 일괄 렌더.

- `concurrency: 1` 강제 — 첫 preset에서 Style Guardian manifest에 저장된 팔레트가 이후 preset들에 순차 적용되어 톤 드리프트를 막는다.
- 1건 실패가 전체 팩을 중단시키지 않는다. 개별 실패는 `_tokens.json.failures[]`에 기록, 나머지 진행.
- `brand.json` 권장 키: `palette`, `line_weight`, `corner_style`, `tone` (`config.preset_pack.brand_json_keys`).

## 프롬프트 규약

- **투명 배경 필수**: `transparent_bg_required: true`. negative에 `white background` 항상 포함.
- **텍스트·숫자·기호 이미지 내부 금지**: `404` 같은 문자열을 이미지에 그리지 않는다 (프리셋의 `negative_extra`에 `404 sign`, `literal error code` 등 포함).
- **귀여움 차단**: `cute mascot, cartoon character, kawaii, chibi` 강제 negative.
- **브랜드 컬러는 이름 구문 주입**: HEX를 그대로 프롬프트에 넣지 않는다. 원본 HEX는 `_tokens.json`에만 저장.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 다크/라이트 팔레트가 단순 invert처럼 뭉개짐 | **분리 생성**이 기본 — 후처리 invert 코드 경로 없음. 다크 cue 프롬프트를 재조립해 재생성 1회. |
| 귀여움 범벅 | negative 강화(`cute mascot, kawaii`는 기본 포함)로 재생성 1회. 지속 시 `--style line-art`로 전환 제안. |
| 투명 배경이 회색 체커보드로 렌더 | alpha 채널 비율 검사. 기준 미달 시 모드별 1회 재생성, 실패 시 사용자에게 경고 + 수동 편집 안내. |
| 프리셋 키 부재 | 즉시 에러 + 카탈로그의 사용 가능한 slug 목록 제시. 자동 매핑 금지. |
| SVG 벡터화 품질 저하 | duotone→single path flatten 경고. 원본 PNG를 유지하고 SVG는 보조 산출물로 표기. potrace 부재 시 PNG만. |
| brand.json 누락 | 기본 팔레트로 진행(`require_brand_json: false`). Style Guardian 체인이 저장되어 있으면 그걸 먼저 사용. |

## 금기

- **단순 색 invert로 다크 모드 제작 금지.** 별도 프롬프트로 분리 생성.
- **이미지 내부 텍스트·에러 번호(`404`, `500`) 렌더 금지.**
- **귀여운 마스코트·얼굴 생성 금지.**
- **HEX를 프롬프트에 직기재 금지.** 이름 구문으로만.
- **투명 배경 실패를 성공처럼 보고 금지.** alpha 검증 실패 시 반드시 경고.
- **프리셋 자동 추가·제거 금지.** 사용자가 `preset-pack`으로 지정한 slug 리스트만 실행.
- **`./images/empty-states/` 외부 쓰기 금지** (`--out-dir` 지정 없는 한).
- **브랜드 간 Style Guardian 누출 금지** (`cross_brand_leak: false`).
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 금지.

## imagine 계열 스킬과의 관계

- **`imagine-service-section` / `imagine-slide`**: 시리즈 일관성 문제 공통이나 Style Guardian 스코프가 다르다 — 이 스킬은 `per_brand`, 데크/페이지는 `per_project`. 브랜드 팔레트는 공유 가능하지만 자동 누출은 금지.
- **`compose-text.js`**: 사용하지 않음 — 빈 상태 일러스트에 글자 얹기는 UI 프레임워크가 담당.
- **`vectorize.js`**: `--svg` opt-in에서만. duotone flatten 경고 포함.
- **`imagine-icon`**: 앱 아이콘은 그 스킬. 이 스킬은 UI 상태 일러스트 전용이며 플랫폼별 다중 해상도 매트릭스를 뽑지 않는다.
- **`imagine-ui`**: 그 스킬은 UI 스타일 *전체 화면* 레퍼런스, 이 스킬은 빈 상태 *블록* 일러스트 — 조합 사용 가능(imagine-ui의 empty 화면 스타일을 reference로 삼아 이 스킬의 톤을 맞춤).
