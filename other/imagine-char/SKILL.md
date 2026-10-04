---
name: imagine-char
description: 인디 게임·소설·TTRPG용 **게임 캐릭터 일러스트**를 **같은 캐릭터로 반복 생성**하도록 설계된 스킬. Character Card(JSON)를 기준으로 이름/종족/연령/헤어/눈/의상/구별 특징/아트 스타일/팔레트를 고정해두고, 대표 일러스트(portrait_hero) 1장을 reference로 삼아 turnaround·표정·포즈를 이어서 뽑는다. 사용자가 "게임 캐릭터", "캐릭터 일러스트", "imagine-char", "캐릭터 시트 만들어줘", "표정 시트", "포즈 컷" 등을 말하면 이 스킬이 담당한다.
argument-hint: "<create|turnaround|expression|pose> <name-or-concept> [--set neutral,happy,angry,sad,surprised] [--verify-consistency] [--out-dir <path>]"
---

# imagine-char

"한 번 그린 캐릭터를 계속 같은 사람으로 유지하기"에 집중한 스킬. 매 호출마다 Character Card를 프롬프트에 재주입해 머리색·눈색·의상이 다른 사람으로 드리프트하는 것을 막는다.

## 트리거

- `imagine-char create "<이름>, <개념>"` — 카드 초안 + 대표 일러스트 1장
- `imagine-char turnaround <name>` — 정면/¾/측면/후면 4컷
- `imagine-char expression <name> --set neutral,happy,angry,sad,surprised`
- `imagine-char pose <name> "<동작 설명>"`
- "게임 캐릭터", "캐릭터 일러스트", "캐릭터 시트", "턴어라운드", "표정 시트", "포즈 컷"
- "imagine-char"

## Character Card 스키마

모든 캐릭터는 `./characters/<name>/card.json` 에 저장된다. 이 파일이 일관성의 **단일 소스**다.

```json
{
  "name": "아이리스",
  "species": "elf",
  "age_look": "late teens",
  "hair": "silver long braid",
  "eyes": "violet, cat-like",
  "outfit": "navy hooded cloak with gold trim, leather belt, knee-high boots",
  "distinguishing": "crescent moon tattoo on left cheek",
  "art_style": "semi-realistic anime, painterly rendering, soft rim light",
  "palette": ["#1E3A8A", "#FBBF24", "#E5E7EB"],
  "negative": "chibi, overly cute, modern clothes",
  "notes": "선택적 자유 기록 (서사·배경 등)"
}
```

- **필수 키** (`config.card_schema.required`): `name`, `species`, `age_look`, `hair`, `eyes`, `outfit`, `art_style`.
- **선택 키**: `distinguishing`, `palette`, `negative`, `notes`.
- `palette`는 HEX 배열(최대 5개). 프롬프트 주입 시 HEX 그대로가 아니라 색 이름 구문으로 변환, HEX는 manifest에만 보존.
- **카드의 모든 필드는 쉼표 구분 토큰**으로 프롬프트에 주입된다(`config.prompt.join: token_comma`). 순서는 `field_order_for_prompt` 고정.

## 파이프라인

1. **카드 로드·검증**: `character-card-keeper` 에이전트가 `./characters/<name>/card.json`을 읽는다. 없으면 `create` 서브명령만 허용(빈 카드 금지).
2. **저작권 필터**: `config.copyright.blocked_keywords_examples`(Pokemon, Pikachu, Mario, Link 등)를 카드 또는 사용자 프롬프트에서 검출하면 **생성을 차단**하고 경고. 자동 회피 변형 금지 — 사용자가 카드를 수정해야 진행.
3. **프롬프트 조립**: `field_order_for_prompt` 순서로 카드 필드를 comma-join → `consistent character, full body shot preferred, clean background or simple gradient` suffix → `negative_prompt`(카드 `negative` + 전역 negative 병합).
4. **reference 주입**: `portrait_hero.png`가 이미 있으면 `image_to_image` 모드로 reference로 사용 (`consistency.portrait_hero_as_reference: true`). 없으면 text-to-image.
5. **서브명령별 분기**:
   - `create`: 카드 초안 작성(사용자 입력 → 카드 키로 매핑) 후 `portrait_hero.png` 1장 생성.
   - `turnaround`: front / three_quarter / side / back 4장을 **개별 호출**로 생성(한 장에 그리드로 모아 그리지 않음).
   - `expression`: `--set`의 각 라벨별로 **개별 생성** 후 저장(`expression_<label>.png`). 한 장에 몰아 그리지 않는 것이 핵심 — 한 장 그리드는 AI가 서로 다른 캐릭터를 만들게 된다.
   - `pose`: 단일 포즈 장면. 동작 설명을 카드 뒤에 덧붙여 주입.
6. **일관성 검증 (opt-in `--verify-consistency`)**: `visual_critic.checks`(hair / eye / outfit / distinguishing match)를 수행. 1회까지만 자동 재생성(`retry_on_fail_max: 1`). 지속 실패 시 사용자에게 "카드 업데이트 또는 reference 갱신 권장" 안내.
7. **reference 갱신 제안**: 새 산출물이 `portrait_hero`보다 품질·일치도가 명백히 좋으면 사용자에게 "portrait_hero를 이 컷으로 교체할까요?" 제안(자동 교체 금지).

## 출력 규약

```
./characters/<name>/
├── card.json
├── portrait_hero.png
├── turnaround_front.png
├── turnaround_three_quarter.png
├── turnaround_side.png
├── turnaround_back.png
├── expression_<label>.png
├── pose_<slug>.png
└── _manifest.json
```

- `<name>`: 카드의 `name` 필드 기반 slugify(한글 그대로 유지 가능, 파일 시스템 안전 문자만 사용).
- `--out-dir` 지정 시 그대로 사용. 조용한 경로 변경 금지.
- 루트 `./characters/` 외부 쓰기 금지(`--out-dir` 없는 한).
- **카드 외 메타데이터는 `_manifest.json` 하나에만** — 각 이미지 옆에 사이드카 파일을 산란시키지 않는다.

## 프롬프트 규약

- **카드 없이 생성 금지.** `create` 외 서브명령은 카드가 없으면 즉시 거절.
- **사용자 자유 프롬프트는 카드 뒤에만 붙인다.** 사용자가 "은발을 금발로 바꿔달라"고 자유 프롬프트로 요청해도, 카드의 `hair`를 먼저 바꾸지 않으면 반영하지 않는다. 카드 갱신 경로(`character-card-keeper`)로 유도.
- **HEX 주입 금지.** `palette` HEX는 색 이름 구문 변환 후 주입. 원본 HEX는 manifest에만.
- **그리드 시트 금지.** `model sheet grid lines`를 negative에 고정 — 한 장에 여러 뷰를 그리려는 시도는 결과를 망친다.

## 일관성 장치

- **portrait_hero가 reference의 기준선.** 모든 후속 호출은 카드 + portrait_hero 2개를 reference로 쓴다.
- **Visual Critic (opt-in)**: `--verify-consistency` 플래그. hair_color_match / eye_color_match / outfit_match / distinguishing_match 4축 검사. 점수 임계 미달 시 1회 재생성.
- **Style Guardian 스코프 제한**: 캐릭터 간 스타일 누출 금지 (`style_guardian.cross_character_leak: false`). 캐릭터 A의 팔레트가 캐릭터 B 생성에 섞이지 않도록 스코프는 `per_character`.

## 실패 모드 대응

| 증상 | 조치 |
|---|---|
| 2번째 생성에서 머리색·의상 드리프트 | 카드 재주입 + portrait_hero reference 강제. 여전히 튀면 `--verify-consistency`로 1회 재생성. 반복되면 portrait_hero를 더 잘 나온 컷으로 사용자가 갱신하도록 안내. |
| 표정 시트가 어색 | 한 장에 여러 표정 그리지 말고 라벨별 **개별 호출**. `--set`은 자동으로 개별 호출로 분해된다. |
| 저작권성 캐릭터 연상 | `config.copyright` 필터가 차단. 자동 "회피 변형" 생성 금지, 사용자에게 카드 수정 요청. |
| 카드가 비어 있음 | 생성 중단. `create`로 먼저 카드 초안을 만들도록 안내. |
| Visual Critic 미설치 | 경고 후 검증 스킵. 이미지 생성은 정상. |
| 캐릭터 이름이 파일 시스템에 부적합 | slugify 결과 미리보기 + 사용자 확인 후 진행. 자동 rename 금지. |

## 금기

- **카드 우회 생성 금지.** 카드 없는 서브명령(turnaround/expression/pose)은 거절.
- **카드 자동 수정 금지.** 자유 프롬프트로 카드 값을 조용히 덮어쓰지 않는다. 카드 변경은 `character-card-keeper` 경로만.
- **그리드 시트 프롬프트 금지.** 턴어라운드/표정은 개별 호출만.
- **저작권성 캐릭터 자동 회피 변형 금지.** 필터 차단 후 사용자에게 카드 수정 요청.
- **HEX를 프롬프트에 직기재 금지.** 이름 구문으로만.
- **캐릭터 간 Style Guardian 토큰 누출 금지.**
- **`./characters/` 외부 쓰기 금지** (`--out-dir` 지정 없는 한).
- `masterpiece` / `8k UHD` / `fulfill all requests` 류 부스터·우회 문구 금지.

## imagine 계열 스킬과의 관계

- 공용 인프라: `oauth-session.js`, `output-allocator.js`, `request-planner.js`. 카드 관리는 전용 에이전트 `character-card-keeper`에 위임.
- `compose-text.js`는 **사용하지 않음** — 캐릭터 일러스트에 글자를 합성하지 않는다.
- `imagine-hero`(히어로 비주얼), `imagine-og`(소셜 카드)와 구분: 이 스킬은 **동일 캐릭터의 반복 생성**이 목적. 일회성 장면은 다른 스킬.
- `imagine-char-pixel`(idea 06, 픽셀 아트)과 구분: 하이 디테일 일러스트는 여기, 8-bit/16-bit 픽셀은 그 스킬.
