---
name: imagine-ui
description: 모바일 앱 화면의 **스타일 레퍼런스 이미지**를 빠르게 뽑는다. 실제 픽셀 퍼펙트 UI·구현 가능한 디자인이 아니라, Figma를 켜기 전에 "대충 이런 느낌인가?"를 여러 장 나열해보기 위한 **무드 보드**다. iOS · Android Material 3 · 한국 fintech(Pretendard 스타일) · 웹 모바일 프리셋을 제공하고, Style Guardian manifest에 `system` · `palette_hex` · `corner_radius_estimate`를 저장해 다음 호출에서 같은 톤으로 이어갈 수 있다. 사용자가 "UI 목업", "앱 화면 레퍼런스", "imagine-ui", "스크린 레퍼런스" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<screen-or-concept> [--system ios|android|web-mobile|kr-minimal] [--screen login|feed|detail|settings|onboarding|empty] [--mood light|dark|warm|cold] [--density loose|compact] [--keep] [--n 1..4]"
---

# imagine-ui

**중요: 이 출력은 설계 자료가 아닙니다.** 구현할 수 있는 UI 스펙이 아니라 *스타일 보드*입니다. 실제 픽셀 퍼펙트 화면은 Figma/Sketch에서 만드세요.

## 트리거

- `imagine-ui <screen>` / `imagine-ui --screen login --system kr-minimal`
- "UI 목업 만들어줘"
- "앱 화면 레퍼런스"
- "스크린 레퍼런스"
- "모바일 UI 스타일 보드"
- "imagine-ui"

## 이 스킬이 **하지 않는** 것 — "이 UI 그대로 개발해주세요" 요청 처리

> 이 스킬의 출력은 **스타일 레퍼런스**입니다. 실제 UI 스펙·와이어프레임·구현 가능한 레이아웃이 아닙니다.
>
> - 글자는 디코레이티브 글리프 placeholder이며 실제 카피가 아닙니다.
> - 탭 타겟 크기·여백·접근성·컴포넌트 계층은 보증되지 않습니다.
> - 브랜드 로고/문구처럼 보이는 것은 우연한 형태일 뿐입니다.
>
> **"이 UI 그대로 개발해주세요" 류 요청은 거절합니다.** 진짜 디자인은 Figma에서 프레임·컴포넌트·토큰으로 만들어야 구현 가능합니다. 이 이미지는 Figma 시작 단계의 **인상 수집용**으로만 사용하세요.

스킬 entrypoint는 실제 호출 결과 출력에 위 경고 블록을 항상 포함해야 한다.

## 파이프라인

1. **프리셋 매핑**: `--system` / `--screen` / `--mood` / `--density`를 `config.json`의 매핑 테이블로 영문 비주얼 구문 변환.
2. **Style Guardian 조회**: `--keep` 플래그 또는 "같은 스타일로"·"이어서" 트리거 시 `scripts/lib/style-guardian.js`로 이전 manifest에서 `system` / `palette_hex` / `corner_radius_estimate` / `mood` / `density`를 불러와 prefix 주입. 트리거 없으면 패스스루.
3. **프롬프트 구성**: 시스템 + 스크린 + mood + density 구문을 영문으로 조립. **사용자가 "login 화면에 실제 한국어 텍스트 넣어줘"라고 해도 넣지 않는다** — 글자 렌더링 기대를 버리는 것이 이 스킬의 원칙.
4. **Negative 강제**: `real readable text, photo of phone, hand holding phone, device frame, bezel, notch, cluttered elements, real brand logo, korean letters, chinese letters, japanese letters`. **디바이스 프레임 금지** — 프레임 합성은 `imagine-product`(12-product-mockup) 담당.
5. **이미지 생성**: `size: 1024x1536` (9:19.5 근사, 2:3) PNG로 Codex 이미지 모델 호출. 기본 `n: 1`, 최대 4 (Style Guardian 이어쓰기가 아닌 첫 탐색일 때만 n을 2~4로).
6. **Style Guardian 저장**: 결과에서 추정되는 `palette_hex`(dominant 3~5색, 후속 PR에서 `sharp`+colorthief 결정적 추출) / `corner_radius_estimate` / `system` / `mood` / `density`를 manifest에 저장해 다음 호출에서 `--keep`으로 재사용.

## 시스템 프리셋

| key | 설명 |
|---|---|
| `ios` | iOS 19 스타일, 12px 라운드, SF Pro-like sans, 하어라인 디바이더. |
| `android` | Material 3, 16dp 라운드, Roboto-like, accent surface. |
| `web-mobile` | 모바일 뷰포트용 반응형 웹 UI, 8px 라운드, 뉴트럴 sans. |
| `kr-minimal` | 한국 fintech 감성, Pretendard-like sans, 베이지/뉴트럴 배경, 부드러운 카드 + 서브틀 섀도. |

## 스크린 프리셋

| key | 구조 |
|---|---|
| `login` | 단일 컬럼, 상단 로고, 입력 2개, CTA, 하단 보조 링크. |
| `feed` | 카드 리스트, 썸네일 좌/상단, 메타데이터 서브 행, 고정 탑바. |
| `detail` | 상단 히어로, 타이틀+메타, 액션 로우, 본문 블록, 관련 섹션. |
| `settings` | 그룹 리스트, 좌측 아이콘, 우측 chevron, 섹션 헤더 small caps. |
| `onboarding` | 풀블리드 일러스트·그라디언트, 큰 헤드라인 placeholder, 보조 한 줄, CTA, pager dots. |
| `empty` | 중앙 일러스트, 짧은 헤드라인 placeholder, 액션 버튼 하나, 넉넉한 여백. |

## 출력 규약

```
./images/ui/
  <screen>_<system>_<mood>_<ts>.png
```

- `<screen>`이 명시되지 않았으면 슬러그화된 사용자 컨셉 문자열을 대입.
- `--out-dir` 명시 없으면 `./images/ui/` 고정. 사용자 지정 경로를 조용히 바꾸지 않는다.
- 루트 `./images/` 직하 쓰기 금지.

## Style Guardian 통합

- **저장 키**: `system`, `palette_hex`, `corner_radius_estimate`, `mood`, `density` (`config.style_guardian.manifest_keys`).
- **자동 개입 트리거**: `--keep`, "같은 스타일로", "같은 톤으로", "이어서", "same style as before" (`config.style_guardian.auto_carry_on`).
- **동작**: 트리거 감지 시 style-guardian 에이전트가 `loadStyle()`로 manifest의 마지막 UI 실행에서 키를 읽어 `buildStylePrefix()`로 prompt 앞에 삽입. 사용자에게는 "이전 [Pretendard sans minimal] 화풍과 [#F5EBDC] 강조색을 유지하여 생성합니다." 같은 보고 라인을 먼저 출력한다.
- **주의**: 실제 HEX는 결정적 추출 가능할 때만 저장. 추정 불가 시 `palette_hex: null`로 기록하고 prefix에서 생략.

## 프롬프트 규약

- **이미지 내부에 실제 텍스트 금지.** 글자는 `decorative sans-serif glyph placeholders`로만 표현. 언어(한/영/일/중)를 모델에 명시하지 않는다 — 깨진 한국어가 "한국어처럼 보이려 애쓰다" 발생하는 실패 방지.
- **디바이스 프레임 금지.** 본체/베젤/노치/손 잡는 포즈 모두 negative.
- **브랜드 로고 금지.** 실제 토스·카카오·네이버·Apple 로고가 우연히 생성되지 않도록 `real brand logo`를 negative에 고정 포함.
- 사용자 컨셉 문자열은 원문 보존 — 정직한 영문 변환만 허용.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 폰트가 뭉개져 진짜 UI처럼 보임 | 예상 동작. README 경고 배너 유지 — 실사 UI 아님을 사용자에게 재공지. |
| 가짜 한글 글자가 깨져 나옴 | 언어 명시 없이 `decorative sans-serif glyph placeholders`로 강제. 재생성 1회만. |
| "이 UI 그대로 개발해주세요" | 스킬 entrypoint가 거절 문구(§위 경고 블록)를 반환하고 Figma 시작 워크플로로 안내. 자동 수락 금지. |
| 디바이스 프레임 섞여 나옴 | negative 강화 후 재생성 1회. 지속되면 `imagine-product` 스킬과 구분 안내. |
| 시리즈 간 톤 일관성 깨짐 | `--keep` 누락. Style Guardian manifest 확인 후 `--keep`으로 재호출 권장. |

## 금기

- **구현용 디자인 스펙으로 사용 유도 금지.** 출력에 반드시 "스타일 레퍼런스입니다 / 구현 스펙 아닙니다" 경고를 포함.
- **이미지 안에 실제 카피·사용자 이름·브랜드 로고 주입 금지.**
- **디바이스 프레임 생성 금지** (프레임은 별도 스킬).
- **언어 명시 금지** — 프롬프트에 "Korean text" / "한국어 문구" 등을 넣으면 깨진 글자가 한국어처럼 보이려다 더 실패한다.
- **사용자 출력 경로 조용한 변경 금지.**
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 금지.

## imagine 계열 스킬과의 관계

- 공용 인프라 재사용: `oauth-session.js`, `output-allocator.js`, `request-planner.js`, `style-guardian.js`.
- 텍스트 합성(`compose-text.js`)은 **사용하지 않는다** — UI 샷에 실제 글자를 얹으면 "완성된 디자인"으로 오해될 수 있음.
- `imagine-hero`(랜딩 히어로)·`imagine-og`(소셜 카드)와 구분: 모바일 **앱 화면 내부 레이아웃** 맥락은 항상 여기.
- `imagine-product`(디바이스 프레임 합성, idea 12)과 조합: 이 스킬의 출력(프레임 없는 화면 내부)을 `imagine-product`의 입력으로 넘기면 디바이스에 끼운 목업이 된다.
- `image-to-code`와 구분: 이 스킬의 출력은 **코드로 변환하지 말 것**. image-to-code가 구현용 스펙이 아닌 스타일 보드를 받으면 환상 코드를 만들어낸다.
