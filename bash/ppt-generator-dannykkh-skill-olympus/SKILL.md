---
name: ppt-generator
description: PPT/프레젠테이션 생성 요청 시 사용. .pptx 파일 언급 시 자동 트리거. python-pptx 기반, 템플릿 활용, 차트/표/이미지 지원.
---

# PPT Generator

python-pptx를 활용하여 템플릿 기반의 전문적인 PowerPoint 프레젠테이션을 생성합니다.

## 사용법

```
/ppt-generator 분기별 실적 보고서 PPT 만들어줘
/ppt-generator --template company.pptx 신제품 소개 자료
/ppt-generator 이 마크다운 내용으로 PPT 생성해줘
```

## 요구사항

```bash
pip install python-pptx Pillow
```

## 템플릿

**번들 템플릿 파일은 제공하지 않습니다.** python-pptx의 기본 테마로 생성하거나, 직접 만든 `.pptx`를 템플릿으로 전달할 수 있습니다.

```python
PPTGenerator()                       # 기본 테마
PPTGenerator("my-template.pptx")     # 사용자 제공 템플릿
```

`template_path`가 없거나 파일이 존재하지 않으면 기본 테마로 폴백합니다(`scripts/pptx_helpers.py:42-45`).

## 핵심 코드

### 기본 PPT 생성

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

class PPTGenerator:
    """템플릿 기반 PPT 생성기"""

    def __init__(self, template_path: str | None = None):
        if template_path and Path(template_path).exists():
            self.prs = Presentation(template_path)
        else:
            self.prs = Presentation()
        self._setup_slide_layouts()

    def _setup_slide_layouts(self):
        """슬라이드 레이아웃 매핑"""
        self.layouts = {
            'title': 0,           # 제목 슬라이드
            'title_content': 1,   # 제목 + 내용
            'section': 2,         # 섹션 헤더
            'two_content': 3,     # 2단 레이아웃
            'comparison': 4,      # 비교
            'title_only': 5,      # 제목만
            'blank': 6,           # 빈 슬라이드
            'content_caption': 7, # 내용 + 캡션
            'picture_caption': 8, # 그림 + 캡션
        }

    def add_title_slide(self, title: str, subtitle: str = ""):
        layout = self.prs.slide_layouts[self.layouts['title']]
        slide = self.prs.slides.add_slide(layout)
        slide.shapes.title.text = title
        if subtitle and len(slide.placeholders) > 1:
            slide.placeholders[1].text = subtitle
        return slide

    def add_content_slide(self, title: str, bullets: list[str]):
        layout = self.prs.slide_layouts[self.layouts['title_content']]
        slide = self.prs.slides.add_slide(layout)
        slide.shapes.title.text = title
        body = slide.placeholders[1]
        tf = body.text_frame
        tf.clear()
        for i, bullet in enumerate(bullets):
            if i == 0:
                tf.paragraphs[0].text = bullet
            else:
                p = tf.add_paragraph()
                p.text = bullet
                p.level = 0
        return slide

    def add_two_column_slide(self, title: str, left: list[str], right: list[str]):
        layout = self.prs.slide_layouts[self.layouts['two_content']]
        slide = self.prs.slides.add_slide(layout)
        slide.shapes.title.text = title
        for placeholder_idx, items in [(1, left), (2, right)]:
            tf = slide.placeholders[placeholder_idx].text_frame
            tf.clear()
            for i, text in enumerate(items):
                if i == 0:
                    tf.paragraphs[0].text = text
                else:
                    p = tf.add_paragraph()
                    p.text = text
        return slide

    def add_image_slide(self, title: str, image_path: str, caption: str = ""):
        layout = self.prs.slide_layouts[self.layouts['title_only']]
        slide = self.prs.slides.add_slide(layout)
        slide.shapes.title.text = title
        slide.shapes.add_picture(image_path, Inches(1.5), Inches(2), width=Inches(7))
        if caption:
            txBox = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
            txBox.text_frame.paragraphs[0].text = caption
            txBox.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        return slide

    def save(self, output_path: str):
        self.prs.save(output_path)
        print(f"PPT 저장 완료: {output_path}")
```

> 표, 차트, 마크다운→PPT, JSON→PPT 변환 코드 및 전체 사용 예시: [references/code-examples.md](references/code-examples.md)

## 템플릿 팁

### 좋은 템플릿 만드는 법

1. **마스터 슬라이드 정의**
   - PowerPoint에서 보기 → 슬라이드 마스터
   - 각 레이아웃에 플레이스홀더 배치
   - 색상 테마, 폰트 설정

2. **플레이스홀더 활용**
   ```
   Layout 0: 제목 슬라이드 (Title, Subtitle)
   Layout 1: 제목+내용 (Title, Body)
   Layout 2: 섹션 헤더
   Layout 3: 2단 (Title, Left, Right)
   Layout 5: 제목만 (이미지/차트용)
   Layout 6: 빈 슬라이드
   ```

3. **브랜드 요소 포함**
   - 로고 위치 고정
   - 푸터 (페이지 번호, 날짜)
   - 색상 팔레트 정의

## Helper Scripts

이 스킬에는 재사용 가능한 헬퍼 스크립트가 포함되어 있습니다.
SKILL.md의 `PPTGenerator` 클래스 없이 슬라이드를 빠르게 조합할 때 사용하세요.

| 스크립트 | 용도 |
|---------|------|
| `scripts/pptx_helpers.py` | python-pptx 기반 슬라이드 생성 헬퍼 (타이틀, 불릿, 이미지, 차트, 테이블) |

```bash
# 설치
pip install python-pptx Pillow

# 직접 실행 (샘플 PPT 생성)
python scripts/pptx_helpers.py
```

주요 함수:

| 함수 | 역할 |
|------|------|
| `create_presentation(title, subtitle, author)` | 타이틀 슬라이드 포함 Presentation 생성 |
| `add_title_slide(prs, title, subtitle)` | 타이틀 슬라이드 추가 |
| `add_content_slide(prs, title, bullets)` | 불릿 목록 슬라이드 추가 (들여쓰기 지원) |
| `add_image_slide(prs, title, image_path, caption)` | 이미지 + 캡션 슬라이드 추가 |
| `add_chart_slide(prs, title, chart_data, chart_type)` | 막대/꺾은선/파이 차트 슬라이드 추가 |
| `add_table_slide(prs, title, headers, rows)` | 교번 색상 테이블 슬라이드 추가 |

---

## 체크리스트

- [ ] python-pptx 설치됨
- [ ] (선택) 사용자 템플릿 `.pptx` 준비 — 없으면 기본 테마
- [ ] 이미지 경로 확인 (절대 경로 권장)
- [ ] 한글 폰트 지원 확인
- [ ] 출력 경로 쓰기 권한 확인

## 관련 명령어

- `/ppt-generator` - 이 스킬 실행
- `/erd-designer` - ERD 다이어그램 생성 (Mermaid)
- `/docker-deploy` - 배포 환경 구성
