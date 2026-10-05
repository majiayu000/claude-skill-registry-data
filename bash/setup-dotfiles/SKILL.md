---
name: setup-dotfiles
description: >
  셸 설정, Homebrew 패키지, mise 툴체인의 기준선을 새 머신에 설치하거나 현재 머신과 대조하는 스킬.
  번들된 zshenv·zprofile·zshrc·Brewfile·mise 설정을 기존 파일과 병합하고, 머신 고유 값은 로컬 파일로 분리한다.
  "dotfiles 설치", "zshrc 셋업", "셸 설정 이식", "셸 설정 정리", "zshenv zprofile zshrc 역할 점검",
  "non-interactive 셸에서 PATH 안 잡혀", "brew 패키지 설치", "Brewfile 적용",
  "mise 툴체인 설정", "dotfiles 대조", "brew 목록 갱신해줘",
  "install dotfiles", "setup shell config", "apply Brewfile", "zsh startup files" 등에서 트리거.
---

# setup-dotfiles

셸·패키지·툴체인 기준선을 다룬다. 에이전트 계층(글로벌 지침, 훅, statusline)은 `setup-machine`이 조율하고 이 스킬은 그 아래 계층만 소유한다.

## 번들 파일

| 파일 | 대상 위치 |
|------|-----------|
| `references/Brewfile` | 임의 위치에서 `brew bundle install --file=` |
| `references/mise-config.toml` | `~/.config/mise/config.toml` |
| `references/zshenv` | `~/.zshenv` |
| `references/zprofile` | `~/.zprofile` |
| `references/zshrc` | `~/.zshrc` |

`${CLAUDE_PLUGIN_ROOT}/skills/setup-dotfiles/references/` 또는 `~/.agents/skills/setup-dotfiles/references/` 로 resolve한다.

## 설치 순서

1. **Brewfile** — 셸 설정이 `zoxide`, `fzf`, `fd`, `fx`, `bat`를 전제하므로 패키지가 먼저다. 이 순서가 뒤집히면 새 셸이 매번 `command not found`를 낸다.
2. **mise 설정** — 언어 런타임. Brewfile은 `mise` 자체만 깔고 런타임은 mise가 관리한다.
3. **zshenv → zprofile → zshrc** — 모든 셸 공통값, 로그인 셸의 PATH와 shellenv, 대화형 설정 순서다. 무엇을 어디에 두는지는 아래 "파일 역할"이 정한다.
4. **oh-my-zsh 커스텀 플러그인** — `fzf-tab`, `zsh-autosuggestions`, `fast-syntax-highlighting`은 oh-my-zsh 번들이 아니다. `$ZSH_CUSTOM/plugins/`에 각각 clone해야 하고, 없으면 셸 시작 시 경고가 난다.

## 파일 역할

어느 파일에 둘지는 "터미널 없이 뜬 프로세스(IDE 태스크, MCP 서버, 빌드 스크립트)가 그 값을 읽는가"로 정한다. 읽으면 zprofile, 대화형 위젯만 쓰면 zshrc다.

| 파일 | 읽는 셸 | 두는 것 |
|------|---------|---------|
| `zshenv` | 모든 zsh (`zsh -c`, 스크립트, ssh 원격 명령) | `typeset -U path`, `~/.local/bin`. 외부 명령 실행은 두지 않는다 |
| `zprofile` | login 셸 | brew shellenv, mise shims, 나머지 PATH, 비대화형 도구가 읽는 env (`ANDROID_HOME`, `REACT_EDITOR`) |
| `zshrc` | 대화형 셸 | oh-my-zsh, alias, completion, 위젯 전용 env (`FZF_*`, `_ZO_MAXAGE`) |

macOS에서 Terminal, IDE의 셸 환경 해석, Claude Code의 셸 스냅샷은 모두 login 셸을 거친다. 그래서 비대화형 프로세스가 실제로 보는 파일은 zshenv가 아니라 zprofile이고, mise 문서도 shims 활성화를 zprofile에 두라고 안내한다. zshenv에는 clean 환경의 `zsh -c`에서도 필요한 최소값만 둔다.

## 기존 파일이 있을 때

덮어쓰지 않는다. 사용자가 손봐둔 내용이 대부분 그 안에 있다.

- 먼저 diff를 보여주고 무엇이 추가·변경되는지 합의한다.
- 덮어쓰기로 합의되면 `<파일>.bak-<timestamp>`를 남긴다.
- 머신 고유 값(회사 CLI PATH, 사설 레지스트리, 자격증명 파생 export)은 번들 파일에 넣지 않는다. `~/.zshrc.local`과 `~/.zprofile.local`로 옮긴다 — 두 파일 모두 번들 설정 맨 끝에서 source되고 추적하지 않는다.

## 레포에 올리지 않는 것

이 레포는 공개다. 다음은 번들 파일에 넣지 않는다.

- 키, 토큰, 비밀번호 값. `$(gh auth token)`처럼 런타임에 읽는 형태도 기본은 주석 처리한다 — 모든 셸의 환경변수로 노출되는 트레이드오프를 각자 선택해야 한다.
- 사용자 홈의 절대경로. `$HOME`을 쓴다.
- 회사·프로젝트 전용 tap, 사설 레지스트리, 사내 도구 PATH.
- 승인·샌드박스를 우회하는 에이전트 CLI 플래그 alias. 개인의 위험 감수 선택이지 기준선이 아니다.

## Brewfile 갱신

`brew bundle dump`는 스냅샷이지 동기화가 아니다. 갱신 시점을 정하지 않으면 파일은 반드시 낡는다. 판별식은 한 방향이다.

- `brew bundle check --file=<f> --verbose` → 등록됐는데 미설치인 것
- 설치 목록(`brew leaves`, `brew list --cask`)과의 차집합 → 설치됐는데 미등록인 것

후자만 쌓이면 dump 이후 갱신이 멈춘 상태다. 이때 통째로 dump해서 덮지 않는다. 번들 Brewfile은 머신 스냅샷이 아니라 큐레이션된 기준선이고, dump는 개인·회사 전용 패키지를 그대로 끌어온다. 차집합을 보고 기준선에 넣을 것만 골라 넣는다.

## 대조 모드

"dotfiles 대조", "뭐가 다른지 봐줘" 류 요청에서는 아무것도 쓰지 않는다. 다섯 대상의 diff와 Brewfile 양방향 차집합만 보고한다.

세 셸 파일의 역할 분담이 지켜지는지는 diff가 아니라 실행으로 판정한다. `env -i HOME=$HOME /bin/zsh -lc 'command -v psql'`처럼 clean 환경의 login 셸에서 도구가 잡히는지, `zsh -lic 'print -l $path' | sort | uniq -d`가 비어 있는지 본다. 대화형 셸에서 잘 되는 설정이 이 검사에서 깨지면 PATH가 zshrc에 있다는 뜻이다.

## Gotchas

- `stty -ixon`이 빠지면 tty가 C-s를 flow control로 삼켜 tmux·herdr의 `ctrl+s` prefix가 앱까지 오지 않는다. Linux·WSL에서 특히 자주 밟는다.
- zshrc의 herdr `chpwd` 훅은 `setup-herdr`가 "config와 함께 옮기라"고 지시하는 그 훅이다. 두 스킬을 같이 쓸 때 중복 삽입하지 않는다.
- macOS `/etc/zprofile`의 `path_helper`가 login 셸마다 PATH를 재구성해 zshenv에서 앞에 붙인 항목을 시스템 경로 뒤로 민다. zshenv만으로는 PATH 순서를 보장할 수 없으므로 zprofile이 다시 앞에 붙이고, zshenv의 `typeset -U`가 그 중복을 지운다.
- GUI에서 뜬 앱은 zsh를 거치지 않아 세 파일 중 어느 것도 못 본다. IDE가 login 셸로 환경을 읽어 오는 것이 우회 경로이고, 그래서 PATH를 zshenv로 옮겨도 GUI 앱 문제는 풀리지 않는다.
- Codex, Antigravity 같은 설치기가 zprofile·zshrc 끝에 `~/.local/bin` export를 덧붙인다. 병합 시 지우고, 다시 생겨도 `typeset -U` 덕에 무해하다.
- zshenv에 `eval "$(brew shellenv)"`나 `$(gh auth token)`처럼 외부 명령을 두면 모든 `zsh -c`와 스크립트 기동마다 실행된다. 값만 두는 파일로 유지한다.
- `fpath` 추가는 `oh-my-zsh.sh`가 실행하는 compinit보다 앞에 있어야 completion에 반영된다. 뒤에 두면 경고 없이 무시된다.
- Homebrew 경로는 Apple Silicon 기준 `/opt/homebrew`다. Intel Mac이나 Linuxbrew는 prefix가 다르므로 `brew shellenv` 줄과 `libpq`·`mysql-client` PATH를 그 머신 prefix로 고친다.
- 셸 설정 변경은 새 셸부터 유효하다. 기존 탭은 반영되지 않는다.
