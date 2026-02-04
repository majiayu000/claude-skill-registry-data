---
name: design-skill
description: 프레젠테이션 슬라이드를 미려한 HTML로 디자인. 슬라이드 HTML 생성, 시각적 디자인, 레이아웃 구성이 필요할 때 사용.
---

# Design Skill - 프로페셔널 프레젠테이션 디자인 시스템

최고 수준의 비즈니스 프레젠테이션을 위한 HTML 슬라이드 디자인 스킬입니다.
미니멀하고 세련된 디자인, 전문적인 타이포그래피, 정교한 레이아웃을 제공합니다.

---

## 핵심 디자인 철학

### 1. Less is More
- 불필요한 장식 요소 제거
- 콘텐츠가 주인공이 되는 디자인
- 여백(Whitespace)을 적극 활용
- 시각적 계층 구조 명확화

### 2. 타이포그래피 중심 디자인
- Pretendard를 기본 폰트로 사용
- 폰트 크기 대비로 시각적 임팩트 생성
- 자간과 행간의 섬세한 조절
- 웨이트 변화로 강조점 표현

### 3. 전략적 색상 사용
- 제한된 색상 팔레트 (2-3색)
- 모노톤 기반 + 포인트 컬러
- 배경색으로 분위기 연출
- 고대비로 가독성 확보

---

## 기본 설정

### 슬라이드 크기 (16:9 기본)
```html
<body style="width: 720pt; height: 405pt;">
```

### 지원 비율
| 비율 | 크기 | 용도 |
|------|------|------|
| 16:9 | 720pt × 405pt | 기본, 모니터/화면 |
| 4:3 | 720pt × 540pt | 구형 프로젝터 |
| 16:10 | 720pt × 450pt | 맥북 |

### 기본 폰트 스택
```css
font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Pretendard 웹폰트 CDN
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
```

---

## 타이포그래피 시스템

### 폰트 크기 스케일
| 용도 | 크기 | 웨이트 | 사용 예시 |
|------|------|--------|----------|
| Hero Title | 72-96pt | 700-800 | 표지 메인 타이틀 |
| Section Title | 48-60pt | 700 | 섹션 구분 제목 |
| Slide Title | 32-40pt | 600-700 | 슬라이드 제목 |
| Subtitle | 20-24pt | 500 | 부제목, 설명 |
| Body | 16-20pt | 400 | 본문 텍스트 |
| Caption | 12-14pt | 400 | 캡션, 출처 |
| Label | 10-12pt | 500-600 | 뱃지, 태그 |

### 자간 설정 (letter-spacing)
```css
/* 대형 제목: 타이트하게 */
letter-spacing: -0.02em;

/* 중형 제목 */
letter-spacing: -0.01em;

/* 본문: 기본 */
letter-spacing: 0;

/* 캡션, 레이블: 약간 넓게 */
letter-spacing: 0.02em;
```

### 행간 설정 (line-height)
```css
/* 제목 */
line-height: 1.2;

/* 본문 */
line-height: 1.6 - 1.8;

/* 한 줄 텍스트 */
line-height: 1;
```

---

## 색상 팔레트 시스템

### 1. Executive Minimal (기본 권장)
세련된 비즈니스 프레젠테이션용
```css
--bg-primary: #f5f5f0;      /* 웜 화이트 배경 */
--bg-secondary: #e8e8e3;    /* 서브 배경 */
--bg-dark: #1a1a1a;         /* 다크 배경 */
--text-primary: #1a1a1a;    /* 메인 텍스트 */
--text-secondary: #666666;  /* 보조 텍스트 */
--text-light: #999999;      /* 약한 텍스트 */
--accent: #1a1a1a;          /* 강조 (검정) */
--border: #d4d4d0;          /* 테두리 */
```

### 2. Sage Professional
차분하고 신뢰감 있는 톤
```css
--bg-primary: #b8c4b8;      /* 세이지 그린 배경 */
--bg-secondary: #a3b0a3;    /* 짙은 세이지 */
--bg-light: #f8faf8;        /* 밝은 배경 */
--text-primary: #1a1a1a;    /* 메인 텍스트 */
--text-secondary: #3d3d3d;  /* 보조 텍스트 */
--accent: #2d2d2d;          /* 강조 */
--border: #9aa89a;          /* 테두리 */
```

### 3. Modern Dark
임팩트 있는 다크 테마
```css
--bg-primary: #0f0f0f;      /* 순수 다크 */
--bg-secondary: #1a1a1a;    /* 카드 배경 */
--bg-elevated: #252525;     /* 강조 영역 */
--text-primary: #ffffff;    /* 메인 텍스트 */
--text-secondary: #b0b0b0;  /* 보조 텍스트 */
--accent: #ffffff;          /* 강조 (화이트) */
--border: #333333;          /* 테두리 */
```

### 4. Corporate Blue
전통적 비즈니스 톤
```css
--bg-primary: #ffffff;      /* 화이트 배경 */
--bg-secondary: #f7f9fc;    /* 밝은 블루 그레이 */
--text-primary: #1e2a3a;    /* 다크 네이비 */
--text-secondary: #5a6b7d;  /* 블루 그레이 */
--accent: #2563eb;          /* 블루 강조 */
--border: #e2e8f0;          /* 테두리 */
```

### 5. Warm Neutral
따뜻하고 친근한 톤
```css
--bg-primary: #faf8f5;      /* 크림 화이트 */
--bg-secondary: #f0ebe3;    /* 웜 베이지 */
--text-primary: #2d2a26;    /* 다크 브라운 */
--text-secondary: #6b6560;  /* 미디움 브라운 */
--accent: #c45a3b;          /* 테라코타 */
--border: #ddd8d0;          /* 테두리 */
```

---

## 레이아웃 시스템

### 여백 기준 (padding/margin)
```css
/* 슬라이드 전체 여백 */
padding: 48pt;

/* 섹션 간 여백 */
gap: 32pt;

/* 요소 간 여백 */
gap: 16pt;

/* 텍스트 블록 내 여백 */
gap: 8pt;
```

### 그리드 시스템
```css
/* 2단 레이아웃 */
display: grid;
grid-template-columns: 1fr 1fr;
gap: 32pt;

/* 3단 레이아웃 */
grid-template-columns: repeat(3, 1fr);

/* 비대칭 레이아웃 (40:60) */
grid-template-columns: 2fr 3fr;

/* 비대칭 레이아웃 (30:70) */
grid-template-columns: 1fr 2.3fr;
```

---

## 디자인 컴포넌트

### 1. 뱃지/태그
```html
<p style="
  display: inline-block;
  padding: 6pt 14pt;
  border: 1px solid #1a1a1a;
  border-radius: 20pt;
  font-size: 10pt;
  font-weight: 500;
  letter-spacing: 0.02em;
  text-transform: uppercase;
">PRESENTATION</p>
```

### 2. 섹션 넘버
```html
<p style="
  display: inline-block;
  padding: 4pt 12pt;
  background: #1a1a1a;
  color: #ffffff;
  border-radius: 4pt;
  font-size: 10pt;
  font-weight: 600;
">SECTION 1</p>
```

### 3. 로고 영역
```html
<div style="display: flex; align-items: center; gap: 8pt;">
  <div style="
    width: 20pt;
    height: 20pt;
    background: #1a1a1a;
    border-radius: 4pt;
    display: flex;
    align-items: center;
    justify-content: center;
  ">
    <p style="color: #fff; font-size: 12pt;">*</p>
  </div>
  <p style="font-size: 12pt; font-weight: 600;">LogoName</p>
</div>
```

### 4. 아이콘 버튼
```html
<div style="
  width: 32pt;
  height: 32pt;
  border: 1px solid #1a1a1a;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
">
  <p style="font-size: 14pt;">↗</p>
</div>
```

### 5. 구분선
```html
<div style="
  width: 100%;
  height: 1pt;
  background: #d4d4d0;
"></div>
```

### 6. 정보 그리드
```html
<div style="display: flex; gap: 48pt;">
  <div>
    <p style="font-size: 10pt; color: #999; margin-bottom: 4pt;">Contact</p>
    <p style="font-size: 12pt; font-weight: 500;">334556774</p>
  </div>
  <div>
    <p style="font-size: 10pt; color: #999; margin-bottom: 4pt;">Date</p>
    <p style="font-size: 12pt; font-weight: 500;">March 2025</p>
  </div>
</div>
```

---

## 슬라이드 템플릿

### 1. 표지 슬라이드 (Cover)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #f5f5f0;
      padding: 32pt 48pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <!-- 헤더 -->
  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="display: flex; align-items: center; gap: 16pt;">
      <div style="display: flex; align-items: center; gap: 8pt;">
        <div style="width: 18pt; height: 18pt; background: #1a1a1a; border-radius: 3pt; display: flex; align-items: center; justify-content: center;">
          <p style="color: #fff; font-size: 10pt;">*</p>
        </div>
        <p style="font-size: 11pt; font-weight: 600; color: #1a1a1a;">LogoName</p>
      </div>
      <p style="display: inline-block; padding: 4pt 10pt; border: 1px solid #1a1a1a; border-radius: 12pt; font-size: 9pt; font-weight: 500;">PRESENTATION</p>
    </div>
    <div style="display: flex; align-items: center; gap: 8pt;">
      <p style="display: inline-block; padding: 4pt 10pt; border: 1px solid #1a1a1a; border-radius: 12pt; font-size: 9pt; font-weight: 500;">OUR PROJECT</p>
      <div style="width: 28pt; height: 28pt; border: 1px solid #1a1a1a; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
        <p style="font-size: 12pt; color: #1a1a1a;">↘</p>
      </div>
    </div>
  </div>

  <!-- 메인 타이틀 -->
  <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
    <h1 style="font-size: 72pt; font-weight: 500; color: #1a1a1a; letter-spacing: -0.02em; line-height: 1.1;">
      Business Deck
    </h1>
    <p style="font-size: 14pt; color: #666; margin-top: 24pt;">
      <span style="color: #999;">Presented by</span>  <span style="font-weight: 500; color: #1a1a1a;">Luna Martinez</span>
    </p>
  </div>

  <!-- 푸터 정보 -->
  <div style="display: flex; gap: 64pt;">
    <div>
      <p style="font-size: 9pt; color: #999; margin-bottom: 4pt;">Contact</p>
      <p style="font-size: 11pt; font-weight: 500; color: #1a1a1a;">334556774</p>
    </div>
    <div>
      <p style="font-size: 9pt; color: #999; margin-bottom: 4pt;">Date</p>
      <p style="font-size: 11pt; font-weight: 500; color: #1a1a1a;">March 2025</p>
    </div>
    <div>
      <p style="font-size: 9pt; color: #999; margin-bottom: 4pt;">Website</p>
      <p style="font-size: 11pt; font-weight: 500; color: #1a1a1a;">www.yourwebsite.com</p>
    </div>
  </div>
</body>
</html>
```

### 2. 목차 슬라이드 (Contents)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #b8c4b8;
      padding: 48pt;
      display: grid;
      grid-template-columns: 1fr 1.8fr;
      gap: 48pt;
    }
  </style>
</head>
<body>
  <!-- 왼쪽: 타이틀 -->
  <div style="display: flex; flex-direction: column; justify-content: flex-end;">
    <p style="font-size: 9pt; color: #3d3d3d; margin-bottom: 16pt;">©2025 YOUR BRAND. ALL RIGHTS RESERVED.</p>
    <h1 style="font-size: 56pt; font-weight: 500; color: #1a1a1a; letter-spacing: -0.02em; line-height: 1.1;">
      Our<br>Contents
    </h1>
    <div style="width: 32pt; height: 32pt; border: 1px solid #1a1a1a; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 24pt;">
      <p style="font-size: 14pt; color: #1a1a1a;">↗</p>
    </div>
  </div>

  <!-- 오른쪽: 목차 리스트 -->
  <div style="display: flex; flex-direction: column; justify-content: center; gap: 16pt;">
    <div style="display: flex; align-items: center; gap: 16pt; padding: 12pt 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 1</p>
      <p style="flex: 1; font-size: 14pt; font-weight: 500; color: #1a1a1a;">SECTION TITLE</p>
      <p style="font-size: 14pt; color: #666;">(1)</p>
    </div>
    <div style="display: flex; align-items: center; gap: 16pt; padding: 12pt 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 2</p>
      <p style="flex: 1; font-size: 14pt; font-weight: 500; color: #1a1a1a;">SECTION TITLE</p>
      <p style="font-size: 14pt; color: #666;">(2)</p>
    </div>
    <div style="display: flex; align-items: center; gap: 16pt; padding: 12pt 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 3</p>
      <p style="flex: 1; font-size: 14pt; font-weight: 500; color: #1a1a1a;">SECTION TITLE</p>
      <p style="font-size: 14pt; color: #666;">(3)</p>
    </div>
    <div style="display: flex; align-items: center; gap: 16pt; padding: 12pt 0; border-bottom: 1px solid rgba(0,0,0,0.1);">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 4</p>
      <p style="flex: 1; font-size: 14pt; font-weight: 500; color: #1a1a1a;">SECTION TITLE</p>
      <p style="font-size: 14pt; color: #666;">(4)</p>
    </div>
    <div style="display: flex; align-items: center; gap: 16pt; padding: 12pt 0;">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 5</p>
      <p style="flex: 1; font-size: 14pt; font-weight: 500; color: #1a1a1a;">SECTION TITLE</p>
      <p style="font-size: 14pt; color: #666;">(5)</p>
    </div>
  </div>
</body>
</html>
```

### 3. 섹션 구분 슬라이드 (Section Divider)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #1a1a1a;
      padding: 48pt;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <!-- 상단 섹션 정보 -->
  <div style="display: flex; justify-content: space-between; align-items: flex-start;">
    <div>
      <p style="display: inline-block; padding: 4pt 10pt; background: #fff; color: #1a1a1a; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 1</p>
    </div>
    <p style="font-size: 9pt; color: #666;">©2025 YOUR BRAND</p>
  </div>

  <!-- 메인 타이틀 -->
  <div>
    <h1 style="font-size: 64pt; font-weight: 500; color: #ffffff; letter-spacing: -0.02em; line-height: 1.1;">
      Introduction
    </h1>
    <p style="font-size: 16pt; color: #888; margin-top: 16pt; max-width: 400pt; line-height: 1.6;">
      Brief description of what this section covers and why it matters.
    </p>
  </div>

  <!-- 페이지 번호 -->
  <div style="display: flex; justify-content: flex-end;">
    <p style="font-size: 10pt; color: #666;">01</p>
  </div>
</body>
</html>
```

### 4. 콘텐츠 슬라이드 (Content)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #ffffff;
      padding: 40pt 48pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <!-- 헤더 -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32pt;">
    <div style="display: flex; align-items: center; gap: 12pt;">
      <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600;">SECTION 1</p>
      <h2 style="font-size: 24pt; font-weight: 600; color: #1a1a1a;">Main Topic</h2>
    </div>
    <p style="font-size: 10pt; color: #999;">02</p>
  </div>

  <!-- 콘텐츠 영역 -->
  <div style="flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 32pt;">
    <div>
      <h3 style="font-size: 18pt; font-weight: 600; color: #1a1a1a; margin-bottom: 16pt;">Key Point One</h3>
      <p style="font-size: 13pt; color: #666; line-height: 1.7;">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore.
      </p>
    </div>
    <div>
      <h3 style="font-size: 18pt; font-weight: 600; color: #1a1a1a; margin-bottom: 16pt;">Key Point Two</h3>
      <p style="font-size: 13pt; color: #666; line-height: 1.7;">
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip.
      </p>
    </div>
  </div>

  <!-- 푸터 -->
  <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 16pt; border-top: 1px solid #eee;">
    <p style="font-size: 9pt; color: #999;">www.yourwebsite.com</p>
    <p style="font-size: 9pt; color: #999;">©2025 YOUR BRAND</p>
  </div>
</body>
</html>
```

### 5. 통계/데이터 슬라이드 (Statistics)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #f5f5f0;
      padding: 40pt 48pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <!-- 헤더 -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32pt;">
    <h2 style="font-size: 28pt; font-weight: 600; color: #1a1a1a;">Key Metrics</h2>
    <p style="font-size: 10pt; color: #999;">03</p>
  </div>

  <!-- 통계 카드 그리드 -->
  <div style="flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 24pt;">
    <div style="background: #1a1a1a; border-radius: 12pt; padding: 28pt; display: flex; flex-direction: column; justify-content: space-between;">
      <p style="font-size: 10pt; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">Revenue Growth</p>
      <div>
        <p style="font-size: 48pt; font-weight: 600; color: #ffffff; letter-spacing: -0.02em;">85%</p>
        <p style="font-size: 11pt; color: #666; margin-top: 8pt;">Year over year</p>
      </div>
    </div>
    <div style="background: #ffffff; border-radius: 12pt; padding: 28pt; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid #e5e5e0;">
      <p style="font-size: 10pt; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">Active Users</p>
      <div>
        <p style="font-size: 48pt; font-weight: 600; color: #1a1a1a; letter-spacing: -0.02em;">2.4M</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt;">+340K this quarter</p>
      </div>
    </div>
    <div style="background: #ffffff; border-radius: 12pt; padding: 28pt; display: flex; flex-direction: column; justify-content: space-between; border: 1px solid #e5e5e0;">
      <p style="font-size: 10pt; color: #888; text-transform: uppercase; letter-spacing: 0.05em;">Customer Satisfaction</p>
      <div>
        <p style="font-size: 48pt; font-weight: 600; color: #1a1a1a; letter-spacing: -0.02em;">4.9</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt;">Out of 5.0 rating</p>
      </div>
    </div>
  </div>

  <!-- 푸터 -->
  <div style="display: flex; justify-content: flex-end; padding-top: 16pt;">
    <p style="font-size: 9pt; color: #999;">Source: Internal Analytics 2025</p>
  </div>
</body>
</html>
```

### 6. 이미지 + 텍스트 슬라이드 (Split Layout)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #ffffff;
      display: grid;
      grid-template-columns: 1fr 1fr;
    }
  </style>
</head>
<body>
  <!-- 이미지 영역 -->
  <div style="background: #e5e5e0; display: flex; align-items: center; justify-content: center; position: relative;">
    <div data-image-placeholder style="width: 100%; height: 100%; background: linear-gradient(135deg, #d0d0c8 0%, #b8b8b0 100%);"></div>
    <p style="position: absolute; bottom: 16pt; left: 16pt; font-size: 9pt; color: #666;">©2025 YOUR BRAND</p>
  </div>

  <!-- 텍스트 영역 -->
  <div style="padding: 48pt; display: flex; flex-direction: column; justify-content: center;">
    <p style="display: inline-block; padding: 4pt 10pt; background: #1a1a1a; color: #fff; border-radius: 4pt; font-size: 8pt; font-weight: 600; margin-bottom: 24pt; align-self: flex-start;">FEATURE</p>
    <h2 style="font-size: 32pt; font-weight: 600; color: #1a1a1a; letter-spacing: -0.01em; line-height: 1.2; margin-bottom: 20pt;">
      Transform Your Business
    </h2>
    <p style="font-size: 14pt; color: #666; line-height: 1.7;">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    </p>
    <div style="margin-top: 32pt; display: flex; align-items: center; gap: 12pt;">
      <p style="font-size: 12pt; font-weight: 500; color: #1a1a1a;">Learn more</p>
      <div style="width: 28pt; height: 28pt; border: 1px solid #1a1a1a; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
        <p style="font-size: 12pt; color: #1a1a1a;">→</p>
      </div>
    </div>
  </div>
</body>
</html>
```

### 7. 팀 소개 슬라이드 (Team)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #f5f5f0;
      padding: 40pt 48pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <!-- 헤더 -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32pt;">
    <h2 style="font-size: 28pt; font-weight: 600; color: #1a1a1a;">Our Team</h2>
    <p style="font-size: 10pt; color: #999;">05</p>
  </div>

  <!-- 팀원 그리드 -->
  <div style="flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 20pt;">
    <div style="text-align: center;">
      <div style="width: 100%; aspect-ratio: 1; background: #d0d0c8; border-radius: 8pt; margin-bottom: 12pt;"></div>
      <p style="font-size: 13pt; font-weight: 600; color: #1a1a1a;">John Smith</p>
      <p style="font-size: 10pt; color: #888; margin-top: 4pt;">CEO & Founder</p>
    </div>
    <div style="text-align: center;">
      <div style="width: 100%; aspect-ratio: 1; background: #d0d0c8; border-radius: 8pt; margin-bottom: 12pt;"></div>
      <p style="font-size: 13pt; font-weight: 600; color: #1a1a1a;">Sarah Johnson</p>
      <p style="font-size: 10pt; color: #888; margin-top: 4pt;">CTO</p>
    </div>
    <div style="text-align: center;">
      <div style="width: 100%; aspect-ratio: 1; background: #d0d0c8; border-radius: 8pt; margin-bottom: 12pt;"></div>
      <p style="font-size: 13pt; font-weight: 600; color: #1a1a1a;">Mike Chen</p>
      <p style="font-size: 10pt; color: #888; margin-top: 4pt;">Design Lead</p>
    </div>
    <div style="text-align: center;">
      <div style="width: 100%; aspect-ratio: 1; background: #d0d0c8; border-radius: 8pt; margin-bottom: 12pt;"></div>
      <p style="font-size: 13pt; font-weight: 600; color: #1a1a1a;">Emily Davis</p>
      <p style="font-size: 10pt; color: #888; margin-top: 4pt;">Marketing</p>
    </div>
  </div>
</body>
</html>
```

### 8. 인용문 슬라이드 (Quote)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #1a1a1a;
      padding: 64pt;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
  </style>
</head>
<body>
  <p style="font-size: 48pt; color: #444; margin-bottom: 24pt;">"</p>
  <h2 style="font-size: 28pt; font-weight: 400; color: #ffffff; letter-spacing: -0.01em; line-height: 1.5; max-width: 540pt;">
    The best way to predict the future is to create it.
  </h2>
  <div style="margin-top: 40pt;">
    <p style="font-size: 13pt; font-weight: 500; color: #ffffff;">Peter Drucker</p>
    <p style="font-size: 11pt; color: #666; margin-top: 4pt;">Management Consultant</p>
  </div>
</body>
</html>
```

### 9. 타임라인 슬라이드 (Timeline)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #ffffff;
      padding: 40pt 48pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <!-- 헤더 -->
  <div style="margin-bottom: 32pt;">
    <h2 style="font-size: 28pt; font-weight: 600; color: #1a1a1a;">Our Journey</h2>
  </div>

  <!-- 타임라인 -->
  <div style="flex: 1; display: flex; align-items: center;">
    <div style="display: flex; width: 100%; justify-content: space-between; position: relative;">
      <!-- 연결선 -->
      <div style="position: absolute; top: 12pt; left: 40pt; right: 40pt; height: 2pt; background: #e5e5e0;"></div>

      <!-- 타임라인 아이템들 -->
      <div style="text-align: center; z-index: 1;">
        <div style="width: 24pt; height: 24pt; background: #1a1a1a; border-radius: 50%; margin: 0 auto 16pt;"></div>
        <p style="font-size: 18pt; font-weight: 600; color: #1a1a1a;">2020</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt; max-width: 100pt;">Company Founded</p>
      </div>
      <div style="text-align: center; z-index: 1;">
        <div style="width: 24pt; height: 24pt; background: #1a1a1a; border-radius: 50%; margin: 0 auto 16pt;"></div>
        <p style="font-size: 18pt; font-weight: 600; color: #1a1a1a;">2021</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt; max-width: 100pt;">First Product Launch</p>
      </div>
      <div style="text-align: center; z-index: 1;">
        <div style="width: 24pt; height: 24pt; background: #1a1a1a; border-radius: 50%; margin: 0 auto 16pt;"></div>
        <p style="font-size: 18pt; font-weight: 600; color: #1a1a1a;">2023</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt; max-width: 100pt;">Series A Funding</p>
      </div>
      <div style="text-align: center; z-index: 1;">
        <div style="width: 24pt; height: 24pt; background: #1a1a1a; border-radius: 50%; margin: 0 auto 16pt;"></div>
        <p style="font-size: 18pt; font-weight: 600; color: #1a1a1a;">2025</p>
        <p style="font-size: 11pt; color: #888; margin-top: 8pt; max-width: 100pt;">Global Expansion</p>
      </div>
    </div>
  </div>

  <!-- 푸터 -->
  <div style="display: flex; justify-content: flex-end; padding-top: 16pt;">
    <p style="font-size: 10pt; color: #999;">06</p>
  </div>
</body>
</html>
```

### 10. 마무리 슬라이드 (Closing)
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: 'Pretendard', sans-serif;
      background: #1a1a1a;
      padding: 48pt;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
  </style>
</head>
<body>
  <!-- 로고 -->
  <div style="display: flex; align-items: center; gap: 8pt;">
    <div style="width: 20pt; height: 20pt; background: #fff; border-radius: 4pt; display: flex; align-items: center; justify-content: center;">
      <p style="color: #1a1a1a; font-size: 12pt;">*</p>
    </div>
    <p style="font-size: 12pt; font-weight: 600; color: #ffffff;">LogoName</p>
  </div>

  <!-- 메인 메시지 -->
  <div>
    <h1 style="font-size: 56pt; font-weight: 500; color: #ffffff; letter-spacing: -0.02em; line-height: 1.1;">
      Thank You
    </h1>
    <p style="font-size: 16pt; color: #888; margin-top: 16pt;">
      Questions? Let's discuss.
    </p>
  </div>

  <!-- 연락처 정보 -->
  <div style="display: flex; gap: 64pt;">
    <div>
      <p style="font-size: 9pt; color: #666; margin-bottom: 4pt;">Email</p>
      <p style="font-size: 12pt; font-weight: 500; color: #ffffff;">hello@company.com</p>
    </div>
    <div>
      <p style="font-size: 9pt; color: #666; margin-bottom: 4pt;">Phone</p>
      <p style="font-size: 12pt; font-weight: 500; color: #ffffff;">+82 10-1234-5678</p>
    </div>
    <div>
      <p style="font-size: 9pt; color: #666; margin-bottom: 4pt;">Website</p>
      <p style="font-size: 12pt; font-weight: 500; color: #ffffff;">www.company.com</p>
    </div>
  </div>
</body>
</html>
```

---

## 고급 디자인 패턴

### 비대칭 레이아웃
시선을 끄는 독창적인 구성
```css
/* 황금비율 기반 */
grid-template-columns: 1fr 1.618fr;

/* 극단적 비대칭 */
grid-template-columns: 1fr 3fr;
```

### 오버레이 텍스트
이미지 위 텍스트 배치
```html
<div style="position: relative;">
  <div style="position: absolute; inset: 0; background: rgba(0,0,0,0.5);"></div>
  <div style="position: relative; z-index: 1;">
    <h2 style="color: #fff;">Overlay Text</h2>
  </div>
</div>
```

### 그라데이션 오버레이
```html
<div style="
  background: linear-gradient(to right, #1a1a1a 0%, transparent 60%);
  position: absolute;
  inset: 0;
"></div>
```

### 카드 스타일
```html
<div style="
  background: #ffffff;
  border-radius: 12pt;
  padding: 24pt;
  box-shadow: 0 2pt 8pt rgba(0,0,0,0.08);
"></div>
```

---

## 텍스트 사용 규칙

### 필수 태그
```html
<!-- 모든 텍스트는 반드시 다음 태그 안에 -->
<p>, <h1>-<h6>, <ul>, <ol>, <li>

<!-- 금지 - PowerPoint에서 무시됨 -->
<div>텍스트</div>
<span>텍스트</span>
```

### 권장 사용법
```html
<!-- 좋은 예 -->
<h1 style="...">제목</h1>
<p style="...">본문 텍스트</p>

<!-- 나쁜 예 -->
<div style="...">텍스트 직접 입력</div>
```

---

## 출력 및 파일 구조

### 파일 저장 규칙
```
slides/
├── slide-01.html  (표지)
├── slide-02.html  (목차)
├── slide-03.html  (섹션 구분)
├── slide-04.html  (내용)
├── ...
└── slide-XX.html  (마무리)
```

### 파일 명명 규칙
- 2자리 숫자 사용: `slide-01.html`, `slide-02.html`
- 순서대로 명명
- 특수문자, 공백 사용 금지

---

## 워크플로우

1. **분석**: `slide-outline.md` 읽고 콘텐츠 파악
2. **테마 결정**: 색상 팔레트, 전체적인 무드 선택
3. **구조 설계**: 슬라이드별 레이아웃 타입 결정
4. **디자인 실행**: 각 슬라이드 HTML 생성
5. **일관성 검토**: 전체 프레젠테이션의 통일성 확인
6. **저장**: `slides/` 디렉토리에 파일 저장

---

## 주의사항

1. **CSS 그라데이션**: PowerPoint 변환 시 지원 안됨 - 배경 이미지로 대체
2. **웹폰트**: Pretendard CDN 링크 항상 포함
3. **이미지 경로**: 절대 경로 또는 URL 사용
4. **호환성**: 모든 색상에 # 포함
5. **텍스트 규칙**: div/span에 직접 텍스트 금지
