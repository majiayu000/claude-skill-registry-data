---
name: dev-study-planner
description: 체계적인 학습 계획 수립, 실행, 검증을 위한 학습 전용 워크플로우입니다. (퓨처 플래너의 학습 버전)
---

# Study Planner Workflow

이 워크플로우는 `dev-feature-planner`의 엄격한 프로세스를 **학습(Study)**에 맞게 최적화했습니다. 단순히 눈으로 보는 공부가 아니라, **"계획 -> 이론 -> 실습 -> 검증"**의 사이클을 통해 확실한 지식 체득을 목표로 합니다.

### 1단계: 학습 목표 및 범위 설정 (Goal Setting)
무엇을 공부할지 명확히 정의하고, **학습 모드(Mode)**를 결정합니다.

### 1단계: 학습 목표 및 범위 설정 (Goal Setting)
무엇을 공부할지 명확히 정의합니다. **"대충 훑어보기"는 이 워크플로우의 대상이 아닙니다.**

1.  **Topic Selection**: 학습할 주제를 선정합니다. (예: "Transformer 아키텍처 이해", "Python 제너레이터 마스터")
2.  **Resources**: 학습에 사용할 자료(공식 문서, 강의, 책, 논문)를 수집합니다.
3.  **Deliverables**:
    *   **Feynman Summary**: 비전공자도 이해할 수 있는 평이한 언어의 요약본.
    *   **Break & Fix Log**: 코드를 고장 내고 고친 기록.
    *   **Implementation**: 직접 구현한 코드 또는 결과물.

### 2단계: 학습 계획 문서 생성 (Study Plan Creation)
`docs/plans/` 디렉토리에 학습 계획 문서를 작성합니다.

1.  **Context Loading**: `this document`를 읽어 'Deep Mastery' 기준을 확인합니다.
2.  **Drafting**: `resources/plan-template.md`를 사용하여 `docs/plans/STUDY_[주제].md`를 작성합니다.
3.  **Approval**: 사용자에게 계획을 검토받습니다.

### 3단계: 심층 학습 실행 루프 (Deep Learning Loop)
각 Session에 대해 다음 3단계를 **반드시** 수행합니다.

1.  **📖 Theory (Feynman Test)**
    *   자료를 학습한 후, 핵심 개념을 **비전공자에게 설명하듯** 쉬운 말로 요약합니다.
    *   전문 용어(Jargon) 사용을 최대한 배제합니다.

2.  **💻 Practice (Break & Fix)**
    *   **Action**: 예제 코드를 실행만 하지 말고, 일부러 **고장(Break)** 냅니다.
    *   **Analysis**: 에러 로그를 분석하고 원인을 파악합니다.
    *   **Fix**: 다시 정상 작동하도록 수정하고, 이 과정을 로그로 남깁니다.

3.  **🧪 Experiment (Implementation)**
    *   이론에서 배운 내용을 바탕으로 Notebook이나 스크립트를 **직접 구현**합니다. (Copy & Paste 지양)
    *   Edge Case를 실험합니다.

### 4단계: 회고 및 아카이빙 (Retrospective & Archiving)
1.  **Summarize**: 오늘 배운 내용의 핵심(Key Takeaways)을 3줄 요약합니다.
2.  **Troubleshooting**: 실습 중 마주친 에러와 해결 방법을 기록합니다. (지식 자산화)
3.  **Next**: 다음 학습 단계를 업데이트하거나, 심화 학습 주제를 잡습니다.


---

## Standards & Rules

# Study Planner Standards (Deep Mastery)

## Purpose
To transform passive information consumption into **active, verified knowledge mastery**. This standard enforces a rigorous cycle of explanation, experimentation, and implementation.

## Core Philosophy: "Deep Work Only"
We do not support "skimming" or "quick summaries". If you are using this planner, you are committing to **fully understanding** the topic.

## Mandatory Strategies

### 1. 🗣️ Feynman Technique (Concept Verification)
**"Simplicity is the ultimate sophistication."**
- **The Rule**: You must explain the concept in simple language, without using jargon.
- **The Test**: If you cannot explain it to a 6-year-old (or a non-technical peer), you don't understand it.
- **Artifact**: Every session must produce a "Plain English Summary" in your notes.

### 2. 🔨 Break & Fix (Practical Verification)
**"You don't know it until you break it."**
- **Action**: Never just run example code.
- **Step 1 (Break)**: Intentionally modify variables, logic, or configurations to cause errors.
- **Step 2 (Analyze)**: Predict the error message before running.
- **Step 3 (Fix)**: Restore functionality and document *why* it broke.
- **Log**: You must maintain a `troubleshooting_log` for every session.

### 3. 🏗️ Implementation First (Output)
**"Code over Concepts."**
- **Artifact**: Passive reading is not counted as progress. You must produce one of:
    - A working script/notebook.
    - A diagram drawn from scratch.
    - A mini-project.

## Quality Gate

Before marking a session as "Complete", you must verify:
- [ ] **Feynman Summary**: Is the summary jargon-free?
- [ ] **Break Log**: Did you break the code at least once?
- [ ] **Implementation**: Is there runnable code or a concrete artifact?
- [ ] **Quiz**: Did you create and solve at least 3 self-test questions?
