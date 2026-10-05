---
name: code-translation
description: Translate code between programming languages while preserving logic, idiomatic style, and test coverage. Use when porting code between languages, migrating.
---

# Code Translation

Systematic translation of code between programming languages while preserving correctness, adapting to idiomatic conventions of the target language, mapping library equivalents, handling type system differences, and verifying the translation through testing. This skill covers both small snippet translations and large-scale project migrations.

## When to Use This Skill

Use this skill for:

- Porting a module or library from one language to another
- Converting code examples from documentation written in a different language
- Migrating a project from one technology stack to another (e.g., Java to Kotlin, Python 2 to Python 3, JavaScript to TypeScript)
- Adapting an algorithm implementation from a reference language to your project's language
- Translating test cases alongside production code
- Creating polyglot implementations that must behave identically across languages

**Trigger phrases**: "translate this code", "port to Python", "convert to JavaScript", "rewrite in Java", "translate from", "code migration", "language conversion", "port this function", "equivalent in", "same thing in Python"

## What This Skill Does

This skill provides a structured translation methodology:

- **Language Mapping**: Maps constructs, keywords, and idioms from the source language to their equivalents in the target language
- **Library Equivalents**: Identifies equivalent libraries and frameworks in the target language ecosystem
- **Type System Adaptation**: Handles differences in type systems (static vs. dynamic, nullable vs. non-nullable, generics, type inference)
- **Idiom Translation**: Converts source-language idioms to target-language idioms rather than producing literal (non-idiomatic) translations
- **Error Handling Translation**: Maps exception handling, error return patterns, and result types between languages
- **Testing the Translation**: Verifies that the translated code produces identical outputs for the same inputs

## Instructions

### Step 1: Analyze the Source Code

Before translating, understand the source code fully.

#### Analysis Checklist

1. **Identify all language-specific constructs**: list comprehensions, pattern matching, operator overloading, extension methods, macros, decorators, annotations
2. **Catalog external dependencies**: libraries, frameworks, system APIs used by the source code
3. **Map data structures**: identify which data structures are used and their properties (ordered, mutable, nullable)
4. **Understand error handling**: exceptions, error codes, Result/Option types, panic/recover
5. **Note concurrency patterns**: threads, async/await, goroutines, actors, coroutines
6. **Check for language-specific behavior**: integer overflow, floating-point precision, string encoding, null semantics

### Step 2: Map Language Constructs

Use the following reference tables to map constructs between common language pairs.

#### Core Construct Mapping

| Concept | Python | JavaScript | Java | Go | Rust |
|---------|--------|------------|------|-----|------|
| **Variable declaration** | `x = 5` | `const x = 5` | `int x = 5` | `x := 5` | `let x = 5` |
| **Function** | `def f(x):` | `function f(x) {}` | `int f(int x) {}` | `func f(x int) int {}` | `fn f(x: i32) -> i32 {}` |
| **Class** | `class C:` | `class C {}` | `class C {}` | `type C struct {}` | `struct C {}` + `impl C {}` |
| **Interface** | `class I(ABC):` | N/A (duck typing) | `interface I {}` | `type I interface {}` | `trait I {}` |
| **List/Array** | `[1, 2, 3]` | `[1, 2, 3]` | `List.of(1, 2, 3)` | `[]int{1, 2, 3}` | `vec![1, 2, 3]` |
| **Dictionary/Map** | `{"a": 1}` | `{a: 1}` or `new Map()` | `Map.of("a", 1)` | `map[string]int{"a": 1}` | `HashMap::from([("a", 1)])` |
| **Null/None** | `None` | `null` / `undefined` | `null` | `nil` | `None` (Option) |
| **String interpolation** | `f"Hello {name}"` | `` `Hello ${name}` `` | `"Hello " + name` or `String.format` | `fmt.Sprintf("Hello %s", name)` | `format!("Hello {name}")` |
| **Lambda** | `lambda x: x + 1` | `(x) => x + 1` | `(x) -> x + 1` | `func(x int) int { return x + 1 }` | `\|x\| x + 1` |
| **Error handling** | `try/except` | `try/catch` | `try/catch` | `if err != nil` | `Result<T, E>` |
| **Async** | `async def / await` | `async function / await` | `CompletableFuture` | goroutines + channels | `async fn / .await` |

#### Collection Operation Mapping

| Operation | Python | JavaScript | Java |
|-----------|--------|------------|------|
| **Filter** | `[x for x in lst if x > 0]` | `lst.filter(x => x > 0)` | `lst.stream().filter(x -> x > 0).toList()` |
| **Map** | `[f(x) for x in lst]` | `lst.map(x => f(x))` | `lst.stream().map(x -> f(x)).toList()` |
| **Reduce** | `functools.reduce(f, lst)` | `lst.reduce((a, b) => f(a, b))` | `lst.stream().reduce(identity, f)` |
| **Sort** | `sorted(lst, key=f)` | `[...lst].sort((a, b) => f(a) - f(b))` | `lst.stream().sorted(Comparator.comparing(f)).toList()` |
| **Any/Some** | `any(p(x) for x in lst)` | `lst.some(x => p(x))` | `lst.stream().anyMatch(x -> p(x))` |
| **All/Every** | `all(p(x) for x in lst)` | `lst.every(x => p(x))` | `lst.stream().allMatch(x -> p(x))` |
| **Find first** | `next((x for x in lst if p(x)), None)` | `lst.find(x => p(x))` | `lst.stream().filter(x -> p(x)).findFirst()` |
| **Group by** | `itertools.groupby(sorted(lst, key=f), f)` | `Object.groupBy(lst, f)` | `lst.stream().collect(Collectors.groupingBy(f))` |
| **Flat map** | `[y for x in lst for y in f(x)]` | `lst.flatMap(x => f(x))` | `lst.stream().flatMap(x -> f(x).stream()).toList()` |

### Step 3: Translate with Idiomatic Style

Produce code that reads naturally in the target language, not a literal word-for-word translation.

#### Example: Python to JavaScript Translation

**Python source**:

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    completed: bool = False
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_overdue(self) -> bool:
        if self.due_date is None or self.completed:
            return False
        return datetime.now() > self.due_date

    def add_tag(self, tag: str) -> None:
        normalized = tag.strip().lower()
        if normalized and normalized not in self.tags:
            self.tags.append(normalized)


class TaskManager:
    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def add_task(self, task: Task) -> None:
        if task.id in self._tasks:
            raise ValueError(f"Task with id '{task.id}' already exists")
        self._tasks[task.id] = task

    def get_overdue_tasks(self) -> List[Task]:
        return [t for t in self._tasks.values() if t.is_overdue()]

    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        normalized = tag.strip().lower()
        return [t for t in self._tasks.values() if normalized in t.tags]

    def complete_task(self, task_id: str) -> Task:
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Task '{task_id}' not found")
        task.completed = True
        return task

    def get_summary(self) -> dict:
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks.values() if t.completed)
        overdue = len(self.get_overdue_tasks())
        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "overdue": overdue,
        }
```

**JavaScript translation (idiomatic)**:

```javascript
class Task {
    constructor(id, title, { description = "", completed = false, tags = [], dueDate = null } = {}) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.completed = completed;
        this.tags = [...tags];
        this.dueDate = dueDate;
        this.createdAt = new Date();
    }

    isOverdue() {
        if (!this.dueDate || this.completed) return false;
        return new Date() > this.dueDate;
    }

    addTag(tag) {
        const normalized = tag.trim().toLowerCase();
        if (normalized && !this.tags.includes(normalized)) {
            this.tags.push(normalized);
        }
    }
}

class TaskManager {
    #tasks = new Map();

    addTask(task) {
        if (this.#tasks.has(task.id)) {
            throw new Error(`Task with id '${task.id}' already exists`);
        }
        this.#tasks.set(task.id, task);
    }

    getOverdueTasks() {
        return [...this.#tasks.values()].filter(t => t.isOverdue());
    }

    getTasksByTag(tag) {
        const normalized = tag.trim().toLowerCase();
        return [...this.#tasks.values()].filter(t => t.tags.includes(normalized));
    }

    completeTask(taskId) {
        const task = this.#tasks.get(taskId);
        if (!task) {
            throw new Error(`Task '${taskId}' not found`);
        }
        task.completed = true;
        return task;
    }

    getSummary() {
        const tasks = [...this.#tasks.values()];
        const total = tasks.length;
        const completed = tasks.filter(t => t.completed).length;
        const overdue = this.getOverdueTasks().length;
        return { total, completed, pending: total - completed, overdue };
    }
}
```

**Translation notes**:

| Python Construct | JavaScript Equivalent | Rationale |
|-----------------|----------------------|-----------|
| `@dataclass` | Constructor with destructured options | JavaScript lacks dataclasses; options object pattern is idiomatic |
| `Optional[datetime]` | Nullable (`null` check) | JavaScript uses null/undefined instead of Optional |
| `dict[str, Task]` | `Map()` with private field (`#tasks`) | Map preserves insertion order and has better key semantics |
| `raise ValueError` | `throw new Error` | JavaScript has a single Error base type |
| `raise KeyError` | `throw new Error` | Same; use descriptive message to differentiate |
| List comprehension `[x for x in ...]` | `.filter()` / `.map()` | Array methods are idiomatic JavaScript |
| `field(default_factory=list)` | `[...tags]` spread copy | Prevent shared mutable default |

#### Example: JavaScript to Java Translation

**JavaScript source**:

```javascript
async function fetchUserProfile(userId) {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.status}`);
    }
    const data = await response.json();
    return {
        id: data.id,
        name: `${data.firstName} ${data.lastName}`,
        email: data.email,
        isActive: data.status === "active",
        roles: data.roles?.map(r => r.name) ?? [],
    };
}
```

**Java translation (idiomatic)**:

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public record UserProfile(
    String id,
    String name,
    String email,
    boolean isActive,
    List<String> roles
) {}

public class UserProfileService {
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String baseUrl;

    public UserProfileService(HttpClient httpClient, ObjectMapper objectMapper, String baseUrl) {
        this.httpClient = httpClient;
        this.objectMapper = objectMapper;
        this.baseUrl = baseUrl;
    }

    public UserProfile fetchUserProfile(String userId) throws UserFetchException {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/api/users/" + userId))
                .GET()
                .build();

            HttpResponse<String> response = httpClient.send(
                request, HttpResponse.BodyHandlers.ofString()
            );

            if (response.statusCode() != 200) {
                throw new UserFetchException(
                    "Failed to fetch user: HTTP " + response.statusCode()
                );
            }

            JsonNode data = objectMapper.readTree(response.body());
            String name = data.get("firstName").asText() + " " + data.get("lastName").asText();
            boolean isActive = "active".equals(data.path("status").asText());

            List<String> roles = Optional.ofNullable(data.get("roles"))
                .filter(JsonNode::isArray)
                .map(rolesNode -> {
                    List<String> result = new java.util.ArrayList<>();
                    rolesNode.forEach(r -> result.add(r.get("name").asText()));
                    return Collections.unmodifiableList(result);
                })
                .orElse(Collections.emptyList());

            return new UserProfile(
                data.get("id").asText(),
                name,
                data.get("email").asText(),
                isActive,
                roles
            );
        } catch (UserFetchException e) {
            throw e;
        } catch (Exception e) {
            throw new UserFetchException("Error fetching user profile", e);
        }
    }
}
```

### Step 4: Map Library Equivalents

When the source code uses language-specific libraries, find the equivalent in the target language.

#### Common Library Equivalents

| Domain | Python | JavaScript / Node.js | Java |
|--------|--------|---------------------|------|
| **HTTP Client** | `requests`, `httpx` | `fetch`, `axios` | `HttpClient` (java.net.http), OkHttp |
| **JSON Parsing** | `json` (stdlib) | `JSON.parse` (built-in) | Jackson, Gson |
| **Date/Time** | `datetime` | `Date`, `dayjs`, `date-fns` | `java.time` (LocalDate, Instant) |
| **Testing** | `pytest`, `unittest` | `jest`, `vitest`, `mocha` | JUnit 5, TestNG |
| **Mocking** | `unittest.mock`, `pytest-mock` | `jest.mock`, `sinon` | Mockito, WireMock |
| **ORM / Database** | SQLAlchemy, Django ORM | Prisma, Sequelize, TypeORM | Hibernate, JOOQ, Spring Data |
| **Web Framework** | Flask, FastAPI, Django | Express, Fastify, Next.js | Spring Boot, Quarkus |
| **Logging** | `logging` (stdlib) | `winston`, `pino` | SLF4J + Logback, Log4j2 |
| **Validation** | `pydantic`, `marshmallow` | `zod`, `joi`, `yup` | Bean Validation (Hibernate Validator) |
| **CLI Parsing** | `argparse`, `click` | `commander`, `yargs` | picocli, JCommander |
| **Concurrency** | `asyncio`, `threading` | Promises, `async/await` | `CompletableFuture`, `ExecutorService` |
| **Regular Expressions** | `re` (stdlib) | `RegExp` (built-in) | `java.util.regex.Pattern` |

### Step 5: Handle Type System Differences

Different type systems require careful adaptation during translation.

| Aspect | Dynamic (Python, JS) | Static (Java, Go, Rust) | Translation Strategy |
|--------|---------------------|------------------------|---------------------|
| **Duck typing** | Objects used by shape, not declared type | Must implement explicit interface | Introduce interfaces in target |
| **Nullable types** | Any variable can be None/null | Explicit Optional, nullable annotation | Add null checks or Optional wrappers |
| **Union types** | `str \| int` | Sealed interfaces, generics | Use sealed classes or generics |
| **Generic collections** | `list` holds any type | `List<String>` requires type parameter | Add type parameters |
| **Tuples** | `(1, "two", 3.0)` | Records, custom classes | Create named types |
| **Dynamic dispatch** | Method calls resolved at runtime | Compile-time type checking | Use interfaces and polymorphism |
| **Type coercion** | Implicit in JS (`"5" + 3 = "53"`) | Explicit in Java | Add explicit conversion calls |

### Step 6: Test the Translation

Verify that the translated code produces identical results to the source code.

#### Testing Strategy

1. **Port the test suite**: translate unit tests alongside the production code; if tests pass in both languages, the translation is likely correct
2. **Use golden output comparison**: run both implementations with the same inputs and compare outputs character by character
3. **Test edge cases**: null/undefined, empty collections, boundary values, special characters, and error conditions
4. **Test error behavior**: verify that both versions throw errors for the same invalid inputs

#### Python Example: Translation Verification Test

```python
import subprocess
import json


def test_translation_equivalence():
    """Run both Python and JavaScript implementations with same inputs
    and verify identical outputs."""
    test_cases = [
        {"input": [3, 1, 4, 1, 5], "operation": "sort"},
        {"input": [1, 2, 3, 4, 5], "operation": "filter_even"},
        {"input": [], "operation": "sort"},
        {"input": [None, 1, None, 2], "operation": "remove_nulls"},
    ]

    for case in test_cases:
        input_json = json.dumps(case)

        # Run Python version
        py_result = subprocess.run(
            ["python", "solution.py", input_json],
            capture_output=True, text=True
        )

        # Run JavaScript version
        js_result = subprocess.run(
            ["node", "solution.js", input_json],
            capture_output=True, text=True
        )

        assert py_result.stdout.strip() == js_result.stdout.strip(), (
            f"Mismatch for input {case}: "
            f"Python={py_result.stdout.strip()}, "
            f"JS={js_result.stdout.strip()}"
        )
```

## Best Practices

- **Translate idioms, not syntax**: a list comprehension in Python should become `.filter().map()` in JavaScript, not a `for` loop that builds an array; each language has its own natural way of expressing the same logic
- **Preserve the public API contract**: method names, parameter order, return types, and error types should match as closely as possible between versions to maintain interoperability expectations
- **Translate tests alongside code**: tests serve as the specification; translating them ensures the target implementation matches the source behavior
- **Use the target language's standard library**: do not import a third-party library to replicate a source-language built-in when the target language has an equivalent in its standard library
- **Handle encoding and locale differences**: string handling, date formatting, and number formatting vary between languages and platforms; explicitly set locale and encoding rather than relying on defaults
- **Preserve error semantics**: if the source throws a specific exception type, the target should throw an equivalent; do not silently swallow errors or change error types during translation
- **Document translation decisions**: when a construct has no direct equivalent and a judgment call was made, document the decision and rationale in a comment
- **Benchmark performance-critical translations**: algorithmic complexity should be preserved, but constant factors and memory usage may differ; benchmark if performance matters

## Common Pitfalls

- **Literal translation that ignores idioms**: writing Java-style code in Python (e.g., getter/setter methods instead of properties, `StringBuilder` instead of f-strings) produces correct but unidiomatic code that is harder for native developers to maintain
- **Missing null/undefined handling differences**: Python's `None`, JavaScript's `null` and `undefined`, Java's `null`, and Rust's `Option` have different semantics; a direct mapping may introduce bugs at boundaries
- **Integer overflow differences**: Python integers have arbitrary precision; JavaScript numbers are 64-bit floats; Java integers are fixed-width with overflow; Go integers are fixed-width with silent overflow; Rust integers panic on overflow in debug mode
- **String encoding differences**: Python 3 strings are Unicode; Java strings are UTF-16; Go strings are UTF-8 byte sequences; JavaScript strings are UTF-16; character indexing and length calculations may differ for non-ASCII text
- **Collection mutability differences**: Python lists are mutable; Java `List.of()` returns an immutable list; JavaScript arrays are always mutable; Go slices have copy-on-write gotchas; ensure mutability semantics match
- **Concurrency model differences**: translating `async/await` from JavaScript to Java requires understanding that JavaScript is single-threaded while Java is multi-threaded; thread safety concerns that do not exist in JavaScript may exist in Java
- **Equality semantics**: Python's `==` compares values; JavaScript's `===` compares values and types; Java's `==` compares references (for objects); ensure equality checks are translated correctly
- **Default parameter handling**: Python evaluates default parameters once at function definition time (mutable default pitfall); JavaScript evaluates defaults at each call; Java does not support default parameters; each requires different translation patterns
- **Error handling model mismatch**: translating Python exceptions to Go error returns (or Rust Results) requires restructuring control flow, not just swapping syntax
