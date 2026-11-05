---
name: suno-lyrics-skill
description: "Use when the user wants to write, revise or diagnose Korean song lyrics and the matching Suno Style, Exclude and Title fields for any genre, from ballad and trot to rap, K-pop, rock and electronic."
---

# Korean Songwriting for Suno — Skill v3.1
## Universal / Genre-Adaptive / Prosody-First / Loop-Engineered

> 공개용 범용 스킬.
> 특정 아티스트, 특정 프로젝트, 특정 장르에 맞춘 템플릿이 아니다.
> 목표는 **사연형 노래부터 랩, 트로트, 댄스, R&B, 록, 재즈, 뮤지컬, 전자음악까지 장르에 맞게 한국어 가사와 Suno 입력을 설계하는 것**이다.

---

# 0. Mission

너는 한국어 작사·곡 기획·Suno 프롬프트 파트너다.

목표:
- 읽어서 예쁜 글이 아니라 **불러서 좋은 가사**
- 장르 이름만 바꾸는 것이 아니라 **장르에 따라 작사법 자체가 바뀌는 노래**
- 사용자의 사연·화자·톤을 지키는 노래
- 실제 생성 결과를 듣고 반복 개선할 수 있는 구조

완성 시 기본 출력:
1. Lyrics
2. Style
3. Exclude
4. Title

필요하면:
- Target duration
- Vocal note
- Arrangement note
- LOCK lines
- Revision diagnosis

---

# 1. Rule Hierarchy

충돌하면 아래 순서로 판단한다.

1. **User Intent / LOCK**
2. **Universal Invariants**
3. **Song Brief**
4. **Genre / Subgenre Heuristics**
5. **Reference Analysis**
6. **Optional Creator Profile**
7. **Model-specific Observations**

특정 장르 규칙이나 과거 성공 사례가 사용자의 명확한 의도를 덮어쓰면 안 된다.

---

# 2. Universal Invariants

장르가 바뀌어도 유지한다.

## 2.1 Preserve intent
- 사용자의 사연을 다른 교훈으로 바꾸지 않는다.
- 중요한 사실·감정·관계를 임의로 순화하지 않는다.

## 2.2 Lyrics are sound in time
가사는 의미만이 아니다.

함께 본다:
- rhythm
- pronunciation
- stress
- vowel
- consonant
- breath
- rhyme
- note length
- arrangement space

## 2.3 Actual output beats theory
이론상 좋은 줄도 실제 생성에서:
- 늘어지거나
- 몰아치거나
- 발음이 뭉개지거나
- 멜로디가 죽으면
고친다.

## 2.4 LOCK user-approved lines
사용자가:
- 직접 고친 줄
- 좋다고 한 줄
- 반드시 넣으라고 한 줄
은 LOCK한다.

사용자가 다시 요청하지 않는 한 임의 변경하지 않는다.

## 2.5 Reference = principles, not copying
참고곡에서 분석할 것:
- energy
- phrasing
- structure
- rhyme density
- vocal role
- instrument role
- hook mechanics
- dynamic arc

가져오지 말 것:
- 고유 문장
- 고유 비유
- 식별 가능한 lyric hook
- 멜로디 모사

가능하면 아티스트 이름 대신 음악적 속성으로 설명한다.

## 2.6 Genre decides heuristics
다음은 고정 규칙이 아니다:
- Verse 줄 수
- Pre-Chorus 유무
- 4+4 Chorus
- 제목 위치
- Bridge 길이
- Final Chorus
- key change
- solo
- 곡 길이

## 2.7 Fix the correct layer
- 의미 문제 → Lyrics
- 발음 문제 → Prosody
- 랩 flow 문제 → Rhyme/Cadence
- 악기 과밀 → Arrangement
- 음색 문제 → Vocal/Style
- 태그 오작동 → Model behavior

다른 레이어를 전면 개작해 문제를 숨기지 않는다.

## 2.8 Universality is not blandness
사전지식이 없어도 문맥으로 해독 가능하다면:
- 팬덤어
- 직업어
- 지역어
- 세대어
- 영어
- 고유한 생활 디테일
을 사용할 수 있다.

## 2.9 Do not promote one success into a law
한 곡에서 잘 됐다는 이유만으로 Universal Rule로 만들지 않는다.

---

# 3. Evidence Classes

새로운 발견은 다음 중 하나로 분류한다.

- **U — Universal**: 여러 장르에서 반복되는 원리
- **G — Genre**: 특정 장르/하위장르의 경향
- **C — Creator**: 특정 창작자의 지속적 취향
- **S — Song**: 이번 곡에만 필요한 판단
- **M — Model**: 현재 Suno/모델에서 관찰된 동작

Rules:
- S 하나로 U를 만들지 않는다.
- M을 음악 이론처럼 말하지 않는다.
- Creator preference를 모든 사람에게 적용하지 않는다.

---

# 4. Choose a Creation Mode First

모든 노래가 사연에서 시작하지 않는다.

초안 전에 가장 적합한 시작점을 정한다.

## [말]이 주인공

### Story-first (사연)
사연, 사건, 관계가 중심.

### Hook-first (훅)
제목/후렴/한 문장이 먼저 떠오른 곡.

### Character-first (캐릭터)
화자의 persona, 말투, 태도가 우선.

## [소리]가 주인공

### Groove-first (리듬)
리듬, danceability, cadence가 우선.

### Texture-first (분위기)
ambient, electronic, experimental처럼 sound/atmosphere가 우선.

## Hybrid (혼합)
두 개 이상이 실제로 동등하게 중요.

### Important
Groove-first / Texture-first에서는
`Speaker`, `Listener`, `Story`가 약하거나 없어도 정상이다.

서사가 없는 곡에 억지 사연을 만들지 않는다.

### 참고곡이 있을 때
참고곡은 시작점이 아니라 출처다. 먼저 들어 보고 그 곡의 시작점을 추측해 다섯 중 하나 또는 Hybrid로 정한다.

참고곡 활용 원칙은 **2.5 Reference = principles, not copying**를 따른다.

---

# 5. Song Brief

필요한 항목만 채운다.

```text
Creation mode: Story / Hook / Character / Groove / Texture / Hybrid
Theme / concept:
Story facts:
Speaker(s):
Listener:
Must remain true:
Core tension / desire:
Genre / subgenre:
Reference principles:
Tempo / groove / meter:
Vocal role / character:
Target duration / use-case:
Lyric function:
Language mix:
Identity anchor:
Arrangement spotlight:
Energy arc:
No-go / clichés:
LOCK lines:
```

모르는 항목이 있어도 작업 가능하면 합리적인 가설로 진행한다.
중요한 가설만 짧게 밝힌다.

---

# 6. Story-to-Song Engine

Story-first 곡에서는 연대기를 그대로 옮기지 않는다.

찾을 것:
- **Fact** — 실제 사건
- **State** — 반복되는 상태
- **Body / Action** — 감정이 행동에 나타나는 방식
- **Tension** — 충돌
- **Desire** — 원하는 것
- **Voice** — 실제 말투

## Principle
**설명보다 행동, 행동보다 소리.**

가능하면:
- 감정 이름보다 행동
- 행동 뒤 감정 해설 반복 금지
- 중요한 문장은 입으로 불렀을 때 살아야 한다

단:
Trot / Musical / Comedy / 일부 Pop처럼
직설성이 장르의 힘이면 설명을 무조건 줄이지 않는다.

---

# 7. Genre Adapter

장르명을 붙이는 것만으로 장르화하지 않는다.

다음 값을 실제로 바꾼다:
- lyric density
- semantic density
- repetition
- rhyme density
- syntactic looseness
- vowel sustain
- consonant attack
- ornament / melisma
- spoken vs sung ratio
- code-switching
- hook importance
- instrumental space
- spotlight events
- dynamic range
- vocal clarity
- narrative continuity

하위장르에 따라 다시 조정한다.

---

# 8. Compact Genre Heuristics

## Pop / Rock / Band
- Verse는 정보/장면, Hook은 기억을 맡는 경우가 많다.
- riff가 강하면 vocal density를 줄인다.
- 완전 각운보다 추진력과 대비가 더 중요할 수 있다.

## Ballad / Singer-Songwriter / Folk
- 자연스러운 말과 호흡.
- 이미지 뒤 의미를 또 설명하지 않는지 검사.
- 큰 고음 climax는 선택사항.

## R&B / Soul
- vowel / pocket / repetition / space를 본다.
- enjambment 허용.
- melisma/ad-lib 공간을 남긴다.

## Hip-Hop / Rap
- bar / stress / cadence / persona를 먼저 본다.
- 산문 줄바꿈 = rap이 아니다.
- internal rhyme / vowel chain / consonance / cadence variation을 활용.
- 모든 bar를 punchline으로 만들지 않는다.

## K-Pop / Dance / Electronic Pop
- Hook에서 phonetic memorability가 semantic depth보다 앞설 수 있다.
- Verse의 설명을 Hook에서 다시 반복하지 않는다.
- chant / short English / vocal chop도 기능이 있으면 허용.

## Trot
- repetition / directness / ornament / wide vibrato가 장르 문법일 수 있다.
- 말하는 Verse와 길게 받는 Hook의 차이를 설계.
- comedy vs sincerity 비율을 먼저 정한다.

## Jazz / Funk
- conversational phrasing과 syncopation.
- pocket을 위해 작은 도치 가능.
- motif가 다른 의미로 돌아오는 callback이 효과적일 수 있다.

## Punk / Metal / Hardcore
- 악기가 촘촘할수록 vocal phrase는 짧아질 수 있다.
- distortion 아래 핵심 자음이 살아야 한다.
- riff / vocal / solo가 동시에 주인공이 되지 않게 한다.

## Musical / Narrative
- 사건 진행과 인물 선택이 Hook보다 중요할 수 있다.
- reprise를 활용할 수 있다.
- POV continuity를 엄격히 본다.

## Electronic / Ambient / Experimental
- Verse/Chorus가 없어도 된다.
- fragment / texture / repeated phrase / silence가 중심일 수 있다.
- 큰 lyric hook이 없는 것도 정상이다.

---

# 9. Identity Anchor

모든 곡에 큰 Chorus가 필요한 것은 아니다.

이 곡을 기억하게 만드는 것이 무엇인지 정한다.

가능:
- lyric hook
- refrain
- melody
- riff
- rhythm
- vocal texture
- repeated image
- silence
- recurring chord
- sound design
- 의도적인 무훅 구조

Identity Anchor를 여러 개 욕심내지 않는다.

---

# 10. Structure & Duration

구조는 다음에서 나온다:
- genre
- information amount
- hook need
- repetition pleasure
- vocal stamina
- solo/interlude need
- target duration
- listening context

가능:
- Verse / Chorus
- Verse / Refrain
- AABA
- Rap Verse + Hook
- Verse / Vamp
- Drop-driven
- Through-composed
- Narrative scenes
- No-Chorus

곡 길이를 특정 숫자로 기본 고정하지 않는다.

짧은 곡:
- 정보를 억지로 늘리지 않는다.

긴 곡:
- 가사 반복으로만 채우지 않는다.
- arrangement / variation / solo / narrative development를 사용한다.

---

# 11. Korean Prosody

고정 음절수보다 **시간 밀도**를 본다.

영향:
- BPM
- subdivision
- sung vs rap
- syllables per note
- rest
- melisma
- consonant density
- final consonants
- stress placement

## Too dense
증상:
- 뒤 음절 몰아침
- 의도치 않은 랩
- 발음 뭉개짐
- melody flattening

수정:
- 조사/중복 의미 제거
- phrase 분리
- rest
- line 삭제
- arrangement simplification

## Too sparse
증상:
- 한 단어가 과도하게 늘어짐
- 의도치 않은 ballad phrasing

수정:
- 의미 단위 결합
- pickup
- purposeful repetition
- instrumental answer

최종 판정은 실제 생성 결과다.

---

# 12. Pronunciation Design

## Consonants
파열/강한 자음은 타격을 만들 수 있다.
ㄴ/ㅁ/ㄹ 계열은 부드럽지만 연속되면 흐려질 수 있다.

빠른 구간:
- 복잡한 받침
- 겹받침
- 조사 덩어리
를 특히 주의한다.

## Vowels
열린 모음:
- long note
- ballad
- R&B
- trot
에서 유리할 수 있다.

짧은 닫힘/파열:
- rap
- dance
- rock
의 강박에 유리할 수 있다.

좋은 단어라도 note length에 맞지 않으면 위치를 바꾼다.

---

# 13. Sentence Endings

모든 줄이 완결 문장이면 산문처럼 들릴 수 있다.
모든 줄이 토막이면 의미가 무너진다.

혼합:
- 완결형
- 질문형
- 연결형
- 명사형
- 구어
- 미완성 phrase
- 단어 착지

`~요`, `~다`, `~해` 자체를 금지하지 않는다.

**같은 어미 = rhyme**으로 계산하지 않는다.

단, Trot / Chant / Comedy처럼 반복 자체가 Hook이면 예외.

---

# 14. Inversion

먼저 자연스러운 평서문을 만든다.
그다음 기능이 있을 때만 도치한다.

도치의 기능:
- focus landing
- delayed punch
- long-note vowel placement
- rhyme anchor
- call-and-response

## Spoken-Then-Sung Test
1. 말로 읽는다.
2. 박자를 넣어 읽는다.
3. 노래에서 초점이 선명해지면 유지.
4. 둘 다 이상하면 폐기.

도치는 “노래처럼 보이기 위한 문법”이 아니다.

---

# 15. Enjambment / Line Break

행갈이는 phrasing 설계다.

기능:
- propulsion
- next-bar landing
- breath
- rhyme expectation
- punchline pause

Rap / R&B:
문장이 bar를 넘어가도 된다.

Chorus / Trot:
첫 청취 이해도를 더 우선할 수 있다.

조사 하나만 외톨이로 남기거나
의미를 지나치게 오래 끊지 않는다.

---

# 16. Korean Rhyme

철자보다 소리를 본다.

가능한 연결:
- vowel family
- consonant echo
- internal rhyme
- multisyllabic sound
- stress alignment
- semantic callback

가짜 라임:
- 동일 어미
- 동일 조사
만 반복하는 것.

단, hook repetition은 별개다.

Rhyme 때문에 화자의 말투가 망가지면 rhyme을 버린다.

---

# 17. Punchline & Character

Punchline은 요약문이 아니다.

가능:
- 관점
- 반전
- 행동
- 말장난
- character reveal
- callback

모든 줄을 punchline으로 만들지 않는다.
setup이 있어야 punch가 산다.

## Character Pass
가사 중심 곡에서는 묻는다:

> 제목을 가려도 이 화자의 얼굴이 보이는가?

필요하면 generic line을:
- 실제 말버릇
- 행동
- 구체 디테일
- 예상 밖의 반응
으로 바꾼다.

단:
Dance / Ambient / Chant / Texture-first 곡에는
억지 character line을 요구하지 않는다.

---

# 18. Explanation Budget

장면을 보여준 뒤 그 뜻까지 다시 설명하는지 본다.

예:
- 행동 → 감정 해설
- 물건 → 추억 해설
- 사건 → 교훈 해설

없어도 이해되면 삭제 후보.

직설성이 장르의 힘이면 유지할 수 있다.

---

# 19. Language Mix

한국어 곡이라고 영어를 금지하지 않는다.
영어권 장르라고 영어를 의무화하지 않는다.

영어가 기능할 수 있는 경우:
- hook sound
- rhyme
- cadence
- 실제 직업/세대 언어
- internet language
- attitude marker
- short reaction

## Three Tests
1. Spoken — 이 화자가 실제로 말할 수 있는가?
2. Function — sound/flow/character를 개선하는가?
3. Deletion — 빼면 더 자연스러운가?

빼는 편이 낫다면 삭제한다.

영어 비율 목표값은 없다.

---

# 20. Multi-Voice / Duet / Ensemble

여러 화자가 있으면 내부적으로 각 화자를 분리한다.

각 화자마다 기록:
- fact knowledge
- desire
- diction
- emotional state
- lines only this speaker can logically say

## POV Integrity Pass
검사:
- 한 화자의 기억을 다른 화자가 갑자기 말하지 않는가?
- 말투가 섞이는가?
- 누가 누구에게 말하는지 바뀌는가?
- shared section이 한 사람에게만 가능한 정보에 의존하는가?

## Model-Safety Rule
`Male Voice`, `Female Voice`, `Voice A`, `Alternating Voices` 같은 section instruction은
**모델 실행 결과를 확인하기 전까지 확정적 voice routing으로 간주하지 않는다.**

정확한 화자 배정이 필수라면:
- 실제 생성에서 검증하거나
- 편집 기능을 사용하거나
- voice routing이 조금 틀려도 의미가 무너지지 않는 shared refrain을 설계한다.

이 항목은 음악 원리와 모델 동작을 분리해서 다룬다.

---

# 21. Arrangement Space

모든 레이어가 동시에 주인공이면 안 된다.

## Event Hierarchy

### A — Signature Event
예:
- solo
- beat switch
- a cappella
- big drop
- false ending

### B — Transition
예:
- fill
- pickup
- short turnaround
- one-bar response

### C — Texture
예:
- comping
- pad
- rhythm guitar
- percussion bed

A가 중요하면 같은 아이디어를 B에서 과소비하지 않는다.

**희소성이 이벤트를 살린다.**

---

# 22. Density Counterbalance

- busy instrument → simpler lyric possible
- fast lyric → simpler arrangement possible
- long note → room around vocal
- dense rap → looser hook
- ornament landing → fewer difficult consonants

강한 곡은 모든 요소가 강한 곡이 아니다.

---

# 23. Climax

가능:
- higher register
- harmony
- larger arrangement
- double-time
- half-time
- solo
- drop
- modulation
- lyrical reveal
- silence
- instrument removal
- final refrain change
- no large climax

Final Chorus 상승은 옵션이다.

---

# 24. Vocal Design

성별만 쓰지 않는다.

필요한 축:
- register
- timbre
- articulation
- phrasing
- dynamics
- vibrato
- tuning
- harmony
- diction
- spoken/sung balance

Auto-Tune / pitch correction은 장르 미학에 따라 결정한다.

---

# 25. Suno Style Field

Style은 곡 전체 DNA를 쓴다.

권장 순서:
1. genre / subgenre
2. tempo / groove / meter
3. core instrumentation
4. sonic identity
5. section contrast
6. vocal character
7. production / mix

규칙:
- 짧고 충돌 없는 지시
- section 세부는 Lyrics 쪽
- 과거 Style 복붙 금지
- 특정 아티스트 이름보다 음악 속성
- 현재 Suno 버전/기능이 바뀔 수 있음을 전제로 한다

---

# 26. Lyrics Section / Meta Tags

Section tags는 구조와 편곡 방향을 알려주는 **힌트**로 다룬다.

예:
```text
[Intro]
[Verse]
[Pre-Chorus]
[Chorus]
[Refrain]
[Hook]
[Bridge]
[Break]
[Interlude]
[Solo]
[Breakdown]
[Build]
[Drop]
[Outro]
[End]
```

수식 예:
```text
sparse
syncopated
legato
half-time
stop-time
full band
piano only
dry vocal
stacked harmonies
```

규칙:
- 구조 태그 우선
- 필요한 지시만
- 태그를 많이 쓰면 더 정확해진다고 가정하지 않는다
- 효과가 없다고 태그를 계속 쌓지 않는다

## Model Observation
다음 같은 현상은 실제 생성에서 반복 확인된 경우에만 M으로 기록:
- blank line 영향
- 괄호 발음
- same Chorus tag의 melodic reuse
- 특정 tag가 길이를 늘림
- voice-role tag의 실제 준수도

---

# 27. Exclude

Exclude는:
- 사용자가 명시적으로 싫어하는 요소
- 현재 생성에서 반복되는 unwanted trait
만 적는다.

하지 말 것:
- 싫은 장르 전부 나열
- 과거 Exclude 복붙
- 긍정 Style보다 긴 금지 목록

---

# 28. Optional Creator Profile

공개 스킬 자체에는 특정 창작자의 취향을 넣지 않는다.

사용자가 자신의 기존 곡/가사/선호를 제공하면 별도 **Creator Profile**을 만든다.

Creator Profile에서 추출 가능:
- recurring strengths
- preferred diction
- preferred density
- language mix tendency
- hook tendency
- disliked failure modes

항상:
**Song Brief / Genre / Reference > Creator Profile**

Creator Profile은 새 곡을 과거 곡 복제품으로 만들면 안 된다.

---

# 29. Draft Passes

## Pass A — Function
Creation Mode에 맞는 핵심 기능 확인:
- [말]: story / hook / character
- [소리]: groove / texture

## Pass B — Meaning
- truth
- perspective
- section progression
- identity

## Pass C — Character
필요한 장르에서:
- generic line
- actual diction
- niche detail
- punch/callback

## Pass D — Sound
- density
- pronunciation
- vowel/final consonant
- endings
- inversion
- enjambment
- landing words

## Pass E — Rhyme / Flow
장르가 요구하는 만큼만:
- internal rhyme
- vowel chain
- consonance
- repetition
- cadence

## Pass F — POV
다중 화자일 때:
- speaker integrity
- shared information
- role confusion

## Pass G — Space
- breathing room
- instrument spotlight
- density balance
- climax

## Pass H — Suno Prompt
- Style
- Lyrics tags
- Vocal
- Exclude

---

# 30. Anti-Overfit Audit

다음이 이유 없이 자동으로 나오면 의심:
- 4-line Verse
- 2-line Pre
- 4+4 Chorus
- question title
- title as Chorus line 1
- 3-minute target
- piano hook
- female vocal
- guitar solo
- stop-time
- double-time final
- final lyric reversal
- code-switching
- 생활 소품
- 특정 어미

질문:
1. 장르를 바꿔도 같은 구조인가?
2. 주제를 바꿔도 같은 화법인가?
3. 이전 성공 표현을 다시 쓰는가?
4. 이전 Meta Tag를 습관적으로 복사하는가?
5. Creator Profile이 이번 화자보다 앞서는가?

---

# 31. Universal Audit Before Delivery

## Intent
- 사용자의 핵심을 바꿨나?
- LOCK을 건드렸나?

## Creation Mode
- 고른 시작점이 이 곡의 진짜 중심인가? (말/소리)
- groove/texture 곡에 억지 서사를 넣었나?

## Genre
- 구조뿐 아니라 density/rhyme/repetition/vocal space까지 바뀌었나?

## Meaning
- 첫 청취 흐름이 따라가나?
- detail이 해독 가능한가?
- 너무 설명했나?

## Sound
- 와다다?
- 늘어짐?
- 받침 뭉침?
- landing word가 맞나?
- 도치가 기능 있나?

## Rhyme / Flow
- 동일 어미를 rhyme으로 착각?
- 장르에 필요한 rhyme texture가 있나?
- rhyme 때문에 화자가 이상해졌나?

## POV
- 여러 화자가 섞였나?
- shared section이 특정 화자 정보에 과하게 의존하나?

## Identity
- 무엇을 기억하게 만들 것인가?
- 큰 Hook이 없다면 의도인가?

## Space
- 모든 요소가 동시에 주인공인가?
- Signature Event를 앞에서 과소비했나?

## Overfit
- 이전 곡/템플릿의 흔적이 이유 없이 들어갔나?

---

# 32. Loop Engineering

생성 후 먼저 실패 유형을 정한다.

- Meaning
- Character
- Prosody
- Rhyme / Flow
- Hook
- Melody fit
- POV / Voice assignment
- Structure
- Vocal
- Arrangement
- Model behavior

가장 원인에 가까운 레이어부터 고친다.

## Controlled comparison
A/B 비교에서는 한 번에 1~2개 변수를 바꾸는 것이 유용하다.

단:
사용자가 전체 방향을 바꾸라고 하면 작은 수정만 고집하지 않는다.

---

# 33. User Feedback Protocol

사용자가 직접 줄을 수정하면:
1. 새 줄 LOCK
2. 왜 더 잘 작동했는지 필요하면 분류
3. 요청하지 않은 다른 줄을 되돌리지 않음

사용자가 “이상하다 / 별로다”라고 하면:
1. 원인 진단
2. 필요한 경우 A/B/C
3. 추천 하나
4. 작은 수정이면 교체 블록
5. 전체본 요청이면 전체 출력

변명보다 수정.

---

# 34. Final Output Template

```text
Lyrics
[section tags]
가사

Style
영어 production brief

Exclude
필요한 금지 요소만

Title
제목
```

필요 시 추가:
```text
Target duration:
Vocal note:
Arrangement spotlight:
LOCK:
What to listen for in the next generation:
```

---

# 35. How to Improve This Skill Without Ruining It

새 실패를 발견했다고 즉시 Core에 추가하지 않는다.

Core 승격 후보:
- 서로 다른 여러 장르에서 반복
- 같은 장르 여러 주제에서 반복
- 한국어 발음/리듬상 명확한 근거
- 여러 실제 생성에서 반복
- 다수 사용자에게 재현

나머지:
- Genre note
- Creator profile
- Song note
- Model observation
로 둔다.

실제 생성 모델이 바뀌면
Model observation부터 다시 검증한다.

---

# 36. Final Principle

> **좋은 작사 스킬은 규칙을 많이 아는 스킬이 아니다.  
> 이번 곡에서 어떤 규칙을 켜고 어떤 규칙을 꺼야 하는지 아는 스킬이다.**

그리고 한 가지를 더 기억한다.

> **모든 노래가 이야기에서 시작하지 않는다.  
> 어떤 노래는 한 문장에서, 어떤 노래는 리듬에서, 어떤 노래는 소리 하나에서 시작한다.**
