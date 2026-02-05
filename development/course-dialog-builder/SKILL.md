---
name: course-dialog-builder
description: Validates narration text, generates audio via ElevenLabs, and synchronizes timestamps.
version: 2.0.0
category: content-generation
---

# Course Dialog Builder

**핵심 기능**: 강의 대본(`refined.json`)의 발음을 교정하고, 오디오를 생성(또는 동기화)하여, 정확한 타임스탬프를 다시 JSON에 기록합니다.

## 🛠️ 3 Core Workflows

이 스킬은 다음 3가지 작업만 수행합니다. 복잡한 생각은 필요 없습니다.

### 1. 발화 검증 및 교정 (Text Validation)
`ref/tts_dictionary.json`에 정의된 규칙에 따라 기술 용어, 숫자, 기호 등을 성우가 읽기 편한 한글로 자동 변환합니다.

- **목적**: 오디오 생성 전 대본 품질 확보
- **입력**: `output/chX/lecture_X_Y_refined.json` (초안)
- **명령어**:
  ```bash
  python script/validate_tts_text.py <json_path> --fix
  ```
- **결과**: JSON 파일의 `content`가 발음 중심 텍스트로 수정됨 (`agent.py` → `에이전트 파이썬 파일`)

### 2. 오디오 생성 (New Generation)
검증된 대본으로 ElevenLabs TTS를 호출하여 오디오를 생성하고, **실제 측정된 시간**을 JSON에 기록합니다.

- **목적**: 최종 강의 오디오 생성
- **입력**: `output/chX/lecture_X_Y_refined.json` (검증됨)
- **명령어**:
  ```bash
  python script/generate_lecture_v3.py <json_path>
  ```
- **결과**:
  - `output/final/lecture_X_Y_complete.mp3` 생성
  - JSON 파일에 `timestamp_start`, `timestamp_end`, `duration_seconds` 자동 업데이트

### 3. 타임스탬프 동기화 (Sync Only)
**이미 오디오 파일이 있는 경우** (재생성 비용 절약), API 호출을 자동으로 건너뛰고 **길이만 다시 측정**하여 JSON 타임스탬프를 복구합니다.

- **목적**: 비용 없이 타임스탬프 메타데이터 갱신
- **입력**: `output/chX/lecture_X_Y_refined.json` + `temp_X_Y/` 폴더 내 기존 파일들
- **명령어** (위와 동일):
  ```bash
  python script/generate_lecture_v3.py <json_path>
  ```
- **동작**: "♻️ File exists, skipping API call" 메시지와 함께 측정 모드로 작동

---

## ⚙️ Configuration

### 발음 규칙 사전
모든 발음 규칙은 JSON 파일로 관리됩니다. 새로운 용어가 생기면 이 파일만 수정하세요.

- **경로**: `ref/tts_dictionary.json`
- **형식**:
  ```json
  {
    "simple_replacements": {
      "CLI": "커맨드라인 인터페이스",
      "agent.py": "에이전트 파이썬 파일"
    }
  }

### 성우 연기 지시 (Voice Direction)
ElevenLabs v3 모델을 사용하여 생동감 있는 오디오를 생성할 수 있습니다. `ref/elevenlabs_v3_audio_tags.md`에 정의된 태그를 지문에 적극적으로 활용하세요.

- **경로**: `ref/elevenlabs_v3_audio_tags.md`
- **사용법**:
  - `[sigh] 힘드네요...` (한숨)
  - `[excited] 정말 대단하지 않나요?` (흥분)
  - `[whispering] 이건 비밀인데요...` (속삭임)

  ```

### 환경 변수
`.env` 파일에 다음 설정이 필요합니다.
```bash
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_DIALOGUE_MODEL=eleven_v3
```

## 📋 Quick Checklist
1. **작성**: CLI 프롬프트로 `refined.json` 초안 생성
2. **검증**: `python script/validate_tts_text.py ... --fix`
3. **생성**: `python script/generate_lecture_v3.py ...`
4. **완료**: JSON에 타임스탬프가 들어갔는지 확인