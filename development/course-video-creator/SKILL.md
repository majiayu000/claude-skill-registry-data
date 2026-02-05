---
name: course-video-creator
description: Generate educational videos from course audio and slide images using timestamp-based synchronization
category: media
trigger:
  keywords: ["course video", "교육 영상", "lecture video", "course creation", "video generation"]
---

# Course Video Creator

슬라이드 이미지와 강의 오디오를 타임스탬프 기반으로 결합하여 교육 영상을 자동 생성하는 스킬입니다.

## Features

- **Timestamp-Based Sync**: lecture_X_Y_refined.json의 타임스탬프 기반 정확한 동기화
- **Automatic Mapping**: segment_id와 이미지 파일 1:1 자동 매핑
- **Video Creation**: 슬라이드 타이밍에 맞춰 이미지와 오디오를 결합한 16:9 영상 생성

## 🎓 NADIO Course Production Pipeline

```
📝 course-builder (기획)
   ↓ visual_concept
🎙️ course-dialog-builder (오디오 + 타임스탬프)
   ↓ lecture_X_Y_complete.mp3 + lecture_X_Y_refined.json ⭐ (with timestamps)
🖼️ course-resource-creator (이미지 생성)
   ↓ slide_*.png (segment_0.png ~ segment_N.png)
🎬 course-video-creator (타임스탬프 기반 조립) ← YOU ARE HERE
   ↓ lecture_X_Y_auto.mp4
📤 course-inflearn-uploader (업로드)
```

### 역할과 출력물

- **Position**: Step 4/5 in NADIO Pipeline
- **Input** (필수 읽기 순서):
  1. **`course-dialog-builder/output/ch{N}/lecture_X_Y_refined.json`** ⭐ (source of truth with timestamps)
     - 각 segment_id의 정확한 content (오디오 대본)
     - **타임스탬프 자동 포함**: `timestamp_start`, `timestamp_end`, `duration_seconds`
  2. **`course-dialog-builder/output/final/lecture_X_Y_complete.mp3`**
     - 실제 오디오 파일
  3. **`course-resource-creator/output/lecture_X_Y/images/`**
     - 슬라이드 이미지 파일들 (segment_0.png ~ segment_N.png)
- **Process**: **lecture_X_Y_refined.json의 타임스탬프** 기반 정확한 슬라이드-오디오 동기화
- **Output**: `output/videos/lecture_X_Y_auto.mp4` (16:9, 1080p)
- **Next Step**: → `course-inflearn-uploader` (인프런 업로드)

### 🎯 타임스탬프 기반 동기화 (Simplified Architecture)

이 스킬은 **lecture_X_Y_refined.json의 자동 생성된 타임스탬프**를 사용하여 슬라이드와 오디오를 정확히 동기화합니다.

#### 타임스탬프 자동 매핑

**자동 처리 과정**:
1. `course-dialog-builder`가 TTS 생성 시 각 세그먼트의 타임스탬프를 자동 계산
2. `lecture_X_Y_refined.json`에 `timestamp_start`, `timestamp_end`, `duration_seconds` 자동 저장
3. `course-video-creator`가 이 타임스탬프를 직접 사용하여 비디오 생성

**필수 참조 파일**:
1. **`course-dialog-builder/output/ch{N}/lecture_{X}_{Y}_refined.json`** ← **기본 참조 (최우선)**
   - 각 segment_id의 정확한 content (오디오 대본)
   - **타임스탬프 자동 포함**: `timestamp_start`, `timestamp_end`, `duration_seconds`
   - segment_id 0-N의 순차적 정의

2. **`course-resource-creator/output/lecture_{X}_{Y}/images/`**
   - 실제 생성된 이미지 파일 목록 (segment_0.png ~ segment_N.png)
   - **세그먼트 ID와 1:1 매핑** (segment_0.png ↔ segment_id 0)

**간단한 매핑 규칙**:
- `segment_id: 0` → `segment_0.png` (`timestamp_start` ~ `timestamp_end`)
- `segment_id: 1` → `segment_1.png` (`timestamp_start` ~ `timestamp_end`)
- `segment_id: N` → `segment_N.png` (`timestamp_start` ~ `timestamp_end`)

**예시**:
```json
{
  "segment_id": 0,
  "timestamp_start": "00:00:00",
  "timestamp_end": "00:00:13",
  "duration_seconds": 13.166
}
```
→ `segment_0.png`를 0초부터 13.166초까지 표시

#### 비디오 생성 워크플로우

**간단한 3단계 프로세스**:

1. **lecture_X_Y_refined.json 읽기**
   ```python
   with open('lecture_1_2_refined.json') as f:
       data = json.load(f)

   for segment in data['segments']:
       segment_id = segment['segment_id']
       start_time = segment['timestamp_start']  # "00:00:00"
       end_time = segment['timestamp_end']      # "00:00:13"
       duration = segment['duration_seconds']   # 13.166
   ```

2. **대응하는 이미지 파일 찾기**
   ```python
   image_file = f"segment_{segment_id}.png"  # segment_0.png
   ```

3. **ffmpeg로 비디오 생성**
   ```bash
   ffmpeg -loop 1 -t {duration} -i {image_file} \
          -ss {start_time} -t {duration} -i {audio_file} \
          -c:v libx264 -c:a aac -shortest {output}
   ```

**전체 예시 (lecture_1_2)**:
```
segment_0.png → 00:00:00 ~ 00:00:13 (13.2초)
segment_1.png → 00:00:13 ~ 00:00:46 (33.7초)
segment_2.png → 00:00:46 ~ 00:01:09 (22.6초)
...
segment_6.png → 00:02:36 ~ 00:03:03 (26.9초)
```

**장점**:
- ✅ 세그먼트와 이미지 1:1 매핑으로 단순화
- ✅ 100% 정확한 타이밍 (refined.json 타임스탬프 사용)

## 빠른 시작

```bash
# 1. 환경 확인
ls course-dialog-builder/output/ch1/lecture_1_2_refined.json  # 타임스탬프 포함 레시피
ls course-resource-creator/output/lecture_1_2/images/segment_*.png  # 이미지 확인
ls course-dialog-builder/output/final/lecture_1_2_complete.mp3  # 오디오 확인

# 2. 비디오 생성
python script/orchestrate_pipeline.py \
  --refined-json course-dialog-builder/output/ch1/lecture_1_2_refined.json \
  --audio course-dialog-builder/output/final/lecture_1_2_complete.mp3 \
  --images course-resource-creator/output/lecture_1_2/images/ \
  --output output/videos/lecture_1_2_auto.mp4
```

## 파이프라인 통합

이 스킬은 이전 2개 스킬의 출력물을 결합하여 최종 비디오를 생성합니다.

### 필수 입력 파일 (3개)

1. **세그먼트 레시피 + 타임스탬프** (`course-dialog-builder`)
   - 경로: `course-dialog-builder/output/ch{N}/lecture_X_Y_refined.json`
   - 내용: segments with `timestamp_start`, `timestamp_end`, `duration_seconds`
   - 용도: 정확한 타이밍 정보 (source of truth)

2. **강의 오디오** (`course-dialog-builder`)
   - 경로: `course-dialog-builder/output/final/lecture_X_Y_complete.mp3`
   - 용도: 최종 비디오의 오디오 트랙

3. **슬라이드 이미지** (`course-resource-creator`)
   - 경로: `course-resource-creator/output/lecture_X_Y/images/segment_*.png`
   - 개수: N개 (세그먼트 개수와 동일)
   - 형식: 16:9 가로 이미지 (1920x1080 or 1280x720)

## Prerequisites

### System Dependencies
```bash
# FFmpeg (video/audio processing)
brew install ffmpeg  # macOS
```

### Python Packages
```bash
pip install python-dotenv
```

## Credits

Simplified from complex semantic matching architecture to straightforward timestamp-based synchronization.
