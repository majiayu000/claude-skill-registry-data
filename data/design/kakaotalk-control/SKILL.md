---
name: kakaotalk-control
description: macOS 카카오톡 제어 skill. AppleScript GUI scripting으로 메시지 전송, 앱 활성화, 채팅방 검색 수행. 카카오톡 자동화, 메시지 보내기, 카톡 제어 관련 작업 시 사용.
---

# KakaoTalk Control Skill

macOS에서 AppleScript를 사용하여 카카오톡을 제어합니다.

## 사전 요구사항

### 접근성 권한 설정 (필수)
1. System Preferences > Security & Privacy > Privacy > Accessibility
2. Terminal (또는 사용 중인 터미널 앱) 추가
3. Claude Code 사용 시 해당 앱도 추가

## 기본 명령어

### 1. 카카오톡 실행/활성화

```bash
osascript -e 'tell application "KakaoTalk" to activate'
```

### 2. 메시지 전송 (현재 열린 채팅창)

한글 깨짐 방지를 위해 클립보드 활용:

```bash
# 메시지를 클립보드에 복사 후 붙여넣기
echo -n "보낼 메시지" | pbcopy && osascript -e '
tell application "KakaoTalk" to activate
delay 0.5
tell application "System Events"
    keystroke "v" using command down
    delay 0.2
    key code 36 -- Enter
end tell
'
```

### 3. 채팅방 검색 후 열기

```bash
# 채팅방 검색
CHAT_NAME="채팅방이름"
echo -n "$CHAT_NAME" | pbcopy && osascript -e '
tell application "KakaoTalk" to activate
delay 0.5
tell application "System Events"
    keystroke "f" using command down
    delay 0.3
    keystroke "v" using command down
    delay 0.5
    key code 36 -- Enter
end tell
'
```

### 4. 특정 채팅방에 메시지 전송 (통합)

```bash
CHAT_NAME="채팅방이름"
MESSAGE="보낼 메시지"

# 1. 채팅방 검색 및 열기
echo -n "$CHAT_NAME" | pbcopy && osascript -e '
tell application "KakaoTalk" to activate
delay 0.5
tell application "System Events"
    keystroke "f" using command down
    delay 0.3
    keystroke "v" using command down
    delay 0.5
    key code 36
    delay 0.5
end tell
'

# 2. 메시지 전송
echo -n "$MESSAGE" | pbcopy && osascript -e '
tell application "System Events"
    keystroke "v" using command down
    delay 0.2
    key code 36
end tell
'
```

### 5. 카카오톡 창 닫기

```bash
osascript -e 'tell application "KakaoTalk" to quit'
```

## 유용한 키보드 단축키

| 단축키 | 기능 | Key Code |
|--------|------|----------|
| Cmd+F | 채팅방 검색 | - |
| Cmd+N | 새 채팅 | - |
| Enter | 메시지 전송 | 36 |
| Escape | 취소/닫기 | 53 |
| Cmd+W | 현재 창 닫기 | - |

## 주의사항

1. **창 구분 불가**: 여러 채팅창이 하나의 윈도우로 인식됨
2. **화면 잠금**: 노트북 잠금 상태에서 동작 안함
3. **타이밍**: delay 값은 시스템 속도에 따라 조정 필요
4. **한글 입력**: 반드시 클립보드(pbcopy) 방식 사용

## 디버깅

### UI 요소 확인
```bash
osascript -e '
tell application "System Events"
    tell process "KakaoTalk"
        get entire contents of window 1
    end tell
end tell
'
```

### 현재 창 정보
```bash
osascript -e '
tell application "System Events"
    tell process "KakaoTalk"
        get properties of window 1
    end tell
end tell
'
```

---

## 기능 확장 가이드

이 skill에 새로운 기능이 필요하면 아래 절차를 따릅니다:

### 새 기능 추가 방법

1. 이 파일(`.claude/skills/kakaotalk-control/SKILL.md`)을 직접 수정
2. "기본 명령어" 섹션에 새 기능 추가
3. 필요시 bash 스크립트나 AppleScript 코드 포함

### 추가 가능한 기능 예시

- 읽지 않은 메시지 확인
- 특정 시간에 메시지 예약 전송
- 여러 채팅방에 동시 메시지 전송
- 채팅방 목록 가져오기

### AppleScript 참고 문법

```applescript
-- 클릭
click button "버튼이름" of window 1

-- 텍스트 필드 입력
set value of text field 1 of window 1 to "텍스트"

-- 메뉴 선택
click menu item "항목" of menu "메뉴" of menu bar 1

-- 조건부 실행
if exists button "확인" of window 1 then
    click button "확인" of window 1
end if
```

### 주의: 이 skill 수정 시

- YAML frontmatter의 `name`과 `description`은 유지
- 새 기능은 "기본 명령어" 섹션에 번호 순서대로 추가
- 테스트 후 동작 확인된 코드만 포함
