---
name: gen-service
description: >
  common-rule.md 컨벤션에 맞는 Service 클래스를 생성하는 스킬.
  "/gen-service"를 입력하거나, "서비스 만들어줘" 같은 요청에 트리거된다.
  대상 도메인과 필요한 비즈니스 메서드를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Service

common-rule.md 컨벤션을 준수하는 Service 클래스를 생성하는 스킬이다.

## 언제 사용하는가

- 새 도메인의 Service가 필요할 때
- "서비스 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 도메인** — 어떤 도메인의 Service인지 (예: `Board`)
2. **비즈니스 메서드 목록** — 필요한 기능 (예: 목록 조회, 상세 조회, 등록, 수정, 삭제)
3. **세션 의존 여부** — 로그인 사용자 정보가 필요한 메서드가 있는지

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 Service 규칙을 따른다:

### 어노테이션 순서

```java
@Transactional(readOnly = true)
@RequiredArgsConstructor
@Service
public class {Domain}Service {
```

### 트랜잭션

- 클래스 레벨: `@Transactional(readOnly = true)` 항상 선언
- 쓰기 메서드(`save`, `update`, `delete`)에는 `@Transactional` 개별 선언

### DTO 반환

- Service에서 DTO를 생성하여 반환 — 날(raw) Entity를 Controller로 전달 금지

## 출력 예시

```java
package com.example.ajax_demo.board;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Transactional(readOnly = true)
@RequiredArgsConstructor
@Service
public class BoardService {

    private final BoardRepository boardRepository;

    public List<BoardResponse.DTO> 게시글목록() {
        List<Board> boards = boardRepository.findAll();
        return boards.stream()
                .map(BoardResponse.DTO::new)
                .toList();
    }

    public BoardResponse.DetailDTO 상세보기(int id) {
        Board board = boardRepository.findById(id);
        return new BoardResponse.DetailDTO(board);
    }

    @Transactional
    public void 게시글쓰기(BoardRequest.SaveOrUpdateDTO reqDTO, User sessionUser) {
        Board board = Board.builder()
                .title(reqDTO.getTitle())
                .content(reqDTO.getContent())
                .user(sessionUser)
                .build();
        boardRepository.save(board);
    }

    @Transactional
    public void 게시글수정(int id, BoardRequest.SaveOrUpdateDTO reqDTO) {
        Board board = boardRepository.findById(id);
        board.setTitle(reqDTO.getTitle());
        board.setContent(reqDTO.getContent());
    }

    @Transactional
    public void 게시글삭제(int id) {
        Board board = boardRepository.findById(id);
        boardRepository.delete(board);
    }
}
```

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}Service.java
```

## 주의사항

- 메서드명은 한국어도 허용한다 (프로젝트 기존 패턴 따름)
- Repository와 DTO가 먼저 존재해야 한다. 없으면 사용자에게 알린다
- Entity를 Controller에 절대 전달하지 않는다
