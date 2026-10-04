---
name: gen-entity
description: >
  common-rule.md 컨벤션에 맞는 JPA Entity 클래스를 생성하는 스킬.
  "/gen-entity"를 입력하거나, "엔티티 만들어줘", "테이블 만들어줘" 같은 요청에 트리거된다.
  도메인명과 필드 정보를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Entity

common-rule.md 컨벤션을 준수하는 JPA Entity 클래스를 생성하는 스킬이다.

## 언제 사용하는가

- 새 도메인의 Entity 클래스가 필요할 때
- "엔티티 만들어줘", "테이블 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **도메인명** — 예: `Board`, `User`, `Reply`
2. **필드 목록** — 각 필드의 이름, 타입, 제약조건 (nullable, unique, length 등)
3. **연관관계** — 다른 Entity와의 관계 (ManyToOne, OneToMany 등)

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

반드시 `_docs/.ai/rules/common-rule.md`의 Entity 규칙을 따른다:

### 어노테이션 순서

```java
@NoArgsConstructor
@Data
@Entity
@Table(name = "{도메인}_tb")
public class {Domain} {
```

### PK

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Integer id;
```

- PK 타입은 반드시 `Integer` — `Long` 사용 금지
- 전략은 `GenerationType.IDENTITY`

### @Builder

- 클래스 레벨 `@Builder` 금지 — 생성자에만 선언
- 컬렉션 필드(`List`, `Set`)는 `@Builder` 생성자에 포함하지 않는다

```java
@Builder
public {Domain}(Integer id, String title, String content, User user) {
    this.id = id;
    this.title = title;
    this.content = content;
    this.user = user;
}
```

### 연관관계

- 모든 연관관계: `FetchType.LAZY` — EAGER 금지
- `@ManyToOne(fetch = FetchType.LAZY)`
- `@OneToMany(mappedBy = "...", fetch = FetchType.LAZY)`

### 생성일

```java
@CreationTimestamp
private LocalDateTime createdAt;
```

### 테이블명

- `@Table(name = "{domain}_tb")` — snake_case + `_tb` 접미사

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}.java
```

도메인 패키지가 없으면 함께 생성한다.

## 출력 예시

```java
package com.example.ajax_demo.board;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;
import java.util.List;

@NoArgsConstructor
@Data
@Entity
@Table(name = "board_tb")
public class Board {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String content;

    @ManyToOne(fetch = FetchType.LAZY)
    private User user;

    @OneToMany(mappedBy = "board", fetch = FetchType.LAZY)
    private List<Reply> replies;

    @CreationTimestamp
    private LocalDateTime createdAt;

    @Builder
    public Board(Integer id, String title, String content, User user) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.user = user;
    }
}
```

## 주의사항

- 기존에 같은 이름의 Entity가 있으면 덮어쓰지 않고 사용자에게 알린다
- data.sql에 초기 데이터가 필요한지 확인한다
