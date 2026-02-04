---
name: emacs-keybind-check
description: Emacs 키바인딩을 검사하고 분석합니다. 키 충돌 확인, 특정 키에 바인딩된 명령 찾기, 명령에 할당된 키 검색에 사용합니다. "키바인딩", "키맵", "단축키", "keybind", "충돌" 등의 키워드에 활성화됩니다.
allowed-tools: Read, Bash
---

# Emacs 키바인딩 검사

Emacs 설정 파일에서 키바인딩을 검색하고 분석하는 스킬입니다.

## 사용 가능한 명령

### 1. 모든 키바인딩 검색

```bash
~/.claude/skills/emacs-keybind-check/scripts/find-keybindings.sh ~/.emacs.d
```

### 2. 특정 키 시퀀스 검색

```bash
~/.claude/skills/emacs-keybind-check/scripts/find-keybindings.sh ~/.emacs.d --key "C-c p"
```

### 3. 특정 명령어로 검색

```bash
~/.claude/skills/emacs-keybind-check/scripts/find-keybindings.sh ~/.emacs.d --cmd "projectile"
```

### 4. 중복 키바인딩 탐지

```bash
~/.claude/skills/emacs-keybind-check/scripts/find-keybindings.sh ~/.emacs.d --conflicts
```

### 5. 충돌 결과를 파일에 저장

```bash
~/.claude/skills/emacs-keybind-check/scripts/find-keybindings.sh ~/.emacs.d --conflicts --output /tmp/keybind-conflicts.md
```

파일 출력시 포함되는 상세 정보:
- 생성 일시
- 검색 경로
- 각 충돌 키별로 정의된 모든 위치 (파일:라인)
- 해당 라인의 전체 코드

## 탐지하는 키바인딩 패턴

- `global-set-key`
- `define-key`
- `local-set-key`
- `bind-key` (bind-key.el)
- `evil-define-key` (evil-mode)
- `general-define-key` (general.el)
- use-package의 `:bind` 키워드

## 분석 절차

1. 사용자가 요청한 내용을 파악 (전체 검색, 특정 키, 충돌 탐지 등)
2. 적절한 옵션으로 스크립트 실행
3. 결과를 분석하여 다음 정보 제공:
   - 발견된 키바인딩 목록
   - 파일 경로와 라인 번호
   - 충돌 가능성이 있는 키들
   - 권장 사항 (필요시)

## 후속 작업

충돌 결과가 파일에 저장되면:
1. 해당 파일을 읽어 충돌 목록 확인
2. 각 충돌에 대해 사용자에게 해결 방안 제시
3. 필요시 설정 파일 수정 제안

## 한계

- 런타임에 동적으로 정의되는 키바인딩은 탐지 불가
- 매크로로 생성되는 키바인딩은 패턴에 따라 탐지되지 않을 수 있음
- `hydra`, `transient` 등 복잡한 키맵은 별도 분석 필요
