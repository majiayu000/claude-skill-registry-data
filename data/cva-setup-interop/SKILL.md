---
name: cva-setup-interop
description: Python interoperability setup using libpython-clj for Clojure agent development. Includes Python environment configuration, module importing strategies, data type conversion between Python and Clojure, NumPy/Pandas/HuggingFace integration, virtual environment setup, and performance optimization. Use when integrating Python ML libraries, setting up data science workflows, troubleshooting Python interop issues, working with NumPy arrays or Pandas DataFrames, or calling HuggingFace transformers from Clojure.
allowed-tools: Read,Bash,Edit,Write
---

# Python Interoperability Setup - libpython-clj

> **Purpose:** Complete guide for seamless Python-Clojure interoperability using libpython-clj
> **Prerequisites:** Python 3.8+, libpython-clj 2.025

## 🎯 Overview

**libpython-clj** enables you to use Python libraries directly from Clojure with idiomatic syntax, bridging two powerful ecosystems. This integration is crucial for agent development because it allows you to leverage Python's rich machine learning and data science ecosystem (NumPy, Pandas, HuggingFace, scikit-learn) while maintaining Clojure's functional programming benefits and concurrency primitives.

The library provides automatic data conversion between Python and Clojure data structures, allowing you to pass Clojure vectors to NumPy functions and receive results as Clojure data. This seamless integration eliminates the need for serialization/deserialization overhead and makes Python libraries feel native to Clojure.

This skill covers three initialization methods (auto-detection, manual configuration, and config files), multiple importing strategies, practical examples with popular ML libraries, and advanced patterns for production use including virtual environments, lazy loading, and performance optimization.

## 🌟 Key Capabilities

- ✅ Import Python modules as if they were Clojure namespaces
- ✅ Call Python functions with Clojure syntax
- ✅ Automatic data conversion between Python ↔ Clojure
- ✅ Use NumPy, Pandas, HuggingFace, scikit-learn, and more
- ✅ Context managers (Python's `with` statement)
- ✅ Thread-safe operations with GIL management

## 📦 Installation

### 1. Add Dependency (deps.edn)

```clojure
{:deps {clj-python/libpython-clj {:mvn/version "2.025"}}}
```

### 2. Verify Python Installation

```bash
# Check Python version (must be 3.8+)
python3 --version
# Expected: Python 3.8.x or higher

# Check Python location
which python3
# Expected: /usr/bin/python3

# Verify libpython shared library
python3 -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))"
# Expected: /usr/lib/x86_64-linux-gnu (or similar)

# List available libpython files
find /usr/lib -name "libpython*.so*" 2>/dev/null
# Expected: Shows libpython3.x.so files
```

## 🚀 Initialization Methods

### Method 1: Auto-Detection (Recommended)

```clojure
(ns lab.config.python
  (:require [libpython-clj2.python :as py]))

(defn init-python!
  "Initialize Python with automatic detection"
  []
  (py/initialize!)  ; Auto-detects installed Python
  (println "✅ Python initialized:"
           (py/get-attr (py/import-module "sys") "version")))

;; Use at application startup
(init-python!)
;; => ✅ Python initialized: 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]

(comment
  ;; Test in REPL
  (init-python!)
  ;; => ✅ Python initialized: 3.10.12...

  ;; Verify Python is initialized
  (def sys (py/import-module "sys"))
  (py/get-attr sys "version")
  ;; => "3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]"
  )
```

### Method 2: Manual Configuration (Fine Control)

```clojure
(py/initialize!
  :python-executable "/usr/bin/python3"
  :library-path "/usr/lib/x86_64-linux-gnu/libpython3.10.so")

;; Use when auto-detection fails or for specific Python version
(comment
  ;; Manual init with specific paths
  (py/initialize!
    :python-executable "/usr/local/bin/python3.11"
    :library-path "/usr/local/lib/libpython3.11.so")
  ;; => :ok
  )
```

### Method 3: Configuration File (python.edn)

Create `resources/python.edn`:
```clojure
{:python-executable "/usr/bin/python3"
 :library-path nil  ; nil = auto-detect
 :python-home nil}
```

In code:
```clojure
(py/initialize!)  ; Automatically loads from python.edn

(comment
  ;; Config file loaded automatically
  (py/initialize!)
  ;; => Reads settings from resources/python.edn
  )
```

## 📚 Importing Python Modules

### Style 1: require-python (Recommended - Clojure-like)

```clojure
(require '[libpython-clj2.require :refer [require-python]])

;; Import with alias (like Clojure namespaces)
(require-python '[numpy :as np])
(require-python '[pandas :as pd])
(require-python 'matplotlib.pyplot :as plt)

;; Use directly with Clojure syntax
(np/array [1 2 3 4 5])
;; => #<numpy.ndarray [1 2 3 4 5]>

(pd/DataFrame {:a [1 2 3] :b [4 5 6]})
;; => #<pandas.DataFrame>
;;      a  b
;;    0  1  4
;;    1  2  5
;;    2  3  6

(comment
  ;; Import and use immediately
  (require-python '[numpy :as np])
  (def arr (np/array [1 2 3]))
  (np/sum arr)
  ;; => 6
  )
```

### Style 2: import-module (Python Classic)

```clojure
(require '[libpython-clj2.python :as py])

(def np (py/import-module "numpy"))
(def pd (py/import-module "pandas"))

;; Use with py/call-attr or py. syntax
(py/call-attr np "array" [1 2 3])
;; => #<numpy.ndarray [1 2 3]>

(py. np array [1 2 3])  ; Java-like syntax
;; => #<numpy.ndarray [1 2 3]>

(comment
  ;; Classic import style
  (def math (py/import-module "math"))
  (py/call-attr math "sqrt" 16)
  ;; => 4.0

  (py. math sqrt 25)
  ;; => 5.0
  )
```

## 🔄 Data Conversion Between Python ↔ Clojure

### Automatic Conversions

| Python Type | Clojure Type | Example Conversion |
|-------------|--------------|-------------------|
| `int`, `float` | `Long`, `Double` | `42` → `42`, `3.14` → `3.14` |
| `str` | `String` | `"hello"` → `"hello"` |
| `list` | `vector` | `[1,2,3]` → `[1 2 3]` |
| `tuple` | `vector` | `(1,2)` → `[1 2]` |
| `dict` | `map` | `{"a":1}` → `{:a 1}` |
| `True`/`False` | `true`/`false` | Boolean conversion |
| `None` | `nil` | Null/nil equivalence |

### Practical Conversion Examples

```clojure
(require '[libpython-clj2.python :as py])
(require-python '[numpy :as np])

;; Clojure → Python automatic conversion
(def clj-data [1 2 3 4 5])
(def np-array (np/array clj-data))  ; Vector converts to NumPy array
;; => #<numpy.ndarray [1 2 3 4 5]>

;; Python → Clojure automatic conversion
(def result (np/sum np-array))  ; Returns Clojure Long
(println result)
;; => 15

;; Complex data structures
(def clj-map {:name "Alice" :scores [95 87 92]})
(def py-dict (py/->py-dict clj-map))
;; => {"name": "Alice", "scores": [95, 87, 92]}

(comment
  ;; Test conversions in REPL
  (def clj-vec [10 20 30])
  (def arr (np/array clj-vec))
  (np/mean arr)
  ;; => 20.0 (automatically converted to Clojure Double)

  ;; Nested structures
  (def nested {:users [{:name "Bob" :age 30}
                       {:name "Carol" :age 25}]})
  (def py-nested (py/->py-dict nested))
  ;; Works with nested maps and vectors
  )
```

### Manual Conversions

```clojure
;; Python object → Clojure data
(py/->jvm python-obj)

;; Clojure → Python explicit conversions
(py/->py-dict {:a 1 :b 2})     ; Map → dict
(py/->py-list [1 2 3])         ; Vector → list
(py/->py-tuple [1 2 3])        ; Vector → tuple
(py/->py-set #{1 2 3})         ; Set → set

(comment
  ;; Explicit conversion example
  (def py-list (py/->py-list [1 2 3 4 5]))
  (type py-list)
  ;; => <class 'list'>

  (def clj-vec (py/->jvm py-list))
  (type clj-vec)
  ;; => clojure.lang.PersistentVector
  )
```

## 💡 Practical Examples

### Example 1: NumPy Operations

```clojure
(require-python '[numpy :as np])

;; Create 2D array from Clojure vectors
(def arr (np/array [[1 2 3]
                     [4 5 6]]))

;; Statistical operations
(np/mean arr)  ; => 3.5
(np/std arr)   ; => 1.707825127659933
(np/max arr)   ; => 6

;; Indexing and slicing
(py/get-item arr 0)  ; First row: [1 2 3]
(py/get-item arr [0 1])  ; Element at [0,1]: 2

;; Mathematical operations
(def result (np/multiply arr 2))
;; => [[2 4 6]
;;     [8 10 12]]

(comment
  ;; REPL testing
  (def matrix (np/array [[1 2] [3 4]]))
  (np/linalg.det matrix)
  ;; => -2.0 (determinant)

  (np/linalg.inv matrix)
  ;; => [[-2.   1. ]
  ;;     [ 1.5 -0.5]]
  )
```

### Example 2: Pandas DataFrames

```clojure
(require-python '[pandas :as pd])

;; Create DataFrame from Clojure map
(def df (pd/DataFrame {:name ["Alice" "Bob" "Carol"]
                        :age [25 30 35]
                        :city ["SP" "RJ" "BH"]}))

;; Display
(py. df head)
;; =>    name  age city
;;    0  Alice   25   SP
;;    1    Bob   30   RJ
;;    2  Carol   35   BH

;; Operations
(py. df describe)  ; Statistical summary
(py/get-attr df "shape")  ; => (3, 3)

;; Column access
(def ages (py/get-item df "age"))
(py. ages mean)  ; => 30.0

;; Filtering
(def filtered (py/get-item df (py. (py/get-item df "age") __gt__ 28)))
;; => Rows where age > 28

(comment
  ;; REPL workflow
  (def sales-data (pd/DataFrame {:product ["A" "B" "C"]
                                  :revenue [1000 1500 1200]}))

  ;; Add computed column
  (py/set-item! sales-data "profit"
                (np/multiply (py/get-item sales-data "revenue") 0.3))

  (py. sales-data head)
  ;; => Shows table with profit column
  )
```

### Example 3: HuggingFace Transformers

```clojure
(require-python '[transformers :as hf])

;; Load sentiment analysis pipeline
(def sentiment (hf/pipeline "sentiment-analysis"))

;; Analyze text
(sentiment "I love Clojure!")
;; => [{"label" "POSITIVE", "score" 0.9998}]

;; Batch processing
(def results (sentiment ["Great!" "Terrible." "It's okay."]))
;; => [{"label" "POSITIVE", "score" 0.9998}
;;     {"label" "NEGATIVE", "score" 0.9995}
;;     {"label" "NEUTRAL", "score" 0.8542}]

(comment
  ;; REPL testing with different models
  (def classifier (hf/pipeline "zero-shot-classification"))
  (classifier "This is a technical document"
              :candidate_labels ["technology" "politics" "sports"])
  ;; => {"labels" ["technology" "politics" "sports"]
  ;;     "scores" [0.95, 0.03, 0.02]}
  )
```

### Example 4: Scikit-learn Machine Learning

```clojure
(require-python '[sklearn.ensemble :as ensemble]
                '[sklearn.model_selection :as model])

;; Create and train model
(def clf (ensemble/RandomForestClassifier :n_estimators 100))

(def X [[0 0] [1 1] [2 2] [3 3]])
(def y [0 1 1 0])

(py. clf fit X y)
;; => RandomForestClassifier(n_estimators=100)

;; Predict
(py. clf predict [[0.5 0.5] [2.5 2.5]])
;; => [0 1]

;; Cross-validation
(def scores (model/cross_val_score clf X y :cv 2))
;; => [0.5 1.0]

(comment
  ;; Full ML workflow
  (require-python '[sklearn.datasets :as datasets])

  (def iris (datasets/load_iris))
  (def X (py/get-attr iris "data"))
  (def y (py/get-attr iris "target"))

  (def model (ensemble/RandomForestClassifier))
  (py. model fit X y)

  (def accuracy (py. model score X y))
  ;; => 1.0 (perfect fit on training data)
  )
```

## 🎨 Advanced Usage Patterns

### Pattern 1: Clojure Wrapper for Python Library

```clojure
(ns lab.tools.sentiment
  "Sentiment analysis tool using HuggingFace"
  (:require [libpython-clj2.require :refer [require-python]]))

(require-python '[transformers :as hf])

(defonce ^:private sentiment-pipeline
  (delay (hf/pipeline "sentiment-analysis")))

(defn analyze-sentiment
  "Analyzes sentiment of text using HuggingFace transformer.

  Args:
    text - String to analyze

  Returns:
    Map with :label (string) and :score (float)

  Example:
    (analyze-sentiment \"Clojure is amazing!\")
    ;; => {:label \"POSITIVE\" :score 0.9998}"
  [text]
  (let [result (first (@sentiment-pipeline text))]
    {:label (py/get-item result "label")
     :score (py/get-item result "score")}))

(comment
  ;; Test wrapper
  (analyze-sentiment "This is great!")
  ;; => {:label "POSITIVE" :score 0.9998}

  (analyze-sentiment "This is terrible.")
  ;; => {:label "NEGATIVE" :score 0.9995}
  )
```

### Pattern 2: Context Manager (Python's `with` statement)

```clojure
(require '[libpython-clj2.python :as py])

;; Equivalent to: with open(file) as f: content = f.read()
(def content
  (py/with [f (py/call-attr (py/import-module "builtins")
                            "open" "file.txt" "r")]
    (py/call-attr f "read")))

(comment
  ;; Context manager for file operations
  (py/with [f (py/call-attr (py/import-module "builtins")
                            "open" "/tmp/test.txt" "w")]
    (py/call-attr f "write" "Hello from Clojure!"))
  ;; File automatically closed after block
  )
```

### Pattern 3: Lazy Loading Modules

```clojure
(defonce numpy
  (delay
    (require '[libpython-clj2.require :refer [require-python]])
    (require-python '[numpy :as np])
    np))

;; Module only loaded when first accessed
(defn calculate-mean [data]
  (@numpy/mean data))

(comment
  ;; Test lazy loading
  ;; numpy not loaded yet...
  (calculate-mean [1 2 3 4 5])
  ;; => 3.0
  ;; numpy loaded on first call
  )
```

### Pattern 4: Thread-Safe GIL Context

```clojure
;; For thread-safe Python operations
(py/with-gil-stack-rc-context
  (np/array [1 2 3]))

;; Use in concurrent scenarios
(defn parallel-numpy-ops [data-chunks]
  (pmap (fn [chunk]
          (py/with-gil-stack-rc-context
            (np/mean (np/array chunk))))
        data-chunks))

(comment
  ;; Test concurrent operations
  (def chunks [[1 2 3] [4 5 6] [7 8 9]])
  (parallel-numpy-ops chunks)
  ;; => (2.0 5.0 8.0)
  )
```

## 🔧 Advanced Configuration

### Using Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install packages
pip install numpy pandas transformers torch

# Test installation
python -c "import numpy; print(numpy.__version__)"
# Expected: Shows version like 1.24.3
```

Configure in Clojure:
```clojure
(py/initialize!
  :python-executable ".venv/bin/python"
  :library-path ".venv/lib/libpython3.10.so")

(comment
  ;; Verify venv Python is used
  (def sys (py/import-module "sys"))
  (py/get-attr sys "prefix")
  ;; => Should show .venv path
  )
```

### deps.edn with Virtual Environment

```clojure
{:aliases
  {:python-venv
   {:jvm-opts ["-Dpython.executable=.venv/bin/python"
               "-Dpython.library=.venv/lib/libpython3.10.so"]}}}
```

Usage:
```bash
clj -M:python-venv
```

## 🐛 Troubleshooting

### Error: "Unable to find library python3"

**Diagnosis:**
```bash
# Find libpython files
find /usr/lib -name "libpython*.so*" 2>/dev/null
# Expected: Shows available library paths

# Ubuntu/Debian - install dev package
sudo apt-get install python3-dev

# Verify installation
python3-config --ldflags
# Expected: Shows linker flags including -lpython3.x
```

**Solution:**
```clojure
;; Specify full path explicitly
(py/initialize!
  :library-path "/usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0")

(comment
  ;; Test explicit path
  (py/initialize!
    :library-path "/usr/lib/x86_64-linux-gnu/libpython3.10.so.1.0")
  ;; => :ok
  )
```

### Error: "Module not found"

```bash
# Check if module is installed
python3 -c "import numpy; print(numpy.__version__)"
# Expected: Shows version number

# Install if missing
pip install numpy pandas transformers

# Verify installation
pip list | grep numpy
# Expected: Shows numpy with version
```

### Error: "GIL-related error"

**Solution - Use GIL context:**
```clojure
(py/with-gil-stack-rc-context
  (np/array [1 2 3]))

;; For functions called from multiple threads
(defn safe-python-call [func & args]
  (py/with-gil-stack-rc-context
    (apply func args)))

(comment
  ;; Test thread-safe execution
  (safe-python-call np/array [1 2 3])
  ;; => Works even when called from different threads
  )
```

### Performance: Python calls slow

**Optimization:**
```clojure
;; Create optimized callable
(def fast-func (py/make-fastcallable python-func))

;; Use optimized version
(fast-func arg1 arg2)  ; Much faster than py/call-attr

(comment
  ;; Benchmark difference
  (require '[criterium.core :as crit])

  ;; Slow
  (crit/quick-bench (py/call-attr np "sum" [1 2 3]))

  ;; Fast
  (def fast-sum (py/make-fastcallable (py/get-attr np "sum")))
  (crit/quick-bench (fast-sum [1 2 3]))
  ;; => Significantly faster
  )
```

## 📊 Python vs Clojure+libpython-clj Comparison

### Python Native
```python
import numpy as np
import pandas as pd

arr = np.array([1, 2, 3, 4, 5])
mean = np.mean(arr)

df = pd.DataFrame({"a": [1, 2, 3]})
result = df["a"].sum()
```

### Clojure with libpython-clj
```clojure
(require-python '[numpy :as np]
                '[pandas :as pd])

(def arr (np/array [1 2 3 4 5]))
(def mean (np/mean arr))

(def df (pd/DataFrame {:a [1 2 3]}))
(def result (py. (py/get-item df "a") sum))

;; Or with pure Clojure data
(def clj-data [1 2 3 4 5])
(def mean (np/mean (np/array clj-data)))
;; => Works seamlessly with Clojure vectors
```

## ✅ Setup Checklist

- [ ] libpython-clj added to deps.edn
- [ ] Python 3.8+ installed and verified
- [ ] libpython shared library found by system
- [ ] `(py/initialize!)` executes without errors
- [ ] NumPy imports and basic operations work
- [ ] Data conversion between Python/Clojure tested
- [ ] Virtual environment configured (if needed)
- [ ] python.edn created (if using config file approach)

## 🔗 Related Skills

- [`cva-setup-clojure`](../cva-setup-clojure/SKILL.md) - Clojure project structure and dependency management
- [`cva-setup-vertex`](../cva-setup-vertex/SKILL.md) - Google Cloud authentication for Vertex AI
- [`cva-tools-python`](../cva-tools-python/SKILL.md) - Creating custom agent tools with Python libraries (if exists)
- [`cva-data-processing`](../cva-data-processing/SKILL.md) - NumPy/Pandas workflows for agent data (if exists)
- [`cva-ml-integration`](../cva-ml-integration/SKILL.md) - Integrating ML models into agents (if exists)

## 📘 Additional Documentation

### Performance Considerations

- **First Call Overhead**: Initial Python module import is slow; use `delay` or startup hooks
- **Data Conversion**: Large arrays convert efficiently; avoid repeated conversions
- **GIL Limitations**: Python GIL limits true parallelism; consider using Java alternatives for CPU-bound tasks
- **Memory Management**: Python objects are garbage collected separately; be mindful of memory usage

### Best Practices

1. **Initialize Once**: Call `py/initialize!` once at application startup
2. **Lazy Loading**: Use `delay` for expensive Python modules
3. **Type Hints**: Add type hints in docstrings for clarity
4. **Error Handling**: Wrap Python calls in try-catch for better error messages
5. **Virtual Environments**: Use venv for dependency isolation

### References

- [libpython-clj GitHub](https://github.com/clj-python/libpython-clj)
- [Official Documentation](https://clj-python.github.io/libpython-clj/)
- [Usage Guide](https://github.com/clj-python/libpython-clj/blob/master/topics/Usage.md)
- [Examples Repository](https://github.com/clj-python/libpython-clj-examples)
- [Data Conversion Deep Dive](https://clj-python.github.io/libpython-clj/DataConversion.html)
