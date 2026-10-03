---
name: youtube-transcript
description: YouTube 영상 자막을 추출하고 요약합니다. yt-dlp 기반으로 MCP 없이 로컬에서 안정적으로 동작합니다. /youtube-transcript 또는 "이 영상 자막 가져와"로 실행.
---

# YouTube Transcript

> YouTube 영상의 자막을 추출하고 분석합니다. yt-dlp 기반, MCP 불필요.

## Quick Start

```
/youtube-transcript https://www.youtube.com/watch?v=VIDEO_ID
"이 영상 자막 가져와: https://youtu.be/VIDEO_ID"
"이 영상 요약해줘: https://www.youtube.com/watch?v=VIDEO_ID"
```

## Prerequisites

- `yt-dlp` 설치 필요
  - Windows: `pip install yt-dlp` 또는 `winget install yt-dlp`
  - Mac: `brew install yt-dlp`
  - Linux: `pip install yt-dlp`

## Workflow

### 1. URL 추출

`$ARGUMENTS` 또는 사용자 메시지에서 YouTube URL을 추출합니다.

지원 형식:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `VIDEO_ID` (11자리 영숫자)

### 2. yt-dlp 설치 확인 + 자동 설치

```bash
yt-dlp --version
```

미설치 시 **자동 설치** (pip 사용 가능하면):

```bash
pip install yt-dlp
```

pip도 없으면 플랫폼별 안내:
- Windows: `winget install yt-dlp`
- Mac: `brew install yt-dlp`
- Linux: `sudo apt install yt-dlp` 또는 `pip install yt-dlp`

설치 후 다시 `yt-dlp --version`으로 확인하고 진행.

### 3. 자막 언어 확인

```bash
yt-dlp --list-subs "URL" 2>&1 | head -5
```

- 수동 자막(manual)이 있으면 우선 사용
- 없으면 자동 생성 자막(auto-generated) 사용
- 사용자가 언어를 지정하지 않으면 영어(en) → 한국어(ko) 순으로 시도

### 4. 자막 다운로드

```bash
# 임시 파일로 다운로드
yt-dlp --write-auto-sub --sub-lang {LANG} --sub-format srt --skip-download \
  -o "/tmp/yt-transcript-%(id)s" "URL"
```

Windows의 경우:
```bash
yt-dlp --write-auto-sub --sub-lang {LANG} --sub-format srt --skip-download \
  -o "$TEMP/yt-transcript-%(id)s" "URL"
```

### 5. 자막 읽기 + 정리

다운로드된 `.srt` 파일을 Read로 읽고, 타임스탬프를 제거하여 순수 텍스트로 정리합니다.

SRT 형식:
```
1
00:00:00,160 --> 00:00:04,799
This is the subtitle text

2
00:00:02,560 --> 00:00:07,040
Next subtitle line
```

정리 후:
```
This is the subtitle text. Next subtitle line...
```

### 6. 결과 제공

사용자 요청에 따라:

| 요청 | 응답 |
|------|------|
| "자막 가져와" | 정리된 전체 자막 텍스트 출력 |
| "요약해줘" | 자막 기반 핵심 내용 요약 (한국어) |
| "번역해줘" | 자막을 한국어로 번역 |
| 특정 질문 | 자막 내용에서 답변 추출 |

### 7. 임시 파일 정리

```bash
rm -f /tmp/yt-transcript-*.srt 2>/dev/null
# Windows
del "%TEMP%\yt-transcript-*.srt" 2>nul
```

## Options

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--lang XX` | 자막 언어 코드 (en, ko, ja 등) | en |
| `--summary` | 자막 추출 후 자동 요약 | false |
| `--raw` | SRT 타임스탬프 포함 원본 출력 | false |

## Error Handling

| 에러 | 대응 |
|------|------|
| yt-dlp 미설치 | 설치 명령어 안내 |
| 영상 없음 / 비공개 | "영상을 찾을 수 없습니다" |
| 자막 없음 | "이 영상에는 자막이 없습니다" |
| 네트워크 오류 | 1회 재시도 후 실패 보고 |
