---
name: similarity-matcher
description: 조사지역 주변 유사 유적 매칭 및 비교 분석
tags: [archaeology, similarity, geospatial, comparison, pipeline-step-2]
---

# Similarity Matcher - 주변 유사 유적 매칭

## 목적
대상 발굴조사 지역을 중심으로 공간적·시대적·유형적으로 유사한 주변 유적과 사례를 식별하고 랭킹하여 고찰 작성의 비교 자료로 제공합니다.

## 입력
- `output/normalized/metadata.csv`: data-normalizer가 생성한 메타데이터
- `output/normalized/documents.jsonl`: 전체 문서 내용
- **사용자 파라미터**:
  - 조사명: (예) "○○지구 도시개발사업 부지 내 유적"
  - 대상지역 중심좌표: (위도, 경도)
  - 비교 반경: (km 단위, 기본값 20km)
  - 주요 시대: (예) ["청동기시대", "원삼국시대"]
  - 주요 유구/유물 유형: (예) ["주거지", "수혈유구", "무문토기"]

## 처리 프로세스

### 1단계: 대상 조사 정보 설정
사용자로부터 입력받거나 파일에서 추출:
```python
target_site = {
    "name": "○○지구 도시개발사업 부지 내 유적",
    "coordinates": (37.5665, 126.9780),  # 위도, 경도
    "radius_km": 20,
    "periods": ["청동기시대", "원삼국시대"],
    "types": ["주거지", "수혈유구", "무문토기", "석기"]
}
```

### 2단계: 공간 유사도 계산
Haversine 공식을 사용하여 각 문서의 좌표와 대상지 간 거리 계산:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """두 지점 간 거리(km) 계산"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# 거리 기반 점수 (0~1, 가까울수록 높음)
def distance_score(distance_km, radius_km):
    if distance_km > radius_km:
        return 0.0
    return 1.0 - (distance_km / radius_km)
```

### 3단계: 시대 유사도 계산
```python
def period_similarity(target_periods, doc_periods):
    """시대 일치도 계산 (Jaccard 유사도)"""
    if not target_periods or not doc_periods:
        return 0.0
    target_set = set(target_periods)
    doc_set = set(doc_periods)
    intersection = target_set & doc_set
    union = target_set | doc_set
    return len(intersection) / len(union) if union else 0.0
```

### 4단계: 유구/유물 유형 유사도 계산
```python
def type_similarity(target_types, doc_types):
    """유구/유물 유형 유사도 (코사인 유사도 또는 Jaccard)"""
    if not target_types or not doc_types:
        return 0.0
    target_set = set(target_types)
    doc_set = set(doc_types)
    intersection = target_set & doc_set
    return len(intersection) / max(len(target_set), len(doc_set))
```

### 5단계: 종합 유사도 점수 계산
가중치를 적용하여 최종 점수 산출:
```python
def calculate_similarity(target, doc):
    """종합 유사도 점수 (0~100)"""
    # 가중치 설정
    w_distance = 0.4  # 공간 거리
    w_period = 0.3    # 시대 일치
    w_type = 0.3      # 유형 일치

    distance_km = haversine(
        target['coordinates'][1], target['coordinates'][0],
        doc['lon'], doc['lat']
    )

    score = (
        w_distance * distance_score(distance_km, target['radius_km']) +
        w_period * period_similarity(target['periods'], doc['periods']) +
        w_type * type_similarity(target['types'], doc['types'])
    ) * 100

    return {
        'score': score,
        'distance_km': round(distance_km, 2),
        'period_match': period_similarity(target['periods'], doc['periods']),
        'type_match': type_similarity(target['types'], doc['types'])
    }
```

### 6단계: 상위 유사 유적 선정 및 요약
- 유사도 점수 기준 상위 N개 선정 (기본값 20개)
- 각 유적에 대해 500~700자 표준 요약 생성:
  - 조사명, 위치, 시대
  - 주요 유구/유물
  - 특징적인 발견사항
  - 조사연도 및 기관

```python
def generate_summary(doc_id, documents_jsonl):
    """문서 ID로부터 표준 요약 생성"""
    doc = load_document(doc_id, documents_jsonl)

    summary = f"""
**{doc['title']}**

- **위치**: {doc['location']} (대상지로부터 {doc['distance_km']}km)
- **시대**: {', '.join(doc['period'])}
- **조사연도**: {doc['year']}
- **조사기관**: {doc['author']}

**주요 내용**:
{doc['abstract'][:300]}...

**주요 유구**: {', '.join(doc['types'][:5])}

**비교 핵심 포인트**:
1. [유구 배치 패턴의 유사성]
2. [출토 유물의 형태적 특징 비교]
3. [연대 추정 근거의 동질성]
4. [취락 구조의 공통점과 차이점]
5. [문화적 교류 가능성]

**출처**: [{doc['author']}({doc['year']})]
    """.strip()

    return summary
```

### 7단계: 비교 핵심 포인트 자동 추출
각 유사 유적에 대해 5개의 비교 핵심 포인트를 자동 생성:
- 유구 배치 및 공간 구조
- 유물 형태 및 제작 기술
- 연대 및 층위 관계
- 취락/유적 성격
- 주변 지역과의 관계

## 출력

### output/compare/nearby_ranked.csv
```csv
rank,doc_id,title,location,distance_km,period,types,similarity_score,distance_score,period_match,type_match
1,doc_015,△△유적 발굴조사보고서,○○시 ××동,5.2,"청동기시대","주거지;수혈;무문토기",85.6,0.74,1.0,0.83
2,doc_027,□□지구 문화재 발굴조사,○○시 ◇◇동,12.8,"청동기시대;원삼국",주거지;석기,78.3,0.36,0.67,0.75
...
```

### output/compare/nearby_summaries.jsonl
```json
{
  "rank": 1,
  "doc_id": "doc_015",
  "title": "△△유적 발굴조사보고서",
  "similarity_score": 85.6,
  "summary": "**△△유적 발굴조사보고서**\n\n- **위치**: ...",
  "comparison_points": [
    "유구 배치 패턴: 대상지와 유사한 방형 배치",
    "출토 유물: 무문토기 구연부 형태의 높은 일치도",
    "연대: C14 측정 결과 대상지와 동일 시기 (B.C. 800~600)",
    "취락 구조: 중심 광장을 둘러싼 환상 배치",
    "교류 증거: 동일 석재 사용으로 원료 공급망 공유 추정"
  ],
  "reference": "○○문화재연구원(2018)"
}
```

### output/compare/similarity_matrix.txt (추가)
모든 문서 간 유사도 행렬 (선택적):
```
         doc_001  doc_015  doc_027  ...
doc_001   100.0     45.2     32.1
doc_015    45.2    100.0     68.5
doc_027    32.1     68.5    100.0
...
```

### output/compare/map_visualization.html (선택적)
대상지와 주변 유적을 지도에 시각화:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>주변 유사 유적 분포도</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="width: 100%; height: 800px;"></div>
    <script>
        var map = L.map('map').setView([37.5665, 126.9780], 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // 대상지 마커
        L.marker([37.5665, 126.9780]).addTo(map)
            .bindPopup('<b>대상 조사지</b>');

        // 유사 유적 마커들
        var sites = [
            {lat: 37.5800, lon: 127.0000, name: "△△유적", score: 85.6},
            // ...
        ];

        sites.forEach(function(site) {
            var color = site.score > 70 ? 'red' : (site.score > 50 ? 'orange' : 'blue');
            L.circleMarker([site.lat, site.lon], {color: color, radius: 8})
                .addTo(map)
                .bindPopup(`<b>${site.name}</b><br>유사도: ${site.score}`);
        });

        // 반경 표시
        L.circle([37.5665, 126.9780], {radius: 20000, color: 'blue', fillOpacity: 0.1}).addTo(map);
    </script>
</body>
</html>
```

## 품질 검증
- [ ] 상위 10개 유적이 실제로 공간·시대·유형 면에서 유사한가?
- [ ] 거리 0km 유적이 없는가? (대상지 자신을 제외했는가?)
- [ ] 좌표 없는 문서는 지명 기반 추정 또는 제외 처리했는가?
- [ ] 요약문이 모두 500~700자 범위인가?

## 오류 처리
- 좌표 없는 문서: 지명으로 지오코딩 시도, 실패 시 제외
- 반경 내 유적 0개: 반경 자동 확대 (20km → 50km → 100km)
- 시대/유형 정보 없음: 텍스트 본문에서 키워드 재추출

## 완료 후 다음 단계
```
다음 스킬 호출: regulation-checker
전달 데이터: output/compare/nearby_ranked.csv, output/compare/nearby_summaries.jsonl
```

## 실행 명령
Claude에게 다음과 같이 요청하세요:
```
similarity-matcher 스킬을 사용하여 대상지역 주변 20km 이내의
유사한 유적을 찾아 비교 분석해주세요.

대상지 정보:
- 조사명: ○○지구 유적
- 좌표: 위도 37.5665, 경도 126.9780
- 시대: 청동기시대, 원삼국시대
- 유형: 주거지, 수혈유구, 무문토기
```

## 고급 옵션
- 가중치 조정: `w_distance`, `w_period`, `w_type` 비율 변경
- 다차원 척도법(MDS): 유적 간 관계를 2D 평면에 시각화
- 클러스터링: 유사 유적을 군집으로 그룹화 (K-means, DBSCAN)
