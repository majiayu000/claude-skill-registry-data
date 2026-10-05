---
name: metamorphic-test-generator
description: Generate metamorphic tests for systems without clear test oracles by defining transformation invariants between inputs and outputs. Use when testing ML.
---

# Metamorphic Test Generator

Generate metamorphic tests that verify software correctness by checking relationships between multiple executions rather than comparing against a single expected output. This technique is essential for testing systems where a traditional test oracle (a known correct answer for every input) is unavailable or impractical to define.

## When to Use This Skill

Use this skill when you need to:

- Test machine learning models where the "correct" prediction is unknown for novel inputs
- Verify search engine result quality without manually ranking every query
- Test numerical computations where exact expected values are difficult to compute independently
- Validate data analytics pipelines where output correctness depends on complex business logic
- Test compilers and code generators where output equivalence is hard to check directly
- Verify image processing, audio processing, or signal processing algorithms
- Test scientific computing software where reference implementations do not exist
- Validate any function where you can describe how the output should change when the input is transformed, even if you cannot specify the exact output

**Trigger phrases**: "metamorphic testing", "test oracle problem", "no expected output", "ML model testing", "search quality testing", "transformation invariant", "metamorphic relation", "test without oracle", "numerical testing", "relative testing"

## What This Skill Does

### The Oracle Problem

In traditional testing, every test case has a known expected output (the oracle). For many real-world systems, this oracle is unavailable:

| System | Why Oracle Is Hard |
|---|---|
| ML classifier | Correct label for a novel image is subjective |
| Search engine | Correct ranking for a query is unknown |
| Numerical solver | Analytical solution may not exist |
| Compiler optimizer | Correct optimized output is the entire specification |
| Weather simulator | Future weather is inherently uncertain |
| Recommendation engine | "Best" recommendation is user-dependent |

### Metamorphic Relations (MRs)

A metamorphic relation defines how the output should change (or stay the same) when the input is transformed in a specific way. Instead of checking `f(x) == expected`, you check `relationship(f(x), f(transform(x)))`.

**Common metamorphic relation patterns:**

| Pattern | Relation | Example |
|---|---|---|
| **Additive** | `f(x + c) == f(x) + c` | Currency converter: converting double the amount gives double the result |
| **Multiplicative** | `f(k * x) == k * f(x)` | Linear functions: scaling input scales output proportionally |
| **Permutation** | `f(permute(x)) == f(x)` | Sorting: output is the same regardless of input order |
| **Negation** | `f(-x) == -f(x)` | Odd functions: negating input negates output |
| **Inclusion** | `f(x) is subset of f(x + more_data)` | Search: adding documents can only increase results |
| **Monotonicity** | `x1 > x2 implies f(x1) >= f(x2)` | Pricing: more items cost at least as much |
| **Idempotency** | `f(f(x)) == f(x)` | Normalization: normalizing twice gives the same result |
| **Symmetry** | `f(x, y) == f(y, x)` | Distance: distance from A to B equals distance from B to A |

### Methodology

1. **Identify the system under test (SUT)** and its input/output domains
2. **Enumerate candidate metamorphic relations** using the patterns above
3. **Select relations** that are easy to verify and likely to catch real bugs
4. **Generate source test cases** (original inputs)
5. **Apply transformations** to produce follow-up test cases
6. **Execute both** and verify the metamorphic relation holds
7. **Report violations** as potential bugs

## Instructions

### Step 1: Define Metamorphic Relations for Your Domain

Before writing tests, enumerate the metamorphic relations that apply to your system.

**Python (relation definition framework):**
```python
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class MetamorphicRelation:
    """Defines a metamorphic relation between source and follow-up test cases."""
    name: str
    description: str
    transform_input: Callable[[Any], Any]
    check_relation: Callable[[Any, Any, Any, Any], bool]
    # check_relation(source_input, source_output, followup_input, followup_output) -> bool


@dataclass
class MetamorphicTestSuite:
    """Collection of metamorphic relations for a system under test."""
    sut: Callable
    relations: list[MetamorphicRelation] = field(default_factory=list)

    def add_relation(self, relation: MetamorphicRelation):
        self.relations.append(relation)

    def run(self, source_inputs: list[Any]) -> list[dict]:
        """Run all metamorphic relations against all source inputs."""
        results = []
        for source_input in source_inputs:
            source_output = self.sut(source_input)
            for relation in self.relations:
                followup_input = relation.transform_input(source_input)
                followup_output = self.sut(followup_input)
                passed = relation.check_relation(
                    source_input, source_output,
                    followup_input, followup_output,
                )
                results.append({
                    "relation": relation.name,
                    "source_input": source_input,
                    "source_output": source_output,
                    "followup_input": followup_input,
                    "followup_output": followup_output,
                    "passed": passed,
                })
        return results
```

### Step 2: Test Search and Retrieval Systems

**Python:**
```python
import pytest


class TestSearchEngineMetamorphic:
    """Metamorphic tests for a search engine where ranking correctness is unknown."""

    def setup_method(self):
        self.engine = SearchEngine()
        self.engine.index([
            {"id": 1, "title": "Python programming guide", "body": "Learn Python basics"},
            {"id": 2, "title": "Java programming tutorial", "body": "Introduction to Java"},
            {"id": 3, "title": "Python advanced topics", "body": "Decorators, generators, async"},
            {"id": 4, "title": "Web development with Python", "body": "Flask and Django frameworks"},
            {"id": 5, "title": "Machine learning in Python", "body": "scikit-learn, TensorFlow"},
        ])

    def test_adding_relevant_document_does_not_decrease_results(self):
        """MR: Adding a document that matches the query should not reduce the
        number of search results (inclusion/monotonicity)."""
        source_results = self.engine.search("Python")
        source_count = len(source_results)

        self.engine.index([
            {"id": 6, "title": "Python data science", "body": "pandas and numpy"},
        ])
        followup_results = self.engine.search("Python")
        followup_count = len(followup_results)

        assert followup_count >= source_count

    def test_restricting_query_reduces_or_maintains_results(self):
        """MR: A more specific query should return fewer or equal results
        compared to a broader query (monotonicity)."""
        broad_results = self.engine.search("Python")
        narrow_results = self.engine.search("Python advanced")

        assert len(narrow_results) <= len(broad_results)

    def test_query_word_order_does_not_change_result_set(self):
        """MR: Reordering query words should return the same set of documents
        (permutation invariance)."""
        results_ab = self.engine.search("Python programming")
        results_ba = self.engine.search("programming Python")

        ids_ab = {r["id"] for r in results_ab}
        ids_ba = {r["id"] for r in results_ba}
        assert ids_ab == ids_ba

    def test_case_insensitivity(self):
        """MR: Changing query case should not change results (invariance)."""
        results_lower = self.engine.search("python")
        results_upper = self.engine.search("PYTHON")
        results_mixed = self.engine.search("PyThOn")

        ids_lower = {r["id"] for r in results_lower}
        ids_upper = {r["id"] for r in results_upper}
        ids_mixed = {r["id"] for r in results_mixed}
        assert ids_lower == ids_upper == ids_mixed

    def test_removing_irrelevant_document_preserves_results(self):
        """MR: Removing a document that does not match the query should not
        change the result set (independence)."""
        source_results = self.engine.search("Python")
        source_ids = {r["id"] for r in source_results}

        # Remove a Java document (irrelevant to "Python" query)
        self.engine.remove(2)
        followup_results = self.engine.search("Python")
        followup_ids = {r["id"] for r in followup_results}

        assert source_ids == followup_ids
```

**JavaScript:**
```javascript
describe("search engine metamorphic tests", () => {
  let engine;

  beforeEach(() => {
    engine = new SearchEngine();
    engine.index([
      { id: 1, title: "Python programming guide", body: "Learn Python basics" },
      { id: 2, title: "Java programming tutorial", body: "Introduction to Java" },
      { id: 3, title: "Python advanced topics", body: "Decorators and generators" },
      { id: 4, title: "Web development with Python", body: "Flask and Django" },
    ]);
  });

  test("MR: narrower query returns subset of broader query results", () => {
    const broad = engine.search("Python");
    const narrow = engine.search("Python advanced");
    expect(narrow.length).toBeLessThanOrEqual(broad.length);
    const broadIds = new Set(broad.map((r) => r.id));
    narrow.forEach((r) => expect(broadIds.has(r.id)).toBe(true));
  });

  test("MR: query word order does not change result set", () => {
    const resultsAB = engine.search("Python programming");
    const resultsBA = engine.search("programming Python");
    const idsAB = new Set(resultsAB.map((r) => r.id));
    const idsBA = new Set(resultsBA.map((r) => r.id));
    expect(idsAB).toEqual(idsBA);
  });

  test("MR: adding relevant document does not reduce result count", () => {
    const before = engine.search("Python");
    engine.index([{ id: 5, title: "Python data science", body: "pandas" }]);
    const after = engine.search("Python");
    expect(after.length).toBeGreaterThanOrEqual(before.length);
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.*;
import java.util.stream.Collectors;
import static org.junit.jupiter.api.Assertions.*;

class SearchEngineMetamorphicTest {

    private SearchEngine engine;

    @BeforeEach
    void setUp() {
        engine = new SearchEngine();
        engine.index(List.of(
                new Document(1, "Python programming guide", "Learn Python basics"),
                new Document(2, "Java programming tutorial", "Introduction to Java"),
                new Document(3, "Python advanced topics", "Decorators and generators"),
                new Document(4, "Web development with Python", "Flask and Django")
        ));
    }

    @Test
    void narrowerQueryReturnsSubsetOfBroaderQuery() {
        var broad = engine.search("Python");
        var narrow = engine.search("Python advanced");

        assertTrue(narrow.size() <= broad.size());
        var broadIds = broad.stream().map(Document::getId).collect(Collectors.toSet());
        narrow.forEach(doc -> assertTrue(broadIds.contains(doc.getId())));
    }

    @Test
    void queryWordOrderDoesNotChangeResultSet() {
        var resultsAB = engine.search("Python programming");
        var resultsBA = engine.search("programming Python");

        var idsAB = resultsAB.stream().map(Document::getId).collect(Collectors.toSet());
        var idsBA = resultsBA.stream().map(Document::getId).collect(Collectors.toSet());
        assertEquals(idsAB, idsBA);
    }

    @Test
    void addingRelevantDocumentDoesNotReduceResultCount() {
        var before = engine.search("Python");
        engine.index(List.of(
                new Document(5, "Python data science", "pandas and numpy")
        ));
        var after = engine.search("Python");
        assertTrue(after.size() >= before.size());
    }
}
```

### Step 3: Test Machine Learning Models

**Python:**
```python
import numpy as np
import pytest


class TestImageClassifierMetamorphic:
    """Metamorphic tests for an image classifier where ground truth is unavailable."""

    def setup_method(self):
        self.model = load_pretrained_classifier()

    def test_brightness_invariance(self):
        """MR: Slightly adjusting brightness should not change the predicted class."""
        image = load_test_image("cat_photo.jpg")
        source_prediction = self.model.predict(image)

        brighter = np.clip(image * 1.1, 0, 255).astype(np.uint8)
        followup_prediction = self.model.predict(brighter)

        assert source_prediction.label == followup_prediction.label

    def test_horizontal_flip_preserves_class(self):
        """MR: Horizontally flipping an image should not change the predicted class
        for classes that are symmetric (e.g., 'cat', 'dog', but not 'left shoe')."""
        image = load_test_image("dog_photo.jpg")
        source_prediction = self.model.predict(image)

        flipped = np.fliplr(image)
        followup_prediction = self.model.predict(flipped)

        assert source_prediction.label == followup_prediction.label

    def test_adding_noise_reduces_confidence(self):
        """MR: Adding random noise should reduce prediction confidence
        (monotonicity of confidence with respect to noise level)."""
        image = load_test_image("bird_photo.jpg")
        source_prediction = self.model.predict(image)

        noise = np.random.normal(0, 25, image.shape).astype(np.int16)
        noisy = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        followup_prediction = self.model.predict(noisy)

        assert followup_prediction.confidence <= source_prediction.confidence + 0.05

    def test_scaling_preserves_class(self):
        """MR: Scaling an image up or down should not change the predicted class."""
        from PIL import Image
        image = load_test_image("car_photo.jpg")
        source_prediction = self.model.predict(image)

        pil_image = Image.fromarray(image)
        scaled = pil_image.resize(
            (pil_image.width * 2, pil_image.height * 2),
            Image.LANCZOS,
        )
        scaled_array = np.array(scaled)
        followup_prediction = self.model.predict(scaled_array)

        assert source_prediction.label == followup_prediction.label

    def test_duplicate_input_gives_same_output(self):
        """MR: The same input should always produce the same output
        (determinism / consistency)."""
        image = load_test_image("house_photo.jpg")
        prediction1 = self.model.predict(image)
        prediction2 = self.model.predict(image)

        assert prediction1.label == prediction2.label
        assert abs(prediction1.confidence - prediction2.confidence) < 1e-6


class TestSentimentAnalyzerMetamorphic:
    """Metamorphic tests for a sentiment analysis model."""

    def setup_method(self):
        self.model = load_sentiment_model()

    def test_negation_reverses_sentiment(self):
        """MR: Negating a sentence should reverse or at least change the sentiment."""
        source_sentiment = self.model.predict("The food was excellent")
        followup_sentiment = self.model.predict("The food was not excellent")

        assert source_sentiment.label != followup_sentiment.label

    def test_irrelevant_addition_preserves_sentiment(self):
        """MR: Adding an irrelevant clause should not change the overall sentiment."""
        source = self.model.predict("The movie was fantastic")
        followup = self.model.predict("The movie was fantastic, by the way it was Tuesday")

        assert source.label == followup.label

    def test_synonym_substitution_preserves_sentiment(self):
        """MR: Replacing words with synonyms should preserve sentiment."""
        source = self.model.predict("The service was terrible")
        followup = self.model.predict("The service was awful")

        assert source.label == followup.label

    def test_intensifier_increases_confidence(self):
        """MR: Adding an intensifier should increase sentiment confidence."""
        source = self.model.predict("The product is good")
        followup = self.model.predict("The product is very good")

        assert followup.confidence >= source.confidence - 0.05
```

### Step 4: Test Numerical Computations

**Python:**
```python
import math
import pytest


class TestNumericalSolverMetamorphic:
    """Metamorphic tests for numerical computations."""

    def test_sin_negation(self):
        """MR: sin(-x) == -sin(x) (odd function property)."""
        for x in [0.1, 0.5, 1.0, 2.5, math.pi, math.pi / 4]:
            assert abs(math.sin(-x) - (-math.sin(x))) < 1e-10

    def test_sin_periodicity(self):
        """MR: sin(x + 2*pi) == sin(x) (periodicity)."""
        for x in [0.0, 0.3, 1.0, math.pi / 2, math.pi]:
            assert abs(math.sin(x + 2 * math.pi) - math.sin(x)) < 1e-10

    def test_distance_symmetry(self):
        """MR: distance(A, B) == distance(B, A) (symmetry)."""
        points = [(0, 0), (1, 1), (3, 4), (-2, 5), (100, -50)]
        for a in points:
            for b in points:
                d_ab = compute_distance(a, b)
                d_ba = compute_distance(b, a)
                assert abs(d_ab - d_ba) < 1e-10

    def test_distance_triangle_inequality(self):
        """MR: distance(A, C) <= distance(A, B) + distance(B, C) (triangle inequality)."""
        import itertools
        points = [(0, 0), (1, 0), (0, 1), (3, 4), (-1, -1)]
        for a, b, c in itertools.combinations(points, 3):
            d_ac = compute_distance(a, c)
            d_ab = compute_distance(a, b)
            d_bc = compute_distance(b, c)
            assert d_ac <= d_ab + d_bc + 1e-10

    def test_matrix_multiplication_associativity(self):
        """MR: (A * B) * C == A * (B * C) (associativity)."""
        import numpy as np
        A = np.random.randn(3, 4)
        B = np.random.randn(4, 5)
        C = np.random.randn(5, 2)

        result1 = (A @ B) @ C
        result2 = A @ (B @ C)
        np.testing.assert_allclose(result1, result2, rtol=1e-10)

    def test_sorting_idempotency(self):
        """MR: sort(sort(x)) == sort(x) (idempotency)."""
        import random
        for _ in range(100):
            xs = [random.randint(-1000, 1000) for _ in range(50)]
            once = sorted(xs)
            twice = sorted(once)
            assert once == twice
```

**JavaScript:**
```javascript
describe("numerical computation metamorphic tests", () => {
  test("MR: sin(-x) == -sin(x) (odd function)", () => {
    const values = [0.1, 0.5, 1.0, 2.5, Math.PI, Math.PI / 4];
    values.forEach((x) => {
      expect(Math.abs(Math.sin(-x) - -Math.sin(x))).toBeLessThan(1e-10);
    });
  });

  test("MR: sin(x + 2pi) == sin(x) (periodicity)", () => {
    const values = [0.0, 0.3, 1.0, Math.PI / 2, Math.PI];
    values.forEach((x) => {
      expect(Math.abs(Math.sin(x + 2 * Math.PI) - Math.sin(x))).toBeLessThan(1e-10);
    });
  });

  test("MR: distance(A, B) == distance(B, A) (symmetry)", () => {
    const pairs = [
      [[0, 0], [3, 4]],
      [[1, 1], [-2, 5]],
      [[100, -50], [0, 0]],
    ];
    pairs.forEach(([a, b]) => {
      const dAB = computeDistance(a, b);
      const dBA = computeDistance(b, a);
      expect(Math.abs(dAB - dBA)).toBeLessThan(1e-10);
    });
  });

  test("MR: sort(sort(x)) == sort(x) (idempotency)", () => {
    for (let i = 0; i < 50; i++) {
      const xs = Array.from({ length: 30 }, () => Math.floor(Math.random() * 2000 - 1000));
      const once = [...xs].sort((a, b) => a - b);
      const twice = [...once].sort((a, b) => a - b);
      expect(once).toEqual(twice);
    }
  });
});
```

**Java:**
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;

class NumericalMetamorphicTest {

    @ParameterizedTest
    @ValueSource(doubles = {0.1, 0.5, 1.0, 2.5, Math.PI, Math.PI / 4})
    void sinNegationProperty(double x) {
        assertEquals(Math.sin(-x), -Math.sin(x), 1e-10,
                "sin(-x) should equal -sin(x)");
    }

    @ParameterizedTest
    @ValueSource(doubles = {0.0, 0.3, 1.0, Math.PI / 2, Math.PI})
    void sinPeriodicityProperty(double x) {
        assertEquals(Math.sin(x + 2 * Math.PI), Math.sin(x), 1e-10,
                "sin(x + 2pi) should equal sin(x)");
    }

    @Test
    void distanceSymmetry() {
        double[][] points = {{0, 0}, {3, 4}, {-2, 5}, {100, -50}};
        for (double[] a : points) {
            for (double[] b : points) {
                double dAB = Distance.compute(a, b);
                double dBA = Distance.compute(b, a);
                assertEquals(dAB, dBA, 1e-10);
            }
        }
    }

    @Test
    void sortingIdempotency() {
        var rng = new java.util.Random(42);
        for (int i = 0; i < 100; i++) {
            var xs = rng.ints(50, -1000, 1000).boxed()
                    .collect(java.util.stream.Collectors.toList());
            var once = new java.util.ArrayList<>(xs);
            java.util.Collections.sort(once);
            var twice = new java.util.ArrayList<>(once);
            java.util.Collections.sort(twice);
            assertEquals(once, twice);
        }
    }
}
```

### Step 5: Test Data Transformation Pipelines

**Python:**
```python
import pandas as pd
import pytest


class TestDataPipelineMetamorphic:
    """Metamorphic tests for a data transformation pipeline."""

    def test_row_count_preserved_by_transform(self):
        """MR: A transformation that does not filter should preserve row count."""
        source_df = pd.DataFrame({
            "name": ["Alice", "Bob", "Carol"],
            "age": [30, 25, 35],
            "salary": [50000, 60000, 70000],
        })
        result = transform_pipeline(source_df)
        assert len(result) == len(source_df)

    def test_adding_rows_increases_aggregate(self):
        """MR: Adding rows with positive values should increase the sum aggregate."""
        source_df = pd.DataFrame({"amount": [100, 200, 300]})
        source_total = aggregate_pipeline(source_df)["total_amount"]

        followup_df = pd.concat([source_df, pd.DataFrame({"amount": [50]})],
                                ignore_index=True)
        followup_total = aggregate_pipeline(followup_df)["total_amount"]

        assert followup_total > source_total

    def test_column_rename_preserves_data(self):
        """MR: Renaming columns should not change the underlying data values."""
        source_df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        renamed_df = source_df.rename(columns={"x": "a", "y": "b"})

        assert list(source_df["x"]) == list(renamed_df["a"])
        assert list(source_df["y"]) == list(renamed_df["b"])

    def test_duplicate_removal_idempotent(self):
        """MR: Removing duplicates twice gives the same result as once (idempotency)."""
        df = pd.DataFrame({"id": [1, 1, 2, 3, 3, 3], "value": [10, 10, 20, 30, 30, 30]})
        once = df.drop_duplicates()
        twice = once.drop_duplicates()
        pd.testing.assert_frame_equal(once, twice)

    def test_filter_then_count_monotonic(self):
        """MR: A stricter filter should produce fewer or equal rows (monotonicity)."""
        df = pd.DataFrame({"score": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        broad_filter = df[df["score"] >= 30]
        narrow_filter = df[df["score"] >= 50]

        assert len(narrow_filter) <= len(broad_filter)
```

## Best Practices

- **Start with domain-specific metamorphic relations**: Every domain has natural invariants; search engines have monotonicity, numerical code has symmetry, ML models have input perturbation robustness
- **Combine metamorphic testing with property-based testing**: Use property-based frameworks (Hypothesis, fast-check) to generate source inputs, then apply metamorphic transformations to those inputs
- **Keep transformations small**: Small perturbations are more likely to preserve the expected relationship; large transformations may legitimately change the output
- **Use multiple independent metamorphic relations**: A single relation catches a limited class of bugs; 5-10 diverse relations provide broader coverage
- **Quantify tolerance explicitly**: For approximate relations (confidence scores, floating-point values), define explicit tolerances rather than using exact equality
- **Generate diverse source inputs**: Metamorphic relations are only as good as the source inputs they are applied to; cover different regions of the input space
- **Document the reasoning behind each relation**: A metamorphic relation is a hypothesis about the system's behaviour; document why you believe it should hold
- **Use metamorphic testing for regression**: When you refactor code, metamorphic tests verify that the behavioural relationships are preserved even if exact outputs change

## Common Pitfalls

- **Choosing relations that are too weak**: The relation "output is not null" is technically metamorphic but catches almost no bugs; relations should make strong claims about the relationship between outputs
- **Assuming exact equality for approximate computations**: Floating-point arithmetic, ML predictions, and probabilistic algorithms produce approximate results; use tolerance-based comparisons
- **Confusing metamorphic testing with fuzz testing**: Fuzz testing generates random inputs to find crashes; metamorphic testing generates related input pairs to find semantic bugs; they are complementary but distinct
- **Not testing the metamorphic relation itself**: If the relation is wrong (the system legitimately violates it), the test produces false positives; validate the relation against known correct examples before deploying it
- **Ignoring the source input distribution**: If all source inputs are trivial (empty lists, zero values), the metamorphic transformations will also be trivial; use representative inputs from production workloads
- **Applying transformations that are too aggressive**: Replacing every word in a sentence is not a "small perturbation"; it legitimately changes the meaning; keep transformations minimal
- **Testing only one direction**: If the relation is "narrower query returns fewer results", also test the reverse: "broader query returns more results"; this catches different bug classes
- **Not reporting the full execution pair**: When a metamorphic test fails, report both the source input/output and the follow-up input/output; without both, debugging is impossible
