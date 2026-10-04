---
name: gen-dto
description: >
  common-rule.md 컨벤션에 맞는 Request/Response DTO 클래스를 생성하는 스킬.
  "/gen-dto"를 입력하거나, "DTO 만들어줘" 같은 요청에 트리거된다.
  대상 도메인과 필요한 내부 클래스를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen DTO

Request/Response DTO 클래스를 생성하는 스킬이다.

## 언제 사용하는가

- 새 도메인의 DTO가 필요할 때
- "DTO 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 도메인** — 어떤 도메인인지 (예: `Board`)
2. **Request 내부 클래스** — 필요한 기능별 클래스 (예: `Save`, `Update`, `Login`)
3. **Response 내부 클래스** — 필요한 데이터 범위별 클래스 (예: `Max`, `Min`, `Detail`)
4. **각 클래스의 필드** — 포함할 필드 목록

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 DTO 규칙을 따른다:

### 파일 구조

- 도메인당 파일 하나씩: `{Domain}Request.java`, `{Domain}Response.java`
- 외부 클래스에는 어노테이션 없음
- `@Data`는 내부 static class에만

### Request 네이밍

내부 클래스 이름은 **기능명**으로:
- `Save` — 등록
- `Update` — 수정
- `Login` — 로그인
- `Join` — 회원가입

### Response 네이밍

내부 클래스 이름은 **데이터 범위 기준**으로:
- `Max` — 테이블 전체 컬럼 (상세/목록 겸용)
- `Min` — 최소 정보 (id + 대표값)
- `Detail` — 조인 포함 확장 정보
- `Option` — 셀렉트박스/드롭다운용
- `DTO` — 범용 (위 분류에 해당하지 않을 때)

### Entity → DTO 변환

생성자 또는 정적 팩토리 메서드로 처리한다.

### Request 예시

```java
package com.example.ajax_demo.board;

public class BoardRequest {

    @Data
    public static class SaveOrUpdateDTO {
        private String title;
        private String content;
    }
}
```

### Response 예시

```java
package com.example.ajax_demo.board;

import lombok.Data;

public class BoardResponse {

    @Data
    public static class DTO {
        private Integer id;
        private String title;

        public DTO(Board board) {
            this.id = board.getId();
            this.title = board.getTitle();
        }
    }

    @Data
    public static class DetailDTO {
        private Integer id;
        private String title;
        private String content;
        private String username;
        private boolean isOwner;

        public DetailDTO(Board board, User sessionUser) {
            this.id = board.getId();
            this.title = board.getTitle();
            this.content = board.getContent();
            this.username = board.getUser().getUsername();
            this.isOwner = sessionUser != null
                    && board.getUser().getId().equals(sessionUser.getId());
        }
    }
}
```

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}Request.java
src/main/java/com/example/ajax_demo/{domain}/{Domain}Response.java
```

## 주의사항

- Entity가 먼저 존재해야 한다. 없으면 사용자에게 알린다
- 외부 클래스에 `@Data` 붙이지 않는다
- Entity를 Controller에 직접 전달하지 않기 위해 DTO 변환은 필수다
