---
name: video-subtitle-dl
description: >
  영상 URL에서 한국어 자막을 다운로드하거나, 영어 자막을 받아 한국어로 번역하는 스킬.
  수동 자막과 자동 생성 자막을 우선순위에 따라 자동 선택한다.
  "자막 다운로드", "자막 뽑아줘", "영상 스크립트 뽑아줘",
  "자막 번역해줘", "이 영상 자막 한국어로", "영상 번역",
  "CC 자막 뽑아줘", "영상 URL 자막", "유튜브 자막 가져와",
  "비디오 자막", "영상 링크 자막" 등에서 트리거.
  YouTube, Vimeo 등 yt-dlp 지원 플랫폼 대응.
---

# Video Subtitle Download & Translate

영상 URL에서 한국어 자막을 확보한다. 한국어 자막이 있으면 바로 다운로드, 없으면 영어 자막을 받아 번역한다.

## 사전 조건

`yt-dlp`가 필요하다. 먼저 존재 여부를 확인한다:

```bash
command -v yt-dlp
```

없으면 설치를 안내한다:

```bash
# macOS
brew install yt-dlp

# pip
pip install yt-dlp
```

## 실행 절차

### 1. URL 수신 및 자막 다운로드

사용자로부터 영상 URL을 받는다. `scripts/fetch-subs.sh`로 자막 조회와 우선순위 다운로드를 한 번에 수행:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/video-subtitle-dl/scripts/fetch-subs.sh" "<URL>"
```

인증이 필요한 경우 추가 옵션 전달:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/video-subtitle-dl/scripts/fetch-subs.sh" "<URL>" --cookies-from-browser chrome
```

`CLAUDE_PLUGIN_ROOT`가 없는 환경에서는 스킬 디렉토리의 절대 경로를 직접 사용한다.

스크립트 출력의 `RESULT:` 라인으로 다음 단계를 판단한다:
- `ko_manual` / `ko_auto` → Step 4 (포맷 변환 및 저장)
- `en_manual_needs_translation` / `en_auto_needs_translation` → Step 3 (번역)
- `none` → Step 5 (자막 없음)

**스크립트 실행 불가 시 수동 절차:**

자막 목록 확인: `yt-dlp --list-subs --skip-download "<URL>"`

우선순위: ko 수동 > ko 자동 > en 수동 > en 자동

| 순위 | 조건 | 액션 | 다음 단계 |
|------|------|------|-----------|
| 1 | 한국어 수동 자막 있음 | `--write-subs --sub-langs ko --convert-subs srt` | → Step 4 (포맷 변환) |
| 2 | 한국어 자동 자막 있음 | `--write-auto-subs --sub-langs ko --convert-subs srt` | → Step 4 (포맷 변환) |
| 3 | 영어 수동 자막 있음 | `--write-subs --sub-langs en` | → Step 3 (번역) |
| 4 | 영어 자동 자막 있음 | `--write-auto-subs --sub-langs en` | → Step 3 (번역) |
| 5 | 둘 다 없음 | — | → Step 5 (자막 없음) |

### 2. 다운로드 실패 시

`yt-dlp`가 실패하면 인증 옵션을 안내한다. 상세는 `references/yt-dlp-options.md` 참조.

사용자에게 선택지 제시:
1. **브라우저 쿠키 사용** — `--cookies-from-browser chrome`
2. **쿠키 파일 지정** — `--cookies cookies.txt`
3. **계정 로그인** — `--username` / `--password`

사용자가 선택하면 해당 옵션을 추가하여 재시도.

### 3. 번역 (영어 → 한국어)

**한국어 자막을 직접 받은 경우 이 단계를 건너뛴다.**

다운로드된 영어 자막 파일을 읽고 한국어로 번역한다. 상세 규칙은 `references/translation-guide.md` 참조.

핵심 규칙:
- **타임코드는 절대 수정하지 않는다.** 텍스트만 번역.
- 기술 용어, 고유명사, 브랜드명은 원문 유지.
- 자연스러운 구어체로 번역. 직역 금지.

번역 절차:
1. 원본 자막 파일을 Read로 읽는다
2. 500 cue 이하: 한 번에 번역
3. 500 cue 초과: 200-300 cue 단위로 청크 분할하여 번역
4. 번역된 내용을 새 파일로 저장

### 4. 포맷 변환 및 저장

**파일명 규칙:**
- 원본(영어): `{영상제목}.en.{vtt|srt}` — 스크립트가 `vtt/srt/best` 순으로 받으므로 포맷이 다를 수 있다. `ls *.srt *.vtt`로 실제 파일명 확인.
- 번역본: `{영상제목}.ko.srt` (예: `codex-for-software-engineers.ko.srt`)
- 한국어 자막 직접 다운로드: `{영상제목}.ko.srt` — Step 1에서 `--convert-subs srt`로 이미 SRT이므로 추가 변환 불필요.
- 영상 제목은 `yt-dlp`가 생성한 파일명 기반. 특수문자 제거, 공백은 하이픈.

**SRT 변환 (번역 경로만 해당):** 영어 자막을 번역한 경우, `references/translation-guide.md`의 "VTT → SRT 변환 규칙"에 따라 변환.

**저장 위치:** 현재 작업 디렉토리 (`$PWD`)

### 5. 완료 / 자막 없음

**자막을 확보한 경우:**
- 저장된 파일 경로 (원본 + 번역본, 또는 한국어 자막만)
- 자막 cue 수

**자막이 없는 경우:**
- "이 영상에는 사용 가능한 자막(한국어/영어)이 없습니다." 출력 후 종료

## Gotchas

- 자동 생성 자막(auto-sub)은 타임코드가 1-2초 단위로 과도하게 쪼개져 있다. 번역 시 인접 cue를 문맥 단위로 묶어 읽어야 자연스러운 번역이 된다.
- VTT→SRT 변환 후 `<c>`, `<font>` 등 VTT 전용 태그가 잔존할 수 있다. 변환 후 `grep '<[a-z]' *.srt`로 확인하고 VTT 전용 태그는 제거. `<b>`, `<i>`는 SRT에서도 지원하므로 유지.
- 연령 제한/멤버십 전용 영상은 `--cookies-from-browser`로도 실패할 수 있다. 이 경우 브라우저에서 수동 export한 cookies.txt 파일이 더 안정적.
- `%(title)s`에 `/`, `?`, `"` 등 파일시스템 금지 문자가 포함되면 yt-dlp가 자동 치환하지만, 후속 파일 참조 시 실제 생성된 파일명을 `ls *.srt *.vtt`로 확인할 것.
- 일부 플랫폼(Vimeo, Naver TV 등)은 자막 포맷이 비표준이라 `--convert-subs srt`가 실패할 수 있다. 이때는 원본 포맷 그대로 저장 후 수동 변환.
