---
name: diagram-design
description: MUST USE when creating, choosing, or improving any diagram or visual explanation - mermaid flowchart/sequence/state/ER diagrams, architecture sketches, gantt/mindmap/timeline, charts for docs or issues, ASCII art, or rendered HTML pages. Triggers include 다이어그램, 그림, diagram, flowchart, sequence diagram, mermaid, 시각화, architecture diagram, chart. Picks the best form and medium for the content, renders high-quality output, and verifies renderability before delivering.
license: MIT
metadata:
  routing_source: https://github.com/melodic-software/claude-code-plugins (visualize skill)
---

# Diagram Design

대화 중에 있는 내용 중 시각적으로 보여줄 가치가 가장 큰 대상을 찾아, 알맞은 형태(form)와 매체(medium)를 결정하고, 고품질 결과물을 렌더링까지 검증해서 전달한다.

## 사용 범위

- **사용**: "다이어그램으로 그려줘", "diagram this", "flowchart 만들어줘", "sequence diagram", "mermaid로 보여줘", "아키텍처 그림", "이 흐름을 시각화해줘", 문서/이슈/PR에 들어갈 도식 작성.
- **사용 안 함**: 차트 색상·축 미세 조정만 요청할 때(이미 만들어진 차트의 폼 자체가 옳다면), 밀도 높은 텍스트를 쉬운 말로 풀어주기만 할 때(그것은 요약 작업이다).

## Step 1 - 대상 추론

대화 상태를 읽고 지금 보여줄 가장 가치 있는 하나의 대상을 고른다. 방금 설명한 프로세스, 비교 중인 선택지, 수치 추이, 설계 중인 구조가 후보다. 사용자가 형태를 지목했다면 그 형태를 존중한다.

## Step 2 - 형태 선택

내용의 모양이 형태를 결정한다. 전체 카탈로그는 `references/decision-matrix.md`에 있다.

| 내용의 모양 | 형태 |
|---|---|
| 흐름, 프로세스, 계층, 순서, 상태, 관계, 타임라인 | **mermaid 다이어그램** (계열은 카탈로그에서 선택) |
| 항목들 간 속성·옵션 비교 | **markdown 표** |
| 수량의 추세, 분포, 비율, 순위 | **차트** (페이지 위 SVG 프리미티브 또는 터미널 Unicode bar) |
| 작은 구조 스케치, 디렉터리 트리, 박스 배치 | **ASCII/Unicode 아트** |
| 복합적이거나 인터랙티브하거나 큰 다중 뷰 | **self-contained HTML 페이지** |

## Step 3 - 매체 선택

풍부함의 오름차순 등급이며, 첫 번째로 맞는 등급을 쓴다.

1. **Git 호스트가 렌더링하는 markdown**(기본): 저장소 문서, 이슈 본문, PR/MR 본문에 들어가는 ` ```mermaid ` 펜스는 GitHub와 GitLab이 기본 렌더링한다. 산출물이 문서·이슈·PR에 귀속된다면 이 등급이 정답이다.
2. **터미널**: 표, ASCII 아트, mermaid 소스 펜스. 터미널에서 mermaid 펜스는 그림이 아니라 소스 텍스트로 보인다는 사실을 숨기지 않는다.
3. **self-contained HTML**: 렌더링된 그림이 필요하지만 Git 호스트 문맥 밖일 때. mermaid 렌더러를 페이지 안에 인라인으로 포함하고(CDN 로딩 금지, 오프라인 동작), 임시 디렉터리에 쓰고 절대 경로를 보고한다. 소비자 저장소 트리에 쓰지 않는다.

외부 클라우드 차트 서비스와 데이터 egress가 있는 서드파티 렌더러는 쓰지 않는다.

## 품질 규칙

### 배치와 크기

- flowchart 기본 방향은 `TD`. 파이프라인·단계 흐름은 `LR`이 읽기 좋다.
- 한 다이어그램에 노드 15개를 넘기지 않는다. 넘으면 하위 프로세스 하나를 `subgraph`로 묶어 축약하거나, 다이어그램을 둘로 나누고 경계 노드로 연결한다.
- `subgraph` 중첩은 2단계까지만. 그룹 이름은 내용이 드러나게 짓는다.

### 라벨과 텍스트

- 노드 ID는 짧게, 표시 라벨은 구체적으로. `A[Node]`, `B[Process]` 같은 빈 라벨을 쓰지 않는다.
- 화살표 관계가 자명하지 않으면 에지 라벨을 붙인다 (`-->|검증 통과|`).
- 한국어 라벨과 특수문자가 있는 라벨은 반드시 따옴표로 감싼다: `A["배포 파이프라인"]`. 괄호, 콜론, 슬래시가 포함된 라벨을 따옴표 없이 쓰면 파싱이 깨진다.
- 다이어그램 안의 한국어 텍스트는 `fluent-korean` 지침을 따르고, 용어는 문서·이슈 본문과 동일하게 유지한다.

### 색과 접근성

- `classDef`는 의미 있는 4개 이하로 제한한다. 장식용 색을 쓰지 않는다.
- 색만으로 의미를 구분하지 않는다. 위험/정상/선택은 라벨이나 모양으로도 구분되게 한다.
- 같은 모양·색은 문서 전체의 모든 다이어그램에서 같은 의미를 가진다.

### mermaid 문법 안전

- 검증되지 않은 신규 계열(`sankey`, `xychart`, `kanban`, `radar`, `treemap`)을 쓰지 않는다. 안정 계열 13종은 `references/decision-matrix.md`의 표를 따른다.
- 노드 ID에 하이픈·특수문자를 쓰지 않고, 예약어(`end`, `graph`, `subgraph`)를 소문자 ID로 쓰지 않는다.
- sequenceDiagram 참가자는 alias를 쓴다: `participant U as 사용자`.

## 전달 전 검증

1. 문법 검증: `npx -y @mermaid-js/mermaid-cli --input <file> --output <svg>`로 컴파일한다. 패키지 이름 뒤에 `mmdc`를 덧붙이지 않는다. `npx @mermaid-js/mermaid-cli`가 이미 `mmdc` 바이너리로 해석되므로 `mmdc`는 위치 인자가 되어 `error: too many arguments. Expected 0 arguments but got 1.`로 거부된다(2026-08-27 확인). 굳이 바이너리 이름을 쓰려면 `npx -y -p @mermaid-js/mermaid-cli mmdc --input <file> --output <svg>`처럼 `-p`로 패키지를 지정한다. 실행 환경에서 불가능하면 괄호·따옴표 균형, 예약어 충돌, 에지 화살표 문법을 직접 대조 검토한다.
2. 렌더링 확인: SVG/PNG 출력 파일을 실제로 열어 라벨 잘림, 겹침, 방향을 눈으로 확인한다. CJK 라벨 잘림이 흔하다.
3. Git 호스트 렌더링 대상이라면 안정 계열인지 다시 확인한다. 호스트 렌더러 버전은 문서화되어 있지 않으므로 새 계열은 검증 전에 신뢰하지 않는다.
4. 검증에 실패했는데 고칠 수 없으면, 그려진다고 암시하지 말고 소스 펜스와 함께 "렌더링 검증 못 함"을 명시한다.

## 안티패턴

- 세 행짜리 비교를 굳이 다이어그램으로 만들지 않는다. 표가 정답이다.
- 터미널에서 mermaid 펜스가 렌더링된 것처럼 행동하지 않는다.
- 노드 30개짜리 스파게티 한 장을 만들지 않는다. 나누는 것이 품질이다.
- CDN 스크립트를 로드하는 HTML을 만들지 않는다. 오프라인에서 깨지고 외부 의존이 생긴다.
