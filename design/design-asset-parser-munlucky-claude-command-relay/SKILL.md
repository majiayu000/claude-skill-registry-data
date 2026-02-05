---
name: design-asset-parser
description: Parse Figma/PDF design exports to extract UI specs and draft design-spec.md and pending-questions.md. Use when analyzing design assets.
---

# Design Asset Parser Skill

> **목적**: 디자인 산출물(Figma export 이미지/CSS/HTML, 화면정의서 PDF)을 파싱하여 개발 스펙 초안 생성
> **출력**: `.claude/docs/tasks/{feature-name}/design-spec.md`, `pending-questions.md`
> **사용 시점**: 신규 기능 구현 전, 디자인 산출물이 제공되었을 때

---

## 역할

디자인 산출물에서 UI/기능 요구사항을 자동으로 추출하고, 개발자가 바로 구현할 수 있는 구조화된 스펙 문서를 생성합니다.

### 입력 파일 유형
1. **화면정의서 PDF**: `.claude/docs/디채오늘의문장/*.pdf` 등
2. **Figma export**: 이미지(PNG/JPG), CSS/HTML export
3. **디자인 가이드**: 색상/폰트/간격 토큰 정의

### 주요 기능
- PDF 텍스트/이미지 추출 (OCR 지원)
- CSS/HTML export에서 컴포넌트/스타일 토큰 추출
- UI 요소, 밸리데이션, 상태, 엣지 케이스 구조화
- 불명확한 요구사항 자동 검출 및 질문 생성

---

## 트리거

다음 상황에서 자동 또는 수동으로 호출:

### 자동 트리거
1. `.claude/docs/디채오늘의문장/` 디렉토리에 PDF 추가 감지
2. Figma export zip 파일 추가 감지
3. PM Agent가 신규 기능으로 분류 + 디자인 산출물 경로 발견

### 수동 트리거
```bash
# 사용자 요청 예시
"화면정의서 PDF를 파싱해서 개발 스펙 만들어줘"
"Figma export CSS를 분석해서 스타일 토큰 정리해줘"
```

---

## 동작 흐름

### 1단계: 입력 파일 확인 (1분)
```markdown
입력 파일 목록:
- 화면정의서: .claude/docs/디채오늘의문장/배치관리_v3.pdf
- Figma export: .claude/docs/디채오늘의문장/batch-management-export.zip
- 기능명: batch-management
```

### 2단계: PDF 파싱 (3-5분)
**작업 내용**:
- PDF 텍스트 추출 (Read 도구로 PDF 읽기)
- 이미지 추출 및 OCR (필요 시)
- 섹션별 구조 파악 (화면 구성, 필드 정의, 기능 요구사항)

**추출 항목**:
- 페이지/모달/탭 구조
- Form 필드: 이름, 타입, 필수 여부, 기본값, 밸리데이션
- Table/Grid: 컬럼명, 정렬/필터, 페이징, 빈 상태
- 버튼/액션: 라벨, 동작, 허용/비활성 조건
- 상태/에러/로딩: 메시지 규칙

### 3단계: CSS/HTML 파싱 (2-3분)
**작업 내용**:
- CSS 변수 추출 (색상, 폰트, 간격)
- 컴포넌트 클래스 및 변형 추출 (Primary/Secondary/Disabled)
- HTML 구조 파악 (레이아웃, 컴포넌트 계층)

**추출 항목**:
```css
/* 스타일 토큰 */
--color-primary: #1a73e8;
--font-size-base: 14px;
--spacing-md: 16px;
```

### 4단계: 스펙 초안 작성 (5-10분)
**출력 파일**: `.claude/docs/tasks/{feature-name}/design-spec.md`

기본 구조:
```markdown
# 디자인 기반 개발 스펙

## 화면 개요
- 페이지 구조
- 주요 플로우

## UI 요소 및 동작
### Form 필드
| 필드명 | 타입 | 필수 | 기본값 | 밸리데이션 |
|--------|------|------|--------|------------|

### Table 컬럼
| 컬럼명 | 정렬 | 필터 | 비고 |
|--------|------|------|------|

### 버튼/액션
- 버튼명: 동작 설명

### 상태/에러/로딩
- 로딩: Spinner 위치
- 성공/에러: 메시지 규칙

## 스타일 토큰
- 색상, 폰트, 간격

## 자산 매니페스트
- 이미지/아이콘 목록

## 추출 근거
- 출처 파일, 페이지 번호

## 미해결/질문
- 불명확한 요구사항 목록
```

### 5단계: 미해결 질문 기록 (1-2분)
**출력 파일**: `.claude/docs/tasks/{feature-name}/pending-questions.md`

```markdown
# 미해결 질문 (Pending Questions)

## 날짜: {YYYY-MM-DD}

### 우선순위: HIGH
1. **질문 제목**
   - 출처: design-spec.md 섹션
   - 질문: 구체적인 질문
   - 영향: 구현/설계에 미치는 영향
```

### 6단계: 결과 요약 및 다음 단계 안내
```markdown
✅ Design Asset Parser Skill 완료

## 산출물
- design-spec.md: N개 UI 요소, N개 스타일 토큰
- pending-questions.md: N개 미해결 질문

## 다음 단계
1. pending-questions.md의 HIGH 우선순위 질문 해결
2. Requirements Analyzer Agent 호출
3. Context Builder Agent 호출
```

---

## 프롬프트 템플릿

```markdown
당신은 Design Asset Parser Skill입니다.
디자인 산출물을 읽고 개발 스펙을 구조화합니다.

## 입력
- 디자인 파일 경로: {designPaths}
- 대상 기능명: {featureName}
- 기존 design-spec.md 존재 여부: {hasSpec}

## 작업
1. PDF/Figma export 파일 읽기 (Read 도구 사용)
2. UI 요소 추출 (Form/Table/Button/State)
3. 밸리데이션/엣지 케이스 명시
4. 스타일 토큰 추출 (CSS 있을 때)
5. 자산 매니페스트 작성
6. 미해결/질문 정리

## 출력
- `.claude/docs/tasks/{feature-name}/design-spec.md`: 구조화된 개발 스펙
- `.claude/docs/tasks/{feature-name}/pending-questions.md`: 미해결 질문 목록

## 품질 기준
- UI 요소는 테이블 형식으로 정리
- 밸리데이션 규칙 명확히 기술 (길이/패턴/범위)
- 불명확한 요구사항은 질문으로 변환
- 우선순위 명시 (HIGH/MEDIUM/LOW)
```

---

## 사용 예시

### 예시 1: PDF 화면정의서 파싱
```
사용자: "화면정의서 PDF를 파싱해서 개발 스펙 만들어줘.
         경로: .claude/docs/디채오늘의문장/배치관리_v3.pdf
         기능명: batch-management"

Design Asset Parser Skill 실행 →
1. PDF 읽기 (Read 도구)
2. 섹션별 파싱 (화면 구성, 필드 정의, 기능 요구사항)
3. design-spec.md 생성
4. pending-questions.md 생성 (불명확한 부분)

산출물:
- .claude/docs/tasks/batch-management/design-spec.md
- .claude/docs/tasks/batch-management/pending-questions.md
```

### 예시 2: Figma CSS export 파싱
```
사용자: "Figma CSS export를 분석해서 스타일 토큰 정리해줘.
         경로: .claude/docs/디채오늘의문장/batch-ui-export.css
         기능명: batch-management"

Design Asset Parser Skill 실행 →
1. CSS 파일 읽기
2. CSS 변수 추출 (--color-*, --font-*, --spacing-*)
3. 컴포넌트 클래스 추출 (.button--primary, .button--disabled)
4. design-spec.md의 "스타일 토큰" 섹션 업데이트

산출물:
- design-spec.md (스타일 토큰 섹션 갱신)
```

### 예시 3: PDF + CSS 동시 파싱
```
사용자: "화면정의서 PDF와 Figma CSS를 함께 파싱해줘.
         PDF: .claude/docs/디채오늘의문장/배치관리_v3.pdf
         CSS: .claude/docs/디채오늘의문장/batch-ui-export.css
         기능명: batch-management"

Design Asset Parser Skill 실행 →
1. PDF 파싱 → UI 요소, 기능 요구사항
2. CSS 파싱 → 스타일 토큰
3. 두 결과 병합 → design-spec.md
4. 불일치/충돌 사항 → pending-questions.md

산출물:
- design-spec.md (UI + 스타일 통합)
- pending-questions.md (충돌 사항 질문)
```

---

## 통합 워크플로우

### Design Asset Parser → Design Spec Extractor Agent
```
1. Design Asset Parser Skill:
   - 입력: PDF/CSS 파일
   - 출력: design-spec.md (초안), pending-questions.md

2. 사용자:
   - pending-questions.md 확인
   - HIGH 우선순위 질문 답변

3. Design Spec Extractor Agent:
   - design-spec.md 검토
   - CLAUDE.md 규칙과 비교
   - 프로젝트 패턴 반영
   - 최종 design-spec.md 생성

4. Requirements Analyzer Agent:
   - design-spec.md 기반 사전 합의서 생성
```

---

## 참고 정보

### 프로젝트별 디자인 산출물 경로
- **디채 오늘의 문장**: `.claude/docs/디채오늘의문장/*.pdf`
- **Figma export**: `.claude/docs/디채오늘의문장/*.zip`, `*.css`, `*.html`

### 기존 프로젝트 패턴 (CLAUDE.md 준수)
- Entity-Request 분리
- API 프록시 패턴
- 활동 로그 헤더 규칙
- fp-ts Either 패턴
- TypeScript strict mode

### 주의사항
1. **PDF 파싱 제약**: 이미지 위주 PDF는 OCR 필요
2. **CSS 파싱 제약**: Inline 스타일은 추출 불가
3. **자동화 한계**: 애매한 요구사항은 질문으로 남기기
4. **버전 관리**: design-spec.md 변경 시 버전 히스토리 기록
