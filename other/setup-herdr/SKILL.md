---
name: setup-herdr
description: >
  완성된 herdr `config.toml`을 다른 머신으로 이식하고 그 버전·플랫폼에서 실제 수락됐는지 검증하는 스킬.
  OS별 config 경로, byte-exact 전송, `config check` 3단 진단, remote attach의 키 소유권,
  플랫폼별 prefix 함정을 다룬다.
  "herdr 설정 이식", "herdr 설정 복사해줘", "herdr 새 머신에 셋업", "herdr prefix 바꿔줘",
  "윈도우에 herdr 설정 적용", "herdr 단축키 안 먹어", "herdr config check",
  "setup herdr", "port herdr config", "herdr prefix not working" 등에서 트리거.
---

# setup-herdr

이미 완성된 herdr `config.toml`을 다른 머신으로 옮기고, 대상 버전·플랫폼에서 전 키가 실제로 수락됐는지 확인한다.

herdr 사용법과 pane·workspace 제어는 이 스킬의 대상이 아니다. `herdr --skill`과 herdr.dev 문서가 담당한다.

## 원본과 대상 확정

원본은 항상 **기존 머신의 `config.toml`**이다. 이 스킬에 정본 config를 두지 않는다. 키맵은 사용자마다 다르고, 복사본을 스킬에 박아두면 원본이 바뀌는 순간 drift한다.

config 경로는 OS마다 다르다. 추측하지 말고 대상 머신에서 `herdr --help`의 마지막 `Config:` 줄을 읽는다. 기준값은 Linux·macOS가 `~/.config/herdr/config.toml`, Windows가 `%APPDATA%\herdr\config.toml`이다. 로그도 같은 디렉토리에 있고 named session 로그는 그 아래 `sessions/<name>/`이다.

양쪽 `herdr --version`을 먼저 기록한다. 버전이 다르면 이식 후 진단이 필수다.

## 전송은 byte-exact로

`scp` 또는 `rsync`로 파일 자체를 옮긴다.

셸 리다이렉트로 내용을 흘려보내면 인코딩이 바뀐다. PowerShell 5.1의 `Set-Content -Encoding utf8`은 BOM을 붙이고 `Out-File`은 기본이 UTF-16LE다. TOML 파서는 BOM과 UTF-16을 문법 오류로 읽고 **설정 전체를 기본값으로 폴백**시킨다. 프리픽스가 그대로인 채 조용히 넘어가는 실패다.

덮어쓰기 전에 대상의 기존 파일을 `config.toml.bak-<timestamp>`로 남긴다.

## 검증: config check 한 줄이 3단 진단이다

```
herdr config check
```

| 출력 | 의미 |
|------|------|
| `config parse error ... using defaults` | TOML 문법 오류 또는 중복 테이블. 설정 전체가 기본값으로 폴백한 상태 |
| `unknown config key X; ignoring key` | 그 키만 대상 버전이 모른다. 버전 차이 지점 |
| `config: ok` | 전 키가 이 버전에서 실제 수락됨 |

따라서 상위 버전 설정을 하위 버전 머신에 넣는 이식도 이 한 줄로 판정이 끝난다. 키를 하나씩 대조할 필요가 없다.

적용은 로컬 서버라면 `herdr server reload-config`로 재시작 없이 끝난다. 응답의 `diagnostics`가 비어야 수락된 것이다. 시작 시점에만 읽는 항목은 재시작이 필요하다.

## remote attach는 예외 — 키는 클라이언트가 소유한다

`herdr --remote <host>`는 로컬 herdr가 thin client로 붙는 구조이고, **키 처리는 기본이 로컬**이다. `--remote-keybindings local|server` CLI 플래그로만 바뀌며 대응하는 config 키는 없다.

- prefix를 바꾸려면 **클라이언트 머신**의 config를 고쳐야 한다. 서버에서 `reload-config`를 해도 remote 클라이언트의 프리픽스는 그대로다.
- 클라이언트는 시작 시점에 config를 읽는다. detach 후 재접속해야 반영된다. 설정 전 기본 detach는 `ctrl+b q`다.
- config를 안 옮기는 대안은 `herdr --remote <host> --remote-keybindings server`다. 서버 키맵을 그대로 쓰므로 클라이언트에 파일을 둘 필요가 없다. 대신 그 머신의 로컬 herdr 세션은 여전히 기본 키맵이다.
- UI는 소유권이 반대다. 서버가 렌더해서 스트리밍하므로 `[ui]`·`[theme]`은 서버 config가 지배한다. 클라이언트 config에서 유효한 것은 `[keys]`와 로컬 IME 동작이다.

## 플랫폼 함정

- **Linux·WSL tty**: Ctrl-S는 XON/XOFF flow control로 소비되어 앱까지 오지 않는다. prefix `ctrl+s`를 쓰려면 shell rc에 `stty -ixon`이 있어야 한다.
- **한글 IME**: `[experimental] switch_ascii_input_source_in_prefix`는 prefix 모드 동안 ASCII 입력으로 임시 전환한다. macOS는 ASCII 키보드 레이아웃으로, Windows는 IME를 영문으로 바꾸고 **Windows 지원은 한국어 IME 전용**이다. 그 외 플랫폼에서는 unknown key 경고 없이 no-op이므로 config 한 벌을 그대로 공유해도 된다.
- **Windows remote attach**: `[remote] manage_ssh_config`의 연결 재사용(OpenSSH control socket)은 Linux·macOS 클라이언트만 쓴다. Windows OpenSSH는 attach마다 재인증한다.
- 키가 아무 동작도 안 하면 herdr가 아니라 바깥 터미널이나 데스크톱 환경이 그 chord를 먹은 경우다. herdr config보다 터미널 키맵을 먼저 본다.

## config 편집 함정

- 키 이름 파서는 named punctuation을 `minus`, `comma`, `ampersand`, `plus`, `backtick`만 수락한다. `pipe`·`underscore`는 거부되고 리터럴 `|`·`_`·`;`·`&`는 그대로 쓸 수 있다.
- 새 서브테이블 삽입 위치를 조심한다. TOML은 테이블 헤더 뒤의 bare key를 그 테이블에 귀속시키므로, `[ui]`의 bare key들 **앞**에 `[ui.sidebar.*]`를 넣으면 그 키들이 서브테이블로 흡수되어 조용히 동작이 바뀐다. 서브테이블은 해당 섹션 bare key 전부 뒤에 붙인다.
- `prefix+` 없는 plain printable key는 입력 자체를 가로챈다. plain key는 navigate-mode 전용 필드에만 쓴다.
- 커스텀 키맵을 버리고 기본값으로 돌아갈 때는 `herdr config reset-keys`를 쓴다. herdr가 백업을 만들고 `[keys]`·`[[keys.command]]`를 제거한다.

## 선택: 사이드바에 작업 디렉토리 노출

workspace label은 생성 시점 cwd로 굳고, 사이드바 행 토큰에 `cwd`가 없다. 경로를 띄우는 경로는 tab label을 디렉토리로 채우거나 `herdr pane report-metadata --token NAME=VALUE`로 커스텀 토큰을 주입하는 둘뿐이다.

shell rc의 `chpwd` 훅에서 `herdr tab rename "$HERDR_TAB_ID" "$(basename "$PWD")"`를 호출하면 claude·codex·plain shell을 한 번에 덮고 `cd`·zoxide 이동까지 반영된다. 에이전트별 세션 훅보다 셸 레벨이 커버 범위가 넓다. config를 이식할 때 이 훅도 함께 옮긴다.

`tab` 토큰은 number가 아니라 label을 렌더한다. 기본 label이 번호 문자열이라 번호처럼 보일 뿐이므로, `label == str(number)`가 "이름을 안 지었다"의 판별식이 된다.

## 체크리스트

1. 원본·대상 `herdr --version` 기록
2. 대상 `herdr --help`의 `Config:` 경로 확인
3. 대상 기존 파일 백업
4. `scp`/`rsync`로 byte-exact 복사
5. `herdr config check` → `config: ok`
6. 로컬 서버는 `herdr server reload-config`, remote attach는 detach 후 재접속
7. prefix와 대표 바인딩 1~2개를 실제 입력으로 확인
