---
name: pokemon-green-ko
description: "포켓몬 그린 버전 텍스트 RPG. 1세대 151마리 포켓몬, 165개 기술, 관동 지방 완전 재현. 한국어 전용. 사용자가 '포켓몬', '피카츄', '전투', '체육관', '야생', '도감', '새 게임', '이어하기' 등의 키워드를 사용할 때 활성화됩니다. (project)"
trigger-keywords: 포켓몬, 피카츄, 체육관, 전투, 야생, 도감, 포켓몬스터, 새 게임, 이어하기, 포켓몬 그린
allowed-tools: Read, Write, Edit, Bash
---

# 포켓몬 그린 버전 - 텍스트 RPG (한국어)

1세대 포켓몬 그린 버전을 텍스트 기반 RPG로 완전 재현한 클로드 스킬입니다. (한국어 전용)

## When to Invoke

이 스킬은 다음 상황에서 자동 활성화됩니다:

- 사용자가 "포켓몬", "피카츄", "포켓몬스터" 언급 시
- "새 게임", "이어하기", "게임 시작" 요청 시
- "전투", "체육관", "야생", "도감" 관련 대화 시
- "pokemon", "pikachu" 영어 키워드 사용 시

## 게임 특징

- **151마리 포켓몬**: 이상해씨부터 뮤까지 완전 수록
- **165개 기술**: 모든 1세대 기술 구현
- **15타입 상성**: 1세대 고유 버그 포함
- **관동 지방**: 태초마을부터 포켓몬 리그까지
- **8개 체육관**: 웅, 이슬, 마티스, 민화, 독수, 초련, 강연, 비주기
- **세이브/로드**: 10개 슬롯 + 자동저장
- **BGM 자동재생**: 45곡 (macOS afplay)
- **ASCII 아트**: 151마리 포켓몬 스프라이트
- **울음소리**: 151마리 포켓몬 울음소리

---

## 게임 시작

### 초기화
```bash
pkill -f 'pokemon-green.*bgm' 2>/dev/null
```

### BGM 재생 규칙

파일 경로: `data/audio/bgm/[파일명].mp3`

#### 주요 BGM 파일명
| 상황 | 파일명 |
|------|--------|
| 오프닝 | opening.mp3 |
| 태초마을 | pallet_town.mp3 |
| 오박사 연구소 | oak_lab.mp3 |
| 도로 | route_theme.mp3 |
| 야생 전투 | wild_battle.mp3 |
| 트레이너 전투 | trainer_battle.mp3 |
| 포켓몬 센터 | pokemon_center.mp3 |

#### 재생 명령어
```bash
# BGM 중지
pkill -f 'afplay.*pokemon-green' 2>/dev/null

# BGM 재생 (백그라운드 반복, 필수!)
while true; do afplay [skillPath]/data/audio/bgm/[파일명].mp3 2>/dev/null || break; done
run_in_background: true
```

#### 에러 처리
- `|| break`: 파일 없을 시 무한루프 방지
- `2>/dev/null`: 에러 메시지 숨김

### 새 게임 / 이어하기
- "새 게임" - 새로운 모험 시작
- "이어하기" - 저장된 게임 불러오기

---

## 명령어 체계

### 필드 명령어

- **북/남/동/서**: 해당 방향으로 이동 (예: "북쪽으로")
- **[장소명]으로 이동**: 특정 장소로 이동 (예: "회색시티로 이동")
- **상태 / 파티**: 파티 포켓몬 확인 (예: "상태 확인")
- **가방**: 소지품 확인 (예: "가방 열기")
- **도감**: 포켓몬 도감 (예: "도감 보기")
- **저장**: 게임 저장 (예: "저장")
- **말 걸기**: NPC 대화 (예: "말 걸기")
- **NPC**: NPC 정보 확인 (예: "NPC 목록")

### 전투 명령어

- **싸운다**: 기술 선택 모드
- **[기술명] / [번호]**: 기술 사용
- **가방**: 아이템 사용
- **포켓몬**: 포켓몬 교체
- **도망**: 야생 전투에서 도망

### 오디오 명령어

- **bgm 끄기**: BGM 중지
- **bgm 켜기**: BGM 재생
- **볼륨 [0-100]**: 볼륨 조절
- **울음소리**: 포켓몬 울음소리

### 기술 효과음

효과음 매핑: data/audio/sfx-mapping.json

---

## 게임 진행 흐름

### 오프닝
1. 오박사 인사
2. 플레이어 이름 설정
3. 라이벌 이름 설정

### 태초마을
1. 오박사 연구소에서 스타터 선택 (이상해씨/파이리/꼬부기)
2. 라이벌과 첫 배틀
3. 상록시티 소포 심부름

### 모험 시작
- 1번 도로 → 상록시티 → 상록숲 → 회색시티 (첫 체육관)
- 8개 뱃지 수집 → 챔피언 로드 → 사천왕 → 챔피언

---

## 전투 시스템

### 오리지널 전투 화면 (1세대 재현)

전투 화면은 원작처럼 간결하게 표시합니다. 불필요한 팁이나 추가 정보 없이 필수 요소만 표시합니다.

**스프라이트 표시 규칙 (원작 재현)**:
- **상대 포켓몬**: 13줄 전체 표시 (우측 정렬) - 정면 모습
- **내 포켓몬**: 상단 5~6줄만 표시 (좌측, 좌우반전) - 뒷모습 느낌
- pokemon-ascii-mini.json 스프라이트는 13줄 × 28자
- 내 포켓몬은 좌우반전 후 상단만 잘라서 표시

**전투 화면 구성**:
```
╔════════════════════════════════════════════════════════════════╗
║  야생 Pokemon                                       Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓░░░░  HP                                           ║
║                                                                ║
║                                  [상대 포켓몬 스프라이트]      ║
║                                  (13줄 전체 - 우측 정렬)       ║
║                                  (정면 모습)                   ║
║                                                                ║
║  [내 포켓몬 - 뒷모습]                                          ║
║  (상단 5~6줄만 - 좌측)                                         ║
║  (좌우반전, 아래쪽 잘림)                                       ║
║                                                                ║
║  Pokemon                                            Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░  HP  22/22                                   ║
╠════════════════════════════════════════════════════════════════╣
║  야생 Pokemon(이/가) 나타났다!                                 ║
╠════════════════════════════════════════════════════════════════╣
║     싸운다              가방                                   ║
║     포켓몬              도망                                   ║
╚════════════════════════════════════════════════════════════════╝
```

**실제 전투 화면 예시**:
```
╔════════════════════════════════════════════════════════════════╗
║  야생 피카츄                                        Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓░░░░  HP                                           ║
║                                                                ║
║                                          :.            :+=.   ║
║                                        .**.       . .-*#**#-  ║
║                                        -*:    =*+::-+#***+-   ║
║                                    .-*##%#+-:#%#+=+**+*+-     ║
║                                    =%%#########- .=***-.      ║
║                                   =%*#%#*+.:%%#*-   -*#=      ║
║                                   .=*#%%#*++*##%%*..+=:       ║
║                                   .:.:+#*%#+=#%##*+=-:        ║
║                                        :**==+*=+%%#=..        ║
║                                         :+*+++#%#%*:          ║
║                                             .++*%*.           ║
║                                                 :             ║
║                                                                ║
║       :  :                                                     ║
║       ++=*.                                                    ║
║    .-+-+--==..                                                 ║
║ .-+*+==+-=++=++:                                               ║
║ :++==+++++=-+=-=-:..==                                         ║
║ :+=-=+==++--=---:-+**#+                                        ║
║                                                                ║
║  이상해씨                                            Lv.5      ║
║  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░  HP  22/22                                   ║
╠════════════════════════════════════════════════════════════════╣
║  야생 피카츄(이/가) 나타났다!                                  ║
╠════════════════════════════════════════════════════════════════╣
║     싸운다              가방                                   ║
║     포켓몬              도망                                   ║
╚════════════════════════════════════════════════════════════════╝
```

### 메시지 표시 원칙 (원작 준수)

**표시하는 것** (원작과 동일):
- "야생 [포켓몬](이/가) 나타났다!"
- "[포켓몬]의 [기술]!"
- "효과가 굉장했다!" 또는 "효과가 별로인 듯하다..."
- "급소에 맞았다!"
- "[포켓몬](은/는) 쓰러졌다!"
- 상태이상 메시지

**표시하지 않는 것** (원작에 없음):
- 데미지 숫자 (HP 바 감소로만 표현)
- 타입 상성 힌트/추천
- 기술 선택 팁
- 전술 조언
- AI의 행동 예측

### ASCII 아트 표시

- **전투 시작**: pokemon-ascii.json (전체 아트 1회)
- **전투 진행 중**: pokemon-ascii-mini.json (축소 아트)
- **도감**: pokemon-ascii.json (전체 아트)

### 데미지 계산 (1세대)
```
데미지 = ((2×Lv÷5+2) × Power × A÷D ÷ 50 + 2) × STAB × 상성 × 급소 × 난수
```

### 1세대 버그 재현
- 에스퍼 vs 고스트: 0배
- 포커스 에너지: 급소율 감소
- 독 vs 벌레: 2배

---

## NPC 시스템

### NPC 스프라이트 로딩 규칙

#### 로딩 순서 (필수!)
1. `data/sprites/npc-mapping.json`에서 한글→영문 변환
2. `data/sprites/npc_ascii/[영문명].json` 파일 로드
3. `.down` 키의 ASCII 아트 표시

#### jq 로딩 예시
```bash
# 스프라이트 로드 (한글 이름으로 직접 로드 불가!)
jq -r '.down | join("\n")' data/sprites/npc_ascii/Professor_Oak.json
```

#### 주요 NPC 영문 파일명
| 한글명 | 파일명 | 카테고리 |
|--------|--------|----------|
| 오박사 | Professor_Oak.json | 스토리 NPC |
| 간호순 | Nurse_Joy.json | 시설 NPC |
| 라이벌 | Rival.json | 챔피언 |
| 웅 | Brock.json | 체육관 관장 |
| 이슬 | Misty.json | 체육관 관장 |

#### 에러 처리
- 파일 없음: 스프라이트 생략, 대화만 표시
- JSON 파싱 실패: 기본 텍스트로 대체

### 대화 화면 예시
```
┌────────────────────────────────────┐
│  [NPC 스프라이트]                  │
│                                    │
│  간호순:                           │
│  "어서오세요! 포켓몬센터입니다."   │
├────────────────────────────────────┤
│  [1] 네    [2] 아니오              │
└────────────────────────────────────┘
```

---

## 세이브 시스템

### 저장
- 수동 저장: "저장" 또는 "저장 [슬롯번호]"
- 자동 저장: 포켓몬 센터, 도시 진입, 전투 후

### 세이브 슬롯 (10개 + 자동저장)

- **저장 [1-10]**: 특정 슬롯에 저장
- **불러오기 [1-10]**: 특정 슬롯 불러오기
- **세이브 목록**: 모든 슬롯 확인

---

## 체육관 정보

1. **회색시티** - 웅 (바위) → 회색뱃지
2. **블루시티** - 이슬 (물) → 블루뱃지
3. **갈색시티** - 마티스 (전기) → 오렌지뱃지
4. **무지개시티** - 민화 (풀) → 레인보우뱃지
5. **연보라시티** - 독수 (독) → 핑크뱃지
6. **황금시티** - 초련 (에스퍼) → 골드뱃지
7. **홍련마을** - 강연 (불꽃) → 크림슨뱃지
8. **상록시티** - 비주기 (땅) → 그린뱃지

---

## 데이터 파일 참조

### 포켓몬 데이터
- data/pokemon/species.json: 151마리 종족 데이터
- data/pokemon/learnsets.json: 레벨업 기술
- data/pokemon/evolutions.json: 진화 조건

### 기술/타입 데이터
- data/moves/moves.json: 165개 기술
- data/types/chart.json: 15타입 상성표

### 월드 데이터
- data/world/locations.json: 마을/도로
- data/world/encounters.json: 야생 출현
- data/world/trainers.json: 트레이너

### 오디오 데이터
- data/audio/bgm-mapping.json: 45곡 BGM 매핑
- data/audio/cries-mapping.json: 151마리 울음소리

### ASCII 아트
- data/sprites/pokemon-ascii.json: 전체 아트
- data/sprites/pokemon-ascii-mini.json: 축소 아트
- data/sprites/npc_ascii/: NPC 축소 아트 (94개 개별 파일)
- data/sprites/npc-mapping.json: NPC 한글→파일명 매핑

---

## 데이터 키 매핑 (최적화 형식)

### species.json
```
n=name, t=types, s=stats[hp,atk,def,spc,spd], c=catchRate, e=baseExp
g=growthRate(ms=medium_slow,mf=medium_fast,s=slow,f=fast), hw=[height,weight]
```

### moves.json
```
i=id, n=name, t=type, c=category, p=power, a=accuracy, pp=pp, pr=priority, ef=effect
타입코드: N=Normal,F=Fire,W=Water,G=Grass,E=Electric,I=Ice,K=Fighting,P=Poison,R=Ground,Y=Flying,S=Psychic,B=Bug,O=Rock,H=Ghost,D=Dragon
카테고리: P=Physical, S=Special, X=Status
```

### learnsets.json
```
lv=levelUp[[level,move]], tm=[번호], hm=[번호]
```

### encounters.json
```
g=grass, c=cave, w=water, f=fishing
포맷: [[포켓몬ID, minLv, maxLv, 출현율]]
```

### trainers.json
```
n=name, ti=title, g=gym, c=city, ty=type, b=badge, r=reward, tm=tmReward
o=order, d=dialogue, p=team[[id,lv,[moves]]], cl=class
gl=gymLeaders, e4=eliteFour, ch=champion, rt=routeTrainers
```

### items.json
```
n=name, d=desc, p=price, cm=catchMod, ha=heal, c=cures, ra=revive
ppr=ppRestore, am=allMoves, sb=statBoost, ef=effect, st=steps, et=evoType
카테고리: pb=pokeballs, pt=potions, sh=statusHealers, rv=revives, pp=ppItems
bt=battleItems, rp=repels, es=escapeItems, ev=evolutionStones, vi=vitamins
```

---

## 데이터 로딩

jq로 필요한 부분만 추출 (대용량 파일 전체 로드 금지)

```bash
jq '.["25"]' data/pokemon/species.json      # 종족값
jq '.["025"]' data/sprites/pokemon-ascii.json  # 스프라이트 (3자리)
```

키 형식:
- species, learnsets: 숫자 키 ("25")
- sprites: 3자리 키 ("025")

---

## References (상세 가이드)

상세한 시스템 정보는 다음 문서를 참조하세요:

- BGM 시스템 가이드 (references/bgm-guide.md) - BGM 자동재생, 명령어, 이벤트 매핑
- 기술 효과음 가이드 (references/sfx-guide.md) - 기술별 효과음, 다운로드 방법
- ASCII 아트 가이드 (references/ascii-guide.md) - ASCII 아트 사용 규칙, 데이터 파일
- NPC 시스템 가이드 (references/npc-guide.md) - NPC 스프라이트 표시, 이름 매핑
- 울음소리 가이드 (references/cries-guide.md) - 울음소리 재생 시점, 명령어
- 데이터 무결성 가이드 (references/data-integrity.md) - 데이터 검증 규칙, 체크리스트

---

## 언어 설정

이 스킬은 **한국어 전용**입니다.

영어 버전은 별도 스킬 `pokemon-green-en`을 사용하세요.

### 데이터 파일 구조

모든 이름/메시지는 한국어 단일 언어로 저장됩니다:
```json
{
  "name": "이상해씨",
  "text": "야생 포켓몬이 나타났다!"
}
```

메시지 파일:
- data/messages/battle.json - 전투 메시지

---

## 도움말

게임 중 언제든지 다음 명령어를 사용할 수 있습니다:
- "도움말" - 명령어 목록
- "현재 위치" - 현재 장소 정보
- "진행 상황" - 스토리 진행도
