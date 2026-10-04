---
name: docx-to-hlz
description: >-
  한국 특허 명세서 워드(.docx)를 특허청 전자출원 편집기(통합명세서작성기 NKEditor /
  신형 "지식재산처 전자문서 작성 S/W")가 여는 .hlz 파일로 변환한다. .hlz는 표준 ZIP =
  KIPO application-body XML(1개) + patNNNNN 도면 이미지. 워드의 【식별항목】 섹션
  (【발명의 명칭】【기술분야】【배경기술】【해결하고자 하는 과제】【과제의 해결 수단】【발명의 효과】
  【도면의 간단한 설명】【발명을 실시하기 위한 구체적인 내용】【청구범위】【요약】【대표도】【도면】)을
  KIPO XML 요소로 매핑하고, 청구항은 <claim-text> + <br/>로, 도면 이미지는 표시크기(EMU→mm)와
  함께 <drawings>로 패키징. 편집기 호환을 위한 하드 규칙을 자동 적용 — (1) ZIP 엔트리 파일명을
  CP949 인코딩 + UTF-8 플래그(0x800) 제거(안 하면 편집기가 압축해제 실패 "…SGM 찾을 수 없습니다"),
  (2) img-format을 DTD 허용값 jpg|tif로 정규화(tiff→tif, png/bmp/gif→jpg 재인코딩),
  (3) 청구항 태그의 작성자 메모 //…// 제거, (4) <p num> description 전관통 4자리 일련번호·abstract만
  별도 접미사 a, (5) 대표도 <abstract-figure><figref num>. .HLT(HAN Lite 독자 바이너리)는 외부
  생성 불가이므로 만들지 않는다 — .hlz를 편집기에서 열고 저장하면 편집기가 .HLT를 만든다.
  "docx를 hlz로", "명세서 hlz 변환", "워드를 통합명세서작성기 형식으로", "hlz 만들어",
  "특허청 편집기 파일로 변환", "명세서를 전자출원 편집기에 넣게", "docx2hlz" 같은 표현이 보이거나,
  완성된 한국 특허 명세서 워드파일을 KIPO 편집기로 불러올 형태로 만들려는 맥락에서 사용.
  (도면만 정리=도면정리, 청구항 트리=claim-tree-chart 스킬은 별개.)
---

# docx-to-hlz — 워드 명세서 → 특허청 편집기(.hlz) 변환

완성된 한국 특허 명세서 `.docx`를 특허청 전자출원 편집기가 여는 **`.hlz`**(ZIP: KIPO XML + 도면)로 변환한다.

## 사용법

```bash
python "<skill>/scripts/docx2hlz.py" "명세서.docx"          # → 같은 폴더에 명세서.hlz
python "<skill>/scripts/docx2hlz.py" "명세서.docx" -o out.hlz
```

의존성: `python-docx`, `Pillow`(png/tiff 재인코딩·크기추정용).

변환 후 사용자가 편집기에서 **[파일 > 열기]로 .hlz 선택**(또는 창에 드래그&드롭). 편집기 GUI 클릭은
자동화 불가이므로 여는 것은 사용자가 한다.

## 입력 워드 전제

- KIPO 별지 서식 **【식별항목】 태그**로 섹션이 구분돼 있어야 한다(위 description의 12개 태그).
- 래퍼 태그(【발명의 설명】【발명의 내용】【요약서】)는 자식만 쓰고 자신은 버린다.
- 비표준 소제목(예 【1. 용어의 정의…】 탐색창용 챕터)은 본문 문단으로 흡수(대괄호 제거).
- 표(table)는 미지원(현재 대상 명세서에 표가 없어 미구현) — 표 있는 건은 확장 필요.

## 산출 포맷 핵심 (application-body DTD)

```
<KIPO keapsVersion="5.6" editorKind="K" pageCount wi imgApply="N" xmlns="http://www.kipo.go.kr">
 <PatentCAFDOC docflag="1.0" documentID="숫자">
  <description>
   <invention-title>한글{ENGLISH}</invention-title>
   <technical-field><p num="0001">…</p></technical-field>
   <background-art>…</background-art>
   <summary-of-invention><tech-problem/><tech-solution/><advantageous-effects/></summary-of-invention>
   <description-of-drawings><p>도 1은…<br/>도 2는…</p></description-of-drawings>
   <description-of-embodiments><p num=…>…</p></description-of-embodiments>
  </description>
  <claims><claim num="1"><claim-text>…단계;<br/>…을 특징으로 하는 ….</claim-text></claim></claims>
  <abstract><summary><p num="0001a"/></summary><abstract-figure><figref num="3"/></abstract-figure></abstract>
  <drawings><figure num="1"><img id he wi file="pat00001.tif" img-format="tif"/></figure></drawings>
 </PatentCAFDOC>
</KIPO>
```

## 편집기 호환 하드 규칙 (스크립트가 자동 적용 — 하나라도 어기면 로딩 실패)

1. **ZIP 파일명 = CP949 + UTF-8 플래그(0x800) 제거.** ★가장 잘 틀리는 부분★
   Python 기본은 한글 파일명에 UTF-8 플래그를 세팅 → 구 MFC 편집기가 엔트리를 못 찾아
   **압축해제 자체가 실패**(temp 폴더 빔) → "…**SGM** 을(를) 찾을 수 없습니다" 에러.
   `ZipInfo._encodeFilenameFlags` 오버라이드로 해결. 레퍼런스 hlz는 전 엔트리 flag=0x0000.
2. **내부 XML basename == .hlz 파일 basename** (편집기가 이름으로 문서파일 탐색).
3. **img-format ∈ {jpg, tif}** (DTD: jpg|tif|st33|st35). tiff→tif(3글자), png/bmp/gif→jpg 재인코딩(투명→흰색).
4. **청구항은 `<claim-text>` 한 덩어리 + `<br/>`.** 【청구항 N】 뒤 작성자 메모 `//…//`는 제거.
5. **`<p num>`** = description 전관통 4자리 일련번호. abstract만 별도 카운터 + 접미사 `a`.
6. **대표도** = `<abstract-figure><figref num>`. **도면** = `<drawings><figure num><img he wi file img-format>`, he/wi=mm(EMU/36000, 최대 165×222mm·E-218).
7. XML 특수문자 이스케이프, UTF-8. ZIP은 XML 먼저.

## .HLT 를 원하면

`.HLT`는 `HAN Lite` **독자 바이너리**라 외부 생성 불가. 파이프라인:
```
docx ──[이 스킬]──▶ .hlz ──[통합명세서작성기(NKEditor) 열기 → 다른이름 저장 → .HLT]──▶ .HLT
```
※ 신형 "지식재산처 전자문서 작성 S/W"에서 저장하면 네이티브가 `.hwpx`. `.HLT`가 목적이면
구형 **통합명세서작성기(`C:\KipoNet\NKEditor\NKEditor.exe`)**로 열어 저장.

## 검증 루틴 (변환 후 권장)

- ZIP 무결성 + 전 엔트리 `flag_bits & 0x800 == 0`.
- XML well-formed, `img-format` 화이트리스트, `file=` 참조 ↔ 실제 patNNNNN 일치, 이미지 PIL 무결성.
- 청구범위 내 `//` 잔존 0, 청구항/도면 개수, 대표도 figref.
- 편집기 생성 레퍼런스(`C:\KipoNet\NKEditor\Data\Hlz\*.hlz`)와 요소 스켈레톤 대조.
- DTD 원본: `C:\KipoNet\NKEditor\Epasl\INCLUDE\DTD\application-body-v1-6.dtd`.

상세 리버스 엔지니어링 기록: `reference/hlz_format_notes.md`.

## 누적 학습 항목

- (2026-07-02) 최초 작성. 실증 건 A(청구항 15·도면 16, png 5장 jpg 재인코딩). 실패→해결한 결정타는 **ZIP UTF-8 파일명 플래그**였음("SGM 못 찾음" 에러의 진짜 원인).
- (2026-07-02) **도면 이미지 최대 165×222mm (검증기 E-218)** — 세로 245로 잡으면 세로 긴 도면이 230으로
  걸림. `PAGE_MAX_H_MM=222` + 반올림 초과 방지 최종 클램프. 실제 출원건도 he 최대 ~221.
- (2026-07-02) **이해편의용 소목차 `【N. …】` 는 본문에서 제거**(`CHAPTER_HEAD_RE`). 도면은 `<figure>`당
  편집기 자동 1페이지 — 수동 페이지나눔 마크업 없음, 작으면 뭉치므로 fill로 키움.
- (2026-07-08) **fill(contain)만으로는 1도면=1페이지 보장 안 됨** — 가로로 긴 도면은 폭 165만 채우고
  세로가 작아(예 71mm) 2장이 한 페이지에 뭉침(71+148=219 ≤ 222). Ctrl+Enter에 해당하는 페이지나눔
  마크업이 스키마에 없으므로 **`pad_drawing_to_page()`: 표시 he < 222인 도면은 이미지 캔버스를
  흰색으로 세로 패딩(내용 수직 중앙, 종횡비 무손상)해 he=222로 강제** → 물리적으로 한 도면 한 페이지.
  tif는 mode "1"이면 Group4 유지 재저장. 실증 건 B(도면 9장 전부 222 통일).
- (2026-07-21) **★위 he=222 패딩 정책 철회 — 기본 OFF(`PAD_TO_PAGE=False`, `--pad-page`로만 켬).**
  이유 둘. ① **【도면】 머리글과 【도 1】은 같은 페이지에 있어야 한다**(사용자 확정 규칙). he=222면
  도1이 머리글에 밀려 다음 페이지로 넘어간다. ② 패딩이 도면마다 상하 20%대 흰 여백을 만들어
  "여백이 너무 많다"는 지적을 받음(실증 건 C). 여러 도면이 한 페이지에 뭉치는 것은 감수한다
  (KIPO는 한 면에 복수 도면 배치를 허용).
- (2026-07-21) **기성 .hlz의 도면 여백만 사후 교정하는 절차** — ZIP 재패킹 시 두 가지가 잘 깨진다.
  ① `zipfile.ZipFile(SRC,'w')`를 원본 읽는 중에 열면 원본이 잘리므로 **먼저 .bak 복사 후 .bak에서 읽기**.
  ② `ZipInfo`를 그대로 재사용해도 파이썬이 비ASCII 파일명에 UTF-8 플래그를 **다시** 세팅한다
  (`flag_bits & ~0x800`만으로는 부족) → `_encodeFilenameFlags` 오버라이드한 CP949 ZipInfo 필수.
  이미지는 `g<200` 마스크 bbox로 크롭 + 내용 최대변의 2% 패딩, `<img he/wi>`는 크롭 종횡비로 재계산.
