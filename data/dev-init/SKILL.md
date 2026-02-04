---
name: dev-init
description: 개발 환경(폴더 구조, README)을 신속하게 초기화하는 Dev 전용 워크플로우입니다.
---

# Dev Init Workflow

개발 또는 학습을 위한 프로젝트 환경을 표준화된 방식으로 초기화합니다.

### 1단계: 프로젝트 정의 (Project Definition)
1.  **Metadata Input**: 프로젝트 이름(Name)과 유형(Type: Study/Dev)을 입력받습니다.
2.  **Context Check**: 현재 디렉토리가 비어있는지 확인합니다.

### 2단계: 스캐폴딩 (Scaffolding)
1.  **Reference Loading**: `this document`를 읽어 표준 레이아웃(Python vs Study)을 확인합니다.
2.  **Structure Generation**:
    *   사용자에게 기술 스택을 묻고, `SKILL.md`에 정의된 구조대로 폴더를 생성합니다.
    *   *Example*: `src/`, `tests/` for Python.
3.  **Git Setup**: `.gitignore`를 생성하되, **`.agent/`가 무시되지 않도록 주의**합니다.

### 3단계: 문서 생성 (Documentation)
1.  **README Generation**:
    *   `resources/README-template.md`를 읽습니다.
    *   입력받은 메타데이터(Type, Date)를 채워 넣어 `README.md`를 생성합니다.

### 4단계: 마무리 (Finalize)
1.  **Completion**: "초기화 완료. `src/`에서 코딩을 시작하세요." 메시지를 출력합니다.


---

## Standards & Rules

# Dev Init Standards

## Purpose
To ensure every project starts with a **consistent, professional structure** that integrates seamlessly with Antigravity Agents.

## Standard Layouts

### 1. Python Project
- `src/`: Source code
- `tests/`: Unit and integration tests
- `docs/`: Documentation
- `scripts/`: Utility scripts
- `.gitignore`: Standard Python ignores

### 2. Study Project
- `notebooks/`: Jupyter Notebooks
- `data/`: Raw and processed data (ignored by git)
- `references/`: Papers and PDFs
- `docs/`: Summaries and plans

## Documentation Standards
- **README.md**: Must exist at root.
- **Metadata**: Must include `Status`, `Type`, `Created` in blockquote.
- **Agent Friendly**: `.agent` folder must NOT be git-ignored.
