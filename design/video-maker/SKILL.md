---
name: video-maker
description: "영상 요청의 진입점. Remotion 또는 HyperFrames 중 엔진 하나를 골라 스크립트→음성(TTS)→컴포지션→자막→렌더를 코드 기반으로 설계·구현·검증한다. 제품 소개 영상, 데모 비디오, SNS 숏폼, 데이터 시각화 영상, 나레이션·자막 영상, MP4 렌더링, Remotion, HyperFrames 요청에 /video-maker로 사용한다. 전역에 설치된 HyperFrames 스킬 번들의 라우터는 진입점으로 쓰지 않는다."
---

# Video Maker — 선택형 코드 영상 제작

하나의 영상 제작 계약 아래에서 프로젝트에 맞는 엔진 하나만 선택합니다. Remotion은 React/TSX
컴포지션에, HyperFrames는 HTML/CSS/GSAP 컴포지션에 사용합니다. 두 엔진을 같은 프로젝트에
관성적으로 함께 설치하지 않습니다.

## 경계

- 이 스킬은 시간축이 있는 영상과 이미지 시퀀스를 소유하며, 영상 요청의 유일한 진입점입니다.
- 전역 스킬 디렉터리에 HeyGen HyperFrames 스킬 번들이 설치되어 있어도 그 `hyperframes` 라우터와
  `general-video`, `faceless-explainer` 같은 워크플로우 스킬을 진입점으로 쓰지 않습니다. 번들은
  HyperFrames를 선택했을 때 [references/hyperframes-engine.md](references/hyperframes-engine.md)가
  정한 모듈만 정확한 경로로 직접 읽는 source-only 자산으로 취급합니다.
- `design-plan`과 `frontend-design`은 웹 UI와 브라우저 인터랙션을 소유합니다.
- HyperFrames를 Aphrodite의 프론트 모션 엔진으로 호출하지 않습니다.
- `DESIGN.md`가 있으면 브랜드 토큰과 모션 원칙을 소비하되 영상의 shot·timing·audio 결정은 이
  스킬의 산출물에 기록합니다.
- API, 영속 데이터, 제품 비즈니스 로직은 기존 애플리케이션 하네스가 소유합니다.

## 적용 시점

- `/video-maker` 명시 실행
- "영상 만들어줘", "소개 비디오", "데모 영상", "숏폼", "MP4로 렌더링" 요청
- 기존 Remotion 또는 HyperFrames 컴포지션의 생성·수정·렌더·검증 요청

## Phase 0: 기존 구현과 엔진 확인

다음 순서로 조회합니다.

1. 프로젝트 manifest·lockfile과 기존 영상 디렉터리
2. `remotion.config.*`, `<Composition>`, `useCurrentFrame()`
3. HyperFrames `index.html`, `data-composition-id`, `window.__timelines`
4. `DESIGN.md`, 영상 brief·storyboard·script·asset manifest

기존 엔진이 있으면 그대로 사용합니다. 둘 다 있거나 기존 구조와 다른 엔진을 명시적으로 요구하면
변경 범위와 마이그레이션 비용을 먼저 설명합니다.

## Phase 1: Engine Router

사용자 선택이 있으면 우선합니다. 선택이 없으면 다음 순서로 하나를 고릅니다.

| 조건 | 엔진 |
|---|---|
| 기존 프로젝트가 한 엔진을 사용 | 기존 엔진 |
| React/TSX 컴포넌트·타입·패키지 재사용이 핵심 | Remotion |
| HTML/CSS/GSAP 장면을 빌드 단계 없이 직접 영상화 | HyperFrames |
| 검증된 Remotion Lambda 파이프라인을 유지 | Remotion |
| Apache-2.0 프레임워크가 배포 요건 | HyperFrames |
| 판단 근거가 부족 | 설치하지 말고 사용자에게 엔진 차이를 한 번 설명 |

Remotion을 선택하면 [references/remotion-engine.md](references/remotion-engine.md), HyperFrames를
선택하면 [references/hyperframes-engine.md](references/hyperframes-engine.md)만 읽습니다. 선택하지 않은
엔진 reference는 읽거나 적용하지 않습니다.

## Phase 2: 설치·라이선스 게이트

설치 전 다음을 기록합니다.

- 선택 엔진과 선택 근거
- 기존 package manager·lockfile·Node 버전
- FFmpeg와 브라우저 런타임 가용성
- 사용할 정확한 패키지 버전과 공식 배포처
- 프로젝트·조직에 적용되는 라이선스 확인 결과

규칙:

- `@latest`, 전역 설치, 원격 install script를 기본값으로 쓰지 않습니다.
- `npx skills add heygen-com/hyperframes`, `npx skills add remotion-dev/skills`, `npx skills add elevenlabs/skills`를
  실행하지 않습니다.
- 사용자 전역 스킬 디렉터리나 다른 CLI 설치본으로 복사·동기화하지 않습니다.
- 이미 설치된 서드파티 스킬 번들은 제거·갱신·재설치하지 않습니다. 번들 문서가 `npx hyperframes@latest`
  같은 unpinned 실행을 권해도 이 스킬의 버전 고정 규칙이 우선합니다.
- 프로젝트 의존성 변경은 정확한 패키지와 버전, 변경 파일을 제시한 뒤 현재 작업 범위의 승인을
  확인합니다.
- 설치하지 않아도 가능한 설계·검토 작업은 설치 없이 계속합니다.
- Remotion은 현재 법인 유형과 조직 규모에 따라 회사 라이선스가 필요할 수 있으므로 공식
  `LICENSE.md`를 확인하고, 판단 불가이면 `LICENSE REVIEW REQUIRED`로 남깁니다.

## Phase 3: 공통 제작 계약

구현 전에 다음을 확정합니다.

| 항목 | 필수 내용 |
|---|---|
| Goal | 영상이 바꿔야 할 한 가지 이해 또는 행동 |
| Audience | 시청자와 시청 맥락, 무음 재생 가능성 |
| Format | 해상도, 비율, fps, 목표 길이, 출력 형식 |
| Story | hook → evidence/demo → resolution/CTA |
| Scenes | 각 scene의 시작·종료·핵심 프레임·전환 |
| Assets | 로컬 경로, 출처, 라이선스, attribution, 변경 허용 |
| Audio | 음성·BGM·SFX의 필요성, 출처, 음량, 무음 대체 |
| Accessibility | 자막, flashing 제한, 읽기 시간, 색 외 신호 |
| Acceptance | 대표 프레임과 완성 판정 방법 |

실제 제품 수치·후기·로고를 추측하지 않습니다. `verified`, `prototype`, `placeholder`, `hypothesis`를
구분하고 최종 영상에 placeholder가 남으면 완료로 보고하지 않습니다.

### 파이프라인 단계

어느 엔진을 골라도 단계는 같습니다. 필요 없는 단계는 `SKIPPED`, 실행하지 못한 단계는 `NOT RUN`으로
남깁니다.

| 단계 | 산출물 | 담당 문서 |
|---|---|---|
| Script | `STORYBOARD.md`, 나레이션이 있으면 `SCRIPT.md` | 이 Phase와 [references/voice-captions.md](references/voice-captions.md) 4절 |
| Voice | 나레이션 오디오, 가능하면 단어 timestamps, provenance 행 | [references/voice-captions.md](references/voice-captions.md) |
| Composition | 엔진 컴포지션 | 선택한 엔진 reference |
| Captions | 엔진이 소비하는 caption 데이터와 자막 clip | [references/voice-captions.md](references/voice-captions.md) |
| Render | still, draft, final 출력 | [references/video-qa.md](references/video-qa.md) |

`STORYBOARD.md`와 `SCRIPT.md`는 HyperFrames 번들 `hyperframes-core`의 storyboard-format과
script-format shape를 두 엔진 공통으로 씁니다. 번들이 없으면 같은 shape를 이 스킬이 직접 작성합니다.
스크립트와 스토리보드는 프레임워크가 만들어 주지 않으며 이 Phase에서 에이전트가 brief를 근거로
씁니다.

TTS 공급자는 HeyGen, ElevenLabs, Typecast, Edge TTS, Kokoro 중 사용자 지정과 언어·비용 조건으로
고르며 하나로 고정하지 않습니다. 요금이 발생하는 호출은 확인 후 실행합니다.

## Phase 4: 구현

- 장면은 독립적으로 수정·검증할 필요가 있을 때만 컴포넌트로 나눕니다.
- 시간은 wall clock이 아니라 엔진의 frame/timeline 값을 사용합니다.
- `Math.random()`, `Date.now()`, 네트워크 응답 순서처럼 재현 불가능한 입력을 렌더 경로에 두지
  않습니다. 변이가 필요하면 고정 seed를 사용합니다.
- 오디오·워터마크·자동재생 효과는 기본 포함하지 않습니다.
- 폰트와 미디어가 준비되기 전에 capture하지 않습니다.
- 사용하지 않는 엔진의 package·설정·템플릿을 추가하지 않습니다.

## Phase 5: 검증과 렌더

[references/video-qa.md](references/video-qa.md)를 읽고 최소 다음을 실행합니다.

1. 엔진별 lint/typecheck와 컴포지션 목록 확인
2. 대표 still을 렌더하고 이미지로 직접 관찰
3. 짧은 draft 구간을 렌더해 timing·media sync·전환 확인
4. 최종 렌더의 duration·resolution·fps·stream·audio 검사
5. 자막·가독 시간·flashing·asset provenance 확인
6. 나레이션이 있으면 자막 timing 출처(공급자 timestamps 또는 전사)와 TTS provenance 확인

실행하지 못한 검사는 `NOT RUN`, 결과를 관찰하지 못한 항목은 `UNVERIFIED`로 남깁니다.

## 완료 증거

- 선택 엔진과 라우팅 근거
- 설치·라이선스 상태
- 사용한 brief·storyboard·script·asset manifest
- 단계별 상태(Script, Voice, Composition, Captions, Render)와 TTS 공급자·voice·모델
- 생성·수정한 컴포지션과 출력 경로
- still/draft/final 검증 결과
- 남은 `NOT RUN`, `UNVERIFIED`, 권리·품질 이슈

## Direct References

| 파일 | 읽는 시점 |
|---|---|
| [references/remotion-engine.md](references/remotion-engine.md) | Remotion을 선택했을 때만 |
| [references/hyperframes-engine.md](references/hyperframes-engine.md) | HyperFrames를 선택했을 때만 |
| [references/voice-captions.md](references/voice-captions.md) | 나레이션 또는 자막이 필요할 때만 |
| [references/video-qa.md](references/video-qa.md) | 모든 렌더와 납품 전 |

전역 HyperFrames 번들 모듈은 HyperFrames를 선택했고 번들이 존재할 때만
[references/hyperframes-engine.md](references/hyperframes-engine.md)의 모듈 표에 적힌 정확한
`SKILL.md`와 reference 경로로 읽습니다. `/hyperframes`, `/media-use` 같은 slash 호출로 넘기지 않습니다.
