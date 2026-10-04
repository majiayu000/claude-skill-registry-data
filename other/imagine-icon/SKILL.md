---
name: imagine-icon
description: 모바일 앱·웹 앱 **아이콘 세트 일괄 생성기**. AI로 1024×1024 마스터 아이콘을 뽑고, 플랫폼별 다중 해상도(iOS 1024 / Android adaptive 전경·배경 / Web favicon·PWA·Apple touch)를 `scripts/lib/icon-exporter.js`로 Lanczos3 리사이즈 익스포트한다. 사용자가 "앱 아이콘", "imagine-icon", "favicon", "launcher icon" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<concept> [--targets ios,android,web] [--variation minimal|3d-glossy|flat-illustration|abstract-geometric] [--android-background auto|#RRGGBB] [--out-dir <path>]"
---

# imagine-icon

한 번의 호출로 **iOS / Android adaptive / Web(favicon+PWA)** 아이콘 세트를 산출한다. 마스터 생성은 AI, 리사이즈·레이아웃은 결정적 후처리다.

## 트리거

- `imagine-icon "<컨셉>"` / `imagine-icon export <master.png>` (명시 호출)
- "앱 아이콘 만들어줘"
- "favicon 만들어줘"
- "런처 아이콘", "launcher icon"
- "PWA 아이콘"
- "아이콘 세트 뽑아줘"

## 파이프라인

1. **마스터 생성 (AI)**: `generate_size: 1024x1024` PNG로 Codex 이미지 모델 호출.
2. **프롬프트 구성**: `config.prompt_template`의 고정 문구 + 사용자 컨셉 키워드만 조합. 제목·앱 이름을 프롬프트에 **넣지 않는다.** 4가지 `variation_directions`(minimal / 3d-glossy / flat-illustration / abstract-geometric) 중 `--variation` 지정이 없으면 기본 1장만 생성(`--n 4`로 4종 배치 생성 가능).
3. **세이프존 검증 (결정적)**: 마스터 PNG의 중앙 60% 박스 밖에 핵심 콘텐츠가 얼마나 있는지 픽셀 비율로 계산. `quality_checks.safe_zone_overflow_max_ratio` 초과 시 사용자에게 경고.
4. **Alpha 검증**: Android foreground는 배경 투명이어야 함 → PNG alpha 채널 검사, 전면 알파 0 픽셀이 없으면 "투명 배경 요청이 반영되지 않았을 수 있다" 경고.
5. **사이즈 익스포트**: `scripts/lib/icon-exporter.js`의 `exportSizes(masterPath, targets, outputDir, options)` 호출. sharp 있으면 Lanczos3, 없으면 pngjs 박스 평균 폴백(작은 사이즈 품질 저하 경고).
6. **리포트 작성**: `_report.md`에 각 파일 경로·resize 엔진·경고 요약.

## 출력 규약

```
./images/icons/<app-slug>/
├── master.png                     (1024×1024)
├── ios/
│   └── AppIcon-1024.png
├── android/
│   ├── ic_launcher_foreground.png   (512 canvas, 432 foreground, transparent)
│   └── ic_launcher_background.png   (512 solid color)
├── web/
│   ├── favicon-16.png
│   ├── favicon-32.png
│   ├── favicon-48.png
│   ├── apple-touch-icon-180.png
│   ├── pwa-192.png
│   └── pwa-512.png
├── manifest.webmanifest            (PWA, 선택)
└── _report.md
```

- `<app-slug>`는 사용자 컨셉에서 slugify. `--out-dir` 지정 시 그대로 사용(조용히 변경 금지).
- 루트 `./images/` 직하 쓰기 금지.

## 마스터 프롬프트 규약

다음 문구를 **그대로** 프롬프트에 포함한다 (config.prompt_template):

```
app icon, single focal motif, centered composition, 15% padding safe zone,
bold silhouette recognizable at small size, solid background or simple gradient,
no text
```

- 앱 이름·브랜드 문구는 프롬프트에 넣지 않는다. 아이콘에 글자가 새겨지는 것을 원천 차단.
- Negative prompt 강제: `text, letters, typography, multiple objects, cluttered detail, photorealistic, watermark, logo text`.
- `--variation`으로 방향성 지정:
  - `minimal`: `minimal flat vector style, limited palette (≤3 colors), geometric primitives only`
  - `3d-glossy`: `soft 3D rendering, subtle glossy highlight, studio lighting, rounded volumes`
  - `flat-illustration`: `flat illustration, solid shapes, decorative but legible at 16px`
  - `abstract-geometric`: `abstract geometric composition, bold shapes, strong silhouette`

## Android Adaptive 처리

- foreground: 마스터를 **432×432로 Lanczos3 리사이즈** 후 512×512 투명 캔버스 중앙 배치 → `ic_launcher_foreground.png`.
- background: `--android-background`(기본 `auto`)가 `auto`이면 마스터의 네 모서리 평균색 샘플링으로 solid 컬러 생성 → `ic_launcher_background.png`. `#RRGGBB` 직접 지정도 허용.
- Adaptive safe zone 108dp(= 108px 기준)를 벗어난 콘텐츠는 마스킹에 의해 잘린다는 점을 경고로 남긴다.
- foreground 프롬프트 변형 시 `transparent background, motif only, no shadow` 명시 권장.

## Web 세트

- favicon 16/32/48, Apple touch 180, PWA 192/512 일괄 출력.
- `config.web.write_manifest: true`면 `manifest.webmanifest` 동반 생성(PWA icon 배열).
- 16×16은 엔트로피 측정(`quality_checks.small_size_entropy_warn_below`) 후 너무 단조/너무 복잡하면 "수동 개선 필요" 경고.

## 리사이즈 엔진

- 기본: **sharp Lanczos3** (`kernel: 'lanczos3'`).
- 폴백: **pngjs 박스 평균** — 작은 사이즈(16/32/48)에서 품질 저하 경고 출력. sharp 설치를 강권하는 안내 메시지.
- 둘 다 없으면 명시적 에러로 중단 (어떤 리사이즈도 하지 않음).

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 16×16에서 모티프가 뭉개짐 | 엔트로피 측정 후 경고 + `_report.md`에 "수동 개선 권장" 기록. |
| 안전 영역 침범(중앙 60% 밖 콘텐츠 과다) | 배경만 재생성 요청, 재생성 1회 한정. 지속 시 경고. |
| Android foreground에 배경이 남음 (alpha 누락) | alpha 0 픽셀 비율 검사 실패 시 경고. 사용자에게 `transparent background` 프롬프트 재시도 권유. |
| sharp 미설치 | pngjs 폴백 + 경고. 둘 다 없으면 중단. |
| 마스터 사이즈 불일치 | 1024×1024 아닌 입력은 거절(자동 리사이즈 금지 — 사용자가 원본을 다시 뽑도록 유도). |

## 금기

- **앱 이름·브랜드 텍스트 프롬프트 주입 금지.** 아이콘에 글자 새겨지는 원인.
- **자동 업스케일 금지.** 마스터가 1024×1024 미만이면 에러로 중단.
- **사용자 출력 경로를 조용히 바꾸는 것 금지.** `--out-dir` 값은 그대로 사용.
- **Android background에 임의 그라디언트 생성 금지.** solid color만 지원(투명 foreground + solid background가 adaptive icon 원칙).
- **`./images/icons/` 외부 쓰기 금지** (`--out-dir` 지정 없는 한).
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 금지.

## imagine 계열 스킬과의 관계

- 공용 인프라 재사용: `oauth-session.js`, `output-allocator.js`, `request-planner.js`.
- 텍스트 합성 모듈(`compose-text.js`)은 이 스킬에서 사용하지 않는다 (아이콘에 글자를 얹지 않는 것이 원칙).
- Style Guardian의 브랜드 팔레트가 있으면 `--android-background` 자동 선택 시 우선 참고.
- `imagine-thumb`(YouTube 썸네일) / `imagine-og`(소셜 카드)와는 별개 산출물. 트리거가 겹치는 "아이콘" 키워드는 항상 여기.
