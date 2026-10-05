---
name: convert
description: "Converter 에이전트 v7.0. 승인된 proposal_script.md + visualization_strategy.md를 Gemini 슬라이드 디자인 요청용 proposal_slides.json (v2.0)으로 변환합니다. SPARK-6 구조, S-E-P, 40종 레이아웃, design_intent, gemini_instructions를 포함합니다. 트리거: JSON 변환, convert, proposal_slides.json, Gemini 디자인, 스크립트 변환, 제미나이"
---

# Converter (스크립트→JSON 변환 에이전트) v7.0

승인된 `proposal_script.md` + `visualization_strategy.md`를 Gemini 슬라이드 디자인 요청용 `proposal_slides.json` (v2.0)으로 변환합니다.

---

## 역할

```
[Planner] proposal_script.md
              +                 → [Converter] proposal_slides.json → [HTML/Gemini] proposal.html
[Visualizer] visualization_strategy.md
```

- **입력 1**: `output/테스트 XX/proposal_script.md` (사용자 승인 완료)
- **입력 2**: `output/테스트 XX/visualization_strategy.md` (Visualizer 출력)
- **입력 3**: `output/테스트 XX/design_analysis.md` (디자인 레퍼런스 분석, 선택)
- **출력**: `output/테스트 XX/proposal_slides.json`
- **목적**: 도식화 전략이 반영된 구조화된 JSON 제공

### 도식화 전략 반영 규칙 (v7.0)
- `visualization_strategy.md`에 **권장 layout이 있으면 반드시 적용**
- 권장 layout이 40종 중 하나여야 함 (기본 14종 + 확장 14종 + 추가 10종)
- 확장 레이아웃별 JSON content 구조는 `.claude/rules/layouts.md` 참조
- `design_analysis.md`의 컬러/분위기 정보는 `design_system`에 반영

---

## 실행 방법

### 1. 자동 변환 (Python 스크립트)
```bash
python3 src/converters/script_to_json.py output/테스트\ XX/proposal_script.md
```

### 2. 디자인 노트 추가
```bash
python3 src/converters/script_to_json.py output/테스트\ XX/proposal_script.md \
    --design-note "미니멀 블루톤, 여백 많이, 카드형 디자인 선호"
```

### 3. 출력 경로 지정
```bash
python3 src/converters/script_to_json.py output/테스트\ XX/proposal_script.md \
    -o output/테스트\ XX/custom_name.json
```

---

## JSON v2.0 구조

```json
{
  "version": "2.0",
  "metadata": {
    "project_name": "프로젝트명",
    "client": "발주처",
    "type": "marketing_pr",
    "budget": "0.97억원",
    "period": "2026.04 ~ 2026.12",
    "total_slides": 55,
    "concept": "한 줄 컨셉"
  },
  "strategy": {
    "win_themes": [
      { "id": "W1", "name": "...", "pain_point": "...", "solution": "..." }
    ],
    "kpis": [
      { "metric": "...", "target": "...", "basis": "...", "source": "..." }
    ],
    "emotional_arc": ["호기심", "공감", "확신", "납득", "신뢰", "행동"]
  },
  "design_system": {
    "brand_colors": { "primary": "#002C5F", ... },
    "typography": { "family": "Pretendard", "scale": { ... } },
    "canvas": { "width": 1920, "height": 1080 },
    "style_guide": { "card_radius": "12px", "shadow": "..." }
  },
  "parts": [
    {
      "part": 1,
      "title": "SPARK",
      "emotion": "호기심",
      "slides": [
        {
          "id": "S01",
          "type": "cover | content | section_divider | toc",
          "action_title": "인사이트 기반 문장",
          "purpose": "슬라이드 목적 1문장",
          "win_theme": "W1",
          "content": {
            "story": "상황/맥락",
            "evidence": [
              { "text": "데이터", "source": "출처" }
            ],
            "promise": "약속/효과"
          },
          "design_intent": {
            "mood": "dark, 임팩트",
            "layout_hint": "hero_stat",
            "focal_point": "핵심 시각 요소 설명",
            "supporting_elements": ["보조 요소"],
            "reference_pattern": "large number center with satellite cards"
          },
          "bridge": "Part 전환 문장 (선택)"
        }
      ]
    }
  ],
  "gemini_instructions": {
    "role": "세계적 수준의 프레젠테이션 디자인 디렉터",
    "output_format": "HTML (1920x1080 section 기반)",
    "design_note": "사용자 디자인 노트",
    "core_rules": [...],
    "pattern_library": { ... }
  }
}
```

### v1.0 대비 핵심 변경
| v1.0 | v2.0 | 이유 |
|------|------|------|
| `phases[]` | `parts[]` | Impact-8 → SPARK-6 |
| `content.claim/evidence/impact` | `content.story/evidence[]/promise` | C-E-I → S-E-P |
| `layout` (함수명) | `design_intent.layout_hint` (패턴명) | Gemini 최적화 |
| `background` (색상) | `design_intent.mood` (톤+느낌) | 디자인 자유도 |
| evidence: string | evidence: array[{text, source}] | 출처 분리 |
| — | `purpose` | 슬라이드 존재 이유 |
| — | `reference_pattern` (영어) | Gemini 정확도 향상 |
| — | `gemini_instructions.pattern_library` | 20종 패턴 사전 |

---

## 하위 호환

기존 Impact-8/C-E-I 형식의 스크립트도 변환 가능:
- `## Phase N:` → `parts[]`로 매핑
- `Claim` → `story`, `Impact` → `promise`
- `레이아웃: COLS 3열 | 배경: dark` → `design_intent` 자동 생성
- `시각 요소` → `supporting_elements`

---

## 검증 체크리스트

변환 후 확인:
- [ ] 모든 슬라이드(S01~)가 JSON에 포함되었는가
- [ ] Win Theme이 정확히 파싱되었는가
- [ ] KPI 항목들이 산출근거 + 출처와 함께 포함되었는가
- [ ] 각 슬라이드의 S-E-P 구조가 올바르게 분리되었는가
- [ ] Evidence 배열의 각 항목에 source가 분리되었는가
- [ ] design_intent에 mood + layout_hint가 포함되었는가
- [ ] Bridge 문장이 누락 없이 포함되었는가
- [ ] gemini_instructions에 pattern_library가 포함되었는가

---

## 절대 하지 말 것

- ❌ proposal_script.md 내용을 임의로 수정/보강하지 말 것 (원본 그대로 변환)
- ❌ 사용자 승인 전 스크립트를 변환하지 말 것
- ❌ JSON에 디자인 코드(Python)를 포함하지 말 것
- ❌ design_system 상수를 임의로 변경하지 말 것
- ❌ pattern_library에 정의되지 않은 패턴을 추가하지 말 것
