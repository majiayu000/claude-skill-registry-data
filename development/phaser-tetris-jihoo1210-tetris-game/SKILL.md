---
name: phaser-tetris
description: Phaser 3 테트리스 게임 개발 스킬. 테트리스 가이드라인(SRS, Wall Kick, 7-Bag)을 준수하여 구현한다. context7 MCP로 최신 Phaser API를 조회하고, 공식 테트리스 위키를 참고한다.
---

# Phaser 3 테트리스 개발 스킬

## MCP 활용 (필수!)

### Context7 - Phaser API 조회
Phaser API 사용 전 반드시 context7로 최신 문서를 조회한다:
- resolve-library-id: "phaser"로 라이브러리 확인
- get-library-docs: 필요한 API 문서 조회

예시 상황:
- Graphics API 사용법 불확실 → context7 조회
- Input.Keyboard 사용법 불확실 → context7 조회
- Time.addEvent 사용법 불확실 → context7 조회

### Sequential-thinking - 복잡한 로직
게임 로직 설계 전 sequential-thinking으로 단계별 계획 수립:
- 회전 시스템 설계
- 충돌 검사 로직
- 라인 클리어 알고리즘


## 테트리스 가이드라인 (Tetris Guideline)

공식 테트리스는 표준 규칙을 따른다. 아래 원칙을 준수하여 구현한다.

### 1. 플레이필드 (Playfield)
- 표준 크기: 10열 x 20행 (보이는 영역)
- 버퍼 영역: 상단 2-4행 (블록 스폰용, 보이지 않음)
- 셀 크기: 자유롭게 설정 (권장 20-30px)

### 2. 테트로미노 7종
| 이름 | 모양 | 색상 (권장) |
|------|------|-------------|
| I | 1x4 직선 | 하늘색 (Cyan) |
| O | 2x2 정사각형 | 노란색 (Yellow) |
| T | T자 모양 | 보라색 (Purple) |
| S | S자 모양 | 초록색 (Green) |
| Z | Z자 모양 | 빨간색 (Red) |
| J | J자 모양 | 파란색 (Blue) |
| L | L자 모양 | 주황색 (Orange) |

### 3. SRS (Super Rotation System)
테트리스 공식 회전 시스템:
- 모든 블록은 중심점을 기준으로 시계방향 90도 회전
- I, O 블록은 그리드 교차점이 회전 중심
- J, L, S, T, Z 블록은 블록 중앙이 회전 중심
- 4가지 회전 상태: 0(스폰), R(시계1회), 2(180도), L(반시계1회)

참고: https://tetris.wiki/Super_Rotation_System

### 4. Wall Kick (벽 차기)
회전 시 충돌하면 자동으로 위치 조정 시도:
- 기본 회전 위치 시도
- 실패 시 미리 정의된 오프셋 위치들을 순차 시도
- 모든 오프셋 실패 시 회전 취소

J, L, S, T, Z 블록 킥 테이블 (0→R 예시):
(0,0) → (-1,0) → (-1,+1) → (0,-2) → (-1,-2)

I 블록은 별도의 킥 테이블 사용

참고: https://harddrop.com/wiki/SRS

### 5. 7-Bag Randomizer
공정한 블록 분배 시스템:
- 7종 블록을 한 세트(가방)로 묶음
- 가방 내 블록을 무작위 순서로 제공
- 가방이 비면 새 가방 생성
- 효과: 최대 12개 블록 내에 모든 종류 등장 보장

### 6. 스폰 규칙
- 스폰 위치: 상단 중앙 (행 21-22, 보이는 영역 위)
- 스폰 방향: 수평 (flat-side up)
- 스폰 즉시 충돌 시: 게임오버

### 7. Lock Delay (고정 지연)
- 바닥/블록에 착지 후 일정 시간 조작 가능
- 이동/회전 시 타이머 리셋 (무한 스핀 방지 위해 횟수 제한 권장)
- 권장: 0.5초, 최대 15회 리셋

### 8. 점수 시스템
| 액션 | 기본 점수 |
|------|-----------|
| 1줄 클리어 (Single) | 100 |
| 2줄 클리어 (Double) | 300 |
| 3줄 클리어 (Triple) | 500 |
| 4줄 클리어 (Tetris) | 800 |
| T-Spin | 보너스 추가 |

점수 = 기본점수 x 레벨


## Phaser 3 구현 가이드

### 기본 설정 원칙
- type: Phaser.AUTO (WebGL 우선, Canvas 폴백)
- scene: 단일 씬 또는 다중 씬 (메뉴, 게임, 게임오버)
- 반드시 context7로 최신 config 옵션 확인

### 렌더링 원칙
- Graphics 객체: 한 번 생성, clear() 후 재사용
- update()에서 new 키워드 사용 금지
- 변경 시에만 다시 그리기 (needsRedraw 플래그)

### 입력 처리 원칙
- createCursorKeys(): 방향키 처리
- addKey(): 개별 키 추가 (Space, R 등)
- JustDown(): 키 반복 방지

### 타이머 원칙
- Time.addEvent(): 자동 낙하 타이머
- delay 속성 동적 변경으로 속도 조절

### 성능 원칙
- 60fps 유지 목표
- 객체 풀링 고려 (파티클 등)
- requestAnimationFrame 자동 관리됨


## 구현 순서 권장

1. 기본 구조: Phaser 설정, 캔버스, 전역 변수
2. 보드: 그리드 배열, 렌더링 함수
3. 테트로미노: 7종 정의, 스폰, 렌더링
4. 이동: 좌우 이동, 충돌 검사
5. 회전: SRS 회전, Wall Kick
6. 낙하: 자동 낙하, 소프트/하드 드롭
7. 고정: Lock Delay, 보드에 블록 고정
8. 라인 클리어: 완성 줄 감지, 제거, 위 블록 낙하
9. 점수/레벨: 점수 계산, 레벨업, 속도 증가
10. 게임오버: 감지, 표시, 재시작
11. UI: 점수, 레벨, 다음 블록, Hold


## 참고 자료

- Tetris Guideline: https://tetris.wiki/Tetris_Guideline
- SRS 상세: https://tetris.wiki/Super_Rotation_System
- Wall Kick: https://harddrop.com/wiki/SRS
- Phaser 3 공식: https://phaser.io/phaser3
