---
name: imagine-logo
description: 회사·개인 프로젝트·팀의 **로고 시안 탐색기**. 마크(심볼)만 Codex 이미지 모델로 생성하고 워드마크(회사명 글자)는 `scripts/lib/compose-text.js`로 합성한다. 회사명 텍스트는 AI 프롬프트에 **절대** 포함하지 않으며, 이미지 생성 후 OCR로 글자 검출 시 1회 자동 재생성한다. 3~6개의 서로 다른 방향성 시안을 한 번에 뽑아 "나쁘지 않은 출발점"을 빠르게 고르도록 돕는다. `scripts/lib/vectorize.js`로 선택된 1장을 SVG로 벡터화하는 옵션도 제공한다. 사용자가 "로고 만들어줘", "imagine-logo", "회사 로고", "팀 로고" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<company-or-concept> [--name <wordmark>] [--direction-count 3..6] [--directions geometric,organic,animal,abstract,monogram,typography-centric] [--color-mode monochrome|duotone|tritone] [--palette #HEX,#HEX] [--vectorize <mark_idx>]"
---

# imagine-logo

**중요: 이 스킬은 시안 탐색용이다.** 본격 브랜딩은 전문 디자이너에게 맡기는 것이 맞다. 법적 안전(유사 기존 로고 존재 여부)·상업 사용 적합성 검토는 이 스킬의 범위 밖이다.

## 트리거

- `imagine-logo "<회사 또는 컨셉>"` / `imagine-logo --name "CodeNest"` (명시 호출)
- `imagine-logo vectorize ./images/logos/<company>/mark_03.png`
- `imagine-logo compose ./images/logos/<company>/mark_03.png --name "CodeNest"`
- "로고 만들어줘", "로고 시안 탐색", "회사 로고", "팀 로고", "사이드 프로젝트 로고"
- "imagine-logo"

## 핵심 분리 계약 — 마크만 AI, 워드마크는 후처리

- **마크(심볼)**: AI 이미지 모델이 그린다. **회사명 텍스트는 절대 프롬프트에 포함하지 않는다.** 마크 프롬프트는 오로지 형태·기하·소재·컨셉만 담는다.
- **워드마크(회사명 글자)**: `scripts/lib/compose-text.js`의 `compositeText()`로 실제 시스템 폰트(기본 `Pretendard Bold`)를 사용해 합성. AI가 글자를 렌더하지 않는다.
- 이 분리를 지키지 않으면 "Aeme Cerp" 같은 깨진 글자가 섞여 나오므로 어떤 경우에도 위반하지 않는다.

## 파이프라인

1. **방향성 시안 프롬프트 구성**:
   - `--direction-count`(기본 4, 허용 3~6)만큼 `config.direction_catalog`에서 방향을 골라 각각 프롬프트 생성. 기본 선택은 `["geometric","abstract","monogram","organic"]`.
   - 모든 프롬프트에 `config.mark_style_common`(`flat, bold edges, no gradient, ..., transparent background`) 강제 접미사.
   - **사용자 회사명 / 슬로건 / CTA 텍스트는 프롬프트에 절대 넣지 않는다.**
   - `--palette`가 주어지면 HEX 대신 색 이름 구문으로 변환해 주입. 원본 HEX는 Run Manifest에 저장.
2. **Negative 강제**: `text, letters, typography, readable words, watermark, photorealistic, gradient, soft edges, anti-aliasing artifacts` (벡터화 품질 보호 포함).
3. **이미지 생성**: `size: 1024x1024` PNG 각 방향 1장씩. 공용 `oauth-session.js`·`output-allocator.js` 재사용.
4. **OCR 글자 검출 (선택적)**: `config.ocr_check.enabled_default: true`. 검출 시 **1회 자동 재생성** (`retry_on_detect_max: 1`). 재검출에도 잔존하면 사용자에게 경고와 함께 해당 마크만 "글자 포함 가능성" 라벨로 노출. OCR 엔진 미설치 시 스킵 + 경고.
5. **Manifest 기록**: 각 마크에 대해 `{ company_name, palette, mark_direction, color_mode }`을 `_manifest.json`에 저장. Style Guardian이 아닌 **logo card** 방식 — 이 스킬 전용 기록이며, 다른 imagine 스킬로 흐르지 않는다.
6. **워드마크 합성 (`compose`)**: 사용자가 시안 1장을 골라 `imagine-logo compose <mark.png> --name "CodeNest"`를 실행하면 `compose-text.js`로 회사명을 실제 폰트로 조판해 `<mark>_wordmark.png`로 저장.
7. **벡터화 (`vectorize`)**: `imagine-logo vectorize <mark.png>`는 `scripts/lib/vectorize.js`의 `vectorize(imgPath, svgPath)`에 위임. 입력 이미지는 반드시 `flat, bold edges, no gradient`를 만족해야 품질이 유지된다(위 마크 생성 프롬프트가 이를 강제). potrace 미설치 시 `mode: 'passthrough'` 반환 — PNG가 복사될 뿐이며 "가짜 SVG"는 생성되지 않는다.

## 출력 규약

```
./images/logos/<company>/
├── mark_01.png ... mark_0N.png      (N = direction-count, 3~6)
├── mark_<idx>_vector.svg             ← vectorize 실행 시
├── mark_<idx>_wordmark.png           ← compose 실행 시
├── _manifest.json
└── _source_prompts.json              ← 각 방향 프롬프트 원문(디버그용)
```

- `<company>`: 사용자 컨셉·회사명 기반 slugify. `--out-dir` 지정 시 그대로 사용.
- 루트 `./images/` 직하 쓰기 금지.
- 사용자 출력 경로를 조용히 바꾸지 않는다.

## 프롬프트 규약 (엄격)

- **회사명·슬로건·CTA 텍스트 주입 금지.** 검증: 프롬프트 조립 후 사용자 `--name` 값이 문자열로 포함되어 있으면 즉시 거절.
- **`monogram` / `typography-centric` 방향도 실제 글자는 그리지 않는다.** 프롬프트는 `abstract single-letter monogram shape (NOT an actual glyph)` / `abstract typographic form built from bold strokes, NOT real letters` 형태로 고정. 실제 문자 렌더링 기대 금지.
- **투명 배경 강제**: `transparent background` 구문 + PNG alpha 채널 사용. 흰 박스가 남으면 해당 시안만 alpha 경고.
- **벡터화 친화 규칙**: `flat, bold edges, no gradient, 20% padding safe zone`를 모든 방향 프롬프트에 강제 포함. 그래디언트·앤티엘리어싱은 potrace 품질을 망친다.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 마크 이미지 내부에 글자가 그려짐 | OCR 검출 → negative 강화 후 해당 마크만 1회 재생성. 지속 시 "글자 포함 가능성" 라벨 + 사용자 경고. |
| 벡터화 결과가 지저분함 | 입력이 `flat, bold edges, no gradient` 가정 위반. 해당 마크를 재생성하거나, 원본 PNG를 그대로 사용하도록 안내. `vectorize.js`가 `mode: 'passthrough'` 반환. |
| potrace 미설치 | `vectorize`가 경고와 함께 PNG 복사본 반환. 사용자에게 `npm i potrace` 안내. |
| 투명 배경 안 됨 (흰 박스 잔존) | alpha 0 픽셀 비율 검사로 경고. 배경 투명이 필수인 경우 재생성 1회 권유. |
| 워드마크 폰트 미설치 | `compose-text.js`가 fallback stack(`sans-serif`)으로 렌더 + 경고. 사용자가 `--font`로 교체하거나 시스템 폰트 설치하도록 안내. |
| 법적 안전 질문 | "이 스킬은 시안 탐색용. 유사 기존 로고 탐지·상업 사용 적합성 검토는 범위 밖." 경고로 답변. 자동 검색 수행 금지. |

## 금기

- **AI 프롬프트에 회사명·영문 글자 주입 금지.** 스킬 존재 이유.
- **깨진 글자를 "typography-centric 의도"로 포장 금지.** `monogram`/`typography-centric` 방향에서도 실제 문자 렌더는 시도하지 않는다.
- **마크 + 워드마크를 한 번의 AI 호출로 처리 금지.** 반드시 두 단계로 분리.
- **유사 기존 로고 자동 탐색 금지.** 이 스킬은 법적 검토를 수행하지 않으며, 외부 검색으로 확인 시늉도 하지 않는다.
- **`./images/logos/` 외부 쓰기 금지** (`--out-dir` 지정 없는 한).
- **Style Guardian 오용 금지.** 로고 정체성은 본질적으로 브랜드 단위 고정 — 이 스킬은 `manifest_keys`(`company_name`, `palette`, `mark_direction`, `color_mode`)를 **자체 logo card**에 저장하고, Style Guardian의 전역 스타일 흐름에는 주입하지 않는다.
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 금지.

## imagine 계열 스킬과의 관계

- 공용 인프라 재사용: `oauth-session.js`, `output-allocator.js`, `request-planner.js`.
- **`compose-text.js` 공유**: `imagine-thumb`·`imagine-og`와 동일 코드베이스. 워드마크 합성 로직을 이 스킬에 복제하지 않는다.
- **`vectorize.js`는 이 스킬 전용** (potrace 래핑). 다른 스킬에서 호출해도 되지만, 기본 사용처는 로고.
- Style Guardian과 분리: 브랜드 정체성은 자체 `_manifest.json`으로만 관리.
- `imagine-icon`과 구분: 앱 아이콘은 `imagine-icon` (플랫폼별 다중 해상도), 로고는 여기 (단일 마크 + 워드마크 + SVG).
