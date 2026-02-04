---
name: Obsidian Refine Content
description: Obsidian vault의 기존 파일 내용을 분석하고, 사용자 확인 후 템플릿에 맞춰 정리/보완합니다. 틀린 부분은 수정하되 최종 문서에는 언급하지 않고 깔끔하게 완성합니다.
---

# Obsidian Refine Content Skill

이 Skill은 Obsidian vault의 기존 파일을 읽어서 분석하고, **사용자 확인을 받은 후** 내용을 정리, 보완, 링크 연결하는 역할을 합니다.

## 핵심 워크플로우

1. **분석**: 문서를 읽고 보충/수정이 필요한 부분 파악
2. **확인**: AskUserQuestion으로 사용자에게 계획 확인
3. **실행**: 승인받은 내용만 반영
4. **완성**: 틀린 부분 언급 없이 깔끔한 문서 완성

## Vault 경로
`/Users/teamsparta/Library/Mobile Documents/iCloud~md~obsidian/Documents/for-dev`

## 템플릿 경로
- **Information 템플릿**: `/Users/teamsparta/Library/Mobile Documents/iCloud~md~obsidian/Documents/for-dev/template/Information.md`
- **Repository 템플릿**: `/Users/teamsparta/Library/Mobile Documents/iCloud~md~obsidian/Documents/for-dev/template/Repository.md`
- **Code 템플릿**: `/Users/teamsparta/Library/Mobile Documents/iCloud~md~obsidian/Documents/for-dev/template/Code.md`

---

## 사용 시나리오

### 1. Frontend 지식 파일 정리

**사용자 입력 예시**:
- "useEffect.md 정리해줘"
- "Context Api 파일 보완해줘"
- "이 파일 정리해줘" (파일 경로 제공 또는 대화 맥락에서 파악)

**동작**:
1. 대상 파일 읽기
2. Information 템플릿 구조에 맞춰 섹션 재구성
3. 내용 보충 (웹 검색 또는 지식 기반)
4. 관련 파일 링크 추가
5. Frontmatter 검증 및 보완
6. 파일 업데이트

### 2. Repository 프로젝트 문서화

**사용자 입력 예시**:
- "dev_proxy.md 분석해서 정리해줘"
- "모두AI 프로젝트 문서 보완해줘"

**동작**:
1. 프로젝트 폴더 내 코드 파일 탐색
2. 주요 파일 읽어서 기능 파악
3. 기술 스택 자동 추출
4. Repository 템플릿 구조에 맞춰 문서 작성
5. Frontmatter 보완 (tech-stack, project-type, description)
6. 파일 업데이트

### 3. Code 파일 분석 및 문서화

**사용자 입력 예시**:
- "config.md 분석해줘"
- "utils 파일 정리해줘"

**동작**:
1. 대상 파일 읽기 (Code 템플릿)
2. "## 코드" 섹션의 코드 분석
3. 개요 작성 (코드가 무엇을 하는지)
4. 주요 함수/클래스 추출 및 설명
5. 사용 방법 작성
6. 주의사항 작성 (있는 경우)
7. Frontmatter 보완 (language, file-path)
8. 파일 업데이트

### 4. 관련 정보 링크 연결

**동작**:
- 본문에서 키워드 추출
- Vault 내 관련 파일 검색
- Obsidian 링크 형식(`[[파일명]]`)으로 자동 연결

---

## 템플릿 판별

파일의 frontmatter를 확인하여 어떤 템플릿을 따를지 결정:

### Repository 템플릿
- `tech-stack` 필드 존재
- `project-type` 필드 존재
- 경로: `Team Sparta/repo/` 하위의 프로젝트 루트 .md 파일

### Code 템플릿
- `language` 필드 존재
- `file-path` 필드 존재
- 경로: `Team Sparta/repo/{프로젝트}/` 하위의 개별 파일
- 본문에 "## 코드" 섹션 존재

### Information 템플릿
- 위 조건에 해당하지 않는 모든 .md 파일
- 경로: `Frontend/` 하위

---

## 정리 작업 워크플로우

### **STEP 1: 전체 문서 분석**

1. 대상 파일 읽기
2. 템플릿 타입 판별 (Information/Repository/Code)
3. 다음 항목 분석:
   - Frontmatter 완성도 (필수 필드 누락 여부)
   - 섹션 구조 (템플릿과 일치 여부)
   - 각 섹션 내용 완성도 (비어있거나 불충분한 부분)
   - 기술적으로 부정확한 내용 (사실과 다른 정보)
   - 관련 정보 링크 누락

4. Repository 타입인 경우 코드 분석:
   - 프로젝트 폴더 내 파일 탐색
   - tech-stack, project-type, 주요 기능 파악

### **STEP 2: 보충 계획 사용자 확인**

분석 결과를 바탕으로 **AskUserQuestion 도구를 사용하여** 다음 질문:

```
📋 문서 보충 계획

다음 부분을 보충하려고 합니다:

**비어있거나 불충분한 섹션**:
- [섹션명]: [보충할 내용 간략히 설명]
- [섹션명]: [보충할 내용 간략히 설명]

**추가할 관련 링크**:
- [[파일1]], [[파일2]] ...

**보충할 Frontmatter**:
- tags: [추천 태그들]
- (Repository인 경우) tech-stack: [추출된 스택]

위 계획대로 진행할까요?
- 진행 (Recommended)
- 일부만 진행 (어떤 부분을 제외할지 알려주세요)
```

### **STEP 3: 틀린 부분 수정 계획 확인**

기술적으로 부정확한 내용이 발견된 경우 **AskUserQuestion 도구를 사용하여** 질문:

```
⚠️ 수정이 필요한 부분 발견

다음 내용이 부정확합니다:

**[섹션명]**:
현재: "[기존 내용]"
수정: "[정확한 내용]"

**[섹션명]**:
현재: "[기존 내용]"
수정: "[정확한 내용]"

위와 같이 수정할까요?
- 모두 수정 (Recommended)
- 일부만 수정 (어떤 부분을 수정할지 알려주세요)
- 수정하지 않음
```

**중요**: 틀린 부분이 없으면 이 단계는 건너뜀

### **STEP 4: 완전한 설명으로 보충**

사용자 확인 후 문서 업데이트:

1. **구조 재구성**
   - Information 템플릿 섹션: `# 제목` → `## 개요` → `## 주요 내용` → `## 핵심 포인트` → `## 참고 자료`
   - Repository 템플릿 섹션: `# 프로젝트명` → `## 프로젝트 개요` → `## 주요 기능` → `## 설정 방법` → `## 참고 자료`
   - Code 템플릿 섹션: `# 파일명` → `## 개요` → `## 코드` → `## 주요 함수/클래스` → `## 사용 방법` → `## 주의사항` → `## 참고 자료`
   - 기존 내용을 적절한 섹션으로 재배치
   - 누락된 섹션은 보충된 내용으로 채움

2. **내용 보충**
   - Information 파일: 개요, 주요 내용, 핵심 포인트를 명확하고 완전하게 작성
   - Repository 파일: 프로젝트 개요, 주요 기능, tech-stack 작성
   - Code 파일: 코드 분석 (개요, 주요 함수/클래스, 사용 방법, 주의사항)

3. **Frontmatter 보완**
   - 공통: `created-at`, `tags`, `color`
   - Repository: `tech-stack`, `project-type`, `description`
   - Code: `language`, `file-path`

4. **관련 정보 링크 추가**
   - Vault 내 관련 .md 파일을 `[[파일명]]` 형식으로 링크
   - 같은 키워드는 첫 출현에만 링크
   - 코드 블록이나 제목은 링크하지 않음

### **STEP 5: 틀린 부분 언급 금지**

**중요한 작성 원칙**:
- ❌ "기존에는 잘못 작성되었지만..." 같은 표현 금지
- ❌ "틀린 부분을 수정했습니다" 같은 언급 금지
- ❌ "이전 설명은 부정확했으나..." 같은 표현 금지
- ✅ 단순히 정확한 사실만 깔끔하게 작성
- ✅ 완성된 문서에는 과거의 실수나 오류에 대한 언급 없음
- ✅ 마치 처음부터 올바르게 작성된 것처럼 자연스럽게

**예시**:
- 나쁜 예: "useEffect는 라이프사이클 메서드라고 잘못 설명되어 있었지만, 실제로는 side effect를 처리하는 Hook입니다."
- 좋은 예: "useEffect는 컴포넌트에서 side effect를 처리하기 위한 React Hook입니다."

### **STEP 6: 사실만 깔끔하게 담긴 글 완성**

최종 문서는 다음 기준을 충족:
- 기술적으로 정확한 정보만 포함
- 명확하고 간결한 설명
- 템플릿 구조 준수
- 적절한 관련 링크 포함
- 과거의 오류나 수정 사항에 대한 언급 없음
- 전문적이고 깔끔한 문서 완성

---

## 관련 정보 링크 생성

### 링크 대상 파일 찾기

1. Vault 내 모든 .md 파일 목록 수집:
   - `Frontend/` 하위 모든 파일
   - `Team Sparta/repo/` 하위 프로젝트 .md 파일
   - 업무일지 제외

2. 파일명 추출 (확장자 제외):
   - `useEffect.md` → `useEffect`
   - `Context Api.md` → `Context Api`
   - `Hash Routing.md` → `Hash Routing`

### 키워드 매칭 및 링크 생성

**매칭 규칙**:
- 대소문자 구분 없이 매칭
- 전체 단어 매칭 (부분 매칭 아님)
- 이미 링크된 부분(`[[...]]`)은 제외

**예시**:
```
원본: "Closure를 사용하면 변수에 접근할 수 있다"
변환: "[[Closure]]를 사용하면 변수에 접근할 수 있다"

원본: "Observer Pattern으로 상태 변경을 감지한다"
변환: "[[Observer Pattern]]으로 상태 변경을 감지한다"

원본: "useRef를 통해 DOM에 접근한다"
변환: "[[useRef]]를 통해 [[DOM]]에 접근한다"
```

**주의사항**:
- 같은 키워드는 첫 출현에만 링크 (중복 링크 방지)
- 코드 블록(```) 내부는 링크하지 않음
- 제목(#)은 링크하지 않음

---

## 코드 분석 (Repository 파일)

### 분석 대상

프로젝트 폴더 내 파일들:
- JavaScript/TypeScript: `.js`, `.ts`, `.jsx`, `.tsx`
- Python: `.py`
- 설정 파일: `package.json`, `requirements.txt`, `Cargo.toml` 등

### 추출 정보

1. **기술 스택**:
   - package.json의 dependencies
   - import/require 문에서 라이브러리 추출
   - 파일 확장자로 언어 파악

2. **주요 기능**:
   - 함수명, 클래스명 추출
   - 주석으로 설명된 부분 참고
   - 파일 구조로 기능 추론

3. **프로젝트 타입**:
   - `src/components/` 존재 → frontend
   - `src/routes/`, `src/controllers/` → backend
   - CLI 관련 코드 → tool
   - 둘 다 있으면 → fullstack

---

## 출력 형식

### STEP 1 완료 후 (분석 결과):
```
📊 문서 분석 완료

📄 파일: Frontend/React/useEffect.md
📋 템플릿 타입: Information

🔍 분석 결과:
- Frontmatter: tags 비어있음
- 섹션 구조: 템플릿과 일치
- 비어있는 섹션: 개요, 주요 내용, 핵심 포인트
- 관련 파일 발견: useState, useRef, useCallback, Component

다음 단계에서 보충 계획을 확인받겠습니다.
```

### STEP 2 (AskUserQuestion 사용):
AskUserQuestion 도구로 사용자에게 보충 계획 확인 요청

### STEP 3 (틀린 부분이 있는 경우만):
AskUserQuestion 도구로 사용자에게 수정 계획 확인 요청

### STEP 4-6 완료 후 (최종 결과):
```
✅ 문서 정리 및 보충 완료!

📄 파일: Frontend/React/useEffect.md

📝 보충된 내용:
- Frontmatter: tags 추가 (front-end, react, hooks)
- 개요: useEffect의 정의와 목적 작성
- 주요 내용: 기본 사용법, 의존성 배열, cleanup 함수 설명
- 핵심 포인트: 주요 사용 사례 3가지 작성
- 관련 링크: [[useState]], [[useRef]], [[useCallback]] 추가

✨ 깔끔하고 정확한 문서가 완성되었습니다!
```

Repository 파일 완료 시:
```
✅ 프로젝트 문서 정리 완료!

📄 파일: Team Sparta/repo/dev_proxy/dev_proxy.md

🔍 코드 분석:
- 기술 스택: AWS, Proxy, saml2aws
- 프로젝트 타입: tool
- 주요 기능: dev-proxy-run, dev-proxy-config, AWS 세션 관리

📝 보충된 내용:
- Frontmatter: tech-stack, project-type, description 추가
- 프로젝트 개요: 프로젝트 목적 및 배경 작성
- 주요 기능: 3가지 핵심 기능 상세 설명
- 설정 방법: 설치 및 사용 가이드 작성

✨ 깔끔하고 정확한 문서가 완성되었습니다!
```

Code 파일 완료 시:
```
✅ 코드 분석 및 문서화 완료!

📄 파일: Team Sparta/repo/dev_proxy/config.md

🔍 코드 분석:
- 언어: javascript
- 주요 함수: configureProxy(), setRoutes(), validateConfig()
- 코드 라인수: 45줄

📝 보충된 내용:
- Frontmatter: language, file-path 추가
- 개요: 코드 목적 한 문장 요약
- 주요 함수/클래스: 3개 함수의 역할 및 파라미터 설명
- 사용 방법: 실제 사용 예시 코드 작성
- 주의사항: 설정 시 주의할 점 2가지 작성

✨ 깔끔하고 정확한 문서가 완성되었습니다!
```

---

## 예외 처리

1. **파일을 찾을 수 없는 경우**:
   - Vault 내 파일명 검색
   - 여러 파일이 매칭되면 목록 표시 후 선택 요청
   - 없으면: "❌ 파일을 찾을 수 없습니다: {파일명}"

2. **업무일지 파일인 경우**:
   - 메시지: "⚠️ 업무일지는 자동 정리 대상이 아닙니다. 수동으로 관리해주세요."

3. **템플릿 구조가 너무 다른 경우**:
   - 기존 구조 최대한 보존
   - 메시지: "⚠️ 파일 구조가 템플릿과 많이 다릅니다. 주요 내용만 보완했습니다."

4. **코드 분석 실패**:
   - 메시지: "⚠️ 코드 분석에 실패했습니다. 수동으로 tech-stack과 description을 입력해주세요."

---

## 중요 지시사항

1. **사용자 확인 필수**: AskUserQuestion 도구를 사용하여 보충 계획과 수정 계획을 반드시 확인받음
2. **단계별 진행**:
   - Phase 1: 분석 후 결과 출력
   - Phase 2: AskUserQuestion으로 사용자 확인
   - Phase 3: 승인받은 내용만 실행
3. **틀린 부분 언급 금지**: 최종 문서에는 과거의 오류나 수정 사항에 대한 언급 절대 금지
4. **자연스러운 완성**: 마치 처음부터 올바르게 작성된 것처럼 깔끔하게 작성
5. **기존 내용 존중**: 사용자가 작성한 내용 중 사용자가 승인한 부분만 수정
6. **링크는 신중하게**: 명확한 키워드만 링크, 과도한 링크는 가독성 저해
7. **코드 분석은 참고용**: 100% 정확하지 않을 수 있으므로 사용자 확인 필수
8. **템플릿 구조 준수**: 새 섹션을 임의로 추가하지 않음
9. **정확성 최우선**: 기술적으로 정확한 정보만 포함

---

## 작업 순서

### Phase 1: 분석
1. 대상 파일 찾기 및 읽기
2. 템플릿 타입 판별 (Information/Repository/Code)
3. 전체 문서 분석:
   - Frontmatter 완성도
   - 섹션 구조
   - 내용 완성도
   - 기술적 부정확성
   - 관련 링크 누락
4. Repository인 경우 코드 분석 (tech-stack, 주요 기능 파악)
5. Vault 내 관련 .md 파일 목록 수집
6. **분석 결과 출력**

### Phase 2: 사용자 확인
7. **AskUserQuestion 도구 사용**: 보충 계획 확인 요청
8. **AskUserQuestion 도구 사용** (틀린 부분이 있는 경우만): 수정 계획 확인 요청
9. 사용자 응답 대기

### Phase 3: 실행
10. 사용자 확인 사항 반영하여 문서 업데이트:
    - 구조 재구성
    - 내용 보충 (사용자가 승인한 항목만)
    - Frontmatter 보완
    - 관련 링크 추가
    - 틀린 부분 수정 (사용자가 승인한 항목만)
11. **중요**: 최종 문서에는 과거의 오류나 틀린 부분에 대한 언급 절대 금지
12. 파일 업데이트 (Edit 도구 사용)
13. **최종 결과 출력**

### 핵심 원칙
- **사용자 승인 없이는 절대 파일 수정하지 않음**
- **AskUserQuestion 도구를 반드시 사용하여 계획 확인**
- **틀린 부분이 있어도 최종 문서에는 언급하지 않고 자연스럽게 수정**
- **정확한 사실만 깔끔하게 작성**
