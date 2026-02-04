---
name: finding-skills
description: Searches and recommends Claude Code skills and plugins from local database and SkillsMP API. Activates when user asks to find skills, search plugins, get recommendations for PDF/Git/code-review/frontend tools, or requests feature-based tool discovery.
---

# 외부 스킬 찾기

사용자가 원하는 기능이나 목적에 맞는 Claude Code 스킬 및 플러그인을 추천하는 대화형 도우미입니다.

## Resources

이 스킬은 다음 리소스를 참조합니다:

- **외부 스킬 데이터베이스**: `references/external-skills-database.json` - 공식 및 커뮤니티 스킬 정보
- **SkillsMP 검색 스크립트**: `scripts/search_skills.py` - 실시간 커뮤니티 스킬 검색

## Instructions

### 1. 사용자 의도 파악

사용자가 다음과 같은 요청을 할 때 이 스킬이 활성화됩니다:
- "PDF 작업할 수 있는 스킬 있어?"
- "Git 커밋을 도와주는 플러그인 찾아줘"
- "코드 리뷰 자동화 도구 추천해줘"
- "프론트엔드 개발에 유용한 스킬은?"
- 기타 기능이나 목적 기반 스킬 검색 요청

### 2. 검색 및 분석 프로세스

스킬 검색은 **2단계 접근법**을 사용합니다:

#### 단계 1: 로컬 데이터베이스 검색

1. **키워드 추출**: 사용자 요청에서 핵심 키워드 추출 (한글은 영어로 변환)

2. **로컬 데이터베이스 조회**: `references/external-skills-database.json` 파일 읽기
   - 키워드를 사용해 `searchIndex` 섹션에서 관련 스킬 찾기
   - 카테고리별로 스킬 정보 탐색
   - 공식 스킬 및 플러그인 우선 매칭

#### 단계 2: SkillsMP API 검색 (Python 스크립트 사용)

로컬 데이터베이스에서 충분한 결과를 찾지 못했거나, 더 많은 커뮤니티 스킬이 필요한 경우:

1. **Python 스크립트 실행**: Bash 도구를 사용하여 `search_skills.py` 스크립트 실행
   ```bash
   python3 scripts/search_skills.py "[영어 검색어]" --limit 5
   ```

   **스크립트 옵션**:
   - `--limit N`: 반환할 결과 수 (기본값: 10, 권장: 5)
   - `--page N`: 페이지 번호 (기본값: 1)
   - `--sort stars|recent|name`: 정렬 기준 (기본값: stars)
   - `--format json|text`: 출력 형식 (기본값: json)

   **예시**:
   ```bash
   # PDF 관련 스킬 검색
   python3 scripts/search_skills.py "pdf" --limit 5

   # Git 관련 스킬을 최신순으로 검색
   python3 scripts/search_skills.py "git commit" --limit 5 --sort recent

   # 이미지 처리 스킬 검색 (텍스트 형식)
   python3 scripts/search_skills.py "image processing" --limit 5 --format text
   ```

2. **스크립트 응답 형식** (JSON):
   ```json
   {
     "success": true,
     "query": "검색어",
     "total": 100,
     "page": 1,
     "totalPages": 10,
     "hasNext": true,
     "skills": [
       {
         "name": "스킬 이름",
         "author": "작성자",
         "description": "스킬 설명",
         "stars": 1234,
         "githubUrl": "https://github.com/...",
         "hasMarketplace": true
       }
     ]
   }
   ```

3. **응답 데이터 처리**:
   - `skills` 배열에서 각 스킬 정보 추출
   - `stars` 수로 인기도 판단
   - `hasMarketplace`가 true이면 마켓플레이스 설치 가능
   - `githubUrl`에서 저장소 정보 확인

4. **결과 병합**:
   - 로컬 데이터베이스 결과 (공식/큐레이션)
   - SkillsMP 스크립트 결과 (커뮤니티/최신)
   - 중복 제거 및 관련성 순으로 정렬

#### 검색 전략

- **한글 쿼리**: 먼저 영어로 변환 후 검색
  - "PDF 작업" → "pdf work" 또는 "pdf"
  - "Git 커밋" → "git commit"
  - "코드 리뷰" → "code review"

- **복합 검색**: 여러 키워드가 있을 경우
  - 각 키워드로 개별 검색 후 결과 병합
  - 또는 공백으로 구분된 검색어로 API 호출

- **결과 우선순위**:
  1. 로컬 데이터베이스의 공식 스킬
  2. 로컬 데이터베이스의 공식 플러그인
  3. SkillsMP의 인기 스킬 (stars 기준)
  4. 로컬 데이터베이스의 커뮤니티 리소스

#### 매칭 및 필터링

- 최종적으로 3-5개의 가장 관련성 높은 스킬 선별
- 각 스킬의 features, useCases, 인기도 확인
- 다양한 옵션 제공 (공식 vs 커뮤니티)

### 3. 응답 형식

사용자에게 다음 정보를 제공합니다:

#### 기본 정보
```
## 추천 스킬: [스킬 이름]

**설명**: [스킬 설명]
**제공자**: [공식/커뮤니티/작성자]
**인기도**: ⭐ [stars 수] (SkillsMP API에서 온 경우)
**태그**: [관련 태그들]
```

**SkillsMP API 결과의 경우 추가 정보:**
- stars 수를 표시하여 인기도 표시
- marketplace 정보가 있으면 해당 마켓플레이스 명시
- author/owner 정보 표시

#### 주요 기능
스킬의 주요 기능을 카테고리별로 나열:
```
### 주요 기능

**[카테고리 1]**
- 기능 1
- 기능 2

**[카테고리 2]**
- 기능 3
- 기능 4
```

#### 설치 방법

**로컬 데이터베이스 스킬의 경우:**
```
### 설치 방법

\`\`\`bash
[설치 명령어들]
\`\`\`

[추가 설명이 있다면 포함]
```

**SkillsMP API 스킬의 경우:**
```
### 설치 방법

[marketplace 정보가 있는 경우]
\`\`\`bash
/plugin marketplace add [marketplace-owner]/[marketplace-repo]
/plugin install [skill-name]@[marketplace-name]
\`\`\`

[marketplace 정보가 없는 경우]
GitHub 저장소를 참고하여 수동 설치하거나 로컬에서 사용하세요:
- 저장소: [repository URL]
```

#### 사용 사례
```
### 이런 경우에 유용합니다

- 사용 사례 1
- 사용 사례 2
- 사용 사례 3
```

#### 추가 정보
```
### 더 알아보기

- **저장소**: [GitHub URL]
- **관련 문서**: [문서 링크]
```

### 4. 다중 스킬 추천

여러 스킬이 관련될 경우:
1. 가장 적합한 스킬을 먼저 소개
2. 관련된 다른 스킬들도 간략히 언급
3. 사용자가 선택할 수 있도록 옵션 제시

### 5. 검색 결과 없음

로컬 데이터베이스와 SkillsMP API 모두에서 관련 스킬을 찾지 못한 경우:
```
죄송합니다. "[검색어]"와 관련된 스킬을 찾을 수 없습니다.

다음을 시도해보세요:
- 다른 키워드로 검색 (영어로 시도해보세요)
- Claude Code 마켓플레이스 확인: `/plugin marketplace list`
- SkillsMP 웹사이트 직접 검색: https://skillsmp.com
- GitHub에서 "claude-code" 토픽 검색: https://github.com/topics/claude-code
```

## 예시

### 예시 1: PDF 관련 스킬 검색 (로컬 DB)

**사용자**: "PDF 파일 작업할 수 있는 스킬 있어?"

**검색 과정**:
1. 로컬 데이터베이스에서 "pdf" 키워드로 검색
2. example-skills가 매칭됨

**응답**:
```
## 추천 스킬: example-skills

**설명**: Anthropic에서 제공하는 공식 예제 스킬 모음입니다.
**제공자**: Anthropic (공식)
**태그**: official, documents, frontend, development-tools

### 주요 기능

**문서 작업**
- PDF 파일 생성/편집/분석
- DOCX 문서 생성/편집
- PPTX 프레젠테이션 생성/편집
- XLSX 스프레드시트 생성/편집

**프론트엔드**
- React 컴포넌트 디자인
- 알고리즘 아트 생성 (p5.js)
- 캔버스 디자인
- 웹 아티팩트 빌더

**개발 도구**
- MCP 서버 빌더
- 웹앱 테스팅 (Playwright)
- 스킬 생성기

### 설치 방법

\`\`\`bash
/plugin marketplace add anthropic/example-skills
/plugin install example-skills@anthropic-agent-skills
\`\`\`

설치 후 개별 스킬을 바로 사용할 수 있습니다.

### 이런 경우에 유용합니다

- 문서 자동화가 필요한 프로젝트
- 프론트엔드 컴포넌트 빠른 프로토타이핑
- MCP 서버 개발
- 비주얼 콘텐츠 생성

### 더 알아보기

- **저장소**: https://github.com/anthropics/anthropic-agent-skills
```

### 예시 2: Git 관련 스킬 검색

**사용자**: "Git 커밋 자동화 도구 추천해줘"

**응답**:
```
Git 커밋 관련해서 두 가지 좋은 옵션이 있습니다:

## 1. commit-commands (공식 플러그인)

**설명**: Git 작업을 간소화하는 커밋 관련 명령어 모음
**제공자**: Claude Code Official

### 주요 기능
- `/commit` - 스마트 커밋 메시지 생성
- `/commit-push-pr` - 커밋, 푸시, PR 생성 일괄 처리
- `/clean_gone` - 삭제된 원격 브랜치 정리

### 설치 방법
\`\`\`bash
/plugin install commit-commands@claude-plugins-official
\`\`\`

---

## 2. git-workflow (이 저장소의 플러그인)

**설명**: 변경 사항을 논리적 단위로 자동 분석하여 커밋
**제공자**: jeongsk

### 주요 기능
- 변경 사항을 논리적 단위로 자동 그룹화
- 의미 있는 커밋 메시지 자동 생성
- 단계별 커밋 또는 일괄 커밋 & 푸시

### 설치 방법
\`\`\`bash
/plugin marketplace add jeongsk/claude-skills
/plugin install git-workflow@jeongsk-claude-skills
\`\`\`

어떤 스킬이 더 필요하신지 알려주시면 자세한 사용법을 안내해드리겠습니다!
```

### 예시 3: SkillsMP 스크립트를 활용한 검색

**사용자**: "Obsidian 관련 스킬 찾아줘"

**검색 과정**:
1. 로컬 데이터베이스에서 "obsidian" 키워드 검색 → 결과 없음
2. Python 스크립트 실행:
   ```bash
   python3 scripts/search_skills.py "obsidian" --limit 5
   ```
3. 스크립트 응답에서 인기 스킬 추출

**스크립트 출력 예시**:
```json
{
  "success": true,
  "query": "obsidian",
  "total": 37,
  "page": 1,
  "totalPages": 4,
  "hasNext": true,
  "skills": [
    {
      "name": "obsidian-vault-ops",
      "author": "ballred",
      "description": "Read and write Obsidian vault files, manage wiki-links, process markdown with YAML frontmatter.",
      "stars": 734,
      "githubUrl": "https://github.com/ballred/obsidian-claude-pkm/tree/main/vault-template/.claude/skills/obsidian-vault-ops",
      "hasMarketplace": false
    },
    {
      "name": "obsidian",
      "author": "gapmiss",
      "description": "Comprehensive guidelines for Obsidian.md plugin development including ESLint rules, TypeScript best practices.",
      "stars": 16,
      "githubUrl": "https://github.com/gapmiss/obsidian-plugin-skill/tree/main/.claude/skills/obsidian",
      "hasMarketplace": false
    }
  ]
}
```

**응답**:
```
"obsidian"으로 SkillsMP에서 검색한 결과입니다:

## 1. obsidian-vault-ops

**설명**: Obsidian vault 파일 읽기/쓰기, wiki-links 관리, YAML frontmatter 처리
**제공자**: ballred (커뮤니티)
**인기도**: ⭐ 734

### 설치 방법
GitHub 저장소를 참고하여 수동 설치:
- **저장소**: https://github.com/ballred/obsidian-claude-pkm

---

## 2. obsidian

**설명**: Obsidian.md 플러그인 개발을 위한 종합 가이드라인
**제공자**: gapmiss (커뮤니티)
**인기도**: ⭐ 16

### 설치 방법
GitHub 저장소를 참고하여 수동 설치:
- **저장소**: https://github.com/gapmiss/obsidian-plugin-skill

더 많은 결과는 SkillsMP에서 확인하세요: https://skillsmp.com
```

## 참고사항

### 데이터 소스
- **로컬 데이터베이스**: 정기적으로 업데이트됩니다 (`lastUpdated` 필드 확인)
- **SkillsMP API**: 실시간 커뮤니티 스킬 정보 제공
- 공식 스킬은 Anthropic 및 Claude Code Official에서 관리
- 커뮤니티 스킬은 개별 개발자가 관리

### SkillsMP 스크립트 주의사항

- 검색어는 영어로 사용 (한글은 영어로 변환 후 실행)
- 로컬 DB 우선 검색 후 스크립트 보조 사용
- 중복 결과 필터링 필요
- 상세 사용법은 "단계 2: SkillsMP API 검색" 참조

## 추가 기능

### 카테고리별 탐색

사용자가 "전체 스킬 목록 보여줘" 또는 "카테고리별로 보여줘" 요청 시:
1. 데이터베이스의 `categories` 섹션 읽기
2. 각 카테고리별로 스킬 요약 제공
3. 사용자가 관심 있는 카테고리 선택 가능

### 태그 기반 검색

사용자가 특정 태그로 검색 요청 시:
- `official`, `development`, `git`, `documents` 등의 태그로 필터링
- 해당 태그를 가진 모든 스킬 나열

## 오류 처리

### 로컬 데이터베이스 오류
- 파일을 읽을 수 없는 경우: 사용자에게 README 참조 안내
- JSON 파싱 오류: 관리자에게 문제 보고 요청

### SkillsMP 스크립트 오류
- 스크립트 실행 실패: 로컬 데이터베이스 결과만 표시
- `"success": false` 응답: error 메시지 확인 후 무시하고 계속 진행
- 타임아웃: "SkillsMP 검색이 응답하지 않습니다. 로컬 결과만 표시합니다." 메시지
- Python 미설치: 스크립트 사용 불가 안내, 로컬 DB만 사용

### 빈 검색 결과
- 로컬 DB와 API 모두 결과 없음: 대체 검색 방법 제안
- 영어로 재시도 권장
- SkillsMP 웹사이트 직접 방문 안내
