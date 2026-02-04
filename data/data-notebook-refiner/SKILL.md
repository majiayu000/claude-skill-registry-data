---
name: data-notebook-refiner
description: Jupyter Notebook의 코드 품질, 문서화 수준, 실행 안정성을 표준화된 절차로 개선하는 워크플로우입니다.
---

# Notebook Refiner Workflow

기존 Jupyter Notebook을 **학습 자료 수준(Study Material Quality)**으로 다듬기 위한 워크플로우입니다. 단순 코드 정리(Linting)를 넘어, **"왜(Why)"**에 대한 설명과 **재현 가능성(Reproducibility)**, 그리고 **시각적 이해(Visual Understanding)**를 확보하는 데 집중합니다.

### 1단계: 분석 및 기준 확인 (Analyze & Context)
1.  **Context Loading**: `this document`를 읽어 'High Quality Notebook'의 기준을 로드합니다.
2.  **Current State Check**: 리팩토링할 노트북을 열고 `resources/checklist.md`와 대조하여 부족한 점을 파악합니다.
    *   **Structure**: 흐름이 논리적인가?
    *   **Structure**: 흐름이 논리적인가?
    *   **Dependency**: 환경 설정이 명시되었는가?
    *   **Filename**: `docs/notebooks/[Topic]_Analysis.ipynb` 이름 규칙을 유지하며, 기존 파일을 덮어쓰거나 수정합니다.

### 2단계: 리팩토링 및 표준화 (Refactor)
기능 변경 없이 코드의 가독성과 구조를 개선합니다.

1.  **Code Quality**: 변수명을 직관적으로 변경하고(`df` -> `titanic_df`), 셀의 단위를 적절히 나눕니다.
2.  **Output Cleaning**: 불필요하게 긴 로그를 숨깁니다.
3.  **Imports**: 모든 import 문을 최상단 셀(`🔧 Setup & Imports`)로 이동합니다.

### 3단계: 학습 요소 보강 (Enrichment)
**"Master Class" 수준의 깊이**를 더하기 위해 다음 요소들을 반드시 포함시킵니다.

1.  **Narrative (스토리텔링)**: 코드 실행 전후에 **"이론적 배경"**과 **"직관적 설명"**을 **한글로** 추가합니다. (예: "왜 ReLU를 사용하는가?", "이 Loss가 줄어든다는 것은 무엇을 의미하는가?")
2.  **Visualization (시각화)**: 텍스트 결과만으로는 부족합니다.
    *   **Data**: 분포, 상관관계 등을 산점도나 히스토그램으로 확인.
    *   **Training**: Loss Curve, Accuracy Trend를 그래프로 시각화.
    *   **Result**: 오분류 이미지(Misclassified), Confusion Matrix 등 시각적 검증.
3.  **Experimentation (실험)**: Hyperparameter(Learning Rate, Batch Size 등)를 변수로 추출하여, 독자가 값을 바꿔가며 실험해볼 수 있도록 구성합니다.
4.  **Evaluation (평가)**: 단순 Loss 외에 Accuracy, F1-Score 등 **"해석 가능한 지표"**를 출력합니다.

### 4단계: 문서화 및 구조화 (Document)
코드를 체계적으로 정리하여 "책"처럼 읽히게 만듭니다.

1.  **Why & Context**: "무엇을 하는 코드인가"보다 **"왜 이렇게 짰는가"**를 주석이나 마크다운으로 **한글로** 설명합니다.
2.  **Headers**: 적절한 Markdown Header(`#`, `##`)를 사용하여 목차를 구성합니다.

### 5단계: 검증 및 인사이트 (Verify & Insight)
1.  **Restart & Run All**: 커널을 재시작하고 에러 없이 끝까지 실행되는지 검증합니다.
2.  **Visual Check**: 그래프의 Title, Label, Legend가 완벽한지 확인합니다.
3.  **Key Takeaways**: 노트북의 맨 마지막에 **"무엇을 배웠는가"**를 요약하는 섹션을 **한글로** 추가합니다.


---

## Standards & Rules

# Notebook Refiner Standards

## Purpose
To ensure Jupyter Notebooks are not just "functioning code dumps" but **educational learning materials** and **reproducible assets**.

## Core Philosophy: "Readability & Reproducibility"
A notebook is a document meant to be read by humans, not just a script for machines.

## Refactoring Standards

### 1. Structure (Flow)
- **Imports**: All imports must be in the first cell.
- **Logical Flow**: Data Load → EDA → Preprocessing → Modeling → Evaluation.
- **Kernel Check**: Must specify required environment (e.g., `venv`, python version).

### 2. Code Quality (Refactor)
- **Naming**: Use descriptive names (`titanic_df`) over generic ones (`df`). Follow conventions (`X`, `y`, `model`).
- **Granularity**: One logical step per cell. Don't mix loading and training in one massive cell.
- **Output**: Suppress verbose logs (e.g., strict `fit()` output).

### 3. Documentation (Context)
**"Explain Why, Not What"**
- **Bad**: "This code splits the data." (Redundant)
- **Good**: "We use `stratify=y` to maintain class balance in the test set." (Insightful)
- **Headers**: Use clear Markdown headers (`#`, `##`) to navigate structure.

### 4. Verification (Reproducibility)
- **Restart & Run All**: The notebook must run from top to bottom without error after a kernel restart.
- **Visuals**: All plots must have Titles, Axis Labels, and Legends.
