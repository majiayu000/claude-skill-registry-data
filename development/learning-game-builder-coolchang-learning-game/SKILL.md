---
name: learning-game-builder
description: Automates creation of interactive language learning games including vocabulary flashcards, song-based games, and multi-level learning systems. Generates complete projects with HTML/JS code, data generation pipelines, level/stage architectures, auto-advance features, and deployment automation. Use when users want to build vocabulary games, create JLPT/HSK study apps, song-based learning games, or any structured language learning application.
---

# 학습 게임 자동 생성 스킬

언어 학습 게임을 **자동으로** 생성하는 전문 스킬입니다. 노래 기반 게임부터 대규모 어휘 학습 시스템까지 완전 자동화된 워크플로우를 제공합니다.

## 이 스킬이 하는 일

언어 학습 게임 개발을 **완전 자동화**합니다:

1. **프로젝트 자동 생성** - 폴더 구조부터 배포까지 한 번에
2. **데이터 파이프라인 자동화** - Python 스크립트로 대량 데이터 생성
3. **게임 코드 자동 생성** - HTML/CSS/JavaScript 완전 작동 코드
4. **레벨/스테이지 시스템** - 계층적 학습 구조 자동 구성
5. **전문적인 UI/UX 디자인** - 공간 최적화, 스크롤 없는 학습 화면 ⭐
6. **배포 자동화** - GitHub Pages 설정 및 온라인 서비스화
7. **문서 자동 생성** - README, CHANGELOG 자동 작성

**수동 작업 8시간 → 자동화 5분**

## 활성화 트리거

다음과 같은 요청 시 자동으로 활성화됩니다:

### 어휘 학습 게임
- "JLPT N5-N1 어휘 학습 게임 만들어줘"
- "한자 플래시카드 게임 자동 생성"
- "2000개 단어 학습 시스템 만들기"
- "레벨별 어휘 학습 앱 개발"

### 노래 기반 게임
- "한국어 학습 게임 만들고 싶어"
- "노래로 언어 배우는 게임 개발하기"
- "가사 빈칸 채우기 게임 코드 생성해줘"

### 자동화 요청
- "학습 게임 프로젝트 자동 생성"
- "언어 학습 앱 배포까지 자동화"
- "대량 어휘 데이터 생성 파이프라인"

## 제공하는 게임 유형

### A. 어휘 학습 시스템 (⭐⭐⭐⭐⭐ 완전 자동화)

#### 1. 레벨/스테이지 플래시카드
- **자동 레벨 구성**: N5~N1, HSK1~6, CEFR A1~C2
- **스테이지 자동 분할**: 2000+ 단어를 30-50개씩 자동 분할
- **자동 진행 모드**: 스테이지→레벨 자동 전환
- **TTS 음성 지원**: 단어, 의미, 예문 자동 재생
- **진도 추적**: LocalStorage 기반 학습 현황
- **데이터 생성 자동화**: Python 스크립트로 대량 생성
- **전문 UI/UX 디자인** ⭐
  - 공간 최적화 (스크롤 없는 풀스크린 학습)
  - 심플한 모드 선택 디자인
  - 반응형 텍스트 크기 (clamp 함수)
  - Pretendard 웹폰트 적용
  - CSS 변수 기반 디자인 시스템

**예시**: JLPT 한자 학습 게임 (2050개 단어, 47개 스테이지)

#### 2. 간격 반복 학습 (SRS)
- Anki 스타일 복습 시스템
- 망각 곡선 기반 스케줄링
- 카드 난이도 자동 조정

### B. 노래 기반 학습 게임

#### 3. 가사 빈칸 채우기
- 난이도별 단어 선택 알고리즘
- 실시간 정답 체크
- 힌트 시스템
- 진도 추적

#### 4. 순서 맞추기
- 드래그 앤 드롭 인터페이스
- 가사 순서 재배열
- 문맥 이해 훈련

#### 5. 번역 매칭
- 한영 매칭 게임
- 타이머 챌린지
- 점수 시스템

#### 6. 듣기 퀴즈
- 오디오 구간 재생
- 받아쓰기 모드
- 발음 평가

## 🚀 완전 자동화 워크플로우

### 신규 프로젝트 자동 생성 (NEW!)

**사용자 요청:**
```
JLPT N5-N1 한자 학습 게임 만들어줘.
2000개 단어, 레벨별로 나눠서, GitHub Pages로 배포까지.
```

**스킬 자동 실행 (5분):**
```
1. ✅ 프로젝트 폴더 구조 생성
   project/
   ├── game.html
   ├── data/vocabulary/
   ├── scripts/
   └── README.md

2. ✅ 데이터 생성 스크립트 작성
   - generate_vocabulary.py (2000+ 단어 생성)
   - split_by_level.py (레벨별 분할)
   - stages.json (메타데이터)

3. ✅ 게임 HTML/CSS/JS 생성
   - 레벨 선택 UI
   - 스테이지 시스템
   - 플래시카드 모드
   - 자동 재생 모드 (풀스크린 최적화) ⭐
   - 자동 진행 기능
   - 전문 디자인 시스템 적용
     * CSS 변수 기반 디자인
     * Pretendard 웹폰트
     * 공간 최적화 (스크롤 제거)
     * 반응형 텍스트 (clamp)

4. ✅ 데이터 실행 및 생성
   - python generate_vocabulary.py
   - python split_by_level.py
   - 2050개 단어 JSON 파일 생성

5. ✅ Git 초기화 및 배포
   - git init
   - GitHub 저장소 연결
   - GitHub Pages 설정
   - 온라인 URL 제공

6. ✅ 문서 자동 생성
   - README.md (기능 설명, 사용법)
   - CHANGELOG.md (작업 내역)
   - .gitignore

결과: https://yourusername.github.io/project/ 🎉
```

**실제 소요 시간**: 5분 (vs 수동 8시간)

### 기존 워크플로우

#### 요청 예시 1: "가사 빈칸 채우기 게임 만들어줘"
1. 게임 컨셉 확인 (난이도, 대상 학습자 레벨)
2. HTML/CSS/JS 게임 코드 생성
3. 노래 데이터 JSON 스키마 제공
4. 통합 가이드 제공

#### 요청 예시 2: "어휘 데이터 구조 어떻게 만들지?"
1. JSON 스키마 제공
2. 샘플 데이터 생성
3. 필드 설명 (word, meaning, example, etc.)
4. 저장 및 로딩 방법 제안

#### 요청 예시 3: "2000개 단어 데이터 자동 생성"
1. 레벨 시스템 설계 (N5~N1 분배)
2. Python 스크립트 생성
3. 단어 생성 로직 구현
4. 스테이지 분할 알고리즘
5. JSON 파일 출력

## 핵심 기능

### 🏗️ 프로젝트 자동화 (NEW!)
- **폴더 구조 자동 생성**: 표준 프로젝트 레이아웃
- **데이터 파이프라인**: Python 스크립트 자동 작성
- **대량 데이터 생성**: AI로 2000+ 단어 자동 생성
- **배포 자동화**: GitHub Pages 설정 스크립트
- **문서 자동 생성**: README, CHANGELOG 템플릿

### 🎮 게임 시스템 아키텍처 (NEW!)
- **레벨 시스템**: N5~N1, HSK1~6, CEFR 등 자동 구성
- **스테이지 분할**: 단어 수 기반 최적 분배
- **자동 진행**: 스테이지→레벨 seamless 전환
- **메타데이터 관리**: stages.json 중앙 제어
- **진도 저장**: LocalStorage 자동 sync

### 💻 코드 생성
- 완전히 작동하는 HTML5 게임
- **전문적인 교육용 디자인 시스템** (NEW!)
- 반응형 디자인 (모바일/데스크톱)
- CSS Variables 기반 디자인 토큰
- Pretendard 웹폰트 (한글 최적화)
- Vanilla JavaScript (의존성 최소화)

### 📊 데이터 관리
- **계층적 구조**: Level → Stage → Words
- **JSON 기반**: 쉬운 수정 및 확장
- **버전 관리**: Git 친화적
- **다국어 지원**: i18n 구조

### 🎓 교육 설계
- **간격 반복 학습** (SRS 알고리즘)
- **맥락 학습** (예문 포함)
- **즉각 피드백** (실시간 정답 확인)
- **적응형 난이도** (레벨별 조정)
- **동기부여** (진도 바, 통계)

## 제공 파일

### `/templates` - 게임 템플릿
#### 어휘 학습 시스템 (NEW!)
- `vocabulary-flashcard-game.html` - 레벨/스테이지 플래시카드
- `vocabulary-auto-study.html` - 자동 재생 모드
- `vocabulary-srs.html` - 간격 반복 학습

#### 노래 기반 게임
- `fill-in-blank-game.html` - 가사 빈칸 채우기
- `flashcard-game.html` - 기본 플래시카드
- `matching-game.html` - 매칭 게임
- `quiz-game.html` - 퀴즈 게임

### `/scripts` - 자동화 스크립트 (NEW!)
- `generate_vocabulary.py` - 대량 어휘 생성
- `split_by_level.py` - 레벨별 분할
- `split_by_stage.py` - 스테이지별 분할
- `generate_stages_metadata.py` - stages.json 생성
- `deploy_github_pages.sh` - GitHub Pages 배포

### `/examples` - 샘플 데이터
#### 어휘 학습 (NEW!)
- `stages.json` - 스테이지 메타데이터 예시
- `vocabulary-n5.json` - JLPT N5 어휘
- `vocabulary-hsk1.json` - HSK 1급 어휘

#### 노래 학습
- `sample-song-data.json` - 노래 데이터 예시
- `vocabulary-database.json` - 어휘 DB 예시
- `game-config.json` - 게임 설정 예시

### `/docs` - 문서
- `professional-design-guide.md` - **전문 교육용 디자인 시스템** (공간 최적화 패턴 추가!)
  - CSS 변수 시스템, Pretendard 폰트
  - 심플 & 컴팩트 모드 선택 디자인
  - **풀스크린 자동학습 최적화** (스크롤 제거) ⭐
  - 반응형 텍스트 (clamp 함수)
- `automation-guide.md` - **자동화 워크플로우 가이드**
- `level-stage-architecture.md` - **레벨/스테이지 시스템**
- `data-structure-guide.md` - 데이터 구조 가이드
- `deployment-guide.md` - **배포 자동화**
- `quick-start-guide.md` - 빠른 시작

## 개발 지원 시나리오

### ⭐ 시나리오 0: 완전 자동 프로젝트 생성 (NEW!)
```
개발자: "JLPT 한자 학습 게임 만들어줘. N5부터 N1까지 2000개 단어.
         배포까지 자동으로 해줘."

스킬 (5분 자동 실행):
1. ✅ 프로젝트 폴더 구조 자동 생성
2. ✅ Python 스크립트 작성 (데이터 생성 파이프라인)
3. ✅ 2050개 단어 AI 생성 및 레벨별 분할
4. ✅ 게임 HTML 코드 생성 (플래시카드 + 자동 재생)
5. ✅ stages.json 메타데이터 생성
6. ✅ Git 초기화 및 GitHub 푸시
7. ✅ GitHub Pages 자동 배포
8. ✅ README, CHANGELOG 생성
9. ✅ 온라인 URL 제공

결과: https://username.github.io/kanji-game/ 🎉
```

### 시나리오 1: 노래 게임 만들기
```
개발자: "한국어 노래로 학습 게임 만들고 싶어. 가사 빈칸 채우기부터 시작할래"

스킬:
1. 요구사항 확인 (대상 학습자, 기술 스택)
2. 프로젝트 구조 제안
3. 게임 HTML/CSS/JS 코드 생성
4. 샘플 데이터 제공
5. 테스트 가이드
6. 다음 단계 제안 (배포, 추가 기능)
```

### 시나리오 2: 대량 데이터 자동 생성
```
개발자: "HSK 1-6급 중국어 단어 5000개 자동 생성해줘"

스킬:
1. 레벨 시스템 설계 (HSK 1~6)
2. 단어 생성 Python 스크립트 작성
3. AI로 5000+ 단어 생성 (단어, 병음, 의미, 예문)
4. 레벨별 분할 (HSK1: 150개, HSK2: 300개...)
5. 스테이지 자동 분배
6. stages.json 메타데이터 생성
7. 데이터 검증 및 품질 체크

결과: 5000개 단어 JSON 파일 + 메타데이터
```

### 시나리오 3: 기존 게임에 기능 추가
```
개발자: "내 플래시카드 게임에 자동 진행 기능 추가해줘"

스킬:
1. 현재 코드 분석
2. autoAdvanceToNextStage() 함수 생성
3. 스테이지→레벨 전환 로직 구현
4. UI 업데이트 (진행 상태 표시)
5. LocalStorage 연동
6. 테스트 케이스 제공
```

### 시나리오 4: 배포 자동화
```
개발자: "내 게임 GitHub Pages로 배포해줘"

스킬:
1. index.html 랜딩 페이지 생성
2. .gitignore 설정
3. README.md 생성
4. Git 초기화 및 첫 커밋
5. GitHub 저장소 연결
6. GitHub Pages 설정 스크립트
7. 온라인 URL 확인

결과: https://username.github.io/project/
```

## 기술 스택

### 프론트엔드
- HTML5 (시맨틱 마크업)
- CSS3 / Tailwind CSS (스타일링)
- Vanilla JavaScript (게임 로직)
- Optional: React/Vue (복잡한 게임)

### 데이터
- JSON (데이터 저장)
- LocalStorage (진도 저장)
- Optional: Firebase/Supabase (클라우드 동기화)

### 오디오
- HTML5 Audio API
- Optional: Web Audio API (고급 기능)

## 학습 효과 최적화

### 교육 원칙 적용
- **간격 반복**: 복습 스케줄링
- **맥락 학습**: 문장 속에서 단어 학습
- **멀티모달**: 시각+청각+운동 결합
- **즉각 피드백**: 실시간 정답/오답 표시
- **적응형 난이도**: 실력에 맞춰 조절

### 동기부여 요소
- 진도 바 및 통계
- 점수 및 순위
- 배지 및 업적
- 학습 스트릭

## 예제 출력

요청: "가사 빈칸 채우기 게임 코드 만들어줘"

출력:
1. ✅ 완전한 HTML 파일 (즉시 실행 가능)
2. ✅ 샘플 노래 데이터 JSON
3. ✅ 통합 가이드 (어떻게 사용하는지)
4. ✅ 커스터마이징 팁
5. ✅ 다음 단계 제안

## 🏛️ 핵심 아키텍처 패턴 (NEW!)

### 1. 계층적 데이터 구조
```
Level (레벨)
  ├── Stage (스테이지)
  │   ├── Words (단어들)
  │   │   ├── word: 한자 표기
  │   │   ├── reading: 히라가나
  │   │   ├── meaning: 의미
  │   │   ├── example: 예문
  │   │   └── metadata: 품사, 레벨 등
```

### 2. 메타데이터 주도 아키텍처
**stages.json이 게임 전체를 제어**
```json
{
  "levels": {
    "N5": {
      "totalWords": 150,
      "totalStages": 5,
      "stages": [
        { "stageNumber": 1, "wordRange": "1-30", "wordCount": 30 }
      ]
    }
  }
}
```

### 3. 자동 진행 패턴
```javascript
// 스테이지 완료 → 다음 스테이지
// 레벨 완료 → 다음 레벨
// 모든 레벨 완료 → 완료 화면

async function autoAdvanceToNextStage() {
  // 1. 현재 레벨에서 다음 스테이지 확인
  if (hasNextStage) { loadNextStage(); return; }

  // 2. 다음 레벨 확인
  if (hasNextLevel) { loadNextLevel(); return; }

  // 3. 모두 완료
  showCompletionScreen();
}
```

### 4. 데이터 생성 파이프라인
```
Python Script → JSON Files → Web Game

generate_vocabulary.py
  ↓
[raw_data.json] (2000+ words)
  ↓
split_by_level.py
  ↓
[n5.json, n4.json, ...] (레벨별)
  ↓
split_by_stage.py
  ↓
[stages.json] (메타데이터)
  ↓
game.html (자동 로딩)
```

### 5. 재사용 가능한 컴포넌트
- **LevelSelector**: 모든 레벨 기반 게임에 적용
- **StageSystem**: 모든 단계별 학습에 적용
- **FlashcardComponent**: 모든 암기 학습에 적용
- **AutoPlayLogic**: 모든 순차 학습에 적용
- **ProgressTracker**: 모든 학습 앱에 적용

### 6. 전문 교육용 디자인 시스템 (NEW!)

**모든 학습 게임에 일관된 전문적인 룩앤필 자동 적용**

#### CSS Variables 디자인 토큰
```css
:root {
  /* 브랜드 색상 */
  --primary: #667eea;
  --secondary: #764ba2;

  /* 시맨틱 색상 */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;

  /* 레벨 색상 (JLPT/HSK 등) */
  --level-n5: #4ade80;  /* 녹색 - 초급 */
  --level-n4: #60a5fa;  /* 파랑 - 초중급 */
  --level-n3: #a78bfa;  /* 보라 - 중급 */
  --level-n2: #fb923c;  /* 주황 - 중상급 */
  --level-n1: #f87171;  /* 빨강 - 고급 */

  /* 타이포그래피 */
  --font-sans: 'Pretendard', system-ui, sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  /* 스페이싱 */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;

  /* 그림자 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

#### 전문 컴포넌트 자동 생성
1. **브랜드 헤더**
   - 그라디언트 로고
   - 실시간 학습 통계
   - 홈 버튼

2. **대시보드 카드**
   - 호버 애니메이션
   - 그림자 효과
   - 반응형 그리드

3. **레벨/스테이지 선택**
   - 레벨별 색상 코딩
   - 진도 표시 배지
   - 부드러운 전환 효과

4. **모드 선택 카드**
   - 아이콘 + 제목 + 설명
   - 예상 소요 시간 표시
   - 추천 모드 배지

5. **학습 통계 시각화**
   - 진도 바
   - 정답률 차트
   - 연속 학습 일수

#### Pretendard 웹폰트
- 한글/영문/일본어 통합 지원
- 교육용 최적화된 가독성
- 9가지 font-weight 지원

**참고**: `docs/professional-design-guide.md`에서 전체 디자인 시스템 확인

## 확장성

### 언어 지원
- 일본어 (JLPT N5-N1) ✅
- 중국어 (HSK 1-6)
- 한국어 (TOPIK 1-6)
- 영어 (TOEFL, IELTS)
- 스페인어 (DELE A1-C2)

### 콘텐츠 유형
- 어휘 학습 ✅
- 노래 가사 ✅
- 팟캐스트 스크립트
- 영화 대사
- 뉴스 기사

### 고급 기능
- AI 음성 인식 통합
- 소셜 기능 (친구 챌린지)
- 게임화 요소 강화
- 개인화 학습 경로

## 라이선스 및 주의사항

노래 가사 사용 시:
- 저작권 확인 필수
- 교육 목적 fair use 검토
- 출처 명시
- 상업적 사용 시 라이선스 획득

이 스킬은 개발 도구와 가이드를 제공하며, 콘텐츠 사용에 대한 법적 책임은 사용자에게 있습니다.
