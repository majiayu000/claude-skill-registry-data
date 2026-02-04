---
name: squares
description: 본 문서는 수 십개의 작은 사각형으로 글씨를 만드는 JavaScript 코드를 생성하는 개발 지침을 제공합니다. 텍스트를 화면에 표시 할 때, 일반 벡터 텍스트를 그대로 쓰지 않고, 수십 개의 작은 정사각형(픽셀)을 격자 형태로 찍어 "Hello, World! It's sure bright out here!" 문자열을 표현합니다. 브라우저에서 바로 실행 가능한 순수 HTML+JavaScript 예제를 만듭니다.
---


# 글씨를 작은 사각형으로 표현하기

## 결과물

- `index.html` 파일 안에서 `<script> ... </script>` 내부에 순수 JavaScript 코드로 작성
- 캔버스(canvas) 요소를 사용하지 말고, 그냥 `<div>` 요소 안에
- 수십 개의 작은 정사각형(픽셀)을 격자 형태로 찍어
- "Hello, World! It's sure bright out here!" 문자열을 표현합니다.
- 각 정사각형은 CSS로 스타일링된 `<div>` 요소로 구현
- 글씨는 중앙 정렬
- 페이지 하단에 입력 창이 있고 사용자가 글씨를 입력하면, 해당 글씨가 작은 사각형으로 표현되어 갱신됩니다.

## UI & 스타일 가이드라인

중앙 정렬된 캔버스 1개와, 아래에 네 개의 슬라이더(라벨 포함):
- 격자 간격(CELL) 4~20 (기본 8)
- 점 크기(SQUARE) 2~20 (기본 6)
- 폰트 크기(FONT_SIZE) 80~260 (기본 160)
- 임계값(THRESHOLD, 알파값) 40~240 (기본 120)
- 배경은 어두운 톤, 점(사각형)은 밝은 색. 둥근 모서리, 은은한 그림자 적용.
- 시스템/한글 가독성 좋은 폰트 스택 사용: "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif

## 개발 지침


1. HTML 구조 설계
   - `<div id="canvas"></div>`: 글씨를 표현할 영역
   - `<input type="text" id="textInput" value="Hello, World! It's sure bright out here!">`: 사용자 입력 창
   - 슬라이더 4개와 라벨
   - 각 요소에 적절한 ID와 클래스를 부여하여 스타일링 및 JavaScript에서 접근 가능하도록 함.
   - CSS 스타일링
   - 배경색, 글씨 색상, 폰트 스타일, 정사각형 스타일 등 정의
   - JavaScript 로직 구현
   - 캔버스 초기화 함수: 격자 크기, 점 크기, 폰트 크기, 임계값 설정
   - 글씨 렌더링 함수: 입력된 텍스트를 작은 사각형으로 변환하여 캔버스에 표시
   - 이벤트 리스너: 입력 창과 슬라이더 값 변경 시 글씨 갱신
2. JavaScript 코드 작성
   - `renderText(text)` 함수: 주어진 텍스트를 작은 사각형으로 변환하여 캔버스에 렌더링
   - `updateSettings()` 함수: 슬라이더 값 변경 시 설정 업데이트 및 글씨 갱신
   - 이벤트 리스너 등록: 입력 창과 슬라이더에 이벤트 리스너 추가
   - 초기화 함수 호출: 페이지 로드 시 초기 설정 및 글씨 렌더링
   - 최적화 및 테스트
