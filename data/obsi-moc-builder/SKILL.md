---
name: obsi-moc-builder
description: 특정 폴더(Single) 또는 하위 구조 전체(Recursive)를 분석하여 구조화된 MOC(Map of Content)를 자동 생성/갱신합니다.
---

# Expert MOC Builder Workflow

흩어진 노트들을 모아 **지도의 역할(Map)**을 하는 MOC 노트를 생성합니다.
타겟 위치에 따라 **단일 모드**와 **재귀 모드(Manager)**를 자동으로 전환하여 수행합니다.

## 1. 모드 감지 및 범위 설정 (Scoping)

1.  **Context Detection**: 타겟 경로를 분석하여 모드를 결정합니다.
    *   **Recursive Mode (Manager)**: 타겟이 `20_Learning`, `10_Projects` 등 루트/상위 폴더인 경우. 하위의 모든 주제별 폴더를 스캔하여 일괄 처리합니다.
    *   **Single Mode (Builder)**: 타겟이 특정 주제 폴더(Leaf Folder)인 경우. 해당 폴더에 대해서만 MOC를 생성합니다.

## 2. 실행 로직 (Execution)

### Case A: Recursive Mode (루트 관리)
**"Structure is Recursive"** - 상위 MOC는 하위 MOC들의 합입니다.

1.  **Scanning**: 하위 디렉토리 구조를 스캔합니다.
2.  **Delegation**: 각 하위 폴더에 대해 **Single Mode** 로직을 순차적으로 호출합니다.
    *   *Preservation*: 기존 MOC가 있다면 덮어쓰지 않고 변경분만 반영(Smart Update)합니다.
3.  **Sync**: 모든 하위 작업 완료 후, 최상위 MOC(예: `Learning_MOC.md`)에 하위 MOC 링크들을 업데이트합니다.

### Case B: Single Mode (개별 생성)
**"Turn Chaos into Order"**

1.  **Analysis**: 폴더 내 파일들의 제목과 태그를 분석하여 하위 주제(Cluster)를 식별합니다.
2.  **Drafting**: `resources/moc-template.md`를 사용하여 MOC 내용을 작성합니다.
    *   **Top Down**: 핵심 개념(Core Concepts)을 상단에 배치.
    *   **Bottom Up**: 나머지 노트들을 클러스터별로 그룹화.
3.  **Linking**:
    *   **Downward**: MOC -> 하위 노트 링크.
    *   **Upward**: 하위 노트 -> MOC (`Up: [[MOC]]`) 역방향 링크 제안.

## 3. 시각화 (Viz)
1.  **Graph**: 생성된 MOC를 중심으로 한 로컬 그래프 뷰 확인을 제안합니다.


---

## Standards & Rules

# MOC Engineering Standards

## 1. Core Philosophy
-   **Top Down & Bottom Up**: MOC는 핵심 개념의 정의(Top)와 개별 노트의 집합(Bottom)을 동시에 보여주어야 합니다.
-   **Structure is Recursive**: 최상위 MOC는 하위 토픽 MOC들의 부모가 되어야 하며, 이 계층 구조는 깨지지 않아야 합니다.

## 2. Smart Update Strategy (Recursive Mode)
-   **Preservation First**: Never blindly replace an existing MOC file. Keep any manually written "Description" or "Goals".
-   **Append Logic**: New topics/clusters should be added to the list, not replace existing ones.
-   **Bidirectional Integrity**: Ensure Parent MOC links to Child MOCs, and Child MOCs link back to Parent.

## 3. MOC File Structure
-   **Naming**: `{FolderName}_MOC.md` (Standard)
-   **Tags**: `#moc` included.
-   **Links**: Must contain WikiLinks `[[Note Name]]` to be valid.
