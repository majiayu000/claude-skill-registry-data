---
name: solution-selection
description: 생성된 아이디어를 평가하고 최적의 솔루션을 선택합니다. MVP 개발을 위한 기능 우선순위를 지정할 때 사용하세요.
---

# 솔루션 선정

## 목적

아이디어를 투표 방식으로 평가하고 우선순위 매트릭스를 통해 최적의 솔루션을 선택합니다.

## 사용 시점

- 아이디어 발상이 완료된 후
- 비즈니스 모델 설계 전
- 여러 솔루션 중 최적안을 선택해야 할 때
- 사용자가 "솔루션 선정", "아이디어 평가", "우선순위"를 언급할 때

## 필수 입력

- 아이디어 발상 결과 (ideation 결과):
  - `think/솔루션후보.md`
- 예시 이미지:
  - `reference/sample-solution-proritization.png`

---

## 1단계: 우선순위 평가 (투표)

각 팀원들이 비즈니스 가치와 실현 가능성을 기준으로 아이디어에 투표합니다.

### 요청사항

- **각자 투표 수행**:
  - 비즈니스 가치 3표 (Business Value)
  - 실현 가능성 3표 (Feasibility)
- **표시 방법**:
  - 비즈니스 가치가 높은 아이디어: **B** (Business)
  - 실현 가능성이 높은 아이디어: **F** (Feasibility)
- **투표 집계**:
  - 각 아이디어별로 받은 B와 F 투표수를 합산하여 표시

### 참고자료

`think/솔루션후보.md`

### 결과 형식: 마크다운 표

```markdown
# 솔루션 평가

| 아이디어 제목 | 비즈니스 가치 (B) | 실현 가능성 (F) |
|--------------|------------------|----------------|
| {아이디어 1} | 5 | 3 |
| {아이디어 2} | 3 | 6 |
| {아이디어 3} | 4 | 4 |
```

### 결과 파일

`think/솔루션평가.md`

---

## 2단계: 솔루션 선정 (우선순위 매트릭스)

우선순위 평가 결과를 2x2 매트릭스로 시각화하고 핵심 솔루션을 선정합니다.

### 요청사항

#### 1. 우선순위 평가 매트릭스 작성

**축 설정**:
- **X축**: 실현가능성 (낮음 → 높음)
- **Y축**: 비즈니스 영향도 (낮음 → 높음)

**4개 영역 구분**:

| 영역 | 설명 | 우선순위 |
|-----|------|---------|
| **No Brainers** | 실현가능성 높음 + 비즈니스 영향도 높음 | 1순위 (즉시 실행) |
| **Bit Bets** | 실현가능성 낮음 + 비즈니스 영향도 높음 | 2순위 (전략적 투자) |
| **Utilities** | 실현가능성 높음 + 비즈니스 영향도 낮음 | 3순위 (리소스 여유 시) |
| **Unwise** | 실현가능성 낮음 + 비즈니스 영향도 낮음 | 4순위 (보류/폐기) |

**매트릭스 작성 지침**:
- 그래프에는 **아이디어 ID**만 표시 (예: A1, A2, B1, B2 등)
- 범례로 **아이디어 ID**와 **아이디어명** 매핑 표시
- 가독성을 위해 점과 레이블을 명확히 구분

#### 2. SVG 파일로 매트릭스 생성

- **파일명**: `think/솔루션우선순위평가.svg`
- **참고 예시**: `reference/sample-solution-proritization.png`

#### 3. 핵심 솔루션 선정

**선정 기준**:
1. **No Brainers** 영역의 아이디어 우선 선정
2. No Brainers가 없으면 **Bit Bets**와 **Utilities** 아이디어도 포함

**선정 결과 테이블**:

```markdown
# 핵심 솔루션

| 아이디어 제목 | 설명 | 비즈니스 가치 | 실현 가능성 |
|--------------|------|--------------|------------|
| {No Brainers 아이디어 1} | {상세 설명} | 5 | 4 |
| {No Brainers 아이디어 2} | {상세 설명} | 4 | 5 |
```

**권장사항**:
- 핵심 솔루션은 **3개 이하**로 선정할 것을 권장
- 팀원들과 검토 및 수정 후 최종 확정

### 참고자료

`think/솔루션평가.md`

### 결과 파일

- **우선순위 매트릭스 SVG**: `think/솔루션우선순위평가.svg`
- **핵심 솔루션 문서**: `think/핵심솔루션.md`

---

## 우선순위 매트릭스 SVG 작성 예시

```xml
<svg width="600" height="500" xmlns="http://www.w3.org/2000/svg">
  <!-- 배경 -->
  <rect width="600" height="500" fill="#f9f9f9"/>

  <!-- 축 -->
  <line x1="100" y1="400" x2="550" y2="400" stroke="#333" stroke-width="2"/>
  <line x1="100" y1="400" x2="100" y2="50" stroke="#333" stroke-width="2"/>

  <!-- 축 레이블 -->
  <text x="320" y="440" text-anchor="middle" font-size="14">실현가능성</text>
  <text x="50" y="230" text-anchor="middle" font-size="14" transform="rotate(-90, 50, 230)">비즈니스 영향도</text>

  <!-- 4개 영역 배경색 -->
  <rect x="100" y="50" width="225" height="175" fill="#ffcccc" opacity="0.3"/>  <!-- Bit Bets -->
  <rect x="325" y="50" width="225" height="175" fill="#ccffcc" opacity="0.3"/>  <!-- No Brainers -->
  <rect x="100" y="225" width="225" height="175" fill="#ffffcc" opacity="0.3"/> <!-- Unwise -->
  <rect x="325" y="225" width="225" height="175" fill="#cce5ff" opacity="0.3"/> <!-- Utilities -->

  <!-- 영역 레이블 -->
  <text x="210" y="130" text-anchor="middle" font-size="12" font-weight="bold">Bit Bets</text>
  <text x="435" y="130" text-anchor="middle" font-size="12" font-weight="bold">No Brainers</text>
  <text x="210" y="310" text-anchor="middle" font-size="12" font-weight="bold">Unwise</text>
  <text x="435" y="310" text-anchor="middle" font-size="12" font-weight="bold">Utilities</text>

  <!-- 아이디어 점 (예시) -->
  <circle cx="450" cy="100" r="8" fill="#0066cc"/>
  <text x="465" y="105" font-size="12">A1</text>

  <!-- 범례 -->
  <text x="100" y="470" font-size="11">A1: 아이디어명 1 | A2: 아이디어명 2</text>
</svg>
```

---

## 평가 가이드라인

- **투표는 팀원 각자 독립적으로 수행**
- **비즈니스 가치와 실현 가능성의 균형** 고려
- **No Brainers 영역의 아이디어를 우선** 선정
- **핵심 솔루션은 3개 이하**로 선정 권장
- **팀원들과 검토 및 합의** 후 최종 확정

---

## 도구 활용

### Sequential MCP 사용

복잡한 평가와 의사결정이 필요할 때 Sequential MCP를 활용하여 체계적으로 최적 솔루션을 도출하세요.

---

## 결과 파일

- **1단계 결과**: `think/솔루션평가.md` (투표 결과 집계표)
- **2단계 결과**:
  - `think/솔루션우선순위평가.svg` (우선순위 매트릭스)
  - `think/핵심솔루션.md` (선정된 핵심 솔루션)

---

## 주의사항

### 1단계 (우선순위 평가)
- 각 팀원이 독립적으로 투표 수행
- 비즈니스 가치 3표, 실현 가능성 3표씩 배분
- B와 F 투표수를 명확히 구분하여 집계

### 2단계 (솔루션 선정)
- 우선순위 매트릭스는 SVG 파일로 작성
- 아이디어 ID 사용으로 가독성 확보
- No Brainers 영역 아이디어를 최우선 선정
- No Brainers가 없으면 Bit Bets와 Utilities 포함
- **핵심 솔루션은 3개 이하로 선정** (권장)

### 최종 검토
- **팀원들과 결과 파일 검토 및 수정**
- `think/핵심솔루션.md`를 백업 후 선택된 핵심 솔루션만 남김
- 합의를 통한 최종 확정

---

## 다음 단계

솔루션 선정 완료 후:
1. **결과 파일 팀원들과 검토 및 수정**
2. 비즈니스 모델 기획 (Lean Canvas)
3. 서비스 기획서 발표자료 작성
4. Event Storming 및 유저스토리 작성
