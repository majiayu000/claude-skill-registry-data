---
name: tables-appendix
description: 고찰 보강을 위한 비교표·부록·참고문헌 생성
tags: [archaeology, tables, appendix, references, pipeline-step-5]
---

# Tables & Appendix - 도표 및 부록 생성

## 목적
고찰(discussion.md) 본문을 보강하고 규정 준수를 위해 필요한 각종 비교표, 일람표, 참고문헌 목록, 도면·사진 목록을 자동 생성합니다.

## 입력
- `output/draft/discussion.md`: 고찰 초안
- `output/normalized/metadata.csv`: 수집 자료 메타데이터
- `output/compare/nearby_ranked.csv`: 주변 유적 목록
- `output/compare/nearby_summaries.jsonl`: 주변 유적 요약

## 생성 항목

### 1. 주변 유사 유적 비교표
발굴조사 보고서 고찰의 필수 요소인 주변 유적 비교를 명확히 제시하는 종합 비교표:

```markdown
## 표 1. 주변 유사 유적 비교표

| 연번 | 유적명 | 소재지 | 거리(km) | 시대 | 주요 유구 | 주요 유물 | 특징 | 조사기관/연도 |
|------|--------|--------|----------|------|-----------|-----------|------|---------------|
| 1 | △△유적 | ○○시 ××동 | 5.2 | 청동기 전기 | 원형주거지 8기 | 무문토기, 석촉 | 환상배치 | ○○연구원(2018) |
| 2 | □□유적 | ○○시 ◇◇동 | 12.8 | 청동기 후기 | 방형주거지 15기 | 마제석검, 석도 | 대규모 취락 | △△대학교(2019) |
| 3 | ☆☆유적 | ○○군 ▽▽면 | 18.5 | 원삼국 | 방형주거지 6기, 수혈 20기 | 적색마연토기, 철기 | 주거+저장 복합 | ××연구소(2020) |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**비교 기준**:
- 거리: 대상지(위도 37.5665, 경도 126.9780)로부터의 직선거리
- 시대: 주요 사용 시기 (복수 가능)
- 유사도: 공간(40%), 시대(30%), 유형(30%) 가중 평균
```

**생성 로직**:
```python
def generate_comparison_table(nearby_ranked_csv):
    """주변 유적 비교표 생성"""
    df = pd.read_csv(nearby_ranked_csv)
    df = df.sort_values('similarity_score', ascending=False).head(10)

    table = "| 연번 | 유적명 | 소재지 | 거리(km) | 시대 | 주요 유구 | 주요 유물 | 특징 | 조사기관/연도 |\n"
    table += "|------|--------|--------|----------|------|-----------|-----------|------|---------------|\n"

    for idx, row in df.iterrows():
        table += f"| {idx+1} | {row['title']} | {row['location']} | "
        table += f"{row['distance_km']} | {row['period']} | "
        table += f"{row['features']} | {row['artifacts']} | "
        table += f"{row['characteristics']} | {row['reference']} |\n"

    return table
```

### 2. 유구 종류별 일람표
조사된 모든 유구를 종류별로 정리:

```markdown
## 표 2. 유구 일람표

### 2-1. 주거지

| 유구번호 | 평면형태 | 규모(m) | 면적(㎡) | 주요시설 | 출토유물 | 시대 추정 | 비고 |
|----------|----------|---------|----------|----------|----------|-----------|------|
| H-01 | 원형 | 직경 4.5 | 15.9 | 노지, 벽구 | 무문토기 구연부 3점, 석촉 1점 | 청동기 전기 | 중복: H-02보다 선행 |
| H-02 | 방형 | 5.2×4.8 | 25.0 | 4주식, 노지 | 적색마연토기 2점 | 원삼국 | H-01 상부 중복 |
| ... | ... | ... | ... | ... | ... | ... | ... |

**소계**: 주거지 총 12기 (원형 5기, 방형 7기)

### 2-2. 수혈유구

| 유구번호 | 평면형태 | 규모(m) | 깊이(cm) | 단면형태 | 출토유물 | 기능 추정 | 비고 |
|----------|----------|---------|----------|----------|----------|-----------|------|
| SX-01 | 원형 | 직경 1.2 | 85 | 주머니형 | 무문토기편 5점 | 저장혈 | - |
| SX-05 | 타원형 | 1.5×1.1 | 62 | U자형 | 소토, 목탄 다량 | 폐기장? | 화재 흔적 |
| ... | ... | ... | ... | ... | ... | ... | ... |

**소계**: 수혈유구 총 34기
```

### 3. 유물 종류별 관찰표
출토 유물을 종류별로 분류 및 상세 기술:

```markdown
## 표 3. 유물 관찰표

### 3-1. 토기류

| 유물번호 | 기종 | 부위 | 크기(cm) | 색조 | 태토 | 제작기법 | 출토위치 | 시대 |
|----------|------|------|----------|------|------|----------|----------|------|
| P-001 | 무문토기 | 구연부 | 구경 18.5 | 적갈색 | 사립 다량 | 물손질 | H-01 노지 | 청동기 전기 |
| P-015 | 적색마연토기 | 동체부 | 높이 12.3 | 적색 | 정선 | 마연 | H-02 바닥 | 원삼국 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 3-2. 석기류

| 유물번호 | 기종 | 길이(cm) | 폭(cm) | 두께(cm) | 석재 | 제작기법 | 출토위치 | 비고 |
|----------|------|----------|---------|----------|------|----------|----------|------|
| S-001 | 석촉 | 3.2 | 1.8 | 0.5 | 혈암 | 양면가공 | H-01 내부 | 이등변삼각형 |
| S-012 | 마제석검 | 28.0 | 4.5 | 1.2 | 셰일 | 마제 | H-05 노지 | 검파 명확 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

### 4. 시대·유형별 매핑표
유구와 유물을 시대·유형별로 교차 분류:

```markdown
## 표 4. 시대별 유구·유물 분포

| 시대 | 주거지 | 수혈 | 토기 | 석기 | 금속기 | 기타 | 소계 |
|------|--------|------|------|------|--------|------|------|
| 청동기 전기 | 5기 | 12기 | 26점 (무문토기) | 8점 (석촉, 석도) | - | - | 51 |
| 청동기 후기 | - | 8기 | 5점 (무문토기) | 3점 (석검) | - | - | 16 |
| 원삼국 | 7기 | 14기 | 18점 (적색마연) | 2점 (석도) | 4점 (철기) | - | 45 |
| **합계** | **12기** | **34기** | **49점** | **13점** | **4점** | **0점** | **112** |

## 표 5. 유구 형태별 규모 분포

| 형태 | 수량 | 평균 면적(㎡) | 최소~최대(㎡) | 비고 |
|------|------|---------------|---------------|------|
| 원형 주거지 | 5기 | 16.2 | 12.5~20.1 | 직경 4~5m |
| 방형 주거지 | 7기 | 26.8 | 20.0~35.6 | 한 변 5~8m |
| 원형 수혈 | 28기 | 1.1 | 0.5~2.3 | 직경 0.8~1.7m |
| 타원형 수혈 | 6기 | 1.5 | 0.9~2.8 | 장축 1.2~2.0m |
```

### 5. 참고문헌 목록
고찰 본문에서 인용된 모든 문헌을 정리:

```markdown
## 참고문헌

### 단행본
- 김철수(2020), 『○○지역 청동기시대 주거지 연구』, ○○문화재연구원.
- 이영희(2015), 『한국 선사시대 취락 고고학』, 서울: 주류성출판사.
- ...

### 논문
- 박민수(2019), 「청동기시대 무문토기 편년 재검토」, 『한국고고학보』 110, 45-78.
- 정○○(2017), 「수계 중심 취락 네트워크 연구」, 『고고학』 16(2), 123-156.
- ...

### 발굴조사 보고서
- ○○문화재연구원(2018), 『△△유적 발굴조사 보고서』.
- △△대학교 박물관(2019), 『□□유적』, 학술조사총서 제45집.
- ...

### 기타
- 국가유산청(2015), 『매장문화재 발굴조사 업무 처리지침』.
- 문화재청(2010), 『발굴조사의 방법 및 절차 등에 관한 규정』.

---

**정렬 기준**: 저자명 가나다순 (단행본→논문→보고서→기타 순)
```

**생성 로직**:
```python
import re

def extract_citations(discussion_text):
    """고찰 본문에서 [저자(연도)] 형식 인용 추출"""
    pattern = r'\[([^\]]+)\((\d{4})\)'
    matches = re.findall(pattern, discussion_text)

    citations = {}
    for author, year in matches:
        key = f"{author}({year})"
        if key not in citations:
            citations[key] = {'author': author, 'year': year}

    return citations

def format_references(citations, metadata):
    """인용 목록을 참고문헌 형식으로 변환"""
    references = []
    for key, cite in sorted(citations.items()):
        # metadata에서 전체 서지정보 찾기
        full_ref = find_in_metadata(cite['author'], cite['year'], metadata)
        references.append(full_ref)

    return '\n'.join(references)
```

### 6. 도면·사진 목록
고찰에서 언급된 도면과 사진을 정리:

```markdown
## 부록 1. 도면 목록

| 도면번호 | 제목 | 축척 | 비고 |
|----------|------|------|------|
| 도면 1 | 유적 위치도 | 1:25,000 | 주변 유적 표시 |
| 도면 2 | 유적 지형도 | 1:5,000 | 등고선 표시 |
| 도면 3 | 유구 배치도 | 1:200 | 전체 평면도 |
| 도면 4 | H-01 주거지 평·단면도 | 1:50 | - |
| 도면 5 | H-03 주거지 평·단면도 | 1:50 | 노지 상세 |
| ... | ... | ... | ... |

## 부록 2. 사진 목록

| 사진번호 | 제목 | 촬영시기 | 방향 | 비고 |
|----------|------|----------|------|------|
| 사진 1 | 조사 전 전경 | 2024.03 | 북→남 | 개간 전 |
| 사진 2 | 조사 중 전경 | 2024.07 | 동→서 | 유구 노출 상태 |
| 사진 12 | H-01 노지 세부 | 2024.05 | 상→하 | 소토 확인 |
| ... | ... | ... | ... | ... |
```

### 7. 영문 초록 (Abstract)
국가유산청 규정상 필수 항목:

```markdown
## Abstract

**Archaeological Excavation of the ○○ Site**

The excavation of the ○○ site, conducted by ○○ Cultural Heritage Research
Institute from March to November 2024, revealed significant evidence of Bronze
Age to Proto-Three Kingdoms period settlements in the ○○ region.

**Main Findings**:
- 12 pit-dwellings (5 circular, 7 rectangular)
- 34 pit features (storage pits)
- Artifacts: plain pottery, polished stone daggers, red burnished pottery

**Significance**:
The site demonstrates a transition from circular to rectangular dwellings,
indicating cultural change during the late Bronze Age. The ring-shaped
settlement layout and prestige goods (stone daggers) suggest social
stratification. Comparative analysis with 10 nearby sites reveals extensive
cultural exchange networks along the [River Name] basin.

**Keywords**: Bronze Age, Proto-Three Kingdoms, pit-dwelling, settlement pattern,
[Region Name]
```

## 출력 파일

### output/draft/tables.md
모든 표를 통합한 파일:
```markdown
# 고찰 보강 자료: 비교표 및 일람표

[표 1~5 전체 내용]
```

### output/draft/appendix.md
부록 전체:
```markdown
# 부록

[부록 1: 도면 목록]
[부록 2: 사진 목록]
[부록 3: 유구 상세 데이터 (선택)]
[부록 4: 유물 실측도 목록 (선택)]
```

### output/draft/references.md
참고문헌:
```markdown
# 참고문헌

[단행본, 논문, 보고서, 기타 순으로 정리]
```

### output/draft/abstract_en.md
영문 초록:
```markdown
# Abstract

[200~300단어 영문 요약]
```

## 작성 프로세스

```python
def generate_all_tables():
    """모든 표와 부록 생성"""

    # 1. 주변 유적 비교표
    table1 = generate_comparison_table('output/compare/nearby_ranked.csv')

    # 2. 유구 일람표
    table2 = generate_feature_table(site_data)

    # 3. 유물 관찰표
    table3 = generate_artifact_table(artifact_data)

    # 4. 시대별 분포표
    table4 = generate_period_distribution(site_data, artifact_data)

    # 5. 참고문헌
    discussion = load_md('output/draft/discussion.md')
    citations = extract_citations(discussion)
    references = format_references(citations, metadata)

    # 6. 도면·사진 목록
    drawings = extract_drawing_references(discussion)
    photos = extract_photo_references(discussion)

    # 7. 영문 초록
    abstract = generate_abstract_en(discussion, site_info)

    # 저장
    save_md('output/draft/tables.md', [table1, table2, table3, table4])
    save_md('output/draft/appendix.md', [drawings, photos])
    save_md('output/draft/references.md', references)
    save_md('output/draft/abstract_en.md', abstract)
```

## 품질 검증
- [ ] 표 5개 이상 생성
- [ ] 참고문헌 30개 이상
- [ ] 영문 초록 200~300단어
- [ ] 모든 인용([저자(연도)])에 대응하는 참고문헌 존재
- [ ] 표 형식 일관성 (열 정렬, 단위 표기)

## 완료 후 다음 단계
```
다음 스킬 호출: compliance-audit
전달 데이터:
  - output/draft/discussion.md
  - output/draft/tables.md
  - output/draft/appendix.md
  - output/draft/references.md
  - output/compliance/checklist.md
```

## 실행 명령
```
tables-appendix 스킬을 사용하여 고찰에 필요한 모든 표, 부록,
참고문헌을 생성해주세요.
```

## 추가 기능 (선택)

### 자동 도표 생성 (matplotlib/seaborn)
```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_period_distribution(df):
    """시대별 유구 분포 막대그래프"""
    plt.figure(figsize=(10, 6))
    df.groupby('period')['count'].sum().plot(kind='bar')
    plt.title('시대별 유구 분포')
    plt.xlabel('시대')
    plt.ylabel('유구 수(기)')
    plt.savefig('output/draft/fig_period_distribution.png', dpi=300)

def plot_site_map(sites_df):
    """주변 유적 분포 지도"""
    plt.figure(figsize=(12, 10))
    plt.scatter(sites_df['lon'], sites_df['lat'],
                s=sites_df['similarity_score']*10,
                c=sites_df['period_code'],
                cmap='viridis', alpha=0.6)
    plt.colorbar(label='시대 코드')
    plt.xlabel('경도')
    plt.ylabel('위도')
    plt.title('주변 유사 유적 분포')
    plt.savefig('output/draft/fig_site_map.png', dpi=300)
```

### Excel 출력 (openpyxl)
```python
import pandas as pd

def export_to_excel():
    """모든 표를 Excel 파일로 출력"""
    with pd.ExcelWriter('output/draft/tables.xlsx') as writer:
        table1.to_excel(writer, sheet_name='주변유적비교')
        table2.to_excel(writer, sheet_name='유구일람')
        table3.to_excel(writer, sheet_name='유물관찰')
        table4.to_excel(writer, sheet_name='시대별분포')
```
