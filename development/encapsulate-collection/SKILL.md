---
name: encapsulate-collection
description: 컬렉션 getter가 내부 List/Set을 직접 노출하는 것을 방지 — unmodifiable 반환 + add/remove 메서드 제공. "컬렉션 캡슐화", "getter가 List 그대로 노출", "unmodifiable로", "/encapsulate-collection" 요청 시 사용. 단, 컬렉션과 관련 로직을 전용 클래스로 뽑는 것은 /first-class-collection이 적합. /encapsulate-collection [commit-ref]로 호출.
argument-hint: "[commit-ref]"
---

# Encapsulate Collection

## GOAL

컬렉션을 반환하는 getter가 내부 상태를 직접 노출하는 것을 방지하여:
- 불변성(Immutability) 보장
- 캡슐화 원칙 준수
- 의도하지 않은 외부 수정 방지
- First Class Collection의 첫 단계

## CONSTRAINTS

- **계열**: System-wide — 후보 제시 후 **승인 받고 적용** (`../../references/refactoring-procedure.md` §0·§3-B)
- **동작 변경 금지**: 구조 개선만 수행 (기능 변경 없음)
- **테스트 수정 금지**: 구조 변경이 테스트를 실패시키면 되돌리기
- **사용자 확인 필수**: 자동 적용 금지
- **명시적 git add**: `git add -A` 금지, 변경된 파일만 명시

## 적용 패턴

### Before: 내부 컬렉션 직접 노출
```java
class Course {
    private List<Student> students = new ArrayList<>();
    
    public List<Student> getStudents() {
        return students;  // 위험: 외부에서 수정 가능
    }
}

// 호출부: 캡슐화 위반
course.getStudents().add(student);  // 직접 수정
course.getStudents().clear();       // 위험한 조작
```

### After: Unmodifiable 반환 + 명시적 메서드
```java
class Course {
    private List<Student> students = new ArrayList<>();
    
    public List<Student> getStudents() {
        return Collections.unmodifiableList(students);
    }
    
    public void addStudent(Student student) {
        students.add(student);
    }
    
    public void removeStudent(Student student) {
        students.remove(student);
    }
}

// 호출부: 명시적 메서드 사용
course.addStudent(student);
course.removeStudent(student);
```

### 추가 예시: Set 컬렉션
```java
class Team {
    private Set<Member> members = new HashSet<>();
    
    public Set<Member> getMembers() {
        return Collections.unmodifiableSet(members);
    }
    
    public void addMember(Member member) {
        members.add(member);
    }
    
    public void removeMember(Member member) {
        members.remove(member);
    }
    
    public boolean hasMember(Member member) {
        return members.contains(member);
    }
}
```

### 추가 예시: 복사본 반환 (방어적 복사)
```java
class Order {
    private List<OrderItem> items = new ArrayList<>();
    
    // Option 1: Unmodifiable (읽기 전용)
    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(items);
    }
    
    // Option 2: 방어적 복사 (완전 격리)
    public List<OrderItem> getItemsCopy() {
        return new ArrayList<>(items);
    }
}
```

### 생성자로 받은 컬렉션도 복사한다

getter는 컬렉션이 반환되는 지점이고 생성자는 입력되는 지점이다. 반환 지점만
보호하면 캡슐화가 불완전하다 — 호출자가 넘긴 리스트를 참조로 보관하면 호출자가
나중에 그 리스트를 변경할 수 있고, 리스트의 성질(불변·가변)이 그대로 유입된다.

```java
class Cart {
    private List<CartLine> lines;

    public Cart(List<CartLine> lines) {
        this.lines = lines;                    // 참조를 그대로 보관
    }
}

class Cart {
    private final List<CartLine> lines;

    public Cart(List<CartLine> lines) {
        this.lines = new ArrayList<>(lines);   // 들어올 때 복사
    }
}
```

JPA 사례: `List.of(...)`로 만든 불변 리스트를 그대로 보관한 엔티티를 재저장하면
Hibernate가 병합 과정에서 `clear()`를 호출해 `UnsupportedOperationException`이
발생한다. 생성자 복사로 해결한다.

`private final`은 재할당을 차단하지만 컬렉션 내용 변경은 방지하지 못한다. 생성자
복사(입력 지점) + getter 방어적 복사(반환 지점, 위 예시) 두 지점을 모두 보호해야
캡슐화가 완성된다.

## First Class Collection으로 발전

이 기법 적용 후 `/first-class-collection` 스킬로 전용 클래스 추출 가능:

```java
// Encapsulate Collection 적용 후
class Course {
    private Students students = new Students();  // First Class Collection
    
    public Students getStudents() { return students; }
}

class Students {
    private List<Student> students = new ArrayList<>();
    
    public void add(Student student) { students.add(student); }
    public void remove(Student student) { students.remove(student); }
    public int size() { return students.size(); }
    public boolean contains(Student student) { return students.contains(student); }
}
```

## 적용 기준

### 적용 대상
- `public List<T> getXxx()` 패턴
- 내부 컬렉션을 그대로 반환하는 getter
- 외부에서 `getXxx().add()` 호출하는 코드
- 도메인 객체의 컬렉션 필드
- **생성자·팩토리가 받은 컬렉션을 그대로 필드에 보관하는 코드** (위 "반대 방향" 참조)

### 적용 제외
- **DTO/VO**: 단순 데이터 전송 객체 (불변성 불필요)
- **Builder 패턴**: 빌더 내부 컬렉션 (완성 전까지 가변)
- **읽기 전용 래퍼**: 이미 Unmodifiable 반환 중
- **불변 컬렉션**: `List.of()`, `Set.of()` 사용 중

### 주의사항
- 호출부에서 `getXxx().add()` 패턴 모두 변경 필요
- 테스트 코드도 영향받음 (명시적 메서드 사용으로 전환)
- Unmodifiable vs 방어적 복사 선택:
  - **읽기 전용**: `Collections.unmodifiableList()` (성능 우수)
  - **완전 격리**: `new ArrayList<>(...)` (안전성 우수)

## OUTPUT FORMAT

### 실행 절차

공통 골격(대상 파일 수집 → 후보 제시(계열별 승인 규칙) → 적용 → 테스트 → 커밋/되돌리기, 브랜치·PR이
필요한 조건)은 이 스킬 디렉터리 기준 `../../references/refactoring-procedure.md`가 정본이다.
아래는 이 기법에 고유한 부분만 규정한다.

#### 후보 식별 (공통 절차 2단계)

- 컬렉션 타입 getter 탐지 (`List<T>`, `Set<T>`, `Map<K,V>`)
- 내부 필드를 직접 반환하는지 확인
- 호출부에서 `getXxx().add()` 패턴 검색
- 각 후보에 대해:
  - 파일명 및 라인 번호
  - Before/After 코드 미리보기
  - 영향받는 호출부 수

#### 후보 제시 예시 (공통 절차 3단계)

```
발견된 후보 2개:

1. Course.java:15
   getter: public List<Student> getStudents()
   → Collections.unmodifiableList() 반환
   → addStudent(), removeStudent() 메서드 추가
   영향받는 호출부: 5곳 (course.getStudents().add() 패턴)

2. Team.java:20
   getter: public Set<Member> getMembers()
   → Collections.unmodifiableSet() 반환
   → addMember(), removeMember() 메서드 추가
   영향받는 호출부: 3곳

적용하시겠습니까? (yes / no / 수정)
Unmodifiable vs 방어적 복사 선택: (unmodifiable / copy)
```

#### 리팩토링 적용 (공통 절차 4단계)

- getter를 Unmodifiable 또는 방어적 복사로 변경
- `add()`, `remove()` 메서드 추가
- 모든 호출부 업데이트:
  - `getXxx().add(item)` → `addXxx(item)`
  - `getXxx().remove(item)` → `removeXxx(item)`
- (선택) 추가 메서드 (`contains()`, `size()`, `isEmpty()`)

커밋 메시지: `refactor: encapsulate collection in <클래스명>` (공통 절차 6단계)

### 출력 예시
```
완료: Encapsulate Collection

변경 내용:
- Course.java:15
  getStudents() → Collections.unmodifiableList() 반환
  + addStudent(Student)
  + removeStudent(Student)
  
- Team.java:20
  getMembers() → Collections.unmodifiableSet() 반환
  + addMember(Member)
  + removeMember(Member)

영향받는 호출부: 8곳 자동 업데이트

테스트: 모든 테스트 통과 (23 tests)
커밋: refactor: encapsulate collection in Course, Team

제안: Course.students는 First Class Collection으로 추출 가능합니다.
   /first-class-collection 스킬을 고려해보세요.
```

## FAILURE CONDITIONS

공통 실패 조건(계열별 승인 규칙 위반, 테스트 실패 방치, 테스트 수정, 커밋 단위, `git add -A`, heredoc
한글 메시지)은 `../../references/refactoring-procedure.md`에 있다. 아래는 이 기법에 고유한 것만.

- [ ] DTO/VO 클래스에 불필요하게 적용함
- [ ] 호출부 업데이트 누락 (`getXxx().add()` 패턴이 남음)
- [ ] Unmodifiable 반환 후에도 외부에서 수정 가능한 상태
