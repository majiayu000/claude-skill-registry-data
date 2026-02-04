---
name: book-detail-page-creator
description: 도서 상세 페이지 제작을 위한 마케팅 문구 생성 및 PPT 템플릿 작업. 책의 내용을 분석하여 4컷 상세 이미지용 문구를 작성하고, 제공된 PPT 템플릿에 문구와 페이지 번호를 채워 넣는다. {{문구}}, {{page_num_left}}, {{page_num_right}} placeholder를 사용하는 템플릿이 제공되거나, 도서 상세 페이지 문구 작성 요청이 있을 때 사용한다.
---

# Book Detail Page Creator

도서 쇼핑몰 상세 페이지 제작을 위한 마케팅 문구 생성 및 PPT 템플릿 자동화 스킬.

## Workflow Overview

전체 프로세스는 3단계로 구성된다:
1. **문구 생성**: 책 내용 분석 → 4컷 마케팅 문구 작성 → 추천 페이지 선정
2. **PPT 작업**: 템플릿에 문구와 페이지 번호 자동 삽입 (서식 완벽 보존)
3. **이미지 처리**: PDF에서 추천 페이지 추출 → PPT에 이미지 삽입 (향후 구현 예정)

---

## Step 1: 마케팅 문구 및 페이지 생성

### 1.1 책 내용 분석

책의 다음 요소들을 종합적으로 분석한다:
- **서문/들어가며**: 저자의 집필 의도와 독자 대상
- **목차**: 전체 구조와 다루는 주제들
- **대상 독자**: 누구를 위한 책인가
- **핵심 주제**: 책의 차별점과 강점

### 1.2 문구 작성 전략

**핵심 원칙:**
1. **실무적 이점 중심**: 독자가 얻을 수 있는 구체적 혜택에 초점
2. **기술 키워드 포함**: 검색성과 신뢰도를 위한 핵심 기술 용어 자연스럽게 배치
3. **차별점 강조**: 이 책만의 독특한 가치 제시
4. **액션 지향**: "배운다", "마스터한다", "구현한다" 등 능동적 표현 사용

**4컷 구성 전략:**

각 문구는 책의 서로 다른 핵심 가치를 다루어야 한다. 예를 들어 LLM 책의 경우:
- 1컷: 데이터 엔지니어링 (기초/입문)
- 2컷: 모델 최적화 (성능/효율)
- 3컷: 고급 기법/패턴 (전문성)
- 4컷: 실전 응용 (실무 활용)

### 1.3 추천 페이지 선정 기준

각 문구당 2개의 페이지를 선정한다:

**선정 기준:**
1. **시각적 임팩트**: 다이어그램, 플로우차트, 구조도가 있는 페이지 우선
2. **코드 예시**: 실제 구현 코드가 있어 실용성을 보여줄 수 있는 페이지
3. **핵심 개념 설명**: 해당 문구를 직접 뒷받침하는 내용
4. **완결성**: 단독으로도 이해 가능한 완결된 내용
5. **분산**: 책 전체에 고르게 분포 (앞/중/뒤 균형)

**배치 전략:**
- `page_left`: 첫 번째 페이지 (보통 더 기초적이거나 개념적인 내용)
- `page_right`: 두 번째 페이지 (보통 더 고급이거나 실전적인 내용)

### 1.4 출력 형식

```
문구 1: [책의 첫 번째 핵심 차별점]
추천 페이지(왼쪽): [페이지 번호]
추천 페이지(오른쪽): [페이지 번호]

문구 2: [두 번째 핵심 차별점]
추천 페이지(왼쪽): [페이지 번호]
추천 페이지(오른쪽): [페이지 번호]

문구 3: [세 번째 핵심 차별점]
추천 페이지(왼쪽): [페이지 번호]
추천 페이지(오른쪽): [페이지 번호]

문구 4: [네 번째 핵심 차별점]
추천 페이지(왼쪽): [페이지 번호]
추천 페이지(오른쪽): [페이지 번호]
```

### 1.5 참고 예제

`references/examples.md`에서 실제 작성 사례를 확인할 수 있다:
- LLM 디자인 패턴 책 예제
- 자바/스프링 실용주의 프로그래밍 예제
- AI 에이전트 구축 예제

---

## Step 2: PPT 템플릿에 문구 채우기 ⭐ 핵심

**CRITICAL:** PPT 템플릿 처리는 매우 정교해야 한다. 다음 원칙을 절대 지켜야 한다:

### 2.1 핵심 원칙

1. **원본 서식 절대 보존**: 템플릿의 폰트 크기, 이름, 굵기 등 모든 서식을 변경하지 않는다
2. **스크립트 필수 사용**: `scripts/fill_ppt_template.py`를 항상 사용한다
3. **직접 구현 금지**: python-pptx로 직접 구현하면 서식이 깨지기 쉽다

### 2.2 템플릿 구조

**제공되는 템플릿:** `assets/template.pptx`

**Placeholder 구조:**
- `{{문구}}`: 메인 마케팅 문구 (1개)
- `{{page_num_left}}`: 왼쪽 페이지 번호 (1개)
- `{{page_num_right}}`: 오른쪽 페이지 번호 (1개)
- 이미지 영역: 2개 (왼쪽/오른쪽)

### 2.3 스크립트 사용법

```python
import json
import subprocess

# 데이터 준비
slides_data = [
    {
        "text": "데이터 수집부터 정제, 증강까지! 고품질 LLM 구축의 기초가 되는 데이터 엔지니어링 패턴을 완벽하게 마스터합니다.",
        "page_left": "15",
        "page_right": "40"
    },
    {
        "text": "파인튜닝, 양자화, 프루닝 등 핵심 기법을 통해 모델 성능을 극대화하고 비용 효율적인 훈련 파이프라인을 설계합니다.",
        "page_left": "123",
        "page_right": "189"
    },
    {
        "text": "CoT, ToT, ReAct 등 최신 고급 프롬프팅 전략과 에이전틱 패턴을 적용해 스스로 추론하고 행동하는 자율 AI 시스템을 구현합니다.",
        "page_left": "332",
        "page_right": "343"
    },
    {
        "text": "단순한 검색 증강 생성(RAG)을 넘어, 그래프 기반 RAG와 하이브리드 검색 전략을 통해 환각 현상을 줄이고 답변의 정확도를 획기적으로 높입니다.",
        "page_left": "412",
        "page_right": "429"
    }
]

# 스크립트 실행
result = subprocess.run([
    'python3',
    '/mnt/skills/user/book-detail-page-creator/scripts/fill_ppt_template.py',
    '/mnt/skills/user/book-detail-page-creator/assets/template.pptx',
    '/mnt/user-data/outputs/도서명_상세페이지.pptx',
    json.dumps(slides_data, ensure_ascii=False)
], capture_output=True, text=True, cwd='/home/claude')

print(result.stdout)
if result.returncode != 0:
    print("Error:", result.stderr)
```

### 2.4 스크립트 동작 원리

1. **첫 번째 슬라이드 처리**
   - 각 shape를 순회하며 placeholder 텍스트 찾기
   - 원본 run의 서식(font.size, font.name, font.bold 등) 저장
   - 텍스트만 교체하고 서식 복원

2. **슬라이드 복제 (2~4번째)**
   - 원본 슬라이드와 동일한 레이아웃으로 빈 슬라이드 추가
   - 기본 shape 모두 제거
   - 원본 슬라이드의 각 shape를 XML 레벨에서 `deepcopy`
   - 복제된 shape를 새 슬라이드에 추가
   - 각 슬라이드의 데이터로 텍스트 교체 (서식 보존)

3. **서식 보존 메커니즘**
   ```python
   # 원본 서식 저장
   first_run = shape.text_frame.paragraphs[0].runs[0]
   font_size = first_run.font.size
   font_name = first_run.font.name
   font_bold = first_run.font.bold
   
   # 텍스트 교체
   shape.text_frame.clear()
   p = shape.text_frame.paragraphs[0]
   run = p.add_run()
   run.text = new_text
   
   # 서식 복원
   run.font.size = font_size
   run.font.name = font_name
   run.font.bold = font_bold
   ```

---

## Step 3: 추천 페이지 이미지 처리 (미구현)

추천 페이지를 이미지로 저장하여 PPT의 이미지 placeholder에 삽입.

**계획된 워크플로우:**
1. PDF에서 특정 페이지 추출 (pymupdf 사용)
2. 이미지로 변환 및 크기 조정
3. PPT의 이미지 placeholder에 삽입
4. 위치와 크기 자동 조정

**TODO:** 향후 구현 예정

---

## Common Pitfalls to Avoid

### ❌ 잘못된 방법 1: 직접 shape.text 수정
```python
# 서식이 깨진다!
shape.text = "새로운 텍스트"
```

### ❌ 잘못된 방법 2: 새 슬라이드에 레이아웃만 복사
```python
# 템플릿의 상세 디자인이 사라진다!
new_slide = prs.slides.add_slide(slide_layout)
for shape in original_slide.shapes:
    # 이 방식으로는 완벽한 복제가 안 된다
```

### ❌ 잘못된 방법 3: run.text로 직접 교체
```python
# 여러 run이 있으면 일부만 바뀐다!
for run in paragraph.runs:
    if "{{문구}}" in run.text:
        run.text = run.text.replace("{{문구}}", new_text)
```

### ✅ 올바른 방법: 스크립트 사용
```python
# 검증된 로직으로 서식 완벽 보존
subprocess.run(['python3', 'scripts/fill_ppt_template.py', ...])
```

---

## Resources

### Scripts
- `scripts/fill_ppt_template.py` - PPT 템플릿 처리 핵심 스크립트
  - 원본 서식 보존 로직 구현
  - XML 레벨 deepcopy로 슬라이드 복제
  - placeholder 자동 교체

### References
- `references/examples.md` - 문구 작성 예제 모음
  - 실제 책 3권의 상세 페이지 문구 사례
  - 작성 가이드라인 및 원칙
  - 페이지 선정 기준

### Assets
- `assets/template.pptx` - 표준 PPT 템플릿
  - {{문구}}, {{page_num_left}}, {{page_num_right}} placeholder 포함
  - 이미지 영역 2개 (왼쪽/오른쪽)
  - 파일 내용 수정 금지 (이름은 변경 가능)
