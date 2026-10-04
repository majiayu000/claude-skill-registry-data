---
name: gen-repository
description: >
  Entity 기반으로 JPA Repository 클래스를 생성하는 스킬.
  "/gen-repository"를 입력하거나, "레포지토리 만들어줘" 같은 요청에 트리거된다.
  대상 Entity와 필요한 쿼리 메서드를 인터뷰로 수집한 뒤 바로 코드를 생성한다.
---

# Gen Repository

Entity 기반으로 Repository 클래스를 생성하는 스킬이다.

## 언제 사용하는가

- 새 도메인의 Repository가 필요할 때
- "레포지토리 만들어줘" 요청 시

## 인터뷰 항목

다음 정보를 질문으로 수집한다. 한 번에 하나씩 묻는다.

1. **대상 도메인** — 어떤 Entity의 Repository인지 (예: `Board`)
2. **구현 방식** — Spring Data JPA 인터페이스 vs EntityManager 수동 구현
3. **커스텀 쿼리 메서드** — 필요한 조회 메서드 (예: `findByUserId`, 조인 페치 등)

사용자가 이미 충분한 정보를 제공했다면 추가 질문 없이 바로 생성한다.

## 생성 규칙

### Spring Data JPA 방식

```java
package com.example.ajax_demo.{domain};

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface {Domain}Repository extends JpaRepository<{Domain}, Integer> {

    // 커스텀 메서드 예시
    @Query("SELECT b FROM Board b JOIN FETCH b.user WHERE b.id = :id")
    {Domain} findByIdJoinUser(@Param("id") int id);
}
```

### EntityManager 수동 구현 방식

```java
package com.example.ajax_demo.{domain};

import jakarta.persistence.EntityManager;
import jakarta.persistence.Query;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.List;

@RequiredArgsConstructor
@Repository
public class {Domain}Repository {

    private final EntityManager em;

    public {Domain} findById(int id) {
        return em.find({Domain}.class, id);
    }

    public List<{Domain}> findAll() {
        return em.createQuery("SELECT e FROM {Domain} e ORDER BY e.id DESC", {Domain}.class)
                .getResultList();
    }

    public void save({Domain} entity) {
        em.persist(entity);
    }

    public void delete({Domain} entity) {
        em.remove(entity);
    }
}
```

## 생성 위치

```
src/main/java/com/example/ajax_demo/{domain}/{Domain}Repository.java
```

## 주의사항

- 기존 프로젝트의 Repository 구현 방식(Spring Data JPA vs EntityManager)을 확인하고 일관성을 유지한다
- PK 타입은 반드시 `Integer` — `Long` 사용 금지
- 조인 페치가 필요한 경우 JPQL로 명시적으로 작성한다
