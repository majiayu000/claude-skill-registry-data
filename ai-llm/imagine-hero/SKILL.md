---
name: imagine-hero
description: SaaS · 개인 사이드 프로젝트의 **랜딩 페이지 히어로 이미지**를 3:2(1536×1024) 전용 프리셋으로 생성한다. 이미지 내부에 텍스트를 넣지 않고(모든 copy는 HTML이 담당), 한쪽 40%를 세이프존으로 비워 CTA·헤드라인을 얹을 수 있게 한다. `--transparent-bg` 플래그 지정 시 `scripts/lib/bg-remove.js`로 배경을 잘라낸 PNG도 함께 저장한다. 사용자가 "히어로 이미지", "랜딩 히어로", "imagine-hero", "landing page hero" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<concept> [--style gradient-abstract|isometric-illust|3d-glow|product-shot|human-device] [--safe-zone left|right|center] [--transparent-bg] [--brand-color #HEX] [--vibe shock|calm|cozy|hype]"
---

# imagine-hero

데스크톱 히어로 섹션용 **3:2 메인 비주얼**을 프리셋 기반으로 뽑는다. 텍스트는 절대 이미지 안에 넣지 않는다(랜딩 페이지 HTML이 담당). CTA 배치용 40% 세이프존을 의도적으로 비워 남긴다.

## 트리거

- `imagine-hero "<컨셉>"` / `imagine-hero --concept "..."` (명시 호출)
- "히어로 이미지", "랜딩 히어로", "랜딩 페이지 메인 이미지"
- "landing hero", "landing page hero", "SaaS hero image"
- "히어로 비주얼 뽑아줘"

애매하게 "배너", "썸네일"만 들어오면 이 스킬이 아니라 각각 `imagine-og`, `imagine-thumb`로 라우팅. 1턴 질문으로 맥락 확인.

## 핵심 제약

| 항목 | 값 |
|---|---|
| 생성 비율 | **3:2 — 1536×1024** |
| 포맷 | **PNG**(투명 지원) + **WebP**(최적화용). 기본은 PNG 저장, WebP 추가 인코딩. |
| 텍스트 | **이미지 내부 금지.** `negative_prompt`에 `text, letters, typography, UI mockup, watermark, logo text` 강제. |
| 세이프존 | 한쪽 **40%** 비움. 기본 `right` (왼쪽에 CTA 붙이는 국내 SaaS 관행). `--safe-zone left/right/center`로 지정. |

## 파이프라인

1. **프롬프트 구성**:
   - `--style` 값을 `config.style_presets` 테이블에서 영문 비주얼 구문으로 매핑.
   - `--safe-zone`이 `right`이면 `"composition weight on left side, empty negative space on right 40%"`를 덧붙이고, `left`이면 반대. `center`면 `"focal motif upper third, empty lower 40% negative space"`.
   - `--brand-color #HEX`가 주어지면 HEX 숫자는 프롬프트에 **직접 넣지 않고** HSL 근사를 색 이름 구문(`"vivid violet tones, accent magenta"` 등)으로 변환해 주입. 원본 HEX는 Run Manifest에 저장해 후처리 톤 매핑용으로 보관.
   - `--vibe`가 있으면 `config.vibe_map`의 한 구문을 append.
   - **사용자 컨셉 문자열 원문 보존** — 정직한 번역만 허용. 정체성을 바꾸지 않는다.
2. **Negative 강제**: `config.negative_prompt` 그대로 주입. 텍스트·UI 목업·여백 없음·복잡한 주변 시각 요소를 모두 차단.
3. **이미지 생성 (AI)**: Codex 이미지 모델로 `size: 1536x1024` PNG 1장 출력. 공용 `oauth-session.js` / `output-allocator.js` 재사용.
4. **세이프존 검증 (결정적, sharp)**: 지정된 40% 영역의 평균 채도(saturation mean)를 측정. `quality_checks.safe_zone_clutter_max_saturation_mean` 초과 시 "세이프존 혼잡" 경고와 함께 사용자에게 재생성 제안(자동 재생성 금지).
5. **WebP 인코딩**: 같은 결과를 `webp.quality=82, effort=4`로 추가 저장. sharp 부재 시 WebP 단계는 스킵 + 경고(PNG는 정상).
6. **`--transparent-bg` 후처리**: 플래그 지정 시 `scripts/lib/bg-remove.js`의 `removeBackground(inputPath, outputPath)` 호출. 라이브러리 부재·실패 시 원본을 `_cutout.png`로 그대로 복사하고 `mode: 'passthrough'` 경고를 사용자에게 노출(**원본 PNG는 항상 보존**). 이 스킬은 `bg-remove.js`가 반환한 `mode` 값을 결과 리포트에 그대로 기록한다.

## 출력 규약

```
./images/landing/
├── hero_<slug>_<style>_<ts>.png
├── hero_<slug>_<style>_<ts>.webp
└── hero_<slug>_<style>_<ts>_cutout.png   ← --transparent-bg 지정 시에만
```

- `<slug>`: 컨셉 기반 slugify. `--out-dir` 명시 시 그대로 사용. `./images/landing/` 외부 쓰기 금지(`--out-dir` 없는 한).
- 사용자 지정 경로를 조용히 바꾸지 않는다.
- 원본 PNG는 **어떤 후처리도 덮어쓰지 않는다**. cutout/WebP는 별도 파일로만 저장.

## 프롬프트 구성 규칙

- **이미지 내부 텍스트 프롬프트 금지.** 브랜드명·헤드라인·CTA 문구를 AI 프롬프트에 섞지 않는다.
- **negative prompt 필수**: 최소한 `text, UI mockup, watermark, logo text, cluttered, fills entire frame, no margin`. `--style human-device`일 때만 `photo of person` 금지를 해제.
- **세이프존 표현은 영문 구문으로 고정**(`empty negative space on right 40%`). "왼쪽 비우기" 같은 모호한 한국어를 모델 프롬프트로 보내지 않는다.
- **brand color는 이름 기반으로만 주입**. `#6B46C1`을 그대로 프롬프트에 넣지 않는다(모델이 HEX를 무시하는 실패 케이스 방지).

## 투명 배경 옵션

- `--transparent-bg` 플래그 해석은 스킬의 entrypoint에서만 이뤄지고, 실제 알파 제거는 `scripts/lib/bg-remove.js`에 **위임**한다. 이 스킬은 자체 cutout 로직을 두지 않는다.
- `bg-remove.js` 반환 규약:
  - `mode: 'cutout'` → 실제 cutout 완료. `_cutout.png` 파일 사용.
  - `mode: 'passthrough'` → 라이브러리 부재 또는 런타임 실패. 원본이 복사된 `_cutout.png`로 **가짜 성공을 연출하지 않는다**. 사용자에게 "알파 제거 실패, 원본 복사본으로 대체됨" 경고를 그대로 보고.
- 원본 이미지 파일은 어떠한 경로에서도 삭제·덮어쓰기하지 않는다.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 브랜드 컬러가 무시됨 | HEX를 이름 구문으로 재변환해 재생성 1회. 여전히 무시되면 manifest의 원본 HEX로 사용자에게 후처리 옵션 안내. |
| 글자·로고·UI를 멋대로 그려 넣음 | negative 강화 후 재생성 1회(최대). OCR 검출 지속 시 사용자에게 보고. |
| 세이프존 영역이 혼잡 | 재생성 제안만 (자동 재생성 금지). 사용자 동의 후 1회만 재실행. |
| bg-remove 라이브러리 부재/실패 | `mode: 'passthrough'` 결과 그대로 보고. 사용자에게 설치 안내(`npm i @imgly/background-removal-node`). |
| sharp 부재 | PNG 저장은 되지만 WebP 인코딩·세이프존 검증 스킵 + 경고. |

## 금기

- **이미지 내부에 브랜드명·헤드라인·CTA 텍스트 주입 금지.** 존재 이유에 반한다.
- **세이프존 영역을 조용히 축소 금지.** `--safe-zone` 값은 그대로 집행.
- **원본 PNG 덮어쓰기 금지.** cutout·WebP는 항상 새 파일.
- **`./images/landing/` 외부 쓰기 금지** (`--out-dir` 지정 없는 한).
- **bg-remove 실패를 성공처럼 표기 금지.** 반드시 `mode: 'passthrough'` 경고를 사용자에게 투명 공개.
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 주입 금지.

## imagine 계열 스킬과의 관계

- 공용 인프라 재사용: `oauth-session.js`, `output-allocator.js`, `request-planner.js`, `bg-remove.js`.
- 텍스트 합성 모듈(`compose-text.js`)은 **사용하지 않는다** — 이 스킬의 원칙은 "히어로에 글자 넣지 않기".
- Style Guardian의 브랜드 팔레트가 있으면 `--brand-color` 미지정 시 자동 주입.
- `imagine-thumb`(유튜브 썸네일) · `imagine-og`(소셜 카드) · `imagine-icon`(앱 아이콘)과 구분: "랜딩 히어로" 맥락은 항상 여기.
