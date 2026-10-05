---
name: edge-case-generator
description: Systematically generate edge case tests for boundary conditions, empty inputs, overflow, null values, concurrency edges, and type coercion. Use when.
---

# Edge Case Test Generator

Systematically generate edge case tests that expose boundary conditions, invalid inputs, overflow scenarios, null/undefined handling, concurrency hazards, and type coercion surprises. This skill applies boundary value analysis, equivalence partitioning, and special-value injection to produce tests that catch the defects most likely to escape basic happy-path coverage.

## When to Use This Skill

Use this skill when you need to:

- Harden a function or API against unexpected, extreme, or adversarial inputs
- Identify boundary bugs around minimum, maximum, and off-by-one values
- Validate null, undefined, empty, and missing-field handling
- Test numeric overflow, underflow, and precision loss scenarios
- Cover Unicode, encoding, and locale-sensitive string edge cases
- Detect type coercion surprises in dynamically typed languages
- Stress-test concurrent access patterns for race conditions and deadlocks
- Satisfy security review requirements for input validation coverage
- Complement existing unit tests that only cover the happy path

**Trigger phrases**: "edge cases", "boundary tests", "null handling tests", "overflow tests", "empty input tests", "special value tests", "corner cases", "defensive tests", "input validation tests", "boundary value analysis", "equivalence partitioning"

## What This Skill Does

### Methodology Overview

The edge case generator follows a structured four-phase approach:

1. **Input Domain Analysis**: Decompose each parameter into its valid domain, boundary values, and equivalence classes
2. **Special Value Injection**: Apply a catalogue of known-problematic values (null, zero, negative, MAX_INT, empty string, Unicode edge cases)
3. **Combination Explosion Management**: Use pairwise or category-partition methods to generate high-value combinations without combinatorial blowup
4. **Oracle Definition**: For each generated input, determine the expected outcome (specific return value, exception type, graceful degradation, or invariant preservation)

### Boundary Value Analysis (BVA)

For every numeric, string-length, or collection-size parameter, test exactly at:

- The minimum valid value
- One below the minimum (invalid)
- One above the minimum
- A nominal (typical) value
- One below the maximum
- The maximum valid value
- One above the maximum (invalid)

### Equivalence Partitioning

Divide the input space into classes that should be treated identically by the code:

- **Valid equivalence classes**: Sets of inputs that should produce a successful result
- **Invalid equivalence classes**: Sets of inputs that should be rejected or handled gracefully
- **Boundary equivalence classes**: Inputs that sit exactly on partition edges

### Special Value Catalogue

| Category | Values to Test |
|---|---|
| Numeric | 0, -1, 1, -0.0, MAX_INT, MIN_INT, MAX_FLOAT, NaN, Infinity, -Infinity, very small floats (5e-324) |
| String | empty string `""`, single character, very long string (10k+ chars), whitespace-only, null character `\0`, multi-byte Unicode, RTL text, emoji, combining characters, surrogate pairs |
| Collection | empty list/array, single element, duplicate elements, very large collection (100k+), nested empty collections |
| Object/Map | empty object, missing required keys, extra unexpected keys, null values for required fields, deeply nested objects, circular references |
| Boolean/Truthy | true, false, null, undefined, 0, 1, empty string (in loosely typed languages) |
| Date/Time | epoch (1970-01-01), far future (9999-12-31), leap year dates (Feb 29), DST transition times, negative timestamps, timezone boundaries |

### Concurrency Edge Cases

- Simultaneous reads and writes to shared state
- Double-submit / double-click scenarios
- Resource exhaustion under concurrent load
- Lock ordering inversions leading to deadlocks
- Check-then-act race conditions (TOCTOU)

## Instructions

### Step 1: Identify the Function Under Test and Its Input Domain

Examine the function signature, documentation, and implementation to catalogue every parameter, its type, its valid range, and any implicit constraints.

**Python example (target function):**
```python
def paginate_results(items: list, page: int, page_size: int) -> dict:
    """Return a page of results with metadata.

    Args:
        items: The full list of items to paginate.
        page: 1-based page number.
        page_size: Number of items per page (1-100).

    Returns:
        Dict with keys: 'data', 'page', 'page_size', 'total_pages', 'total_items'.

    Raises:
        ValueError: If page < 1 or page_size not in [1, 100].
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if not 1 <= page_size <= 100:
        raise ValueError("page_size must be between 1 and 100")
    start = (page - 1) * page_size
    end = start + page_size
    total_pages = max(1, -(-len(items) // page_size))
    return {
        "data": items[start:end],
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_items": len(items),
    }
```

### Step 2: Apply Boundary Value Analysis

Generate tests at each boundary for every parameter.

**Python (pytest):**
```python
import pytest
from pagination import paginate_results


class TestPaginateResultsBoundaryValues:
    """Boundary value analysis for paginate_results."""

    # --- page parameter boundaries ---

    def test_page_minimum_valid(self):
        result = paginate_results(list(range(50)), page=1, page_size=10)
        assert result["page"] == 1
        assert result["data"] == list(range(10))

    def test_page_below_minimum_raises(self):
        with pytest.raises(ValueError, match="page must be >= 1"):
            paginate_results(list(range(50)), page=0, page_size=10)

    def test_page_negative_raises(self):
        with pytest.raises(ValueError, match="page must be >= 1"):
            paginate_results(list(range(50)), page=-1, page_size=10)

    def test_page_beyond_last_returns_empty(self):
        result = paginate_results(list(range(10)), page=100, page_size=10)
        assert result["data"] == []

    # --- page_size parameter boundaries ---

    def test_page_size_minimum_valid(self):
        result = paginate_results(list(range(5)), page=1, page_size=1)
        assert result["data"] == [0]
        assert result["total_pages"] == 5

    def test_page_size_maximum_valid(self):
        result = paginate_results(list(range(200)), page=1, page_size=100)
        assert len(result["data"]) == 100

    def test_page_size_below_minimum_raises(self):
        with pytest.raises(ValueError, match="page_size must be between 1 and 100"):
            paginate_results(list(range(10)), page=1, page_size=0)

    def test_page_size_above_maximum_raises(self):
        with pytest.raises(ValueError, match="page_size must be between 1 and 100"):
            paginate_results(list(range(10)), page=1, page_size=101)

    # --- items parameter boundaries ---

    def test_empty_items_list(self):
        result = paginate_results([], page=1, page_size=10)
        assert result["data"] == []
        assert result["total_items"] == 0
        assert result["total_pages"] == 1

    def test_single_item_list(self):
        result = paginate_results(["only"], page=1, page_size=10)
        assert result["data"] == ["only"]
        assert result["total_items"] == 1

    def test_items_exactly_fill_one_page(self):
        result = paginate_results(list(range(10)), page=1, page_size=10)
        assert len(result["data"]) == 10
        assert result["total_pages"] == 1

    def test_items_one_more_than_page_size(self):
        result = paginate_results(list(range(11)), page=2, page_size=10)
        assert result["data"] == [10]
        assert result["total_pages"] == 2
```

**JavaScript (Jest):**
```javascript
const { paginateResults } = require("./pagination");

describe("paginateResults boundary values", () => {
  // --- page parameter boundaries ---

  test("page=1 returns the first page", () => {
    const result = paginateResults(Array.from({ length: 50 }, (_, i) => i), 1, 10);
    expect(result.page).toBe(1);
    expect(result.data).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
  });

  test("page=0 throws an error", () => {
    expect(() => paginateResults([1, 2, 3], 0, 10)).toThrow("page must be >= 1");
  });

  test("page=-1 throws an error", () => {
    expect(() => paginateResults([1, 2, 3], -1, 10)).toThrow("page must be >= 1");
  });

  test("page beyond last page returns empty data", () => {
    const result = paginateResults([1, 2, 3], 100, 10);
    expect(result.data).toEqual([]);
  });

  // --- page_size parameter boundaries ---

  test("page_size=1 returns one item per page", () => {
    const result = paginateResults([10, 20, 30], 1, 1);
    expect(result.data).toEqual([10]);
    expect(result.totalPages).toBe(3);
  });

  test("page_size=100 is the maximum allowed", () => {
    const items = Array.from({ length: 200 }, (_, i) => i);
    const result = paginateResults(items, 1, 100);
    expect(result.data).toHaveLength(100);
  });

  test("page_size=0 throws an error", () => {
    expect(() => paginateResults([1], 1, 0)).toThrow();
  });

  test("page_size=101 throws an error", () => {
    expect(() => paginateResults([1], 1, 101)).toThrow();
  });

  // --- items parameter boundaries ---

  test("empty array returns empty data", () => {
    const result = paginateResults([], 1, 10);
    expect(result.data).toEqual([]);
    expect(result.totalItems).toBe(0);
  });

  test("single-element array", () => {
    const result = paginateResults(["only"], 1, 10);
    expect(result.data).toEqual(["only"]);
    expect(result.totalItems).toBe(1);
  });
});
```

**Java (JUnit 5):**
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class PaginateResultsBoundaryTest {

    // --- page parameter boundaries ---

    @Test
    void page1ReturnsFirstPage() {
        var items = java.util.stream.IntStream.range(0, 50)
                .boxed().toList();
        var result = Paginator.paginate(items, 1, 10);
        assertEquals(1, result.getPage());
        assertEquals(10, result.getData().size());
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, -100, Integer.MIN_VALUE})
    void pageBelowMinimumThrows(int invalidPage) {
        var items = java.util.List.of(1, 2, 3);
        assertThrows(IllegalArgumentException.class,
                () -> Paginator.paginate(items, invalidPage, 10));
    }

    @Test
    void pageBeyondLastReturnsEmptyData() {
        var items = java.util.List.of(1, 2, 3);
        var result = Paginator.paginate(items, 100, 10);
        assertTrue(result.getData().isEmpty());
    }

    // --- page_size parameter boundaries ---

    @Test
    void pageSizeOneReturnsOneItemPerPage() {
        var items = java.util.List.of(10, 20, 30);
        var result = Paginator.paginate(items, 1, 1);
        assertEquals(1, result.getData().size());
        assertEquals(3, result.getTotalPages());
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, 101, 1000, Integer.MAX_VALUE})
    void pageSizeOutOfRangeThrows(int invalidSize) {
        var items = java.util.List.of(1, 2, 3);
        assertThrows(IllegalArgumentException.class,
                () -> Paginator.paginate(items, 1, invalidSize));
    }

    // --- items parameter boundaries ---

    @Test
    void emptyListReturnsEmptyData() {
        var result = Paginator.paginate(java.util.List.of(), 1, 10);
        assertTrue(result.getData().isEmpty());
        assertEquals(0, result.getTotalItems());
    }

    @Test
    void singleElementList() {
        var result = Paginator.paginate(java.util.List.of("only"), 1, 10);
        assertEquals(1, result.getData().size());
        assertEquals(1, result.getTotalItems());
    }
}
```

### Step 3: Apply Special Value Injection

Test with values from the special value catalogue that are relevant to each parameter type.

**Python:**
```python
class TestPaginateResultsSpecialValues:
    """Special value injection for paginate_results."""

    def test_page_max_int(self):
        import sys
        result = paginate_results([1, 2, 3], page=sys.maxsize, page_size=10)
        assert result["data"] == []

    def test_page_size_negative_raises(self):
        with pytest.raises(ValueError):
            paginate_results([1, 2, 3], page=1, page_size=-1)

    def test_items_contain_none_values(self):
        result = paginate_results([None, None, None], page=1, page_size=10)
        assert result["data"] == [None, None, None]

    def test_items_contain_mixed_types(self):
        mixed = [1, "two", 3.0, None, True, [], {}]
        result = paginate_results(mixed, page=1, page_size=10)
        assert result["data"] == mixed

    def test_items_contain_empty_strings(self):
        result = paginate_results(["", "", ""], page=1, page_size=2)
        assert result["data"] == ["", ""]

    def test_very_large_items_list(self):
        large = list(range(100_000))
        result = paginate_results(large, page=1, page_size=100)
        assert len(result["data"]) == 100
        assert result["total_items"] == 100_000

    def test_items_with_unicode(self):
        items = ["\u0000", "\uffff", "\U0001f600", "\u200b", "\u202e"]
        result = paginate_results(items, page=1, page_size=10)
        assert result["data"] == items

    def test_items_with_deeply_nested_structures(self):
        nested = [{"a": {"b": {"c": {"d": [1, 2, 3]}}}}]
        result = paginate_results(nested, page=1, page_size=10)
        assert result["data"] == nested
```

**JavaScript:**
```javascript
describe("paginateResults special values", () => {
  test("page = Number.MAX_SAFE_INTEGER returns empty data", () => {
    const result = paginateResults([1, 2, 3], Number.MAX_SAFE_INTEGER, 10);
    expect(result.data).toEqual([]);
  });

  test("page = NaN throws an error", () => {
    expect(() => paginateResults([1], NaN, 10)).toThrow();
  });

  test("page = Infinity throws an error", () => {
    expect(() => paginateResults([1], Infinity, 10)).toThrow();
  });

  test("page_size = 1.5 (non-integer) throws or truncates", () => {
    expect(() => paginateResults([1, 2, 3], 1, 1.5)).toThrow();
  });

  test("items containing undefined values", () => {
    const result = paginateResults([undefined, undefined], 1, 10);
    expect(result.data).toHaveLength(2);
  });

  test("items containing objects with circular references", () => {
    const obj = { name: "test" };
    obj.self = obj;
    // Should not throw during pagination (only during serialization)
    const result = paginateResults([obj], 1, 10);
    expect(result.data).toHaveLength(1);
  });

  test("string passed as page coercion", () => {
    // Depending on implementation, this should throw or be handled
    expect(() => paginateResults([1], "1", 10)).toThrow();
  });
});
```

**Java:**
```java
class PaginateResultsSpecialValuesTest {

    @Test
    void pageMaxIntReturnsEmptyData() {
        var items = java.util.List.of(1, 2, 3);
        var result = Paginator.paginate(items, Integer.MAX_VALUE, 10);
        assertTrue(result.getData().isEmpty());
    }

    @Test
    void nullItemsListThrowsNullPointerException() {
        assertThrows(NullPointerException.class,
                () -> Paginator.paginate(null, 1, 10));
    }

    @Test
    void itemsContainingNullElements() {
        var items = java.util.Arrays.asList(null, null, null);
        var result = Paginator.paginate(items, 1, 10);
        assertEquals(3, result.getData().size());
    }

    @Test
    void unmodifiableListAsInput() {
        var items = java.util.Collections.unmodifiableList(
                java.util.List.of(1, 2, 3));
        // Should work without attempting to modify the input
        var result = Paginator.paginate(items, 1, 10);
        assertEquals(3, result.getData().size());
    }

    @Test
    void concurrentModificationDuringPagination() {
        var items = new java.util.ArrayList<>(java.util.List.of(1, 2, 3, 4, 5));
        // Simulating concurrent modification risk
        assertDoesNotThrow(() -> Paginator.paginate(items, 1, 2));
    }
}
```

### Step 4: Test Type Coercion Edges (Dynamic Languages)

In JavaScript and Python, implicit type coercion can cause subtle bugs.

**Python:**
```python
class TestTypeCoercionEdges:
    """Type coercion edge cases for loosely typed inputs."""

    def test_boolean_true_as_page_acts_as_1(self):
        # bool is a subclass of int in Python: True == 1
        result = paginate_results([1, 2, 3], page=True, page_size=10)
        assert result["page"] == 1

    def test_boolean_false_as_page_raises(self):
        # False == 0, which is below the minimum
        with pytest.raises(ValueError):
            paginate_results([1, 2, 3], page=False, page_size=10)

    def test_float_page_that_is_whole_number(self):
        # 2.0 == 2 in Python, but may cause slicing issues
        result = paginate_results(list(range(30)), page=2, page_size=10)
        assert result["data"] == list(range(10, 20))

    def test_string_page_raises_type_error(self):
        with pytest.raises(TypeError):
            paginate_results([1, 2], page="1", page_size=10)

    def test_none_page_raises_type_error(self):
        with pytest.raises(TypeError):
            paginate_results([1, 2], page=None, page_size=10)
```

**JavaScript:**
```javascript
describe("type coercion edge cases", () => {
  test("boolean true as page (coerces to 1)", () => {
    // true === 1 in numeric context
    expect(() => paginateResults([1, 2], true, 10)).toThrow();
  });

  test("null as page_size", () => {
    expect(() => paginateResults([1, 2], 1, null)).toThrow();
  });

  test("undefined as page", () => {
    expect(() => paginateResults([1], undefined, 10)).toThrow();
  });

  test("object as page triggers type check", () => {
    expect(() => paginateResults([1], {}, 10)).toThrow();
  });

  test("array as page triggers type check", () => {
    expect(() => paginateResults([1], [1], 10)).toThrow();
  });

  test("empty string as page_size", () => {
    // "" coerces to 0 in numeric context
    expect(() => paginateResults([1], 1, "")).toThrow();
  });
});
```

### Step 5: Test Unicode and Encoding Edge Cases

**Python:**
```python
class TestUnicodeEdgeCases:
    """Unicode and encoding edge cases in string-processing functions."""

    def test_empty_string(self):
        assert normalize_name("") == ""

    def test_null_character_in_string(self):
        result = normalize_name("hello\x00world")
        assert "\x00" not in result

    def test_zero_width_space(self):
        result = normalize_name("hello\u200bworld")
        # Zero-width space should be stripped or handled
        assert result in ("helloworld", "hello world")

    def test_combining_characters(self):
        # e followed by combining acute accent vs precomposed e-acute
        assert normalize_name("e\u0301") == normalize_name("\u00e9")

    def test_surrogate_pairs(self):
        # Emoji that requires surrogate pairs in UTF-16
        result = normalize_name("\U0001f600")  # grinning face
        assert isinstance(result, str)

    def test_right_to_left_override(self):
        result = normalize_name("\u202ehello")
        # RTL override character should be stripped
        assert "\u202e" not in result

    def test_very_long_unicode_string(self):
        long_str = "\u00e9" * 10_000
        result = normalize_name(long_str)
        assert len(result) <= 10_000

    def test_mixed_scripts(self):
        result = normalize_name("Hello\u4e16\u754c\u041f\u0440\u0438\u0432\u0435\u0442")
        assert isinstance(result, str)
```

**JavaScript:**
```javascript
describe("Unicode edge cases", () => {
  test("empty string input", () => {
    expect(normalizeName("")).toBe("");
  });

  test("null character in string", () => {
    const result = normalizeName("hello\x00world");
    expect(result).not.toContain("\x00");
  });

  test("emoji input (surrogate pair in UTF-16)", () => {
    const result = normalizeName("\uD83D\uDE00");
    expect(typeof result).toBe("string");
  });

  test("zero-width joiner sequences", () => {
    // Family emoji: multiple code points joined with ZWJ
    const family = "\u{1F468}\u200D\u{1F469}\u200D\u{1F467}";
    const result = normalizeName(family);
    expect(typeof result).toBe("string");
  });

  test("string with only whitespace variants", () => {
    const whitespace = "\t \n \r \u00A0 \u2003";
    const result = normalizeName(whitespace);
    expect(result.trim()).toBe("");
  });
});
```

**Java:**
```java
class UnicodeEdgeCasesTest {

    @Test
    void emptyStringInput() {
        assertEquals("", NameNormalizer.normalize(""));
    }

    @Test
    void nullCharacterInString() {
        String result = NameNormalizer.normalize("hello\0world");
        assertFalse(result.contains("\0"));
    }

    @Test
    void supplementaryPlaneCharacter() {
        // Emoji U+1F600 requires two chars in Java's UTF-16
        String emoji = "\uD83D\uDE00";
        String result = NameNormalizer.normalize(emoji);
        assertNotNull(result);
    }

    @Test
    void combiningCharacterNormalization() {
        // e + combining acute vs precomposed e-acute
        String decomposed = "e\u0301";
        String precomposed = "\u00E9";
        assertEquals(
                NameNormalizer.normalize(precomposed),
                NameNormalizer.normalize(decomposed)
        );
    }

    @Test
    void mixedScriptsInput() {
        String mixed = "Hello\u4E16\u754C\u041F\u0440\u0438\u0432\u0435\u0442";
        assertDoesNotThrow(() -> NameNormalizer.normalize(mixed));
    }
}
```

### Step 6: Test Concurrency Edge Cases

**Python:**
```python
import threading
import time


class TestConcurrencyEdgeCases:
    """Concurrency edge cases for shared-state operations."""

    def test_concurrent_counter_increments(self):
        counter = ThreadSafeCounter()
        threads = []
        for _ in range(100):
            t = threading.Thread(target=counter.increment)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        assert counter.value == 100

    def test_concurrent_reads_during_write(self):
        cache = SharedCache()
        cache.put("key", "initial")
        errors = []

        def reader():
            for _ in range(1000):
                val = cache.get("key")
                if val is None:
                    errors.append("Got None during concurrent read")

        def writer():
            for i in range(1000):
                cache.put("key", f"value_{i}")

        reader_thread = threading.Thread(target=reader)
        writer_thread = threading.Thread(target=writer)
        reader_thread.start()
        writer_thread.start()
        reader_thread.join()
        writer_thread.join()
        assert len(errors) == 0, f"Concurrent read failures: {errors[:5]}"

    def test_double_close_resource(self):
        resource = ManagedResource()
        resource.close()
        # Second close should not raise
        resource.close()
        assert resource.is_closed
```

**JavaScript:**
```javascript
describe("concurrency edge cases", () => {
  test("concurrent promise resolution order", async () => {
    const results = [];
    const fast = new Promise((resolve) =>
      setTimeout(() => { results.push("fast"); resolve(); }, 10)
    );
    const slow = new Promise((resolve) =>
      setTimeout(() => { results.push("slow"); resolve(); }, 50)
    );
    await Promise.all([slow, fast]);
    expect(results[0]).toBe("fast");
  });

  test("double-submit prevention", async () => {
    const handler = new SubmitHandler();
    const [result1, result2] = await Promise.all([
      handler.submit({ id: 1 }),
      handler.submit({ id: 1 }),
    ]);
    // One should succeed, one should be rejected as duplicate
    const successes = [result1, result2].filter((r) => r.status === "ok");
    expect(successes).toHaveLength(1);
  });

  test("race condition in check-then-act", async () => {
    const inventory = new Inventory({ widget: 1 });
    const purchase1 = inventory.purchase("widget");
    const purchase2 = inventory.purchase("widget");
    const results = await Promise.allSettled([purchase1, purchase2]);
    const fulfilled = results.filter((r) => r.status === "fulfilled");
    expect(fulfilled.length).toBeLessThanOrEqual(1);
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.RepeatedTest;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import static org.junit.jupiter.api.Assertions.*;

class ConcurrencyEdgeCasesTest {

    @RepeatedTest(10)
    void concurrentIncrementsAreAtomic() throws Exception {
        var counter = new ThreadSafeCounter();
        int threadCount = 100;
        var latch = new CountDownLatch(threadCount);
        var executor = Executors.newFixedThreadPool(threadCount);

        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                counter.increment();
                latch.countDown();
            });
        }
        latch.await(5, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(threadCount, counter.getValue());
    }

    @Test
    void doubleCloseDoesNotThrow() {
        var resource = new ManagedResource();
        resource.close();
        assertDoesNotThrow(resource::close);
    }

    @Test
    void concurrentMapAccessDoesNotLoseEntries() throws Exception {
        var map = new ConcurrentHashMap<String, Integer>();
        int threadCount = 50;
        var latch = new CountDownLatch(threadCount);
        var executor = Executors.newFixedThreadPool(threadCount);

        for (int i = 0; i < threadCount; i++) {
            final int idx = i;
            executor.submit(() -> {
                map.put("key-" + idx, idx);
                latch.countDown();
            });
        }
        latch.await(5, TimeUnit.SECONDS);
        executor.shutdown();
        assertEquals(threadCount, map.size());
    }
}
```

### Step 7: Combine Edge Cases with Equivalence Partitioning

Use the category-partition method to generate meaningful combinations without testing every permutation.

**Python:**
```python
import pytest


class TestPaginateResultsCombinations:
    """Category-partition combinations for paginate_results."""

    @pytest.mark.parametrize(
        "items, page, page_size, expected_len",
        [
            # empty items + valid pagination
            ([], 1, 10, 0),
            # single item + first page + size=1
            ([42], 1, 1, 1),
            # many items + last page + size=1
            (list(range(100)), 100, 1, 1),
            # many items + first page + max size
            (list(range(200)), 1, 100, 100),
            # items exactly fill page
            (list(range(10)), 1, 10, 10),
            # items one short of filling second page
            (list(range(11)), 2, 10, 1),
        ],
    )
    def test_partition_combinations(self, items, page, page_size, expected_len):
        result = paginate_results(items, page, page_size)
        assert len(result["data"]) == expected_len

    @pytest.mark.parametrize(
        "page, page_size",
        [
            (0, 10),     # page below min
            (-1, 10),    # page negative
            (1, 0),      # size below min
            (1, 101),    # size above max
            (0, 0),      # both invalid
            (-1, 101),   # both invalid, opposite extremes
        ],
    )
    def test_invalid_combinations_raise(self, page, page_size):
        with pytest.raises(ValueError):
            paginate_results([1, 2, 3], page, page_size)
```

## Best Practices

- **Start with boundary value analysis**: It catches the most common off-by-one and range errors with minimal test count
- **Use parameterized tests**: Avoid duplicating test boilerplate when only inputs and expected outputs differ
- **Name tests descriptively**: Each test name should describe the specific edge condition, not just "test1", "test2"
- **Test one edge per test method**: Isolate edge cases so that failures pinpoint the exact boundary that broke
- **Include both the input and the expected outcome**: Edge case tests are only valuable when the oracle (expected result) is clearly defined
- **Prioritize edges by risk**: Focus first on edges that involve security (overflow, injection), data loss (null handling), or financial impact (rounding, precision)
- **Keep the special value catalogue project-specific**: Add domain-relevant special values (e.g., for a healthcare app, test with patient ages of 0, 150, and negative)
- **Automate edge case discovery**: Use property-based testing (see the property-based-test-generator skill) to discover edge cases you did not anticipate
- **Revisit edges after bug fixes**: Every production bug reveals a missing edge case test; add it to the suite
- **Document why each edge matters**: A comment explaining "tests integer overflow on 32-bit systems" is more valuable than the test code alone

## Common Pitfalls

- **Testing only the happy path**: Writing 20 tests for valid inputs and zero tests for invalid inputs provides a false sense of security
- **Ignoring implicit boundaries**: Many boundaries are not in the specification but in the implementation (e.g., array index calculations, string encoding limits, database column widths)
- **Combinatorial explosion**: Testing every combination of every edge value is impractical; use pairwise or category-partition to keep the test count manageable
- **Asserting too loosely**: Using `assert result is not None` instead of asserting the specific expected value weakens the test oracle
- **Hardcoding environment-specific values**: Tests that use `MAX_INT` for a 64-bit system will behave differently on 32-bit; use language constants like `sys.maxsize` or `Integer.MAX_VALUE`
- **Forgetting concurrency edges**: Single-threaded tests pass, but the same code fails under concurrent load; always test shared-state operations with multiple threads
- **Not testing error message content**: Verifying that an exception is thrown is good; verifying that the error message is helpful for debugging is better
- **Neglecting cleanup in edge case tests**: Edge cases that allocate large resources (100k-element lists, temporary files) must clean up to avoid test suite resource exhaustion
- **Copy-pasting boundary values incorrectly**: When porting edge case tests between languages, numeric limits differ (JavaScript `Number.MAX_SAFE_INTEGER` is not the same as Java `Integer.MAX_VALUE`)
- **Assuming defensive code exists**: Edge case tests should verify that the code handles the edge, not assume it does; if the code lacks validation, the test exposes the gap
