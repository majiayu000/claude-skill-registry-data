---
name: course-resource-creator
description: course-builder의 강의 섹션을 읽고 핵심 기술 내용을 추출하여 Gemini에서 고품질 슬라이드 이미지를 생성하기 위한 프롬프트를 작성합니다.
version: 9.2.0
category: image-generation
---

# Course Resource Creator (교육 자료 이미지 프롬프트 생성기)

이 스킬은 **course-builder의 강의 섹션**을 읽고 **핵심 기술 내용을 추출**하여, **Google Gemini**가 최상의 품질로 **슬라이드 이미지**를 생성할 수 있도록 최적화된 프롬프트를 작성하는 수동 작업 도구입니다.

## 🎓 NADIO Course Production Pipeline

```
📝 course-builder (기획)
   ↓ section_XX_XX_*.md (교육 콘텐츠)
🎙️ course-dialog-builder (오디오 + 타임스탬프)
   ↓ lecture_X_Y_refined.json (segments with timestamps)
   ↓ lecture_X_Y_complete.mp3
🖼️ course-resource-creator (이미지 프롬프트) ← YOU ARE HERE
   ↓ segment_*.md (기술 내용 추출)
   ↓ image_prompts.txt (Gemini 입력용)
   ↓ segment_*.png (수동 생성, 1:1 매핑)
🎬 course-video-creator (타임스탬프 기반 조립)
   ↓ lecture_X_Y_auto.mp4 (refined.json 타임스탬프 직접 사용)
📤 course-inflearn-uploader (업로드)
```

## 🎯 목적

- **course-builder**에서 생성한 상세한 교육 콘텐츠를 읽고 **핵심 기술 내용만 추출**
- 추출한 내용을 기반으로 **segment 파일** 생성 (이미지 설명용)
- segment 파일을 읽고 **Gemini 이미지 생성 프롬프트** 작성
- **수동으로** Gemini 웹사이트에서 이미지 생성

## 📂 입력 및 출력

### 입력 파일
- **강의 섹션**: `course-builder/output/inflearn_sections/ch{N}/section_{chapter}_{section}_{topic}.md`
  - 예: `section_01_01_agent.md`, `section_01_02_runtime.md`
  - 상세한 교육 내용, 코드 예시, 설명 포함

### 출력 파일
- **segment 파일 (기술 내용 + 이미지 프롬프트)**: `output/lecture_{X}_{Y}/segment_{N}_{type}.md`
  - 예: `segment_0_opening.md`, `segment_1_concept.md`
  - 각 파일에 다음 두 섹션 포함:
    1. **이미지에 그려질 기술 내용**: 코드, 다이어그램, 플로우차트
    2. **Gemini 이미지 생성 프롬프트**: `=== Slide N: ... ===` 형식의 전체 프롬프트
  - Gemini에서 직접 복사하여 사용 가능

- **생성된 이미지**: `output/lecture_{X}_{Y}/images/segment_{N}.png`
  - Gemini 웹사이트에서 수동 생성
  - 16:9 가로 형식 (1920x1080 or 1280x720)
  - segment_N.png는 segment_id N과 1:1 매핑

**⚠️ 중요**: image_prompts.txt 별도 파일은 생성하지 않음. 모든 프롬프트는 각 segment 파일 내부에 포함됨

## 🛠️ 작업 흐름 (Manual Workflow)

### 1단계: 강의 섹션 분석 및 Segment 파일 작성 (🔴 필수)

**목적**: refined.json의 각 segment를 분석하여 이미지 설명용 마크다운 파일 작성

**🔴 필수 규칙**:
**refined.json의 segment 개수 = segment 파일의 개수**
- refined.json에 4개 segments가 있으면 → 반드시 4개 segment 파일 생성
- refined.json에 7개 segments가 있으면 → 반드시 7개 segment 파일 생성
- segment_id와 파일 개수가 정확히 1:1 매핑되어야 함

**작업 과정**:
1. `lecture_X_Y_refined.json` 파일 읽기
   - `segments` 배열의 개수 파악
   - segment_id 범위 확인 (0부터 N까지)

2. 각 segment마다 시각화할 내용 추출
   - segment_id와 type 기반으로 파일명 결정
   - 기술 내용, 코드, 다이어그램 포함
   - 교육용 시각 요소(아이콘, 화살표, 구조도) 추가
   - **마지막에 반드시 4가지 필수 준수사항 포함**

3. Segment 파일 생성 (모든 segment에 대해)
   - 기술 내용은 간결하게 요약
   - **Gemini 이미지 생성 프롬프트**는 `references/nano_minimalist_standard.md`의 형식을 엄격히 준수

4. 각 segment 파일 검증
   - ✅ segment_id 순서대로 생성되었는지 확인
   - ✅ refined.json의 segments 개수와 파일 개수 일치 확인
   - ✅ 모든 파일에 필수 준수사항 포함 확인
   - ✅ 시각화 가능성 확인

**출력**: `output/lecture_X_Y/segment_0_*.md` ~ `segment_N_*.md` (총 N+1개)

### 2단계: 각 Segment 파일에 이미지 프롬프트 추가 (🔴 필수)

**목적**: 각 segment 파일의 기술 내용 아래에 Gemini 이미지 프롬프트를 직접 포함

**참고 문서**: 
- **`references/nano_minimalist_standard.md`**: 프롬프트 템플릿과 스타일 가이드의 Source of Truth입니다. 모든 프롬프트 작성 시 이 파일을 반드시 참조하십시오.

**파일 구조** (각 segment_{N}_{type}.md):
```markdown
# Segment {N}: {type} - {제목}

## 이미지에 그려질 기술 내용
[코드, 다이어그램, 플로우차트 등]

---

## Gemini 이미지 생성 프롬프트

=== Slide {N}: {Type} - {제목} ===

FORMAT: 16:9 horizontal educational slide (1920x1080)

CONTENT:
{시각화할 내용에 대한 한국어 지시문. 상황 묘사, 배치, 메타포 등을 간결하게 서술.}
상단 라벨: "Segment {N}: {Type} - {제목}"
메인 제목: "{압축된 메인 제목}"
제목 아래 얇은 구분선.

{구체적인 비주얼 요소 묘사. 왼쪽/오른쪽/중앙 배치 등.}

DESIGN REQUIREMENTS:
- 배경: 순수 흰색
- 시각 요소:
  * 상단 라벨 및 제목
  * {핵심 비주얼 요소 1}
  * {핵심 비주얼 요소 2}
- 스타일: {스타일 정의 (예: 현대적 인포그래픽, 미니멀리즘 다이어그램)}

EXACT KOREAN TEXT:
Segment {N}: {Type} - {제목}

{메인 제목}

{본문 텍스트 - 나노 미니멀리즘 적용}
[키워드] 내용
⬇️
[키워드] 내용

"여기에 핵심 메시지 한 문장 (따옴표 포함)."

🖼️ 이미지 생성 필수 조건:
- 시간 필요없어 , 오늘 날짜
- 오늘 시간 필요 없다 표현 하지 마라
- 항상 흰 바탕
- 전체에 꽉차게 그려줘
```

**필수 규칙**:
- **Nano-Minimalism**: 텍스트는 극한으로 압축
- **No Robot**: 로봇 금지, 추상적 형상/아이콘 사용
- **4가지 필수 조건**: `EXACT KOREAN TEXT` 마지막에 반드시 포함

**출력**: `output/lecture_X_Y/segment_0_*.md` ~ `segment_N_*.md`

### 3단계: Segment 파일 검증 및 최적화

**목적**: 작성된 segment 파일들이 이미지 생성에 최적화되어 있는지 확인

**검증 과정**:
1. 각 segment 파일의 "이미지에 그려질 기술 내용" 섹션 검토
2. 각 segment 파일의 "Gemini 이미지 생성 프롬프트" 섹션 검증
   - **`references/nano_minimalist_standard.md`** 준수 여부 확인
   - 4가지 필수 준수사항 포함 확인
   - FORMAT이 "16:9 horizontal" 지정되어 있는지 확인

**출력**: 최적화된 segment 파일들 (프롬프트 포함)

### 4단계: Gemini 이미지 생성 (수동)

**⚠️ 완전 수동 작업 - 자동화 불가**

**작업 순서**:
1. segment 파일 열기
2. **Gemini 3 웹사이트** 접속: https://gemini.google.com
3. 각 segment 파일의 "Gemini 이미지 생성 프롬프트" 섹션을 순차적으로 복사하여 붙여넣기
4. 생성된 이미지 다운로드 및 저장 (`output/lecture_X_Y/images/`)

## 📋 segment 파일 작성 가이드

**참고**: 상세한 가이드와 예시는 **`.claude/skills/course-resource-creator/references/nano_minimalist_standard.md`** 파일을 참조하세요.

### 필수 포함 사항
1. **이미지에 그려질 기술 내용** 섹션
2. **Gemini 이미지 생성 프롬프트** 섹션
   - `=== Slide N: ... ===` 형식
   - EXACT KOREAN TEXT 마지막에 반드시 🖼️ 이미지 생성 필수 조건 4가지 포함

## 🎨 이미지 생성 품질 기준

**Nano-Minimalist Standard** 준수:
- **포맷**: 16:9 가로
- **텍스트**: 압축적이고 간결하게 (구구절절 설명 금지)
- **비주얼**: 로봇 금지. 직관적인 인포그래픽, 아이콘, 다이어그램 사용
- **스타일**: 깔끔하고 전문적인 교육용 디자인

## � 참고 자료

- **`references/nano_minimalist_standard.md`**: 이미지 프롬프트 작성의 표준 가이드
- **`references/manual_workflow.md`**: 수동 작업 워크플로우 참고/