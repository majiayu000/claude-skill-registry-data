---
name: translation
description: 영어 ↔ 한국어 번역 스킬. 학술 논문, 기술 문서 번역 시 사용. Ollama gpt-oss:20b 모델 활용. 원문 아래 번역문 병렬 표시.
allowed-tools: Read, Write, Bash
---

# Translation Skill (번역 스킬)

로컬 LLM을 활용한 고품질 영어-한국어 양방향 번역 스킬.

## 모델 정보

- **모델명**: `gpt-oss:20b` (Ollama)
- **컨텍스트**: 8K tokens
- **최적 용도**: 학술 논문, 기술 문서, 일반 텍스트

## 사용 시점

이 스킬은 다음 상황에서 자동으로 활성화됩니다:
- "번역해줘", "translate" 키워드 포함 시
- 영어 문서를 한국어로 변환 요청 시
- 한국어 문서를 영어로 변환 요청 시
- PDF 파싱 후 번역 옵션 활성화 시

## 번역 규칙

### 1. 문단 단위 번역
- 한 문단씩 번역하여 컨텍스트 유지
- 원문 바로 아래에 번역문 배치

### 2. 출력 형식
```markdown
원문 텍스트 (영어 또는 한국어)

> **[번역]** 번역된 텍스트

---
```

### 3. 전문 용어 처리
- 학술 용어는 첫 등장 시 `영어(한국어)` 형태로 표기
- 예: `Transformer(트랜스포머)`
- 약어는 풀어서 번역 후 약어 유지

### 4. 번역하지 않는 항목
- 코드 블록 (```` ``` ````)
- 수식 (`$...$`, `$$...$$`)
- 참조 (`[1]`, `et al.`)
- 고유명사 (모델명, 회사명, 인명)

## 프롬프트 템플릿

### 영어 → 한국어
```
다음 영어 텍스트를 한국어로 번역하세요.
- 학술적이고 전문적인 어조를 유지하세요
- 전문 용어는 첫 등장 시 영어를 괄호 안에 병기하세요
- 문장 구조를 자연스러운 한국어로 재구성하세요

원문:
{text}

번역:
```

### 한국어 → 영어
```
Translate the following Korean text to English.
- Maintain academic and professional tone
- Keep proper nouns in their original form
- Ensure grammatically correct and fluent English

Original:
{text}

Translation:
```

## 스크립트 사용

### 단일 파일 번역
```bash
python scripts/translate_file.py input.md --direction en2ko --output output_translated.md
```

### 배치 번역
```bash
python scripts/batch_translate.py ./docs/ --direction en2ko --parallel
```

## 품질 개선 팁

1. **긴 문서**: 섹션별로 나누어 번역
2. **표/리스트**: 구조 유지하며 내용만 번역
3. **수식 설명**: 수식은 유지, 설명만 번역
4. **검토**: 번역 후 용어 일관성 확인

## 예시

### 입력
```markdown
## Introduction

Deep learning has revolutionized natural language processing...
```

### 출력
```markdown
## Introduction

Deep learning has revolutionized natural language processing...

> **[번역]** 딥러닝(Deep Learning)은 자연어 처리 분야에 혁명을 가져왔습니다...

---
```

## 관련 파일

- `src/translation/translator.py`: 메인 번역 모듈
- `scripts/translate_file.py`: CLI 번역 스크립트
- `scripts/batch_translate.py`: 배치 처리 스크립트
