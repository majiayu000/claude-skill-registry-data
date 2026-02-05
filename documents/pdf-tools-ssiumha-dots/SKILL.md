---
name: pdf-tools
description: PDF 문서를 분석하고 내용을 추출합니다. PDF 읽기, 요약, 특정 정보 검색, UI/디자인 확인이 필요할 때 사용하세요. 자동으로 Markdown 변환과 페이지 이미지 export를 수행합니다.
---

# PDF Tools

PDF 문서를 Markdown 형식으로 변환하여 Claude가 읽고 처리할 수 있도록 합니다.

## Instructions

### 워크플로우: 변환 → 검증 → 정리 → 제공

#### Step 1: 환경 준비 (최초 1회만)
```bash
mise install && mise run setup
```

#### Step 2: PDF 변환 실행

**기본 변환 (Markdown만):**
```bash
mise run convert -- <pdf_path> -o <output_path>
```

**페이지 이미지 export (권장):**
```bash
mise run convert -- <pdf_path> --export-images -o <output_path>
```

이 옵션은 각 페이지를 JPG 이미지로 `<basename>_pages/` 폴더에 저장합니다.
텍스트 변환이 부정확하거나 UI/디자인 문서의 경우 이미지를 Read 도구로 직접 분석할 수 있습니다.

#### Step 3: 결과 검증 및 분석

**텍스트 기반 PDF:**
- Read 도구로 출력 Markdown을 읽고 품질 확인
- 필요시 Edit 도구로 자동 정리

**UI/디자인 PDF (이미지 export 사용):**
- `<basename>_pages/page_001.jpg` 등의 이미지 파일을 Read 도구로 직접 확인
- 시각적 정보가 중요한 경우 이미지 분석을 우선 사용

#### Step 4: 자동 정리 (텍스트 변환 품질 개선)
변환 후 **반드시** Read 도구로 출력 Markdown을 읽고 품질 문제를 확인하세요.

**다음 문제를 발견하면 Edit 도구로 자동 수정:**
1. **중복 테이블 열**: 동일한 내용이 여러 열에 반복되면 제거
2. **과도한 `<br>` 태그**: 실제 줄바꿈(`\n\n`)으로 변환하여 가독성 개선
3. **빈 테이블**: 의미 없는 내용(`•`, `---` 만 있는 테이블) 제거
4. **섹션 구조 부족**: 필요시 `## Page N` 또는 `## 섹션명` 헤더 추가

**정리 생략 조건:**
- 이미 깔끔하게 변환된 경우
- 내용이 간단하고 문제가 없는 경우
- 사용자가 원본 그대로 요청한 경우

#### Step 4: 사용자에게 제공
정리된 Markdown을 요약하거나 요청받은 분석을 수행하여 제공합니다.

## Examples

### Example 1: PDF를 Markdown으로 변환
```
User: "이 PDF를 Markdown으로 변환해줘"
Assistant:
1. mise run convert -- /path/to/document.pdf -o /path/to/document.md
2. Read /path/to/document.md (처음 100줄 확인)
3. 품질 문제 발견 시 Edit로 자동 정리
4. 사용자에게 변환 완료 알림 및 내용 요약 제공
```

### Example 2: PDF 내용 요약 (자동 정리 포함)
```
User: "invoice.pdf 내용을 요약해줘"
Assistant:
1. mise run convert -- invoice.pdf
2. Read invoice.md
3. 중복 테이블 열, <br> 태그 발견 → Edit로 정리
4. 정리된 내용을 분석하여 요약 제공
```

### Example 3: PDF에서 특정 정보 추출
```
User: "research_paper.pdf에서 실험 결과 부분만 보여줘"
Assistant:
1. mise run convert -- research_paper.pdf
2. Read research_paper.md
3. 필요시 섹션 헤더 추가하여 구조 개선
4. Markdown에서 실험 결과 섹션을 찾아 제공
```

## Technical Details

상세한 구현 사항과 트러블슈팅은 `REFERENCE.md`를 참조하세요.
