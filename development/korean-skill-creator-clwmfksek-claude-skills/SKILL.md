---
name: korean-skill-creator
description: 한글 기반 클로드 스킬 자동 생성 도구. 사용자가 "클로드 스킬을 만들어줘" 또는 "[요구사항] 스킬 만들어줘"라고 요청할 때 사용. Progressive disclosure 원칙을 따르는 한글 문서 구조(SKILL.md + references/)를 자동으로 생성하고, 실전 예시를 포함한 일관성 있는 스킬 템플릿을 제공.
---

# 한글 클로드 스킬 생성기

## 개요 (Overview)

사용자의 요구사항을 바탕으로 한글 기반 클로드 스킬을 자동 생성합니다. Progressive disclosure 원칙에 따라 SKILL.md(개요), references/detailed_guide.md(상세), references/examples.md(예시)로 구조화된 스킬을 만듭니다.

**핵심 특징**:
- 모든 문서를 한글로 작성
- SKILL.md는 간결하게, 상세 내용은 references/로 분리
- 실전 예시를 포함한 일관성 있는 템플릿 제공

## 스킬 생성 프로세스

### 1단계: 요구사항 수집

사용자에게 다음 정보를 질문:
1. **스킬 이름** (kebab-case)
2. **스킬 설명** (한 문장)
3. **주요 기능** (3-5개)
4. **사용 예시** (2-3개)
5. **필요 리소스** (scripts/assets/references)

### 2단계: 스킬 구조 생성

```bash
python scripts/create_skill.py <스킬-이름> "<설명>" "<개요>" <출력-디렉토리>
```

자동 생성되는 파일:
- `SKILL.md` - 개요 및 기본 사용법
- `references/detailed_guide.md` - 상세 가이드
- `references/examples.md` - 예시 모음
- `references/api_reference.md` - API 문서 (선택)

### 3단계: 내용 채우기

생성된 템플릿을 사용자 요구사항에 맞게 구체화합니다.

**중요**: SKILL.md가 길어지면 해당 부분을 별도 md 파일로 분리하고 링크로 참조하세요.

상세한 작성 방법은 [references/writing_guide.md](references/writing_guide.md)를 참조하세요.

### 4단계: 추가 리소스 (선택)

필요시 scripts/ 또는 assets/에 리소스를 추가합니다.

### 5단계: Claude Code에서 사용

생성된 스킬 디렉토리를 Claude Code의 스킬 폴더에 배치하면 바로 사용할 수 있습니다.

```bash
# 예: ~/.claude/skills/ 디렉토리로 복사
cp -r <생성된-스킬-디렉토리> ~/.claude/skills/
```

## 빠른 참조

- **작성 가이드**: [references/writing_guide.md](references/writing_guide.md)
- **템플릿 구조**: [references/template_structure.md](references/template_structure.md)  
- **실전 예시**: [references/examples.md](references/examples.md)
- **문제 해결**: [references/troubleshooting.md](references/troubleshooting.md)

## 주의사항

1. 스킬 이름은 kebab-case 사용
2. SKILL.md는 500줄 이하 유지 (길어지면 분리)
3. 모든 문서는 UTF-8 인코딩
4. Progressive disclosure 원칙 준수
5. 생성된 스킬은 디렉토리 형태로 Claude Code에서 바로 사용 가능
