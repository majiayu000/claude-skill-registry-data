---
name: imagine-thumb
description: YouTube 썸네일 전용 생성기. 배경/인물 일러스트는 Codex 이미지 모델로 뽑고, 제목 텍스트는 **AI가 아니라 Node 후처리**(`scripts/lib/compose-text.js`)로 합성한다. 한국어 글자 깨짐을 원천 차단한다. 사용자가 "썸네일 만들어줘", "imagine-thumb <제목>", "유튜브 썸네일" 등을 말하면 이 스킬이 담당한다. 기본 A/B용 2장을 같은 제목 텍스트로 합성해 저장한다.
argument-hint: "--title <text> [--style vlog|tech|reaction|meme|cinematic] [--subject-side left|right] [--vibe shock|calm|cozy|hype] [--n 2|3] [--subtitle <text>]"
---

# imagine-thumb

YouTube 업로드용 **1280×720 JPEG 썸네일**을 30초 안에 뽑는다. AI에게 글자를 맡기지 않는 것이 이 스킬의 핵심 계약이다.

## 트리거

- `imagine-thumb <제목>` / `imagine-thumb --title "..."` (명시 호출)
- "썸네일 만들어줘"
- "유튜브 썸네일"
- "YouTube thumbnail for <제목>"

## 파이프라인

1. **배경 생성**: `imagine` 스킬의 Phase 1 공용 모듈(Request Planner / Output Allocator / OAuth Session)로 Codex 이미지 모델 호출. `size: 1536x1024` (3:2) 로 뽑아 `1280×720`으로 크롭한다.
2. **프롬프트 가공**: `--title` 값은 **모델 프롬프트에 포함하지 않는다**. `--style`/`--vibe`로 배경·조명·구도만 지시하고, negative prompt에 `text, watermark, logo, blurry, deformed hands, asymmetric eyes`를 강제 포함.
3. **텍스트 합성**: `scripts/lib/compose-text.js`의 `compositeText(bgPath, textOptions, outPath)`로 SVG→sharp composite. 세이프존(좌/우 45%)과 배경 명도 자동 측정(어두우면 흰색, 밝으면 검정).
4. **A/B variant**: 기본 `n=2`. 같은 제목 텍스트를 각 배경에 합성해 `_final_v1.jpg` / `_final_v2.jpg` 두 벌 저장. `--n 3`이면 3벌.
5. **모바일 프리뷰**: 최종본을 640×360으로도 리사이즈해 동반 저장(규격 가독성 점검용).

에이전트·하위 LLM은 서로를 직접 호출하지 않는다. 모든 단계는 이 스킬의 entrypoint 스크립트가 순차 지휘한다.

## 출력 규약

```
./images/thumbs/
├── <slug>_<ts>_bg_v1.jpg         ← AI 배경 원본 (크롭 전)
├── <slug>_<ts>_bg_v2.jpg
├── <slug>_<ts>_final_v1.jpg      ← 텍스트 합성 완료 (1280×720)
├── <slug>_<ts>_final_v2.jpg
└── <slug>_<ts>_final_v1_mobile.jpg  (640×360)
```

- `<slug>`: 제목 기반 안전 문자열 (`slugify`).
- 사용자가 `--out-dir`로 지정하지 않는 한 경로를 조용히 바꾸지 않는다.

## 프롬프트 구성 규칙

- **제목 텍스트 프롬프트 금지.** 어떤 variant든 모델 프롬프트에 사용자의 `--title` 값을 그대로 섞어 넣지 않는다 (한국어 글자 깨짐 방지 핵심).
- **negative에 `text` 포함 필수.** `text, watermark, logo, ...` 한 줄을 모든 실행에서 강제 주입.
- **스타일 매핑** (예시):
  - `tech`: `clean studio lighting, vibrant blue/purple gradient background, product shot composition, negative space on <subject-side>`
  - `vlog`: `warm afternoon light, shallow depth of field, approachable portrait framing`
  - `reaction`: `bold color background, exaggerated expression reference composition`(얼굴 기형 방지를 위해 `deformed face, extra fingers`를 negative에 추가)
  - `cinematic`: `filmic tonemapping, high contrast teal-orange, wide cinematic framing`
  - `meme`: `flat bright colors, exaggerated composition, strong focal point`
- **`--vibe`**: `shock`/`hype`는 high contrast + saturated, `calm`/`cozy`는 soft muted palette로 반영.

## 가독성 체크

- `compose-text.js`가 텍스트 배치 영역의 평균 휘도를 WCAG sRGB 공식으로 계산 → `luminance < 0.5`면 `#ffffff`, 아니면 `#111111` 자동 선택.
- 사용자가 `--color`로 지정하면 자동 선택을 건너뛴다.
- 최종 JPG에 OCR을 돌려 글자 검출 시 경고(문서 §실패 모드) — 구현은 후속 PR.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 배경에 AI 글자 새겨 나옴 | 프롬프트 재조합 없이 variant 1회 추가 재생성 (최대 1회). 그래도 검출되면 사용자에게 원인 배너와 함께 bg 파일만 전달. |
| 얼굴 기형 (`reaction` 스타일) | 해당 variant만 negative 강화 후 재생성 1회. |
| 모바일 640×360에서 글자 가독성 실패 | `titleSize`를 한 단계 키워 재합성. 재생성은 하지 않음(텍스트만 다시 얹음). |
| `sharp` 미설치 | 텍스트 합성 단계에서 명시적 에러. 사용자에게 `npm i sharp` 안내. 배경 이미지는 저장되어 있음. |

## 금기

- **AI 모델 프롬프트에 제목 텍스트 넣기** (스킬 전체 존재 이유에 반한다).
- 모델이 그린 글자를 "그래도 써보자"로 최종 배포.
- `./images/thumbs/` 밖으로 출력 쓰기 (사용자 지정 `--out-dir` 없으면).
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 주입.

## 설정 기본값

`config.json` 참고. 핵심:
- `size`: `"1536x1024"` (3:2 → 16:9 크롭)
- `format`: `"jpeg"`, `quality`: `"medium"`
- `n`: `2` (A/B 기본)
- `output_dir`: `"./images/thumbs"`
- `safe_zone_ratio`: `0.45`
- `negative_prompt`: `"text, watermark, logo, blurry, deformed hands, asymmetric eyes"`

## imagine 스킬과의 관계

- `imagine`의 공용 모듈(OAuth session, Output Allocator, Request Planner)을 재사용한다.
- 단, `imagine-thumb`는 텍스트 후처리와 A/B variant 생성을 자체 entrypoint에서 지휘한다. 일반 `imagine` 호출 경로로 우회 생성하지 않는다.
- Style Guardian에 채널 브랜드 토큰(`channel_palette`)이 저장되어 있으면 스타일 프롬프트에 자동 반영 (후속 PR).
