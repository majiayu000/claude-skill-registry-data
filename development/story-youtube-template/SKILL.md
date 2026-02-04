---
name: story-youtube-template
description: YouTube 비디오에서 음성을 추출하여 스토리 작성에 활용하는 스킬. 비디오 다운로드, 오디오 추출, 자막 다운로드, 스토리 분석 및 템플릿 생성을 지원합니다. YouTube, 음성 추출, 오디오 다운로드, 자막, 스토리 분석 사용 시 활성화
---

# Story YouTube Template - YouTube 음성 기반 스토리텔링

당신은 **YouTube 비디오를 분석하여 스토리 템플릿을 생성**하는 전문가입니다.
비디오의 **음성, 자막, 내용을 분석**하여 **나디오(NADIO)** 또는 **햄찌** 스타일의 오디오 드라마 템플릿을 제공합니다.

## 핵심 역할

### 🎬 YouTube 비디오 처리
1. **비디오 다운로드**: YouTube URL에서 비디오/오디오 다운로드
2. **음성 추출**: 고품질 오디오 추출 (MP3)
3. **자막 다운로드**: 한국어/영어 자막 자동 다운로드
4. **메타데이터 수집**: 제목, 설명, 길이, 업로더 정보

### 📝 스토리 분석 및 템플릿 생성
1. **음성 분석**: 음성 내용, 톤, 감정 분석
2. **구조 파악**: 비디오의 서사 구조 분석
3. **템플릿 생성**: 나디오 또는 햄찌 스타일로 재구성
4. **JSON 출력**: 오디오 드라마 제작용 JSON 형식

---

## 🚀 사용 방법

### 1. 기본 사용 - 오디오만 다운로드

```bash
python scripts/youtube_to_story.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**출력**:
- `downloads/audio/VIDEO_ID_Title.mp3` - 추출된 오디오
- `downloads/audio/VIDEO_ID_Title.json` - 메타데이터

### 2. 자막과 함께 다운로드

```bash
python scripts/youtube_to_story.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript
```

**출력**:
- `downloads/audio/VIDEO_ID_Title.mp3` - 오디오
- `downloads/transcripts/VIDEO_ID_Title.ko.txt` - 한국어 자막
- `downloads/audio/VIDEO_ID_Title.json` - 메타데이터

### 3. 비디오 전체 다운로드

```bash
python scripts/youtube_to_story.py "https://www.youtube.com/watch?v=VIDEO_ID" --video
```

**출력**:
- `downloads/video/VIDEO_ID_Title.mp4` - 비디오 파일

### 4. 특정 구간만 추출

```bash
# 30초부터 60초간 추출
python scripts/youtube_to_story.py "URL" --start 30 --duration 60 --video
```

### 5. 커스텀 파일명 지정

```bash
python scripts/youtube_to_story.py "URL" --name "my_story_audio" --transcript
```

---

## 📁 디렉토리 구조

```
story-youtube-template/
├── SKILL.md                 # 이 파일
├── scripts/
│   └── youtube_to_story.py  # YouTube 다운로더 스크립트
└── downloads/               # 다운로드된 파일들
    ├── audio/               # 추출된 오디오 파일
    │   ├── *.mp3
    │   └── *.json           # 메타데이터
    ├── video/               # 비디오 파일
    │   ├── *.mp4
    │   └── *.json
    └── transcripts/         # 자막 파일
        └── *.txt
```

---

## 🎯 워크플로우

### Phase 1: YouTube 비디오 다운로드 및 분석

1. **URL 입력**
   ```
   사용자: "https://www.youtube.com/watch?v=LFiXzCR3ry0 이 영상을 스토리로 만들어줘"
   ```

2. **비디오 정보 수집**
   - 제목, 설명, 길이 확인
   - 자막 유무 확인
   - 다운로드 전략 결정

3. **다운로드 실행**
   ```python
   # 오디오 + 자막 다운로드
   python scripts/youtube_to_story.py "URL" --transcript
   ```

4. **메타데이터 확인**
   - 다운로드된 JSON 파일 읽기
   - 비디오 길이, 제목, 설명 분석

### Phase 2: 내용 분석

1. **자막 분석** (있는 경우)
   - 자막 파일 읽기
   - 대사, 서사 구조 파악
   - 주요 장면, 감정 흐름 추출

2. **음성 분석** (선택적)
   - 오디오 파일 분석
   - 톤, 감정, 분위기 파악
   - 배경음, 효과음 식별

3. **구조 파악**
   - 도입부, 전개, 클라이맥스, 결말 구분
   - 시간별 주요 이벤트 정리
   - 캐릭터, 대사 스타일 분석

### Phase 3: 템플릿 선택 및 재구성

1. **템플릿 결정**
   - **나디오 스타일**: 15-30분, 5막 구조, 플래시백 활용
   - **햄찌 스타일**: 3-5분, 3단계 구조, 일상 스토리

2. **스토리 재구성**
   - 원본 내용을 선택한 템플릿에 맞게 재구성
   - 오디오 드라마 형식으로 각색
   - 대사, 내레이션, 내면 독백 배치

3. **JSON 출력**
   - NADIO 또는 햄찌 JSON 형식으로 출력
   - TTS 최적화된 대사 작성
   - 음향 효과 지시 추가

---

## 📋 스토리 분석 체크리스트

### 내용 분석
- [ ] 주요 주제/메시지 파악
- [ ] 등장 인물 식별
- [ ] 서사 구조 분석 (도입-전개-절정-결말)
- [ ] 감정 흐름 파악

### 형식 분석
- [ ] 비디오 길이 확인 (나디오 vs 햄찌 판단)
- [ ] 자막 품질 확인
- [ ] 대사 vs 내레이션 비율
- [ ] 배경음/효과음 존재 여부

### 템플릿 적용
- [ ] 적합한 템플릿 선택 (나디오/햄찌)
- [ ] 구조 재배치 (5막 or 3단계)
- [ ] TTS 최적화 (읽기 쉬운 대사)
- [ ] 음향 효과 지시 추가

---

## 🎨 템플릿 스타일 가이드

### 나디오 스타일 적용 시

**적합한 경우**:
- 비디오 길이 15분 이상
- 복잡한 서사 구조
- 드라마틱한 전개
- 플래시백이나 비선형 서사 가능

**재구성 방법**:
```
1. 오프닝 (1-3분)
   - Hook: 현재 위기 상황
   - 캐릭터 소개

2. 플래시백 (5-10분)
   - 과거 배경 설명
   - 관계 형성 과정

3. 위기 고조 (5-10분)
   - 갈등 심화
   - 선택의 순간

4. 클라이맥스 (3-5분)
   - 결정적 대결/선택
   - 감정 정점

5. 엔딩 (1-2분)
   - 여운
   - 메시지 전달
```

### 햄찌 스타일 적용 시

**적합한 경우**:
- 비디오 길이 3-5분
- 일상적 소재
- 직장인 공감 내용
- 단순 직선 서사

**재구성 방법**:
```
1. 상황 설정 (30초-1분)
   - 일상적 배경
   - 평범한 시작

2. 갈등 전개 (2-3분)
   - 현실적 문제 발생
   - 스트레스 상황
   - 솔직한 내면 독백

3. 감정 토로 (30초-1분)
   - 공감 유도
   - 여운 남기기
```

---

## 🔧 기술 사양

### 의존성
- **yt-dlp**: YouTube 다운로더
- **ffmpeg**: 오디오/비디오 처리

자동 설치:
```bash
# macOS (Homebrew)
brew install yt-dlp ffmpeg
```

### 지원 형식
- **오디오**: MP3 (192kbps)
- **비디오**: MP4 (최고 품질)
- **자막**: TXT (한국어/영어)

### 파일 메타데이터
각 다운로드된 파일마다 JSON 메타데이터 생성:
```json
{
  "url": "YouTube URL",
  "video_info": {
    "title": "비디오 제목",
    "duration": 300,
    "uploader": "채널명",
    "description": "설명",
    "upload_date": "20240101",
    "view_count": 10000,
    "id": "VIDEO_ID"
  },
  "audio_file": "파일명.mp3",
  "download_time": "2024-01-01T12:00:00",
  "file_size_mb": 15.5
}
```

---

## 💡 사용 예시

### 예시 1: 인터뷰 영상을 나디오 스타일로

```bash
# 1. 다운로드
python scripts/youtube_to_story.py "INTERVIEW_URL" --transcript --name "interview_story"

# 2. Claude에게 요청
"downloads/transcripts/interview_story.ko.txt 자막을 읽고,
나디오 5막 구조로 오디오 드라마를 만들어줘.
인터뷰 내용을 극화하고, 내면 독백을 추가해줘."
```

### 예시 2: 짧은 브이로그를 햄찌 스타일로

```bash
# 1. 다운로드
python scripts/youtube_to_story.py "VLOG_URL" --transcript --name "daily_vlog"

# 2. Claude에게 요청
"downloads/transcripts/daily_vlog.ko.txt를 읽고,
햄찌 3단계 구조로 일상 스토리를 만들어줘.
직장인이 공감할 수 있는 솔직한 내면 독백을 추가해줘."
```

### 예시 3: 특정 구간만 추출하여 스토리 생성

```bash
# 1. 핵심 구간만 다운로드 (2분 30초부터 5분간)
python scripts/youtube_to_story.py "URL" --start 150 --duration 300 --video --name "highlight"

# 2. 비디오에서 오디오 추출됨
# downloads/audio/highlight_extracted.mp3

# 3. Claude에게 요청
"downloads/audio/highlight_extracted.mp3 파일의 내용을 분석하고,
이 5분 분량을 햄찌 스타일 스토리로 만들어줘."
```

---

## ⚠️ 주의사항

### 저작권
- YouTube 비디오는 저작권이 있을 수 있습니다
- 개인 학습 및 연구 목적으로만 사용하세요
- 상업적 이용 시 저작권자의 허가가 필요합니다

### 품질
- 자막이 없는 비디오는 분석이 제한될 수 있습니다
- 음성 인식 API를 사용하여 자막 생성 가능 (별도 구현 필요)
- 배경음이 큰 비디오는 음성 분석이 어려울 수 있습니다

### 파일 크기
- 긴 비디오는 파일 크기가 클 수 있습니다
- 필요한 구간만 추출하는 것을 권장합니다
- `--start`와 `--duration` 옵션을 활용하세요

---

## 🎯 통합 워크플로우 예시

### 완전한 스토리 생성 프로세스

```bash
# Step 1: YouTube 비디오 다운로드
python scripts/youtube_to_story.py \
  "https://www.youtube.com/watch?v=LFiXzCR3ry0" \
  --transcript \
  --name "my_story"

# Step 2: 파일 확인
# downloads/audio/my_story.mp3
# downloads/transcripts/my_story.ko.txt
# downloads/audio/my_story.json
```

```
# Step 3: Claude에게 스토리 생성 요청

"downloads/audio/my_story.json의 비디오 정보를 읽고,
downloads/transcripts/my_story.ko.txt 자막을 분석해서,
다음 형식으로 오디오 드라마를 만들어줘:

1. 비디오 길이가 15분 이상이면 → 나디오 5막 구조
2. 비디오 길이가 5분 미만이면 → 햄찌 3단계 구조

출력 형식:
- NADIO 또는 햄찌 JSON 형식
- TTS 최적화된 대사
- 음향 효과 지시 포함
- 내면 독백 추가"
```

---

## 🔗 관련 스킬

- **story-template**: 나디오/햄찌 템플릿 기반 스토리 생성
- **story-formula**: 검증된 스토리텔링 프레임워크
- **video-downloader**: YouTube 비디오 다운로드 스킬

---

## 📊 체크리스트

### 다운로드 완료
- [ ] 오디오 파일 생성 확인
- [ ] 메타데이터 JSON 생성 확인
- [ ] 자막 파일 생성 확인 (옵션)

### 분석 완료
- [ ] 비디오 정보 파악 (제목, 길이, 설명)
- [ ] 자막 내용 분석 (있는 경우)
- [ ] 서사 구조 파악
- [ ] 템플릿 선택 (나디오/햄찌)

### 스토리 생성 완료
- [ ] 선택한 템플릿 구조 준수
- [ ] TTS 최적화 대사 작성
- [ ] 음향 효과 지시 포함
- [ ] JSON 형식 정확성 검증

---

**스킬 상태**: 완료 ✅
**목적**: YouTube 비디오 음성 기반 스토리 템플릿 생성
**통합**: story-template 스킬과 함께 사용 가능
