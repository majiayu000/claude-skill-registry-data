---
name: audio-processor
description: ffmpeg 기반 오디오 변환 및 처리. "오디오 변환", "wav 변환", "샘플레이트 변경", "모노 변환", "세그먼트 분할", "ffmpeg" 요청 시 활성화됩니다.
---

# Audio Processor 스킬

## Overview

ffmpeg을 활용한 오디오 파일 변환 및 처리 자동화 스킬입니다.

**중요**: 이 스킬이 활성화되면 Claude가 자동으로 스크립트를 실행합니다. 사용자가 직접 명령어를 입력할 필요가 없습니다.

**핵심 기능:**
- **포맷 변환**: wav, m4a, opus, mp3 등 상호 변환
- **샘플레이트 변환**: 8kHz, 16kHz, 22.05kHz, 44.1kHz, 48kHz
- **채널 변환**: 스테레오 → 모노, 모노 → 스테레오
- **세그먼트 분할**: 고정 시간 또는 타임스탬프 기반 분할
- **배치 처리**: 디렉토리 내 여러 파일 일괄 처리

## Script Location

```
SCRIPT: ./scripts/audio-process.sh
```

Claude는 이 스크립트를 Bash 도구로 직접 실행합니다.

## When to Use

이 스킬은 다음 상황에서 활성화됩니다:

**명시적 요청:**
- "오디오 변환해줘", "wav로 바꿔줘"
- "샘플레이트 16kHz로 변경해줘"
- "모노로 변환해줘"
- "10초 단위로 분할해줘"
- "ffmpeg으로 처리해줘"

**자동 활성화:**
- 오디오 파일 처리 요청 시 (.wav, .mp3, .m4a, .opus 등)
- 음성 데이터 전처리 요청 시

## Prerequisites

```bash
# ffmpeg 설치 확인
ffmpeg -version

# 스크립트 실행 권한
chmod +x /path/to/agent-skills/ml/audio-processor/scripts/audio-process.sh
```

## Workflow

### Claude 실행 절차

**Step 1**: 사용자 요청 분석
- 입력 파일 경로 확인
- 원하는 변환 유형 파악 (포맷/샘플레이트/채널/분할)
- 출력 경로 결정 (명시되지 않으면 입력 파일과 같은 디렉토리)

**Step 2**: 스크립트 실행
```bash
# 스크립트 경로
SCRIPT=./scripts/audio-process.sh

# 포맷 변환
$SCRIPT convert <input> <output> [--sr <rate>] [--mono|--stereo]

# 세그먼트 분할
$SCRIPT segment <input> <output_dir> --duration <sec>

# 배치 변환
$SCRIPT batch <input_dir> <output_dir> --format <fmt> [--sr <rate>] [--mono]

# 파일 정보 조회
$SCRIPT info <file>
```

**Step 3**: 결과 보고
- 스크립트 출력을 사용자에게 전달
- 변환 성공/실패 여부 확인

### 명령어 레퍼런스

| 작업 | 명령어 |
|------|--------|
| 포맷 변환 | `$SCRIPT convert in.mp3 out.wav` |
| 16kHz mono 변환 | `$SCRIPT convert in.mp3 out.wav --sr 16000 --mono` |
| 8kHz 전화 품질 | `$SCRIPT convert in.mp3 out.wav --sr 8000 --mono` |
| 10초 분할 | `$SCRIPT segment in.wav segs/ --duration 10` |
| 배치 처리 | `$SCRIPT batch raw/ out/ --format wav --sr 16000 --mono` |
| 정보 조회 | `$SCRIPT info file.wav` |

### 자주 사용하는 변환 조합

| 용도 | 명령어 |
|------|--------|
| ML 학습용 (16kHz mono) | `audio-process.sh convert in.mp3 out.wav --sr 16000 --mono` |
| 전화 품질 (8kHz mono) | `audio-process.sh convert in.mp3 out.wav --sr 8000 --mono` |
| 고품질 (48kHz stereo) | `audio-process.sh convert in.mp3 out.wav --sr 48000` |
| 10초 청크 분할 | `audio-process.sh segment in.wav out/ --duration 10` |

---

## Examples

### 예시 1: 기본 포맷 변환

```
사용자: test.mp3를 wav로 변환해줘

Claude: 오디오 변환을 수행합니다.

$ audio-process.sh convert test.mp3 test.wav

✅ 변환 완료
- 입력: test.mp3 (44.1kHz, stereo, 3:25)
- 출력: test.wav (44.1kHz, stereo, 3:25)
```

### 예시 2: ML 전처리 (16kHz mono)

```
사용자: 이 오디오 파일을 음성인식 모델용으로 변환해줘

Claude: ML 학습에 적합한 형식으로 변환합니다.

$ audio-process.sh convert input.m4a output.wav --sr 16000 --mono

✅ 변환 완료
- 입력: input.m4a (48kHz, stereo, 5:30)
- 출력: output.wav (16kHz, mono, 5:30)
- 파일 크기: 48MB → 10.5MB
```

### 예시 3: 세그먼트 분할

```
사용자: 긴 오디오를 10초 단위로 나눠줘

Claude: 10초 단위로 세그먼트를 분할합니다.

$ audio-process.sh segment long_audio.wav segments/ --duration 10

✅ 분할 완료
- 입력: long_audio.wav (2:30)
- 출력: 15개 세그먼트
  - segments/seg_000.wav (10s)
  - segments/seg_001.wav (10s)
  ...
  - segments/seg_014.wav (10s)
```

### 예시 4: 배치 처리

```
사용자: recordings 폴더의 모든 mp3를 16kHz mono wav로 변환해줘

Claude: 배치 변환을 수행합니다.

$ audio-process.sh batch recordings/ converted/ --format wav --sr 16000 --mono

✅ 배치 변환 완료
- 처리: 25개 파일
- 성공: 25개
- 출력 디렉토리: converted/
```

---

## Configuration

### 기본값 설정

스크립트 상단에서 기본값 수정 가능:

```bash
DEFAULT_SAMPLE_RATE=16000
DEFAULT_CHANNELS=1  # mono
DEFAULT_FORMAT="wav"
DEFAULT_SEGMENT_DURATION=10
```

### 출력 포맷별 권장 설정

| 포맷 | 코덱 | 품질 옵션 |
|------|------|-----------|
| wav | pcm_s16le | (무손실) |
| mp3 | libmp3lame | -b:a 192k |
| opus | libopus | -b:a 128k |
| m4a | aac | -b:a 192k |

---

## Best Practices

**DO:**
- 변환 전 `info` 명령으로 원본 파일 확인
- ML용 오디오는 16kHz mono PCM 사용
- 배치 처리 시 출력 디렉토리 미리 확인
- 긴 파일 분할 시 적절한 세그먼트 길이 선택

**DON'T:**
- 손실 포맷(mp3, opus)으로 여러 번 재인코딩
- 업샘플링으로 품질 향상 기대 (8kHz → 48kHz)
- 원본 파일 덮어쓰기 (항상 새 파일로 출력)

---

## Troubleshooting

### ffmpeg not found

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### 코덱 지원 안됨

```bash
# 지원 코덱 확인
ffmpeg -codecs | grep -i opus

# 코덱 설치 (Ubuntu)
sudo apt install libopus-dev
```

### 메모리 부족 (대용량 파일)

```bash
# 스트리밍 모드 사용
audio-process.sh convert large.wav output.wav --streaming
```

---

## Resources

| 파일 | 설명 |
|------|------|
| `scripts/audio-process.sh` | 오디오 처리 통합 스크립트 |
