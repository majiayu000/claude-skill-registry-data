---
name: property-based-test-generator
description: Generate property-based tests using QuickCheck/Hypothesis-style frameworks that verify invariants over randomly generated inputs. Use when testing.
---

# Property-Based Test Generator

Generate property-based tests that verify invariants, algebraic properties, and behavioural contracts over large numbers of randomly generated inputs. Instead of manually choosing specific test cases, property-based testing describes what should always be true and lets the framework find counterexamples through automated input generation and shrinking.

## When to Use This Skill

Use this skill when you need to:

- Verify mathematical or algebraic properties (commutativity, associativity, idempotency)
- Test round-trip conversions (serialize then deserialize, encode then decode)
- Validate sorting, searching, and collection operations against their contracts
- Discover edge cases that manual test writing would miss
- Test state machines and stateful protocols with model-based testing
- Verify that refactored code preserves the same behaviour as the original
- Test parsers, compilers, or transformers with grammar-based input generation
- Ensure API contract invariants hold across arbitrary valid request payloads

**Trigger phrases**: "property-based test", "hypothesis test", "quickcheck", "generative testing", "shrinking", "property test", "invariant test", "round-trip test", "model-based test", "stateful test", "fuzzy test inputs", "random test generation"

## What This Skill Does

### Core Concepts

#### Properties

A property is a universally quantified statement: "For all valid inputs x, some condition holds". Unlike an example-based test that checks one specific case, a property test checks thousands of randomly generated cases.

**Examples of properties:**
- For all lists `xs`: `sorted(xs)` has the same length as `xs`
- For all strings `s`: `decode(encode(s)) == s`
- For all positive integers `n`: `sqrt(n * n) == n`
- For all valid JSON objects `obj`: `parse(stringify(obj))` equals `obj`

#### Generators (Strategies)

Generators produce random values within a specified domain. Frameworks provide built-in generators for primitive types and combinators to build complex ones.

#### Shrinking

When a property test finds a failing input, the framework automatically simplifies (shrinks) it to the smallest counterexample that still fails. This makes debugging dramatically easier: instead of a 500-element list causing a failure, you see a 2-element list that triggers the same bug.

#### Stateful / Model-Based Testing

For systems with mutable state (databases, caches, queues), property-based testing can generate random sequences of operations, execute them against both the real system and a simplified reference model, and verify that outputs match at every step.

### Framework Mapping

| Language | Framework | Generator Term | Decorator/Annotation |
|---|---|---|---|
| Python | Hypothesis | `st.strategy()` | `@given(...)` |
| JavaScript | fast-check | `fc.arbitrary()` | `fc.assert(fc.property(...))` |
| Java | jqwik | `@Provide Arbitrary<T>` | `@Property` |
| Haskell | QuickCheck | `Gen a` | `prop_` prefix |
| Scala | ScalaCheck | `Gen[A]` | `forAll { ... }` |
| Rust | proptest | `proptest! { ... }` | `prop_compose!` |

## Instructions

### Step 1: Identify Properties Worth Testing

Before writing generators, identify the properties that your code should satisfy. Here are common property patterns:

| Property Pattern | Description | Example |
|---|---|---|
| **Round-trip** | `decode(encode(x)) == x` | JSON, Base64, compression |
| **Idempotency** | `f(f(x)) == f(x)` | Formatting, normalization, deduplication |
| **Commutativity** | `f(a, b) == f(b, a)` | Addition, set union, merge |
| **Associativity** | `f(f(a, b), c) == f(a, f(b, c))` | String concatenation, list append |
| **Invariant preservation** | Some condition holds before and after | Sorted order after insert, size after filter |
| **Equivalence** | Two implementations produce the same result | Optimized vs naive, new vs old |
| **No crash** | Function does not throw for any valid input | Parser, validator, API handler |

### Step 2: Write Round-Trip Property Tests

**Python (Hypothesis):**
```python
from hypothesis import given, strategies as st, settings, assume
import json


@given(st.text())
def test_json_string_round_trip(s):
    """Encoding a string to JSON and decoding it back yields the original."""
    encoded = json.dumps(s)
    decoded = json.loads(encoded)
    assert decoded == s


@given(st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=50,
))
def test_json_object_round_trip(obj):
    """Any JSON-compatible object survives a round-trip through dumps/loads."""
    encoded = json.dumps(obj)
    decoded = json.loads(encoded)
    assert decoded == obj


@given(st.binary())
def test_base64_round_trip(data):
    """Base64 encoding and decoding preserves the original bytes."""
    import base64
    encoded = base64.b64encode(data)
    decoded = base64.b64decode(encoded)
    assert decoded == data


@given(st.lists(st.integers()))
def test_sort_preserves_elements(xs):
    """Sorting a list does not add or remove elements."""
    sorted_xs = sorted(xs)
    assert sorted(sorted_xs) == sorted(xs)
    assert len(sorted_xs) == len(xs)
```

**JavaScript (fast-check):**
```javascript
const fc = require("fast-check");

describe("round-trip properties", () => {
  test("JSON round-trip preserves strings", () => {
    fc.assert(
      fc.property(fc.string(), (s) => {
        const encoded = JSON.stringify(s);
        const decoded = JSON.parse(encoded);
        return decoded === s;
      })
    );
  });

  test("JSON round-trip preserves objects", () => {
    fc.assert(
      fc.property(fc.jsonValue(), (obj) => {
        const encoded = JSON.stringify(obj);
        const decoded = JSON.parse(encoded);
        expect(decoded).toEqual(obj);
      })
    );
  });

  test("Base64 round-trip preserves buffers", () => {
    fc.assert(
      fc.property(fc.uint8Array(), (data) => {
        const buffer = Buffer.from(data);
        const encoded = buffer.toString("base64");
        const decoded = Buffer.from(encoded, "base64");
        return buffer.equals(decoded);
      })
    );
  });

  test("sort preserves elements", () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (xs) => {
        const sorted = [...xs].sort((a, b) => a - b);
        expect(sorted).toHaveLength(xs.length);
        expect([...sorted].sort((a, b) => a - b)).toEqual(
          [...xs].sort((a, b) => a - b)
        );
      })
    );
  });
});
```

**Java (jqwik):**
```java
import net.jqwik.api.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class RoundTripPropertyTest {

    private final ObjectMapper mapper = new ObjectMapper();

    @Property
    void jsonStringRoundTrip(@ForAll String s) throws Exception {
        String encoded = mapper.writeValueAsString(s);
        String decoded = mapper.readValue(encoded, String.class);
        assertEquals(s, decoded);
    }

    @Property
    void base64RoundTrip(@ForAll byte[] data) {
        String encoded = Base64.getEncoder().encodeToString(data);
        byte[] decoded = Base64.getDecoder().decode(encoded);
        assertArrayEquals(data, decoded);
    }

    @Property
    void sortPreservesElements(@ForAll List<@ForAll Integer> xs) {
        var sorted = new ArrayList<>(xs);
        Collections.sort(sorted);
        assertEquals(xs.size(), sorted.size());
        var xsSorted = new ArrayList<>(xs);
        Collections.sort(xsSorted);
        assertEquals(xsSorted, sorted);
    }
}
```

### Step 3: Write Invariant Preservation Properties

**Python:**
```python
from hypothesis import given, strategies as st


@given(st.lists(st.integers()), st.integers())
def test_insert_into_sorted_list_preserves_order(xs, value):
    """Inserting a value into a sorted list keeps it sorted."""
    import bisect
    sorted_xs = sorted(xs)
    bisect.insort(sorted_xs, value)
    assert sorted_xs == sorted(sorted_xs)
    assert len(sorted_xs) == len(xs) + 1


@given(st.lists(st.integers(), min_size=1))
def test_max_is_greater_or_equal_to_all_elements(xs):
    """The maximum of a non-empty list is >= every element."""
    m = max(xs)
    for x in xs:
        assert m >= x


@given(st.dictionaries(st.text(), st.integers()))
def test_dict_keys_are_unique(d):
    """Dictionary keys are always unique."""
    assert len(d.keys()) == len(set(d.keys()))


@given(st.lists(st.integers()))
def test_filter_produces_subset(xs):
    """Filtering a list produces a subset of the original."""
    evens = [x for x in xs if x % 2 == 0]
    assert len(evens) <= len(xs)
    for e in evens:
        assert e in xs
        assert e % 2 == 0
```

**JavaScript:**
```javascript
const fc = require("fast-check");

describe("invariant preservation properties", () => {
  test("inserting into sorted array preserves sorted order", () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), fc.integer(), (xs, value) => {
        const sorted = [...xs].sort((a, b) => a - b);
        // Binary insert
        const idx = sorted.findIndex((x) => x >= value);
        sorted.splice(idx === -1 ? sorted.length : idx, 0, value);

        for (let i = 1; i < sorted.length; i++) {
          expect(sorted[i]).toBeGreaterThanOrEqual(sorted[i - 1]);
        }
        expect(sorted).toHaveLength(xs.length + 1);
      })
    );
  });

  test("filter produces a subset", () => {
    fc.assert(
      fc.property(fc.array(fc.integer()), (xs) => {
        const evens = xs.filter((x) => x % 2 === 0);
        expect(evens.length).toBeLessThanOrEqual(xs.length);
        evens.forEach((e) => {
          expect(xs).toContain(e);
          expect(e % 2).toBe(0);
        });
      })
    );
  });
});
```

**Java:**
```java
import net.jqwik.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class InvariantPropertyTest {

    @Property
    void insertIntoSortedPreservesOrder(
            @ForAll List<@ForAll Integer> xs,
            @ForAll int value) {
        var sorted = new ArrayList<>(xs);
        Collections.sort(sorted);
        int idx = Collections.binarySearch(sorted, value);
        if (idx < 0) idx = -(idx + 1);
        sorted.add(idx, value);

        for (int i = 1; i < sorted.size(); i++) {
            assertTrue(sorted.get(i) >= sorted.get(i - 1));
        }
        assertEquals(xs.size() + 1, sorted.size());
    }

    @Property
    void maxIsGreaterOrEqualToAllElements(
            @ForAll @Size(min = 1) List<@ForAll Integer> xs) {
        int max = Collections.max(xs);
        for (int x : xs) {
            assertTrue(max >= x);
        }
    }
}
```

### Step 4: Write Custom Generators

**Python:**
```python
from hypothesis import given, strategies as st
from dataclasses import dataclass


@dataclass
class Money:
    amount: int  # cents
    currency: str


# Custom strategy for Money objects
money_strategy = st.builds(
    Money,
    amount=st.integers(min_value=0, max_value=100_000_00),  # 0 to $100,000
    currency=st.sampled_from(["USD", "EUR", "GBP", "JPY"]),
)


@given(money_strategy, money_strategy)
def test_money_addition_is_commutative(a, b):
    """Adding money in the same currency is commutative."""
    from hypothesis import assume
    assume(a.currency == b.currency)
    result_ab = Money(a.amount + b.amount, a.currency)
    result_ba = Money(b.amount + a.amount, b.currency)
    assert result_ab == result_ba


# Strategy for valid email addresses
email_strategy = st.from_regex(
    r"[a-z][a-z0-9]{0,19}@[a-z]{2,10}\.(com|org|net)",
    fullmatch=True,
)


@given(email_strategy)
def test_email_validation_accepts_valid_emails(email):
    """The email validator accepts all structurally valid emails."""
    assert validate_email(email) is True


# Strategy for nested tree structures
def tree_strategy(max_depth=3):
    """Generate a random tree structure."""
    if max_depth <= 0:
        return st.just({"value": 0, "children": []})
    return st.fixed_dictionaries({
        "value": st.integers(min_value=-100, max_value=100),
        "children": st.lists(
            st.deferred(lambda: tree_strategy(max_depth - 1)),
            max_size=3,
        ),
    })


@given(tree_strategy())
def test_tree_traversal_visits_all_nodes(tree):
    """In-order traversal visits every node exactly once."""
    visited = []
    traverse(tree, visited)
    assert count_nodes(tree) == len(visited)
```

**JavaScript:**
```javascript
const fc = require("fast-check");

// Custom arbitrary for Money
const moneyArb = fc.record({
  amount: fc.integer({ min: 0, max: 10000000 }),
  currency: fc.constantFrom("USD", "EUR", "GBP", "JPY"),
});

describe("custom generators", () => {
  test("money addition is commutative for same currency", () => {
    fc.assert(
      fc.property(moneyArb, moneyArb, (a, b) => {
        fc.pre(a.currency === b.currency);
        const ab = { amount: a.amount + b.amount, currency: a.currency };
        const ba = { amount: b.amount + a.amount, currency: b.currency };
        expect(ab).toEqual(ba);
      })
    );
  });

  // Custom arbitrary for valid email
  const emailArb = fc
    .tuple(
      fc.stringOf(fc.constantFrom(..."abcdefghijklmnopqrstuvwxyz0123456789"), {
        minLength: 1,
        maxLength: 20,
      }),
      fc.stringOf(fc.constantFrom(..."abcdefghijklmnopqrstuvwxyz"), {
        minLength: 2,
        maxLength: 10,
      }),
      fc.constantFrom("com", "org", "net")
    )
    .map(([user, domain, tld]) => `${user}@${domain}.${tld}`);

  test("email validator accepts valid emails", () => {
    fc.assert(
      fc.property(emailArb, (email) => {
        expect(validateEmail(email)).toBe(true);
      })
    );
  });

  // Custom arbitrary for tree structures
  const treeArb = fc.letrec((tie) => ({
    tree: fc.record({
      value: fc.integer({ min: -100, max: 100 }),
      children: fc.array(tie("tree"), { maxLength: 3, depthIdentifier: "tree" }),
    }),
  })).tree;

  test("tree traversal visits all nodes", () => {
    fc.assert(
      fc.property(treeArb, (tree) => {
        const visited = [];
        traverse(tree, visited);
        expect(visited.length).toBe(countNodes(tree));
      })
    );
  });
});
```

**Java:**
```java
import net.jqwik.api.*;
import java.util.*;

class CustomGeneratorPropertyTest {

    record Money(int amountCents, String currency) {}

    @Provide
    Arbitrary<Money> moneyArbitrary() {
        var amount = Arbitraries.integers().between(0, 10_000_00);
        var currency = Arbitraries.of("USD", "EUR", "GBP", "JPY");
        return Combinators.combine(amount, currency).as(Money::new);
    }

    @Property
    void moneyAdditionIsCommutative(
            @ForAll("moneyArbitrary") Money a,
            @ForAll("moneyArbitrary") Money b) {
        Assume.that(a.currency().equals(b.currency()));
        var ab = new Money(a.amountCents() + b.amountCents(), a.currency());
        var ba = new Money(b.amountCents() + a.amountCents(), b.currency());
        assertEquals(ab, ba);
    }

    @Provide
    Arbitrary<String> validEmailArbitrary() {
        var user = Arbitraries.strings()
                .withCharRange('a', 'z').ofMinLength(1).ofMaxLength(20);
        var domain = Arbitraries.strings()
                .withCharRange('a', 'z').ofMinLength(2).ofMaxLength(10);
        var tld = Arbitraries.of("com", "org", "net");
        return Combinators.combine(user, domain, tld)
                .as((u, d, t) -> u + "@" + d + "." + t);
    }

    @Property
    void emailValidatorAcceptsValidEmails(
            @ForAll("validEmailArbitrary") String email) {
        assertTrue(EmailValidator.isValid(email));
    }
}
```

### Step 5: Write Stateful / Model-Based Tests

**Python (Hypothesis stateful testing):**
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, initialize
from hypothesis import strategies as st


class QueueModel(RuleBasedStateMachine):
    """Model-based test comparing a queue implementation against a list model."""

    def __init__(self):
        super().__init__()
        self.model = []  # Reference model: a simple list
        self.queue = None  # System under test

    @initialize()
    def create_queue(self):
        self.queue = BoundedQueue(max_size=100)
        self.model = []

    @rule(value=st.integers())
    def enqueue(self, value):
        if len(self.model) < 100:
            self.queue.enqueue(value)
            self.model.append(value)

    @rule()
    def dequeue(self):
        if len(self.model) > 0:
            expected = self.model.pop(0)
            actual = self.queue.dequeue()
            assert actual == expected

    @rule()
    def peek(self):
        if len(self.model) > 0:
            expected = self.model[0]
            actual = self.queue.peek()
            assert actual == expected

    @invariant()
    def size_matches(self):
        if self.queue is not None:
            assert self.queue.size() == len(self.model)

    @invariant()
    def empty_matches(self):
        if self.queue is not None:
            assert self.queue.is_empty() == (len(self.model) == 0)


TestQueueModel = QueueModel.TestCase
```

**JavaScript (fast-check model-based):**
```javascript
const fc = require("fast-check");

describe("queue model-based test", () => {
  test("queue behaves like a list model", () => {
    const EnqueueCommand = fc.record({ value: fc.integer() }).map((r) => ({
      check: (model) => model.length < 100,
      run: (model, real) => {
        model.push(r.value);
        real.enqueue(r.value);
      },
      toString: () => `enqueue(${r.value})`,
    }));

    const DequeueCommand = fc.constant({
      check: (model) => model.length > 0,
      run: (model, real) => {
        const expected = model.shift();
        const actual = real.dequeue();
        expect(actual).toBe(expected);
      },
      toString: () => "dequeue()",
    });

    const PeekCommand = fc.constant({
      check: (model) => model.length > 0,
      run: (model, real) => {
        const expected = model[0];
        const actual = real.peek();
        expect(actual).toBe(expected);
      },
      toString: () => "peek()",
    });

    fc.assert(
      fc.property(
        fc.commands([EnqueueCommand, DequeueCommand, PeekCommand], {
          maxCommands: 100,
        }),
        (cmds) => {
          const model = [];
          const real = new BoundedQueue(100);
          fc.modelRun(() => ({ model, real }), cmds);
        }
      )
    );
  });
});
```

### Step 6: Leverage Shrinking for Debugging

**Python:**
```python
from hypothesis import given, strategies as st, settings


@given(st.lists(st.integers(min_value=1, max_value=1000), min_size=1))
@settings(max_examples=1000)
def test_average_is_within_range(xs):
    """The average of a list of positive integers is between min and max.

    If this property fails, Hypothesis will shrink the counterexample
    to the smallest list that still fails. For example, instead of
    reporting [342, 1, 789, 23, ...], it might shrink to [1, 2].
    """
    avg = sum(xs) / len(xs)
    assert min(xs) <= avg <= max(xs)


@given(st.text(min_size=1))
def test_reverse_reverse_is_identity(s):
    """Reversing a string twice yields the original.

    If this fails (it should not), Hypothesis will shrink to the
    shortest possible counterexample string.
    """
    assert s[::-1][::-1] == s
```

## Best Practices

- **Start with round-trip and invariant properties**: These are the easiest to identify and provide the highest value; every serialization format, every sorted collection, and every normalization function has a natural round-trip or invariant
- **Write properties that are independent of the implementation**: A property like "sorted output has the same elements as the input" is implementation-independent; a property like "quicksort partitions around the pivot" is testing the algorithm, not the contract
- **Use `assume` / `fc.pre` sparingly**: Rejecting too many generated inputs wastes test budget; instead, write generators that produce only valid inputs
- **Set a high example count in CI**: Use 100 examples locally for fast feedback, but 10,000 in CI to catch rare edge cases
- **Save and replay failing seeds**: When a property test fails, save the random seed so you can reproduce the exact failure deterministically
- **Trust the shrinking**: Do not try to interpret the original large counterexample; wait for the framework to shrink it to the minimal case
- **Combine with example-based tests**: Property-based tests complement but do not replace specific example-based tests for known edge cases and regression tests
- **Keep properties simple**: A property that is harder to understand than the code it tests provides no value; each property should express one clear invariant

## Common Pitfalls

- **Writing properties that are too weak**: `assert result is not None` is a property, but it catches almost no bugs; properties should make strong claims about the output
- **Accidentally re-implementing the function in the property**: If your property is `assert my_sort(xs) == sorted(xs)`, you are testing against Python's built-in sort, which may mask bugs in your sort that happen to match Python's behaviour
- **Ignoring floating-point properties**: Floating-point arithmetic is not associative or commutative; properties involving floats need approximate comparison with tolerances
- **Generating inputs that are too constrained**: If your generator only produces lists of length 0-3, you will miss bugs that appear at length 100+; use the default ranges unless you have a specific reason to constrain
- **Not running enough examples**: 100 examples may be enough for simple properties, but complex state machines need 10,000+ to cover interesting operation sequences
- **Forgetting to handle the empty case**: Many properties should hold for empty inputs too (empty list, empty string, empty dict); make sure your generator includes them
- **Mixing up the model and the system under test**: In stateful testing, the model must be trivially correct (e.g., a list for a queue); if the model itself has bugs, the test is worthless
- **Not investigating shrunken counterexamples**: The shrunken counterexample is a gift; it tells you the minimal conditions for failure; investigate it carefully before fixing
