---
name: story-to-veo3
description: NADIO 오디오 드라마 JSON을 Google Veo 3 비디오 프롬프트로 변환. 캐릭터 비주얼, 감정 표현, 시네마틱 샷 구성을 최적화하여 고품질 비디오 생성 프롬프트 제공.
category: video-generation
triggers:
  keywords: ["veo3", "veo 3", "google video", "video generation", "오디오 드라마 비디오화"]
  file_patterns: ["*.json"]
  content_patterns: ["scenes", "characters", "dialogue", "narration"]
---

# Story to Veo 3 - NADIO Audio Drama to Google Veo 3 Video Prompts

NADIO 포맷 오디오 드라마를 Google Veo 3 비디오 생성 프롬프트로 자동 변환합니다.

## 주요 기능

### 1. **Google Veo 3 최적화**
- **8초 최적 세그먼트**: Veo 3의 8초 최적 길이에 맞춰 자동 분할
- **고해상도 지원**: 4K (3840×2160) 해상도 최적화
- **자연스러운 모션**: Veo 3의 고급 물리 엔진 활용
- **정확한 텍스트 프롬프트 해석**: 상세한 장면 묘사로 정확도 향상

### 2. **캐릭터 비주얼라이제이션**
- 성별, 나이, 성격 기반 외모 프로필 자동 생성
- 감정별 표정 매핑 (37종 감정 → 영어 표현)
- 첫 등장 시 상세 묘사, 이후 간결한 참조
- 일관된 캐릭터 외모 유지

```python
# 감정 → 표정 매핑 예시
"충격": "shocked, frozen expression, eyes wide"
"간절함": "desperate, pleading eyes, earnest expression"
"눈물": "crying, tears streaming down face"
```

### 3. **시네마틱 샷 구성**
- **카메라 앵글**: 12종 (extreme close-up ~ bird's eye view)
- **카메라 무브먼트**: 11종 (static ~ dolly zoom)
- **조명 디자인**: 자연광, 극적 조명, 분위기별 설정
- **한국 드라마 스타일**: 한국 영상미 반영

### 4. **요소별 변환 로직**

#### 내레이션 → 장면 설정 샷
```
[SHOT 1: ESTABLISHING]
Wide shot: Modern Korean apartment interior. Morning light, soft golden hour.
Camera: Slow push in, stabilized, cinematic framing
Lighting: Natural ambient light, realistic shadows
```

#### 대화 → 캐릭터 샷
```
[SHOT 2: DIALOGUE - 민주]
Medium close-up: MINJU (late 30s, female), confident, determined eyes, firm jaw, speaking.
Action: "I know who you really are..."
Camera: Static, focused on face
Lighting: Soft key light on face
```

#### 내적 독백 → 표정 클로즈업
```
[SHOT 3: INNER THOUGHT - 민주]
Close-up: Minju, shocked expression, eyes wide, deep in thought.
Thought process: "Could it really be her after 30 years?"
Camera: Slow push in, shallow depth of field
Lighting: Dramatic emotional lighting
```

#### 음향 효과 → 시각적 디테일
```
[SHOT 4: DETAIL]
Close-up: Hand pressing apartment doorbell button.
Light flickers on intercom panel.
Camera: Static close-up, sharp focus
```

## 사용법

### 기본 변환
```bash
cd /Users/realpio4/Documents/vibe-with-kimi-cli-main/.claude/skills/story-to-veo3

# 1. JSON → Veo 3 프롬프트 변환
python3 scripts/story_to_veo.py \
  ../story-to-voice/output/lost_sister_found.json

# 출력: output/lost_sister_found_veo_prompts.txt
```

### 8초 세그먼트 분할
```bash
# 2. 긴 프롬프트를 8초 단위로 분할 (Veo 3 최적화)
python3 scripts/split_for_veo.py \
  output/lost_sister_found_veo_prompts.txt

# 출력: output/lost_sister_found_veo_prompts_8sec_segments.txt
```

### 개별 파일 분할
```bash
# 3. 각 세그먼트를 독립 파일로 저장
python3 scripts/split_to_files.py \
  output/lost_sister_found_veo_prompts_8sec_segments.txt \
  output/lost_sister_found_veo_prompts.txt \
  output/segments

# 출력: output/segments/segment_001.txt ~ segment_NNN.txt
```

### 스타일 옵션
```bash
# 한국 드라마 스타일 (기본)
python3 scripts/story_to_veo.py story.json

# 시네마틱 스타일
python3 scripts/story_to_veo.py story.json output.txt cinematic

# 다큐멘터리 스타일
python3 scripts/story_to_veo.py story.json output.txt documentary
```

## Google Veo 3 프롬프트 최적화 원칙

### 1. **시각적 디테일 강조**
- ✅ **구체적 묘사**: "middle-aged woman in tailored blazer"
- ❌ **모호한 표현**: "woman in professional attire"

### 2. **카메라 워크 명시**
- 카메라 앵글: close-up, medium shot, wide shot
- 카메라 움직임: slow push in, tracking shot, static
- 렌즈 효과: shallow depth of field, bokeh

### 3. **조명과 분위기**
- 조명 소스: natural light, soft key light, dramatic lighting
- 색감: warm tones, cold blue, natural palette
- 분위기: tense, emotional, hopeful

### 4. **자연스러운 모션**
- Veo 3는 물리 법칙을 잘 이해함
- "speaking, mouth moving naturally"
- "tears streaming down face"
- "hand pressing button"

### 5. **시간 최적화**
- **8초 세그먼트**: Veo 3의 최적 길이
- **2-3 샷 per 세그먼트**: 자연스러운 편집 리듬
- **연속성 유지**: 세그먼트 간 캐릭터/조명 일관성

## 출력 형식

### 프롬프트 파일 구조
```
################################################################################
# VEO 3 VIDEO PROMPTS
# Story: 30년 만의 재회: 예비시댁에서 찾은 여동생
################################################################################

[PROJECT OVERVIEW]
Title: ...
Duration: ...
Genre: ...

[CHARACTER VISUAL GUIDE]
민주:
  - Gender: female
  - Age: 30대 후반
  - Personality: 사업가, 단호함
  - Visual: professional attire, tailored blazer, confident posture

================================================================================
Scene: 예비시댁에서의 충격 (Act 1)
Recommended Duration: 30-40 seconds
Style: korean-drama
================================================================================

[SCENE CONTEXT]
Modern Korean household, affluent neighborhood...

[SHOT 1: ESTABLISHING]
...

[SHOT 2: DIALOGUE - 민주]
...

================================================================================
[TECHNICAL SPECIFICATIONS]
- Aspect Ratio: 16:9 (widescreen)
- Frame Rate: 24fps (cinematic)
- Resolution: 4K (3840×2160)
- Color Grading: Natural Korean drama palette
- Style: Realistic Korean cinematography
================================================================================
```

## 워크플로우

### 전체 프로세스
```
1. NADIO JSON 준비
   ↓
2. story_to_veo.py 실행
   → 전체 프롬프트 생성 (*.txt)
   ↓
3. split_for_veo.py 실행
   → 8초 세그먼트 분할 (*_8sec_segments.txt)
   ↓
4. split_to_files.py 실행
   → 개별 파일 생성 (segments/segment_*.txt)
   ↓
5. Google Veo 3 생성
   - 각 segment_*.txt를 복사
   - Veo 3 UI에 붙여넣기
   - 8초 비디오 생성
   ↓
6. 후반 작업
   - 세그먼트 순서대로 결합
   - 색보정 (consistent grading)
   - 오디오 싱크
```

## 기술 사양

### Veo 3 최적 설정
- **해상도**: 4K (3840×2160)
- **프레임레이트**: 24fps (cinematic)
- **종횡비**: 16:9 (widescreen)
- **세그먼트 길이**: 8초 (optimal)
- **샷 수**: 2-3 shots per segment

### 권장 사양
- **Color Space**: Rec. 709 (standard video)
- **동적 범위**: SDR (standard) or HDR10
- **인코딩**: H.264 (호환성) or H.265 (품질)

## 캐릭터 프로필 예시

```python
{
  "민주": {
    "gender": "female",
    "age": "30대 후반",
    "personality": "사업가, 단호함, 성공한 커리어우먼",
    "visual": "professional attire, tailored blazer, confident posture, sleek hairstyle",
    "age_desc": "late 30s",
    "role": "protagonist"
  },

  "민정": {
    "gender": "female",
    "age": "30대 초반",
    "personality": "순함, 착함, 두려움",
    "visual": "gentle features, soft eyes, simple clothing, warm demeanor",
    "age_desc": "early 30s",
    "role": "sister"
  }
}
```

## 감정 표현 매핑

| 한국어 감정 | 영어 표정 묘사 |
|------------|---------------|
| 중립 | neutral, calm expression |
| 긴장 | tense, worried eyes, furrowed brow |
| 놀람 | wide eyes, mouth slightly open in surprise |
| 충격 | shocked, frozen expression, eyes wide |
| 슬픔 | sad eyes, downturned mouth, tears welling |
| 분노 | angry, jaw clenched, intense glare |
| 두려움 | fearful, trembling, wide frightened eyes |
| 간절함 | desperate, pleading eyes, earnest expression |
| 확신 | confident, determined eyes, firm jaw |
| 눈물 | crying, tears streaming down face |
| 감동 | moved, emotional, misty eyes |
| 행복 | happy, bright smile, sparkling eyes |

## 예시: 실제 변환 결과

### 입력 (NADIO JSON)
```json
{
  "type": "dialogue",
  "speaker": "민주",
  "content": "30년... 정말 민정이구나...",
  "emotion": "눈물"
}
```

### 출력 (Veo 3 프롬프트)
```
[SHOT 5: DIALOGUE - 민주]
Medium close-up: Minju, crying, tears streaming down face, speaking.
Action: Character saying "30 years... It's really you, Minjeong..."
Camera: Static or subtle handheld, focused on face
Lighting: Soft key light on face, natural shadows
```

## 제한사항

- Veo 3는 8초 최적, 최대 15초까지 생성 가능
- 복잡한 카메라 무브먼트는 단순화 권장
- 한 샷에 여러 캐릭터 동시 등장 시 배치 명시 필요
- 빠른 액션 시퀀스는 여러 세그먼트로 분할

## 팁

### 1. 프롬프트 작성
- 구체적인 시각적 디테일 우선
- 카메라 앵글과 움직임 명시
- 조명과 분위기 설명

### 2. 세그먼트 분할
- 자연스러운 편집 포인트에서 분할
- 캐릭터 일관성 유지
- 조명/색감 연속성 확인

### 3. 후반 작업
- 색보정으로 톤 통일
- 오디오 싱크 정확히 맞추기
- 자연스러운 트랜지션

## 파일 구조

```
story-to-veo3/
├── SKILL.md                    # 이 문서
├── README.md                   # 간단한 가이드
├── scripts/
│   ├── story_to_veo.py        # 메인 변환 스크립트
│   ├── split_for_veo.py       # 8초 세그먼트 분할
│   └── split_to_files.py      # 개별 파일 생성
└── output/                     # 생성된 프롬프트
```

## 관련 스킬

- **story-to-voice**: NADIO 스토리를 음성으로 변환
- **story-with-effect**: 오디오에 효과음과 배경음악 추가
- **story-to-sora2**: OpenAI Sora 2용 프롬프트 생성

## 참고 자료

- Google Veo 3 Documentation
- 시네마틱 촬영 기법
- 한국 드라마 영상미 분석
- 감정 표현 연기론
